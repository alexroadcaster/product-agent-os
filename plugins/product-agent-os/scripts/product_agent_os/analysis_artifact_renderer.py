from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from product_agent_os.first_run_analysis import ANALYSIS_DIR, SECRET_LIKE_VALUE_RE, validate_first_run_analysis_packet
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


def render_first_run_analysis_artifact(packet: dict[str, Any], workspace: str | Path) -> dict[str, Any]:
    """Render a first-run analysis packet into offline in-project HTML artifacts."""

    errors = validate_first_run_analysis_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))
    workspace_path = Path(workspace)
    if not workspace_path.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace_path}")
    if not workspace_path.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace_path}")

    analysis_dir = workspace_path / ANALYSIS_DIR
    previous_manifest = _load_previous_manifest(analysis_dir / ANALYSIS_MANIFEST_NAME)
    pages = [_page_entry(page_id, packet) for page_id in FIRST_RUN_ANALYSIS_PAGE_IDS]
    source_artifacts = _source_artifacts(packet)
    page_digests = {page["page_id"]: page["digest"] for page in pages}
    source_digests = {item["artifact_id"]: item["digest"] for item in source_artifacts}
    redaction_report = _redaction_report([packet, pages, source_artifacts, page_digests, source_digests])
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
        "previous_baseline": _previous_baseline(previous_manifest),
        "change_summary": _change_summary(previous_manifest, page_digests, source_digests),
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
        "analysis_dir": ANALYSIS_DIR,
        "manifest": ANALYSIS_MANIFEST_NAME,
        "page_count": len(pages),
        "written_files": [ANALYSIS_MANIFEST_NAME] + [page["path"] for page in pages],
        "generated_view_policy": "orientation_only_not_proof",
    }


def _page_entry(page_id: str, packet: dict[str, Any]) -> dict[str, Any]:
    path = "index.html" if page_id == "overview" else f"{page_id}.html"
    body = _page_html(page_id, packet)
    return {
        "page_id": page_id,
        "path": path,
        "digest": content_digest(body),
        "source_policy": "generated_view_only",
        "html": body,
    }


def _page_html(page_id: str, packet: dict[str, Any]) -> str:
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
        f"{graph_depth_html}"
        "</body>\n"
        "</html>\n"
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
