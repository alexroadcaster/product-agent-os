from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
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
CANONICAL_SKILL_ROOT = Path("plugins/product-agent-os/skills")
STALE_AFTER = timedelta(hours=48)
WORKSPACE_ROOT_ENV = "CODEX_HOOK_WORKSPACE_ROOT"
TASK_BRIEF_REQUIRED_FIELDS = ["Request", "Goal", "Context", "Scope", "Value", "Execution", "Acceptance", "Risks / approvals", "Next step"]


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


def _skill_provenance(root: Path) -> str:
    """Return a stable repository-local skill digest without exposing host paths."""
    skill_root = root / CANONICAL_SKILL_ROOT
    skill_files = sorted(skill_root.glob("*/SKILL.md")) if skill_root.exists() else []
    if not skill_files:
        return "canonical_skill_source=" + CANONICAL_SKILL_ROOT.as_posix() + "; status=missing"
    digest = hashlib.sha256()
    for path in skill_files:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\\0")
        digest.update(path.read_bytes())
    return (
        "canonical_skill_source="
        + CANONICAL_SKILL_ROOT.as_posix()
        + "; skill_count="
        + str(len(skill_files))
        + "; sha256="
        + digest.hexdigest()
        + "; mixed_source=forbidden"
    )


def _lifecycle_state_summary(root: Path) -> str:
    path = root / LIFECYCLE_STATE
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return "lifecycle_state=missing"
    except (OSError, json.JSONDecodeError):
        return "lifecycle_state=invalid; action=repair_before_mutation"
    if not isinstance(marker, dict):
        return "lifecycle_state=invalid; action=repair_before_mutation"
    status = str(marker.get("status") or "missing")
    task_id = str(marker.get("task_id") or "missing")
    if status != "in_progress":
        return "lifecycle_state=" + status + "; task_id=" + task_id + "; action=start_new_root_run"
    try:
        updated_at = datetime.fromisoformat(str(marker.get("updated_at", "")).replace("Z", "+00:00"))
    except ValueError:
        return "lifecycle_state=invalid_timestamp; task_id=" + task_id + "; action=repair_before_mutation"
    if updated_at.tzinfo is None:
        return "lifecycle_state=invalid_timestamp; task_id=" + task_id + "; action=repair_before_mutation"
    if datetime.now(timezone.utc) - updated_at.astimezone(timezone.utc) > STALE_AFTER:
        return "lifecycle_state=stale_in_progress; task_id=" + task_id + "; action=stop_and_recover_not_resume"
    return "lifecycle_state=in_progress; task_id=" + task_id + "; action=resume_only_if_user_request_matches"


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
        + "; "
        + _lifecycle_state_summary(root)
        + ". Skill provenance: "
        + _skill_provenance(root)
        + ". Load the config-routed task-start-brief.md and completion-ledger.md templates. "
        + "Use task_start_brief_v2 with nine bold labels for large/high-risk or financially material "
        + "implementation, release/readiness or an explicit packet request: "
        + ", ".join(TASK_BRIEF_REQUIRED_FIELDS)
        + ". Ordinary fixes and read-only/partial/blocked work may use concise results, evidence and limits. "
        + "Before authorized mutations record the applicable full or concise scope marker. Complete checks and "
        + "control-plane sync before one terminal Completion Ledger (13 items) or concise result, with no later tools. "
        + "Stop is advisory and does not validate chat. Preserve already-loaded legacy session contracts."
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
