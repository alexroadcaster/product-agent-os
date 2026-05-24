from __future__ import annotations

from pathlib import Path
from typing import Any


CONTROL_PLANE_FILES = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]


def load_control_plane_context(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace)
    files: dict[str, dict[str, Any]] = {}
    for name in CONTROL_PLANE_FILES:
        files[name] = _read_file(root / name)
    return {
        "workspace": str(root),
        "exists": root.exists(),
        "is_dir": root.is_dir(),
        "files": files,
        "missing": [name for name, item in files.items() if not item["exists"]],
        "unreadable": [name for name, item in files.items() if item["exists"] and item["error"]],
    }


def _read_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "text": "", "error": ""}
    if not path.is_file():
        return {"exists": True, "text": "", "error": "not a file"}
    try:
        return {"exists": True, "text": path.read_text(encoding="utf-8"), "error": ""}
    except (OSError, UnicodeDecodeError):
        return {"exists": True, "text": "", "error": "unable to read file as utf-8 text"}
