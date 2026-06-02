"""LLM semantic extraction proposal gate for Product-Agent OS project graphs.

Batch 22 stages generated semantic node, edge, rationale and comment
proposals. The default implementation is local and deterministic: it records
an approved prompt/model policy but does not call live model APIs.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import time
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload
from product_agent_os.project_graph_index import graph_content_fingerprint
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text
from product_agent_os.project_graph_semantic import validate_semantic_retrieval_index


LLM_EXTRACTION_TARGET = ".codex/product-agent-os/project-code-graph-llm-proposals.json"
DEFAULT_MAX_PROMPT_TOKENS = 1_500
DEFAULT_MAX_OUTPUT_TOKENS = 1_500
DEFAULT_MAX_LATENCY_MS = 250
MAX_PROPOSALS = 20

_APPROVAL_FIELDS = {
    "explicit_approval",
    "storage_path",
    "extraction_schema",
    "prompt_model_policy",
    "redaction_policy",
    "cache_policy",
    "token_budget",
    "eval_threshold",
    "incident_path",
    "owner",
    "rollback_path",
}
_REVIEW_DECISIONS = {"accepted", "rejected", "accepted_gap", "incident_blocked"}


def validate_llm_extraction_approval(approval: dict[str, Any] | None) -> dict[str, Any]:
    """Validate explicit approval before staging LLM extraction proposals."""

    if not isinstance(approval, dict):
        return _validation(False, ["llm_extraction_approval:missing"], "llm_extraction_approval")
    errors: list[str] = []
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"llm_extraction_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("llm_extraction_approval:explicit_approval")
    if safe_relative_path_text(approval.get("storage_path") or "") != LLM_EXTRACTION_TARGET:
        errors.append("llm_extraction_approval:storage_path")

    schema = approval.get("extraction_schema") if isinstance(approval.get("extraction_schema"), dict) else {}
    for key in ["semantic_nodes", "semantic_edges", "rationale_comments", "review_required"]:
        if schema.get(key) is not True:
            errors.append(f"llm_extraction_approval:extraction_schema:{key}")

    model = approval.get("prompt_model_policy") if isinstance(approval.get("prompt_model_policy"), dict) else {}
    if model.get("provider") != "local_deterministic":
        errors.append("llm_extraction_approval:prompt_model_policy:provider")
    if model.get("external_model_calls_allowed") is not False:
        errors.append("llm_extraction_approval:prompt_model_policy:external_calls")
    if not model.get("model") or not model.get("version"):
        errors.append("llm_extraction_approval:prompt_model_policy:identity")
    if model.get("output_format") != "structured_json":
        errors.append("llm_extraction_approval:prompt_model_policy:output_format")
    approved_context = set(str(item) for item in model.get("approved_context", []) if isinstance(item, str))
    if not {"redacted_graph_artifact", "semantic_retrieval_index"}.issubset(approved_context):
        errors.append("llm_extraction_approval:prompt_model_policy:approved_context")

    redaction = approval.get("redaction_policy") if isinstance(approval.get("redaction_policy"), dict) else {}
    for key in [
        "raw_source_excluded",
        "private_comments_excluded",
        "secrets_redacted",
        "absolute_paths_redacted",
        "unsupported_claims_labelled",
    ]:
        if redaction.get(key) is not True:
            errors.append(f"llm_extraction_approval:redaction_policy:{key}")

    cache = approval.get("cache_policy") if isinstance(approval.get("cache_policy"), dict) else {}
    if cache.get("stale_policy") != "block_if_graph_or_semantic_fingerprint_mismatch":
        errors.append("llm_extraction_approval:cache_policy:stale_policy")
    if "semantic" not in str(cache.get("fingerprint_scope") or "") or "graph" not in str(cache.get("fingerprint_scope") or ""):
        errors.append("llm_extraction_approval:cache_policy:fingerprint_scope")

    token_budget = approval.get("token_budget") if isinstance(approval.get("token_budget"), dict) else {}
    if _positive_int(token_budget.get("max_prompt_tokens"), 0) <= 0:
        errors.append("llm_extraction_approval:token_budget:max_prompt_tokens")
    if _positive_int(token_budget.get("max_output_tokens"), 0) <= 0:
        errors.append("llm_extraction_approval:token_budget:max_output_tokens")
    if _positive_int(token_budget.get("max_cost_units"), -1) != 0:
        errors.append("llm_extraction_approval:token_budget:max_cost_units")

    thresholds = approval.get("eval_threshold") if isinstance(approval.get("eval_threshold"), dict) else {}
    for key in ["min_precision", "max_unsupported_claim_rate", "max_privacy_violations", "max_latency_ms"]:
        if key not in thresholds:
            errors.append(f"llm_extraction_approval:eval_threshold:{key}")
    if _positive_int(thresholds.get("max_latency_ms"), 0) <= 0:
        errors.append("llm_extraction_approval:eval_threshold:max_latency_ms")
    if "incident" not in str(approval.get("incident_path") or "").lower():
        errors.append("llm_extraction_approval:incident_path")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("llm_extraction_approval:owner")
    if approval.get("rollback_path") != f"delete {LLM_EXTRACTION_TARGET}":
        errors.append("llm_extraction_approval:rollback_path")
    return _validation(not errors, errors, "llm_extraction_approval")


def build_llm_extraction_proposals(
    graph: dict[str, Any],
    *,
    semantic_index: dict[str, Any] | None = None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build deterministic generated proposal artifacts from redacted graph context."""

    approval_validation = validate_llm_extraction_approval(approval)
    if approval_validation["ok"] is not True:
        return _approval_required_proposals(approval_validation)
    safe_graph = _redacted_dict(graph)
    validation_errors: list[str] = []
    semantic_fingerprint = ""
    if semantic_index is not None:
        semantic_validation = validate_semantic_retrieval_index(semantic_index)
        if semantic_validation.get("ok") is not True:
            validation_errors.append("semantic_index:invalid")
        if semantic_index.get("graph_fingerprint") != graph_content_fingerprint(safe_graph):
            validation_errors.append("semantic_index:stale")
        semantic_fingerprint = _fingerprint(semantic_index)
    if validation_errors:
        return _blocked_proposals(validation_errors, approval)

    model = approval.get("prompt_model_policy", {})
    thresholds = approval.get("eval_threshold", {})
    selected_nodes, blocked_records = _proposal_source_nodes(graph, safe_graph)
    semantic_node_proposals = [_semantic_node_proposal(node, index) for index, node in enumerate(selected_nodes[:MAX_PROPOSALS])]
    semantic_edge_proposals = _semantic_edge_proposals(safe_graph, selected_nodes)
    rationale_comment_proposals = [_rationale_comment_proposal(node, index) for index, node in enumerate(selected_nodes[:MAX_PROPOSALS])]
    proposals = {
        "schema_version": 1,
        "artifact_kind": "project_graph_llm_extraction_proposals",
        "write_policy": "read_only",
        "status": "ready",
        "source_boundary": "redacted_graph_and_semantic_index_artifacts_only_no_raw_source_or_private_comments",
        "generated_view_policy": "llm_extraction_proposals_are_generated_not_source_of_truth",
        "approval_boundary": "batch22_explicit_llm_semantic_extraction_gate",
        "graph_fingerprint": graph_content_fingerprint(safe_graph),
        "semantic_index_fingerprint": semantic_fingerprint,
        "cache_key": _cache_key(safe_graph, semantic_index, approval),
        "model_policy": {
            "provider": sanitize_graph_text(model.get("provider") or ""),
            "model": sanitize_graph_text(model.get("model") or ""),
            "version": sanitize_graph_text(model.get("version") or ""),
            "sampling": _redacted_dict(model.get("sampling", {}) if isinstance(model.get("sampling"), dict) else {}),
            "external_model_calls_allowed": False,
            "implementation_mode": "local_deterministic_proposal_engine",
        },
        "prompt_contract": {
            "approved_context": list(model.get("approved_context") or []),
            "output_format": "structured_json",
            "provenance_required": True,
            "uncertainty_required": True,
            "required_labels": ["unsupported_claim", "inferred_unverified", "private_input_blocked"],
            "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_comments"],
        },
        "cache_policy": {
            "cache_status": str(approval.get("cache_policy", {}).get("cache_status") or "generated"),
            "fingerprint_scope": "redacted_graph_semantic_index_prompt_policy",
            "stale_policy": "block_if_graph_or_semantic_fingerprint_mismatch",
            "storage_path": LLM_EXTRACTION_TARGET,
            "ttl_days": _positive_int(approval.get("cache_policy", {}).get("ttl_days"), 30),
        },
        "token_budget": {
            "max_prompt_tokens": _positive_int(approval.get("token_budget", {}).get("max_prompt_tokens"), DEFAULT_MAX_PROMPT_TOKENS),
            "max_output_tokens": _positive_int(approval.get("token_budget", {}).get("max_output_tokens"), DEFAULT_MAX_OUTPUT_TOKENS),
            "max_cost_units": 0,
            "actual_cost_units": 0,
        },
        "eval_policy": {
            "llm_extraction_eval_suite": True,
            "min_precision": _float_value(thresholds.get("min_precision"), 1.0),
            "max_unsupported_claim_rate": _float_value(thresholds.get("max_unsupported_claim_rate"), 0.0),
            "max_privacy_violations": _positive_int(thresholds.get("max_privacy_violations"), 0),
            "max_latency_ms": _positive_int(thresholds.get("max_latency_ms"), DEFAULT_MAX_LATENCY_MS),
        },
        "review_policy": {
            "owner": sanitize_graph_text(approval.get("owner") or ""),
            "human_review_required": True,
            "allowed_decisions": sorted(_REVIEW_DECISIONS),
            "canonical_graph_acceptance": "requires_owner_acceptance_outside_generated_proposal_artifact",
        },
        "incident_workflow": {
            "status": "armed",
            "incident_path": sanitize_graph_text(approval.get("incident_path") or ""),
            "disable_on_failed_eval_or_privacy_violation": True,
        },
        "rollback": {
            "disable_path": f"delete {LLM_EXTRACTION_TARGET}",
            "fallback": "semantic_retrieval_or_graph_only",
            "deletion_scope": "stage_root_generated_llm_proposals_only",
        },
        "canonical_graph_mutation": "forbidden",
        "semantic_node_proposals": semantic_node_proposals,
        "semantic_edge_proposals": semantic_edge_proposals,
        "rationale_comment_proposals": rationale_comment_proposals,
        "blocked_records": blocked_records,
        "review_ledger": [],
    }
    proposals["validation"] = validate_llm_extraction_proposals(proposals)
    return proposals


def validate_llm_extraction_proposals(proposals: dict[str, Any]) -> dict[str, Any]:
    """Validate proposal schema and source-boundary invariants."""

    errors: list[str] = []
    if proposals.get("schema_version") != 1:
        errors.append("schema_version")
    if proposals.get("artifact_kind") != "project_graph_llm_extraction_proposals":
        errors.append("artifact_kind")
    if proposals.get("write_policy") != "read_only":
        errors.append("write_policy")
    if proposals.get("source_boundary") != "redacted_graph_and_semantic_index_artifacts_only_no_raw_source_or_private_comments":
        errors.append("source_boundary")
    if proposals.get("generated_view_policy") != "llm_extraction_proposals_are_generated_not_source_of_truth":
        errors.append("generated_view_policy")
    if proposals.get("approval_boundary") != "batch22_explicit_llm_semantic_extraction_gate":
        errors.append("approval_boundary")
    if proposals.get("canonical_graph_mutation") != "forbidden":
        errors.append("canonical_graph_mutation")
    if proposals.get("model_policy", {}).get("external_model_calls_allowed") is not False:
        errors.append("model_policy:external_calls")
    for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals", "blocked_records", "review_ledger"]:
        if not isinstance(proposals.get(key), list):
            errors.append(key)
    for proposal in _all_proposal_records(proposals):
        if not isinstance(proposal, dict):
            errors.append("proposal:shape")
            continue
        if not proposal.get("proposal_id") or not proposal.get("source_observation_ids"):
            errors.append("proposal:provenance")
        if proposal.get("confidence") != "inferred_unverified":
            errors.append("proposal:confidence")
        if proposal.get("review_status") not in {"proposed", *_REVIEW_DECISIONS}:
            errors.append("proposal:review_status")
    if _has_unsafe_text(proposals):
        errors.append("source_boundary:unsafe_text")
    return _validation(not errors, errors, "llm_extraction_proposals")


def stage_llm_extraction_proposals(
    graph_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    semantic_index_artifact: str | Path | None = None,
) -> dict[str, Any]:
    """Stage or reuse generated LLM extraction proposals under an explicit stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    approval_validation = validate_llm_extraction_approval(approval)
    if approval_validation["ok"] is not True:
        return _stage_result("approval_required", "blocked", approval_validation, action="blocked")
    graph = load_graph_artifact(graph_artifact)
    semantic_index = _load_optional_json(semantic_index_artifact) if semantic_index_artifact else None
    safe_graph = _redacted_dict(graph)
    cache_key = _cache_key(safe_graph, semantic_index, approval)
    target = stage_path / LLM_EXTRACTION_TARGET
    previous = _load_existing_proposals(target)
    if previous and previous.get("cache_key") == cache_key and previous.get("validation", {}).get("ok") is True:
        return _stage_result("ready", "hit", previous["validation"], action="leave_unchanged")
    cache_status = "miss_invalidated" if previous else "miss"
    if previous:
        _backup_existing(target, target.with_name("project-code-graph-llm-proposals.previous.json"))
    proposals = build_llm_extraction_proposals(graph, semantic_index=semantic_index, approval=approval)
    if proposals.get("validation", {}).get("ok") is not True:
        return _stage_result("blocked", cache_status, proposals["validation"], action="blocked")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(proposals, indent=2, sort_keys=True), encoding="utf-8")
    return _stage_result("ready", cache_status, proposals["validation"], action="create")


def load_llm_extraction_proposals(path: str | Path) -> dict[str, Any]:
    """Load generated LLM extraction proposals without reading workspace source files."""

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("LLM extraction proposals must be a JSON object")
    return payload


def disable_llm_extraction_proposals(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable LLM extraction proposals by deleting only the stage-root artifact."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    target = stage_path / LLM_EXTRACTION_TARGET
    if target.exists() and target.is_file():
        target.unlink()
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-llm-proposals",
            "root_status": "redacted",
            "fallback": "semantic_retrieval_or_graph_only",
            "files": [
                {
                    "target_path": LLM_EXTRACTION_TARGET,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": LLM_EXTRACTION_TARGET,
                }
            ],
            "rollback": {"disable_path": f"delete {LLM_EXTRACTION_TARGET}"},
        }
    }


def apply_llm_proposal_review(
    proposals: dict[str, Any],
    *,
    proposal_id: str,
    decision: str,
    owner: str,
    rationale: str,
) -> dict[str, Any]:
    """Record a staged owner review decision without mutating canonical graph facts."""

    if decision not in _REVIEW_DECISIONS:
        raise ValueError("unsupported proposal review decision")
    updated = json.loads(json.dumps(proposals))
    safe_owner = sanitize_graph_text(owner)
    safe_rationale = _safe_review_text(rationale)
    for proposal in _all_proposal_records(updated):
        if proposal.get("proposal_id") == proposal_id:
            proposal["review_status"] = decision
    updated.setdefault("review_ledger", []).append(
        {
            "proposal_id": sanitize_graph_text(proposal_id),
            "decision": decision,
            "owner": safe_owner,
            "rationale": safe_rationale,
            "canonical_graph_mutation": "forbidden",
        }
    )
    updated["canonical_graph_mutation"] = "forbidden"
    updated["validation"] = validate_llm_extraction_proposals(updated)
    return updated


def evaluate_llm_extraction_proposals(
    proposals: dict[str, Any],
    *,
    cases: list[dict[str, Any]],
    thresholds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate proposal quality, privacy and unsupported-claim thresholds."""

    started = time.perf_counter()
    applied = {**_default_thresholds(proposals), **(thresholds or {})}
    validation = validate_llm_extraction_proposals(proposals)
    proposal_records = _all_proposal_records(proposals)
    unsupported = _unsupported_claim_count(proposals)
    privacy_violations = 1 if _has_unsafe_text(proposals) else 0
    evaluated_cases = []
    for case in cases:
        expected_kinds = set(str(item) for item in case.get("expected_proposal_kinds", []) if item)
        expected_sources = set(str(item) for item in case.get("expected_source_node_ids", []) if item)
        matching_kinds = {str(record.get("proposal_kind")) for record in proposal_records}
        matching_sources = {str(record.get("source_node_id")) for record in proposal_records}
        kind_ok = expected_kinds.issubset(matching_kinds)
        source_ok = not expected_sources or expected_sources.issubset(matching_sources)
        evaluated_cases.append(
            {
                "id": sanitize_graph_text(case.get("id") or "llm-extraction-case")[:80],
                "status": "passed" if kind_ok and source_ok else "failed",
                "kind_ok": kind_ok,
                "source_ok": source_ok,
            }
        )
    precision = 1.0 if evaluated_cases and all(case["status"] == "passed" for case in evaluated_cases) else 0.0
    unsupported_rate = 0.0 if not proposal_records else round(unsupported / len(proposal_records), 4)
    latency_ms = round((time.perf_counter() - started) * 1000, 3)
    metrics = {
        "precision": precision,
        "unsupported_claim_rate": unsupported_rate,
        "privacy_violations": privacy_violations,
        "cost_units": 0,
        "latency_ms": latency_ms,
    }
    failed = []
    if validation.get("ok") is not True:
        failed.append("proposal_validation_failed")
    if metrics["precision"] < _float_value(applied.get("min_precision"), 1.0):
        failed.append("precision_below_threshold")
    if metrics["unsupported_claim_rate"] > _float_value(applied.get("max_unsupported_claim_rate"), 0.0):
        failed.append("unsupported_claim_rate_above_threshold")
    if metrics["privacy_violations"] > _positive_int(applied.get("max_privacy_violations"), 0):
        failed.append("privacy_violations_above_threshold")
    if metrics["cost_units"] > _positive_int(applied.get("max_cost_units"), 0):
        failed.append("cost_units_above_threshold")
    if metrics["latency_ms"] > _positive_int(applied.get("max_latency_ms"), DEFAULT_MAX_LATENCY_MS):
        failed.append("latency_ms_above_threshold")
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": "passed" if evaluated_cases and not failed else "blocked",
        "approval_boundary": "batch22_explicit_llm_semantic_extraction_gate",
        "quality_metrics": metrics,
        "thresholds": applied,
        "failed_thresholds": failed,
        "cases": evaluated_cases,
        "incident_workflow": {
            "status": "disabled_until_fixed" if failed else "armed",
            "reason": failed,
        },
        "rollback": proposals.get("rollback", {"disable_path": f"delete {LLM_EXTRACTION_TARGET}"}),
        "safe_next_action": "Treat generated semantics as staged proposals, not canonical graph facts.",
    }


def _approval_required_proposals(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_llm_extraction_proposals",
        "write_policy": "read_only",
        "status": "approval_required",
        "source_boundary": "redacted_graph_and_semantic_index_artifacts_only_no_raw_source_or_private_comments",
        "approval_boundary": "batch22_explicit_llm_semantic_extraction_gate",
        "canonical_graph_mutation": "forbidden",
        "rollback": {"disable_path": f"delete {LLM_EXTRACTION_TARGET}", "fallback": "semantic_retrieval_or_graph_only"},
        "validation": validation,
    }


def _blocked_proposals(errors: list[str], approval: dict[str, Any]) -> dict[str, Any]:
    return {
        **_approval_required_proposals(_validation(False, errors, "llm_extraction_proposals")),
        "status": "blocked",
        "review_policy": {"owner": sanitize_graph_text(approval.get("owner") or "")},
    }


def _proposal_source_nodes(original_graph: dict[str, Any], safe_graph: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    original_by_id = {
        str(node.get("id") or ""): node
        for node in original_graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    selected: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []
    for node in safe_graph.get("nodes", []):
        if not isinstance(node, dict) or not node.get("id"):
            continue
        node_id = str(node.get("id") or "")
        if _node_has_private_input(original_by_id.get(node_id, node)):
            blocked.append(
                {
                    "record_id": _proposal_id("blocked", node_id),
                    "node_id": _safe_review_text(node_id),
                    "reason": "private_or_secret_like_input",
                    "redaction_status": "blocked",
                }
            )
            continue
        node_type = str(node.get("type") or "")
        path = str(node.get("path") or "")
        if node_type in {"function", "method", "class", "module"} and not path.startswith("tests/"):
            selected.append(_safe_node(node))
    return sorted(selected, key=lambda item: str(item.get("id") or "")), blocked


def _semantic_node_proposal(node: dict[str, Any], index: int) -> dict[str, Any]:
    node_id = _safe_review_text(node.get("id") or "")
    return {
        "proposal_id": _proposal_id("semantic-node", node_id),
        "proposal_kind": "semantic_node",
        "source_node_id": node_id,
        "source_observation_ids": _observation_ids(node),
        "label": _safe_review_text(node.get("label") or node_id)[:120],
        "rationale": f"Generated proposal from redacted graph evidence for {node_id}.",
        "uncertainty": "requires_owner_review",
        "confidence": "inferred_unverified",
        "truth_status": "unverified_inference",
        "review_status": "proposed",
        "redaction_status": "redacted",
        "unsupported_claim_labels": [],
        "rank": index + 1,
    }


def _semantic_edge_proposals(graph: dict[str, Any], selected_nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected_ids = {str(node.get("id") or "") for node in selected_nodes}
    proposals: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = _safe_review_text(edge.get("source") or "")
        target = _safe_review_text(edge.get("target") or "")
        if source not in selected_ids and target not in selected_ids:
            continue
        proposals.append(
            {
                "proposal_id": _proposal_id("semantic-edge", f"{source}->{target}"),
                "proposal_kind": "semantic_edge",
                "source_node_id": source,
                "target_node_id": target,
                "source_observation_ids": [_safe_review_text(item) for item in edge.get("observation_ids", []) if item][:5]
                or ["obs:generated-proposal"],
                "rationale": "Generated semantic relationship proposal from existing graph edge evidence.",
                "uncertainty": "requires_owner_review",
                "confidence": "inferred_unverified",
                "truth_status": "unverified_inference",
                "review_status": "proposed",
                "redaction_status": "redacted",
                "unsupported_claim_labels": [],
            }
        )
        if len(proposals) >= MAX_PROPOSALS:
            break
    if proposals or len(selected_nodes) < 2:
        return proposals
    source = _safe_review_text(selected_nodes[0].get("id") or "")
    target = _safe_review_text(selected_nodes[1].get("id") or "")
    return [
        {
            "proposal_id": _proposal_id("semantic-edge", f"{source}->{target}"),
            "proposal_kind": "semantic_edge",
            "source_node_id": source,
            "target_node_id": target,
            "source_observation_ids": _observation_ids(selected_nodes[0]),
            "rationale": "Generated adjacency proposal from redacted graph co-occurrence.",
            "uncertainty": "requires_owner_review",
            "confidence": "inferred_unverified",
            "truth_status": "unverified_inference",
            "review_status": "proposed",
            "redaction_status": "redacted",
            "unsupported_claim_labels": [],
        }
    ]


def _rationale_comment_proposal(node: dict[str, Any], index: int) -> dict[str, Any]:
    node_id = _safe_review_text(node.get("id") or "")
    return {
        "proposal_id": _proposal_id("rationale-comment", node_id),
        "proposal_kind": "rationale_comment",
        "source_node_id": node_id,
        "source_observation_ids": _observation_ids(node),
        "summary": f"Generated rationale/comment proposal for {node_id}; verify against source before use.",
        "source_boundary": "approved_redacted_spans_only",
        "uncertainty": "requires_owner_review",
        "confidence": "inferred_unverified",
        "truth_status": "unverified_inference",
        "review_status": "proposed",
        "redaction_status": "redacted",
        "unsupported_claim_labels": [],
        "rank": index + 1,
    }


def _safe_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": _safe_review_text(node.get("id") or ""),
        "type": _safe_review_text(node.get("type") or ""),
        "label": _safe_review_text(node.get("label") or ""),
        "path": safe_relative_path_text(node.get("path") or ""),
        "observation_ids": _observation_ids(node),
    }


def _observation_ids(node: dict[str, Any]) -> list[str]:
    values = [_safe_review_text(item) for item in node.get("observation_ids", []) if item]
    return values[:5] or ["obs:generated-proposal"]


def _all_proposal_records(proposals: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
        records.extend(item for item in proposals.get(key, []) if isinstance(item, dict))
    return records


def _unsupported_claim_count(proposals: dict[str, Any]) -> int:
    count = 0
    for record in _all_proposal_records(proposals):
        labels = set(str(item) for item in record.get("unsupported_claim_labels", []) if item)
        text = json.dumps(record, sort_keys=True).lower()
        if labels or "source of truth" in text or "canonical graph fact" in text:
            count += 1
    return count


def _default_thresholds(proposals: dict[str, Any]) -> dict[str, Any]:
    policy = proposals.get("eval_policy", {}) if isinstance(proposals.get("eval_policy"), dict) else {}
    return {
        "min_precision": _float_value(policy.get("min_precision"), 1.0),
        "max_unsupported_claim_rate": _float_value(policy.get("max_unsupported_claim_rate"), 0.0),
        "max_privacy_violations": _positive_int(policy.get("max_privacy_violations"), 0),
        "max_cost_units": 0,
        "max_latency_ms": _positive_int(policy.get("max_latency_ms"), DEFAULT_MAX_LATENCY_MS),
    }


def _stage_result(status: str, cache_status: str, validation: dict[str, Any], *, action: str) -> dict[str, Any]:
    return {
        "rendered_artifacts": {
            "status": status,
            "mode": "build-llm-proposals",
            "root_status": "redacted",
            "cache_status": cache_status,
            "source_boundary": "redacted_graph_and_semantic_index_artifacts_only_no_raw_source_or_private_comments",
            "fallback": "semantic_retrieval_or_graph_only",
            "rollback": {"disable_path": f"delete {LLM_EXTRACTION_TARGET}"},
            "files": [
                {
                    "target_path": LLM_EXTRACTION_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action in {"create", "leave_unchanged"} else "blocked",
                    "staged_path": LLM_EXTRACTION_TARGET,
                }
            ],
            "validation": validation,
        }
    }


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _load_existing_proposals(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return load_llm_extraction_proposals(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def _load_optional_json(path: str | Path | None) -> dict[str, Any] | None:
    if not path:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _backup_existing(target: Path, backup_target: Path) -> None:
    if not target.exists() or not target.is_file():
        return
    backup_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, backup_target)


def _cache_key(graph: dict[str, Any], semantic_index: dict[str, Any] | None, approval: dict[str, Any]) -> str:
    payload = {
        "graph_fingerprint": graph_content_fingerprint(graph),
        "semantic_index_fingerprint": _fingerprint(semantic_index) if isinstance(semantic_index, dict) else "",
        "prompt_model_policy": approval.get("prompt_model_policy", {}),
        "extraction_schema": approval.get("extraction_schema", {}),
    }
    return _fingerprint(payload)


def _fingerprint(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _proposal_id(kind: str, seed: str) -> str:
    return f"{kind}:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


def _node_has_private_input(node: dict[str, Any]) -> bool:
    return _has_unsafe_text(node) or "comment says" in json.dumps(node, sort_keys=True).lower()


def _has_unsafe_text(value: Any) -> bool:
    serialized = json.dumps(value, sort_keys=True).lower()
    forbidden = ["fixture-secret", "http://", "https://", "c:\\users\\", "/users/", "/home/", "/tmp/"]
    return any(item in serialized for item in forbidden)


def _safe_review_text(value: Any) -> str:
    text = sanitize_graph_text(value)
    text = re.sub(
        r"(?i)\b(token|secret|password|api[_-]?key|private[_-]?key)\s*=\s*[^\s\"'<>]+",
        "[REDACTED_SECRET]",
        text,
    )
    text = re.sub(r"(?i)fixture-secret", "[REDACTED_SECRET]", text)
    return text


def _float_value(value: Any, default: float) -> float:
    if value is None:
        return default
    return float(value)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _validation(ok: bool, errors: list[str], check: str) -> dict[str, Any]:
    return {"ok": ok, "checks": [check], "errors": sorted(set(errors))}
