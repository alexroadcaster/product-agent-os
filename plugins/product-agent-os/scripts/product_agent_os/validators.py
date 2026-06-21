from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import tomllib

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.doubt_verification import (
    DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
    main_doubt_verification,
    validate_doubt_verification_packet,
    validate_doubt_verification_packet_file,
)


AGENT_REQUIRED_FIELDS = [
    "name",
    "description",
    "developer_instructions",
]
AGENT_FORBIDDEN_TOP_LEVEL_FIELDS = {
    "ownership",
    "inputs",
    "outputs",
    "stop_conditions",
    "model_policy",
    "handoff_requirements",
}
TASK_MATRIX_SCHEMA_VERSION = "task_matrix_plan_v1"
TASK_MATRIX_ALLOWED_STATUSES = {"planned", "in_progress", "implemented", "blocked", "accepted_gap"}
TASK_MATRIX_REQUIRED_FIELDS = [
    "Task",
    "Status",
    "Schema version",
    "Timezone",
    "Plan trigger",
    "Validator target",
    "Date and time of task implementation",
    "Depends on",
    "Blocks",
    "Source",
    "Short description",
    "Technical value",
    "Product value",
    "Scope",
    "Non-goals",
    "Expected result",
    "Acceptance criteria",
    "Verification gates",
    "Risks / approval gates",
    "Complexity",
    "Estimated execution time",
    "Agents",
    "Skills",
    "Output artifacts",
    "Next step",
]
TASK_MATRIX_COMPLETION_FIELDS = [
    "status",
    "what was done",
    "files touched / work locations",
    "technical value delivered",
    "product value delivered",
    "actual implementation date and time",
    "verification evidence",
    "residual risks",
    "follow-up",
]
READ_TEXT_ERROR = "unable to read file as utf-8 text"
SECRET_NAME_PATTERN = re.compile(r"(?i)(SECRET|TOKEN|PASSWORD|PRIVATE[_-]?KEY|API[_-]?KEY)")
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    (?:export\s+)?
    ["']?
    (?P<name>[A-Z_][A-Z0-9_.-]*)
    ["']?
    \s*(?:=|:)\s*
    (?P<value>[^#\r\n]+?)
    \s*$
    """
)
SECRET_ENVIRON_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    os\.environ\[
    (?P<quote>["'])
    (?P<name>[A-Z_][A-Z0-9_.-]*)
    (?P=quote)
    \]
    \s*=\s*
    (?P<value>[^#\r\n]+?)
    \s*$
    """
)
SAFE_ENV_LOOKUP_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    os\.
    (?:
        getenv
        |
        environ\.get
    )
    \(
    \s*
    (?P<quote>["'])
    [A-Z_][A-Z0-9_.-]*
    (?P=quote)
    \s*
    \)
    \s*$
    """
)
TASK_HEADING_PATTERN = re.compile(r"^###\s+Task\s+`?(?P<id>[^`\r\n]+?)`?\s*$")
TASK_FIELD_PATTERN = re.compile(r"^\s*-\s+(?P<name>[^:]+):\s*(?P<value>.*)$")
TASK_TIMESTAMP_PATTERN = re.compile(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$")
TASK_PLACEHOLDER_PATTERN = re.compile(r"(<[^>]+>|\{\{[^}]+\}\}|\{generated_at\}|\bTODO\b|\bTBD\b|\?\?\?|\.\.\.)")
HOOK_JSON_REQUIRED_EVENTS = [
    "SessionStart",
    "PreToolUse",
    "PermissionRequest",
    "PostToolUse",
    "Stop",
]


def validate_control_plane(root: Path) -> dict[str, Any]:
    missing = [name for name in CONTROL_PLANE_FILES if not (root / name).exists()]
    return {
        "ok": not missing,
        "missing": missing,
    }


def validate_agent_file(path: Path) -> list[str]:
    text, error = read_utf8_text(path)
    if error:
        return [error]
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid toml: {exc}"]
    errors: list[str] = []
    for field in AGENT_REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing required field: {field}")
    for field in sorted(AGENT_FORBIDDEN_TOP_LEVEL_FIELDS):
        if field in data:
            errors.append(f"unsupported top-level agent metadata field: {field}")
    instructions = data.get("developer_instructions")
    if isinstance(instructions, str) and instructions.strip():
        lowered = instructions.lower()
        for expected in ["ownership", "inputs", "outputs", "stop conditions", "handoff"]:
            if expected not in lowered:
                errors.append(f"developer_instructions missing agent contract term: {expected}")
    return errors


def read_utf8_text(path: Path) -> tuple[str, str | None]:
    try:
        if not path.exists():
            return "", "file does not exist"
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError):
        return "", READ_TEXT_ERROR


def is_forbidden_secret_assignment(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped or stripped.startswith(("#", "//", ";")):
        return False
    match = SECRET_ENVIRON_PATTERN.match(line) or SECRET_ASSIGNMENT_PATTERN.match(line)
    if not match:
        return False
    if not SECRET_NAME_PATTERN.search(match.group("name")):
        return False
    value = match.group("value").strip()
    if not value or value.startswith(("$", "{{", "<")):
        return False
    if SAFE_ENV_LOOKUP_PATTERN.match(value):
        return False
    return True


def validate_hook_file(path: Path) -> list[str]:
    text, error = read_utf8_text(path)
    if error:
        return [error]
    errors: list[str] = []
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        errors.append("contains forbidden secret-like literal")
    if path.name == "hooks.json":
        errors.extend(validate_hook_json_text(text))
    return errors


def validate_hook_json_text(text: str) -> list[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"invalid json: {exc}"]
    if not isinstance(data, dict):
        return ["hook json must be an object"]
    hook_events = data.get("hooks", data)
    if not isinstance(hook_events, dict):
        return ["hook json hooks must be an object"]
    errors: list[str] = []
    for event in HOOK_JSON_REQUIRED_EVENTS:
        value = hook_events.get(event)
        if value is None:
            errors.append(f"missing hook event: {event}")
            continue
        if not isinstance(value, list):
            errors.append(f"hook event must be a list: {event}")
            continue
        for index, group in enumerate(value):
            if not isinstance(group, dict):
                errors.append(f"hook event group must be an object: {event}[{index}]")
                continue
            commands = group.get("hooks")
            if not isinstance(commands, list) or not commands:
                errors.append(f"hook event group hooks must be a non-empty list: {event}[{index}]")
                continue
            for hook_index, hook in enumerate(commands):
                if not isinstance(hook, dict):
                    errors.append(f"hook command must be an object: {event}[{index}].hooks[{hook_index}]")
                    continue
                if hook.get("type") != "command":
                    errors.append(f"hook command type must be command: {event}[{index}].hooks[{hook_index}]")
                command = hook.get("command")
                if not isinstance(command, str) or not command.strip():
                    errors.append(f"hook command must be a non-empty string: {event}[{index}].hooks[{hook_index}]")
    return errors


def validate_task_matrix_file(path: Path) -> list[str]:
    text, error = read_utf8_text(path)
    if error:
        return [error]
    return validate_task_matrix_text(text)


def validate_task_matrix_text(text: str) -> list[str]:
    tasks = _parse_task_matrix_tasks(text)
    if not tasks:
        return ["no detailed task blocks found"]

    errors: list[str] = []
    for task in tasks:
        errors.extend(_validate_task_matrix_task(task))
    return errors


def _parse_task_matrix_tasks(text: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    section = "fields"
    for line in text.splitlines():
        heading = TASK_HEADING_PATTERN.match(line)
        if heading:
            current = {
                "id": heading.group("id").strip(),
                "fields": {},
                "completion": {},
                "raw": [line],
            }
            tasks.append(current)
            section = "fields"
            continue
        if current is None:
            continue
        current["raw"].append(line)
        if line.strip().lower() == "#### completion report":
            section = "completion"
            continue
        field = TASK_FIELD_PATTERN.match(line)
        if not field:
            continue
        name = field.group("name").strip()
        value = field.group("value").strip()
        target = current["completion"] if section == "completion" else current["fields"]
        target[name.lower()] = value
    return tasks


def _validate_task_matrix_task(task: dict[str, Any]) -> list[str]:
    task_id = _task_matrix_task_id(task)
    errors: list[str] = []
    fields = task["fields"]
    completion = task["completion"]

    if _contains_task_matrix_placeholder("\n".join(task["raw"])):
        errors.append(f"{task_id}: unresolved placeholder in task block")

    for field in TASK_MATRIX_REQUIRED_FIELDS:
        if field.lower() not in fields:
            errors.append(f"{task_id}: missing required field: {field}")

    for field in TASK_MATRIX_COMPLETION_FIELDS:
        if field.lower() not in completion:
            errors.append(f"{task_id}: missing completion report field: {field}")

    status = _normalize_task_matrix_status(fields.get("status", ""))
    completion_status = _normalize_task_matrix_status(completion.get("status", ""))
    if status and status not in TASK_MATRIX_ALLOWED_STATUSES:
        errors.append(f"{task_id}: invalid status: {fields.get('status', '')}")
    if completion_status and completion_status != status:
        errors.append(f"{task_id}: completion report status must match task status")
    if fields.get("schema version") and fields["schema version"] != TASK_MATRIX_SCHEMA_VERSION:
        errors.append(f"{task_id}: schema version must be {TASK_MATRIX_SCHEMA_VERSION}")
    if fields.get("timezone") and fields["timezone"] != "Europe/Moscow":
        errors.append(f"{task_id}: timezone must be Europe/Moscow")
    if fields.get("validator target") and "detailed task blocks" not in fields["validator target"].lower():
        errors.append(f"{task_id}: validator target must be detailed task blocks")

    task_timestamp = fields.get("date and time of task implementation", "")
    completion_timestamp = completion.get("actual implementation date and time", "")
    if status == "planned":
        if task_timestamp != "pending_execution_timestamp":
            errors.append(f"{task_id}: planned requires pending_execution_timestamp")
        if TASK_TIMESTAMP_PATTERN.match(completion_timestamp):
            errors.append(f"{task_id}: planned rows must not contain actual implementation date/time")
    if status == "implemented":
        if not TASK_TIMESTAMP_PATTERN.match(task_timestamp):
            errors.append(f"{task_id}: implemented requires actual DD-MM-YYYY HH:mm timestamp")
        if not TASK_TIMESTAMP_PATTERN.match(completion_timestamp):
            errors.append(f"{task_id}: implemented completion report requires actual DD-MM-YYYY HH:mm timestamp")
        for field in [
            "what was done",
            "files touched / work locations",
            "technical value delivered",
            "product value delivered",
            "verification evidence",
            "residual risks",
            "follow-up",
        ]:
            value = completion.get(field, "")
            if not value or value.lower() in {"pending", "n/a", "none"}:
                errors.append(f"{task_id}: implemented requires {field}")
        evidence = completion.get("verification evidence", "").lower()
        if "inspection-only" in evidence or "inspection only" in evidence:
            errors.append(f"{task_id}: implemented cannot use inspection-only verification evidence")
    return errors


def _task_matrix_task_id(task: dict[str, Any]) -> str:
    if _contains_task_matrix_placeholder(task["id"]):
        return task["id"]
    return task["fields"].get("task") or task["id"]


def _normalize_task_matrix_status(value: str) -> str:
    return value.strip().strip("`").lower()


def _contains_task_matrix_placeholder(value: str) -> bool:
    return bool(TASK_PLACEHOLDER_PATTERN.search(value))


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok") else 1


def main_control_plane(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_control_plane.py [workspace]")
        return 0
    root = Path(argv[0]) if argv else Path.cwd()
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "missing": CONTROL_PLANE_FILES,
                "errors": ["workspace does not exist"],
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "missing": CONTROL_PLANE_FILES,
                "errors": ["workspace is not a directory"],
            }
        )
    result = validate_control_plane(root)
    result["root"] = str(root)
    result["errors"] = []
    return print_json(result)


def main_agents(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_agents.py [agents-dir]")
        return 0
    root = Path(argv[0]) if argv else Path(".codex/agents")
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["agent directory does not exist"],
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["agent path is not a directory"],
            }
        )
    files = sorted(root.glob("*.toml"))
    file_errors = {str(path): validate_agent_file(path) for path in files}
    errors = ["no agent TOML files found"] if not files else []
    ok = bool(files) and all(not item for item in file_errors.values())
    return print_json(
        {
            "ok": ok,
            "root": str(root),
            "files": [str(path) for path in files],
            "errors": errors,
            "file_errors": file_errors,
        }
    )


def main_hooks(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_hooks.py [hooks-dir]")
        return 0
    root = Path(argv[0]) if argv else Path(".codex/hooks")
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["hook directory does not exist"],
            }
        )
    if root.is_file():
        file_errors = {str(root): validate_hook_file(root)}
        ok = not file_errors[str(root)]
        return print_json(
            {
                "ok": ok,
                "root": str(root),
                "files": [str(root)],
                "errors": [],
                "file_errors": file_errors,
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["hook path is not a directory"],
            }
        )
    files = sorted(path for path in root.iterdir() if path.is_file())
    file_errors = {str(path): validate_hook_file(path) for path in files}
    errors = ["no hook files found"] if not files else []
    ok = bool(files) and all(not item for item in file_errors.values())
    return print_json(
        {
            "ok": ok,
            "root": str(root),
            "files": [str(path) for path in files],
            "errors": errors,
            "file_errors": file_errors,
        }
    )


def main_task_matrix(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_task_matrix.py <task-matrix-file>")
        return 0
    if not argv:
        return print_json(
            {
                "ok": False,
                "path": "",
                "schema_version": TASK_MATRIX_SCHEMA_VERSION,
                "errors": ["task matrix path is required"],
            }
        )
    path = Path(argv[0])
    errors = validate_task_matrix_file(path)
    return print_json(
        {
            "ok": not errors,
            "path": str(path),
            "schema_version": TASK_MATRIX_SCHEMA_VERSION,
            "errors": errors,
        }
    )
