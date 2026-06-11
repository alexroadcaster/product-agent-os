from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS: tuple[str, ...] = (
    ".codex/agents",
    ".codex/skills",
    ".codex/workflows",
    ".codex/artifact-templates",
    ".codex/evals",
    ".codex/runlogs",
    ".codex/automation-candidates",
    ".codex/pr",
    ".codex/product-agent-os",
    ".codex/eval-reports",
)

SENSITIVE_CODEX_PATHS: tuple[str, ...] = (
    ".codex/config.toml",
    ".codex/hooks",
    ".codex/automations",
    ".codex/plugins",
    ".codex/settings.json",
    ".codex/harness",
)

_SID_RE = re.compile(r"\bS-\d(?:-\d+){2,}\b")


def suggested_config_entries() -> dict[str, str]:
    entries = {".": "write", ".codex": "read"}
    entries.update({path: "write" for path in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS})
    return entries


def build_permission_plan(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace).resolve()
    return {
        "status": "plan",
        "workspace": str(root),
        "windows_only": True,
        "config_profile": "product-agent-os-project",
        "config_entries": suggested_config_entries(),
        "managed_write_dirs": list(PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS),
        "not_opened_by_default": list(SENSITIVE_CODEX_PATHS),
        "approval_boundary": (
            "Apply only after owner approval. The script creates project-scoped "
            ".codex subdirectories, disables inherited ACLs on those subdirectories "
            "and removes inherited deny ACEs from the same subdirectories."
        ),
    }


def check_permissions(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace).resolve()
    result = build_permission_plan(root)
    result["status"] = "checked"
    result["platform"] = os.name
    result["dirs"] = [_dir_state(root, path) for path in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS]
    result["warnings"] = []
    if os.name != "nt":
        result["warnings"].append("Windows ACL inspection skipped on non-Windows platform.")
    else:
        result["codex_root_deny_sids"] = _deny_sids(root / ".codex")
    return result


def apply_permissions(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace).resolve()
    result = check_permissions(root)
    result["status"] = "unsupported" if os.name != "nt" else "applied"
    result["actions"] = []
    result["errors"] = []

    if os.name != "nt":
        result["errors"].append("--apply is supported only on Windows.")
        return result

    deny_sids = set(result.get("codex_root_deny_sids", []))
    for rel in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS:
        path = root / rel
        action: dict[str, Any] = {"path": rel, "commands": []}
        try:
            path.mkdir(parents=True, exist_ok=True)
            _run_icacls(path, "/inheritance:d")
            action["commands"].append("icacls <path> /inheritance:d")
            for sid in sorted(deny_sids | set(_deny_sids(path))):
                _run_icacls(path, "/remove:d", sid)
                action["commands"].append(f"icacls <path> /remove:d {sid}")
            action["status"] = "ok"
        except (OSError, subprocess.CalledProcessError) as exc:
            action["status"] = "failed"
            action["error"] = str(exc)
            result["errors"].append(f"{rel}: {exc}")
        result["actions"].append(action)

    result["dirs"] = [_dir_state(root, path) for path in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS]
    if result["errors"]:
        result["status"] = "failed"
    return result


def dumps_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def _dir_state(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    state: dict[str, Any] = {
        "path": rel,
        "exists": path.exists(),
        "sensitive_default_open": rel in SENSITIVE_CODEX_PATHS,
    }
    if os.name == "nt" and path.exists():
        state["deny_sids"] = _deny_sids(path)
    return state


def _deny_sids(path: Path) -> list[str]:
    if not path.exists():
        return []
    completed = subprocess.run(
        ["icacls", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return []
    sids: set[str] = set()
    for line in completed.stdout.splitlines():
        if "(DENY)" not in line.upper():
            continue
        sids.update(_SID_RE.findall(line))
    return sorted(sids)


def _run_icacls(path: Path, *args: str) -> None:
    subprocess.run(
        ["icacls", str(path), *args],
        check=True,
        capture_output=True,
        text=True,
    )
