"""Bounded graph-only query packets for Product-Agent OS project graphs."""

from __future__ import annotations

import hashlib
import json
import re
from collections import deque
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_index import (
    graph_content_fingerprint,
    query_static_search_index,
    validate_static_search_index,
)
from product_agent_os.project_graph_ontology import default_ontology


MAX_QUERY_TEXT_LENGTH = 120
DEFAULT_MAX_RESULTS = 25
DEFAULT_MAX_TOKENS = 4_000
DEFAULT_HUB_THRESHOLD = 100
MAX_QUERY_DEPTH = 25
MAX_QUERY_RESULTS = 250
MAX_QUERY_TOKENS = 20_000
MAX_HUB_THRESHOLD = 1_000
QUERY_KINDS = {
    "neighbors",
    "path",
    "node",
    "status",
    "search",
    "hotspots",
    "read_order",
    "trace",
    "impact",
    "affected_tests",
    "agent_reading_packet",
    "changed_since",
    "why_changed",
}
_ONTOLOGY = default_ontology()
_ALLOWED_NODE_TYPES = set(str(item) for item in _ONTOLOGY["node_types"])
_ALLOWED_EDGE_TYPES = set(str(item) for item in _ONTOLOGY["edge_types"])
_ALLOWED_CONFIDENCE = set(str(item) for item in _ONTOLOGY["confidence_levels"])


def load_graph_artifact(path: str | Path) -> dict[str, Any]:
    """Load a graph JSON or JSONL artifact without reading workspace source files."""

    graph_path = Path(path)
    text = graph_path.read_text(encoding="utf-8")
    if graph_path.suffix.lower() == ".jsonl":
        graph: dict[str, Any] = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {},
            "nodes": [],
            "edges": [],
            "observations": [],
        }
        for line in text.splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            kind = record.get("record_kind")
            payload = record.get("payload")
            if kind == "metadata" and isinstance(payload, dict):
                graph["metadata"] = payload
            elif kind == "node" and isinstance(payload, dict):
                graph["nodes"].append(payload)
            elif kind == "edge" and isinstance(payload, dict):
                graph["edges"].append(payload)
            elif kind == "observation" and isinstance(payload, dict):
                graph["observations"].append(payload)
        return graph
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("graph artifact must be a JSON object")
    return payload


def query_project_graph(
    graph: dict[str, Any],
    request: dict[str, Any],
    *,
    static_index: dict[str, Any] | None = None,
    semantic_index: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run a deterministic query against graph JSON/JSONL content only."""

    errors = _validate_request(request)
    kind = str(request.get("query") or "")
    if errors:
        return _packet(graph, request, kind or "invalid", status="blocked", errors=errors)
    index = _index_graph(graph)
    if kind == "neighbors":
        return _neighbors(graph, index, request)
    if kind == "path":
        return _path_packet(graph, index, request, result_kind="path")
    if kind == "trace":
        return _path_packet(graph, index, request, result_kind="trace")
    if kind == "node":
        node = index["nodes"].get(str(request.get("node_id") or ""))
        return _packet(graph, request, kind, nodes=[node] if node else [], status="ok" if node else "not_found")
    if kind == "status":
        return _status_packet(graph, request)
    if kind == "search":
        return _search(graph, index, request, static_index=static_index, semantic_index=semantic_index)
    if kind == "hotspots":
        return _hotspots(graph, index, request)
    if kind == "read_order":
        return _read_order(graph, index, request)
    if kind == "impact":
        return _impact(graph, index, request)
    if kind == "affected_tests":
        return _affected_tests(graph, index, request)
    if kind == "agent_reading_packet":
        return _agent_reading_packet(graph, index, request)
    if kind == "changed_since":
        return _changed_since(graph, request)
    if kind == "why_changed":
        return _why_changed(graph, request)
    return _packet(graph, request, kind, status="blocked", errors=["query:unknown"])


def _validate_request(request: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = request.get("query")
    if kind not in QUERY_KINDS:
        errors.append("query:unknown")
    text = request.get("text")
    if isinstance(text, str) and len(text) > MAX_QUERY_TEXT_LENGTH:
        errors.append("query:text_too_long")
    for key in ["path_prefixes"]:
        value = request.get(key)
        if value is None:
            continue
        if not isinstance(value, list) or any(not _safe_relative_path(str(item)) for item in value):
            errors.append(f"query:{key}:invalid")
    allowed_values = {
        "node_types": _ALLOWED_NODE_TYPES,
        "edge_types": _ALLOWED_EDGE_TYPES,
        "confidence": _ALLOWED_CONFIDENCE,
    }
    for key in ["node_types", "edge_types", "confidence"]:
        value = request.get(key)
        if value is None:
            continue
        if not isinstance(value, list):
            errors.append(f"query:{key}:invalid")
            continue
        if any(str(item) not in allowed_values[key] for item in value):
            errors.append(f"query:{key}:unknown")
    for key, max_value in [
        ("max_depth", MAX_QUERY_DEPTH),
        ("max_results", MAX_QUERY_RESULTS),
        ("max_tokens", MAX_QUERY_TOKENS),
        ("hub_threshold", MAX_HUB_THRESHOLD),
    ]:
        errors.extend(_validate_positive_int_limit(request, key, max_value))
    return errors


def _validate_positive_int_limit(request: dict[str, Any], key: str, max_value: int) -> list[str]:
    if key not in request:
        return []
    value = request.get(key)
    if isinstance(value, bool):
        return [f"query:{key}:invalid"]
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return [f"query:{key}:invalid"]
    if parsed <= 0:
        return [f"query:{key}:invalid"]
    if parsed > max_value:
        return [f"query:{key}:too_large"]
    return []


def _neighbors(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    edges = index["adjacent"].get(node_id, [])
    hub_threshold = _positive_int(request.get("hub_threshold"), DEFAULT_HUB_THRESHOLD)
    truncation_reasons: list[str] = []
    if len(edges) > hub_threshold:
        edges = edges[:hub_threshold]
        truncation_reasons.append("hub_suppressed")
    edges = _filter_edges(edges, request)
    nodes = [index["nodes"].get(_other(edge, node_id)) for edge in edges]
    return _packet(
        graph,
        request,
        "neighbors",
        nodes=[node for node in nodes if node],
        edges=edges,
        status="ok",
        truncation_reasons=truncation_reasons,
        omitted_count=max(0, len(index["adjacent"].get(node_id, [])) - len(edges)),
    )


def _path_packet(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any], *, result_kind: str) -> dict[str, Any]:
    source = str(request.get("node_id") or request.get("source_id") or "")
    target = str(request.get("target_id") or "")
    max_depth = _positive_int(request.get("max_depth"), 6)
    node_path, edge_path = _shortest_path(index, source, target, max_depth=max_depth)
    payload_key = "trace" if result_kind == "trace" else "path"
    packet = _packet(
        graph,
        request,
        result_kind,
        nodes=[index["nodes"][node_id] for node_id in node_path if node_id in index["nodes"]],
        edges=edge_path,
        status="ok" if node_path else "not_found",
    )
    packet[payload_key] = [_compact_node(index["nodes"][node_id]) for node_id in node_path if node_id in index["nodes"]]
    _enforce_budget(packet)
    return packet


def _search(
    graph: dict[str, Any],
    index: dict[str, Any],
    request: dict[str, Any],
    *,
    static_index: dict[str, Any] | None = None,
    semantic_index: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if semantic_index is not None:
        from product_agent_os.project_graph_semantic import query_semantic_retrieval

        return query_semantic_retrieval(semantic_index, request, graph=graph)
    if static_index is not None:
        validation = static_index.get("validation") if isinstance(static_index.get("validation"), dict) else validate_static_search_index(static_index)
        if validation.get("ok") is not True:
            return _packet(graph, request, "search", status="blocked", errors=["static_index:invalid"])
        if static_index.get("graph_fingerprint") != graph_content_fingerprint(graph):
            return _packet(graph, request, "search", status="blocked", errors=["static_index:stale"])
        return query_static_search_index(static_index, request)
    needle = str(request.get("text") or "").lower()
    terms = _search_terms(needle)
    scored_nodes = []
    for node in index["nodes"].values():
        haystack = " ".join(
            str(node.get(key) or "")
            for key in ["id", "label", "type", "language", "path", "status"]
        ).lower()
        score = _search_score(node, haystack, terms, needle)
        if _node_matches_filters(node, request) and ((terms and score > 0) or (not terms and needle in haystack)):
            scored_nodes.append((node, score))
    nodes = [
        node
        for node, _score in sorted(
            scored_nodes,
            key=lambda item: (-item[1], str(item[0].get("id") or "")),
        )
    ]
    return _packet(graph, request, "search", nodes=nodes, status="ok")


def _hotspots(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    scored = sorted(
        (
            {
                **_compact_node(node),
                "degree": len(index["adjacent"].get(node_id, [])),
            }
            for node_id, node in index["nodes"].items()
        ),
        key=lambda item: (-int(item["degree"]), item["id"]),
    )
    packet = _packet(graph, request, "hotspots", status="ok")
    packet["hotspots"] = scored[: _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)]
    _enforce_budget(packet)
    return packet


def _read_order(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    seed = str(request.get("node_id") or "")
    nodes = []
    if seed in index["nodes"]:
        nodes.append(index["nodes"][seed])
    for edge in index["outgoing"].get(seed, []) + index["incoming"].get(seed, []):
        target = edge.get("target") if edge.get("source") == seed else edge.get("source")
        node = index["nodes"].get(str(target))
        if node and node not in nodes:
            nodes.append(node)
    packet = _packet(graph, request, "read_order", nodes=nodes, status="ok")
    packet["read_order"] = [_compact_node(node) for node in packet["nodes"]]
    _enforce_budget(packet)
    return packet


def _impact(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    nodes, edges = _reverse_reachable(
        index,
        node_id,
        max_depth=_positive_int(request.get("max_depth"), 6),
        max_results=_positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS),
    )
    return _packet(graph, request, "impact", nodes=nodes, edges=edges, status="ok")


def _affected_tests(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    nodes, edges = _reverse_reachable(
        index,
        node_id,
        max_depth=_positive_int(request.get("max_depth"), 6),
        max_results=_positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS),
    )
    tests = [
        _compact_node(node)
        for node in nodes
        if node.get("type") in {"test", "function", "method"} and ("test" in str(node.get("id") or "").lower())
    ]
    packet = _packet(graph, request, "affected_tests", nodes=nodes, edges=edges, status="ok")
    packet["tests"] = tests
    packet["coverage_status"] = "partial_static"
    _enforce_budget(packet)
    return packet


def _agent_reading_packet(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    node = index["nodes"].get(node_id)
    if not node:
        return _packet(graph, request, "agent_reading_packet", status="not_found")

    max_results = _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)
    max_depth = _positive_int(request.get("max_depth"), 6)
    related_edges = _filter_edges(index["outgoing"].get(node_id, []) + index["incoming"].get(node_id, []), request)
    related_nodes = _related_nodes(index, node_id, related_edges, limit=max_results)
    affected_nodes, affected_edges = _reverse_reachable(index, node_id, max_depth=max_depth, max_results=max_results)
    affected_tests = _compact_test_nodes(affected_nodes)
    read_nodes = [node] + [candidate for candidate in related_nodes if candidate.get("id") != node_id]

    packet = _packet(
        graph,
        request,
        "agent_reading_packet",
        nodes=[node],
        edges=[],
        status="ok",
    )
    packet["target_entity"] = _compact_node(node)
    packet["related_entities"] = [_compact_node(item) for item in related_nodes[:max_results]]
    packet["read_order"] = [_compact_node(item) for item in read_nodes[:max_results]]
    packet["source_spans"] = _compact_source_spans([node] + related_nodes, limit=max_results)
    packet["confidence_summary"] = _confidence_summary(related_edges + affected_edges)
    packet["must_read_source_before_edit"] = True
    packet["source_read_required"] = True
    packet["affected_tests"] = affected_tests[:max_results]
    packet["stale_status"] = _stale_status_for_node(graph, node)
    packet["freshness_status"] = _freshness_status_for_graph(graph)
    packet["rejected_links"] = _rejected_links(graph, node_id, limit=max_results)
    packet["unresolved_edges"] = _unresolved_edges(related_edges + affected_edges, limit=max_results)
    packet["unsupported_languages"] = _unsupported_languages(graph, [node] + related_nodes)
    packet["framework_semantics"] = _framework_semantics(graph, [node] + related_nodes, limit=max_results)
    packet["unsupported_claims"] = _unsupported_agent_packet_claims(graph, [node] + related_nodes)
    if packet["freshness_status"]["blocks_action_claims"]:
        packet["safe_next_action"] = "Refresh graph or read source files from listed spans before edits, impact claims, or completion/readiness claims."
    else:
        packet["safe_next_action"] = "Read source files from listed spans before edits, impact claims, or completion/readiness claims."
    _enforce_budget(packet)
    return packet


def _changed_since(graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    packet = _packet(graph, request, "changed_since", status="ok")
    packet["temporal_delta"] = _bounded_delta(graph)
    _enforce_budget(packet)
    return packet


def _why_changed(graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    delta = graph.get("metadata", {}).get("temporal_delta")
    reasons: list[str] = []
    if isinstance(delta, dict):
        for item in delta.get("new_edges", []):
            if isinstance(item, dict) and node_id in {item.get("source"), item.get("target")}:
                reasons.append("added")
        for item in delta.get("invalidated_edges", []):
            if isinstance(item, dict) and node_id in {item.get("source"), item.get("target")}:
                reasons.append("removed")
        for item in delta.get("superseded_edges", []):
            if isinstance(item, dict) and node_id in {item.get("source"), item.get("target")}:
                reasons.append("changed")
    packet = _packet(graph, request, "why_changed", status="ok")
    packet["change_reasons"] = sorted(set(reasons)) or ["not_available"]
    _enforce_budget(packet)
    return packet


def _status_packet(graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    packet = _packet(graph, request, "status", status="ok")
    packet["graph_status"] = {
        "scan_id": str(metadata.get("scan_id") or ""),
        "node_count": int(metadata.get("node_count") or len(graph.get("nodes", []))),
        "edge_count": int(metadata.get("edge_count") or len(graph.get("edges", []))),
        "observation_count": int(metadata.get("observation_count") or len(graph.get("observations", []))),
        "language_support_summary": metadata.get("language_support_summary", {}),
        "temporal_delta": _bounded_delta(graph),
        "freshness_status": _freshness_status_for_graph(graph),
        "coverage_map": _bounded_coverage_map(graph),
        "rejected_link_summary": _rejected_link_summary(graph),
    }
    _enforce_budget(packet)
    return packet


def _packet(
    graph: dict[str, Any],
    request: dict[str, Any],
    result_kind: str,
    *,
    nodes: list[dict[str, Any]] | None = None,
    edges: list[dict[str, Any]] | None = None,
    status: str,
    errors: list[str] | None = None,
    truncation_reasons: list[str] | None = None,
    omitted_count: int = 0,
) -> dict[str, Any]:
    max_results = _positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS)
    max_tokens = _positive_int(request.get("max_tokens"), DEFAULT_MAX_TOKENS)
    compact_nodes = [_compact_node(node) for node in (nodes or []) if isinstance(node, dict)]
    compact_edges = [_compact_edge(edge) for edge in (edges or []) if isinstance(edge, dict)]
    omitted = omitted_count
    truncated = False
    if len(compact_nodes) > max_results:
        omitted += len(compact_nodes) - max_results
        compact_nodes = compact_nodes[:max_results]
        truncated = True
    if len(compact_edges) > max_results * 2:
        omitted += len(compact_edges) - max_results * 2
        compact_edges = compact_edges[: max_results * 2]
        truncated = True
    packet: dict[str, Any] = {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "result_kind": result_kind,
        "query_id": _query_id(request),
        "as_of_scan": str(graph.get("metadata", {}).get("scan_id") or ""),
        "source_boundary": "graph_artifact_only_raw_source_excluded",
        "generated_view_policy": "graph_packets_are_orientation_evidence_only",
        "nodes": compact_nodes,
        "edges": compact_edges,
        "errors": errors or [],
        "filters": _filters(request),
        "budget": {
            "max_results": max_results,
            "max_tokens": max_tokens,
            "estimated_tokens": 0,
            "truncated": truncated,
            "omitted_count": omitted,
            "truncation_reasons": sorted(set(truncation_reasons or [])),
        },
        "safe_next_action": "Use graph as orientation only; read source files before edits or completion claims.",
    }
    _enforce_budget(packet)
    return packet


def _enforce_budget(packet: dict[str, Any]) -> None:
    budget = packet.get("budget") if isinstance(packet.get("budget"), dict) else {}
    max_tokens = _positive_int(budget.get("max_tokens"), DEFAULT_MAX_TOKENS)
    trim_keys = [
        "hotspots",
        "read_order",
        "related_entities",
        "source_spans",
        "affected_tests",
        "path",
        "trace",
        "tests",
        "nodes",
        "edges",
    ]
    while _estimated_tokens(packet) > max_tokens:
        trimmed = False
        for key in trim_keys:
            value = packet.get(key)
            if isinstance(value, list) and value:
                value.pop()
                _mark_truncated(packet, "token_budget")
                trimmed = True
                break
        if not trimmed:
            delta = packet.get("temporal_delta")
            if isinstance(delta, dict):
                for key in ["new_edges", "invalidated_edges", "superseded_edges"]:
                    value = delta.get(key)
                    if isinstance(value, list) and value:
                        value.pop()
                        _mark_truncated(packet, "token_budget")
                        trimmed = True
                        break
        if not trimmed:
            break
    packet["budget"]["estimated_tokens"] = _estimated_tokens(packet)


def _mark_truncated(packet: dict[str, Any], reason: str) -> None:
    budget = packet["budget"]
    budget["omitted_count"] = int(budget.get("omitted_count") or 0) + 1
    budget["truncated"] = True
    budget["truncation_reasons"] = sorted(set(list(budget.get("truncation_reasons") or []) + [reason]))


def _index_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {str(node.get("id")): node for node in graph.get("nodes", []) if isinstance(node, dict) and node.get("id")}
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, dict)]
    outgoing: dict[str, list[dict[str, Any]]] = {}
    incoming: dict[str, list[dict[str, Any]]] = {}
    adjacent: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        outgoing.setdefault(source, []).append(edge)
        incoming.setdefault(target, []).append(edge)
        adjacent.setdefault(source, []).append(edge)
        adjacent.setdefault(target, []).append(edge)
    for bucket in [outgoing, incoming, adjacent]:
        for key in bucket:
            bucket[key] = sorted(bucket[key], key=lambda item: (str(item.get("type")), str(item.get("source")), str(item.get("target"))))
    return {"nodes": nodes, "edges": edges, "outgoing": outgoing, "incoming": incoming, "adjacent": adjacent}


def _shortest_path(index: dict[str, Any], source: str, target: str, *, max_depth: int) -> tuple[list[str], list[dict[str, Any]]]:
    if source not in index["nodes"] or target not in index["nodes"]:
        return [], []
    queue = deque([(source, [source], [])])
    visited = {source}
    while queue:
        current, node_path, edge_path = queue.popleft()
        if current == target:
            return node_path, edge_path
        if len(edge_path) >= max_depth:
            continue
        for edge in index["adjacent"].get(current, []):
            other = _other(edge, current)
            if other in visited:
                continue
            visited.add(other)
            queue.append((other, node_path + [other], edge_path + [edge]))
    return [], []


def _reverse_reachable(index: dict[str, Any], node_id: str, *, max_depth: int, max_results: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    queue = deque([(node_id, 0)])
    visited = {node_id}
    while queue and len(nodes) < max_results:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for edge in index["incoming"].get(current, []):
            source = str(edge.get("source") or "")
            if source in visited:
                continue
            visited.add(source)
            edges.append(edge)
            node = index["nodes"].get(source)
            if node:
                nodes.append(node)
            queue.append((source, depth + 1))
            if len(nodes) >= max_results:
                break
    return nodes, edges


def _filter_edges(edges: list[dict[str, Any]], request: dict[str, Any]) -> list[dict[str, Any]]:
    edge_types = set(str(item) for item in request.get("edge_types", []) if isinstance(item, str))
    confidence = set(str(item) for item in request.get("confidence", []) if isinstance(item, str))
    filtered = []
    for edge in edges:
        if edge_types and edge.get("type") not in edge_types:
            continue
        if confidence and edge.get("confidence") not in confidence:
            continue
        filtered.append(edge)
    return filtered


def _node_matches_filters(node: dict[str, Any], request: dict[str, Any]) -> bool:
    node_types = set(str(item) for item in request.get("node_types", []) if isinstance(item, str))
    path_prefixes = [str(item) for item in request.get("path_prefixes", []) if isinstance(item, str)]
    if node_types and node.get("type") not in node_types:
        return False
    if path_prefixes and not any(str(node.get("path") or "").startswith(prefix) for prefix in path_prefixes):
        return False
    return True


def _compact_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(node.get("id") or ""),
        "type": str(node.get("type") or ""),
        "label": str(node.get("label") or "")[:120],
        "status": str(node.get("status") or ""),
        "language": str(node.get("language") or ""),
        "path": str(node.get("path") or ""),
    }


def _related_nodes(index: dict[str, Any], node_id: str, edges: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    seen = {node_id}
    for edge in edges:
        related_id = _other(edge, node_id)
        if related_id in seen:
            continue
        node = index["nodes"].get(related_id)
        if not node:
            continue
        seen.add(related_id)
        nodes.append(node)
        if len(nodes) >= limit:
            break
    return nodes


def _compact_test_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _compact_node(node)
        for node in nodes
        if node.get("type") in {"test", "function", "method"} and ("test" in str(node.get("id") or "").lower())
    ]


def _compact_source_spans(nodes: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    seen: set[tuple[str, int, int]] = set()
    for node in nodes:
        for span in node.get("source_spans") or []:
            if not isinstance(span, dict):
                continue
            relative_path = str(span.get("relative_path") or "")
            if not _safe_relative_path(relative_path):
                continue
            start_line = _positive_int(span.get("start_line"), 1)
            end_line = _positive_int(span.get("end_line"), start_line)
            key = (relative_path, start_line, end_line)
            if key in seen:
                continue
            seen.add(key)
            spans.append(
                {
                    "relative_path": relative_path,
                    "start_line": start_line,
                    "end_line": end_line,
                    "fingerprint": str(span.get("fingerprint") or ""),
                }
            )
            if len(spans) >= limit:
                return spans
    return spans


def _confidence_summary(edges: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "verified_edges": 0,
        "inferred_edges": 0,
        "unsupported_edges": 0,
        "accepted_gap_edges": 0,
        "unknown_edges": 0,
    }
    for edge in edges:
        confidence = str(edge.get("confidence") or "")
        status = str(edge.get("status") or "")
        if confidence == "verified":
            summary["verified_edges"] += 1
        elif confidence == "inferred":
            summary["inferred_edges"] += 1
        elif confidence == "accepted_gap" or status == "accepted_gap":
            summary["accepted_gap_edges"] += 1
        elif confidence == "unsupported" or status == "unsupported":
            summary["unsupported_edges"] += 1
        else:
            summary["unknown_edges"] += 1
    return summary


def _stale_status_for_node(graph: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
    delta = _bounded_delta(graph)
    node_id = str(node.get("id") or "")
    path = str(node.get("path") or "")
    file_id = f"file:{path}" if path else ""
    related: list[dict[str, Any]] = []
    for key in ["new_edges", "invalidated_edges", "superseded_edges"]:
        for item in delta.get(key, []):
            if not isinstance(item, dict):
                continue
            if node_id in {item.get("source"), item.get("target")} or file_id in {item.get("source"), item.get("target")}:
                related.append(_compact_delta_edge(item, key))
    if related:
        status = "stale"
    elif delta.get("status") == "changed":
        status = "partial"
    elif delta.get("status") in {"not_available"}:
        status = "unknown"
    else:
        status = "fresh"
    return {
        "schema_version": 1,
        "status": status,
        "graph_delta_status": str(delta.get("status") or "not_available"),
        "blocks_action_claims": status in {"partial", "stale", "unknown"},
        "related_delta_edges": related[:5],
    }


def _freshness_status_for_graph(graph: dict[str, Any]) -> dict[str, Any]:
    delta = _bounded_delta(graph)
    delta_status = str(delta.get("status") or "not_available")
    if delta_status in {"changed", "stale"}:
        status = "stale"
    elif delta_status in {"current", "fresh"}:
        status = "fresh"
    else:
        status = "unknown"
    blocks = status in {"partial", "stale", "unknown"}
    return {
        "schema_version": 1,
        "status": status,
        "graph_delta_status": delta_status,
        "blocks_action_claims": blocks,
        "safe_next_action": (
            "Refresh graph or read source files before edits or readiness claims."
            if blocks
            else "Read source files before edits or readiness claims."
        ),
    }


def _bounded_coverage_map(graph: dict[str, Any]) -> dict[str, Any]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    coverage = metadata.get("coverage_map")
    if not isinstance(coverage, dict):
        return {
            "schema_version": 1,
            "status": "not_available",
            "source_boundary": "graph_artifact_only_raw_source_excluded",
            "by_language": {},
            "by_node_type": {},
            "unsupported_languages": {},
            "partial_languages": {},
            "recommended_next_parser_or_linker_action": "Review source files before graph-backed claims.",
        }
    bounded = dict(coverage)
    for key in ["by_language", "by_path_prefix", "by_file_type", "by_node_type", "confidence_distribution"]:
        value = bounded.get(key)
        if isinstance(value, dict):
            bounded[key] = dict(sorted(value.items())[:25])
    for key in ["unsupported_languages", "partial_languages"]:
        value = bounded.get(key)
        if isinstance(value, dict):
            bounded[key] = dict(sorted(value.items())[:25])
    return bounded


def _compact_delta_edge(edge: dict[str, Any], bucket: str) -> dict[str, Any]:
    return {
        "bucket": bucket,
        "type": str(edge.get("type") or ""),
        "source": str(edge.get("source") or ""),
        "target": str(edge.get("target") or ""),
        "status": str(edge.get("status") or ""),
    }


def _rejected_links(graph: dict[str, Any], node_id: str, *, limit: int) -> list[dict[str, Any]]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    rejected = metadata.get("rejected_links")
    if not isinstance(rejected, list):
        return []
    items: list[dict[str, Any]] = []
    for item in rejected:
        if not isinstance(item, dict):
            continue
        if node_id not in {item.get("source"), item.get("target"), item.get("target_candidate"), item.get("node_id")}:
            continue
        items.append(
            {
                "source": str(item.get("source") or ""),
                "target": str(item.get("target") or item.get("target_candidate") or ""),
                "target_candidate": str(item.get("target_candidate") or item.get("target") or ""),
                "rule": str(item.get("rule") or "not_available")[:120],
                "reason": str(item.get("reason") or "not_available")[:120],
                "confidence": str(item.get("confidence") or ""),
                "status": str(item.get("status") or ""),
                "source_read_required": bool(item.get("source_read_required")),
                "future_parser_or_linker_task": str(item.get("future_parser_or_linker_task") or item.get("future_resolution") or "")[:120],
            }
        )
        if len(items) >= limit:
            break
    return items


def _rejected_link_summary(graph: dict[str, Any]) -> dict[str, Any]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    rejected = metadata.get("rejected_links")
    if not isinstance(rejected, list):
        return {"schema_version": 1, "total": 0, "by_reason": {}, "by_rule": {}, "policy": "rejected_candidates_are_not_dependencies"}
    by_reason: dict[str, int] = {}
    by_rule: dict[str, int] = {}
    for item in rejected:
        if not isinstance(item, dict):
            continue
        reason = str(item.get("reason") or "not_available")
        rule = str(item.get("rule") or "not_available")
        by_reason[reason] = by_reason.get(reason, 0) + 1
        by_rule[rule] = by_rule.get(rule, 0) + 1
    return {
        "schema_version": 1,
        "total": sum(by_reason.values()),
        "by_reason": dict(sorted(by_reason.items())[:25]),
        "by_rule": dict(sorted(by_rule.items())[:25]),
        "policy": "rejected_candidates_are_not_dependencies",
    }


def _unresolved_edges(edges: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for edge in edges:
        status = str(edge.get("status") or "")
        confidence = str(edge.get("confidence") or "")
        if status not in {"unresolved", "unsupported"} and confidence not in {"unsupported", "accepted_gap"}:
            continue
        items.append(_compact_edge(edge))
        if len(items) >= limit:
            break
    return items


def _unsupported_languages(graph: dict[str, Any], nodes: list[dict[str, Any]]) -> list[dict[str, str]]:
    language_summary = graph.get("metadata", {}).get("language_support_summary")
    if not isinstance(language_summary, dict):
        return []
    warnings: list[dict[str, str]] = []
    seen: set[str] = set()
    for node in nodes:
        language = str(node.get("language") or "")
        if not language or language in seen:
            continue
        support = language_summary.get(language)
        support_level = ""
        if isinstance(support, dict):
            support_level = str(support.get("support_level") or support.get("status") or "")
        elif isinstance(support, str):
            support_level = support
        if support_level and support_level not in {"supported", "supported_stdlib", "supported_conservative_stdlib"}:
            seen.add(language)
            warnings.append({"language": language, "support_level": support_level})
    return warnings


def _unsupported_agent_packet_claims(graph: dict[str, Any], nodes: list[dict[str, Any]]) -> list[str]:
    claims = [
        "release_readiness",
        "production_runtime_behavior",
        "source_read_completion",
        "completion_verification",
    ]
    for warning in _unsupported_languages(graph, nodes):
        claims.append(f"unsupported_language:{warning['language']}")
    if _framework_semantics(graph, nodes, limit=1):
        claims.append("framework_runtime_behavior")
    return sorted(set(claims))


def _framework_semantics(graph: dict[str, Any], nodes: list[dict[str, Any]], *, limit: int) -> list[dict[str, Any]]:
    metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
    scanner = metadata.get("typescript_javascript_scanner")
    if not isinstance(scanner, dict):
        return []
    semantics = scanner.get("framework_semantics")
    if not isinstance(semantics, list):
        return []
    node_ids = {str(node.get("id") or "") for node in nodes}
    paths = {str(node.get("path") or "") for node in nodes}
    results: list[dict[str, Any]] = []
    for item in semantics:
        if not isinstance(item, dict):
            continue
        if str(item.get("symbol_id") or "") not in node_ids and str(item.get("relative_path") or "") not in paths:
            continue
        results.append(
            {
                "framework": str(item.get("framework") or ""),
                "semantic_type": str(item.get("semantic_type") or ""),
                "relative_path": str(item.get("relative_path") or ""),
                "symbol_id": str(item.get("symbol_id") or ""),
                "confidence": str(item.get("confidence") or ""),
                "status": str(item.get("status") or ""),
                "source_read_required": bool(item.get("source_read_required")),
                "source_boundary": str(item.get("source_boundary") or ""),
                "unsupported_claims": list(item.get("unsupported_claims") or [])[:8],
            }
        )
        if len(results) >= limit:
            break
    return results


def _compact_edge(edge: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(edge.get("id") or ""),
        "type": str(edge.get("type") or ""),
        "source": str(edge.get("source") or ""),
        "target": str(edge.get("target") or ""),
        "confidence": str(edge.get("confidence") or ""),
        "status": str(edge.get("status") or ""),
        "observation_ids": list(edge.get("observation_ids") or [])[:3],
    }


def _bounded_delta(graph: dict[str, Any], limit: int = 10) -> dict[str, Any]:
    delta = graph.get("metadata", {}).get("temporal_delta")
    if not isinstance(delta, dict):
        return {"schema_version": 1, "status": "not_available", "invalidated_edges": [], "superseded_edges": [], "new_edges": []}
    return {
        "schema_version": 1,
        "scan_id": str(delta.get("scan_id") or ""),
        "status": str(delta.get("status") or "not_available"),
        "invalidated_edges": list(delta.get("invalidated_edges") or [])[:limit],
        "superseded_edges": list(delta.get("superseded_edges") or [])[:limit],
        "new_edges": list(delta.get("new_edges") or [])[:limit],
    }


def _other(edge: dict[str, Any], node_id: str) -> str:
    source = str(edge.get("source") or "")
    target = str(edge.get("target") or "")
    return target if source == node_id else source


def _filters(request: dict[str, Any]) -> dict[str, Any]:
    return {
        key: request[key]
        for key in ["node_types", "edge_types", "confidence", "path_prefixes"]
        if key in request
    }


def _query_id(request: dict[str, Any]) -> str:
    return "query:" + hashlib.sha256(json.dumps(request, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def _estimated_tokens(packet: dict[str, Any]) -> int:
    return max(1, len(json.dumps(packet, sort_keys=True)) // 4)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _safe_relative_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    if not normalized or normalized.startswith(("/", "../", "http://", "https://")):
        return False
    if ":/" in normalized:
        return False
    return ".." not in normalized.split("/")


def _search_terms(value: str) -> list[str]:
    return [term for term in re.split(r"[^a-z0-9]+", value.lower()) if term]


def _search_score(node: dict[str, Any], haystack: str, terms: list[str], needle: str) -> int:
    if not terms:
        return 1 if needle in haystack else 0
    score = 0
    for term in terms:
        if term in haystack:
            score += 10
    if str(node.get("type")) in {"function", "method", "class"}:
        score += 4
    path = str(node.get("path") or "")
    if "/tests/" not in f"/{path}" and not path.startswith("tests/"):
        score += 2
    else:
        score -= 15
    if str(node.get("status") or "") == "current":
        score += 1
    return score
