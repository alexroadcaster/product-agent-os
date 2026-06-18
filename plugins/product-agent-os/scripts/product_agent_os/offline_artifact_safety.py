"""Shared safety helpers for generated offline Product-Agent OS views."""

from __future__ import annotations

import html
import json
import re
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction


EMBEDDED_JSON_BYTE_LIMIT = 12_000
GENERATED_VIEW_ONLY_TEXT = (
    "Generated review view only. It is not source of truth and cannot approve, apply, or prove work complete."
)
EXTERNAL_URL_PATTERN = re.compile(r"https?://", re.IGNORECASE)
SCRIPT_SRC_PATTERN = re.compile(r"<script\s+[^>]*\bsrc\s*=", re.IGNORECASE)


def prepare_offline_payload(
    payload: Any,
    *,
    max_json_bytes: int = EMBEDDED_JSON_BYTE_LIMIT,
) -> dict[str, Any]:
    """Return a redacted, external-URL-safe payload and bounded JSON strings."""

    redacted, redaction_summary = redact_payload(payload)
    safe_payload = _sanitize_external_urls(redacted)
    json_text = json.dumps(safe_payload, ensure_ascii=False, indent=2, sort_keys=True)
    byte_size = len(json_text.encode("utf-8"))
    if byte_size > max_json_bytes:
        preserved_sections = _preserved_trimmed_sections(safe_payload)
        safe_payload = {
            "schema_version": 1,
            "write_policy": "read_only",
            "status": "trimmed",
            "trimmed": True,
            "max_json_bytes": max_json_bytes,
            "original_json_bytes": byte_size,
            "summary": _payload_summary(safe_payload),
            **preserved_sections,
        }
        json_text = json.dumps(safe_payload, ensure_ascii=False, indent=2, sort_keys=True)
        byte_size = len(json_text.encode("utf-8"))
    return {
        "payload": safe_payload,
        "json": json_text,
        "json_for_html": json_for_html_text(json_text),
        "embedded_json_bytes": byte_size,
        "redaction_summary": redaction_summary,
    }


def escape_html(value: Any) -> str:
    """Escape text for offline HTML after neutralizing external URLs."""

    return html.escape(str(_sanitize_external_urls(value)), quote=True)


def json_for_html(payload: Any) -> str:
    """Serialize payload for embedding in an application/json script tag."""

    return prepare_offline_payload(payload)["json_for_html"]


def json_for_html_text(json_text: str) -> str:
    """Escape an existing JSON string for a non-executable script tag."""

    return (
        json_text.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("http://", "http:\\/\\/")
        .replace("https://", "https:\\/\\/")
    )


def validate_offline_artifact(
    *,
    html_text: str,
    embedded_json: str,
    payload: dict[str, Any] | None = None,
    max_json_bytes: int = EMBEDDED_JSON_BYTE_LIMIT,
) -> dict[str, Any]:
    """Validate generated offline HTML and embedded JSON safety properties."""

    errors: list[str] = []
    lower_html = html_text.lower()
    if not lower_html.startswith("<!doctype html>"):
        errors.append("html:doctype_missing")
    if '<meta name="viewport"' not in lower_html:
        errors.append("html:viewport_missing")
    if EXTERNAL_URL_PATTERN.search(html_text):
        errors.append("html:external_url_forbidden")
    if SCRIPT_SRC_PATTERN.search(html_text):
        errors.append("html:script_src_forbidden")
    if GENERATED_VIEW_ONLY_TEXT not in html_text:
        errors.append("html:generated_view_policy_missing")
    if len(embedded_json.encode("utf-8")) > max_json_bytes:
        errors.append("embedded_json:size_limit_exceeded")
    if payload is not None and payload.get("write_policy") not in {None, "read_only"}:
        errors.append("payload.write_policy:must_be_read_only")
    errors.extend(validate_redaction(html_text))
    errors.extend(validate_redaction(embedded_json))
    return {
        "ok": not errors,
        "checks": validation_checks(),
        "errors": _unique(errors),
    }


def validation_checks() -> list[str]:
    return [
        "offline html doctype present",
        "viewport meta present",
        "external urls absent",
        "external scripts absent",
        "embedded json escaped",
        "embedded json bounded",
        "generated view policy present",
        "redaction validated",
    ]


def _sanitize_external_urls(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _sanitize_external_urls(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_external_urls(item) for item in value]
    if isinstance(value, tuple):
        return [_sanitize_external_urls(item) for item in value]
    if isinstance(value, str):
        return EXTERNAL_URL_PATTERN.sub("[EXTERNAL_URL_REDACTED]", value)
    return value


def _payload_summary(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return {
            "top_level_keys": sorted(str(key) for key in payload)[:40],
            "top_level_key_count": len(payload),
        }
    if isinstance(payload, list):
        return {"item_count": len(payload)}
    return {"payload_type": type(payload).__name__}


def _preserved_trimmed_sections(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    preserved: dict[str, Any] = {}
    hygiene = payload.get("system_file_hygiene")
    if isinstance(hygiene, dict):
        file_statuses = hygiene.get("file_statuses")
        preserved["system_file_hygiene"] = {
            "status": str(hygiene.get("status") or "not_available"),
            "summary": hygiene.get("summary") if isinstance(hygiene.get("summary"), dict) else {},
            "file_statuses": _bounded_file_statuses(file_statuses),
            "source_policy": str(hygiene.get("source_policy") or "generated status summary is not source of truth"),
        }
    return preserved


def _bounded_file_statuses(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    allowed_keys = {
        "path",
        "class",
        "owner",
        "state",
        "severity",
        "finding_count",
        "age_days",
        "last_audit_at",
        "top_finding",
    }
    statuses: list[dict[str, Any]] = []
    for item in value[:8]:
        if not isinstance(item, dict):
            continue
        statuses.append({key: item[key] for key in sorted(allowed_keys) if key in item})
    return statuses


def _unique(items: list[str]) -> list[str]:
    return sorted(set(items))
