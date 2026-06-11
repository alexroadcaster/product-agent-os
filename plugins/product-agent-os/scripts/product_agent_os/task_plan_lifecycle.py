from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import argparse
import json
import re
from zoneinfo import ZoneInfo

from product_agent_os.validators import validate_task_matrix_text


TASK_TIMESTAMP_PATTERN = re.compile(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$")
TASK_HEADING_TEMPLATE = "### Task `{task_id}`"


@dataclass(frozen=True)
class TaskPlanRequest:
    task_id: str
    task: str
    plan_trigger: str
    source: str
    short_description: str
    technical_value: str
    product_value: str
    scope: str
    non_goals: str
    expected_result: str
    acceptance_criteria: str
    verification_gates: str
    risks_approval_gates: str
    complexity: str
    estimated_execution_time: str
    agents: str
    skills: str
    output_artifacts: str
    next_step: str
    depends_on: str = "none"
    blocks: str = "none"
    title: str = "Task Matrix Plan"
    source_status: str = "project-local task plan"


@dataclass(frozen=True)
class TaskCompletion:
    timestamp: str
    what_was_done: str
    files_touched: str
    technical_value_delivered: str
    product_value_delivered: str
    verification_evidence: str
    residual_risks: str
    follow_up: str


def build_planned_task_matrix(request: TaskPlanRequest) -> str:
    """Create a validator-compatible pre-execution task matrix."""
    _require_values(request.__dict__, "task plan request")
    lines = [
        f"# {request.title}",
        "",
        f"Source status: {request.source_status}",
        "",
        "## Task Brief",
        "",
        "- User-visible moment: before execution",
        f"- Task ID: {request.task_id}",
        f"- Product value: {request.product_value}",
        f"- Technical value: {request.technical_value}",
        f"- Source: {request.source}",
        f"- Scope: {request.scope}",
        f"- Non-goals: {request.non_goals}",
        f"- Agents and skills: {request.agents}; {request.skills}",
        f"- Files / artifacts: {request.output_artifacts}",
        f"- Verification: {request.verification_gates}",
        f"- Approval boundary: {request.risks_approval_gates}",
        f"- Complexity: {request.complexity}",
        f"- Estimated execution time: {request.estimated_execution_time}",
        f"- Next action: {request.next_step}",
        "",
        TASK_HEADING_TEMPLATE.format(task_id=request.task_id),
        "",
        f"- Task: {request.task}",
        "- Status: planned",
        "- Schema version: task_matrix_plan_v1",
        "- Timezone: Europe/Moscow",
        f"- Plan trigger: {request.plan_trigger}",
        "- Validator target: detailed task blocks",
        "- Date and time of task implementation: pending_execution_timestamp",
        f"- Depends on: {request.depends_on}",
        f"- Blocks: {request.blocks}",
        f"- Source: {request.source}",
        f"- Short description: {request.short_description}",
        f"- Technical value: {request.technical_value}",
        f"- Product value: {request.product_value}",
        f"- Scope: {request.scope}",
        f"- Non-goals: {request.non_goals}",
        f"- Expected result: {request.expected_result}",
        f"- Acceptance criteria: {request.acceptance_criteria}",
        f"- Verification gates: {request.verification_gates}",
        f"- Risks / approval gates: {request.risks_approval_gates}",
        f"- Complexity: {request.complexity}",
        f"- Estimated execution time: {request.estimated_execution_time}",
        f"- Agents: {request.agents}",
        f"- Skills: {request.skills}",
        f"- Output artifacts: {request.output_artifacts}",
        f"- Next step: {request.next_step}",
        "",
        "#### Completion Report",
        "",
        "- status: planned",
        "- what was done: pending",
        "- files touched / work locations: pending",
        "- technical value delivered: pending",
        "- product value delivered: pending",
        "- actual implementation date and time: pending_execution_timestamp",
        "- verification evidence: pending",
        "- residual risks: pending",
        "- follow-up: pending",
        "",
    ]
    return "\n".join(lines)


def mark_task_implemented(text: str, task_id: str, completion: TaskCompletion) -> str:
    """Update one task block with post-execution evidence."""
    _require_values(completion.__dict__, "task completion")
    if not TASK_TIMESTAMP_PATTERN.match(completion.timestamp):
        raise ValueError("timestamp must use DD-MM-YYYY HH:mm")

    lines = text.splitlines()
    start, end = _find_task_block(lines, task_id)
    block = lines[start:end]
    replacements = {
        "Status": "implemented",
        "Date and time of task implementation": completion.timestamp,
        "status": "implemented",
        "what was done": completion.what_was_done,
        "files touched / work locations": completion.files_touched,
        "technical value delivered": completion.technical_value_delivered,
        "product value delivered": completion.product_value_delivered,
        "actual implementation date and time": completion.timestamp,
        "verification evidence": completion.verification_evidence,
        "residual risks": completion.residual_risks,
        "follow-up": completion.follow_up,
    }

    for field, value in replacements.items():
        block = _replace_field(block, field, value)

    updated = lines[:start] + block + lines[end:]
    updated = _replace_or_append_completion_brief(updated, completion)
    return "\n".join(updated) + ("\n" if text.endswith("\n") else "")


def current_moscow_timestamp() -> str:
    """Return the current Europe/Moscow timestamp in task-matrix format."""
    return datetime.now(ZoneInfo("Europe/Moscow")).strftime("%d-%m-%Y %H:%M")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create and close Product-Agent OS task-matrix plan files.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    new_parser = subparsers.add_parser("new", help="Create a pre-execution task plan file.")
    new_parser.add_argument("--output", required=True)
    new_parser.add_argument("--force", action="store_true")
    for field in [
        "task-id",
        "task",
        "plan-trigger",
        "source",
        "short-description",
        "technical-value",
        "product-value",
        "scope",
        "non-goals",
        "expected-result",
        "acceptance-criteria",
        "verification-gates",
        "risks-approval-gates",
        "complexity",
        "estimated-execution-time",
        "agents",
        "skills",
        "output-artifacts",
        "next-step",
    ]:
        new_parser.add_argument(f"--{field}", required=True)
    new_parser.add_argument("--depends-on", default="none")
    new_parser.add_argument("--blocks", default="none")
    new_parser.add_argument("--title", default="Task Matrix Plan")
    new_parser.add_argument("--source-status", default="project-local task plan")

    complete_parser = subparsers.add_parser("complete", help="Mark one task as implemented with evidence.")
    complete_parser.add_argument("--path", required=True)
    complete_parser.add_argument("--task-id", required=True)
    complete_parser.add_argument("--timestamp", default="")
    for field in [
        "what-was-done",
        "files-touched",
        "technical-value-delivered",
        "product-value-delivered",
        "verification-evidence",
        "residual-risks",
        "follow-up",
    ]:
        complete_parser.add_argument(f"--{field}", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "new":
            return _main_new(args)
        if args.command == "complete":
            return _main_complete(args)
    except Exception as exc:  # pragma: no cover - exercised through CLI behavior.
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 1
    raise AssertionError(args.command)


def _main_new(args: argparse.Namespace) -> int:
    path = Path(args.output)
    if path.exists() and not args.force:
        raise ValueError(f"output file already exists: {path}")
    text = build_planned_task_matrix(
        TaskPlanRequest(
            task_id=args.task_id,
            task=args.task,
            plan_trigger=args.plan_trigger,
            source=args.source,
            short_description=args.short_description,
            technical_value=args.technical_value,
            product_value=args.product_value,
            scope=args.scope,
            non_goals=args.non_goals,
            expected_result=args.expected_result,
            acceptance_criteria=args.acceptance_criteria,
            verification_gates=args.verification_gates,
            risks_approval_gates=args.risks_approval_gates,
            complexity=args.complexity,
            estimated_execution_time=args.estimated_execution_time,
            agents=args.agents,
            skills=args.skills,
            output_artifacts=args.output_artifacts,
            next_step=args.next_step,
            depends_on=args.depends_on,
            blocks=args.blocks,
            title=args.title,
            source_status=args.source_status,
        )
    )
    return _write_validated(path, text, "created")


def _main_complete(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if not path.exists():
        raise ValueError(f"plan file does not exist: {path}")
    text = path.read_text(encoding="utf-8")
    updated = mark_task_implemented(
        text,
        args.task_id,
        TaskCompletion(
            timestamp=args.timestamp or current_moscow_timestamp(),
            what_was_done=args.what_was_done,
            files_touched=args.files_touched,
            technical_value_delivered=args.technical_value_delivered,
            product_value_delivered=args.product_value_delivered,
            verification_evidence=args.verification_evidence,
            residual_risks=args.residual_risks,
            follow_up=args.follow_up,
        ),
    )
    return _write_validated(path, updated, "updated")


def _write_validated(path: Path, text: str, action: str) -> int:
    errors = validate_task_matrix_text(text)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2, sort_keys=True))
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(json.dumps({"ok": True, "action": action, "path": str(path)}, indent=2, sort_keys=True))
    return 0


def _find_task_block(lines: list[str], task_id: str) -> tuple[int, int]:
    heading = TASK_HEADING_TEMPLATE.format(task_id=task_id)
    start = next((index for index, line in enumerate(lines) if line.strip() == heading), None)
    if start is None:
        raise ValueError(f"task not found: {task_id}")
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("### Task `"):
            end = index
            break
    return start, end


def _replace_field(lines: list[str], field: str, value: str) -> list[str]:
    prefix = f"- {field}:"
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            updated = list(lines)
            updated[index] = f"{prefix} {value}"
            return updated
    raise ValueError(f"task block missing field: {field}")


def _replace_or_append_completion_brief(lines: list[str], completion: TaskCompletion) -> list[str]:
    brief = [
        "## Completion Brief",
        "",
        "- User-visible moment: after execution",
        "- Result status: implemented",
        f"- Done: {completion.what_was_done}",
        f"- Files / artifacts: {completion.files_touched}",
        f"- Technical value delivered: {completion.technical_value_delivered}",
        f"- Product value delivered: {completion.product_value_delivered}",
        f"- Evidence: {completion.verification_evidence}",
        f"- Residual risk: {completion.residual_risks}",
        f"- Next action: {completion.follow_up}",
    ]
    start = next((index for index, line in enumerate(lines) if line.strip() == "## Completion Brief"), None)
    if start is None:
        return lines + [""] + brief
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## ") or lines[index].startswith("### Task `"):
            end = index
            break
    return lines[:start] + brief + lines[end:]


def _require_values(values: dict[str, str], label: str) -> None:
    for name, value in values.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{label} missing required value: {name}")
