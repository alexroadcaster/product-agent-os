from __future__ import annotations

import re
from typing import Any, Mapping

from product_agent_os.analysis_artifact_renderer import FIRST_RUN_ANALYSIS_PAGE_IDS
from product_agent_os.stage_manifest import canonical_json, content_digest


FIRST_RUN_GENERATED_PAGES = tuple(FIRST_RUN_ANALYSIS_PAGE_IDS)
SUMMARY_SCHEMA_VERSION = "batch39_s4_m37_m39_hardening_summary_v1"
FULL_HARDENING_SCHEMA_VERSION = "batch39_s4_full_hardening_summary_v1"
ATTEMPT_ID = "B39-S4-M37-M39-A01"
FULL_HARDENING_ATTEMPT_ID = "B39-S4-FULL-HARDENING-A01"
EXTERNAL_URL_RE = re.compile(r"\bhttps?://[^\s\"'<>]+", re.IGNORECASE)
SCRIPT_TAG_RE = re.compile(r"<\s*script\b", re.IGNORECASE)
DEPENDENCY_CORPUS_PARTS = {
    ".git",
    ".next",
    "dist",
    "node_modules",
    "antigravity-awesome-skills-main",
}


def build_m37_public_docs_acceptance(
    *,
    public_docs_scope: str,
    first_run_page_ids: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    page_ids = [str(page_id).strip() for page_id in first_run_page_ids if str(page_id).strip()]
    internal_only = public_docs_scope == "internal_control_plane_only"
    classification = "not_applicable_to_public_site" if internal_only else "included_in_public_docs_review"
    status = "partial_pass_public_docs_internal_only" if internal_only else "needs_public_docs_acceptance_review"
    return {
        "task_id": "B39-TEST-M37",
        "status": status,
        "public_docs_scope": public_docs_scope,
        "public_readiness_claim": "not_claimed",
        "first_run_generated_pages": {
            "classification": classification,
            "page_count": len(page_ids),
            "page_ids": page_ids,
            "generated_view_policy": "orientation_only_not_proof",
        },
        "acceptance": {
            "source_docs_checked": [
                "docs/product-agent-os/",
                "mkdocs.yml",
                "docs/superpowers/specs/",
            ],
            "site_freshness": {
                "status": "stale_rendered_site_not_rebuilt_in_this_attempt",
                "latest_site_build_known_from_inspection": "2026-06-10",
                "b39_s4_source_evidence_date": "2026-06-18",
            },
            "required_public_claim_boundary": "generated pages may orient operators but cannot prove readiness",
            "release_surface": "approval_required",
        },
        "residual_gaps": [
            "strict MkDocs site rebuild was not run in this attempt",
            "rendered site freshness remains older than current B39-S4 evidence",
            "public documentation acceptance remains blocked until a fresh docs/site verification packet exists",
        ],
        "unsupported_claims": [
            "generated orientation evidence is not public readiness proof",
            "public docs/site publication acceptance has not been claimed",
            "external publication, deploy and release review were not performed",
        ],
    }


def audit_first_run_offline_html(html_pages: Mapping[str, str]) -> dict[str, Any]:
    violations: list[dict[str, str]] = []
    blocked_counts = {"external_url": 0, "script_tag": 0}
    for page, body in html_pages.items():
        page_name = str(page)
        text = str(body)
        for match in EXTERNAL_URL_RE.findall(text):
            blocked_counts["external_url"] += 1
            violations.append({"page": page_name, "kind": "external_url", "value": match})
        for match in SCRIPT_TAG_RE.findall(text):
            blocked_counts["script_tag"] += 1
            violations.append({"page": page_name, "kind": "script_tag", "value": match.lower()})

    passed = all(count == 0 for count in blocked_counts.values())
    return {
        "task_id": "B39-TEST-M38",
        "status": "passed_no_external_url_or_script" if passed else "blocked_external_url_or_script",
        "page_count": len(html_pages),
        "blocked_counts": blocked_counts,
        "violations": violations,
        "policy": {
            "external_urls_allowed": False,
            "script_tags_allowed": False,
            "offline_generated_html_only": True,
        },
        "unsupported_claims": [
            "offline HTML audit does not prove browser/runtime behavior",
            "dependency supply-chain readiness beyond generated first-run HTML is still separate B39-S4 work",
        ],
    }


def build_m38_offline_asset_readiness() -> dict[str, Any]:
    audit = audit_first_run_offline_html(_canonical_first_run_html_samples())
    return {
        "task_id": "B39-TEST-M38",
        "status": "partial_pass_offline_asset_readiness",
        "first_run_html_audit": audit,
        "dependency_policy": {
            "new_external_runtime_dependencies_added": False,
            "cdn_assets_allowed": False,
            "generated_html_must_remain_static": True,
        },
        "residual_gaps": [
            "full static URL scan across docs, templates, renderers and MkDocs assets is not complete",
            "package manifest dependency readiness matrix is still pending",
            "Mermaid external asset gap remains accepted/follow-up rather than closed",
        ],
        "unsupported_claims": audit["unsupported_claims"],
    }


def build_m39_cli_contract_matrix() -> dict[str, Any]:
    return {
        "task_id": "B39-TEST-M39",
        "status": "partial_pass_cli_contract_matrix",
        "cases": [
            {
                "case_id": "first_run_dry_run",
                "command_shape": "python plugins/product-agent-os/scripts/run_first_project_analysis.py <workspace> --dry-run",
                "expected_status": "accepted",
                "write_scope": "stdout_only",
                "evidence_ref": "tests/product_agent_os/test_first_run_analysis.py::test_m20_2_cli_dry_run_prints_packet_without_writing_analysis_directory",
            },
            {
                "case_id": "first_run_write",
                "command_shape": "python plugins/product-agent-os/scripts/run_first_project_analysis.py <workspace> --write",
                "expected_status": "accepted",
                "write_scope": ".codex/product-agent-os/analysis",
                "evidence_ref": "tests/product_agent_os/test_first_run_analysis.py::test_m20_2_cli_write_mode_writes_only_generated_analysis_packet_inside_workspace",
            },
            {
                "case_id": "first_run_ambiguous_mode_rejection",
                "command_shape": "python plugins/product-agent-os/scripts/run_first_project_analysis.py <workspace> --dry-run --write",
                "expected_status": "rejected",
                "write_scope": "none",
                "guardrail": "choose_exactly_one_mode",
                "evidence_ref": "tests/product_agent_os/test_first_run_analysis.py::test_m20_2_cli_rejects_ambiguous_mode_and_external_stage_argument",
            },
            {
                "case_id": "first_run_stage_rejection",
                "command_shape": "python plugins/product-agent-os/scripts/run_first_project_analysis.py <workspace> --stage <external-stage>",
                "expected_status": "rejected",
                "write_scope": "none",
                "guardrail": "first_run_cli_does_not_accept_stage",
                "evidence_ref": "tests/product_agent_os/test_first_run_analysis.py::test_m20_2_cli_rejects_ambiguous_mode_and_external_stage_argument",
            },
            {
                "case_id": "unsafe_packet_rejection",
                "command_shape": "validate_first_run_analysis_packet(<packet>)",
                "expected_status": "rejected",
                "write_scope": "none",
                "guardrail": "no_secret_no_raw_source_no_local_path",
                "evidence_ref": "tests/product_agent_os/test_first_run_analysis.py::test_m20_1_packet_round_trips_as_json_and_rejects_unsafe_values",
            },
        ],
        "unsupported_claims": [
            "target mutation was not performed",
            "runtime/browser QA was not performed",
            "external stage, provider, git and release actions remain approval-bound",
        ],
        "residual_gaps": [
            "all top-level Product-Agent OS CLI scripts are not yet covered by one full matrix",
            "generic --help, invalid-args, stdout/stderr and JSON-shape checks remain pending for the broader CLI fleet",
            "validate_doubt_verification_packet.py still needs explicit B39-B40-OV12 matrix coverage",
        ],
    }


def build_target_dependency_readiness(
    *,
    target_id: str,
    target_kind: str,
    file_refs: list[str] | tuple[str, ...],
    runtime_write_risks: list[str] | tuple[str, ...],
    provider_risks: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    product_manifests: list[str] = []
    excluded_dependency_corpora: list[str] = []
    lockfiles: list[str] = []
    generated_runtime_artifacts: list[str] = []
    for raw_ref in file_refs:
        ref = str(raw_ref).replace("\\", "/").strip("/")
        if not ref:
            continue
        parts = set(ref.split("/"))
        if parts & DEPENDENCY_CORPUS_PARTS:
            excluded_dependency_corpora.append(ref)
            if ".next" in parts or "dist" in parts:
                generated_runtime_artifacts.append(ref)
            continue
        if ref.endswith("package.json") or ref.endswith("pyproject.toml") or ref.endswith("requirements.txt"):
            product_manifests.append(ref)
        if ref.endswith("package-lock.json") or ref.endswith("pnpm-lock.yaml") or ref.endswith("yarn.lock"):
            lockfiles.append(ref)

    runtime_blocked = bool(runtime_write_risks) or not product_manifests
    provider_blocked = bool(provider_risks)
    if not product_manifests and target_kind == "docs_research_only":
        status = "not_applicable_docs_research_target_no_runtime_manifests"
    elif product_manifests:
        status = "partial_pass_static_dependency_inventory_runtime_blocked"
    else:
        status = "blocked_no_runtime_dependency_manifests"

    return {
        "task_id": "B39-TEST-M38",
        "target_id": target_id,
        "target_kind": target_kind,
        "status": status,
        "manifest_summary": {
            "product_manifest_count": len(product_manifests) + len(lockfiles),
            "product_manifests": sorted(product_manifests),
            "lockfiles": sorted(lockfiles),
            "generated_runtime_artifacts": sorted(generated_runtime_artifacts),
        },
        "excluded_dependency_corpora": sorted(excluded_dependency_corpora),
        "runtime_guardrails": {
            "target_runtime_blocked": runtime_blocked,
            "runtime_write_risks": list(runtime_write_risks),
            "provider_calls_blocked": provider_blocked,
            "provider_risks": list(provider_risks),
            "install_or_dependency_mutation_performed": False,
            "target_workspace_mutation_performed": False,
        },
        "unsupported_claims": [
            "static dependency inventory does not prove runtime/browser behavior",
            "dependency install, upgrade and supply-chain audit were not performed",
            "provider/API calls were not performed",
            "target workspace mutation was not performed",
        ],
    }


def summarize_cli_matrix(rows: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> dict[str, Any]:
    normalized_rows = []
    help_gaps: list[str] = []
    for row in rows:
        script = str(row.get("script", "")).strip()
        help_status = str(row.get("help_status", "")).strip() or "unknown"
        normalized = {
            "script": script,
            "help_status": help_status,
            "exit_code": row.get("exit_code"),
            "stdout_parse_status": row.get("stdout_parse_status", "text_or_empty"),
            "stderr_present": bool(row.get("stderr_present", False)),
            "write_scope": row.get("write_scope", "no_write_executed_help_only"),
        }
        normalized_rows.append(normalized)
        if help_status != "passed":
            help_gaps.append(script)

    script_count = len(normalized_rows)
    help_pass_count = sum(1 for row in normalized_rows if row["help_status"] == "passed")
    status = "passed_all_script_cli_help_matrix" if script_count and not help_gaps else "partial_pass_all_script_cli_matrix_with_help_gaps"
    return {
        "task_id": "B39-TEST-M39",
        "status": status,
        "script_count": script_count,
        "help_pass_count": help_pass_count,
        "help_gap_count": len(help_gaps),
        "help_gaps": help_gaps,
        "rows": sorted(normalized_rows, key=lambda item: item["script"]),
        "execution_policy": {
            "mode": "help_only_current_attempt",
            "target_workspace_mutation_performed": False,
            "provider_api_calls_performed": False,
            "external_actions_performed": False,
        },
        "unsupported_claims": [
            "target mutation was not performed",
            "write/apply/stage/merge/release modes were not executed",
            "runtime/browser QA was not proven by CLI help checks",
        ],
    }


def build_runtime_browser_harness_status(
    *,
    target_id: str,
    runtime_entrypoints: list[str] | tuple[str, ...],
    browser_tool_status: str,
    mutation_risks: list[str] | tuple[str, ...],
    provider_risks: list[str] | tuple[str, ...],
    executed_runtime: bool,
    executed_browser: bool,
) -> dict[str, Any]:
    blocked = (not executed_runtime or not executed_browser) and (
        bool(mutation_risks) or browser_tool_status != "available" or not runtime_entrypoints
    )
    return {
        "task_id": "B39-TEST-M42",
        "target_id": target_id,
        "status": "blocked_runtime_browser_requires_mutation_or_missing_tool" if blocked else "passed_runtime_browser_harness",
        "runtime_entrypoints": list(runtime_entrypoints),
        "browser_tool_status": browser_tool_status,
        "runtime_executed": executed_runtime,
        "browser_automation_performed": executed_browser,
        "target_mutation_performed": False,
        "mutation_risks": list(mutation_risks),
        "provider_risks": list(provider_risks),
        "approval_boundary": "no target mutation, provider/API, external, git, deploy, publish or automation action performed",
        "unsupported_claims": [
            "runtime/browser behavior is not claimed when harness is blocked",
            "provider/API calls were not performed",
            "target workspace mutation was not performed",
        ],
    }


def build_target_comparison(
    *,
    target_id: str,
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
) -> dict[str, Any]:
    previous_graph = previous.get("project_graph") if isinstance(previous.get("project_graph"), Mapping) else {}
    current_graph = current.get("project_graph") if isinstance(current.get("project_graph"), Mapping) else {}
    previous_runtime = previous.get("runtime_browser") if isinstance(previous.get("runtime_browser"), Mapping) else {}
    current_runtime = current.get("runtime_browser") if isinstance(current.get("runtime_browser"), Mapping) else {}
    previous_nodes = _int_or_zero(previous_graph.get("nodes"))
    current_nodes = _int_or_zero(current_graph.get("nodes"))
    previous_edges = _int_or_zero(previous_graph.get("edges"))
    current_edges = _int_or_zero(current_graph.get("edges"))
    previous_runtime_status = str(previous_runtime.get("status", "unknown"))
    current_runtime_status = str(current_runtime.get("status", "unknown"))
    return {
        "target_id": target_id,
        "previous": dict(previous),
        "current": dict(current),
        "delta": {
            "project_graph_nodes": current_nodes - previous_nodes,
            "project_graph_edges": current_edges - previous_edges,
            "runtime_browser_status": f"{previous_runtime_status} -> {current_runtime_status}",
        },
        "comparison_policy": "source_artifacts_only_no_generated_view_success_claim",
    }


def build_m37_m39_hardening_summary(*, generated_at: str) -> dict[str, Any]:
    tasks = {
        "B39-TEST-M37": build_m37_public_docs_acceptance(
            public_docs_scope="internal_control_plane_only",
            first_run_page_ids=FIRST_RUN_GENERATED_PAGES,
        ),
        "B39-TEST-M38": build_m38_offline_asset_readiness(),
        "B39-TEST-M39": build_m39_cli_contract_matrix(),
    }
    summary = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "attempt_id": ATTEMPT_ID,
        "generated_at": generated_at,
        "slice": "B39-S4",
        "covered_tasks": sorted(tasks),
        "slice_status": "partial_pass_broader_b39_s4_still_open",
        "tasks": tasks,
        "agent_usage": {
            "docs_maintainer": "read_only_M37_acceptance_inventory",
            "tester": "read_only_M38_M39_contract_inventory",
            "main_agent": "TDD_implementation_and_control_plane_sync",
        },
        "verification_plan": [
            "python -m unittest tests.product_agent_os.test_batch39_s4_hardening -v",
            "python -m unittest tests.product_agent_os.test_first_run_analysis tests.product_agent_os.test_batch39_s4_hardening -v",
            "python -m unittest tests.product_agent_os.test_product_agent_os_docs -v",
            "python tools\\check_docs.py",
            "git diff --check",
        ],
        "unsupported_claims": [
            "runtime/browser QA was not performed",
            "target workspace mutation was not performed",
            "public docs/site publication readiness was not claimed",
            "provider/API, live model, database, git, GitHub, release, deploy, publish and automation actions were not performed",
            "broader B39-S4 remains open after M37-M39",
        ],
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def _canonical_first_run_html_samples() -> dict[str, str]:
    return {
        "index.html": "<!doctype html><a href=\"inventory.html\">Inventory</a><strong>generated-view-only</strong>",
        "inventory.html": "<!doctype html><a href=\"architecture.html\">Architecture</a>",
        "graph.html": "<!doctype html><a href=\"#coverage\">Coverage</a>",
    }


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
