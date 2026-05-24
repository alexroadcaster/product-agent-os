from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any


MANIFEST_NAME = "product-agent-os-stage-manifest.json"
APPROVAL_TEMPLATE_NAME = "product-agent-os-approval-template.json"
APPROVAL_RECORD_NAME = "product-agent-os-approval.json"
ALLOWED_FILE_ACTIONS = {"create", "update", "leave_unchanged", "blocked"}
ALLOWED_WRITE_POLICIES = {"staged_only", "approved_write_required", "blocked"}
REQUIRED_FILE_ENTRY_FIELDS = {
    "target_path",
    "staged_path",
    "action",
    "write_policy",
    "digest",
    "managed_section",
}
REQUIRED_TOP_LEVEL_FIELDS = {
    "generated_at",
    "workspace_audit_digest",
    "infrastructure_plan_digest",
}


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_digest(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return "sha256:" + hashlib.sha256(content).hexdigest()


def file_digest(path: Path) -> str:
    return content_digest(path.read_bytes())


def plan_digest(plan: dict[str, Any]) -> str:
    return content_digest(canonical_json(plan))


def build_stage_manifest(
    *,
    workspace: Path,
    stage_root: Path,
    renderer_result: dict[str, Any],
    renderer_version: str,
) -> dict[str, Any]:
    stage_root = stage_root.resolve()
    managed_sections = {
        item["target_path"]: item.get("section_id", "")
        for item in renderer_result["rendered_artifacts"].get("managed_sections", [])
        if isinstance(item, dict) and "target_path" in item
    }
    files = [
        _manifest_file_entry(item, stage_root, managed_sections)
        for item in renderer_result["rendered_artifacts"].get("files", [])
        if item.get("staged_path")
    ]
    target_paths = [
        item["target_path"]
        for item in renderer_result["rendered_artifacts"].get("files", [])
        if isinstance(item, dict) and isinstance(item.get("target_path"), str)
    ]
    return {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": renderer_version,
        "workspace": str(workspace.resolve()),
        "workspace_audit_digest": workspace_audit_digest(workspace, target_paths),
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "validation": renderer_result["rendered_artifacts"]["validation"],
        "files": files,
        "infrastructure_plan_digest": plan_digest(renderer_result["infrastructure_plan"]),
    }


def write_stage_manifest(stage_root: Path, manifest: dict[str, Any]) -> Path:
    errors = validate_stage_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    path = stage_root / MANIFEST_NAME
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_stage_manifest(stage_root: str | Path) -> dict[str, Any]:
    stage_root = Path(stage_root)
    manifest_path = stage_root / MANIFEST_NAME
    if not manifest_path.exists():
        raise ValueError(f"stage manifest does not exist: {manifest_path}")
    if not manifest_path.is_file():
        raise ValueError(f"stage manifest is not a file: {manifest_path}")
    try:
        text = manifest_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError(f"unable to read stage manifest: {manifest_path}: {exc}") from exc
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid stage manifest json: {exc}") from exc
    errors = validate_stage_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def validate_stage_manifest(manifest: Any) -> list[str]:
    if not isinstance(manifest, dict):
        return ["stage manifest must be an object"]

    errors: list[str] = []
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if manifest.get("renderer") != "product-agent-os":
        errors.append("renderer must be product-agent-os")
    if not str(manifest.get("renderer_version", "")).strip():
        errors.append("renderer_version is required")
    if _unsafe_absolute_path(str(manifest.get("workspace", ""))):
        errors.append("workspace must be an absolute path")
    for field in sorted(REQUIRED_TOP_LEVEL_FIELDS):
        if field not in manifest:
            errors.append(f"{field} is required")
    if "generated_at" in manifest and not _valid_iso_datetime(str(manifest.get("generated_at", ""))):
        errors.append("generated_at must be a valid ISO datetime")
    for field in ["workspace_audit_digest", "infrastructure_plan_digest"]:
        if field in manifest and not _valid_sha256_digest(str(manifest.get(field, ""))):
            errors.append(f"{field} must be a sha256 digest")
    validation = manifest.get("validation")
    if not isinstance(validation, dict):
        errors.append("validation must be an object")

    files = manifest.get("files")
    if not isinstance(files, list):
        errors.append("files must be a list")
        return errors

    for item in files:
        if not isinstance(item, dict):
            errors.append("file entry must be an object")
            continue
        raw_target_path = item.get("target_path", "")
        raw_staged_path = item.get("staged_path", "")
        raw_managed_section = item.get("managed_section", "")
        target_path = raw_target_path if isinstance(raw_target_path, str) else ""
        staged_path = raw_staged_path if isinstance(raw_staged_path, str) else ""
        target_label = target_path or "<invalid>"
        missing_fields = sorted(REQUIRED_FILE_ENTRY_FIELDS - set(item))
        for field in missing_fields:
            errors.append(f"missing file entry field for {target_label}: {field}")
        action = item.get("action")
        write_policy = item.get("write_policy")
        if "target_path" in item and not isinstance(raw_target_path, str):
            errors.append("target_path must be a string")
        if "staged_path" in item and not isinstance(raw_staged_path, str):
            errors.append("staged_path must be a string")
        if "managed_section" in item and not isinstance(raw_managed_section, str):
            errors.append(f"managed_section must be a string for {target_label}")
        if "action" in item and not isinstance(action, str):
            errors.append(f"action must be a string for staged file {target_label}")
        elif "action" in item and action not in ALLOWED_FILE_ACTIONS:
            errors.append(f"invalid action for staged file {target_label}: {action}")
        if "write_policy" in item and not isinstance(write_policy, str):
            errors.append(f"write_policy must be a string for staged file {target_label}")
        elif "write_policy" in item and write_policy not in ALLOWED_WRITE_POLICIES:
            errors.append(f"invalid write_policy for staged file {target_label}: {write_policy}")
        if isinstance(raw_target_path, str) and _unsafe_relative_path(target_path):
            errors.append(f"target path escapes workspace: {target_path}")
        if isinstance(raw_staged_path, str) and _unsafe_relative_path(staged_path):
            errors.append(f"staged path escapes stage root: {staged_path}")
        digest = str(item.get("digest", ""))
        if action != "blocked" and not _valid_sha256_digest(digest):
            errors.append(f"missing digest for staged file: {target_label}")
    return errors


def build_approval_template(merge_plan: dict[str, Any]) -> dict[str, Any]:
    decisions = [
        item
        for item in merge_plan.get("decisions", [])
        if isinstance(item, dict) and item.get("approval_required")
    ]
    return {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": merge_plan["id"],
            "approved_by": "",
            "approved_at": "",
            "approved_targets": [item["target_path"] for item in decisions],
            "approved_actions": sorted({item["action"] for item in decisions}),
            "accepted_risks": [],
            "denied_targets": [],
            "notes": "",
            "enable_hooks": False,
            "approved_hook_events": [],
            "blocking_hooks": [],
            "hook_rollback": "",
        }
    }


def validate_approval_record(
    approval_payload: Any,
    merge_plan_id: str,
    required_targets: list[str],
    required_actions: list[str],
) -> list[str]:
    if not isinstance(approval_payload, dict):
        return ["approval record must be an object"]
    approval = approval_payload.get("approval")
    if not isinstance(approval, dict):
        return ["approval field must be an object"]

    errors: list[str] = []
    if approval.get("schema_version") != 1:
        errors.append("approval schema_version must be 1")
    if approval.get("merge_plan_id") != merge_plan_id:
        errors.append("approval merge_plan_id does not match current merge plan")
    if not str(approval.get("approved_by", "")).strip():
        errors.append("approved_by is required")
    if not str(approval.get("approved_at", "")).strip():
        errors.append("approved_at is required")
    elif not _valid_iso_datetime(str(approval.get("approved_at", ""))):
        errors.append("approved_at must be a valid ISO datetime with timezone")

    approved_targets = approval.get("approved_targets")
    approved_actions = approval.get("approved_actions")
    if not isinstance(approved_targets, list):
        errors.append("approved_targets must be a list")
    elif not _is_string_list(approved_targets):
        errors.append("approved_targets must contain only strings")
    elif sorted(approved_targets) != sorted(required_targets):
        errors.append("approved_targets do not match merge plan write targets")
    if not isinstance(approved_actions, list):
        errors.append("approved_actions must be a list")
    elif not _is_string_list(approved_actions):
        errors.append("approved_actions must contain only strings")
    elif sorted(approved_actions) != sorted(required_actions):
        errors.append("approved_actions do not match merge plan write actions")
    if not isinstance(approval.get("accepted_risks"), list):
        errors.append("accepted_risks must be a list")
    _validate_required_approval_field(approval, errors, "denied_targets", list)
    _validate_required_approval_field(approval, errors, "notes", str)
    _validate_required_approval_field(approval, errors, "enable_hooks", bool)
    _validate_required_approval_field(approval, errors, "approved_hook_events", list)
    _validate_required_approval_field(approval, errors, "blocking_hooks", list)
    _validate_required_approval_field(approval, errors, "hook_rollback", str)
    _validate_string_list(approval, errors, "accepted_risks")
    _validate_string_list(approval, errors, "denied_targets")
    _validate_string_list(approval, errors, "approved_hook_events")
    _validate_string_list(approval, errors, "blocking_hooks")
    return errors


def _manifest_file_entry(
    item: dict[str, Any],
    stage_root: Path,
    managed_sections: dict[str, str],
) -> dict[str, Any]:
    staged_path_value = str(item.get("staged_path", ""))
    staged_path = Path(staged_path_value) if staged_path_value else None
    relative_staged_path = _relative_staged_path(stage_root, staged_path) if staged_path is not None else ""
    digest = "" if item.get("action") == "blocked" or staged_path is None else file_digest(staged_path)
    return {
        "target_path": item["target_path"],
        "staged_path": relative_staged_path,
        "action": item["action"],
        "write_policy": item["write_policy"],
        "digest": digest,
        "managed_section": managed_sections.get(item["target_path"], ""),
    }


def workspace_audit_digest(workspace: Path, target_paths: list[str]) -> str:
    """Build a digest for the target-file snapshot captured by a staged manifest."""
    snapshot = [_workspace_snapshot_entry(workspace, target_path) for target_path in sorted(set(target_paths))]
    return content_digest(canonical_json(snapshot))


def _workspace_snapshot_entry(workspace: Path, target_path: str) -> dict[str, Any]:
    path = workspace / target_path
    entry: dict[str, Any] = {
        "target_path": target_path,
        "exists": path.exists(),
        "is_file": path.is_file(),
        "is_symlink": path.is_symlink(),
    }
    if path.is_symlink():
        entry["kind"] = "symlink"
        return entry
    if path.is_file():
        try:
            entry["digest"] = file_digest(path)
            entry["kind"] = "file"
        except OSError as exc:
            entry["kind"] = "error"
            entry["error"] = exc.__class__.__name__
    elif path.exists():
        entry["kind"] = "other"
    else:
        entry["kind"] = "missing"
    return entry


def _relative_staged_path(stage_root: Path, staged_path: Path) -> str:
    try:
        return staged_path.resolve().relative_to(stage_root).as_posix()
    except ValueError as exc:
        raise ValueError(f"staged path escapes stage root: {staged_path}") from exc


def _unsafe_relative_path(value: str) -> bool:
    if not value:
        return True
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return (
        path.is_absolute()
        or bool(path.drive)
        or bool(path.root)
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or bool(windows_path.root)
        or ".." in path.parts
        or ".." in windows_path.parts
    )


def _unsafe_absolute_path(value: str) -> bool:
    if not value:
        return True
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return not (path.is_absolute() or windows_path.is_absolute())


def _valid_sha256_digest(value: str) -> bool:
    if not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(char in "0123456789abcdef" for char in digest)


def _valid_iso_datetime(value: str) -> bool:
    if not value or "T" not in value:
        return False
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _validate_required_approval_field(
    approval: dict[str, Any],
    errors: list[str],
    field: str,
    expected_type: type,
) -> None:
    if field not in approval:
        errors.append(f"{field} is required")
    elif not isinstance(approval[field], expected_type):
        errors.append(f"{field} has invalid type")


def _validate_string_list(approval: dict[str, Any], errors: list[str], field: str) -> None:
    value = approval.get(field)
    if isinstance(value, list) and not _is_string_list(value):
        errors.append(f"{field} must contain only strings")


def _is_string_list(value: list[Any]) -> bool:
    return all(isinstance(item, str) for item in value)
