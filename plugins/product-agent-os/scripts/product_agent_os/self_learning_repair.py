from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any


SELF_LEARNING_REPAIR_TASK_SCHEMA_VERSION = "self_learning_staged_repair_task_v1"
SELF_LEARNING_REPAIR_RESULT_SCHEMA_VERSION = "self_learning_staged_repair_result_v1"

_CHANGE_SURFACES = {
    "docs",
    "tests",
    "plugin_script",
    "skill_contract",
    "eval_fixture",
    "control_plane",
}
_APPROVAL_STATES = {"not_requested", "approved_for_staged_repair"}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def build_staged_repair_task_contract(
    *,
    candidate_id: str,
    objective: str,
    allowed_files: list[str],
    validation_commands: list[str],
    change_surface: str,
    forbidden_files: list[str] | None = None,
    expected_behavior: list[str] | None = None,
    forbidden_behavior: list[str] | None = None,
    rollback_target: str | None = None,
    approval_state: str = "not_requested",
    generated_at: str | None = None,
) -> dict[str, Any]:
    task_id = _stable_id("sll-repair", candidate_id, objective)
    return {
        "schema_version": SELF_LEARNING_REPAIR_TASK_SCHEMA_VERSION,
        "task_id": task_id,
        "candidate_id": candidate_id,
        "generated_at": generated_at or _now(),
        "objective": objective,
        "change_surface": change_surface,
        "allowed_files": allowed_files,
        "forbidden_files": forbidden_files or [],
        "expected_behavior": expected_behavior or [],
        "forbidden_behavior": forbidden_behavior or [
            "auto_apply",
            "target_workspace_write",
            "provider_call",
            "external_write",
        ],
        "validation_commands": validation_commands,
        "rollback_target": rollback_target or "no-op until owner-approved staged packet is applied",
        "privacy_boundary": {
            "raw_private_data_allowed": False,
            "raw_workspace_paths_allowed": False,
            "redacted_summaries_only": True,
        },
        "approval_state": approval_state,
        "write_policy": "staged_only",
        "auto_apply": "disabled",
        "target_workspace_writes": "not_performed",
        "provider_calls": "not_performed",
        "codex_exec_status": "not_run",
        "owner_review_required_before_apply": True,
    }


def validate_staged_repair_task_contract(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["repair_task:not_object"]
    errors: list[str] = []
    if packet.get("schema_version") != SELF_LEARNING_REPAIR_TASK_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    for field in (
        "task_id",
        "candidate_id",
        "objective",
        "change_surface",
        "allowed_files",
        "validation_commands",
        "rollback_target",
        "privacy_boundary",
        "approval_state",
    ):
        if not packet.get(field):
            errors.append(f"{field}:required")
    if packet.get("change_surface") not in _CHANGE_SURFACES:
        errors.append("change_surface:invalid")
    if packet.get("approval_state") not in _APPROVAL_STATES:
        errors.append("approval_state:invalid")
    if packet.get("write_policy") != "staged_only":
        errors.append("write_policy:must_be_staged_only")
    if packet.get("auto_apply") != "disabled":
        errors.append("auto_apply:must_be_disabled")
    if packet.get("target_workspace_writes") != "not_performed":
        errors.append("target_workspace_writes:must_be_not_performed")
    if packet.get("provider_calls") != "not_performed":
        errors.append("provider_calls:must_be_not_performed")
    _validate_relative_paths(packet.get("allowed_files"), errors, "allowed_files", required=True)
    _validate_relative_paths(packet.get("forbidden_files", []), errors, "forbidden_files", required=False)
    if _contains_private_reference(packet):
        errors.append("raw_private_reference_not_allowed")
    return errors


def build_staged_repair_result_packet(
    *,
    task_contract: dict[str, Any],
    changed_files: list[str],
    validation_results: list[dict[str, Any]],
    summary: str,
    generated_at: str | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": SELF_LEARNING_REPAIR_RESULT_SCHEMA_VERSION,
        "task_id": task_contract.get("task_id"),
        "candidate_id": task_contract.get("candidate_id"),
        "generated_at": generated_at or _now(),
        "summary": summary,
        "status": "ready_for_owner_review",
        "write_policy": "staged_only",
        "changed_files": changed_files,
        "allowed_files": task_contract.get("allowed_files", []),
        "validation_results": validation_results,
        "auto_apply": "disabled",
        "target_workspace_writes": "not_performed",
        "provider_calls": "not_performed",
        "codex_exec_status": "not_run" if not validation_results else "local_commands_reported",
        "owner_review_required_before_apply": True,
        "rollback_target": task_contract.get("rollback_target"),
        "unsupported_claims": [
            "repair was applied to workspace",
            "owner approved the repair",
            "provider or live eval verified the repair",
        ],
    }


def validate_staged_repair_result_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["repair_result:not_object"]
    errors: list[str] = []
    if packet.get("schema_version") != SELF_LEARNING_REPAIR_RESULT_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    allowed_files = set(packet.get("allowed_files", [])) if isinstance(packet.get("allowed_files"), list) else set()
    changed_files = packet.get("changed_files")
    if not isinstance(changed_files, list) or not changed_files:
        errors.append("changed_files:required")
    else:
        for file_path in changed_files:
            if not isinstance(file_path, str) or _unsafe_relative_path(file_path):
                errors.append("changed_files:invalid_path")
            elif file_path not in allowed_files:
                errors.append(f"{file_path}:outside_allowed_files")
    if packet.get("write_policy") != "staged_only":
        errors.append("write_policy:must_be_staged_only")
    if packet.get("auto_apply") != "disabled":
        errors.append("auto_apply:must_be_disabled")
    if packet.get("target_workspace_writes") != "not_performed":
        errors.append("target_workspace_writes:must_be_not_performed")
    if packet.get("provider_calls") != "not_performed":
        errors.append("provider_calls:must_be_not_performed")
    validation_results = packet.get("validation_results")
    if not isinstance(validation_results, list):
        errors.append("validation_results:must_be_list")
    elif not validation_results:
        errors.append("validation_results:required")
    else:
        for result in validation_results:
            if not isinstance(result, dict):
                errors.append("validation_result:not_object")
                continue
            if result.get("status") not in {"passed", "failed", "blocked", "not_run"}:
                errors.append("validation_result.status:invalid")
            if not result.get("command"):
                errors.append("validation_result.command:required")
    if _contains_private_reference(packet):
        errors.append("raw_private_reference_not_allowed")
    return errors


def _validate_relative_paths(value: Any, errors: list[str], field: str, *, required: bool) -> None:
    if not isinstance(value, list):
        errors.append(f"{field}:must_be_list")
        return
    if required and not value:
        errors.append(f"{field}:must_be_non_empty_list")
        return
    for item in value:
        if not isinstance(item, str) or _unsafe_relative_path(item):
            errors.append(f"{field}:invalid_path")


def _unsafe_relative_path(value: str) -> bool:
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return (
        not value
        or path.is_absolute()
        or windows_path.is_absolute()
        or bool(path.drive)
        or bool(windows_path.drive)
        or ".." in path.parts
        or ".." in windows_path.parts
    )


def _contains_private_reference(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_private_reference(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_private_reference(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return (
            "c:\\users\\" in lowered
            or lowered.startswith("/users/")
            or lowered.startswith("/home/")
            or bool(_EMAIL_RE.search(value))
        )
    return False


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
