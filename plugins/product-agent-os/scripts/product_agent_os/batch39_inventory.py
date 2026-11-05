from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from product_agent_os.plugin_components import resolve_plugin_components
from product_agent_os.stage_manifest import canonical_json, content_digest, file_digest


REQUIRED_INVENTORY_CATEGORIES = ("source", "cache", "package", "session")
SOURCE_STATUSES = {"present", "missing", "not_directory", "unreadable"}
CACHE_STATUSES = {"present", "missing", "not_configured"}
SESSION_STATUSES = {"present", "missing"}


def build_batch39_inventory(
    *,
    workspace: Path,
    plugin_root: Path | None = None,
    cache_roots: list[Path] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build a redacted local inventory for Batch 39 M01."""

    workspace = workspace.resolve()
    plugin_root = (plugin_root or workspace / "plugins" / "product-agent-os").resolve()
    cache_roots = [root.resolve() for root in (cache_roots or [])]
    timestamp = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()

    inventory = {
        "source": _source_inventory(workspace, plugin_root),
        "cache": _cache_inventory(workspace, cache_roots),
        "package": _package_inventory(workspace, plugin_root),
        "session": _session_inventory(workspace),
    }
    packet = {
        "schema_version": "batch39_inventory_v1",
        "batch": "B39",
        "test_id": "B39-TEST-M01",
        "generated_at": timestamp,
        "generated_view_policy": "orientation_only_not_proof",
        "approval_boundary": {
            "pilot_target_workspace_mutation": "not_performed",
            "local_evidence_artifact_write": "allowed_workspace_output_only",
            "cache_mutation": "not_performed",
            "provider_or_api_calls": "not_performed",
            "browser_automation": "not_performed",
            "external_actions": "not_performed",
            "git_actions": "not_performed",
        },
        "inventory": inventory,
        "status": _packet_status(inventory),
    }
    packet["packet_digest"] = content_digest(canonical_json(packet))
    return packet


def validate_batch39_inventory(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("schema_version") != "batch39_inventory_v1":
        errors.append("schema_version must be batch39_inventory_v1")
    inventory = packet.get("inventory")
    if not isinstance(inventory, dict):
        errors.append("inventory must be an object")
        inventory = {}
    for category in REQUIRED_INVENTORY_CATEGORIES:
        if category not in inventory:
            errors.append(f"missing inventory category: {category}")
    errors.extend(_validate_source_inventory(inventory.get("source")))
    errors.extend(_validate_cache_inventory(inventory.get("cache")))
    errors.extend(_validate_package_inventory(inventory.get("package")))
    errors.extend(_validate_session_inventory(inventory.get("session")))
    if packet.get("generated_view_policy") not in {None, "orientation_only_not_proof"}:
        errors.append("generated_view_policy must be orientation_only_not_proof")
    if _contains_local_absolute_path(packet):
        errors.append("local absolute path leaked")
    return errors


def _source_inventory(workspace: Path, plugin_root: Path) -> dict[str, Any]:
    summary = _tree_summary(workspace, plugin_root)
    return {
        "path_ref": _path_ref(workspace, plugin_root),
        "status": summary["status"],
        "file_count": summary["file_count"],
        "skill_count": _count_named_files(plugin_root / "skills", "SKILL.md"),
        "workflow_template_count": _count_files(plugin_root / "assets" / "templates" / "workflows", "*.md"),
        "agent_template_count": _count_files(plugin_root / "assets" / "templates" / "agents", "*.toml"),
        "inventory_digest": summary["inventory_digest"],
        "read_errors": summary["read_errors"],
    }


def _cache_inventory(workspace: Path, cache_roots: list[Path]) -> dict[str, Any]:
    if not cache_roots:
        return {
            "status": "not_configured",
            "roots": [],
            "note": "No cache root was supplied; no cache mutation or install/update check was attempted.",
        }
    roots = [_cache_root_inventory(workspace, root, index) for index, root in enumerate(cache_roots, start=1)]
    return {
        "status": "present" if any(root["status"] == "present" for root in roots) else "missing",
        "roots": roots,
    }


def _cache_root_inventory(workspace: Path, root: Path, index: int) -> dict[str, Any]:
    summary = _tree_summary(workspace, root)
    return {
        "label": _path_ref(workspace, root, external_label=f"cache_root_{index}"),
        "status": summary["status"],
        "file_count": summary["file_count"],
        "skill_count": _count_named_files(root / "skills", "SKILL.md"),
        "plugin_json_present": (root / ".codex-plugin" / "plugin.json").is_file() or (root / "plugin.json").is_file(),
        "mcp_present": (root / ".mcp.json").is_file() or (root / "mcp.json").is_file(),
        "inventory_digest": summary["inventory_digest"],
        "read_errors": summary["read_errors"],
    }


def _package_inventory(workspace: Path, plugin_root: Path) -> dict[str, Any]:
    components = resolve_plugin_components(plugin_root)
    manifest_path = plugin_root / (components["manifest_path"] or ".codex-plugin/plugin.json")
    mcp_path = plugin_root / (components["mcp"]["path"] or ".mcp.json")
    manifest = _read_json_object(manifest_path)
    mcp = _read_json_object(mcp_path)
    return {
        "manifest_path_ref": _path_ref(workspace, manifest_path),
        "mcp_path_ref": _path_ref(workspace, mcp_path),
        "manifest_present": manifest_path.is_file(),
        "mcp_present": mcp_path.is_file(),
        "manifest": {
            "name": _string_value(manifest.get("name")),
            "version": _string_value(manifest.get("version")),
            "skills": _string_value(manifest.get("skills")),
            "mcpServers": _string_value(manifest.get("mcpServers")),
        },
        "mcp_server_keys": components["mcp"]["server_names"],
        "component_inventory": components,
        "package_digest": content_digest(canonical_json({"manifest": manifest, "mcp_keys": sorted(mcp.keys())})),
    }


def _session_inventory(workspace: Path) -> dict[str, Any]:
    codex_root = workspace / ".codex"
    agents_root = codex_root / "agents"
    workflows_root = codex_root / "workflows"
    return {
        "codex_root_ref": _path_ref(workspace, codex_root),
        "status": "present" if codex_root.exists() else "missing",
        "config_present": (codex_root / "config.toml").is_file(),
        "rules_present": (workspace / ".rules").is_file(),
        "agent_count": _count_files(agents_root, "*.toml"),
        "workflow_count": _count_files(workflows_root, "*.md"),
        "runlogs_present": (codex_root / "runlogs").exists(),
        "session_digest": content_digest(
            canonical_json(
                {
                    "agents": _relative_file_list(workspace, agents_root, "*.toml"),
                    "workflows": _relative_file_list(workspace, workflows_root, "*.md"),
                    "config_present": (codex_root / "config.toml").is_file(),
                    "rules_present": (workspace / ".rules").is_file(),
                }
            )
        ),
    }


def _tree_summary(workspace: Path, root: Path) -> dict[str, Any]:
    if not root.exists():
        return {"status": "missing", "file_count": 0, "inventory_digest": "sha256:missing", "read_errors": []}
    if not root.is_dir():
        return {"status": "not_directory", "file_count": 0, "inventory_digest": "sha256:not_directory", "read_errors": []}
    try:
        files = sorted(path for path in root.rglob("*") if path.is_file())
    except OSError as exc:
        return {
            "status": "unreadable",
            "file_count": 0,
            "inventory_digest": content_digest(exc.__class__.__name__),
            "read_errors": [exc.__class__.__name__],
        }
    entries = [_tree_file_entry(root, path, index) for index, path in enumerate(files, start=1)]
    read_errors = [entry["path_ref"] for entry in entries if entry.get("digest") == "sha256:unreadable"]
    return {
        "status": "present",
        "file_count": len(files),
        "inventory_digest": content_digest(canonical_json(entries)),
        "read_errors": read_errors,
    }


def _count_named_files(root: Path, filename: str) -> int:
    if not root.is_dir():
        return 0
    try:
        return sum(1 for path in root.rglob(filename) if path.is_file())
    except OSError:
        return 0


def _count_files(root: Path, pattern: str) -> int:
    if not root.is_dir():
        return 0
    try:
        return sum(1 for path in root.glob(pattern) if path.is_file())
    except OSError:
        return 0


def _relative_file_list(workspace: Path, root: Path, pattern: str) -> list[str]:
    if not root.is_dir():
        return []
    try:
        return sorted(_path_ref(workspace, path) for path in root.glob(pattern) if path.is_file())
    except OSError:
        return []


def _read_json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _tree_file_entry(root: Path, path: Path, index: int) -> dict[str, str]:
    try:
        path_ref = path.relative_to(root).as_posix()
    except ValueError:
        path_ref = f"external_file_{index}"
    try:
        digest = file_digest(path)
    except OSError:
        digest = "sha256:unreadable"
    return {"path_ref": path_ref, "digest": digest}


def _path_ref(workspace: Path, path: Path, *, external_label: str = "external") -> str:
    try:
        return path.resolve().relative_to(workspace.resolve()).as_posix()
    except ValueError:
        return external_label


def _packet_status(inventory: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if inventory["source"]["status"] != "present":
        blockers.append("source_inventory_missing")
    if not inventory["package"]["manifest_present"]:
        blockers.append("package_manifest_missing")
    if inventory["cache"]["status"] == "not_configured":
        blockers.append("cache_root_not_supplied")
    return {
        "overall": "ready" if not blockers else "needs_attention",
        "open_blockers": blockers,
    }


def _string_value(value: Any) -> str:
    return value if isinstance(value, str) else ""


def _contains_local_absolute_path(payload: Any) -> bool:
    if isinstance(payload, str):
        return _looks_like_absolute_path(payload)
    if isinstance(payload, dict):
        return any(_contains_local_absolute_path(key) or _contains_local_absolute_path(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(_contains_local_absolute_path(item) for item in payload)
    return False


def _looks_like_absolute_path(value: str) -> bool:
    normalized = value.strip()
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] in {"\\", "/"} and normalized[0].isalpha():
        return True
    if normalized.startswith("\\\\") or normalized.startswith("//"):
        return True
    if normalized.startswith("/"):
        return True
    return False


def _validate_source_inventory(source: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(source, dict):
        return ["source must be an object"]
    if source.get("status") not in SOURCE_STATUSES:
        errors.append("source.status missing or invalid")
    for field in ("file_count", "skill_count", "workflow_template_count", "agent_template_count"):
        if not isinstance(source.get(field), int):
            errors.append(f"source.{field} must be integer")
    if not isinstance(source.get("inventory_digest"), str):
        errors.append("source.inventory_digest must be string")
    return errors


def _validate_cache_inventory(cache: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(cache, dict):
        return ["cache must be an object"]
    if cache.get("status") not in CACHE_STATUSES:
        errors.append("cache.status missing or invalid")
    roots = cache.get("roots")
    if not isinstance(roots, list):
        errors.append("cache.roots must be list")
        return errors
    for index, root in enumerate(roots, start=1):
        if not isinstance(root, dict):
            errors.append(f"cache.roots[{index}] must be object")
            continue
        if root.get("status") not in SOURCE_STATUSES:
            errors.append(f"cache.roots[{index}].status missing or invalid")
        for field in ("file_count", "skill_count"):
            if not isinstance(root.get(field), int):
                errors.append(f"cache.roots[{index}].{field} must be integer")
        for field in ("plugin_json_present", "mcp_present"):
            if not isinstance(root.get(field), bool):
                errors.append(f"cache.roots[{index}].{field} must be boolean")
    return errors


def _validate_package_inventory(package: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(package, dict):
        return ["package must be an object"]
    for field in ("manifest_present", "mcp_present"):
        if not isinstance(package.get(field), bool):
            errors.append(f"package.{field} must be boolean")
    manifest = package.get("manifest")
    if not isinstance(manifest, dict):
        errors.append("package.manifest must be object")
        manifest = {}
    for field in ("name", "version", "skills", "mcpServers"):
        if not isinstance(manifest.get(field), str):
            errors.append(f"package.manifest.{field} must be string")
    if not isinstance(package.get("mcp_server_keys"), list):
        errors.append("package.mcp_server_keys must be list")
    return errors


def _validate_session_inventory(session: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(session, dict):
        return ["session must be an object"]
    if session.get("status") not in SESSION_STATUSES:
        errors.append("session.status missing or invalid")
    for field in ("config_present", "rules_present", "runlogs_present"):
        if not isinstance(session.get(field), bool):
            errors.append(f"session.{field} must be boolean")
    for field in ("agent_count", "workflow_count"):
        if not isinstance(session.get(field), int):
            errors.append(f"session.{field} must be integer")
    return errors


__all__ = ["build_batch39_inventory", "validate_batch39_inventory"]
