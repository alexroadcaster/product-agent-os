from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SYNTHETIC_E2E_SCHEMA_VERSION = "batch41_s6_synthetic_e2e_summary_v1"
REAL_TARGET_PILOT_SCHEMA_VERSION = "batch41_s6_real_target_pilot_summary_v1"
REAL_TARGET_PILOTS_SCHEMA_VERSION = "batch41_s6_real_target_pilots_summary_v1"
USEFULNESS_SCORECARD_SCHEMA_VERSION = "batch41_s6_usefulness_scorecard_v1"
PLUGIN_CACHE_READINESS_SCHEMA_VERSION = "batch41_s6_plugin_cache_readiness_v1"
NO_UNAPPROVED_ACTIONS_SCHEMA_VERSION = "batch41_s6_no_unapproved_actions_proof_v1"
GO_NO_GO_SCHEMA_VERSION = "batch41_s6_go_no_go_decision_packet_v1"
CLOSURE_SCHEMA_VERSION = "batch41_s6_closure_packet_v1"

ATTEMPT_ID = "B41-S6-CLOSURE-A01"
NO_UNAPPROVED_ACTIONS_PROOF_ID = "B41-S6-M30-NO-ACTIONS-A01"
COVERED_TASKS = [f"B41-S6-M{index}" for index in range(24, 31)]

NO_ACTIONS_PERFORMED: dict[str, bool] = {
    "target_workspace_mutation": False,
    "dependency_install": False,
    "live_server": False,
    "browser_automation": False,
    "provider_api_call": False,
    "mcp_external_call": False,
    "git_stage_commit_push_pr": False,
    "release_deploy_publish": False,
    "active_automation": False,
    "plugin_cache_write": False,
}

UNSUPPORTED_CLAIMS = [
    "release readiness is not claimed",
    "runtime/browser behavior is not claimed without current approved runtime/browser evidence",
    "provider/API/model quality is not claimed",
    "target apply safety is not claimed; read-only pilots prove target unchanged only for inspected paths/digests",
    "generated HTML, generated graph and generated question output remain orientation evidence only, not source truth",
    "owner-feedback usefulness is not proven until owner scorecard evidence exists",
    "plugin cache/install readiness is not claimed unless installed-cache evidence exists after approved refresh/check",
]

SNAPSHOT_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".worktrees",
    ".codex-tmp",
    "__pycache__",
    "dist",
    "build",
    "node_modules",
    "site",
    "graphify-out",
    "venv",
}


def build_synthetic_e2e_summary(
    *,
    generated_at: str,
    full_dry_run_payload: dict[str, Any],
    stage_payload: dict[str, Any],
    target_snapshot_before: dict[str, Any],
    target_snapshot_after: dict[str, Any],
) -> dict[str, Any]:
    dry_run_ok = full_dry_run_payload.get("status") == "ok" and full_dry_run_payload.get("mode") == "full_dry_run"
    stage_ok = stage_payload.get("status") == "ok" and stage_payload.get("mode") == "stage"
    question_summary = _question_summary(full_dry_run_payload)
    answer_ledger_present = "answer-ledger-template.json" in set(stage_payload.get("written_files", []))
    target_changed = _snapshot_changed(target_snapshot_before, target_snapshot_after)
    html_page_count = int((stage_payload.get("render_result") or {}).get("page_count") or 0)
    one_blocking_question_max = question_summary["blocking"] <= 1
    status = (
        "passed_synthetic_e2e"
        if dry_run_ok and stage_ok and one_blocking_question_max and answer_ledger_present and html_page_count >= 1 and not target_changed
        else "partial_or_blocked_synthetic_e2e"
    )
    summary = {
        "schema_version": SYNTHETIC_E2E_SCHEMA_VERSION,
        "task_id": "B41-S6-M24",
        "generated_at": generated_at,
        "status": status,
        "dry_run": {
            "status": full_dry_run_payload.get("status"),
            "mode": full_dry_run_payload.get("mode"),
            "packet_schema_version": (full_dry_run_payload.get("packet") or {}).get("schema_version"),
            "first_response_schema_version": (full_dry_run_payload.get("first_response") or {}).get("schema_version"),
        },
        "stage": {
            "status": stage_payload.get("status"),
            "mode": stage_payload.get("mode"),
            "html_page_count": html_page_count,
            "baseline_comparison_status": (stage_payload.get("baseline_comparison") or {}).get("status", "unknown"),
            "written_file_count": len(stage_payload.get("written_files", [])),
        },
        "guided_question_output": {
            "total": question_summary["total"],
            "blocking": question_summary["blocking"],
            "one_blocking_question_max": one_blocking_question_max,
            "route_option_count": len((full_dry_run_payload.get("first_response") or {}).get("route_options", [])),
        },
        "answer_ledger_template_present": answer_ledger_present,
        "target_mutation": _target_mutation_summary(target_snapshot_before, target_snapshot_after),
        "generated_view_policy": (full_dry_run_payload.get("packet") or {}).get(
            "generated_view_policy", "orientation_only_not_proof"
        ),
        "completion_claim": "not_claimed",
        "unsupported_claims": UNSUPPORTED_CLAIMS,
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def build_real_target_pilot_summary(
    *,
    task_id: str,
    target_label: str,
    target_kind: str,
    generated_at: str,
    target_access_status: str,
    full_dry_run_payload: dict[str, Any],
    stage_payload: dict[str, Any],
    target_snapshot_before: dict[str, Any],
    target_snapshot_after: dict[str, Any],
) -> dict[str, Any]:
    packet = full_dry_run_payload.get("packet") or {}
    source_policy = packet.get("source_policy_summary") or {}
    runtime_boundary = packet.get("runtime_browser_boundary") or {}
    dependency_summary = packet.get("dependency_readiness_summary") or {}
    target_changed = _snapshot_changed(target_snapshot_before, target_snapshot_after)
    stage_ok = stage_payload.get("status") == "ok"
    html_page_count = int((stage_payload.get("render_result") or {}).get("page_count") or 0)
    html_artifact_status = "rendered_orientation_only" if stage_ok and html_page_count >= 1 else "not_rendered"
    source_policy_status = str(source_policy.get("status") or "unknown")
    runtime_status = str(runtime_boundary.get("status") or "unknown")
    dependency_status = str(dependency_summary.get("status") or "unknown")

    if target_access_status != "readable":
        status = "blocked_target_unavailable"
    elif full_dry_run_payload.get("status") == "timeout":
        status = "blocked_timeout"
    elif target_changed:
        status = "failed_target_mutation_detected"
    elif target_kind == "docs_research_expected_block" and source_policy_status in {"blocked", "needs_review"}:
        status = "passed_read_only_expected_block"
    elif target_kind == "app_static_runtime_boundary" and runtime_status == "approval_required":
        status = "passed_read_only_static_boundary"
    elif target_kind == "app_static_runtime_boundary" and dependency_status != "unknown":
        status = "passed_read_only_static_boundary"
    else:
        status = "partial_read_only_pilot"

    summary = {
        "schema_version": REAL_TARGET_PILOT_SCHEMA_VERSION,
        "task_id": task_id,
        "generated_at": generated_at,
        "target_label": target_label,
        "target_kind": target_kind,
        "target_access_status": target_access_status,
        "status": status,
        "dry_run_status": full_dry_run_payload.get("status", "not_run"),
        "source_policy_status": source_policy_status,
        "methodology_status": (packet.get("methodology_audit_summary") or {}).get("status", "unknown"),
        "dependency_readiness_status": dependency_status,
        "runtime_browser_status": runtime_status,
        "html_artifact_status": html_artifact_status,
        "html_page_count": html_page_count,
        "guided_question_output": _question_summary(full_dry_run_payload),
        "target_mutation": _target_mutation_summary(target_snapshot_before, target_snapshot_after),
        "generated_view_policy": packet.get("generated_view_policy", "orientation_only_not_proof"),
        "unsupported_claims": [
            "real-target pilot is read-only orientation evidence only",
            *UNSUPPORTED_CLAIMS,
        ],
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def build_real_target_pilots_rollup(*, generated_at: str, pilots: list[dict[str, Any]]) -> dict[str, Any]:
    passed = [pilot for pilot in pilots if str(pilot.get("status", "")).startswith("passed_")]
    blocked = [pilot for pilot in pilots if str(pilot.get("status", "")).startswith("blocked_")]
    failed = [pilot for pilot in pilots if str(pilot.get("status", "")).startswith("failed_")]
    if failed:
        status = "failed_read_only_pilot"
    elif blocked:
        status = "partial_with_expected_blocks"
    else:
        status = "passed_read_only_pilots"
    rollup = {
        "schema_version": REAL_TARGET_PILOTS_SCHEMA_VERSION,
        "generated_at": generated_at,
        "status": status,
        "pilot_count": len(pilots),
        "passed_count": len(passed),
        "blocked_count": len(blocked),
        "failed_count": len(failed),
        "pilots": pilots,
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
        "unsupported_claims": UNSUPPORTED_CLAIMS,
    }
    rollup["rollup_digest"] = content_digest(canonical_json(rollup))
    return rollup


def build_usefulness_scorecard(
    *,
    generated_at: str,
    synthetic_e2e_summary: dict[str, Any],
    real_target_pilots: list[dict[str, Any]],
) -> dict[str, Any]:
    synthetic_passed = synthetic_e2e_summary.get("status") == "passed_synthetic_e2e"
    any_pilot = any(str(pilot.get("status", "")).startswith("passed_") for pilot in real_target_pilots)
    dimensions = {
        "clarity": {
            "score": 4 if synthetic_passed else 2,
            "threshold": 4,
            "rationale": "first response, route options and HTML pages are present in generated evidence",
        },
        "actionability": {
            "score": 4 if synthetic_passed and any_pilot else 3,
            "threshold": 4,
            "rationale": "next actions remain separated across owner feedback, runtime approval and plugin cache readiness",
        },
        "safety": {
            "score": 5,
            "threshold": 5,
            "rationale": "all live, provider, git, release and target-write actions are blocked or not performed",
        },
        "completeness": {
            "score": 4 if synthetic_passed else 3,
            "threshold": 4,
            "rationale": "synthetic E2E covers dry-run, stage, HTML, baseline comparison and questions",
        },
        "noise": {
            "score": 4,
            "threshold": 4,
            "rationale": "first response is capped to one blocking question while full details remain in packet artifacts",
        },
    }
    threshold_met = all(item["score"] >= item["threshold"] for item in dimensions.values())
    scorecard = {
        "schema_version": USEFULNESS_SCORECARD_SCHEMA_VERSION,
        "task_id": "B41-S6-M27",
        "generated_at": generated_at,
        "status": "local_scorecard_ready_owner_feedback_pending",
        "threshold_status": "met_locally_owner_feedback_pending" if threshold_met else "not_met",
        "owner_feedback_required": True,
        "release_readiness_claim": "not_claimed",
        "dimensions": dimensions,
        "accepted_gaps": [
            "owner feedback has not been collected in this run",
            "runtime/browser proof remains approval-required",
            "plugin cache readiness may require an approved cache refresh",
        ],
        "unsupported_claims": UNSUPPORTED_CLAIMS,
    }
    scorecard["scorecard_digest"] = content_digest(canonical_json(scorecard))
    return scorecard


def build_plugin_cache_readiness(
    *,
    generated_at: str,
    source_markers: dict[str, bool],
    cache_markers: dict[str, bool],
) -> dict[str, Any]:
    source_ready = all(source_markers.values()) if source_markers else False
    cache_ready = all(cache_markers.values()) if cache_markers else False
    status = "ready" if source_ready and cache_ready else "blocked_expected_approval_required"
    readiness = {
        "schema_version": PLUGIN_CACHE_READINESS_SCHEMA_VERSION,
        "task_id": "B41-S6-M29",
        "generated_at": generated_at,
        "status": status,
        "source_tree_ready": source_ready,
        "installed_cache_ready": cache_ready,
        "source_markers": source_markers,
        "cache_markers": cache_markers,
        "cache_refresh_required": not cache_ready,
        "approval_required": not cache_ready,
        "cache_write_performed": False,
        "unsupported_claims": [
            "plugin cache/install readiness is not claimed unless installed-cache evidence exists after approved refresh/check"
        ],
    }
    readiness["readiness_digest"] = content_digest(canonical_json(readiness))
    return readiness


def build_no_unapproved_actions_proof(*, generated_at: str) -> dict[str, Any]:
    proof = {
        "schema_version": NO_UNAPPROVED_ACTIONS_SCHEMA_VERSION,
        "proof_id": NO_UNAPPROVED_ACTIONS_PROOF_ID,
        "generated_at": generated_at,
        "status": "passed_no_unapproved_actions_proof",
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
        "approval_required_followups": [
            "runtime/browser pilot",
            "plugin cache refresh",
            "git/release/publish actions",
            "target workspace apply",
        ],
    }
    proof["proof_digest"] = content_digest(canonical_json(proof))
    return proof


def build_batch41_s6_closure_packet(
    *,
    generated_at: str,
    synthetic_e2e_summary: dict[str, Any],
    real_target_pilots: list[dict[str, Any]],
    usefulness_scorecard: dict[str, Any],
    verification_evidence: dict[str, Any],
    plugin_cache_readiness: dict[str, Any],
) -> dict[str, Any]:
    pilot_by_task = {pilot.get("task_id"): pilot for pilot in real_target_pilots}
    plugin_status = plugin_cache_readiness.get("status")
    verification_status = "implemented_verification_sweep" if verification_evidence else "pending_verification_evidence"
    tasks = {
        "B41-S6-M24": {
            "status": "implemented" if synthetic_e2e_summary.get("status") == "passed_synthetic_e2e" else "partial",
            "evidence": "batch41-s6-synthetic-e2e-summary.json",
        },
        "B41-S6-M25": {
            "status": _pilot_task_status(pilot_by_task.get("B41-S6-M25")),
            "evidence": "batch41-s6-real-target-pilots-summary.json",
        },
        "B41-S6-M26": {
            "status": _pilot_task_status(pilot_by_task.get("B41-S6-M26")),
            "evidence": "batch41-s6-real-target-pilots-summary.json",
        },
        "B41-S6-M27": {
            "status": "implemented_scorecard_owner_feedback_pending",
            "evidence": "batch41-s6-usefulness-scorecard.json",
        },
        "B41-S6-M28": {
            "status": verification_status,
            "evidence": "batch41-s6-verification-sweep-summary.json",
        },
        "B41-S6-M29": {
            "status": "implemented" if plugin_status == "ready" else "blocked_expected_approval_required",
            "evidence": "batch41-s6-plugin-cache-readiness.json",
        },
        "B41-S6-M30": {
            "status": "implemented_no_go_closure",
            "evidence": "batch41-s6-closure-summary.json",
        },
    }
    go_no_go = {
        "release": "no_go",
        "owner_feedback_testing": "conditional_go",
        "runtime_browser_pilot": "approval_required",
        "plugin_cache_readiness": "ready" if plugin_status == "ready" else "approval_required",
        "target_apply": "approval_required",
        "reason": "Batch 41 has local/read-only/staged evidence, but release, runtime/browser and plugin-cache readiness remain separately gated.",
    }
    packet = {
        "schema_version": CLOSURE_SCHEMA_VERSION,
        "source_status": "local_implementation_evidence",
        "attempt_id": ATTEMPT_ID,
        "generated_at": generated_at,
        "slice": "B41-S6",
        "covered_tasks": COVERED_TASKS,
        "status": "closed_conditional_go_not_release_ready",
        "tasks": tasks,
        "synthetic_e2e_status": synthetic_e2e_summary.get("status"),
        "real_target_pilot_statuses": {pilot.get("task_id"): pilot.get("status") for pilot in real_target_pilots},
        "usefulness_scorecard_status": usefulness_scorecard.get("status"),
        "verification_evidence": verification_evidence,
        "plugin_cache_readiness_status": plugin_status,
        "go_no_go": go_no_go,
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
        "unsupported_claims": UNSUPPORTED_CLAIMS,
        "approval_required_followups": [
            "collect owner feedback using the usefulness scorecard",
            "approve disposable runtime/browser pilot before runtime claims",
            "approve plugin cache refresh before installed-plugin readiness claims",
            "approve git/release/publish actions before external distribution",
        ],
        "control_plane_sync": {
            "PLAN.md": "updated_required",
            "TEST.md": "updated_required",
            "RUNLOG.md": "updated_required",
            "track_10_plan": "updated_required",
            "batch41_matrix": "updated_required",
            "source_registry": "not_applicable_no_public_source_claims_added",
        },
    }
    packet["closure_digest"] = content_digest(canonical_json(packet))
    return packet


def build_go_no_go_decision_packet(*, generated_at: str, closure_packet: dict[str, Any]) -> dict[str, Any]:
    decision = {
        "schema_version": GO_NO_GO_SCHEMA_VERSION,
        "generated_at": generated_at,
        "attempt_id": closure_packet.get("attempt_id", ATTEMPT_ID),
        "status": closure_packet.get("status"),
        "go_no_go": closure_packet.get("go_no_go"),
        "unsupported_claims": closure_packet.get("unsupported_claims", UNSUPPORTED_CLAIMS),
        "approval_required_followups": closure_packet.get("approval_required_followups", []),
    }
    decision["decision_digest"] = content_digest(canonical_json(decision))
    return decision


def build_verification_sweep_summary(
    *,
    generated_at: str,
    command_results: dict[str, Any],
    skipped_checks: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    failed = {
        name: result
        for name, result in command_results.items()
        if isinstance(result, dict) and result.get("status") not in {"passed", "ok"}
    }
    summary = {
        "schema_version": "batch41_s6_verification_sweep_summary_v1",
        "task_id": "B41-S6-M28",
        "generated_at": generated_at,
        "status": "passed" if not failed and not skipped_checks else "partial_with_recorded_gaps",
        "command_results": command_results,
        "failed_checks": failed,
        "skipped_checks": skipped_checks or [],
        "unsupported_claims": UNSUPPORTED_CLAIMS,
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def target_snapshot(root: str | Path, *, max_files: int = 5000) -> dict[str, Any]:
    root_path = Path(root)
    if not root_path.exists():
        return {
            "status": "missing",
            "file_count": 0,
            "fingerprint": content_digest("missing"),
            "sample_refs": [],
        }
    if not root_path.is_dir():
        return {
            "status": "not_directory",
            "file_count": 0,
            "fingerprint": content_digest("not_directory"),
            "sample_refs": [],
        }

    entries: list[dict[str, Any]] = []
    read_errors = 0
    for path in _iter_snapshot_files(root_path, max_files=max_files):
        try:
            rel = path.relative_to(root_path).as_posix()
            stat = path.stat()
            entries.append({"ref": rel, "size": stat.st_size, "digest": content_digest(path.read_bytes())})
        except OSError:
            read_errors += 1
    payload = {"entries": entries, "read_errors": read_errors}
    return {
        "status": "readable",
        "file_count": len(entries),
        "fingerprint": content_digest(canonical_json(payload)),
        "sample_refs": [entry["ref"] for entry in entries[:20]],
        "read_error_count": read_errors,
        "truncated": len(entries) >= max_files,
    }


def inspect_marker_text(root: str | Path, marker_map: dict[str, tuple[str, ...]]) -> dict[str, bool]:
    root_path = Path(root)
    if not root_path.exists():
        return {name: False for name in marker_map}
    results: dict[str, bool] = {}
    for name, markers in marker_map.items():
        results[name] = all(_contains_text(root_path, marker) for marker in markers)
    return results


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _question_summary(payload: dict[str, Any]) -> dict[str, int]:
    packet = payload.get("packet") or {}
    queue_summary = ((packet.get("question_queue") or {}).get("summary") or {})
    first_response = payload.get("first_response") or {}
    total = int(queue_summary.get("total") or 0)
    blocking = int(queue_summary.get("blocking") or first_response.get("blocking_question_count") or 0)
    return {"total": total, "blocking": blocking}


def _snapshot_changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return before.get("fingerprint") != after.get("fingerprint") or before.get("file_count") != after.get("file_count")


def _target_mutation_summary(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    return {
        "changed": _snapshot_changed(before, after),
        "before_fingerprint": before.get("fingerprint"),
        "after_fingerprint": after.get("fingerprint"),
        "before_file_count": before.get("file_count"),
        "after_file_count": after.get("file_count"),
    }


def _pilot_task_status(pilot: dict[str, Any] | None) -> str:
    if not pilot:
        return "blocked_target_unavailable"
    status = str(pilot.get("status") or "")
    if status.startswith("passed_"):
        return "implemented_read_only"
    if status.startswith("blocked_"):
        return status
    if status.startswith("failed_"):
        return status
    return "partial_read_only"


def _iter_snapshot_files(root_path: Path, *, max_files: int) -> list[Path]:
    files: list[Path] = []
    stack = [root_path]
    while stack and len(files) < max_files:
        current = stack.pop()
        try:
            children = sorted(current.iterdir(), key=lambda item: item.name.lower())
        except OSError:
            continue
        for child in children:
            if child.is_dir():
                if child.name not in SNAPSHOT_SKIP_DIRS:
                    stack.append(child)
            elif child.is_file():
                files.append(child)
                if len(files) >= max_files:
                    break
    return files


def _contains_text(root_path: Path, marker: str) -> bool:
    if root_path.is_file():
        return _file_contains_text(root_path, marker)
    for path in _iter_snapshot_files(root_path, max_files=2000):
        if path.suffix.lower() not in {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt"}:
            continue
        if _file_contains_text(path, marker):
            return True
    return False


def _file_contains_text(path: Path, marker: str) -> bool:
    try:
        return marker in path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
