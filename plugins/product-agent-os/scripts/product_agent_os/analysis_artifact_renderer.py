from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from product_agent_os.first_run_analysis import ANALYSIS_DIR, SECRET_LIKE_VALUE_RE, validate_first_run_analysis_packet
from product_agent_os.project_cockpit_model import COCKPIT_PAGE_IDS, COCKPIT_PAGE_LABELS, build_project_cockpit_model
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
    graph_summary = _graph_depth_summary(packet)
    code_graph_status = str(graph_summary.get("status", "not_available") or "not_available")
    if code_graph_status in {"", "not_available"}:
        code_graph_status = "not_available"
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
        "source_file_graph": {
            "status": "adapter_ready",
            "graphology_compatible_payload": True,
            "node_count": len(graph_payload["nodes"]),
            "edge_count": len(graph_payload["edges"]),
            "source_artifact_count": len(source_artifacts),
            "section_count": len(packet.get("section_summaries", {})),
            "omitted_node_count": 0,
            "generated_view_policy": "orientation_only_not_proof",
        },
        "code_graph": {
            "status": code_graph_status,
            "empty_state": "not_available" if code_graph_status == "not_available" else "",
            "safe_next_action": "Read source files before graph-backed edits or completion claims.",
        },
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
    css = _cockpit_css()
    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<title>Product-Agent OS First-Run Cockpit</title>"
        f"<style>{css}</style></head>\n"
        "<body>\n"
        "<main class=\"first-run-cockpit cockpit-shell\" data-schema=\"first_run_cockpit_artifact_v1\">\n"
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
        "<section class=\"cockpit-band\" aria-labelledby=\"status-cards\"><h2 id=\"status-cards\">Evidence Status</h2>"
        f"<div class=\"status-grid\">{status_cards}</div></section>\n"
        "<section class=\"cockpit-band\" aria-labelledby=\"unsupported-claims\"><h2 id=\"unsupported-claims\">Unsupported Claims</h2>"
        f"<ul class=\"claim-list\">{unsupported}</ul></section>\n"
        f"{pages_html}\n"
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
        "<article class=\"section-card\">"
        f"<h3>{_text(section.get('label'))}</h3>"
        f"<p>{_text(section.get('source_boundary'))}</p>"
        "</article>"
        for section in sections
        if isinstance(section, dict)
    )
    extra = ""
    if page_id == "project-map":
        graph = primary_cockpit["source_file_graph"]
        extra = _definition_rows(
            [
                ("Status", graph.get("status")),
                ("Graphology-compatible", str(graph.get("graphology_compatible_payload")).lower()),
                ("Nodes", graph.get("node_count")),
                ("Edges", graph.get("edge_count")),
                ("Fallback", "bounded table fallback"),
            ]
        )
    elif page_id == "code-intelligence":
        code_graph = primary_cockpit["code_graph"]
        extra = _definition_rows(
            [
                ("Status", code_graph.get("status")),
                ("Empty state", code_graph.get("empty_state") or "available"),
                ("Safe next action", code_graph.get("safe_next_action")),
            ]
        )
    return (
        f"<section class=\"cockpit-page\" id=\"page-{_attr(page_id)}\">\n"
        f"<h2>{_text(page.get('label'))}</h2>\n"
        f"<p class=\"page-role\">{_text(page.get('role'))}</p>\n"
        f"<p class=\"boundary\">{_text('; '.join(str(item) for item in boundaries[:2]))}</p>\n"
        f"{extra}<div class=\"section-grid\">{body}</div>\n"
        "</section>\n"
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
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 Arial,Helvetica,sans-serif}.cockpit-shell{max-width:1180px;margin:0 auto;padding:24px}.cockpit-hero{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:24px}.eyebrow{margin:0 0 8px;color:var(--accent);font-weight:700;text-transform:uppercase;font-size:12px}h1{font-size:34px;line-height:1.12;margin:0 0 12px}h2{font-size:21px;margin:0 0 12px}h3{font-size:15px;margin:0 0 8px}.hero-grid,.status-grid,.section-grid{display:grid;gap:10px}.hero-grid{grid-template-columns:repeat(4,minmax(0,1fr));margin-top:18px}.hero-grid span,.status-card,.section-card,.cockpit-band,.cockpit-page{background:var(--panel);border:1px solid var(--line);border-radius:8px}.hero-grid span{padding:12px}.cockpit-nav{position:sticky;top:0;z-index:2;display:flex;gap:8px;overflow:auto;padding:12px 0;background:var(--paper)}.cockpit-nav a{white-space:nowrap;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:8px 10px}.cockpit-band,.cockpit-page{margin-top:14px;padding:18px}.status-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.status-card,.section-card{padding:14px}.section-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.page-role,.boundary,.status-card p,.section-card p{color:var(--muted);margin:0 0 6px}.claim-list{margin:0;padding-left:20px}.compact-table{width:100%;border-collapse:collapse;margin:10px 0}.compact-table th,.compact-table td{border-top:1px solid var(--line);padding:9px;text-align:left;vertical-align:top;overflow-wrap:anywhere}.compact-table th{width:210px;color:var(--muted);font-weight:600}@media(max-width:760px){.cockpit-shell{padding:14px}.hero-grid,.status-grid,.section-grid{grid-template-columns:1fr}h1{font-size:26px}.cockpit-nav{position:static}.compact-table th{width:auto}}
""".strip()


def _attr(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def _text(value: Any) -> str:
    return html.escape(str(value or ""))


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
