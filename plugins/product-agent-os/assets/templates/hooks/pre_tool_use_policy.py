from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


LIFECYCLE_STATE_REL = Path(".codex/product-agent-os/lifecycle-state.json")

DESTRUCTIVE_PATTERNS = [
    re.compile(r"(?i)\brm\s+-(?:[a-z]*r[a-z]*f|[a-z]*f[a-z]*r)\b"),
    re.compile(r"(?i)\bremove-item\b.*\b-recurse\b"),
    re.compile(r"(?i)\bgit\s+reset\s+--hard\b"),
    re.compile(r"(?i)\bgit\s+clean\s+-[a-z]*[fd][a-z]*\b"),
    re.compile(r"(?i)\brmdir\s+/s\b"),
    re.compile(r"(?i)\bdel\s+/[a-z]*s\b"),
    re.compile(r"(?i)\bformat\b\s+[a-z]:"),
]
FORBIDDEN_PATH_PATTERNS = [
    re.compile(r"(?i)(?:^|\s)(?:~|%USERPROFILE%|\$HOME)[/\\]\.ssh(?:[/\\]|\s|$)"),
    re.compile(r"(?i)(?:^|\s)c:[/\\]windows[/\\]system32(?:[/\\]|\s|$)"),
    re.compile(r"(?i)(?:^|\s)/etc(?:/|\s|$)"),
    re.compile(r"(?i)(?:^|\s)/var(?:/|\s|$)"),
]
SENSITIVE_WRITE_PATTERNS = [
    re.compile(r"(?i)(?:^|\s)>+\s*[^\s]*(?:\.env|credential|secret|private[_-]?key)[^\s]*"),
    re.compile(r"(?i)(?:setx|export)\s+[a-z0-9_]*(?:secret|token|password|private[_-]?key|api[_-]?key)"),
    re.compile(r"(?i)os\.environ\[[\"'][^\"']*(?:secret|token|password|private[_-]?key|api[_-]?key)[^\"']*[\"']\]\s*="),
]
MUTATING_PATTERNS = [
    re.compile(r"(?i)\b(apply_patch|set-content|add-content|out-file|new-item|copy-item|move-item|remove-item|rename-item)\b"),
    re.compile(r"(?i)\b(git\s+(?:add|commit|push|checkout|switch|branch|merge|rebase|tag)|npm\s+install|pip\s+install)\b"),
    re.compile(r"(?i)\bpython\b.*\b(?:--stage|complete|apply|merge|write|update)\b"),
    re.compile(r"(?i)(?:^|\s)>+\s*[^\s]+"),
]
READ_ONLY_PATTERNS = [
    re.compile(r"(?i)^\s*(get-content|get-childitem|select-string|rg|git\s+(?:diff|status|show|log)|python\b.*(?:--help|-h)|type|dir|ls)\b"),
]
LIFECYCLE_MARKER_WRITE_PATTERNS = [
    re.compile(r"(?i)\.codex[/\\]product-agent-os[/\\]lifecycle-state\.json"),
    re.compile(r"(?i)task_start_brief_shown"),
]
TASK_BRIEF_SCHEMA_VERSION = "task_start_brief_v1"
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
BRIEF_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{16,64}$")


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


def _read_payload() -> tuple[dict[str, Any], str]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}, ""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}, raw
    if isinstance(data, dict):
        return data, raw
    return {}, raw


def _strings_from(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        result: list[str] = []
        for nested in value.values():
            result.extend(_strings_from(nested))
        return result
    if isinstance(value, list):
        result = []
        for item in value:
            result.extend(_strings_from(item))
        return result
    return []


def _command_text(payload: dict[str, Any], raw: str) -> str:
    values: list[str] = []
    for key in ("command", "cmd", "tool_input", "arguments", "input", "parameters"):
        if key in payload:
            values.extend(_strings_from(payload[key]))
    return "\n".join(values) if values else raw


def _tool_name(payload: dict[str, Any]) -> str:
    for key in ("tool", "tool_name", "toolName", "name", "recipient_name"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _matches(patterns: list[re.Pattern[str]], text: str) -> list[str]:
    return [pattern.pattern for pattern in patterns if pattern.search(text)]


def _is_read_only(command: str) -> bool:
    return bool(command.strip()) and bool(_matches(READ_ONLY_PATTERNS, command.strip()))


def _is_lifecycle_marker_write(command: str) -> bool:
    matches = _matches(LIFECYCLE_MARKER_WRITE_PATTERNS, command)
    return len(matches) == len(LIFECYCLE_MARKER_WRITE_PATTERNS)


def _is_mutating(tool: str, command: str) -> bool:
    lowered_tool = tool.lower()
    if "apply_patch" in lowered_tool:
        return True
    if _is_read_only(command):
        return False
    return bool(_matches(MUTATING_PATTERNS, command))


def _lifecycle_marker_ok(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing lifecycle marker"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, "invalid lifecycle marker"
    if not isinstance(payload, dict):
        return False, "lifecycle marker must be a JSON object"
    if payload.get("task_start_brief_shown") is not True:
        return False, "task_start_brief_shown must be true"
    for key in ("task_id", "scope", "updated_at", "approval_boundary"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, "missing lifecycle marker field: " + key
    if payload.get("brief_schema_version") != TASK_BRIEF_SCHEMA_VERSION:
        return False, "brief_schema_version must be " + TASK_BRIEF_SCHEMA_VERSION
    if payload.get("brief_format") != "field_list":
        return False, "brief_format must be field_list"
    brief_digest = payload.get("brief_digest")
    if not isinstance(brief_digest, str) or not BRIEF_DIGEST_RE.match(brief_digest):
        return False, "brief_digest must match sha256:<hex>"
    fields = payload.get("brief_fields_present")
    if not isinstance(fields, list) or not all(isinstance(item, str) for item in fields):
        return False, "brief_fields_present must list Task Brief fields"
    missing_fields = [field for field in TASK_BRIEF_REQUIRED_FIELDS if field not in fields]
    if missing_fields:
        return False, "brief_fields_present missing: " + ", ".join(missing_fields)
    raw = json.dumps(payload, sort_keys=True).lower()
    if any(secret_word in raw for secret_word in ("api_key", "password", "secret", "token", "private_key")):
        return False, "lifecycle marker must not contain secrets"
    return True, "ok"


def _finding(kind: str, severity: str, blocking: bool, message: str) -> dict[str, Any]:
    return {"kind": kind, "severity": severity, "blocking": blocking, "message": message}


def main() -> int:
    payload, raw = _read_payload()
    command = _command_text(payload, raw)
    tool = _tool_name(payload)
    findings: list[dict[str, Any]] = []
    blocking = False

    if _matches(DESTRUCTIVE_PATTERNS, command):
        blocking = True
        findings.append(_finding("destructive_command", "high", True, "Command appears destructive; require explicit approval and scoped target review."))
    if _matches(FORBIDDEN_PATH_PATTERNS, command):
        blocking = True
        findings.append(_finding("forbidden_path", "high", True, "Command references a path outside normal project ownership."))
    if _matches(SENSITIVE_WRITE_PATTERNS, command):
        blocking = True
        findings.append(_finding("secret_risk_write", "medium", True, "Command may write sensitive material; avoid storing credentials in project artifacts."))

    mutating = _is_mutating(tool, command)
    marker_write = _is_lifecycle_marker_write(command)
    lifecycle_state = _workspace_root() / LIFECYCLE_STATE_REL
    marker_ok, marker_reason = _lifecycle_marker_ok(lifecycle_state)
    if mutating and not marker_write and not marker_ok:
        blocking = True
        findings.append(
            _finding(
                "missing_lifecycle_marker",
                "medium",
                True,
                "Mutating Product-Agent OS work requires a user-visible Task Brief and .codex/product-agent-os/lifecycle-state.json before execution.",
            )
        )

    output = {
        "hook": "pre_tool_use_policy",
        "decision": "block" if blocking else "observe",
        "input_bytes": len(raw.encode("utf-8")),
        "tool": tool,
        "mutating_command_detected": mutating,
        "lifecycle_marker": {
            "path": str(LIFECYCLE_STATE_REL),
            "ok": marker_ok,
            "reason": marker_reason,
            "marker_write_allowed": marker_write,
            "brief_schema_version": TASK_BRIEF_SCHEMA_VERSION if marker_ok else "",
            "required_brief_fields": TASK_BRIEF_REQUIRED_FIELDS,
        },
        "findings": findings,
        "notes": [
            "Read-only discovery remains allowed.",
            "For non-mechanical execution, show the full field-list Task Brief in chat before creating the lifecycle marker.",
            "For non-mechanical code edits, apply .codex/workflows/coding-standards.md and record coding-standard-checklist.md or a not_applicable reason.",
            "The lifecycle marker is a guardrail, not a raw transcript store.",
        ],
    }
    print(json.dumps(output, sort_keys=True))
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
