"""Shared sanitization helpers for generated project graph review surfaces."""

from __future__ import annotations

import re
from pathlib import PureWindowsPath
from typing import Any


EXTERNAL_URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
WINDOWS_LOCAL_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>]+")
POSIX_LOCAL_PATH_PATTERN = re.compile(r"(^|\s)/(Users|home|private|Volumes|mnt|tmp|var)/[^\s\"'<>]+")


def sanitize_graph_text(value: Any) -> str:
    """Neutralize script tags, external URLs and common local paths in generated views."""

    text = str(value or "")
    text = re.sub(r"</?script", "[SCRIPT_TAG_REDACTED]", text, flags=re.IGNORECASE)
    text = EXTERNAL_URL_PATTERN.sub("[EXTERNAL_URL_REDACTED]", text)
    text = WINDOWS_LOCAL_PATH_PATTERN.sub("[REDACTED_LOCAL_PATH]", text)
    text = POSIX_LOCAL_PATH_PATTERN.sub(" [REDACTED_LOCAL_PATH]", text)
    return text


def safe_relative_path_text(value: Any) -> str:
    """Return a normalized relative path, or blank when the value is unsafe for review JSON."""

    text = sanitize_graph_text(value).strip()
    normalized = text.replace("\\", "/")
    if not normalized:
        return ""
    if normalized.startswith(("/", "../", "http://", "https://", "[REDACTED", "[EXTERNAL", "[SCRIPT")):
        return ""
    if ":/" in normalized or normalized.startswith("~"):
        return ""
    windows_path = PureWindowsPath(text)
    if windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return ""
    if ".." in normalized.split("/"):
        return ""
    return normalized
