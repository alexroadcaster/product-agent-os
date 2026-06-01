"""Eight-page project cockpit model for Product-Agent OS graph review views."""

from __future__ import annotations

from typing import Any

from product_agent_os.project_graph_sanitization import safe_relative_path_text, sanitize_graph_text


COCKPIT_PAGE_LABELS = [
    "Overview",
    "Project Map",
    "Docs & Sources",
    "Code Intelligence",
    "Contracts",
    "Quality & Metrics",
    "Operations & Risk",
    "Proposal Ledger",
]

COCKPIT_PAGE_IDS = [
    "overview",
    "project-map",
    "docs-sources",
    "code-intelligence",
    "contracts",
    "quality-metrics",
    "operations-risk",
    "proposal-ledger",
]

SOURCE_POLICY = "generated cockpit is not source of truth"
SAFE_NEXT_ACTION = "Use graph and HTML as orientation only; read source files before edits or completion claims."

_PAGE_DEFINITIONS = [
    {
        "id": "overview",
        "label": "Overview",
        "role": "Current scan, freshness, source boundary and safe next action.",
        "sections": [
            ("scan-summary", "Scan Summary"),
            ("source-boundary", "Source Boundary"),
            ("safe-next-action", "Safe Next Action"),
        ],
        "approval_boundaries": ["No approval, write or completion claim can come from this generated view."],
        "action_surfaces": ["Open graph artifact", "Read source before acting", "Refresh scan if stale"],
    },
    {
        "id": "project-map",
        "label": "Project Map",
        "role": "Graph projection, filters, selected-node evidence and fallback table.",
        "sections": [
            ("visual-projection", "Visual Projection"),
            ("graph-filters", "Graph Filters"),
            ("selected-node-evidence", "Selected Node Evidence"),
            ("fallback-static-view", "Fallback Static View"),
        ],
        "approval_boundaries": ["Project Map is generated navigation, not dependency proof."],
        "action_surfaces": ["Fit graph", "Isolate selected node", "Expand neighborhood", "Reset filters", "Copy node id"],
    },
    {
        "id": "docs-sources",
        "label": "Docs & Sources",
        "role": "Document, source and graph artifact references with stale flags.",
        "sections": [
            ("source-links", "Source Links"),
            ("docs-overlays", "Docs Overlays"),
            ("unsupported-languages", "Unsupported Languages"),
        ],
        "approval_boundaries": ["Unsupported or stale graph areas require source reads or owner questions."],
        "action_surfaces": ["Open source artifact", "Check unsupported languages", "Ask owner when evidence is missing"],
    },
    {
        "id": "code-intelligence",
        "label": "Code Intelligence",
        "role": "Hotspots, read order, trace packets, impact hints and Code Flow.",
        "sections": [
            ("hotspots", "Hotspots"),
            ("read-order", "Read Order"),
            ("trace-packets", "Trace Packets"),
            ("impact-packets", "Impact Packets"),
            ("code-flow", "Code Flow"),
        ],
        "approval_boundaries": ["Code intelligence is static and partial; dynamic runtime paths require source/runtime evidence."],
        "action_surfaces": ["Inspect trace", "Open read order", "Read source files", "Confirm ambiguous calls"],
    },
    {
        "id": "contracts",
        "label": "Contracts",
        "role": "API, schema, diagram and explicit contract overlays.",
        "sections": [
            ("contract-overlays", "Contract Overlays"),
            ("schema-overlays", "Schema Overlays"),
            ("diagram-overlays", "Diagram Overlays"),
        ],
        "approval_boundaries": ["Contract overlays do not replace contract tests or owner-approved API changes."],
        "action_surfaces": ["Open contract node", "Check schema edges", "Validate contract tests"],
    },
    {
        "id": "quality-metrics",
        "label": "Quality & Metrics",
        "role": "Tests, fixtures, affected-test packets and quality evidence pointers.",
        "sections": [
            ("tests-fixtures", "Tests & Fixtures"),
            ("affected-tests", "Affected Tests"),
            ("quality-evidence", "Quality Evidence"),
        ],
        "approval_boundaries": ["Affected-test output is partial static evidence and needs actual test execution."],
        "action_surfaces": ["Run focused tests", "Inspect fixture links", "Record verification evidence"],
    },
    {
        "id": "operations-risk",
        "label": "Operations & Risk",
        "role": "Gaps, ambiguous edges, stale data, scale budget and operational risks.",
        "sections": [
            ("graph-gaps", "Graph Gaps"),
            ("ambiguous-edges", "Ambiguous Edges"),
            ("scale-budget", "Scale Budget"),
            ("visual-qa", "Visual QA"),
        ],
        "approval_boundaries": ["Risk and visual QA hints do not approve releases or production changes."],
        "action_surfaces": ["Review gaps", "Confirm ambiguous edges", "Run visual QA", "Escalate owner questions"],
    },
    {
        "id": "proposal-ledger",
        "label": "Proposal Ledger",
        "role": "Generated output ledger, approval boundaries and next proposed actions.",
        "sections": [
            ("artifact-ledger", "Artifact Ledger"),
            ("approval-boundaries", "Approval Boundaries"),
            ("next-actions", "Next Actions"),
        ],
        "approval_boundaries": ["Generated proposals must go through the staged approval flow before workspace writes."],
        "action_surfaces": ["Review staged artifacts", "Check merge plan", "Request explicit approval"],
    },
]


def build_project_cockpit_model(
    graph: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
    query_packets: list[dict[str, Any]] | None = None,
    active_page: str = "overview",
    section_anchor: str = "",
) -> dict[str, Any]:
    """Build a bounded eight-page cockpit model from graph artifacts only."""

    packets = [_compact_query_packet(packet) for packet in (query_packets or []) if isinstance(packet, dict)]
    analysis_packet = analysis if isinstance(analysis, dict) else {}
    graph_summary = _graph_summary(graph)
    source_links = _source_links(graph, analysis_packet)
    stale_flags = _stale_flags(graph, packets, analysis_packet)
    pages = [
        _page(definition, graph_summary, source_links, stale_flags, packets, analysis_packet)
        for definition in _PAGE_DEFINITIONS
    ]
    all_section_ids = {section["id"] for page in pages for section in page["sections"]}
    resolved_active_page = active_page if active_page in COCKPIT_PAGE_IDS else "overview"
    resolved_anchor = section_anchor if section_anchor in all_section_ids else ""
    model_stale_flags = list(stale_flags)
    if active_page and active_page != resolved_active_page:
        model_stale_flags.append("active_page_fallback")
    if section_anchor and section_anchor != resolved_anchor:
        model_stale_flags.append("section_anchor_fallback")

    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "source_policy": SOURCE_POLICY,
        "generated_view_policy": "graph cockpit is generated review output only",
        "safe_next_action": SAFE_NEXT_ACTION,
        "active_page": resolved_active_page,
        "section_anchor": resolved_anchor,
        "pages": pages,
        "navigation": {
            "local_page_anchors": [f"page-{page_id}" for page_id in COCKPIT_PAGE_IDS],
            "local_section_anchors": [f"section-{section_id}" for section_id in sorted(all_section_ids)],
            "section_to_page": {
                section["id"]: page["id"]
                for page in pages
                for section in page["sections"]
            },
        },
        "graph_summary": graph_summary,
        "code_flow": _code_flow(graph),
        "query_packet_summary": packets,
        "analysis_summary": _analysis_summary(analysis_packet),
        "stale_flags": _unique(model_stale_flags),
        "validation": _validate_pages(pages),
    }


def _page(
    definition: dict[str, Any],
    graph_summary: dict[str, Any],
    source_links: list[dict[str, str]],
    stale_flags: list[str],
    packets: list[dict[str, Any]],
    analysis: dict[str, Any],
) -> dict[str, Any]:
    page_id = str(definition["id"])
    sections = [
        {
            "id": section_id,
            "label": label,
            "source_boundary": "section uses graph artifacts and compact packets only",
        }
        for section_id, label in definition["sections"]
    ]
    return {
        "id": page_id,
        "label": str(definition["label"]),
        "role": str(definition["role"]),
        "sections": sections,
        "source_links": _page_source_links(page_id, source_links),
        "stale_flags": stale_flags[:8],
        "graph_packets": _page_packets(page_id, packets, graph_summary, analysis),
        "approval_boundaries": list(definition["approval_boundaries"]),
        "action_surfaces": list(definition["action_surfaces"]),
    }


def _graph_summary(graph: dict[str, Any]) -> dict[str, Any]:
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    language_summary = metadata.get("language_support_summary") if isinstance(metadata.get("language_support_summary"), dict) else {}
    temporal_delta = metadata.get("temporal_delta") if isinstance(metadata.get("temporal_delta"), dict) else {}
    return {
        "scan_id": _text(metadata.get("scan_id")),
        "node_count": _int(metadata.get("node_count"), len(graph.get("nodes", []))),
        "edge_count": _int(metadata.get("edge_count"), len(graph.get("edges", []))),
        "observation_count": _int(metadata.get("observation_count"), len(graph.get("observations", []))),
        "source_boundary": _text(metadata.get("source_boundary") or "raw_source_bodies_excluded"),
        "generated_view_policy": _text(metadata.get("generated_view_policy") or "html_is_review_only"),
        "language_support_summary": {str(key): str(value) for key, value in sorted(language_summary.items())},
        "temporal_delta_status": _text(temporal_delta.get("status") or "not_available"),
    }


def _source_links(graph: dict[str, Any], analysis: dict[str, Any]) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    targets = graph.get("artifact_targets") if isinstance(graph.get("artifact_targets"), dict) else {}
    for label, path in sorted(targets.items()):
        safe_path = safe_relative_path_text(path)
        if safe_path:
            links.append({"label": f"graph_{label}", "path": safe_path, "kind": "graph_artifact"})
    graph_ref = analysis.get("graph_ref") if isinstance(analysis.get("graph_ref"), dict) else {}
    if graph_ref:
        links.append({"label": "analysis_report", "path": "project_graph_analysis", "kind": "generated_report"})
    if not links:
        links.append({"label": "graph_artifact", "path": "not_available", "kind": "not_available"})
    return links[:8]


def _page_source_links(page_id: str, links: list[dict[str, str]]) -> list[dict[str, str]]:
    if page_id in {"project-map", "code-intelligence", "quality-metrics"}:
        return links[:6]
    if page_id == "proposal-ledger":
        return [{"label": "stage_manifest", "path": "product-agent-os-stage-manifest.json", "kind": "approval_artifact"}]
    return links[:3]


def _page_packets(
    page_id: str,
    packets: list[dict[str, Any]],
    graph_summary: dict[str, Any],
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    wanted = {
        "overview": {"status"},
        "project-map": {"neighbors", "path", "trace", "search"},
        "docs-sources": {"status", "search"},
        "code-intelligence": {"trace", "read_order", "hotspots", "impact"},
        "contracts": {"search", "neighbors"},
        "quality-metrics": {"affected_tests", "impact"},
        "operations-risk": {"status", "changed_since", "why_changed"},
        "proposal-ledger": {"status"},
    }
    selected = [packet for packet in packets if packet.get("result_kind") in wanted.get(page_id, set())]
    if selected:
        return selected[:4]
    if page_id == "overview":
        return [{"result_kind": "status", "status": "available", "graph_status": graph_summary}]
    if page_id == "operations-risk" and analysis:
        return [{"result_kind": "analysis", "status": "available", "budget": _safe_budget(analysis.get("budget"))}]
    return []


def _stale_flags(graph: dict[str, Any], packets: list[dict[str, Any]], analysis: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    validation = graph.get("validation") if isinstance(graph.get("validation"), dict) else {}
    if validation and not validation.get("ok", True):
        flags.append("graph_validation_failed")
    temporal_delta = metadata.get("temporal_delta") if isinstance(metadata.get("temporal_delta"), dict) else {}
    if temporal_delta.get("status") in {"changed", "stale"}:
        flags.append(f"temporal_delta_{temporal_delta.get('status')}")
    language_summary = metadata.get("language_support_summary") if isinstance(metadata.get("language_support_summary"), dict) else {}
    if any(str(value) in {"file_only", "unsupported"} for value in language_summary.values()):
        flags.append("unsupported_language_precision")
    if any(packet.get("status") in {"blocked", "not_found"} for packet in packets):
        flags.append("query_packet_gap")
    unsupported = analysis.get("unsupported_language_summary") if isinstance(analysis.get("unsupported_language_summary"), dict) else {}
    if unsupported:
        flags.append("analysis_unsupported_languages")
    return _unique(flags)


def _compact_query_packet(packet: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "result_kind": _text(packet.get("result_kind")),
        "status": _text(packet.get("status")),
        "query_id": _text(packet.get("query_id")),
        "as_of_scan": _text(packet.get("as_of_scan")),
        "node_count": len(packet.get("nodes", [])) if isinstance(packet.get("nodes"), list) else 0,
        "edge_count": len(packet.get("edges", [])) if isinstance(packet.get("edges"), list) else 0,
        "budget": _safe_budget(packet.get("budget")),
        "generated_view_policy": "graph_packets_are_orientation_evidence_only",
    }


def _analysis_summary(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "hotspot_count": len(analysis.get("hotspots", [])) if isinstance(analysis.get("hotspots"), list) else 0,
        "ambiguous_edge_count": (
            len(analysis.get("ambiguous_edge_inventory", []))
            if isinstance(analysis.get("ambiguous_edge_inventory"), list)
            else 0
        ),
        "suggested_question_count": (
            len(analysis.get("suggested_agent_questions", []))
            if isinstance(analysis.get("suggested_agent_questions"), list)
            else 0
        ),
        "budget": _safe_budget(analysis.get("budget")),
    }


def _code_flow(graph: dict[str, Any], limit: int = 20) -> dict[str, Any]:
    nodes = {str(node.get("id")): node for node in graph.get("nodes", []) if isinstance(node, dict)}
    flows: list[dict[str, Any]] = []
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict) or edge.get("type") not in {"calls", "imports", "tests", "references"}:
            continue
        source = str(edge.get("source") or "")
        target = str(edge.get("target") or "")
        flows.append(
            {
                "edge_id": _text(edge.get("id")),
                "type": _text(edge.get("type")),
                "confidence": _text(edge.get("confidence")),
                "status": _text(edge.get("status")),
                "source": _compact_node(nodes.get(source, {"id": source})),
                "target": _compact_node(nodes.get(target, {"id": target})),
                "source_domain": _domain(source),
                "target_domain": _domain(target),
                "safe_next_action": "Read source before treating this flow as complete dependency proof.",
            }
        )
    flows = sorted(flows, key=lambda item: (item["source"]["id"], item["target"]["id"], item["type"]))
    return {
        "source_boundary": "module and call-flow summaries are derived from graph edges only",
        "module_flows": flows[:limit],
        "omitted_count": max(0, len(flows) - limit),
    }


def _compact_node(node: dict[str, Any]) -> dict[str, str]:
    return {
        "id": _text(node.get("id")),
        "type": _text(node.get("type")),
        "label": _text(node.get("label"))[:120],
        "status": _text(node.get("status")),
        "language": _text(node.get("language")),
        "path": safe_relative_path_text(node.get("path")),
    }


def _validate_pages(pages: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    page_ids = [page.get("id") for page in pages]
    if page_ids != COCKPIT_PAGE_IDS:
        errors.append("pages:eight_page_contract_mismatch")
    section_ids = [section.get("id") for page in pages for section in page.get("sections", [])]
    if len(section_ids) != len(set(section_ids)):
        errors.append("sections:not_mapped_once")
    if "code-flow" not in section_ids:
        errors.append("code_flow:missing")
    return {
        "ok": not errors,
        "checks": [
            "exactly eight top-level pages",
            "sections mapped once",
            "Code Flow nested under Code Intelligence",
            "source boundary and approval boundary present",
        ],
        "errors": errors,
    }


def _domain(node_id: str) -> str:
    value = node_id.split(":", 1)[-1]
    for separator in ("/", "."):
        if separator in value:
            return value.split(separator, 1)[0]
    return value


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_budget(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    allowed = {"max_items", "truncated", "omitted_count"}
    result: dict[str, Any] = {}
    for key in allowed:
        if key in source:
            item = source[key]
            result[key] = item if isinstance(item, bool) else _int(item, 0)
    return result


def _int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _text(value: Any) -> str:
    return sanitize_graph_text(value)


def _unique(items: list[str]) -> list[str]:
    unique: list[str] = []
    for item in items:
        if item and item not in unique:
            unique.append(item)
    return unique
