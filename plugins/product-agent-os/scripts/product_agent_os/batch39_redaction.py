from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from codex_runtime_runner.redaction import redact_payload, validate_redaction
from product_agent_os.stage_manifest import canonical_json, content_digest


REDACTION_REPORT_SCHEMA_VERSION = "redaction_report_v1"


def build_redaction_report(
    *,
    test_id: str,
    attempt_id: str,
    artifact_refs: list[str],
    sample_payload: dict[str, Any],
    generated_at: str | None = None,
) -> dict[str, Any]:
    redacted_raw_payload, redaction_summary = redact_payload(sample_payload)
    redacted_payload = _strip_raw_fields(redacted_raw_payload)
    redacted_refs, ref_summary = redact_payload([_safe_ref(ref) for ref in artifact_refs])
    categories = set(str(item) for item in redaction_summary.get("categories", []))
    categories.update(str(item) for item in ref_summary.get("categories", []))
    report = {
        "schema_version": REDACTION_REPORT_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "artifact_refs": redacted_refs,
        "sample_digest": content_digest(canonical_json(sample_payload)),
        "redacted_sample": redacted_payload,
        "redaction_summary": {
            "count": int(redaction_summary.get("count", 0)) + int(ref_summary.get("count", 0)),
            "categories": sorted(categories),
        },
        "policy": {
            "local_absolute_paths_allowed": False,
            "raw_file_bodies_stored": False,
            "raw_private_logs_stored": False,
            "secrets_allowed": False,
        },
        "approval_boundary": _default_approval_boundary(),
    }
    report["verdict"] = _verdict(report)
    report["report_digest"] = content_digest(canonical_json(report))
    return report


def validate_redaction_report(report: dict[str, Any]) -> list[str]:
    if not isinstance(report, dict):
        return ["redaction report must be an object"]
    errors: list[str] = []
    for field in [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "generated_at",
        "artifact_refs",
        "sample_digest",
        "redacted_sample",
        "redaction_summary",
        "policy",
        "approval_boundary",
        "verdict",
        "report_digest",
    ]:
        if field not in report:
            errors.append(f"{field} is required")
    if report.get("schema_version") != REDACTION_REPORT_SCHEMA_VERSION:
        errors.append(f"schema_version must be {REDACTION_REPORT_SCHEMA_VERSION}")
    if report.get("batch") != "B39":
        errors.append("batch must be B39")
    for field in ("test_id", "attempt_id", "generated_at", "sample_digest", "report_digest"):
        if not isinstance(report.get(field), str) or not report.get(field):
            errors.append(f"{field} must be a non-empty string")
    if not str(report.get("sample_digest", "")).startswith("sha256:"):
        errors.append("sample_digest must be a sha256 digest")
    if not str(report.get("report_digest", "")).startswith("sha256:"):
        errors.append("report_digest must be a sha256 digest")
    if not isinstance(report.get("artifact_refs"), list):
        errors.append("artifact_refs must be list")
    errors.extend(_validate_summary(report.get("redaction_summary")))
    errors.extend(_validate_policy(report.get("policy")))
    errors.extend(_validate_approval_boundary(report.get("approval_boundary")))
    encoded = json.dumps(report, ensure_ascii=False, sort_keys=True)
    errors.extend(validate_redaction(encoded))
    if '"raw_body"' in encoded or '"raw_private_log"' in encoded or '"raw_private_logs"' in encoded:
        errors.append("raw content field retained")
    if report.get("verdict") != _verdict(report):
        errors.append("verdict does not match redaction policy")
    return errors


def _strip_raw_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_raw_fields(item)
            for key, item in value.items()
            if key not in {"raw_body", "raw_private_log", "raw_private_logs", "raw_chat_log", "raw_source"}
        }
    if isinstance(value, list):
        return [_strip_raw_fields(item) for item in value]
    return value


def _validate_summary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["redaction_summary must be an object"]
    errors: list[str] = []
    if not isinstance(value.get("count"), int):
        errors.append("redaction_summary.count must be integer")
    if not isinstance(value.get("categories"), list):
        errors.append("redaction_summary.categories must be list")
    return errors


def _validate_policy(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["policy must be an object"]
    errors: list[str] = []
    for field in ("local_absolute_paths_allowed", "raw_file_bodies_stored", "raw_private_logs_stored", "secrets_allowed"):
        if value.get(field) is not False:
            errors.append(f"policy.{field} must be false")
    return errors


def _validate_approval_boundary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["approval_boundary must be an object"]
    errors: list[str] = []
    for field, expected in _default_approval_boundary().items():
        if value.get(field) != expected:
            errors.append(f"approval_boundary.{field} must be {expected}")
    return errors


def _default_approval_boundary() -> dict[str, str]:
    return {
        "provider_or_api_calls": "not_performed",
        "browser_automation": "not_performed",
        "live_server": "not_performed",
        "cache_mutation": "not_performed",
        "external_actions": "not_performed",
        "git_actions": "not_performed",
        "automation_activation": "not_performed",
        "local_evidence_artifact_write": "allowed_workspace_output_only",
    }


def _safe_ref(value: str) -> str:
    text = str(value).replace("\\", "/")
    if len(text) >= 3 and text[1] == ":" and text[2] == "/":
        return "[REDACTED_LOCAL_PATH]"
    if text.startswith(("/", "//")):
        return "[REDACTED_LOCAL_PATH]"
    return text


def _verdict(report: dict[str, Any]) -> str:
    policy = report.get("policy") if isinstance(report.get("policy"), dict) else {}
    if any(value is not False for value in policy.values()):
        return "blocked_redaction_policy"
    if validate_redaction(json.dumps(report, ensure_ascii=False, sort_keys=True)):
        return "blocked_redaction_leak"
    return "passed_redacted_local_paths"


__all__ = [
    "REDACTION_REPORT_SCHEMA_VERSION",
    "build_redaction_report",
    "validate_redaction_report",
]
