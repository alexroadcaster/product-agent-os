from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


SELF_LEARNING_STATE_SCHEMA_VERSION = "self_learning_state_v1"
SELF_LEARNING_TRIGGER_POLICY_SCHEMA_VERSION = "self_learning_trigger_policy_v1"
STATE_RELATIVE_PATH = ".codex/product-agent-os/self-learning-state.json"
DEFAULT_PLUGIN_ID = "product-agent-os"
DEFAULT_CADENCE_LEVEL = "manual_only"
DEFAULT_APPROVAL_STATE = "manual_only"
WEEKLY_INTERVAL = timedelta(days=7)


TRIGGER_CLASSES: list[dict[str, Any]] = [
    {
        "id": "manual_now",
        "label": "Run manually now",
        "activation": "owner_requested_manual_skill_or_cli",
        "action": "recommend_manual_run_only",
        "approval_required": False,
    },
    {
        "id": "weekly_due_check",
        "label": "Weekly due check",
        "activation": "manual_due_check_or_future_approved_schedule",
        "action": "report_due_status_only",
        "approval_required": False,
    },
    {
        "id": "on_change",
        "label": "After Product-Agent OS change",
        "activation": "skill_config_docs_or_control_plane_change",
        "action": "recommend_review_only",
        "approval_required": False,
    },
    {
        "id": "post_failure_review",
        "label": "After failed verification or owner rejection",
        "activation": "explicit_failure_or_reopen_signal",
        "action": "recommend_review_only",
        "approval_required": False,
    },
    {
        "id": "post_owner_feedback_review",
        "label": "After owner feedback",
        "activation": "owner_provided_redacted_feedback",
        "action": "recommend_review_only",
        "approval_required": False,
    },
    {
        "id": "release_readiness_review",
        "label": "Before release readiness claim",
        "activation": "release_or_promotion_gate",
        "action": "recommend_review_only",
        "approval_required": True,
    },
]


CADENCE_OPTIONS: list[dict[str, Any]] = [
    {
        "id": "manual_only",
        "label": "Manual only",
        "due_basis": "installed_at_or_last_success_at",
        "schedule_status": "not_created",
        "description": "The owner can check due status and run the loop manually; no recurring job exists.",
    },
    {
        "id": "weekly",
        "label": "Weekly due check",
        "due_basis": "last_success_at_or_installed_at_plus_7_days",
        "schedule_status": "not_created",
        "description": "A weekly recommendation can be shown, but it is not an active schedule.",
    },
    {
        "id": "on_change",
        "label": "After Product-Agent OS changes",
        "due_basis": "skill_config_docs_or_control_plane_change",
        "schedule_status": "not_created",
        "description": "The loop can be suggested after local Product-Agent OS changes.",
    },
    {
        "id": "disabled",
        "label": "Disabled",
        "due_basis": "none",
        "schedule_status": "not_created",
        "description": "The due check reports disabled until the owner changes the state.",
    },
]


def build_trigger_policy() -> dict[str, Any]:
    return {
        "schema_version": SELF_LEARNING_TRIGGER_POLICY_SCHEMA_VERSION,
        "write_policy": "read_only_due_check",
        "schedule_status": "not_created",
        "automation_status": "not_created",
        "auto_apply_status": "not_enabled",
        "trigger_classes": TRIGGER_CLASSES,
        "cadence_options": CADENCE_OPTIONS,
        "approval_boundary": [
            "active scheduler requires separate exact approval",
            "Codex App automation requires separate exact approval",
            "hooks integration requires separate exact approval",
            "provider/model calls require separate exact approval",
            "target workspace writes require separate exact approval",
            "auto-apply is disabled unless a future approved automation packet exists",
        ],
    }


def build_default_self_learning_state(
    *,
    plugin_version: str,
    installed_at: str,
    cadence_level: str = DEFAULT_CADENCE_LEVEL,
    approval_state: str = DEFAULT_APPROVAL_STATE,
    disable_reason: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": SELF_LEARNING_STATE_SCHEMA_VERSION,
        "plugin_id": DEFAULT_PLUGIN_ID,
        "plugin_version": plugin_version,
        "installed_at": installed_at,
        "last_analysis_at": None,
        "last_success_at": None,
        "last_failure_at": None,
        "next_due_at": None,
        "cadence_level": cadence_level,
        "last_report_id": None,
        "last_metrics_digest": None,
        "approval_state": approval_state,
        "disable_reason": disable_reason,
    }


def load_self_learning_state(workspace: str | Path) -> tuple[dict[str, Any] | None, list[str]]:
    state_path = Path(workspace) / STATE_RELATIVE_PATH
    return load_self_learning_state_file(state_path)


def load_self_learning_state_file(path: str | Path) -> tuple[dict[str, Any] | None, list[str]]:
    state_path = Path(path)
    if not state_path.exists():
        return None, ["state_file:missing"]
    try:
        payload = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, [f"state_file:invalid_json:{exc.__class__.__name__}"]
    if not isinstance(payload, dict):
        return None, ["state_file:not_object"]
    return payload, []


def evaluate_self_learning_due(state: dict[str, Any] | None, *, now: str | datetime) -> dict[str, Any]:
    trigger_policy = build_trigger_policy()
    try:
        now_dt = _parse_datetime(now)
    except ValueError:
        return _base_due_packet(
            status="state_invalid",
            now=datetime.now(UTC).replace(microsecond=0),
            trigger_policy=trigger_policy,
            errors=["now:invalid_datetime"],
        )
    errors = validate_self_learning_state(state)
    if errors:
        return _base_due_packet(
            status="state_invalid",
            now=now_dt,
            trigger_policy=trigger_policy,
            errors=errors,
        )

    assert isinstance(state, dict)
    cadence_level = str(state.get("cadence_level") or DEFAULT_CADENCE_LEVEL)
    approval_state = str(state.get("approval_state") or DEFAULT_APPROVAL_STATE)
    if cadence_level == "disabled" or approval_state == "disabled":
        packet = _base_due_packet(status="disabled", now=now_dt, trigger_policy=trigger_policy)
        packet["disable_reason"] = state.get("disable_reason") or "disabled"
        return packet

    if cadence_level == "on_change":
        packet = _base_due_packet(status="not_due", now=now_dt, trigger_policy=trigger_policy)
        packet.update(
            {
                "action": "wait_for_product_agent_os_change",
                "cadence_level": cadence_level,
                "approval_state": approval_state,
                "due_basis": "change_event_required",
                "installed_at": state.get("installed_at"),
                "last_analysis_at": state.get("last_analysis_at"),
                "last_success_at": state.get("last_success_at"),
                "last_failure_at": state.get("last_failure_at"),
                "next_due_at": None,
                "last_report_id": state.get("last_report_id"),
                "last_metrics_digest": state.get("last_metrics_digest"),
            }
        )
        return packet

    due_at, due_basis = _due_at(state)
    status = "due" if now_dt >= due_at else "not_due"
    packet = _base_due_packet(status=status, now=now_dt, trigger_policy=trigger_policy)
    packet.update(
        {
            "action": "manual_run_available" if status == "due" else "wait_until_next_due",
            "cadence_level": cadence_level,
            "approval_state": approval_state,
            "due_basis": "manual_only" if cadence_level == "manual_only" else due_basis,
            "installed_at": state.get("installed_at"),
            "last_analysis_at": state.get("last_analysis_at"),
            "last_success_at": state.get("last_success_at"),
            "last_failure_at": state.get("last_failure_at"),
            "next_due_at": _isoformat(due_at),
            "last_report_id": state.get("last_report_id"),
            "last_metrics_digest": state.get("last_metrics_digest"),
        }
    )
    return packet


def validate_self_learning_state(state: Any) -> list[str]:
    if not isinstance(state, dict):
        return ["state:not_object"]
    errors: list[str] = []
    required = [
        "schema_version",
        "plugin_id",
        "plugin_version",
        "installed_at",
        "last_analysis_at",
        "last_success_at",
        "last_failure_at",
        "next_due_at",
        "cadence_level",
        "last_report_id",
        "last_metrics_digest",
        "approval_state",
        "disable_reason",
    ]
    for field in required:
        if field not in state:
            errors.append(f"{field}:required")
    if state.get("schema_version") != SELF_LEARNING_STATE_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    if state.get("plugin_id") != DEFAULT_PLUGIN_ID:
        errors.append("plugin_id:invalid")
    if state.get("cadence_level") not in {"manual_only", "weekly", "weekly_due_check", "on_change", "disabled"}:
        errors.append("cadence_level:invalid")
    if state.get("approval_state") not in {"manual_only", "disabled", "candidate_only", "approval_required"}:
        errors.append("approval_state:invalid")
    for field in ("installed_at", "last_analysis_at", "last_success_at", "last_failure_at", "next_due_at"):
        value = state.get(field)
        if value is not None and not _can_parse_datetime(value):
            errors.append(f"{field}:invalid_datetime")
    return errors


def workspace_ref(workspace: str | Path) -> dict[str, Any]:
    raw = str(Path(workspace).resolve())
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return {
        "path_hash": f"sha256:{digest}",
        "raw_path_included": False,
    }


def _base_due_packet(*, status: str, now: datetime, trigger_policy: dict[str, Any], errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "schema_version": "self_learning_due_check_v1",
        "status": status,
        "now": _isoformat(now),
        "analysis_executed": False,
        "state_written": False,
        "trigger_policy": trigger_policy,
        "errors": errors or [],
    }


def _due_at(state: dict[str, Any]) -> tuple[datetime, str]:
    explicit_next = state.get("next_due_at")
    if explicit_next:
        return _parse_datetime(explicit_next), "next_due_at"
    if state.get("last_success_at"):
        return _parse_datetime(state["last_success_at"]) + WEEKLY_INTERVAL, "last_success_at_plus_7_days"
    if state.get("last_analysis_at"):
        return _parse_datetime(state["last_analysis_at"]) + WEEKLY_INTERVAL, "last_analysis_at_plus_7_days"
    return _parse_datetime(state.get("installed_at")) + WEEKLY_INTERVAL, "installed_at_plus_7_days"


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        normalized = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _can_parse_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        _parse_datetime(value)
    except ValueError:
        return False
    return True


def _isoformat(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
