"""Canonical graph mutation dry-run, journal and rollback for project graph proposals.

Batch 30 consumes the Batch 29 human review ledger and proposal diff preview.
It writes only staged artifacts under an explicit stage root; it does not call
providers or silently mutate a target workspace graph.
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
from product_agent_os.project_graph_ontology import validate_graph_schema
from product_agent_os.project_graph_queries import load_graph_artifact
from product_agent_os.project_graph_review_ledger import (
    PROPOSAL_DIFF_TARGET,
    REVIEW_LEDGER_TARGET,
    validate_human_review_ledger,
    validate_proposal_diff_preview,
)
from product_agent_os.project_graph_sanitization import sanitize_graph_text


MUTATION_PLAN_TARGET = ".codex/product-agent-os/project-code-graph-mutation-plan.json"
MUTATION_JOURNAL_TARGET = ".codex/product-agent-os/project-code-graph-mutation-journal.jsonl"
MUTATED_GRAPH_TARGET = ".codex/product-agent-os/project-code-graph-canonical-mutated.json"
ROLLBACK_PROOF_TARGET = ".codex/product-agent-os/project-code-graph-rollback-proof.json"

_APPROVAL_BOUNDARY = "batch30_canonical_graph_mutation_journal_and_rollback"
_SOURCE_BOUNDARY = "reviewed_redacted_proposal_diff_and_ledger_only_no_raw_source"
_ROLLBACK_PATH = "delete generated Batch 30 mutation artifacts under stage root"
_BATCH30_ALLOWED_SURFACES = {
    "canonical_mutation_dry_run",
    "mutation_journal",
    "accepted_mutation_apply",
    "rollback_engine",
}
_FORBIDDEN_INPUTS = {"raw_source_bodies", "secrets", "absolute_local_paths", "private_text"}
_GENERATED_CACHE_TARGETS = (
    ".codex/product-agent-os/project-code-graph-search-index.json",
    ".codex/product-agent-os/project-code-graph-backend.json",
    ".codex/product-agent-os/project-code-graph-semantic-index.json",
    ".codex/product-agent-os/project-code-graph-llm-proposals.json",
    ".codex/product-agent-os/project-code-graph-embedding-provider.json",
    ".codex/product-agent-os/project-code-graph-reranker-provider.json",
    ".codex/product-agent-os/project-code-graph-hybrid-retrieval.json",
    ".codex/product-agent-os/project-code-graph-llm-proposal-provider.json",
    ".codex/product-agent-os/project-code-graph-llm-proposal-eval.json",
    MUTATION_PLAN_TARGET,
    MUTATION_JOURNAL_TARGET,
    MUTATED_GRAPH_TARGET,
    ROLLBACK_PROOF_TARGET,
)
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


def validate_canonical_mutation_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 30 canonical mutation approval."""

    if not isinstance(approval, dict):
        return _validation(False, ["canonical_mutation_approval:missing"], "canonical_mutation_approval")
    errors: list[str] = []
    required_fields = {
        "explicit_approval",
        "owner",
        "allowed_surfaces",
        "mutation_policy",
        "journal_policy",
        "rollback_policy",
        "data_classification",
        "rollback_path",
        "residual_risks",
    }
    errors.extend(f"canonical_mutation_approval:{field}:missing" for field in sorted(required_fields - set(approval)))
    if approval.get("explicit_approval") is not True:
        errors.append("canonical_mutation_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("canonical_mutation_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH30_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"canonical_mutation_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH30_ALLOWED_SURFACES):
        errors.append(f"canonical_mutation_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_mutation_policy(approval.get("mutation_policy")))
    errors.extend(_validate_journal_policy(approval.get("journal_policy")))
    errors.extend(_validate_rollback_policy(approval.get("rollback_policy")))
    errors.extend(_validate_data_classification(approval.get("data_classification")))
    if approval.get("rollback_path") != _ROLLBACK_PATH:
        errors.append("canonical_mutation_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("canonical_mutation_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("canonical_mutation_approval:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "canonical_mutation_approval")


def build_canonical_mutation_plan(
    graph: dict[str, Any],
    *,
    review_ledger: dict[str, Any],
    proposal_diff: dict[str, Any],
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build the Batch 30 dry-run mutation plan without changing the graph."""

    approval_validation = validate_canonical_mutation_approval(approval, governance_packet)
    ledger_validation = validate_human_review_ledger(review_ledger)
    diff_validation = validate_proposal_diff_preview(proposal_diff, review_ledger)
    fingerprint_validation = _validate_input_fingerprints(graph, review_ledger, proposal_diff)
    accepted_validation = _validate_accepted_entries_have_diff(review_ledger, proposal_diff)
    pre_graph_digest = graph_content_fingerprint(_redacted_dict(graph))
    operations, skipped = _planned_operations(proposal_diff)
    conflict_errors = _conflict_errors(graph, operations)
    simulated_graph = _apply_operations_to_graph(graph, operations) if not conflict_errors else _json_copy(graph)
    planned_graph_digest = graph_content_fingerprint(_redacted_dict(simulated_graph))
    digest_errors = []
    if operations and planned_graph_digest == pre_graph_digest:
        digest_errors.append("graph_digest_comparison:unchanged_after_operations")
    validation = _merge_validation(
        approval_validation,
        ledger_validation,
        diff_validation,
        fingerprint_validation,
        accepted_validation,
        _validation(not conflict_errors, conflict_errors, "mutation_conflict_checks"),
        _validation(not digest_errors, digest_errors, "graph_digest_comparison"),
    )
    if approval_validation.get("ok") is not True:
        return _approval_required_plan(validation, pre_graph_digest)

    status = "ready" if validation.get("ok") is True else "blocked"
    plan = {
        "schema_version": 1,
        "artifact_kind": "project_graph_canonical_mutation_plan",
        "write_policy": "dry_run_only",
        "status": status,
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "generated_view_policy": "mutation_plan_is_generated_evidence_not_source_of_truth",
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "provider_call_allowed": False,
        "external_call_performed": False,
        "canonical_graph_mutation": "dry_run_only",
        "mutation_write_policy": "stage_root_generated_graph_copy_only",
        "accepted_for_canonical_graph": status == "ready" and bool(operations),
        "no_mutation_without_dry_run_plan": True,
        "mutation_plan_required_for_apply": True,
        "only_accepted_proposals_mutate_graph": True,
        "accepted_gap_remains_non_mutating": True,
        "input_fingerprints": {
            "graph": pre_graph_digest,
            "review_ledger": _artifact_fingerprint(review_ledger),
            "proposal_diff": _artifact_fingerprint(proposal_diff),
        },
        "graph_digest_comparison": {
            "pre_graph_digest": pre_graph_digest,
            "planned_graph_digest": planned_graph_digest,
            "digest_changed": planned_graph_digest != pre_graph_digest,
            "versioned_graph_digest": _versioned_digest(planned_graph_digest),
        },
        "dry_run": {
            "status": "passed" if status == "ready" else "blocked",
            "conflict_check_required": True,
            "graph_digest_check_required": True,
            "conflicts": sorted(set(conflict_errors)),
            "operation_count": len(operations),
        },
        "mutation_policy": {
            "dry_run_required": True,
            "conflict_check_required": True,
            "graph_digest_check_required": True,
            "accepted_only": True,
            "accepted_gap_not_mutation_eligible": True,
            "review_ledger_required": REVIEW_LEDGER_TARGET,
            "proposal_diff_required": PROPOSAL_DIFF_TARGET,
            "stage_root_only": True,
        },
        "journal_policy": {
            "append_only": True,
            "jsonl_required": True,
            "inverse_patch_required": True,
            "target": MUTATION_JOURNAL_TARGET,
            "every_mutation_has_rollback_patch": True,
        },
        "rollback_policy": {
            "restore_prior_digest": True,
            "delete_generated_caches": True,
            "rollback_proof_required": True,
            "generated_cache_targets": list(_GENERATED_CACHE_TARGETS),
            "target": ROLLBACK_PROOF_TARGET,
            "rollback_restores_previous_graph_digest": True,
        },
        "operations": operations,
        "skipped_review_decisions": skipped,
        "rollback": {
            "disable_path": _ROLLBACK_PATH,
            "fallback": "review_ledger_or_graph_only",
            "deletion_scope": "stage_root_generated_mutation_artifacts_and_graph_derived_caches",
        },
        "git_action": "explicit_only_not_performed",
        "residual_risks": _safe_string_list(approval.get("residual_risks"))[:10],
        "validation": validation,
        "safe_next_action": "Apply this dry-run plan only to a staged graph copy, then verify journal rollback proof.",
    }
    safe_plan, report = redact_payload(plan)
    if isinstance(safe_plan, dict):
        safe_plan["redaction_summary"] = report
        safe_plan["validation"] = _merge_validation(validation, validate_canonical_mutation_plan(safe_plan))
        if safe_plan["validation"]["ok"] is not True:
            safe_plan["status"] = "blocked"
        return safe_plan
    plan["validation"] = validate_canonical_mutation_plan(plan)
    return plan


def validate_canonical_mutation_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 30 dry-run plan invariants."""

    errors: list[str] = []
    if plan.get("schema_version") != 1:
        errors.append("schema_version")
    if plan.get("artifact_kind") != "project_graph_canonical_mutation_plan":
        errors.append("artifact_kind")
    if plan.get("write_policy") != "dry_run_only":
        errors.append("write_policy")
    if plan.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if plan.get("source_boundary") != _SOURCE_BOUNDARY:
        errors.append("source_boundary")
    if plan.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if plan.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if plan.get("canonical_graph_mutation") != "dry_run_only":
        errors.append("canonical_graph_mutation")
    if plan.get("mutation_write_policy") != "stage_root_generated_graph_copy_only":
        errors.append("mutation_write_policy")
    if plan.get("no_mutation_without_dry_run_plan") is not True:
        errors.append("no_mutation_without_dry_run_plan")
    if plan.get("mutation_plan_required_for_apply") is not True:
        errors.append("mutation_plan_required_for_apply")
    if plan.get("only_accepted_proposals_mutate_graph") is not True:
        errors.append("only_accepted_proposals_mutate_graph")
    if plan.get("accepted_gap_remains_non_mutating") is not True:
        errors.append("accepted_gap_remains_non_mutating")
    digest = plan.get("graph_digest_comparison") if isinstance(plan.get("graph_digest_comparison"), dict) else {}
    if not str(digest.get("pre_graph_digest") or "").startswith("sha256:"):
        errors.append("graph_digest_comparison:pre_graph_digest")
    if not str(digest.get("planned_graph_digest") or "").startswith("sha256:"):
        errors.append("graph_digest_comparison:planned_graph_digest")
    if not str(digest.get("versioned_graph_digest") or "").startswith("graph-v1@sha256:"):
        errors.append("graph_digest_comparison:versioned_graph_digest")
    dry_run = plan.get("dry_run") if isinstance(plan.get("dry_run"), dict) else {}
    if dry_run.get("conflict_check_required") is not True:
        errors.append("dry_run:conflict_check_required")
    if dry_run.get("graph_digest_check_required") is not True:
        errors.append("dry_run:graph_digest_check_required")
    policy = plan.get("mutation_policy") if isinstance(plan.get("mutation_policy"), dict) else {}
    if policy.get("accepted_only") is not True:
        errors.append("mutation_policy:accepted_only")
    if policy.get("stage_root_only") is not True:
        errors.append("mutation_policy:stage_root_only")
    journal_policy = plan.get("journal_policy") if isinstance(plan.get("journal_policy"), dict) else {}
    if journal_policy.get("append_only") is not True:
        errors.append("journal_policy:append_only")
    if journal_policy.get("inverse_patch_required") is not True:
        errors.append("journal_policy:inverse_patch_required")
    rollback_policy = plan.get("rollback_policy") if isinstance(plan.get("rollback_policy"), dict) else {}
    if rollback_policy.get("restore_prior_digest") is not True:
        errors.append("rollback_policy:restore_prior_digest")
    if rollback_policy.get("delete_generated_caches") is not True:
        errors.append("rollback_policy:delete_generated_caches")
    operations = plan.get("operations")
    if not isinstance(operations, list):
        errors.append("operations")
        operations = []
    for operation in operations:
        errors.extend(_validate_operation(operation))
    if _has_unsafe_text(plan):
        errors.append("source_boundary:unsafe_text")
    errors.extend(f"redaction:{error}" for error in validate_redaction(json.dumps(plan, sort_keys=True, default=str)))
    return _validation(not errors, sorted(set(errors)), "canonical_mutation_plan")


def apply_accepted_mutations_to_graph(
    graph: dict[str, Any],
    mutation_plan: dict[str, Any],
) -> dict[str, Any]:
    """Apply accepted-only plan operations to an in-memory staged graph copy."""

    plan_validation = validate_canonical_mutation_plan(mutation_plan)
    errors = [] if plan_validation.get("ok") is True else ["mutation_plan:invalid"]
    if mutation_plan.get("status") != "ready":
        errors.append("mutation_plan:not_ready")
    if mutation_plan.get("dry_run", {}).get("status") != "passed":
        errors.append("mutation_plan:dry_run_not_passed")
    if mutation_plan.get("no_mutation_without_dry_run_plan") is not True:
        errors.append("mutation_plan:dry_run_required")
    operations = mutation_plan.get("operations", []) if isinstance(mutation_plan.get("operations"), list) else []
    conflict_errors = _conflict_errors(graph, operations)
    errors.extend(conflict_errors)
    if errors:
        return _blocked_mutation_result(_merge_validation(plan_validation, _validation(False, errors, "apply_accepted_mutations")))

    pre_digest = graph_content_fingerprint(_redacted_dict(graph))
    mutated_graph, journal_entries = _apply_operations_with_journal(graph, operations)
    post_digest = graph_content_fingerprint(_redacted_dict(mutated_graph))
    graph_validation = validate_graph_schema(mutated_graph)
    validation = _merge_validation(
        plan_validation,
        graph_validation,
        _validation(
            bool(journal_entries) == bool(operations) and all(entry.get("inverse_patch") for entry in journal_entries),
            ["mutation_journal:inverse_patch"] if operations and not journal_entries else [],
            "mutation_journal",
        ),
    )
    result = {
        "schema_version": 1,
        "artifact_kind": "project_graph_canonical_mutation_result",
        "write_policy": "staged_only",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "generated_view_policy": "mutated_graph_copy_is_staged_evidence_not_source_of_truth",
        "provider_call_allowed": False,
        "external_call_performed": False,
        "canonical_graph_mutation": "stage_root_generated_graph_copy_only",
        "mutation_plan_required_for_apply": True,
        "only_accepted_proposals_mutate_graph": True,
        "accepted_gap_remains_non_mutating": True,
        "accepted_for_canonical_graph": bool(operations),
        "applied_operation_count": len(operations),
        "journal_entry_count": len(journal_entries),
        "pre_graph_digest": pre_digest,
        "post_graph_digest": post_digest,
        "versioned_graph_digest": _versioned_digest(post_digest),
        "mutation_plan_fingerprint": _artifact_fingerprint(mutation_plan),
        "journal_target": MUTATION_JOURNAL_TARGET,
        "mutated_graph_target": MUTATED_GRAPH_TARGET,
        "rollback_proof_required": True,
        "mutated_graph": mutated_graph,
        "journal_entries": journal_entries,
        "validation": validation,
    }
    safe_result, report = redact_payload(result)
    if isinstance(safe_result, dict):
        safe_result["redaction_summary"] = report
        return safe_result
    return result


def build_graph_rollback_proof(
    original_graph: dict[str, Any],
    mutated_graph: dict[str, Any],
    journal_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build rollback proof by applying inverse patches and comparing digests."""

    pre_digest = graph_content_fingerprint(_redacted_dict(original_graph))
    mutated_digest = graph_content_fingerprint(_redacted_dict(mutated_graph))
    restored_graph = _json_copy(mutated_graph)
    inverse_errors: list[str] = []
    for entry in reversed(journal_entries):
        patch = entry.get("inverse_patch") if isinstance(entry, dict) else None
        if not isinstance(patch, dict):
            inverse_errors.append("journal_entry:inverse_patch")
            continue
        restored_graph, patch_errors = _apply_inverse_patch(restored_graph, patch)
        inverse_errors.extend(patch_errors)
    restored_digest = graph_content_fingerprint(_redacted_dict(restored_graph))
    digest_ok = restored_digest == pre_digest
    validation = _merge_validation(
        validate_graph_schema(restored_graph),
        _validation(not inverse_errors, inverse_errors, "rollback_inverse_patches"),
        _validation(digest_ok, [] if digest_ok else ["rollback_digest:mismatch"], "rollback_digest"),
    )
    proof = {
        "schema_version": 1,
        "artifact_kind": "project_graph_rollback_proof",
        "write_policy": "staged_only",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "canonical_graph_mutation": "rollback_restores_stage_root_generated_graph_copy",
        "restore_prior_digest": True,
        "rollback_restores_previous_graph_digest": digest_ok,
        "delete_generated_caches": True,
        "pre_graph_digest": pre_digest,
        "mutated_graph_digest": mutated_digest,
        "restored_graph_digest": restored_digest,
        "journal_entry_count": len(journal_entries),
        "inverse_patch_count": sum(1 for entry in journal_entries if isinstance(entry, dict) and entry.get("inverse_patch")),
        "generated_cache_deletion": {
            "targets_checked": list(_GENERATED_CACHE_TARGETS),
            "deletion_scope": "stage_root_generated_mutation_artifacts_and_graph_derived_caches",
            "delete_generated_caches": True,
        },
        "rollback": {
            "disable_path": _ROLLBACK_PATH,
            "fallback": "review_ledger_or_graph_only",
        },
        "validation": validation,
    }
    safe_proof, report = redact_payload(proof)
    if isinstance(safe_proof, dict):
        safe_proof["redaction_summary"] = report
        safe_proof["validation"] = _merge_validation(validation, validate_graph_rollback_proof(safe_proof))
        if safe_proof["validation"]["ok"] is not True:
            safe_proof["status"] = "blocked"
        return safe_proof
    proof["validation"] = validate_graph_rollback_proof(proof)
    return proof


def validate_graph_rollback_proof(proof: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 30 rollback proof invariants."""

    errors: list[str] = []
    if proof.get("schema_version") != 1:
        errors.append("schema_version")
    if proof.get("artifact_kind") != "project_graph_rollback_proof":
        errors.append("artifact_kind")
    if proof.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if proof.get("restore_prior_digest") is not True:
        errors.append("restore_prior_digest")
    if proof.get("rollback_restores_previous_graph_digest") is not True:
        errors.append("rollback_restores_previous_graph_digest")
    if proof.get("delete_generated_caches") is not True:
        errors.append("delete_generated_caches")
    if proof.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if proof.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    for key in ["pre_graph_digest", "mutated_graph_digest", "restored_graph_digest"]:
        if not str(proof.get(key) or "").startswith("sha256:"):
            errors.append(key)
    deletion = proof.get("generated_cache_deletion") if isinstance(proof.get("generated_cache_deletion"), dict) else {}
    if deletion.get("delete_generated_caches") is not True:
        errors.append("generated_cache_deletion:delete_generated_caches")
    if not isinstance(deletion.get("targets_checked"), list) or MUTATION_PLAN_TARGET not in deletion.get("targets_checked", []):
        errors.append("generated_cache_deletion:targets_checked")
    if _has_unsafe_text(proof):
        errors.append("source_boundary:unsafe_text")
    errors.extend(f"redaction:{error}" for error in validate_redaction(json.dumps(proof, sort_keys=True, default=str)))
    return _validation(not errors, sorted(set(errors)), "graph_rollback_proof")


def stage_canonical_graph_mutation(
    graph_artifact: str | Path,
    review_ledger_artifact: str | Path,
    proposal_diff_artifact: str | Path,
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path | None,
) -> dict[str, Any]:
    """Stage Batch 30 dry-run plan, mutated graph copy, journal and rollback proof."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    graph = load_graph_artifact(graph_artifact)
    review_ledger = _load_json_file(review_ledger_artifact)
    proposal_diff = _load_json_file(proposal_diff_artifact)
    governance = _load_json_file(governance_artifact) if governance_artifact else None
    plan = build_canonical_mutation_plan(
        graph,
        review_ledger=review_ledger,
        proposal_diff=proposal_diff,
        approval=approval,
        governance_packet=governance,
    )
    result: dict[str, Any] | None = None
    rollback_proof: dict[str, Any] | None = None
    action = "blocked"
    journal_action = "blocked"
    validation = plan.get("validation")
    if plan.get("status") == "ready" and plan.get("validation", {}).get("ok") is True:
        result = apply_accepted_mutations_to_graph(graph, plan)
        rollback_proof = build_graph_rollback_proof(
            graph,
            result.get("mutated_graph", {}),
            result.get("journal_entries", []) if isinstance(result.get("journal_entries"), list) else [],
        )
        validation = _merge_validation(
            plan.get("validation", {}),
            result.get("validation", {}),
            rollback_proof.get("validation", {}),
        )
        if (
            result.get("status") == "ready"
            and rollback_proof.get("status") == "ready"
            and validation.get("ok") is True
        ):
            plan_target = stage_path / MUTATION_PLAN_TARGET
            mutated_target = stage_path / MUTATED_GRAPH_TARGET
            journal_target = stage_path / MUTATION_JOURNAL_TARGET
            rollback_target = stage_path / ROLLBACK_PROOF_TARGET
            plan_target.parent.mkdir(parents=True, exist_ok=True)
            plan_target.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
            mutated_target.write_text(json.dumps(result["mutated_graph"], indent=2, sort_keys=True), encoding="utf-8")
            _append_journal_entries(journal_target, result["journal_entries"])
            rollback_target.write_text(json.dumps(rollback_proof, indent=2, sort_keys=True), encoding="utf-8")
            action = "create"
            journal_action = "append"
    return {
        "rendered_artifacts": {
            "status": "ready" if action == "create" else plan.get("status"),
            "mode": "build-canonical-mutation",
            "root_status": "redacted",
            "source_boundary": _SOURCE_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "canonical_graph_mutation": "stage_root_generated_graph_copy_only" if action == "create" else "dry_run_only",
            "mutation_plan_required_for_apply": True,
            "only_accepted_proposals_mutate_graph": True,
            "accepted_gap_remains_non_mutating": True,
            "rollback_restores_previous_graph_digest": (
                rollback_proof.get("rollback_restores_previous_graph_digest") if isinstance(rollback_proof, dict) else False
            ),
            "files": [
                _file_record(MUTATION_PLAN_TARGET, action, "staged_only" if action == "create" else "blocked"),
                _file_record(MUTATED_GRAPH_TARGET, action, "staged_only" if action == "create" else "blocked"),
                _file_record(MUTATION_JOURNAL_TARGET, journal_action, "append_only" if journal_action == "append" else "blocked"),
                _file_record(ROLLBACK_PROOF_TARGET, action, "staged_only" if action == "create" else "blocked"),
            ],
            "rollback": {"disable_path": _ROLLBACK_PATH},
            "validation": validation,
        }
    }


def disable_canonical_graph_mutation(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 30 artifacts and graph-derived caches under stage root."""

    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    _validate_stage_boundary(stage_path, workspace_path)
    deleted: list[str] = []
    remaining: list[str] = []
    for relative in _GENERATED_CACHE_TARGETS:
        target = stage_path / relative
        if target.exists() and target.is_file():
            target.unlink()
            deleted.append(relative)
        if target.exists():
            remaining.append(relative)
    return {
        "rendered_artifacts": {
            "status": "disabled" if not remaining else "blocked",
            "mode": "disable-canonical-mutation",
            "root_status": "redacted",
            "fallback": "review_ledger_or_graph_only",
            "deletion_proof": {
                "targets_checked": list(_GENERATED_CACHE_TARGETS),
                "deleted": deleted,
                "remaining": remaining,
                "deletion_scope": "stage_root_generated_mutation_artifacts_and_graph_derived_caches",
                "delete_generated_caches": True,
            },
            "files": [
                _file_record(relative, "delete_if_present", "stage_generated_file_only")
                for relative in _GENERATED_CACHE_TARGETS
            ],
            "rollback": {"disable_path": _ROLLBACK_PATH},
        }
    }


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["canonical_mutation_approval:governance_packet:missing"]
    errors: list[str] = []
    if governance_packet.get("status") != "ready":
        errors.append("canonical_mutation_approval:governance_packet:not_ready")
    if validate_live_governance_packet(governance_packet).get("ok") is not True:
        errors.append("canonical_mutation_approval:governance_packet:invalid")
    provider_policy = governance_packet.get("provider_policy") if isinstance(governance_packet.get("provider_policy"), dict) else {}
    if provider_policy.get("requires_batch_specific_approval") is not True:
        errors.append("canonical_mutation_approval:governance_packet:batch_specific_approval")
    return errors


def _validate_mutation_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["canonical_mutation_approval:mutation_policy"]
    required_true = [
        "dry_run_required",
        "conflict_check_required",
        "graph_digest_check_required",
        "accepted_only",
        "stage_root_only",
        "review_ledger_required",
        "proposal_diff_required",
    ]
    return [f"canonical_mutation_approval:mutation_policy:{field}" for field in required_true if policy.get(field) is not True]


def _validate_journal_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["canonical_mutation_approval:journal_policy"]
    required_true = ["append_only", "jsonl_required", "inverse_patch_required"]
    return [f"canonical_mutation_approval:journal_policy:{field}" for field in required_true if policy.get(field) is not True]


def _validate_rollback_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["canonical_mutation_approval:rollback_policy"]
    required_true = ["restore_prior_digest", "delete_generated_caches", "stage_root_only", "rollback_proof_required"]
    return [f"canonical_mutation_approval:rollback_policy:{field}" for field in required_true if policy.get(field) is not True]


def _validate_data_classification(classification: Any) -> list[str]:
    if not isinstance(classification, dict):
        return ["canonical_mutation_approval:data_classification"]
    allowed = {str(item) for item in classification.get("allowed_inputs", []) if isinstance(item, str)}
    forbidden = {str(item) for item in classification.get("forbidden_inputs", []) if isinstance(item, str)}
    errors = [f"canonical_mutation_approval:data_classification:{field}" for field in sorted(_FORBIDDEN_INPUTS - forbidden)]
    if not allowed:
        errors.append("canonical_mutation_approval:data_classification:allowed_inputs")
    return errors


def _validate_input_fingerprints(
    graph: dict[str, Any],
    review_ledger: dict[str, Any],
    proposal_diff: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    graph_digest = graph_content_fingerprint(_redacted_dict(graph))
    ledger_graph = review_ledger.get("input_fingerprints", {}).get("graph")
    diff_graph = proposal_diff.get("graph_fingerprint")
    if ledger_graph and ledger_graph != graph_digest:
        errors.append("review_ledger:graph_fingerprint:mismatch")
    if diff_graph != graph_digest:
        errors.append("proposal_diff:graph_fingerprint:mismatch")
    ledger_diff = proposal_diff.get("review_ledger_fingerprint")
    if ledger_diff and ledger_diff != _artifact_fingerprint(review_ledger):
        errors.append("proposal_diff:review_ledger_fingerprint:mismatch")
    return _validation(not errors, errors, "mutation_input_fingerprints")


def _validate_accepted_entries_have_diff(review_ledger: dict[str, Any], proposal_diff: dict[str, Any]) -> dict[str, Any]:
    accepted_ids = {
        str(entry.get("proposal_id") or "")
        for entry in review_ledger.get("review_entries", [])
        if isinstance(entry, dict) and entry.get("decision") == "accepted"
    }
    diff_ids = {
        str(item.get("proposal_id") or "")
        for items in (proposal_diff.get("diff") or {}).values()
        if isinstance(items, list)
        for item in items
        if isinstance(item, dict)
    }
    missing = sorted(accepted_ids - diff_ids)
    return _validation(not missing, [f"accepted_proposal_missing_diff:{proposal_id}" for proposal_id in missing], "accepted_entries")


def _planned_operations(proposal_diff: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    change_set = proposal_diff.get("diff") if isinstance(proposal_diff.get("diff"), dict) else {}
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for key, operation_type in [
        ("added_nodes", "add_node"),
        ("added_edges", "add_edge"),
        ("rationale_comments", "add_rationale_comment"),
    ]:
        records = change_set.get(key, [])
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            decision = sanitize_graph_text(record.get("review_decision") or "")
            proposal_id = sanitize_graph_text(record.get("proposal_id") or "")
            if decision != "accepted":
                skipped.append(
                    {
                        "proposal_id": proposal_id,
                        "proposal_kind": sanitize_graph_text(record.get("proposal_kind") or ""),
                        "review_decision": decision,
                        "reason": "accepted_gap_not_mutation_eligible" if decision == "accepted_gap" else "not_accepted",
                    }
                )
                continue
            operation = _operation_from_preview(record, operation_type)
            if operation:
                operations.append(operation)
    return operations, skipped


def _operation_from_preview(record: dict[str, Any], operation_type: str) -> dict[str, Any]:
    proposal_id = sanitize_graph_text(record.get("proposal_id") or "")
    evidence_refs = _safe_string_list(record.get("evidence_refs"))[:10]
    source_node_id = sanitize_graph_text(record.get("source_node_id") or "")
    target_node_id = sanitize_graph_text(record.get("target_node_id") or "")
    operation_id = f"mutation:{operation_type}:{_short_hash(proposal_id)}"
    base = {
        "operation_id": operation_id,
        "operation": operation_type,
        "proposal_id": proposal_id,
        "proposal_kind": sanitize_graph_text(record.get("proposal_kind") or ""),
        "review_decision": "accepted",
        "evidence_refs": evidence_refs,
        "source_node_id": source_node_id,
        "target_node_id": target_node_id,
        "rollback_patch_present": True,
    }
    if operation_type == "add_node":
        node_id = f"generated:semantic-node:{_short_hash(proposal_id)}"
        return {
            **base,
            "node": {
                "id": node_id,
                "type": "generated_artifact",
                "label": sanitize_graph_text(record.get("label") or proposal_id)[:120],
                "status": "generated",
                "language": "unknown",
                "observation_ids": evidence_refs,
            },
            "inverse_patch": {"operation": "delete_node", "node_id": node_id},
        }
    if operation_type == "add_edge":
        edge_id = f"accepted:semantic-edge:{_short_hash(proposal_id)}"
        return {
            **base,
            "edge": {
                "id": edge_id,
                "type": "references",
                "source": source_node_id,
                "target": target_node_id,
                "confidence": "inferred",
                "status": "generated",
                "observation_ids": evidence_refs,
            },
            "inverse_patch": {"operation": "delete_edge", "edge_id": edge_id},
        }
    comment_id = f"accepted:rationale-comment:{_short_hash(proposal_id)}"
    return {
        **base,
        "comment": {
            "id": comment_id,
            "source_node_id": source_node_id,
            "summary": sanitize_graph_text(record.get("rationale") or record.get("label") or proposal_id)[:240],
            "evidence_refs": evidence_refs,
            "status": "generated",
        },
        "inverse_patch": {"operation": "delete_rationale_comment", "comment_id": comment_id},
    }


def _conflict_errors(graph: dict[str, Any], operations: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    node_ids = {str(node.get("id") or "") for node in graph.get("nodes", []) if isinstance(node, dict)}
    edge_ids = {str(edge.get("id") or "") for edge in graph.get("edges", []) if isinstance(edge, dict)}
    observation_ids = {str(obs.get("id") or "") for obs in graph.get("observations", []) if isinstance(obs, dict)}
    operation_ids: set[str] = set()
    planned_node_ids: set[str] = set()
    planned_edge_ids: set[str] = set()
    for operation in operations:
        operation_id = str(operation.get("operation_id") or "")
        if operation_id in operation_ids:
            errors.append("operation:duplicate")
        operation_ids.add(operation_id)
        evidence_refs = {str(item) for item in operation.get("evidence_refs", []) if item}
        if not evidence_refs:
            errors.append(f"{operation_id}:evidence_refs:missing")
        if not evidence_refs.issubset(observation_ids):
            errors.append(f"{operation_id}:evidence_refs:unknown")
        if operation.get("operation") == "add_node":
            node = operation.get("node") if isinstance(operation.get("node"), dict) else {}
            node_id = str(node.get("id") or "")
            if node_id in node_ids or node_id in planned_node_ids:
                errors.append(f"{operation_id}:node:duplicate")
            planned_node_ids.add(node_id)
        if operation.get("operation") == "add_edge":
            edge = operation.get("edge") if isinstance(operation.get("edge"), dict) else {}
            edge_id = str(edge.get("id") or "")
            if edge_id in edge_ids or edge_id in planned_edge_ids:
                errors.append(f"{operation_id}:edge:duplicate")
            planned_edge_ids.add(edge_id)
            all_nodes = node_ids | planned_node_ids
            if str(edge.get("source") or "") not in all_nodes:
                errors.append(f"{operation_id}:edge:source")
            if str(edge.get("target") or "") not in all_nodes:
                errors.append(f"{operation_id}:edge:target")
        if operation.get("operation") == "add_rationale_comment":
            comment = operation.get("comment") if isinstance(operation.get("comment"), dict) else {}
            if str(comment.get("source_node_id") or "") not in node_ids:
                errors.append(f"{operation_id}:comment:source_node")
    return sorted(set(errors))


def _validate_operation(operation: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(operation, dict):
        return ["operation:shape"]
    if operation.get("operation") not in {"add_node", "add_edge", "add_rationale_comment"}:
        errors.append("operation:unknown")
    if operation.get("review_decision") != "accepted":
        errors.append("operation:review_decision")
    if not operation.get("proposal_id") or not operation.get("operation_id"):
        errors.append("operation:identity")
    if not operation.get("evidence_refs"):
        errors.append("operation:evidence_refs")
    if not isinstance(operation.get("inverse_patch"), dict):
        errors.append("operation:inverse_patch")
    if operation.get("rollback_patch_present") is not True:
        errors.append("operation:rollback_patch_present")
    return errors


def _apply_operations_with_journal(
    graph: dict[str, Any],
    operations: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    current = _json_copy(graph)
    journal_entries: list[dict[str, Any]] = []
    for sequence, operation in enumerate(operations, start=1):
        before_digest = graph_content_fingerprint(_redacted_dict(current))
        current = _apply_single_operation(current, operation)
        after_digest = graph_content_fingerprint(_redacted_dict(current))
        journal_entries.append(
            {
                "schema_version": 1,
                "artifact_kind": "project_graph_mutation_journal",
                "journal_format": "jsonl",
                "append_only": True,
                "sequence": sequence,
                "approval_boundary": _APPROVAL_BOUNDARY,
                "source_boundary": _SOURCE_BOUNDARY,
                "provider_call_allowed": False,
                "external_call_performed": False,
                "operation_id": operation.get("operation_id"),
                "operation": operation.get("operation"),
                "proposal_id": operation.get("proposal_id"),
                "review_decision": "accepted",
                "graph_digest_before": before_digest,
                "graph_digest_after": after_digest,
                "versioned_graph_digest_after": _versioned_digest(after_digest),
                "inverse_patch": operation.get("inverse_patch"),
                "rollback_patch_present": True,
            }
        )
    current["validation"] = validate_graph_schema(current)
    return current, journal_entries


def _apply_operations_to_graph(graph: dict[str, Any], operations: list[dict[str, Any]]) -> dict[str, Any]:
    current = _json_copy(graph)
    for operation in operations:
        current = _apply_single_operation(current, operation)
    current["validation"] = validate_graph_schema(current)
    return current


def _apply_single_operation(graph: dict[str, Any], operation: dict[str, Any]) -> dict[str, Any]:
    updated = _json_copy(graph)
    kind = operation.get("operation")
    if kind == "add_node":
        updated.setdefault("nodes", []).append(_json_copy(operation["node"]))
    elif kind == "add_edge":
        updated.setdefault("edges", []).append(_json_copy(operation["edge"]))
    elif kind == "add_rationale_comment":
        metadata = updated.setdefault("metadata", {})
        comments = metadata.setdefault("rationale_comments", [])
        comments.append(_json_copy(operation["comment"]))
    updated["nodes"] = sorted(updated.get("nodes", []), key=lambda item: str(item.get("id") or ""))
    updated["edges"] = sorted(updated.get("edges", []), key=lambda item: str(item.get("id") or ""))
    metadata = updated.get("metadata") if isinstance(updated.get("metadata"), dict) else {}
    metadata["node_count"] = len(updated.get("nodes", []))
    metadata["edge_count"] = len(updated.get("edges", []))
    return updated


def _apply_inverse_patch(graph: dict[str, Any], patch: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    updated = _json_copy(graph)
    errors: list[str] = []
    operation = patch.get("operation")
    if operation == "delete_node":
        node_id = str(patch.get("node_id") or "")
        updated["nodes"] = [node for node in updated.get("nodes", []) if not (isinstance(node, dict) and node.get("id") == node_id)]
    elif operation == "delete_edge":
        edge_id = str(patch.get("edge_id") or "")
        updated["edges"] = [edge for edge in updated.get("edges", []) if not (isinstance(edge, dict) and edge.get("id") == edge_id)]
    elif operation == "delete_rationale_comment":
        comment_id = str(patch.get("comment_id") or "")
        metadata = updated.get("metadata") if isinstance(updated.get("metadata"), dict) else {}
        comments = metadata.get("rationale_comments", [])
        if isinstance(comments, list):
            metadata["rationale_comments"] = [
                comment
                for comment in comments
                if not (isinstance(comment, dict) and comment.get("id") == comment_id)
            ]
            if not metadata["rationale_comments"]:
                metadata.pop("rationale_comments", None)
    else:
        errors.append("inverse_patch:operation")
    metadata = updated.get("metadata") if isinstance(updated.get("metadata"), dict) else {}
    metadata["node_count"] = len(updated.get("nodes", []))
    metadata["edge_count"] = len(updated.get("edges", []))
    updated["validation"] = validate_graph_schema(updated)
    return updated, errors


def _append_journal_entries(target: Path, entries: list[dict[str, Any]]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as stream:
        for entry in entries:
            stream.write(json.dumps(entry, sort_keys=True) + "\n")


def _blocked_mutation_result(validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_canonical_mutation_result",
        "write_policy": "staged_only",
        "status": "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "canonical_graph_mutation": "blocked",
        "accepted_for_canonical_graph": False,
        "validation": validation,
    }


def _approval_required_plan(validation: dict[str, Any], pre_graph_digest: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_canonical_mutation_plan",
        "write_policy": "dry_run_only",
        "status": "approval_required",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": _SOURCE_BOUNDARY,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "canonical_graph_mutation": "forbidden_until_batch30_approval",
        "no_mutation_without_dry_run_plan": True,
        "mutation_plan_required_for_apply": True,
        "only_accepted_proposals_mutate_graph": True,
        "input_fingerprints": {"graph": pre_graph_digest},
        "validation": validation,
        "safe_next_action": "Provide explicit Batch 30 approval, governance, review ledger and proposal diff before dry-run apply.",
    }


def _file_record(relative: str, action: str, write_policy: str) -> dict[str, str]:
    return {
        "target_path": relative,
        "action": action,
        "write_policy": write_policy,
        "staged_path": relative,
    }


def _load_json_file(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("artifact must be a JSON object")
    return payload


def _validate_stage_boundary(stage_path: Path, workspace_path: Path) -> None:
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise ValueError("stage output directory must be outside workspace")
    if stage_path.exists() and not stage_path.is_dir():
        raise ValueError("stage output path is not a directory")


def _artifact_fingerprint(payload: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(_redacted_dict(payload), sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _redacted_dict(payload: dict[str, Any]) -> dict[str, Any]:
    safe_payload, _report = redact_payload(payload)
    return safe_payload if isinstance(safe_payload, dict) else {}


def _versioned_digest(digest: str) -> str:
    return f"graph-v1@{digest}"


def _short_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _json_copy(payload: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(payload, sort_keys=True, default=str))


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [sanitize_graph_text(item) for item in value if sanitize_graph_text(item)]


def _merge_validation(*validations: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    checks: list[str] = []
    for validation in validations:
        if not isinstance(validation, dict):
            continue
        errors.extend(str(error) for error in validation.get("errors", []) if error)
        checks.extend(str(check) for check in validation.get("checks", []) if check)
    return {"ok": not errors, "checks": sorted(set(checks)), "errors": sorted(set(errors))}


def _validation(ok: bool, errors: list[str], check: str) -> dict[str, Any]:
    return {"ok": ok, "checks": [check], "errors": sorted(set(errors))}


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
        return bool(_WINDOWS_PATH_PATTERN.search(value) or _POSIX_PATH_PATTERN.search(value) or _SECRET_VALUE_PATTERN.search(value))
    return False
