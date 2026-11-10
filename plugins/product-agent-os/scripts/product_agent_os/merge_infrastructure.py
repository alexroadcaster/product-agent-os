from __future__ import annotations

import json
import re
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.merge_markdown import merge_section
from product_agent_os.stage_manifest import (
    APPROVAL_TEMPLATE_NAME,
    build_approval_template,
    canonical_json,
    content_digest,
    file_digest,
    load_stage_manifest,
    validate_approval_record,
    workspace_audit_digest,
)


OWNER = "product-agent-os"
ROLLBACK_MANIFEST_NAME = "product-agent-os-rollback-manifest.json"
MERGE_PLAN_NAME = "product-agent-os-merge-plan.json"
HOOKS_CONFIG_TARGET = ".codex/hooks.json"
ALLOWED_HOOK_EVENTS = {"SessionStart", "PreToolUse", "PermissionRequest", "PostToolUse", "Stop"}
WRITABLE_ACTIONS = {"create_file", "append_managed_section", "replace_managed_section"}
SAFE_EXISTING_SUFFIXES = {".md", ".markdown", ".toml", ".json", ".py"}
SECTION_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


class MergeInfrastructureError(RuntimeError):
    pass


def build_merge_plan(workspace: str | Path, stage_root: str | Path) -> dict[str, Any]:
    """Build a read-only merge plan and write approval artifacts into the stage root."""
    plan = _build_merge_plan(workspace, stage_root, enable_hooks=False)
    _write_plan_artifacts(Path(stage_root), plan)
    return plan


def apply_merge_plan(
    workspace: str | Path,
    stage_root: str | Path,
    approval_file: str | Path,
) -> dict[str, Any]:
    """Apply exact approvals; formation creates use a write-ahead recovery receipt."""
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    approval_payload = _load_approval_file(Path(approval_file))
    approval = approval_payload.get("approval") if isinstance(approval_payload, dict) else {}
    enable_hooks = bool(approval.get("enable_hooks")) if isinstance(approval, dict) else False
    hook_approval_errors = _hook_approval_errors(approval) if enable_hooks else []
    if hook_approval_errors:
        raise MergeInfrastructureError("; ".join(hook_approval_errors))

    current_plan = _build_merge_plan(workspace_path, stage_path, enable_hooks=False)
    effective_current_plan = _with_hook_activation(current_plan, workspace_path, enable_hooks)
    if effective_current_plan.get("status") == "blocked" or effective_current_plan.get("blocked"):
        raise MergeInfrastructureError(
            "current merge plan is blocked: " + "; ".join(effective_current_plan.get("blocked", []))
        )
    required_decisions = _approval_required_decisions(effective_current_plan)
    required_targets = [item["target_path"] for item in required_decisions]
    required_actions = sorted({item["action"] for item in required_decisions})
    _reject_changed_current_plan_id(stage_path, approval_payload, effective_current_plan)
    errors = validate_approval_record(approval_payload, effective_current_plan["id"], required_targets, required_actions)
    if errors:
        raise MergeInfrastructureError("; ".join(errors))

    _reject_stale_decisions(effective_current_plan, effective_current_plan, required_decisions)

    rollback_path = stage_path / ROLLBACK_MANIFEST_NAME
    _preflight_apply(workspace_path, rollback_path, required_decisions)
    entries: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    _write_rollback_manifest(rollback_path, workspace_path, entries)
    formation_apply = "formation" in load_stage_manifest(stage_path)
    for decision in required_decisions:
        current_decision = _decision_by_target(effective_current_plan, decision["target_path"])
        if current_decision["action"] != decision["action"]:
            raise MergeInfrastructureError(f"stale decision for {decision['target_path']}")
        entry = _rollback_entry(workspace_path, stage_path, current_decision)
        if formation_apply:
            # Write-ahead receipt closes the crash window after file replacement.
            if current_decision['action'] != 'create_file':
                raise MergeInfrastructureError('formation may only create absent files')
            entry.update(formation=True, prepared=True, digest_after=current_decision['staged_digest'])
            entries.append(entry)
            _write_rollback_manifest(rollback_path, workspace_path, entries)
        _apply_decision(workspace_path, stage_path, current_decision | {'formation_atomic_create': formation_apply})
        entry['prepared'] = False
        entry["digest_after"] = file_digest(workspace_path / current_decision["target_path"])
        entry["verification"] = {"digest_after_recorded": True}
        if not formation_apply:
            entries.append(entry)
        results.append(
            {
                "target_path": current_decision["target_path"],
                "action": current_decision["action"],
                "status": "applied",
            }
        )
        _write_rollback_manifest(rollback_path, workspace_path, entries)

    return {
        "status": "applied",
        "merge_plan_id": effective_current_plan["id"],
        "results": results,
        "rollback_manifest": str(rollback_path),
    }


def rollback_merge(workspace: str | Path, rollback_manifest: str | Path) -> dict[str, Any]:
    """Restore owned writes only when current bytes still match the recovery record."""
    workspace_path = Path(workspace).resolve()
    manifest_path = Path(rollback_manifest).resolve()
    payload = _load_json_file(manifest_path, "rollback manifest")
    if not isinstance(payload, dict):
        raise MergeInfrastructureError("rollback manifest must be an object")
    _validate_rollback_workspace(workspace_path, payload)
    entries = payload.get("entries")
    if not isinstance(entries, list):
        raise MergeInfrastructureError("rollback manifest entries must be a list")

    if any(isinstance(e, dict) and e.get('formation') for e in entries):
        from product_agent_os.control_plane_compaction import _authority
        try:
            _authority(workspace_path, [e['target_path'] for e in entries])
        except ValueError as exc:
            raise MergeInfrastructureError(str(exc)) from exc
    results: list[dict[str, str]] = []
    for entry in reversed(entries):
        if not isinstance(entry, dict):
            raise MergeInfrastructureError("rollback manifest entry must be an object")
        target_path = str(entry.get("target_path", ""))
        target = _target_path(workspace_path, target_path)
        _reject_symlink_path(target, workspace_path, include_file=target.exists() or target.is_symlink())
        expected_after = str(entry.get("digest_after", ""))
        if not target.exists():
            if entry.get('formation') and entry.get('prepared') and entry.get('action') == 'created':
                results.append({'target_path': target_path, 'status': 'not_written'})
                continue
            raise MergeInfrastructureError(f"target changed after apply: {target_path}")
        if not target.is_file():
            raise MergeInfrastructureError(f"rollback target is not a file: {target_path}")
        try:
            current_digest = file_digest(target)
        except OSError as exc:
            raise MergeInfrastructureError(f"unable to read rollback target digest: {target_path}: {exc}") from exc
        if current_digest != expected_after:
            raise MergeInfrastructureError(f"target changed after apply: {target_path}")
        if entry.get("action") == "created":
            try:
                target.unlink()
            except OSError as exc:
                raise MergeInfrastructureError(f"unable to remove created target during rollback: {target_path}: {exc}") from exc
        elif entry.get("action") == "updated":
            backup_path = _backup_path(manifest_path.parent, str(entry.get("backup_path", "")))
            if not backup_path.exists() or not backup_path.is_file():
                raise MergeInfrastructureError(f"rollback backup is missing or not a file: {entry.get('backup_path')}")
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copyfile(backup_path, target)
            except OSError as exc:
                raise MergeInfrastructureError(f"unable to restore rollback backup for {target_path}: {exc}") from exc
        else:
            raise MergeInfrastructureError(f"unknown rollback action: {entry.get('action')}")
        results.append({"target_path": target_path, "status": "rolled_back"})

    return {"status": "rolled_back", "results": results}


def _build_merge_plan(
    workspace: str | Path,
    stage_root: str | Path,
    *,
    enable_hooks: bool = False,
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    try:
        manifest = load_stage_manifest(stage_path)
    except ValueError as exc:
        raise MergeInfrastructureError(f"invalid stage manifest: {exc}") from exc

    blocked: list[str] = []
    warnings: list[str] = []
    manifest_binding_errors = _manifest_binding_errors(workspace_path, manifest)
    if manifest_binding_errors:
        blocked.extend(manifest_binding_errors)
        decisions = [
            _blocked_decision_for_entry(item, "; ".join(manifest_binding_errors))
            for item in manifest.get("files", [])
            if isinstance(item, dict)
        ]
        return _merge_plan(
            workspace_path,
            stage_path,
            manifest,
            decisions,
            blocked,
            warnings,
        )

    decisions = [
        _decision_for_entry(workspace_path, stage_path, item, enable_hooks, blocked, warnings)
        for item in manifest.get("files", [])
    ]
    return _merge_plan(
        workspace_path,
        stage_path,
        manifest,
        decisions,
        blocked,
        warnings,
    )


def _merge_plan(
    workspace_path: Path,
    stage_path: Path,
    manifest: dict[str, Any],
    decisions: list[dict[str, Any]],
    blocked: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    status = "blocked" if blocked else "needs_approval" if any(item["approval_required"] for item in decisions) else "ready"
    plan_seed = {
        "workspace": str(workspace_path),
        "stage_manifest": manifest,
        "decisions": decisions,
        "hook_activation": "approval-gated",
    }
    plan_id = "merge-plan-" + content_digest(canonical_json(plan_seed))
    approval_template_path = stage_path / APPROVAL_TEMPLATE_NAME
    return {
        "id": plan_id,
        "status": status,
        "workspace": str(workspace_path),
        "stage_root": str(stage_path),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "decisions": decisions,
        "blocked": _unique(blocked),
        "warnings": _unique(warnings),
        "verification": {
            "stage_manifest_loaded": True,
            "path_safety_checked": True,
            "symlink_safety_checked": True,
        },
        "approval_template_path": str(approval_template_path),
    }


def _manifest_binding_errors(workspace: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "formation" in manifest:
        from product_agent_os.project_formation import formation_binding_errors
        errors.extend(formation_binding_errors(workspace, manifest["formation"],
                      [item['target_path'] for item in manifest['files']]))
    manifest_workspace = str(manifest.get("workspace", "")).strip()
    if not manifest_workspace:
        errors.append("stage manifest workspace is required")
    elif Path(manifest_workspace).resolve() != workspace:
        errors.append("stage manifest workspace does not match requested workspace")

    target_paths = [
        item["target_path"]
        for item in manifest.get("files", [])
        if isinstance(item, dict) and isinstance(item.get("target_path"), str)
    ]
    expected_digest = workspace_audit_digest(workspace, target_paths)
    if manifest.get("workspace_audit_digest") != expected_digest:
        errors.append("stage manifest workspace audit digest is stale")
    return errors


def _blocked_decision_for_entry(item: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "target_path": str(item.get("target_path", "")),
        "staged_path": str(item.get("staged_path", "")),
        "target_digest_before": "",
        "staged_digest": str(item.get("digest", "")),
        "approval_required": False,
        "rollback_entry": {},
        "managed_section": str(item.get("managed_section", "")),
        "action": "blocked",
        "reason": reason,
    }


def _decision_for_entry(
    workspace: Path,
    stage_root: Path,
    item: dict[str, Any],
    enable_hooks: bool,
    blocked: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    target_path_value = str(item.get("target_path", ""))
    staged_path_value = str(item.get("staged_path", ""))
    managed_section = str(item.get("managed_section", ""))
    base = {
        "target_path": target_path_value,
        "staged_path": staged_path_value,
        "target_digest_before": "",
        "staged_digest": str(item.get("digest", "")),
        "approval_required": False,
        "rollback_entry": {},
        "managed_section": managed_section,
        "reason": "",
    }
    try:
        target = _target_path(workspace, target_path_value)
        staged = _staged_path(stage_root, staged_path_value)
        _reject_symlink_path(target, workspace, include_file=target.exists() or target.is_symlink())
        _reject_symlink_path(staged, stage_root, include_file=True)
    except MergeInfrastructureError as exc:
        blocked.append(f"{target_path_value}: {exc}")
        return base | {"action": "blocked", "reason": str(exc)}

    if item.get("action") == "blocked" or item.get("write_policy") == "blocked":
        reason = "stage manifest marks target blocked"
        blocked.append(f"{target_path_value}: {reason}")
        return base | {"action": "blocked", "reason": reason}
    if not staged.exists() or not staged.is_file():
        reason = "staged file is missing or not a file"
        blocked.append(f"{target_path_value}: {reason}")
        return base | {"action": "blocked", "reason": reason}

    actual_staged_digest = file_digest(staged)
    base["staged_digest"] = actual_staged_digest
    if item.get("digest") and item.get("digest") != actual_staged_digest:
        reason = "staged digest does not match manifest"
        blocked.append(f"{target_path_value}: {reason}")
        return base | {"action": "blocked", "reason": reason}
    if target.exists() and not target.is_file():
        reason = "target exists and is not a file"
        blocked.append(f"{target_path_value}: {reason}")
        return base | {"action": "blocked", "reason": reason}
    if target.exists():
        base["target_digest_before"] = file_digest(target)
    if managed_section and not SECTION_ID_PATTERN.fullmatch(managed_section):
        reason = f"invalid managed_section: {managed_section}"
        blocked.append(f"{target_path_value}: {reason}")
        return base | {"action": "blocked", "reason": reason}

    if item.get("preserve_existing") is True and target.exists():
        # Regeneration has no ancestor baseline proving a safe replacement.
        # Bulk approval cannot silently upgrade a preserved proposal to a write.
        return base | {"action": "companion_only", "approval_required": False,
                       "reason": "filled managed content preserved; explicit content merge required"}
    action, reason = _planned_action(target, target_path_value, managed_section, enable_hooks, blocked, warnings)
    decision = base | {
        "action": action,
        "approval_required": action in WRITABLE_ACTIONS,
        "reason": reason,
    }
    if decision["approval_required"]:
        decision["rollback_entry"] = {
            "target_path": target_path_value,
            "action": "created" if not target.exists() else "updated",
            "digest_before": decision["target_digest_before"],
        }
    return decision


def _planned_action(
    target: Path,
    target_path: str,
    managed_section: str,
    enable_hooks: bool,
    blocked: list[str],
    warnings: list[str],
) -> tuple[str, str]:
    if target_path == HOOKS_CONFIG_TARGET:
        if not enable_hooks:
            warnings.append(f"{HOOKS_CONFIG_TARGET}: hook activation requires explicit enable_hooks approval")
            return "companion_only", "hook activation is gated"
        if target.exists():
            reason = "existing hooks.json replacement is blocked in Track 4"
            blocked.append(f"{target_path}: {reason}")
            return "blocked", reason
        return "create_file", "enable_hooks approval allows creating hooks.json"

    if not target.exists():
        return "create_file", "target is absent"

    suffix = target.suffix.lower()
    if suffix not in SAFE_EXISTING_SUFFIXES and not _is_config_or_hook_path(target_path):
        return "companion_only", "existing file type is not safe for managed merge"
    if suffix != ".md" and managed_section:
        return "companion_only", "managed section merge is only supported for markdown in this slice"
    if not managed_section:
        return "companion_only", "existing target has no managed section contract"

    try:
        existing = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "companion_only", "existing target is not safely readable as utf-8"

    marker_error = _managed_marker_error(existing, managed_section)
    if marker_error:
        blocked.append(f"{target_path}: {marker_error}")
        return "blocked", marker_error
    start = f"<!-- {OWNER}:start {managed_section} -->"
    if start in existing:
        return "replace_managed_section", "matching managed section exists"
    return "append_managed_section", "target exists without managed section marker"


def _apply_decision(workspace: Path, stage_root: Path, decision: dict[str, Any]) -> None:
    target = _target_path(workspace, decision["target_path"])
    staged = _staged_path(stage_root, decision["staged_path"])
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        if decision["action"] == "create_file":
            if decision.get('formation_atomic_create'):
                from product_agent_os.control_plane_compaction import _write
                if target.exists():
                    raise MergeInfrastructureError('formation target appeared during apply')
                _write(target, staged.read_bytes())
                return
            shutil.copyfile(staged, target)
            return
        existing = target.read_text(encoding="utf-8")
        staged_text = staged.read_text(encoding="utf-8")
        body = _managed_body(staged_text, decision["managed_section"])
        updated = merge_section(existing, OWNER, decision["managed_section"], body)
        target.write_text(updated, encoding="utf-8", newline="")
    except ValueError as exc:
        raise MergeInfrastructureError(f"unable to merge managed section for {decision['target_path']}: {exc}") from exc
    except (OSError, UnicodeError) as exc:
        raise MergeInfrastructureError(f"unable to apply merge decision for {decision['target_path']}: {exc}") from exc


def _preflight_apply(workspace: Path, rollback_path: Path, decisions: list[dict[str, Any]]) -> None:
    if rollback_path.exists() and not rollback_path.is_file():
        raise MergeInfrastructureError(f"rollback manifest path is not a file: {rollback_path}")
    _reject_target_conflicts(decisions)
    for decision in decisions:
        target = _target_path(workspace, decision["target_path"])
        _reject_symlink_path(target, workspace, include_file=target.exists() or target.is_symlink())
        _reject_non_directory_parents(workspace, target)


def _reject_target_conflicts(decisions: list[dict[str, Any]]) -> None:
    targets = sorted(str(item["target_path"]) for item in decisions)
    target_parts = [
        (target, tuple(part.casefold() for part in PureWindowsPath(target).parts))
        for target in targets
    ]
    for index, (left_target, left_parts) in enumerate(target_parts):
        for right_target, right_parts in target_parts[index + 1 :]:
            if left_parts == right_parts or _is_ancestor_parts(left_parts, right_parts):
                raise MergeInfrastructureError(f"approved target conflict: {left_target} conflicts with {right_target}")
            if _is_ancestor_parts(right_parts, left_parts):
                raise MergeInfrastructureError(f"approved target conflict: {right_target} conflicts with {left_target}")


def _is_ancestor_parts(parent: tuple[str, ...], child: tuple[str, ...]) -> bool:
    return len(parent) < len(child) and child[: len(parent)] == parent


def _reject_non_directory_parents(workspace: Path, target: Path) -> None:
    relative_parts = target.relative_to(workspace).parts[:-1]
    cursor = workspace
    for part in relative_parts:
        cursor = cursor / part
        if cursor.exists() and not cursor.is_dir():
            raise MergeInfrastructureError(f"target parent is not a directory: {cursor}")


def _validate_rollback_workspace(workspace: Path, payload: dict[str, Any]) -> None:
    manifest_workspace = payload.get("workspace")
    if not isinstance(manifest_workspace, str) or not manifest_workspace.strip():
        raise MergeInfrastructureError("rollback manifest workspace is required")
    if Path(manifest_workspace).resolve() != workspace:
        raise MergeInfrastructureError("rollback manifest workspace does not match requested workspace")


def _rollback_entry(workspace: Path, stage_root: Path, decision: dict[str, Any]) -> dict[str, Any]:
    target = workspace / decision["target_path"]
    existed_before = bool(decision["target_digest_before"])
    backup_path = ""
    if existed_before:
        backup_root = stage_root / "_rollback"
        try:
            backup_root.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise MergeInfrastructureError(f"unable to create rollback backup directory: {backup_root}: {exc}") from exc
        backup = backup_root / f"{_safe_name(decision['target_path'])}.backup"
        try:
            shutil.copyfile(target, backup)
        except OSError as exc:
            raise MergeInfrastructureError(f"unable to create rollback backup for {decision['target_path']}: {exc}") from exc
        backup_path = backup.relative_to(stage_root).as_posix()
    return {
        "target_path": decision["target_path"],
        "action": "updated" if existed_before else "created",
        "existed_before": existed_before,
        "digest_before": decision["target_digest_before"],
        "digest_after": "",
        "backup_path": backup_path,
        "verification": {"backup_recorded": existed_before},
    }


def _write_rollback_manifest(path: Path, workspace: Path, entries: list[dict[str, Any]]) -> None:
    """Atomically retain the last complete recovery receipt on interruption."""
    from product_agent_os.control_plane_compaction import _write
    payload = {'schema_version': 1, 'workspace': str(workspace),
               'generated_at': datetime.now(UTC).replace(microsecond=0).isoformat(), 'entries': entries}
    raw = json.dumps(payload, indent=2, sort_keys=True).encode('utf-8')
    for attempt in range(3):
        try:
            _write(path, raw)
            return
        except PermissionError as exc:
            # Windows readers can briefly lock replacement. Retry the same
            # atomic write, never delete the journal or bypass a pending writer.
            if attempt == 2:
                raise MergeInfrastructureError(f'unable to write rollback manifest: {path}: {exc}') from exc
            time.sleep(0.05 * (attempt + 1))
        except OSError as exc:
            raise MergeInfrastructureError(f'unable to write rollback manifest: {path}: {exc}') from exc


def _write_plan_artifacts(stage_root: Path, plan: dict[str, Any]) -> None:
    stage_path = stage_root.resolve()
    approval_template = build_approval_template(plan)
    (stage_path / APPROVAL_TEMPLATE_NAME).write_text(
        json.dumps(approval_template, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (stage_path / MERGE_PLAN_NAME).write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")


def _with_hook_activation(plan: dict[str, Any], workspace: Path, enable_hooks: bool) -> dict[str, Any]:
    if not enable_hooks:
        return plan
    updated = json.loads(json.dumps(plan))
    for decision in updated.get("decisions", []):
        if decision.get("target_path") != HOOKS_CONFIG_TARGET:
            continue
        target = workspace / HOOKS_CONFIG_TARGET
        if target.exists():
            decision["action"] = "blocked"
            decision["approval_required"] = False
            decision["reason"] = "existing hooks.json replacement is blocked in Track 4"
            updated.setdefault("blocked", []).append(f"{HOOKS_CONFIG_TARGET}: existing hooks.json replacement is blocked")
            updated["status"] = "blocked"
        else:
            decision["action"] = "create_file"
            decision["approval_required"] = True
            decision["reason"] = "enable_hooks approval allows creating hooks.json"
            decision["rollback_entry"] = {
                "target_path": HOOKS_CONFIG_TARGET,
                "action": "created",
                "digest_before": "",
            }
            if updated.get("status") == "ready":
                updated["status"] = "needs_approval"
    return updated


def _hook_approval_errors(approval: Any) -> list[str]:
    if not isinstance(approval, dict):
        return ["approval field must be an object when enable_hooks is true"]

    errors: list[str] = []
    approved_events = approval.get("approved_hook_events")
    blocking_hooks = approval.get("blocking_hooks")
    hook_rollback = approval.get("hook_rollback")

    if not isinstance(approved_events, list) or not approved_events:
        errors.append("approved_hook_events must be non-empty when enable_hooks is true")
    elif any(not isinstance(item, str) or item not in ALLOWED_HOOK_EVENTS for item in approved_events):
        errors.append("approved_hook_events must contain only supported hook event names")

    if not isinstance(blocking_hooks, list) or not blocking_hooks:
        errors.append("blocking_hooks must describe hook blocking behavior when enable_hooks is true")
    elif any(not isinstance(item, str) or item not in ALLOWED_HOOK_EVENTS for item in blocking_hooks):
        errors.append("blocking_hooks must contain only supported hook event names")

    if not isinstance(hook_rollback, str) or not hook_rollback.strip():
        errors.append("hook_rollback is required when enable_hooks is true")
    return errors


def _reject_changed_current_plan_id(
    stage_root: Path,
    approval_payload: Any,
    current_plan: dict[str, Any],
) -> None:
    approval = approval_payload.get("approval") if isinstance(approval_payload, dict) else {}
    approved_id = approval.get("merge_plan_id") if isinstance(approval, dict) else ""
    if approved_id == current_plan["id"]:
        return
    approved_plan = _approved_plan_by_id(stage_root, approved_id)
    if approved_plan is not None:
        _reject_stale_target_digest(approved_plan, current_plan)
    errors = validate_approval_record(
        approval_payload,
        current_plan["id"],
        [item["target_path"] for item in _approval_required_decisions(current_plan)],
        sorted({item["action"] for item in _approval_required_decisions(current_plan)}),
    )
    raise MergeInfrastructureError("; ".join(errors) if errors else "approval merge_plan_id does not match current merge plan")


def _approved_plan_by_id(stage_root: Path, approved_id: str) -> dict[str, Any] | None:
    plan_path = stage_root / MERGE_PLAN_NAME
    if not approved_id or not plan_path.exists():
        return None
    payload = _load_json_file(plan_path, "merge plan")
    if isinstance(payload, dict) and payload.get("id") == approved_id:
        return payload
    return None


def _reject_stale_target_digest(approved_plan: dict[str, Any], current_plan: dict[str, Any]) -> None:
    for approved in _approval_required_decisions(approved_plan):
        current = _decision_by_target(current_plan, approved["target_path"])
        if current["target_digest_before"] != approved["target_digest_before"]:
            raise MergeInfrastructureError(f"stale target digest for {approved['target_path']}")


def _approval_required_decisions(plan: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in plan.get("decisions", [])
        if isinstance(item, dict) and item.get("approval_required") and item.get("action") in WRITABLE_ACTIONS
    ]


def _reject_stale_decisions(
    approved_plan: dict[str, Any],
    current_plan: dict[str, Any],
    required_decisions: list[dict[str, Any]],
) -> None:
    if approved_plan.get("status") == "blocked":
        raise MergeInfrastructureError("approved merge plan is blocked")
    for approved in required_decisions:
        current = _decision_by_target(current_plan, approved["target_path"])
        if current["action"] != approved["action"]:
            raise MergeInfrastructureError(f"stale decision action for {approved['target_path']}")
        if current["target_digest_before"] != approved["target_digest_before"]:
            raise MergeInfrastructureError(f"stale target digest for {approved['target_path']}")
        if current["staged_digest"] != approved["staged_digest"]:
            raise MergeInfrastructureError(f"stale staged digest for {approved['target_path']}")


def _decision_by_target(plan: dict[str, Any], target_path: str) -> dict[str, Any]:
    for decision in plan.get("decisions", []):
        if isinstance(decision, dict) and decision.get("target_path") == target_path:
            return decision
    raise MergeInfrastructureError(f"merge decision not found: {target_path}")


def _target_path(workspace: Path, relative_path: str) -> Path:
    _reject_unsafe_relative_path(relative_path, "target path")
    target = workspace / Path(relative_path)
    return target


def _staged_path(stage_root: Path, relative_path: str) -> Path:
    _reject_unsafe_relative_path(relative_path, "staged path")
    staged = stage_root / Path(relative_path)
    return staged


def _backup_path(stage_root: Path, relative_path: str) -> Path:
    if not relative_path:
        raise MergeInfrastructureError("rollback backup path is required")
    return _staged_path(stage_root, relative_path)


def _reject_unsafe_relative_path(value: str, label: str) -> None:
    path = Path(value)
    windows_path = PureWindowsPath(value)
    # Discovery aliases must not fall through to the ordinary-file approval route.
    hook_alias = "/".join(part.rstrip(" .").casefold() for part in windows_path.parts)
    if hook_alias == HOOKS_CONFIG_TARGET and value != HOOKS_CONFIG_TARGET:
        raise MergeInfrastructureError(f"{label} must use canonical hook definition path: {HOOKS_CONFIG_TARGET}")
    unsafe = (
        not value
        or path.is_absolute()
        or bool(path.drive)
        or bool(path.root)
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or bool(windows_path.root)
        or ".." in path.parts
        or ".." in windows_path.parts
    )
    if unsafe:
        raise MergeInfrastructureError(f"{label} escapes root: {value}")


def _reject_symlink_path(path: Path, root: Path, *, include_file: bool) -> None:
    parts = path.relative_to(root).parts
    cursor = root
    parents = parts if include_file else parts[:-1]
    for part in parents:
        cursor = cursor / part
        if cursor.is_symlink():
            raise MergeInfrastructureError(f"symlink path is not mergeable: {path}")


def _managed_marker_error(existing: str, section_id: str) -> str:
    start = f"<!-- {OWNER}:start {section_id} -->"
    end = f"<!-- {OWNER}:end {section_id} -->"
    start_positions = [match.start() for match in re.finditer(re.escape(start), existing)]
    end_positions = [match.start() for match in re.finditer(re.escape(end), existing)]
    if not start_positions and not end_positions:
        return ""
    if len(start_positions) > 1 or len(end_positions) > 1:
        return "duplicate managed section"
    if len(start_positions) != len(end_positions):
        return "unpaired managed section"
    if end_positions[0] < start_positions[0]:
        return "broken managed section marker order"
    return ""


def _managed_body(rendered: str, section_id: str) -> str:
    start = f"<!-- {OWNER}:start {section_id} -->"
    end = f"<!-- {OWNER}:end {section_id} -->"
    pattern = re.compile(re.escape(start) + r"\s*(.*?)\s*" + re.escape(end), re.DOTALL)
    match = pattern.search(rendered)
    return match.group(1).strip() if match else rendered


def _is_config_or_hook_path(target_path: str) -> bool:
    return target_path.endswith(".conf") or "/hooks/" in target_path.replace("\\", "/")


def _load_approval_file(path: Path) -> Any:
    if not path.exists() or not path.is_file():
        raise MergeInfrastructureError(f"approval file does not exist: {path}")
    return _load_json_file(path, "approval file")


def _load_json_file(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MergeInfrastructureError(f"invalid {label} json: {exc}") from exc
    except OSError as exc:
        raise MergeInfrastructureError(f"unable to read {label}: {path}: {exc}") from exc


def _safe_name(target_path: str) -> str:
    return target_path.replace("/", "__").replace("\\", "__").replace(":", "_")


def _unique(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return unique
