from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import analyze_workspace  # noqa: E402
from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402
from product_agent_os.infrastructure import InfrastructureError, render_infrastructure_plan, stage_infrastructure  # noqa: E402
from product_agent_os.merge_infrastructure import (  # noqa: E402
    ROLLBACK_MANIFEST_NAME,
    MergeInfrastructureError,
    apply_merge_plan,
    build_merge_plan,
)
from product_agent_os.source_policy import validate_source_policy  # noqa: E402
from product_agent_os.stage_manifest import MANIFEST_NAME, content_digest, workspace_audit_digest  # noqa: E402
from product_agent_os.transcript_evals import evaluate_transcript_sessions  # noqa: E402
from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.guards import validate_automation_boundary, validate_codex_handoff  # noqa: E402
from codex_runtime_runner.redaction import redact_text, validate_redaction  # noqa: E402


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PLUGIN_ROOT / "assets" / "fixtures"
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates"
PLAN_QUALITY_TERMS = (
    "no-placeholder",
    "plan quality gate",
    "exact files",
    "owned files",
    "forbidden files",
    "exact commands",
    "expected outputs",
    "rollback",
    "evidence owner",
    "placeholder scan",
    "mechanical_change",
    "plan repair",
    "stop before build",
    "vague validation",
    "repeated-by-reference",
)
ACCEPTANCE_SCENARIO_TERMS = (
    "acceptance scenarios",
    "atdd",
    "bdd",
    "requirement -> scenario -> check -> evidence owner",
    "given",
    "when",
    "then",
    "equivalent behavior format",
    "business rule",
    "edge case",
    "non-goal",
    "explicit gap",
    "evidence owner",
)
DOMAIN_MODEL_GATE_TERMS = (
    "domain_model_when_complex_domain",
    "domain-modeling.md",
    "complex backend",
    "workflow",
    "enterprise",
    "data-heavy",
    "bounded context",
    "ubiquitous language",
    "invariant",
    "accepted gap",
    "simple crud",
    "simple mvp",
    "missing domain model for complex domain",
)
BOUNDED_CONTEXT_TRACE_TERMS = (
    "bounded_context_architecture_boundary_trace",
    "context-to-boundary traceability",
    "architecture-overview.md",
    "architecture boundary",
    "boundary id",
    "mapped bounded context",
    "domain model context",
    "every bounded context maps to architecture boundary",
    "missing bounded context architecture boundary trace",
)
UBIQUITOUS_LANGUAGE_TRACE_TERMS = (
    "ubiquitous_language_traceability",
    "term-to-requirement",
    "requirement or source",
    "api/event/contract",
    "ui label",
    "code module or owner",
    "domain expert review",
    "every ubiquitous language term",
    "accepted gap",
    "missing ubiquitous language traceability",
)
METRIC_HARDENING_TERMS = (
    "metric_hardening_when_product_behavior_changes",
    "metric-spec.md",
    "north star",
    "input metric",
    "counter-metric",
    "proxy metric",
    "guardrail",
    "qualitative review",
    "privacy classification",
    "retention period",
    "data minimization",
    "owner signoff",
    "post-release review evidence",
    "do not claim success",
)
COMPLETION_EVIDENCE_TERMS = (
    "evidence_before_completion",
    "evidence-before-completion",
    "ready claim",
    "completed claim",
    "fixed claim",
    "works claim",
    "release claim",
    "current command evidence",
    "current eval evidence",
    "current runtime evidence",
    "inspection-only",
    "explicit test gap",
    "unsupported completion claim",
    "completion claim without current evidence",
)
DOCS_TOOLING_SELECTOR_TERMS = (
    "docs_tooling_selector",
    "docs-tooling-decision.md",
    "docs_as_code_impact",
    "not_applicable",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
    "selected tools",
    "rejected tools",
    "no forced install",
    "no ci activation without approval",
    "hosted docs approval",
    "db introspection approval",
    "docs-light",
    "internal-only",
    "evidence owner",
    "maintenance owner",
)
TRANSCRIPT_SESSION_EVAL_TERMS = (
    "evaluate_transcript_sessions",
    "transcript/session eval runner",
    "product-agent-os-synthetic-sessions.json",
    "behavioral_case",
    "expected_terms",
    "forbidden_terms",
    "missing_expected_terms",
    "forbidden_terms_present",
    "privacy_errors",
)
STANDARDS_TRIGGER_TERMS = (
    "standards_trigger_policy",
    "adr trigger policy",
    "architecture boundary",
    "api contract",
    "storage",
    "auth/security",
    "irreversible migration",
    "automation activation",
    "c4 system context",
    "c4 container",
    "component/code only when useful",
    "arc42",
    "architecture goals",
    "constraints",
    "quality attributes",
    "openapi source of truth",
    "swagger ui",
    "asyncapi",
    "channel",
    "message",
    "payload schema",
    "producer",
    "consumer",
    "ordering",
    "idempotency",
    "compatibility check",
    "semver impact",
    "major",
    "minor",
    "patch",
    "keep a changelog",
    "added",
    "changed",
    "deprecated",
    "removed",
    "fixed",
    "security",
    "governance-proposal.md",
    "codeowners status",
    "github actions",
    "least privilege",
    "workflow names",
    "commands",
    "permissions",
    "triggers",
    "owners",
    "proposal_staged",
    "approval_required",
    "no external activation without approval",
    "no forced external activation",
)
TRANSCRIPT_FIXTURE = (
    PLUGIN_ROOT
    / "assets"
    / "eval-fixtures"
    / "transcripts"
    / "product-agent-os-synthetic-sessions.json"
)
CONDITIONAL_READINESS_GATE_IDS = (
    "acceptance_scenarios_when_behavior_changes",
    "domain_model_when_complex_domain",
    "fsd_boundary_when_ui_grows",
    "ai_eval_spec_when_ai_behavior_changes",
    "docs_tooling_decision",
    "contract_docs_when_api_or_event_changes",
    "db_docs_when_schema_changes",
    "release_version_impact_when_public_contract_changes",
    "reproduction_evidence_when_bug_rescue",
    "approval_before_greenfield_scaffold",
    "integration_catalog_when_external_systems_exist",
    "ownership_split_when_parallel_agents_used",
    "pr_risk_review_when_review_mode",
    "onboarding_map_when_legacy_repo",
    "migration_plan_when_contract_or_data_changes",
    "security_review_when_sensitive_surface",
    "platform_runtime_check_when_native_or_desktop",
    "ci_failure_evidence_when_ci_stabilization",
    "release_readiness_when_distribution_changes",
    "plugin_success_metric_for_major_workflow",
    "root_cause_before_bug_fix",
    "no_placeholder_plan_when_plan_ready",
    "two_stage_review_when_risky_or_parallel",
    "fresh_context_handoff_when_subagents_used",
    "behavioral_eval_when_new_route_added",
    "codex_only_compatibility_when_plugin_packaging_changes",
    "finish_options_when_release_ready",
    "standards_trigger_policy_when_architecture_api_release_or_governance_changes",
)
READINESS_STATUSES = (
    "not_applicable",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "proposal_staged",
    "explicit_gap_accepted",
    "approval_required",
)
CONDITIONAL_READINESS_TERMS = (
    "conditional readiness gates",
    "readiness_statuses",
    "applicable_missing",
    "present_unverified",
    "present_verified",
    "not_applicable",
    "explicit_gap_accepted",
    "approval_required",
    "detection alone",
    "applicability reason",
    "owner",
    "residual risk",
)


def _failed_result(fixture: str, reason: str) -> dict[str, Any]:
    return {
        "fixture": fixture,
        "ok": False,
        "profile": "",
        "risks": [reason],
        "renderer_status": "",
        "merge_status": "",
        "source_policy_status": "",
        "automation_status": "",
        "rollback_status": "",
        "failure_log_regression_status": "",
        "codex_runtime_runner_status": "",
        "codex_runtime_runner_checks": {},
        "renderer_file_count": 0,
        "renderer_actions": {},
        "expected_checks": {},
        "evidence": {},
    }


def evaluate_fixture(path: Path) -> dict[str, Any]:
    try:
        audit = analyze_workspace(path)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        return _failed_result(path.name, str(exc))
    except Exception as exc:
        return _failed_result(path.name, f"discovery failed: {type(exc).__name__}: {exc}")

    profile = audit.get("complexity_profile", {})
    profile_name = profile.get("name", "") if isinstance(profile, dict) else ""
    risks = audit.get("risks", [])
    try:
        rendered = render_infrastructure_plan(path)
        renderer_status = str(rendered["infrastructure_plan"]["status"])
        merge_status = renderer_status
        renderer_files = rendered["rendered_artifacts"]["files"]
        renderer_validation = rendered["rendered_artifacts"]["validation"]
        renderer_actions = _renderer_actions(renderer_files)
        expected_checks = _expected_checks(path.name, audit, rendered, renderer_actions)
        source_policy_status = _source_policy_status(path)
        automation_status = _automation_status(path)
        behavior = _track_four_behavior(path)
        rollback_status = behavior["rollback_status"] or _rollback_status(path)
        failure_log_status, failure_log_checks = _failure_log_status(path)
        codex_runtime_runner_status, codex_runtime_runner_checks = _codex_runtime_runner_eval(path)
        expected_checks.update(failure_log_checks)
        expected_checks.update(codex_runtime_runner_checks)
        expected_checks.update(
            _track_four_expected_checks(
                path.name,
                source_policy_status,
                automation_status,
                rollback_status,
                failure_log_status,
            )
        )
        expected_checks.update(behavior["expected_checks"])
        merge_status = behavior["merge_status"] or renderer_status
        evidence = _evidence(path, source_policy_status, automation_status, behavior)
        renderer_ok = (
            bool(renderer_validation.get("ok"))
            and renderer_status in {"needs_approval", "blocked"}
            and all(expected_checks.values())
        )
    except InfrastructureError as exc:
        renderer_status = ""
        merge_status = ""
        source_policy_status = ""
        automation_status = ""
        rollback_status = ""
        failure_log_status = ""
        codex_runtime_runner_status = ""
        codex_runtime_runner_checks = {}
        renderer_files = []
        renderer_actions = {}
        expected_checks = {}
        evidence = {}
        renderer_ok = False
        risks = risks if isinstance(risks, list) else ["invalid discovery risks"]
        risks = [*risks, f"renderer failed: {exc}"]
    except Exception as exc:
        renderer_status = ""
        merge_status = ""
        source_policy_status = ""
        automation_status = ""
        rollback_status = ""
        failure_log_status = ""
        renderer_files = []
        renderer_actions = {}
        expected_checks = {}
        evidence = {}
        renderer_ok = False
        risks = risks if isinstance(risks, list) else ["invalid discovery risks"]
        risks = [*risks, f"renderer failed: {type(exc).__name__}: {exc}"]

    ok = bool(audit.get("workspace")) and bool(profile_name) and isinstance(risks, list) and renderer_ok
    return {
        "fixture": path.name,
        "ok": ok,
        "profile": profile_name,
        "risks": risks if isinstance(risks, list) else ["invalid discovery risks"],
        "renderer_status": renderer_status,
        "merge_status": merge_status,
        "source_policy_status": source_policy_status,
        "automation_status": automation_status,
        "rollback_status": rollback_status,
        "failure_log_regression_status": failure_log_status,
        "codex_runtime_runner_status": codex_runtime_runner_status,
        "codex_runtime_runner_checks": codex_runtime_runner_checks,
        "renderer_file_count": len(renderer_files),
        "renderer_actions": renderer_actions,
        "expected_checks": expected_checks,
        "evidence": evidence,
    }


def _renderer_actions(files: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(item.get("target_path")): str(item.get("action"))
        for item in files
        if isinstance(item, dict) and item.get("target_path")
    }


def _expected_checks(
    fixture: str,
    audit: dict[str, Any],
    rendered: dict[str, Any],
    actions: dict[str, str],
) -> dict[str, bool]:
    plan = rendered.get("infrastructure_plan", {})
    warnings = " ".join(plan.get("warnings", [])) if isinstance(plan, dict) else ""
    blocked = " ".join(plan.get("blocked", [])) if isinstance(plan, dict) else ""
    payload = json.dumps(rendered, sort_keys=True).lower()
    checks: dict[str, bool] = {}
    if fixture in {"empty-repo", "node-app", "python-app"}:
        checks["agents_md_create"] = actions.get("AGENTS.md") == "create"
        checks["config_create"] = actions.get(".codex/config.toml") == "create"
    if fixture == "python-app":
        checks["plan_quality_contract_present"] = _plan_quality_contract_present()
        checks["acceptance_scenarios_contract_present"] = _acceptance_scenarios_contract_present()
        checks["domain_model_gate_contract_present"] = _domain_model_gate_contract_present()
        checks["bounded_context_trace_contract_present"] = _bounded_context_trace_contract_present()
        checks["ubiquitous_language_traceability_contract_present"] = (
            _ubiquitous_language_traceability_contract_present()
        )
        checks["metric_hardening_contract_present"] = _metric_hardening_contract_present()
        checks["completion_evidence_contract_present"] = _completion_evidence_contract_present()
        checks["docs_tooling_selector_contract_present"] = _docs_tooling_selector_contract_present()
        checks["conditional_readiness_gates_contract_present"] = (
            _conditional_readiness_gates_contract_present()
        )
        checks["transcript_session_eval_runner_contract_present"] = (
            _transcript_session_eval_runner_contract_present()
        )
        checks["standards_trigger_contract_present"] = _standards_trigger_contract_present()
        checks["methodology_applicability_contract_present"] = (
            _methodology_applicability_contract_present(audit)
        )
    if fixture in {"existing-codex-config", "unsafe-write-request"}:
        checks["config_leave_unchanged"] = actions.get(".codex/config.toml") == "leave_unchanged"
        checks["agents_md_leave_unchanged"] = actions.get("AGENTS.md") == "leave_unchanged"
    if fixture == "duplicate-managed-section":
        checks["duplicate_markers_blocked"] = (
            actions.get("AGENTS.md") == "blocked" and "duplicate managed section" in blocked
        )
    if fixture == "monorepo":
        checks["worktree_ownership_warning"] = "worktree ownership" in warnings
    if fixture == "docs-source-conflict":
        checks["source_registry_warning"] = "source registry" in warnings
    if fixture == "failed-verification":
        checks["failed_verification_warning"] = (
            "failed verification evidence" in warnings and "checks passed" not in payload
        )
    usage_mode = audit.get("usage_mode", {})
    primary_mode = usage_mode.get("primary") if isinstance(usage_mode, dict) else ""
    expected_usage_modes = {
        "empty-repo": "greenfield_idea",
        "failed-verification": "bug_rescue",
        "monorepo": "complex_system_acceleration",
        "docs-repo": "docs_only",
        "node-app": "standard_feature",
        "legacy-undocumented-repo": "legacy_onboarding",
        "api-migration-repo": "api_migration",
        "rag-quality-regression": "ai_eval_regression",
        "native-mobile-permissions": "native_mobile_feature",
        "desktop-local-indexer": "desktop_local_first",
        "data-migration-pii": "data_migration",
        "security-auth-payment": "security_sensitive_change",
        "ci-flaky-tests": "ci_stabilization",
        "package-release": "release_packaging",
    }
    if fixture in expected_usage_modes:
        expected_mode = expected_usage_modes[fixture]
        checks[f"usage_mode_{expected_mode}"] = primary_mode == expected_mode
    signals = audit.get("methodology_signals", {})
    methodology_gaps = audit.get("methodology_gaps", [])
    route_methodology_signals = _route_methodology_signals(audit)
    if fixture == "backend-no-fsd":
        checks["fsd_structure_not_detected_for_backend"] = (
            isinstance(signals, dict)
            and signals.get("fsd_structure") is False
            and "fsd_structure" not in route_methodology_signals
            and primary_mode == "standard_feature"
        )
    if fixture == "native-no-fsd":
        checks["fsd_structure_not_detected_for_native"] = (
            isinstance(signals, dict)
            and signals.get("fsd_structure") is False
            and "fsd_structure" not in route_methodology_signals
            and primary_mode == "native_mobile_feature"
        )
    if fixture == "simple-crud-no-ddd":
        checks["domain_model_not_forced_for_simple_crud"] = (
            isinstance(signals, dict)
            and signals.get("domain_model") is False
            and isinstance(methodology_gaps, list)
            and "missing domain model for complex domain" not in methodology_gaps
            and primary_mode == "standard_feature"
        )
    if fixture == "docs-light-no-portal":
        checks["docs_light_does_not_select_heavy_portal"] = _docs_light_no_portal_check(audit)
    if fixture == "hosted-docs-approval":
        checks["hosted_docs_and_db_introspection_require_approval"] = _hosted_docs_approval_check(audit)
    return checks


def _route_methodology_signals(audit: dict[str, Any]) -> list[str]:
    route_inputs = audit.get("route_inputs", {})
    if not isinstance(route_inputs, dict):
        return []
    workspace_signals = route_inputs.get("workspace_signals", {})
    if not isinstance(workspace_signals, dict):
        return []
    methodology_signals = workspace_signals.get("methodology_signals", [])
    return methodology_signals if isinstance(methodology_signals, list) else []


def _docs_light_no_portal_check(audit: dict[str, Any]) -> bool:
    decision = audit.get("docs_tooling_decision", {})
    if not isinstance(decision, dict):
        return False
    impact = decision.get("docs_as_code_impact", {})
    tool_statuses = decision.get("tool_statuses", {})
    selected_tools = decision.get("selected_tools", [])
    approval_required = decision.get("approval_required", [])
    docs_portal = tool_statuses.get("docs_portal", {}) if isinstance(tool_statuses, dict) else {}
    heavy_portal_tools = {"MkDocs", "Docusaurus", "Sphinx", "Antora", "Read the Docs"}
    return (
        isinstance(impact, dict)
        and impact.get("status") == "not_applicable"
        and isinstance(docs_portal, dict)
        and docs_portal.get("status") == "not_applicable"
        and isinstance(selected_tools, list)
        and not heavy_portal_tools.intersection(selected_tools)
        and approval_required == []
    )


def _hosted_docs_approval_check(audit: dict[str, Any]) -> bool:
    decision = audit.get("docs_tooling_decision", {})
    if not isinstance(decision, dict):
        return False
    impact = decision.get("docs_as_code_impact", {})
    tool_statuses = decision.get("tool_statuses", {})
    approval_required = decision.get("approval_required", [])
    hosted_docs = tool_statuses.get("hosted_docs", {}) if isinstance(tool_statuses, dict) else {}
    db_introspection = tool_statuses.get("db_introspection", {}) if isinstance(tool_statuses, dict) else {}
    return (
        isinstance(impact, dict)
        and impact.get("status") == "approval_required"
        and isinstance(approval_required, list)
        and "hosted docs" in approval_required
        and "db introspection" in approval_required
        and isinstance(hosted_docs, dict)
        and hosted_docs.get("status") == "approval_required"
        and isinstance(db_introspection, dict)
        and db_introspection.get("status") == "approval_required"
    )


def _methodology_applicability_contract_present(audit: dict[str, Any]) -> bool:
    applicability = audit.get("methodology_applicability", {})
    expected_keys = {
        "architecture_boundary",
        "test_eval_first_evidence",
        "docs_as_code_ownership",
        "product_measurement",
        "domain_model_when_complex_domain",
        "fsd_structure_when_ui_architecture_applies",
        "docs_tooling_decision",
        "standards_trigger_policy",
    }
    allowed_statuses = {
        "not_applicable",
        "applicable_missing",
        "present_unverified",
        "present_verified",
        "proposal_staged",
        "explicit_gap_accepted",
        "approval_required",
    }
    if not isinstance(applicability, dict) or set(applicability) != expected_keys:
        return False
    for packet in applicability.values():
        if not isinstance(packet, dict):
            return False
        if set(packet) != {
            "status",
            "applies_when",
            "reason",
            "evidence",
            "required_evidence",
            "owner",
            "residual_risk",
        }:
            return False
        if packet["status"] not in allowed_statuses:
            return False
        if not isinstance(packet["evidence"], list) or not isinstance(packet["required_evidence"], list):
            return False
        if not packet["owner"] or not packet["residual_risk"]:
            return False
    return True


def _plan_quality_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "workflows" / "build-slice.md",
        TEMPLATE_ROOT / "artifact-templates" / "plan-quality-check.md",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in PLAN_QUALITY_TERMS)


def _acceptance_scenarios_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "workflows" / "development-standards.md",
        TEMPLATE_ROOT / "artifact-templates" / "acceptance-scenarios.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in ACCEPTANCE_SCENARIO_TERMS)


def _domain_model_gate_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "domain-modeling.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in DOMAIN_MODEL_GATE_TERMS)


def _bounded_context_trace_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "domain-modeling.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-overview.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in BOUNDED_CONTEXT_TRACE_TERMS)


def _ubiquitous_language_traceability_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "domain-modeling.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in UBIQUITOUS_LANGUAGE_TRACE_TERMS)


def _metric_hardening_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "metric-spec.md",
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in METRIC_HARDENING_TERMS)


def _completion_evidence_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "workflows" / "development-standards.md",
        TEMPLATE_ROOT / "control-plane" / "AGENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "agent-team-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "automation-promoter" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in COMPLETION_EVIDENCE_TERMS)


def _docs_tooling_selector_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "docs-tooling-decision.md",
        TEMPLATE_ROOT / "workflows" / "documentation-system.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in DOCS_TOOLING_SELECTOR_TERMS)


def _transcript_session_eval_runner_contract_present() -> bool:
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "transcript_evals.py",
        PLUGIN_ROOT / "scripts" / "run_transcript_eval.py",
        TRANSCRIPT_FIXTURE,
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT.parents[1] / "docs" / "product-agent-os" / "behavioral-evals.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    report = evaluate_transcript_sessions(
        TRANSCRIPT_FIXTURE,
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    )
    return bool(report.get("ok")) and all(term in payload for term in TRANSCRIPT_SESSION_EVAL_TERMS)


def _standards_trigger_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "artifact-templates" / "adr.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-overview.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "governance-proposal.md",
        TEMPLATE_ROOT / "workflows" / "documentation-system.md",
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "control-plane" / "AGENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in STANDARDS_TRIGGER_TERMS)


def _conditional_readiness_gates_contract_present() -> bool:
    readiness_path = TEMPLATE_ROOT / "evals" / "project-readiness.json"
    data = json.loads(readiness_path.read_text(encoding="utf-8"))
    expected = data["cases"][0]["expected"]
    gates = expected.get("conditional_readiness_gates", {})
    if tuple(expected.get("readiness_statuses", [])) != READINESS_STATUSES:
        return False
    if set(gates) != set(CONDITIONAL_READINESS_GATE_IDS):
        return False
    for gate in gates.values():
        if set(gate) != {
            "applies_when",
            "pass_condition",
            "accepted_gap",
            "required_evidence",
            "owner",
            "residual_risk",
        }:
            return False
        if not gate["required_evidence"] or "explicit_gap_accepted" not in gate["accepted_gap"]:
            return False

    paths = [
        readiness_path,
        TEMPLATE_ROOT / "control-plane" / "AGENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(term in payload for term in CONDITIONAL_READINESS_TERMS)


def _track_four_expected_checks(
    fixture: str,
    source_policy_status: str,
    automation_status: str,
    rollback_status: str,
    failure_log_status: str,
) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    if fixture == "source-policy-conflict":
        checks["source_policy_status_needs_review"] = source_policy_status == "needs_review"
    if fixture == "automation-candidate-valid":
        checks["automation_status_ready_for_manual_approval"] = (
            automation_status == "ready_for_manual_approval"
        )
    if fixture == "automation-candidate-invalid":
        checks["automation_status_blocked"] = automation_status == "blocked"
    if fixture == "failure-log-regression":
        checks["failure_log_regression_status_ready"] = failure_log_status == "ready"
    if fixture == "rollback-required":
        checks["rollback_status_required"] = rollback_status == "required"
    return checks


def _source_policy_status(path: Path) -> str:
    report = validate_source_policy(path)
    return str(report["status"])


def _automation_status(path: Path) -> str:
    candidates = sorted(path.rglob("automation-candidate.md"))
    if not candidates:
        return "not_applicable"
    report = validate_automation_candidate(candidates[0])
    return str(report["status"])


def _rollback_status(path: Path) -> str:
    runlog = path / "RUNLOG.md"
    if not runlog.exists():
        return "not_exercised"
    text = runlog.read_text(encoding="utf-8")
    if "rollback_manifest_visible" in text or "rollback-required" in text:
        return "required"
    return "not_exercised"


def _track_four_behavior(path: Path) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    commands: list[str] = []
    reports: list[dict[str, str]] = []
    merge_status = ""
    rollback_status = ""

    if path.name == "stale-merge-plan":
        merge_status, check = _exercise_stale_merge_plan(path)
        checks["stale_digest_blocked"] = check
        commands.extend(["stage_infrastructure", "build_merge_plan"])
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "path-traversal-stage":
        merge_status, check = _exercise_path_traversal_stage()
        checks["path_traversal_blocked"] = check
        commands.append("build_merge_plan")
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "symlink-escape":
        merge_status, check = _exercise_symlink_escape()
        checks["symlink_escape_blocked"] = check
        commands.append("build_merge_plan")
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "hook-activation-unapproved":
        merge_status, check = _exercise_unapproved_hook_activation()
        checks["hooks_unapproved_companion_only"] = check
        commands.extend(["build_merge_plan", "apply_merge_plan"])
        reports.append({"name": "hook_activation", "status": merge_status})
    elif path.name == "hook-activation-approved":
        merge_status, rollback_status, hook_check, rollback_check = _exercise_approved_hook_activation()
        checks["hooks_approved_apply"] = hook_check
        checks["rollback_manifest_visible"] = rollback_check
        commands.extend(["build_merge_plan", "apply_merge_plan"])
        reports.append({"name": "hook_activation", "status": merge_status})

    return {
        "expected_checks": checks,
        "merge_status": merge_status,
        "rollback_status": rollback_status,
        "commands": commands,
        "reports": reports,
    }


def _exercise_stale_merge_plan(path: Path) -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        shutil.copytree(path, workspace)
        stage_infrastructure(workspace, stage_root)
        (workspace / "AGENTS.md").write_text("# Added after staging\n", encoding="utf-8")
        plan = build_merge_plan(workspace, stage_root)
    blocked = " ".join(plan.get("blocked", []))
    return str(plan.get("status", "")), plan.get("status") == "blocked" and "workspace audit digest" in blocked


def _exercise_path_traversal_stage() -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, "AGENTS.md", "content\n")
        _write_stage_manifest(workspace, stage_root, [{"target_path": "../AGENTS.md", "staged_path": "AGENTS.md"}])
        try:
            build_merge_plan(workspace, stage_root)
        except MergeInfrastructureError as exc:
            return "blocked", "escapes" in str(exc)
    return "needs_approval", False


def _exercise_symlink_escape() -> tuple[str, bool]:
    if not hasattr(os, "symlink"):
        return "skipped_unsupported", True
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        outside = Path(tmp) / "outside.md"
        workspace.mkdir()
        stage_root.mkdir()
        outside.write_text("outside\n", encoding="utf-8")
        try:
            os.symlink(outside, workspace / "AGENTS.md")
        except (OSError, NotImplementedError):
            return "skipped_unsupported", True
        _write_stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": "AGENTS.md", "staged_path": "AGENTS.md", "managed_section": "project-rules"}],
        )
        plan = build_merge_plan(workspace, stage_root)
    blocked = " ".join(plan.get("blocked", []))
    return str(plan.get("status", "")), plan.get("status") == "blocked" and "symlink" in blocked


def _exercise_unapproved_hook_activation() -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": ".codex/hooks/hooks.json", "staged_path": ".codex/hooks/hooks.json"}],
        )
        plan = build_merge_plan(workspace, stage_root)
        approval = _write_approval(stage_root, plan["id"], [], [])
        result = apply_merge_plan(workspace, stage_root, approval)
        hooks_path = workspace / ".codex" / "hooks" / "hooks.json"
    decision = plan["decisions"][0]
    return (
        str(result.get("status", "")),
        decision.get("action") == "companion_only" and not hooks_path.exists(),
    )


def _exercise_approved_hook_activation() -> tuple[str, str, bool, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": ".codex/hooks/hooks.json", "staged_path": ".codex/hooks/hooks.json"}],
        )
        plan = build_merge_plan(workspace, stage_root)
        approval = _write_approval(
            stage_root,
            plan["id"],
            [".codex/hooks/hooks.json"],
            ["create_file"],
            enable_hooks=True,
        )
        result = apply_merge_plan(workspace, stage_root, approval)
        hooks_path = workspace / ".codex" / "hooks" / "hooks.json"
        rollback_path = stage_root / ROLLBACK_MANIFEST_NAME
        hook_check = result.get("status") == "applied" and hooks_path.exists()
        rollback_check = rollback_path.exists() and rollback_path.is_file()
    return str(result.get("status", "")), "available" if rollback_check else "missing", hook_check, rollback_check


def _write_stage_file(stage_root: Path, relative_path: str, content: str) -> None:
    path = stage_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_stage_manifest(workspace: Path, stage_root: Path, files: list[dict[str, str]]) -> None:
    manifest_files: list[dict[str, str]] = []
    target_paths: list[str] = []
    for item in files:
        target_path = item["target_path"]
        staged_path = item["staged_path"]
        target_paths.append(target_path)
        staged = stage_root / staged_path
        manifest_files.append(
            {
                "target_path": target_path,
                "staged_path": staged_path,
                "action": item.get("action", "create"),
                "write_policy": item.get("write_policy", "staged_only"),
                "digest": content_digest(staged.read_bytes()),
                "managed_section": item.get("managed_section", ""),
            }
        )
    manifest = {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "workspace": str(workspace.resolve()),
        "generated_at": "2026-05-14T00:00:00+00:00",
        "workspace_audit_digest": workspace_audit_digest(workspace, target_paths),
        "infrastructure_plan_digest": content_digest("fixture\n"),
        "validation": {"ok": True, "checks": [], "errors": {}},
        "files": manifest_files,
    }
    (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _write_approval(
    stage_root: Path,
    plan_id: str,
    approved_targets: list[str],
    approved_actions: list[str],
    *,
    enable_hooks: bool = False,
) -> Path:
    path = stage_root / "approval.json"
    payload = {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": plan_id,
            "approved_by": "fixture-eval",
            "approved_at": "2026-05-14T00:00:00+00:00",
            "approved_targets": approved_targets,
            "approved_actions": approved_actions,
            "accepted_risks": ["synthetic fixture workspace write"],
            "denied_targets": [],
            "notes": "fixture eval approval",
            "enable_hooks": enable_hooks,
            "approved_hook_events": ["SessionStart"] if enable_hooks else [],
            "blocking_hooks": ["PreToolUse"] if enable_hooks else [],
            "hook_rollback": "remove hooks.json when rollback digest matches" if enable_hooks else "",
        }
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _managed_doc(section_id: str, body: str) -> str:
    return (
        "# Generated\n\n"
        f"<!-- product-agent-os:start {section_id} -->\n"
        f"{body}\n"
        f"<!-- product-agent-os:end {section_id} -->\n"
    )


def _failure_log_status(path: Path) -> tuple[str, dict[str, bool]]:
    runlog = path / "RUNLOG.md"
    if not runlog.exists():
        return "not_applicable", {}
    text = runlog.read_text(encoding="utf-8")
    if "expected_regression_fixture:" not in text and "expected_check:" not in text:
        return "not_applicable", {}
    checks = {
        "failure_log_regression_visible": (
            "expected_regression_fixture:" in text and "expected_check:" in text
        )
    }
    return "ready" if all(checks.values()) else "needs_review", checks


def _codex_runtime_runner_eval(path: Path) -> tuple[str, dict[str, bool]]:
    if not path.name.startswith("codex-runner-"):
        return "not_applicable", {}

    checks: dict[str, bool] = {"contract_mode_offline": True}
    if path.name == "codex-runner-ready":
        result = run_contract(path)
        checks["route_matches_lifecycle_state"] = (
            result["lifecycle_state"] == "quality_gate"
            and result["route_packet"]["recommended_skill"] == "risk-reviewer"
        )
        return str(result["status"]), checks

    if path.name == "codex-runner-missing-context":
        result = run_contract(path)
        checks["missing_context_detected"] = result["status"] == "needs_context"
        return str(result["status"]), checks

    if path.name == "codex-runner-approval-required":
        result = run_contract(path, allow_subagents=True)
        checks["approval_required_for_writes"] = result["status"] == "needs_approval"
        return str(result["status"]), checks

    if path.name == "codex-runner-handoff-incomplete":
        errors = validate_codex_handoff(
            {
                "lifecycle_state": "quality_gate",
                "constraints": [],
                "verification_evidence": [],
            }
        )
        checks["handoff_incomplete_blocked"] = (
            "constraints:empty" in errors and "verification_evidence:empty" in errors
        )
        return "blocked", checks

    if path.name == "codex-runner-automation-blocked":
        errors = validate_automation_boundary((path / "RUNLOG.md").read_text(encoding="utf-8"))
        checks["active_automation_blocked"] = "automation:active_request_blocked" in errors
        return "blocked", checks

    if path.name == "codex-runner-secret-redaction":
        redacted, _report = redact_text("TOKEN=fixture-secret\nC:\\Users\\person\\workspace")
        checks["secret_redaction_enforced"] = validate_redaction(redacted) == []
        return "blocked", checks

    return "not_applicable", {}


def _evidence(
    path: Path,
    source_policy_status: str,
    automation_status: str,
    behavior: dict[str, Any],
) -> dict[str, Any]:
    return {
        "files_inspected": sorted(str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()),
        "commands": [
            "render_infrastructure_plan",
            "validate_source_policy",
            "validate_automation_candidate",
            *behavior["commands"],
        ],
        "reports": [
            {"name": "source_policy", "status": source_policy_status},
            {"name": "automation_policy", "status": automation_status},
            *behavior["reports"],
        ],
    }


def evaluate_all(fixtures_root: Path = FIXTURES) -> list[dict[str, Any]]:
    if not fixtures_root.exists():
        return [_failed_result(fixtures_root.name, f"fixture directory does not exist: {fixtures_root}")]
    if not fixtures_root.is_dir():
        return [_failed_result(fixtures_root.name, f"fixture path is not a directory: {fixtures_root}")]

    return [
        evaluate_fixture(path)
        for path in sorted(fixtures_root.iterdir(), key=lambda item: item.name)
        if path.is_dir()
    ]


def main() -> int:
    results = evaluate_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if results and all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
