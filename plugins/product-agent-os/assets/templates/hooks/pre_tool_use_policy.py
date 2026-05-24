from __future__ import annotations

import json
import re
import sys


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
    re.compile(r"(?i)(?:^|\s)(?:~|%USERPROFILE%|\\\$HOME)[/\\]\.ssh(?:[/\\]|\s|$)"),
    re.compile(r"(?i)(?:^|\s)c:[/\\]windows[/\\]system32(?:[/\\]|\s|$)"),
    re.compile(r"(?i)(?:^|\s)/etc(?:/|\s|$)"),
    re.compile(r"(?i)(?:^|\s)/var(?:/|\s|$)"),
]
SENSITIVE_WRITE_PATTERNS = [
    re.compile(r"(?i)(?:^|\s)>+\s*[^\s]*(?:\.env|credential|secret|private[_-]?key)[^\s]*"),
    re.compile(r"(?i)(?:setx|export)\s+[a-z0-9_]*(?:secret|token|password|private[_-]?key|api[_-]?key)"),
    re.compile(r"(?i)os\.environ\[[\"'][^\"']*(?:secret|token|password|private[_-]?key|api[_-]?key)[^\"']*[\"']\]\s*="),
]


def _read_payload() -> tuple[dict[str, object], str]:
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


def _command_text(payload: dict[str, object], raw: str) -> str:
    values: list[str] = []
    for key in ("command", "cmd", "tool_input", "arguments"):
        value = payload.get(key)
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, dict):
            for nested_key in ("command", "cmd", "script"):
                nested = value.get(nested_key)
                if isinstance(nested, str):
                    values.append(nested)
    if values:
        return "\n".join(values)
    return raw


def _matches(patterns: list[re.Pattern[str]], text: str) -> list[str]:
    return [pattern.pattern for pattern in patterns if pattern.search(text)]


def main() -> int:
    payload, raw = _read_payload()
    command = _command_text(payload, raw)
    findings = []
    blocking = False
    if _matches(DESTRUCTIVE_PATTERNS, command):
        blocking = True
        findings.append(
            {
                "kind": "destructive_command",
                "severity": "high",
                "blocking": True,
                "message": "Command appears destructive; require explicit approval and scoped target review.",
            }
        )
    if _matches(FORBIDDEN_PATH_PATTERNS, command):
        blocking = True
        findings.append(
            {
                "kind": "forbidden_path",
                "severity": "high",
                "blocking": True,
                "message": "Command references a path outside normal project ownership.",
            }
        )
    if _matches(SENSITIVE_WRITE_PATTERNS, command):
        blocking = True
        findings.append(
            {
                "kind": "secret_risk_write",
                "severity": "medium",
                "blocking": True,
                "message": "Command may write sensitive material; avoid storing credentials in project artifacts.",
            }
        )
    payload = {
        "hook": "pre_tool_use_policy",
        "decision": "block" if blocking else "observe",
        "input_bytes": len(raw.encode("utf-8")),
        "findings": findings,
        "notes": ["Respect sandbox boundaries and current file ownership."],
    }
    print(json.dumps(payload, sort_keys=True))
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
