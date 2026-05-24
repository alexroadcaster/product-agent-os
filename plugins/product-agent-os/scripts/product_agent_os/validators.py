from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import tomllib

from product_agent_os.contracts import CONTROL_PLANE_FILES


AGENT_REQUIRED_FIELDS = [
    "name",
    "description",
    "developer_instructions",
    "ownership",
    "inputs",
    "outputs",
    "stop_conditions",
    "model_policy",
    "handoff_requirements",
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
    return errors


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok") else 1


def main_control_plane(argv: list[str]) -> int:
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
