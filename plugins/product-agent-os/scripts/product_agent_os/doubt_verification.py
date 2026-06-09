from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import validate_redaction


DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION = "doubt_verification_packet_v1"
DOUBT_SOURCE_POLICY = "doubt verification packet is evidence ledger, not generated dashboard proof"
COMPLETION_SKEPTIC_SOURCE_POLICY = (
    "completion skeptic recommendation is generated routing guidance, not source of truth"
)

DOUBT_VERDICTS = {
    "pass",
    "revise",
    "needs_more_context",
    "blocked_by_approval",
    "accepted_risk",
    "blocked",
}
CLAIM_STATUSES = {
    "supported",
    "unsupported",
    "contradicted",
    "needs_fresh_check",
    "assumption",
    "accepted_gap",
}
REQUIREMENT_STATUSES = {
    "covered",
    "partial",
    "missing",
    "not_applicable",
    "accepted_gap",
}
EVIDENCE_STATUSES = {
    "available",
    "missing",
    "stale",
    "approval_required",
    "not_applicable",
    "accepted_gap",
}
EVIDENCE_PROVIDERS = {
    "command",
    "source_registry",
    "local_file",
    "fixture_eval",
    "transcript_eval",
    "codex_compatibility",
    "owner_evidence",
    "accepted_gap",
    "status_snapshot",
    "status_dashboard",
    "project_graph",
    "generated_site",
    "not_available",
}
GENERATED_VIEW_PROVIDERS = {"status_snapshot", "status_dashboard", "project_graph", "generated_site"}
RECOMMENDATION_LEVELS = {"skip", "lightweight", "recommended", "required", "approval_blocked", "manual_only"}
ARTIFACT_KINDS = {
    "not_available",
    "runtime_result",
    "handoff_packet",
    "task_row",
    "docs_page",
    "code_change",
    "staged_artifact",
}
ARTIFACT_TYPES = {
    "code",
    "docs",
    "research",
    "architecture",
    "product",
    "review",
    "release",
    "eval",
    "security",
    "data",
    "frontend_runtime",
    "backend_api",
    "plugin_skill",
    "not_available",
}
REF_KINDS = {"not_available", "staged_artifact", "generated_artifact"}
APPROVAL_STATUSES = {"not_required", "required", "approval_blocked"}
REDACTION_STATUSES = {"clean", "redacted", "blocked"}
COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS = {
    "trigger_sources": 8,
    "risk_classes": 8,
    "reasons": 8,
    "skip_reasons": 8,
    "required_evidence": 12,
    "approval_hits": 8,
}
DOUBT_PACKET_LIMITS = {
    "claim_ledger": 20,
    "requirement_ledger": 20,
    "evidence_ledger": 20,
    "gap_ledger": 20,
    "approval_hits": 10,
}
LOCAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:[/\\]|[/\\]Users[/\\]|[/\\]home[/\\]|\\\\)")


def build_completion_skeptic_recommendation(
    *,
    lifecycle_state: str,
    write_policy: str,
    usage_mode: dict[str, Any] | None = None,
    methodology_packet: dict[str, Any] | None = None,
    project_graph_status: dict[str, Any] | None = None,
    agent_skill_metrics_loop: dict[str, Any] | None = None,
) -> dict[str, Any]:
    usage = usage_mode if isinstance(usage_mode, dict) else {}
    methodology = methodology_packet if isinstance(methodology_packet, dict) else {}
    graph = project_graph_status if isinstance(project_graph_status, dict) else {}
    metrics = agent_skill_metrics_loop if isinstance(agent_skill_metrics_loop, dict) else {}
    reasons: list[str] = []
    trigger_sources: list[str] = []
    risk_classes: list[str] = []
    required_evidence = ["current verification evidence", "source artifact ledger", "accepted gaps ledger"]
    approval_hits: list[str] = []

    if lifecycle_state in {"quality_gate", "review_ready", "release_ready"}:
        trigger_sources.append("completion_claim")
        risk_classes.append("verification_gap")
        reasons.append("completion claim needs a second-pass evidence check")
    if lifecycle_state in {"review_ready", "release_ready"}:
        risk_classes.append("release_or_review_claim")
        required_evidence.append("release or review readiness evidence")
    if write_policy == "approved_write":
        risk_classes.append("approved_write_boundary")
        approval_hits.append("workspace write route requires explicit approval")
    if methodology.get("status") in {"present_unverified", "applicable_missing", "evidence_required"}:
        trigger_sources.append("methodology_packet")
        risk_classes.append("methodology_present_unverified")
        reasons.append("methodology evidence is present_unverified")
        required_evidence.append("methodology evidence confirmation")
    if _graph_blocks(graph):
        trigger_sources.append("project_graph_status")
        risk_classes.append("generated_graph_boundary")
        reasons.append("stale or ambiguous graph cannot prove readiness")
        required_evidence.append("source file confirmation")
    if metrics:
        trigger_sources.append("agent_skill_metrics_loop")
        risk_classes.append("generated_metrics_boundary")
        reasons.append("metrics reports are staged evidence only")
        required_evidence.append("metrics source run record")

    primary_usage = str(usage.get("primary") or "")
    if not reasons and primary_usage in {"inspection_only", "docs_only"}:
        status = "lightweight"
        trigger_sources.append(primary_usage)
        risk_classes.append("inspection_only")
        reasons.append("inspection-only or docs-only work still needs claim/evidence separation")
    elif not reasons:
        status = "skip"
    elif approval_hits:
        status = "approval_blocked"
    elif lifecycle_state in {"review_ready", "release_ready"}:
        status = "required"
    else:
        status = "recommended"

    required_evidence = _unique(required_evidence)[: COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["required_evidence"]]
    missing = len(required_evidence)
    accepted_gap = 0
    if methodology.get("status") == "explicit_gap_accepted":
        accepted_gap = 1
        missing = max(0, missing - 1)

    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "recommended_skill": "completion-skeptic",
        "trigger_level": status,
        "trigger_sources": _unique(trigger_sources)[: COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["trigger_sources"]],
        "risk_classes": _unique(risk_classes)[: COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["risk_classes"]],
        "reasons": _unique(reasons)[: COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["reasons"]],
        "skip_reasons": [] if status != "skip" else ["no completion-risk trigger detected"],
        "artifact_under_review": {"kind": "runtime_result", "path": "", "label": lifecycle_state},
        "artifact_type": _artifact_type_for_usage(primary_usage),
        "required_evidence": required_evidence,
        "evidence_summary": {
            "required": len(required_evidence),
            "available": 0,
            "missing": missing,
            "stale": 1 if _graph_blocks(graph) else 0,
            "approval_required": len(approval_hits),
            "accepted_gap": accepted_gap,
        },
        "approval_boundary": {
            "status": "approval_blocked" if approval_hits else "not_required",
            "hits": approval_hits[: COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["approval_hits"]],
        },
        "packet_ref": {"kind": "not_available", "path": "", "digest": ""},
        "safe_next_action": _safe_next_action_for_status(status),
        "source_policy": COMPLETION_SKEPTIC_SOURCE_POLICY,
        "redaction_status": {"status": "clean", "categories": []},
    }


def completion_skeptic_first_response_summary(packet: dict[str, Any]) -> dict[str, Any]:
    evidence = packet.get("evidence_summary") if isinstance(packet.get("evidence_summary"), dict) else {}
    approval = packet.get("approval_boundary") if isinstance(packet.get("approval_boundary"), dict) else {}
    reasons = packet.get("reasons") if isinstance(packet.get("reasons"), list) else []
    return {
        "status": _string(packet.get("status") or "not_available"),
        "trigger_level": _string(packet.get("trigger_level") or packet.get("status") or "not_available"),
        "top_reason": _string(reasons[0] if reasons else ""),
        "missing_evidence_count": _int(evidence.get("missing")),
        "approval_required_count": len(approval.get("hits", [])) if isinstance(approval.get("hits"), list) else 0,
        "safe_next_action": _string(packet.get("safe_next_action")),
    }


def validate_completion_skeptic_recommendation_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["completion_skeptic_recommendation:invalid"]
    errors: list[str] = []
    prefix = "completion_skeptic_recommendation"
    if packet.get("schema_version") != 1:
        errors.append(f"{prefix}.schema_version:must_be_1")
    if packet.get("write_policy") != "read_only":
        errors.append(f"{prefix}.write_policy:must_be_read_only")
    status = packet.get("status")
    trigger_level = packet.get("trigger_level")
    if status not in RECOMMENDATION_LEVELS:
        errors.append(f"{prefix}.status:invalid")
    if trigger_level not in RECOMMENDATION_LEVELS:
        errors.append(f"{prefix}.trigger_level:invalid")
    if packet.get("recommended_skill") != "completion-skeptic":
        errors.append(f"{prefix}.recommended_skill:invalid")
    for field, limit in COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS.items():
        if field == "approval_hits":
            continue
        value = packet.get(field)
        if not isinstance(value, list):
            errors.append(f"{prefix}.{field}:invalid")
        elif len(value) > limit:
            errors.append(f"{prefix}.{field}:too_many")
    if status in {"recommended", "required", "approval_blocked", "manual_only"}:
        if not packet.get("trigger_sources"):
            errors.append(f"{prefix}.trigger_sources:required")
        if not packet.get("reasons"):
            errors.append(f"{prefix}.reasons:required")
    if packet.get("artifact_type") not in ARTIFACT_TYPES:
        errors.append(f"{prefix}.artifact_type:invalid")
    errors.extend(_validate_ref_packet(packet.get("artifact_under_review"), f"{prefix}.artifact_under_review", ARTIFACT_KINDS))
    errors.extend(_validate_ref_packet(packet.get("packet_ref"), f"{prefix}.packet_ref", REF_KINDS))
    errors.extend(_validate_evidence_summary(packet.get("evidence_summary"), f"{prefix}.evidence_summary"))
    approval = packet.get("approval_boundary")
    if not isinstance(approval, dict):
        errors.append(f"{prefix}.approval_boundary:invalid")
    else:
        if approval.get("status") not in APPROVAL_STATUSES:
            errors.append(f"{prefix}.approval_boundary.status:invalid")
        hits = approval.get("hits")
        if not isinstance(hits, list):
            errors.append(f"{prefix}.approval_boundary.hits:invalid")
        elif len(hits) > COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["approval_hits"]:
            errors.append(f"{prefix}.approval_boundary.hits:too_many")
        if status == "approval_blocked" and not hits:
            errors.append(f"{prefix}.approval_boundary.hits:required")
    if not _non_empty_string(packet.get("safe_next_action")):
        errors.append(f"{prefix}.safe_next_action:required")
    if packet.get("source_policy") != COMPLETION_SKEPTIC_SOURCE_POLICY:
        errors.append(f"{prefix}.source_policy:invalid")
    errors.extend(_validate_redaction_status(packet.get("redaction_status"), f"{prefix}.redaction_status"))
    if _contains_unsafe_text(packet):
        errors.append(f"{prefix}:contains_local_path")
    return errors


def validate_doubt_verification_packet_file(path: Path) -> list[str]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ["unable to read file as utf-8 text"]
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"invalid json: {exc}"]
    return validate_doubt_verification_packet(payload)


def validate_doubt_verification_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["doubt_verification_packet:invalid"]
    errors: list[str] = []
    if packet.get("schema_version") != DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION:
        errors.append(f"schema_version:must_be_{DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION}")
    verdict = packet.get("verdict")
    if verdict not in DOUBT_VERDICTS:
        errors.append("verdict:required")
    errors.extend(_validate_ref_packet(packet.get("artifact_under_review"), "artifact_under_review", ARTIFACT_KINDS))
    errors.extend(_validate_claim_ledger(packet.get("claim_ledger"), verdict))
    errors.extend(_validate_requirement_ledger(packet.get("requirement_ledger"), verdict))
    errors.extend(_validate_evidence_ledger(packet.get("evidence_ledger"), verdict))
    approval = packet.get("approval_boundary")
    if not isinstance(approval, dict):
        errors.append("approval_boundary:invalid")
    else:
        if approval.get("status") not in APPROVAL_STATUSES:
            errors.append("approval_boundary.status:invalid")
        hits = approval.get("hits")
        if not isinstance(hits, list):
            errors.append("approval_boundary.hits:invalid")
        elif len(hits) > DOUBT_PACKET_LIMITS["approval_hits"]:
            errors.append("approval_boundary.hits:too_many")
    gap_ledger = packet.get("gap_ledger")
    if not isinstance(gap_ledger, list):
        errors.append("gap_ledger:invalid")
    elif len(gap_ledger) > DOUBT_PACKET_LIMITS["gap_ledger"]:
        errors.append("gap_ledger:too_many")
    handoff = packet.get("handoff")
    if not isinstance(handoff, dict):
        errors.append("handoff:invalid")
    else:
        for field in ["verified_claims", "unsupported_claims", "verification_evidence"]:
            if not isinstance(handoff.get(field), list):
                errors.append(f"handoff.{field}:invalid")
        for field in ["stop_reason", "recommended_next_role"]:
            if not _non_empty_string(handoff.get(field)):
                errors.append(f"handoff.{field}:required")
    if packet.get("source_policy") != DOUBT_SOURCE_POLICY:
        errors.append("source_policy:invalid")
    errors.extend(_validate_redaction_status(packet.get("redaction_status"), "redaction_status"))
    if _contains_unsafe_text(packet):
        errors.append("doubt_verification_packet:contains_local_path")
    return errors


def main_doubt_verification(argv: list[str]) -> int:
    if not argv:
        return print_json(
            {
                "ok": False,
                "path": "",
                "schema_version": DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
                "errors": ["doubt verification packet path is required"],
            }
        )
    path = Path(argv[0])
    errors = validate_doubt_verification_packet_file(path)
    return print_json(
        {
            "ok": not errors,
            "path": str(path),
            "schema_version": DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
            "errors": errors,
        }
    )


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok") else 1


def _validate_claim_ledger(value: Any, verdict: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return ["claim_ledger:invalid"]
    if len(value) > DOUBT_PACKET_LIMITS["claim_ledger"]:
        errors.append("claim_ledger:too_many")
    for index, item in enumerate(value):
        prefix = f"claim_ledger[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}:invalid")
            continue
        if not _non_empty_string(item.get("claim_id")):
            errors.append(f"{prefix}.claim_id:required")
        if not _non_empty_string(item.get("claim")):
            errors.append(f"{prefix}.claim:required")
        status = item.get("status")
        if status not in CLAIM_STATUSES:
            errors.append(f"{prefix}.status:invalid")
        if verdict == "pass" and status in {"unsupported", "contradicted", "needs_fresh_check"}:
            errors.append(f"{prefix}.status:blocks_pass_verdict")
        errors.extend(_validate_provenance(item.get("provenance"), f"{prefix}.provenance"))
    return errors


def _validate_requirement_ledger(value: Any, verdict: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return ["requirement_ledger:invalid"]
    if len(value) > DOUBT_PACKET_LIMITS["requirement_ledger"]:
        errors.append("requirement_ledger:too_many")
    for index, item in enumerate(value):
        prefix = f"requirement_ledger[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}:invalid")
            continue
        if not _non_empty_string(item.get("requirement_id")):
            errors.append(f"{prefix}.requirement_id:required")
        if item.get("status") not in REQUIREMENT_STATUSES:
            errors.append(f"{prefix}.status:invalid")
        if verdict == "pass" and item.get("status") in {"partial", "missing"}:
            errors.append(f"{prefix}.status:blocks_pass_verdict")
        errors.extend(_validate_provenance(item.get("provenance"), f"{prefix}.provenance"))
    return errors


def _validate_evidence_ledger(value: Any, verdict: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return ["evidence_ledger:invalid"]
    if len(value) > DOUBT_PACKET_LIMITS["evidence_ledger"]:
        errors.append("evidence_ledger:too_many")
    for index, item in enumerate(value):
        prefix = f"evidence_ledger[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix}:invalid")
            continue
        if not _non_empty_string(item.get("evidence_id")):
            errors.append(f"{prefix}.evidence_id:required")
        provider = item.get("evidence_provider")
        if provider not in EVIDENCE_PROVIDERS:
            errors.append(f"{prefix}.evidence_provider:invalid")
        status = item.get("status")
        if status not in EVIDENCE_STATUSES:
            errors.append(f"{prefix}.status:invalid")
        if status == "available" and not _non_empty_string(item.get("evidence_ref")):
            errors.append(f"{prefix}.evidence_ref:required")
        if provider in GENERATED_VIEW_PROVIDERS and item.get("evidence_role") != "orientation":
            errors.append(f"{prefix}.provider:generated_view_not_completion_proof")
        if verdict == "pass" and status in {"missing", "stale", "approval_required"}:
            errors.append(f"{prefix}.status:blocks_pass_verdict")
        errors.extend(_validate_provenance(item.get("provenance"), f"{prefix}.provenance"))
    return errors


def _validate_provenance(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{prefix}:required"]
    errors: list[str] = []
    for field in ["kind", "ref", "checked_at"]:
        if not _non_empty_string(value.get(field)):
            errors.append(f"{prefix}.{field}:required")
    return errors


def _validate_ref_packet(value: Any, prefix: str, allowed_kinds: set[str]) -> list[str]:
    if not isinstance(value, dict):
        return [f"{prefix}:invalid"]
    errors: list[str] = []
    kind = value.get("kind")
    if kind not in allowed_kinds:
        errors.append(f"{prefix}.kind:invalid")
    path = _string(value.get("path"))
    if path:
        if path.startswith(("http://", "https://")):
            errors.append(f"{prefix}.path:external_url_forbidden")
        elif not _safe_relative_path(path):
            errors.append(f"{prefix}.path:absolute_or_unsafe")
    digest = value.get("digest")
    if digest not in (None, "") and not _non_empty_string(digest):
        errors.append(f"{prefix}.digest:invalid")
    return errors


def _validate_evidence_summary(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{prefix}:invalid"]
    errors: list[str] = []
    for field in ["required", "available", "missing", "stale", "approval_required", "accepted_gap"]:
        if field not in value:
            errors.append(f"{prefix}.{field}:required")
        elif _int(value.get(field)) < 0:
            errors.append(f"{prefix}.{field}:invalid")
    return errors


def _validate_redaction_status(value: Any, prefix: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{prefix}:invalid"]
    errors: list[str] = []
    if value.get("status") not in REDACTION_STATUSES:
        errors.append(f"{prefix}.status:invalid")
    if not isinstance(value.get("categories"), list):
        errors.append(f"{prefix}.categories:invalid")
    return errors


def _safe_relative_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if not normalized:
        return True
    if normalized.startswith(("/", "../", "~")):
        return False
    if ":/" in normalized:
        return False
    return ".." not in normalized.split("/")


def _contains_unsafe_text(packet: Any) -> bool:
    rendered = json.dumps(packet, sort_keys=True, ensure_ascii=False)
    return bool(validate_redaction(rendered) or LOCAL_PATH_PATTERN.search(rendered))


def _graph_blocks(packet: dict[str, Any]) -> bool:
    if not packet:
        return False
    if packet.get("status") in {"stale", "ambiguous", "unsupported"}:
        return True
    freshness = packet.get("freshness")
    return isinstance(freshness, dict) and freshness.get("status") in {"stale", "ambiguous"}


def _artifact_type_for_usage(primary_usage: str) -> str:
    return {
        "docs_only": "docs",
        "security_sensitive_change": "security",
        "release_packaging": "release",
        "ai_eval_regression": "eval",
        "data_migration": "data",
        "native_mobile_feature": "code",
        "desktop_local_first": "code",
    }.get(primary_usage, "plugin_skill")


def _safe_next_action_for_status(status: str) -> str:
    if status == "skip":
        return "Continue with normal verification; do not claim completion without current evidence."
    if status == "approval_blocked":
        return "Request explicit approval or accepted gap before claiming completion."
    return "Run completion-skeptic before claiming completion."


def _string(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


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
