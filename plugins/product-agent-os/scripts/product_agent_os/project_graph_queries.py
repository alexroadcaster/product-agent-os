"""Bounded graph-only query packets for Product-Agent OS project graphs."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_ontology import default_ontology


MAX_QUERY_TEXT_LENGTH = 120
DEFAULT_MAX_RESULTS = 25
DEFAULT_MAX_TOKENS = 4_000
DEFAULT_HUB_THRESHOLD = 100
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


def query_project_graph(graph: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
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
        return _search(graph, index, request)
    if kind == "hotspots":
        return _hotspots(graph, index, request)
    if kind == "read_order":
        return _read_order(graph, index, request)
    if kind == "impact":
        return _impact(graph, index, request)
    if kind == "affected_tests":
        return _affected_tests(graph, index, request)
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
    return errors


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


def _search(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    needle = str(request.get("text") or "").lower()
    nodes = []
    for node in index["nodes"].values():
        haystack = " ".join(
            str(node.get(key) or "")
            for key in ["id", "label", "type", "language", "path", "status"]
        ).lower()
        if needle in haystack and _node_matches_filters(node, request):
            nodes.append(node)
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
    nodes, edges = _reverse_reachable(index, node_id, max_results=_positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS))
    return _packet(graph, request, "impact", nodes=nodes, edges=edges, status="ok")


def _affected_tests(graph: dict[str, Any], index: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    node_id = str(request.get("node_id") or "")
    nodes, edges = _reverse_reachable(index, node_id, max_results=_positive_int(request.get("max_results"), DEFAULT_MAX_RESULTS))
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
    trim_keys = ["hotspots", "read_order", "path", "trace", "tests", "nodes", "edges"]
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


def _reverse_reachable(index: dict[str, Any], node_id: str, *, max_results: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    queue = deque([node_id])
    visited = {node_id}
    while queue and len(nodes) < max_results:
        current = queue.popleft()
        for edge in index["incoming"].get(current, []):
            source = str(edge.get("source") or "")
            if source in visited:
                continue
            visited.add(source)
            edges.append(edge)
            node = index["nodes"].get(source)
            if node:
                nodes.append(node)
            queue.append(source)
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
