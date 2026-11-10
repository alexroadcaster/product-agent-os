from __future__ import annotations

import json
import hashlib
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
    """Separate executable payload from tool metadata; retain opaque forms for review."""
    call = _literal_call(payload)
    if call and call[0] == "exec_command" and isinstance(call[1], dict):
        command = call[1].get("cmd")
        if isinstance(command, str):
            return command
    if call and call[0] == "apply_patch" and isinstance(call[1], str):
        return call[1]
    if _tool_name(payload).rsplit(".", 1)[-1] in {"Bash", "shell_command"}:
        arguments = payload.get("tool_input", {})
        if isinstance(arguments, dict) and isinstance(arguments.get("command"), str):
            return arguments["command"]
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


def _literal_read_tokens(command: str) -> list[str] | None:
    """Lex a deliberately small literal subset; never interpret shell programs.

    Single-quoted metacharacters are data. Expanding strings, concatenated
    quoting, escapes and unknown syntax stay on the scoped lifecycle route.
    """
    if any(c in command for c in '\r\n"\0'):
        return None  # Newlines execute another statement; legacy native quoting can split argv.
    lexemes: list[str] = []
    pattern = re.compile(r"""\s*(?:'([^'\r\n]*)'|([^\s'";&><\x60$\r\n{}()\[\],]+))""")
    position = 0
    while position < len(command):
        if not command[position:].strip():
            break
        match = pattern.match(command, position)
        if not match:
            return None
        lexeme = match[1] if match[1] is not None else match[2]
        if match[2] is not None and any(c in lexeme for c in '\\*?!#@'):
            return None  # Do not interpret escapes, glob expansion or comments across shells.
        if match[2] is not None and "|" in lexeme and lexeme != "|":
            return None
        position = match.end()
        if position < len(command) and not command[position].isspace():
            return None
        if lexeme == "--%" or any(c in lexeme for c in "‘’“”"):
            return None
        if _matches(FORBIDDEN_PATH_PATTERNS, " " + lexeme):
            return None
        lexemes.append("\0PIPE" if match[2] == "|" else lexeme)
    return lexemes


def _is_read_only(command: str) -> bool:
    """Recognize literal reads without granting authority to unknown shell syntax."""
    # A bounded sequence of independently safe literal reads is still read-only.
    # Split only outside single quotes; never execute or interpret shell code.
    if len(command) > 32768:
        return False
    quoted, start, statements = False, 0, []
    for index, char in enumerate(command):
        if char == "'":
            quoted = not quoted
        elif char == ";" and not quoted:
            statements.append(command[start:index].strip())
            start = index + 1
    if statements:
        statements.append(command[start:].strip())
        return (not quoted and len(statements) <= 16 and all(statements)
                and all(_is_read_only(part) for part in statements))
    lexemes = _literal_read_tokens(command)
    if not lexemes:
        return False
    name = lexemes[0].lower()
    # A pipe is trusted only as a separate lexeme and with a fixed read consumer.
    if "\0PIPE" in lexemes:
        if lexemes.count("\0PIPE") != 1:
            return False
        index = lexemes.index("\0PIPE")
        left, right = lexemes[:index], lexemes[index + 1:]
        if name not in {"get-content", "rg", "get-childitem"} or not right:
            return False
        if not _read_command_tokens(left):
            return False
        consumer = right[0].lower()
        if consumer == "select-string":
            return _read_command_tokens(right)
        if consumer == "select-object":
            pairs = right[1:]
            return bool(pairs) and len(pairs) % 2 == 0 and all(
                pairs[i].lower() in {"-first", "-last", "-skip"}
                and pairs[i + 1].isdigit() for i in range(0, len(pairs), 2)
            )
        return False
    return _read_command_tokens(lexemes)


def _read_command_tokens(lexemes: list[str]) -> bool:
    """Keep executable names and switches exact; aliases and expansions are untrusted."""
    name = lexemes[0].lower()
    if name not in {"rg", "get-content", "get-childitem", "select-string", "git", "type", "dir", "ls"}:
        return False
    # Only known inert switches are admitted; abbreviations/config/executors fail closed.
    flags = {
        "rg": {"-n", "-i", "-l", "-s", "-f", "-g", "-e", "-a", "-b", "-c",
               "--files", "--hidden", "--glob", "--iglob", "--fixed-strings",
               "--line-number", "--ignore-case", "--files-with-matches", "--no-ignore",
               "--heading", "--no-heading", "--count", "--max-count", "--"},
        "get-content": {"-raw", "-literalpath", "-path", "-totalcount", "-encoding", "-tail"},
        "get-childitem": {"-literalpath", "-path", "-recurse", "-file", "-directory", "-force", "-name"},
        "select-string": {"-simplematch", "-pattern", "-path", "-literalpath", "-casesensitive", "-list", "-quiet", "-context"},
        "type": set(), "dir": set(), "ls": set(),
        "git": {"--stat", "--short", "--oneline", "--name-only", "--name-status", "--check",
                "--no-ext-diff", "--no-textconv", "--", "-n"},
    }
    if name == "git" and (len(lexemes) < 2 or lexemes[1].lower() not in {"diff", "status", "show", "log"}):
        return False
    return all(not lexeme.startswith("-") or lexeme.lower() in flags[name] for lexeme in lexemes[1:])


def lifecycle_session_id(payload: dict[str, Any]) -> str | None:
    """Use only the host envelope; tool arguments never select another chat."""
    if "session_id" not in payload:
        return None
    value = payload["session_id"]
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", value):
        raise ValueError("invalid host session_id")
    return value


def lifecycle_marker_path(root: Path, payload: dict[str, Any]) -> Path:
    """Select an isolated marker, with legacy mode only when identity is absent."""
    session = lifecycle_session_id(payload)
    relative = LIFECYCLE_STATE_REL
    if session is not None:
        digest = hashlib.sha256(session.encode("utf-8")).hexdigest()
        relative = relative.with_name("lifecycle-state." + digest + ".json")
    root = root.resolve()
    path = root / relative
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
            raise ValueError("lifecycle marker must not use a symlink or junction")
    if not path.resolve().is_relative_to(root):
        raise ValueError("lifecycle marker must stay in workspace")
    return path


def _marker_write_targets(payload: dict[str, Any], command: str) -> tuple[list[str], bool]:
    """Recognize patch destinations or one literal marker write, not body mentions."""
    call = _literal_call(payload)
    patch = call[1] if call and call[0] == "apply_patch" else None
    if isinstance(patch, str):
        lines = patch.strip().splitlines()
        targets = re.findall(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$", patch, re.MULTILINE)
        exact = (len(targets) == 1 and len(lines) >= 4 and lines[0] == "*** Begin Patch"
                 and lines[-1] == "*** End Patch" and not any(
                     line.startswith(("*** Delete File:", "*** Move to:")) for line in lines))
        return targets, exact
    match = re.fullmatch(
        r"(?is)\s*Set-Content\s+(?:-LiteralPath\s+)?('([^']+)'|\"([^\"]+)\"|([^\s;|]+))"
        r"\s+(?:-Value\s+)?'((?:[^']|'')*)'(?:\s+-Encoding\s+utf8)?\s*", command
    )
    if match:
        return [next(value for value in match.group(2, 3, 4) if value is not None)], True
    return [], False


def _marker_write_policy(root: Path, payload: dict[str, Any], command: str) -> tuple[bool, str | None]:
    """Bootstrap only this chat's marker; other targets need ordinary validation."""
    own = lifecycle_marker_path(root, payload)
    targets, exact = _marker_write_targets(payload, command)
    marker_targets = []
    for value in targets:
        path = Path(value)
        path = path if path.is_absolute() else root / path
        path = path.resolve()
        if path.parent == own.parent and re.fullmatch(r"lifecycle-state(?:\.[0-9a-f]+)?\.json", path.name, re.IGNORECASE):
            marker_targets.append(path)
    if not marker_targets:
        return False, None
    if not exact or len(targets) != 1 or marker_targets != [own]:
        return False, "lifecycle writes must target only this session's marker"
    shown = re.search(r"task_start_brief_shown|scope_note_shown", command)
    return bool(shown), None


def _is_mutating(tool: str, command: str) -> bool:
    if "apply_patch" in tool.lower():
        return True
    if tool.rsplit(".", 1)[-1] in {"", "exec_command", "shell_command", "Bash"} and _is_read_only(command):
        return False
    # Unknown commands need the same scoped lifecycle check as known writes.
    return bool(command.strip())


def _safety_reasons(root: Path | None, payload: dict[str, Any], command: str) -> list[str]:
    """Inspect executable text or patch destinations, never Markdown patch prose."""
    call = _literal_call(payload)
    authoring = _authoring_call(payload)
    if authoring is not None:
        call = ("apply_patch", authoring[1])
    if call and call[0] == "apply_patch" and isinstance(call[1], str):
        root = root or _workspace_root(payload)
        targets = re.findall(r"^\*\*\* (?:(?:Add|Update|Delete) File|Move to): (.+)$", call[1], re.MULTILINE)
        reasons = []
        for target in targets:
            path = Path(target)
            path = path if path.is_absolute() else root / path
            if not path.resolve().is_relative_to(root.resolve()):
                reasons.append("Patch destination is outside project ownership.")
            if re.search(r"(?i)(?:^|[/\\])(?:\.env(?:\.|$)|[^/\\]*(?:credential|secret|private[_-]?key))", target):
                reasons.append("Patch destination may contain sensitive material.")
        return reasons
    if call and call[0] == "exec_command" and isinstance(call[1], dict):
        command = str(call[1].get("cmd", ""))
    reasons = []
    explicit_shell = bool(call and call[0] == "exec_command" and isinstance(call[1], dict) and call[1].get("shell"))
    if (explicit_shell or not _is_read_only(command)) and _matches(DESTRUCTIVE_PATTERNS, command):
        reasons.append("Destructive command blocked; require explicit approval and scoped target review.")
    if _matches(FORBIDDEN_PATH_PATTERNS, command):
        reasons.append("Command references a path outside normal project ownership.")
    if _matches(SENSITIVE_WRITE_PATTERNS, command):
        reasons.append("Command may write sensitive material; credentials must not enter project artifacts.")
    return reasons


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


def _lifecycle_marker_ok(path: Path, *, now: datetime | None = None, report_authorized: bool = False,
                         expected_session_id: str | None = None) -> tuple[bool, str]:
    """Validate current lifecycle scope; reporting never grants action authority."""
    if not path.exists():
        return False, "missing lifecycle marker"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, "invalid lifecycle marker"
    if not isinstance(payload, dict):
        return False, "lifecycle marker must be a JSON object"
    if payload.get("session_id") != expected_session_id:
        return False, "lifecycle marker session_id does not match host session"
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
        if scope.get("work_type") not in {"implementation", "fix", "review", "research", "planning", "report_authoring"} or scope.get("size") not in {"bounded", "large"} or scope.get("risk") not in {"low", "medium", "high"}:
            return False, "invalid lifecycle_scope classification"
        flags = ("financially_material", "release_or_readiness", "explicit_packet_request")
        if any(type(scope.get(key)) is not bool for key in flags) or not isinstance(scope.get("reason"), str) or not scope["reason"].strip():
            return False, "lifecycle_scope requires boolean triggers and a reason"
        # Reporting scope never grants mutation authority to a read-only request.
        if scope["work_type"] in {"review", "research", "planning", "report_authoring"} and not report_authorized:
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


def _literal_call(payload: dict[str, Any]) -> tuple[str, Any] | None:
    """Recognize one literal tool call, never evaluate arbitrary wrapper code."""
    tool = _tool_name(payload).rsplit(".", 1)[-1]
    value = payload.get("tool_input", payload.get("arguments", payload.get("input")))
    if tool in {"apply_patch", "exec_command"}:
        if tool == "apply_patch" and isinstance(value, dict) and len(value) == 1:
            value = value.get("command", value.get("patch", value.get("input")))
        return tool, value
    if tool != "exec":
        return None
    code = value.get("code") if isinstance(value, dict) else value
    if not isinstance(code, str):
        return None
    prefix = re.match(r"^\s*(text\(\s*)?await\s+tools\.(apply_patch|exec_command)\(\s*", code)
    if not prefix:
        return None
    try:
        argument, end = json.JSONDecoder().raw_decode(code[prefix.end():])
    except ValueError:
        return None
    suffix = code[prefix.end() + end:]
    pattern = r"\s*\)\s*\)\s*;?\s*" if prefix[1] else r"\s*\)\s*;?\s*"
    return (prefix[2], argument) if re.fullmatch(pattern, suffix) else None


def _report_read_only(payload: dict[str, Any]) -> bool:
    """Allow literal PowerShell reads only; flags such as git --output can write."""
    call = _literal_call(payload)
    if call is None or call[0] != "exec_command" or not isinstance(call[1], dict):
        return False
    args = call[1]
    if set(args) - {"cmd", "login", "max_output_tokens", "yield_time_ms"} or args.get("login") is not False:
        return False
    command = args.get("cmd")
    return isinstance(command, str) and bool(re.fullmatch(
        r"(?i)(?:Get-Content|Get-ChildItem) -LiteralPath '[A-Za-z0-9_./\\ :\-]+'(?: -Raw)?", command
    ))


def _report_path(root: Path, value: Any, *, allow_existing: bool = False) -> Path:
    """Reject traversal, aliases and existing/symlink targets before create-only writes."""
    if not isinstance(value, str) or not value or value != value.strip() or any(ord(c) < 32 for c in value):
        raise ValueError("invalid_report_path")
    value = value.replace("\\", "/")
    path = Path(value)
    if path.is_absolute():
        value = path.relative_to(root).as_posix()
    parts = value.split("/")
    if any(p in {"", ".."} or p.endswith((".", " ")) or ":" in p or "~" in p for p in parts):
        raise ValueError("report_path_alias_or_traversal")
    parts = [p for p in parts if p != "."]
    protected = {"agents.md", "agents.override.md", "requirements.md", "plan.md", "test.md", "evals.md", "runlog.md", "skill.md"}
    if not parts or any(p.startswith(".") for p in parts) or parts[-1].lower() in protected:
        raise ValueError("protected_report_destination")
    if any(re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", p) for p in parts):
        raise ValueError("reserved_report_destination")
    candidate = root.joinpath(*parts)
    if candidate.suffix.lower() != ".md" or not candidate.resolve().is_relative_to(root):
        raise ValueError("report_must_be_workspace_markdown")
    if (candidate.exists() and not allow_existing) or any(
        p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction())
        for p in (candidate, *candidate.parents)
    ):
        raise ValueError("report_destination_exists_or_is_symlink")
    if candidate.exists() and (not candidate.is_file() or candidate.stat().st_nlink != 1):
        raise ValueError("report_destination_not_regular_or_has_aliases")
    return candidate.resolve()


def _authoring_call(payload: dict[str, Any]) -> tuple[str, str] | None:
    """A literal digest comment plus one patch call; no evaluated expressions."""
    if _tool_name(payload).rsplit(".", 1)[-1] != "exec":
        return None
    value = payload.get("tool_input", payload.get("arguments", payload.get("input")))
    code = value.get("code") if isinstance(value, dict) else value
    if not isinstance(code, str) or len(code) > 2_000_000:
        return None
    header = re.match(r"\A// paos-report-previous-sha256: (absent|[0-9a-f]+)\n", code)
    if not header:
        return None
    if header[1] != "absent" and len(header[1]) != 64:
        return None
    call = _literal_call({"tool_name": "functions.exec", "tool_input": code[header.end():]})
    if call is None or call[0] != "apply_patch" or not isinstance(call[1], str):
        return None
    return header[1], call[1]


def _report_authoring_action_ok(root: Path, payload: dict[str, Any], authority: Path,
                               expected_sha256: str) -> tuple[bool, str]:
    """Opt-in v2: one session/report, CAS preflight and whole-file patch context.

    The host still owns the actual write. This guard cannot lock the interval
    between hook return and patch application; concurrent writers must be excluded.
    """
    root = root.resolve()
    try:
        if (not authority.resolve().is_relative_to(root) or authority.is_symlink()
                or authority.stat().st_size > 65536):
            return False, "authority_path_or_size_invalid"
        raw = authority.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            return False, "authority_pin_mismatch"
        grant = json.loads(raw)
        fields = {"schema_version", "task_id", "session_id", "workspace_sha256", "marker_sha256",
                  "output_path", "issued_at", "expires_at"}
        if (not isinstance(grant, dict) or set(grant) != fields
                or type(grant["schema_version"]) is not int or grant["schema_version"] != 2
                or any(not isinstance(grant[k], str) or not grant[k] for k in fields - {"schema_version"})):
            return False, "authoring_schema_invalid"
        session = lifecycle_session_id(payload)
        if session is None or grant["session_id"] != session:
            return False, "authoring_session_mismatch"
        if grant["workspace_sha256"] != hashlib.sha256(os.path.normcase(str(root)).encode()).hexdigest():
            return False, "authority_workspace_mismatch"
        now = datetime.now(timezone.utc)
        issued, expiry = _parse_updated_at(grant["issued_at"]), _parse_updated_at(grant["expires_at"])
        if issued is None or expiry is None or issued > now + MARKER_FUTURE_SKEW or not issued < expiry or expiry <= now or expiry - issued > timedelta(hours=24):
            return False, "authority_expired_or_invalid_window"
        marker_path = lifecycle_marker_path(root, payload)
        marker_raw = marker_path.read_bytes()
        if hashlib.sha256(marker_raw).hexdigest() != grant["marker_sha256"]:
            return False, "authority_marker_mismatch"
        marker = json.loads(marker_raw)
        if (marker.get("task_id") != grant["task_id"] or not isinstance(marker.get("lifecycle_scope"), dict)
                or marker["lifecycle_scope"].get("work_type") != "report_authoring"):
            return False, "explicit_report_authoring_scope_required"
        valid, reason = _lifecycle_marker_ok(marker_path, now=now, report_authorized=True,
                                            expected_session_id=session)
        if not valid:
            return False, reason
        name = grant["output_path"]
        if Path(name).is_absolute() or "\\" in name or any(p in {"", ".", ".."} for p in name.split("/")):
            return False, "authoring_path_must_be_canonical_relative"
        report = _report_path(root, name, allow_existing=True)
        call = _authoring_call(payload)
        if call is None:
            return False, "literal_digest_and_single_patch_required"
        previous, patch = call
        lines = patch.splitlines()
        if len(lines) < 4 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
            return False, "invalid_authoring_patch"
        if previous == "absent":
            if report.exists() or lines[1] != "*** Add File: " + name or any(not line.startswith("+") for line in lines[2:-1]):
                return False, "authoring_create_conflict"
        else:
            if not report.exists() or report.stat().st_size > 1_000_000:
                return False, "authoring_report_missing_or_too_large"
            before = report.read_bytes()
            if hashlib.sha256(before).hexdigest() != previous:
                return False, "authoring_previous_digest_conflict"
            if (lines[1] != "*** Update File: " + name or lines[2] != "@@"
                    or lines[-2] != "*** End of File" or any(not line.startswith(("-", "+")) for line in lines[3:-2])):
                return False, "single_whole_report_update_required"
            # All previous lines must occur verbatim; partial/mixed hunks fail closed.
            removed = [line[1:] for line in lines[3:-2] if line.startswith("-")]
            if removed != before.decode("utf-8").splitlines():
                return False, "authoring_previous_content_conflict"
        return True, "ok"
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return False, "report_authoring_invalid"


def _report_action_ok(root: Path, payload: dict[str, Any], authority: Path, expected_sha256: str) -> tuple[bool, str]:
    """Validate operator-pinned authority, task transition and one exact Add File.

    The pin is supplied only by trusted hook command arguments, never tool data.
    This is a preflight guard, not an atomic filesystem transaction or sandbox.
    """
    root = root.resolve()
    try:
        authority = authority.resolve()
        if not authority.is_relative_to(root) or authority.stat().st_size > 65536:
            return False, "authority_path_or_size_invalid"
        raw = authority.read_bytes()
        if len(expected_sha256) != 64 or not re.fullmatch(r"[0-9a-f]+", expected_sha256) or hashlib.sha256(raw).hexdigest() != expected_sha256:
            return False, "authority_pin_mismatch"
        grant = json.loads(raw)
        fields = {"schema_version", "task_id", "previous_task_id", "workspace_sha256", "marker_sha256", "output_path", "issued_at", "expires_at"}
        if not isinstance(grant, dict) or set(grant) != fields or type(grant["schema_version"]) is not int or grant["schema_version"] != 1:
            return False, "authority_schema_invalid"
        if any(not isinstance(grant[k], str) or not grant[k].strip() for k in fields - {"schema_version"}):
            return False, "authority_fields_invalid"
        if grant["workspace_sha256"] != hashlib.sha256(os.path.normcase(str(root)).encode()).hexdigest():
            return False, "authority_workspace_mismatch"
        issued, expiry = _parse_updated_at(grant["issued_at"]), _parse_updated_at(grant["expires_at"])
        now = datetime.now(timezone.utc)
        if issued is None or expiry is None or issued > now + MARKER_FUTURE_SKEW or not issued < expiry or expiry <= now or expiry - issued > timedelta(hours=24):
            return False, "authority_expired_or_invalid_window"
        marker_path = lifecycle_marker_path(root, payload)
        marker_raw = marker_path.read_bytes()
        if hashlib.sha256(marker_raw).hexdigest() != grant["marker_sha256"]:
            return False, "authority_marker_mismatch"
        marker = json.loads(marker_raw)
        if not isinstance(marker, dict) or marker.get("task_id") != grant["task_id"] or marker.get("previous_task_id") != grant["previous_task_id"] or grant["task_id"] == grant["previous_task_id"]:
            return False, "explicit_new_task_transition_required"
        if not isinstance(marker.get("lifecycle_scope"), dict) or marker["lifecycle_scope"].get("work_type") not in {"research", "review", "planning"}:
            return False, "report_authority_requires_read_only_task"
        valid, reason = _lifecycle_marker_ok(marker_path, now=now, report_authorized=True,
                                            expected_session_id=lifecycle_session_id(payload))
        if not valid:
            return False, reason
        allowed = _report_path(root, grant["output_path"])
        call = _literal_call(payload)
        if call is None or call[0] != "apply_patch" or not isinstance(call[1], str):
            return False, "only_literal_single_report_patch_allowed"
        lines = call[1].strip().splitlines()
        if len(lines) < 4 or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch" or not lines[1].startswith("*** Add File: ") or any(not line.startswith("+") for line in lines[2:-1]):
            return False, "only_single_add_file_patch_allowed"
        if _report_path(root, lines[1][len("*** Add File: "):]) != allowed:
            return False, "report_output_not_authorized"
        return True, "ok"
    except (OSError, ValueError, TypeError, KeyError):
        return False, "report_authority_invalid"


def _report_options(argv: list[str], root: Path) -> tuple[Path, str] | None:
    """Only trusted command-line flags select report mode; payload fields are inert."""
    if not any(arg.startswith("--report-authority") for arg in argv):
        return None
    if len(argv) != 4 or argv[0] != "--report-authority" or argv[2] != "--report-authority-sha256":
        raise ValueError("invalid_report_authority_arguments")
    path = Path(argv[1])
    return (path if path.is_absolute() else root / path), argv[3]


def main(argv: list[str] | None = None) -> int:
    """Deny unsafe or unbriefed mutations through the official PreToolUse wire contract."""
    payload, raw = _read_payload()
    command = _command_text(payload, raw)
    tool = _tool_name(payload)
    call = _literal_call(payload)
    if call is not None:
        tool = call[0]
    reasons = _safety_reasons(None, payload, command)

    arguments = sys.argv[1:] if argv is None else argv
    if any(arg.startswith("--report-authoring") for arg in arguments):
        if len(arguments) != 4 or arguments[0] != "--report-authoring" or arguments[2] != "--report-authoring-sha256":
            _deny("Invalid pinned report authoring configuration.")
            return 0
        if not _report_read_only(payload):
            root = _workspace_root(payload)
            allowed, reason = _report_authoring_action_ok(root, payload, root / arguments[1], arguments[3])
            if not allowed:
                reasons.append("Report authoring denied: " + reason)
        if reasons:
            _deny(" ".join(dict.fromkeys(reasons)))
        return 0
    try:
        options = _report_options(arguments, _workspace_root(payload)) if any(arg.startswith("--report-authority") for arg in arguments) else None
    except ValueError:
        _deny("Invalid pinned report authority configuration.")
        return 0
    if options is not None:
        if not _report_read_only(payload):
            allowed, reason = _report_action_ok(_workspace_root(payload), payload, *options)
            if not allowed:
                reasons.append("Report authority denied: " + reason)
        if reasons:
            _deny(" ".join(dict.fromkeys(reasons)))
        return 0

    mutating = _is_mutating(tool, command)
    if call and call[0] == "exec_command" and isinstance(call[1], dict) and call[1].get("shell"):
        mutating = True  # An explicit interpreter can assign different semantics to literal text.
    if mutating:
        try:
            root = _workspace_root(payload)
            marker_path = lifecycle_marker_path(root, payload)
            marker_write, write_error = _marker_write_policy(root, payload, command)
            if write_error:
                reasons.append(write_error)
            elif not marker_write:
                marker_ok, marker_reason = _lifecycle_marker_ok(
                    marker_path, expected_session_id=lifecycle_session_id(payload)
                )
                if not marker_ok:
                    reasons.append(
                        "Mutating Product-Agent OS work requires current scope-applicable reporting and an active lifecycle marker: "
                        + marker_reason + ". Selected marker: " + marker_path.relative_to(root).as_posix()
                        + ". Do not reset another chat's marker."
                    )
        except ValueError as exc:
            reasons.append(str(exc))

    if reasons:
        _deny(" ".join(dict.fromkeys(reasons)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
