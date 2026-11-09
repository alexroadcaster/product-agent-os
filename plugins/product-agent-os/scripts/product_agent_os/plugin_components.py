"""Read-only package component resolution; presence never proves host activation.

Portable identity/components win over compatibility overlays. Inline OpenAI
settings replace the overlay rather than merging it. No commands, endpoints,
environment values or credentials are returned or executed by this inventory.
"""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject ambiguous JSON without exposing keys or values in diagnostics."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_json_key")
        result[key] = value
    return result


def _path(root: Path, value: Any) -> tuple[Path, str]:
    if not isinstance(value, str) or not value.startswith("./"):
        raise ValueError("component_path_requires_dot_prefix")
    name = value[2:].replace("\\", "/")
    if not name or ":" in name or ".." in PurePosixPath(name).parts or name.startswith("/") or any(ord(c) < 32 for c in name):
        raise ValueError("component_path_outside_package")
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError("component_path_outside_package")
    return path, PurePosixPath(name).as_posix()


def _read(root: Path, relative: str, issues: list[str]) -> dict[str, Any] | None:
    try:
        path, _ = _path(root, "./" + relative)
        if not path.exists():
            return None
        if path.stat().st_size > 1024 * 1024:
            raise ValueError("component_file_too_large")
        value = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_json_object)
        if not isinstance(value, dict):
            raise ValueError("component_object_required")
        return value
    except (OSError, ValueError) as exc:
        issues.append(relative + ":" + (str(exc) if type(exc) is ValueError else "unreadable_or_invalid_json"))
        return None


def _string_map(value: Any) -> bool:
    return isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in value.items())


def _mcp(root: Path, relative: str | None, portable: bool, issues: list[str]) -> dict[str, Any]:
    result = {"path": relative, "format": "absent", "status": "absent", "server_names": [], "transports": {}}
    if relative is None:
        return result
    before = len(issues)
    data = _read(root, relative, issues)
    if data is None:
        if len(issues) != before:
            result.update(format="malformed", status="needs_review")
        return result
    wrapped = "mcpServers" in data
    result["format"] = "agent_plugins_1.0.0" if portable else "codex_wrapped" if wrapped else "legacy_flat_observed"
    if portable and (data.get("$schema") != MCP_SCHEMA or set(data) - {"$schema", "mcpServers"}):
        issues.append("unsupported_portable_mcp_schema_or_fields")
    if not portable and not wrapped:
        issues.append("legacy_flat_mcp_requires_schema_review")
    if not portable and wrapped and set(data) - {"mcpServers"}:
        issues.append("unsupported_codex_mcp_root_fields")
    servers = data.get("mcpServers") if wrapped else data if not portable else None
    if not isinstance(servers, dict):
        issues.append("mcp_servers_object_required")
        servers = {}
    for name, server in sorted(servers.items()):
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", name) or not isinstance(server, dict):
            issues.append("invalid_mcp_server_entry")
            continue
        result["server_names"].append(name)
        kind = server.get("type") or ("stdio" if "command" in server else "streamable-http" if "url" in server else "unknown")
        result["transports"][name] = kind if isinstance(kind, str) else "invalid"
        invalid = portable and server.get("type") not in ("stdio", "streamable-http", "sse")
        # The compatibility subset is intentionally narrow. Do not silently
        # accept transport mixtures or config.toml-only options in plugin JSON.
        if not portable:
            allowed = {"type", "command", "args", "env"} if kind == "stdio" else {"type", "url", "headers"}
            invalid |= bool(set(server) - allowed)
        if kind == "stdio":
            invalid |= not isinstance(server.get("command"), str) or not server.get("command", "").strip()
            args = server.get("args", [])
            invalid |= not isinstance(args, list) or any(not isinstance(x, str) for x in args)
            invalid |= not _string_map(server.get("env", {}))
            if portable:
                invalid |= bool(set(server) - {"type", "command", "args", "env", "cwd"})
                invalid |= bool(set(server.get("env", {})) & {"PLUGIN_ROOT", "PLUGIN_DATA"}) if isinstance(server.get("env", {}), dict) else True
                if "cwd" in server:
                    cwd = server["cwd"]
                    if isinstance(cwd, str) and cwd.startswith("${PLUGIN_ROOT}/"):
                        cwd = "./" + cwd[len("${PLUGIN_ROOT}/"):]
                    try:
                        _path(root, cwd)
                    except ValueError:
                        invalid = True
        elif kind in ("streamable-http", "sse"):
            try:
                url = urlsplit(server.get("url", ""))
                invalid |= url.scheme not in {"https", "http"} or not url.hostname or bool(url.username or url.password or url.fragment)
                _ = url.port  # Access validates malformed/out-of-range port syntax.
                invalid |= not _string_map(server.get("headers", {}))
            except (TypeError, ValueError, AttributeError):
                invalid = True
            if portable:
                invalid |= bool(set(server) - {"type", "url", "headers", "extensions"})
                # OpenAI documents auth extensions beyond the portable schema.
                # Keep them discoverable but require separate schema/host review.
                if "extensions" in server:
                    issues.append("mcp_auth_extension_requires_separate_review")
        else:
            invalid = True
        if invalid:
            issues.append("invalid_or_unsupported_mcp_server:" + name)
    result["status"] = "needs_review" if len(issues) != before else "present_unverified"
    return result


def resolve_plugin_components(plugin_root: str | Path) -> dict[str, Any]:
    """Normalize observed components with explicit format, precedence and gaps.

    This bounded supported-subset check is not a complete schema validator or
    a host receipt. Unknown fields/transports stay reviewable, never verified.
    """
    root = Path(plugin_root).resolve()
    issues: list[str] = []
    root_present = (root / "plugin.json").exists()
    legacy_present = (root / ".codex-plugin/plugin.json").exists()
    manifest_ref = "plugin.json" if root_present else ".codex-plugin/plugin.json"
    manifest = _read(root, manifest_ref, issues) if root_present or legacy_present else None
    portable = root_present and isinstance(manifest, dict) and manifest.get("$schema") == PLUGIN_SCHEMA
    fmt = "agent_plugins_1.0.0" if portable else "unsupported_root_manifest" if root_present else "codex_compatibility" if legacy_present else "absent"
    data = manifest or {}
    if root_present and not portable:
        issues.append("unrecognized_root_manifest_no_silent_fallback")
    if manifest is not None and (not isinstance(data.get("name"), str) or not re.fullmatch(r"(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", data.get("name", "")) or len(data.get("name", "")) > 64):
        issues.append("invalid_plugin_identity")
    settings, settings_source = data, manifest_ref if manifest else None
    if portable:
        allowed = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
        if set(data) - allowed:
            issues.append("unsupported_portable_manifest_fields")
        if any(not isinstance(data[key], str) for key in ("version", "description", "homepage", "repository", "license") if key in data):
            issues.append("invalid_manifest_string_field")
        if "author" in data and (not _string_map(data["author"]) or set(data["author"]) - {"name", "email", "url"}):
            issues.append("invalid_manifest_author")
        if "keywords" in data and (not isinstance(data["keywords"], list) or any(not isinstance(value, str) for value in data["keywords"])):
            issues.append("invalid_manifest_keywords")
        extensions = data.get("extensions", {})
        if not isinstance(extensions, dict) or any(not isinstance(v, dict) for v in extensions.values()):
            issues.append("invalid_manifest_extensions")
            extensions = {}
        if "com.openai" in extensions:
            settings, settings_source = extensions["com.openai"], "plugin.json:extensions.com.openai"
        else:
            settings = _read(root, ".codex-plugin/plugin.json", issues) or {}
            settings_source = ".codex-plugin/plugin.json" if legacy_present else None
    skill_values = ["./skills/"] if portable else settings.get("skills", "./skills/")
    skill_values = [skill_values] if isinstance(skill_values, str) else skill_values
    paths, skill_names = [], []
    if not isinstance(skill_values, list):
        issues.append("invalid_skills_paths")
        skill_values = []
    for value in skill_values:
        try:
            path, name = _path(root, value)
            paths.append(name)
            skill_names.extend(p.parent.name for p in sorted(path.glob("*/SKILL.md")) if p.resolve().is_relative_to(root))
        except (OSError, ValueError):
            issues.append("invalid_skills_path")
    mcp_ref = "mcp.json" if portable else settings.get("mcpServers", "./.mcp.json")
    if not portable:
        try:
            _, mcp_ref = _path(root, mcp_ref)
        except ValueError:
            mcp_ref = None
            issues.append("invalid_mcp_component_path")
    mcp = _mcp(root, mcp_ref, portable, issues)
    hooks_ref = settings.get("hooks", "./hooks/hooks.json")
    try:
        hook_path, hooks_ref = _path(root, hooks_ref)
        hooks_present = hook_path.is_file()
    except (OSError, ValueError):
        hooks_ref, hooks_present = None, False
        issues.append("unsupported_hooks_component_path")
    return {
        "schema_version": 1, "format": fmt, "format_version": "1.0.0" if portable else "legacy" if legacy_present else None,
        "status": "needs_review" if issues else "present_unverified" if manifest is not None else "absent",
        "manifest_path": manifest_ref if root_present or legacy_present else None,
        "identity": {k: data.get(k) if isinstance(data.get(k), str) else None for k in ("name", "version")},
        "settings_source": settings_source, "portable_components_override_overlay": portable,
        "skills": {"paths": sorted(set(paths)), "names": sorted(set(skill_names)), "status": "present_unverified" if skill_names else "absent"},
        "mcp": mcp, "hooks": {"path": hooks_ref, "status": "present_unverified" if hooks_present else "absent"},
        "issues": sorted(set(issues)), "host_status": "not_verified",
        "validation_scope": "bounded_supported_subset_not_full_schema_or_host_validation",
    }


def discover_plugin_components(workspace: Path, files: list[str]) -> list[dict[str, Any]]:
    """Resolve only discovered package roots; never scan installed/global caches."""
    roots = set()
    for name in files:
        path = PurePosixPath(name)
        if name.endswith("/.codex-plugin/plugin.json") or name == ".codex-plugin/plugin.json":
            roots.add(path.parent.parent.as_posix())
        elif path.name == "plugin.json":
            roots.add(path.parent.as_posix())
    return [{"package_path": name, "inventory": resolve_plugin_components(workspace / name)} for name in sorted(roots)[:100]]
