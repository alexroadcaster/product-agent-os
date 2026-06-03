"""Live LLM proposal provider gate for Product-Agent OS project graphs.

Batch 28 defines an approval-bound external LLM proposal adapter contract and
safety eval gate. It never calls external providers by itself and never turns
provider output into canonical graph facts.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_index import graph_content_fingerprint
from product_agent_os.project_graph_live_governance import validate_live_governance_packet
from product_agent_os.project_graph_llm_extraction import (
    load_llm_extraction_proposals,
    validate_llm_extraction_proposals,
)
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text
from product_agent_os.project_graph_semantic import (
    load_semantic_retrieval_index,
    validate_semantic_retrieval_index,
)


LLM_PROPOSAL_PROVIDER_TARGET = ".codex/product-agent-os/project-code-graph-llm-proposal-provider.json"
LLM_PROPOSAL_EVAL_TARGET = ".codex/product-agent-os/project-code-graph-llm-proposal-eval.json"
_APPROVAL_FIELDS = {
    "explicit_approval",
    "owner",
    "allowed_surfaces",
    "provider",
    "data_classification",
    "redaction_policy",
    "cache_policy",
    "budget_policy",
    "eval_threshold",
    "failure_handling",
    "rollback_path",
    "incident_path",
    "residual_risks",
}
_BATCH28_ALLOWED_SURFACES = {"external_llm_proposal_adapter", "llm_proposal_safety_eval"}
_FORBIDDEN_INPUTS = {"raw_source_bodies", "secrets", "absolute_local_paths"}
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_SECRET_FIELD_NAMES = {
    "access_token",
    "api_key",
    "apikey",
    "client_secret",
    "credential",
    "credential_value",
    "key",
    "password",
    "private_key",
    "refresh_token",
    "secret",
    "secret_value",
    "token",
}
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)


def validate_llm_proposal_provider_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 28 LLM proposal provider approval."""

    if not isinstance(approval, dict):
        return _validation(False, ["llm_proposal_provider_approval:missing"], "llm_proposal_provider_approval")
    errors: list[str] = []
    missing = sorted(field for field in _APPROVAL_FIELDS if field not in approval)
    errors.extend(f"llm_proposal_provider_approval:{field}:missing" for field in missing)
    if approval.get("explicit_approval") is not True:
        errors.append("llm_proposal_provider_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("llm_proposal_provider_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH28_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"llm_proposal_provider_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH28_ALLOWED_SURFACES):
        errors.append(f"llm_proposal_provider_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_provider_policy(approval.get("provider")))
    errors.extend(_validate_data_classification(approval.get("data_classification")))
    errors.extend(_validate_redaction_policy(approval.get("redaction_policy")))
    errors.extend(_validate_cache_policy(approval.get("cache_policy")))
    errors.extend(_validate_budget_policy(approval.get("budget_policy")))
    errors.extend(_validate_eval_threshold(approval.get("eval_threshold")))
    errors.extend(_validate_failure_handling(approval.get("failure_handling")))
    if approval.get("rollback_path") != f"delete {LLM_PROPOSAL_PROVIDER_TARGET}":
        errors.append("llm_proposal_provider_approval:rollback_path")
    if "incident" not in str(approval.get("incident_path") or "").lower():
        errors.append("llm_proposal_provider_approval:incident_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("llm_proposal_provider_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("llm_proposal_provider_approval:unsafe_text")
    return _validation(not errors, errors, "llm_proposal_provider_approval")


def build_llm_proposal_provider_gate(
    graph: dict[str, Any],
    *,
    semantic_index: dict[str, Any] | None,
    local_proposals: dict[str, Any] | None,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a source-free Batch 28 external LLM proposal provider gate."""

    approval_validation = validate_llm_proposal_provider_approval(approval, governance_packet)
    semantic_validation = (
        validate_semantic_retrieval_index(semantic_index)
        if isinstance(semantic_index, dict)
        else _validation(False, ["semantic_index:missing"], "semantic_retrieval_index")
    )
    proposal_validation = (
        validate_llm_extraction_proposals(local_proposals)
        if isinstance(local_proposals, dict)
        else _validation(False, ["local_llm_proposals:missing"], "llm_extraction_proposals")
    )
    validation = _merge_validation(approval_validation, semantic_validation, proposal_validation)
    if validation["ok"] is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_live_llm_proposal_provider_gate",
            "status": "approval_required",
            "write_policy": "read_only",
            "approval_boundary": "batch28_live_llm_proposal_adapter_and_safety_eval",
            "provider_enabled": False,
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "validation": validation,
            "safe_next_action": "Provide Batch 28 approval, governance, semantic index and local proposal evidence.",
        }
    approval = approval if isinstance(approval, dict) else {}
    provider = approval.get("provider") if isinstance(approval.get("provider"), dict) else {}
    gate = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_llm_proposal_provider_gate",
        "status": "ready",
        "write_policy": "read_only",
        "approval_boundary": "batch28_live_llm_proposal_adapter_and_safety_eval",
        "source_boundary": "redacted_prompt_schema_and_evidence_ids_only_no_raw_source",
        "generated_view_policy": "llm_proposal_provider_gate_is_generated_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "allowed_surfaces": sorted(_BATCH28_ALLOWED_SURFACES),
        "blocked_surfaces": [
            "external_provider_call_without_runtime_invocation_approval",
            "secret_storage",
            "raw_source_payload",
            "canonical_graph_mutation",
            "accepted_without_human_review",
            "production_server",
            "git_action",
        ],
        "governance": {
            "artifact_kind": "project_graph_live_governance",
            "status": "ready",
            "approval_boundary": "batch24_live_governance_only_no_live_calls",
        },
        "provider_policy": {
            "provider": sanitize_graph_text(provider.get("provider") or ""),
            "model": sanitize_graph_text(provider.get("model") or ""),
            "credential_source": sanitize_graph_text(provider.get("credential_source") or ""),
            "credential_env_var": sanitize_graph_text(provider.get("credential_env_var") or ""),
            "secret_material_stored": False,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "provider_enabled": False,
            "provider_enabled_by_default": False,
        },
        "data_classification": _classification_packet(approval.get("data_classification")),
        "redaction_policy": _redaction_policy_packet(approval.get("redaction_policy")),
        "cache_policy": _cache_policy_packet(approval.get("cache_policy")),
        "budget_policy": _budget_policy_packet(approval.get("budget_policy")),
        "eval_policy": _eval_policy_packet(approval.get("eval_threshold")),
        "failure_handling": _failure_handling_packet(approval.get("failure_handling")),
        "prompt_contract": _prompt_contract(provider.get("prompt_policy")),
        "graph_fingerprint": graph_content_fingerprint(_redacted_dict(graph)),
        "semantic_index_fingerprint": _artifact_fingerprint(semantic_index or {}, record_key="corpus_records"),
        "local_proposals_fingerprint": _artifact_fingerprint(local_proposals or {}, record_key="semantic_node_proposals"),
        "provider_payload_contract": _provider_payload_contract(local_proposals or {}, provider.get("prompt_policy")),
        "incident_workflow": {
            "status": "armed",
            "incident_path": sanitize_graph_text(approval.get("incident_path") or ""),
            "disable_on_failed_eval_or_privacy_violation": True,
        },
        "canonical_graph_mutation": "forbidden",
        "accepted_for_canonical_graph": False,
        "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
        "rollback": {
            "disable_path": f"delete {LLM_PROPOSAL_PROVIDER_TARGET}",
            "delete_eval_path": f"delete {LLM_PROPOSAL_EVAL_TARGET}",
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "deletion_scope": "stage_root_generated_llm_proposal_provider_and_eval_only",
        },
        "residual_risks": [
            sanitize_graph_text(item)
            for item in approval.get("residual_risks", [])
            if isinstance(item, str)
        ][:10],
        "safe_next_action": (
            "Run Batch 28 safety eval with approved provider result evidence; keep output as proposals for "
            "human review and never as canonical graph facts."
        ),
    }
    safe_gate, report = redact_payload(gate)
    if isinstance(safe_gate, dict):
        safe_gate["redaction_summary"] = report
        safe_gate["validation"] = _merge_validation(validation, validate_llm_proposal_provider_gate(safe_gate))
        if safe_gate["validation"]["ok"] is not True:
            safe_gate["status"] = "blocked"
        return safe_gate
    gate["validation"] = validate_llm_proposal_provider_gate(gate)
    return gate


def validate_llm_proposal_provider_gate(gate: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 28 provider gate schema and safety invariants."""

    errors: list[str] = []
    if gate.get("schema_version") != 1:
        errors.append("schema_version")
    if gate.get("artifact_kind") != "project_graph_live_llm_proposal_provider_gate":
        errors.append("artifact_kind")
    if gate.get("write_policy") != "read_only":
        errors.append("write_policy")
    if gate.get("approval_boundary") != "batch28_live_llm_proposal_adapter_and_safety_eval":
        errors.append("approval_boundary")
    if gate.get("source_boundary") != "redacted_prompt_schema_and_evidence_ids_only_no_raw_source":
        errors.append("source_boundary")
    provider = gate.get("provider_policy") if isinstance(gate.get("provider_policy"), dict) else {}
    if provider.get("provider") != "external_llm":
        errors.append("provider_policy:provider")
    if provider.get("credential_source") != "environment":
        errors.append("provider_policy:credential_source")
    if provider.get("secret_material_stored") is not False:
        errors.append("provider_policy:secret_material")
    for field in ["provider_call_allowed", "external_call_performed", "provider_enabled_by_default"]:
        if provider.get(field) is not False:
            errors.append(f"provider_policy:{field}")
    prompt = gate.get("prompt_contract") if isinstance(gate.get("prompt_contract"), dict) else {}
    if prompt.get("output_format") != "structured_json":
        errors.append("prompt_contract:output_format")
    if prompt.get("proposal_only") is not True:
        errors.append("prompt_contract:proposal_only")
    if "unsupported_claim" not in prompt.get("required_labels", []):
        errors.append("prompt_contract:unsupported_claim_label")
    redaction = gate.get("redaction_policy") if isinstance(gate.get("redaction_policy"), dict) else {}
    for field in [
        "raw_source_excluded",
        "private_comments_excluded",
        "secrets_redacted",
        "absolute_paths_redacted",
        "unsupported_claims_labelled",
        "provider_payload_validation_required",
    ]:
        if redaction.get(field) is not True:
            errors.append(f"redaction_policy:{field}")
    cache = gate.get("cache_policy") if isinstance(gate.get("cache_policy"), dict) else {}
    if cache.get("storage_path") != LLM_PROPOSAL_PROVIDER_TARGET:
        errors.append("cache_policy:storage_path")
    if cache.get("cache_target") != LLM_PROPOSAL_EVAL_TARGET:
        errors.append("cache_policy:cache_target")
    if cache.get("deletion_proof_required") is not True:
        errors.append("cache_policy:deletion_proof")
    budget = gate.get("budget_policy") if isinstance(gate.get("budget_policy"), dict) else {}
    if _positive_int(budget.get("max_cost_units"), -1) != 0:
        errors.append("budget_policy:max_cost_units")
    payload_contract = gate.get("provider_payload_contract") if isinstance(gate.get("provider_payload_contract"), dict) else {}
    for field in ["raw_source_bodies_included", "absolute_local_paths_included", "secrets_included"]:
        if payload_contract.get(field) is not False:
            errors.append(f"provider_payload_contract:{field}")
    if gate.get("canonical_graph_mutation") != "forbidden":
        errors.append("canonical_graph_mutation")
    if gate.get("accepted_for_canonical_graph") is not False:
        errors.append("accepted_for_canonical_graph")
    if gate.get("fallback") != "local_llm_proposals_or_semantic_retrieval_or_graph_only":
        errors.append("fallback")
    if _has_unsafe_text(gate):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(gate, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, sorted(set(errors)), "llm_proposal_provider_gate")


def evaluate_llm_proposal_safety(
    gate: dict[str, Any],
    *,
    graph: dict[str, Any],
    semantic_index: dict[str, Any],
    cases: list[dict[str, Any]],
    provider_results: dict[str, dict[str, Any]] | None,
) -> dict[str, Any]:
    """Evaluate approved provider result evidence without calling a provider."""

    gate_validation = validate_llm_proposal_provider_gate(gate)
    thresholds = gate.get("eval_policy", {}) if isinstance(gate.get("eval_policy"), dict) else {}
    source_node_ids = {
        str(node.get("id"))
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id")
    }
    failed = [] if gate_validation.get("ok") is True else ["llm_proposal_provider_gate:invalid"]
    if not provider_results:
        failed.append("llm_proposal_eval:missing")
    evaluated: list[dict[str, Any]] = []
    totals = {
        "proposal_count": 0,
        "grounded_count": 0,
        "unsupported_count": 0,
        "privacy_violations": 0,
        "stale_context_results": 0,
        "mutation_attempts": 0,
        "max_query_ms": 0,
        "max_payload_tokens": 0,
    }
    for case in cases:
        if not isinstance(case, dict):
            continue
        case_id = sanitize_graph_text(case.get("id") or "llm-proposal-case")
        result = provider_results.get(case_id, {}) if isinstance(provider_results, dict) else {}
        proposals = result.get("proposals", []) if isinstance(result.get("proposals"), list) else []
        case_failed: list[str] = []
        if result.get("graph_fingerprint") != gate.get("graph_fingerprint"):
            totals["stale_context_results"] += 1
            case_failed.append("stale_context")
        query_ms = _positive_int(result.get("query_ms"), 0)
        payload_tokens = _positive_int(result.get("payload_tokens"), 0)
        totals["max_query_ms"] = max(totals["max_query_ms"], query_ms)
        totals["max_payload_tokens"] = max(totals["max_payload_tokens"], payload_tokens)
        expected_kinds = {str(item) for item in case.get("expected_proposal_kinds", []) if item}
        expected_sources = {str(item) for item in case.get("expected_source_node_ids", []) if item}
        found_kinds: set[str] = set()
        found_sources: set[str] = set()
        for proposal in proposals:
            if not isinstance(proposal, dict):
                case_failed.append("proposal_shape")
                continue
            totals["proposal_count"] += 1
            found_kinds.add(str(proposal.get("proposal_kind") or ""))
            source_id = str(proposal.get("source_node_id") or "")
            found_sources.add(source_id)
            if _proposal_is_grounded(proposal, source_node_ids):
                totals["grounded_count"] += 1
            else:
                case_failed.append("hallucinated_or_ungrounded_proposal")
            if proposal.get("unsupported_claim_labels"):
                totals["unsupported_count"] += 1
            if proposal.get("canonical_graph_mutation") != "forbidden":
                totals["mutation_attempts"] += 1
                case_failed.append("canonical_graph_mutation_attempt")
            if _has_unsafe_text(proposal):
                totals["privacy_violations"] += 1
                case_failed.append("privacy_violation")
        if expected_kinds and not expected_kinds.issubset(found_kinds):
            case_failed.append("missing_expected_proposal_kind")
        if expected_sources and not expected_sources.issubset(found_sources):
            case_failed.append("missing_expected_source")
        evaluated.append(
            {
                "id": case_id,
                "status": "passed" if not case_failed and proposals else "failed",
                "failed_checks": sorted(set(case_failed)),
                "proposal_count": len(proposals),
            }
        )
    if provider_results:
        failed.extend(_threshold_failures(totals, thresholds))
    failed = sorted(set(failed))
    if "llm_proposal_eval:missing" in failed:
        decision = "disabled_fallback"
    elif any(
        item in failed
        for item in [
            "privacy_violation",
            "hallucinated_or_ungrounded_proposal",
            "stale_context",
            "canonical_graph_mutation_attempt",
        ]
    ):
        decision = "incident_blocked"
    else:
        decision = "passed" if not failed and evaluated else "blocked"
    return _redacted_dict(
        {
            "schema_version": 1,
            "artifact_kind": "project_graph_llm_proposal_safety_eval",
            "write_policy": "read_only",
            "decision_status": decision,
            "approval_boundary": gate.get("approval_boundary"),
            "source_boundary": gate.get("source_boundary"),
            "provider_enabled": False,
            "provider_enabled_by_default": False,
            "external_call_performed": False,
            "accepted_for_canonical_graph": False,
            "canonical_graph_mutation": "forbidden",
            "quality_metrics": _quality_metrics(totals),
            "thresholds": thresholds,
            "failed_thresholds": failed,
            "cases": evaluated,
            "incident_workflow": {
                "status": "active" if decision == "incident_blocked" else "armed",
                "reason": failed,
            },
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "rollback": gate.get("rollback", {}),
            "safe_next_action": "Stage proposals for human review; never treat provider output as canonical fact.",
        }
    )


def stage_llm_proposal_provider_gate(
    graph_artifact: str | Path,
    semantic_index_artifact: str | Path,
    local_proposals_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage Batch 28 LLM provider gate and disabled safety-eval evidence."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    semantic_index = load_semantic_retrieval_index(semantic_index_artifact)
    local_proposals = load_llm_extraction_proposals(local_proposals_artifact)
    governance = _load_json_file(governance_artifact) if governance_artifact else None
    gate = build_llm_proposal_provider_gate(
        graph,
        semantic_index=semantic_index,
        local_proposals=local_proposals,
        approval=approval,
        governance_packet=governance,
    )
    eval_packet = evaluate_llm_proposal_safety(
        gate,
        graph=graph,
        semantic_index=semantic_index,
        cases=[],
        provider_results=None,
    )
    provider_target = stage_path / LLM_PROPOSAL_PROVIDER_TARGET
    eval_target = stage_path / LLM_PROPOSAL_EVAL_TARGET
    action = "blocked"
    if gate.get("status") == "ready" and gate.get("validation", {}).get("ok") is True:
        provider_target.parent.mkdir(parents=True, exist_ok=True)
        provider_target.write_text(json.dumps(gate, indent=2, sort_keys=True), encoding="utf-8")
        eval_target.write_text(json.dumps(eval_packet, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": gate.get("status"),
            "mode": "validate-llm-proposal-provider",
            "root_status": "redacted",
            "source_boundary": gate.get(
                "source_boundary",
                "redacted_prompt_schema_and_evidence_ids_only_no_raw_source",
            ),
            "provider_call_allowed": False,
            "provider_enabled_by_default": False,
            "accepted_for_canonical_graph": False,
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "files": [
                {
                    "target_path": LLM_PROPOSAL_PROVIDER_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": LLM_PROPOSAL_PROVIDER_TARGET,
                },
                {
                    "target_path": LLM_PROPOSAL_EVAL_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": LLM_PROPOSAL_EVAL_TARGET,
                },
            ],
            "rollback": {"disable_path": f"delete {LLM_PROPOSAL_PROVIDER_TARGET}"},
            "validation": gate.get("validation"),
        }
    }


def disable_llm_proposal_provider_gate(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable Batch 28 generated artifacts by deleting stage-root files."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    targets = [LLM_PROPOSAL_PROVIDER_TARGET, LLM_PROPOSAL_EVAL_TARGET]
    deleted: list[str] = []
    for relative in targets:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-llm-proposal-provider",
            "root_status": "redacted",
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "deletion_proof": {
                "targets_checked": targets,
                "deleted": deleted,
                "remaining": [relative for relative in targets if (stage_path / relative).exists()],
            },
            "files": [
                {
                    "target_path": relative,
                    "action": "delete_if_present",
                    "write_policy": "stage_generated_file_only",
                    "staged_path": relative,
                }
                for relative in targets
            ],
            "rollback": {"disable_path": f"delete {LLM_PROPOSAL_PROVIDER_TARGET}"},
        }
    }


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["llm_proposal_provider_approval:governance_packet:missing"]
    errors: list[str] = []
    if governance_packet.get("status") != "ready":
        errors.append("llm_proposal_provider_approval:governance_packet:not_ready")
    validation = validate_live_governance_packet(governance_packet)
    if validation.get("ok") is not True:
        errors.append("llm_proposal_provider_approval:governance_packet:invalid")
    provider_policy = governance_packet.get("provider_policy") if isinstance(governance_packet.get("provider_policy"), dict) else {}
    if provider_policy.get("requires_batch_specific_approval") is not True:
        errors.append("llm_proposal_provider_approval:governance_packet:batch_specific_approval")
    if "external_llm" not in provider_policy.get("approved_providers", []):
        errors.append("llm_proposal_provider_approval:governance_packet:external_llm")
    return errors


def _validate_provider_policy(provider: Any) -> list[str]:
    if not isinstance(provider, dict):
        return ["llm_proposal_provider_approval:provider"]
    errors: list[str] = []
    if provider.get("provider") != "external_llm":
        errors.append("llm_proposal_provider_approval:provider:provider")
    if not sanitize_graph_text(provider.get("model") or ""):
        errors.append("llm_proposal_provider_approval:provider:model")
    if provider.get("credential_source") != "environment":
        errors.append("llm_proposal_provider_approval:provider:credential_source")
    if not sanitize_graph_text(provider.get("credential_env_var") or ""):
        errors.append("llm_proposal_provider_approval:provider:credential_env_var")
    if provider.get("external_calls_allowed") is not False:
        errors.append("llm_proposal_provider_approval:provider:external_calls_allowed")
    if any(key in provider for key in ["credential_value", "api_key", "token"]):
        errors.append("llm_proposal_provider_approval:provider:stored_secret")
    prompt_policy = provider.get("prompt_policy") if isinstance(provider.get("prompt_policy"), dict) else {}
    if _positive_int(prompt_policy.get("max_prompt_tokens"), 0) <= 0:
        errors.append("llm_proposal_provider_approval:provider:max_prompt_tokens")
    if _positive_int(prompt_policy.get("max_output_tokens"), 0) <= 0:
        errors.append("llm_proposal_provider_approval:provider:max_output_tokens")
    return errors


def _validate_data_classification(classification: Any) -> list[str]:
    if not isinstance(classification, dict):
        return ["llm_proposal_provider_approval:data_classification"]
    allowed = set(str(item) for item in classification.get("allowed_inputs", []) if isinstance(item, str))
    forbidden = set(str(item) for item in classification.get("forbidden_inputs", []) if isinstance(item, str))
    errors = [
        f"llm_proposal_provider_approval:data_classification:{required}"
        for required in sorted(_FORBIDDEN_INPUTS - forbidden)
    ]
    if not allowed:
        errors.append("llm_proposal_provider_approval:data_classification:allowed_inputs")
    return errors


def _validate_redaction_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["llm_proposal_provider_approval:redaction_policy"]
    required = [
        "raw_source_excluded",
        "private_comments_excluded",
        "secrets_redacted",
        "absolute_paths_redacted",
        "unsupported_claims_labelled",
        "provider_payload_validation_required",
    ]
    return [
        f"llm_proposal_provider_approval:redaction_policy:{field}"
        for field in required
        if policy.get(field) is not True
    ]


def _validate_cache_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["llm_proposal_provider_approval:cache_policy"]
    errors: list[str] = []
    if safe_relative_path_text(policy.get("storage_path") or "") != LLM_PROPOSAL_PROVIDER_TARGET:
        errors.append("llm_proposal_provider_approval:cache_policy:storage_path")
    if safe_relative_path_text(policy.get("cache_target") or "") != LLM_PROPOSAL_EVAL_TARGET:
        errors.append("llm_proposal_provider_approval:cache_policy:cache_target")
    if policy.get("stale_policy") != "block_if_graph_or_semantic_or_local_proposal_or_policy_fingerprint_mismatch":
        errors.append("llm_proposal_provider_approval:cache_policy:stale_policy")
    if "graph" not in str(policy.get("fingerprint_scope") or ""):
        errors.append("llm_proposal_provider_approval:cache_policy:fingerprint_scope")
    if policy.get("deletion_proof_required") is not True:
        errors.append("llm_proposal_provider_approval:cache_policy:deletion_proof_required")
    if _positive_int(policy.get("ttl_days"), 0) <= 0:
        errors.append("llm_proposal_provider_approval:cache_policy:ttl_days")
    return errors


def _validate_budget_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["llm_proposal_provider_approval:budget_policy"]
    errors: list[str] = []
    for field in ["max_prompt_tokens", "max_output_tokens", "max_latency_ms"]:
        if _positive_int(policy.get(field), 0) <= 0:
            errors.append(f"llm_proposal_provider_approval:budget_policy:{field}")
    if _positive_int(policy.get("max_cost_units"), -1) != 0:
        errors.append("llm_proposal_provider_approval:budget_policy:max_cost_units")
    if "fallback" not in str(policy.get("on_exceed") or ""):
        errors.append("llm_proposal_provider_approval:budget_policy:on_exceed")
    return errors


def _validate_eval_threshold(thresholds: Any) -> list[str]:
    if not isinstance(thresholds, dict):
        return ["llm_proposal_provider_approval:eval_threshold"]
    required = {
        "min_grounded_proposal_rate",
        "max_unsupported_claim_rate",
        "max_privacy_violations",
        "max_stale_context_results",
        "max_query_ms",
        "max_payload_tokens",
    }
    errors = [f"llm_proposal_provider_approval:eval_threshold:{field}" for field in sorted(required - set(thresholds))]
    if _positive_int(thresholds.get("max_query_ms"), 0) <= 0:
        errors.append("llm_proposal_provider_approval:eval_threshold:max_query_ms")
    if _positive_int(thresholds.get("max_payload_tokens"), 0) <= 0:
        errors.append("llm_proposal_provider_approval:eval_threshold:max_payload_tokens")
    return errors


def _validate_failure_handling(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["llm_proposal_provider_approval:failure_handling"]
    errors: list[str] = []
    for field in ["on_missing_provider_eval", "on_failed_eval"]:
        if "fallback" not in str(policy.get(field) or "") and "incident" not in str(policy.get(field) or ""):
            errors.append(f"llm_proposal_provider_approval:failure_handling:{field}")
    return errors


def _classification_packet(classification: Any) -> dict[str, Any]:
    source = classification if isinstance(classification, dict) else {}
    return {
        "allowed_inputs": _safe_string_list(source.get("allowed_inputs")),
        "forbidden_inputs": _safe_string_list(source.get("forbidden_inputs")),
    }


def _redaction_policy_packet(policy: Any) -> dict[str, Any]:
    source = policy if isinstance(policy, dict) else {}
    return {
        "raw_source_excluded": source.get("raw_source_excluded") is True,
        "private_comments_excluded": source.get("private_comments_excluded") is True,
        "secrets_redacted": source.get("secrets_redacted") is True,
        "absolute_paths_redacted": source.get("absolute_paths_redacted") is True,
        "unsupported_claims_labelled": source.get("unsupported_claims_labelled") is True,
        "provider_payload_validation_required": source.get("provider_payload_validation_required") is True,
    }


def _cache_policy_packet(policy: Any) -> dict[str, Any]:
    source = policy if isinstance(policy, dict) else {}
    return {
        "storage_path": LLM_PROPOSAL_PROVIDER_TARGET,
        "cache_target": LLM_PROPOSAL_EVAL_TARGET,
        "fingerprint_scope": sanitize_graph_text(source.get("fingerprint_scope") or ""),
        "stale_policy": sanitize_graph_text(source.get("stale_policy") or ""),
        "ttl_days": _positive_int(source.get("ttl_days"), 7),
        "deletion_proof_required": source.get("deletion_proof_required") is True,
    }


def _budget_policy_packet(policy: Any) -> dict[str, Any]:
    source = policy if isinstance(policy, dict) else {}
    return {
        "max_prompt_tokens": _positive_int(source.get("max_prompt_tokens"), 0),
        "max_output_tokens": _positive_int(source.get("max_output_tokens"), 0),
        "max_cost_units": _positive_int(source.get("max_cost_units"), 0),
        "max_latency_ms": _positive_int(source.get("max_latency_ms"), 0),
        "on_exceed": sanitize_graph_text(source.get("on_exceed") or ""),
    }


def _eval_policy_packet(thresholds: Any) -> dict[str, Any]:
    source = thresholds if isinstance(thresholds, dict) else {}
    return {
        "llm_proposal_safety_eval": True,
        "min_grounded_proposal_rate": _float_value(source.get("min_grounded_proposal_rate"), 1.0),
        "max_unsupported_claim_rate": _float_value(source.get("max_unsupported_claim_rate"), 0.0),
        "max_privacy_violations": _positive_int(source.get("max_privacy_violations"), 0),
        "max_stale_context_results": _positive_int(source.get("max_stale_context_results"), 0),
        "max_query_ms": _positive_int(source.get("max_query_ms"), 250),
        "max_payload_tokens": _positive_int(source.get("max_payload_tokens"), 1200),
    }


def _failure_handling_packet(policy: Any) -> dict[str, Any]:
    source = policy if isinstance(policy, dict) else {}
    return {
        "on_missing_provider_eval": sanitize_graph_text(
            source.get("on_missing_provider_eval") or "disabled_fallback_to_local_proposals_or_graph"
        ),
        "on_failed_eval": sanitize_graph_text(source.get("on_failed_eval") or "incident_blocked_and_fallback"),
    }


def _prompt_contract(prompt_policy: Any) -> dict[str, Any]:
    source = prompt_policy if isinstance(prompt_policy, dict) else {}
    return {
        "approved_context": ["redacted_graph_artifact", "semantic_retrieval_index", "local_llm_proposals"],
        "output_format": "structured_json",
        "proposal_only": True,
        "provenance_required": True,
        "uncertainty_required": True,
        "required_labels": ["unsupported_claim", "inferred_unverified", "private_input_blocked"],
        "required_schema": ["semantic_node", "semantic_edge", "rationale_comment"],
        "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_comments"],
        "max_prompt_tokens": _positive_int(source.get("max_prompt_tokens"), 1200),
        "max_output_tokens": _positive_int(source.get("max_output_tokens"), 1200),
    }


def _provider_payload_contract(local_proposals: dict[str, Any], prompt_policy: Any) -> dict[str, Any]:
    proposal_ids = []
    for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
        for proposal in local_proposals.get(key, []) if isinstance(local_proposals.get(key), list) else []:
            if isinstance(proposal, dict) and proposal.get("proposal_id"):
                proposal_ids.append(sanitize_graph_text(proposal.get("proposal_id")))
    return {
        "payload_shape": "redacted_prompt_schema_evidence_ids_only",
        "raw_source_bodies_included": False,
        "absolute_local_paths_included": False,
        "secrets_included": False,
        "proposal_ids": proposal_ids[:50],
        "max_prompt_tokens": _prompt_contract(prompt_policy).get("max_prompt_tokens"),
        "schema_validation_required_before_acceptance": True,
    }


def _threshold_failures(totals: dict[str, Any], thresholds: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    metrics = _quality_metrics(totals)
    if metrics["grounded_proposal_rate"] < _float_value(thresholds.get("min_grounded_proposal_rate"), 1.0):
        failures.append("hallucinated_or_ungrounded_proposal")
    if metrics["unsupported_claim_rate"] > _float_value(thresholds.get("max_unsupported_claim_rate"), 0.0):
        failures.append("unsupported_claim_rate_above_threshold")
    if metrics["privacy_violations"] > _positive_int(thresholds.get("max_privacy_violations"), 0):
        failures.append("privacy_violation")
    if metrics["stale_context_results"] > _positive_int(thresholds.get("max_stale_context_results"), 0):
        failures.append("stale_context")
    if totals["mutation_attempts"] > 0:
        failures.append("canonical_graph_mutation_attempt")
    if totals["max_query_ms"] > _positive_int(thresholds.get("max_query_ms"), 250):
        failures.append("latency_ms_above_threshold")
    if totals["max_payload_tokens"] > _positive_int(thresholds.get("max_payload_tokens"), 1200):
        failures.append("payload_tokens_above_threshold")
    return failures


def _quality_metrics(totals: dict[str, Any]) -> dict[str, Any]:
    proposal_count = _positive_int(totals.get("proposal_count"), 0)
    grounded_count = _positive_int(totals.get("grounded_count"), 0)
    unsupported_count = _positive_int(totals.get("unsupported_count"), 0)
    return {
        "proposal_count": proposal_count,
        "grounded_proposal_rate": round(grounded_count / proposal_count, 4) if proposal_count else 0.0,
        "unsupported_claim_rate": round(unsupported_count / proposal_count, 4) if proposal_count else 0.0,
        "privacy_violations": _positive_int(totals.get("privacy_violations"), 0),
        "stale_context_results": _positive_int(totals.get("stale_context_results"), 0),
        "canonical_graph_mutation_attempts": _positive_int(totals.get("mutation_attempts"), 0),
        "cost_units": 0,
        "max_query_ms": _positive_int(totals.get("max_query_ms"), 0),
        "max_payload_tokens": _positive_int(totals.get("max_payload_tokens"), 0),
    }


def _proposal_is_grounded(proposal: dict[str, Any], source_node_ids: set[str]) -> bool:
    source_id = str(proposal.get("source_node_id") or "")
    observations = proposal.get("source_observation_ids")
    return source_id in source_node_ids and isinstance(observations, list) and bool(observations)


def _artifact_fingerprint(artifact: dict[str, Any], *, record_key: str) -> str:
    payload = {
        "schema_version": artifact.get("schema_version"),
        "artifact_kind": artifact.get("artifact_kind"),
        "record_key": record_key,
        "records": artifact.get(record_key, []),
        "graph_fingerprint": artifact.get("graph_fingerprint"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _safe_string_list(value: Any) -> list[str]:
    return [sanitize_graph_text(item) for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _redacted_dict(payload: Any) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else {}


def _has_unsafe_text(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in _SECRET_FIELD_NAMES:
                return True
            if _has_unsafe_text(item):
                return True
        return False
    if isinstance(value, list):
        return any(_has_unsafe_text(item) for item in value)
    if isinstance(value, str):
        return bool(
            _WINDOWS_PATH_PATTERN.search(value)
            or _POSIX_PATH_PATTERN.search(value)
            or _SECRET_VALUE_PATTERN.search(value)
            or "return 'ok'" in value
        )
    return False


def _load_json_file(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON artifact must be an object")
    return payload


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    try:
        stage_path.relative_to(workspace_path)
    except ValueError:
        return
    raise ValueError("stage directory must be outside the target workspace")


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def _float_value(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _merge_validation(*validations: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for validation in validations:
        if isinstance(validation, dict):
            errors.extend(str(error) for error in validation.get("errors", []))
    return _validation(not errors, sorted(set(errors)), "llm_proposal_provider_gate")


def _validation(ok: bool, errors: list[str], kind: str) -> dict[str, Any]:
    return {"ok": ok, "kind": kind, "errors": sorted(set(errors))}
