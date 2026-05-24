from __future__ import annotations

import re
from typing import Any


SECRET_ASSIGNMENT = re.compile(r"(?im)^\s*[A-Z_]*(?:SECRET|TOKEN|PASSWORD|KEY)[A-Z_]*\s*[=:]\s*[^\r\n]+")
WINDOWS_USER_PATH = re.compile(r"C:\\Users\\[^\s\\]+(?:\\[^\s]+)*", re.IGNORECASE)
PRIVATE_MARKERS = re.compile(r"(?i)(private customer data|raw private chat log|raw chat log)")


def redact_text(text: str) -> tuple[str, dict[str, object]]:
    categories: list[str] = []
    redacted = text

    redacted, secret_count = SECRET_ASSIGNMENT.subn("[REDACTED_SECRET_ASSIGNMENT]", redacted)
    if secret_count:
        categories.append("secret")

    redacted, path_count = WINDOWS_USER_PATH.subn("[REDACTED_LOCAL_PATH]", redacted)
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
    if SECRET_ASSIGNMENT.search(text):
        errors.append("redaction:secret_retained")
    if WINDOWS_USER_PATH.search(text):
        errors.append("redaction:absolute_path_retained")
    if PRIVATE_MARKERS.search(text):
        errors.append("redaction:private_data_retained")
    return errors
