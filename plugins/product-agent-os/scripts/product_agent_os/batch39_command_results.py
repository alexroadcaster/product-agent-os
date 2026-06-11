from __future__ import annotations

import json
from typing import Any

from product_agent_os.stage_manifest import content_digest


COMMAND_RESULT_EVIDENCE_CLASSES = {
    "current_command",
    "user_claimed",
    "fake_evidence",
    "generated_view",
    "stale_evidence",
}
TRUST_LEVEL_BY_CLASS = {
    "current_command": "current_run",
    "user_claimed": "unverified_claim",
    "fake_evidence": "rejected",
    "generated_view": "orientation_only_not_proof",
    "stale_evidence": "stale_not_current",
}
NO_ACTION_BOUNDARY_VALUE = "not_performed"


def build_command_result_entry(
    *,
    test_id: str,
    attempt_id: str,
    manifest_ref: str,
    command_id: str,
    command: str,
    exit_code: int | None,
    started_at: str,
    finished_at: str,
    evidence_class: str,
    evidence_source: str,
    stdout: str = "",
    stderr: str = "",
) -> dict[str, Any]:
    """Build one redacted command-results.jsonl entry for Batch 39."""

    evidence_class = evidence_class.strip()
    status = _status(exit_code=exit_code, evidence_class=evidence_class)
    entry = {
        "schema_version": "command_result_v1",
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "manifest_ref": _safe_ref(manifest_ref),
        "command_id": command_id,
        "command": command,
        "started_at": started_at,
        "finished_at": finished_at,
        "exit_code": exit_code,
        "status": status,
        "evidence": {
            "class": evidence_class,
            "source": evidence_source,
            "trust_level": TRUST_LEVEL_BY_CLASS.get(evidence_class, "invalid"),
            "current_command_proof": evidence_class == "current_command" and exit_code is not None,
        },
        "output": {
            "stdout_digest": content_digest(stdout),
            "stderr_digest": content_digest(stderr),
            "stdout_line_count": _line_count(stdout),
            "stderr_line_count": _line_count(stderr),
        },
        "redaction": {
            "raw_stdout_stored": False,
            "raw_stderr_stored": False,
            "local_absolute_paths_allowed": False,
            "secrets_allowed": False,
        },
        "approval_boundary": _default_approval_boundary(),
    }
    entry["entry_digest"] = content_digest(json.dumps(entry, ensure_ascii=False, sort_keys=True))
    return entry


def parse_command_results_jsonl(text: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"invalid JSONL at line {line_number}: entry must be object")
        entries.append(payload)
    return entries


def validate_command_results_jsonl(text: str) -> list[str]:
    try:
        entries = parse_command_results_jsonl(text)
    except ValueError as exc:
        return [str(exc)]
    errors: list[str] = []
    seen_command_ids: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        for error in validate_command_result_entry(entry):
            errors.append(f"line {index}: {error}")
        command_id = str(entry.get("command_id", ""))
        if command_id in seen_command_ids:
            errors.append(f"line {index}: duplicate command_id: {command_id}")
        seen_command_ids.add(command_id)
    if not entries:
        errors.append("command results jsonl must contain at least one entry")
    return errors


def validate_command_result_entry(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "manifest_ref",
        "command_id",
        "command",
        "started_at",
        "finished_at",
        "exit_code",
        "status",
        "evidence",
        "output",
        "redaction",
        "approval_boundary",
        "entry_digest",
    ]
    for field in required:
        if field not in entry:
            errors.append(f"{field} is required")
    if entry.get("schema_version") != "command_result_v1":
        errors.append("schema_version must be command_result_v1")
    if entry.get("batch") != "B39":
        errors.append("batch must be B39")
    for field in ("test_id", "attempt_id", "manifest_ref", "command_id", "command", "started_at", "finished_at"):
        if not isinstance(entry.get(field), str) or not entry.get(field):
            errors.append(f"{field} must be a non-empty string")
    if not (isinstance(entry.get("exit_code"), int) or entry.get("exit_code") is None):
        errors.append("exit_code must be integer or null")
    if entry.get("status") not in {"passed", "failed", "not_proof", "rejected"}:
        errors.append("status missing or invalid")
    errors.extend(_validate_evidence(entry.get("evidence")))
    errors.extend(_validate_output(entry.get("output")))
    errors.extend(_validate_redaction(entry.get("redaction")))
    errors.extend(_validate_approval_boundary(entry.get("approval_boundary")))
    if not isinstance(entry.get("entry_digest"), str) or not entry.get("entry_digest", "").startswith("sha256:"):
        errors.append("entry_digest must be a sha256 digest")
    if _contains_local_absolute_path(entry):
        errors.append("local absolute path leaked")
    return errors


def _validate_evidence(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["evidence must be an object"]
    errors: list[str] = []
    evidence_class = value.get("class")
    if evidence_class not in COMMAND_RESULT_EVIDENCE_CLASSES:
        errors.append("evidence.class missing or invalid")
    if not isinstance(value.get("source"), str) or not value.get("source"):
        errors.append("evidence.source must be a non-empty string")
    if value.get("trust_level") != TRUST_LEVEL_BY_CLASS.get(evidence_class):
        errors.append("evidence.trust_level missing or invalid")
    if not isinstance(value.get("current_command_proof"), bool):
        errors.append("evidence.current_command_proof must be boolean")
    if evidence_class == "fake_evidence":
        errors.append("fake_evidence cannot satisfy command proof")
    return errors


def _validate_output(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["output must be an object"]
    errors: list[str] = []
    for field in ("stdout_digest", "stderr_digest"):
        if not isinstance(value.get(field), str) or not value.get(field, "").startswith("sha256:"):
            errors.append(f"output.{field} must be a sha256 digest")
    for field in ("stdout_line_count", "stderr_line_count"):
        if not isinstance(value.get(field), int):
            errors.append(f"output.{field} must be integer")
    return errors


def _validate_redaction(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["redaction must be an object"]
    errors: list[str] = []
    for field in ("raw_stdout_stored", "raw_stderr_stored", "local_absolute_paths_allowed", "secrets_allowed"):
        if value.get(field) is not False:
            errors.append(f"redaction.{field} must be false")
    return errors


def _validate_approval_boundary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["approval_boundary must be an object"]
    errors: list[str] = []
    expected = _default_approval_boundary()
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            errors.append(f"approval_boundary.{field} must be {expected_value}")
    return errors


def _default_approval_boundary() -> dict[str, str]:
    return {
        "target_workspace_mutation": NO_ACTION_BOUNDARY_VALUE,
        "provider_or_api_calls": NO_ACTION_BOUNDARY_VALUE,
        "browser_automation": NO_ACTION_BOUNDARY_VALUE,
        "live_server": NO_ACTION_BOUNDARY_VALUE,
        "cache_mutation": NO_ACTION_BOUNDARY_VALUE,
        "external_actions": NO_ACTION_BOUNDARY_VALUE,
        "git_actions": NO_ACTION_BOUNDARY_VALUE,
        "automation_activation": NO_ACTION_BOUNDARY_VALUE,
        "local_evidence_artifact_write": "allowed_workspace_output_only",
    }


def _status(*, exit_code: int | None, evidence_class: str) -> str:
    if evidence_class == "fake_evidence":
        return "rejected"
    if evidence_class != "current_command":
        return "not_proof"
    if exit_code == 0:
        return "passed"
    return "failed"


def _line_count(value: str) -> int:
    if not value:
        return 0
    return len(value.splitlines())


def _safe_ref(value: str) -> str:
    normalized = value.replace("\\", "/")
    if _looks_like_absolute_path(normalized):
        return "redacted_absolute_path"
    return normalized


def _contains_local_absolute_path(payload: Any) -> bool:
    if isinstance(payload, str):
        return _looks_like_absolute_path(payload)
    if isinstance(payload, dict):
        return any(_contains_local_absolute_path(key) or _contains_local_absolute_path(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(_contains_local_absolute_path(item) for item in payload)
    return False


def _looks_like_absolute_path(value: str) -> bool:
    normalized = value.strip()
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] in {"\\", "/"} and normalized[0].isalpha():
        return True
    if normalized.startswith("\\\\") or normalized.startswith("//"):
        return True
    if normalized.startswith("/"):
        return True
    return False


__all__ = [
    "COMMAND_RESULT_EVIDENCE_CLASSES",
    "build_command_result_entry",
    "parse_command_results_jsonl",
    "validate_command_result_entry",
    "validate_command_results_jsonl",
]
