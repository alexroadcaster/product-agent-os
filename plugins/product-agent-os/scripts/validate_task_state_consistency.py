from __future__ import annotations

import json
import sys
from pathlib import Path


TERMINAL_LOCAL_STATUSES = {"locally_implemented_focused_verified", "approval_required_not_started"}


def validate_workspace(root: Path) -> list[str]:
    errors: list[str] = []
    group_path = root / "docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json"
    lifecycle_path = root / ".codex/product-agent-os/lifecycle-state.json"
    try:
        group = json.loads(group_path.read_text(encoding="utf-8"))
        lifecycle = json.loads(lifecycle_path.read_text(encoding="utf-8"))
        # Legacy receipts omit plan_path; new runs must not be forced into an old plan.
        plan_ref = lifecycle.get("plan_path", "docs/superpowers/plans/2026-08-17-product-agent-os-loop-remediation.md") if isinstance(lifecycle, dict) else None
        if not isinstance(plan_ref, str) or not plan_ref.strip() or Path(plan_ref).is_absolute():
            return ["lifecycle_plan_path_invalid"]
        plan_path = (root / plan_ref).resolve()
        if not plan_path.is_relative_to(root.resolve()):
            return ["lifecycle_plan_path_invalid"]
        plan = plan_path.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"state_input_invalid:{exc.__class__.__name__}"]

    tasks = {str(item.get("task_id")): item for item in group.get("tasks", []) if isinstance(item, dict)}
    for task_id, task in tasks.items():
        if task.get("status") != "locally_implemented_focused_verified":
            continue
        for dependency in task.get("depends_on", []):
            dependency_task = tasks.get(str(dependency))
            if dependency_task and dependency_task.get("status") not in TERMINAL_LOCAL_STATUSES:
                errors.append(f"{task_id}:dependency_not_ready:{dependency}")

    task_id = lifecycle.get("task_id") if isinstance(lifecycle, dict) else None
    if not isinstance(task_id, str) or task_id not in plan:
        errors.append("lifecycle_task_missing_from_active_plan")
    if group.get("latest_execution_evidence_id") not in {"B45-CQRR-A04", "B45-CQRR-A05", "B45-CQRR-A06", "B45-CQRR-A07"}:
        errors.append("task_group_latest_evidence_unknown")

    projections = {
        "PLAN.md": "A04-A06 locally implement/focused-verify T23-T29",
        "RUNLOG.md": "A04-A06 locally implement/focused-verify T23-T29",
        "TEST.md": "A04-A06 locally implement/focused-verify T23-T29",
    }
    for filename, needle in projections.items():
        try:
            text = (root / filename).read_text(encoding="utf-8")
        except OSError:
            errors.append(f"projection_missing:{filename}")
            continue
        if needle not in text:
            errors.append(f"projection_stale:{filename}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    errors = validate_workspace(root)
    print(json.dumps({"ok": not errors, "errors": errors}, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
