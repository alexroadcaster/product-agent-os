from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.discovery import analyze_workspace
from product_agent_os.methodology_audit import build_methodology_audit
from product_agent_os.project_code_graph import build_project_code_graph
from product_agent_os.question_ledger import build_answer_ledger, validate_answer_ledger
from product_agent_os.question_protocol import build_question_queue
from product_agent_os.source_policy import validate_source_policy
from product_agent_os.stage_manifest import canonical_json, content_digest


FIRST_RUN_ANALYSIS_PACKET_SCHEMA_VERSION = "first_run_analysis_packet_v1"
FIRST_RUN_ORCHESTRATOR_CONTRACT_SCHEMA_VERSION = "first_run_orchestrator_contract_v1"
FIRST_RUN_SCRIPT_REGISTRY_SCHEMA_VERSION = "first_run_script_registry_v1"
FIRST_RUN_COMMAND_MATRIX_SCHEMA_VERSION = "first_run_command_matrix_v1"
FIRST_RUN_EVIDENCE_SUMMARY_SCHEMA_VERSION = "first_run_evidence_summary_v1"
FIRST_RUN_RESUME_LEDGER_SCHEMA_VERSION = "first_run_resume_ledger_v1"
FIRST_RUN_GUIDED_RESPONSE_SCHEMA_VERSION = "first_run_guided_response_v1"
FIRST_RUN_ANSWER_LEDGER_ROUTING_SCHEMA_VERSION = "first_run_answer_ledger_routing_v1"
FIRST_RUN_ANALYSIS_ARTIFACT_VERSION = 1
GENERATED_VIEW_POLICY = "orientation_only_not_proof"
WRITE_POLICY = "read_only_generated_analysis_only"
ANSWER_LEDGER_TEMPLATE_NAME = "answer-ledger-template.json"
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
FIRST_RUN_ANALYSIS_ARTIFACT_PREFIX = f"{ANALYSIS_DIR}/"
FIRST_RUN_PACKET_NAME = "first-run-analysis-packet.json"
SECRET_LIKE_VALUE_RE = re.compile(r"\b(?:sk-proj|sk)-[A-Za-z0-9_-]{12,}")
DEFAULT_SCRIPT_HELP_TIMEOUT_SECONDS = 10


APPROVAL_REQUIRED_SCRIPTS = {
    "merge_infrastructure.py",
    "merge_markdown.py",
    "prepare_windows_codex_permissions.py",
}
BLOCKED_LIVE_SCRIPTS = {
    "run_codex_runtime_runner.py",
}


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
        "project_analysis_summary": {"type": "object"},
        "methodology_audit_summary": {"type": "object"},
        "source_policy_summary": {"type": "object"},
        "graph_dry_run_summary": {"type": "object"},
        "docs_logging_summary": {"type": "object"},
        "dependency_readiness_summary": {"type": "object"},
        "runtime_browser_boundary": {"type": "object"},
        "question_queue": {"type": "object"},
        "first_response": {"type": "object"},
        "answer_ledger_routing": {"type": "object"},
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
    project_analysis_summary: dict[str, Any] | None = None,
    methodology_audit_summary: dict[str, Any] | None = None,
    source_policy_summary: dict[str, Any] | None = None,
    graph_dry_run_summary: dict[str, Any] | None = None,
    docs_logging_summary: dict[str, Any] | None = None,
    dependency_readiness_summary: dict[str, Any] | None = None,
    runtime_browser_boundary: dict[str, Any] | None = None,
    question_queue: dict[str, Any] | None = None,
    first_response: dict[str, Any] | None = None,
    answer_ledger_routing: dict[str, Any] | None = None,
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
        "project_analysis_summary": project_analysis_summary or _empty_project_analysis_summary(),
        "methodology_audit_summary": methodology_audit_summary or _empty_methodology_audit_summary(),
        "source_policy_summary": source_policy_summary or _empty_source_policy_summary(),
        "graph_dry_run_summary": graph_dry_run_summary or _empty_graph_dry_run_summary(),
        "docs_logging_summary": docs_logging_summary or _empty_docs_logging_summary(),
        "dependency_readiness_summary": dependency_readiness_summary or _empty_dependency_readiness_summary(),
        "runtime_browser_boundary": runtime_browser_boundary or _empty_runtime_browser_boundary(),
        "question_queue": question_queue or build_question_queue(runtime_status="not_available"),
        "first_response": first_response or _empty_guided_first_response(safe_next_action),
        "answer_ledger_routing": answer_ledger_routing or _empty_answer_ledger_routing(generated_at),
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
    errors.extend(_validate_guided_first_response(packet.get("first_response")))
    errors.extend(_validate_answer_ledger_routing(packet.get("answer_ledger_routing")))
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
    s3 = build_first_run_project_analysis_summaries(workspace_path, inventory=inventory, generated_at=generated_at)
    sections = adapt_first_run_analysis_sections(
        {
            "discovery": {
                "source_module": "product_agent_os.discovery.analyze_workspace",
                "source_artifact": "project_analysis_summary",
                "evidence_freshness": "current",
                "confidence": s3["project_analysis_summary"]["usage_mode"]["confidence"],
            },
            "runtime_route": {
                "source_module": "first_run_runtime_browser_boundary",
                "source_artifact": "runtime_browser_boundary",
                "evidence_freshness": "approval_required",
                "confidence": "medium",
                "unsupported_claims": ["runtime/browser proof not run"],
            },
            "control_plane": {
                "source_module": "product_agent_os.discovery.analyze_workspace",
                "source_artifact": "project_analysis_summary",
                "evidence_freshness": "present_unverified",
                "confidence": "low",
            },
            "source_policy": {
                "source_module": "product_agent_os.source_policy.validate_source_policy",
                "source_artifact": "source_policy_summary",
                "evidence_freshness": s3["source_policy_summary"]["section_status"],
                "confidence": "medium",
                "unsupported_claims": s3["source_policy_summary"]["unsupported_claims"],
            },
            "graph": {
                "source_module": "product_agent_os.project_code_graph.build_project_code_graph",
                "source_artifact": "graph_dry_run_summary",
                "evidence_freshness": "inspection_only",
                "confidence": "medium",
                "unsupported_claims": ["generated graph is not source truth", "semantic completeness not claimed"],
            },
        }
    )
    packet = build_first_run_analysis_packet(
        target_label=workspace_path.name,
        generated_at=generated_at,
        source_artifacts=_first_run_source_artifacts(inventory),
        generated_pages=[],
        section_summaries=sections,
        safe_next_action=s3["safe_next_action"],
        project_analysis_summary=s3["project_analysis_summary"],
        methodology_audit_summary=s3["methodology_audit_summary"],
        source_policy_summary=s3["source_policy_summary"],
        graph_dry_run_summary=s3["graph_dry_run_summary"],
        docs_logging_summary=s3["docs_logging_summary"],
        dependency_readiness_summary=s3["dependency_readiness_summary"],
        runtime_browser_boundary=s3["runtime_browser_boundary"],
        question_queue=s3["question_queue"],
        first_response=s3["first_response"],
        answer_ledger_routing=s3["answer_ledger_routing"],
    )
    errors = validate_first_run_analysis_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))

    scripts_root = Path(__file__).resolve().parents[1]
    script_registry = build_first_run_script_registry(scripts_root)
    registry_errors = validate_first_run_script_registry(script_registry)
    if registry_errors:
        raise ValueError("; ".join(registry_errors))
    command_matrix = execute_first_run_safe_script_matrix(script_registry, generated_at=generated_at)
    evidence_summary = normalize_first_run_command_outputs(command_matrix)
    resume_ledger = build_first_run_resume_ledger(command_matrix)

    result: dict[str, Any] = {
        "status": "ok",
        "mode": "write" if write else "dry_run",
        "write_boundary": {
            "analysis_dir": ANALYSIS_DIR,
            "allowed_workspace_writes": [f"{ANALYSIS_DIR}/{FIRST_RUN_PACKET_NAME}"],
            "external_stage_required": False,
        },
        "packet": packet,
        "first_response": packet["first_response"],
        "answer_ledger_routing": _answer_ledger_routing_response(packet["answer_ledger_routing"]),
        "script_registry": script_registry,
        "command_matrix": command_matrix,
        "evidence_summary": evidence_summary,
        "resume_ledger": resume_ledger,
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


def build_first_run_project_analysis_summaries(
    workspace: str | Path,
    *,
    inventory: dict[str, Any] | None = None,
    generated_at: str = "",
) -> dict[str, Any]:
    """Build bounded read-only S3 first-run project analysis summaries."""

    workspace_path = Path(workspace)
    inventory = inventory if isinstance(inventory, dict) else _workspace_inventory(workspace_path)
    discovery = analyze_workspace(workspace_path)
    methodology = build_methodology_audit(
        workspace_path,
        intent_hint="",
        ignored_path_prefixes=(FIRST_RUN_ANALYSIS_ARTIFACT_PREFIX,),
    )
    source_policy = validate_source_policy(workspace_path)
    graph = build_project_code_graph(workspace_path)

    project_analysis_summary = _project_analysis_summary(discovery)
    methodology_summary = _methodology_audit_summary(methodology)
    source_policy_summary = _source_policy_summary(source_policy)
    graph_summary = _graph_dry_run_summary(graph)
    docs_logging_summary = _docs_logging_summary(inventory)
    dependency_summary = _dependency_readiness_summary(workspace_path, inventory)
    runtime_boundary = _runtime_browser_boundary(dependency_summary)
    safe_next_action = _s3_safe_next_action(source_policy_summary, runtime_boundary, methodology_summary)
    question_queue = _first_run_question_queue(
        methodology=methodology,
        source_policy_summary=source_policy_summary,
        runtime_boundary=runtime_boundary,
        project_analysis_summary=project_analysis_summary,
    )
    first_response = _guided_first_response(
        question_queue=question_queue,
        project_analysis_summary=project_analysis_summary,
        source_policy_summary=source_policy_summary,
        runtime_boundary=runtime_boundary,
        methodology_summary=methodology_summary,
        safe_next_action=safe_next_action,
    )
    answer_ledger_routing = _answer_ledger_routing(question_queue, generated_at=generated_at)
    return {
        "project_analysis_summary": project_analysis_summary,
        "methodology_audit_summary": methodology_summary,
        "source_policy_summary": source_policy_summary,
        "graph_dry_run_summary": graph_summary,
        "docs_logging_summary": docs_logging_summary,
        "dependency_readiness_summary": dependency_summary,
        "runtime_browser_boundary": runtime_boundary,
        "question_queue": question_queue,
        "first_response": first_response,
        "answer_ledger_routing": answer_ledger_routing,
        "safe_next_action": safe_next_action,
    }


def build_first_run_script_registry(scripts_root: str | Path) -> dict[str, Any]:
    """Build a versioned registry for top-level Product-Agent OS scripts."""

    root = Path(scripts_root)
    scripts: list[dict[str, Any]] = []
    for script_path in sorted(root.glob("*.py")):
        source = script_path.read_text(encoding="utf-8", errors="replace")
        risk_class = _classify_first_run_script(script_path.name, source)
        help_contract = "present" if _has_help_contract(source) else "missing"
        safe_to_execute = risk_class == "safe_read_only" and help_contract == "present"
        execution_mode = "help_only" if safe_to_execute else "skip"
        scripts.append(
            {
                "script": script_path.name,
                "command_shape": f"python plugins/product-agent-os/scripts/{script_path.name} --help",
                "safe_command": ["python", f"plugins/product-agent-os/scripts/{script_path.name}", "--help"],
                "execution_mode": execution_mode,
                "risk_class": risk_class,
                "help_contract": help_contract,
                "safe_to_execute": safe_to_execute,
                "approval_required": risk_class in {"approval_required", "blocked_live"},
                "timeout_seconds": DEFAULT_SCRIPT_HELP_TIMEOUT_SECONDS,
                "expected_output_shape": "help_text",
                "write_boundary": _script_write_boundary(risk_class),
                "prerequisites": [],
                "stop_condition": _script_stop_condition(risk_class, help_contract),
            }
        )
    registry = {
        "schema_version": FIRST_RUN_SCRIPT_REGISTRY_SCHEMA_VERSION,
        "script_root": "plugins/product-agent-os/scripts",
        "execution_policy": "help_only_safe_read_only_scripts",
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "scripts": scripts,
        "counts": _count_by_field(scripts, "risk_class"),
    }
    registry["registry_digest"] = content_digest(canonical_json(registry))
    return registry


def validate_first_run_script_registry(registry: Any) -> list[str]:
    if not isinstance(registry, dict):
        return ["first-run script registry must be an object"]
    errors: list[str] = []
    if registry.get("schema_version") != FIRST_RUN_SCRIPT_REGISTRY_SCHEMA_VERSION:
        errors.append(f"schema_version must be {FIRST_RUN_SCRIPT_REGISTRY_SCHEMA_VERSION}")
    scripts = registry.get("scripts")
    if not isinstance(scripts, list) or not scripts:
        return errors + ["scripts must be a non-empty list"]
    seen: set[str] = set()
    for index, row in enumerate(scripts):
        if not isinstance(row, dict):
            errors.append(f"scripts[{index}] must be an object")
            continue
        script = str(row.get("script", "")).strip()
        if not script.endswith(".py") or not _safe_relative_path(script):
            errors.append(f"scripts[{index}].script must be a top-level Python file name")
        if script in seen:
            errors.append(f"duplicate script registry row: {script}")
        seen.add(script)
        if row.get("risk_class") not in {"safe_read_only", "approval_required", "blocked_live"}:
            errors.append(f"scripts[{index}].risk_class missing or invalid")
        if row.get("help_contract") not in {"present", "missing"}:
            errors.append(f"scripts[{index}].help_contract missing or invalid")
        if row.get("help_contract") != "present":
            errors.append(f"scripts[{index}].help_contract must be present")
        if row.get("execution_mode") not in {"help_only", "skip"}:
            errors.append(f"scripts[{index}].execution_mode missing or invalid")
        if not isinstance(row.get("safe_to_execute"), bool):
            errors.append(f"scripts[{index}].safe_to_execute must be boolean")
        if not isinstance(row.get("timeout_seconds"), int) or row.get("timeout_seconds", 0) <= 0:
            errors.append(f"scripts[{index}].timeout_seconds must be a positive integer")
        safe_command = row.get("safe_command")
        if not isinstance(safe_command, list) or "--help" not in [str(part) for part in safe_command]:
            errors.append(f"scripts[{index}].safe_command must include --help")
        if _contains_local_absolute_path(row):
            errors.append(f"scripts[{index}] leaks a local absolute path")
    return errors


def execute_first_run_safe_script_matrix(
    registry: dict[str, Any],
    *,
    executor: Any | None = None,
    generated_at: str = "",
) -> dict[str, Any]:
    """Execute only safe help-only rows from the first-run script registry."""

    runner = executor or _default_help_executor
    commands: list[dict[str, Any]] = []
    for row in registry.get("scripts", []):
        if not isinstance(row, dict):
            continue
        risk_class = str(row.get("risk_class", "blocked_live"))
        command_entry = {
            "script": str(row.get("script", "")).strip(),
            "risk_class": risk_class,
            "execution_mode": str(row.get("execution_mode", "skip")),
            "safe_command": _safe_command_parts(row.get("safe_command")),
            "command": _command_string(row.get("safe_command")),
            "raw_stdout_stored": False,
            "raw_stderr_stored": False,
            "redaction_status": {
                "status": "passed_redacted",
                "raw_stdout_stored": False,
                "raw_stderr_stored": False,
                "local_absolute_paths_allowed": False,
                "secrets_allowed": False,
            },
        }
        if row.get("safe_to_execute") is not True:
            command_entry.update(
                {
                    "status": _skip_status_for_risk(risk_class),
                    "exit_code": None,
                    "duration_ms": 0,
                    "stdout_digest": content_digest(""),
                    "stderr_digest": content_digest(""),
                    "stdout_line_count": 0,
                    "stderr_line_count": 0,
                    "skip_reason": str(row.get("stop_condition", "approval or live runtime boundary")),
                }
            )
            commands.append(command_entry)
            continue
        try:
            result = runner(row)
            exit_code = _int(result.get("exit_code"))
            duration_ms = _int(result.get("duration_ms"))
            stdout = str(result.get("stdout", ""))
            stderr = str(result.get("stderr", ""))
            command_entry.update(
                {
                    "status": "passed" if exit_code == 0 else "failed",
                    "exit_code": exit_code,
                    "duration_ms": duration_ms,
                    "stdout_digest": content_digest(stdout),
                    "stderr_digest": content_digest(stderr),
                    "stdout_line_count": _line_count(stdout),
                    "stderr_line_count": _line_count(stderr),
                }
            )
        except subprocess.TimeoutExpired:
            command_entry.update(
                {
                    "status": "failed",
                    "exit_code": None,
                    "duration_ms": _int(row.get("timeout_seconds")) * 1000,
                    "stdout_digest": content_digest(""),
                    "stderr_digest": content_digest("timeout"),
                    "stdout_line_count": 0,
                    "stderr_line_count": 1,
                    "failure_reason": "timeout",
                }
            )
        commands.append(command_entry)
    matrix = {
        "schema_version": FIRST_RUN_COMMAND_MATRIX_SCHEMA_VERSION,
        "generated_at": str(generated_at),
        "execution_policy": "safe_help_only_no_target_mutation",
        "commands": commands,
        "counts": _count_by_field(commands, "status"),
        "completion_claim": "not_claimed",
        "generated_view_policy": GENERATED_VIEW_POLICY,
    }
    matrix["matrix_digest"] = content_digest(canonical_json(matrix))
    return matrix


def normalize_first_run_command_outputs(matrix: dict[str, Any]) -> dict[str, Any]:
    """Build a bounded evidence summary from the command matrix."""

    commands = [row for row in matrix.get("commands", []) if isinstance(row, dict)]
    counts = _count_by_field(commands, "status")
    failed = sorted(str(row.get("script", "")) for row in commands if row.get("status") == "failed")
    skipped_approval = sorted(
        str(row.get("script", ""))
        for row in commands
        if row.get("status") == "skipped_approval_required"
    )
    skipped_live = sorted(
        str(row.get("script", ""))
        for row in commands
        if row.get("status") == "skipped_blocked_live"
    )
    if failed:
        overall_status = "partial_failure"
    elif skipped_approval or skipped_live:
        overall_status = "partial_with_skips"
    elif commands and counts.get("passed", 0) == len(commands):
        overall_status = "complete"
    else:
        overall_status = "not_available"
    summary = {
        "schema_version": FIRST_RUN_EVIDENCE_SUMMARY_SCHEMA_VERSION,
        "overall_status": overall_status,
        "counts": counts,
        "failed_commands": failed,
        "skipped_commands": sorted(skipped_approval + skipped_live),
        "approval_required_commands": skipped_approval,
        "blocked_live_commands": skipped_live,
        "redaction_status": {
            "raw_stdout_stored": False,
            "raw_stderr_stored": False,
            "local_absolute_paths_allowed": False,
            "secrets_allowed": False,
        },
        "completion_claim": "not_claimed",
        "safe_next_action": _safe_next_action_for_command_summary(overall_status),
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def build_first_run_resume_ledger(matrix: dict[str, Any]) -> dict[str, Any]:
    """Build the partial-failure and resume ledger for first-run command evidence."""

    commands = [row for row in matrix.get("commands", []) if isinstance(row, dict)]
    summary = normalize_first_run_command_outputs({"commands": commands})
    failed_rows = [row for row in commands if row.get("status") == "failed"]
    approval_rows = [row for row in commands if row.get("status") == "skipped_approval_required"]
    blocked_rows = [row for row in commands if row.get("status") == "skipped_blocked_live"]
    resume_commands = [
        {
            "script": str(row.get("script", "")),
            "command": _command_string(row.get("safe_command")),
            "reason": "previous_run_failed",
        }
        for row in failed_rows
    ]
    ledger = {
        "schema_version": FIRST_RUN_RESUME_LEDGER_SCHEMA_VERSION,
        "status": summary["overall_status"],
        "completion_claim": "not_claimed",
        "resume_required_for": sorted(str(row.get("script", "")) for row in failed_rows),
        "approval_required_for": sorted(str(row.get("script", "")) for row in approval_rows),
        "blocked_live_for": sorted(str(row.get("script", "")) for row in blocked_rows),
        "resume_commands": resume_commands,
        "safe_next_action": _safe_next_action_for_command_summary(summary["overall_status"]),
        "state_policy": "passed_blocked_failed_skipped_states_are_preserved",
    }
    ledger["ledger_digest"] = content_digest(canonical_json(ledger))
    return ledger


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


def _first_run_source_artifacts(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    artifacts = [
        {
            "artifact_id": "workspace_inventory",
            "path": "workspace-inventory",
            "digest": content_digest(canonical_json(inventory)),
            "evidence_status": "inspection_only",
            "provenance": "run_first_project_analysis",
        }
    ]
    files = inventory.get("files") if isinstance(inventory, dict) else []
    if not isinstance(files, list):
        return artifacts
    for item in files[:200]:
        if not isinstance(item, dict):
            continue
        relative_path = _safe_relative_ref(str(item.get("path", "")))
        if not relative_path:
            continue
        artifacts.append(
            {
                "artifact_id": relative_path,
                "path": relative_path,
                "digest": content_digest(canonical_json({"path": relative_path, "size": _int(item.get("size"))})),
                "evidence_status": "inspection_only",
                "provenance": "workspace_inventory_file",
            }
        )
    return artifacts


def _project_analysis_summary(discovery: dict[str, Any]) -> dict[str, Any]:
    usage_mode = discovery.get("usage_mode") if isinstance(discovery.get("usage_mode"), dict) else {}
    generated_inputs = discovery.get("generated_artifact_inputs") if isinstance(discovery.get("generated_artifact_inputs"), dict) else {}
    first_run_generated = generated_inputs.get("first_run_analysis") if isinstance(generated_inputs.get("first_run_analysis"), dict) else {}
    return {
        "schema_version": "first_run_project_analysis_summary_v1",
        "usage_mode": {
            "primary": str(usage_mode.get("primary", "maintenance")),
            "secondary": _safe_string_list(usage_mode.get("secondary"))[:5],
            "confidence": _confidence_or_default(usage_mode.get("confidence")),
        },
        "route_reasons": _safe_string_list(usage_mode.get("reasons"))[:5],
        "detected_stack": _safe_string_list(discovery.get("detected_stack"))[:8],
        "complexity_profile": {
            "name": str((discovery.get("complexity_profile") or {}).get("name", "unknown")),
            "confidence": _confidence_or_default((discovery.get("complexity_profile") or {}).get("confidence")),
        },
        "control_plane": {
            "existing": _safe_string_list(discovery.get("existing_control_plane"))[:12],
            "missing": _safe_string_list(discovery.get("missing_control_plane"))[:12],
        },
        "generated_artifact_inputs": {
            "status": str(first_run_generated.get("status", "not_available")),
            "source_truth_allowed": False,
            "generated_view_policy": GENERATED_VIEW_POLICY,
            "evidence_ref_count": len(first_run_generated.get("evidence_refs", []))
            if isinstance(first_run_generated.get("evidence_refs"), list)
            else 0,
        },
        "source_policy": "route uses source files; generated artifacts are orientation-only",
        "completion_claim": "not_claimed",
    }


def _methodology_audit_summary(methodology: dict[str, Any]) -> dict[str, Any]:
    domains = methodology.get("methodology_domains") if isinstance(methodology.get("methodology_domains"), list) else []
    recommendations = methodology.get("recommendations") if isinstance(methodology.get("recommendations"), list) else []
    return {
        "schema_version": "first_run_methodology_audit_summary_v1",
        "status": str(methodology.get("status", "not_available")),
        "write_policy": str(methodology.get("write_policy", "read_only")),
        "maturity_level": _selected_packet(methodology.get("maturity_level")),
        "complexity_profile": _selected_packet(methodology.get("complexity_profile")),
        "applicable_domains": [
            {
                "id": str(item.get("id", "")),
                "status": str(item.get("status", "")),
            }
            for item in domains
            if isinstance(item, dict) and str(item.get("status", "")) != "not_applicable"
        ][:8],
        "top_recommendations": [
            {
                "priority": str(item.get("priority", "")),
                "domain": str(item.get("domain", "")),
                "gate": str(item.get("gate", "")),
                "safe_next_action": str(item.get("safe_next_action", "")),
            }
            for item in recommendations
            if isinstance(item, dict)
        ][:5],
        "first_safe_action": _first_safe_action_text(methodology.get("first_safe_action")),
        "safe_next_action": str(methodology.get("safe_next_action", "")),
        "question_count": len(methodology.get("questions_for_owner", []))
        if isinstance(methodology.get("questions_for_owner"), list)
        else 0,
        "completion_claim": "not_claimed",
    }


def _source_policy_summary(source_policy: dict[str, Any]) -> dict[str, Any]:
    status = str(source_policy.get("status", "not_available"))
    blocked = status in {"blocked", "needs_review"}
    errors = _safe_string_list(source_policy.get("errors"))[:8]
    registry_updates = _safe_string_list(source_policy.get("registry_updates_required"))[:12]
    secret_findings = _safe_string_list(source_policy.get("secret_findings"))[:8]
    unsupported = ["source policy blocked apply/promotion"] if blocked else []
    if secret_findings:
        unsupported.append("secret findings block generated evidence promotion")
    return {
        "schema_version": "first_run_source_policy_summary_v1",
        "status": status,
        "section_status": "approval_required" if blocked else "current",
        "file_count": len(source_policy.get("files", [])) if isinstance(source_policy.get("files"), list) else 0,
        "registry_update_required_count": len(source_policy.get("registry_updates_required", []))
        if isinstance(source_policy.get("registry_updates_required"), list)
        else 0,
        "registry_updates_required": registry_updates,
        "error_count": len(errors),
        "errors": errors,
        "secret_finding_count": len(secret_findings),
        "unsupported_claims": unsupported,
        "safe_next_action": "Fix source-policy blockers before apply, promotion or readiness claims."
        if blocked
        else "Source policy has no current blocker in this read-only pass.",
        "completion_claim": "not_claimed",
    }


def _graph_dry_run_summary(graph: dict[str, Any]) -> dict[str, Any]:
    metadata = graph.get("metadata") if isinstance(graph.get("metadata"), dict) else {}
    validation = graph.get("validation") if isinstance(graph.get("validation"), dict) else {}
    coverage = metadata.get("coverage_map") if isinstance(metadata.get("coverage_map"), dict) else {}
    return {
        "schema_version": "first_run_graph_dry_run_summary_v1",
        "status": "inspection_only",
        "write_policy": str(graph.get("write_policy", "read_only")),
        "node_count": len(graph.get("nodes", [])) if isinstance(graph.get("nodes"), list) else 0,
        "edge_count": len(graph.get("edges", [])) if isinstance(graph.get("edges"), list) else 0,
        "observation_count": len(graph.get("observations", [])) if isinstance(graph.get("observations"), list) else 0,
        "validation_ok": bool(validation.get("ok", False)),
        "coverage": {
            "status": str(coverage.get("status", "not_available")),
            "total_files": _int((coverage.get("files") or {}).get("total") if isinstance(coverage.get("files"), dict) else 0),
            "partial_files": _int((coverage.get("files") or {}).get("partial") if isinstance(coverage.get("files"), dict) else 0),
        },
        "source_policy": "generated graph is not source truth",
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "completion_claim": "not_claimed",
        "unsupported_claims": ["semantic completeness", "runtime behavior", "impact proof"],
    }


def _docs_logging_summary(inventory: dict[str, Any]) -> dict[str, Any]:
    files = _inventory_paths(inventory)
    lowered = {path.lower() for path in files}
    docs_systems: list[str] = []
    if "mkdocs.yml" in lowered:
        docs_systems.append("mkdocs")
    if any(path.startswith("docs/") and path.endswith(".md") for path in lowered) or "readme.md" in lowered:
        docs_systems.append("markdown_docs")
    if any(path.startswith(".github/workflows/") for path in lowered):
        docs_systems.append("github_actions")
    signals: list[str] = []
    if _package_has_script(inventory, "test"):
        signals.append("package_test_script")
    if any(path.endswith(".log") or "runlog" in path for path in lowered):
        signals.append("log_or_runlog_files")
    if any(path.startswith("tests/") or "/tests/" in path for path in lowered):
        signals.append("test_files")
    return {
        "schema_version": "first_run_docs_logging_summary_v1",
        "status": "inspection_only",
        "docs_systems": sorted(set(docs_systems)) or ["not_detected"],
        "logging_or_test_signals": sorted(set(signals)) or ["not_detected"],
        "install_or_build_triggered": False,
        "source_policy": "static detection only; docs/logging presence is not verification success",
        "completion_claim": "not_claimed",
    }


def _dependency_readiness_summary(workspace: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    files = _inventory_paths(inventory)
    product_manifests: list[str] = []
    lockfiles: list[str] = []
    generated_runtime_artifacts: list[str] = []
    excluded_dependency_corpora: list[str] = []
    for ref in files:
        parts = set(ref.split("/"))
        if parts & {".git", ".next", "dist", "node_modules", "site", "vendor"}:
            excluded_dependency_corpora.append(ref)
            if parts & {".next", "dist", "site"}:
                generated_runtime_artifacts.append(ref)
            continue
        if ref.endswith(("package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod")):
            product_manifests.append(ref)
        if ref.endswith(("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "poetry.lock", "uv.lock")):
            lockfiles.append(ref)
    provider_risks = _provider_risks(workspace)
    runtime_entrypoints = _runtime_entrypoints_from_workspace(workspace)
    return {
        "schema_version": "first_run_dependency_readiness_summary_v1",
        "status": "partial_static_inventory" if product_manifests or lockfiles else "not_available",
        "product_manifests": sorted(product_manifests)[:20],
        "lockfiles": sorted(lockfiles)[:20],
        "generated_runtime_artifacts": sorted(generated_runtime_artifacts)[:20],
        "excluded_dependency_corpora_count": len(excluded_dependency_corpora),
        "provider_risks": provider_risks,
        "runtime_entrypoints": runtime_entrypoints,
        "install_or_dependency_mutation_performed": False,
        "build_performed": False,
        "source_policy": "static dependency inventory is not install/build/supply-chain proof",
        "completion_claim": "not_claimed",
    }


def _runtime_browser_boundary(dependency_summary: dict[str, Any]) -> dict[str, Any]:
    runtime_entrypoints = _safe_string_list(dependency_summary.get("runtime_entrypoints"))
    has_runtime = bool(runtime_entrypoints)
    return {
        "schema_version": "first_run_runtime_browser_boundary_v1",
        "status": "approval_required" if has_runtime else "not_available",
        "runtime_entrypoints": runtime_entrypoints[:12],
        "runtime_executed": False,
        "browser_automation_performed": False,
        "provider_api_call_performed": False,
        "target_workspace_mutation_performed": False,
        "browser_tool_status": "not_run",
        "provider_risks": dependency_summary.get("provider_risks", []),
        "approval_boundary": "runtime/browser/provider checks require exact approval and current evidence",
        "unsupported_claims": [
            "runtime/browser behavior",
            "provider/API/model quality",
            "performance",
            "accessibility",
        ],
        "completion_claim": "not_claimed",
    }


def _first_run_question_queue(
    *,
    methodology: dict[str, Any],
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
    project_analysis_summary: dict[str, Any],
) -> dict[str, Any]:
    owner_questions = list(methodology.get("questions_for_owner") or [])
    source_status = str(source_policy_summary.get("status", "not_available"))
    if source_status in {"blocked", "needs_review"}:
        owner_questions.append(
            {
                "text": "Which source-policy blocker should be fixed or accepted as a gap before apply, promotion or readiness claims?",
                "priority": "blocking",
                "category": "approval",
                "answer_type": "single_choice_or_text",
                "source_kind": "first_run_source_policy",
                "source_key": "source_policy_blocker_owner_decision",
                "block": "source_policy_summary",
                "artifact": "docs/sources/registry.md",
                "choices": ["fix_source_policy", "record_accepted_gap", "keep_blocked"],
            }
        )
    if runtime_boundary.get("status") == "approval_required":
        owner_questions.append(
            {
                "text": "Is runtime, browser or provider execution approved for a later separate run, or should this stay static-only?",
                "priority": "recommended",
                "category": "approval",
                "answer_type": "single_choice_or_text",
                "source_kind": "first_run_runtime_boundary",
                "source_key": "runtime_browser_provider_approval",
                "block": "runtime_browser_boundary",
                "artifact": "RUNLOG.md",
                "choices": ["static_only", "approve_disposable_runtime_later", "record_gap"],
            }
        )
    unknowns = [
        {
            "text": "Whether generated first-run output is useful enough for the next owner-reviewed slice.",
            "priority": "recommended",
            "category": "product",
            "source_key": "first_run_usefulness_review",
        }
    ]
    usage_mode = project_analysis_summary.get("usage_mode") if isinstance(project_analysis_summary.get("usage_mode"), dict) else {}
    return build_question_queue(
        owner_questions=owner_questions,
        unknowns=unknowns,
        usage_mode=usage_mode,
        runtime_status=str(runtime_boundary.get("status", "")),
    )


def _guided_first_response(
    *,
    question_queue: dict[str, Any],
    project_analysis_summary: dict[str, Any],
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
    methodology_summary: dict[str, Any],
    safe_next_action: str,
) -> dict[str, Any]:
    summary = question_queue.get("summary") if isinstance(question_queue.get("summary"), dict) else {}
    questions = [item for item in question_queue.get("questions", []) if isinstance(item, dict)]
    next_blocking = question_queue.get("next_blocking_question")
    deferred_questions = [item for item in questions if item != next_blocking]
    confidence = _guided_confidence(project_analysis_summary, source_policy_summary, runtime_boundary)
    route_options = _first_run_route_options(
        project_analysis_summary=project_analysis_summary,
        source_policy_summary=source_policy_summary,
        runtime_boundary=runtime_boundary,
        methodology_summary=methodology_summary,
    )
    return {
        "schema_version": FIRST_RUN_GUIDED_RESPONSE_SCHEMA_VERSION,
        "mode": "guided_first_response",
        "confidence": confidence,
        "summary": _first_response_summary(project_analysis_summary, source_policy_summary, runtime_boundary),
        "blocking_question": next_blocking if isinstance(next_blocking, dict) else None,
        "blocking_question_count": 1 if isinstance(next_blocking, dict) else 0,
        "question_counts": {
            "total": _int(summary.get("total")),
            "blocking": _int(summary.get("blocking")),
            "recommended": _int(summary.get("recommended")),
            "optional": _int(summary.get("optional")),
            "remaining": _int(summary.get("remaining")),
        },
        "deferred_question_count": len(deferred_questions),
        "deferred_question_preview_count": min(2, len(deferred_questions)),
        "deferred_question_preview": [
            {
                "id": str(item.get("id", "")),
                "priority": str(item.get("priority", "")),
                "category": str(item.get("category", "")),
                "text": str(item.get("text", "")),
            }
            for item in deferred_questions[:2]
        ],
        "route_options": route_options,
        "safe_next_action": str(safe_next_action),
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "answer_policy": "answers_require_staged_ledger_and_owner_review",
        "completion_claim": "not_claimed",
    }


def _answer_ledger_routing(question_queue: dict[str, Any], *, generated_at: str) -> dict[str, Any]:
    as_of_date = _date_from_timestamp(generated_at)
    ledger_template = build_answer_ledger(question_queue, {}, as_of_date=as_of_date)
    validation_errors = validate_answer_ledger(ledger_template)
    return {
        "schema_version": FIRST_RUN_ANSWER_LEDGER_ROUTING_SCHEMA_VERSION,
        "write_policy": "staged_only",
        "artifact_name": ANSWER_LEDGER_TEMPLATE_NAME,
        "target_workspace_mutation_performed": False,
        "unreviewed_answers_mutate_source_docs": False,
        "source_truth_policy": "answers_are_not_source_truth_until_owner_reviewed_and_staged",
        "ledger_template": ledger_template,
        "validation_errors": validation_errors,
        "completion_claim": "not_claimed",
    }


def _answer_ledger_routing_response(routing: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": str(routing.get("schema_version", "")),
        "write_policy": str(routing.get("write_policy", "")),
        "artifact_name": str(routing.get("artifact_name", "")),
        "target_workspace_mutation_performed": bool(routing.get("target_workspace_mutation_performed", True)),
        "unreviewed_answers_mutate_source_docs": bool(routing.get("unreviewed_answers_mutate_source_docs", True)),
        "validation_errors": _safe_string_list(routing.get("validation_errors")),
        "completion_claim": str(routing.get("completion_claim", "not_claimed")),
    }


def _first_run_route_options(
    *,
    project_analysis_summary: dict[str, Any],
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
    methodology_summary: dict[str, Any],
) -> list[dict[str, str]]:
    options = [
        {
            "id": "static_read_only_analysis",
            "label": "Review static first-run analysis",
            "safe_next_action": "Review packet and generated HTML as orientation evidence only.",
            "write_boundary": "no_target_mutation",
        }
    ]
    if source_policy_summary.get("status") in {"blocked", "needs_review"}:
        options.append(
            {
                "id": "fix_source_policy_or_record_gap",
                "label": "Resolve source-policy blocker",
                "safe_next_action": "Fix source-policy blockers or record an owner-reviewed accepted gap before promotion.",
                "write_boundary": "staged_docs_only_after_owner_review",
            }
        )
    elif methodology_summary.get("top_recommendations"):
        options.append(
            {
                "id": "stage_methodology_recommendation",
                "label": "Stage methodology recommendation",
                "safe_next_action": str(methodology_summary.get("safe_next_action") or "Stage the next methodology recommendation for review."),
                "write_boundary": "staged_generated_analysis_only",
            }
        )
    if runtime_boundary.get("status") == "approval_required":
        options.append(
            {
                "id": "request_runtime_browser_approval",
                "label": "Request separate runtime approval",
                "safe_next_action": "Ask for exact runtime/browser/provider approval before any live check.",
                "write_boundary": "approval_required_before_runtime_or_browser",
            }
        )
    if len(options) == 1:
        primary = str((project_analysis_summary.get("usage_mode") or {}).get("primary", "unknown"))
        options.append(
            {
                "id": "clarify_first_product_slice",
                "label": "Clarify first product slice",
                "safe_next_action": f"Confirm whether the detected route '{primary}' is the intended next slice.",
                "write_boundary": "answer_ledger_staged_only",
            }
        )
    return options[:3]


def _first_response_summary(
    project_analysis_summary: dict[str, Any],
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
) -> str:
    usage = project_analysis_summary.get("usage_mode") if isinstance(project_analysis_summary.get("usage_mode"), dict) else {}
    primary = str(usage.get("primary", "unknown"))
    source_status = str(source_policy_summary.get("status", "not_available"))
    runtime_status = str(runtime_boundary.get("status", "not_available"))
    return f"Detected route: {primary}; source policy: {source_status}; runtime boundary: {runtime_status}."


def _guided_confidence(
    project_analysis_summary: dict[str, Any],
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
) -> str:
    if source_policy_summary.get("status") in {"blocked", "needs_review"}:
        return "medium"
    if runtime_boundary.get("status") == "approval_required":
        return "medium"
    usage = project_analysis_summary.get("usage_mode") if isinstance(project_analysis_summary.get("usage_mode"), dict) else {}
    return _confidence_or_default(usage.get("confidence"))


def _date_from_timestamp(value: str) -> str:
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", str(value or ""))
    return match.group(1) if match else "1970-01-01"


def _empty_guided_first_response(safe_next_action: str) -> dict[str, Any]:
    return {
        "schema_version": FIRST_RUN_GUIDED_RESPONSE_SCHEMA_VERSION,
        "mode": "guided_first_response",
        "confidence": "unknown",
        "summary": "First-run guided response is not available.",
        "blocking_question": None,
        "blocking_question_count": 0,
        "question_counts": {"total": 0, "blocking": 0, "recommended": 0, "optional": 0, "remaining": 0},
        "deferred_question_count": 0,
        "deferred_question_preview_count": 0,
        "deferred_question_preview": [],
        "route_options": [],
        "safe_next_action": str(safe_next_action or "Review first-run analysis."),
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "answer_policy": "answers_require_staged_ledger_and_owner_review",
        "completion_claim": "not_claimed",
    }


def _empty_answer_ledger_routing(generated_at: str) -> dict[str, Any]:
    return _answer_ledger_routing(build_question_queue(runtime_status="not_available"), generated_at=generated_at)


def _empty_project_analysis_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_project_analysis_summary_v1",
        "usage_mode": {"primary": "unknown", "secondary": [], "confidence": "unknown"},
        "route_reasons": [],
        "detected_stack": [],
        "complexity_profile": {"name": "unknown", "confidence": "unknown"},
        "control_plane": {"existing": [], "missing": []},
        "generated_artifact_inputs": {"status": "not_available", "source_truth_allowed": False, "generated_view_policy": GENERATED_VIEW_POLICY, "evidence_ref_count": 0},
        "source_policy": "not_available",
        "completion_claim": "not_claimed",
    }


def _empty_methodology_audit_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_methodology_audit_summary_v1",
        "status": "not_available",
        "write_policy": "read_only",
        "maturity_level": {"selected": "unknown", "confidence": "unknown"},
        "complexity_profile": {"selected": "unknown", "confidence": "unknown"},
        "applicable_domains": [],
        "top_recommendations": [],
        "first_safe_action": "",
        "safe_next_action": "",
        "question_count": 0,
        "completion_claim": "not_claimed",
    }


def _empty_source_policy_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_source_policy_summary_v1",
        "status": "not_available",
        "section_status": "not_available",
        "file_count": 0,
        "registry_update_required_count": 0,
        "registry_updates_required": [],
        "error_count": 0,
        "errors": [],
        "secret_finding_count": 0,
        "unsupported_claims": [],
        "safe_next_action": "Run source-policy validation before promotion.",
        "completion_claim": "not_claimed",
    }


def _empty_graph_dry_run_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_graph_dry_run_summary_v1",
        "status": "not_available",
        "write_policy": "read_only",
        "node_count": 0,
        "edge_count": 0,
        "observation_count": 0,
        "validation_ok": False,
        "coverage": {"status": "not_available", "total_files": 0, "partial_files": 0},
        "source_policy": "generated graph is not source truth",
        "generated_view_policy": GENERATED_VIEW_POLICY,
        "completion_claim": "not_claimed",
        "unsupported_claims": [],
    }


def _empty_docs_logging_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_docs_logging_summary_v1",
        "status": "not_available",
        "docs_systems": [],
        "logging_or_test_signals": [],
        "install_or_build_triggered": False,
        "source_policy": "static detection only",
        "completion_claim": "not_claimed",
    }


def _empty_dependency_readiness_summary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_dependency_readiness_summary_v1",
        "status": "not_available",
        "product_manifests": [],
        "lockfiles": [],
        "generated_runtime_artifacts": [],
        "excluded_dependency_corpora_count": 0,
        "provider_risks": [],
        "runtime_entrypoints": [],
        "install_or_dependency_mutation_performed": False,
        "build_performed": False,
        "source_policy": "static dependency inventory is not install/build/supply-chain proof",
        "completion_claim": "not_claimed",
    }


def _empty_runtime_browser_boundary() -> dict[str, Any]:
    return {
        "schema_version": "first_run_runtime_browser_boundary_v1",
        "status": "not_available",
        "runtime_entrypoints": [],
        "runtime_executed": False,
        "browser_automation_performed": False,
        "provider_api_call_performed": False,
        "target_workspace_mutation_performed": False,
        "browser_tool_status": "not_run",
        "provider_risks": [],
        "approval_boundary": "runtime/browser/provider checks require exact approval and current evidence",
        "unsupported_claims": [],
        "completion_claim": "not_claimed",
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


def _validate_guided_first_response(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["first_response must be an object"]
    errors: list[str] = []
    if value.get("schema_version") != FIRST_RUN_GUIDED_RESPONSE_SCHEMA_VERSION:
        errors.append(f"first_response.schema_version must be {FIRST_RUN_GUIDED_RESPONSE_SCHEMA_VERSION}")
    if value.get("mode") != "guided_first_response":
        errors.append("first_response.mode must be guided_first_response")
    if "questions" in value:
        errors.append("first_response.questions is forbidden")
    if _int(value.get("blocking_question_count")) > 1:
        errors.append("first_response.blocking_question_count must be <= 1")
    route_options = value.get("route_options")
    if not isinstance(route_options, list):
        errors.append("first_response.route_options must be list")
    elif len(route_options) > 3:
        errors.append("first_response.route_options must contain at most 3 options")
    if value.get("generated_view_policy") != GENERATED_VIEW_POLICY:
        errors.append(f"first_response.generated_view_policy must be {GENERATED_VIEW_POLICY}")
    if value.get("completion_claim") != "not_claimed":
        errors.append("first_response.completion_claim must be not_claimed")
    return errors


def _validate_answer_ledger_routing(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["answer_ledger_routing must be an object"]
    errors: list[str] = []
    if value.get("schema_version") != FIRST_RUN_ANSWER_LEDGER_ROUTING_SCHEMA_VERSION:
        errors.append(f"answer_ledger_routing.schema_version must be {FIRST_RUN_ANSWER_LEDGER_ROUTING_SCHEMA_VERSION}")
    if value.get("write_policy") != "staged_only":
        errors.append("answer_ledger_routing.write_policy must be staged_only")
    if value.get("target_workspace_mutation_performed") is not False:
        errors.append("answer_ledger_routing.target_workspace_mutation_performed must be false")
    if value.get("unreviewed_answers_mutate_source_docs") is not False:
        errors.append("answer_ledger_routing.unreviewed_answers_mutate_source_docs must be false")
    template = value.get("ledger_template")
    if not isinstance(template, dict):
        errors.append("answer_ledger_routing.ledger_template must be an object")
    else:
        errors.extend(f"answer_ledger_routing.{error}" for error in validate_answer_ledger(template))
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


def _selected_packet(value: Any) -> dict[str, str]:
    source = value if isinstance(value, dict) else {}
    return {
        "selected": str(source.get("selected", "unknown")),
        "confidence": _confidence_or_default(source.get("confidence")),
    }


def _first_safe_action_text(value: Any) -> str:
    if isinstance(value, dict):
        direct = value.get("safe_next_action")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        recommendations = value.get("recommendations")
        if isinstance(recommendations, list):
            for item in recommendations:
                if isinstance(item, dict) and isinstance(item.get("safe_next_action"), str):
                    return item["safe_next_action"].strip()
        return str(value.get("status", "not_available"))
    return str(value or "").strip()


def _inventory_paths(inventory: dict[str, Any]) -> list[str]:
    files = inventory.get("files") if isinstance(inventory.get("files"), list) else []
    paths = []
    for item in files:
        if not isinstance(item, dict):
            continue
        ref = _safe_relative_ref(str(item.get("path", "")))
        if ref and ref != "[REDACTED_LOCAL_PATH]":
            paths.append(ref)
    return paths


def _package_has_script(inventory: dict[str, Any], script_name: str) -> bool:
    return "package.json" in {path.lower() for path in _inventory_paths(inventory)} and bool(script_name)


def _runtime_entrypoints_from_workspace(workspace: Path) -> list[str]:
    package_file = workspace / "package.json"
    if not package_file.is_file():
        return []
    try:
        payload = json.loads(package_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    scripts = payload.get("scripts") if isinstance(payload, dict) else None
    if not isinstance(scripts, dict):
        return []
    entrypoints: list[str] = []
    for name in ("dev", "start", "serve", "preview", "electron", "tauri"):
        value = scripts.get(name)
        if isinstance(value, str) and value.strip():
            entrypoints.append(f"package.json:scripts.{name}")
    return entrypoints


def _provider_risks(workspace: Path) -> list[str]:
    risks: set[str] = set()
    package_file = workspace / "package.json"
    if package_file.is_file():
        try:
            payload = json.loads(package_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        dependencies: dict[str, Any] = {}
        if isinstance(payload, dict):
            for field in ("dependencies", "devDependencies", "optionalDependencies"):
                if isinstance(payload.get(field), dict):
                    dependencies.update(payload[field])
        for name in dependencies:
            lowered = str(name).lower()
            if any(term in lowered for term in ("openai", "anthropic", "google", "genai", "stripe", "supabase")):
                risks.add(f"provider_dependency:{name}")
    env_refs = [path.name for path in workspace.glob(".env*") if path.is_file()]
    if env_refs:
        risks.add("env_file_provider_credentials_possible")
    return sorted(risks)[:12]


def _s3_safe_next_action(
    source_policy_summary: dict[str, Any],
    runtime_boundary: dict[str, Any],
    methodology_summary: dict[str, Any],
) -> str:
    if source_policy_summary.get("status") in {"blocked", "needs_review"}:
        return str(source_policy_summary.get("safe_next_action"))
    if runtime_boundary.get("status") == "approval_required":
        return "Review static first-run analysis; request exact approval before runtime/browser/provider checks."
    return str(methodology_summary.get("safe_next_action") or "Review first-run project analysis before the next slice.")


def _classify_first_run_script(script_name: str, source: str) -> str:
    if script_name in BLOCKED_LIVE_SCRIPTS:
        return "blocked_live"
    if script_name in APPROVAL_REQUIRED_SCRIPTS:
        return "approval_required"
    if re.search(r"\b(--apply|rollback|Start-Process|browser|provider|deploy|publish)\b", source):
        return "approval_required"
    return "safe_read_only"


def _has_help_contract(source: str) -> bool:
    return any(
        marker in source
        for marker in ("argparse", "ArgumentParser", "--help", "def main", "main(sys.argv", 'if __name__ == "__main__"')
    )


def _script_write_boundary(risk_class: str) -> str:
    if risk_class == "safe_read_only":
        return "help_only_no_target_mutation"
    if risk_class == "approval_required":
        return "script_has_write_or_apply_modes_approval_required"
    return "live_runtime_or_external_boundary_blocked"


def _script_stop_condition(risk_class: str, help_contract: str) -> str:
    if help_contract != "present":
        return "missing help contract"
    if risk_class == "safe_read_only":
        return "stop if help output leaks raw source, secrets or local absolute paths"
    if risk_class == "approval_required":
        return "approval required before non-help execution"
    return "live/runtime/provider/browser boundary requires exact approval"


def _count_by_field(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        key = str(row.get(field, "unknown")).strip() or "unknown"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))


def _safe_command_parts(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [_safe_relative_ref(str(part)) if index > 0 else str(part).strip() for index, part in enumerate(value)]


def _command_string(value: Any) -> str:
    return " ".join(_safe_command_parts(value))


def _skip_status_for_risk(risk_class: str) -> str:
    if risk_class == "approval_required":
        return "skipped_approval_required"
    if risk_class == "blocked_live":
        return "skipped_blocked_live"
    return "skipped_not_applicable"


def _line_count(value: str) -> int:
    if not value:
        return 0
    return len(value.splitlines())


def _default_help_executor(row: dict[str, Any]) -> dict[str, Any]:
    script_name = str(row.get("script", "")).strip()
    script_path = Path(__file__).resolve().parents[1] / script_name
    started = time.perf_counter()
    result = subprocess.run(
        [sys.executable, str(script_path), "--help"],
        check=False,
        capture_output=True,
        text=True,
        timeout=_int(row.get("timeout_seconds")) or DEFAULT_SCRIPT_HELP_TIMEOUT_SECONDS,
    )
    return {
        "exit_code": result.returncode,
        "duration_ms": int((time.perf_counter() - started) * 1000),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def _safe_next_action_for_command_summary(overall_status: str) -> str:
    if overall_status == "partial_failure":
        return "Inspect failed help-only command rows, fix the local script contract, then rerun first-run analysis."
    if overall_status == "partial_with_skips":
        return "Review approval-required or live-bound scripts before any non-help execution."
    if overall_status == "complete":
        return "Continue to the next first-run integration slice without claiming release or runtime readiness."
    return "Review the command matrix before continuing."


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
    "ANSWER_LEDGER_TEMPLATE_NAME",
    "FIRST_RUN_PACKET_NAME",
    "SECRET_LIKE_VALUE_RE",
    "adapt_first_run_analysis_sections",
    "build_first_run_analysis_packet",
    "build_first_run_automation_contract",
    "build_first_run_project_analysis_summaries",
    "build_first_run_resume_ledger",
    "build_first_run_script_registry",
    "execute_first_run_safe_script_matrix",
    "normalize_first_run_command_outputs",
    "run_first_project_analysis",
    "validate_first_run_automation_contract",
    "validate_first_run_analysis_packet",
    "validate_first_run_script_registry",
]
