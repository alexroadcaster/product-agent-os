"""Local search-quality eval packets for Product-Agent OS project graphs."""

from __future__ import annotations

from typing import Any

from product_agent_os.project_graph_queries import query_project_graph
from product_agent_os.project_graph_sanitization import sanitize_graph_text


DEFAULT_SEARCH_QUALITY_THRESHOLDS = {
    "min_symbol_recall": 0.8,
    "min_top_k_mrr": 0.5,
    "min_trace_success_rate": 0.8,
    "min_affected_test_precision": 0.8,
    "max_edge_density": 10.0,
}


def evaluate_project_graph_search_quality(
    graph: dict[str, Any],
    *,
    cases: list[dict[str, Any]],
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Evaluate deterministic graph query quality without source reads or external calls."""

    applied_thresholds = {**DEFAULT_SEARCH_QUALITY_THRESHOLDS, **(thresholds or {})}
    evaluated_cases = [_evaluate_case(graph, case) for case in cases if isinstance(case, dict)]
    metrics = _quality_metrics(graph, evaluated_cases)
    failed_thresholds = _failed_thresholds(metrics, applied_thresholds)
    decision_status = "passed" if not failed_thresholds and evaluated_cases else "blocked"
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "decision_status": decision_status,
        "source_boundary": "graph_artifact_only_raw_source_excluded",
        "generated_view_policy": "quality_packet_is_orientation_evidence_only",
        "approval_boundary": "local_fixture_only_no_live_backend_or_model_calls",
        "quality_metrics": metrics,
        "thresholds": {
            "explicit_thresholds_required_before_closure": bool(thresholds),
            **applied_thresholds,
        },
        "failed_thresholds": failed_thresholds,
        "cases": evaluated_cases,
        "safe_next_action": "Use search-quality evals as local structural evidence only; read source before edits or completion claims.",
    }


def _evaluate_case(graph: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    query = str(case.get("query") or "")
    if query == "search":
        return _evaluate_search_case(graph, case)
    if query == "trace":
        return _evaluate_trace_case(graph, case)
    if query == "affected_tests":
        return _evaluate_affected_tests_case(graph, case)
    return {
        "id": _case_id(case),
        "query": sanitize_graph_text(query),
        "status": "failed",
        "failure_label": "unsupported_case_query",
    }


def _evaluate_search_case(graph: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    top_k = _positive_int(case.get("top_k"), 5)
    packet = query_project_graph(
        graph,
        {
            "query": "search",
            "text": sanitize_graph_text(case.get("text") or ""),
            "max_results": max(top_k, 1),
        },
    )
    result_ids = [str(node.get("id")) for node in packet.get("nodes", []) if isinstance(node, dict)]
    expected_ids = [str(item) for item in case.get("expected_node_ids", []) if item]
    hits = [item for item in expected_ids if item in result_ids[:top_k]]
    first_rank = _first_rank(result_ids, expected_ids)
    return {
        "id": _case_id(case),
        "query": "search",
        "status": "passed" if expected_ids and len(hits) == len(expected_ids) else "failed",
        "result_status": packet.get("status"),
        "expected_node_count": len(expected_ids),
        "hit_count": len(hits),
        "top_k": top_k,
        "first_relevant_rank": first_rank,
        "reciprocal_rank": 0.0 if first_rank == 0 else 1.0 / first_rank,
    }


def _evaluate_trace_case(graph: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    packet = query_project_graph(
        graph,
        {
            "query": "trace",
            "source_id": sanitize_graph_text(case.get("source_id") or case.get("node_id") or ""),
            "target_id": sanitize_graph_text(case.get("target_id") or ""),
            "max_depth": _positive_int(case.get("max_depth"), 6),
        },
    )
    expected_status = str(case.get("expected_status") or "ok")
    trace_label = str(packet.get("status") or "not_available")
    return {
        "id": _case_id(case),
        "query": "trace",
        "status": "passed" if trace_label == expected_status else "failed",
        "trace_label": trace_label,
        "expected_status": expected_status,
        "path_length": len(packet.get("trace", [])) if isinstance(packet.get("trace"), list) else 0,
    }


def _evaluate_affected_tests_case(graph: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    packet = query_project_graph(
        graph,
        {
            "query": "affected_tests",
            "node_id": sanitize_graph_text(case.get("node_id") or ""),
            "max_results": _positive_int(case.get("max_results"), 25),
        },
    )
    result_ids = [str(node.get("id")) for node in packet.get("tests", []) if isinstance(node, dict)]
    expected_ids = [str(item) for item in case.get("expected_test_ids", []) if item]
    hits = [item for item in expected_ids if item in result_ids]
    precision = 0.0 if not result_ids else len(hits) / len(result_ids)
    return {
        "id": _case_id(case),
        "query": "affected_tests",
        "status": "passed" if expected_ids and len(hits) == len(expected_ids) else "failed",
        "expected_test_count": len(expected_ids),
        "returned_test_count": len(result_ids),
        "hit_count": len(hits),
        "precision": round(precision, 4),
        "coverage_status": packet.get("coverage_status", "not_available"),
    }


def _quality_metrics(graph: dict[str, Any], cases: list[dict[str, Any]]) -> dict[str, float]:
    search_cases = [case for case in cases if case.get("query") == "search"]
    trace_cases = [case for case in cases if case.get("query") == "trace"]
    affected_cases = [case for case in cases if case.get("query") == "affected_tests"]
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    node_count = _positive_int(metadata.get("node_count") or len(graph.get("nodes", [])), 1)
    edge_count = _positive_int(metadata.get("edge_count") or len(graph.get("edges", [])), 0)
    return {
        "symbol_recall": _average(_case_ratio(case, "hit_count", "expected_node_count") for case in search_cases),
        "top_k_mrr": _average(float(case.get("reciprocal_rank") or 0.0) for case in search_cases),
        "trace_success_rate": _pass_rate(trace_cases),
        "affected_test_precision": _average(float(case.get("precision") or 0.0) for case in affected_cases),
        "edge_density": round(edge_count / max(node_count, 1), 4),
    }


def _failed_thresholds(metrics: dict[str, float], thresholds: dict[str, float]) -> list[str]:
    failures: list[str] = []
    minimums = {
        "symbol_recall": "min_symbol_recall",
        "top_k_mrr": "min_top_k_mrr",
        "trace_success_rate": "min_trace_success_rate",
        "affected_test_precision": "min_affected_test_precision",
    }
    for metric, threshold_name in minimums.items():
        if float(metrics.get(metric) or 0.0) < float(thresholds.get(threshold_name) or 0.0):
            failures.append(f"{metric}_below_threshold")
    if float(metrics.get("edge_density") or 0.0) > float(thresholds.get("max_edge_density") or 0.0):
        failures.append("edge_density_above_threshold")
    return failures


def _case_ratio(case: dict[str, Any], numerator: str, denominator: str) -> float:
    total = _positive_int(case.get(denominator), 0)
    if total <= 0:
        return 0.0
    return _positive_int(case.get(numerator), 0) / total


def _pass_rate(cases: list[dict[str, Any]]) -> float:
    if not cases:
        return 1.0
    return sum(1 for case in cases if case.get("status") == "passed") / len(cases)


def _average(values: Any) -> float:
    materialized = [float(value) for value in values]
    if not materialized:
        return 1.0
    return round(sum(materialized) / len(materialized), 4)


def _first_rank(result_ids: list[str], expected_ids: list[str]) -> int:
    for index, result_id in enumerate(result_ids, start=1):
        if result_id in expected_ids:
            return index
    return 0


def _case_id(case: dict[str, Any]) -> str:
    return sanitize_graph_text(case.get("id") or "unnamed-case")[:80]


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default
