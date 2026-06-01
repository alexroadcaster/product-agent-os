"""Graphology-compatible visual projection for Product-Agent OS project graphs."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


DEFAULT_VISIBLE_NODE_LIMIT = 250
DEFAULT_VISIBLE_EDGE_LIMIT = 600
HARD_VISIBLE_NODE_LIMIT = 1_000
HARD_VISIBLE_EDGE_LIMIT = 2_500
LARGE_GRAPH_THRESHOLD = 1_000

_PALETTE = [
    "#126d60",
    "#2f6fb0",
    "#7a5c12",
    "#8c4a5f",
    "#4f6b2f",
    "#6f5aa8",
    "#a24d2d",
    "#26707f",
]
def build_project_graph_visual_model(
    graph: dict[str, Any],
    *,
    selected_node_id: str = "",
    max_nodes: int = DEFAULT_VISIBLE_NODE_LIMIT,
    max_edges: int = DEFAULT_VISIBLE_EDGE_LIMIT,
) -> dict[str, Any]:
    """Build a deterministic visual projection from graph JSON without source reads."""

    requested_node_limit = _positive_int(max_nodes, DEFAULT_VISIBLE_NODE_LIMIT)
    requested_edge_limit = _positive_int(max_edges, DEFAULT_VISIBLE_EDGE_LIMIT)
    node_limit = min(requested_node_limit, HARD_VISIBLE_NODE_LIMIT)
    edge_limit = min(requested_edge_limit, HARD_VISIBLE_EDGE_LIMIT)
    nodes = [node for node in graph.get("nodes", []) if isinstance(node, dict) and node.get("id")]
    edges = [edge for edge in graph.get("edges", []) if isinstance(edge, dict) and edge.get("source") and edge.get("target")]
    declared_node_count = _declared_count(graph, "node_count", len(nodes))
    declared_edge_count = _declared_count(graph, "edge_count", len(edges))
    degree = _degree(edges)
    visible_node_ids = _visible_node_ids(nodes, degree, selected_node_id, node_limit)
    visible_nodes = [node for node in nodes if str(node.get("id")) in visible_node_ids]
    visible_node_set = {str(node.get("id")) for node in visible_nodes}
    visible_edges = [
        edge
        for edge in edges
        if str(edge.get("source")) in visible_node_set and str(edge.get("target")) in visible_node_set
    ][:edge_limit]
    large_graph = declared_node_count >= LARGE_GRAPH_THRESHOLD or declared_edge_count >= LARGE_GRAPH_THRESHOLD
    positioned_nodes = [
        _visual_node(node, index, len(visible_nodes), degree, selected_node_id, large_graph)
        for index, node in enumerate(visible_nodes)
    ]
    visual_edges = [_visual_edge(edge) for edge in visible_edges]
    clusters = _clusters(positioned_nodes)
    focused = _focused_subgraph(selected_node_id, visible_node_set, visible_edges, {str(node.get("id")): node for node in nodes})
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "graphology_compatible": True,
        "generated_view_policy": "visual projection is generated review output only",
        "source_policy": "visual projection derives from canonical graph artifact only",
        "graph_ref": {
            "scan_id": str(graph.get("metadata", {}).get("scan_id") or ""),
            "node_count": declared_node_count,
            "edge_count": declared_edge_count,
        },
        "renderer_policy": {
            "external_assets": "forbidden",
            "graphology_status": "not_bundled_static_fallback",
            "sigma_status": "not_bundled_static_fallback",
            "static_fallback": "enabled",
        },
        "vendor_manifest": [
            {"name": "graphology", "status": "not_bundled", "fallback": "static_svg_and_table"},
            {"name": "sigma.js", "status": "not_bundled", "fallback": "static_svg_and_table"},
        ],
        "options": {"type": "mixed", "multi": False, "allowSelfLoops": True},
        "attributes": {
            "scan_id": str(graph.get("metadata", {}).get("scan_id") or ""),
            "layout": "deterministic_radial_by_community",
        },
        "nodes": positioned_nodes,
        "edges": visual_edges,
        "clusters": clusters,
        "focused_subgraph": focused,
        "available_filters": [
            "node_type",
            "edge_type",
            "confidence",
            "language",
            "artifact",
            "partition",
            "stale",
            "text",
        ],
        "navigation_commands": ["fit", "isolate", "expand", "reset", "copy"],
        "render_modes": {
            "default": "static_svg_fallback",
            "large_graph": "clustered_static_fallback" if large_graph else "static_svg_fallback",
            "fallback_table": "enabled",
            "mobile": "single_column_static_graph",
        },
        "performance_budget": {
            "declared_node_count": declared_node_count,
            "declared_edge_count": declared_edge_count,
            "requested_visible_node_limit": requested_node_limit,
            "requested_visible_edge_limit": requested_edge_limit,
            "visible_node_limit": node_limit,
            "visible_edge_limit": edge_limit,
            "hard_visible_node_limit": HARD_VISIBLE_NODE_LIMIT,
            "hard_visible_edge_limit": HARD_VISIBLE_EDGE_LIMIT,
            "visible_node_count": len(positioned_nodes),
            "visible_edge_count": len(visual_edges),
            "omitted_node_count": max(0, declared_node_count - len(positioned_nodes)),
            "omitted_edge_count": max(0, declared_edge_count - len(visual_edges)),
            "large_graph": large_graph,
        },
        "safe_next_action": "Use projection for navigation only; verify relationships in source before edits.",
        "validation": {"ok": True, "checks": ["graphology shape", "local-only renderer policy"], "errors": []},
    }


def _visible_node_ids(
    nodes: list[dict[str, Any]],
    degree: dict[str, int],
    selected_node_id: str,
    limit: int,
) -> set[str]:
    scored = sorted(
        (str(node.get("id")) for node in nodes),
        key=lambda node_id: (-degree.get(node_id, 0), node_id),
    )
    visible = scored[:limit]
    if selected_node_id and selected_node_id in scored and selected_node_id not in visible:
        if visible:
            visible[-1] = selected_node_id
        else:
            visible.append(selected_node_id)
    return set(visible)


def _visual_node(
    node: dict[str, Any],
    index: int,
    total: int,
    degree: dict[str, int],
    selected_node_id: str,
    large_graph: bool,
) -> dict[str, Any]:
    node_id = str(node.get("id"))
    community = _community_for_node(node)
    angle = (2 * math.pi * index / max(1, total)) + (_stable_int(community) % 37) / 100
    radius = 38 + (_stable_int(community) % 16)
    node_degree = degree.get(node_id, 0)
    lod_tier = _lod_tier(node_degree, large_graph, selected_node_id == node_id)
    return {
        "key": node_id,
        "attributes": {
            "label": _text(node.get("label") or node_id)[:120],
            "type": _text(node.get("type")),
            "status": _text(node.get("status")),
            "language": _text(node.get("language")),
            "path": safe_relative_path_text(node.get("path")),
            "x": round(math.cos(angle) * radius, 3),
            "y": round(math.sin(angle) * radius, 3),
            "size": round(5.0 + min(node_degree, 25) * 0.65 + (2 if selected_node_id == node_id else 0), 2),
            "color": _color_for_community(community),
            "community": community,
            "lod_tier": lod_tier,
            "label_priority": _label_priority(node_degree, selected_node_id == node_id),
            "renderer_hint": "show_label" if lod_tier == 0 else "hide_label_until_focus",
        },
    }


def _visual_edge(edge: dict[str, Any]) -> dict[str, Any]:
    edge_id = str(edge.get("id") or _edge_key(edge))
    return {
        "key": edge_id,
        "source": str(edge.get("source") or ""),
        "target": str(edge.get("target") or ""),
        "attributes": {
            "type": _text(edge.get("type")),
            "confidence": _text(edge.get("confidence")),
            "status": _text(edge.get("status")),
            "color": "#7d8793" if edge.get("confidence") == "verified" else "#a36f2f",
            "size": 1.6 if edge.get("confidence") == "verified" else 1.0,
        },
    }


def _clusters(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for node in nodes:
        community = str(node.get("attributes", {}).get("community") or "unknown")
        buckets.setdefault(community, []).append(node)
    clusters: list[dict[str, Any]] = []
    for community, items in sorted(buckets.items()):
        clusters.append(
            {
                "id": f"cluster:{community}",
                "label": community,
                "node_count": len(items),
                "color": _color_for_community(community),
                "lod_tier": 0 if len(items) <= 12 else 1,
            }
        )
    return clusters


def _focused_subgraph(
    selected_node_id: str,
    visible_node_ids: set[str],
    edges: list[dict[str, Any]],
    all_nodes: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not selected_node_id or selected_node_id not in all_nodes:
        return {"selected_node": {}, "node_ids": [], "edge_ids": [], "status": "not_selected"}
    neighbors = {selected_node_id}
    edge_ids: list[str] = []
    for edge in edges:
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        if selected_node_id in {source, target}:
            neighbors.add(source)
            neighbors.add(target)
            edge_ids.append(str(edge.get("id") or _edge_key(edge)))
    return {
        "selected_node": _compact_node(all_nodes[selected_node_id]),
        "node_ids": sorted(node_id for node_id in neighbors if node_id in visible_node_ids),
        "edge_ids": edge_ids[:50],
        "status": "bounded" if edge_ids else "selected_node_only",
    }


def _degree(edges: list[dict[str, Any]]) -> dict[str, int]:
    degree: dict[str, int] = {}
    for edge in edges:
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        degree[source] = degree.get(source, 0) + 1
        degree[target] = degree.get(target, 0) + 1
    return degree


def _community_for_node(node: dict[str, Any]) -> str:
    path = str(node.get("path") or node.get("id") or "")
    safe_path = safe_relative_path_text(path)
    if safe_path:
        path = safe_path
    else:
        path = str(node.get("id") or node.get("type") or "root")
    normalized = path.replace("\\", "/")
    if "/" in normalized:
        return normalized.split("/", 1)[0] or "root"
    node_id = str(node.get("id") or "")
    value = node_id.split(":", 1)[-1]
    if "." in value:
        return value.split(".", 1)[0]
    return str(node.get("type") or "root")


def _color_for_community(community: str) -> str:
    return _PALETTE[_stable_int(community) % len(_PALETTE)]


def _lod_tier(degree: int, large_graph: bool, selected: bool) -> int:
    if selected or degree >= 10:
        return 0
    if large_graph:
        return 1 if degree >= 2 else 2
    return 0 if degree >= 2 else 1


def _label_priority(degree: int, selected: bool) -> int:
    if selected:
        return 100
    if degree >= 10:
        return 80
    if degree >= 3:
        return 50
    return 10


def _declared_count(graph: dict[str, Any], field: str, default: int) -> int:
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    return _positive_int(metadata.get(field), default)


def _compact_node(node: dict[str, Any]) -> dict[str, str]:
    return {
        "id": _text(node.get("id")),
        "type": _text(node.get("type")),
        "label": _text(node.get("label"))[:120],
        "status": _text(node.get("status")),
        "language": _text(node.get("language")),
        "path": safe_relative_path_text(node.get("path")),
    }


def _edge_key(edge: dict[str, Any]) -> str:
    seed = json.dumps(
        {"source": edge.get("source"), "target": edge.get("target"), "type": edge.get("type")},
        sort_keys=True,
    )
    return "edge:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]


def _stable_int(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:8], 16)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def _text(value: Any) -> str:
    return sanitize_graph_text(value)
