"""Runtime browser QA, performance budget and stabilization packets.

Batch 33 turns real-testing readiness into staged QA evidence. It does not
start browser automation, launch a live server, call providers, mutate the
canonical graph or perform git actions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_live_runtime import validate_live_runtime_contract
from product_agent_os.project_graph_real_testing import (
    validate_codex_surface_smoke_plan,
    validate_real_testing_readiness_packet,
)
from product_agent_os.project_graph_sanitization import sanitize_graph_text


RUNTIME_BROWSER_QA_TARGET = ".codex/product-agent-os/project-code-graph-runtime-browser-qa.json"
PERFORMANCE_BUDGET_TARGET = ".codex/product-agent-os/project-code-graph-performance-budget.json"
STABILIZATION_LEDGER_TARGET = ".codex/product-agent-os/project-code-graph-stabilization-ledger.json"

_APPROVAL_BOUNDARY = "batch33_runtime_browser_qa_performance_stabilization"
_ROLLBACK_PATH = "delete generated Batch 33 runtime QA, performance and stabilization artifacts under stage root"
_BATCH33_ALLOWED_SURFACES = {
    "runtime_browser_qa",
    "runtime_performance_budget",
    "runtime_stabilization_loop",
}
_QA_POLICY_FIELDS = {
    "browser_smoke_required",
    "console_network_checks_required",
    "mobile_overflow_check_required",
    "generated_view_labels_required",
    "source_boundary_labels_required",
    "external_requests_require_approved_provider",
}
_PERFORMANCE_POLICY_FIELDS = {
    "max_nodes",
    "max_edges",
    "max_search_latency_ms",
    "max_provider_latency_ms",
    "max_memory_mb",
    "breach_policy",
}
_STABILIZATION_POLICY_FIELDS = {
    "severity_policy_required",
    "no_open_p0_p1",
    "remaining_issue_owner_required",
    "rerun_plan_required",
}
_RESOLVED_STATUSES = {"fixed", "resolved", "closed"}
_ACCEPTED_GAP_STATUSES = {"accepted_gap"}
_BUDGET_BREACH_MITIGATIONS = {"accepted_gap", "live_layer_disabled"}
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_PROMPT_INJECTION_PATTERN = re.compile(
    r"(?i)(ignore previous instructions|exfiltrate|reveal secrets|system prompt|developer message)"
)


def validate_runtime_qa_approval(
    approval: dict[str, Any] | None,
    readiness_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 33 approval and Batch 32 readiness evidence."""

    if not isinstance(approval, dict):
        return _validation(False, ["runtime_qa_approval:missing"], "runtime_qa_approval")

    errors: list[str] = []
    required_fields = {
        "explicit_approval",
        "owner",
        "allowed_surfaces",
        "qa_policy",
        "performance_policy",
        "stabilization_policy",
        "rollback_path",
        "residual_risks",
    }
    errors.extend(f"runtime_qa_approval:{field}:missing" for field in sorted(required_fields - set(approval)))
    if approval.get("explicit_approval") is not True:
        errors.append("runtime_qa_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("runtime_qa_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH33_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"runtime_qa_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH33_ALLOWED_SURFACES):
        errors.append(f"runtime_qa_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_readiness_prerequisite(readiness_packet))
    errors.extend(_validate_qa_policy(approval.get("qa_policy")))
    errors.extend(_validate_performance_policy(approval.get("performance_policy")))
    errors.extend(_validate_stabilization_policy(approval.get("stabilization_policy")))
    if approval.get("rollback_path") != _ROLLBACK_PATH:
        errors.append("runtime_qa_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("runtime_qa_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("runtime_qa_approval:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "runtime_qa_approval")


def build_runtime_browser_qa_packet(
    *,
    readiness_packet: dict[str, Any],
    smoke_plan: dict[str, Any],
    runtime_contract: dict[str, Any],
    approval: dict[str, Any] | None,
    browser_checks: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build staged browser-smoke, console/network and responsive QA evidence."""

    approval_validation = validate_runtime_qa_approval(approval, readiness_packet)
    readiness_validation = _prefixed_validation(
        validate_real_testing_readiness_packet(readiness_packet),
        "real_testing_readiness",
    )
    smoke_validation = _prefixed_validation(validate_codex_surface_smoke_plan(smoke_plan), "codex_surface_smoke")
    runtime_validation = _validate_runtime_prerequisite(runtime_contract)
    qa_validation = _validate_browser_checks(browser_checks)
    validation = _merge_validation(
        approval_validation,
        readiness_validation,
        smoke_validation,
        runtime_validation,
        qa_validation,
    )
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_runtime_browser_qa",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": RUNTIME_BROWSER_QA_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Provide Batch 33 approval before runtime browser QA evidence.",
        }

    checks = _browser_check_summary(browser_checks)
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_runtime_browser_qa",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "staged_browser_qa_metadata_only_no_raw_source_or_live_runtime",
        "generated_view_policy": "runtime_browser_qa_is_generated_evidence_not_source_of_truth",
        "target": RUNTIME_BROWSER_QA_TARGET,
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "browser_smoke_status": checks["browser_smoke_status"],
        "browser_automation_started": False,
        "console_network_checks_present": checks["console_network_checks_present"],
        "console_errors": checks["console_errors"],
        "network_requests": checks["network_requests"],
        "no_external_requests_beyond_approved_providers": checks["no_external_requests_beyond_approved_providers"],
        "mobile_overflow_check_present": checks["mobile_overflow_check_present"],
        "mobile_checks": checks["mobile_checks"],
        "generated_view_labels_visible": checks["generated_view_labels_visible"],
        "source_boundary_labels_visible": checks["source_boundary_labels_visible"],
        "not_source_of_truth_label_visible": checks["not_source_of_truth_label_visible"],
        "staged_evidence_only": True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Use this staged evidence to decide whether separately approved real browser QA is needed.",
    }
    return _redacted_packet(packet, validate_runtime_browser_qa_packet)


def validate_runtime_browser_qa_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 33 runtime browser QA packet invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_runtime_browser_qa":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("target") != RUNTIME_BROWSER_QA_TARGET:
        errors.append("target")
    if packet.get("browser_automation_started") is not False:
        errors.append("browser_automation_started")
    if packet.get("console_network_checks_present") is not True and packet.get("status") == "ready":
        errors.append("console_network_checks_present")
    if packet.get("mobile_overflow_check_present") is not True and packet.get("status") == "ready":
        errors.append("mobile_overflow_check_present")
    if packet.get("generated_view_labels_visible") is not True and packet.get("status") == "ready":
        errors.append("generated_view_labels_visible")
    if packet.get("source_boundary_labels_visible") is not True and packet.get("status") == "ready":
        errors.append("source_boundary_labels_visible")
    if packet.get("not_source_of_truth_label_visible") is not True and packet.get("status") == "ready":
        errors.append("not_source_of_truth_label_visible")
    if packet.get("no_external_requests_beyond_approved_providers") is not True and packet.get("status") == "ready":
        errors.append("no_external_requests_beyond_approved_providers")
    errors.extend(_validate_common_runtime_safety(packet))
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_runtime_browser_qa")


def build_performance_budget_packet(
    *,
    readiness_packet: dict[str, Any],
    runtime_contract: dict[str, Any],
    approval: dict[str, Any] | None,
    measurements: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Build staged node/edge/search/provider latency and memory budget evidence."""

    approval_validation = validate_runtime_qa_approval(approval, readiness_packet)
    readiness_validation = _prefixed_validation(
        validate_real_testing_readiness_packet(readiness_packet),
        "real_testing_readiness",
    )
    runtime_validation = _validate_runtime_prerequisite(runtime_contract)
    performance_validation = _validate_performance_measurements(approval, measurements)
    validation = _merge_validation(approval_validation, readiness_validation, runtime_validation, performance_validation)
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_performance_budget",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": PERFORMANCE_BUDGET_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Provide Batch 33 approval before performance budget evidence.",
        }

    summary = _performance_summary(approval, measurements)
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_performance_budget",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "staged_budget_measurements_only_no_provider_calls",
        "generated_view_policy": "performance_budget_is_generated_evidence_not_source_of_truth",
        "target": PERFORMANCE_BUDGET_TARGET,
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "performance_caps": summary["performance_caps"],
        "node_edge_search_provider_latency_caps_present": summary[
            "node_edge_search_provider_latency_caps_present"
        ],
        "memory_bounds_present": summary["memory_bounds_present"],
        "measurements": summary["measurements"],
        "breach_summary": summary["breach_summary"],
        "budget_breach_disables_live_layer_or_records_accepted_gap": summary[
            "budget_breach_disables_live_layer_or_records_accepted_gap"
        ],
        "runtime_layer_state": summary["runtime_layer_state"],
        "staged_evidence_only": True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Keep the live layer disabled unless a future approved run stays within budget.",
    }
    return _redacted_packet(packet, validate_performance_budget_packet)


def validate_performance_budget_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 33 performance budget packet invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_performance_budget":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("target") != PERFORMANCE_BUDGET_TARGET:
        errors.append("target")
    if packet.get("node_edge_search_provider_latency_caps_present") is not True and packet.get("status") == "ready":
        errors.append("node_edge_search_provider_latency_caps_present")
    if packet.get("memory_bounds_present") is not True and packet.get("status") == "ready":
        errors.append("memory_bounds_present")
    if (
        packet.get("budget_breach_disables_live_layer_or_records_accepted_gap") is not True
        and packet.get("status") == "ready"
    ):
        errors.append("budget_breach_disables_live_layer_or_records_accepted_gap")
    errors.extend(_validate_common_runtime_safety(packet))
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_performance_budget")


def build_stabilization_ledger_packet(
    *,
    qa_packet: dict[str, Any],
    performance_packet: dict[str, Any],
    approval: dict[str, Any] | None,
    defects: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    """Build staged defect triage, accepted-gap and rerun-plan evidence."""

    approval_validation = validate_runtime_qa_approval(approval, _readiness_stub())
    qa_validation = _prefixed_validation(validate_runtime_browser_qa_packet(qa_packet), "runtime_browser_qa")
    performance_validation = _prefixed_validation(validate_performance_budget_packet(performance_packet), "performance_budget")
    defects_validation = _validate_defects(approval, defects)
    validation = _merge_validation(approval_validation, qa_validation, performance_validation, defects_validation)
    if not isinstance(approval, dict) or approval.get("explicit_approval") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_stabilization_ledger",
            "status": "approval_required",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "target": STABILIZATION_LEDGER_TARGET,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "validation": validation,
            "safe_next_action": "Provide Batch 33 approval before stabilization ledger evidence.",
        }

    summary = _defect_summary(approval, defects)
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_stabilization_ledger",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "defect_triage_metadata_only_no_raw_source_or_external_issue_mutation",
        "generated_view_policy": "stabilization_ledger_is_generated_evidence_not_source_of_truth",
        "target": STABILIZATION_LEDGER_TARGET,
        "owner": sanitize_graph_text(approval.get("owner") or ""),
        "severity_policy_present": summary["severity_policy_present"],
        "fix_or_accepted_gap_ledger_present": summary["fix_or_accepted_gap_ledger_present"],
        "rerun_plan_present": summary["rerun_plan_present"],
        "no_open_p0_p1": summary["no_open_p0_p1"],
        "remaining_issues_have_owner_risk_follow_up": summary["remaining_issues_have_owner_risk_follow_up"],
        "defects": summary["defects"],
        "defect_summary": summary["defect_summary"],
        "upstream_artifacts": {
            "runtime_browser_qa": qa_packet.get("target"),
            "performance_budget": performance_packet.get("target"),
        },
        "staged_evidence_only": True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Close P0/P1 defects before any owner-approved live QA execution.",
    }
    return _redacted_packet(packet, validate_stabilization_ledger_packet)


def validate_stabilization_ledger_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 33 stabilization packet invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_stabilization_ledger":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("target") != STABILIZATION_LEDGER_TARGET:
        errors.append("target")
    for field in [
        "severity_policy_present",
        "fix_or_accepted_gap_ledger_present",
        "rerun_plan_present",
        "no_open_p0_p1",
        "remaining_issues_have_owner_risk_follow_up",
    ]:
        if packet.get(field) is not True and packet.get("status") == "ready":
            errors.append(field)
    errors.extend(_validate_common_runtime_safety(packet))
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_stabilization_ledger")


def stage_runtime_qa(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    readiness_artifact: str | Path,
    smoke_artifact: str | Path,
    runtime_artifact: str | Path,
    browser_checks: dict[str, Any] | None = None,
    performance_measurements: list[dict[str, Any]] | None = None,
    defects: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Stage Batch 33 runtime QA, performance and stabilization artifacts."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")

    readiness = _load_json(readiness_artifact)
    smoke = _load_json(smoke_artifact)
    runtime = _load_json(runtime_artifact)
    qa = build_runtime_browser_qa_packet(
        readiness_packet=readiness,
        smoke_plan=smoke,
        runtime_contract=runtime,
        approval=approval,
        browser_checks=browser_checks or {},
    )
    performance = build_performance_budget_packet(
        readiness_packet=readiness,
        runtime_contract=runtime,
        approval=approval,
        measurements=performance_measurements or [],
    )
    stabilization = build_stabilization_ledger_packet(
        qa_packet=qa,
        performance_packet=performance,
        approval=approval,
        defects=defects or [],
    )
    _write_json(stage_path / RUNTIME_BROWSER_QA_TARGET, qa)
    _write_json(stage_path / PERFORMANCE_BUDGET_TARGET, performance)
    _write_json(stage_path / STABILIZATION_LEDGER_TARGET, stabilization)
    validation = _merge_validation(
        qa.get("validation", {}),
        performance.get("validation", {}),
        stabilization.get("validation", {}),
    )
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "build-runtime-qa",
            "status": _aggregate_status([qa, performance, stabilization]),
            "approval_boundary": _APPROVAL_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "files": [
                RUNTIME_BROWSER_QA_TARGET,
                PERFORMANCE_BUDGET_TARGET,
                STABILIZATION_LEDGER_TARGET,
            ],
            "validation": validation,
        },
    }


def disable_runtime_qa(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 33 runtime QA artifacts from a stage root."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")

    removed: list[str] = []
    missing: list[str] = []
    for target in [RUNTIME_BROWSER_QA_TARGET, PERFORMANCE_BUDGET_TARGET, STABILIZATION_LEDGER_TARGET]:
        path = stage_path / target
        if path.exists():
            path.unlink()
            removed.append(target)
        else:
            missing.append(target)
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "disable-runtime-qa",
            "status": "disabled",
            "deletion_proof": {
                "delete_generated_runtime_qa_artifacts": True,
                "removed": removed,
                "missing": missing,
                "deletion_scope": "stage_root_generated_batch33_runtime_qa_artifacts_only",
            },
            "fallback": "graph_only_query_mode",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
        },
    }


def _validate_readiness_prerequisite(readiness_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(readiness_packet, dict):
        return ["real_testing_readiness:missing"]
    errors = [
        f"real_testing_readiness:{error}"
        for error in validate_real_testing_readiness_packet(readiness_packet).get("errors", [])
    ]
    if readiness_packet.get("status") != "ready":
        errors.append("real_testing_readiness:status")
    if readiness_packet.get("live_server_started") is not False:
        errors.append("real_testing_readiness:live_server_started")
    if readiness_packet.get("external_call_performed") is not False:
        errors.append("real_testing_readiness:external_call_performed")
    if readiness_packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("real_testing_readiness:canonical_graph_mutation")
    return sorted(set(errors))


def _validate_runtime_prerequisite(runtime_contract: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(runtime_contract, dict):
        return _validation(False, ["live_runtime:missing"], "live_runtime_prerequisite")
    validation = validate_live_runtime_contract(runtime_contract)
    errors = [f"live_runtime:{error}" for error in validation.get("errors", [])]
    if runtime_contract.get("status") != "ready":
        errors.append("live_runtime:status")
    if runtime_contract.get("runtime_status") != "disabled_by_default_not_started":
        errors.append("live_runtime:runtime_status")
    if runtime_contract.get("server_lifecycle", {}).get("server_started") is not False:
        errors.append("live_runtime:server_started")
    if runtime_contract.get("external_call_performed") is True:
        errors.append("live_runtime:external_call_performed")
    if runtime_contract.get("server_contract", {}).get("canonical_mutation_allowed") is not False:
        errors.append("live_runtime:canonical_mutation_allowed")
    return _validation(not errors, sorted(set(errors)), "live_runtime_prerequisite")


def _validate_qa_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["qa_policy"]
    errors: list[str] = []
    for field in sorted(_QA_POLICY_FIELDS):
        if policy.get(field) is not True:
            errors.append(f"qa_policy:{field}")
    return errors


def _validate_performance_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["performance_policy"]
    errors: list[str] = []
    for field in sorted(_PERFORMANCE_POLICY_FIELDS - {"breach_policy"}):
        if _non_negative_number(policy.get(field)) is None:
            errors.append(f"performance_policy:{field}")
    if policy.get("breach_policy") != "disable_live_layer_or_accepted_gap":
        errors.append("performance_policy:breach_policy")
    return errors


def _validate_stabilization_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["stabilization_policy"]
    errors: list[str] = []
    for field in sorted(_STABILIZATION_POLICY_FIELDS):
        if policy.get(field) is not True:
            errors.append(f"stabilization_policy:{field}")
    return errors


def _validate_browser_checks(browser_checks: Any) -> dict[str, Any]:
    checks = browser_checks if isinstance(browser_checks, dict) else {}
    errors: list[str] = []
    smoke = checks.get("browser_smoke") if isinstance(checks.get("browser_smoke"), dict) else {}
    if smoke.get("status") not in {"passed", "accepted_gap"}:
        errors.append("browser_smoke:status")
    if smoke.get("browser_automation_started") is not False:
        errors.append("browser_smoke:browser_automation_started")
    if smoke.get("status") == "accepted_gap":
        errors.extend(_gap_errors(smoke, "browser_smoke"))

    console = checks.get("console") if isinstance(checks.get("console"), dict) else {}
    console_errors = console.get("errors") if isinstance(console.get("errors"), list) else []
    if console_errors and console.get("status") != "accepted_gap":
        errors.append("console:errors")
    if console_errors and console.get("status") == "accepted_gap":
        errors.extend(_gap_errors(console, "console"))

    network = checks.get("network") if isinstance(checks.get("network"), dict) else {}
    requests = network.get("requests") if isinstance(network.get("requests"), list) else []
    if not isinstance(requests, list):
        errors.append("network:requests")
    for index, request in enumerate(requests):
        if not isinstance(request, dict):
            errors.append(f"network:{index}:type")
            continue
        if request.get("external") is True and request.get("approved_provider") is not True:
            errors.append(f"network:{index}:unapproved_external_request")

    mobile = checks.get("mobile") if isinstance(checks.get("mobile"), list) else []
    if not mobile:
        errors.append("mobile:missing")
    for index, item in enumerate(mobile):
        if not isinstance(item, dict):
            errors.append(f"mobile:{index}:type")
            continue
        if item.get("status") not in {"passed", "accepted_gap"}:
            errors.append(f"mobile:{index}:status")
        if item.get("horizontal_overflow") is not False:
            errors.append(f"mobile:{index}:horizontal_overflow")
        if item.get("status") == "accepted_gap":
            errors.extend(_gap_errors(item, f"mobile:{index}"))

    labels = checks.get("labels") if isinstance(checks.get("labels"), dict) else {}
    for field in [
        "generated_view_label_visible",
        "source_boundary_label_visible",
        "not_source_of_truth_label_visible",
    ]:
        if labels.get(field) is not True:
            errors.append(f"labels:{field}")
    return _validation(not errors, sorted(set(errors)), "runtime_browser_checks")


def _browser_check_summary(browser_checks: Any) -> dict[str, Any]:
    checks = browser_checks if isinstance(browser_checks, dict) else {}
    smoke = checks.get("browser_smoke") if isinstance(checks.get("browser_smoke"), dict) else {}
    console = checks.get("console") if isinstance(checks.get("console"), dict) else {}
    network = checks.get("network") if isinstance(checks.get("network"), dict) else {}
    mobile = checks.get("mobile") if isinstance(checks.get("mobile"), list) else []
    labels = checks.get("labels") if isinstance(checks.get("labels"), dict) else {}
    requests = [
        {
            "url": sanitize_graph_text(request.get("url") or ""),
            "external": request.get("external") is True,
            "approved_provider": request.get("approved_provider") is True,
        }
        for request in network.get("requests", [])
        if isinstance(request, dict)
    ]
    mobile_checks = [
        {
            "viewport": sanitize_graph_text(item.get("viewport") or ""),
            "status": sanitize_graph_text(item.get("status") or "blocked"),
            "horizontal_overflow": item.get("horizontal_overflow") is True,
        }
        for item in mobile
        if isinstance(item, dict)
    ]
    console_errors = [sanitize_graph_text(error) for error in console.get("errors", []) if isinstance(error, str)]
    return {
        "browser_smoke_status": sanitize_graph_text(smoke.get("status") or "blocked"),
        "console_network_checks_present": not console_errors
        and all(request.get("external") is not True or request.get("approved_provider") is True for request in requests),
        "console_errors": console_errors,
        "network_requests": requests,
        "no_external_requests_beyond_approved_providers": all(
            request.get("external") is not True or request.get("approved_provider") is True for request in requests
        ),
        "mobile_overflow_check_present": bool(mobile_checks)
        and all(item.get("horizontal_overflow") is not True for item in mobile_checks),
        "mobile_checks": mobile_checks,
        "generated_view_labels_visible": labels.get("generated_view_label_visible") is True,
        "source_boundary_labels_visible": labels.get("source_boundary_label_visible") is True,
        "not_source_of_truth_label_visible": labels.get("not_source_of_truth_label_visible") is True,
    }


def _validate_performance_measurements(
    approval: dict[str, Any] | None,
    measurements: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    errors: list[str] = []
    policy = approval.get("performance_policy") if isinstance(approval, dict) else {}
    if not isinstance(measurements, list) or not measurements:
        errors.append("performance_measurements:missing")
    for index, measurement in enumerate(measurements or []):
        if not isinstance(measurement, dict):
            errors.append(f"performance_measurement:{index}:type")
            continue
        if not sanitize_graph_text(measurement.get("scenario") or ""):
            errors.append(f"performance_measurement:{index}:scenario")
        for field in ["node_count", "edge_count", "search_latency_ms", "provider_latency_ms", "memory_mb"]:
            if _non_negative_number(measurement.get(field)) is None:
                errors.append(f"performance_measurement:{index}:{field}")
        breach_fields = _breach_fields(policy, measurement)
        if breach_fields and not _breach_is_mitigated(measurement):
            errors.append(f"performance_measurement:{index}:breach_mitigation")
        if _has_unsafe_text(measurement):
            errors.append(f"performance_measurement:{index}:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "performance_measurements")


def _performance_summary(approval: dict[str, Any] | None, measurements: list[dict[str, Any]] | None) -> dict[str, Any]:
    policy = approval.get("performance_policy") if isinstance(approval, dict) else {}
    caps = {
        "max_nodes": int(policy.get("max_nodes") or 0),
        "max_edges": int(policy.get("max_edges") or 0),
        "max_search_latency_ms": int(policy.get("max_search_latency_ms") or 0),
        "max_provider_latency_ms": int(policy.get("max_provider_latency_ms") or 0),
        "max_memory_mb": int(policy.get("max_memory_mb") or 0),
        "breach_policy": sanitize_graph_text(policy.get("breach_policy") or ""),
    }
    measurement_items: list[dict[str, Any]] = []
    breaches = 0
    mitigated = 0
    for index, measurement in enumerate(measurements or []):
        if not isinstance(measurement, dict):
            continue
        breach_fields = _breach_fields(policy, measurement)
        if breach_fields:
            breaches += 1
        if breach_fields and _breach_is_mitigated(measurement):
            mitigated += 1
        measurement_items.append(
            {
                "scenario": sanitize_graph_text(measurement.get("scenario") or f"scenario-{index}"),
                "node_count": _non_negative_number(measurement.get("node_count")) or 0,
                "edge_count": _non_negative_number(measurement.get("edge_count")) or 0,
                "search_latency_ms": _non_negative_number(measurement.get("search_latency_ms")) or 0,
                "provider_latency_ms": _non_negative_number(measurement.get("provider_latency_ms")) or 0,
                "memory_mb": _non_negative_number(measurement.get("memory_mb")) or 0,
                "breach_fields": breach_fields,
                "breach_mitigation": sanitize_graph_text(measurement.get("breach_mitigation") or "not_needed"),
                "owner": sanitize_graph_text(measurement.get("owner") or ""),
                "risk": sanitize_graph_text(measurement.get("risk") or ""),
                "follow_up_condition": sanitize_graph_text(measurement.get("follow_up_condition") or ""),
            }
        )
    all_breaches_mitigated = breaches == mitigated
    return {
        "performance_caps": caps,
        "node_edge_search_provider_latency_caps_present": all(
            _non_negative_number(policy.get(field)) is not None
            for field in ["max_nodes", "max_edges", "max_search_latency_ms", "max_provider_latency_ms"]
        ),
        "memory_bounds_present": _non_negative_number(policy.get("max_memory_mb")) is not None,
        "measurements": measurement_items,
        "breach_summary": {
            "measurements": len(measurement_items),
            "breaches": breaches,
            "mitigated_breaches": mitigated,
            "unmitigated_breaches": max(0, breaches - mitigated),
        },
        "budget_breach_disables_live_layer_or_records_accepted_gap": all_breaches_mitigated,
        "runtime_layer_state": "disabled_or_accepted_gap" if breaches else "within_budget_staged_only",
    }


def _validate_defects(approval: dict[str, Any] | None, defects: list[dict[str, Any]] | None) -> dict[str, Any]:
    errors: list[str] = []
    policy = approval.get("stabilization_policy") if isinstance(approval, dict) else {}
    if policy.get("severity_policy_required") is not True:
        errors.append("stabilization_policy:severity_policy_required")
    if not isinstance(defects, list):
        errors.append("defects:type")
    for index, defect in enumerate(defects or []):
        if not isinstance(defect, dict):
            errors.append(f"defect:{index}:type")
            continue
        severity = sanitize_graph_text(defect.get("severity") or "")
        status = sanitize_graph_text(defect.get("status") or "")
        if severity not in {"P0", "P1", "P2", "P3", "P4"}:
            errors.append(f"defect:{index}:severity")
        if status not in _RESOLVED_STATUSES | _ACCEPTED_GAP_STATUSES | {"open"}:
            errors.append(f"defect:{index}:status")
        if severity in {"P0", "P1"} and status not in _RESOLVED_STATUSES:
            errors.append(f"defect:{index}:open_p0_p1")
        if status not in _RESOLVED_STATUSES:
            for field in ["owner", "risk", "follow_up_condition"]:
                if not sanitize_graph_text(defect.get(field) or ""):
                    errors.append(f"defect:{index}:{field}")
        if not isinstance(defect.get("rerun_plan"), list) or not defect.get("rerun_plan"):
            errors.append(f"defect:{index}:rerun_plan")
        if _has_unsafe_text(defect):
            errors.append(f"defect:{index}:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "stabilization_defects")


def _defect_summary(approval: dict[str, Any] | None, defects: list[dict[str, Any]] | None) -> dict[str, Any]:
    policy = approval.get("stabilization_policy") if isinstance(approval, dict) else {}
    defect_items: list[dict[str, Any]] = []
    open_p0_p1 = 0
    remaining_without_owner = 0
    rerun_missing = 0
    for index, defect in enumerate(defects or []):
        if not isinstance(defect, dict):
            continue
        severity = sanitize_graph_text(defect.get("severity") or "")
        status = sanitize_graph_text(defect.get("status") or "open")
        if severity in {"P0", "P1"} and status not in _RESOLVED_STATUSES:
            open_p0_p1 += 1
        if status not in _RESOLVED_STATUSES and not all(
            sanitize_graph_text(defect.get(field) or "") for field in ["owner", "risk", "follow_up_condition"]
        ):
            remaining_without_owner += 1
        if not isinstance(defect.get("rerun_plan"), list) or not defect.get("rerun_plan"):
            rerun_missing += 1
        defect_items.append(
            {
                "defect_id": sanitize_graph_text(defect.get("defect_id") or f"defect-{index}"),
                "severity": severity,
                "status": status,
                "owner": sanitize_graph_text(defect.get("owner") or ""),
                "risk": sanitize_graph_text(defect.get("risk") or ""),
                "follow_up_condition": sanitize_graph_text(defect.get("follow_up_condition") or ""),
                "rerun_plan": [
                    sanitize_graph_text(item)
                    for item in defect.get("rerun_plan", [])
                    if isinstance(item, str)
                ],
            }
        )
    return {
        "severity_policy_present": policy.get("severity_policy_required") is True,
        "fix_or_accepted_gap_ledger_present": all(
            item.get("status") in _RESOLVED_STATUSES | _ACCEPTED_GAP_STATUSES for item in defect_items
        ),
        "rerun_plan_present": rerun_missing == 0,
        "no_open_p0_p1": open_p0_p1 == 0,
        "remaining_issues_have_owner_risk_follow_up": remaining_without_owner == 0,
        "defects": defect_items,
        "defect_summary": {
            "total": len(defect_items),
            "open_p0_p1": open_p0_p1,
            "remaining_without_owner_risk_follow_up": remaining_without_owner,
            "rerun_plan_missing": rerun_missing,
        },
    }


def _validate_common_runtime_safety(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("live_server_started") is not False:
        errors.append("live_server_started")
    if packet.get("canonical_graph_mutation") != "not_performed":
        errors.append("canonical_graph_mutation")
    if packet.get("git_action") not in {None, "explicit_only_not_performed"}:
        errors.append("git_action")
    return errors


def _breach_fields(policy: Any, measurement: dict[str, Any]) -> list[str]:
    policy = policy if isinstance(policy, dict) else {}
    fields = [
        ("node_count", "max_nodes"),
        ("edge_count", "max_edges"),
        ("search_latency_ms", "max_search_latency_ms"),
        ("provider_latency_ms", "max_provider_latency_ms"),
        ("memory_mb", "max_memory_mb"),
    ]
    breaches: list[str] = []
    for measurement_field, cap_field in fields:
        observed = _non_negative_number(measurement.get(measurement_field))
        cap = _non_negative_number(policy.get(cap_field))
        if observed is not None and cap is not None and observed > cap:
            breaches.append(measurement_field)
    return breaches


def _breach_is_mitigated(measurement: dict[str, Any]) -> bool:
    mitigation = sanitize_graph_text(measurement.get("breach_mitigation") or "")
    if mitigation not in _BUDGET_BREACH_MITIGATIONS:
        return False
    return all(
        sanitize_graph_text(measurement.get(field) or "")
        for field in ["owner", "risk", "follow_up_condition"]
    )


def _gap_errors(value: dict[str, Any], prefix: str) -> list[str]:
    errors: list[str] = []
    for field in ["owner", "risk", "follow_up_condition"]:
        if not sanitize_graph_text(value.get(field) or ""):
            errors.append(f"{prefix}:{field}")
    return errors


def _non_negative_number(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


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
        contexts.append(str(validation.get("context") or "+".join(validation.get("checks", [])) or "validation"))
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


def _readiness_stub() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_kind": "project_graph_real_testing_readiness",
        "status": "ready",
        "approval_boundary": "batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke",
        "target": ".codex/product-agent-os/project-code-graph-real-testing-readiness.json",
        "real_testing_start_policy": "approved_targets_only",
        "no_hidden_unresolved_track10_gates": True,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "live_server_started": False,
        "canonical_graph_mutation": "not_performed",
        "gate_statuses": [
            {"gate": "audit_operability", "status": "implemented_verified"},
            {"gate": "canonical_graph_mutation", "status": "explicitly_disabled"},
            {"gate": "external_embedding", "status": "blocked_by_missing_approval"},
            {"gate": "external_llm", "status": "blocked_by_missing_approval"},
            {"gate": "external_reranker", "status": "blocked_by_missing_approval"},
            {"gate": "human_review_ledger", "status": "implemented_verified"},
            {"gate": "live_governance", "status": "implemented_verified"},
            {"gate": "live_runtime", "status": "explicitly_disabled"},
        ],
        "validation": {"ok": True, "errors": [], "context": "project_graph_real_testing_readiness"},
    }


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
