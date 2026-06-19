from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from product_agent_os.first_run_analysis import ANALYSIS_DIR, SECRET_LIKE_VALUE_RE, validate_first_run_analysis_packet
from product_agent_os.project_cockpit_model import COCKPIT_PAGE_IDS, COCKPIT_PAGE_LABELS, build_project_cockpit_model
from product_agent_os.project_graph_visual_model import build_project_graph_visual_model
from product_agent_os.stage_manifest import canonical_json, content_digest


FIRST_RUN_ANALYSIS_PAGE_IDS = [
    "overview",
    "inventory",
    "architecture",
    "methodology",
    "runtime-route",
    "control-plane",
    "graph",
    "code-flow",
    "quality-evals",
    "risks",
    "recommendations",
]
ANALYSIS_RENDERER_VERSION = 1
PRODUCT_AGENT_OS_PLUGIN_VERSION = "local-first-run-analysis"
ANALYSIS_MANIFEST_NAME = "analysis-manifest.json"
FIRST_RUN_COCKPIT_ARTIFACT_SCHEMA_VERSION = "first_run_cockpit_artifact_v1"
FIRST_RUN_COCKPIT_CONTRACT_SCHEMA_VERSION = "first_run_cockpit_artifact_contract_v1"


def render_first_run_analysis_artifact(
    packet: dict[str, Any],
    workspace: str | Path,
    *,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Render a first-run analysis packet into offline in-project HTML artifacts."""

    errors = validate_first_run_analysis_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))
    workspace_path = Path(workspace)
    if not workspace_path.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace_path}")
    if not workspace_path.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace_path}")

    analysis_dir = Path(output_dir) if output_dir is not None else workspace_path / ANALYSIS_DIR
    previous_manifest = _load_previous_manifest(analysis_dir / ANALYSIS_MANIFEST_NAME)
    source_artifacts = _source_artifacts(packet)
    source_digests = {item["artifact_id"]: item["digest"] for item in source_artifacts}
    previous_baseline = _previous_baseline(previous_manifest)
    preliminary_change_summary = _change_summary(previous_manifest, {}, source_digests)
    cleanup_guidance = _cleanup_guidance(FIRST_RUN_ANALYSIS_PAGE_IDS)
    cockpit_contract = build_first_run_cockpit_artifact_contract()
    pages = [
        _page_entry(
            page_id,
            packet,
            previous_baseline=previous_baseline,
            change_summary=preliminary_change_summary,
            cleanup_guidance=cleanup_guidance,
            cockpit_contract=cockpit_contract,
        )
        for page_id in FIRST_RUN_ANALYSIS_PAGE_IDS
    ]
    page_digests = {page["page_id"]: page["digest"] for page in pages}
    change_summary = _change_summary(previous_manifest, page_digests, source_digests)
    primary_cockpit = build_first_run_cockpit_view_model(
        packet,
        previous_baseline=previous_baseline,
        change_summary=change_summary,
        cleanup_guidance=cleanup_guidance,
        cockpit_contract=cockpit_contract,
        page_digests=page_digests,
        source_digests=source_digests,
    )
    redaction_report = _redaction_report(
        [
            packet,
            pages,
            source_artifacts,
            page_digests,
            source_digests,
            previous_baseline,
            change_summary,
            cleanup_guidance,
            cockpit_contract,
            primary_cockpit,
        ]
    )
    if redaction_report["status"] != "passed_redacted":
        raise ValueError("generated analysis artifact failed redaction guardrails")
    analysis_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        path = analysis_dir / page["path"]
        path.write_text(page["html"], encoding="utf-8")
        page.pop("html")

    manifest = {
        "schema_version": "first_run_analysis_manifest_v1",
        "renderer_version": ANALYSIS_RENDERER_VERSION,
        "plugin_version": PRODUCT_AGENT_OS_PLUGIN_VERSION,
        "generated_view_policy": "orientation_only_not_proof",
        "source_packet_digest": packet["packet_digest"],
        "target_fingerprint": _target_fingerprint(packet, source_digests),
        "pages": pages,
        "page_digests": page_digests,
        "source_artifacts": source_artifacts,
        "source_digests": source_digests,
        "previous_baseline": previous_baseline,
        "change_summary": change_summary,
        "cleanup_guidance": cleanup_guidance,
        "cockpit_contract": cockpit_contract,
        "primary_cockpit": _primary_cockpit_manifest_entry(primary_cockpit),
        "redaction_report": redaction_report,
        "source_policy_gate": _source_policy_gate(packet),
        "graph_depth_summary": _graph_depth_summary(packet),
        "graph_artifact_summary": _graph_depth_summary(packet),
    }
    manifest["manifest_digest"] = content_digest(canonical_json(manifest))
    (analysis_dir / ANALYSIS_MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "status": "ready",
        "analysis_dir": ANALYSIS_DIR if output_dir is None else ".",
        "manifest": ANALYSIS_MANIFEST_NAME,
        "page_count": len(pages),
        "written_files": [ANALYSIS_MANIFEST_NAME] + [page["path"] for page in pages],
        "generated_view_policy": "orientation_only_not_proof",
        "primary_cockpit": {
            "schema_version": primary_cockpit["schema_version"],
            "path": primary_cockpit["path"],
            "page_count": primary_cockpit["page_count"],
            "view_model_digest": primary_cockpit["view_model_digest"],
            "selected_graph_renderer": cockpit_contract["selected_graph_renderer"],
        },
        "baseline_comparison": {
            "status": previous_baseline.get("status", "missing"),
            "previous_manifest_digest": previous_baseline.get("manifest_digest", "not_available"),
            "previous_baseline": previous_baseline,
            "change_summary": change_summary,
        },
        "cleanup_guidance": cleanup_guidance,
    }


def _page_entry(
    page_id: str,
    packet: dict[str, Any],
    *,
    previous_baseline: dict[str, Any],
    change_summary: dict[str, list[str]],
    cleanup_guidance: dict[str, Any],
    cockpit_contract: dict[str, Any],
) -> dict[str, Any]:
    path = "index.html" if page_id == "overview" else f"{page_id}.html"
    body = _page_html(
        page_id,
        packet,
        previous_baseline=previous_baseline,
        change_summary=change_summary,
        cleanup_guidance=cleanup_guidance,
        cockpit_contract=cockpit_contract,
    )
    return {
        "page_id": page_id,
        "path": path,
        "digest": content_digest(body),
        "source_policy": "generated_view_only",
        "html": body,
    }


def _page_html(
    page_id: str,
    packet: dict[str, Any],
    *,
    previous_baseline: dict[str, Any],
    change_summary: dict[str, list[str]],
    cleanup_guidance: dict[str, Any],
    cockpit_contract: dict[str, Any],
) -> str:
    if page_id == "overview":
        primary_cockpit = build_first_run_cockpit_view_model(
            packet,
            previous_baseline=previous_baseline,
            change_summary=change_summary,
            cleanup_guidance=cleanup_guidance,
            cockpit_contract=cockpit_contract,
        )
        return _cockpit_page_html(primary_cockpit, previous_baseline, change_summary, cleanup_guidance)
    title = page_id.replace("-", " ").title()
    source_links = "\n".join(
        f"<li><code>{html.escape(item['artifact_id'])}</code>: {html.escape(item['path'])}</li>"
        for item in _source_artifacts(packet)
    )
    sections = "\n".join(
        "<tr>"
        f"<td>{html.escape(section_id)}</td>"
        f"<td>{html.escape(str(summary.get('status', '')))}</td>"
        f"<td>{html.escape(str(summary.get('source_module', '')))}</td>"
        f"<td>{html.escape(str(summary.get('source_artifact', '')))}</td>"
        f"<td>{html.escape(str(summary.get('evidence_freshness', '')))}</td>"
        f"<td>{html.escape(str(summary.get('confidence', '')))}</td>"
        "</tr>"
        for section_id, summary in packet.get("section_summaries", {}).items()
        if isinstance(summary, dict)
    )
    safe_next = html.escape(str(packet.get("safe_next_action", "")))
    graph_depth_html = _graph_depth_html(packet) if page_id == "graph" else ""
    s4_html = _s4_page_summary_html(page_id, packet)
    baseline_html = _baseline_html(previous_baseline, change_summary)
    cleanup_html = _cleanup_html(cleanup_guidance)
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><title>"
        f"{html.escape(title)}"
        "</title></head>\n"
        "<body>\n"
        f"<h1>{html.escape(title)}</h1>\n"
        "<p><strong>generated-view-only</strong>: orientation evidence only, not readiness proof.</p>\n"
        f"<p>Packet digest: <code>{html.escape(str(packet.get('packet_digest', '')))}</code></p>\n"
        f"<p>Safe next action: {safe_next}</p>\n"
        "<h2>Source Artifacts</h2>\n"
        f"<ul>{source_links}</ul>\n"
        "<h2>Section Evidence</h2>\n"
        "<table><thead><tr><th>Section</th><th>Status</th><th>Module</th><th>Artifact</th><th>Freshness</th><th>Confidence</th></tr></thead>"
        f"<tbody>{sections}</tbody></table>\n"
        f"{s4_html}"
        f"{baseline_html}"
        f"{cleanup_html}"
        f"{graph_depth_html}"
        "</body>\n"
        "</html>\n"
    )


def build_first_run_cockpit_artifact_contract() -> dict[str, Any]:
    """Describe the primary Batch 41 S7 first-run cockpit artifact contract."""

    return {
        "schema_version": FIRST_RUN_COCKPIT_CONTRACT_SCHEMA_VERSION,
        "artifact_schema_version": FIRST_RUN_COCKPIT_ARTIFACT_SCHEMA_VERSION,
        "primary_artifact": "index.html",
        "artifact_mode": "single_self_contained_index_html",
        "legacy_diagnostics_policy": "separate first-run pages are diagnostic/raw evidence only",
        "generated_view_policy": "orientation_only_not_proof",
        "primary_pages": [
            {"id": page_id, "label": label}
            for page_id, label in zip(COCKPIT_PAGE_IDS, COCKPIT_PAGE_LABELS, strict=True)
        ],
        "graph_layers": ["project_file_source_graph", "code_graph_when_available"],
        "graph_interchange": "Graphology-compatible payload",
        "selected_graph_renderer": "Cosmos.gl",
        "renderer_policy": {
            "primary": "Cosmos.gl",
            "fallback": "static summary, cluster cards and bounded table fallback",
            "sigma_js": "compatibility_or_fallback_only",
            "dependency_policy": "no CDN, no network fetch, no install by default",
            "vendored_library_requires": ["version", "license", "hash", "offline validation evidence"],
        },
        "large_graph_policy": {
            "do_not_render_full_graph_by_default_at": {"nodes": 5000, "edges": 50000},
            "default_strategy": [
                "clustered overview",
                "sampled or aggregated edges",
                "selected-neighborhood expansion",
                "LOD label suppression",
                "bounded table fallback",
            ],
        },
        "fallback_states": ["not_available", "static_table_fallback", "cluster_summary_only"],
        "raw_diagnostics_policy": "raw packet diagnostics appear outside the primary reading path",
        "unsupported_claims": [
            "release readiness",
            "runtime/browser proof",
            "provider/API/model quality",
            "target apply safety",
            "source-read semantic completeness",
            "external writes or deployment safety",
        ],
    }


def _primary_cockpit_manifest_entry(view_model: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": view_model["schema_version"],
        "path": view_model["path"],
        "page_count": view_model["page_count"],
        "view_model_digest": view_model["view_model_digest"],
        "generated_view_policy": view_model["generated_view_policy"],
        "view_model": view_model,
    }


def build_first_run_cockpit_view_model(
    packet: dict[str, Any],
    *,
    previous_baseline: dict[str, Any],
    change_summary: dict[str, list[str]],
    cleanup_guidance: dict[str, Any],
    cockpit_contract: dict[str, Any] | None = None,
    page_digests: dict[str, str] | None = None,
    source_digests: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build the bounded first-run cockpit view model from packet and manifest inputs."""

    contract = cockpit_contract or build_first_run_cockpit_artifact_contract()
    graph_payload = _first_run_cockpit_graph_payload(packet)
    cockpit = build_project_cockpit_model(
        graph_payload,
        analysis=_first_run_cockpit_analysis(packet),
        query_packets=[],
        active_page="overview",
    )
    source_artifacts = _source_artifacts(packet)
    section_cards = _section_status_cards(packet)
    source_file_graph = _first_run_source_file_graph_view(graph_payload, contract)
    code_graph = _first_run_code_graph_view(packet, contract)
    navigation_search = _first_run_navigation_search_model(cockpit, section_cards, source_file_graph, code_graph)
    progressive_diagnostics = _first_run_progressive_diagnostics(
        packet,
        previous_baseline=previous_baseline,
        change_summary=change_summary,
        cleanup_guidance=cleanup_guidance,
    )
    visual_qa = _first_run_visual_qa_contract(source_file_graph, code_graph)
    safety_accessibility = _first_run_safety_accessibility_contract()
    model = {
        "schema_version": FIRST_RUN_COCKPIT_ARTIFACT_SCHEMA_VERSION,
        "path": "index.html",
        "page_count": len(COCKPIT_PAGE_IDS),
        "generated_view_policy": "orientation_only_not_proof",
        "source_truth_policy": "source files and current command evidence remain source truth",
        "contract": contract,
        "cockpit": cockpit,
        "overview": {
            "target": packet.get("target", {}),
            "safe_next_action": str(packet.get("safe_next_action", "")),
            "completion_claim": packet.get("evidence_status", {}).get("completion_claim", "not_claimed"),
            "unsupported_claims": _unsupported_claims(packet),
        },
        "source_file_graph": source_file_graph,
        "code_graph": code_graph,
        "navigation_search": navigation_search,
        "progressive_diagnostics": progressive_diagnostics,
        "visual_qa": visual_qa,
        "safety_accessibility": safety_accessibility,
        "section_cards": section_cards,
        "source_artifacts": source_artifacts,
        "baseline_comparison": {
            "status": previous_baseline.get("status", "missing"),
            "change_summary": change_summary,
        },
        "cleanup_guidance": cleanup_guidance,
        "page_digests": page_digests or {},
        "source_digests": source_digests or {},
    }
    model["view_model_digest"] = content_digest(canonical_json(model))
    return model


def _first_run_cockpit_graph_payload(packet: dict[str, Any]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    artifact_targets: dict[str, str] = {}
    for artifact in _source_artifacts(packet):
        artifact_id = artifact["artifact_id"] or "artifact"
        node_id = f"source:{artifact_id}"
        artifact_targets[artifact_id] = artifact["path"]
        nodes.append(
            {
                "id": node_id,
                "type": "source_artifact",
                "label": artifact_id,
                "status": artifact.get("evidence_status", "inspection_only"),
                "language": "",
                "path": artifact["path"],
            }
        )
    for section_id, summary in packet.get("section_summaries", {}).items():
        if not isinstance(summary, dict):
            continue
        section_node = f"section:{section_id}"
        nodes.append(
            {
                "id": section_node,
                "type": "section",
                "label": section_id,
                "status": str(summary.get("status", "not_available")),
                "language": "",
                "path": str(summary.get("source_artifact", "")),
            }
        )
        source_artifact = str(summary.get("source_artifact", ""))
        for artifact in _source_artifacts(packet):
            if artifact["artifact_id"] and artifact["artifact_id"] in source_artifact:
                edges.append(
                    {
                        "id": f"edge:{artifact['artifact_id']}:{section_id}",
                        "source": f"source:{artifact['artifact_id']}",
                        "target": section_node,
                        "type": "references",
                        "confidence": "inferred",
                        "status": "generated",
                    }
                )
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "metadata": {
            "scan_id": "first-run-cockpit",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "observation_count": len(nodes) + len(edges),
            "source_boundary": "raw_source_bodies_excluded",
            "generated_view_policy": "orientation_only_not_proof",
        },
        "artifact_targets": artifact_targets,
        "nodes": nodes,
        "edges": edges,
        "observations": [],
    }


def _first_run_source_file_graph_view(graph_payload: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    visual = build_project_graph_visual_model(graph_payload, max_nodes=500, max_edges=1_000)
    cosmos_payload = _cosmos_payload_from_visual_projection(visual)
    budget = visual.get("performance_budget") if isinstance(visual.get("performance_budget"), dict) else {}
    return {
        "schema_version": "first_run_source_file_graph_view_v1",
        "status": "adapter_ready",
        "write_policy": "read_only",
        "source_boundary": "raw_source_bodies_excluded",
        "renderer": "Cosmos.gl",
        "selected_renderer": "Cosmos.gl",
        "renderer_mode": "cosmos_gl_payload_with_static_html_fallback",
        "runtime_asset_status": "not_vendored_static_fallback",
        "external_assets": "forbidden",
        "renderer_policy": contract.get("renderer_policy", {}),
        "graphology_compatible_payload": True,
        "graphology_payload": {
            "schema_version": graph_payload.get("schema_version", 1),
            "metadata": graph_payload.get("metadata", {}),
            "nodes": graph_payload.get("nodes", []),
            "edges": graph_payload.get("edges", []),
        },
        "cosmos_payload": cosmos_payload,
        "visual_projection": visual,
        "legend": _graph_legend(visual),
        "status_colors": _graph_status_colors(visual),
        "selected_file_panel": _selected_file_panel(visual),
        "table_fallback": _graph_table_fallback(visual),
        "large_graph_policy": contract.get("large_graph_policy", {}),
        "cluster_policy": "clustered_overview_with_lod_label_suppression",
        "node_count": int(budget.get("declared_node_count", len(graph_payload.get("nodes", [])))),
        "edge_count": int(budget.get("declared_edge_count", len(graph_payload.get("edges", [])))),
        "visible_node_count": int(budget.get("visible_node_count", 0)),
        "visible_edge_count": int(budget.get("visible_edge_count", 0)),
        "omitted_node_count": int(budget.get("omitted_node_count", 0)),
        "omitted_edge_count": int(budget.get("omitted_edge_count", 0)),
        "source_artifact_count": len(graph_payload.get("artifact_targets", {})),
        "section_count": len([node for node in graph_payload.get("nodes", []) if node.get("type") == "section"]),
        "generated_view_policy": "orientation_only_not_proof",
        "source_read_required": True,
        "must_read_source_before_edit": True,
        "safe_next_action": "Use the file/source graph for navigation only; read source files before edits.",
    }


def _first_run_code_graph_view(packet: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    graph_summary = _graph_depth_summary(packet)
    status = str(graph_summary.get("status", "not_available") or "not_available")
    if status in {"", "not_available"}:
        return {
            "schema_version": "first_run_code_graph_view_v1",
            "status": "not_available",
            "write_policy": "read_only",
            "source_boundary": "raw_source_bodies_excluded",
            "renderer": "Cosmos.gl",
            "selected_renderer": "Cosmos.gl",
            "renderer_mode": "not_available_static_empty_state",
            "runtime_asset_status": "not_vendored_static_fallback",
            "external_assets": "forbidden",
            "renderer_policy": contract.get("renderer_policy", {}),
            "graphology_compatible_payload": True,
            "empty_state": "not_available",
            "not_available_reason": "No code graph packet data is present in the first-run packet.",
            "large_graph_policy": contract.get("large_graph_policy", {}),
            "node_count": 0,
            "edge_count": 0,
            "visible_node_count": 0,
            "visible_edge_count": 0,
            "omitted_node_count": 0,
            "omitted_edge_count": 0,
            "hotspots": [],
            "hotspot_count": 0,
            "relationships": _empty_code_graph_relationships(),
            "table_fallback": {"status": "empty", "rows": []},
            "safe_next_action": "Run or refresh the project graph packet, then read source files before graph-backed edits.",
            "generated_view_policy": "orientation_only_not_proof",
            "source_read_required": True,
            "must_read_source_before_edit": True,
        }
    graph_payload = _first_run_code_graph_payload(graph_summary)
    visual = build_project_graph_visual_model(graph_payload, max_nodes=500, max_edges=1_000)
    budget = visual.get("performance_budget") if isinstance(visual.get("performance_budget"), dict) else {}
    hotspots = _code_graph_hotspots(graph_summary)
    return {
        "schema_version": "first_run_code_graph_view_v1",
        "status": "available",
        "availability_detail": "summary_available",
        "write_policy": "read_only",
        "source_boundary": "raw_source_bodies_excluded",
        "renderer": "Cosmos.gl",
        "selected_renderer": "Cosmos.gl",
        "renderer_mode": "cosmos_gl_summary_payload_with_static_html_fallback",
        "runtime_asset_status": "not_vendored_static_fallback",
        "external_assets": "forbidden",
        "renderer_policy": contract.get("renderer_policy", {}),
        "graphology_compatible_payload": True,
        "empty_state": "",
        "graph_packet_ref": graph_summary.get("graph_packet_digest", ""),
        "graphology_payload": graph_payload,
        "cosmos_payload": _cosmos_payload_from_visual_projection(visual),
        "visual_projection": visual,
        "legend": _graph_legend(visual),
        "status_colors": _graph_status_colors(visual),
        "selected_file_panel": _selected_file_panel(visual),
        "table_fallback": _graph_table_fallback(visual),
        "large_graph_policy": contract.get("large_graph_policy", {}),
        "node_count": int(budget.get("declared_node_count", len(graph_payload.get("nodes", [])))),
        "edge_count": int(budget.get("declared_edge_count", len(graph_payload.get("edges", [])))),
        "visible_node_count": int(budget.get("visible_node_count", 0)),
        "visible_edge_count": int(budget.get("visible_edge_count", 0)),
        "omitted_node_count": int(budget.get("omitted_node_count", 0)),
        "omitted_edge_count": int(budget.get("omitted_edge_count", 0)),
        "hotspots": hotspots,
        "hotspot_count": len(hotspots),
        "relationships": _code_graph_relationships(graph_summary),
        "safe_next_action": graph_summary.get("freshness", {}).get(
            "safe_next_action",
            "Read source files before graph-backed edits or completion claims.",
        )
        if isinstance(graph_summary.get("freshness"), dict)
        else "Read source files before graph-backed edits or completion claims.",
        "generated_view_policy": "orientation_only_not_proof",
        "source_policy": graph_summary.get("source_policy", "graph artifacts are generated orientation evidence, not source truth"),
        "source_read_required": True,
        "must_read_source_before_edit": True,
    }


def _first_run_code_graph_payload(graph_summary: dict[str, Any]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = [
        {
            "id": "code_graph:summary",
            "type": "code_graph_summary",
            "label": "Code graph summary",
            "status": str(graph_summary.get("status", "inspection_only")),
            "language": "",
            "path": "graph_artifact_summary",
        }
    ]
    edges: list[dict[str, Any]] = []

    def add_node(node_id: str, node_type: str, label: str, status: str, path: str = "") -> None:
        nodes.append({"id": node_id, "type": node_type, "label": label, "status": status, "language": "", "path": path})
        edges.append(
            {
                "id": f"edge:code_graph:summary:{node_id}",
                "source": "code_graph:summary",
                "target": node_id,
                "type": "references",
                "confidence": "inferred",
                "status": "generated",
            }
        )

    coverage = graph_summary.get("coverage") if isinstance(graph_summary.get("coverage"), dict) else {}
    if coverage:
        add_node("code_graph:coverage", "coverage", "Coverage", str(coverage.get("status", "not_available")))
    freshness = graph_summary.get("freshness") if isinstance(graph_summary.get("freshness"), dict) else {}
    if freshness:
        add_node("code_graph:freshness", "freshness", "Freshness", str(freshness.get("status", "not_available")))
    rejected = graph_summary.get("rejected_link_summary") if isinstance(graph_summary.get("rejected_link_summary"), dict) else {}
    if int(rejected.get("total", 0) or 0) > 0:
        add_node("code_graph:rejected_links", "rejected_links", "Rejected links", "inspection_only")
    framework = graph_summary.get("framework_semantic_summary") if isinstance(graph_summary.get("framework_semantic_summary"), dict) else {}
    if int(framework.get("total", 0) or 0) > 0:
        add_node("code_graph:framework_semantics", "framework_semantics", "Framework semantics", "inspection_only")
    for index, ref in enumerate(graph_summary.get("agent_packet_refs", []) if isinstance(graph_summary.get("agent_packet_refs"), list) else []):
        if not isinstance(ref, dict):
            continue
        add_node(
            f"code_graph:agent_packet:{index}",
            "agent_packet",
            str(ref.get("kind", "agent_packet")),
            "inspection_only",
            str(ref.get("path", "")),
        )
    for index, item in enumerate(graph_summary.get("guided_tour", []) if isinstance(graph_summary.get("guided_tour"), list) else []):
        if not isinstance(item, dict):
            continue
        add_node(
            f"code_graph:guided_tour:{index}",
            "guided_tour",
            str(item.get("page", "guided_tour")),
            "inspection_only",
        )
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "metadata": {
            "scan_id": "first-run-code-graph-summary",
            "node_count": len(nodes),
            "edge_count": len(edges),
            "observation_count": len(nodes) + len(edges),
            "source_boundary": "raw_source_bodies_excluded",
            "generated_view_policy": "orientation_only_not_proof",
        },
        "artifact_targets": {"summary": "graph_artifact_summary"},
        "nodes": nodes,
        "edges": edges,
        "observations": [],
    }


def _cosmos_payload_from_visual_projection(projection: dict[str, Any]) -> dict[str, Any]:
    nodes = projection.get("nodes") if isinstance(projection.get("nodes"), list) else []
    edges = projection.get("edges") if isinstance(projection.get("edges"), list) else []
    node_index_by_id: dict[str, int] = {}
    cosmos_nodes: list[dict[str, Any]] = []
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        node_id = str(node.get("key", ""))
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        node_index_by_id[node_id] = len(cosmos_nodes)
        cosmos_nodes.append(
            {
                "index": len(cosmos_nodes),
                "id": node_id,
                "label": str(attrs.get("label", "")),
                "type": str(attrs.get("type", "")),
                "status": str(attrs.get("status", "")),
                "x": float(attrs.get("x") or 0),
                "y": float(attrs.get("y") or 0),
                "size": float(attrs.get("size") or 1),
                "color": str(attrs.get("color", "")),
                "cluster": str(attrs.get("community", "")),
                "lod_tier": int(attrs.get("lod_tier") or 0),
                "label_priority": int(attrs.get("label_priority") or 0),
            }
        )
    cosmos_links: list[dict[str, Any]] = []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        source_id = str(edge.get("source", ""))
        target_id = str(edge.get("target", ""))
        if source_id not in node_index_by_id or target_id not in node_index_by_id:
            continue
        attrs = edge.get("attributes") if isinstance(edge.get("attributes"), dict) else {}
        cosmos_links.append(
            {
                "index": len(cosmos_links),
                "id": str(edge.get("key", "")),
                "source": node_index_by_id[source_id],
                "target": node_index_by_id[target_id],
                "source_id": source_id,
                "target_id": target_id,
                "type": str(attrs.get("type", "")),
                "status": str(attrs.get("status", "")),
                "color": str(attrs.get("color", "")),
                "size": float(attrs.get("size") or 1),
            }
        )
    return {
        "schema_version": "cosmos_gl_static_adapter_v1",
        "renderer": "Cosmos.gl",
        "adapter_status": "payload_ready_runtime_not_bundled",
        "external_assets": "forbidden",
        "typed_array_contract": {
            "node_positions": "x/y fields are deterministic numeric coordinates",
            "link_indices": "source/target fields are zero-based node indexes",
            "index_maps": "node_index_by_id preserves Graphology ids for selected-neighborhood lookup",
        },
        "nodes": cosmos_nodes,
        "links": cosmos_links,
        "node_index_by_id": node_index_by_id,
        "link_index_by_id": {item["id"]: item["index"] for item in cosmos_links},
    }


def _graph_legend(projection: dict[str, Any]) -> list[dict[str, Any]]:
    clusters = projection.get("clusters") if isinstance(projection.get("clusters"), list) else []
    return [
        {
            "id": str(cluster.get("id", "")),
            "label": str(cluster.get("label", "")),
            "color": str(cluster.get("color", "")),
            "node_count": int(cluster.get("node_count", 0) or 0),
            "lod_tier": int(cluster.get("lod_tier", 0) or 0),
        }
        for cluster in clusters[:12]
        if isinstance(cluster, dict)
    ]


def _graph_status_colors(projection: dict[str, Any]) -> dict[str, str]:
    colors: dict[str, str] = {}
    for node in projection.get("nodes", []) if isinstance(projection.get("nodes"), list) else []:
        if not isinstance(node, dict):
            continue
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        status = str(attrs.get("status", "") or "unknown")
        colors.setdefault(status, str(attrs.get("color", "") or "#7d8793"))
    return colors


def _selected_file_panel(projection: dict[str, Any]) -> dict[str, Any]:
    selected = projection.get("focused_subgraph") if isinstance(projection.get("focused_subgraph"), dict) else {}
    node = selected.get("selected_node") if isinstance(selected.get("selected_node"), dict) else {}
    if not node:
        rows = _graph_table_fallback(projection).get("rows", [])
        node = rows[0] if rows else {}
    return {
        "status": "selected" if node else "not_selected",
        "node_id": str(node.get("id", "")),
        "type": str(node.get("type", "")),
        "label": str(node.get("label", "")),
        "path": str(node.get("path", "")),
        "source_boundary": "raw source bodies are excluded; selected file is an orientation pointer only",
    }


def _graph_table_fallback(projection: dict[str, Any], limit: int = 80) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    for node in projection.get("nodes", []) if isinstance(projection.get("nodes"), list) else []:
        if not isinstance(node, dict):
            continue
        attrs = node.get("attributes") if isinstance(node.get("attributes"), dict) else {}
        rows.append(
            {
                "id": str(node.get("key", "")),
                "type": str(attrs.get("type", "")),
                "status": str(attrs.get("status", "")),
                "cluster": str(attrs.get("community", "")),
                "path": str(attrs.get("path", "")),
            }
        )
    return {
        "status": "available" if rows else "empty",
        "rows": rows[:limit],
        "omitted_row_count": max(0, len(rows) - limit),
    }


def _code_graph_hotspots(graph_summary: dict[str, Any]) -> list[dict[str, str]]:
    hotspots: list[dict[str, str]] = []
    coverage = graph_summary.get("coverage") if isinstance(graph_summary.get("coverage"), dict) else {}
    if coverage:
        hotspots.append(
            {
                "id": "coverage",
                "status": str(coverage.get("status", "not_available")),
                "detail": f"covered_files={coverage.get('covered_files', 0)} partial_files={coverage.get('partial_files', 0)}",
            }
        )
        unsupported = coverage.get("unsupported_languages") if isinstance(coverage.get("unsupported_languages"), dict) else {}
        for language, status in sorted(unsupported.items())[:6]:
            hotspots.append({"id": f"unsupported_language:{language}", "status": str(status), "detail": "source read required"})
    freshness = graph_summary.get("freshness") if isinstance(graph_summary.get("freshness"), dict) else {}
    if freshness:
        hotspots.append(
            {
                "id": "freshness",
                "status": str(freshness.get("status", "not_available")),
                "detail": str(freshness.get("safe_next_action", "Read source files before action.")),
            }
        )
    rejected = graph_summary.get("rejected_link_summary") if isinstance(graph_summary.get("rejected_link_summary"), dict) else {}
    if int(rejected.get("total", 0) or 0) > 0:
        hotspots.append({"id": "rejected_links", "status": "inspection_only", "detail": f"total={rejected.get('total', 0)}"})
    return hotspots[:12]


def _empty_code_graph_relationships() -> dict[str, Any]:
    return {
        "imports": {"status": "not_available", "count": 0},
        "calls": {"status": "not_available", "count": 0},
        "tests": {"status": "not_available", "count": 0},
        "routes": {"status": "not_available", "count": 0},
        "code_flow": {"status": "not_available", "count": 0},
        "read_order": {"status": "not_available", "count": 0},
        "trace_impact": {"status": "not_available", "count": 0},
    }


def _code_graph_relationships(graph_summary: dict[str, Any]) -> dict[str, Any]:
    relationships = _empty_code_graph_relationships()
    refs = graph_summary.get("agent_packet_refs") if isinstance(graph_summary.get("agent_packet_refs"), list) else []
    guided_tour = graph_summary.get("guided_tour") if isinstance(graph_summary.get("guided_tour"), list) else []
    coverage = graph_summary.get("coverage") if isinstance(graph_summary.get("coverage"), dict) else {}
    relationships["read_order"] = {"status": "summary_available" if guided_tour else "not_available", "count": len(guided_tour)}
    relationships["trace_impact"] = {"status": "summary_available" if refs else "not_available", "count": len(refs)}
    relationships["code_flow"] = {
        "status": str(coverage.get("status", "summary_available")) if coverage else "summary_available",
        "count": int(coverage.get("covered_files", 0) or 0) if coverage else 0,
    }
    return relationships


def _first_run_navigation_search_model(
    cockpit: dict[str, Any],
    section_cards: list[dict[str, str]],
    source_file_graph: dict[str, Any],
    code_graph: dict[str, Any],
) -> dict[str, Any]:
    pages = cockpit.get("pages") if isinstance(cockpit.get("pages"), list) else []
    anchors = [f"page-{page.get('id')}" for page in pages if isinstance(page, dict) and page.get("id")]
    rows = source_file_graph.get("table_fallback", {}).get("rows", [])
    graph_rows = rows if isinstance(rows, list) else []
    search_index: list[dict[str, str]] = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        page_id = str(page.get("id", ""))
        search_index.append(
            {
                "id": f"page:{page_id}",
                "label": str(page.get("label", "")),
                "kind": "page",
                "anchor": f"#page-{page_id}",
                "tokens": " ".join([str(page.get("label", "")), str(page.get("role", ""))]).lower(),
            }
        )
    for card in section_cards:
        search_index.append(
            {
                "id": f"section:{card['id']}",
                "label": card["id"],
                "kind": "section_status",
                "anchor": "#status-cards",
                "tokens": " ".join([card["id"], card["status"], card["confidence"], card["source_artifact"]]).lower(),
            }
        )
    for row in graph_rows[:80]:
        if not isinstance(row, dict):
            continue
        search_index.append(
            {
                "id": str(row.get("id", "")),
                "label": str(row.get("id", "")),
                "kind": "graph_node",
                "anchor": "#page-project-map",
                "tokens": " ".join(str(row.get(field, "")) for field in ["id", "type", "status", "cluster", "path"]).lower(),
            }
        )
    return {
        "schema_version": "first_run_cockpit_navigation_search_v1",
        "status": "static_controls_ready",
        "interaction_policy": "offline_no_script_static_controls_with_table_fallback",
        "persistent_navigation": True,
        "skip_link_target": "#main-content",
        "anchors": anchors,
        "search_index": search_index[:160],
        "search_index_count": min(len(search_index), 160),
        "filters": [
            {"id": "section-status-filter", "label": "Section status", "source": "section_cards", "field": "status"},
            {"id": "graph-node-type-filter", "label": "Graph node type", "source": "source_file_graph", "field": "type"},
            {"id": "graph-status-filter", "label": "Graph status", "source": "source_file_graph", "field": "status"},
            {"id": "code-graph-status-filter", "label": "Code graph status", "source": "code_graph", "field": "status"},
        ],
        "filter_state": {
            "mode": "static_default_all_visible",
            "script_required": False,
            "layout_shift_policy": "controls have stable dimensions and tables remain visible",
        },
        "detail_panels": [
            {"id": "source-file-graph-selected-file-panel", "kind": "selected_file", "status": source_file_graph["selected_file_panel"]["status"]},
            {"id": "code-graph-selected-file-panel", "kind": "selected_code_graph_node", "status": code_graph.get("selected_file_panel", {}).get("status", "not_available")},
            {"id": "cockpit-diagnostics", "kind": "progressive_diagnostics", "status": "collapsed_by_default"},
        ],
        "keyboard_contract": {
            "controls": ["skip link", "anchor navigation", "labelled search input", "labelled select filters", "details summary"],
            "focus_management": "native browser focus order only; no custom JavaScript trap",
        },
    }


def _first_run_progressive_diagnostics(
    packet: dict[str, Any],
    *,
    previous_baseline: dict[str, Any],
    change_summary: dict[str, list[str]],
    cleanup_guidance: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "first_run_progressive_diagnostics_v1",
        "status": "collapsed_diagnostics_ready",
        "raw_json_policy": "collapsed_only_or_packet_ref",
        "primary_surface_policy": "human_summary_first_no_preformatted_json_dump",
        "diagnostic_sections": [
            {
                "id": "packet-boundary",
                "label": "Packet Boundary",
                "status": packet.get("evidence_status", {}).get("overall_status", "inspection_only"),
                "detail": "Primary cockpit shows summaries; raw packet JSON stays outside the main reading path.",
            },
            {
                "id": "baseline-diff",
                "label": "Baseline Diff",
                "status": previous_baseline.get("status", "missing"),
                "detail": f"changed_pages={len(change_summary.get('changed_pages', []))}; added_sources={len(change_summary.get('added_sources', []))}",
            },
            {
                "id": "cleanup-rollback",
                "label": "Cleanup And Rollback",
                "status": cleanup_guidance.get("status", "preview_only"),
                "detail": cleanup_guidance.get("rollback_policy", "cleanup requires explicit approval"),
            },
            {
                "id": "source-policy",
                "label": "Source Policy",
                "status": packet.get("section_summaries", {}).get("source_policy", {}).get("status", "not_available"),
                "detail": "Source files and current command evidence remain source truth.",
            },
        ],
        "raw_packet_ref": "first-run-analysis-packet.json",
        "html_elements": ["details", "summary", "compact-table"],
        "source_read_required": True,
    }


def _first_run_visual_qa_contract(source_file_graph: dict[str, Any], code_graph: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "first_run_cockpit_static_visual_qa_v1",
        "status": "static_checks_present_browser_gap_accepted",
        "browser_screenshot_status": "not_run_approval_required",
        "checks": [
            {"id": "cockpit-shell-not-default-browser", "status": "present_static_css"},
            {"id": "persistent-nav-visible", "status": "present_static_html"},
            {"id": "generated-view-label-visible", "status": "present_static_html"},
            {"id": "source-graph-visible", "status": "present" if source_file_graph.get("visible_node_count", 0) else "empty_state_present"},
            {"id": "code-graph-state-visible", "status": code_graph.get("status", "not_available")},
            {"id": "mobile-breakpoint", "status": "present_static_css"},
            {"id": "text-overflow-guard", "status": "present_static_css"},
            {"id": "white-page-regression-gate", "status": "blocked_by_static_assertions"},
        ],
        "accepted_static_gaps": [
            "No browser screenshot, canvas pixel, layout engine or responsiveness proof was produced in this slice.",
            "Cosmos.gl runtime execution remains unverified until an approved browser/runtime pass.",
        ],
    }


def _first_run_safety_accessibility_contract() -> dict[str, Any]:
    return {
        "schema_version": "first_run_cockpit_safety_accessibility_v1",
        "status": "static_contract_present",
        "offline_policy": {
            "external_urls_allowed": False,
            "script_tags_allowed": False,
            "fetch_allowed": False,
            "network_dependency_allowed": False,
        },
        "privacy_policy": {
            "absolute_local_paths_allowed": False,
            "raw_source_bodies_allowed": False,
            "secret_like_values_allowed": False,
            "private_logs_allowed": False,
        },
        "accessibility_contract": {
            "landmarks": ["main", "nav", "section"],
            "keyboard_reachable_controls": ["skip link", "nav anchors", "search input", "select filters", "details summary"],
            "labels_required": True,
            "aria_labels_required": True,
            "contrast_policy": "light theme uses dark text on light panels and non-color status text",
        },
        "readability_contract": {
            "font_family": "Arial, Helvetica, sans-serif",
            "overflow_wrap": "anywhere",
            "mobile_breakpoint": "760px",
            "stable_graph_min_height": "320px desktop / 240px mobile",
        },
    }


def _first_run_cockpit_analysis(packet: dict[str, Any]) -> dict[str, Any]:
    graph_summary = _graph_depth_summary(packet)
    return {
        "graph_ref": {
            "scan_id": "first-run-cockpit",
            "node_count": len(_source_artifacts(packet)) + len(packet.get("section_summaries", {})),
            "edge_count": 0,
        },
        "hotspots": [],
        "ambiguous_edge_inventory": [],
        "unsupported_language_summary": graph_summary.get("coverage", {}).get("unsupported_languages", {})
        if isinstance(graph_summary.get("coverage"), dict)
        else {},
        "suggested_agent_questions": [],
        "budget": {"max_items": 80, "truncated": False, "omitted_count": 0},
    }


def _section_status_cards(packet: dict[str, Any]) -> list[dict[str, str]]:
    cards: list[dict[str, str]] = []
    for section_id, summary in packet.get("section_summaries", {}).items():
        if not isinstance(summary, dict):
            continue
        cards.append(
            {
                "id": str(section_id),
                "status": str(summary.get("status", "not_available")),
                "confidence": str(summary.get("confidence", "unknown")),
                "source_artifact": str(summary.get("source_artifact", "not_available")),
                "safe_next_action": _section_safe_next_action(section_id, summary),
            }
        )
    return sorted(cards, key=lambda item: item["id"])


def _section_safe_next_action(section_id: str, summary: dict[str, Any]) -> str:
    unsupported = summary.get("unsupported_claims")
    if isinstance(unsupported, list) and unsupported:
        return f"Review {section_id} blockers before stronger claims."
    if summary.get("status") == "approval_required":
        return f"Request exact approval before expanding {section_id}."
    return "Use this section as orientation; verify source evidence before action."


def _unsupported_claims(packet: dict[str, Any]) -> list[str]:
    claims: list[str] = []
    evidence_claims = packet.get("evidence_status", {}).get("unsupported_claims")
    if isinstance(evidence_claims, list):
        claims.extend(str(item) for item in evidence_claims)
    for summary in packet.get("section_summaries", {}).values():
        if not isinstance(summary, dict):
            continue
        section_claims = summary.get("unsupported_claims")
        if isinstance(section_claims, list):
            claims.extend(str(item) for item in section_claims)
    return sorted(set(item for item in claims if item))


def _cockpit_page_html(
    primary_cockpit: dict[str, Any],
    previous_baseline: dict[str, Any],
    change_summary: dict[str, list[str]],
    cleanup_guidance: dict[str, Any],
) -> str:
    contract = primary_cockpit["contract"]
    cockpit = primary_cockpit["cockpit"]
    pages = cockpit.get("pages") if isinstance(cockpit.get("pages"), list) else []
    nav = "\n".join(
        f'<a href="#page-{_attr(page.get("id"))}">{_text(page.get("label"))}</a>'
        for page in pages
        if isinstance(page, dict)
    )
    controls_html = _cockpit_controls_html(primary_cockpit)
    status_cards = "\n".join(
        "<article class=\"status-card\">"
        f"<h3>{_text(card['id'])}</h3>"
        f"<p>Status <strong>{_text(card['status'])}</strong></p>"
        f"<p>Confidence {_text(card['confidence'])}</p>"
        f"<p>{_text(card['safe_next_action'])}</p>"
        "</article>"
        for card in primary_cockpit.get("section_cards", [])[:12]
    )
    pages_html = "\n".join(_cockpit_section_html(page, primary_cockpit) for page in pages if isinstance(page, dict))
    unsupported = "\n".join(
        f"<li>{_text(claim)}</li>"
        for claim in primary_cockpit.get("overview", {}).get("unsupported_claims", [])[:12]
    )
    baseline_rows = _definition_rows(
        [
            ("Status", previous_baseline.get("status", "missing")),
            ("Previous manifest", previous_baseline.get("manifest_digest", "not_available")),
            ("Changed pages", ", ".join(change_summary.get("changed_pages", [])) or "none"),
            ("Added sources", ", ".join(change_summary.get("added_sources", [])) or "none"),
        ]
    )
    cleanup_rows = _definition_rows(
        [
            ("Status", cleanup_guidance.get("status", "preview_only")),
            ("Approval required", str(cleanup_guidance.get("approval_required", True)).lower()),
            ("Deletion performed", str(cleanup_guidance.get("deletion_performed", False)).lower()),
            ("Rollback", cleanup_guidance.get("rollback_policy", "")),
        ]
    )
    diagnostics_html = _progressive_diagnostics_html(primary_cockpit)
    css = _cockpit_css()
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Product-Agent OS First-Run Cockpit</title>"
        f"<style>{css}</style></head>\n"
        "<body>\n"
        "<a class=\"skip-link\" href=\"#main-content\">Skip to cockpit content</a>\n"
        "<main id=\"main-content\" class=\"first-run-cockpit cockpit-shell\" data-schema=\"first_run_cockpit_artifact_v1\" tabindex=\"-1\">\n"
        "<header class=\"cockpit-hero\">\n"
        "<p class=\"eyebrow\">Generated view only</p>\n"
        "<h1>Product-Agent OS First-Run Cockpit</h1>\n"
        f"<p>{_text(primary_cockpit['source_truth_policy'])}.</p>\n"
        "<div class=\"hero-grid\">\n"
        f"<span>Primary artifact <strong>{_text(contract['primary_artifact'])}</strong></span>\n"
        f"<span>Graph renderer <strong>{_text(contract['selected_graph_renderer'])}</strong></span>\n"
        f"<span>Pages <strong>{_text(primary_cockpit['page_count'])}</strong></span>\n"
        f"<span>Completion claim <strong>{_text(primary_cockpit['overview']['completion_claim'])}</strong></span>\n"
        "</div>\n"
        "</header>\n"
        f"<nav class=\"cockpit-nav\" aria-label=\"First-run cockpit sections\">{nav}</nav>\n"
        f"{controls_html}\n"
        "<section class=\"cockpit-band\" aria-labelledby=\"status-cards\"><h2 id=\"status-cards\">Evidence Status</h2>"
        f"<div class=\"status-grid\">{status_cards}</div></section>\n"
        "<section class=\"cockpit-band\" aria-labelledby=\"unsupported-claims\"><h2 id=\"unsupported-claims\">Unsupported Claims</h2>"
        f"<ul class=\"claim-list\">{unsupported}</ul></section>\n"
        f"{pages_html}\n"
        f"{diagnostics_html}\n"
        "<section class=\"cockpit-band\" aria-labelledby=\"baseline-comparison\"><h2 id=\"baseline-comparison\">Baseline Comparison</h2>"
        f"{baseline_rows}</section>\n"
        "<section class=\"cockpit-band\" aria-labelledby=\"artifact-cleanup-rollback\"><h2 id=\"artifact-cleanup-rollback\">Artifact Cleanup And Rollback</h2>"
        f"<p>Cleanup is preview-only and requires explicit approval; no files are deleted by default.</p>{cleanup_rows}</section>\n"
        "</main>\n"
        "</body>\n"
        "</html>\n"
    )


def _cockpit_section_html(page: dict[str, Any], primary_cockpit: dict[str, Any]) -> str:
    page_id = str(page.get("id", ""))
    sections = page.get("sections") if isinstance(page.get("sections"), list) else []
    boundaries = page.get("approval_boundaries") if isinstance(page.get("approval_boundaries"), list) else []
    body = "\n".join(
        f"<article class=\"section-card\" id=\"section-{_attr(section.get('id'))}\">"
        f"<h3>{_text(section.get('label'))}</h3>"
        f"<p>{_text(section.get('source_boundary'))}</p>"
        "</article>"
        for section in sections
        if isinstance(section, dict)
    )
    extra = ""
    if page_id == "project-map":
        extra = _graph_panel_html(
            primary_cockpit["source_file_graph"],
            graph_id="source-file-graph",
            title="File / Source Graph",
            empty_message="No file/source graph rows are available.",
        )
    elif page_id == "code-intelligence":
        extra = _code_graph_panel_html(primary_cockpit["code_graph"])
    elif page_id == "quality-metrics":
        extra = _visual_qa_html(primary_cockpit["visual_qa"])
    elif page_id == "operations-risk":
        extra = _safety_accessibility_html(primary_cockpit["safety_accessibility"])
    return (
        f"<section class=\"cockpit-page\" id=\"page-{_attr(page_id)}\">\n"
        f"<h2>{_text(page.get('label'))}</h2>\n"
        f"<p class=\"page-role\">{_text(page.get('role'))}</p>\n"
        f"<p class=\"boundary\">{_text('; '.join(str(item) for item in boundaries[:2]))}</p>\n"
        f"{extra}<div class=\"section-grid\">{body}</div>\n"
        "</section>\n"
    )


def _code_graph_panel_html(code_graph: dict[str, Any]) -> str:
    status = str(code_graph.get("status", "not_available"))
    hotspots = "\n".join(
        "<tr>"
        f"<td><code>{_text(item.get('id'))}</code></td>"
        f"<td>{_text(item.get('status'))}</td>"
        f"<td>{_text(item.get('detail'))}</td>"
        "</tr>"
        for item in code_graph.get("hotspots", [])[:12]
        if isinstance(item, dict)
    )
    hotspot_table = (
        "<table class=\"compact-table graph-hotspots\"><thead><tr><th>Hotspot</th><th>Status</th><th>Detail</th></tr></thead>"
        f"<tbody>{hotspots}</tbody></table>"
        if hotspots
        else "<p class=\"empty-state\">No hotspots are available in the current first-run packet.</p>"
    )
    empty = ""
    if status == "not_available":
        empty = (
            "<p class=\"empty-state\"><strong>not_available</strong>: "
            f"{_text(code_graph.get('not_available_reason'))}</p>"
        )
    return (
        _graph_panel_html(
            code_graph,
            graph_id="code-graph",
            title="Code Graph And Hotspots",
            empty_message="Code graph data is not available for this packet.",
        )
        + empty
        + hotspot_table
    )


def _cockpit_controls_html(primary_cockpit: dict[str, Any]) -> str:
    model = primary_cockpit.get("navigation_search") if isinstance(primary_cockpit.get("navigation_search"), dict) else {}
    filters = model.get("filters") if isinstance(model.get("filters"), list) else []
    filter_controls = "\n".join(
        '<label class="filter-control" for="{id}">{label}<select id="{id}" name="{id}" data-filter-source="{source}" data-filter-field="{field}">'
        '<option value="">All</option><option value="current">current</option><option value="inspection_only">inspection_only</option>'
        '<option value="approval_required">approval_required</option><option value="not_available">not_available</option></select></label>'.format(
            id=_attr(item.get("id")),
            label=_text(item.get("label")),
            source=_attr(item.get("source")),
            field=_attr(item.get("field")),
        )
        for item in filters
        if isinstance(item, dict)
    )
    detail_panels = "\n".join(
        f"<li><a href=\"#{_attr(item.get('id'))}\">{_text(item.get('kind'))}: {_text(item.get('status'))}</a></li>"
        for item in model.get("detail_panels", [])[:8]
        if isinstance(item, dict)
    )
    return (
        '<form class="cockpit-controls" role="search" aria-label="Cockpit search and filters" '
        'data-filter-state="static-default-all-visible" action="#page-overview">'
        '<label class="search-control" for="cockpit-search">Search cockpit'
        '<input id="cockpit-search" name="q" type="search" autocomplete="off" placeholder="section, file, status, graph node"></label>'
        f"{filter_controls}"
        '<button type="submit">Apply static filters</button>'
        '<p class="control-note">Controls are offline and script-free; tables remain visible as fallback.</p>'
        f'<ul class="detail-panel-links" aria-label="Detail panels">{detail_panels}</ul>'
        "</form>"
    )


def _progressive_diagnostics_html(primary_cockpit: dict[str, Any]) -> str:
    diagnostics = primary_cockpit.get("progressive_diagnostics")
    if not isinstance(diagnostics, dict):
        return ""
    rows = "\n".join(
        "<tr>"
        f"<td><code>{_text(item.get('id'))}</code></td>"
        f"<td>{_text(item.get('status'))}</td>"
        f"<td>{_text(item.get('detail'))}</td>"
        "</tr>"
        for item in diagnostics.get("diagnostic_sections", [])[:12]
        if isinstance(item, dict)
    )
    return (
        '<section class="cockpit-band diagnostic-disclosure" id="cockpit-diagnostics" aria-labelledby="diagnostics-heading">'
        '<h2 id="diagnostics-heading">Progressive Diagnostics</h2>'
        '<p>Primary cockpit sections show summaries first; raw packet data stays behind collapsed diagnostics or packet references.</p>'
        '<details><summary>Raw Diagnostics Boundary</summary>'
        f"{_definition_rows([('Raw JSON policy', diagnostics.get('raw_json_policy')), ('Raw packet ref', diagnostics.get('raw_packet_ref')), ('Source read required', str(diagnostics.get('source_read_required', True)).lower())])}"
        '<table class="compact-table"><thead><tr><th>Diagnostic</th><th>Status</th><th>Detail</th></tr></thead>'
        f"<tbody>{rows}</tbody></table></details></section>"
    )


def _visual_qa_html(visual_qa: dict[str, Any]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td><code>{_text(item.get('id'))}</code></td>"
        f"<td>{_text(item.get('status'))}</td>"
        "</tr>"
        for item in visual_qa.get("checks", [])[:16]
        if isinstance(item, dict)
    )
    gaps = "".join(f"<li>{_text(item)}</li>" for item in visual_qa.get("accepted_static_gaps", [])[:8])
    return (
        '<div class="qa-contract" id="static-visual-qa" aria-label="Static visual QA contract">'
        '<h3>Static Visual QA</h3>'
        f"{_definition_rows([('Status', visual_qa.get('status')), ('Browser screenshots', visual_qa.get('browser_screenshot_status'))])}"
        '<table class="compact-table"><thead><tr><th>Check</th><th>Status</th></tr></thead>'
        f"<tbody>{rows}</tbody></table><ul class=\"claim-list\">{gaps}</ul></div>"
    )


def _safety_accessibility_html(safety: dict[str, Any]) -> str:
    offline = safety.get("offline_policy") if isinstance(safety.get("offline_policy"), dict) else {}
    privacy = safety.get("privacy_policy") if isinstance(safety.get("privacy_policy"), dict) else {}
    accessibility = safety.get("accessibility_contract") if isinstance(safety.get("accessibility_contract"), dict) else {}
    readability = safety.get("readability_contract") if isinstance(safety.get("readability_contract"), dict) else {}
    return (
        '<div class="safety-contract" id="offline-privacy-accessibility" aria-label="Offline privacy and accessibility contract">'
        '<h3>Offline, Privacy And Accessibility</h3>'
        f"{_definition_rows([('Status', safety.get('status')), ('External URLs allowed', str(offline.get('external_urls_allowed', False)).lower()), ('Script tags allowed', str(offline.get('script_tags_allowed', False)).lower()), ('Raw source bodies allowed', str(privacy.get('raw_source_bodies_allowed', False)).lower()), ('Labels required', str(accessibility.get('labels_required', True)).lower()), ('Font family', readability.get('font_family')), ('Overflow wrap', readability.get('overflow_wrap'))])}"
        "</div>"
    )


def _graph_panel_html(graph: dict[str, Any], *, graph_id: str, title: str, empty_message: str) -> str:
    budget_rows = _definition_rows(
        [
            ("Status", graph.get("status")),
            ("Renderer", graph.get("renderer", "Cosmos.gl")),
            ("Renderer mode", graph.get("renderer_mode")),
            ("Runtime assets", graph.get("runtime_asset_status")),
            ("Graphology-compatible", str(graph.get("graphology_compatible_payload", True)).lower()),
            ("Nodes", graph.get("node_count", 0)),
            ("Edges", graph.get("edge_count", 0)),
            ("Visible nodes", graph.get("visible_node_count", 0)),
            ("Visible edges", graph.get("visible_edge_count", 0)),
            ("Omitted nodes", graph.get("omitted_node_count", 0)),
            ("Omitted edges", graph.get("omitted_edge_count", 0)),
            ("Fallback", "bounded table fallback"),
        ]
    )
    legend = "\n".join(
        "<li>"
        f"<span class=\"legend-swatch\" style=\"background:{_attr(item.get('color'))}\"></span>"
        f"{_text(item.get('label'))} ({_text(item.get('node_count'))})"
        "</li>"
        for item in graph.get("legend", [])[:12]
        if isinstance(item, dict)
    )
    selected = graph.get("selected_file_panel") if isinstance(graph.get("selected_file_panel"), dict) else {}
    selected_panel = _definition_rows(
        [
            ("Status", selected.get("status", "not_selected")),
            ("Node", selected.get("node_id", "")),
            ("Type", selected.get("type", "")),
            ("Path", selected.get("path", "")),
            ("Boundary", selected.get("source_boundary", "raw source bodies are excluded")),
        ]
    )
    table_fallback = _graph_table_html(graph)
    canvas = _graph_svg_html(graph, graph_id=graph_id, empty_message=empty_message)
    return (
        f"<div class=\"graph-surface\" data-graph-kind=\"{_attr(graph_id)}\" data-renderer=\"Cosmos.gl\" "
        f"data-adapter-status=\"{_attr(graph.get('runtime_asset_status'))}\">\n"
        f"<h3>{_text(title)}</h3>\n"
        "<p class=\"graph-boundary\">Cosmos.gl is the selected renderer; this offline file carries a Cosmos-ready payload "
        "and uses a static SVG/table fallback with no external assets.</p>\n"
        f"{budget_rows}\n"
        f"{canvas}\n"
        f"<div class=\"graph-side-panel\" id=\"{_attr(graph_id)}-selected-file-panel\"><h4>Selected File Panel</h4>{selected_panel}</div>\n"
        f"<ul class=\"graph-legend\" aria-label=\"Graph legend\">{legend}</ul>\n"
        f"{table_fallback}\n"
        "</div>\n"
    )


def _graph_svg_html(graph: dict[str, Any], *, graph_id: str, empty_message: str) -> str:
    payload = graph.get("cosmos_payload") if isinstance(graph.get("cosmos_payload"), dict) else {}
    nodes = payload.get("nodes") if isinstance(payload.get("nodes"), list) else []
    links = payload.get("links") if isinstance(payload.get("links"), list) else []
    if not nodes:
        return (
            f"<div id=\"{_attr(graph_id)}-canvas\" class=\"graph-canvas empty-graph\" role=\"img\" "
            f"aria-label=\"{_attr(graph_id)} empty state\" data-renderer=\"Cosmos.gl\">{_text(empty_message)}</div>"
        )
    by_index = {int(node.get("index", 0)): node for node in nodes if isinstance(node, dict)}
    edge_parts: list[str] = []
    for link in links[:300]:
        if not isinstance(link, dict):
            continue
        source = by_index.get(int(link.get("source", 0) or 0))
        target = by_index.get(int(link.get("target", 0) or 0))
        if not source or not target:
            continue
        edge_parts.append(
            f"<line class=\"graph-edge\" x1=\"{_attr(_num(source.get('x')))}\" y1=\"{_attr(_num(source.get('y')))}\" "
            f"x2=\"{_attr(_num(target.get('x')))}\" y2=\"{_attr(_num(target.get('y')))}\" "
            f"stroke=\"{_attr(link.get('color') or '#7d8793')}\" data-edge-type=\"{_attr(link.get('type'))}\" />"
        )
    node_parts: list[str] = []
    for node in nodes[:500]:
        if not isinstance(node, dict):
            continue
        label = str(node.get("label", ""))
        node_parts.append(
            f"<g class=\"graph-node\" data-node-id=\"{_attr(node.get('id'))}\" data-node-type=\"{_attr(node.get('type'))}\" "
            f"data-status=\"{_attr(node.get('status'))}\" data-cluster=\"{_attr(node.get('cluster'))}\">"
            f"<circle cx=\"{_attr(_num(node.get('x')))}\" cy=\"{_attr(_num(node.get('y')))}\" "
            f"r=\"{_attr(max(2.5, min(8.0, float(node.get('size') or 3))))}\" fill=\"{_attr(node.get('color') or '#2f6fb0')}\"></circle>"
            f"<text x=\"{_attr(_num(float(node.get('x') or 0) + 3))}\" y=\"{_attr(_num(float(node.get('y') or 0) - 3))}\">"
            f"{_text(label[:42])}</text></g>"
        )
    return (
        f"<svg id=\"{_attr(graph_id)}-canvas\" class=\"graph-canvas\" viewBox=\"-70 -70 140 140\" "
        f"role=\"img\" aria-label=\"{_attr(graph_id)} static Cosmos.gl fallback\" data-renderer=\"Cosmos.gl\">"
        + "".join(edge_parts)
        + "".join(node_parts)
        + "</svg>"
    )


def _graph_table_html(graph: dict[str, Any]) -> str:
    fallback = graph.get("table_fallback") if isinstance(graph.get("table_fallback"), dict) else {}
    rows = "\n".join(
        "<tr>"
        f"<td><code>{_text(item.get('id'))}</code></td>"
        f"<td>{_text(item.get('type'))}</td>"
        f"<td>{_text(item.get('status'))}</td>"
        f"<td>{_text(item.get('cluster'))}</td>"
        f"<td>{_text(item.get('path'))}</td>"
        "</tr>"
        for item in fallback.get("rows", [])[:80]
        if isinstance(item, dict)
    )
    return (
        "<table class=\"graph-fallback-table\" aria-label=\"Bounded graph table fallback\">"
        "<thead><tr><th>Node</th><th>Type</th><th>Status</th><th>Cluster</th><th>Path</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _definition_rows(rows: list[tuple[str, Any]]) -> str:
    body = "\n".join(
        f"<tr><th scope=\"row\">{_text(label)}</th><td>{_text(value)}</td></tr>"
        for label, value in rows
    )
    return f"<table class=\"compact-table\"><tbody>{body}</tbody></table>"


def _cockpit_css() -> str:
    return """
:root{color-scheme:light;--ink:#151515;--muted:#5f6368;--line:#d7d9dd;--paper:#f7f8f5;--panel:#ffffff;--accent:#1f7a5a;--warn:#a05a00}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Arial,Helvetica,sans-serif}.skip-link{position:absolute;left:12px;top:-48px;background:var(--ink);color:#fff;padding:8px 10px;border-radius:4px;z-index:5}.skip-link:focus{top:12px}.cockpit-shell{max-width:1180px;margin:0 auto;padding:24px}.cockpit-hero{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:24px}.eyebrow{margin:0 0 8px;color:var(--accent);font-weight:700;text-transform:uppercase;font-size:12px}h1{font-size:34px;line-height:1.12;margin:0 0 12px}h2{font-size:21px;margin:0 0 12px}h3{font-size:15px;margin:0 0 8px}h4{font-size:14px;margin:0 0 8px}.hero-grid,.status-grid,.section-grid{display:grid;gap:10px}.hero-grid{grid-template-columns:repeat(4,minmax(0,1fr));margin-top:18px}.hero-grid span,.status-card,.section-card,.cockpit-band,.cockpit-page,.cockpit-controls{background:var(--panel);border:1px solid var(--line);border-radius:8px}.hero-grid span{padding:12px}.cockpit-nav{position:sticky;top:0;z-index:2;display:flex;gap:8px;overflow:auto;padding:12px 0;background:var(--paper)}.cockpit-nav a{white-space:nowrap;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:8px 10px}.cockpit-controls{display:grid;grid-template-columns:2fr repeat(4,minmax(120px,1fr));gap:10px;align-items:end;margin-top:10px;padding:12px}.cockpit-controls label{display:grid;gap:4px;font-size:13px;font-weight:700}.cockpit-controls input,.cockpit-controls select,.cockpit-controls button{min-height:38px;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);padding:7px}.control-note,.detail-panel-links{grid-column:1/-1;color:var(--muted);margin:0}.detail-panel-links{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none}.detail-panel-links a{color:var(--ink)}.cockpit-band,.cockpit-page{margin-top:14px;padding:18px}.status-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.status-card,.section-card{padding:14px}.section-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.page-role,.boundary,.status-card p,.section-card p,.graph-boundary,.empty-state{color:var(--muted);margin:0 0 6px}.claim-list{margin:0;padding-left:20px}.diagnostic-disclosure details{border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:12px}.diagnostic-disclosure summary{cursor:pointer;font-weight:700}.compact-table,.graph-fallback-table{width:100%;border-collapse:collapse;margin:10px 0}.compact-table th,.compact-table td,.graph-fallback-table th,.graph-fallback-table td{border-top:1px solid var(--line);padding:9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}.compact-table th{width:210px;color:var(--muted);font-weight:600}.graph-surface,.qa-contract,.safety-contract{margin:12px 0;padding:14px;border:1px solid var(--line);border-radius:8px;background:#fbfbf8}.graph-canvas{display:block;width:100%;min-height:320px;margin:12px 0;border:1px solid var(--line);border-radius:8px;background:#fdfdfb}.empty-graph{display:flex;align-items:center;justify-content:center;padding:24px;color:var(--muted)}.graph-edge{stroke-width:1;opacity:.58}.graph-node text{font-size:3.5px;fill:#252525;paint-order:stroke;stroke:#fff;stroke-width:1.8px}.graph-side-panel{margin:10px 0;padding:12px;border:1px solid var(--line);border-radius:8px;background:var(--panel)}.graph-legend{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 12px;padding:0;list-style:none}.graph-legend li{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;background:var(--panel);padding:5px 8px}.legend-swatch{width:10px;height:10px;border-radius:50%;display:inline-block}.graph-hotspots th:first-child,.graph-fallback-table th:first-child{width:230px}@media(max-width:760px){.cockpit-shell{padding:14px}.hero-grid,.status-grid,.section-grid,.cockpit-controls{grid-template-columns:1fr}h1{font-size:26px}.cockpit-nav{position:static}.compact-table th{width:auto}.graph-canvas{min-height:240px}.graph-legend{display:block}.graph-legend li{margin:6px 0}}
""".strip()


def _attr(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _text(value: Any) -> str:
    return html.escape(str(value or ""))


def _num(value: Any) -> str:
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return "0.000"


def _s4_page_summary_html(page_id: str, packet: dict[str, Any]) -> str:
    blocks_by_page = {
        "overview": [
            ("Project Analysis", packet.get("project_analysis_summary", {})),
            ("Safe Next Action", {"safe_next_action": packet.get("safe_next_action", "")}),
        ],
        "inventory": [
            ("Project Analysis", packet.get("project_analysis_summary", {})),
            ("Docs And Logging", packet.get("docs_logging_summary", {})),
            ("Dependency Readiness", packet.get("dependency_readiness_summary", {})),
        ],
        "methodology": [("Methodology Audit", packet.get("methodology_audit_summary", {}))],
        "runtime-route": [("Runtime Browser Boundary", packet.get("runtime_browser_boundary", {}))],
        "graph": [("Graph Dry Run", packet.get("graph_dry_run_summary", {}))],
        "recommendations": [
            ("Safe Next Action", {"safe_next_action": packet.get("safe_next_action", "")}),
            ("Unsupported Claims", packet.get("evidence_status", {}).get("unsupported_claims", [])),
        ],
    }
    blocks = blocks_by_page.get(page_id, [])
    if not blocks:
        return ""
    return (
        "\n".join(
            "<section>"
            f"<h2>{html.escape(title)}</h2>"
            f"<pre>{html.escape(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))}</pre>"
            "</section>"
            for title, value in blocks
        )
        + "\n"
    )


def _baseline_html(previous_baseline: dict[str, Any], change_summary: dict[str, list[str]]) -> str:
    return (
        "<section aria-labelledby=\"baseline-comparison\">\n"
        "<h2 id=\"baseline-comparison\">Baseline Comparison</h2>\n"
        f"<p>Status: <code>{html.escape(str(previous_baseline.get('status', 'missing')))}</code></p>\n"
        f"<pre>{html.escape(json.dumps(change_summary, ensure_ascii=False, sort_keys=True, indent=2))}</pre>\n"
        "</section>\n"
    )


def _cleanup_html(cleanup_guidance: dict[str, Any]) -> str:
    return (
        "<section aria-labelledby=\"artifact-cleanup-rollback\">\n"
        "<h2 id=\"artifact-cleanup-rollback\">Artifact Cleanup And Rollback</h2>\n"
        "<p>Cleanup is preview-only and requires explicit approval; no files are deleted by default.</p>\n"
        f"<pre>{html.escape(json.dumps(cleanup_guidance, ensure_ascii=False, sort_keys=True, indent=2))}</pre>\n"
        "</section>\n"
    )


def _source_artifacts(packet: dict[str, Any]) -> list[dict[str, str]]:
    artifacts: list[dict[str, str]] = []
    for item in packet.get("source_artifacts", []):
        if not isinstance(item, dict):
            continue
        artifacts.append(
            {
                "artifact_id": str(item.get("artifact_id", "")),
                "path": str(item.get("path", "")),
                "digest": str(item.get("digest", "")),
            }
        )
    return artifacts


def _redaction_report(payloads: list[Any]) -> dict[str, Any]:
    blocked_categories = {
        "local_absolute_path": sum(_count_local_absolute_paths(payload) for payload in payloads),
        "raw_source_field": sum(_count_raw_source_fields(payload) for payload in payloads),
        "secret_like_value": sum(_count_secret_like_values(payload) for payload in payloads),
    }
    status = "passed_redacted" if all(count == 0 for count in blocked_categories.values()) else "blocked_redaction_leak"
    return {
        "schema_version": "first_run_redaction_report_v1",
        "status": status,
        "blocked_categories": blocked_categories,
        "accepted_false_positives": [],
        "policy": {
            "local_absolute_paths_allowed": False,
            "raw_source_fields_allowed": False,
            "secret_like_values_allowed": False,
        },
    }


def _source_policy_gate(packet: dict[str, Any]) -> dict[str, Any]:
    source_policy = packet.get("section_summaries", {}).get("source_policy", {})
    status = source_policy.get("status", "not_available") if isinstance(source_policy, dict) else "not_available"
    apply_allowed = status == "current"
    return {
        "status": str(status),
        "apply_allowed": apply_allowed,
        "promotion_allowed": False,
        "diagnostic_artifact_allowed": True,
    }


def _graph_depth_summary(packet: dict[str, Any]) -> dict[str, Any]:
    summary = packet.get("graph_depth_summary")
    if not isinstance(summary, dict):
        summary = packet.get("graph_artifact_summary")
    return summary if isinstance(summary, dict) else {}


def _graph_depth_html(packet: dict[str, Any]) -> str:
    summary = _graph_depth_summary(packet)
    if not summary:
        return ""
    coverage = summary.get("coverage") if isinstance(summary.get("coverage"), dict) else {}
    freshness = summary.get("freshness") if isinstance(summary.get("freshness"), dict) else {}
    rejected = summary.get("rejected_link_summary") if isinstance(summary.get("rejected_link_summary"), dict) else {}
    framework = (
        summary.get("framework_semantic_summary")
        if isinstance(summary.get("framework_semantic_summary"), dict)
        else {}
    )
    unsupported_languages = coverage.get("unsupported_languages") if isinstance(coverage.get("unsupported_languages"), dict) else {}
    rejected_reasons = rejected.get("by_reason") if isinstance(rejected.get("by_reason"), dict) else {}
    frameworks = framework.get("frameworks") if isinstance(framework.get("frameworks"), dict) else {}
    tour = summary.get("guided_tour") if isinstance(summary.get("guided_tour"), list) else []
    tour_items = "\n".join(
        "<li>"
        f"<code>{html.escape(str(item.get('page', '')))}</code>: "
        f"{html.escape(str(item.get('safe_next_action', '')))}"
        "</li>"
        for item in tour
        if isinstance(item, dict)
    )
    return (
        "<section aria-labelledby=\"graph-packet-summary\">\n"
        "<h2 id=\"graph-packet-summary\">Graph Packet Summary</h2>\n"
        "<p><strong>Boundary</strong>: graph packets are orientation evidence only; read source files before edits or completion claims.</p>\n"
        "<h3>Coverage</h3>\n"
        "<dl>"
        f"<dt>Status</dt><dd>{html.escape(str(coverage.get('status', 'not_available')))}</dd>"
        f"<dt>Covered files</dt><dd>{html.escape(str(coverage.get('covered_files', 0)))}</dd>"
        f"<dt>Partial files</dt><dd>{html.escape(str(coverage.get('partial_files', 0)))}</dd>"
        f"<dt>Unsupported languages</dt><dd>{html.escape(json.dumps(unsupported_languages, sort_keys=True))}</dd>"
        "</dl>\n"
        "<h3>Freshness</h3>\n"
        "<dl>"
        f"<dt>Status</dt><dd>{html.escape(str(freshness.get('status', 'not_available')))}</dd>"
        f"<dt>Blocks action claims</dt><dd>{html.escape(str(bool(freshness.get('blocks_action_claims'))).lower())}</dd>"
        f"<dt>Safe next action</dt><dd>{html.escape(str(freshness.get('safe_next_action', 'Read source files before graph-backed actions.')))}</dd>"
        "</dl>\n"
        "<h3>Rejected Links</h3>\n"
        "<dl>"
        f"<dt>Total</dt><dd>{html.escape(str(rejected.get('total', 0)))}</dd>"
        f"<dt>Reasons</dt><dd>{html.escape(json.dumps(rejected_reasons, sort_keys=True))}</dd>"
        "</dl>\n"
        "<h3>Framework Hints</h3>\n"
        "<dl>"
        f"<dt>Total</dt><dd>{html.escape(str(framework.get('total', 0)))}</dd>"
        f"<dt>Frameworks</dt><dd>{html.escape(json.dumps(frameworks, sort_keys=True))}</dd>"
        "</dl>\n"
        "<h3>Guided Tour</h3>\n"
        f"<ul>{tour_items}</ul>\n"
        "</section>\n"
    )


def _cleanup_guidance(page_ids: list[str]) -> dict[str, Any]:
    generated_files = [ANALYSIS_MANIFEST_NAME]
    generated_files.extend("index.html" if page_id == "overview" else f"{page_id}.html" for page_id in page_ids)
    return {
        "schema_version": "first_run_artifact_cleanup_guidance_v1",
        "status": "preview_only",
        "deletion_performed": False,
        "approval_required": True,
        "generated_files": generated_files,
        "cleanup_command_preview": "Remove only the generated files listed in this manifest after explicit approval.",
        "rollback_policy": "Re-run first-run analysis to regenerate generated orientation artifacts.",
        "forbidden_scope": ["user_authored_files", "source_docs", "project_config", "git_metadata"],
    }


def _count_local_absolute_paths(payload: Any) -> int:
    if isinstance(payload, str):
        text = payload.replace("\\", "/").strip()
        if len(text) >= 3 and text[1] == ":" and text[2] == "/" and text[0].isalpha():
            return 1
        if text.startswith(("/", "//")):
            return 1
        return 0
    if isinstance(payload, dict):
        return sum(_count_local_absolute_paths(key) + _count_local_absolute_paths(value) for key, value in payload.items())
    if isinstance(payload, list):
        return sum(_count_local_absolute_paths(item) for item in payload)
    return 0


def _count_raw_source_fields(payload: Any) -> int:
    if isinstance(payload, dict):
        count = 0
        for key, value in payload.items():
            if str(key) in {"raw_source", "raw_body", "raw_file_body"}:
                count += 1
            count += _count_raw_source_fields(value)
        return count
    if isinstance(payload, list):
        return sum(_count_raw_source_fields(item) for item in payload)
    return 0


def _count_secret_like_values(payload: Any) -> int:
    if isinstance(payload, str):
        return len(SECRET_LIKE_VALUE_RE.findall(payload))
    if isinstance(payload, dict):
        return sum(_count_secret_like_values(key) + _count_secret_like_values(value) for key, value in payload.items())
    if isinstance(payload, list):
        return sum(_count_secret_like_values(item) for item in payload)
    return 0


def _load_previous_manifest(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {
            "manifest_digest": "unreadable",
            "page_digests": {},
            "source_digests": {},
        }
    return payload if isinstance(payload, dict) else None


def _target_fingerprint(packet: dict[str, Any], source_digests: dict[str, str]) -> str:
    return content_digest(
        canonical_json(
            {
                "target": packet.get("target", {}),
                "source_digests": source_digests,
            }
        )
    )


def _previous_baseline(previous_manifest: dict[str, Any] | None) -> dict[str, Any]:
    if previous_manifest is None:
        return {
            "status": "missing",
            "manifest_digest": "not_available",
        }
    return {
        "status": "compared",
        "manifest_digest": str(previous_manifest.get("manifest_digest", "not_available")),
    }


def _change_summary(
    previous_manifest: dict[str, Any] | None,
    page_digests: dict[str, str],
    source_digests: dict[str, str],
) -> dict[str, list[str]]:
    previous_pages = _previous_page_digests(previous_manifest)
    previous_sources = _previous_source_digests(previous_manifest)
    return {
        "added_pages": _added_keys(previous_pages, page_digests),
        "removed_pages": _removed_keys(previous_pages, page_digests),
        "changed_pages": _changed_keys(previous_pages, page_digests),
        "added_sources": _added_keys(previous_sources, source_digests),
        "removed_sources": _removed_keys(previous_sources, source_digests),
        "changed_sources": _changed_keys(previous_sources, source_digests),
    }


def _previous_page_digests(previous_manifest: dict[str, Any] | None) -> dict[str, str]:
    if not previous_manifest:
        return {}
    explicit = previous_manifest.get("page_digests")
    if isinstance(explicit, dict):
        return {str(key): str(value) for key, value in explicit.items()}
    pages = previous_manifest.get("pages")
    if not isinstance(pages, list):
        return {}
    return {
        str(page.get("page_id", "")): str(page.get("digest", ""))
        for page in pages
        if isinstance(page, dict) and page.get("page_id") and page.get("digest")
    }


def _previous_source_digests(previous_manifest: dict[str, Any] | None) -> dict[str, str]:
    if not previous_manifest:
        return {}
    explicit = previous_manifest.get("source_digests")
    if isinstance(explicit, dict):
        return {str(key): str(value) for key, value in explicit.items()}
    sources = previous_manifest.get("source_artifacts")
    if not isinstance(sources, list):
        return {}
    return {
        str(source.get("artifact_id", "")): str(source.get("digest", ""))
        for source in sources
        if isinstance(source, dict) and source.get("artifact_id") and source.get("digest")
    }


def _added_keys(previous: dict[str, str], current: dict[str, str]) -> list[str]:
    return sorted(set(current) - set(previous))


def _removed_keys(previous: dict[str, str], current: dict[str, str]) -> list[str]:
    return sorted(set(previous) - set(current))


def _changed_keys(previous: dict[str, str], current: dict[str, str]) -> list[str]:
    return sorted(key for key in set(previous) & set(current) if previous[key] != current[key])


__all__ = [
    "ANALYSIS_RENDERER_VERSION",
    "FIRST_RUN_ANALYSIS_PAGE_IDS",
    "render_first_run_analysis_artifact",
]
