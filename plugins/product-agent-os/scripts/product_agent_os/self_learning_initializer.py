from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.discovery import detect_product_agent_os_scope
from product_agent_os.self_learning_state import (
    DEFAULT_APPROVAL_STATE,
    DEFAULT_CADENCE_LEVEL,
    STATE_RELATIVE_PATH,
    build_default_self_learning_state,
    validate_self_learning_state,
    workspace_ref,
)
from product_agent_os.stage_manifest import MANIFEST_NAME, content_digest


SELF_LEARNING_STATE_INITIALIZER_PACKET_SCHEMA_VERSION = "self_learning_state_initializer_packet_v1"
STATE_INITIALIZER_PACKET_TARGET = ".codex/product-agent-os/self-learning/state-initializer-packet.json"


class SelfLearningInitializerError(RuntimeError):
    pass


def build_state_initializer_packet(
    *,
    workspace: str | Path,
    now: str | datetime,
    mode: str,
    plugin_version: str,
    installed_at: str | datetime | None = None,
    cadence_level: str = DEFAULT_CADENCE_LEVEL,
    approval_state: str = DEFAULT_APPROVAL_STATE,
    disable_reason: str | None = None,
) -> dict[str, Any]:
    """Build a review packet for the initial Self-Learning Loop state file."""
    now_dt = _parse_datetime(now)
    installed_dt = _parse_datetime(installed_at or now_dt)
    scope_packet = detect_product_agent_os_scope(workspace)
    state = build_default_self_learning_state(
        plugin_version=plugin_version,
        installed_at=_isoformat(installed_dt),
        cadence_level=cadence_level,
        approval_state=approval_state,
        disable_reason=disable_reason,
    )
    state_errors = validate_self_learning_state(state)
    blockers: list[str] = []
    if not scope_packet.get("eligible"):
        blockers.append("Product-Agent OS scope is not eligible")
    blockers.extend(state_errors)
    status = "blocked" if blockers else "ready_for_owner_review"
    return {
        "schema_version": SELF_LEARNING_STATE_INITIALIZER_PACKET_SCHEMA_VERSION,
        "generated_at": _isoformat(now_dt),
        "mode": mode,
        "status": status,
        "write_policy": "staged_only" if mode == "stage" else "read_only",
        "workspace_ref": (
            scope_packet.get("workspace_ref")
            if isinstance(scope_packet.get("workspace_ref"), dict)
            else workspace_ref(workspace)
        ),
        "product_agent_os_scope": scope_packet,
        "state_target_path": STATE_RELATIVE_PATH,
        "state_exists_in_workspace": (Path(workspace) / STATE_RELATIVE_PATH).exists(),
        "proposed_state": state,
        "validation_errors": state_errors,
        "state_written": False,
        "target_workspace_writes": "not_performed",
        "provider_calls": "not_performed",
        "live_eval_services": "not_performed",
        "schedule_status": "not_created",
        "automation_status": "not_created",
        "auto_apply": "disabled",
        "approval_required_before_workspace_write": True,
        "approval_boundary": [
            "workspace state write requires separate owner approval",
            "active schedule requires separate owner approval",
            "Codex App automation requires separate owner approval",
            "provider/model calls require separate owner approval",
            "candidate apply or target mutation requires separate owner approval",
        ],
        "rendered_artifacts": {
            "mode": mode,
            "targets": [STATE_RELATIVE_PATH, STATE_INITIALIZER_PACKET_TARGET],
            "validation": {"ok": not state_errors, "errors": state_errors},
        },
        "blockers": blockers,
    }


def stage_state_initializer_packet(
    *,
    workspace: str | Path,
    stage_root: str | Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise SelfLearningInitializerError("stage output directory must be outside workspace")
    if packet.get("status") == "blocked":
        raise SelfLearningInitializerError("initializer packet is blocked")

    state_json = json.dumps(packet["proposed_state"], ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    packet_json = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    contents = {
        STATE_RELATIVE_PATH: state_json,
        STATE_INITIALIZER_PACKET_TARGET: packet_json,
    }
    files: list[dict[str, Any]] = []
    for target, content in contents.items():
        _validate_relative_target(target)
        destination = stage_path / Path(target)
        _write_inside_root(stage_path, destination, content)
        files.append(
            {
                "key": _artifact_key(target),
                "category": "self-learning-loop",
                "target_path": target,
                "action": "create",
                "write_policy": "staged_only",
                "staged_path": target,
                "digest": content_digest(content),
                "managed_section": "",
            }
        )

    validation = {"ok": True, "errors": []}
    manifest = {
        "schema_version": "self_learning_state_initializer_manifest_v1",
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "workspace_ref": packet.get("workspace_ref") if isinstance(packet.get("workspace_ref"), dict) else workspace_ref(workspace),
        "raw_workspace_path_included": False,
        "stage_root_ref": {
            "path_hash": workspace_ref(stage_path).get("path_hash"),
            "raw_path_included": False,
        },
        "write_policy": "staged_only",
        "approval_required_before_workspace_write": True,
        "validation": validation,
        "files": files,
    }
    manifest_path = stage_path / MANIFEST_NAME
    _write_inside_root(stage_path, manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return {
        "mode": "stage",
        "root": "[STAGE_ROOT]",
        "targets": [STATE_RELATIVE_PATH, STATE_INITIALIZER_PACKET_TARGET],
        "files": files,
        "manifest_path": f"[STAGE_ROOT]/{MANIFEST_NAME}",
        "validation": validation,
    }


def _artifact_key(target: str) -> str:
    return target.replace("/", "-").replace(".", "-").strip("-")


def _write_inside_root(root: Path, destination: Path, content: str) -> None:
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise SelfLearningInitializerError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_relative_target(target: str) -> None:
    if not target:
        raise SelfLearningInitializerError("empty target path")
    path = Path(target)
    windows_path = PureWindowsPath(target)
    if (
        path.is_absolute()
        or windows_path.is_absolute()
        or bool(path.drive)
        or bool(windows_path.drive)
        or ".." in path.parts
        or ".." in windows_path.parts
    ):
        raise SelfLearningInitializerError(f"invalid target path: {target}")


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _isoformat(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
