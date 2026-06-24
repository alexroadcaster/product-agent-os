from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


SELF_LEARNING_CANDIDATE_PACKET_SCHEMA_VERSION = "self_learning_candidate_packet_v1"
SELF_LEARNING_FORBIDDEN_ACTION_REPORT_SCHEMA_VERSION = "self_learning_forbidden_action_report_v1"
CANDIDATE_PACKET_RELATIVE_PATH = ".codex/product-agent-os/self-learning-candidates.json"


_FORBIDDEN_ACTION_ALIASES = {
    "active_schedule_creation": {
        "active_schedule",
        "activate_schedule",
        "create_schedule",
        "recurring_automation",
        "schedule_creation",
    },
    "hook_activation": {"activate_hook", "enable_hook", "hook_activation", "install_hook"},
    "raw_transcript_storage": {
        "raw_transcript",
        "store_raw_transcript",
        "raw_chat_storage",
        "private_transcript_storage",
    },
    "provider_call": {"provider_call", "live_model_call", "model_call", "api_call", "live_eval_service"},
    "global_config_mutation": {"global_config_mutation", "edit_global_config", "config_write"},
    "git_action": {"git_commit", "git_push", "git_tag", "open_pr", "create_pr", "git_action"},
    "target_mutation": {"target_mutation", "edit_target", "target_write", "apply_patch_to_target"},
    "release_deploy_publish": {"release", "deploy", "publish", "deploy_publish", "package_registry_write"},
    "auto_apply": {"auto_apply", "apply_automatically", "self_apply", "apply_patch"},
    "external_write": {"external_write", "send_external", "create_ticket", "mutate_external_system"},
    "hidden_telemetry": {"hidden_telemetry", "scrape_hidden_logs", "codex_app_hidden_logs"},
}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def build_self_learning_candidate_packet(
    *,
    metrics_summary: dict[str, Any] | None = None,
    feedback_summary: dict[str, Any] | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Build review-only modernization candidates from local summaries."""

    metrics = metrics_summary or {}
    feedback = feedback_summary or {}
    candidates: list[dict[str, Any]] = []

    regression_flags = [str(flag) for flag in metrics.get("regression_flags", [])]
    if metrics.get("status") == "available" and regression_flags:
        candidates.append(
            _candidate(
                component="eval_harness",
                target_id="eval:self-learning-regression-review",
                reason="Metric regressions need a focused review candidate.",
                evidence_refs=_metric_evidence_refs(metrics),
                metric_deltas={"regression_flags": regression_flags, "metric_delta_count": metrics.get("metric_delta_count", 0)},
                feedback_refs=[],
                expected_impact="Expose regressions before any skill, prompt or routing change is reviewed.",
                risk="medium",
                rollback_target="current_eval_contract",
                tests_required=[
                    "python -m unittest tests.product_agent_os.test_agent_skill_metrics -v",
                    "python -m unittest tests.product_agent_os.test_self_learning_state -v",
                ],
            )
        )

    satisfaction = feedback.get("satisfaction_report") if isinstance(feedback.get("satisfaction_report"), dict) else {}
    dissatisfied_count = int(satisfaction.get("dissatisfied_count") or 0)
    if feedback.get("status") == "available" and dissatisfied_count:
        candidates.append(
            _candidate(
                component="prompt",
                target_id="prompt:self-learning-owner-feedback-response",
                reason="Owner feedback indicates dissatisfaction or rework pressure.",
                evidence_refs=["owner_feedback_ledger:summary"],
                metric_deltas={
                    "dissatisfied_count": dissatisfied_count,
                    "human_label_denominator": satisfaction.get("denominator", 0),
                    "promotion_signal": satisfaction.get("promotion_signal", "unknown"),
                },
                feedback_refs=["owner_feedback_ledger"],
                expected_impact="Improve acknowledgement of owner corrections while preserving verification boundaries.",
                risk="medium",
                rollback_target="current_prompt_contract",
                tests_required=[
                    "python -m unittest tests.product_agent_os.test_self_learning_state -v",
                ],
            )
        )

    safety_report = evaluate_forbidden_action_fixtures(candidates)
    return {
        "schema_version": SELF_LEARNING_CANDIDATE_PACKET_SCHEMA_VERSION,
        "generated_at": generated_at,
        "status": "available" if candidates else "no_candidates",
        "candidate_policy": "candidate_only",
        "candidate_count": len(candidates),
        "candidates": candidates,
        "apply_policy": "cannot_apply",
        "auto_apply": "disabled",
        "provider_calls": "not_performed",
        "live_eval_services": "not_performed",
        "target_workspace_writes": "not_performed",
        "external_write_action": "none",
        "approval_required_before_apply": True,
        "safety_report": safety_report,
        "unsupported_claims": [
            "candidate packet applied changes",
            "candidate packet created schedules or hooks",
            "candidate packet called providers or live eval services",
            "candidate packet performed target, git, release, deploy or publish actions",
        ],
    }


def evaluate_forbidden_action_fixtures(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    """Evaluate synthetic candidate actions without executing side effects."""

    results: list[dict[str, Any]] = []
    blocked_count = 0
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id") or "unknown")
        blocked_actions: set[str] = set()
        for action in candidate.get("proposed_actions", []):
            blocked_actions.update(_blocked_action_types(action))
        if blocked_actions:
            blocked_count += 1
        results.append(
            {
                "candidate_id": candidate_id,
                "status": "blocked" if blocked_actions else "review_ready",
                "blocked_actions": sorted(blocked_actions),
            }
        )
    return {
        "schema_version": SELF_LEARNING_FORBIDDEN_ACTION_REPORT_SCHEMA_VERSION,
        "fixture_execution_policy": "synthetic_only_no_side_effects",
        "candidate_results": results,
        "blocked_candidate_count": blocked_count,
        "promotion_status": "blocked" if blocked_count else "review_ready",
        "forbidden_action_catalog": sorted(_FORBIDDEN_ACTION_ALIASES),
    }


def validate_candidate_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["packet:not_object"]
    errors: list[str] = []
    if packet.get("schema_version") != SELF_LEARNING_CANDIDATE_PACKET_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    if packet.get("candidate_policy") != "candidate_only":
        errors.append("candidate_policy:must_be_candidate_only")
    if packet.get("apply_policy") != "cannot_apply":
        errors.append("apply_policy:must_be_cannot_apply")
    if packet.get("auto_apply") != "disabled":
        errors.append("auto_apply:must_be_disabled")
    for field in ("provider_calls", "live_eval_services", "target_workspace_writes"):
        if packet.get(field) != "not_performed":
            errors.append(f"{field}:must_be_not_performed")
    if packet.get("external_write_action") != "none":
        errors.append("external_write_action:must_be_none")
    if packet.get("approval_required_before_apply") is not True:
        errors.append("approval_required_before_apply:must_be_true")
    if _contains_raw_private_content(packet):
        errors.append("raw_private_content_not_allowed")
    safety = packet.get("safety_report")
    if not isinstance(safety, dict):
        errors.append("safety_report:required")
    elif safety.get("promotion_status") == "blocked":
        errors.append("safety_report:blocked")
    for candidate in packet.get("candidates", []):
        if not isinstance(candidate, dict):
            errors.append("candidate:not_object")
            continue
        candidate_id = str(candidate.get("candidate_id") or "unknown")
        for field in ("rollback_target", "tests_required", "evidence_refs"):
            if not candidate.get(field):
                errors.append(f"{candidate_id}.{field}:required")
        if candidate.get("external_write_action") != "none":
            errors.append(f"{candidate_id}.external_write_action:must_be_none")
        if candidate.get("auto_apply") != "disabled":
            errors.append(f"{candidate_id}.auto_apply:must_be_disabled")
        if candidate.get("approval_state") != "not_requested":
            errors.append(f"{candidate_id}.approval_state:must_be_not_requested")
    return errors


def load_candidate_packet(workspace: str | Path) -> tuple[dict[str, Any] | None, list[str]]:
    path = Path(workspace) / CANDIDATE_PACKET_RELATIVE_PATH
    if not path.exists():
        return None, []
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except ValueError:
        return None, ["json:invalid"]
    errors = validate_candidate_packet(packet)
    return packet, errors


def summarize_self_learning_candidates(
    workspace: str | Path,
    *,
    metrics_summary: dict[str, Any] | None = None,
    feedback_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    packet, load_errors = load_candidate_packet(workspace)
    if packet is None and load_errors:
        return _summary_from_packet(None, load_errors)
    if packet is None:
        packet = build_self_learning_candidate_packet(
            metrics_summary=metrics_summary,
            feedback_summary=feedback_summary,
        )
    return _summary_from_packet(packet, validate_candidate_packet(packet))


def _summary_from_packet(packet: dict[str, Any] | None, errors: list[str]) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": "self_learning_candidate_summary_v1",
            "status": "invalid_candidate_packet",
            "candidate_count": 0,
            "auto_apply": "disabled",
            "apply_policy": "cannot_apply",
            "errors": errors,
        }
    return {
        "schema_version": "self_learning_candidate_summary_v1",
        "status": packet.get("status", "unknown") if not errors else "candidate_packet_blocked",
        "candidate_count": int(packet.get("candidate_count") or 0),
        "auto_apply": packet.get("auto_apply"),
        "apply_policy": packet.get("apply_policy"),
        "approval_required_before_apply": packet.get("approval_required_before_apply"),
        "provider_calls": packet.get("provider_calls"),
        "target_workspace_writes": packet.get("target_workspace_writes"),
        "external_write_action": packet.get("external_write_action"),
        "safety_report": packet.get("safety_report"),
        "candidate_ids": [str(item.get("candidate_id")) for item in packet.get("candidates", []) if isinstance(item, dict)],
        "validation_errors": errors,
    }


def _candidate(
    *,
    component: str,
    target_id: str,
    reason: str,
    evidence_refs: list[str],
    metric_deltas: dict[str, Any],
    feedback_refs: list[str],
    expected_impact: str,
    risk: str,
    rollback_target: str,
    tests_required: list[str],
) -> dict[str, Any]:
    candidate_id = _stable_id("sll-candidate", component, target_id, reason)
    return {
        "candidate_id": candidate_id,
        "component": component,
        "target_id": target_id,
        "status": "staged_for_review",
        "reason": reason,
        "evidence_refs": evidence_refs,
        "metric_deltas": metric_deltas,
        "feedback_refs": feedback_refs,
        "expected_impact": expected_impact,
        "risk": risk,
        "approval_state": "not_requested",
        "rollback_target": rollback_target,
        "tests_required": tests_required,
        "external_write_action": "none",
        "auto_apply": "disabled",
        "proposed_actions": [
            {
                "action_type": "stage_candidate_packet",
                "effect": "review_only",
            }
        ],
    }


def _metric_evidence_refs(metrics: dict[str, Any]) -> list[str]:
    refs = [str(item) for item in metrics.get("latest_report_paths", []) if str(item)]
    latest_run_id = metrics.get("latest_run_id")
    if latest_run_id:
        refs.append(f"metrics_run:{latest_run_id}")
    return refs or ["metrics_summary"]


def _blocked_action_types(action: Any) -> set[str]:
    if isinstance(action, dict):
        tokens = [str(action.get("action_type") or ""), str(action.get("description") or "")]
    else:
        tokens = [str(action)]
    normalized = " ".join(tokens).lower().replace("-", "_")
    blocked: set[str] = set()
    for canonical, aliases in _FORBIDDEN_ACTION_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            blocked.add(canonical)
    return blocked


def _contains_raw_private_content(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in {"raw_chat", "raw_transcript", "private_source_body", "message_body"}:
                return True
            if _contains_raw_private_content(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_raw_private_content(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        if "raw private chat" in lowered or "raw transcript body" in lowered:
            return True
        return bool(_EMAIL_RE.search(value))
    return False


def _stable_id(*parts: str) -> str:
    digest = hashlib.sha256(":".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"{parts[0]}-{digest}"
