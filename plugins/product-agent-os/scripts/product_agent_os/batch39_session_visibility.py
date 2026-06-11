from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SESSION_VISIBILITY_SCHEMA_VERSION = "session_visibility_report_v1"
REQUIRED_OPERATIONS = ("install", "update", "uninstall", "session_visible")


def build_session_visibility_report(
    *,
    test_id: str,
    attempt_id: str,
    package_ref: str,
    events: list[dict[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    coverage = {operation: "missing" for operation in REQUIRED_OPERATIONS}
    safe_events = []
    for event in events:
        operation = str(event.get("operation", "")).strip()
        status = str(event.get("status", "")).strip() or "missing"
        artifact = _safe_ref(str(event.get("artifact", "")).strip())
        if operation in coverage:
            coverage[operation] = status
        safe_events.append({"operation": operation, "status": status, "artifact": artifact})
    report = {
        "schema_version": SESSION_VISIBILITY_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "package_ref": _safe_ref(package_ref),
        "events": safe_events,
        "coverage": coverage,
        "approval_boundary": {
            "cache_mutation": "not_performed",
            "external_actions": "not_performed",
            "git_actions": "not_performed",
            "automation_activation": "not_performed",
            "local_evidence_artifact_write": "allowed_workspace_output_only",
        },
    }
    report["verdict"] = "session_visibility_verified" if all(value == "observed" for value in coverage.values()) else "session_visibility_incomplete"
    report["report_digest"] = content_digest(canonical_json(report))
    return report


def validate_session_visibility_report(report: dict[str, Any]) -> list[str]:
    if not isinstance(report, dict):
        return ["session visibility report must be an object"]
    errors: list[str] = []
    if report.get("schema_version") != SESSION_VISIBILITY_SCHEMA_VERSION:
        errors.append(f"schema_version must be {SESSION_VISIBILITY_SCHEMA_VERSION}")
    if report.get("batch") != "B39":
        errors.append("batch must be B39")
    coverage = report.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("coverage must be an object")
        coverage = {}
    for operation in REQUIRED_OPERATIONS:
        if coverage.get(operation) != "observed":
            errors.append(f"missing required operation: {operation}")
    if report.get("verdict") not in {"session_visibility_verified", "session_visibility_incomplete"}:
        errors.append("verdict missing or invalid")
    if not str(report.get("report_digest", "")).startswith("sha256:"):
        errors.append("report_digest must be a sha256 digest")
    boundary = report.get("approval_boundary") if isinstance(report.get("approval_boundary"), dict) else {}
    if boundary.get("cache_mutation") != "not_performed":
        errors.append("approval_boundary.cache_mutation must be not_performed")
    return errors


def _safe_ref(value: str) -> str:
    normalized = value.replace("\\", "/")
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] == "/":
        return "[REDACTED_LOCAL_PATH]"
    return normalized


__all__ = [
    "REQUIRED_OPERATIONS",
    "build_session_visibility_report",
    "validate_session_visibility_report",
]
