from __future__ import annotations

import json
import re
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION = "first_run_analysis_packet_v1"
FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION = "first_run_orchestrator_contract_v1"
FIRST_RUN_ANALYSIS_ARTIFACT_VERSION = 1
GENERATED_VIEW_POLICY = "orientation_only_not_proof"
WRITE_POLICY = "read_only_generated_analysis_only"
REQUIRED_SECTION_IDS = {
    "discovery",
    "runtime_route",
    "methodology_audit",
    "control_plane",
    "source_policy",
    "graph",
    "status_snapshot",
}
EVIDENCE_STATUSES = {
    "current",
    "stale",
    "inspection_only",
    "present_unverified",
    "approval_required",
    "not_available",
}
CONFIDENCE_LEVELS = {"high", "medium", "low", "unknown"}
ANALYSIS_DIR = ".codex/product-agent-os/analysis"
FIRST_RUN_PACKET_NAME = "first-run-analysis-packet.json"
SECRET_LIKE_VALUE_RE = re.compile(r"\b(?:sk-proj|sk)-[A-Za-z0-9_-]{12,}")


FIRST_RUN_UNSUPPORTED_CLAIMS = [
    "release readiness",
    "runtime/browser proof",
    "provider/API/model quality",
    "target apply safety",
    "public docs/site acceptance",
    "active automation promotion",
    "source-read semantic completeness",
    "external writes or deployment safety",
]


FIRST_RUN_ANALYSIS_PACKET_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "First Run Analysis Packet",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "artifact_version",
        "generated_at",
        "target",
        "write_policy",
        "source_artifacts",
        "generated_pages",
        "section_summaries",
        "redaction_status",
        "evidence_status",
        "generated_view_policy",
        "safe_next_action",
        "packet_digest",
    ],
    "properties": {
        "schema_version": {"const": FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION},
        "artifact_version": {"const": FIRST_RUN_ANALYSIS_ARTIFACT_VERSION},
        "generated_at": {"type": "string"},
        "target": {
            "type": "object",
            "required": ["label", "mutation_allowed", "target_ref"],
        },
        "write_policy": {"const": WRITE_POLICY},
        "source_artifacts": {"type": "array"},
        "generated_pages": {"type": "array"},
        "section_summaries": {"type": "object"},
        "redaction_status": {"type": "object"},
        "evidence_status": {"type": "object"},
        "generated_view_policy": {"const": GENERATED_VIEW_POLICY},
        "graph_depth_summary": {"type": "object"},
        "graph_artifact_summary": {"type": "object"},
        "safe_next_action": {"type": "string"},
        "packet_digest": {"type": "string"},
    },
}


def build_first_run_automation_contract() -> dict[str, Any]:
    """Build the Batch 41 first-run orchestration contract."""

    return {
        "schema_version": FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION,
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "default_mode": "read_only",
        "modes": [
            {
                "id": "read_only",
                "cli_flags": ["--full-dry-run", "--dry-run"],
                "target_mutation_allowed": False,
                "allowed_write_roots": [],
                "description": "Build and print a first-run packet without writing target files.",
            },
            {
                "id": "stage",
                "cli_flags": ["--stage <dir>"],
                "target_mutation_allowed": False,
                "allowed_write_roots": ["explicit external stage root"],
                "description": "Write packet and offline HTML artifacts under an explicit stage root outside the target.",
            },
            {
                "id": "write_analysis",
                "cli_flags": ["--write-analysis"],
                "target_mutation_allowed": True,
                "allowed_write_roots": [ANALYSIS_DIR],
                "description": "Write generated analysis artifacts only under the target analysis directory.",
            },
            {
                "id": "render_html",
                "cli_flags": ["--stage <dir>", "--write-analysis"],
                "target_mutation_allowed": False,
                "allowed_write_roots": ["stage root", ANALYSIS_DIR],
                "description": "Render offline HTML as generated orientation evidence only.",
            },
            {
                "id": "ask",
                "cli_flags": [],
                "target_mutation_allowed": False,
                "allowed_write_roots": [],
                "description": "Expose at most one blocking owner question in the first-launch response.",
            },
            {
                "id": "compare",
                "cli_flags": ["--stage <dir>", "--write-analysis"],
                "target_mutation_allowed": False,
                "allowed_write_roots": ["stage root", ANALYSIS_DIR],
                "description": "Compare against previous generated manifest when one exists.",
            },
        ],
        "inputs": ["workspace", "generated_at", "stage_dir"],
        "outputs": [
            FIRST_RUN_PACKET_NAME,
            "index.html",
            "analysis-manifest.json",
            "first-launch summary",
        ],
        "write_boundaries": {
            "target_default": "read_only",
            "stage_inside_target": "blocked_without_write_analysis_mode",
            "write_analysis_root": ANALYSIS_DIR,
            "external_actions": "not_performed",
        },
        "unsupported_claims": FIRST_RUN_UNSUPPORTED_CLAIMS,
        "stop_conditions": [
            "silent target mutation",
            "stage path is inside target without write-analysis mode",
            "help suggests unsafe writes or live actions",
            "generated view is treated as source truth",
            "runtime/browser/provider/git/release claim without current evidence",
        ],
    }


def validate_first_run_automation_contract(contract: Any) -> list[str]:
    if not isinstance(contract, dict):
        return ["first-run automation contract must be an object"]
    errors: list[str] = []
    if contract.get("schema_version") != FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION}")
    if contract.get("generated_view_policy") != GENERATED_VIEW_POLICY:
        errors.append(f"generated_view_policy must be {GENERATED_VIEW_POLICY}")
    modes = contract.get("modes")
    if not isinstance(modes, list):
        errors.append("modes must be list")
        modes = []
    mode_ids = {str(mode.get("id", "")) for mode in modes if isinstance(mode, dict)}
    for mode_id in {"read_only", "stage", "write_analysis", "render_html", "ask", "compare"}:
        if mode_id not in mode_ids:
            errors.append(f"mode {mode_id} is required")
    for mode in modes:
        if not isinstance(mode, dict):
            errors.append("mode entry must be an object")
            continue
        if not isinstance(mode.get("target_mutation_allowed"), bool):
            errors.append(f"mode {mode.get('id', '')}.target_mutation_allowed must be boolean")
        if not isinstance(mode.get("allowed_write_roots"), list):
            errors.append(f"mode {mode.get('id', '')}.allowed_write_roots must be list")
    if not isinstance(contract.get("unsupported_claims"), list):
        errors.append("unsupported_claims must be list")
    else:
        for claim in FIRST_RUN_UNSUPPORTED_CLAIMS:
            if claim not in contract["unsupported_claims"]:
                errors.append(f"unsupported claim missing: {claim}")
    write_boundaries = contract.get("write_boundaries")
    if not isinstance(write_boundaries, dict):
        errors.append("write_boundaries must be object")
    elif write_boundaries.get("stage_inside_target") != "blocked_without_write_analysis_mode":
        errors.append("stage_inside_target boundary must block without write-analysis mode")
    return errors


def build_first_run_analysis_packet(
    *,
    target_label: str,
    generated_at: str,
    source_artifacts: list[dict[str, Any]],
    generated_pages: list[dict[str, Any]],
    section_summaries: dict[str, dict[str, Any]],
    safe_next_action: str,
    graph_artifact_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the source packet for first-run project analysis."""

    artifact_entries = [_source_artifact_entry(item) for item in source_artifacts]
    page_entries = [_generated_page_entry(item) for item in generated_pages]
    section_entries = {
        section_id: _section_summary_entry(section_summaries.get(section_id, {}))
        for section_id in sorted(REQUIRED_SECTION_IDS)
    }
    graph_summary = _graph_artifact_summary_entry(graph_artifact_summary)
    packet = {
        "schema_version": FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION,
        "artifact_version": FIRST_RUN_ANALYSIS_ARTIFACT_VERSION,
        "generated_at": generated_at,
        "target": {
            "label": str(target_label).strip(),
            "target_ref": _safe_relative_ref(str(target_label).strip()),
            "mutation_allowed": False,
        },
        "write_policy": WRITE_POLICY,
        "source_artifacts": artifact_entries,
        "generated_pages": page_entries,
        "section_summaries": section_entries,
        "redaction_status": {
            "status": "passed_redacted",
            "local_absolute_paths_allowed": False,
            "raw_file_bodies_allowed": False,
            "raw_private_logs_allowed": False,
            "secrets_allowed": False,
        },
        "evidence_status": _evidence_status(artifact_entries, page_entries, section_entries),
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "graph_depth_summary": graph_summary,
        "graph_artifact_summary": graph_summary,
        "safe_next_action": str(safe_next_action).strip(),
    }
    packet["packet_digest"] = content_digest(canonical_json(packet))
    return packet


def validate_first_run_analysis_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["first-run analysis packet must be an object"]

    errors: list[str] = []
    for field in FIRST_RUN_ANALYSIS_PACKET_SCHEMA["required"]:
        if field not in packet:
            errors.append(f"{field} is required")
    if packet.get("schema_version") != FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION}")
    if packet.get("artifact_version") != FIRST_RUN_ANALYSIS_ARTIFACT_VERSION:
        errors.append(f"artifact_version must be {FIRST_RUN_ANALYSIS_ARTIFACT_VERSION}")
    if packet.get("write_policy") != WRITE_POLICY:
        errors.append(f"write_policy must be {WRITE_POLICY}")
    if packet.get("generated_view_policy") != GENERATED_VIEW_POLICY:
        errors.append(f"generated_view_policy must be {GENERATED_VIEW_POLICY}")
    errors.extend(_validate_target(packet.get("target")))
    errors.extend(_validate_source_artifacts(packet.get("source_artifacts")))
    errors.extend(_validate_generated_pages(packet.get("generated_pages")))
    errors.extend(_validate_section_summaries(packet.get("section_summaries")))
    errors.extend(_validate_redaction_status(packet.get("redaction_status")))
    errors.extend(_validate_evidence_status(packet.get("evidence_status")))
    errors.extend(_validate_graph_artifact_summary(packet.get("graph_depth_summary"), field_name="graph_depth_summary"))
    errors.extend(_validate_graph_artifact_summary(packet.get("graph_artifact_summary")))
    if not isinstance(packet.get("safe_next_action"), str) or not packet.get("safe_next_action", "").strip():
        errors.append("safe_next_action must be a non-empty string")
    if not _valid_sha256_digest(str(packet.get("packet_digest", ""))):
        errors.append("packet_digest must be a sha256 digest")
    if _contains_local_absolute_path(packet):
        errors.append("local absolute path leaked")
    if _contains_raw_source_field(packet):
        errors.append("raw source field retained")
    if _contains_secret_like_value(packet):
        errors.append("secret-like value retained")
    return errors


def run_first_project_analysis(
    workspace: str | Path,
    *,
    generated_at: str,
    write: bool = False,
) -> dict[str, Any]:
    """Run the first project analysis packet composition without live/runtime actions."""

    workspace_path = Path(workspace)
    if not workspace_path.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace_path}")
    if not workspace_path.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace_path}")

    inventory = _workspace_inventory(workspace_path)
    sections = adapt_first_run_analysis_sections(
        {
            "discovery": {
                "source_module": "run_first_project_analysis",
                "source_artifact": "workspace-inventory",
                "evidence_freshness": "inspection_only",
                "confidence": "medium",
            },
            "runtime_route": {
                "source_module": "not_run",
                "source_artifact": "not_available",
                "evidence_freshness": "approval_required",
                "confidence": "medium",
                "unsupported_claims": ["live runtime not run"],
            },
            "control_plane": {
                "source_module": "run_first_project_analysis",
                "source_artifact": "workspace-inventory",
                "evidence_freshness": "present_unverified",
                "confidence": "low",
            },
            "source_policy": {
                "source_module": "run_first_project_analysis",
                "source_artifact": "workspace-inventory",
                "evidence_freshness": "present_unverified",
                "confidence": "low",
            },
            "graph": {
                "source_module": "not_run",
                "source_artifact": "not_available",
                "evidence_freshness": "not_available",
                "confidence": "unknown",
                "unsupported_claims": ["graph not generated in M20.2"],
            },
        }
    )
    packet = build_first_run_analysis_packet(
        target_label=workspace_path.name,
        generated_at=generated_at,
        source_artifacts=[
            {
                "artifact_id": "workspace_inventory",
                "path": "workspace-inventory",
                "digest": content_digest(canonical_json(inventory)),
                "evidence_status": "inspection_only",
                "provenance": "run_first_project_analysis",
            }
        ],
        generated_pages=[],
        section_summaries=sections,
        safe_next_action="Review first-run packet; continue only with approved generated analysis artifacts.",
    )
    errors = validate_first_run_analysis_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))

    result: dict[str, Any] = {
        "status": "ok",
        "mode": "write" if write else "dry_run",
        "write_boundary": {
            "analysis_dir": ANALYSIS_DIR,
            "allowed_workspace_writes": [f"{ANALYSIS_DIR}/{FIRST_RUN_PACKET_NAME}"],
            "external_stage_required": False,
        },
        "packet": packet,
        "written_files": [],
    }
    if write:
        output_ref = f"{ANALYSIS_DIR}/{FIRST_RUN_PACKET_NAME}"
        output_path = _analysis_output_path(workspace_path, output_ref)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["written_files"] = [output_ref]
    return result


def adapt_first_run_analysis_sections(analyzer_outputs: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Normalize analyzer outputs into packet section summaries."""

    return {
        section_id: _adapter_section_entry(analyzer_outputs.get(section_id, {}))
        for section_id in sorted(REQUIRED_SECTION_IDS)
    }


def _source_artifact_entry(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": str(item.get("artifact_id", "")).strip(),
        "path": _safe_relative_ref(str(item.get("path", ""))),
        "digest": str(item.get("digest", "")).strip(),
        "evidence_status": _status_or_default(item.get("evidence_status")),
        "provenance": str(item.get("provenance", "")).strip(),
    }


def _workspace_inventory(workspace: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file() or _is_generated_analysis_path(workspace, path):
            continue
        relative = path.relative_to(workspace).as_posix()
        files.append(
            {
                "path": relative,
                "size": path.stat().st_size,
            }
        )
    return {
        "file_count": len(files),
        "files": files[:200],
        "truncated": len(files) > 200,
    }


def _is_generated_analysis_path(workspace: Path, path: Path) -> bool:
    try:
        relative = path.relative_to(workspace).as_posix()
    except ValueError:
        return False
    return relative.startswith(f"{ANALYSIS_DIR}/")


def _analysis_output_path(workspace: Path, output_ref: str) -> Path:
    output_path = (workspace / output_ref).resolve()
    analysis_root = (workspace / ANALYSIS_DIR).resolve()
    try:
        output_path.relative_to(analysis_root)
    except ValueError as exc:
        raise ValueError("analysis output path escapes generated analysis directory") from exc
    return output_path


def _generated_page_entry(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "page_id": str(item.get("page_id", "")).strip(),
        "path": _safe_relative_ref(str(item.get("path", ""))),
        "digest": str(item.get("digest", "")).strip(),
        "source_policy": str(item.get("source_policy", GENERATED_VIEW_POLICY)).strip() or GENERATED_VIEW_POLICY,
    }


def _graph_artifact_summary_entry(value: dict[str, Any] | None) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    rejected_link_summary = _bounded_reason_summary(source.get("rejected_link_summary"))
    framework_semantic_summary = _bounded_reason_summary(source.get("framework_semantic_summary"))
    return {
        "schema_version": "graph_depth_first_run_summary_v1",
        "status": _status_or_default(source.get("status")),
        "graph_packet_digest": str(source.get("graph_packet_digest", "")).strip(),
        "agent_packet_refs": _safe_refs(source.get("agent_packet_refs")),
        "coverage": _bounded_graph_coverage(source.get("coverage")),
        "freshness": _bounded_graph_freshness(source.get("freshness")),
        "rejected_link_summary": rejected_link_summary,
        "rejected_links": rejected_link_summary,
        "framework_semantic_summary": framework_semantic_summary,
        "framework_semantics": framework_semantic_summary,
        "guided_tour": _bounded_guided_tour(source.get("guided_tour")),
        "unsupported_claims": _safe_string_list(source.get("unsupported_claims")),
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "source_policy": "graph artifacts are generated orientation evidence, not source truth",
        "source_read_required": True,
        "must_read_source_before_edit": True,
        "completion_claim": "not_claimed",
        "decision_status": "manual_only",
        "promotion_decision": "not_promoted",
        "promotion_boundary": "manual_only_not_promoted",
    }


def _safe_refs(value: Any, limit: int = 4) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    if not isinstance(value, list):
        return refs
    for item in value[:limit]:
        if not isinstance(item, dict):
            continue
        path = _safe_relative_ref(str(item.get("path", "")))
        if not path or path == "[REDACTED_LOCAL_PATH]":
            continue
        refs.append(
            {
                "kind": str(item.get("kind", "staged_artifact")).strip() or "staged_artifact",
                "path": path,
                "digest": str(item.get("digest", "")).strip(),
            }
        )
    return refs


def _bounded_graph_coverage(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    unsupported = source.get("unsupported_languages") if isinstance(source.get("unsupported_languages"), dict) else {}
    return {
        "status": str(source.get("status", "not_available")).strip() or "not_available",
        "covered_files": _int(source.get("covered_files")),
        "partial_files": _int(source.get("partial_files")),
        "unsupported_languages": {
            str(key): str(item)
            for key, item in sorted(unsupported.items())[:8]
        },
    }


def _bounded_graph_freshness(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    return {
        "status": str(source.get("status", "not_available")).strip() or "not_available",
        "blocks_action_claims": bool(source.get("blocks_action_claims")),
        "safe_next_action": str(source.get("safe_next_action", "Read source files before graph-backed actions.")).strip(),
    }


def _bounded_reason_summary(value: Any) -> dict[str, Any]:
    source = value if isinstance(value, dict) else {}
    reasons = source.get("by_reason") if isinstance(source.get("by_reason"), dict) else {}
    frameworks = source.get("frameworks") if isinstance(source.get("frameworks"), dict) else {}
    result: dict[str, Any] = {"total": _int(source.get("total"))}
    if reasons:
        result["by_reason"] = {str(key): _int(item) for key, item in sorted(reasons.items())[:8]}
    if frameworks:
        result["frameworks"] = {str(key): _int(item) for key, item in sorted(frameworks.items())[:8]}
    return result


def _bounded_guided_tour(value: Any, limit: int = 8) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    items: list[dict[str, str]] = []
    for item in value[:limit]:
        if not isinstance(item, dict):
            continue
        items.append(
            {
                "page": str(item.get("page", "")).strip(),
                "safe_next_action": str(item.get("safe_next_action", "")).strip(),
            }
        )
    return items


def _section_summary_entry(item: dict[str, Any]) -> dict[str, Any]:
    status = _status_or_default(item.get("status"))
    unsupported_claims = item.get("unsupported_claims")
    accepted_gaps = item.get("accepted_gaps")
    return {
        "status": status,
        "source_module": str(item.get("source_module", "not_available")).strip() or "not_available",
        "source_artifact": _safe_relative_ref(str(item.get("source_artifact", "not_available"))),
        "evidence_freshness": _status_or_default(item.get("evidence_freshness") or status),
        "confidence": _confidence_or_default(item.get("confidence")),
        "unsupported_claims": [
            str(claim).strip()
            for claim in (unsupported_claims if isinstance(unsupported_claims, list) else [])
            if str(claim).strip()
        ],
        "accepted_gaps": [
            str(gap).strip()
            for gap in (accepted_gaps if isinstance(accepted_gaps, list) else [])
            if str(gap).strip()
        ],
    }


def _adapter_section_entry(item: dict[str, Any]) -> dict[str, Any]:
    status = _status_or_default(item.get("status") or item.get("evidence_freshness"))
    return _section_summary_entry(
        {
            "status": status,
            "source_module": item.get("source_module", "not_available"),
            "source_artifact": item.get("source_artifact", "not_available"),
            "evidence_freshness": item.get("evidence_freshness", status),
            "confidence": item.get("confidence", "unknown"),
            "unsupported_claims": item.get("unsupported_claims", []),
            "accepted_gaps": item.get("accepted_gaps", []),
        }
    )


def _evidence_status(
    source_artifacts: list[dict[str, Any]],
    generated_pages: list[dict[str, Any]],
    section_summaries: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    statuses = [str(item.get("evidence_status", "")) for item in source_artifacts]
    statuses.extend(str(item.get("status", "")) for item in section_summaries.values())
    known_statuses = [status for status in statuses if status]
    if not known_statuses:
        freshness = "missing"
    elif all(status == "current" for status in known_statuses):
        freshness = "current"
    elif "stale" in known_statuses:
        freshness = "stale"
    else:
        freshness = "mixed"
    return {
        "freshness": freshness,
        "source_artifact_count": len(source_artifacts),
        "generated_page_count": len(generated_pages),
        "completion_claim": "not_claimed",
        "unsupported_claim_count": sum(
            len(item.get("unsupported_claims", [])) for item in section_summaries.values()
        ),
    }


def _validate_target(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["target must be an object"]
    errors: list[str] = []
    if not isinstance(value.get("label"), str) or not value.get("label", "").strip():
        errors.append("target.label must be a non-empty string")
    if value.get("mutation_allowed") is not False:
        errors.append("target.mutation_allowed must be false")
    if not isinstance(value.get("target_ref"), str) or not value.get("target_ref", "").strip():
        errors.append("target.target_ref must be a non-empty string")
    return errors


def _validate_source_artifacts(value: Any) -> list[str]:
    if not isinstance(value, list):
        return ["source_artifacts must be list"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"source_artifacts[{index}] must be an object")
            continue
        for field in ("artifact_id", "path", "digest", "evidence_status", "provenance"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"source_artifacts[{index}].{field} must be a non-empty string")
        if "digest" in item and not _valid_sha256_digest(str(item.get("digest", ""))):
            errors.append(f"source_artifacts[{index}].digest must be a sha256 digest")
        if item.get("evidence_status") not in EVIDENCE_STATUSES:
            errors.append(f"source_artifacts[{index}].evidence_status missing or invalid")
        if not _safe_relative_path(str(item.get("path", ""))):
            errors.append(f"source_artifacts[{index}].path must be workspace-relative")
    return errors


def _validate_generated_pages(value: Any) -> list[str]:
    if not isinstance(value, list):
        return ["generated_pages must be list"]
    errors: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"generated_pages[{index}] must be an object")
            continue
        for field in ("page_id", "path", "digest", "source_policy"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"generated_pages[{index}].{field} must be a non-empty string")
        if "digest" in item and not _valid_sha256_digest(str(item.get("digest", ""))):
            errors.append(f"generated_pages[{index}].digest must be a sha256 digest")
        if not _safe_relative_path(str(item.get("path", ""))):
            errors.append(f"generated_pages[{index}].path must be workspace-relative")
    return errors


def _validate_section_summaries(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["section_summaries must be an object"]
    errors: list[str] = []
    missing = sorted(REQUIRED_SECTION_IDS - set(value))
    for section_id in missing:
        errors.append(f"section_summaries.{section_id} is required")
    for section_id, item in value.items():
        if not isinstance(item, dict):
            errors.append(f"section_summaries.{section_id} must be an object")
            continue
        if item.get("status") not in EVIDENCE_STATUSES:
            errors.append(f"section_summaries.{section_id}.status missing or invalid")
        if item.get("evidence_freshness") not in EVIDENCE_STATUSES:
            errors.append(f"section_summaries.{section_id}.evidence_freshness missing or invalid")
        if item.get("confidence") not in CONFIDENCE_LEVELS:
            errors.append(f"section_summaries.{section_id}.confidence missing or invalid")
        for field in ("source_module", "source_artifact"):
            if not isinstance(item.get(field), str) or not item.get(field, "").strip():
                errors.append(f"section_summaries.{section_id}.{field} must be a non-empty string")
        if not isinstance(item.get("unsupported_claims"), list):
            errors.append(f"section_summaries.{section_id}.unsupported_claims must be list")
        if not isinstance(item.get("accepted_gaps"), list):
            errors.append(f"section_summaries.{section_id}.accepted_gaps must be list")
    return errors


def _validate_redaction_status(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["redaction_status must be an object"]
    errors: list[str] = []
    if value.get("status") not in {"passed_redacted", "blocked_redaction_policy", "blocked_redaction_leak"}:
        errors.append("redaction_status.status missing or invalid")
    for field in (
        "local_absolute_paths_allowed",
        "raw_file_bodies_allowed",
        "raw_private_logs_allowed",
        "secrets_allowed",
    ):
        if value.get(field) is not False:
            errors.append(f"redaction_status.{field} must be false")
    return errors


def _validate_evidence_status(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["evidence_status must be an object"]
    errors: list[str] = []
    if value.get("freshness") not in {"current", "mixed", "stale", "missing"}:
        errors.append("evidence_status.freshness missing or invalid")
    for field in ("source_artifact_count", "generated_page_count", "unsupported_claim_count"):
        if not isinstance(value.get(field), int):
            errors.append(f"evidence_status.{field} must be integer")
    if value.get("completion_claim") != "not_claimed":
        errors.append("evidence_status.completion_claim must be not_claimed")
    return errors


def _validate_graph_artifact_summary(value: Any, *, field_name: str = "graph_artifact_summary") -> list[str]:
    if not isinstance(value, dict):
        return [f"{field_name} must be an object"]
    errors: list[str] = []
    if value.get("schema_version") != "graph_depth_first_run_summary_v1":
        errors.append(f"{field_name}.schema_version must be graph_depth_first_run_summary_v1")
    if value.get("status") not in EVIDENCE_STATUSES:
        errors.append(f"{field_name}.status missing or invalid")
    digest = str(value.get("graph_packet_digest", ""))
    if digest and not _valid_sha256_digest(digest):
        errors.append(f"{field_name}.graph_packet_digest must be a sha256 digest when present")
    if not isinstance(value.get("agent_packet_refs"), list):
        errors.append(f"{field_name}.agent_packet_refs must be list")
    if not isinstance(value.get("coverage"), dict):
        errors.append(f"{field_name}.coverage must be object")
    if not isinstance(value.get("freshness"), dict):
        errors.append(f"{field_name}.freshness must be object")
    if not isinstance(value.get("rejected_link_summary"), dict):
        errors.append(f"{field_name}.rejected_link_summary must be object")
    if not isinstance(value.get("framework_semantic_summary"), dict):
        errors.append(f"{field_name}.framework_semantic_summary must be object")
    if not isinstance(value.get("guided_tour"), list):
        errors.append(f"{field_name}.guided_tour must be list")
    if value.get("generated_view_policy") != GENERATED_VIEW_POLICY:
        errors.append(f"{field_name}.generated_view_policy must be {GENERATED_VIEW_POLICY}")
    if value.get("source_read_required") is not True:
        errors.append(f"{field_name}.source_read_required must be true")
    if value.get("must_read_source_before_edit") is not True:
        errors.append(f"{field_name}.must_read_source_before_edit must be true")
    if value.get("completion_claim") != "not_claimed":
        errors.append(f"{field_name}.completion_claim must be not_claimed")
    return errors


def _status_or_default(value: Any) -> str:
    status = str(value or "not_available").strip()
    return status if status in EVIDENCE_STATUSES else "not_available"


def _confidence_or_default(value: Any) -> str:
    confidence = str(value or "unknown").strip()
    return confidence if confidence in CONFIDENCE_LEVELS else "unknown"


def _safe_relative_ref(value: str) -> str:
    text = value.replace("\\", "/").strip()
    if not text:
        return ""
    if not _safe_relative_path(text):
        return "[REDACTED_LOCAL_PATH]"
    return text


def _safe_relative_path(path: str) -> bool:
    normalized = path.replace("\\", "/").strip()
    windows_path = PureWindowsPath(path)
    posix_path = Path(normalized)
    if not normalized:
        return False
    if normalized.startswith(("/", "//", "~")):
        return False
    if ":/" in normalized or windows_path.is_absolute() or windows_path.drive or windows_path.root:
        return False
    return ".." not in normalized.split("/") and ".." not in posix_path.parts


def _contains_local_absolute_path(payload: Any) -> bool:
    if isinstance(payload, str):
        text = payload.replace("\\", "/").strip()
        if len(text) >= 3 and text[1] == ":" and text[2] == "/" and text[0].isalpha():
            return True
        return text.startswith(("/", "//"))
    if isinstance(payload, dict):
        return any(_contains_local_absolute_path(key) or _contains_local_absolute_path(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(_contains_local_absolute_path(item) for item in payload)
    return False


def _contains_raw_source_field(payload: Any) -> bool:
    if isinstance(payload, dict):
        return any(
            str(key) in {"raw_source", "raw_body", "raw_file_body"}
            or _contains_raw_source_field(value)
            for key, value in payload.items()
        )
    if isinstance(payload, list):
        return any(_contains_raw_source_field(item) for item in payload)
    return False


def _contains_secret_like_value(payload: Any) -> bool:
    if isinstance(payload, str):
        return SECRET_LIKE_VALUE_RE.search(payload) is not None
    if isinstance(payload, dict):
        return any(_contains_secret_like_value(key) or _contains_secret_like_value(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(_contains_secret_like_value(item) for item in payload)
    return False


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _valid_sha256_digest(value: str) -> bool:
    if not value.startswith("sha256:"):
        return False
    digest = value.removeprefix("sha256:")
    return len(digest) == 64 and all(char in "0123456789abcdef" for char in digest)


__all__ = [
    "FIRST_RUN_ANALYSIS_PACKET_SCHEMA",
    "FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION",
    "FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION",
    "ANALYSIS_DIR",
    "FIRST_RUN_PACKET_NAME",
    "SECRET_LIKE_VALUE_RE",
    "adapt_first_run_analysis_sections",
    "build_first_run_analysis_packet",
    "build_first_run_automation_contract",
    "run_first_project_analysis",
    "validate_first_run_automation_contract",
    "validate_first_run_analysis_packet",
]
