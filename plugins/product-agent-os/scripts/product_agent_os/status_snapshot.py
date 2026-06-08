"""Read-only project status snapshot builder for Product-Agent OS."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from codex_runtime_runner.redaction import redact_payload


DEFAULT_EVIDENCE_MAX_AGE_DAYS = 14
_SUCCESS_WORDS = ("tests pass", "checks passed")
MAX_METRICS_REPORT_REFS = 4
MAX_METRICS_UPDATE_CANDIDATES = 5
MAX_PROJECT_GRAPH_REFS = 4
MAX_PROJECT_GRAPH_GAPS = 5
MAX_PROJECT_GRAPH_UNSUPPORTED_LANGUAGES = 8
MAX_SYSTEM_FILE_STATUSES = 50
TASK_MATRIX_PROJECTION_DECISION = {
    "status": "deferred_in_b37",
    "state_projection": "not_projected",
    "source_policy": "task matrix state is not projected into status snapshot/dashboard in B37",
    "future_projection_policy": (
        "future projection must be bounded read-only generated orientation evidence, "
        "never source of truth or completion evidence"
    ),
}


def build_status_snapshot(
    *,
    runtime_result: dict[str, Any] | None = None,
    discovery_result: dict[str, Any] | None = None,
    renderer_result: dict[str, Any] | None = None,
    stage_manifest: dict[str, Any] | None = None,
    question_ledger: dict[str, Any] | None = None,
    system_file_hygiene_audit: dict[str, Any] | None = None,
    generated_at: str,
    evidence_max_age_days: int = DEFAULT_EVIDENCE_MAX_AGE_DAYS,
) -> dict[str, Any]:
    """Build a JSON-serializable read-only status snapshot from existing packets."""

    runtime = runtime_result if isinstance(runtime_result, dict) else {}
    discovery = discovery_result if isinstance(discovery_result, dict) else {}
    route = runtime.get("route_packet") if isinstance(runtime.get("route_packet"), dict) else {}
    usage_mode = _usage_mode(route, discovery)
    question_summary = _question_summary(route, discovery)
    methodology_packet = route.get("methodology_packet") if isinstance(route.get("methodology_packet"), dict) else {}
    project_graph_status = route.get("project_graph_status") if isinstance(route.get("project_graph_status"), dict) else {}
    evidence_summary = _evidence_summary(runtime, generated_at, evidence_max_age_days)
    readiness_summary = _readiness_summary(runtime, usage_mode, evidence_summary, methodology_packet, project_graph_status)

    snapshot = {
        "schema_version": 1,
        "write_policy": "read_only",
        "generated_at": generated_at,
        "workspace": _workspace(runtime, discovery),
        "lifecycle_state": _string(runtime.get("lifecycle_state") or discovery.get("lifecycle_state")),
        "usage_mode": usage_mode,
        "question_summary": question_summary,
        "readiness_summary": readiness_summary,
        "evidence_summary": evidence_summary,
        "next_safe_action": _next_safe_action(route, methodology_packet),
        "dashboard_policy": {
            "write_policy": "read_only",
            "source_of_truth": "underlying_artifacts",
            "success_claim_policy": "never from dashboard alone",
            "external_assets": "forbidden",
        },
        "renderer_file_count": _renderer_file_count(renderer_result),
        "staged_artifacts": _staged_artifacts(renderer_result),
        "manifest_digests": _manifest_digests(stage_manifest),
        "source_artifact_ledger": _safe_list(methodology_packet.get("source_artifact_ledger")),
        "semantic_evidence_sufficiency": (
            methodology_packet.get("semantic_evidence_sufficiency")
            if isinstance(methodology_packet.get("semantic_evidence_sufficiency"), dict)
            else {}
        ),
        "project_graph_summary": _project_graph_summary(project_graph_status),
        "agent_skill_metrics_loop": _agent_skill_metrics_loop_summary(route, discovery),
        "system_file_hygiene": _system_file_hygiene_summary(system_file_hygiene_audit),
        "projection_decisions": {
            "task_matrix_state": dict(TASK_MATRIX_PROJECTION_DECISION),
        },
        "question_ledger_summary": (
            question_ledger.get("summary") if isinstance(question_ledger, dict) and isinstance(question_ledger.get("summary"), dict) else {}
        ),
        "question_ledger_artifact_updates": _safe_list(
            question_ledger.get("artifact_updates") if isinstance(question_ledger, dict) else []
        ),
        "approval_summary": {
            "status": _string(runtime.get("approval_status") or "not_available"),
            "requirements": _safe_list(route.get("approval_requirements")),
        },
    }
    return _redacted_snapshot(snapshot)


def _usage_mode(route: dict[str, Any], discovery: dict[str, Any]) -> dict[str, Any]:
    value = route.get("usage_mode") if isinstance(route.get("usage_mode"), dict) else discovery.get("usage_mode")
    packet = value if isinstance(value, dict) else {}
    primary = _string(packet.get("primary") or "unknown")
    return {
        "primary": primary,
        "confidence": _string(packet.get("confidence") or "unknown"),
        "inspection_only": primary in {"inspection_only", "docs_only"},
        "minimum_artifacts": _safe_list(packet.get("minimum_artifacts")),
    }


def _question_summary(route: dict[str, Any], discovery: dict[str, Any]) -> dict[str, Any]:
    queue = route.get("question_queue") if isinstance(route.get("question_queue"), dict) else discovery.get("question_queue")
    if not isinstance(queue, dict):
        queue = {}
    summary = queue.get("summary") if isinstance(queue.get("summary"), dict) else {}
    first_response = route.get("first_response_contract") if isinstance(route.get("first_response_contract"), dict) else {}
    counts = first_response.get("question_counts") if isinstance(first_response.get("question_counts"), dict) else summary
    return {
        "total": _int(counts.get("total")),
        "blocking": _int(counts.get("blocking")),
        "recommended": _int(counts.get("recommended")),
        "optional": _int(counts.get("optional")),
        "remaining": _int(counts.get("remaining")),
        "next_blocking_question": queue.get("next_blocking_question"),
        "first_response_summary": _safe_list(first_response.get("question_summary")),
    }


def _evidence_summary(
    runtime: dict[str, Any],
    generated_at: str,
    evidence_max_age_days: int,
) -> dict[str, Any]:
    evidence = runtime.get("verification_evidence")
    items = evidence if isinstance(evidence, list) else []
    freshness = "missing"
    stale_items = 0
    if items:
        freshness = "current"
        generated = _parse_datetime(generated_at)
        for item in items:
            recorded_at = _evidence_recorded_at(item)
            if generated is not None and recorded_at is not None:
                if (generated - recorded_at).days > evidence_max_age_days:
                    stale_items += 1
        if stale_items:
            freshness = "stale"
    return {
        "freshness": freshness,
        "evidence_count": len(items),
        "stale_count": stale_items,
        "max_age_days": evidence_max_age_days,
    }


def _readiness_summary(
    runtime: dict[str, Any],
    usage_mode: dict[str, Any],
    evidence_summary: dict[str, Any],
    methodology_packet: dict[str, Any],
    project_graph_status: dict[str, Any],
) -> dict[str, Any]:
    warnings: list[str] = []
    runtime_status = _string(runtime.get("status") or "unknown")
    status = runtime_status
    if usage_mode.get("inspection_only"):
        status = "inspection_only"
        warnings.append("inspection-only evidence cannot prove completion")
    if evidence_summary.get("freshness") == "stale":
        warnings.append("stale evidence")
    if evidence_summary.get("freshness") == "missing" and runtime_status == "completed":
        warnings.append("completion status lacks current verification evidence")
    if methodology_packet.get("status") == "present_unverified":
        warnings.append("methodology evidence is present_unverified")
    graph_status = _string(project_graph_status.get("status"))
    if graph_status in {"stale", "ambiguous", "unsupported"}:
        warnings.append(f"{graph_status} project graph")
    return {
        "status": status,
        "runtime_status": runtime_status,
        "success_claim": "not_claimed",
        "warnings": _unique(warnings),
    }


def _next_safe_action(route: dict[str, Any], methodology_packet: dict[str, Any]) -> str:
    first_response = route.get("first_response_contract") if isinstance(route.get("first_response_contract"), dict) else {}
    return (
        _string(first_response.get("safe_next_action"))
        or _string(methodology_packet.get("safe_next_action"))
        or _string(route.get("next_action"))
        or "Review status snapshot and continue only from underlying artifacts."
    )


def _agent_skill_metrics_loop_summary(route: dict[str, Any], discovery: dict[str, Any]) -> dict[str, Any]:
    packet = route.get("agent_skill_metrics_loop")
    if not isinstance(packet, dict):
        packet = discovery.get("agent_skill_metrics_loop") if isinstance(discovery.get("agent_skill_metrics_loop"), dict) else {}
    applicability = discovery.get("methodology_applicability") if isinstance(discovery.get("methodology_applicability"), dict) else {}
    readiness = applicability.get("agent_skill_metrics_loop") if isinstance(applicability.get("agent_skill_metrics_loop"), dict) else {}
    summary = packet.get("summary") if isinstance(packet.get("summary"), dict) else {}
    update_summary = (
        packet.get("update_candidate_summary")
        if isinstance(packet.get("update_candidate_summary"), dict)
        else {}
    )
    top_candidates = _safe_list(update_summary.get("top_candidates"))[:MAX_METRICS_UPDATE_CANDIDATES]
    return {
        "status": _string(packet.get("status") or readiness.get("status") or "not_available"),
        "summary": {
            "target_count": _int(summary.get("target_count")),
            "overall_status": _string(summary.get("overall_status")),
            "cadence_level": _string(summary.get("cadence_level") or _nested(packet, "cadence", "level")),
        },
        "report_refs": _safe_metrics_report_refs(packet.get("report_refs")),
        "update_candidate_summary": {
            "candidate_count": _int(update_summary.get("candidate_count")),
            "top_candidates": top_candidates,
        },
        "source_policy": "generated summaries are not source of truth",
        "approval_boundary": "owner review required before modernization or automation activation",
        "readiness_reason": _string(readiness.get("reason")),
    }


def _project_graph_summary(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "counts": {"nodes": 0, "edges": 0, "observations": 0, "omitted_nodes": 0},
            "unsupported_languages": [],
            "artifact_refs": [],
            "top_gaps": [],
            "source_policy": "generated graph is not source of truth",
            "safe_next_action": "Read source files before graph-backed claims.",
        }
    counts = packet.get("counts") if isinstance(packet.get("counts"), dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "freshness": packet.get("freshness") if isinstance(packet.get("freshness"), dict) else {},
        "counts": {
            "nodes": _int(counts.get("nodes")),
            "edges": _int(counts.get("edges")),
            "observations": _int(counts.get("observations")),
            "omitted_nodes": _int(counts.get("omitted_nodes")),
        },
        "unsupported_languages": _safe_project_graph_unsupported_languages(packet.get("unsupported_languages")),
        "artifact_refs": _safe_project_graph_refs(packet.get("artifact_refs")),
        "top_gaps": _safe_project_graph_gaps(packet.get("top_gaps")),
        "source_policy": "generated graph is not source of truth",
        "safe_next_action": _string(packet.get("safe_next_action") or "Read source files before graph-backed claims."),
    }


def _system_file_hygiene_summary(packet: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "audit_trigger": "",
            "last_audit_at": "",
            "summary": {"files_scanned": 0, "warnings": 0, "errors": 0, "active_schedule_markers": 0},
            "file_statuses": [],
            "source_policy": "system file hygiene projection is generated status evidence, not source of truth",
            "approval_boundary": "owner_approval_required_for_writes",
        }
    summary = packet.get("summary") if isinstance(packet.get("summary"), dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "audit_trigger": _string(packet.get("audit_trigger")),
        "last_audit_at": _string(packet.get("last_audit_at")),
        "write_policy": _string(packet.get("write_policy") or "read_only"),
        "schedule_status": _string(packet.get("schedule_status") or "not_created"),
        "summary": {
            "files_scanned": _int(summary.get("files_scanned")),
            "warnings": _int(summary.get("warnings")),
            "errors": _int(summary.get("errors")),
            "active_schedule_markers": _int(summary.get("active_schedule_markers")),
        },
        "file_statuses": _safe_system_file_statuses(packet.get("file_statuses")),
        "source_policy": "system file hygiene projection is generated status evidence, not source of truth",
        "approval_boundary": _string(summary.get("approval_boundary") or "owner_approval_required_for_writes"),
    }


def _safe_system_file_statuses(value: Any) -> list[dict[str, Any]]:
    statuses: list[dict[str, Any]] = []
    if not isinstance(value, list):
        return statuses
    for item in value[:MAX_SYSTEM_FILE_STATUSES]:
        if not isinstance(item, dict):
            continue
        path = _string(item.get("path"))
        if not _safe_project_graph_relative_path(path):
            continue
        statuses.append(
            {
                "path": path,
                "class": _string(item.get("class")),
                "owner": _string(item.get("owner")),
                "state": _string(item.get("state")),
                "severity": _string(item.get("severity")),
                "finding_count": _int(item.get("finding_count")),
                "size": _int(item.get("size")),
                "line_count": _int(item.get("line_count")),
                "mtime_utc": _string(item.get("mtime_utc")),
                "age_days": _int(item.get("age_days")),
                "content_digest": _string(item.get("content_digest")),
                "last_audit_at": _string(item.get("last_audit_at")),
                "top_finding": _string(item.get("top_finding") or "none"),
            }
        )
    return statuses


def _safe_project_graph_refs(value: Any) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if not isinstance(value, list):
        return refs
    for item in value[:MAX_PROJECT_GRAPH_REFS]:
        if not isinstance(item, dict):
            continue
        kind = _string(item.get("kind") or "staged_artifact")
        path = _string(item.get("path"))
        if kind == "external_ref" or path.startswith(("http://", "https://")) or not _safe_project_graph_relative_path(path):
            continue
        if not path:
            continue
        refs.append(
            {
                "kind": kind,
                "path": path,
                "digest": _string(item.get("digest")),
            }
        )
    return refs


def _safe_project_graph_unsupported_languages(value: Any) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if not isinstance(value, list):
        return items
    for item in value[:MAX_PROJECT_GRAPH_UNSUPPORTED_LANGUAGES]:
        if not isinstance(item, dict):
            continue
        items.append(
            {
                "language": _string(item.get("language")),
                "file_count": _int(item.get("file_count")),
                "status": _string(item.get("status")),
            }
        )
    return items


def _safe_project_graph_relative_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if not normalized:
        return False
    if normalized.startswith(("/", "../", "~")):
        return False
    if ":/" in normalized:
        return False
    return ".." not in normalized.split("/")


def _safe_project_graph_gaps(value: Any) -> list[dict[str, str]]:
    gaps: list[dict[str, str]] = []
    if not isinstance(value, list):
        return gaps
    for item in value[:MAX_PROJECT_GRAPH_GAPS]:
        if not isinstance(item, dict):
            continue
        gaps.append(
            {
                "id": _string(item.get("id")),
                "severity": _string(item.get("severity")),
                "safe_next_action": _string(item.get("safe_next_action")),
            }
        )
    return gaps


def _safe_metrics_report_refs(value: Any) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if not isinstance(value, list):
        return refs
    for item in value[:MAX_METRICS_REPORT_REFS]:
        if not isinstance(item, dict):
            continue
        kind = _string(item.get("kind") or "staged_artifact")
        path = _string(item.get("path"))
        if kind == "external_ref" or path.startswith(("http://", "https://")):
            continue
        if not path:
            continue
        refs.append(
            {
                "kind": kind,
                "path": path,
                "digest": _string(item.get("digest")),
            }
        )
    return refs


def _nested(packet: dict[str, Any], *keys: str) -> Any:
    current: Any = packet
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _renderer_file_count(renderer_result: dict[str, Any] | None) -> int:
    if not isinstance(renderer_result, dict):
        return 0
    rendered = renderer_result.get("rendered_artifacts")
    if not isinstance(rendered, dict):
        return 0
    files = rendered.get("files")
    return len(files) if isinstance(files, list) else 0


def _staged_artifacts(renderer_result: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(renderer_result, dict):
        return {"mode": "not_available", "targets": [], "validation_ok": False}
    rendered = renderer_result.get("rendered_artifacts")
    if not isinstance(rendered, dict):
        return {"mode": "not_available", "targets": [], "validation_ok": False}
    targets = []
    for item in rendered.get("files", []):
        if isinstance(item, dict) and item.get("target_path"):
            targets.append(
                {
                    "target_path": _string(item.get("target_path")),
                    "action": _string(item.get("action")),
                }
            )
    validation = rendered.get("validation") if isinstance(rendered.get("validation"), dict) else {}
    return {
        "mode": _string(rendered.get("mode") or "not_available"),
        "targets": targets,
        "validation_ok": bool(validation.get("ok")),
    }


def _manifest_digests(stage_manifest: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(stage_manifest, dict):
        return {
            "workspace_audit_digest": "",
            "infrastructure_plan_digest": "",
            "file_count": 0,
            "file_digests": [],
        }
    files = stage_manifest.get("files") if isinstance(stage_manifest.get("files"), list) else []
    return {
        "workspace_audit_digest": _string(stage_manifest.get("workspace_audit_digest")),
        "infrastructure_plan_digest": _string(stage_manifest.get("infrastructure_plan_digest")),
        "file_count": len(files),
        "file_digests": [
            {
                "target_path": _string(item.get("target_path")),
                "digest": _string(item.get("digest")),
            }
            for item in files
            if isinstance(item, dict)
        ],
    }


def _workspace(runtime: dict[str, Any], discovery: dict[str, Any]) -> str:
    return _string(runtime.get("workspace") or discovery.get("workspace") or "")


def _redacted_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    redacted, report = redact_payload(snapshot)
    if not isinstance(redacted, dict):
        return {
            "schema_version": 1,
            "write_policy": "read_only",
            "redaction_summary": report,
            "readiness_summary": {"status": "blocked", "success_claim": "not_claimed", "warnings": ["snapshot redaction failed"]},
        }
    redacted["redaction_summary"] = report
    return _remove_success_words(redacted)


def _remove_success_words(payload: dict[str, Any]) -> dict[str, Any]:
    text = json.dumps(payload, sort_keys=True).lower()
    if not any(word in text for word in _SUCCESS_WORDS):
        return payload
    sanitized, _report = redact_payload(
        _replace_in_strings(payload, {"tests pass": "tests status redacted", "checks passed": "checks status redacted"})
    )
    return sanitized if isinstance(sanitized, dict) else payload


def _replace_in_strings(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        result = value
        for source, target in replacements.items():
            result = result.replace(source, target).replace(source.title(), target)
        return result
    if isinstance(value, list):
        return [_replace_in_strings(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: _replace_in_strings(item, replacements) for key, item in value.items()}
    return value


def _evidence_recorded_at(item: Any) -> datetime | None:
    if isinstance(item, dict):
        for key in ("recorded_at", "generated_at", "completed_at"):
            parsed = _parse_datetime(_string(item.get(key)))
            if parsed is not None:
                return parsed
    return None


def _parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return result
