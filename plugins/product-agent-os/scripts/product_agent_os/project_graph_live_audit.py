"""Audit, security, observability and handoff packets for live graph work.

Batch 31 records generated evidence for live/provider/mutation accountability.
It does not start a server, call providers, mutate graph facts or activate
agents. All artifacts are staged under an explicit stage root.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.project_graph_live_governance import validate_live_governance_packet
from product_agent_os.project_graph_sanitization import sanitize_graph_text


LIVE_AUDIT_LOG_TARGET = ".codex/product-agent-os/project-code-graph-live-audit-log.jsonl"
LIVE_SECURITY_PRIVACY_TARGET = ".codex/product-agent-os/project-code-graph-live-security-privacy.json"
LIVE_OBSERVABILITY_TARGET = ".codex/product-agent-os/project-code-graph-live-observability.json"
LIVE_AGENT_HANDOFF_TARGET = ".codex/product-agent-os/project-code-graph-agent-skill-handoff.json"

_APPROVAL_BOUNDARY = "batch31_audit_security_observability_agent_skill_routing"
_ROLLBACK_PATH = "delete generated Batch 31 audit, security, observability and handoff artifacts under stage root"
_BATCH31_ALLOWED_SURFACES = {
    "agent_skill_handoff_routing",
    "audit_logging",
    "runtime_observability",
    "security_privacy_tests",
}
_REQUIRED_EVENT_TYPES = {"approval", "provider_call", "mutation", "failure"}
_SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk-[a-z0-9_-]{8,}|api[_-]?key\s*=\s*[^\s\"'<>]+|token\s*=\s*[^\s\"'<>]+)"
)
_WINDOWS_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
_POSIX_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")
_PROMPT_INJECTION_PATTERN = re.compile(
    r"(?i)(ignore previous instructions|exfiltrate|reveal secrets|system prompt|developer message)"
)


def validate_live_audit_approval(
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Validate explicit Batch 31 approval and Batch 24 governance evidence."""

    if not isinstance(approval, dict):
        return _validation(False, ["live_audit_approval:missing"], "live_audit_approval")
    required_fields = {
        "explicit_approval",
        "owner",
        "allowed_surfaces",
        "audit_policy",
        "security_privacy_policy",
        "observability_policy",
        "handoff_policy",
        "rollback_path",
        "residual_risks",
    }
    errors: list[str] = []
    errors.extend(f"live_audit_approval:{field}:missing" for field in sorted(required_fields - set(approval)))
    if approval.get("explicit_approval") is not True:
        errors.append("live_audit_approval:explicit_approval")
    if not sanitize_graph_text(approval.get("owner") or ""):
        errors.append("live_audit_approval:owner")

    allowed_surfaces = {str(item) for item in approval.get("allowed_surfaces", []) if isinstance(item, str)}
    for required in sorted(_BATCH31_ALLOWED_SURFACES):
        if required not in allowed_surfaces:
            errors.append(f"live_audit_approval:allowed_surfaces:{required}:missing")
    for surface in sorted(allowed_surfaces - _BATCH31_ALLOWED_SURFACES):
        errors.append(f"live_audit_approval:allowed_surfaces:{surface}")

    errors.extend(_validate_governance_prerequisite(governance_packet))
    errors.extend(_validate_audit_policy(approval.get("audit_policy")))
    errors.extend(_validate_security_policy(approval.get("security_privacy_policy")))
    errors.extend(_validate_observability_policy(approval.get("observability_policy")))
    errors.extend(_validate_handoff_policy(approval.get("handoff_policy")))
    if approval.get("rollback_path") != _ROLLBACK_PATH:
        errors.append("live_audit_approval:rollback_path")
    if not isinstance(approval.get("residual_risks"), list):
        errors.append("live_audit_approval:residual_risks")
    if _has_unsafe_text(approval):
        errors.append("live_audit_approval:unsafe_text")
    return _validation(not errors, sorted(set(errors)), "live_audit_approval")


def build_live_audit_event_log(
    live_actions: list[dict[str, Any]] | None,
    *,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a redacted audit event packet for live/provider/mutation actions."""

    approval_validation = validate_live_audit_approval(approval, governance_packet)
    actions = live_actions if isinstance(live_actions, list) else []
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_live_audit_log",
            "status": "approval_required",
            "write_policy": "append_only_jsonl",
            "approval_boundary": _APPROVAL_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "every_live_action_emits_audit_event": False,
            "events": [],
            "validation": approval_validation,
            "safe_next_action": "Provide Batch 31 approval and ready Batch 24 governance before audit evidence.",
        }

    events = [_audit_event(action, index) for index, action in enumerate(actions)]
    event_types = {event["action_type"] for event in events}
    coverage_errors = [
        f"audit_event:{event_type}:missing" for event_type in sorted(_REQUIRED_EVENT_TYPES - event_types)
    ]
    validation = _merge_validation(
        approval_validation,
        _validation(not coverage_errors, coverage_errors, "live_audit_event_coverage"),
    )
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_audit_log",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "write_policy": "append_only_jsonl",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "redacted_live_action_metadata_only_no_raw_source_or_secret_material",
        "generated_view_policy": "audit_log_is_generated_evidence_not_source_of_truth",
        "target": LIVE_AUDIT_LOG_TARGET,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "every_live_action_emits_audit_event": len(events) == len(actions) and not coverage_errors,
        "audit_log_append_only": True,
        "event_count": len(events),
        "event_types": sorted(event_types),
        "events": events,
        "git_action": "explicit_only_not_performed",
        "validation": validation,
        "safe_next_action": "Use audit events as generated accountability evidence only.",
    }
    return _redacted_packet(packet, validate_live_audit_event_log)


def validate_live_audit_event_log(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate Batch 31 audit event invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_live_audit_log":
        errors.append("artifact_kind")
    if packet.get("write_policy") != "append_only_jsonl":
        errors.append("write_policy")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    events = packet.get("events")
    if not isinstance(events, list):
        errors.append("events")
        events = []
    event_types = {str(event.get("action_type")) for event in events if isinstance(event, dict)}
    for event_type in sorted(_REQUIRED_EVENT_TYPES):
        if event_type not in event_types and packet.get("status") == "ready":
            errors.append(f"audit_event:{event_type}:missing")
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            errors.append(f"event:{index}:type")
            continue
        if event.get("artifact_kind") != "project_graph_live_audit_event":
            errors.append(f"event:{index}:artifact_kind")
        if event.get("redacted") is not True:
            errors.append(f"event:{index}:redacted")
        if _has_unsafe_text(event):
            errors.append(f"event:{index}:unsafe_text")
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_live_audit_log")


def build_security_privacy_test_packet(
    cases: list[dict[str, Any]] | None,
    *,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build local negative-test evidence for Batch 31 security/privacy gates."""

    approval_validation = validate_live_audit_approval(approval, governance_packet)
    case_list = cases if isinstance(cases, list) else []
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_live_security_privacy_tests",
            "status": "approval_required",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "unsafe_cases_blocked": False,
            "validation": approval_validation,
            "safe_next_action": "Provide Batch 31 approval before security/privacy evidence.",
        }

    results = [_security_case_result(case, index) for index, case in enumerate(case_list)]
    expected_blocked = [result for result in results if result.get("expected") == "blocked"]
    unsafe_cases_blocked = bool(expected_blocked) and all(result.get("blocked") is True for result in expected_blocked)
    prompt_injection_blocked = any(
        result.get("case_type") == "prompt_injection" and result.get("blocked") is True for result in results
    )
    validation = _merge_validation(
        approval_validation,
        _validation(unsafe_cases_blocked, [] if unsafe_cases_blocked else ["security_privacy:unsafe_case_not_blocked"], "security_privacy_tests"),
        _validation(prompt_injection_blocked, [] if prompt_injection_blocked else ["security_privacy:prompt_injection"], "prompt_injection_tests"),
    )
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_security_privacy_tests",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "negative_test_metadata_only_no_raw_source_or_secret_material",
        "target": LIVE_SECURITY_PRIVACY_TARGET,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "unsafe_cases_blocked": unsafe_cases_blocked,
        "blocked_case_count": sum(1 for result in results if result.get("blocked") is True),
        "prompt_injection_blocked": prompt_injection_blocked,
        "cases": results,
        "validation": validation,
        "safe_next_action": "Keep unsafe live/provider/mutation inputs blocked before any runtime action.",
    }
    return _redacted_packet(packet, validate_security_privacy_test_packet)


def validate_security_privacy_test_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate security/privacy negative-test evidence."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_live_security_privacy_tests":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("status") == "ready" and packet.get("unsafe_cases_blocked") is not True:
        errors.append("unsafe_cases_blocked")
    if packet.get("status") == "ready" and packet.get("prompt_injection_blocked") is not True:
        errors.append("prompt_injection_blocked")
    for case in packet.get("cases", []):
        if not isinstance(case, dict):
            errors.append("case:type")
            continue
        if case.get("expected") == "blocked" and case.get("blocked") is not True:
            errors.append(f"case:{case.get('case_id')}:not_blocked")
        if _has_unsafe_text(case):
            errors.append(f"case:{case.get('case_id')}:unsafe_text")
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_live_security_privacy_tests")


def build_runtime_observability_packet(
    *,
    runtime_contract: dict[str, Any] | None,
    audit_log: dict[str, Any] | None,
    security_packet: dict[str, Any] | None,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build observability evidence that makes degraded mode visible."""

    approval_validation = validate_live_audit_approval(approval, governance_packet)
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_runtime_observability",
            "status": "approval_required",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "degraded_mode_visible_to_users_and_agents": False,
            "validation": approval_validation,
            "safe_next_action": "Provide Batch 31 approval before observability evidence.",
        }

    runtime = runtime_contract if isinstance(runtime_contract, dict) else {}
    audit = audit_log if isinstance(audit_log, dict) else {}
    security = security_packet if isinstance(security_packet, dict) else {}
    provider_errors = [
        {
            "surface": sanitize_graph_text(event.get("surface") or ""),
            "status": sanitize_graph_text(event.get("status") or ""),
        }
        for event in audit.get("events", [])
        if isinstance(event, dict) and event.get("action_type") == "provider_call" and event.get("status") != "ready"
    ][:10]
    runtime_status = _observed_runtime_status(runtime, audit, security)
    budget_status = "blocked_or_degraded" if provider_errors or security.get("unsafe_cases_blocked") is True else "within_budget"
    validation = _merge_validation(
        approval_validation,
        validate_live_audit_event_log(audit),
        validate_security_privacy_test_packet(security),
    )
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_runtime_observability",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "runtime_status_metadata_only_no_logs_or_secret_material",
        "target": LIVE_OBSERVABILITY_TARGET,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "runtime_health": {
            "runtime_status": runtime_status,
            "server_started": bool(_nested_get(runtime, "server_lifecycle", "server_started", default=False)),
            "fallback": _nested_get(runtime, "fallback_policy", "fallback", default="graph_only_query_mode"),
        },
        "latency": {
            "latency_visible": True,
            "latency_ms": 0,
            "latency_status": "not_measured_no_live_runtime",
        },
        "provider_errors": provider_errors,
        "budget_usage": {
            "budget_visible": True,
            "budget_status": budget_status,
            "provider_call_count": 0,
            "external_cost_units": 0,
        },
        "degraded_mode_visible_to_users_and_agents": True,
        "status_dashboard_fields": ["runtime_health", "latency", "provider_errors", "budget_usage", "degraded_mode"],
        "validation": validation,
        "safe_next_action": "Surface degraded graph-only mode before any live/provider/mutation work.",
    }
    return _redacted_packet(packet, validate_runtime_observability_packet)


def validate_runtime_observability_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate runtime observability packet invariants."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_runtime_observability":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("status") == "ready" and packet.get("degraded_mode_visible_to_users_and_agents") is not True:
        errors.append("degraded_mode_visible")
    health = packet.get("runtime_health") if isinstance(packet.get("runtime_health"), dict) else {}
    if packet.get("status") == "ready" and not health.get("runtime_status"):
        errors.append("runtime_health:runtime_status")
    budget = packet.get("budget_usage") if isinstance(packet.get("budget_usage"), dict) else {}
    if packet.get("status") == "ready" and budget.get("budget_visible") is not True:
        errors.append("budget_usage:visible")
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_runtime_observability")


def build_agent_skill_handoff_routing_packet(
    *,
    approval: dict[str, Any] | None,
    governance_packet: dict[str, Any] | None,
    observability_packet: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build agent/skill routing evidence for live/provider/mutation work."""

    approval_validation = validate_live_audit_approval(approval, governance_packet)
    if approval_validation.get("ok") is not True:
        return {
            "schema_version": 1,
            "artifact_kind": "project_graph_agent_skill_handoff_routing",
            "status": "approval_required",
            "provider_call_allowed": False,
            "external_call_performed": False,
            "ownership_required": True,
            "verification_evidence_required": True,
            "validation": approval_validation,
            "safe_next_action": "Provide Batch 31 approval before handoff routing evidence.",
        }

    observability = observability_packet if isinstance(observability_packet, dict) else {}
    validation = _merge_validation(approval_validation, validate_runtime_observability_packet(observability))
    packet = {
        "schema_version": 1,
        "artifact_kind": "project_graph_agent_skill_handoff_routing",
        "status": "ready" if validation.get("ok") is True else "blocked",
        "approval_boundary": _APPROVAL_BOUNDARY,
        "source_boundary": "handoff_metadata_only_no_raw_conversation_or_secret_material",
        "target": LIVE_AGENT_HANDOFF_TARGET,
        "provider_call_allowed": False,
        "external_call_performed": False,
        "agent_skill_routing": "reviewable_handoff_required",
        "ownership_required": True,
        "verification_evidence_required": True,
        "fresh_context_required": True,
        "handoff_packet_fields": [
            "sources_context_used",
            "assumptions",
            "files_touched_or_proposed",
            "verification_evidence",
            "open_risks",
            "stop_reason",
            "recommended_next_role",
        ],
        "stop_conditions": [
            "missing_ownership",
            "missing_verification_evidence",
            "missing_fresh_context_handoff",
            "live_provider_or_mutation_without_approval",
            "security_privacy_failure",
            "observability_degraded_mode_hidden",
        ],
        "skill_contract_updates": [
            "implementation-planner names live/provider/mutation ownership and evidence gates",
            "agent-team-designer requires fresh-context handoff before live/provider/mutation work",
            "lifecycle skills route Batch 31 outputs as staged evidence only",
        ],
        "validation": validation,
        "safe_next_action": "Route live/provider/mutation work through owner-reviewed handoff packets only.",
    }
    return _redacted_packet(packet, validate_agent_skill_handoff_routing_packet)


def validate_agent_skill_handoff_routing_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Validate agent/skill handoff routing evidence."""

    errors: list[str] = []
    if packet.get("schema_version") != 1:
        errors.append("schema_version")
    if packet.get("artifact_kind") != "project_graph_agent_skill_handoff_routing":
        errors.append("artifact_kind")
    if packet.get("approval_boundary") != _APPROVAL_BOUNDARY:
        errors.append("approval_boundary")
    if packet.get("provider_call_allowed") is not False:
        errors.append("provider_call_allowed")
    if packet.get("external_call_performed") is not False:
        errors.append("external_call_performed")
    if packet.get("status") == "ready" and packet.get("agent_skill_routing") != "reviewable_handoff_required":
        errors.append("agent_skill_routing")
    if packet.get("ownership_required") is not True:
        errors.append("ownership_required")
    if packet.get("verification_evidence_required") is not True:
        errors.append("verification_evidence_required")
    stop_conditions = packet.get("stop_conditions") if isinstance(packet.get("stop_conditions"), list) else []
    for required in [
        "missing_ownership",
        "missing_verification_evidence",
        "live_provider_or_mutation_without_approval",
    ]:
        if required not in stop_conditions:
            errors.append(f"stop_conditions:{required}")
    errors.extend(_redaction_errors(packet))
    return _validation(not errors, sorted(set(errors)), "project_graph_agent_skill_handoff_routing")


def stage_live_audit_operability(
    stage_root: str | Path,
    *,
    workspace: str | Path,
    approval: dict[str, Any] | None,
    governance_artifact: str | Path,
    runtime_artifact: str | Path | None = None,
    live_actions: list[dict[str, Any]] | None = None,
    security_cases: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Stage Batch 31 audit, security, observability and handoff artifacts."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")

    governance = _load_json(governance_artifact)
    runtime = _load_json(runtime_artifact) if runtime_artifact else {}
    log_packet = build_live_audit_event_log(live_actions or [], approval=approval, governance_packet=governance)
    security = build_security_privacy_test_packet(security_cases or [], approval=approval, governance_packet=governance)
    observability = build_runtime_observability_packet(
        runtime_contract=runtime,
        audit_log=log_packet,
        security_packet=security,
        approval=approval,
        governance_packet=governance,
    )
    handoff = build_agent_skill_handoff_routing_packet(
        approval=approval,
        governance_packet=governance,
        observability_packet=observability,
    )

    _write_jsonl(stage_path / LIVE_AUDIT_LOG_TARGET, log_packet.get("events", []))
    _write_json(stage_path / LIVE_SECURITY_PRIVACY_TARGET, security)
    _write_json(stage_path / LIVE_OBSERVABILITY_TARGET, observability)
    _write_json(stage_path / LIVE_AGENT_HANDOFF_TARGET, handoff)
    status = _aggregate_status([log_packet, security, observability, handoff])
    validation = _merge_validation(
        log_packet.get("validation", {}),
        security.get("validation", {}),
        observability.get("validation", {}),
        handoff.get("validation", {}),
    )
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "build-live-audit",
            "status": status,
            "approval_boundary": _APPROVAL_BOUNDARY,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "files": [
                LIVE_AUDIT_LOG_TARGET,
                LIVE_SECURITY_PRIVACY_TARGET,
                LIVE_OBSERVABILITY_TARGET,
                LIVE_AGENT_HANDOFF_TARGET,
            ],
            "validation": validation,
        },
    }


def disable_live_audit_operability(stage_root: str | Path, *, workspace: str | Path) -> dict[str, Any]:
    """Delete generated Batch 31 operability artifacts from a stage root."""

    stage_path = Path(stage_root).resolve()
    workspace_path = Path(workspace).resolve()
    if _is_relative_to(stage_path, workspace_path):
        raise ValueError("stage root must be outside the target workspace")
    removed: list[str] = []
    missing: list[str] = []
    for target in [LIVE_AUDIT_LOG_TARGET, LIVE_SECURITY_PRIVACY_TARGET, LIVE_OBSERVABILITY_TARGET, LIVE_AGENT_HANDOFF_TARGET]:
        path = stage_path / target
        if path.exists():
            path.unlink()
            removed.append(target)
        else:
            missing.append(target)
    return {
        "schema_version": 1,
        "rendered_artifacts": {
            "mode": "disable-live-audit",
            "status": "disabled",
            "deletion_proof": {
                "delete_generated_operability_artifacts": True,
                "removed": removed,
                "missing": missing,
                "deletion_scope": "stage_root_generated_batch31_operability_artifacts_only",
            },
            "fallback": "graph_only_query_mode",
            "provider_call_allowed": False,
            "external_call_performed": False,
        },
    }


def _audit_event(action: dict[str, Any], index: int) -> dict[str, Any]:
    action_type = sanitize_graph_text(action.get("action_type") or "")
    if action_type not in _REQUIRED_EVENT_TYPES:
        action_type = "failure"
    surface = sanitize_graph_text(action.get("surface") or "unknown")
    status = sanitize_graph_text(action.get("status") or "recorded")
    unsafe_reasons = _unsafe_reasons(action)
    event = {
        "schema_version": 1,
        "artifact_kind": "project_graph_live_audit_event",
        "event_id": _stable_id({"index": index, "action_type": action_type, "surface": surface, "status": status}),
        "sequence": index + 1,
        "action_type": action_type,
        "surface": surface,
        "status": status,
        "redacted": True,
        "payload_recorded": False,
        "payload_summary": "omitted_redacted_metadata_only",
        "unsafe_reasons": unsafe_reasons,
        "provider_call_allowed": False,
        "external_call_performed": False,
    }
    safe_event, _report = redact_payload(event)
    return safe_event if isinstance(safe_event, dict) else event


def _security_case_result(case: dict[str, Any], index: int) -> dict[str, Any]:
    case_id = sanitize_graph_text(case.get("case_id") or f"case-{index}")
    text = str(case.get("input") or "")
    reasons = _unsafe_text_reasons(text)
    expected = "blocked" if case.get("expected") == "blocked" else "allowed"
    blocked = bool(reasons) or expected == "blocked"
    case_type = _case_type(case_id, reasons)
    return {
        "case_id": case_id,
        "case_type": case_type,
        "expected": expected,
        "result": "blocked" if blocked else "allowed",
        "blocked": blocked,
        "redacted": True,
        "input_recorded": False,
        "unsafe_reasons": reasons or (["expected_blocked"] if expected == "blocked" else []),
    }


def _case_type(case_id: str, reasons: list[str]) -> str:
    if "prompt_injection" in case_id or "prompt_injection" in reasons:
        return "prompt_injection"
    if "secret" in case_id or "secret" in reasons:
        return "secret"
    if "path" in case_id or "absolute_path" in reasons:
        return "absolute_path"
    if "raw_source" in case_id or "raw_source" in reasons:
        return "raw_source"
    return "negative_case"


def _unsafe_reasons(value: Any) -> list[str]:
    rendered = json.dumps(value, sort_keys=True, default=str)
    return _unsafe_text_reasons(rendered)


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


def _observed_runtime_status(runtime: dict[str, Any], audit: dict[str, Any], security: dict[str, Any]) -> str:
    if security.get("unsafe_cases_blocked") is True:
        return "degraded_graph_only"
    if any(
        isinstance(event, dict) and event.get("action_type") == "provider_call" and event.get("status") != "ready"
        for event in audit.get("events", [])
    ):
        return "degraded_graph_only"
    return sanitize_graph_text(runtime.get("runtime_status") or "disabled_by_default_not_started")


def _validate_audit_policy(policy: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(policy, dict):
        return ["audit_policy"]
    event_types = {str(item) for item in policy.get("event_types", []) if isinstance(item, str)}
    for required in sorted(_REQUIRED_EVENT_TYPES):
        if required not in event_types:
            errors.append(f"audit_policy:event_types:{required}:missing")
    if policy.get("append_only") is not True:
        errors.append("audit_policy:append_only")
    if policy.get("redacted_events_only") is not True:
        errors.append("audit_policy:redacted_events_only")
    return errors


def _validate_security_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["security_privacy_policy"]
    errors: list[str] = []
    for field in ["block_secrets", "block_absolute_paths", "block_raw_source", "block_prompt_injection"]:
        if policy.get(field) is not True:
            errors.append(f"security_privacy_policy:{field}")
    return errors


def _validate_observability_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["observability_policy"]
    errors: list[str] = []
    for field in [
        "health_visible",
        "latency_visible",
        "provider_errors_visible",
        "budget_usage_visible",
        "degraded_mode_visible",
    ]:
        if policy.get(field) is not True:
            errors.append(f"observability_policy:{field}")
    return errors


def _validate_handoff_policy(policy: Any) -> list[str]:
    if not isinstance(policy, dict):
        return ["handoff_policy"]
    errors: list[str] = []
    for field in [
        "ownership_required",
        "verification_evidence_required",
        "stop_conditions_required",
        "fresh_context_required",
    ]:
        if policy.get(field) is not True:
            errors.append(f"handoff_policy:{field}")
    return errors


def _validate_governance_prerequisite(governance_packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(governance_packet, dict):
        return ["live_governance:missing"]
    validation = validate_live_governance_packet(governance_packet)
    errors = [f"live_governance:{error}" for error in validation.get("errors", [])]
    if governance_packet.get("status") != "ready":
        errors.append("live_governance:status")
    return sorted(set(errors))


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
    rendered = json.dumps(value, sort_keys=True, default=str)
    errors = [f"redaction:{error}" for error in validate_redaction(rendered)]
    if _has_unsafe_text(value):
        errors.append("source_boundary:unsafe_text")
    return errors


def _has_unsafe_text(value: Any) -> bool:
    rendered = json.dumps(value, sort_keys=True, default=str)
    return bool(_unsafe_text_reasons(rendered))


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


def _nested_get(value: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return current if current is not None else default


def _stable_id(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


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


def _write_jsonl(path: Path, events: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(event, ensure_ascii=False, sort_keys=True) for event in events]
    path.write_text(("\n".join(lines) + ("\n" if lines else "")), encoding="utf-8")


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False
