from __future__ import annotations

import json
import subprocess
from pathlib import Path


CONTROL_PLANE_FILES = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
LIFECYCLE_FILES = [
    ".codex/config.toml",
    ".codex/workflows/task-plan-lifecycle.md",
    ".codex/workflows/control-plane-sync.md",
    ".codex/evals/agent-context-contract.json",
    ".codex/hooks.json",
    ".codex/hooks/hooks.json",
]
LIFECYCLE_STATE = ".codex/product-agent-os/lifecycle-state.json"


def _workspace_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        result = ""
    if result and result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip())
    current = Path.cwd()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex").exists():
            return candidate
    return current


def _present(root: Path, files: list[str]) -> list[str]:
    return [name for name in files if (root / name).exists()]


def _missing(root: Path, files: list[str]) -> list[str]:
    return [name for name in files if not (root / name).exists()]


def main() -> int:
    root = _workspace_root()
    payload = {
        "hook": "session_start_context",
        "workspace": str(root),
        "control_plane": {
            "present": _present(root, CONTROL_PLANE_FILES),
            "missing": _missing(root, CONTROL_PLANE_FILES),
        },
        "lifecycle": {
            "present": _present(root, LIFECYCLE_FILES),
            "missing": _missing(root, LIFECYCLE_FILES),
            "state_marker": LIFECYCLE_STATE,
            "task_start_brief_required_for": "non_mechanical_tasks",
            "completion_brief_required": True,
        },
        "reminders": [
            "Show a user-visible Task Brief before non-mechanical execution.",
            "Record the lightweight lifecycle marker after the Task Brief and before mutating commands.",
            "Run control-plane sync before the Completion Brief when scope, plan, tests, evals, runlog, or evidence state changes.",
        ],
    }
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
