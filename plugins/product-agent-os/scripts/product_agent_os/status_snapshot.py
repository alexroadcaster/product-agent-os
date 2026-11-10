"""Read-only project status snapshot builder for Product-Agent OS."""

from __future__ import annotations

import json
import hashlib
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload
from product_agent_os.plugin_components import unique_json_object


DEFAULT_EVIDENCE_MAX_AGE_DAYS = 14
_SUCCESS_WORDS = ("tests pass", "checks passed")
MAX_METRICS_REPORT_REFS = 4
MAX_METRICS_UPDATE_CANDIDATES = 5
MAX_PROJECT_GRAPH_REFS = 4
MAX_PROJECT_GRAPH_GAPS = 5
MAX_PROJECT_GRAPH_UNSUPPORTED_LANGUAGES = 8
MAX_SYSTEM_FILE_STATUSES = 50
MAX_COMPLETION_SKEPTIC_ITEMS = 8
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
    workspace: str | Path | None = None,
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
    current_state = _current_state(Path(workspace) if workspace is not None else None, generated_at)

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
        "current_state": current_state,
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
        "pilot_evidence_rollup": _pilot_evidence_rollup_summary(route),
        "first_run_analysis": _first_run_analysis_summary(route),
        "completion_skeptic": _completion_skeptic_summary(route),
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
    if current_state["pointer_present"]:
        snapshot["projection_decisions"]["task_matrix_state"] = {
            "status": current_state["status"], "state_projection": "bounded_source_revision_projection",
            "source_policy": "PLAN pointer selects owning sources; generated view is not completion proof",
        }
    return _redacted_snapshot(snapshot)


_CURRENT_POINTER = re.compile(r"<!-- product-agent-os:current-state:start -->\s*```json\s*(.*?)\s*```\s*<!-- product-agent-os:current-state:end -->", re.S)
_TASK_ID = re.compile(r"[A-Za-z0-9_.-]{1,128}")
_REVISION = re.compile(r"sha256:[a-f0-9]{64}")
_TASK_STATES = {
    "planned": ("planned", "not_verified"),
    "planned_not_started": ("planned", "not_verified"),
    "approval_required_not_started": ("blocked", "not_verified"),
    "in_progress": ("in_progress", "not_verified"),
    "implemented": ("implemented", "not_verified"),
    "locally_implemented_focused_verified": ("implemented", "locally_verified"),
    "implemented_locally_verified": ("implemented", "locally_verified"),
    "implemented_locally_verified_explicit_only": ("implemented", "locally_verified"),
    "implemented_locally_synthetic_route": ("implemented", "synthetic_verified"),
    "partially_verified_local_inventory": ("unknown", "partially_verified"),
    "partially_verified_synthetic_only": ("unknown", "partially_verified"),
    "not_verified_fresh_host_required": ("unknown", "not_verified"),
    "blocked": ("blocked", "not_verified"),
}


def _current_state(workspace: Path | None, generated_at: str) -> dict[str, Any]:
    """Read a single revision-pinned PLAN pointer, never infer ownership from headings.

    Sources remain authoritative. No writes, global search, arbitrary Markdown
    execution or automatic acceptance; malformed/stale sources have no fallback.
    """
    result = {"status": "unknown", "pointer_present": False, "tasks": [], "sources": [],
              "issues": [], "source_policy": "generated_orientation_only_not_acceptance"}
    if workspace is None:
        result["issues"].append("workspace_not_provided")
        return result
    root = workspace.resolve()
    try:
        plan = _read_current_source(root, "PLAN.md").decode("utf-8")
        matches = _CURRENT_POINTER.findall(plan)
        result["pointer_present"] = "<!-- product-agent-os:current-state:start -->" in plan
        if len(matches) != 1:
            raise ValueError("current_pointer_missing_or_ambiguous")
        pointer = json.loads(matches[0], object_pairs_hook=unique_json_object)
        if not isinstance(pointer, dict) or pointer.get("schema_version") != 1 or set(pointer) != {"schema_version", "sources"}:
            raise ValueError("invalid_current_pointer")
        sources = pointer["sources"]
        # Compact task groups may need more source files. Keep the original
        # aggregate read ceiling (8 * 2 MiB), rather than multiplying it by 32.
        if not isinstance(sources, list) or not 1 <= len(sources) <= 32:
            raise ValueError("invalid_current_sources")
        total_source_bytes = 0
        for ref in sources:
            if not isinstance(ref, dict) or not {"path", "revision"} <= set(ref) or set(ref) - {"path", "revision", "task_prefixes"} or not isinstance(ref["revision"], str) or not _REVISION.fullmatch(ref["revision"]):
                raise ValueError("invalid_source_reference")
            prefixes = ref.get("task_prefixes", [])
            if not isinstance(prefixes, list) or len(prefixes) > 8 or any(not isinstance(prefix, str) or not _TASK_ID.fullmatch(prefix) for prefix in prefixes):
                raise ValueError("invalid_task_scope")
            path = ref["path"]
            if not isinstance(path, str) or not path.endswith((".json", ".md")) or not path.startswith(("docs/superpowers/", "research/")):
                raise ValueError("unsupported_source_path")
            content = _read_current_source(root, path)
            total_source_bytes += len(content)
            if total_source_bytes > 16 * 1024 * 1024:
                raise ValueError("current_source_byte_limit")
            revision = "sha256:" + hashlib.sha256(content).hexdigest()
            if revision != ref["revision"]:
                raise ValueError("source_revision_mismatch")
            result["sources"].append({"path": path, "revision": revision, "task_prefixes": prefixes})
            if path.endswith(".json"):
                doc = json.loads(content.decode("utf-8"), object_pairs_hook=unique_json_object)
                if not isinstance(doc, dict) or not isinstance(doc.get("tasks"), list):
                    raise ValueError("invalid_task_source")
                tasks = doc["tasks"]
                baseline_date = doc.get("generated_at") or doc.get("checked_at")
            else:
                tasks = _markdown_tasks(content.decode("utf-8"))
                baseline_date = None
            if len(tasks) > 2000 or len(result["tasks"]) + len(tasks) > 2000:
                raise ValueError("task_projection_limit")
            for task in tasks:
                row = _project_task(task, path, revision, baseline_date, generated_at)
                if not prefixes or any(row["task_id"].startswith(prefix) for prefix in prefixes):
                    result["tasks"].append(row)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        # Never copy raw input, paths from exceptions, or partial success.
        reason = str(exc) if type(exc) is ValueError and re.fullmatch(r"[a-z_]+", str(exc)) else "invalid_current_source"
        result["issues"].append(reason)
        result["tasks"] = []
        return result
    seen = set()
    for row in result["tasks"]:
        if row["task_id"] in seen:
            result["issues"].append("duplicate_task_ownership")
            for duplicate in result["tasks"]:
                if duplicate["task_id"] == row["task_id"]:
                    _uncertain_task(duplicate, "conflict")
        seen.add(row["task_id"])
    states = {row["projection_status"] for row in result["tasks"]}
    result["status"] = "conflict" if "conflict" in states else "unknown" if "unknown" in states or not states else "projected"
    return result


def _read_current_source(root: Path, relative: str) -> bytes:
    if not _safe_project_graph_relative_path(relative) or ":" in relative or "\\" in relative:
        raise ValueError("unsafe_source_path")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("unsafe_source_path")
    with path.open("rb") as stream:
        content = stream.read(2 * 1024 * 1024 + 1)
    if len(content) > 2 * 1024 * 1024:
        raise ValueError("source_size_limit")
    return content


def _markdown_tasks(text: str) -> list[dict[str, Any]]:
    tasks = []
    for block in re.split(r"(?m)^### Task `", text)[1:]:
        task_id = block.split("`", 1)[0]
        status = re.findall(r"(?m)^- Status: ([a-z_]+)\s*$", block)
        completion = re.findall(r"(?m)^- status: ([a-z_]+)\s*$", block)
        if len(status) != 1 or len(completion) != 1:
            raise ValueError("ambiguous_markdown_task")
        tasks.append({"task_id": task_id, "status": status[0], "completion_status": completion[0]})
    return tasks


def _project_task(task: Any, path: str, revision: str, baseline_date: Any, generated_at: str) -> dict[str, Any]:
    if not isinstance(task, dict):
        raise ValueError("invalid_task_record")
    task_id = task.get("task_id") or task.get("id")
    if not isinstance(task_id, str) or not _TASK_ID.fullmatch(task_id):
        raise ValueError("invalid_task_id")
    historical = task.get("status")
    row = {"task_id": task_id, "source_path": path, "source_revision": revision,
           "historical_status": historical if isinstance(historical, str) and historical in _TASK_STATES else "unknown",
           "selected_evidence": "source_status", "projection_status": "projected",
           "task_state": "unknown", "run_state": "unknown", "verification_state": "not_verified", "acceptance_state": "unknown"}
    selected = task
    receipts = task.get("execution_evidence")
    if receipts is not None:
        receipts = receipts if isinstance(receipts, list) else [receipts]
        current = _state_date(generated_at)
        baseline = _state_date(baseline_date)
        if not receipts or len(receipts) > 16 or current is None or baseline is None:
            return _uncertain_task(row, "unknown")
        dated = []
        for receipt in receipts:
            checked = _state_date(receipt.get("checked_at")) if isinstance(receipt, dict) else None
            if checked is None or checked > current:
                return _uncertain_task(row, "unknown")
            dated.append((checked, receipt))
        latest = max(when for when, _ in dated)
        candidates = [item for when, item in dated if when == latest]
        signatures = {json.dumps({key: item.get(key) for key in ("status", "run_status", "verification_status", "acceptance_status")}, sort_keys=True) for item in candidates}
        if len(signatures) != 1 or latest == baseline and candidates[0].get("status") != historical:
            return _uncertain_task(row, "conflict")
        if latest > baseline:
            selected = candidates[0]
            row["selected_evidence"] = "execution_evidence"
    if task.get("completion_status", historical) != historical:
        return _uncertain_task(row, "conflict")
    state = selected.get("status")
    if not isinstance(state, str) or state not in _TASK_STATES:
        return _uncertain_task(row, "unknown")
    row["task_state"], row["verification_state"] = _TASK_STATES[state]
    for field, allowed in (("run", {"not_started", "running", "completed", "failed", "blocked"}),
                           ("verification", {"not_verified", "locally_verified", "partially_verified", "failed"}),
                           ("acceptance", {"accepted", "needs_user_acceptance", "rejected"})):
        value = selected.get(field + "_status")
        if value is not None:
            if not isinstance(value, str) or value not in allowed:
                return _uncertain_task(row, "unknown")
            row[field + "_state"] = value
    return row


def _uncertain_task(row: dict[str, Any], status: str) -> dict[str, Any]:
    row.update(projection_status=status, task_state=status, run_state="unknown", verification_state="not_verified", acceptance_state="unknown")
    return row


def _state_date(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    parsed = _parse_datetime(value)
    if parsed is not None and parsed.tzinfo is None and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        parsed = parsed.replace(tzinfo=UTC)
    return parsed if parsed is not None and parsed.tzinfo is not None else None


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
    stale_items = unknown_items = future_items = 0
    if items:
        freshness = "current"
        generated = _parse_datetime(generated_at)
        for item in items:
            recorded_at = _evidence_recorded_at(item)
            if generated is None or generated.tzinfo is None or recorded_at is None or recorded_at.tzinfo is None:
                unknown_items += 1
            elif recorded_at > generated:
                future_items += 1
            elif (generated - recorded_at).days > evidence_max_age_days:
                stale_items += 1
        if unknown_items:
            freshness = "unknown"
        elif future_items:
            freshness = "future"
        elif stale_items:
            freshness = "stale"
    return {
        "freshness": freshness,
        "evidence_count": len(items),
        "stale_count": stale_items,
        "unknown_count": unknown_items,
        "future_count": future_items,
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
    if evidence_summary.get("freshness") != "current" and runtime_status == "completed":
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


def _pilot_evidence_rollup_summary(route: dict[str, Any]) -> dict[str, Any]:
    packet = route.get("pilot_evidence_rollup")
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "counts": {},
            "blockers": [],
            "accepted_gaps": [],
            "safe_next_action": "Review underlying pilot evidence before dashboard claims.",
            "source_policy": "generated view is not proof",
        }
    counts = packet.get("counts") if isinstance(packet.get("counts"), dict) else {}
    return {
        "status": _string(packet.get("safe_next_action") or "available"),
        "counts": {key: _int(value) for key, value in counts.items()},
        "blockers": _safe_string_list(packet.get("blockers"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        "accepted_gaps": _safe_string_list(packet.get("accepted_gaps"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        "safe_next_action": _string(packet.get("safe_next_action") or "Review underlying pilot evidence before dashboard claims."),
        "generated_view_policy": _string(packet.get("generated_view_policy") or "orientation_only_not_proof"),
        "source_policy": "generated view is not proof",
    }


def _first_run_analysis_summary(route: dict[str, Any]) -> dict[str, Any]:
    packet = route.get("first_run_analysis_ref")
    if not isinstance(packet, dict):
        packet = _first_run_ref_from_rollup(route.get("pilot_evidence_rollup"))
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "kind": "not_available",
            "path": "",
            "manifest_digest": "",
            "page_count": 0,
            "freshness": "not_available",
            "unsupported_claim_count": 0,
            "generated_view_policy": "orientation_only_not_proof",
            "source_policy": "first-run analysis is generated orientation evidence, not proof",
        }
    safe_ref = _safe_ref(
        {
            "kind": packet.get("kind") or "generated_analysis_pack",
            "path": packet.get("path") or "",
            "digest": packet.get("digest") or packet.get("manifest_digest") or "",
        }
    )
    return {
        "status": "available" if safe_ref["path"] and safe_ref["digest"] else "not_available",
        "kind": safe_ref["kind"],
        "path": safe_ref["path"],
        "manifest_digest": safe_ref["digest"],
        "page_count": _int(packet.get("page_count")),
        "freshness": _string(packet.get("freshness") or "not_available"),
        "unsupported_claim_count": _int(packet.get("unsupported_claim_count")),
        "generated_view_policy": "orientation_only_not_proof",
        "source_policy": "first-run analysis is generated orientation evidence, not proof",
    }


def _first_run_ref_from_rollup(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    rows = value.get("task_rows")
    if not isinstance(rows, list):
        return {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        ref = row.get("first_run_analysis_ref")
        if isinstance(ref, dict) and ref:
            return ref
    return {}


def _project_graph_summary(packet: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "generated_view_policy": "orientation_only_not_proof",
            "counts": {"nodes": 0, "edges": 0, "observations": 0, "omitted_nodes": 0},
            "coverage": _safe_project_graph_coverage({}),
            "freshness": _safe_project_graph_freshness({}),
            "rejected_link_summary": _bounded_project_graph_counter_summary({}),
            "framework_semantic_summary": _bounded_project_graph_counter_summary({}),
            "agent_packet_refs": [],
            "unsupported_languages": [],
            "artifact_refs": [],
            "top_gaps": [],
            "source_policy": "generated graph is not source of truth",
            "safe_next_action": "Read source files before graph-backed claims.",
        }
    counts = packet.get("counts") if isinstance(packet.get("counts"), dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "generated_view_policy": _string(packet.get("generated_view_policy") or "orientation_only_not_proof"),
        "freshness": _safe_project_graph_freshness(packet.get("freshness")),
        "counts": {
            "nodes": _int(counts.get("nodes")),
            "edges": _int(counts.get("edges")),
            "observations": _int(counts.get("observations")),
            "omitted_nodes": _int(counts.get("omitted_nodes")),
        },
        "coverage": _safe_project_graph_coverage(packet.get("coverage_map") or packet.get("coverage")),
        "rejected_link_summary": _bounded_project_graph_counter_summary(packet.get("rejected_link_summary")),
        "framework_semantic_summary": _bounded_project_graph_counter_summary(packet.get("framework_semantic_summary")),
        "agent_packet_refs": _safe_project_graph_refs(packet.get("agent_packet_refs")),
        "unsupported_languages": _safe_project_graph_unsupported_languages(packet.get("unsupported_languages")),
        "artifact_refs": _safe_project_graph_refs(packet.get("artifact_refs")),
        "top_gaps": _safe_project_graph_gaps(packet.get("top_gaps")),
        "source_policy": "generated graph is not source of truth",
        "safe_next_action": _string(packet.get("safe_next_action") or "Read source files before graph-backed claims."),
    }


def _completion_skeptic_summary(route: dict[str, Any]) -> dict[str, Any]:
    packet = route.get("completion_skeptic_recommendation")
    if not isinstance(packet, dict) or not packet:
        return {
            "status": "not_available",
            "trigger_level": "not_available",
            "recommended_skill": "completion-skeptic",
            "top_reason": "",
            "trigger_sources": [],
            "risk_classes": [],
            "required_evidence": [],
            "evidence_summary": {
                "required": 0,
                "available": 0,
                "missing": 0,
                "stale": 0,
                "approval_required": 0,
                "accepted_gap": 0,
            },
            "approval_boundary": {"status": "not_required", "hits": []},
            "packet_ref": {"kind": "not_available", "path": "", "digest": ""},
            "safe_next_action": "Run normal verification before any completion claim.",
            "source_policy": "completion skeptic recommendation is generated routing guidance, not source of truth",
        }
    reasons = _safe_string_list(packet.get("reasons"))[:MAX_COMPLETION_SKEPTIC_ITEMS]
    evidence = packet.get("evidence_summary") if isinstance(packet.get("evidence_summary"), dict) else {}
    approval = packet.get("approval_boundary") if isinstance(packet.get("approval_boundary"), dict) else {}
    packet_ref = packet.get("packet_ref") if isinstance(packet.get("packet_ref"), dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "trigger_level": _string(packet.get("trigger_level") or packet.get("status") or "not_available"),
        "recommended_skill": _string(packet.get("recommended_skill") or "completion-skeptic"),
        "top_reason": reasons[0] if reasons else "",
        "trigger_sources": _safe_string_list(packet.get("trigger_sources"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        "risk_classes": _safe_string_list(packet.get("risk_classes"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        "required_evidence": _safe_string_list(packet.get("required_evidence"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        "evidence_summary": {
            "required": _int(evidence.get("required")),
            "available": _int(evidence.get("available")),
            "missing": _int(evidence.get("missing")),
            "stale": _int(evidence.get("stale")),
            "approval_required": _int(evidence.get("approval_required")),
            "accepted_gap": _int(evidence.get("accepted_gap")),
        },
        "approval_boundary": {
            "status": _string(approval.get("status") or "not_required"),
            "hits": _safe_string_list(approval.get("hits"))[:MAX_COMPLETION_SKEPTIC_ITEMS],
        },
        "packet_ref": _safe_ref(packet_ref),
        "safe_next_action": _string(packet.get("safe_next_action") or "Run normal verification before any completion claim."),
        "source_policy": "completion skeptic recommendation is generated routing guidance, not source of truth",
    }


def _safe_ref(value: dict[str, Any]) -> dict[str, str]:
    kind = _string(value.get("kind") or "not_available")
    path = _string(value.get("path"))
    if path and (
        path.startswith(("http://", "https://"))
        or not _safe_project_graph_relative_path(path)
    ):
        path = ""
        kind = "not_available"
    return {"kind": kind, "path": path, "digest": _string(value.get("digest"))}


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


def _safe_project_graph_coverage(value: Any) -> dict[str, Any]:
    packet = value if isinstance(value, dict) else {}
    unsupported = packet.get("unsupported_languages") if isinstance(packet.get("unsupported_languages"), dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "covered_files": _int(packet.get("covered_files")),
        "partial_files": _int(packet.get("partial_files")),
        "unsupported_languages": {
            _string(key): _string(item)
            for key, item in sorted(unsupported.items(), key=lambda entry: str(entry[0]))[
                :MAX_PROJECT_GRAPH_UNSUPPORTED_LANGUAGES
            ]
            if _string(key)
        },
    }


def _safe_project_graph_freshness(value: Any) -> dict[str, Any]:
    packet = value if isinstance(value, dict) else {}
    return {
        "status": _string(packet.get("status") or "not_available"),
        "blocks_action_claims": bool(packet.get("blocks_action_claims")),
        "safe_next_action": _string(
            packet.get("safe_next_action") or "Read source files before graph-backed claims."
        ),
    }


def _bounded_project_graph_counter_summary(value: Any) -> dict[str, Any]:
    packet = value if isinstance(value, dict) else {}
    reasons = packet.get("by_reason") if isinstance(packet.get("by_reason"), dict) else {}
    frameworks = packet.get("frameworks") if isinstance(packet.get("frameworks"), dict) else {}
    result: dict[str, Any] = {"total": _int(packet.get("total"))}
    if reasons:
        result["by_reason"] = {
            _string(key): _int(item)
            for key, item in sorted(reasons.items(), key=lambda entry: str(entry[0]))[:MAX_PROJECT_GRAPH_GAPS]
            if _string(key)
        }
    if frameworks:
        result["frameworks"] = {
            _string(key): _int(item)
            for key, item in sorted(frameworks.items(), key=lambda entry: str(entry[0]))[
                :MAX_PROJECT_GRAPH_UNSUPPORTED_LANGUAGES
            ]
            if _string(key)
        }
    return result


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


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_string(item) for item in value if _string(item)]


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
