from __future__ import annotations

from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SUMMARY_SCHEMA_VERSION = "batch39_s4_remaining_gates_summary_v1"
ATTEMPT_ID = "B39-S4-REMAINING-GATES-A01"
ALLOWED_STATUSES = [
    "passed_all_script_cli_help_matrix",
    "partial_pass_contract_evidence_only",
    "blocked_expected_mkdocs_unavailable",
    "blocked_expected_runtime_browser_requires_approval",
    "approval_required_live_or_external_surface",
]


def build_remaining_gates_summary(
    *,
    generated_at: str,
    cli_help_pass_count: int,
    cli_help_gap_count: int,
    mkdocs_available: bool,
) -> dict[str, Any]:
    tasks = _task_records(
        cli_help_pass_count=cli_help_pass_count,
        cli_help_gap_count=cli_help_gap_count,
        mkdocs_available=mkdocs_available,
    )
    summary = {
        "schema_version": SUMMARY_SCHEMA_VERSION,
        "attempt_id": ATTEMPT_ID,
        "generated_at": generated_at,
        "slice": "B39-S4",
        "slice_status": "executed_remaining_s4_gates_with_expected_approval_blocks",
        "allowed_statuses": ALLOWED_STATUSES,
        "covered_tasks": sorted(tasks),
        "tasks": tasks,
        "actions_performed": {
            "target_workspace_mutation": False,
            "dependency_install": False,
            "live_server": False,
            "browser_automation": False,
            "provider_api_call": False,
            "mcp_external_call": False,
            "git_stage_commit_push_pr": False,
            "release_deploy_publish": False,
            "active_automation": False,
        },
        "unsupported_claims": [
            "runtime/browser pass is not claimed",
            "release readiness is not claimed",
            "public site acceptance is not claimed while MkDocs is unavailable",
            "security/privacy/compliance output is not a legal or security certification",
            "MCP/Context7 boundary evidence did not call external services",
            "LLM-as-judge calibration did not call live models",
            "go/no-go remains blocked until B39-S5",
        ],
        "safe_next_actions": [
            "fix any new CLI help regressions before mass-user use",
            "run MkDocs in an environment with dependencies installed before public docs/site acceptance",
            "run disposable SOL runtime/browser pilot only after exact approval names write dirs, provider boundary and rollback",
            "enter B39-S5 closure after owner review of expected blocks",
        ],
    }
    summary["summary_digest"] = content_digest(canonical_json(summary))
    return summary


def _task_records(*, cli_help_pass_count: int, cli_help_gap_count: int, mkdocs_available: bool) -> dict[str, dict[str, Any]]:
    cli_status = "passed_all_script_cli_help_matrix" if cli_help_gap_count == 0 else "partial_pass_contract_evidence_only"
    public_docs_status = "partial_pass_contract_evidence_only" if mkdocs_available else "blocked_expected_mkdocs_unavailable"
    return {
        "B39-TEST-M37": _record(
            status=public_docs_status,
            technical_value="keeps public docs/site freshness separate from internal generated orientation artifacts",
            product_value="prevents stale rendered site evidence from being treated as public readiness",
            evidence_refs=["docs/superpowers/specs/batch39-s4-m37-m39-hardening-summary.json", "python -m mkdocs --version"],
            blockers=[] if mkdocs_available else ["mkdocs package unavailable in current Python environment"],
        ),
        "B39-TEST-M39": _record(
            status=cli_status,
            technical_value=f"all-script help matrix now reports {cli_help_pass_count} passed scripts and {cli_help_gap_count} gaps",
            product_value="improves first-use operator ergonomics and prevents accidental path-as-argument failures",
            evidence_refs=["docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json"],
            blockers=[] if cli_help_gap_count == 0 else ["remaining CLI help gaps"],
        ),
        "B39-TEST-M41": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="canonical mutation and rollback stay staged/approval-gated with rollback proof contracts",
            product_value="protects graph users from silent canonical changes while preserving a future mutation path",
            evidence_refs=[
                "tests/product_agent_os/test_project_graph_canonical_mutation.py",
                "tests/product_agent_os/test_project_graph_review_ledger.py",
            ],
            blockers=["no canonical graph mutation approval was granted"],
        ),
        "B39-TEST-M42": _record(
            status="blocked_expected_runtime_browser_requires_approval",
            technical_value="runtime/browser harness records SOL and Neural_Flow blockers instead of a false pass",
            product_value="keeps user trust by requiring a disposable runtime pilot before behavior claims",
            evidence_refs=[
                "docs/superpowers/specs/batch39-s4-full-hardening-sol_0_6-summary.json",
                "docs/superpowers/specs/batch39-s4-full-hardening-neural_flow-summary.json",
            ],
            blockers=["SOL runtime writes target caches/data", "Neural_Flow has no runnable entrypoint", "Playwright unavailable"],
        ),
        "B39-TEST-M43": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="security/privacy/compliance/supply-chain gates are classified and evidence-bound",
            product_value="prevents release or automation claims without secrets, data, CI permission and supply-chain review",
            evidence_refs=[
                "tests/product_agent_os/test_agent_skill_metrics.py",
                "tests/product_agent_os/test_system_file_hygiene.py",
                "docs/superpowers/specs/batch39-s4-full-hardening-sol_0_6-summary.json",
            ],
            blockers=["no external security scan or legal compliance review was requested"],
        ),
        "B39-TEST-M44": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="artifact/workflow template completeness is covered by infrastructure/template tests",
            product_value="keeps generated first-run and handoff artifacts consistent for new users",
            evidence_refs=[
                "tests/product_agent_os/test_infrastructure_templates.py",
                "tests/product_agent_os/test_task_plan_lifecycle.py",
            ],
            blockers=[],
        ),
        "B39-TEST-M45": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="skill/subagent contracts preserve handoff, ownership and no-proof boundaries",
            product_value="makes delegated agent work explainable and reviewable before user-facing claims",
            evidence_refs=[
                "tests/product_agent_os/test_agent_skill_metrics.py",
                "tests/product_agent_os/test_lifecycle_skills.py",
            ],
            blockers=["no live subagent fleet pilot was run in this attempt"],
        ),
        "B39-TEST-M46": _record(
            status="approval_required_live_or_external_surface",
            technical_value="MCP/Context7 boundary remains no-call and approval-gated",
            product_value="prevents external documentation/tool calls from silently changing project evidence",
            evidence_refs=["tests/product_agent_os/test_batch39_inventory.py", "AGENTS.md"],
            blockers=["no MCP/Context7 live call approval was granted"],
        ),
        "B39-TEST-M47": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="onboarding measurement is reduced to time-to-first-safe-action packet requirements",
            product_value="sets up the next owner-feedback pilot without inventing user-value evidence",
            evidence_refs=[
                "docs/superpowers/specs/batch39-s4-full-hardening-comparison.json",
                "RUNLOG.md",
            ],
            blockers=["owner-feedback pilot not yet run"],
        ),
        "B39-TEST-M48": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="cross-platform matrix records Windows PowerShell behavior and command shim risks",
            product_value="keeps setup guidance realistic for Windows users before broader platform claims",
            evidence_refs=["docs/superpowers/specs/batch39-s4-all-script-cli-matrix.json", "AGENTS.md"],
            blockers=["macOS/Linux verification not run in this Windows session"],
        ),
        "B39-TEST-M49": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="source freshness is kept as a current-docs audit gate and stale-evidence blocker",
            product_value="prevents old generated artifacts from becoming decision evidence",
            evidence_refs=["TEST.md", "EVALS.md", "docs/sources/registry.md"],
            blockers=["fresh public docs/site build still blocked by missing MkDocs"],
        ),
        "B39-TEST-M50": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="offline generated HTML remains safety-checked and generated-view-only",
            product_value="keeps generated cockpit/report pages usable as orientation without overstating accessibility proof",
            evidence_refs=[
                "tests/product_agent_os/test_offline_artifact_export.py",
                "tests/product_agent_os/test_agent_skill_metrics_report.py",
                "tests/product_agent_os/test_project_graph_renderer.py",
            ],
            blockers=["no live browser/a11y engine evidence in current run"],
        ),
        "B39-TEST-M51": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="LLM-as-judge calibration is staged as optional metadata and no-live-model evidence",
            product_value="keeps subjective scoring useful without adding unapproved model calls or fake precision",
            evidence_refs=["tests/product_agent_os/test_agent_skill_metrics.py", "EVALS.md"],
            blockers=["live model judge not approved or run"],
        ),
        "B39-TEST-M52": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="data retention/cache/stage cleanup proof is scoped to generated artifact boundaries",
            product_value="reduces operator risk from retained packets, temp output and stale baselines",
            evidence_refs=[
                "tests/product_agent_os/test_stage_manifest.py",
                "tests/product_agent_os/test_offline_artifact_export.py",
            ],
            blockers=["no destructive cleanup was performed"],
        ),
        "B39-TEST-M53": _record(
            status="partial_pass_contract_evidence_only",
            technical_value="incident/recovery drills cover malformed packets, redaction leaks, bad manifests and stale evidence classes",
            product_value="gives operators a recovery path before mass-user rollout",
            evidence_refs=[
                "tests/product_agent_os/test_first_run_analysis.py",
                "tests/product_agent_os/test_doubt_verification.py",
                "tests/product_agent_os/test_stage_manifest.py",
            ],
            blockers=[],
        ),
        "B39-TEST-M54": _record(
            status="approval_required_live_or_external_surface",
            technical_value="release/distribution governance remains manual_only/not_promoted without external writes",
            product_value="prevents accidental release, deployment, marketplace, package registry or automation promotion",
            evidence_refs=["prod_test.md", "RUNLOG.md", "EVALS.md"],
            blockers=["B39-S5 go/no-go and owner approval still pending"],
        ),
    }


def _record(
    *,
    status: str,
    technical_value: str,
    product_value: str,
    evidence_refs: list[str],
    blockers: list[str],
) -> dict[str, Any]:
    return {
        "status": status,
        "technical_value": technical_value,
        "product_value": product_value,
        "evidence_refs": evidence_refs,
        "blockers": blockers,
        "target_mutation_performed": False,
        "external_action_performed": False,
        "readiness_claim": "not_claimed",
        "promotion_status": "manual_only_not_promoted",
    }
