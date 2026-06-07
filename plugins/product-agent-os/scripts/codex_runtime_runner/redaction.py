from __future__ import annotations

import re
from typing import Any


SECRET_ASSIGNMENT = re.compile(r"(?im)^\s*[A-Z_]*(?:SECRET|TOKEN|PASSWORD|KEY)[A-Z_]*\s*[=:]\s*[^\r\n]+")
SECRET_VALUE = re.compile(r"(?i)\b(?:sk|rk|sess|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9][A-Za-z0-9._-]{5,}")
WINDOWS_USER_PATH = re.compile(r"C:\\Users\\[^\s\\]+(?:\\[^\s]+)*", re.IGNORECASE)
WINDOWS_ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z]:[\\/]+[^\s<>\"'`|]+|\\\\[^\\/\s<>\"'`|]+[\\/][^\s<>\"'`|]+)",
    re.IGNORECASE,
)
UNIX_HOME_PATH = re.compile(r"(?<![A-Za-z0-9_])/(?:Users|home)/[^\s<>\"'`]+")
PRIVATE_MARKERS = re.compile(
    r"(?i)(private customer data|raw private chat log|raw chat log|payment data|raw pii|raw personally identifiable information)"
)
LOCAL_PATH_PATTERNS = (WINDOWS_USER_PATH, WINDOWS_ABSOLUTE_PATH, UNIX_HOME_PATH)


def redact_text(text: str) -> tuple[str, dict[str, object]]:
    categories: list[str] = []
    redacted = text

    redacted, secret_count = SECRET_ASSIGNMENT.subn("[REDACTED_SECRET_ASSIGNMENT]", redacted)
    redacted, secret_value_count = SECRET_VALUE.subn("[REDACTED_SECRET_VALUE]", redacted)
    secret_count += secret_value_count
    if secret_count:
        categories.append("secret")

    path_count = 0
    for pattern in LOCAL_PATH_PATTERNS:
        redacted, pattern_count = pattern.subn("[REDACTED_LOCAL_PATH]", redacted)
        path_count += pattern_count
    if path_count:
        categories.append("absolute_path")

    redacted, private_count = PRIVATE_MARKERS.subn("[REDACTED_PRIVATE_DATA]", redacted)
    if private_count:
        categories.append("private_data")

    return redacted, {
        "count": secret_count + path_count + private_count,
        "categories": sorted(set(categories)),
    }


def redact_payload(payload: Any) -> tuple[Any, dict[str, object]]:
    categories: set[str] = set()
    count = 0

    def visit(value: Any) -> Any:
        nonlocal count
        if isinstance(value, str):
            redacted, report = redact_text(value)
            count += int(report["count"])
            categories.update(str(item) for item in report["categories"])
            return redacted
        if isinstance(value, list):
            return [visit(item) for item in value]
        if isinstance(value, dict):
            return {key: visit(item) for key, item in value.items()}
        return value

    return visit(payload), {"count": count, "categories": sorted(categories)}


def validate_redaction(text: str) -> list[str]:
    errors: list[str] = []
    if SECRET_ASSIGNMENT.search(text) or SECRET_VALUE.search(text):
        errors.append("redaction:secret_retained")
    if any(pattern.search(text) for pattern in LOCAL_PATH_PATTERNS):
        errors.append("redaction:absolute_path_retained")
    if PRIVATE_MARKERS.search(text):
        errors.append("redaction:private_data_retained")
    return errors
