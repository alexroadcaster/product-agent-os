from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path
from typing import Any

from product_agent_os.plugin_components import resolve_plugin_components


SUPPORTED_CODEX_SURFACES = ["Codex App", "CLI", "IDE extension"]
NON_CODEX_ADAPTER_PATHS = [
    ".claude-plugin",
    ".cursor-plugin",
    ".opencode",
    ".gemini-plugin",
    "CLAUDE.md",
    "CURSOR.md",
    "GEMINI.md",
]


def validate_codex_compatibility(
    plugin_root: Path, *, observations: dict[str, Any] | None = None,
    cache_root: Path | None = None,
) -> dict[str, Any]:
    """Check local structure and separately report bounded, supplied observations.

    No host discovery, subprocess, network, trust change or model promotion.
    Optional cache comparison reads only the explicit directory, never searches
    global caches; matching bytes do not prove host selection or invocation.
    """
    plugin_root = plugin_root.resolve()
    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    skills_path = plugin_root / "skills"
    mcp_path = plugin_root / ".mcp.json"
    hooks_template_path = plugin_root / "assets" / "templates" / "hooks" / "hooks.json"
    root_hooks_config = plugin_root / "hooks" / "hooks.json"
    readme_path = plugin_root / "README.md"

    components = resolve_plugin_components(plugin_root)
    checks = {
        "codex_manifest": {"status": "ok" if components["identity"]["name"] == "product-agent-os" else "needs_review", "detail": "observed package identity; not host evidence"},
        "bundled_skills": _check_bundled_skills(skills_path),
        "context7_mcp": {"status": "ok" if components["mcp"]["status"] == "present_unverified" and "context7" in components["mcp"]["server_names"] else "needs_review", "detail": "component schema scope: " + components["mcp"]["format"]},
        "staged_hooks": _check_staged_hooks(hooks_template_path, root_hooks_config),
        "readme_codex_scope": _check_readme_scope(readme_path),
        "non_codex_adapters_absent": _check_non_codex_adapters_absent(plugin_root),
    }
    non_codex_adapter_paths_present = [
        relative
        for relative in NON_CODEX_ADAPTER_PATHS
        if (plugin_root / relative).exists()
    ]
    forbidden_required_adapters = _required_non_codex_adapters(readme_path, manifest_path)
    status = (
        "compatible"
        if components["status"] == "present_unverified" and all(check["status"] == "ok" for check in checks.values())
        and not forbidden_required_adapters
        and not non_codex_adapter_paths_present
        else "needs_review"
    )

    evidence_files = [
        ".codex-plugin/plugin.json",
        ".mcp.json",
        "README.md",
        "assets/templates/hooks/hooks.json",
    ]
    evidence_directories = [".codex-plugin", "skills", "assets/templates/hooks"]

    diagnostics = _host_diagnostics(plugin_root, observations, cache_root)
    return {
        "status": status,
        "component_inventory": components,
        "compatibility_scope": "local_structure_only_not_host_or_distribution_readiness",
        "capability_matrix": _capability_matrix(diagnostics),
        "host_diagnostics": diagnostics,
        "distribution": {"status": "gated", "publisher": "not_verified", "listing_urls": "not_verified",
                         "required": ["verified_publisher", "verified_listing_urls", "distribution_icons", "owner_release_review"],
                         "scope": "local_structure_check_is_not_full_submission_validation"},
        "supported_surfaces": SUPPORTED_CODEX_SURFACES,
        "supported_surfaces_scope": "standalone_skills_and_workflows_not_native_plugin_support",
        "requires_non_codex_adapters": bool(forbidden_required_adapters),
        "forbidden_required_adapters": forbidden_required_adapters,
        "non_codex_adapter_paths_present": non_codex_adapter_paths_present,
        "checks": checks,
        "evidence": {
            "files": [item for item in evidence_files if (plugin_root / item).exists()],
            "directories": [item for item in evidence_directories if (plugin_root / item).is_dir()],
        },
    }


def _capability_matrix(diagnostics: dict[str, Any]) -> dict[str, Any]:
    """Support is immutable under observations; checked 2026-11-09.

    Sources: https://learn.chatgpt.com/docs/plugins and /docs/build-skills.
    """
    matrix = {}
    for surface in SUPPORTED_CODEX_SURFACES:
        row = {"local_executor": "project_specific_verification_required", "host_status": "not_verified"}
        for component in ("standalone_skills", "native_plugin"):
            support = "unsupported" if surface == "IDE extension" and component == "native_plugin" else "documented"
            observed = diagnostics["surface"] == surface and diagnostics["observations"].get(component + "_observed") is True
            observation = "not_verified"
            if observed:
                observation = "conflicts_with_documented_support" if support == "unsupported" else "observed"
            row[component] = {"support": support, "observation": observation}
        matrix[surface] = row
    return matrix


_MODEL_IDS = {"gpt-6-astra", "gpt-6.1-sol", "gpt-6.1-terra", "gpt-6-luna"}
_OBSERVATION_KEYS = {"surface", "client_version", "configured_model", "observed_model", "trust",
                     "native_plugin_observed", "standalone_skills_observed"}
_VERSION = re.compile(r"[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}")


def _host_diagnostics(root: Path, supplied: dict[str, Any] | None, cache_root: Path | None) -> dict[str, Any]:
    """Project only allowlisted non-secret fields; inputs are not authenticated receipts."""
    issues = []
    data = supplied if isinstance(supplied, dict) else {}
    if supplied is not None and not isinstance(supplied, dict):
        issues.append("observations_object_required")
    if set(data) - _OBSERVATION_KEYS:
        issues.append("unrecognized_observation_fields")
    surface = data.get("surface") if data.get("surface") in SUPPORTED_CODEX_SURFACES else "unknown"
    version = data.get("client_version")
    version = version if isinstance(version, str) and _VERSION.fullmatch(version) else None
    models = {}
    for key in ("configured_model", "observed_model"):
        value = data.get(key)
        models[key] = value if isinstance(value, str) and value in _MODEL_IDS else None
    minimum = "0.159.0" if surface == "CLI" and models["configured_model"] == "gpt-6.1-terra" else None
    if data.get("client_version") is None:
        client_status = "missing"
    elif version is None:
        client_status = "unknown"
    elif surface == "unknown":
        client_status = "unknown_surface"
    else:
        client_status = "minimum_not_documented"
    if version and minimum:
        client_status = "meets_documented_minimum" if tuple(map(int, version.split("."))) >= (0, 159, 0) else "below_documented_minimum"
    trust = data.get("trust")
    trust = trust if isinstance(trust, str) and trust in {"trusted", "untrusted"} else None
    model_status = "not_verified"
    if models["observed_model"]:
        model_status = "observed"
        if models["configured_model"]:
            model_status = "match" if models["configured_model"] == models["observed_model"] else "mismatch"
    for key in ("configured_model", "observed_model"):
        if data.get(key) is not None and models[key] is None:
            issues.append("unrecognized_" + key)
    return {
        "surface": surface, "input_scope": "caller_supplied_observations_not_authenticated_host_receipts",
        "client": {"version": version, "status": client_status, "documented_minimum": minimum,
                   "minimum_source": "https://learn.chatgpt.com/docs/models" if minimum else None},
        "model": {**models, "status": model_status, "promotion": "not_assessed"},
        "trust": {"value": trust, "status": "observed" if trust else "unknown"},
        "account_access": "not_verified", "issues": issues,
        "observations": {key: data[key] for key in ("native_plugin_observed", "standalone_skills_observed") if type(data.get(key)) is bool},
        "provenance": _provenance(root, cache_root),
    }


def _fingerprint(root: Path) -> dict[str, Any]:
    """Bounded component-byte comparison; omit contents and absolute paths.

    Only manifests and skill source files belong to this evidence scope. Runtime
    scripts/templates and host selection need separate evidence. Refuse links,
    unreadable files and excess size instead of reporting a partial match.
    """
    digest = hashlib.sha256()
    count = size = entries = 0
    try:
        if _linked(root) or not root.is_dir():
            raise ValueError("invalid_root")
        files = []
        for name in ("plugin.json", ".codex-plugin/plugin.json", "mcp.json", ".mcp.json"):
            path = root / name
            if _linked(path.parent) or _linked(path):
                raise ValueError("linked_component")
            if path.exists():
                files.append(path)
        skills = root / "skills"
        if _linked(skills):
            raise ValueError("linked_component")
        if skills.exists():
            for directory, dirs, names in os.walk(skills, followlinks=False, onerror=_raise_walk_error):
                entries += len(dirs) + len(names)
                if entries > 10000:
                    raise ValueError("too_many_entries")
                if any(_linked(Path(directory) / name) for name in dirs + names):
                    raise ValueError("linked_component")
                files.extend(Path(directory) / name for name in names if name == "SKILL.md")
                if len(files) > 2048:
                    raise ValueError("too_many_components")
        for path in sorted(files):
            if path.stat().st_size > 1024 * 1024:
                raise ValueError("component_too_large")
            with path.open("rb") as stream:
                content = stream.read(1024 * 1024 + 1)
            if len(content) > 1024 * 1024:
                raise ValueError("component_grew_beyond_limit")
            size += len(content)
            if size > 16 * 1024 * 1024:
                raise ValueError("components_too_large")
            name = path.relative_to(root).as_posix().encode("utf-8")
            digest.update(len(name).to_bytes(4, "big") + name + len(content).to_bytes(8, "big") + content)
            count += 1
        return {"status": "observed" if count else "missing", "sha256": digest.hexdigest() if count else None, "file_count": count}
    except (OSError, ValueError):
        return {"status": "needs_review", "sha256": None, "file_count": None}


def _raise_walk_error(error: OSError) -> None:
    raise error


def _linked(path: Path) -> bool:
    """Windows junctions are traversal links too, not ordinary directories."""
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def _provenance(root: Path, cache_root: Path | None) -> dict[str, Any]:
    canonical = _fingerprint(root)
    cache = _fingerprint(Path(cache_root)) if cache_root is not None else None
    status = "cache_not_provided"
    if canonical["status"] != "observed" or cache is not None and cache["status"] != "observed":
        status = "needs_review"
    elif cache is not None:
        status = "match" if canonical["sha256"] == cache["sha256"] else "drift"
    return {"status": status, "canonical": canonical, "cache": cache,
            "scope": "manifests_mcp_and_SKILL.md_only_not_full_package_or_host_selection"}


def _check_bundled_skills(path: Path) -> dict[str, str]:
    if not path.is_dir():
        return {"status": "missing", "detail": "skills directory is missing"}
    skill_files = sorted(path.glob("*/SKILL.md"))
    if not skill_files:
        return {"status": "needs_review", "detail": "no bundled SKILL.md files found"}
    return {"status": "ok", "detail": f"{len(skill_files)} bundled skills found"}


def _check_staged_hooks(template_path: Path, root_hooks_config: Path) -> dict[str, str]:
    if not template_path.exists():
        return {"status": "missing", "detail": "hook template config is missing"}
    if root_hooks_config.exists():
        return {"status": "needs_review", "detail": "root hook config would activate hooks"}
    return {"status": "ok", "detail": "hooks are templates only"}


def _check_readme_scope(path: Path) -> dict[str, str]:
    if not path.exists():
        return {"status": "missing", "detail": "README.md is missing"}
    text = path.read_text(encoding="utf-8")
    required_terms = ["Codex App", "CLI", "IDE extension"]
    if not all(term in text for term in required_terms):
        return {"status": "needs_review", "detail": "README does not state supported Codex surfaces"}
    return {"status": "ok", "detail": "README states Codex-only surfaces"}


def _check_non_codex_adapters_absent(plugin_root: Path) -> dict[str, str]:
    present = [
        relative
        for relative in NON_CODEX_ADAPTER_PATHS
        if (plugin_root / relative).exists()
    ]
    if present:
        return {"status": "needs_review", "detail": "non-Codex adapter paths present: " + ", ".join(present)}
    return {"status": "ok", "detail": "no non-Codex adapter paths are packaged"}


def _required_non_codex_adapters(readme_path: Path, manifest_path: Path) -> list[str]:
    texts = []
    for path in [readme_path, manifest_path]:
        if path.exists():
            texts.append(path.read_text(encoding="utf-8").lower())
    combined = "\n".join(texts)
    required: list[str] = []
    for name in ["claude", "cursor", "opencode", "gemini"]:
        if f"requires {name}" in combined or f"required {name}" in combined:
            required.append(name)
    return required
