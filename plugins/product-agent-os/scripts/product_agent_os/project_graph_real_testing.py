"""Real testing readiness and pilot packets for live graph work.

Batch 32 prepares approved target selection and reproducible pilot evidence.
It does not start a server, call providers, mutate canonical graph facts or
write to a target workspace. All artifacts are generated evidence staged under
an explicit stage root.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_live_audit import (
    validate_agent_skill_handoff_routing_packet,
    validate_live_audit_event_log,
    validate_runtime_observability_packet,
    validate_security_privacy_test_packet,
)
from product_agent_os.project_graph_live_governance import validate_live_governance_packet
from product_agent_os.project_graph_live_runtime import validate_live_runtime_contract
from product_agent_os.project_graph_sanitization import sanitize_graph_text


REAL_TESTING_READINESS_TARGET = ".codex/product-agent-os/project-code-graph-real-testing-readiness.json"
REAL_TESTING_TARGETS_TARGET = ".codex/product-agent-os/project-code-graph-real-testing-targets.json"
PILOT_HARNESS_TARGET = ".codex/product-agent-os/project-code-graph-pilot-harness.json"
CODEX_SURFACE_SMOKE_TARGET = ".codex/product-agent-os/project-code-graph-codex-surface-smoke.json"
PILOT_MATRIX_TARGET = ".codex/product-agent-os/project-code-graph-real-testing-pilot-matrix.json"

_APPROVAL_BOUNDARY = "batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke"
_ROLLBACK_PATH = "delete generated Batch 32 real testing readiness and pilot artifacts under stage root"
_BATCH32_ALLOWED_SURFACES = {
    "codex_surface_smoke",
    "pilot_harness",
    "real_project_target_selection",
    "real_testing_readiness",
    "use_case_pilot_matrix",
}
_REQUIRED_GATES = {
    "audit_operability",
    "canonical_graph_mutation",
    "external_embedding",
    "external_llm",
    "external_reranker",
    "human_review_ledger",
    "live_governance",
    "live_runtime",
}
_CLOSED_GATE_STATUSES = {
    "accepted_gap",
    "blocked_by_missing_approval",
    "explicitly_disabled",
    "implemented_verified",
}
_REQUIRED_CODEX_SURFACES = {"Codex App", "CLI", "IDE extension"}
_SURFACE_STATUSES = {"accepted_gap", "blocked", "planned_smoke", "passed"}
_REQUIRED_ARCHETYPES = {"web", "backend", "docs", "pr_review", "evals", "automation", "ai_rag"}
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_PROMPT_INJECTION_PATTERN = re.compile(
    r"(?i)(ignore previous instructions|exfiltrate|reveal secrets|system prompt|developer message)"
)


def validate_real_testing_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 32 approval and Batch 24 governance evidence."""

    if not isinstance(approval, dict):
        return _validation(False, ["real_testing_approval:missing"], "real_testing_approval")
    errors: list[str] = []
    required_fields = {
        "explicit_approval",
        "owner",
        "allowed_surfaces",
        "readiness_policy",
        "target_policy",
        "pilot_harness_policy",
        "surface_smoke_policy",
        "pilot_matrix_policy",
        "rollback_path",
        "residual_risks",
    }
    errors.extend(f"real_testing_approval:{field}:missing" for field in sorted(required_fields - set(approval)))
    if approval.get("explicit_approval") is not True:
        errors.append("real_testing_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("real_testing_approval:owner")
    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH32_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"real_testing_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH32_ALLOWED_SURFACES):
        errors.append(f"real_testing_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_readiness_policy(approval.get("readiness_policy")))
    errors.extend(_validate_target_policy(approval.get("target_policy")))
    errors.extend(_validate_pilot_harness_policy(approval.get("pilot_harness_policy")))
    errors.extend(_validate_surface_smoke_policy(approval.get("surface_smoke_policy")))
    errors.extend(_validate_pilot_matrix_policy(approval.get("pilot_matrix_policy")))
    if approval.get("rollback_path") != _ROLLBACK_PATH:
        errors.append("real_testing_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("real_testing_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("real_testing_approval:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "real_testing_approval")


def build_real_testing_readiness_packet(
    *,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
    runtime_contract: dict[str, Any] | None,
    audit_operability: dict[str, Any] | None,
    gate_statuses: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Build Batch 32 real-testing entry/exit criteria and gate status evidence."""

    approval_validation = validate_real_testing_approval(approval, governance_packet)
    runtime_validation = _validate_runtime_prerequisite(runtime_contract)
    audit_validation = _validate_audit_operability(audit_operability)
    gate_validation = _validate_gate_statuses(gate_statuses)
    validation = _merge_validation(approval_validation, runtime_validation, audit_validation, gate_validation)
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_real_testing_readiness",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": REAL_TESTING_READINESS_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Provide Batch 32 approval before real-testing readiness evidence.",
        }

    gate_map = _gate_map(gate_statuses)
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_real_testing_readiness",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "redacted_gate_status_and_operability_metadata_only_no_raw_source",
        "generated_view_policy": "real_testing_readiness_is_generated_evidence_not_source_of_truth",
        "target": REAL_TESTING_READINESS_TARGET,
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "real_testing_start_policy": "approved_targets_only",
        "entry_criteria": [
            "Batch 24 live governance ready",
            "Batch 25 runtime contract ready or explicitly disabled",
            "Batch 31 audit/security/observability/handoff evidence ready",
            "Every Track 10 live/provider/mutation gate is closed, blocked, disabled or owner-accepted",
            "Target consent names owner, data policy and allowed commands",
        ],
        "exit_criteria": [
            "Pilot harness produces reproducible dry-run evidence",
            "Codex App, CLI and IDE extension smoke are planned, blocked or accepted gaps",
            "Use-case pilot matrix maps enabled surfaces to Track 8 archetypes",
            "No unapproved live server, provider call, canonical mutation or git action occurs",
        ],
        "accepted_gap_policy": "accepted_gaps_require_owner_and_risk_note",
        "gate_statuses": [
            {"gate": gate, "status": gate_map[gate]} for gate in sorted(gate_map)
        ],
        "no_hidden_unresolved_track10_gates": validation.get("ok") is True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Select approved target classes and run only staged dry-run pilot evidence.",
    }
    return _redacted_packet(packet, validate_real_testing_readiness_packet)


def validate_real_testing_readiness_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 32 readiness packet invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_real_testing_readiness":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    if packet.get("status") == "ready" and packet.get("no_hidden_unresolved_track10_gates") is not True:
        errors.append("no_hidden_unresolved_track10_gates")
    gate_map = _gate_map(packet.get("gate_statuses"))
    missing = sorted(_REQUIRED_GATES - set(gate_map))
    errors.extend(f"gate_statuses:{gate}:missing" for gate in missing)
    errors.extend(
        f"gate_statuses:{gate}:unresolved"
        for gate, status in sorted(gate_map.items())
        if status not in _CLOSED_GATE_STATUSES
    )
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_real_testing_readiness")


def build_real_project_target_selection_packet(
    *,
    targets: list[dict[str, Any]] | None,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build owner-approved target selection evidence for real testing."""

    approval_validation = validate_real_testing_approval(approval, governance_packet)
    target_items = [_target_entry(target, index) for index, target in enumerate(targets or [])]
    target_validation = _validate_target_entries(target_items)
    validation = _merge_validation(approval_validation, target_validation)
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_real_testing_targets",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": REAL_TESTING_TARGETS_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "targets": [],
            "validation": validation,
            "safe_next_action": "Provide Batch 32 approval before selecting real-testing targets.",
        }
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_real_testing_targets",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "owner_target_metadata_only_no_raw_source_or_private_data",
        "generated_view_policy": "target_selection_is_generated_evidence_not_source_of_truth",
        "target": REAL_TESTING_TARGETS_TARGET,
        "owner_approved_target_and_data_policy_required": True,
        "production_targets_blocked_without_separate_approval": True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "target_classes": sorted({item["target_id"] for item in target_items}),
        "targets": target_items,
        "validation": validation,
        "safe_next_action": "Run pilots only against owner-approved target classes and allowed commands.",
    }
    return _redacted_packet(packet, validate_real_project_target_selection_packet)


def validate_real_project_target_selection_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate target consent and data policy evidence."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_real_testing_targets":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("owner_approved_target_and_data_policy_required") is not True:
        errors.append("owner_approved_target_and_data_policy_required")
    if packet.get("production_targets_blocked_without_separate_approval") is not True:
        errors.append("production_targets_blocked_without_separate_approval")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    errors.extend(
        _validate_target_entries(packet.get("targets") if isinstance(packet.get("targets"), list) else []).get(
            "errors", []
        )
    )
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_real_testing_targets")


def build_end_to_end_pilot_harness_packet(
    *,
    readiness_packet: dict[str, Any],
    target_packet: dict[str, Any],
    approval: dict[str, Any] | None,
    pilot_steps: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Build a reproducible dry-run pilot harness packet."""

    readiness_validation = validate_real_testing_readiness_packet(readiness_packet)
    target_validation = validate_real_project_target_selection_packet(target_packet)
    steps = [_pilot_step(step, index) for index, step in enumerate(pilot_steps or [])]
    step_validation = _validate_pilot_steps(steps)
    validation = _merge_validation(readiness_validation, target_validation, step_validation)
    if approval is None or readiness_packet.get("status") == "approval_required":
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_pilot_harness",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": PILOT_HARNESS_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Prepare readiness and target consent before pilot harness evidence.",
        }
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_pilot_harness",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "scripted_command_classes_only_no_raw_source_or_private_data",
        "generated_view_policy": "pilot_harness_is_generated_evidence_not_source_of_truth",
        "target": PILOT_HARNESS_TARGET,
        "dry_run_only": True,
        "target_file_mutation_allowed_only_if_approved": True,
        "mutation_policy": "no_target_file_mutation_without_explicit_target_approval",
        "reproducible_pilot": True,
        "pilot_steps": [step["step_id"] for step in steps],
        "step_packets": steps,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Run this harness only as dry-run/staged evidence until target owner approves execution.",
    }
    return _redacted_packet(packet, validate_end_to_end_pilot_harness_packet)


def validate_end_to_end_pilot_harness_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate pilot harness invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_pilot_harness":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("dry_run_only") is not True:
        errors.append("dry_run_only")
    if packet.get("target_file_mutation_allowed_only_if_approved") is not True:
        errors.append("target_file_mutation_allowed_only_if_approved")
    if packet.get("mutation_policy") != "no_target_file_mutation_without_explicit_target_approval":
        errors.append("mutation_policy")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    step_ids = set(packet.get("pilot_steps") if isinstance(packet.get("pilot_steps"), list) else [])
    for required in ["scan_project_code_graph_dry_run", "graph_only_fallback"]:
        if required not in step_ids:
            errors.append(f"pilot_steps:{required}:missing")
    for step in packet.get("step_packets", []):
        if not isinstance(step, dict):
            errors.append("pilot_step:type")
            continue
        if step.get("mutates_target") is not False:
            errors.append(f"pilot_step:{step.get('step_id')}:mutates_target")
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_pilot_harness")


def build_codex_surface_smoke_plan(
    *,
    readiness_packet: dict[str, Any],
    surfaces: list[dict[str, Any]] | None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build Codex App, CLI and IDE extension smoke planning evidence."""

    readiness_validation = validate_real_testing_readiness_packet(readiness_packet)
    surface_items = [_surface_entry(surface, index) for index, surface in enumerate(surfaces or [])]
    surface_validation = _validate_surface_entries(surface_items)
    validation = _merge_validation(readiness_validation, surface_validation)
    if approval is None or readiness_packet.get("status") == "approval_required":
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_codex_surface_smoke",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": CODEX_SURFACE_SMOKE_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Prepare readiness before Codex surface smoke evidence.",
        }
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_codex_surface_smoke",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "surface_smoke_metadata_only_no_external_actions",
        "generated_view_policy": "codex_surface_smoke_is_generated_evidence_not_source_of_truth",
        "target": CODEX_SURFACE_SMOKE_TARGET,
        "surfaces": surface_items,
        "missing_surface_recorded_as_gap_or_blocked": validation.get("ok") is True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Record smoke evidence per Codex surface without claiming unavailable surfaces work.",
    }
    return _redacted_packet(packet, validate_codex_surface_smoke_plan)


def validate_codex_surface_smoke_plan(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Codex surface smoke evidence."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_codex_surface_smoke":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("missing_surface_recorded_as_gap_or_blocked") is not True and packet.get("status") == "ready":
        errors.append("missing_surface_recorded_as_gap_or_blocked")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    errors.extend(
        _validate_surface_entries(packet.get("surfaces") if isinstance(packet.get("surfaces"), list) else []).get(
            "errors", []
        )
    )
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_codex_surface_smoke")


def build_use_case_pilot_matrix(
    *,
    readiness_packet: dict[str, Any],
    smoke_plan: dict[str, Any],
    pilots: list[dict[str, Any]] | None,
    approval: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build Track 8 use-case archetype pilot matrix evidence."""

    readiness_validation = validate_real_testing_readiness_packet(readiness_packet)
    smoke_validation = validate_codex_surface_smoke_plan(smoke_plan)
    pilot_items = [_pilot_matrix_entry(pilot, index) for index, pilot in enumerate(pilots or [])]
    matrix_validation = _validate_pilot_matrix_entries(pilot_items, smoke_plan)
    validation = _merge_validation(readiness_validation, smoke_validation, matrix_validation)
    if approval is None or readiness_packet.get("status") == "approval_required":
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_real_testing_pilot_matrix",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": PILOT_MATRIX_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Prepare readiness and smoke plan before use-case pilot matrix evidence.",
        }
    archetypes = sorted({item["archetype"] for item in pilot_items})
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_real_testing_pilot_matrix",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "track8_archetype_mapping_metadata_only",
        "generated_view_policy": "pilot_matrix_is_generated_evidence_not_source_of_truth",
        "target": PILOT_MATRIX_TARGET,
        "use_case_archetypes": archetypes,
        "pilots": pilot_items,
        "each_enabled_surface_has_pilot_or_accepted_gap": validation.get("ok") is True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Use this matrix to choose real testing runs after target owner approval.",
    }
    return _redacted_packet(packet, validate_use_case_pilot_matrix)


def validate_use_case_pilot_matrix(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate use-case pilot matrix coverage."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_real_testing_pilot_matrix":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    archetypes = set(packet.get("use_case_archetypes") if isinstance(packet.get("use_case_archetypes"), list) else [])
    for required in sorted(_REQUIRED_ARCHETYPES - archetypes):
        errors.append(f"use_case_archetypes:{required}:missing")
    if packet.get("each_enabled_surface_has_pilot_or_accepted_gap") is not True and packet.get("status") == "ready":
        errors.append("each_enabled_surface_has_pilot_or_accepted_gap")
    errors.extend(
        _validate_pilot_matrix_entries(
            packet.get("pilots") if isinstance(packet.get("pilots"), list) else []
        ).get("errors", [])
    )
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_real_testing_pilot_matrix")


def stage_real_testing_readiness(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path,
    runtime_artifact: str | Path,
    audit_operability_artifact: str | Path,
    targets: list[dict[str, Any]] | None = None,
    gate_statuses: list[dict[str, Any]] | None = None,
    pilot_steps: list[dict[str, Any]] | None = None,
    surfaces: list[dict[str, Any]] | None = None,
    pilots: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Stage Batch 32 readiness, target, harness, smoke and pilot matrix artifacts."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")

    governance = _load_json(governance_artifact)
    runtime = _load_json(runtime_artifact)
    audit_operability = _load_json(audit_operability_artifact)
    readiness = build_real_testing_readiness_packet(
        approval=approval,
        governance_packet=governance,
        runtime_contract=runtime,
        audit_operability=audit_operability,
        gate_statuses=gate_statuses or [],
    )
    target_packet = build_real_project_target_selection_packet(
        targets=targets or [],
        approval=approval,
        governance_packet=governance,
    )
    harness = build_end_to_end_pilot_harness_packet(
        readiness_packet=readiness,
        target_packet=target_packet,
        approval=approval,
        pilot_steps=pilot_steps or [],
    )
    smoke = build_codex_surface_smoke_plan(readiness_packet=readiness, surfaces=surfaces or [], approval=approval)
    matrix = build_use_case_pilot_matrix(
        readiness_packet=readiness,
        smoke_plan=smoke,
        pilots=pilots or [],
        approval=approval,
    )

    _write_json(stage_path / REAL_TESTING_READINESS_TARGET, readiness)
    _write_json(stage_path / REAL_TESTING_TARGETS_TARGET, target_packet)
    _write_json(stage_path / PILOT_HARNESS_TARGET, harness)
    _write_json(stage_path / CODEX_SURFACE_SMOKE_TARGET, smoke)
    _write_json(stage_path / PILOT_MATRIX_TARGET, matrix)
    status = _aggregate_status([readiness, target_packet, harness, smoke, matrix])
    validation = _merge_validation(
        readiness.get("validation", {}),
        target_packet.get("validation", {}),
        harness.get("validation", {}),
        smoke.get("validation", {}),
        matrix.get("validation", {}),
    )
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "build-real-testing-readiness",
            "status": status,
            "approval_boundary": _APPROVAL_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "files": [
                REAL_TESTING_READINESS_TARGET,
                REAL_TESTING_TARGETS_TARGET,
                PILOT_HARNESS_TARGET,
                CODEX_SURFACE_SMOKE_TARGET,
                PILOT_MATRIX_TARGET,
            ],
            "validation": validation,
        },
    }


def disable_real_testing_readiness(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 32 real-testing artifacts from a stage root."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")
    removed: list[str] = []
    missing: list[str] = []
    for target in [
        REAL_TESTING_READINESS_TARGET,
        REAL_TESTING_TARGETS_TARGET,
        PILOT_HARNESS_TARGET,
        CODEX_SURFACE_SMOKE_TARGET,
        PILOT_MATRIX_TARGET,
    ]:
        path = stage_path / target
        if path.exists():
            path.unlink()
            removed.append(target)
        else:
            missing.append(target)
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "disable-real-testing-readiness",
            "status": "disabled",
            "deletion_proof": {
                "delete_generated_real_testing_artifacts": True,
                "removed": removed,
                "missing": missing,
                "deletion_scope": "stage_root_generated_batch32_real_testing_artifacts_only",
            },
            "fallback": "graph_only_query_mode",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
        },
    }


def _target_entry(target: dict[str, Any], index: int) -> dict[str, Any]:
    allowed_commands = target.get("allowed_commands") if isinstance(target.get("allowed_commands"), list) else []
    return {
        "target_id": sanitize_graph_text(target.get("target_id") or f"target-{index}"),
        "workspace_class": sanitize_graph_text(target.get("workspace_class") or "unknown"),
        "owner": sanitize_graph_text(target.get("owner") or ""),
        "owner_approved": target.get("owner_approved") is True,
        "data_policy": sanitize_graph_text(target.get("data_policy") or ""),
        "allowed_commands": [sanitize_graph_text(command) for command in allowed_commands if isinstance(command, str)],
        "production_data": target.get("production_data") is True,
        "target_file_mutation_allowed": target.get("target_file_mutation_allowed") is True,
        "redacted": True,
    }


def _validate_target_entries(targets: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    if not targets:
        errors.append("targets:missing")
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            errors.append(f"target:{index}:type")
            continue
        for field in ["target_id", "workspace_class", "owner", "data_policy"]:
            if not sanitize_graph_text(target.get(field) or ""):
                errors.append(f"target:{index}:{field}")
        if target.get("owner_approved") is not True:
            errors.append(f"target:{index}:owner_approved")
        if not isinstance(target.get("allowed_commands"), list) or not target.get("allowed_commands"):
            errors.append(f"target:{index}:allowed_commands")
        if target.get("production_data") is True:
            errors.append(f"target:{index}:production_data")
        if _has_unsafe_text(target):
            errors.append(f"target:{index}:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "real_testing_targets")


def _pilot_step(step: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "step_id": sanitize_graph_text(step.get("step_id") or f"step-{index}"),
        "command_class": sanitize_graph_text(step.get("command_class") or "unknown"),
        "mutates_target": step.get("mutates_target") is True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
    }


def _validate_pilot_steps(steps: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    step_ids = {step.get("step_id") for step in steps if isinstance(step, dict)}
    for required in ["scan_project_code_graph_dry_run", "graph_only_fallback"]:
        if required not in step_ids:
            errors.append(f"pilot_steps:{required}:missing")
    for step in steps:
        if step.get("mutates_target") is not False:
            errors.append(f"pilot_step:{step.get('step_id')}:mutates_target")
        if step.get("provider_call_allowed") is not False:
            errors.append(f"pilot_step:{step.get('step_id')}:provider_call_allowed")
        if step.get("external_call_performed") is not False:
            errors.append(f"pilot_step:{step.get('step_id')}:external_call_performed")
        if step.get("live_server_started") is not False:
            errors.append(f"pilot_step:{step.get('step_id')}:live_server_started")
        if step.get("canonical_graph_mutation") != "not_performed":
            errors.append(f"pilot_step:{step.get('step_id')}:canonical_graph_mutation")
    return _validation(not errors, sorted(set(errors)), "pilot_steps")


def _surface_entry(surface: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "surface": sanitize_graph_text(surface.get("surface") or f"surface-{index}"),
        "status": sanitize_graph_text(surface.get("status") or "blocked"),
        "evidence": sanitize_graph_text(surface.get("evidence") or "recorded_gap"),
        "external_action_performed": False,
    }


def _validate_surface_entries(surfaces: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    surface_names = {surface.get("surface") for surface in surfaces if isinstance(surface, dict)}
    for required in sorted(_REQUIRED_CODEX_SURFACES - surface_names):
        errors.append(f"codex_surface:{required}:missing")
    for surface in surfaces:
        if surface.get("status") not in _SURFACE_STATUSES:
            errors.append(f"codex_surface:{surface.get('surface')}:status")
        if not sanitize_graph_text(surface.get("evidence") or ""):
            errors.append(f"codex_surface:{surface.get('surface')}:evidence")
        if surface.get("external_action_performed") is not False:
            errors.append(f"codex_surface:{surface.get('surface')}:external_action_performed")
        if _has_unsafe_text(surface):
            errors.append(f"codex_surface:{surface.get('surface')}:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "codex_surface_smoke")


def _pilot_matrix_entry(pilot: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "archetype": sanitize_graph_text(pilot.get("archetype") or f"archetype-{index}"),
        "surface": sanitize_graph_text(pilot.get("surface") or "CLI"),
        "pilot_id": sanitize_graph_text(pilot.get("pilot_id") or f"pilot-{index}"),
        "status": sanitize_graph_text(pilot.get("status") or "planned"),
    }


def _validate_pilot_matrix_entries(
    pilots: list[dict[str, Any]],
    smoke_plan: dict[str, Any] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    archetypes = {pilot.get("archetype") for pilot in pilots if isinstance(pilot, dict)}
    for required in sorted(_REQUIRED_ARCHETYPES - archetypes):
        errors.append(f"use_case_archetypes:{required}:missing")
    for pilot in pilots:
        if pilot.get("status") not in {"accepted_gap", "blocked", "planned", "passed"}:
            errors.append(f"pilot:{pilot.get('pilot_id')}:status")
        if _has_unsafe_text(pilot):
            errors.append(f"pilot:{pilot.get('pilot_id')}:unsafe_text")
    if isinstance(smoke_plan, dict):
        enabled_surfaces = {
            surface.get("surface")
            for surface in smoke_plan.get("surfaces", [])
            if isinstance(surface, dict) and surface.get("status") not in {"accepted_gap", "blocked"}
        }
        pilot_surfaces = {pilot.get("surface") for pilot in pilots}
        for surface in sorted(enabled_surfaces - pilot_surfaces):
            errors.append(f"enabled_surface:{surface}:pilot_or_gap_missing")
    return _validation(not errors, sorted(set(errors)), "use_case_pilot_matrix")


def _validate_readiness_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["readiness_policy"]
    errors: list[str] = []
    for field in [
        "entry_criteria_required",
        "exit_criteria_required",
        "accepted_gaps_allowed_with_owner",
        "hidden_unresolved_gates_blocked",
    ]:
        if policy.get(field) is not True:
            errors.append(f"readiness_policy:{field}")
    return errors


def _validate_target_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["target_policy"]
    errors: list[str] = []
    for field in [
        "owner_approved_targets_only",
        "data_policy_required",
        "allowed_commands_required",
        "production_targets_blocked_without_separate_approval",
    ]:
        if policy.get(field) is not True:
            errors.append(f"target_policy:{field}")
    return errors


def _validate_pilot_harness_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["pilot_harness_policy"]
    errors: list[str] = []
    for field in [
        "dry_run_first",
        "target_file_mutation_requires_explicit_target_approval",
        "provider_calls_require_batch_approval",
        "fallback_required",
    ]:
        if policy.get(field) is not True:
            errors.append(f"pilot_harness_policy:{field}")
    return errors


def _validate_surface_smoke_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["surface_smoke_policy"]
    errors: list[str] = []
    for field in [
        "codex_app_required",
        "cli_required",
        "ide_extension_required",
        "missing_surface_recorded_as_gap_or_blocked",
    ]:
        if policy.get(field) is not True:
            errors.append(f"surface_smoke_policy:{field}")
    return errors


def _validate_pilot_matrix_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["pilot_matrix_policy"]
    errors: list[str] = []
    required = set(policy.get("track8_archetypes_required", [])) if isinstance(policy.get("track8_archetypes_required"), list) else set()
    for archetype in sorted(_REQUIRED_ARCHETYPES - required):
        errors.append(f"pilot_matrix_policy:track8_archetypes_required:{archetype}:missing")
    if policy.get("enabled_surface_requires_pilot_or_gap") is not True:
        errors.append("pilot_matrix_policy:enabled_surface_requires_pilot_or_gap")
    return errors


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["live_governance:missing"]
    validation = validate_live_governance_packet(governance_packet)
    errors = [f"live_governance:{error}" for error in validation.get("errors", [])]
    if governance_packet.get("status") != "ready":
        errors.append("live_governance:status")
    return sorted(set(errors))


def _validate_runtime_prerequisite(runtime_contract: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(runtime_contract, dict):
        return _validation(False, ["live_runtime:missing"], "live_runtime_prerequisite")
    validation = validate_live_runtime_contract(runtime_contract)
    errors = [f"live_runtime:{error}" for error in validation.get("errors", [])]
    if runtime_contract.get("status") != "ready":
        errors.append("live_runtime:status")
    if runtime_contract.get("provider_call_allowed") is True:
        errors.append("live_runtime:provider_call_allowed")
    if runtime_contract.get("external_call_performed") is True:
        errors.append("live_runtime:external_call_performed")
    if runtime_contract.get("server_contract", {}).get("canonical_mutation_allowed") is not False:
        errors.append("live_runtime:canonical_mutation_allowed")
    return _validation(not errors, sorted(set(errors)), "live_runtime_prerequisite")


def _validate_audit_operability(audit_operability: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(audit_operability, dict):
        return _validation(False, ["audit_operability:missing"], "audit_operability")
    audit_log = audit_operability.get("audit_log") or audit_operability.get("live_audit_log")
    security = audit_operability.get("security_privacy") or audit_operability.get("security_packet")
    observability = audit_operability.get("observability") or audit_operability.get("runtime_observability")
    handoff = audit_operability.get("agent_skill_handoff") or audit_operability.get("handoff")
    validations = [
        _prefixed_validation(validate_live_audit_event_log(audit_log), "audit_log") if isinstance(audit_log, dict) else _validation(False, ["audit_log:missing"], "audit_log"),
        _prefixed_validation(validate_security_privacy_test_packet(security), "security_privacy") if isinstance(security, dict) else _validation(False, ["security_privacy:missing"], "security_privacy"),
        _prefixed_validation(validate_runtime_observability_packet(observability), "runtime_observability") if isinstance(observability, dict) else _validation(False, ["runtime_observability:missing"], "runtime_observability"),
        _prefixed_validation(validate_agent_skill_handoff_routing_packet(handoff), "agent_skill_handoff") if isinstance(handoff, dict) else _validation(False, ["agent_skill_handoff:missing"], "agent_skill_handoff"),
    ]
    readiness_errors: list[str] = []
    for name, packet in [
        ("audit_log", audit_log),
        ("security_privacy", security),
        ("runtime_observability", observability),
        ("agent_skill_handoff", handoff),
    ]:
        if isinstance(packet, dict) and packet.get("status") != "ready":
            readiness_errors.append(f"{name}:status")
    return _merge_validation(*validations, _validation(not readiness_errors, readiness_errors, "audit_operability_status"))


def _validate_gate_statuses(gate_statuses: list[dict[str, Any]] | None) -> dict[str, Any]:
    gate_map = _gate_map(gate_statuses)
    errors: list[str] = []
    for gate in sorted(_REQUIRED_GATES - set(gate_map)):
        errors.append(f"gate_statuses:{gate}:missing")
    for gate, status in sorted(gate_map.items()):
        if status not in _CLOSED_GATE_STATUSES:
            errors.append(f"gate_statuses:{gate}:unresolved")
    return _validation(not errors, sorted(set(errors)), "gate_statuses")


def _gate_map(gate_statuses: Any) -> dict[str, str]:
    if not isinstance(gate_statuses, list):
        return {}
    result: dict[str, str] = {}
    for item in gate_statuses:
        if not isinstance(item, dict):
            continue
        gate = sanitize_graph_text(item.get("gate") or "")
        status = sanitize_graph_text(item.get("status") or "")
        if gate:
            result[gate] = status
    return result


def _redacted_packet(packet: dict[str, Any], validator: Any) -> dict[str, Any]:
    safe_packet, report = redact_payload(packet)
    if isinstance(safe_packet, dict):
        safe_packet["redaction_summary"] = report
        safe_packet["validation"] = _merge_validation(safe_packet.get("validation", {}), validator(safe_packet))
        if safe_packet["validation"]["ok"] is not True and safe_packet.get("status") == "ready":
            safe_packet["status"] = "blocked"
        return safe_packet
    packet["validation"] = validator(packet)
    return packet


def _redaction_errors(value: Any) -> list[str]:
    value_for_redaction = _without_internal_validation(value)
    rendered = json.dumps(value_for_redaction, sort_keys=True, default=str)
    errors = [f"redaction:{error}" for error in validate_redaction(rendered)]
    if _has_unsafe_text(value_for_redaction):
        errors.append("source_boundary:unsafe_text")
    return errors


def _without_internal_validation(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_internal_validation(item)
            for key, item in value.items()
            if key not in {"redaction_summary", "validation"}
        }
    if isinstance(value, list):
        return [_without_internal_validation(item) for item in value]
    return value


def _has_unsafe_text(value: Any) -> bool:
    rendered = json.dumps(value, sort_keys=True, default=str)
    return bool(_unsafe_text_reasons(rendered))


def _unsafe_text_reasons(text: str) -> list[str]:
    reasons: list[str] = []
    if _SECRET_VALUE_PATTERN.search(text):
        reasons.append("secret")
    if _WINDOWS_PATH_PATTERN.search(text) or _POSIX_PATH_PATTERN.search(text):
        reasons.append("absolute_path")
    stripped = text.strip()
    if "\n" in stripped and re.search(r"(?m)^\s*(def|class|import|from)\s+", stripped):
        reasons.append("raw_source")
    if _PROMPT_INJECTION_PATTERN.search(text):
        reasons.append("prompt_injection")
    return sorted(set(reasons))


def _prefixed_validation(validation: dict[str, Any], prefix: str) -> dict[str, Any]:
    return _validation(
        validation.get("ok") is True,
        [f"{prefix}:{error}" for error in validation.get("errors", [])],
        prefix,
    )


def _merge_validation(*validations: Any) -> dict[str, Any]:
    errors: list[str] = []
    contexts: list[str] = []
    for validation in validations:
        if not isinstance(validation, dict):
            continue
        contexts.append(str(validation.get("context") or "validation"))
        errors.extend(str(error) for error in validation.get("errors", []) if error)
    return _validation(not errors, sorted(set(errors)), "+".join(contexts) if contexts else "validation")


def _validation(ok: bool, errors: list[str], context: str) -> dict[str, Any]:
    return {"ok": bool(ok), "errors": sorted(set(errors)), "context": context}


def _aggregate_status(packets: list[dict[str, Any]]) -> str:
    statuses = {packet.get("status") for packet in packets}
    if "approval_required" in statuses:
        return "approval_required"
    if statuses == {"ready"}:
        return "ready"
    return "blocked"


def _load_json(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    return loaded if isinstance(loaded, dict) else {}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False
