"""Human review ledger and proposal diff preview for project graph proposals.

Batch 29 stages owner review decisions and an inspectable proposal diff. It
does not call providers and does not mutate the canonical graph.
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
from product_agent_os.project_graph_llm_proposal_provider import validate_llm_proposal_provider_gate
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


REVIEW_LEDGER_TARGET = ".codex/product-agent-os/project-code-graph-review-ledger.json"
PROPOSAL_DIFF_TARGET = ".codex/product-agent-os/project-code-graph-proposal-diff.json"
_APPROVAL_BOUNDARY = "batch29_human_review_ledger_and_proposal_diff_preview"
_SOURCE_BOUNDARY = "redacted_proposal_ids_and_evidence_refs_only_no_raw_source"
_BATCH29_ALLOWED_SURFACES = {"human_review_ledger", "proposal_diff_preview"}
_ALLOWED_DECISIONS = {"accepted", "rejected", "accepted_gap"}
_FORBIDDEN_INPUTS = {"raw_source_bodies", "secrets", "absolute_local_paths"}
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
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)


def validate_review_ledger_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 29 review-ledger approval."""

    if not isinstance(approval, dict):
        return _validation(False, ["review_ledger_approval:missing"], "review_ledger_approval")
    errors: list[str] = []
    required_fields = {
        "explicit_approval",
        "owner",
        "allowed_surfaces",
        "review_policy",
        "diff_policy",
        "data_classification",
        "rollback_path",
        "residual_risks",
    }
    errors.extend(f"review_ledger_approval:{field}:missing" for field in sorted(required_fields - set(approval)))
    if approval.get("explicit_approval") is not True:
        errors.append("review_ledger_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("review_ledger_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH29_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"review_ledger_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH29_ALLOWED_SURFACES):
        errors.append(f"review_ledger_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_review_policy(approval.get("review_policy")))
    errors.extend(_validate_diff_policy(approval.get("diff_policy")))
    errors.extend(_validate_data_classification(approval.get("data_classification")))
    if approval.get("rollback_path") != f"delete {REVIEW_LEDGER_TARGET}":
        errors.append("review_ledger_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("review_ledger_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("review_ledger_approval:unsafe_text")
    return _validation(not errors, errors, "review_ledger_approval")


def build_human_review_ledger(
    graph: dict[str, Any],
    *,
    local_proposals: dict[str, Any] | None,
    provider_gate: dict[str, Any] | None,
    safety_eval: dict[str, Any] | None,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
    review_decisions: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a source-free Batch 29 human review ledger."""

    approval_validation = validate_review_ledger_approval(approval, governance_packet)
    proposal_validation = (
        validate_llm_extraction_proposals(local_proposals)
        if isinstance(local_proposals, dict)
        else _validation(False, ["llm_proposals:missing"], "llm_extraction_proposals")
    )
    provider_validation = _validate_provider_gate(provider_gate)
    safety_validation = _validate_safety_eval(safety_eval)
    decision_validation = _validate_review_decision_packet(review_decisions, local_proposals or {}, safety_eval)
    validation = _merge_validation(
        approval_validation,
        proposal_validation,
        provider_validation,
        safety_validation,
        decision_validation,
    )
    if approval_validation.get("ok") is not True:
        return _approval_required_ledger(validation)

    decisions = _review_entries(local_proposals or {}, review_decisions or {}, safety_eval)
    status = "ready" if validation.get("ok") is True else "blocked"
    if safety_eval and safety_eval.get("decision_status") == "incident_blocked":
        decisions = [_blocked_review_entry(proposal) for proposal in _all_proposal_records(local_proposals or {})]
    ledger = {
        "schema_version": 1,
        "artifact_kind": "project_graph_human_review_ledger",
        "write_policy": "read_only",
        "status": status,
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "generated_view_policy": "human_review_ledger_is_staged_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "review_policy": {
            "human_review_required": True,
            "owner_decision_required": True,
            "evidence_refs_required": True,
            "allowed_decisions": sorted(_ALLOWED_DECISIONS),
            "accepted_gap_requires_risk": True,
            "no_accepted_proposal_without_owner_decision": True,
            "batch30_dry_run_required_before_mutation": True,
        },
        "input_fingerprints": {
            "graph": graph_content_fingerprint(_redacted_dict(graph)),
            "local_proposals": _artifact_fingerprint(local_proposals or {}),
            "provider_gate": _artifact_fingerprint(provider_gate or {}),
            "safety_eval": _artifact_fingerprint(safety_eval or {}),
        },
        "provider_call_allowed": False,
        "external_call_performed": False,
        "provider_enabled_by_default": False,
        "accepted_for_canonical_graph": False,
        "canonical_graph_mutation": "forbidden",
        "mutation_plan_required_for_apply": True,
        "blocked_surfaces": [
            "provider_call",
            "live_external_model_api_call",
            "canonical_graph_mutation",
            "accepted_without_owner_decision",
            "git_action",
        ],
        "decision_summary": _decision_summary(decisions),
        "review_entries": decisions,
        "rollback": {
            "disable_path": f"delete {REVIEW_LEDGER_TARGET}",
            "delete_diff_path": f"delete {PROPOSAL_DIFF_TARGET}",
            "fallback": "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            "deletion_scope": "stage_root_generated_review_ledger_and_diff_only",
        },
        "git_action": "explicit_only_not_performed",
        "residual_risks": _safe_string_list(approval.get("residual_risks"))[:10],
        "validation": validation,
        "safe_next_action": (
            "Inspect proposal diff and run Batch 30 mutation dry run before any canonical graph update."
        ),
    }
    safe_ledger, report = redact_payload(ledger)
    if isinstance(safe_ledger, dict):
        safe_ledger["redaction_summary"] = report
        safe_ledger["validation"] = _merge_validation(validation, validate_human_review_ledger(safe_ledger))
        if safe_ledger["validation"]["ok"] is not True:
            safe_ledger["status"] = "blocked"
        return safe_ledger
    ledger["validation"] = validate_human_review_ledger(ledger)
    return ledger


def validate_human_review_ledger(ledger: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 29 review ledger schema and no-mutation invariants."""

    errors: list[str] = []
    if ledger.get("schema_version") != 1:
        errors.append("schema_version")
    if ledger.get("artifact_kind") != "project_graph_human_review_ledger":
        errors.append("artifact_kind")
    if ledger.get("write_policy") != "read_only":
        errors.append("write_policy")
    if ledger.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if ledger.get("source_boundary") != _SOURCE_BOUNDARY:
        errors.append("source_boundary")
    if ledger.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if ledger.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if ledger.get("accepted_for_canonical_graph") is not False:
        errors.append("accepted_for_canonical_graph")
    if ledger.get("canonical_graph_mutation") != "forbidden":
        errors.append("canonical_graph_mutation")
    policy = ledger.get("review_policy") if isinstance(ledger.get("review_policy"), dict) else {}
    if policy.get("owner_decision_required") is not True:
        errors.append("review_policy:owner_decision_required")
    if policy.get("evidence_refs_required") is not True:
        errors.append("review_policy:evidence_refs_required")
    if policy.get("no_accepted_proposal_without_owner_decision") is not True:
        errors.append("review_policy:no_accepted_without_owner")
    if ledger.get("mutation_plan_required_for_apply") is not True:
        errors.append("mutation_plan_required_for_apply")
    entries = ledger.get("review_entries")
    if not isinstance(entries, list):
        errors.append("review_entries")
        entries = []
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("review_entry:shape")
            continue
        decision = entry.get("decision")
        if decision not in _ALLOWED_DECISIONS and decision != "blocked":
            errors.append("review_entry:decision")
        if decision == "accepted":
            if not entry.get("decision_by") or not entry.get("owner_decision_at"):
                errors.append("review_entry:accepted:owner_decision")
            if not entry.get("evidence_refs"):
                errors.append("review_entry:accepted:evidence_refs")
            if entry.get("eligible_for_canonical_mutation") is not False:
                errors.append("review_entry:accepted:canonical_mutation")
        if decision == "accepted_gap":
            if not entry.get("accepted_gap_risk") or not entry.get("follow_up_condition"):
                errors.append("review_entry:accepted_gap:risk")
            if entry.get("eligible_for_canonical_mutation") is not False:
                errors.append("review_entry:accepted_gap:canonical_mutation")
    if _has_unsafe_text(ledger):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(ledger, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, sorted(set(errors)), "human_review_ledger")


def build_proposal_diff_preview(
    graph: dict[str, Any],
    *,
    local_proposals: dict[str, Any] | None,
    review_ledger: dict[str, Any],
) -> dict[str, Any]:
    """Build an inspectable proposal diff preview without applying changes."""

    entries = [
        entry
        for entry in review_ledger.get("review_entries", [])
        if isinstance(entry, dict) and entry.get("decision") in {"accepted", "accepted_gap"}
    ]
    proposals_by_id = _proposal_map(local_proposals or {})
    added_nodes: list[dict[str, Any]] = []
    added_edges: list[dict[str, Any]] = []
    rationale_comments: list[dict[str, Any]] = []
    for entry in entries:
        proposal = proposals_by_id.get(str(entry.get("proposal_id") or ""))
        if not proposal:
            continue
        preview = _proposal_preview(proposal, entry)
        kind = proposal.get("proposal_kind")
        if kind == "semantic_node":
            added_nodes.append(preview)
        elif kind == "semantic_edge":
            added_edges.append(preview)
        elif kind == "rationale_comment":
            rationale_comments.append(preview)
    diff = {
        "schema_version": 1,
        "artifact_kind": "project_graph_proposal_diff_preview",
        "write_policy": "read_only",
        "status": "preview_ready" if review_ledger.get("status") == "ready" else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "generated_view_policy": "proposal_diff_preview_is_generated_evidence_not_source_of_truth",
        "graph_fingerprint": graph_content_fingerprint(_redacted_dict(graph)),
        "review_ledger_fingerprint": _artifact_fingerprint(review_ledger),
        "human_can_inspect_before_mutation": True,
        "mutation_plan_required_for_apply": True,
        "mutated_canonical_graph": False,
        "accepted_for_canonical_graph": False,
        "canonical_graph_mutation": "forbidden",
        "provider_call_allowed": False,
        "external_call_performed": False,
        "diff": {
            "added_nodes": added_nodes,
            "added_edges": added_edges,
            "changed_nodes": [],
            "rationale_comments": rationale_comments,
        },
        "summary": {
            "added_nodes": len(added_nodes),
            "added_edges": len(added_edges),
            "rationale_comments": len(rationale_comments),
            "changed_nodes": 0,
        },
        "rollback": review_ledger.get(
            "rollback",
            {"disable_path": f"delete {REVIEW_LEDGER_TARGET}", "delete_diff_path": f"delete {PROPOSAL_DIFF_TARGET}"},
        ),
        "safe_next_action": "Review this preview; Batch 30 owns dry-run mutation, journal and rollback.",
    }
    safe_diff, report = redact_payload(diff)
    if isinstance(safe_diff, dict):
        safe_diff["redaction_summary"] = report
        safe_diff["validation"] = validate_proposal_diff_preview(safe_diff, review_ledger)
        if safe_diff["validation"]["ok"] is not True:
            safe_diff["status"] = "blocked"
        return safe_diff
    diff["validation"] = validate_proposal_diff_preview(diff, review_ledger)
    return diff


def validate_proposal_diff_preview(
    diff: dict[str, Any],
    review_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate Batch 29 proposal diff preview schema and no-apply boundary."""

    errors: list[str] = []
    if diff.get("schema_version") != 1:
        errors.append("schema_version")
    if diff.get("artifact_kind") != "project_graph_proposal_diff_preview":
        errors.append("artifact_kind")
    if diff.get("write_policy") != "read_only":
        errors.append("write_policy")
    if diff.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if diff.get("source_boundary") != _SOURCE_BOUNDARY:
        errors.append("source_boundary")
    if diff.get("human_can_inspect_before_mutation") is not True:
        errors.append("human_can_inspect_before_mutation")
    if diff.get("mutation_plan_required_for_apply") is not True:
        errors.append("mutation_plan_required_for_apply")
    if diff.get("mutated_canonical_graph") is not False:
        errors.append("mutated_canonical_graph")
    if diff.get("accepted_for_canonical_graph") is not False:
        errors.append("accepted_for_canonical_graph")
    if diff.get("canonical_graph_mutation") != "forbidden":
        errors.append("canonical_graph_mutation")
    if diff.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if diff.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    change_set = diff.get("diff") if isinstance(diff.get("diff"), dict) else {}
    for key in ["added_nodes", "added_edges", "changed_nodes", "rationale_comments"]:
        if not isinstance(change_set.get(key), list):
            errors.append(f"diff:{key}")
    if isinstance(review_ledger, dict) and review_ledger.get("status") == "ready" and diff.get("status") != "preview_ready":
        errors.append("status")
    if _has_unsafe_text(diff):
        errors.append("source_boundary:unsafe_text")
    rendered = json.dumps(diff, sort_keys=True, default=str)
    errors.extend(f"redaction:{error}" for error in validate_redaction(rendered))
    return _validation(not errors, sorted(set(errors)), "proposal_diff_preview")


def stage_review_ledger(
    graph_artifact: str | Path,
    local_proposals_artifact: str | Path,
    provider_gate_artifact: str | Path,
    safety_eval_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path | None,
    review_decisions_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage Batch 29 review ledger and proposal diff preview artifacts."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    proposals = load_llm_extraction_proposals(local_proposals_artifact)
    provider_gate = _load_json_file(provider_gate_artifact)
    safety_eval = _load_json_file(safety_eval_artifact)
    governance = _load_json_file(governance_artifact) if governance_artifact else None
    review_decisions = _load_json_file(review_decisions_artifact) if review_decisions_artifact else None
    ledger = build_human_review_ledger(
        graph,
        local_proposals=proposals,
        provider_gate=provider_gate,
        safety_eval=safety_eval,
        approval=approval,
        governance_packet=governance,
        review_decisions=review_decisions,
    )
    diff = build_proposal_diff_preview(graph, local_proposals=proposals, review_ledger=ledger)
    action = "blocked"
    if ledger.get("status") == "ready" and ledger.get("validation", {}).get("ok") is True:
        ledger_target = stage_path / REVIEW_LEDGER_TARGET
        diff_target = stage_path / PROPOSAL_DIFF_TARGET
        ledger_target.parent.mkdir(parents=True, exist_ok=True)
        ledger_target.write_text(json.dumps(ledger, indent=2, sort_keys=True), encoding="utf-8")
        diff_target.write_text(json.dumps(diff, indent=2, sort_keys=True), encoding="utf-8")
        action = "create"
    return {
        "rendered_artifacts": {
            "status": ledger.get("status"),
            "mode": "build-review-ledger",
            "root_status": "redacted",
            "source_boundary": _SOURCE_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "accepted_for_canonical_graph": False,
            "canonical_graph_mutation": "forbidden",
            "mutation_plan_required_for_apply": True,
            "files": [
                {
                    "target_path": REVIEW_LEDGER_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": REVIEW_LEDGER_TARGET,
                },
                {
                    "target_path": PROPOSAL_DIFF_TARGET,
                    "action": action,
                    "write_policy": "staged_only" if action == "create" else "blocked",
                    "staged_path": PROPOSAL_DIFF_TARGET,
                },
            ],
            "rollback": {"disable_path": f"delete {REVIEW_LEDGER_TARGET}"},
            "validation": ledger.get("validation"),
        }
    }


def disable_review_ledger(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Disable Batch 29 generated artifacts by deleting stage-root files."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    targets = [REVIEW_LEDGER_TARGET, PROPOSAL_DIFF_TARGET]
    deleted: list[str] = []
    for relative in targets:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled",
            "mode": "disable-review-ledger",
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
            "rollback": {"disable_path": f"delete {REVIEW_LEDGER_TARGET}"},
        }
    }


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["review_ledger_approval:governance_packet:missing"]
    errors: list[str] = []
    if governance_packet.get("status") != "ready":
        errors.append("review_ledger_approval:governance_packet:not_ready")
    if validate_live_governance_packet(governance_packet).get("ok") is not True:
        errors.append("review_ledger_approval:governance_packet:invalid")
    provider_policy = governance_packet.get("provider_policy") if isinstance(governance_packet.get("provider_policy"), dict) else {}
    if provider_policy.get("requires_batch_specific_approval") is not True:
        errors.append("review_ledger_approval:governance_packet:batch_specific_approval")
    return errors


def _validate_review_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["review_ledger_approval:review_policy"]
    errors: list[str] = []
    required_true = [
        "owner_decision_required",
        "evidence_refs_required",
        "accepted_gap_requires_risk",
        "safety_eval_required",
    ]
    for field in required_true:
        if policy.get(field) is not True:
            errors.append(f"review_ledger_approval:review_policy:{field}")
    allowed = {str(item) for item in policy.get("allowed_decisions", []) if isinstance(item, str)}
    if not _ALLOWED_DECISIONS.issubset(allowed):
        errors.append("review_ledger_approval:review_policy:allowed_decisions")
    return errors


def _validate_diff_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["review_ledger_approval:diff_policy"]
    errors: list[str] = []
    if policy.get("preview_nodes_edges_rationale_comments") is not True:
        errors.append("review_ledger_approval:diff_policy:preview")
    if policy.get("canonical_mutation_allowed") is not False:
        errors.append("review_ledger_approval:diff_policy:canonical_mutation")
    if policy.get("batch30_dry_run_required") is not True:
        errors.append("review_ledger_approval:diff_policy:batch30_dry_run")
    return errors


def _validate_data_classification(classification: Any) -> list[str]:
    if not isinstance(classification, dict):
        return ["review_ledger_approval:data_classification"]
    allowed = {str(item) for item in classification.get("allowed_inputs", []) if isinstance(item, str)}
    forbidden = {str(item) for item in classification.get("forbidden_inputs", []) if isinstance(item, str)}
    errors = [f"review_ledger_approval:data_classification:{field}" for field in sorted(_FORBIDDEN_INPUTS - forbidden)]
    if not allowed:
        errors.append("review_ledger_approval:data_classification:allowed_inputs")
    return errors


def _validate_provider_gate(provider_gate: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(provider_gate, dict):
        return _validation(False, ["llm_proposal_provider_gate:missing"], "llm_proposal_provider_gate")
    errors: list[str] = []
    validation = validate_llm_proposal_provider_gate(provider_gate)
    if validation.get("ok") is not True:
        errors.append("llm_proposal_provider_gate:invalid")
    if provider_gate.get("provider_policy", {}).get("provider_call_allowed") is not False:
        errors.append("llm_proposal_provider_gate:provider_call_allowed")
    if provider_gate.get("canonical_graph_mutation") != "forbidden":
        errors.append("llm_proposal_provider_gate:canonical_graph_mutation")
    return _validation(not errors, errors, "llm_proposal_provider_gate")


def _validate_safety_eval(safety_eval: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(safety_eval, dict):
        return _validation(False, ["llm_proposal_safety_eval:missing"], "llm_proposal_safety_eval")
    errors: list[str] = []
    if safety_eval.get("artifact_kind") != "project_graph_llm_proposal_safety_eval":
        errors.append("llm_proposal_safety_eval:artifact_kind")
    if safety_eval.get("external_call_performed") is not False:
        errors.append("llm_proposal_safety_eval:external_call_performed")
    if safety_eval.get("canonical_graph_mutation") != "forbidden":
        errors.append("llm_proposal_safety_eval:canonical_graph_mutation")
    if safety_eval.get("decision_status") == "incident_blocked":
        errors.append("llm_proposal_safety_eval:incident_blocked")
    return _validation(not errors, errors, "llm_proposal_safety_eval")


def _validate_review_decision_packet(
    review_decisions: dict[str, Any] | None,
    local_proposals: dict[str, Any],
    safety_eval: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(review_decisions, dict):
        return _validation(False, ["review_decisions:missing"], "review_decisions")
    proposal_map = _proposal_map(local_proposals)
    errors: list[str] = []
    decisions = review_decisions.get("decisions")
    if not isinstance(decisions, list):
        return _validation(False, ["review_decisions:decisions"], "review_decisions")
    decision_ids: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append("review_decision:shape")
            continue
        proposal_id = sanitize_graph_text(decision.get("proposal_id") or "")
        decision_ids.add(proposal_id)
        if proposal_id not in proposal_map:
            errors.append("review_decision:proposal_id")
        decision_value = decision.get("decision")
        if decision_value not in _ALLOWED_DECISIONS:
            errors.append("review_decision:decision")
        if decision_value == "accepted":
            if not sanitize_graph_text(decision.get("decision_by") or ""):
                errors.append("review_decision:accepted:owner_decision")
            if not _valid_evidence_refs(decision.get("evidence_refs"), proposal_map.get(proposal_id, {})):
                errors.append("review_decision:accepted:evidence_refs")
            if isinstance(safety_eval, dict) and safety_eval.get("decision_status") == "incident_blocked":
                errors.append("review_decision:accepted:safety_eval")
        if decision_value == "accepted_gap":
            if not sanitize_graph_text(decision.get("decision_by") or ""):
                errors.append("review_decision:accepted_gap:owner_decision")
            if not _valid_evidence_refs(decision.get("evidence_refs"), proposal_map.get(proposal_id, {})):
                errors.append("review_decision:accepted_gap:evidence_refs")
            if not sanitize_graph_text(decision.get("accepted_gap_risk") or ""):
                errors.append("review_decision:accepted_gap:risk")
            if not sanitize_graph_text(decision.get("follow_up_condition") or ""):
                errors.append("review_decision:accepted_gap:follow_up")
    if _has_unsafe_text(review_decisions):
        errors.append("review_decisions:unsafe_text")
    return _validation(not errors, errors, "review_decisions")


def _review_entries(
    local_proposals: dict[str, Any],
    review_decisions: dict[str, Any],
    safety_eval: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    proposal_map = _proposal_map(local_proposals)
    decisions = review_decisions.get("decisions", []) if isinstance(review_decisions.get("decisions"), list) else []
    entries: list[dict[str, Any]] = []
    for decision in decisions:
        if not isinstance(decision, dict):
            continue
        proposal = proposal_map.get(str(decision.get("proposal_id") or ""))
        if not proposal:
            continue
        decision_value = sanitize_graph_text(decision.get("decision") or "")
        if isinstance(safety_eval, dict) and safety_eval.get("decision_status") == "incident_blocked":
            decision_value = "blocked"
        entries.append(
            {
                "proposal_id": sanitize_graph_text(proposal.get("proposal_id") or ""),
                "proposal_kind": sanitize_graph_text(proposal.get("proposal_kind") or ""),
                "decision": decision_value,
                "decision_by": sanitize_graph_text(decision.get("decision_by") or ""),
                "owner_decision_at": sanitize_graph_text(decision.get("owner_decision_at") or "staged_review_packet"),
                "source_node_id": sanitize_graph_text(proposal.get("source_node_id") or ""),
                "target_node_id": sanitize_graph_text(proposal.get("target_node_id") or ""),
                "evidence_refs": _safe_string_list(decision.get("evidence_refs"))[:10],
                "rationale": sanitize_graph_text(decision.get("rationale") or "")[:300],
                "accepted_gap_risk": sanitize_graph_text(decision.get("accepted_gap_risk") or "")[:300],
                "follow_up_condition": sanitize_graph_text(decision.get("follow_up_condition") or "")[:300],
                "eligible_for_canonical_mutation": False,
                "requires_batch30_dry_run": decision_value in {"accepted", "accepted_gap"},
                "canonical_graph_mutation": "forbidden",
            }
        )
    return entries


def _blocked_review_entry(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": sanitize_graph_text(proposal.get("proposal_id") or ""),
        "proposal_kind": sanitize_graph_text(proposal.get("proposal_kind") or ""),
        "decision": "blocked",
        "decision_by": "",
        "owner_decision_at": "",
        "source_node_id": sanitize_graph_text(proposal.get("source_node_id") or ""),
        "target_node_id": sanitize_graph_text(proposal.get("target_node_id") or ""),
        "evidence_refs": _safe_string_list(proposal.get("source_observation_ids"))[:10],
        "rationale": "Blocked because LLM proposal safety eval is incident_blocked.",
        "eligible_for_canonical_mutation": False,
        "requires_batch30_dry_run": False,
        "canonical_graph_mutation": "forbidden",
    }


def _proposal_preview(proposal: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": sanitize_graph_text(proposal.get("proposal_id") or ""),
        "proposal_kind": sanitize_graph_text(proposal.get("proposal_kind") or ""),
        "review_decision": sanitize_graph_text(entry.get("decision") or ""),
        "source_node_id": sanitize_graph_text(proposal.get("source_node_id") or ""),
        "target_node_id": sanitize_graph_text(proposal.get("target_node_id") or ""),
        "label": sanitize_graph_text(proposal.get("label") or proposal.get("proposal_id") or "")[:160],
        "rationale": sanitize_graph_text(proposal.get("rationale") or "")[:300],
        "evidence_refs": _safe_string_list(proposal.get("source_observation_ids"))[:10],
        "would_apply": False,
        "requires_batch30_dry_run": True,
        "canonical_graph_mutation": "forbidden",
    }


def _all_proposal_records(proposals: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
        records.extend(item for item in proposals.get(key, []) if isinstance(item, dict))
    return records


def _proposal_map(proposals: dict[str, Any]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for proposal in _all_proposal_records(proposals):
        proposal_id = str(proposal.get("proposal_id") or "")
        if not proposal_id:
            continue
        if proposal_id not in by_id:
            by_id[proposal_id] = dict(proposal)
            by_id[proposal_id]["source_observation_ids"] = _safe_string_list(proposal.get("source_observation_ids"))
            continue
        existing = by_id[proposal_id]
        refs = list(existing.get("source_observation_ids", []))
        for ref in _safe_string_list(proposal.get("source_observation_ids")):
            if ref not in refs:
                refs.append(ref)
        existing["source_observation_ids"] = refs
    return by_id


def _decision_summary(entries: list[dict[str, Any]]) -> dict[str, int]:
    summary = {"accepted": 0, "rejected": 0, "accepted_gap": 0, "blocked": 0, "total": len(entries)}
    for entry in entries:
        decision = str(entry.get("decision") or "")
        if decision in summary:
            summary[decision] += 1
    return summary


def _approval_required_ledger(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_human_review_ledger",
        "write_policy": "read_only",
        "status": "approval_required",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "accepted_for_canonical_graph": False,
        "canonical_graph_mutation": "forbidden",
        "decision_summary": {"accepted": 0, "rejected": 0, "accepted_gap": 0, "blocked": 0, "total": 0},
        "validation": validation,
        "safe_next_action": "Provide Batch 29 approval, governance and owner review decisions.",
    }


def _valid_evidence_refs(value: Any, proposal: dict[str, Any]) -> bool:
    if not isinstance(value, list) or not value:
        return False
    allowed = {str(item) for item in proposal.get("source_observation_ids", []) if item}
    if not allowed:
        return False
    return {str(item) for item in value}.issubset(allowed)


def _artifact_fingerprint(artifact: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(_redacted_dict(artifact), sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _redacted_dict(payload: Any) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else {}


def _safe_string_list(value: Any) -> list[str]:
    return [sanitize_graph_text(item) for item in value if isinstance(item, str)] if isinstance(value, list) else []


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


def _merge_validation(*validations: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for validation in validations:
        if isinstance(validation, dict):
            errors.extend(str(error) for error in validation.get("errors", []))
    return _validation(not errors, sorted(set(errors)), "human_review_ledger")


def _validation(ok: bool, errors: list[str], kind: str) -> dict[str, Any]:
    return {"ok": ok, "kind": kind, "errors": sorted(set(errors))}
