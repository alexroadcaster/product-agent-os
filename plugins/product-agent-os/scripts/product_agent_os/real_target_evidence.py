"""Read-only evidence normalization for real-target Product-Agent OS retests."""

from __future__ import annotations

from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


REAL_TARGET_EVIDENCE_SCHEMA_VERSION = "real_target_evidence_summary_v1"


def normalize_real_target_evidence(
    *,
    target_label: str,
    detect_project_output: dict[str, Any] | None = None,
    first_run_dry_run_output: dict[str, Any] | None = None,
    runtime_contract_output: dict[str, Any] | None = None,
    source_policy_output: dict[str, Any] | None = None,
    methodology_audit_output: dict[str, Any] | None = None,
    project_graph_output: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize nested tool packets into stable summary fields for retest ledgers."""

    summary: dict[str, Any] = {
        "schema_version": REAL_TARGET_EVIDENCE_SCHEMA_VERSION,
        "target_label": str(target_label),
        "write_policy": "read_only_summary_only",
        "detect_project_summary": normalize_detect_project_summary(detect_project_output or {}),
        "first_run_dry_run_summary": normalize_first_run_dry_run_summary(first_run_dry_run_output or {}),
        "runtime_contract_summary": normalize_runtime_contract_summary(runtime_contract_output or {}),
        "source_policy_summary": normalize_source_policy_summary(source_policy_output or {}),
        "methodology_audit_summary": normalize_methodology_audit_summary(methodology_audit_output or {}),
        "project_graph_summary": normalize_project_graph_summary(project_graph_output or {}),
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def normalize_detect_project_summary(packet: dict[str, Any]) -> dict[str, Any]:
    usage_mode = _dict(packet.get("usage_mode"))
    generated_inputs = _dict(packet.get("generated_artifact_inputs"))
    first_run_inputs = _dict(generated_inputs.get("first_run_analysis"))
    return {
        "status": str(packet.get("status") or "ok" if packet else "not_available"),
        "usage_mode_primary": _string_or_none(usage_mode.get("primary")),
        "usage_mode_confidence": _string_or_none(usage_mode.get("confidence")),
        "usage_mode_reasons": _string_list(usage_mode.get("reasons")),
        "detected_stack": _string_list(packet.get("detected_stack")),
        "existing_control_plane": _string_list(packet.get("existing_control_plane")),
        "missing_control_plane": _string_list(packet.get("missing_control_plane")),
        "risk_count": len(_list(packet.get("risks"))),
        "risks": _string_list(packet.get("risks"))[:10],
        "first_run_analysis_input_status": _string_or_none(first_run_inputs.get("status")),
    }


def normalize_first_run_dry_run_summary(packet: dict[str, Any]) -> dict[str, Any]:
    first_run_packet = _packet_payload(packet)
    generated_pages = _list(first_run_packet.get("generated_pages"))
    return {
        "status": str(packet.get("status") or first_run_packet.get("status") or "not_available"),
        "mode": _string_or_none(packet.get("mode")),
        "schema_version": _string_or_none(first_run_packet.get("schema_version")),
        "write_policy": _string_or_none(first_run_packet.get("write_policy")),
        "generated_view_policy": _string_or_none(first_run_packet.get("generated_view_policy")),
        "packet_digest": _string_or_none(first_run_packet.get("packet_digest")),
        "safe_next_action": _string_or_none(first_run_packet.get("safe_next_action")),
        "graph_depth_summary": _bounded_graph_depth_summary(first_run_packet.get("graph_depth_summary")),
        "first_run_page_count": len(generated_pages),
        "written_file_count": len(_list(packet.get("written_files"))),
    }


def normalize_runtime_contract_summary(packet: dict[str, Any]) -> dict[str, Any]:
    route_packet = _dict(packet.get("route_packet"))
    usage_mode = _dict(packet.get("usage_mode") or route_packet.get("usage_mode"))
    return {
        "status": str(packet.get("status") or "not_available"),
        "usage_mode_primary": _string_or_none(packet.get("usage_mode_primary") or usage_mode.get("primary")),
        "usage_mode_reasons": _string_list(usage_mode.get("reasons"))[:10],
        "route_id": _string_or_none(packet.get("route_id")),
        "approval_required": bool(packet.get("approval_required", False)),
        "source_policy_status": _string_or_none(packet.get("source_policy_status")),
        "errors": _string_list(packet.get("errors"))[:10],
    }


def normalize_source_policy_summary(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": str(packet.get("status") or "not_available"),
        "source_policy_status": _string_or_none(packet.get("source_policy_status") or packet.get("policy_status")),
        "blocker_count": len(_list(packet.get("blockers"))),
        "unsupported_claims": _string_list(packet.get("unsupported_claims"))[:10],
    }


def normalize_methodology_audit_summary(packet: dict[str, Any]) -> dict[str, Any]:
    first_safe_action = _dict(packet.get("first_safe_action"))
    return {
        "status": str(packet.get("status") or "not_available"),
        "recommendation_count": len(_list(packet.get("recommendations"))),
        "recommendation_group_count": len(_list(packet.get("recommendation_groups"))),
        "first_safe_action_count": len(_list(first_safe_action.get("recommendations"))),
        "first_safe_action_policy": _string_or_none(first_safe_action.get("policy")),
        "safe_next_action": _string_or_none(packet.get("safe_next_action") or first_safe_action.get("safe_next_action")),
    }


def normalize_project_graph_summary(packet: dict[str, Any]) -> dict[str, Any]:
    validation = _dict(packet.get("validation"))
    metadata = _dict(packet.get("metadata"))
    scope_policy = _dict(metadata.get("scope_policy") or packet.get("scope_policy"))
    coverage = _dict(metadata.get("coverage_map") or packet.get("coverage_map") or packet.get("coverage"))
    freshness = _dict(metadata.get("temporal_delta") or packet.get("freshness"))
    rejected_links = _list(metadata.get("rejected_links") or packet.get("rejected_links"))
    conservative_linker = _dict(metadata.get("conservative_linker"))
    ts_js = _dict(metadata.get("typescript_javascript_scanner"))
    framework_semantics = _dict(
        ts_js.get("framework_semantics")
        or metadata.get("framework_semantics")
        or packet.get("framework_semantic_summary")
    )
    if packet.get("status"):
        status = str(packet.get("status"))
    elif validation.get("ok") is True:
        status = "ok"
    elif validation.get("errors"):
        status = "blocked"
    else:
        status = "not_available"
    return {
        "status": status,
        "validation_ok": bool(validation.get("ok", False)),
        "validation_errors": _string_list(validation.get("errors")),
        "node_count": _int_or_zero(packet.get("node_count") or len(_list(packet.get("nodes")))),
        "edge_count": _int_or_zero(packet.get("edge_count") or len(_list(packet.get("edges")))),
        "observation_count": _int_or_zero(packet.get("observation_count") or len(_list(packet.get("observations")))),
        "scope_policy_status": _string_or_none(scope_policy.get("status")),
        "excluded_prefixes": _string_list(scope_policy.get("excluded_prefixes")),
        "coverage": _bounded_coverage_summary(coverage),
        "freshness": _bounded_freshness_summary(freshness),
        "rejected_link_summary": _bounded_rejected_link_summary(rejected_links, conservative_linker),
        "framework_semantic_summary": _bounded_framework_summary(framework_semantics),
    }


def _bounded_graph_depth_summary(value: Any) -> dict[str, Any]:
    packet = _dict(value)
    return {
        "status": str(packet.get("status") or "not_available"),
        "coverage": _bounded_coverage_summary(_dict(packet.get("coverage"))),
        "freshness": _bounded_freshness_summary(_dict(packet.get("freshness"))),
        "rejected_link_summary": _bounded_counter_summary(_dict(packet.get("rejected_link_summary"))),
        "framework_semantic_summary": _bounded_counter_summary(_dict(packet.get("framework_semantic_summary"))),
        "generated_view_policy": _string_or_none(packet.get("generated_view_policy")),
    }


def _bounded_coverage_summary(packet: dict[str, Any]) -> dict[str, Any]:
    unsupported = packet.get("unsupported_languages")
    skipped = packet.get("skipped_reasons")
    return {
        "status": str(packet.get("status") or "not_available"),
        "supported_file_count": _int_or_zero(packet.get("supported_file_count")),
        "partial_file_count": _int_or_zero(packet.get("partial_file_count")),
        "unsupported_file_count": _int_or_zero(packet.get("unsupported_file_count")),
        "unsupported_languages": _bounded_string_counter(_dict(unsupported)),
        "skipped_reasons": _bounded_string_counter(_dict(skipped)),
        "recommended_next_parser_or_linker_action": _string_or_none(
            packet.get("recommended_next_parser_or_linker_action")
        ),
    }


def _bounded_freshness_summary(packet: dict[str, Any]) -> dict[str, Any]:
    status = str(packet.get("status") or "not_available")
    return {
        "status": status,
        "changed_edge_count": _int_or_zero(packet.get("changed_edge_count")),
        "removed_edge_count": _int_or_zero(packet.get("removed_edge_count")),
        "blocks_action_claims": bool(packet.get("blocks_action_claims", status != "current")),
    }


def _bounded_rejected_link_summary(rejected_links: list[Any], conservative_linker: dict[str, Any]) -> dict[str, Any]:
    by_reason: dict[str, int] = {}
    for item in rejected_links:
        reason = _string_or_none(_dict(item).get("reason")) or "unknown"
        by_reason[reason] = by_reason.get(reason, 0) + 1
    total = len(rejected_links) if rejected_links else _int_or_zero(conservative_linker.get("rejected_link_count"))
    return {
        "total": total,
        "by_reason": {key: by_reason[key] for key in sorted(by_reason)[:10]},
    }


def _bounded_framework_summary(packet: dict[str, Any]) -> dict[str, Any]:
    frameworks = _dict(packet.get("frameworks"))
    total = _int_or_zero(packet.get("framework_count") or packet.get("total") or sum(_int_or_zero(item) for item in frameworks.values()))
    return {
        "total": total,
        "frameworks": {key: _int_or_zero(frameworks[key]) for key in sorted(frameworks)[:10]},
    }


def _bounded_counter_summary(packet: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "total": _int_or_zero(packet.get("total")),
    }
    by_reason = _bounded_string_counter(_dict(packet.get("by_reason")))
    frameworks = _bounded_string_counter(_dict(packet.get("frameworks")))
    if by_reason:
        summary["by_reason"] = by_reason
    if frameworks:
        summary["frameworks"] = frameworks
    return summary


def _bounded_string_counter(packet: dict[str, Any]) -> dict[str, str]:
    return {str(key): str(packet[key]) for key in sorted(packet)[:10] if str(key)}


def _packet_payload(packet: dict[str, Any]) -> dict[str, Any]:
    wrapped = packet.get("packet")
    if isinstance(wrapped, dict):
        return wrapped
    return packet


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [str(item) for item in _list(value)]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


__all__ = [
    "REAL_TARGET_EVIDENCE_SCHEMA_VERSION",
    "normalize_detect_project_summary",
    "normalize_first_run_dry_run_summary",
    "normalize_methodology_audit_summary",
    "normalize_project_graph_summary",
    "normalize_real_target_evidence",
    "normalize_runtime_contract_summary",
    "normalize_source_policy_summary",
]
