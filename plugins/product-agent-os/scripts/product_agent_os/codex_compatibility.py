from __future__ import annotations

import json
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


def validate_codex_compatibility(plugin_root: Path) -> dict[str, Any]:
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
        "context7_mcp": {"status": "ok" if components["mcp"]["status"] == "present_unverified" else "needs_review", "detail": "component schema scope: " + components["mcp"]["format"]},
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

    return {
        "status": status,
        "component_inventory": components,
        "compatibility_scope": "local_structure_only_not_host_or_distribution_readiness",
        "capability_matrix": {surface: {"standalone_skills": "documented", "local_executor": "project_specific_verification_required", "native_plugin": "requires_surface_specific_host_receipt", "host_status": "not_verified"} for surface in SUPPORTED_CODEX_SURFACES},
        "supported_surfaces": SUPPORTED_CODEX_SURFACES,
        "requires_non_codex_adapters": bool(forbidden_required_adapters),
        "forbidden_required_adapters": forbidden_required_adapters,
        "non_codex_adapter_paths_present": non_codex_adapter_paths_present,
        "checks": checks,
        "evidence": {
            "files": [item for item in evidence_files if (plugin_root / item).exists()],
            "directories": [item for item in evidence_directories if (plugin_root / item).is_dir()],
        },
    }


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
