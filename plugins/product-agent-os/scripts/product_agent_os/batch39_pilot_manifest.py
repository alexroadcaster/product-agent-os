from __future__ import annotations

from datetime import UTC, datetime
from pathlib import PurePosixPath
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


COMPLETION_SKEPTIC_VERDICTS = {
    "pass",
    "revise",
    "needs_more_context",
    "blocked_by_approval",
    "accepted_risk",
    "blocked",
    "not_run",
    "accepted_gap",
}
COMPLETION_SKEPTIC_FAILURE_CLASSES = {
    "false_pass_blocked",
    "false_rewrite_blocked",
    "fake_evidence_rejected",
    "missing_current_evidence",
    "generated_view_not_proof",
    "synthetic_only_boundary",
}
PROMOTION_BOUNDARIES = {
    "manual_only",
    "not_promoted",
    "manual_only_not_promoted",
    "synthetic_only_boundary",
    "owner_review_required",
}
PILOT_ARCHETYPES = {
    "docs_research",
    "code_check",
    "expected_block",
    "web_frontend",
    "backend_api",
    "ai_rag",
    "data_migration",
    "pr_review",
    "automation_release",
    "desktop_native",
    "plugin_skill",
}
NO_ACTION_BOUNDARY_VALUE = "not_performed"


PILOT_RUN_MANIFEST_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Batch 39 Pilot Run Manifest",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "slice",
        "generated_at",
        "pilot",
        "target",
        "source_inventory_ref",
        "approval_boundary",
        "execution_plan",
        "completion_skeptic",
        "redaction",
        "status",
        "manifest_digest",
    ],
    "properties": {
        "schema_version": {"const": "pilot_run_manifest_v1"},
        "batch": {"const": "B39"},
        "test_id": {"type": "string", "pattern": "^B39-TEST-M\\d{2}$"},
        "attempt_id": {"type": "string", "pattern": "^B39-TEST-M\\d{2}-A\\d{2}$"},
        "slice": {"type": "string", "pattern": "^B39-S\\d$"},
        "generated_at": {"type": "string"},
        "pilot": {
            "type": "object",
            "required": ["pilot_id", "archetype", "mode", "real_pilot_evidence"],
            "properties": {
                "pilot_id": {"type": "string"},
                "archetype": {"enum": sorted(PILOT_ARCHETYPES)},
                "mode": {"enum": ["schema_fixture", "synthetic_local", "real_project", "expected_block"]},
                "real_pilot_evidence": {"type": "boolean"},
            },
        },
        "target": {
            "type": "object",
            "required": ["target_ref", "target_kind", "mutation_allowed", "source_policy_status"],
            "properties": {
                "target_ref": {"type": "string"},
                "target_kind": {"enum": ["fixture", "local_workspace", "real_project", "none"]},
                "mutation_allowed": {"type": "boolean"},
                "source_policy_status": {"enum": ["not_applicable", "present", "blocked", "accepted_gap"]},
            },
        },
        "source_inventory_ref": {"type": "string"},
        "approval_boundary": {
            "type": "object",
            "required": [
                "target_workspace_mutation",
                "provider_or_api_calls",
                "browser_automation",
                "live_server",
                "cache_mutation",
                "external_actions",
                "git_actions",
                "automation_activation",
                "local_evidence_artifact_write",
            ],
        },
        "execution_plan": {
            "type": "object",
            "required": ["commands_planned", "checks_planned", "evidence_artifacts", "expected_outputs"],
        },
        "completion_skeptic": {
            "type": "object",
            "required": [
                "doubt_packet_ref",
                "verdict",
                "trigger",
                "failure_classes",
                "accepted_gap_refs",
                "scorecard_ref",
                "promotion_boundary",
            ],
        },
        "redaction": {
            "type": "object",
            "required": [
                "local_absolute_paths_allowed",
                "raw_private_logs_stored",
                "secrets_allowed",
                "redaction_report_ref",
            ],
        },
        "status": {"type": "object", "required": ["overall", "open_blockers"]},
        "manifest_digest": {"type": "string"},
    },
}


def build_pilot_run_manifest(
    *,
    test_id: str,
    attempt_id: str,
    slice_id: str,
    pilot_id: str,
    archetype: str,
    target_ref: str,
    source_inventory_ref: str,
    generated_at: str | None = None,
    commands_planned: list[str] | None = None,
    checks_planned: list[str] | None = None,
    evidence_artifacts: list[str] | None = None,
    expected_outputs: list[str] | None = None,
    target_kind: str = "fixture",
    mode: str = "schema_fixture",
    source_policy_status: str = "not_applicable",
) -> dict[str, Any]:
    """Build a redaction-safe Batch 39 pilot run manifest."""

    timestamp = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    manifest = {
        "schema_version": "pilot_run_manifest_v1",
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "slice": slice_id,
        "generated_at": timestamp,
        "pilot": {
            "pilot_id": pilot_id,
            "archetype": archetype,
            "mode": mode,
            "real_pilot_evidence": False,
        },
        "target": {
            "target_ref": _safe_ref(target_ref),
            "target_kind": target_kind,
            "mutation_allowed": False,
            "source_policy_status": source_policy_status,
        },
        "source_inventory_ref": _safe_ref(source_inventory_ref),
        "approval_boundary": _default_approval_boundary(),
        "execution_plan": {
            "commands_planned": list(commands_planned or []),
            "checks_planned": list(checks_planned or []),
            "evidence_artifacts": [_safe_ref(value) for value in (evidence_artifacts or [])],
            "expected_outputs": list(expected_outputs or ["pilot-run-manifest.json validates against schema"]),
        },
        "completion_skeptic": {
            "doubt_packet_ref": "none",
            "verdict": "not_run",
            "trigger": "not_applicable_schema_fixture",
            "failure_classes": [],
            "accepted_gap_refs": [],
            "scorecard_ref": "none",
            "promotion_boundary": "manual_only_not_promoted",
        },
        "redaction": {
            "local_absolute_paths_allowed": False,
            "raw_private_logs_stored": False,
            "secrets_allowed": False,
            "redaction_report_ref": "pending_B39_TEST_M05",
        },
        "status": _status(),
    }
    manifest["manifest_digest"] = content_digest(canonical_json(manifest))
    return manifest


def validate_pilot_run_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    for field in PILOT_RUN_MANIFEST_SCHEMA["required"]:
        if field not in manifest:
            errors.append(f"{field} is required")

    if manifest.get("schema_version") != "pilot_run_manifest_v1":
        errors.append("schema_version must be pilot_run_manifest_v1")
    if manifest.get("batch") != "B39":
        errors.append("batch must be B39")
    errors.extend(_validate_pilot(manifest.get("pilot")))
    errors.extend(_validate_target(manifest.get("target")))
    errors.extend(_validate_approval_boundary(manifest.get("approval_boundary")))
    errors.extend(_validate_execution_plan(manifest.get("execution_plan")))
    errors.extend(_validate_completion_skeptic(manifest.get("completion_skeptic")))
    errors.extend(_validate_redaction(manifest.get("redaction")))
    errors.extend(_validate_status(manifest.get("status")))

    if not isinstance(manifest.get("source_inventory_ref"), str) or not manifest.get("source_inventory_ref"):
        errors.append("source_inventory_ref must be a non-empty string")
    if not isinstance(manifest.get("manifest_digest"), str) or not manifest.get("manifest_digest", "").startswith("sha256:"):
        errors.append("manifest_digest must be a sha256 digest")
    if _contains_local_absolute_path(manifest):
        errors.append("local absolute path leaked")
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


def _status() -> dict[str, Any]:
    return {
        "overall": "ready_for_planned_pilot",
        "open_blockers": [],
        "next_test": "B39-TEST-M03",
    }


def _validate_pilot(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["pilot must be an object"]
    for field in ("pilot_id", "archetype", "mode"):
        if not isinstance(value.get(field), str) or not value.get(field):
            errors.append(f"pilot.{field} must be a non-empty string")
    if value.get("archetype") not in PILOT_ARCHETYPES:
        errors.append("pilot.archetype missing or invalid")
    if value.get("mode") not in {"schema_fixture", "synthetic_local", "real_project", "expected_block"}:
        errors.append("pilot.mode missing or invalid")
    if not isinstance(value.get("real_pilot_evidence"), bool):
        errors.append("pilot.real_pilot_evidence must be boolean")
    return errors


def _validate_target(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["target must be an object"]
    if not isinstance(value.get("target_ref"), str) or not value.get("target_ref"):
        errors.append("target.target_ref must be a non-empty string")
    if value.get("target_kind") not in {"fixture", "local_workspace", "real_project", "none"}:
        errors.append("target.target_kind missing or invalid")
    if value.get("mutation_allowed") is not False:
        errors.append("target.mutation_allowed must be false for B39-TEST-M02 schema fixture")
    if value.get("source_policy_status") not in {"not_applicable", "present", "blocked", "accepted_gap"}:
        errors.append("target.source_policy_status missing or invalid")
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


def _validate_execution_plan(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["execution_plan must be an object"]
    errors: list[str] = []
    for field in ("commands_planned", "checks_planned", "evidence_artifacts", "expected_outputs"):
        if not isinstance(value.get(field), list):
            errors.append(f"execution_plan.{field} must be list")
    return errors


def _validate_completion_skeptic(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["completion_skeptic must be an object"]
    errors: list[str] = []
    for field in PILOT_RUN_MANIFEST_SCHEMA["properties"]["completion_skeptic"]["required"]:
        if field not in value:
            errors.append(f"completion_skeptic.{field} is required")
    if value.get("verdict") not in COMPLETION_SKEPTIC_VERDICTS:
        errors.append("completion_skeptic.verdict missing or invalid")
    if value.get("promotion_boundary") not in PROMOTION_BOUNDARIES:
        errors.append("completion_skeptic.promotion_boundary missing or invalid")
    for field in ("failure_classes", "accepted_gap_refs"):
        if not isinstance(value.get(field), list):
            errors.append(f"completion_skeptic.{field} must be list")
    for failure_class in value.get("failure_classes", []):
        if failure_class not in COMPLETION_SKEPTIC_FAILURE_CLASSES:
            errors.append(f"completion_skeptic.failure_classes contains invalid value: {failure_class}")
    return errors


def _validate_redaction(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["redaction must be an object"]
    errors: list[str] = []
    for field in ("local_absolute_paths_allowed", "raw_private_logs_stored", "secrets_allowed"):
        if value.get(field) is not False:
            errors.append(f"redaction.{field} must be false")
    if not isinstance(value.get("redaction_report_ref"), str):
        errors.append("redaction.redaction_report_ref must be string")
    return errors


def _validate_status(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["status must be an object"]
    errors: list[str] = []
    if value.get("overall") not in {"ready_for_planned_pilot", "blocked", "needs_attention"}:
        errors.append("status.overall missing or invalid")
    if not isinstance(value.get("open_blockers"), list):
        errors.append("status.open_blockers must be list")
    return errors


def _safe_ref(value: str) -> str:
    normalized = str(PurePosixPath(value.replace("\\", "/")))
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
    "PILOT_RUN_MANIFEST_SCHEMA",
    "build_pilot_run_manifest",
    "validate_pilot_run_manifest",
]
