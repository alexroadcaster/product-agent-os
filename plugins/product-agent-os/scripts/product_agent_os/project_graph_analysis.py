"""Bounded analysis report for Product-Agent OS project graphs."""

from __future__ import annotations

from typing import Any

from product_agent_os.project_graph_queries import _compact_edge, _compact_node


DEFAULT_MAX_ITEMS = 20


def build_project_graph_analysis(graph: dict[str, Any], *, max_items: int = DEFAULT_MAX_ITEMS) -> dict[str, Any]:
    """Build a source-free orientation report from an existing graph artifact."""

    limit = max(1, int(max_items or DEFAULT_MAX_ITEMS))
    index = _index_graph(graph)
    hotspots = _hotspots(index, limit)
    ambiguous = _ambiguous_edge_inventory(graph, limit)
    cross_module = _surprising_cross_module_links(graph, limit)
    unsupported = _unsupported_language_summary(graph)
    partial = _partial_language_summary(graph)
    truncated = any(
        [
            len(hotspots["all"]) > limit,
            len(ambiguous["all"]) > limit,
            len(cross_module["all"]) > limit,
        ]
    )
    visible_hotspots = hotspots["all"][:limit]
    report = {
        "schema_version": 1,
        "write_policy": "read_only",
        "source_policy": "generated graph is not source of truth",
        "generated_view_policy": "analysis report is orientation evidence only",
        "graph_ref": {
            "scan_id": str(graph.get("metadata", {}).get("scan_id") or ""),
            "node_count": _int(graph.get("metadata", {}).get("node_count"), len(graph.get("nodes", []))),
            "edge_count": _int(graph.get("metadata", {}).get("edge_count"), len(graph.get("edges", []))),
        },
        "hotspots": visible_hotspots,
        "god_nodes": [item for item in visible_hotspots if int(item.get("degree", 0)) >= 3] or visible_hotspots[:1],
        "surprising_cross_module_links": cross_module["all"][:limit],
        "ambiguous_edge_inventory": ambiguous["all"][:limit],
        "unsupported_language_summary": unsupported,
        "partial_language_summary": partial,
        "suggested_agent_questions": _suggested_agent_questions(visible_hotspots, ambiguous["all"], unsupported, partial)[:limit],
        "safe_next_action": "Use the graph as orientation only; read source files before edits, impact claims, or readiness claims.",
        "redaction_summary": {"raw_source_bodies": "excluded", "local_paths": "not_included"},
        "validation": {"ok": True, "checks": ["bounded analysis", "source-free report"], "errors": []},
        "budget": {
            "max_items": limit,
            "truncated": truncated,
            "omitted_count": max(
                0,
                len(hotspots["all"]) - limit,
            )
            + max(0, len(ambiguous["all"]) - limit)
            + max(0, len(cross_module["all"]) - limit),
        },
    }
    return report


def _index_graph(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {str(node.get("id")): node for node in graph.get("nodes", []) if isinstance(node, dict) and node.get("id")}
    degree: dict[str, int] = {node_id: 0 for node_id in nodes}
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        if source in degree:
            degree[source] += 1
        if target in degree:
            degree[target] += 1
    return {"nodes": nodes, "degree": degree}


def _hotspots(index: dict[str, Any], limit: int) -> dict[str, Any]:
    scored = sorted(
        (
            {
                **_compact_node(node),
                "degree": int(index["degree"].get(node_id, 0)),
            }
            for node_id, node in index["nodes"].items()
        ),
        key=lambda item: (-int(item["degree"]), item["id"]),
    )
    return {"all": scored[: max(limit * 2, limit)]}


def _ambiguous_edge_inventory(graph: dict[str, Any], limit: int) -> dict[str, Any]:
    inventory: list[dict[str, Any]] = []
    scanner = graph.get("metadata", {}).get("python_scanner")
    unresolved = scanner.get("unresolved_calls") if isinstance(scanner, dict) else []
    if isinstance(unresolved, list):
        for item in unresolved:
            if not isinstance(item, dict):
                continue
            inventory.append(
                {
                    "source": str(item.get("source") or item.get("scope") or ""),
                    "call_name": _safe_call_name(item.get("call") or item.get("name")),
                    "status": "ambiguous",
                    "safe_next_action": "Read source file before impact or readiness claims.",
                }
            )
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("confidence") in {"inferred", "ambiguous"}:
            inventory.append(
                {
                    **_compact_edge(edge),
                    "status": "ambiguous" if edge.get("confidence") == "ambiguous" else str(edge.get("status") or "current"),
                    "safe_next_action": "Confirm inferred relationship from source before acting.",
                }
            )
    inventory = sorted(inventory, key=lambda item: str(item.get("source") or item.get("id") or ""))
    return {"all": inventory[: max(limit * 2, limit)]}


def _surprising_cross_module_links(graph: dict[str, Any], limit: int) -> dict[str, Any]:
    links: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict) or edge.get("type") not in {"calls", "imports", "tests", "references"}:
            continue
        source_domain = _domain(str(edge.get("source") or ""))
        target_domain = _domain(str(edge.get("target") or ""))
        if source_domain and target_domain and source_domain != target_domain:
            links.append(
                {
                    **_compact_edge(edge),
                    "source_domain": source_domain,
                    "target_domain": target_domain,
                    "safe_next_action": "Confirm cross-module ownership before parallel edits.",
                }
            )
    links = sorted(links, key=lambda item: (item["source_domain"], item["target_domain"], item["id"]))
    return {"all": links[: max(limit * 2, limit)]}


def _unsupported_language_summary(graph: dict[str, Any]) -> dict[str, int]:
    summary: dict[str, int] = {}
    metadata_summary = graph.get("metadata", {}).get("language_support_summary")
    if isinstance(metadata_summary, dict):
        for language, status in metadata_summary.items():
            if str(status) in {"file_only", "unsupported"}:
                summary[str(language)] = summary.get(str(language), 0)
    for node in graph.get("nodes", []):
        if not isinstance(node, dict):
            continue
        if node.get("status") != "unsupported":
            continue
        language = str(node.get("language") or "unknown")
        summary[language] = summary.get(language, 0) + 1
    return dict(sorted(summary.items()))


def _partial_language_summary(graph: dict[str, Any]) -> dict[str, int]:
    summary: dict[str, int] = {}
    partial_statuses = {"supported_conservative_stdlib", "structured_overlay_supported"}
    metadata_summary = graph.get("metadata", {}).get("language_support_summary")
    if isinstance(metadata_summary, dict):
        partial_languages = {str(language) for language, status in metadata_summary.items() if str(status) in partial_statuses}
    else:
        partial_languages = set()
    for node in graph.get("nodes", []):
        if not isinstance(node, dict):
            continue
        language = str(node.get("language") or "unknown")
        if language in partial_languages:
            summary[language] = summary.get(language, 0) + 1
    for language in partial_languages:
        summary.setdefault(language, 0)
    return dict(sorted(summary.items()))


def _suggested_agent_questions(
    hotspots: list[dict[str, Any]],
    ambiguous: list[dict[str, Any]],
    unsupported: dict[str, int],
    partial: dict[str, int],
) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    if hotspots:
        questions.append(
            {
                "id": "graph-hotspot-owner",
                "text": f"Who owns the hotspot {hotspots[0]['id']} before impact claims?",
                "source": "project_graph_analysis",
            }
        )
    if ambiguous:
        questions.append(
            {
                "id": "graph-ambiguous-edge",
                "text": "Which source file should confirm ambiguous graph relationships before edits?",
                "source": "project_graph_analysis",
            }
        )
    if unsupported:
        languages = ", ".join(sorted(unsupported.keys()))
        questions.append(
            {
                "id": "graph-unsupported-language",
                "text": f"Which source-read path covers unsupported graph languages: {languages}?",
                "source": "project_graph_analysis",
            }
        )
    if partial:
        languages = ", ".join(sorted(partial.keys()))
        questions.append(
            {
                "id": "graph-partial-language",
                "text": f"Which source files confirm partial graph language hints before claims: {languages}?",
                "source": "project_graph_analysis",
            }
        )
    if not questions:
        questions.append(
            {
                "id": "graph-source-confirmation",
                "text": "Which source files should be read before acting on this graph orientation?",
                "source": "project_graph_analysis",
            }
        )
    return questions


def _domain(node_id: str) -> str:
    value = node_id.split(":", 1)[-1]
    for separator in ("/", "."):
        if separator in value:
            return value.split(separator, 1)[0]
    return value


def _safe_call_name(value: Any) -> str:
    text = str(value or "")
    text = text.replace("()", "")
    return text[:80]


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
