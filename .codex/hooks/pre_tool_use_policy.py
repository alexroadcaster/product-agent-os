from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


LIFECYCLE_STATE_REL = Path(".codex/product-agent-os/lifecycle-state.json")
WORKSPACE_ROOT_ENV = "CODEX_HOOK_WORKSPACE_ROOT"
TASK_BRIEF_SCHEMA_VERSION = "task_start_brief_v1"
MARKER_MAX_AGE = timedelta(hours=48)
MARKER_FUTURE_SKEW = timedelta(minutes=5)
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
BRIEF_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]+$")
TASK_START_FIELDS = [
    "Request", "Goal", "Context", "Scope", "Value", "Execution", "Acceptance",
    "Risks / approvals", "Next step",
]
SENSITIVE_KEY_RE = re.compile(r"(?i)(?:api[_-]?key|password|secret|token|private[_-]?key|credential)")

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
    re.compile(r"(?i)\b(git\s+(?:add|apply|commit|push|checkout|switch|branch|merge|rebase|tag)|npm\s+install|pip\s+install)\b"),
    re.compile(r"(?i)\bpython\b.*\b(?:--stage|complete|apply|merge|write|update)\b"),
    re.compile(r"(?i)(?:^|\s)>+\s*[^\s]+"),
]
READ_ONLY_PATTERNS = [
    re.compile(r"(?i)^\s*(get-content|get-childitem|select-string|rg|git\s+(?:diff|status|show|log)|python\b.*(?:--help|-h)|type|dir|ls)\b"),
]
LIFECYCLE_MARKER_WRITE_PATTERNS = [
    re.compile(r"(?i)\.codex[/\\]product-agent-os[/\\]lifecycle-state\.json"),
    re.compile(r"(?i)(?:task_start_brief_shown|scope_note_shown)"),
]


def _workspace_root(payload: dict[str, Any] | None = None) -> Path:
    """Resolve the project root without exposing it in hook output."""
    override = os.environ.get(WORKSPACE_ROOT_ENV)
    if override:
        return Path(override).resolve()
    payload_cwd = payload.get("cwd") if payload else None
    if isinstance(payload_cwd, str) and payload_cwd.strip():
        current = Path(payload_cwd).resolve()
        for candidate in [current, *current.parents]:
            if (candidate / ".codex").exists():
                return candidate
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


def _read_payload() -> tuple[dict[str, Any], str]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}, ""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}, raw
    return (data, raw) if isinstance(data, dict) else ({}, raw)


def _strings_from(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [item for nested in value.values() for item in _strings_from(nested)]
    if isinstance(value, list):
        return [item for nested in value for item in _strings_from(nested)]
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


def _matches(patterns: list[re.Pattern[str]], text: str) -> bool:
    return any(pattern.search(text) for pattern in patterns)


def _is_read_only(command: str) -> bool:
    return bool(command.strip()) and _matches(READ_ONLY_PATTERNS, command.strip())


def _is_lifecycle_marker_write(command: str) -> bool:
    return all(pattern.search(command) for pattern in LIFECYCLE_MARKER_WRITE_PATTERNS)


def _is_mutating(tool: str, command: str) -> bool:
    if "apply_patch" in tool.lower():
        return True
    if _is_read_only(command):
        return False
    return _matches(MUTATING_PATTERNS, command)


def _contains_sensitive_key(value: Any) -> bool:
    if isinstance(value, dict):
        return any(SENSITIVE_KEY_RE.search(str(key)) or _contains_sensitive_key(item) for key, item in value.items())
    if isinstance(value, list):
        return any(_contains_sensitive_key(item) for item in value)
    return False


def _parse_updated_at(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _lifecycle_marker_ok(path: Path, *, now: datetime | None = None) -> tuple[bool, str]:
    """Validate current lifecycle scope; reporting never grants action authority."""
    if not path.exists():
        return False, "missing lifecycle marker"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, "invalid lifecycle marker"
    if not isinstance(payload, dict):
        return False, "lifecycle marker must be a JSON object"
    schema = payload.get("brief_schema_version")
    concise = schema == "task_scope_note_v1"
    if concise and payload.get("scope_note_shown") is not True:
        return False, "scope_note_shown must be true"
    if not concise and payload.get("task_start_brief_shown") is not True:
        return False, "task_start_brief_shown must be true"
    if payload.get("completion_brief_shown") is True:
        return False, "lifecycle marker belongs to a completed task"
    if payload.get("completion_ready") is True:
        return False, "completion_ready marker cannot authorize further mutation"
    if payload.get("status") != "in_progress":
        return False, "lifecycle marker status must be in_progress"
    for key in ("task_id", "scope", "updated_at", "approval_boundary"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, "missing lifecycle marker field: " + key
    if schema not in {TASK_BRIEF_SCHEMA_VERSION, "task_start_brief_v2", "task_scope_note_v1"}:
        return False, "unsupported brief_schema_version"
    expected_format = "concise" if concise else "bold_fields" if schema == "task_start_brief_v2" else "field_list"
    if payload.get("brief_format") != expected_format:
        return False, "brief_format must be " + expected_format
    if schema != TASK_BRIEF_SCHEMA_VERSION:
        scope = payload.get("lifecycle_scope")
        if not isinstance(scope, dict):
            return False, "lifecycle_scope must classify packet applicability"
        if scope.get("work_type") not in {"implementation", "fix", "review", "research", "planning"} or scope.get("size") not in {"bounded", "large"} or scope.get("risk") not in {"low", "medium", "high"}:
            return False, "invalid lifecycle_scope classification"
        flags = ("financially_material", "release_or_readiness", "explicit_packet_request")
        if any(type(scope.get(key)) is not bool for key in flags) or not isinstance(scope.get("reason"), str) or not scope["reason"].strip():
            return False, "lifecycle_scope requires boolean triggers and a reason"
        # Reporting scope never grants mutation authority to a read-only request.
        if scope["work_type"] in {"review", "research", "planning"}:
            return False, "read-only lifecycle scope does not authorize mutation"
        full_required = scope["size"] == "large" or scope["risk"] == "high" or any(scope[key] for key in flags)
        if concise and full_required:
            return False, "full Task Start Brief required for this scope"
    brief_digest = payload.get("brief_digest")
    if (
        not isinstance(brief_digest, str)
        or len(brief_digest) != len("sha256:") + 64
        or not BRIEF_DIGEST_RE.fullmatch(brief_digest)
    ):
        return False, "brief_digest must match sha256:<64 lowercase hex characters>"
    fields = payload.get("brief_fields_present")
    if not isinstance(fields, list) or not all(isinstance(item, str) for item in fields):
        return False, "brief_fields_present must list applicable lifecycle fields"
    required = ["Scope", "Evidence", "Limits"] if concise else TASK_START_FIELDS if schema == "task_start_brief_v2" else TASK_BRIEF_REQUIRED_FIELDS
    missing_fields = [field for field in required if field not in fields]
    if missing_fields:
        return False, "brief_fields_present missing: " + ", ".join(missing_fields)
    updated_at = _parse_updated_at(payload["updated_at"])
    if updated_at is None:
        return False, "updated_at must be an ISO-8601 timestamp with timezone"
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    age = current - updated_at
    if age < -MARKER_FUTURE_SKEW:
        return False, "lifecycle marker updated_at is too far in the future"
    if age > MARKER_MAX_AGE:
        return False, "lifecycle marker is stale; refresh updated_at after showing current task state"
    if _contains_sensitive_key(payload):
        return False, "lifecycle marker contains a sensitive-looking field name"
    return True, "ok"


def _deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            },
            sort_keys=True,
        )
    )


def main() -> int:
    """Deny unsafe or unbriefed mutations through the official PreToolUse wire contract."""
    payload, raw = _read_payload()
    command = _command_text(payload, raw)
    tool = _tool_name(payload)
    reasons: list[str] = []

    if _matches(DESTRUCTIVE_PATTERNS, command):
        reasons.append("Destructive command blocked; require explicit approval and scoped target review.")
    if _matches(FORBIDDEN_PATH_PATTERNS, command):
        reasons.append("Command references a path outside normal project ownership.")
    if _matches(SENSITIVE_WRITE_PATTERNS, command):
        reasons.append("Command may write sensitive material; credentials must not enter project artifacts.")

    mutating = _is_mutating(tool, command)
    marker_write = _is_lifecycle_marker_write(command)
    if mutating and not marker_write:
        marker_ok, marker_reason = _lifecycle_marker_ok(_workspace_root(payload) / LIFECYCLE_STATE_REL)
        if not marker_ok:
            reasons.append(
                "Mutating Product-Agent OS work requires current scope-applicable reporting and an active lifecycle marker: "
                + marker_reason
                + "."
            )

    if reasons:
        _deny(" ".join(dict.fromkeys(reasons)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
