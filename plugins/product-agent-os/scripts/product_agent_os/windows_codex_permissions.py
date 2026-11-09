from __future__ import annotations

import hashlib
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

IS_WINDOWS = os.name == "nt"

_SID_RE = re.compile(r"\bS-\d(?:-\d+){2,}\b")
_ICACLS_TEXT_ENCODING = "mbcs" if os.name == "nt" else "utf-8"


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
            "Diagnostic only by default. Repair requires one existing allowlisted target, "
            "one explicit SID, a reviewed current ACL plan digest and a new backup. "
            "Other DENY entries are preserved. No recursive or onboarding repair."
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


def _checked_path(root: Path, path: Path) -> Path:
    """Reject aliases/reparse points before resolve can hide their identity."""
    if not path.is_absolute():
        path = root / path
    if not path.is_relative_to(root) or ".." in path.parts:
        raise ValueError("path outside workspace")
    for part in (path, *path.parents):
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("reparse path is not allowed")
        if part == root:
            break
    if not path.resolve().is_relative_to(root):
        raise ValueError("resolved path outside workspace")
    return path


def _repair_target(workspace: str | Path, target: str) -> tuple[Path, Path]:
    supplied = Path(workspace).absolute()
    # Inspect every existing ancestor, including ancestors above the workspace.
    for part in (supplied, *supplied.parents):
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("workspace uses a reparse path")
    root = supplied.resolve()
    if target not in PRODUCT_AGENT_OS_WRITABLE_CODEX_DIRS:
        raise ValueError("target must be one exact allowlisted directory")
    path = _checked_path(root, root / target)
    if not path.is_dir():
        raise ValueError("repair target must already exist")
    return root, path


def _acl_text(path: Path) -> str:
    completed = subprocess.run(["icacls", str(path)], check=True, capture_output=True,
                               text=True, encoding=_ICACLS_TEXT_ENCODING, errors="strict")
    return completed.stdout


def build_repair_plan(workspace: str | Path, target: str, sid: str) -> dict[str, Any]:
    """Read-only preview of one owner-selected SID removal; never select all DENYs."""
    if not IS_WINDOWS:
        raise ValueError("ACL repair is Windows-only")
    root, path = _repair_target(workspace, target)
    if not isinstance(sid, str) or not _SID_RE.fullmatch(sid):
        raise ValueError("one explicit numeric SID is required")
    plan = {"schema_version": 1, "workspace": str(root), "target": target, "sid": sid,
            "acl_sha256": hashlib.sha256(_acl_text(path).encode("utf-8")).hexdigest(),
            "commands": [["icacls", str(path), "/inheritance:d"],
                         ["icacls", str(path), "/remove:d", "*" + sid]],
            "recursive": False}
    plan["plan_digest"] = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
    return plan


def restore_permissions(workspace: str | Path, target: str, backup: str | Path,
                        backup_sha256: str) -> dict[str, Any]:
    """Restore only the snapshot bound to this exact target and workspace."""
    root, path = _repair_target(workspace, target)
    snapshot = _checked_path(root, Path(backup))
    receipt_path = _checked_path(root, Path(str(snapshot) + ".json"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (receipt != {"workspace": str(root), "target": target, "backup_sha256": backup_sha256}
            or hashlib.sha256(snapshot.read_bytes()).hexdigest() != backup_sha256):
        raise ValueError("snapshot binding or digest mismatch")
    if not IS_WINDOWS:
        raise ValueError("ACL restore is Windows-only")
    _run_icacls(path.parent, "/restore", str(snapshot))
    return {"status": "restored", "target": target}


def apply_permissions(workspace: str | Path, *, target: str | None = None,
                      sid: str | None = None, plan_digest: str | None = None,
                      backup: str | Path | None = None) -> dict[str, Any]:
    """Apply one reviewed repair, saving a restorable ACL before any ACL mutation."""
    result: dict[str, Any] = {"status": "blocked", "actions": [], "errors": []}
    try:
        if not all((target, sid, plan_digest, backup)):
            raise ValueError("exact target, SID, reviewed plan digest and backup are required")
        plan = build_repair_plan(workspace, target, sid)
        if plan["plan_digest"] != plan_digest:
            raise ValueError("permission plan digest drift")
        root, path = _repair_target(workspace, target)
        snapshot = _checked_path(root, Path(backup))
        receipt_path = _checked_path(root, Path(str(snapshot) + ".json"))
        if snapshot.exists() or receipt_path.exists() or not snapshot.parent.is_dir():
            raise ValueError("backup must be new with an existing parent")
        _run_icacls(path, "/save", str(snapshot))
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        receipt_path.write_text(json.dumps({"workspace": str(root), "target": target,
                                           "backup_sha256": digest}), encoding="utf-8")
        result.update(backup_sha256=digest, backup=str(snapshot))
        # Recheck after backup: an external ACL edit must not be silently repaired.
        if build_repair_plan(workspace, target, sid)["plan_digest"] != plan_digest:
            raise ValueError("permission plan changed during snapshot")
        try:
            _run_icacls(path, "/inheritance:d")
            _run_icacls(path, "/remove:d", "*" + sid)
        except (OSError, subprocess.CalledProcessError):
            result["rollback"] = restore_permissions(root, target, snapshot, digest)
            raise
        result.update(status="applied", actions=plan["commands"])
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        result["errors"].append(str(exc))
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
    """Read DENY SIDs from localized icacls output using the platform code page."""
    if not path.exists():
        return []
    completed = subprocess.run(
        ["icacls", str(path)],
        check=False,
        capture_output=True,
        text=True,
        encoding=_ICACLS_TEXT_ENCODING,
        errors="replace",
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
        encoding=_ICACLS_TEXT_ENCODING,
        errors="replace",
    )
