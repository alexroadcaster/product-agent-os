from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES


STACK_MARKERS = {
    "package.json": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "mkdocs.yml": "docs",
    "Cargo.toml": "rust",
    "go.mod": "go",
}

IGNORED_DIR_NAMES = {
    ".git",
    ".angular",
    ".cache",
    ".codex-cache",
    ".docusaurus",
    ".eggs",
    ".gradle",
    ".hypothesis",
    ".mypy_cache",
    ".next",
    ".nox",
    ".nuxt",
    ".parcel-cache",
    ".pytest_cache",
    ".ruff_cache",
    ".svelte-kit",
    ".tox",
    ".turbo",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "node_modules",
    "site",
    "target",
    "vendor",
    "venv",
}


def _relative_files(root: Path) -> set[str]:
    files: set[str] = set()
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIR_NAMES]
        current_path = Path(current_root)
        for filename in filenames:
            try:
                files.add((current_path / filename).relative_to(root).as_posix())
            except ValueError:
                continue
    return files


def _detect_stack(files: set[str]) -> list[str]:
    stack: list[str] = []
    for marker, name in STACK_MARKERS.items():
        if marker in files and name not in stack:
            stack.append(name)
    if any(path.startswith("packages/") for path in files):
        stack.append("monorepo")
    return stack


def _profile_for(files: set[str], stack: list[str]) -> dict[str, Any]:
    service_count = len({path.split("/")[1] for path in files if path.startswith("packages/") and "/" in path})
    ci_present = any(path.startswith(".github/workflows/") for path in files)
    test_maturity = "partial" if any("test" in path.lower() for path in files) else "none"
    if "monorepo" in stack or service_count > 1:
        name = "production-team"
    elif "docs" in stack and len(stack) == 1:
        name = "guided-small"
    elif ci_present:
        name = "standard-product"
    else:
        name = "guided-small"
    return {
        "name": name,
        "confidence": "medium",
        "drivers": {
            "repo_size": "small" if len(files) < 200 else "medium",
            "stack_count": len([item for item in stack if item != "monorepo"]),
            "service_count": max(service_count, 1),
            "test_maturity": test_maturity,
            "ci_present": ci_present,
        },
    }


def analyze_workspace(root: str | Path) -> dict[str, Any]:
    workspace = Path(root).resolve()
    if not workspace.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not workspace.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace}")
    files = _relative_files(workspace)
    stack = _detect_stack(files)
    existing_control_plane = [name for name in CONTROL_PLANE_FILES if name in files]
    missing_control_plane = [name for name in CONTROL_PLANE_FILES if name not in files]
    existing_codex_assets = sorted(path for path in files if path.startswith(".codex/"))
    risks: list[str] = []
    if "AGENTS.md" not in files:
        risks.append("missing durable project instructions")
    if not any("test" in path.lower() for path in files):
        risks.append("no detected test files or test configuration")
    return {
        "workspace": str(workspace),
        "detected_files": sorted(files),
        "detected_stack": stack,
        "existing_control_plane": existing_control_plane,
        "missing_control_plane": missing_control_plane,
        "existing_codex_assets": existing_codex_assets,
        "git": {
            "present": (workspace / ".git").exists(),
        },
        "risks": risks,
        "complexity_profile": _profile_for(files, stack),
    }


def main(argv: list[str]) -> int:
    root = Path(argv[0]) if argv else Path.cwd()
    try:
        audit = analyze_workspace(root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0
