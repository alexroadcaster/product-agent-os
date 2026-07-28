from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


CONTROL_PLANE_FILES = ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]
LIFECYCLE_FILES = [
    ".codex/config.toml",
    ".codex/workflows/task-plan-lifecycle.md",
    ".codex/workflows/control-plane-sync.md",
    ".codex/evals/agent-context-contract.json",
    ".codex/hooks.json",
]
LIFECYCLE_STATE = ".codex/product-agent-os/lifecycle-state.json"
WORKSPACE_ROOT_ENV = "CODEX_HOOK_WORKSPACE_ROOT"
TASK_BRIEF_REQUIRED_FIELDS = [
    "Task ID",
    "Product value",
    "Technical value",
    "Source / trigger",
    "Scope",
    "Non-goals",
    "Agents and skills",
    "Files / artifacts expected",
    "Verification gate",
    "Approval boundary / risks",
    "Complexity",
    "Estimated execution time",
    "Next action",
]


def _workspace_root() -> Path:
    """Resolve the project root for relative presence checks only."""
    override = os.environ.get(WORKSPACE_ROOT_ENV)
    if override:
        return Path(override).resolve()
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        result = None
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
    present_control = _present(root, CONTROL_PLANE_FILES)
    missing_control = _missing(root, CONTROL_PLANE_FILES)
    present_lifecycle = _present(root, LIFECYCLE_FILES)
    missing_lifecycle = _missing(root, LIFECYCLE_FILES)
    context = (
        "Product-Agent OS startup context: control-plane present="
        + ", ".join(present_control)
        + ("; missing=" + ", ".join(missing_control) if missing_control else "; missing=none")
        + ". Lifecycle contracts present="
        + ", ".join(present_lifecycle)
        + ("; missing=" + ", ".join(missing_lifecycle) if missing_lifecycle else "; missing=none")
        + ". State marker="
        + LIFECYCLE_STATE
        + ". For non-mechanical work, show a user-visible task_start_brief_v1 "
        + "Task Brief with fields: "
        + ", ".join(TASK_BRIEF_REQUIRED_FIELDS)
        + ". Record the marker before mutations, run control-plane sync when owned state changes, and show a "
        + "Completion Brief before closure."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context,
                }
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())