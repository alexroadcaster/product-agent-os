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
from product_agent_os.agent_skill_metrics import (  # noqa: E402
    build_scorecard_ledger_record,
    enforce_trace_data_classification_gate,
    render_scorecard_ledger_markdown,
)
from product_agent_os.agent_skill_metrics_report import (  # noqa: E402
    METRICS_REPORT_TARGET,
    render_agent_skill_metrics_report,
)
from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402
from product_agent_os.infrastructure import InfrastructureError, render_infrastructure_plan, stage_infrastructure  # noqa: E402
from product_agent_os.methodology_audit import build_methodology_audit  # noqa: E402
from product_agent_os.methodology_catalog import load_methodology_catalog, validate_methodology_catalog  # noqa: E402
from product_agent_os.methodology_synthesis import (  # noqa: E402
    build_methodology_synthesis,
    classify_source_artifact,
    dedupe_owner_questions,
)
from product_agent_os.project_code_graph import (  # noqa: E402
    build_project_code_graph,
    build_synthetic_project_graph_from_fixture,
)
from product_agent_os.project_graph_backend import (  # noqa: E402
    LOCAL_BACKEND_TARGET,
    build_local_query_backend_store,
    evaluate_backend_query_contract,
    handle_backend_api_request,
    validate_local_query_backend_store,
)
from product_agent_os.project_graph_extension_closure import (  # noqa: E402
    EXTENSION_CLOSURE_TARGET,
    build_future_extension_closure_packet,
    disable_future_extensions,
    validate_future_extension_closure_packet,
)
from product_agent_os.project_graph_index import (  # noqa: E402
    STATIC_SEARCH_INDEX_TARGET,
    build_static_search_index,
    query_static_search_index,
)
from product_agent_os.project_graph_llm_extraction import (  # noqa: E402
    LLM_EXTRACTION_TARGET,
    build_llm_extraction_proposals,
    evaluate_llm_extraction_proposals,
    validate_llm_extraction_approval,
    validate_llm_extraction_proposals,
)
from product_agent_os.project_graph_live_governance import (  # noqa: E402
    LIVE_CACHE_TARGET,
    LIVE_GOVERNANCE_TARGET,
    build_live_governance_packet,
    disable_live_governance,
    enforce_live_budget,
    sanitize_live_provider_payload,
    validate_live_runtime_approval,
)
from product_agent_os.project_graph_queries import query_project_graph  # noqa: E402
from product_agent_os.project_graph_renderer import render_project_graph_cockpit  # noqa: E402
from product_agent_os.project_graph_search_quality import evaluate_project_graph_search_quality  # noqa: E402
from product_agent_os.project_graph_semantic import (  # noqa: E402
    SEMANTIC_RETRIEVAL_TARGET,
    build_semantic_retrieval_index,
    evaluate_semantic_retrieval_quality,
    query_semantic_retrieval,
    validate_semantic_retrieval_approval,
    validate_semantic_retrieval_index,
)
from product_agent_os.question_protocol import (  # noqa: E402
    MAX_FIRST_RESPONSE_BLOCKING,
    MAX_TOTAL_QUESTIONS,
    build_question_queue,
)
from product_agent_os.status_dashboard import render_status_dashboard  # noqa: E402
from product_agent_os.status_snapshot import build_status_snapshot  # noqa: E402
from product_agent_os.templates import (  # noqa: E402
    AI_RAG_TEMPLATE_ALIASES,
    DELIVERY_TEMPLATE_ALIASES,
    SECURITY_TEMPLATE_ALIASES,
    required_templates,
)
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
from codex_runtime_runner.contracts import build_result, validate_runner_result  # noqa: E402
from codex_runtime_runner.guards import (  # noqa: E402
    validate_approval_boundary,
    validate_automation_boundary,
    validate_codex_handoff,
    validate_route_packet,
)
from codex_runtime_runner.redaction import redact_payload, redact_text, validate_redaction  # noqa: E402
from codex_runtime_runner.routes import plan_route  # noqa: E402


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PLUGIN_ROOT / "assets" / "fixtures"
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "templates"
PROJECT_ROOT = PLUGIN_ROOT.parents[1]
_PROJECT_GRAPH_SAMPLE_CACHE: dict[str, Any] | None = None
_PROJECT_GRAPH_COCKPIT_CACHE: dict[str, Any] | None = None
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
BUSINESS_PRODUCT_GATES = (
    "product_hypothesis_present",
    "target_user_segment_present",
    "value_proposition_evidence_present",
    "opportunity_not_solution_present",
    "success_metric_present",
    "metric_hardening_when_product_behavior_changes",
    "analytics_tracking_plan_present",
    "qualitative_feedback_loop_present",
    "privacy_classification_for_metrics_present",
    "ai_product_eval_when_ai_behavior_changes",
    "post_release_measurement_plan_present",
    "release_measurement_evidence_present",
    "workflow_promotion_value_evidence_present",
    "decision_horizon_present",
    "outcome_metric_level_separated",
    "metric_scope_classified",
)
BUSINESS_PRODUCT_ARTIFACTS = (
    "product-brief.md",
    "value-proposition.md",
    "opportunity-tree.md",
    "experiment-plan.md",
    "tracking-plan.md",
    "metric-spec.md",
    "acceptance-scenarios.md",
)
BUSINESS_PRODUCT_EVAL_FIELDS = (
    "product_hypothesis_contract_present",
    "target_user_segment_contract_present",
    "value_proposition_trace_present",
    "opportunity_solution_assumption_trace_present",
    "metric_hardening_contract_present",
    "analytics_tracking_plan_contract_present",
    "privacy_classification_for_metrics_present",
    "ai_behavior_eval_contract_present",
    "post_release_measurement_contract_present",
    "workflow_promotion_value_evidence_present",
    "decision_horizon_contract_present",
    "outcome_metric_level_contract_present",
    "metric_scope_contract_present",
)
BUSINESS_PRODUCT_DECISION_HORIZONS = (
    "discovery",
    "MVP",
    "beta",
    "production",
    "scale",
)
BUSINESS_PRODUCT_TERMS = (
    "product_hypothesis_present",
    "value_proposition_evidence_present",
    "analytics_tracking_plan_present",
    "qualitative_feedback_loop_present",
    "release_measurement_evidence_present",
    "decision_horizon_present",
    "outcome_metric_level_separated",
    "metric_scope_classified",
    "tracking-plan.md",
    "product-brief.md",
    "value-proposition.md",
    "opportunity-tree.md",
    "experiment-plan.md",
    "business outcome",
    "product outcome",
    "feature traction metric",
    "heart",
    "no-production-telemetry",
    "engineering time saved",
)
REQUIREMENTS_DOMAIN_GATES = (
    "requirements_scope_present",
    "requirements_owner_present",
    "requirement_quality_present",
    "requirement_ids_present",
    "acceptance_scenarios_when_behavior_changes",
    "declarative_acceptance_scenarios_present",
    "requirements_traceability_present",
    "business_rules_present",
    "non_goals_constraints_present",
    "constraints_traceability_present",
    "open_questions_recorded",
    "example_mapping_when_unclear_story",
    "domain_discovery_workshop_when_complex_process",
    "domain_model_when_complex_domain",
    "bounded_context_architecture_boundary_trace",
    "ubiquitous_language_traceability",
    "invariants_and_failure_modes_present",
    "domain_event_contracts_present",
    "api_ui_data_traceability_present",
    "domain_expert_review_present",
    "requirement_change_impact_review_present",
    "accepted_gap_recorded",
    "requirements_evidence_before_implementation",
)
REQUIREMENTS_DOMAIN_ARTIFACTS = (
    "requirement-registry.md",
    "stakeholder-owner-map.md",
    "story-slice-map.md",
    "acceptance-scenarios.md",
    "requirements-traceability-matrix.md",
    "business-rules.md",
    "example-map.md",
    "domain-modeling.md",
    "requirement-change-impact.md",
    "domain-review-record.md",
)
REQUIREMENTS_DOMAIN_EVAL_FIELDS = (
    "requirements_scope_contract_present",
    "requirements_owner_contract_present",
    "requirement_quality_contract_present",
    "requirement_ids_contract_present",
    "acceptance_scenarios_contract_present",
    "declarative_scenario_quality_contract_present",
    "requirements_traceability_contract_present",
    "business_rules_contract_present",
    "non_goals_constraints_contract_present",
    "constraints_traceability_contract_present",
    "open_questions_contract_present",
    "stakeholder_owner_map_contract_present",
    "story_slice_map_contract_present",
    "example_mapping_contract_present",
    "domain_discovery_contract_present",
    "domain_model_contract_present",
    "bounded_context_trace_contract_present",
    "ubiquitous_language_traceability_contract_present",
    "invariants_failure_modes_contract_present",
    "domain_event_contracts_present",
    "api_ui_data_traceability_contract_present",
    "domain_expert_review_contract_present",
    "requirement_change_impact_contract_present",
    "accepted_gap_contract_present",
    "requirements_evidence_before_implementation_contract_present",
    "unsupported_claims_rejected_contract_present",
)
REQUIREMENTS_DOMAIN_TERMS = (
    "requirement-registry.md",
    "stakeholder-owner-map.md",
    "story-slice-map.md",
    "requirements-traceability-matrix.md",
    "business-rules.md",
    "example-map.md",
    "requirement-change-impact.md",
    "domain-review-record.md",
    "requirements_traceability_present",
    "requirement_quality_present",
    "constraints_traceability_present",
    "declarative_acceptance_scenarios_present",
    "business_rules_present",
    "domain_expert_review_present",
    "requirement_change_impact_review_present",
    "accepted_gap_recorded",
    "requirements_evidence_before_implementation",
    "no ui selectors",
    "database internals",
    "function names",
    "test harness",
    "bdd replaces testing",
    "gherkin is mandatory",
    "openapi is requirements source of truth",
)
SOLUTION_ARCHITECTURE_GATES = (
    "solution_architecture_scope_present",
    "architecture_context_view_present",
    "architecture_container_boundary_present",
    "architecture_boundary_per_slice",
    "boundary_responsibility_owner_present",
    "bounded_context_architecture_boundary_trace",
    "dependency_rules_present",
    "public_contract_boundary_trace_present",
    "data_ownership_boundary_present",
    "runtime_deployment_topology_present",
    "observability_architecture_present",
    "quality_attribute_scenarios_present",
    "tradeoff_record_for_high_impact_decision",
    "adr_for_architecture_decision",
    "trust_boundary_security_review_present",
    "domain_to_architecture_trace_present",
    "diagram_render_check_present",
    "architecture_fitness_function_present",
    "migration_rollback_path_present",
    "architecture_docs_as_code_present",
    "architecture_owner_review_present",
    "accepted_gap_recorded",
)
SOLUTION_ARCHITECTURE_ARTIFACTS = (
    "architecture-overview.md",
    "adr.md",
    "architecture-review-record.md",
    "architecture-fitness-functions.md",
    "trust-boundary-map.md",
    "architecture-docs-tooling-decision.md",
    "api-contract-review.md",
    "database-dictionary.md",
    "security-risk-review.md",
    "migration-plan.md",
    "integration-catalog.md",
)
SOLUTION_ARCHITECTURE_EVAL_FIELDS = (
    "solution_architecture_scope_contract_present",
    "architecture_context_view_contract_present",
    "architecture_boundary_contract_present",
    "boundary_owner_contract_present",
    "domain_architecture_trace_contract_present",
    "public_contract_trace_contract_present",
    "data_ownership_boundary_contract_present",
    "trust_boundary_review_contract_present",
    "quality_attribute_scenarios_contract_present",
    "architecture_decision_record_contract_present",
    "runtime_observability_contract_present",
    "diagram_render_check_contract_present",
    "architecture_fitness_function_contract_present",
    "migration_rollback_contract_present",
    "architecture_docs_lifecycle_contract_present",
    "accepted_gap_contract_present",
    "unsupported_architecture_claims_rejected_contract_present",
)
SOLUTION_ARCHITECTURE_TERMS = (
    "solution_architecture_scope_present",
    "architecture_boundary_per_slice",
    "boundary_responsibility_owner_present",
    "adr_for_architecture_decision",
    "diagram_render_check_present",
    "runtime_deployment_topology_present",
    "observability_architecture_present",
    "migration_rollback_path_present",
    "architecture_fitness_function_present",
    "architecture-overview.md",
    "adr.md",
    "architecture-review-record.md",
    "architecture-fitness-functions.md",
    "trust-boundary-map.md",
    "architecture-docs-tooling-decision.md",
    "c4/arc42 only when applicable",
    "architecture-as-code is conditional",
    "well-architected review is conditional",
    "architecture means diagrams",
    "rendered diagram proves correctness",
    "adr is bureaucracy",
)
QUALITY_TESTING_EVALS_GATES = (
    "quality_strategy_present",
    "risk_based_scope_present",
    "test_first_or_gap_present",
    "acceptance_traceability_present",
    "contract_check_present",
    "runtime_evidence_present",
    "manual_qa_evidence_present",
    "visual_a11y_evidence_present",
    "eval_spec_present",
    "eval_rerun_evidence_present",
    "current_evidence_before_completion",
    "ci_quality_gate_present",
    "flaky_test_policy_present",
    "coverage_policy_present",
    "test_data_privacy_present",
    "bug_reproduction_evidence_present",
    "regression_impact_present",
)
QUALITY_TESTING_EVALS_ARTIFACTS = (
    "test-eval-matrix.md",
    "quality-strategy.md",
    "ci-evidence-record.md",
    "flaky-test-policy.md",
    "manual-qa-evidence.md",
)
QUALITY_TESTING_EVALS_EVAL_FIELDS = (
    "quality_strategy_contract_present",
    "risk_based_scope_contract_present",
    "test_first_or_gap_contract_present",
    "acceptance_traceability_contract_present",
    "contract_check_contract_present",
    "runtime_evidence_contract_present",
    "manual_qa_evidence_contract_present",
    "visual_a11y_evidence_contract_present",
    "eval_spec_contract_present",
    "eval_rerun_evidence_contract_present",
    "current_evidence_before_completion_contract_present",
    "ci_quality_gate_contract_present",
    "flaky_test_policy_contract_present",
    "coverage_policy_contract_present",
    "test_data_privacy_contract_present",
    "bug_reproduction_evidence_contract_present",
    "regression_impact_contract_present",
    "unsupported_quality_claims_rejected_contract_present",
)
QUALITY_TESTING_EVALS_TERMS = (
    "quality_testing_evals",
    "quality-strategy.md",
    "test-eval-matrix.md",
    "ci-evidence-record.md",
    "flaky-test-policy.md",
    "manual-qa-evidence.md",
    "current command evidence",
    "current eval evidence",
    "current runtime evidence",
    "manual qa",
    "visual_a11y_evidence_present",
    "coverage is a signal, not proof",
    "test data privacy",
    "present_unverified",
    "explicit_gap_accepted",
    "approval_required",
)
SEMANTIC_EVIDENCE_SUFFICIENCY_TERMS = (
    "semantic_evidence_sufficiency",
    "owner_reviewed_evidence_sufficient_for_real_project_risk",
    "high-risk",
    "production",
    "release",
    "security-sensitive",
    "ai",
    "public-contract",
    "owner",
    "reason",
    "review_date",
    "downstream_risk",
    "follow_up_condition",
    "present_unverified",
    "explicit_gap_accepted",
    "approval_required",
)
FRONTEND_GATES = (
    "frontend_user_flow_acceptance_present",
    "frontend_component_docs_present",
    "frontend_component_state_matrix_present",
    "frontend_design_system_boundary_present",
    "frontend_fsd_boundary_reviewed",
    "frontend_api_contract_alignment_present",
    "frontend_accessibility_review_present",
    "frontend_keyboard_focus_contract_present",
    "frontend_responsive_viewport_matrix_present",
    "frontend_visual_evidence_present",
    "frontend_runtime_console_evidence_present",
    "frontend_performance_budget_present",
    "frontend_browser_support_present",
    "frontend_content_i18n_boundary_present",
    "frontend_interaction_test_evidence_present",
)
FRONTEND_ARTIFACTS = (
    "frontend-flow-spec.md",
    "frontend-state-matrix.md",
    "frontend-visual-qa.md",
    "frontend-accessibility-review.md",
    "frontend-performance-budget.md",
    "component-card.md",
    "acceptance-scenarios.md",
    "api-contract-review.md",
    "quality-strategy.md",
    "test-eval-matrix.md",
    "manual-qa-evidence.md",
)
FRONTEND_EVAL_FIELDS = (
    "frontend_user_flow_contract_present",
    "frontend_component_docs_contract_present",
    "frontend_component_state_matrix_contract_present",
    "frontend_design_system_boundary_contract_present",
    "frontend_fsd_boundary_contract_present",
    "frontend_api_contract_alignment_contract_present",
    "frontend_accessibility_review_contract_present",
    "frontend_keyboard_focus_contract_present",
    "frontend_responsive_viewport_matrix_contract_present",
    "frontend_visual_evidence_contract_present",
    "frontend_runtime_console_evidence_contract_present",
    "frontend_performance_budget_contract_present",
    "frontend_browser_support_contract_present",
    "frontend_content_i18n_contract_present",
    "frontend_interaction_test_evidence_contract_present",
    "unsupported_frontend_claims_rejected_contract_present",
)
FRONTEND_TERMS = (
    "frontend",
    "frontend-flow-spec.md",
    "frontend-state-matrix.md",
    "frontend-visual-qa.md",
    "frontend-accessibility-review.md",
    "frontend-performance-budget.md",
    "route params",
    "auth/permission",
    "seo/meta",
    "token owner",
    "variant policy",
    "local state",
    "server-cache",
    "persisted state",
    "browser/runtime evidence",
    "console status",
    "playwright trace",
    "baseline owner",
    "reduced motion",
    "input modality",
    "wcag 2.2 aa",
    "external visual service approval",
    "storybook proves ui quality",
    "present_unverified",
    "explicit_gap_accepted",
    "approval_required",
    "no secrets",
)
BACKEND_GATES = (
    "backend_service_boundary_present",
    "backend_runtime_behavior_present",
    "backend_dependency_failure_matrix_present",
    "backend_observability_contract_present",
    "backend_slo_or_gap_present",
    "backend_health_probe_contract_present",
    "backend_job_queue_contract_present",
    "backend_data_consistency_strategy_present",
    "backend_config_secrets_boundary_present",
    "backend_security_reviewed",
    "backend_rollback_plan_present",
)
BACKEND_ARTIFACTS = (
    "backend-service-overview.md",
    "backend-runtime-behavior.md",
    "backend-dependency-failure-matrix.md",
    "backend-observability-map.md",
    "backend-slo-sheet.md",
    "backend-health-check-contract.md",
    "backend-job-queue-contract.md",
    "backend-data-consistency-record.md",
    "backend-config-secrets-manifest.md",
    "backend-release-rollback-notes.md",
    "backend-operational-runbook.md",
    "architecture-overview.md",
    "api-contract-review.md",
    "quality-strategy.md",
    "test-eval-matrix.md",
    "manual-qa-evidence.md",
    "security-risk-review.md",
    "release-packet.md",
)
BACKEND_EVAL_FIELDS = (
    "backend_service_boundary_contract_present",
    "backend_runtime_behavior_contract_present",
    "backend_dependency_failure_matrix_contract_present",
    "backend_observability_contract_present",
    "backend_slo_or_gap_contract_present",
    "backend_health_probe_contract_present",
    "backend_job_queue_contract_present",
    "backend_data_consistency_contract_present",
    "backend_config_secrets_boundary_contract_present",
    "backend_security_review_contract_present",
    "backend_rollback_plan_contract_present",
    "unsupported_backend_claims_rejected_contract_present",
)
BACKEND_TERMS = (
    "backend",
    "backend-service-overview.md",
    "backend-runtime-behavior.md",
    "backend-dependency-failure-matrix.md",
    "backend-observability-map.md",
    "backend-slo-sheet.md",
    "backend-health-check-contract.md",
    "backend-job-queue-contract.md",
    "backend-data-consistency-record.md",
    "backend-config-secrets-manifest.md",
    "backend-release-rollback-notes.md",
    "backend-operational-runbook.md",
    "module/service boundary",
    "ports and adapters",
    "inbound contracts",
    "outbound dependencies",
    "deployment/runtime shape",
    "openapi",
    "asyncapi",
    "pact",
    "protobuf",
    "timeout",
    "retry",
    "verification evidence",
    "retry/backoff/max attempts",
    "idempotency",
    "replay",
    "dead-letter behavior",
    "dead-letter queue",
    "observability",
    "reconciliation",
    "migration impact",
    "alert ownership",
    "no-private-payload logging",
    "logs alone are not accepted as observability",
    "slo",
    "sli/slo or explicit gap",
    "health check",
    "health endpoint semantics",
    "queue",
    "data consistency",
    "env/config keys without values",
    "secret source",
    "rollback trigger",
    "handoff to delivery/operations",
    "rollback command",
    "manual procedure",
    "data recovery/replay",
    "irreversible side effects",
    "twelve-factor vocabulary",
    "build-release-run",
    "logs-as-event-stream",
    "decision authority",
    "boundary rationale",
    "adr link or accepted gap",
    "service/user behavior",
    "affected backend unit",
    "semantic conventions or accepted gaps",
    "collector/instrumentation notes",
    "platform-unavailable gap owner",
    "log/query links or placeholders",
    "severity assumptions",
    "no-secrets/no-private-data constraints",
    "contract changes synced with code and tests",
    "provider contracts",
    "backend dependency categories",
    "third-party http/provider clients",
    "backend stack",
    "backend commands",
    "deployment manifests",
    "without executing deployments",
    "blocker/high-risk",
    "simple local/backend-light",
    "accepted gap downgrade",
    "framework-agnostic",
    "node.js, python, java, .net and go snippets",
    "deeper static analysis deferred",
    "owner reviewed test/eval/runtime evidence sufficiency",
    "real project risk",
    "t9-s",
    "track 9 backend methodology",
    "microservices conditional",
    "modular monolith is the default",
    "independent deploy/scale/team/ownership evidence",
    "microservices require explicit owner review",
    "ports/adapters boundary",
    "domain logic independent from http/db/queue/vendor sdk",
    "backpressure",
    "poison message",
    "runtime/failure/observability/security/rollback evidence",
    "owner reviewed evidence sufficiency",
    "logs-only observability",
    "health-endpoint-only readiness",
    "package docs do not prove backend runtime safety",
    "code inspection alone is not backend completion evidence",
    "present_unverified",
    "explicit_gap_accepted",
    "approval_required",
    "no secrets",
)
API_INTEGRATIONS_GATES = (
    "api_contract_source_present",
    "api_consumer_map_present",
    "api_breaking_change_reviewed",
    "api_security_reviewed",
    "api_error_contract_present",
    "api_contract_test_matrix_present",
    "event_delivery_contract_present",
    "generated_client_manifest_present",
    "external_write_approval_present",
    "api_observability_contract_present",
    "api_style_choice_recorded",
    "api_unsupported_claims_rejected",
)
API_INTEGRATIONS_ARTIFACTS = (
    "api-inventory.md",
    "api-contract-review.md",
    "api-error-catalog.md",
    "api-auth-authorization-matrix.md",
    "api-consumer-map.md",
    "api-compatibility-record.md",
    "api-contract-test-matrix.md",
    "generated-sdk-manifest.md",
    "webhook-event-contract.md",
    "external-integration-approval.md",
    "api-style-guide.md",
    "migration-plan.md",
    "integration-catalog.md",
    "security-risk-review.md",
    "release-packet.md",
)
API_INTEGRATIONS_EVAL_FIELDS = (
    "api_integrations_contract_present",
    "api_contract_source_contract_present",
    "api_consumer_map_contract_present",
    "api_breaking_change_review_contract_present",
    "api_security_review_contract_present",
    "api_error_contract_present",
    "api_contract_test_matrix_contract_present",
    "event_delivery_contract_present",
    "generated_client_manifest_contract_present",
    "external_write_approval_contract_present",
    "api_observability_contract_present",
    "unsupported_api_claims_rejected_contract_present",
)
API_INTEGRATIONS_TERMS = (
    "openapi",
    "asyncapi",
    "graphql schema",
    "grpc/protobuf",
    "json schema dialect",
    "pact",
    "source of truth",
    "swagger ui is not source of truth",
    "consumer map",
    "generated clients",
    "breaking/non-breaking classification",
    "contract drift",
    "rfc 9457 problem details",
    "success example",
    "validation failure",
    "auth failure",
    "domain failure",
    "security schemes",
    "scopes",
    "token claims",
    "object-level authorization",
    "rate limits",
    "abuse cases",
    "request ids",
    "correlation ids",
    "error counters",
    "latency",
    "integration failure alerts",
    "provider verification",
    "consumer-driven tests",
    "schema validation is not contract testing",
    "generator config",
    "reviewable diff",
    "multi-repository generated clients deferred",
    "signature verification",
    "idempotency key",
    "dead-letter",
    "cloudevents",
    "external writes are approval_required",
    "no universal graphql/grpc/event default",
    "spectral/redocly/framework-native deferred",
    "api-only contract fixtures do not force backend blockers",
)
DATABASE_DATA_GATES = (
    "database_inventory_present",
    "database_dictionary_present",
    "database_schema_source_present",
    "database_migration_plan_present",
    "database_expand_contract_reviewed",
    "database_transaction_boundary_present",
    "database_rollback_feasibility_present",
    "database_backup_restore_evidence_present",
    "database_data_classification_present",
    "database_data_quality_contract_present",
    "database_data_contract_present",
    "database_lineage_present",
    "database_performance_review_present",
    "database_retention_deletion_policy_present",
    "database_synthetic_fixture_policy_present",
    "database_production_access_approval_present",
    "database_constraints_integrity_review_present",
    "database_unsupported_claims_rejected",
)
DATABASE_DATA_ARTIFACTS = (
    "database-inventory.md",
    "database-dictionary.md",
    "database-migration-plan.md",
    "database-expand-contract-record.md",
    "database-backfill-runbook.md",
    "database-rollback-feasibility.md",
    "database-backup-restore-evidence.md",
    "database-data-classification-matrix.md",
    "database-data-quality-checks.md",
    "database-data-contract.md",
    "database-lineage-map.md",
    "database-query-performance-review.md",
    "database-retention-deletion-policy.md",
    "database-synthetic-fixtures-policy.md",
    "database-production-access-approval.md",
    "migration-plan.md",
    "security-risk-review.md",
    "api-contract-review.md",
    "ai-eval-spec.md",
    "release-readiness.md",
)
DATABASE_DATA_EVAL_FIELDS = (
    "database_data_contract_present",
    "database_inventory_contract_present",
    "database_dictionary_contract_present",
    "database_schema_source_contract_present",
    "database_migration_plan_contract_present",
    "database_expand_contract_contract_present",
    "database_transaction_boundary_contract_present",
    "database_rollback_feasibility_contract_present",
    "database_backup_restore_contract_present",
    "database_data_classification_contract_present",
    "database_data_quality_contract_present",
    "database_lineage_contract_present",
    "database_performance_review_contract_present",
    "database_retention_deletion_contract_present",
    "database_synthetic_fixture_policy_contract_present",
    "database_production_access_approval_contract_present",
    "database_constraints_integrity_contract_present",
    "unsupported_database_claims_rejected_contract_present",
)
DATABASE_DATA_TERMS = (
    "database_data",
    "database_data_signals",
    "database inventory",
    "database dictionary",
    "schema source",
    "data contract",
    "constraints",
    "indexes",
    "foreign keys",
    "unique",
    "not null",
    "transaction boundary",
    "expand-contract",
    "backfill",
    "dry run",
    "rollback feasibility",
    "backup restore evidence",
    "pii",
    "retention",
    "deletion",
    "data quality",
    "great expectations",
    "dbt tests",
    "lineage",
    "openlineage",
    "query performance",
    "destructive migration",
    "drop/rename/truncate",
    "production access approval_required",
    "do not access production data",
    "do not run migration",
    "no universal database tooling default",
    "schema-diff tooling deferred",
    "runtime pipeline and RAG ingestion signals are present_unverified",
    "schema-only artifact is not safety proof",
)
CODEX_AGENTIC_WORKFLOW_GATES = (
    "agentic_scope_classified",
    "control_plane_present",
    "source_of_truth_present",
    "read_only_discovery_complete",
    "model_reasoning_policy_present",
    "fresh_context_handoff_present",
    "ownership_split_present",
    "subagent_parallelism_safe",
    "approval_boundary_present",
    "mcp_permission_review_present",
    "hook_activation_approval_present",
    "plugin_boundary_present",
    "skill_promotion_evidence_present",
    "automation_manual_stability_present",
    "agent_eval_workflow_present",
    "memory_policy_present",
    "agentic_evidence_before_completion",
    "unsupported_agentic_claims_rejected",
)
CODEX_AGENTIC_WORKFLOW_ARTIFACTS = (
    "AGENTS.md",
    "PLAN.md",
    "TEST.md",
    "EVALS.md",
    "RUNLOG.md",
    "agent-task-packet.md",
    "handoff-contract.md",
    "worktree-ownership.md",
    "approval-record.md",
    "plugin-blueprint.md",
    "automation-candidate.md",
    "model-reasoning-policy.md",
    "mcp-permission-review.md",
    "hook-governance.md",
    "skill-promotion-record.md",
    "agent-eval-workflow.md",
)
CODEX_AGENTIC_WORKFLOW_EVAL_FIELDS = (
    "agentic_scope_classified_contract_present",
    "control_plane_contract_present",
    "source_of_truth_contract_present",
    "read_only_discovery_contract_present",
    "model_reasoning_policy_contract_present",
    "fresh_context_handoff_contract_present",
    "ownership_split_contract_present",
    "subagent_parallelism_safe_contract_present",
    "approval_boundary_contract_present",
    "mcp_permission_review_contract_present",
    "hook_activation_approval_contract_present",
    "plugin_boundary_contract_present",
    "skill_promotion_evidence_contract_present",
    "automation_manual_stability_contract_present",
    "agent_eval_workflow_contract_present",
    "memory_policy_contract_present",
    "agentic_evidence_before_completion_contract_present",
    "unsupported_agentic_claims_rejected_contract_present",
)
CODEX_AGENTIC_WORKFLOW_TERMS = (
    "codex_agentic_workflow",
    "model-reasoning-policy.md",
    "mcp-permission-review.md",
    "hook-governance.md",
    "skill-promotion-record.md",
    "agent-eval-workflow.md",
    "codex app",
    "ide extension",
    "codex exec",
    "github action",
    "mcp",
    "agents sdk",
    "automation",
    "memory as recall only",
    "no silent activation",
    "present_unverified",
    "explicit_gap_accepted",
    "approval_required",
)
LLM_AI_RAG_GATES = (
    "ai_behavior_spec_present",
    "ai_baseline_eval_present",
    "ai_eval_rerun_command_present",
    "ai_dataset_governance_present",
    "ai_prompt_contract_present",
    "ai_model_decision_record_present",
    "ai_structured_output_contract_present",
    "ai_tool_contract_present",
    "ai_human_approval_boundary_present",
    "rag_source_inventory_present",
    "rag_retrieval_config_present",
    "rag_grounding_eval_present",
    "agent_workflow_trace_present",
    "ai_safety_review_present",
    "ai_cost_latency_budget_present",
    "ai_no_private_data_in_fixtures_present",
    "ai_unsupported_claims_rejected",
    "ai_agent_handoff_contract_compatible",
    "ai_eval_tooling_selector_present",
    "ai_model_migration_policy_present",
    "rag_corpus_lifecycle_privacy_present",
    "ai_behavior_diff_signal_policy_present",
    "ai_incident_workflow_present",
)
LLM_AI_RAG_ARTIFACTS = (
    "ai-behavior-spec.md",
    "prompt-contract.md",
    "model-decision-record.md",
    "ai-eval-spec.md",
    "eval-run-report.md",
    "ai-dataset-manifest.md",
    "structured-output-schema.md",
    "ai-tool-contract.md",
    "rag-source-inventory.md",
    "rag-retrieval-config.md",
    "rag-eval-report.md",
    "grounding-rubric.md",
    "agent-task-packet.md",
    "agent-workflow-map.md",
    "guardrail-matrix.md",
    "trace-evidence-packet.md",
    "ai-cost-latency-budget.md",
)
LLM_AI_RAG_EVAL_FIELDS = (
    "llm_ai_rag_contract_present",
    "ai_behavior_spec_contract_present",
    "ai_baseline_eval_contract_present",
    "ai_eval_rerun_command_contract_present",
    "ai_dataset_governance_contract_present",
    "ai_prompt_contract_contract_present",
    "ai_model_decision_record_contract_present",
    "ai_structured_output_contract_present",
    "ai_tool_contract_contract_present",
    "ai_human_approval_boundary_contract_present",
    "rag_source_inventory_contract_present",
    "rag_retrieval_config_contract_present",
    "rag_grounding_eval_contract_present",
    "agent_workflow_trace_contract_present",
    "ai_safety_review_contract_present",
    "ai_cost_latency_budget_contract_present",
    "ai_no_private_data_in_fixtures_contract_present",
    "unsupported_ai_claims_rejected_contract_present",
    "ai_agent_handoff_contract_compatibility_present",
    "ai_eval_tooling_selector_contract_present",
    "ai_model_migration_policy_contract_present",
    "rag_corpus_lifecycle_privacy_contract_present",
    "ai_behavior_diff_signal_policy_contract_present",
    "ai_incident_workflow_contract_present",
)
LLM_AI_RAG_TERMS = (
    "llm_ai_rag",
    "llm_ai_rag_readiness_when_ai_behavior_changes",
    "ai behavior promise",
    "baseline eval",
    "eval rerun evidence",
    "app-backed eval path",
    "prompt/context inventory",
    "dataset governance",
    "retrieval metrics",
    "grounding",
    "safety evidence",
    "cost evidence",
    "current-run evidence",
    "accepted-gap handling",
    "prompt inspection is enough",
    "ai quality claim without current eval evidence",
    "citations alone prove grounding",
    "model upgrade automatically improves quality",
    "do not force one eval runner",
    "do not force multi-agent architecture",
    "do not run live model calls",
    "present_unverified",
    "not_applicable",
    "approval_required",
    "private customer data",
    "raw private chat logs",
    "agent-handoff-contract.md",
    "handoff owner",
    "trace source type",
    "opentelemetry genai span",
    "promptfoo",
    "openai evals",
    "pytest/jest",
    "ragas",
    "langsmith",
    "snapshot or approved alias",
    "prompt migration impact",
    "vector store lifecycle",
    "ai incident boundary",
    "security/privacy handoff",
)
SECURITY_PRIVACY_COMPLIANCE_GATES = (
    "security_sensitive_classification_present",
    "threat_surface_present",
    "security_risk_review_present",
    "asvs_mapping_present",
    "asvs_level_selection_present",
    "secure_sdlc_ssdf_samm_present",
    "api_security_scheme_present",
    "authz_negative_tests_present",
    "secrets_policy_present",
    "data_classification_present",
    "data_redaction_lifecycle_present",
    "privacy_impact_record_present",
    "external_write_approval_present",
    "abuse_rate_limit_review_present",
    "audit_logging_review_present",
    "supply_chain_review_present",
    "sbom_provenance_decision_present",
    "ci_permission_review_present",
    "ai_security_review_present",
    "compliance_overlay_present",
    "compliance_overlay_taxonomy_present",
    "vulnerability_response_workflow_present",
    "codex_security_scan_status_present",
    "security_evidence_before_completion",
    "security_unsupported_claims_rejected",
)
SECURITY_PRIVACY_COMPLIANCE_ARTIFACTS = (
    "security-risk-review.md",
    "threat-surface.md",
    "asvs-ssdf-mapping.md",
    "authz-negative-test-matrix.md",
    "secrets-policy.md",
    "data-classification-register.md",
    "privacy-impact-record.md",
    "api-security-review.md",
    "abuse-rate-limit-plan.md",
    "supply-chain-review.md",
    "sbom-manifest.md",
    "ci-permissions-review.md",
    "audit-logging-review.md",
    "ai-security-review.md",
    "compliance-overlay.md",
    "vulnerability-response-record.md",
    "approval-record.md",
)
SECURITY_PRIVACY_COMPLIANCE_EVAL_FIELDS = (
    "security_privacy_compliance_contract_present",
    "security_sensitive_classification_contract_present",
    "threat_surface_contract_present",
    "security_risk_review_contract_present",
    "asvs_ssdf_mapping_contract_present",
    "asvs_level_selection_contract_present",
    "secure_sdlc_ssdf_samm_contract_present",
    "api_security_review_contract_present",
    "authz_negative_tests_contract_present",
    "secrets_policy_contract_present",
    "data_classification_contract_present",
    "data_redaction_lifecycle_contract_present",
    "privacy_impact_contract_present",
    "external_write_approval_contract_present",
    "abuse_rate_limit_contract_present",
    "audit_logging_contract_present",
    "supply_chain_contract_present",
    "sbom_provenance_contract_present",
    "ci_permission_contract_present",
    "ai_security_review_contract_present",
    "compliance_overlay_contract_present",
    "compliance_overlay_taxonomy_contract_present",
    "vulnerability_response_contract_present",
    "codex_security_scan_status_contract_present",
    "security_evidence_before_completion_contract_present",
    "unsupported_security_claims_rejected_contract_present",
)
SECURITY_PRIVACY_COMPLIANCE_TERMS = (
    "security_privacy_compliance",
    "security_privacy_compliance_when_sensitive_surface",
    "security_sensitive_surface",
    "security_sensitive_classification_present",
    "threat surface",
    "codex security scan status",
    "not requested/run/blocked",
    "asvs level 1",
    "asvs level 2",
    "asvs level 3",
    "ssdf",
    "samm",
    "bola",
    "bfla",
    "object property authorization",
    "unsafe consumption",
    "raw secrets",
    "payment data",
    "raw pii",
    "private customer data",
    "data redaction lifecycle",
    "sbom/provenance",
    "ci permissions",
    "supply chain",
    "compliance overlay",
    "legal/regulatory",
    "customer contractual",
    "internal policy",
    "vulnerability response",
    "approval_required",
    "explicit_gap_accepted",
    "not legal advice",
    "docs-only security article",
    "docs-only security articles are not regulated automatically",
    "security review after coding",
    "no secrets in code means safe",
    "asvs/owasp proves compliance",
    "sbom once is enough",
    "codex security scan is implied",
    "oauth proves api security",
    "privacy compliance is universal",
)
DELIVERY_RELEASE_OPERATIONS_GATES = (
    "release_scope_present",
    "version_impact_present",
    "changelog_release_notes_present",
    "artifact_manifest_present",
    "release_evidence_present",
    "release_evidence_before_completion",
    "rollout_strategy_present",
    "rollback_recovery_present",
    "environment_approval_boundary_present",
    "external_release_approval_present",
    "ci_cd_governance_present",
    "slo_or_operational_gap_present",
    "observability_release_evidence_present",
    "operations_runbook_present",
    "incident_response_path_present",
    "post_release_measurement_present",
    "automation_manual_stability_present",
    "release_mode_policy_present",
    "build_release_run_boundary_present",
    "platform_distribution_evidence_present",
    "release_communication_present",
    "versioning_tooling_decision_present",
    "github_environment_controls_present",
    "dora_measurement_design_present",
    "incident_postmortem_learning_present",
    "observability_on_call_tooling_present",
    "release_integrity_security_handoff_present",
    "release_evidence_sufficiency_owner_reviewed",
    "delivery_unsupported_claims_rejected",
)
DELIVERY_RELEASE_OPERATIONS_ARTIFACTS = (
    "release-readiness.md",
    "versioning-policy.md",
    "release-artifact-manifest.md",
    "rollout-plan.md",
    "rollback-recovery-plan.md",
    "environment-matrix.md",
    "deployment-plan.md",
    "ci-cd-workflow-inventory.md",
    "observability-map.md",
    "slo-spec.md",
    "operations-runbook.md",
    "incident-record.md",
    "postmortem.md",
    "automation-candidate.md",
    "post-release-review.md",
    "approval-record.md",
    "metric-spec.md",
    "supply-chain-review.md",
    "sbom-manifest.md",
    "vulnerability-response-record.md",
)
DELIVERY_RELEASE_OPERATIONS_EVAL_FIELDS = (
    "delivery_release_operations_contract_present",
    "release_scope_contract_present",
    "version_impact_contract_present",
    "changelog_release_notes_contract_present",
    "release_evidence_contract_present",
    "release_evidence_before_completion_contract_present",
    "artifact_manifest_contract_present",
    "rollout_strategy_contract_present",
    "rollback_recovery_contract_present",
    "ci_cd_governance_contract_present",
    "operations_runbook_contract_present",
    "incident_response_contract_present",
    "post_release_measurement_contract_present",
    "automation_manual_stability_contract_present",
    "release_mode_policy_contract_present",
    "build_release_run_boundary_contract_present",
    "platform_distribution_evidence_contract_present",
    "release_communication_contract_present",
    "versioning_tooling_decision_contract_present",
    "github_environment_controls_contract_present",
    "dora_measurement_design_contract_present",
    "incident_postmortem_learning_contract_present",
    "observability_on_call_tooling_contract_present",
    "release_integrity_security_handoff_contract_present",
    "release_evidence_sufficiency_owner_reviewed_contract_present",
    "unsupported_delivery_claims_rejected_contract_present",
)
DELIVERY_RELEASE_OPERATIONS_TERMS = (
    "delivery_release_operations",
    "delivery_release_operations_readiness_when_release_or_operations_changes",
    "release-readiness.md",
    "versioning-policy.md",
    "release-artifact-manifest.md",
    "rollout-plan.md",
    "rollback-recovery-plan.md",
    "environment-matrix.md",
    "deployment-plan.md",
    "ci-cd-workflow-inventory.md",
    "observability-map.md",
    "slo-spec.md",
    "operations-runbook.md",
    "incident-record.md",
    "postmortem.md",
    "automation-candidate.md",
    "post-release-review.md",
    "supply-chain-review.md",
    "sbom-manifest.md",
    "vulnerability-response-record.md",
    "release scope",
    "version impact",
    "release evidence",
    "release evidence before completion",
    "artifact manifest",
    "rollout strategy",
    "rollback/recovery",
    "environment approval boundary",
    "external release approval",
    "ci/cd governance",
    "observability release evidence",
    "slo or operational gap",
    "operations runbook",
    "incident response",
    "post-release measurement",
    "manual success evidence",
    "stable inputs/outputs",
    "approval requirements",
    "value evidence",
    "rollback/disable path",
    "candidate-only automation",
    "active schedules remain out of scope",
    "release mode policy",
    "build-release-run boundary",
    "platform distribution evidence",
    "release communication",
    "versioning tooling decision",
    "github environment controls",
    "dora measurement design",
    "incident postmortem learning",
    "observability on-call tooling",
    "release integrity security handoff",
    "owner-reviewed release evidence sufficiency",
    "release_evidence_sufficiency_owner_reviewed",
    "immutable artifact",
    "release identifier",
    "runtime configuration boundary",
    "environment-specific config injection",
    "accepted platform exception",
    "team-only interpretation",
    "selected/rejected/deferred",
    "accepted no-tooling gap",
    "security ownership",
    "approval_required",
    "explicit_gap_accepted",
    "release-ready",
    "feature flags remove release risk",
    "gitops is automatically safe",
    "automation is safer because it is repeatable",
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
QUESTION_QUEUE_TERMS = (
    "question_queue",
    "max_total_questions",
    "max_first_response_blocking",
    "max_blocking_questions_in_first_response",
    "next_blocking_question",
    "question_counts",
    "question_summary",
    "questions_for_owner",
    "not_applicable_or_gap",
)
STATUS_SNAPSHOT_TERMS = (
    "status snapshot",
    "dashboard_policy",
    "underlying_artifacts",
    "success_claim_policy",
    "never from dashboard alone",
    "stale evidence",
    "not_claimed",
)
STATUS_DASHBOARD_TERMS = (
    "status_dashboard",
    ".codex/product-agent-os/status.html",
    ".codex/product-agent-os/status.json",
    "offline html doctype present",
    "external urls absent",
    "external scripts absent",
    "snapshot redaction validated",
)
GUIDED_QUESTION_BEHAVIOR_TERMS = (
    "guided-question-smallest-blocking-question",
    "guided-question-no-broad-methodology-interview",
    "runtime-first-response-no-question-dump",
    "one blocking question maximum",
    "no broad methodology interview",
    "no full question queue dump",
)
STATUS_DASHBOARD_BEHAVIOR_TERMS = (
    "status-dashboard-generated-view-only",
    "status-dashboard-stale-evidence-no-success-claim",
    "dashboard is a generated view",
    "no success claim from stale evidence",
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
    "api_contract_readiness_when_api_or_integration_changes",
    "database_data_readiness_when_database_or_data_changes",
    "release_version_impact_when_public_contract_changes",
    "reproduction_evidence_when_bug_rescue",
    "approval_before_greenfield_scaffold",
    "integration_catalog_when_external_systems_exist",
    "ownership_split_when_parallel_agents_used",
    "pr_risk_review_when_review_mode",
    "onboarding_map_when_legacy_repo",
    "migration_plan_when_contract_or_data_changes",
    "security_review_when_sensitive_surface",
    "security_privacy_compliance_when_sensitive_surface",
    "backend_readiness_when_backend_changes",
    "platform_runtime_check_when_native_or_desktop",
    "ci_failure_evidence_when_ci_stabilization",
    "release_readiness_when_distribution_changes",
    "delivery_release_operations_readiness_when_release_or_operations_changes",
    "plugin_success_metric_for_major_workflow",
    "root_cause_before_bug_fix",
    "no_placeholder_plan_when_plan_ready",
    "two_stage_review_when_risky_or_parallel",
    "fresh_context_handoff_when_subagents_used",
    "behavioral_eval_when_new_route_added",
    "codex_only_compatibility_when_plugin_packaging_changes",
    "finish_options_when_release_ready",
    "standards_trigger_policy_when_architecture_api_release_or_governance_changes",
    "quality_testing_evals_when_non_trivial_change",
    "semantic_evidence_sufficiency",
    "runtime_methodology_packet_safety",
    "agent_skill_metrics_loop",
    "codex_agentic_workflow",
    "frontend_methodology",
    "llm_ai_rag_readiness_when_ai_behavior_changes",
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
        "methodology_domains": [],
        "renderer_file_count": 0,
        "renderer_actions": {},
        "expected_checks": {},
        "evidence": {},
    }


def evaluate_fixture(path: Path) -> dict[str, Any]:
    try:
        audit = analyze_workspace(path)
        methodology_audit = build_methodology_audit(path)
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
        expected_checks = _expected_checks(path.name, audit, methodology_audit, rendered, renderer_actions)
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
        expected_checks.update(_methodology_expected_checks(methodology_audit))
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
        methodology_audit = {}
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
        methodology_audit = {}
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
        "methodology_domains": _applicable_methodology_domains(methodology_audit),
        "renderer_file_count": len(renderer_files),
        "renderer_actions": renderer_actions,
        "expected_checks": expected_checks,
        "evidence": evidence,
    }


def _applicable_methodology_domains(methodology_audit: dict[str, Any]) -> list[str]:
    domains = methodology_audit.get("methodology_domains", {}) if isinstance(methodology_audit, dict) else []
    if not isinstance(domains, list):
        return []
    return [
        str(domain["id"])
        for domain in domains
        if isinstance(domain, dict) and domain.get("id") and domain.get("status") != "not_applicable"
    ]


def _methodology_expected_checks(methodology_audit: dict[str, Any]) -> dict[str, bool]:
    return {
        "methodology_catalog_contract_present": _methodology_catalog_contract_present(),
        "methodology_intelligence_contract_present": _methodology_intelligence_contract_present(methodology_audit),
        "methodology_recommendations_prioritized": _methodology_recommendations_prioritized(methodology_audit),
        "cross_domain_synthesis_contract_present": _cross_domain_synthesis_contract_present(methodology_audit),
        "safe_next_action_risk_ordered": _safe_next_action_risk_ordered(),
        "source_artifact_mapping_contract_present": _source_artifact_mapping_contract_present(methodology_audit),
        "cross_domain_false_positive_guards_present": _cross_domain_false_positive_guards_present(),
        "methodology_audit_read_only": methodology_audit.get("write_policy") == "read_only"
        if isinstance(methodology_audit, dict)
        else False,
    }


def _methodology_catalog_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    return not validate_methodology_catalog(catalog) and len(catalog.get("domains", [])) == 12


def _methodology_intelligence_contract_present(methodology_audit: dict[str, Any]) -> bool:
    if not isinstance(methodology_audit, dict):
        return False
    required_keys = {
        "status",
        "write_policy",
        "maturity_level",
        "complexity_profile",
        "observed_signals",
        "intent_signals",
        "unknowns",
        "questions_for_owner",
        "provisional_assumptions",
        "delivery_map",
        "methodology_domains",
        "recommendations",
        "recommendation_groups",
        "methodology_synthesis",
        "safe_next_action",
    }
    if not required_keys.issubset(methodology_audit):
        return False
    if methodology_audit.get("write_policy") != "read_only":
        return False
    delivery_map = methodology_audit.get("delivery_map")
    if not isinstance(delivery_map, dict):
        return False
    return all(
        key in delivery_map
        for key in ["surface_map", "system_map", "lifecycle_map", "methodology_map", "next_action_map"]
    )


def _methodology_recommendations_prioritized(methodology_audit: dict[str, Any]) -> bool:
    if not isinstance(methodology_audit, dict):
        return False
    recommendations = methodology_audit.get("recommendations", [])
    if not isinstance(recommendations, list):
        return False
    priority_order = {
        "P0_blocker": 0,
        "P1_high_risk": 1,
        "P2_recommended": 2,
        "P3_optional_maturity": 3,
        "not_applicable": 4,
    }
    ranks = [
        priority_order.get(str(recommendation.get("priority", "not_applicable")), 99)
        for recommendation in recommendations
        if isinstance(recommendation, dict)
    ]
    return ranks == sorted(ranks)


def _cross_domain_synthesis_contract_present(methodology_audit: dict[str, Any]) -> bool:
    if not isinstance(methodology_audit, dict):
        return False
    packet = methodology_audit.get("methodology_synthesis")
    if not isinstance(packet, dict):
        return False
    required_keys = {
        "status",
        "write_policy",
        "recommendation_groups",
        "source_artifact_ledger",
        "semantic_evidence_sufficiency",
        "owner_questions",
        "safe_next_action",
    }
    if not required_keys.issubset(packet):
        return False
    if methodology_audit.get("recommendation_groups") != packet.get("recommendation_groups"):
        return False
    if packet.get("write_policy") != "read_only":
        return False
    semantic = packet.get("semantic_evidence_sufficiency")
    ledger = packet.get("source_artifact_ledger")
    if not isinstance(semantic, dict) or not isinstance(ledger, list):
        return False
    if "owner_reviewed_evidence_sufficient_for_real_project_risk" not in semantic.get("satisfied_by", []):
        return False
    decisions = {str(item.get("decision")) for item in ledger if isinstance(item, dict)}
    if not {"alias", "existing_non_template"}.issubset(decisions):
        return False
    return bool(packet.get("safe_next_action"))


def _safe_next_action_risk_ordered() -> bool:
    packet = build_methodology_synthesis(
        [
            {
                "priority": "P0_blocker",
                "domain": "quality_testing_evals",
                "gate": "quality_strategy_present",
                "artifact": "quality-strategy.md",
                "reason": "Generic quality strategy is missing.",
                "evidence_required": ["verification command"],
                "safe_next_action": "Stage quality-strategy.md.",
            },
            {
                "priority": "P1_high_risk",
                "domain": "security_privacy_compliance",
                "gate": "external_write_approval_present",
                "artifact": "approval-record.md",
                "reason": "Payment or external write work needs approval.",
                "evidence_required": ["approval_required", "owner"],
                "safe_next_action": "Record approval_required before the external write.",
            },
            {
                "priority": "P1_high_risk",
                "domain": "delivery_release_operations",
                "gate": "release_evidence_present",
                "artifact": "release-readiness.md",
                "reason": "Package release needs release readiness evidence.",
                "evidence_required": ["release scope", "publish approval"],
                "safe_next_action": "Stage release-readiness.md before publish.",
            },
        ]
    )
    artifacts = [str(group.get("artifact")) for group in packet.get("recommendation_groups", [])]
    return (
        artifacts[:2] == ["approval-record.md", "release-readiness.md"]
        and "quality-strategy.md" in artifacts
        and packet.get("safe_next_action") == "Record approval_required before the external write."
    )


def _source_artifact_mapping_contract_present(methodology_audit: dict[str, Any] | None = None) -> bool:
    context_map = classify_source_artifact("context-map.md")
    changelog = classify_source_artifact("CHANGELOG.md")
    unknown = classify_source_artifact("unpackaged-source-experiment.md")
    if context_map.get("decision") != "alias" or context_map.get("target") != "architecture-overview.md":
        return False
    if changelog.get("decision") != "existing_non_template":
        return False
    if unknown.get("decision") != "deferred" or not unknown.get("reason"):
        return False
    if methodology_audit:
        ledger = methodology_audit.get("methodology_synthesis", {}).get("source_artifact_ledger", [])
        if not isinstance(ledger, list) or not any(
            isinstance(item, dict) and item.get("artifact") == "context-map.md" for item in ledger
        ):
            return False
    return True


def _cross_domain_false_positive_guards_present() -> bool:
    try:
        synthesis = load_methodology_catalog()["synthesis"]
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    rule_ids = {
        str(rule.get("id"))
        for rule in synthesis.get("false_positive_rules", [])
        if isinstance(rule, dict)
    }
    return {
        "docs_only_lightweight",
        "backend_fsd_like_without_ui",
        "ci_only_without_release_mutation",
        "release_tooling_only_present_unverified",
        "internal_cli_no_heavy_surfaces",
    }.issubset(rule_ids)


def _owner_question_dedupe_contract_present() -> bool:
    return dedupe_owner_questions(
        [
            "Who owns the highest-priority missing methodology gate?",
            "Who owns the highest priority missing methodology gate?",
            "Which detected surfaces are in scope for this slice?",
        ]
    ) == [
        "Who owns the highest-priority missing methodology gate?",
        "Which detected surfaces are in scope for this slice?",
    ]


def _renderer_actions(files: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(item.get("target_path")): str(item.get("action"))
        for item in files
        if isinstance(item, dict) and item.get("target_path")
    }


def _expected_checks(
    fixture: str,
    audit: dict[str, Any],
    methodology_audit: dict[str, Any],
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
        checks["business_product_contract_present"] = _business_product_contract_present()
        checks["requirements_domain_contract_present"] = _requirements_domain_contract_present()
        checks["solution_architecture_contract_present"] = _solution_architecture_contract_present()
        checks["quality_testing_evals_contract_present"] = _quality_testing_evals_contract_present()
        checks["codex_agentic_workflow_contract_present"] = _codex_agentic_workflow_contract_present()
        checks["frontend_contract_present"] = _frontend_contract_present()
        checks["backend_contract_present"] = _backend_contract_present()
        checks["api_integrations_contract_present"] = _api_integrations_contract_present()
        checks["api_contract_source_present"] = _api_integrations_contract_present()
        checks["external_write_approval_present"] = _api_integrations_contract_present()
        checks["database_data_contract_present"] = _database_data_contract_present()
        checks["llm_ai_rag_contract_present"] = _llm_ai_rag_contract_present()
        checks["security_privacy_compliance_contract_present"] = _security_privacy_compliance_contract_present()
        checks["delivery_release_operations_contract_present"] = _delivery_release_operations_contract_present()
        checks["question_queue_contract_present"] = _question_queue_contract_present()
        checks["status_snapshot_present"] = _status_snapshot_present()
        checks["status_dashboard_present"] = _status_dashboard_present()
        checks["dashboard_no_external_assets"] = _dashboard_no_external_assets()
        checks["trace_data_classification_gate_present"] = _trace_data_classification_gate_present()
        checks["offline_artifact_safety_shared"] = _offline_artifact_safety_shared()
        checks["no_baseline_renderer_pollution"] = _no_baseline_renderer_pollution(rendered)
        checks["metrics_report_redacted"] = _metrics_report_redacted()
        checks["scorecard_ledger_contract_present"] = _scorecard_ledger_contract_present()
        checks["active_metrics_automation_blocked"] = _active_metrics_automation_blocked()
        checks["metrics_loop_runtime_route_contract_present"] = _metrics_loop_runtime_route_contract_present()
        checks["metrics_loop_lifecycle_contract_present"] = _metrics_loop_lifecycle_contract_present()
        checks["update_candidate_rollback_required"] = _update_candidate_rollback_required()
        checks["metrics_loop_false_positive_guards_present"] = _metrics_loop_false_positive_guards_present()
        checks["question_budget_false_positive_guard_present"] = (
            _question_budget_false_positive_guard_present()
        )
        checks["dashboard_not_source_of_truth"] = _dashboard_not_source_of_truth()
        checks["stale_evidence_no_success_claim"] = _stale_evidence_no_success_claim()
        checks["project_graph_contract_present"] = _project_graph_contract_present()
        checks["project_graph_no_external_assets"] = _project_graph_no_external_assets()
        checks["project_graph_redaction_present"] = _project_graph_redaction_present()
        checks["project_graph_scale_bounds_present"] = _project_graph_scale_bounds_present()
        checks["project_graph_generated_view_only"] = _project_graph_generated_view_only()
        checks["project_graph_eight_page_cockpit_present"] = _project_graph_eight_page_cockpit_present()
        checks["project_graph_section_preservation_present"] = _project_graph_section_preservation_present()
        checks["project_graph_cockpit_generated_view_boundary_present"] = (
            _project_graph_cockpit_generated_view_boundary_present()
        )
        checks["project_graph_search_quality_present"] = _project_graph_search_quality_present()
        checks["project_graph_search_quality_thresholds_present"] = (
            _project_graph_search_quality_thresholds_present()
        )
        checks["project_graph_static_search_index_present"] = _project_graph_static_search_index_present()
        checks["project_graph_static_search_index_quality_present"] = (
            _project_graph_static_search_index_quality_present()
        )
        checks["project_graph_local_backend_gate_present"] = _project_graph_local_backend_gate_present()
        checks["project_graph_backend_decision_packet_present"] = (
            _project_graph_backend_decision_packet_present()
        )
        checks["project_graph_backend_disabled_by_default"] = _project_graph_backend_disabled_by_default()
        checks["project_graph_backend_operational_controls_present"] = (
            _project_graph_backend_operational_controls_present()
        )
        checks["project_graph_backend_graph_only_fallback_present"] = (
            _project_graph_backend_graph_only_fallback_present()
        )
        checks["project_graph_backend_no_production_or_source_truth_claims"] = (
            _project_graph_backend_no_production_or_source_truth_claims()
        )
        checks["project_graph_semantic_retrieval_gate_present"] = (
            _project_graph_semantic_retrieval_gate_present()
        )
        checks["project_graph_semantic_retrieval_eval_present"] = (
            _project_graph_semantic_retrieval_eval_present()
        )
        checks["project_graph_semantic_present_unverified_routing_present"] = (
            _project_graph_semantic_present_unverified_routing_present()
        )
        checks["project_graph_llm_extraction_gate_present"] = _project_graph_llm_extraction_gate_present()
        checks["project_graph_llm_proposal_schema_present"] = _project_graph_llm_proposal_schema_present()
        checks["project_graph_rationale_comment_proposals_present"] = (
            _project_graph_rationale_comment_proposals_present()
        )
        checks["project_graph_llm_extraction_eval_present"] = _project_graph_llm_extraction_eval_present()
        checks["project_graph_future_extension_closure_present"] = _project_graph_future_extension_closure_present()
        checks["project_graph_extension_rollback_deletion_present"] = (
            _project_graph_extension_rollback_deletion_present()
        )
        checks["project_graph_unapproved_surface_blocking_present"] = (
            _project_graph_unapproved_surface_blocking_present()
        )
        checks["project_graph_extension_full_verification_contract_present"] = (
            _project_graph_extension_full_verification_contract_present()
        )
        checks["project_graph_live_approval_packet_present"] = _project_graph_live_approval_packet_present()
        checks["project_graph_live_data_classification_policy_present"] = (
            _project_graph_live_data_classification_policy_present()
        )
        checks["project_graph_live_redaction_guard_present"] = _project_graph_live_redaction_guard_present()
        checks["project_graph_provider_credentials_boundary_present"] = (
            _project_graph_provider_credentials_boundary_present()
        )
        checks["project_graph_live_cache_deletion_policy_present"] = (
            _project_graph_live_cache_deletion_policy_present()
        )
        checks["project_graph_live_budget_guard_present"] = _project_graph_live_budget_guard_present()
        checks["project_graph_live_governance_no_live_calls_present"] = (
            _project_graph_live_governance_no_live_calls_present()
        )
        checks["project_graph_future_backend_semantic_gates_present"] = (
            _project_graph_future_backend_semantic_gates_present()
        )
        checks["methodology_applicability_contract_present"] = (
            _methodology_applicability_contract_present(audit)
        )
        checks["semantic_evidence_sufficiency_contract_present"] = (
            _semantic_evidence_sufficiency_contract_present()
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
        "ai-prompt-model-change": "ai_eval_regression",
        "ai-tool-approval": "ai_eval_regression",
        "ai-structured-output": "ai_eval_regression",
        "ai-agent-trace": "ai_eval_regression",
        "ai-latency-cost-budget": "ai_eval_regression",
        "native-mobile-permissions": "native_mobile_feature",
        "desktop-local-indexer": "desktop_local_first",
        "data-migration-pii": "data_migration",
        "database-schema-only": "data_migration",
        "database-destructive-migration": "data_migration",
        "database-production-access-approval": "data_migration",
        "database-lineage-rag-overlap": "data_migration",
        "security-auth-payment": "security_sensitive_change",
        "ci-flaky-tests": "ci_stabilization",
        "package-release": "release_packaging",
    }
    if fixture in expected_usage_modes:
        expected_mode = expected_usage_modes[fixture]
        checks[f"usage_mode_{expected_mode}"] = primary_mode == expected_mode
    if fixture in {
        "project-code-graph-scale-1k",
        "project-code-graph-scale-5k",
        "project-code-graph-scale-10k",
    }:
        checks["project_graph_scale_bounds_present"] = _project_graph_scale_bounds_present(
            FIXTURES / fixture
        )
        checks["project_graph_generated_view_only"] = _project_graph_generated_view_only(
            FIXTURES / fixture
        )
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
    if fixture == "frontend-ui-app":
        applicability = audit.get("methodology_applicability", {})
        frontend_packet = (
            applicability.get("frontend_methodology", {}) if isinstance(applicability, dict) else {}
        )
        checks["frontend_contract_present"] = _frontend_contract_present()
        checks["frontend_methodology_detected_for_ui"] = (
            isinstance(signals, dict)
            and signals.get("frontend") is True
            and "frontend" in route_methodology_signals
            and isinstance(frontend_packet, dict)
            and frontend_packet.get("status") == "present_unverified"
        )
    if fixture == "backend-service-app":
        applicability = audit.get("methodology_applicability", {})
        backend_packet = (
            applicability.get("backend_methodology", {}) if isinstance(applicability, dict) else {}
        )
        checks["backend_contract_present"] = _backend_contract_present()
        checks["backend_methodology_detected_for_service"] = (
            isinstance(signals, dict)
            and signals.get("backend") is True
            and "backend" in route_methodology_signals
            and isinstance(backend_packet, dict)
            and backend_packet.get("status") == "present_unverified"
        )
    if fixture == "api-migration-repo":
        checks["api_integrations_detected"] = (
            "api_integrations" in _applicable_methodology_domains(methodology_audit)
            and primary_mode == "api_migration"
        )
        checks["api_contract_source_present"] = _api_integrations_contract_present()
    if fixture == "api-external-write-approval":
        recommendations = methodology_audit.get("recommendations", [])
        checks["external_write_approval_required"] = any(
            isinstance(item, dict)
            and item.get("gate") == "external_write_approval_present"
            and item.get("priority") == "P0_blocker"
            for item in recommendations
        )
    if fixture == "swagger-ui-only-api-docs":
        checks["swagger_ui_only_not_api_contract"] = (
            "api_contract_surface" not in audit.get("route_inputs", {}).get("workspace_signals", {}).get("active_surfaces", [])
        )
    if fixture == "agent-metrics-docs-only":
        checks["metrics_loop_not_forced_for_docs_only"] = _metrics_loop_not_forced(audit, methodology_audit)
    if fixture == "agent-metrics-simple-maintenance":
        checks["metrics_loop_not_forced_for_simple_maintenance"] = _metrics_loop_not_forced(audit, methodology_audit)
    if fixture == "agent-metrics-private-data":
        checks["metrics_loop_private_data_blocks_readiness"] = _metrics_loop_private_data_blocks_readiness()
    if fixture == "agent-metrics-uncalibrated-judge":
        checks["metrics_loop_uncalibrated_judge_blocks_candidate"] = _metrics_loop_uncalibrated_judge_blocks_candidate()
    if fixture == "agent-metrics-trace-missing-span":
        checks["metrics_loop_trace_missing_span_blocks_readiness"] = _metrics_loop_trace_missing_span_blocks_readiness()
    if fixture == "graphql-grpc-style-choice":
        recommendations = methodology_audit.get("recommendations", [])
        checks["api_style_choice_not_universal_default"] = any(
            isinstance(item, dict)
            and item.get("gate") == "api_style_choice_recorded"
            for item in recommendations
        )
    if fixture == "database-schema-only":
        db_signals = audit.get("database_data_signals", {})
        checks["database_schema_only_not_safety_proof"] = (
            isinstance(db_signals, dict)
            and db_signals.get("schema_sources", {}).get("status") == "present_unverified"
            and db_signals.get("migration_sources", {}).get("status") == "applicable_missing"
            and "present_verified" not in db_signals.get("note", "")
        )
    if fixture == "database-destructive-migration":
        recommendations = methodology_audit.get("recommendations", [])
        checks["database_destructive_change_requires_approval"] = any(
            isinstance(item, dict)
            and item.get("gate") == "database_production_access_approval_present"
            and item.get("priority") == "P0_blocker"
            for item in recommendations
        )
    if fixture == "database-production-access-approval":
        recommendations = methodology_audit.get("recommendations", [])
        checks["database_production_access_requires_approval"] = any(
            isinstance(item, dict)
            and item.get("gate") == "database_production_access_approval_present"
            and "approval_required" in str(item.get("approval_boundary", ""))
            for item in recommendations
        )
    if fixture == "database-lineage-rag-overlap":
        db_signals = audit.get("database_data_signals", {})
        checks["database_lineage_rag_overlap_present_unverified"] = (
            isinstance(db_signals, dict)
            and db_signals.get("lineage_sources", {}).get("status") == "present_unverified"
            and db_signals.get("rag_ingestion_sources", {}).get("status") == "present_unverified"
            and db_signals.get("pipeline_sources", {}).get("status") == "present_unverified"
        )
    if fixture == "security-auth-payment":
        recommendations = methodology_audit.get("recommendations", [])
        checks["security_privacy_compliance_detected"] = (
            "security_privacy_compliance" in _applicable_methodology_domains(methodology_audit)
            and isinstance(signals, dict)
            and signals.get("security_privacy_compliance") is True
            and _security_privacy_compliance_contract_present()
        )
        checks["security_sensitive_approval_required"] = any(
            isinstance(item, dict)
            and item.get("domain") == "security_privacy_compliance"
            and item.get("gate") == "external_write_approval_present"
            and item.get("priority") == "P0_blocker"
            and "approval_required" in str(item.get("approval_boundary", ""))
            for item in recommendations
        )
        checks["security_privacy_fixture_safe"] = _security_fixture_privacy_safe(FIXTURES / fixture)
    if fixture == "security-docs-only-mention":
        checks["security_docs_only_not_forced"] = (
            "security_privacy_compliance" not in _applicable_methodology_domains(methodology_audit)
            and isinstance(signals, dict)
            and signals.get("security_privacy_compliance") is False
            and "security_privacy_compliance" not in route_methodology_signals
        )
    if fixture == "security-compliance-claim":
        intent_audit = build_methodology_audit(FIXTURES / fixture, intent_hint=_fixture_text(FIXTURES / fixture))
        checks["unsupported_security_claims_rejected"] = any(
            isinstance(item, dict)
            and item.get("domain") == "security_privacy_compliance"
            and item.get("gate") == "security_unsupported_claims_rejected"
            and item.get("priority") == "P1_high_risk"
            for item in intent_audit.get("recommendations", [])
        )
    if fixture == "security-ci-sbom":
        security_signals = audit.get("security_sensitive_signals", {})
        checks["security_supply_chain_ci_sbom_present_unverified"] = (
            "security_privacy_compliance" in _applicable_methodology_domains(methodology_audit)
            and isinstance(security_signals, dict)
            and security_signals.get("supply_chain", {}).get("status") == "present_unverified"
            and security_signals.get("sbom_provenance", {}).get("status") == "present_unverified"
            and security_signals.get("ci_permissions", {}).get("status") == "present_unverified"
        )
    if fixture == "package-release":
        recommendations = methodology_audit.get("recommendations", [])
        checks["delivery_release_operations_detected"] = (
            "delivery_release_operations" in _applicable_methodology_domains(methodology_audit)
            and _delivery_release_operations_contract_present()
        )
        checks["release_approval_required"] = any(
            isinstance(item, dict)
            and item.get("domain") == "delivery_release_operations"
            and item.get("gate") == "external_release_approval_present"
            and item.get("priority") == "P0_blocker"
            and "approval_required" in str(item.get("approval_boundary", ""))
            for item in recommendations
        )
        checks["artifact_manifest_contract_present"] = "release-artifact-manifest.md" in "\n".join(
            str(item.get("artifact", ""))
            for item in recommendations
            if isinstance(item, dict) and item.get("domain") == "delivery_release_operations"
        )
        checks["release_evidence_before_completion_contract_present"] = any(
            isinstance(item, dict)
            and item.get("domain") == "delivery_release_operations"
            and item.get("gate") == "release_evidence_before_completion"
            for item in recommendations
        )
        checks["rollout_rollback_operations_terms_present"] = all(
            term in DELIVERY_RELEASE_OPERATIONS_TERMS
            for term in [
                "rollout strategy",
                "rollback/recovery",
                "operations runbook",
                "incident response",
                "post-release measurement",
            ]
        )
        checks["final_delivery_depth_terms_present"] = all(
            term in DELIVERY_RELEASE_OPERATIONS_TERMS
            for term in [
                "release mode policy",
                "build-release-run boundary",
                "platform distribution evidence",
                "release communication",
                "versioning tooling decision",
                "github environment controls",
                "dora measurement design",
                "incident postmortem learning",
                "observability on-call tooling",
                "release integrity security handoff",
                "owner-reviewed release evidence sufficiency",
            ]
        )
    if fixture == "release-mobile-signing-only":
        intent_audit = build_methodology_audit(FIXTURES / fixture, intent_hint=_fixture_text(FIXTURES / fixture))
        recommendations = intent_audit.get("recommendations", [])
        checks["mobile_signing_only_requires_platform_owner_evidence"] = any(
            isinstance(item, dict)
            and item.get("domain") == "delivery_release_operations"
            and item.get("gate") == "platform_distribution_evidence_present"
            and "platform owner evidence" in "\n".join(
                str(term) for term in item.get("evidence_required", [])
            )
            for item in recommendations
        )
    if fixture == "release-dora-individual-quota":
        intent_audit = build_methodology_audit(FIXTURES / fixture, intent_hint=_fixture_text(FIXTURES / fixture))
        checks["dora_individual_quota_rejected"] = any(
            isinstance(item, dict)
            and item.get("domain") == "delivery_release_operations"
            and item.get("gate") == "delivery_unsupported_claims_rejected"
            and item.get("priority") == "P1_high_risk"
            for item in intent_audit.get("recommendations", [])
        )
    if fixture == "release-tooling-only":
        delivery_signals = audit.get("delivery_release_operations_signals", {})
        intent_audit = build_methodology_audit(FIXTURES / fixture, intent_hint=_fixture_text(FIXTURES / fixture))
        recommendations = intent_audit.get("recommendations", [])
        checks["release_tooling_only_stays_present_unverified"] = (
            isinstance(delivery_signals, dict)
            and delivery_signals.get("versioning_tooling_status") == "present_unverified"
            and delivery_signals.get("observability_on_call_tooling_status") == "present_unverified"
            and any(
                isinstance(item, dict)
                and item.get("domain") == "delivery_release_operations"
                and item.get("gate") == "versioning_tooling_decision_present"
                for item in recommendations
            )
            and any(
                isinstance(item, dict)
                and item.get("domain") == "delivery_release_operations"
                and item.get("gate") == "observability_on_call_tooling_present"
                for item in recommendations
            )
        )
    if fixture in {
        "rag-quality-regression",
        "ai-prompt-model-change",
        "ai-tool-approval",
        "ai-structured-output",
        "ai-agent-trace",
        "ai-latency-cost-budget",
    }:
        llm_signals = audit.get("llm_ai_rag_signals", {})
        readiness = audit.get("methodology_applicability", {}).get("llm_ai_rag_readiness", {})
        checks["llm_ai_rag_detected"] = (
            "llm_ai_rag" in _applicable_methodology_domains(methodology_audit)
            and isinstance(llm_signals, dict)
            and llm_signals.get("verification_status") == "applicable_missing"
            and isinstance(readiness, dict)
            and readiness.get("status") == "present_unverified"
        )
        checks["llm_ai_rag_contract_present"] = _llm_ai_rag_contract_present()
        checks["llm_ai_rag_privacy_safe_fixture"] = _ai_rag_fixture_privacy_safe(FIXTURES / fixture)
    if fixture == "cross-domain-small-pii-app":
        checks["small_pii_security_without_complexity"] = _small_pii_security_without_complexity(
            audit,
            methodology_audit,
        )
    if fixture == "cross-domain-complex-monorepo-no-prod":
        checks["complex_monorepo_without_production_release_blockers"] = (
            _complex_monorepo_without_production_release_blockers(audit, methodology_audit)
        )
    if fixture == "internal-cli-no-heavy-methodology":
        checks["internal_cli_no_ui_api_release_hard_blockers"] = (
            _internal_cli_no_ui_api_release_hard_blockers(methodology_audit)
        )
    if fixture == "cross-domain-ai-rag-data-security":
        checks["ai_rag_data_security_overlap_present_unverified"] = (
            _ai_rag_data_security_overlap_present_unverified(audit, methodology_audit)
        )
    if fixture == "package-release-security-handoff":
        checks["package_release_security_handoff_prioritized"] = (
            _package_release_security_handoff_prioritized(methodology_audit)
        )
    if fixture == "source-artifact-alias-mapping":
        checks["source_artifact_alias_deferred_mapping_visible"] = (
            _source_artifact_mapping_contract_present(methodology_audit)
        )
    if fixture == "owner-question-dedupe":
        checks["owner_question_dedupe_visible"] = _owner_question_dedupe_contract_present()
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


def _small_pii_security_without_complexity(
    audit: dict[str, Any],
    methodology_audit: dict[str, Any],
) -> bool:
    domains = set(_applicable_methodology_domains(methodology_audit))
    profile = audit.get("complexity_profile", {})
    profile_name = str(profile.get("name", "")) if isinstance(profile, dict) else ""
    return (
        "security_privacy_compliance" in domains
        and profile_name not in {"complex", "large", "enterprise"}
        and not _has_domain_priority(methodology_audit, {"delivery_release_operations"}, {"P0_blocker"})
    )


def _complex_monorepo_without_production_release_blockers(
    audit: dict[str, Any],
    methodology_audit: dict[str, Any],
) -> bool:
    usage_mode = audit.get("usage_mode", {})
    primary_mode = usage_mode.get("primary") if isinstance(usage_mode, dict) else ""
    return (
        primary_mode == "complex_system_acceleration"
        and not _has_domain_priority(methodology_audit, {"delivery_release_operations"}, {"P0_blocker"})
        and not _has_domain_priority(methodology_audit, {"security_privacy_compliance"}, {"P0_blocker"})
    )


def _internal_cli_no_ui_api_release_hard_blockers(methodology_audit: dict[str, Any]) -> bool:
    return not _has_domain_priority(
        methodology_audit,
        {
            "frontend",
            "api_integrations",
            "database_data",
            "security_privacy_compliance",
            "delivery_release_operations",
        },
        {"P0_blocker", "P1_high_risk"},
    )


def _ai_rag_data_security_overlap_present_unverified(
    audit: dict[str, Any],
    methodology_audit: dict[str, Any],
) -> bool:
    domains = set(_applicable_methodology_domains(methodology_audit))
    applicability = audit.get("methodology_applicability", {})
    if not isinstance(applicability, dict):
        return False
    expected_statuses = [
        applicability.get("llm_ai_rag_readiness", {}).get("status"),
        applicability.get("database_data_readiness", {}).get("status"),
        applicability.get("security_privacy_compliance_readiness", {}).get("status"),
    ]
    return (
        {"llm_ai_rag", "database_data", "security_privacy_compliance"}.issubset(domains)
        and all(status == "present_unverified" for status in expected_statuses)
        and "present_verified" not in json.dumps(applicability, sort_keys=True)
    )


def _package_release_security_handoff_prioritized(methodology_audit: dict[str, Any]) -> bool:
    domains = set(_applicable_methodology_domains(methodology_audit))
    groups = methodology_audit.get("recommendation_groups", [])
    artifacts = [
        str(group.get("artifact"))
        for group in groups
        if isinstance(group, dict)
    ]
    safe_next_action = str(methodology_audit.get("safe_next_action", "")).lower()
    return (
        {"delivery_release_operations", "security_privacy_compliance"}.issubset(domains)
        and any(artifact in artifacts for artifact in ["approval-record.md", "security-risk-review.md"])
        and "release-readiness.md" in artifacts
        and (
            "approval" in safe_next_action
            or "security" in safe_next_action
            or "release" in safe_next_action
        )
        and (
            "quality-strategy.md" not in artifacts
            or artifacts.index("release-readiness.md") < artifacts.index("quality-strategy.md")
        )
    )


def _has_domain_priority(
    methodology_audit: dict[str, Any],
    domains: set[str],
    priorities: set[str],
) -> bool:
    recommendations = methodology_audit.get("recommendations", [])
    if not isinstance(recommendations, list):
        return False
    return any(
        isinstance(item, dict)
        and item.get("domain") in domains
        and item.get("priority") in priorities
        for item in recommendations
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
        "codex_agentic_workflow",
        "frontend_methodology",
        "backend_methodology",
        "database_data_readiness",
        "llm_ai_rag_readiness",
        "security_privacy_compliance_readiness",
        "delivery_release_operations_readiness",
        "agent_skill_metrics_loop",
        "methodology_synthesis",
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


def _business_product_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    business_product = domains.get("business_product")
    if not isinstance(business_product, dict):
        return False
    if not set(BUSINESS_PRODUCT_GATES).issubset(set(business_product.get("gates", []))):
        return False
    if not set(BUSINESS_PRODUCT_ARTIFACTS).issubset(set(business_product.get("artifacts", []))):
        return False
    if not set(BUSINESS_PRODUCT_EVAL_FIELDS).issubset(set(business_product.get("eval_fields", []))):
        return False
    if tuple(business_product.get("decision_horizons", [])) != BUSINESS_PRODUCT_DECISION_HORIZONS:
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "product-brief.md",
        TEMPLATE_ROOT / "artifact-templates" / "value-proposition.md",
        TEMPLATE_ROOT / "artifact-templates" / "opportunity-tree.md",
        TEMPLATE_ROOT / "artifact-templates" / "experiment-plan.md",
        TEMPLATE_ROOT / "artifact-templates" / "tracking-plan.md",
        TEMPLATE_ROOT / "artifact-templates" / "metric-spec.md",
        TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "pr" / "release-notes.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "automation-promoter" / "SKILL.md",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in BUSINESS_PRODUCT_TERMS)


def _requirements_domain_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    requirements_domain = domains.get("requirements_domain")
    if not isinstance(requirements_domain, dict):
        return False
    if not set(REQUIREMENTS_DOMAIN_GATES).issubset(set(requirements_domain.get("gates", []))):
        return False
    if not set(REQUIREMENTS_DOMAIN_ARTIFACTS).issubset(set(requirements_domain.get("artifacts", []))):
        return False
    if not set(REQUIREMENTS_DOMAIN_EVAL_FIELDS).issubset(set(requirements_domain.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "requirement-registry.md",
        TEMPLATE_ROOT / "artifact-templates" / "stakeholder-owner-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "story-slice-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "acceptance-scenarios.md",
        TEMPLATE_ROOT / "artifact-templates" / "requirements-traceability-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "business-rules.md",
        TEMPLATE_ROOT / "artifact-templates" / "example-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "domain-modeling.md",
        TEMPLATE_ROOT / "artifact-templates" / "requirement-change-impact.md",
        TEMPLATE_ROOT / "artifact-templates" / "domain-review-record.md",
        TEMPLATE_ROOT / "control-plane" / "REQUIREMENTS.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "agent-team-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in REQUIREMENTS_DOMAIN_TERMS)


def _solution_architecture_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    solution_architecture = domains.get("solution_architecture")
    if not isinstance(solution_architecture, dict):
        return False
    if not set(SOLUTION_ARCHITECTURE_GATES).issubset(set(solution_architecture.get("gates", []))):
        return False
    if not set(SOLUTION_ARCHITECTURE_ARTIFACTS).issubset(set(solution_architecture.get("artifacts", []))):
        return False
    if not set(SOLUTION_ARCHITECTURE_EVAL_FIELDS).issubset(set(solution_architecture.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-overview.md",
        TEMPLATE_ROOT / "artifact-templates" / "adr.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-review-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-fitness-functions.md",
        TEMPLATE_ROOT / "artifact-templates" / "trust-boundary-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-docs-tooling-decision.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-dictionary.md",
        TEMPLATE_ROOT / "artifact-templates" / "security-risk-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "migration-plan.md",
        TEMPLATE_ROOT / "artifact-templates" / "integration-catalog.md",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "agent-team-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in SOLUTION_ARCHITECTURE_TERMS)


def _quality_testing_evals_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    quality = domains.get("quality_testing_evals")
    if not isinstance(quality, dict):
        return False
    if not set(QUALITY_TESTING_EVALS_GATES).issubset(set(quality.get("gates", []))):
        return False
    if not set(QUALITY_TESTING_EVALS_ARTIFACTS).issubset(set(quality.get("artifacts", []))):
        return False
    if not set(QUALITY_TESTING_EVALS_EVAL_FIELDS).issubset(set(quality.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "quality-strategy.md",
        TEMPLATE_ROOT / "artifact-templates" / "test-eval-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "ci-evidence-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "flaky-test-policy.md",
        TEMPLATE_ROOT / "artifact-templates" / "manual-qa-evidence.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in QUALITY_TESTING_EVALS_TERMS)


def _semantic_evidence_sufficiency_contract_present() -> bool:
    paths = [
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in SEMANTIC_EVIDENCE_SUFFICIENCY_TERMS)


def _frontend_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    frontend = domains.get("frontend")
    if not isinstance(frontend, dict):
        return False
    if not set(FRONTEND_GATES).issubset(set(frontend.get("gates", []))):
        return False
    if not set(FRONTEND_ARTIFACTS).issubset(set(frontend.get("artifacts", []))):
        return False
    if not set(FRONTEND_EVAL_FIELDS).issubset(set(frontend.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "frontend-flow-spec.md",
        TEMPLATE_ROOT / "artifact-templates" / "frontend-state-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "frontend-visual-qa.md",
        TEMPLATE_ROOT / "artifact-templates" / "frontend-accessibility-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "frontend-performance-budget.md",
        TEMPLATE_ROOT / "artifact-templates" / "component-card.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in FRONTEND_TERMS)


def _backend_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    backend = domains.get("backend")
    if not isinstance(backend, dict):
        return False
    if not set(BACKEND_GATES).issubset(set(backend.get("gates", []))):
        return False
    if not set(BACKEND_ARTIFACTS).issubset(set(backend.get("artifacts", []))):
        return False
    if not set(BACKEND_EVAL_FIELDS).issubset(set(backend.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "backend-service-overview.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-runtime-behavior.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-dependency-failure-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-observability-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-slo-sheet.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-health-check-contract.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-job-queue-contract.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-data-consistency-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-config-secrets-manifest.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-release-rollback-notes.md",
        TEMPLATE_ROOT / "artifact-templates" / "backend-operational-runbook.md",
        TEMPLATE_ROOT / "artifact-templates" / "architecture-overview.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "quality-strategy.md",
        TEMPLATE_ROOT / "artifact-templates" / "test-eval-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "manual-qa-evidence.md",
        TEMPLATE_ROOT / "artifact-templates" / "security-risk-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "domain-modeling.md",
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in BACKEND_TERMS)


def _api_integrations_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    api = domains.get("api_integrations")
    if not isinstance(api, dict):
        return False
    if not set(API_INTEGRATIONS_GATES).issubset(set(api.get("gates", []))):
        return False
    if not set(API_INTEGRATIONS_ARTIFACTS).issubset(set(api.get("artifacts", []))):
        return False
    if not set(API_INTEGRATIONS_EVAL_FIELDS).issubset(set(api.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "api-inventory.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-contract-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-error-catalog.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-auth-authorization-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-consumer-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-compatibility-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-contract-test-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "generated-sdk-manifest.md",
        TEMPLATE_ROOT / "artifact-templates" / "webhook-event-contract.md",
        TEMPLATE_ROOT / "artifact-templates" / "external-integration-approval.md",
        TEMPLATE_ROOT / "artifact-templates" / "api-style-guide.md",
        TEMPLATE_ROOT / "artifact-templates" / "integration-catalog.md",
        TEMPLATE_ROOT / "artifact-templates" / "migration-plan.md",
        TEMPLATE_ROOT / "artifact-templates" / "security-risk-review.md",
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in API_INTEGRATIONS_TERMS)


def _database_data_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    database = domains.get("database_data")
    if not isinstance(database, dict):
        return False
    if not set(DATABASE_DATA_GATES).issubset(set(database.get("gates", []))):
        return False
    if not set(DATABASE_DATA_ARTIFACTS).issubset(set(database.get("artifacts", []))):
        return False
    if not set(DATABASE_DATA_EVAL_FIELDS).issubset(set(database.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "database-inventory.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-dictionary.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-migration-plan.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-expand-contract-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-backfill-runbook.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-rollback-feasibility.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-backup-restore-evidence.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-data-classification-matrix.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-data-quality-checks.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-data-contract.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-lineage-map.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-query-performance-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-retention-deletion-policy.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-synthetic-fixtures-policy.md",
        TEMPLATE_ROOT / "artifact-templates" / "database-production-access-approval.md",
        TEMPLATE_ROOT / "workflows" / "data-migration.md",
        TEMPLATE_ROOT / "control-plane" / "PLAN.md",
        TEMPLATE_ROOT / "control-plane" / "TEST.md",
        TEMPLATE_ROOT / "control-plane" / "EVALS.md",
        TEMPLATE_ROOT / "control-plane" / "RUNLOG.md",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term.lower() in payload for term in DATABASE_DATA_TERMS)


def _llm_ai_rag_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    ai_rag = domains.get("llm_ai_rag")
    if not isinstance(ai_rag, dict):
        return False
    if not set(LLM_AI_RAG_GATES).issubset(set(ai_rag.get("gates", []))):
        return False
    if not set(LLM_AI_RAG_ARTIFACTS).issubset(set(ai_rag.get("artifacts", []))):
        return False
    if not set(LLM_AI_RAG_EVAL_FIELDS).issubset(set(ai_rag.get("eval_fields", []))):
        return False

    canonical_targets = {
        f".codex/artifact-templates/{name}" for name in LLM_AI_RAG_ARTIFACTS
    }
    rendered_targets = {item.target_path for item in required_templates()}
    if not canonical_targets.issubset(rendered_targets):
        return False
    if any(
        f".codex/artifact-templates/{legacy}" in rendered_targets
        for legacy in AI_RAG_TEMPLATE_ALIASES
    ):
        return False
    if AI_RAG_TEMPLATE_ALIASES != {
        "ai-prompt-contract.md": "prompt-contract.md",
        "ai-model-decision-record.md": "model-decision-record.md",
        "rag-grounding-eval.md": "rag-eval-report.md",
        "agent-handoff-contract.md": "agent-task-packet.md",
    }:
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "workflows" / "ai-eval-regression.md",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
    ]
    paths.extend(TEMPLATE_ROOT / "control-plane" / name for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"])
    paths.extend(TEMPLATE_ROOT / "artifact-templates" / name for name in LLM_AI_RAG_ARTIFACTS)
    if not all(path.exists() for path in paths):
        return False
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in LLM_AI_RAG_TERMS)


def _security_privacy_compliance_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    security = domains.get("security_privacy_compliance")
    if not isinstance(security, dict):
        return False
    if not set(SECURITY_PRIVACY_COMPLIANCE_GATES).issubset(set(security.get("gates", []))):
        return False
    if not set(SECURITY_PRIVACY_COMPLIANCE_ARTIFACTS).issubset(set(security.get("artifacts", []))):
        return False
    if not set(SECURITY_PRIVACY_COMPLIANCE_EVAL_FIELDS).issubset(set(security.get("eval_fields", []))):
        return False

    canonical_targets = {
        f".codex/artifact-templates/{name}" for name in SECURITY_PRIVACY_COMPLIANCE_ARTIFACTS
    }
    rendered_targets = {item.target_path for item in required_templates()}
    if not canonical_targets.issubset(rendered_targets):
        return False
    if any(
        f".codex/artifact-templates/{source_name}" in rendered_targets
        for source_name in SECURITY_TEMPLATE_ALIASES
    ):
        return False
    if SECURITY_TEMPLATE_ALIASES != {
        "threat-model.md": "threat-surface.md",
        "asvs-mapping.md": "asvs-ssdf-mapping.md",
        "secrets-inventory.md": "secrets-policy.md",
        "authz-matrix.md": "authz-negative-test-matrix.md",
        "audit-log-policy.md": "audit-logging-review.md",
        "compliance-applicability-matrix.md": "compliance-overlay.md",
    }:
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "source_policy.py",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
    ]
    paths.extend(TEMPLATE_ROOT / "control-plane" / name for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"])
    paths.extend(TEMPLATE_ROOT / "artifact-templates" / name for name in SECURITY_PRIVACY_COMPLIANCE_ARTIFACTS)
    if not all(path.exists() for path in paths):
        return False
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term.lower() in payload for term in SECURITY_PRIVACY_COMPLIANCE_TERMS)


def _delivery_release_operations_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    delivery = domains.get("delivery_release_operations")
    if not isinstance(delivery, dict):
        return False
    if not set(DELIVERY_RELEASE_OPERATIONS_GATES).issubset(set(delivery.get("gates", []))):
        return False
    if not set(DELIVERY_RELEASE_OPERATIONS_ARTIFACTS).issubset(set(delivery.get("artifacts", []))):
        return False
    if not set(DELIVERY_RELEASE_OPERATIONS_EVAL_FIELDS).issubset(set(delivery.get("eval_fields", []))):
        return False

    rendered_targets = {item.target_path for item in required_templates()}
    artifact_targets = {
        f".codex/artifact-templates/{name}"
        for name in DELIVERY_RELEASE_OPERATIONS_ARTIFACTS
        if name not in {"automation-candidate.md"}
    }
    if not artifact_targets.issubset(rendered_targets):
        return False
    if ".codex/automation-candidates/automation-candidate.md" not in rendered_targets:
        return False
    if any(
        f".codex/artifact-templates/{source_name}" in rendered_targets
        for source_name in DELIVERY_TEMPLATE_ALIASES
    ):
        return False
    if DELIVERY_TEMPLATE_ALIASES != {
        "release-scope.md": "release-readiness.md",
        "version-impact-record.md": "versioning-policy.md",
        "artifact-manifest.md": "release-artifact-manifest.md",
        "rollout-strategy.md": "rollout-plan.md",
        "ci-cd-governance.md": "ci-cd-workflow-inventory.md",
        "incident-response-path.md": "incident-record.md",
        "post-release-measurement.md": "post-release-review.md",
    }:
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "workflows" / "release-packet.md",
        TEMPLATE_ROOT / "workflows" / "release-packaging.md",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
        TEMPLATE_ROOT / "evals" / "project-readiness.json",
        TEMPLATE_ROOT / "automations" / "automation-candidate.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_report.py",
        PLUGIN_ROOT / "skills" / "workspace-discovery-auditor" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "project-lifecycle-orchestrator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "requirements-author" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "implementation-planner" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "test-eval-designer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "risk-reviewer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "automation-promoter" / "SKILL.md",
    ]
    paths.extend(TEMPLATE_ROOT / "control-plane" / name for name in ["PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"])
    paths.extend(
        TEMPLATE_ROOT / "artifact-templates" / name
        for name in DELIVERY_RELEASE_OPERATIONS_ARTIFACTS
        if name != "automation-candidate.md"
    )
    if not all(path.exists() for path in paths):
        return False
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term.lower() in payload for term in DELIVERY_RELEASE_OPERATIONS_TERMS)


def _fixture_text(path: Path) -> str:
    if not path.is_dir():
        return ""
    return "\n".join(
        item.read_text(encoding="utf-8", errors="ignore")
        for item in path.rglob("*")
        if item.is_file()
    )


def _security_fixture_privacy_safe(path: Path) -> bool:
    lowered = _fixture_text(path).lower()
    forbidden = [
        "private customer",
        "raw private chat",
        "raw pii",
        "payment data",
        "token=",
        "api_key",
        "sk-",
        "begin private key",
    ]
    return bool(lowered) and all(term not in lowered for term in forbidden)


def _ai_rag_fixture_privacy_safe(path: Path) -> bool:
    if not path.is_dir():
        return False
    payload = "\n".join(
        item.read_text(encoding="utf-8")
        for item in path.rglob("*")
        if item.is_file()
    )
    lowered = payload.lower()
    forbidden = (
        "sk-",
        "token=",
        "api_key",
        "begin private key",
        "password=",
        "private customer",
        "raw private chat",
    )
    return "synthetic" in payload and not any(marker in lowered for marker in forbidden)


def _project_graph_sample() -> dict[str, Any]:
    global _PROJECT_GRAPH_SAMPLE_CACHE
    if _PROJECT_GRAPH_SAMPLE_CACHE is None:
        _PROJECT_GRAPH_SAMPLE_CACHE = build_project_code_graph(FIXTURES / "project-code-graph-minimal-python")
    return _PROJECT_GRAPH_SAMPLE_CACHE


def _project_graph_cockpit() -> dict[str, Any]:
    global _PROJECT_GRAPH_COCKPIT_CACHE
    if _PROJECT_GRAPH_COCKPIT_CACHE is None:
        _PROJECT_GRAPH_COCKPIT_CACHE = render_project_graph_cockpit(_project_graph_sample())
    return _PROJECT_GRAPH_COCKPIT_CACHE


def _project_graph_contract_present() -> bool:
    graph = _project_graph_sample()
    cockpit = _project_graph_cockpit()
    serialized = json.dumps(graph, sort_keys=True).lower()
    return (
        graph.get("schema_version") == 1
        and graph.get("write_policy") == "read_only"
        and graph.get("validation", {}).get("ok") is True
        and graph.get("metadata", {}).get("source_boundary") == "raw_source_bodies_excluded"
        and graph.get("metadata", {}).get("generated_view_policy") == "html_is_review_only"
        and bool(graph.get("artifact_targets", {}).get("json"))
        and bool(graph.get("artifact_targets", {}).get("jsonl"))
        and '"raw_source":' not in serialized
        and "return 'ok'" not in serialized
        and cockpit.get("validation", {}).get("ok") is True
    )


def _project_graph_no_external_assets() -> bool:
    html = str(_project_graph_cockpit().get("html") or "").lower()
    forbidden = ["http://", "https://", "<script src", "fetch(", "xmlhttprequest", "sendbeacon"]
    return bool(html) and all(marker not in html for marker in forbidden)


def _project_graph_redaction_present() -> bool:
    unsafe_graph = {
        "schema_version": 1,
        "write_policy": "read_only",
        "metadata": {
            "scan_id": "scan-unsafe",
            "source_boundary": "raw_source_bodies_excluded",
            "generated_view_policy": "html_is_review_only",
            "node_count": 1,
            "edge_count": 0,
            "observation_count": 0,
        },
        "nodes": [
            {
                "id": "file:unsafe.py",
                "type": "module",
                "label": "TOKEN=fixture-secret C:\\Users\\person\\private.py",
                "status": "current",
                "language": "python",
                "path": "C:\\Users\\person\\private.py",
            }
        ],
        "edges": [],
        "observations": [],
    }
    rendered = render_project_graph_cockpit(unsafe_graph)
    payload = str(rendered.get("html") or "") + str(rendered.get("json") or "")
    lowered = payload.lower()
    return (
        rendered.get("validation", {}).get("ok") is True
        and "fixture-secret" not in lowered
        and "c:\\users\\person" not in lowered
        and "private.py" not in lowered
    )


def _project_graph_scale_bounds_present(fixture_path: Path | None = None) -> bool:
    paths = (
        [fixture_path]
        if fixture_path is not None
        else [
            FIXTURES / "project-code-graph-scale-1k",
            FIXTURES / "project-code-graph-scale-5k",
            FIXTURES / "project-code-graph-scale-10k",
        ]
    )
    for path in paths:
        if path is None or not (path / "scale.json").exists():
            return False
        graph = build_synthetic_project_graph_from_fixture(path)
        metadata = graph.get("metadata", {}) if isinstance(graph.get("metadata"), dict) else {}
        if not (
            graph.get("validation", {}).get("ok") is True
            and len(graph.get("nodes", [])) <= 250
            and metadata.get("scale_policy") == "large_graph_payload_is_bounded"
            and int(metadata.get("omitted_node_count") or 0) >= 0
        ):
            return False
    return True


def _project_graph_generated_view_only(fixture_path: Path | None = None) -> bool:
    if fixture_path is not None and (fixture_path / "scale.json").exists():
        graph = build_synthetic_project_graph_from_fixture(fixture_path)
        return graph.get("metadata", {}).get("generated_view_policy") == "html_is_review_only"
    cockpit = _project_graph_cockpit()
    payload = str(cockpit.get("html") or "").lower() + str(cockpit.get("json") or "").lower()
    return (
        "generated review view only" in payload
        and "not source of truth" in payload
        and "cannot approve, apply, or prove work complete" in payload
    )


def _project_graph_eight_page_cockpit_present() -> bool:
    cockpit = _project_graph_cockpit().get("cockpit", {})
    pages = cockpit.get("pages") if isinstance(cockpit, dict) else []
    labels = [page.get("label") for page in pages if isinstance(page, dict)]
    return labels == [
        "Overview",
        "Project Map",
        "Docs & Sources",
        "Code Intelligence",
        "Contracts",
        "Quality & Metrics",
        "Operations & Risk",
        "Proposal Ledger",
    ]


def _project_graph_section_preservation_present() -> bool:
    cockpit = _project_graph_cockpit().get("cockpit", {})
    pages = cockpit.get("pages") if isinstance(cockpit, dict) else []
    section_ids = [
        section.get("id")
        for page in pages
        if isinstance(page, dict)
        for section in page.get("sections", [])
        if isinstance(section, dict)
    ]
    code_intelligence = next(
        (page for page in pages if isinstance(page, dict) and page.get("id") == "code-intelligence"),
        {},
    )
    code_section_ids = [
        section.get("id")
        for section in code_intelligence.get("sections", [])
        if isinstance(section, dict)
    ]
    return (
        len(section_ids) == len(set(section_ids))
        and "code-flow" in code_section_ids
        and "visual-projection" in section_ids
        and "selected-node-evidence" in section_ids
    )


def _project_graph_cockpit_generated_view_boundary_present() -> bool:
    cockpit = _project_graph_cockpit()
    payload = json.loads(str(cockpit.get("json") or "{}"))
    return (
        payload.get("write_policy") == "read_only"
        and "review output only" in str(payload.get("source_policy") or "").lower()
        and payload.get("generated_view_policy")
        == "Generated review view only. It is not source of truth and cannot approve, apply, or prove work complete."
    )


def _project_graph_search_quality_packet() -> dict[str, Any]:
    return evaluate_project_graph_search_quality(
        _project_graph_sample(),
        cases=[
            {
                "id": "symbol-worker",
                "query": "search",
                "text": "app.worker.run",
                "expected_node_ids": ["function:app.worker.run"],
                "top_k": 3,
            },
            {
                "id": "trace-test-to-worker",
                "query": "trace",
                "source_id": "function:tests.test_worker.test_run",
                "target_id": "function:app.worker.run",
                "expected_status": "ok",
            },
            {
                "id": "affected-tests-worker",
                "query": "affected_tests",
                "node_id": "function:app.worker.run",
                "expected_test_ids": [
                    "file:tests/test_worker.py",
                    "function:tests.test_worker.test_run",
                ],
            },
        ],
        thresholds={
            "min_symbol_recall": 1.0,
            "min_top_k_mrr": 1.0,
            "min_trace_success_rate": 1.0,
            "min_affected_test_precision": 1.0,
            "max_edge_density": 4.0,
        },
    )


def _project_graph_static_index() -> dict[str, Any]:
    return build_static_search_index(_project_graph_sample())


def _project_graph_static_search_index_present() -> bool:
    index = _project_graph_static_index()
    packet = query_static_search_index(
        index,
        {
            "text": "worker run",
            "node_types": ["function"],
            "path_prefixes": ["app/"],
            "max_results": 3,
            "max_tokens": 800,
        },
    )
    payload = json.dumps([index, packet], sort_keys=True).lower()
    return (
        index.get("validation", {}).get("ok") is True
        and index.get("artifact_kind") == "project_graph_static_search_index"
        and index.get("source_boundary") == "graph_artifact_only_raw_source_excluded"
        and index.get("generated_view_policy") == "static_search_index_is_generated_cache_not_source_of_truth"
        and index.get("approval_boundary") == "batch19_explicit_offline_static_index_no_live_backend_model_or_database"
        and index.get("query_policy", {}).get("no_live_database_or_server") is True
        and index.get("query_policy", {}).get("no_llm_embedding_or_cross_encoder") is True
        and packet.get("search_backend") == "static_index"
        and packet.get("status") == "ok"
        and packet.get("nodes", [{}])[0].get("id") == "function:app.worker.run"
        and "return 'ok'" not in payload
        and "c:\\users" not in payload
    )


def _project_graph_static_search_index_quality_present() -> bool:
    packet = evaluate_project_graph_search_quality(
        _project_graph_sample(),
        static_index=_project_graph_static_index(),
        cases=[
            {
                "id": "symbol-worker-indexed",
                "query": "search",
                "text": "worker run",
                "expected_node_ids": ["function:app.worker.run"],
                "unexpected_node_ids": ["function:tests.test_worker.test_run"],
                "top_k": 3,
            },
            {
                "id": "trace-test-to-worker",
                "query": "trace",
                "source_id": "function:tests.test_worker.test_run",
                "target_id": "function:app.worker.run",
                "expected_status": "ok",
            },
            {
                "id": "affected-tests-worker",
                "query": "affected_tests",
                "node_id": "function:app.worker.run",
                "expected_test_ids": [
                    "file:tests/test_worker.py",
                    "function:tests.test_worker.test_run",
                ],
            },
        ],
        thresholds={
            "min_symbol_recall": 1.0,
            "min_top_k_mrr": 1.0,
            "min_trace_success_rate": 1.0,
            "min_affected_test_precision": 1.0,
            "max_index_false_positive_rate": 0.0,
            "max_edge_density": 4.0,
            "max_edge_density_delta": 0.0,
        },
    )
    comparison = packet.get("index_comparison", {}) if isinstance(packet.get("index_comparison"), dict) else {}
    return (
        packet.get("decision_status") == "passed"
        and comparison.get("search_backend") == "static_index"
        and comparison.get("false_positive_rate") == 0.0
        and comparison.get("edge_density_delta") == 0.0
        and packet.get("failed_thresholds") == []
    )


def _project_graph_backend_approval() -> dict[str, Any]:
    return {
        "explicit_approval": True,
        "storage_path": LOCAL_BACKEND_TARGET,
        "port_policy": {"host": "127.0.0.1", "port": 0, "mode": "disabled_by_default"},
        "process_lifecycle": {
            "server_enabled_by_default": False,
            "start_requires_explicit_command": True,
            "pid_path": ".codex/product-agent-os/project-code-graph-backend.pid",
        },
        "auth_boundary": {"local_only": True, "write_controls": False},
        "cleanup": {"delete_generated_store": True},
        "logging": {
            "log_path": ".codex/product-agent-os/project-code-graph-backend.log",
            "redacted": True,
        },
        "performance_threshold": {"max_query_ms": 250, "max_payload_tokens": 4000},
        "rollback_path": f"delete {LOCAL_BACKEND_TARGET}",
    }


def _project_graph_backend_store() -> dict[str, Any]:
    return build_local_query_backend_store(
        _project_graph_sample(),
        static_index=_project_graph_static_index(),
        approval=_project_graph_backend_approval(),
    )


def _project_graph_local_backend_gate_present() -> bool:
    store = _project_graph_backend_store()
    query = handle_backend_api_request(
        store,
        {"method": "POST", "path": "/query", "body": {"query": "search", "text": "worker run", "max_results": 3}},
    )
    payload = json.dumps([store, query], sort_keys=True).lower()
    return (
        validate_local_query_backend_store(store).get("ok") is True
        and store.get("artifact_kind") == "project_graph_local_query_backend"
        and store.get("approval_boundary") == "batch20_explicit_local_backend_gate_no_active_server_default"
        and store.get("source_boundary") == "graph_and_static_index_artifacts_only_raw_source_excluded"
        and query.get("query_backend") == "local_file_store"
        and query.get("status") == "ok"
        and "return 'ok'" not in payload
        and "c:\\users" not in payload
    )


def _project_graph_backend_decision_packet_present() -> bool:
    store = _project_graph_backend_store()
    approval = _project_graph_backend_approval()
    required_approval_fields = {
        "explicit_approval",
        "storage_path",
        "port_policy",
        "process_lifecycle",
        "auth_boundary",
        "cleanup",
        "logging",
        "performance_threshold",
        "rollback_path",
    }
    return (
        required_approval_fields.issubset(approval)
        and store.get("approval_boundary") == "batch20_explicit_local_backend_gate_no_active_server_default"
        and store.get("storage", {}).get("storage_path") == LOCAL_BACKEND_TARGET
        and store.get("performance_threshold", {}).get("max_query_ms") == 250
    )


def _project_graph_backend_disabled_by_default() -> bool:
    lifecycle = _project_graph_backend_store().get("server_lifecycle", {})
    return (
        lifecycle.get("server_status") == "disabled_by_default"
        and lifecycle.get("active_process") is False
        and lifecycle.get("host") == "127.0.0.1"
        and lifecycle.get("port") == 0
        and lifecycle.get("start_requires_explicit_command") is True
    )


def _project_graph_backend_operational_controls_present() -> bool:
    store = _project_graph_backend_store()
    eval_packet = evaluate_backend_query_contract(
        store,
        [{"query": "search", "text": "worker", "max_results": 3}],
        thresholds={"max_query_ms": 250, "max_payload_tokens": 4000},
    )
    return (
        store.get("api_contract", {}).get("stable_json_errors") is True
        and store.get("api_contract", {}).get("external_network_dependency") is False
        and store.get("storage", {}).get("cleanup_command") == f"delete {LOCAL_BACKEND_TARGET}"
        and store.get("server_lifecycle", {}).get("log_path") == ".codex/product-agent-os/project-code-graph-backend.log"
        and eval_packet.get("status") == "ok"
        and eval_packet.get("concurrency", {}).get("deterministic_read_results") is True
    )


def _project_graph_backend_graph_only_fallback_present() -> bool:
    store = _project_graph_backend_store()
    graph_packet = query_project_graph(_project_graph_sample(), {"query": "search", "text": "worker", "max_results": 3})
    return (
        store.get("rollback", {}).get("fallback") == "graph_only_query_mode"
        and graph_packet.get("status") == "ok"
        and graph_packet.get("result_kind") == "search"
    )


def _project_graph_backend_no_production_or_source_truth_claims() -> bool:
    store = _project_graph_backend_store()
    payload = json.dumps(store, sort_keys=True).lower()
    forbidden = [
        "production server",
        "source of truth database",
        "server_status\": \"running",
        "active_process\": true",
        "0.0.0.0",
        "https://",
        "http://",
    ]
    return (
        store.get("generated_view_policy") == "local_backend_store_is_generated_cache_not_source_of_truth"
        and not any(term in payload for term in forbidden)
    )


def _project_graph_semantic_approval() -> dict[str, Any]:
    return {
        "explicit_approval": True,
        "storage_path": SEMANTIC_RETRIEVAL_TARGET,
        "embedding_provider": "local_deterministic",
        "embedding_model": {
            "name": "local-hash-embedding-v1",
            "version": "1",
            "dimension": 64,
            "external_model_calls_allowed": False,
        },
        "cross_encoder": {
            "provider": "local_deterministic",
            "model": "local-lexical-cross-encoder-v1",
            "enabled": True,
            "external_model_calls_allowed": False,
        },
        "data_classification": {
            "allowed_inputs": ["redacted_graph_labels", "static_index_terms", "observation_ids"],
            "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
        },
        "redaction_policy": {
            "raw_source_excluded": True,
            "secrets_redacted": True,
            "absolute_paths_redacted": True,
        },
        "cache_policy": {
            "cache_status": "generated",
            "fingerprint_scope": "canonical_redacted_graph_and_static_index",
            "stale_policy": "block_if_graph_fingerprint_mismatch",
            "ttl_days": 30,
        },
        "token_budget": {"max_query_tokens": 1200, "max_corpus_record_tokens": 120},
        "eval_threshold": {
            "min_recall_at_k": 1.0,
            "min_mrr": 1.0,
            "min_cross_encoder_mrr_delta": 0.0,
            "max_false_positive_rate": 0.0,
            "max_query_ms": 250,
            "max_payload_tokens": 1200,
        },
        "failure_handling": {"on_stale_or_failed_eval": "block_and_fallback_to_lexical_or_graph"},
        "rollback_path": f"delete {SEMANTIC_RETRIEVAL_TARGET}",
    }


def _project_graph_semantic_index() -> dict[str, Any]:
    return build_semantic_retrieval_index(
        _project_graph_sample(),
        static_index=_project_graph_static_index(),
        approval=_project_graph_semantic_approval(),
    )


def _project_graph_semantic_retrieval_gate_present() -> bool:
    approval = _project_graph_semantic_approval()
    semantic_index = _project_graph_semantic_index()
    packet = query_semantic_retrieval(
        semantic_index,
        {"query": "search", "text": "worker run", "node_types": ["function"], "path_prefixes": ["app/"]},
        graph=_project_graph_sample(),
    )
    payload = json.dumps([semantic_index, packet], sort_keys=True).lower()
    return (
        validate_semantic_retrieval_approval(approval).get("ok") is True
        and validate_semantic_retrieval_index(semantic_index).get("ok") is True
        and semantic_index.get("artifact_kind") == "project_graph_semantic_retrieval_index"
        and semantic_index.get("approval_boundary") == "batch21_explicit_semantic_retrieval_gate"
        and semantic_index.get("model_decision", {}).get("embedding_provider") == "local_deterministic"
        and semantic_index.get("model_decision", {}).get("cross_encoder_provider") == "local_deterministic"
        and semantic_index.get("model_decision", {}).get("external_model_calls_allowed") is False
        and semantic_index.get("corpus_policy", {}).get("semantic_corpus_and_chunk_policy")
        == "redacted_graph_labels_static_index_terms_observation_ids_only"
        and semantic_index.get("embedding", {}).get("cache_kind") == "embeddings_cache_metadata"
        and packet.get("search_backend") == "semantic_retrieval"
        and packet.get("nodes", [{}])[0].get("id") == "function:app.worker.run"
        and "return 'ok'" not in payload
        and "c:\\users" not in payload
    )


def _project_graph_semantic_retrieval_eval_present() -> bool:
    semantic_index = _project_graph_semantic_index()
    packet = evaluate_semantic_retrieval_quality(
        semantic_index,
        graph=_project_graph_sample(),
        cases=[
            {
                "id": "semantic-worker",
                "text": "worker run",
                "expected_node_ids": ["function:app.worker.run"],
                "unexpected_node_ids": ["function:tests.test_worker.test_run"],
                "top_k": 3,
            }
        ],
        thresholds={
            "min_recall_at_k": 1.0,
            "min_mrr": 1.0,
            "min_cross_encoder_mrr_delta": 0.0,
            "max_false_positive_rate": 0.0,
            "max_query_ms": 250,
            "max_payload_tokens": 1200,
        },
    )
    return (
        packet.get("decision_status") == "passed"
        and packet.get("search_backend") == "semantic_retrieval"
        and packet.get("quality_metrics", {}).get("recall_at_k") == 1.0
        and packet.get("quality_metrics", {}).get("mrr") == 1.0
        and packet.get("quality_metrics", {}).get("false_positive_rate") == 0.0
        and packet.get("failed_thresholds") == []
    )


def _project_graph_semantic_present_unverified_routing_present() -> bool:
    semantic_index = _project_graph_semantic_index()
    packet = query_project_graph(
        _project_graph_sample(),
        {"query": "search", "text": "worker run", "max_results": 3},
        semantic_index=semantic_index,
    )
    payload = json.dumps([semantic_index, packet], sort_keys=True).lower()
    return (
        semantic_index.get("query_policy", {}).get("semantic_hits_confidence") == "present_unverified"
        and semantic_index.get("cross_encoder", {}).get("canonical_graph_edge_rewrites") is False
        and semantic_index.get("rollback", {}).get("disable_path") == f"delete {SEMANTIC_RETRIEVAL_TARGET}"
        and packet.get("nodes", [{}])[0].get("confidence") == "present_unverified"
        and "semantic matches alone" in packet.get("safe_next_action", "")
        and "canonical graph edge rewrites" not in payload
    )


def _project_graph_llm_extraction_approval() -> dict[str, Any]:
    return {
        "explicit_approval": True,
        "storage_path": LLM_EXTRACTION_TARGET,
        "extraction_schema": {
            "semantic_nodes": True,
            "semantic_edges": True,
            "rationale_comments": True,
            "review_required": True,
        },
        "prompt_model_policy": {
            "provider": "local_deterministic",
            "model": "local-proposal-extractor-v1",
            "version": "1",
            "sampling": {"temperature": 0},
            "external_model_calls_allowed": False,
            "approved_context": ["redacted_graph_artifact", "semantic_retrieval_index"],
            "output_format": "structured_json",
        },
        "redaction_policy": {
            "raw_source_excluded": True,
            "private_comments_excluded": True,
            "secrets_redacted": True,
            "absolute_paths_redacted": True,
            "unsupported_claims_labelled": True,
        },
        "cache_policy": {
            "cache_status": "generated",
            "fingerprint_scope": "redacted_graph_semantic_index_prompt_policy",
            "stale_policy": "block_if_graph_or_semantic_fingerprint_mismatch",
            "ttl_days": 30,
        },
        "token_budget": {"max_prompt_tokens": 1500, "max_output_tokens": 1500, "max_cost_units": 0},
        "eval_threshold": {
            "min_precision": 1.0,
            "max_unsupported_claim_rate": 0.0,
            "max_privacy_violations": 0,
            "max_latency_ms": 250,
        },
        "incident_path": "disable extraction and record AI incident workflow",
        "owner": "product-agent-owner",
        "rollback_path": f"delete {LLM_EXTRACTION_TARGET}",
    }


def _project_graph_llm_extraction_proposals() -> dict[str, Any]:
    return build_llm_extraction_proposals(
        _project_graph_sample(),
        semantic_index=_project_graph_semantic_index(),
        approval=_project_graph_llm_extraction_approval(),
    )


def _project_graph_llm_extraction_gate_present() -> bool:
    approval = _project_graph_llm_extraction_approval()
    proposals = _project_graph_llm_extraction_proposals()
    payload = json.dumps(proposals, sort_keys=True).lower()
    return (
        validate_llm_extraction_approval(approval).get("ok") is True
        and validate_llm_extraction_proposals(proposals).get("ok") is True
        and proposals.get("artifact_kind") == "project_graph_llm_extraction_proposals"
        and proposals.get("approval_boundary") == "batch22_explicit_llm_semantic_extraction_gate"
        and proposals.get("model_policy", {}).get("provider") == "local_deterministic"
        and proposals.get("model_policy", {}).get("external_model_calls_allowed") is False
        and proposals.get("canonical_graph_mutation") == "forbidden"
        and "return 'ok'" not in payload
        and "c:\\users" not in payload
    )


def _project_graph_llm_proposal_schema_present() -> bool:
    proposals = _project_graph_llm_extraction_proposals()
    node = proposals.get("semantic_node_proposals", [{}])[0]
    edge = proposals.get("semantic_edge_proposals", [{}])[0]
    return (
        proposals.get("generated_view_policy") == "llm_extraction_proposals_are_generated_not_source_of_truth"
        and proposals.get("prompt_contract", {}).get("output_format") == "structured_json"
        and "unsupported_claim" in proposals.get("prompt_contract", {}).get("required_labels", [])
        and node.get("proposal_kind") == "semantic_node"
        and edge.get("proposal_kind") == "semantic_edge"
        and node.get("review_status") == "proposed"
        and edge.get("review_status") == "proposed"
        and node.get("confidence") == "inferred_unverified"
        and edge.get("confidence") == "inferred_unverified"
        and bool(node.get("source_observation_ids"))
        and bool(edge.get("source_observation_ids"))
    )


def _project_graph_rationale_comment_proposals_present() -> bool:
    proposals = _project_graph_llm_extraction_proposals()
    comment = proposals.get("rationale_comment_proposals", [{}])[0]
    return (
        comment.get("proposal_kind") == "rationale_comment"
        and comment.get("source_boundary") == "approved_redacted_spans_only"
        and comment.get("truth_status") == "unverified_inference"
        and comment.get("review_status") == "proposed"
        and proposals.get("review_policy", {}).get("human_review_required") is True
        and proposals.get("incident_workflow", {}).get("disable_on_failed_eval_or_privacy_violation") is True
        and proposals.get("rollback", {}).get("disable_path") == f"delete {LLM_EXTRACTION_TARGET}"
    )


def _project_graph_llm_extraction_eval_present() -> bool:
    proposals = _project_graph_llm_extraction_proposals()
    packet = evaluate_llm_extraction_proposals(
        proposals,
        cases=[
            {
                "id": "worker-proposal",
                "expected_proposal_kinds": ["semantic_node", "semantic_edge", "rationale_comment"],
                "expected_source_node_ids": ["function:app.worker.run"],
            }
        ],
        thresholds={
            "min_precision": 1.0,
            "max_unsupported_claim_rate": 0.0,
            "max_privacy_violations": 0,
            "max_cost_units": 0,
            "max_latency_ms": 250,
        },
    )
    return (
        packet.get("decision_status") == "passed"
        and packet.get("approval_boundary") == "batch22_explicit_llm_semantic_extraction_gate"
        and packet.get("quality_metrics", {}).get("precision") == 1.0
        and packet.get("quality_metrics", {}).get("unsupported_claim_rate") == 0.0
        and packet.get("quality_metrics", {}).get("privacy_violations") == 0
        and packet.get("quality_metrics", {}).get("cost_units") == 0
        and packet.get("failed_thresholds") == []
    )


def _project_graph_extension_artifacts() -> dict[str, dict[str, Any]]:
    static_index = _project_graph_static_index()
    return {
        "static_index": static_index,
        "backend": build_local_query_backend_store(
            _project_graph_sample(),
            static_index=static_index,
            approval=_project_graph_backend_approval(),
        ),
        "semantic": _project_graph_semantic_index(),
        "llm_proposals": _project_graph_llm_extraction_proposals(),
    }


def _project_graph_extension_verification_evidence() -> dict[str, Any]:
    return {
        "focused_suites": {
            "static_index": "passed",
            "backend": "passed",
            "semantic": "passed",
            "llm_proposals": "passed",
        },
        "full_verification_required": True,
        "timeout_ms": 1_200_000,
        "docs_check_required": True,
        "strict_mkdocs_required": True,
        "diff_hygiene_required": True,
    }


def _project_graph_extension_closure_packet() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp:
        return build_future_extension_closure_packet(
            workspace=FIXTURES / "project-code-graph-minimal-python",
            stage_root=Path(tmp) / "stage",
            graph=_project_graph_sample(),
            artifacts=_project_graph_extension_artifacts(),
            verification_evidence=_project_graph_extension_verification_evidence(),
        )


def _project_graph_future_extension_closure_present() -> bool:
    packet = _project_graph_extension_closure_packet()
    payload = json.dumps(packet, sort_keys=True).lower()
    return (
        validate_future_extension_closure_packet(packet).get("ok") is True
        and packet.get("artifact_kind") == "project_graph_future_extension_closure"
        and packet.get("approval_boundary") == "batch23_future_extension_verification_rollback_closure"
        and packet.get("status") == "ready"
        and packet.get("runtime_visual_qa", {}).get("backend_server_status") == "disabled_by_default"
        and packet.get("runtime_visual_qa", {}).get("external_requests_allowed") is False
        and packet.get("deferred_surface_status", {}).get("live_external_llm_semantic_extraction")
        == "blocked_without_new_explicit_approval"
        and packet.get("graph_only_fallback", {}).get("status") == "ok"
        and "c:\\users" not in payload
        and "return 'ok'" not in payload
    )


def _project_graph_extension_rollback_deletion_present() -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        stage_root = Path(tmp) / "stage"
        for relative in [
            STATIC_SEARCH_INDEX_TARGET,
            ".codex/product-agent-os/project-code-graph-search-index.previous.json",
            LOCAL_BACKEND_TARGET,
            ".codex/product-agent-os/project-code-graph-backend.previous.json",
            ".codex/product-agent-os/project-code-graph-backend.log",
            ".codex/product-agent-os/project-code-graph-backend.pid",
            SEMANTIC_RETRIEVAL_TARGET,
            ".codex/product-agent-os/project-code-graph-semantic-index.previous.json",
            LLM_EXTRACTION_TARGET,
            ".codex/product-agent-os/project-code-graph-llm-proposals.previous.json",
            EXTENSION_CLOSURE_TARGET,
        ]:
            target = stage_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("generated\n", encoding="utf-8")
        result = disable_future_extensions(
            stage_root,
            workspace=FIXTURES / "project-code-graph-minimal-python",
            graph=_project_graph_sample(),
        )
        proof = result.get("rendered_artifacts", {}).get("deletion_proof", {})
        return (
            result.get("rendered_artifacts", {}).get("status") == "disabled"
            and result.get("rendered_artifacts", {}).get("graph_only_fallback", {}).get("status") == "ok"
            and proof.get("remaining") == []
            and all(not (stage_root / relative).exists() for relative in proof.get("targets_checked", []))
        )


def _project_graph_unapproved_surface_blocking_present() -> bool:
    artifacts = _project_graph_extension_artifacts()
    artifacts["backend"]["server_lifecycle"]["active_process"] = True
    artifacts["backend"]["server_lifecycle"]["server_status"] = "running"
    artifacts["semantic"]["model_decision"]["external_model_calls_allowed"] = True
    artifacts["llm_proposals"]["model_policy"]["external_model_calls_allowed"] = True
    artifacts["llm_proposals"]["canonical_graph_mutation"] = "allowed"
    with tempfile.TemporaryDirectory() as tmp:
        packet = build_future_extension_closure_packet(
            workspace=FIXTURES / "project-code-graph-minimal-python",
            stage_root=Path(tmp) / "stage",
            graph=_project_graph_sample(),
            artifacts=artifacts,
            verification_evidence=_project_graph_extension_verification_evidence(),
        )
    errors = set(packet.get("validation", {}).get("errors", []))
    return (
        packet.get("status") == "blocked"
        and "backend:live_server_active" in errors
        and "semantic:external_model_calls" in errors
        and "llm_proposals:external_model_calls" in errors
        and "llm_proposals:canonical_graph_mutation" in errors
        and packet.get("deferred_surface_status", {}).get("canonical_graph_mutation_from_generated_proposals")
        == "blocked_without_new_explicit_approval"
    )


def _project_graph_extension_full_verification_contract_present() -> bool:
    packet = _project_graph_extension_closure_packet()
    contract = packet.get("full_verification_contract", {})
    commands = " ".join(contract.get("full_commands_required", []))
    return (
        contract.get("timeout_ms") == 1_200_000
        and "python -m unittest discover" in commands
        and "run_fixture_eval.py" in commands
        and "run_transcript_eval.py" in commands
        and "validate_codex_compatibility.py" in commands
        and ("tools\\check_docs.py" in commands or "tools/check_docs.py" in commands)
        and "git diff --check" in commands
        and packet.get("git_boundary") == "explicit_only"
    )


def _project_graph_live_governance_approval() -> dict[str, Any]:
    return {
        "explicit_approval": True,
        "owner": "Product-Agent OS Maintainer",
        "allowed_surfaces": [
            "approval_packet",
            "data_classification",
            "redaction_pipeline",
            "credential_boundary",
            "cache_policy",
            "budget_policy",
        ],
        "data_classification": {
            "allowed_fields": ["node_id", "label", "type", "observation_ids", "redacted_summary"],
            "redacted_fields": ["relative_path", "source_span", "review_comment"],
            "blocked_fields": ["absolute_local_paths", "raw_source_bodies", "secrets"],
        },
        "redaction_boundary": {
            "raw_source_excluded": True,
            "absolute_paths_redacted": True,
            "secrets_redacted": True,
            "provider_payload_validation_required": True,
        },
        "provider_policy": {
            "external_provider_calls_allowed": False,
            "approved_providers": ["external_embedding", "external_reranker", "external_llm"],
            "requires_batch_specific_approval": True,
        },
        "credential_policy": {
            "storage": "environment_only",
            "secret_material_stored": False,
            "providers": [
                {
                    "provider": "external_embedding",
                    "credential_source": "environment",
                    "env_var": "PRODUCT_AGENT_OS_EMBEDDING_API_KEY",
                }
            ],
        },
        "cache_policy": {
            "storage_path": LIVE_CACHE_TARGET,
            "ttl_days": 7,
            "fingerprint_scope": "redacted_graph_and_live_governance_policy",
            "stale_policy": "block_if_graph_or_policy_fingerprint_mismatch",
            "deletion_proof_required": True,
        },
        "budget_policy": {
            "max_run_tokens": 1500,
            "max_query_tokens": 600,
            "max_mutation_tokens": 0,
            "max_cost_units": 0,
            "max_latency_ms": 250,
            "on_exceed": "blocked_or_degraded_graph_only",
        },
        "rollback_path": f"delete {LIVE_GOVERNANCE_TARGET}",
        "residual_risks": ["provider drift remains blocked until later Task 26 batches"],
    }


def _project_graph_live_governance_packet() -> dict[str, Any]:
    return build_live_governance_packet(_project_graph_live_governance_approval())


def _project_graph_live_approval_packet_present() -> bool:
    approval = _project_graph_live_governance_approval()
    packet = _project_graph_live_governance_packet()
    return (
        validate_live_runtime_approval(approval).get("ok") is True
        and packet.get("artifact_kind") == "project_graph_live_governance"
        and packet.get("approval_boundary") == "batch24_live_governance_only_no_live_calls"
        and packet.get("status") == "ready"
        and set(packet.get("allowed_surfaces", []))
        == {
            "approval_packet",
            "data_classification",
            "redaction_pipeline",
            "credential_boundary",
            "cache_policy",
            "budget_policy",
        }
    )


def _project_graph_live_data_classification_policy_present() -> bool:
    classification = _project_graph_live_governance_packet().get("data_classification", {})
    return (
        classification.get("blocked_fields") == ["absolute_local_paths", "raw_source_bodies", "secrets"]
        and classification.get("raw_source_bodies") == "blocked"
        and classification.get("absolute_local_paths") == "blocked"
        and classification.get("secrets") == "blocked"
    )


def _project_graph_live_redaction_guard_present() -> bool:
    result = sanitize_live_provider_payload(
        {
            "query": "find worker",
            "path": r"C:\Users\user\Desktop\private\app.py",
            "raw_source_body": "OPENAI_API_KEY=sk-test-secret",
            "metadata": {"api_key": "sk-test-secret"},
        },
        approval=_project_graph_live_governance_approval(),
    )
    payload = json.dumps(result, sort_keys=True).lower()
    errors = set(result.get("validation", {}).get("errors", []))
    return (
        result.get("status") == "blocked"
        and result.get("provider_call_allowed") is False
        and "blocked_input:absolute_local_paths" in errors
        and "blocked_input:raw_source_bodies" in errors
        and "blocked_input:secrets" in errors
        and "sk-test-secret" not in payload
        and "c:\\users" not in payload
    )


def _project_graph_provider_credentials_boundary_present() -> bool:
    approval = _project_graph_live_governance_approval()
    approval["credential_policy"]["providers"][0]["credential_value"] = "sk-test-secret"
    packet = build_live_governance_packet(approval)
    payload = json.dumps(packet, sort_keys=True).lower()
    return (
        packet.get("status") == "blocked"
        and "credential_policy:stored_secret" in packet.get("validation", {}).get("errors", [])
        and packet.get("credential_policy", {}).get("secret_material_stored") is False
        and packet.get("credential_policy", {}).get("providers", [{}])[0].get("credential_source") == "environment"
        and "sk-test-secret" not in payload
    )


def _project_graph_live_cache_deletion_policy_present() -> bool:
    packet = _project_graph_live_governance_packet()
    with tempfile.TemporaryDirectory() as tmp:
        stage_root = Path(tmp) / "stage"
        for relative in [LIVE_GOVERNANCE_TARGET, LIVE_CACHE_TARGET]:
            target = stage_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("generated\n", encoding="utf-8")
        result = disable_live_governance(stage_root, workspace=FIXTURES / "project-code-graph-minimal-python")
        proof = result.get("rendered_artifacts", {}).get("deletion_proof", {})
        remaining = [relative for relative in proof.get("targets_checked", []) if (stage_root / relative).exists()]
    return (
        packet.get("cache_policy", {}).get("ttl_days") == 7
        and packet.get("cache_policy", {}).get("deletion_proof_required") is True
        and packet.get("cache_policy", {}).get("cache_can_be_deleted_without_graph_loss") is True
        and result.get("rendered_artifacts", {}).get("status") == "disabled"
        and remaining == []
    )


def _project_graph_live_budget_guard_present() -> bool:
    budget = _project_graph_live_governance_packet().get("budget_policy", {})
    result = enforce_live_budget(
        {
            "estimated_tokens": 1501,
            "estimated_query_tokens": 601,
            "estimated_cost_units": 1,
            "estimated_latency_ms": 251,
        },
        budget,
    )
    return (
        result.get("status") == "blocked"
        and result.get("degraded_mode") == "graph_only"
        and "budget:estimated_tokens" in result.get("errors", [])
        and "budget:estimated_query_tokens" in result.get("errors", [])
        and "budget:estimated_cost_units" in result.get("errors", [])
        and "budget:estimated_latency_ms" in result.get("errors", [])
    )


def _project_graph_live_governance_no_live_calls_present() -> bool:
    packet = _project_graph_live_governance_packet()
    return (
        packet.get("provider_policy", {}).get("external_provider_calls_allowed") is False
        and "live_server_start" in packet.get("blocked_surfaces", [])
        and "external_provider_call" in packet.get("blocked_surfaces", [])
        and "canonical_graph_mutation" in packet.get("blocked_surfaces", [])
        and packet.get("rollback", {}).get("fallback") == "graph_only_query_mode"
        and packet.get("generated_view_policy") == "live_governance_packet_is_policy_evidence_not_source_of_truth"
    )


def _project_graph_search_quality_present() -> bool:
    packet = _project_graph_search_quality_packet()
    metrics = packet.get("quality_metrics", {}) if isinstance(packet.get("quality_metrics"), dict) else {}
    return (
        packet.get("schema_version") == 1
        and packet.get("write_policy") == "read_only"
        and packet.get("decision_status") == "passed"
        and packet.get("approval_boundary") == "local_fixture_only_no_live_backend_or_model_calls"
        and metrics.get("symbol_recall") == 1.0
        and metrics.get("top_k_mrr") == 1.0
        and metrics.get("trace_success_rate") == 1.0
        and metrics.get("affected_test_precision") == 1.0
        and float(metrics.get("edge_density") or 0) <= 4.0
    )


def _project_graph_search_quality_thresholds_present() -> bool:
    packet = _project_graph_search_quality_packet()
    thresholds = packet.get("thresholds", {}) if isinstance(packet.get("thresholds"), dict) else {}
    return (
        thresholds.get("explicit_thresholds_required_before_closure") is True
        and "min_symbol_recall" in thresholds
        and "min_top_k_mrr" in thresholds
        and "min_trace_success_rate" in thresholds
        and "min_affected_test_precision" in thresholds
        and "max_edge_density" in thresholds
        and packet.get("failed_thresholds") == []
    )


def _project_graph_future_backend_semantic_gates_present() -> bool:
    paths = [
        PROJECT_ROOT / "REQUIREMENTS.md",
        PROJECT_ROOT / "PLAN.md",
        PROJECT_ROOT / "TEST.md",
        PROJECT_ROOT / "EVALS.md",
        PROJECT_ROOT / "RUNLOG.md",
        PROJECT_ROOT / "README.md",
        PLUGIN_ROOT / "README.md",
        PROJECT_ROOT / "docs" / "product-agent-os" / "index.md",
        PROJECT_ROOT / "docs" / "product-agent-os" / "technical.md",
        PROJECT_ROOT / "docs" / "product-agent-os" / "scenarios.md",
        PROJECT_ROOT / "docs" / "sources" / "product-agent-os-track-10-backlog.md",
    ]
    if not all(path.exists() for path in paths):
        return False
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    required_terms = [
        "future backend and semantic gates",
        "live database/server",
        "llm, embedding, cross-encoder",
        "semantic extraction and rationale/comment extraction",
        "explicit approval",
        "redaction, cache, token budget, eval threshold and rollback path",
    ]
    implemented_claims = [
        "live database/server is implemented",
        "live external model/api extraction is implemented",
        "canonical graph mutation by llm extraction is implemented",
        "llm proposals are canonical graph facts",
    ]
    return all(term in payload for term in required_terms) and not any(
        claim in payload for claim in implemented_claims
    )


def _codex_agentic_workflow_contract_present() -> bool:
    try:
        catalog = load_methodology_catalog()
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    if validate_methodology_catalog(catalog):
        return False
    domains = {
        str(domain.get("id")): domain
        for domain in catalog.get("domains", [])
        if isinstance(domain, dict) and domain.get("id")
    }
    workflow = domains.get("codex_agentic_workflow")
    if not isinstance(workflow, dict):
        return False
    if not set(CODEX_AGENTIC_WORKFLOW_GATES).issubset(set(workflow.get("gates", []))):
        return False
    if not set(CODEX_AGENTIC_WORKFLOW_ARTIFACTS).issubset(set(workflow.get("artifacts", []))):
        return False
    if not set(CODEX_AGENTIC_WORKFLOW_EVAL_FIELDS).issubset(set(workflow.get("eval_fields", []))):
        return False

    paths = [
        PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json",
        TEMPLATE_ROOT / "artifact-templates" / "model-reasoning-policy.md",
        TEMPLATE_ROOT / "artifact-templates" / "mcp-permission-review.md",
        TEMPLATE_ROOT / "artifact-templates" / "hook-governance.md",
        TEMPLATE_ROOT / "artifact-templates" / "skill-promotion-record.md",
        TEMPLATE_ROOT / "artifact-templates" / "agent-eval-workflow.md",
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
        PLUGIN_ROOT / "skills" / "docs-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "pr-release-operator" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "learning-loop-maintainer" / "SKILL.md",
        PLUGIN_ROOT / "skills" / "automation-promoter" / "SKILL.md",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "discovery.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "methodology_audit.py",
    ]
    payload = "\n".join(
        f"{path.name}\n{path.read_text(encoding='utf-8')}" for path in paths
    ).lower()
    return all(term in payload for term in CODEX_AGENTIC_WORKFLOW_TERMS)


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


def _question_queue_contract_present() -> bool:
    queue = build_question_queue(
        owner_questions=[
            "Who owns the release decision?",
            "Which command proves current verification evidence?",
            "Who owns the security review?",
        ],
        unknowns=[
            {
                "question": "runtime evidence",
                "category": "verification",
                "priority": "recommended",
            }
        ],
        usage_mode={"primary": "greenfield_idea"},
        runtime_status="needs_context",
    )
    questions = queue.get("questions", [])
    blocking = [item for item in questions if isinstance(item, dict) and item.get("priority") == "blocking"]
    structural_checks = [
        queue.get("schema_version") == 1,
        queue.get("write_policy") == "read_only",
        queue.get("policy", {}).get("max_total_questions") == MAX_TOTAL_QUESTIONS,
        queue.get("policy", {}).get("max_blocking_questions_in_first_response") == MAX_FIRST_RESPONSE_BLOCKING,
        isinstance(questions, list) and 0 < len(questions) <= MAX_TOTAL_QUESTIONS,
        len(blocking) == MAX_FIRST_RESPONSE_BLOCKING,
        queue.get("next_blocking_question") == blocking[0],
        queue.get("summary", {}).get("blocking") == MAX_FIRST_RESPONSE_BLOCKING,
        all(
            isinstance(item, dict)
            and item.get("id")
            and item.get("text")
            and item.get("answer_type")
            and isinstance(item.get("source"), dict)
            for item in questions
        ),
    ]
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "question_protocol.py",
        PLUGIN_ROOT / "scripts" / "codex_runtime_runner" / "contracts.py",
        PLUGIN_ROOT / "scripts" / "codex_runtime_runner" / "routes.py",
        PLUGIN_ROOT / "scripts" / "codex_runtime_runner" / "guards.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_question_protocol.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_codex_runtime_runner_state_routes.py",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(structural_checks) and all(term in payload for term in QUESTION_QUEUE_TERMS)


def _status_snapshot_present() -> bool:
    snapshot = build_status_snapshot(
        runtime_result={
            "status": "completed",
            "lifecycle_state": "quality_gate",
            "verification_evidence": [
                {"command": "python -m unittest", "recorded_at": "2026-05-01T00:00:00"}
            ],
            "route_packet": {
                "question_queue": build_question_queue(
                    owner_questions=["Which command proves current verification evidence?"],
                    runtime_status="needs_context",
                ),
                "first_response_contract": {
                    "safe_next_action": "Refresh current verification evidence.",
                    "question_counts": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
                    "question_summary": ["1 blocking question"],
                },
            },
        },
        generated_at="2026-05-28T00:00:00",
    )
    structural_checks = [
        snapshot.get("schema_version") == 1,
        snapshot.get("write_policy") == "read_only",
        snapshot.get("evidence_summary", {}).get("freshness") == "stale",
        snapshot.get("readiness_summary", {}).get("success_claim") == "not_claimed",
        "stale evidence" in snapshot.get("readiness_summary", {}).get("warnings", []),
        snapshot.get("dashboard_policy", {}).get("source_of_truth") == "underlying_artifacts",
        snapshot.get("dashboard_policy", {}).get("external_assets") == "forbidden",
    ]
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_snapshot.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_status_snapshot.py",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return all(structural_checks) and all(term in payload for term in STATUS_SNAPSHOT_TERMS)


def _status_dashboard_present() -> bool:
    rendered = render_status_dashboard(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "generated_at": "2026-05-28T00:00:00",
            "workspace": "synthetic",
            "lifecycle_state": "quality_gate",
            "usage_mode": {"primary": "inspection_only", "confidence": "high", "inspection_only": True},
            "question_summary": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
            "readiness_summary": {
                "status": "inspection_only",
                "runtime_status": "completed",
                "success_claim": "not_claimed",
                "warnings": ["stale evidence", "inspection-only evidence cannot prove completion"],
            },
            "evidence_summary": {"freshness": "stale", "evidence_count": 1, "stale_count": 1, "max_age_days": 14},
            "approval_summary": {"status": "not_available", "requirements": []},
            "dashboard_policy": {
                "write_policy": "read_only",
                "source_of_truth": "underlying_artifacts",
                "success_claim_policy": "never from dashboard alone",
                "external_assets": "forbidden",
            },
            "next_safe_action": "Refresh current verification evidence.",
            "staged_artifacts": {"mode": "dry-run", "targets": [], "validation_ok": True},
            "manifest_digests": {"file_count": 0},
        }
    )
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_dashboard.py",
        PLUGIN_ROOT / "scripts" / "render_status_dashboard.py",
        TEMPLATE_ROOT / "status-dashboard" / "status.html",
        TEMPLATE_ROOT / "status-dashboard" / "status.css",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_status_dashboard.py",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return (
        rendered.get("status") == "ready"
        and rendered.get("validation", {}).get("ok") is True
        and ".codex/product-agent-os/status.html" in payload
        and all(term in payload for term in STATUS_DASHBOARD_TERMS)
    )


def _dashboard_no_external_assets() -> bool:
    html = (TEMPLATE_ROOT / "status-dashboard" / "status.html").read_text(encoding="utf-8")
    css = (TEMPLATE_ROOT / "status-dashboard" / "status.css").read_text(encoding="utf-8")
    rendered = render_status_dashboard(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "generated_at": "2026-05-28T00:00:00",
            "dashboard_policy": {"source_of_truth": "underlying_artifacts", "write_policy": "read_only"},
            "readiness_summary": {"success_claim": "not_claimed", "warnings": []},
            "evidence_summary": {"freshness": "current"},
        }
    )
    payload = f"{html}\n{css}\n{rendered.get('html', '')}"
    return (
        "http://" not in payload.lower()
        and "https://" not in payload.lower()
        and "<script src" not in payload.lower()
        and rendered.get("validation", {}).get("ok") is True
        and "external urls absent" in rendered.get("validation", {}).get("checks", [])
        and "external scripts absent" in rendered.get("validation", {}).get("checks", [])
    )


def _trace_data_classification_gate_present() -> bool:
    blocked = enforce_trace_data_classification_gate(
        {
            "traces": [
                {"trace_id": "real-trace", "trace_source_type": "agents_sdk", "synthetic": False},
                {"trace_id": "synthetic-trace", "trace_source_type": "tool_report", "synthetic": True},
            ]
        }
    )
    allowed = enforce_trace_data_classification_gate(
        {"traces": [{"trace_id": "real-trace", "trace_source_type": "agents_sdk", "synthetic": False}]},
        accepted_gap={"owner": "Security", "reason": "synthetic fixture gap"},
    )
    payload = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            PLUGIN_ROOT / "scripts" / "product_agent_os" / "agent_skill_metrics.py",
            TEMPLATE_ROOT / "artifact-templates" / "data-classification-register.md",
            TEMPLATE_ROOT / "artifact-templates" / "secrets-policy.md",
            PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_agent_skill_metrics.py",
        ]
    )
    return (
        blocked.get("status") == "blocked"
        and "real_trace_requires_data_classification_or_gap" in blocked.get("blockers", [])
        and allowed.get("status") == "accepted_gap"
        and "data-classification-register.md" in payload
        and "secrets-policy.md" in payload
    )


def _offline_artifact_safety_shared() -> bool:
    dashboard = render_status_dashboard(
        {
            "schema_version": 1,
            "write_policy": "read_only",
            "generated_at": "2026-05-28T00:00:00",
            "dashboard_policy": {"source_of_truth": "underlying_artifacts", "write_policy": "read_only"},
            "readiness_summary": {"success_claim": "not_claimed", "warnings": []},
            "evidence_summary": {"freshness": "current"},
        }
    )
    report = render_agent_skill_metrics_report(_synthetic_metrics_report_packet())
    payload = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            PLUGIN_ROOT / "scripts" / "product_agent_os" / "offline_artifact_safety.py",
            PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_dashboard.py",
            PLUGIN_ROOT / "scripts" / "product_agent_os" / "agent_skill_metrics_report.py",
            PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_status_dashboard.py",
            PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_agent_skill_metrics_report.py",
        ]
    )
    return (
        dashboard.get("validation", {}).get("ok") is True
        and report.get("validation", {}).get("ok") is True
        and "generated view policy present" in dashboard.get("validation", {}).get("checks", [])
        and "generated view policy present" in report.get("validation", {}).get("checks", [])
        and "prepare_offline_payload" in payload
        and "offline_artifact_safety" in payload
    )


def _no_baseline_renderer_pollution(rendered: dict[str, Any]) -> bool:
    forbidden_targets = {
        METRICS_REPORT_TARGET,
        ".codex/automation-candidates/daily-agent-skill-metrics.md",
        ".codex/automation-candidates/weekly-agent-skill-metrics.md",
    }
    template_targets = {item.target_path for item in required_templates()}
    rendered_targets = {
        str(item.get("target_path"))
        for item in rendered.get("rendered_artifacts", {}).get("files", [])
        if isinstance(item, dict)
    }
    return forbidden_targets.isdisjoint(template_targets) and forbidden_targets.isdisjoint(rendered_targets)


def _metrics_report_redacted() -> bool:
    packet = _synthetic_metrics_report_packet()
    packet["raw_appendix"] = {"tool_output": "TOKEN=abc123", "path": "C:\\Users\\person\\private-project"}
    rendered = render_agent_skill_metrics_report(packet)
    serialized = json.dumps(rendered, sort_keys=True)
    return (
        rendered.get("status") == "ready"
        and rendered.get("validation", {}).get("ok") is True
        and "TOKEN=abc123" not in serialized
        and "C:\\Users\\person" not in serialized
        and "http://" not in rendered.get("html", "").lower()
        and "https://" not in rendered.get("html", "").lower()
    )


def _scorecard_ledger_contract_present() -> bool:
    record = build_scorecard_ledger_record(
        ledger_id="fixture-ledger",
        generated_at="2026-05-28T00:00:00Z",
        baseline_version={"skill:review": "1.0.0"},
        current_version={"skill:review": "1.1.0"},
        candidate_version={"skill:review": "1.2.0-candidate"},
        run_record_ids=["run-fixture"],
        raw_counts={"task_success_rate": {"numerator": 1, "denominator": 1}},
        confidence_intervals={"task_success_rate": {"lower": 0.5, "upper": 1.0}},
        cost_latency={"total_cost_usd": 0.1, "p95_latency_ms": 1000},
        evidence_links=[".codex/eval-reports/run-fixture.json"],
        redaction_status="ready",
        report_anchors=["#target-skill-review"],
    )
    markdown = render_scorecard_ledger_markdown(record)
    template = (TEMPLATE_ROOT / "artifact-templates" / "agent-skill-scorecard-ledger.md").read_text(
        encoding="utf-8"
    ).lower()
    return (
        record.get("ledger_policy") == "append_only"
        and "Append-only policy" in markdown
        and "confidence intervals" in template
        and "run record ids" in template
        and "TOKEN=" not in json.dumps(record, sort_keys=True) + markdown
    )


def _active_metrics_automation_blocked() -> bool:
    text = (
        "# Weekly Agent Skill Metrics Automation Candidate\n\n"
        "Automation type: metrics-loop\n"
        "## Owner\n\n"
        "- Accountable owner: Quality\n\n"
        "## Verification\n\n"
        "- Deterministic checks: python -m unittest tests.product_agent_os.test_agent_skill_metrics -v\n"
        "- Successful manual workflow runs: 2\n\n"
        "## Rollback Or Disable Path\n\n"
        "- Disable path: remove candidate packet\n\n"
        "## Explicit Write Policy\n\n"
        "- Allowed write targets: staged artifacts only\n\n"
        "## Active Schedule\n\n"
        "- Cron: 0 9 * * *\n"
        "- GitHub Actions workflow: active\n"
    )
    report = validate_automation_candidate.from_text(text, "weekly-agent-skill-metrics.md")
    return (
        report.get("status") == "blocked"
        and report.get("metrics_automation_candidate") is True
        and "active metrics automation is forbidden" in report.get("errors", [])
        and "external workflow creation is forbidden" in report.get("errors", [])
    )


def _metrics_loop_runtime_route_contract_present() -> bool:
    packet = _synthetic_metrics_loop_route_packet(status="regression_detected")
    route = plan_route("quality_gate", allow_subagents=False, agent_skill_metrics_loop=packet)
    result = build_result(
        status="route_ready",
        workspace="C:/workspace/synthetic",
        lifecycle_state="quality_gate",
        route_packet=route,
        source_policy_status="ok",
        approval_status="not_required",
        next_action=route["next_action"],
    )
    return (
        validate_runner_result(result) == []
        and "stage_metrics_report" in route.get("finish_options", [])
        and "request_owner_review" in route.get("finish_options", [])
        and "block_automation_promotion" in route.get("finish_options", [])
        and "investigate_regression" in route.get("finish_options", [])
        and "apply_update" not in route.get("finish_options", [])
        and "metrics loop reports are staged evidence only" in route.get("stop_conditions", [])
    )


def _metrics_loop_lifecycle_contract_present() -> bool:
    paths = [
        PLUGIN_ROOT / "skills" / name / "SKILL.md"
        for name in [
            "project-lifecycle-orchestrator",
            "workspace-discovery-auditor",
            "requirements-author",
            "implementation-planner",
            "agent-team-designer",
            "test-eval-designer",
            "risk-reviewer",
            "docs-maintainer",
            "pr-release-operator",
            "learning-loop-maintainer",
            "automation-promoter",
        ]
    ]
    payload = "\n".join(path.read_text(encoding="utf-8").lower() for path in paths)
    terms = [
        "agent_skill_metrics_loop",
        "self-verification metrics loop",
        "staged evidence only",
        "do not apply modernization candidates",
        "do not activate schedules",
        "do not call live eval services",
        "dashboard or report is not proof",
        "rollback evidence required",
    ]
    return all(term in payload for term in terms)


def _update_candidate_rollback_required() -> bool:
    route = plan_route(
        "quality_gate",
        allow_subagents=False,
        agent_skill_metrics_loop=_synthetic_metrics_loop_route_packet(
            top_candidates=[{"candidate_id": "unsafe-candidate", "action": "stage_patch"}]
        ),
    )
    result = build_result(
        status="route_ready",
        workspace="C:/workspace/synthetic",
        lifecycle_state="quality_gate",
        route_packet=route,
        source_policy_status="ok",
        approval_status="not_required",
        next_action=route["next_action"],
    )
    errors = validate_runner_result(result)
    return "agent_skill_metrics_loop.update_candidate_summary.top_candidates[0].requires_rollback:required" in errors


def _metrics_loop_false_positive_guards_present() -> bool:
    payload = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
            PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_behavioral_workflow_evals.py",
            PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_transcript_session_evals.py",
        ]
    )
    return all(
        term in payload
        for term in [
            "headline metric only approval",
            "self-applied update",
            "active automation",
            "live eval call",
            "dashboard success claim",
            "raw trace leakage",
            "uncalibrated judge approval",
            "update candidate without rollback",
        ]
    )


def _metrics_loop_not_forced(audit: dict[str, Any], methodology_audit: dict[str, Any]) -> bool:
    signals = audit.get("methodology_signals", {})
    applicability = audit.get("methodology_applicability", {})
    packet = applicability.get("agent_skill_metrics_loop", {}) if isinstance(applicability, dict) else {}
    recommendations = methodology_audit.get("recommendations", []) if isinstance(methodology_audit, dict) else []
    return (
        isinstance(signals, dict)
        and signals.get("agent_skill_metrics_loop") is False
        and isinstance(packet, dict)
        and packet.get("status") == "not_applicable"
        and not any(
            isinstance(item, dict) and item.get("gate") == "agent_skill_metrics_loop_present"
            for item in recommendations
        )
    )


def _metrics_loop_private_data_blocks_readiness() -> bool:
    packet = {
        "traces": [
            {
                "trace_id": "private-trace",
                "trace_source_type": "agents_sdk",
                "synthetic": False,
                "contains_private_data": True,
            }
        ]
    }
    blocked = enforce_trace_data_classification_gate(packet)
    return blocked.get("status") == "blocked" and "real_trace_requires_data_classification_or_gap" in blocked.get("blockers", [])


def _metrics_loop_uncalibrated_judge_blocks_candidate() -> bool:
    payload = _synthetic_metrics_loop_route_packet(status="judge_not_calibrated")
    payload["summary"]["overall_status"] = "blocked_by_judge_calibration"
    payload["update_candidate_summary"]["top_candidates"][0]["requires_rollback"] = True
    route = plan_route("quality_gate", allow_subagents=False, agent_skill_metrics_loop=payload)
    return "request_owner_review" in route.get("finish_options", []) and "stage_metrics_report" in route.get("finish_options", [])


def _metrics_loop_trace_missing_span_blocks_readiness() -> bool:
    payload = _synthetic_metrics_loop_route_packet(status="trace_missing_span")
    payload["summary"]["overall_status"] = "blocked_missing_trace_span"
    route = plan_route("quality_gate", allow_subagents=False, agent_skill_metrics_loop=payload)
    snapshot = build_status_snapshot(
        runtime_result={
            "status": "route_ready",
            "route_packet": route,
            "verification_evidence": [],
        },
        generated_at="2026-05-28T00:00:00",
    )
    return (
        snapshot.get("agent_skill_metrics_loop", {}).get("status") == "trace_missing_span"
        and snapshot.get("readiness_summary", {}).get("success_claim") == "not_claimed"
    )


def _synthetic_metrics_loop_route_packet(
    *,
    status: str = "present_unverified",
    top_candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    candidates = top_candidates or [
        {
            "candidate_id": "candidate-skill-review",
            "priority": "high",
            "requires_rollback": True,
        }
    ]
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": status,
        "summary": {
            "target_count": 2,
            "overall_status": "blocked_by_guardrail",
            "cadence_level": "L1",
        },
        "report_refs": [
            {
                "kind": "staged_artifact",
                "path": ".codex/eval-reports/agent-skill-evaluation-report.html",
                "digest": "sha256:fixture",
            }
        ],
        "cadence": {"level": "L1", "recommended": ["weekly"]},
        "update_candidate_summary": {
            "candidate_count": len(candidates),
            "top_candidates": candidates,
        },
        "automation_policy": "candidate_only",
        "source_policy": "generated summaries are not source of truth",
    }


def _synthetic_metrics_report_packet() -> dict[str, Any]:
    return {
        "report_id": "fixture-report",
        "generated_at": "2026-05-28T00:00:00Z",
        "project_id": "fixture",
        "eval_window": {"started_at": "2026-05-28T00:00:00Z", "ended_at": "2026-05-28T01:00:00Z"},
        "cadence": {"level": "L1", "recommended": ["weekly"]},
        "target_inventory": [{"target_id": "skill:review", "target_type": "skill", "version": "1.0.0"}],
        "metrics": {
            "sections": {
                "outcome": {
                    "metrics": {
                        "task_success_rate": {
                            "metric_id": "task_success_rate",
                            "numerator": 1,
                            "denominator": 1,
                            "value": 1.0,
                            "status": "ready",
                        }
                    }
                }
            }
        },
        "version_comparison": {"current": {"skill:review": "1.0.0"}},
        "trace_evidence": {"trace_sources": ["agents_sdk"]},
        "update_candidates": [],
        "source_datasets": [".codex/eval-reports/run-fixture.json"],
        "redaction_status": "ready",
    }


def _question_budget_false_positive_guard_present() -> bool:
    quiet_queue = build_question_queue(usage_mode={"primary": "docs_only"}, runtime_status="ready")
    noisy_queue = build_question_queue(
        owner_questions=["Who owns the highest-priority missing methodology gate?"],
        unknowns=[
            {
                "question": f"missing evidence item {index}",
                "category": "verification",
                "priority": "recommended",
                "source_key": f"missing_evidence_{index}",
            }
            for index in range(20)
        ],
        runtime_status="needs_context",
    )
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "question_protocol.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_question_protocol.py",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return (
        quiet_queue.get("questions") == []
        and len(noisy_queue.get("questions", [])) == MAX_TOTAL_QUESTIONS
        and noisy_queue.get("summary", {}).get("blocking") == MAX_FIRST_RESPONSE_BLOCKING
        and all(term in payload for term in GUIDED_QUESTION_BEHAVIOR_TERMS)
    )


def _dashboard_not_source_of_truth() -> bool:
    snapshot = build_status_snapshot(
        runtime_result={"status": "completed", "verification_evidence": []},
        generated_at="2026-05-28T00:00:00",
    )
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_snapshot.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_dashboard.py",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return (
        snapshot.get("dashboard_policy", {}).get("source_of_truth") == "underlying_artifacts"
        and snapshot.get("dashboard_policy", {}).get("success_claim_policy") == "never from dashboard alone"
        and "source_of_truth\": \"status_snapshot\"" in payload
        and all(term in payload for term in STATUS_DASHBOARD_BEHAVIOR_TERMS)
    )


def _stale_evidence_no_success_claim() -> bool:
    snapshot = build_status_snapshot(
        runtime_result={
            "status": "completed",
            "verification_evidence": [
                {"command": "python -m unittest", "recorded_at": "2026-05-01T00:00:00"}
            ],
        },
        generated_at="2026-05-28T00:00:00",
    )
    rendered = render_status_dashboard(snapshot)
    serialized = json.dumps({"snapshot": snapshot, "dashboard": rendered}, sort_keys=True).lower()
    paths = [
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_snapshot.py",
        PLUGIN_ROOT / "scripts" / "product_agent_os" / "status_dashboard.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_status_snapshot.py",
        PLUGIN_ROOT.parents[1] / "tests" / "product_agent_os" / "test_status_dashboard.py",
        TEMPLATE_ROOT / "evals" / "behavioral-workflows.json",
    ]
    payload = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
    return (
        snapshot.get("evidence_summary", {}).get("freshness") == "stale"
        and snapshot.get("readiness_summary", {}).get("success_claim") == "not_claimed"
        and "stale evidence" in snapshot.get("readiness_summary", {}).get("warnings", [])
        and "tests pass" not in serialized
        and "checks passed" not in serialized
        and "no success claim from stale evidence" in payload
    )


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
    cross_domain_runtime_bridge_fixtures = {
        "cross-domain-ai-rag-data-security",
        "package-release-security-handoff",
        "source-artifact-alias-mapping",
    }
    if path.name in cross_domain_runtime_bridge_fixtures:
        methodology_audit = build_methodology_audit(path)
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            methodology_intelligence=methodology_audit,
        )
        packet = route.get("methodology_packet", {})
        first_response = route.get("first_response_contract", {})
        question_queue = route.get("question_queue", {})
        checks = {
            "runtime_cross_domain_bridge_present": (
                bool(packet.get("recommendation_groups"))
                and bool(packet.get("source_artifact_ledger"))
                and bool(packet.get("safe_next_action"))
                and bool(route.get("finish_options"))
            ),
            "runtime_first_response_compact": (
                isinstance(first_response, dict)
                and isinstance(question_queue, dict)
                and bool(route.get("question_queue"))
                and "next_blocking_question" in first_response
                and isinstance(first_response.get("question_counts"), dict)
                and isinstance(first_response.get("question_summary"), list)
                and bool(first_response.get("safe_next_action"))
                and "owner_questions" not in first_response
                and "questions" not in first_response
                and "methodology_domains" not in first_response
                and "methodology_gates" not in first_response
            ),
        }
        return "route_ready" if all(checks.values()) else "blocked", checks

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

    if path.name == "codex-runner-methodology-ready":
        result = run_contract(path)
        packet = result["route_packet"].get("methodology_packet", {})
        checks["runtime_methodology_packet_present"] = (
            result["status"] == "route_ready"
            and bool(packet.get("recommendation_groups"))
            and bool(packet.get("safe_next_action"))
            and bool(result["route_packet"].get("finish_options"))
        )
        return str(result["status"]), checks

    if path.name == "codex-runner-methodology-approval-required":
        route = plan_route(
            "review_ready",
            allow_subagents=False,
            methodology_intelligence=_runtime_methodology_intelligence(
                artifact="release-readiness.md",
                safe_next_action="Publish package to the package registry.",
            ),
        )
        approval_errors = validate_approval_boundary(route, {"approval_status": "not_required"})
        checks["runtime_finish_options_approval_bound"] = (
            "request_approval" in route["finish_options"]
            and "approval:required_for_methodology_action" in approval_errors
        )
        return "needs_approval", checks

    if path.name == "codex-runner-detection-completion-blocked":
        route = plan_route(
            "review_ready",
            allow_subagents=False,
            methodology_intelligence=_runtime_methodology_intelligence(
                artifact="quality-strategy.md",
                safe_next_action="Stage quality evidence before completion claim.",
            ),
        )
        result = build_result(
            status="completed",
            workspace=str(path),
            lifecycle_state="review_ready",
            route_packet=route,
            source_policy_status="ok",
            approval_status="not_required",
            next_action="No action.",
        )
        errors = validate_runner_result(result)
        checks["runtime_detection_not_completion"] = "methodology_packet:detection_not_completion" in errors
        return "blocked", checks

    if path.name == "codex-runner-external-write-blocked":
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            methodology_intelligence=_runtime_methodology_intelligence(
                artifact="external-integration-approval.md",
                safe_next_action="Deploy service and mutate an external system.",
            ),
        )
        approval_errors = validate_approval_boundary(route, {"approval_status": "not_required"})
        checks["runtime_external_write_blocked"] = (
            "approval:required_for_methodology_action" in approval_errors
            and "deploy" not in " ".join(route["expected_outputs"]).lower()
        )
        return "needs_approval", checks

    if path.name == "codex-runner-automation-maturity-missing":
        route = plan_route(
            "learning_ready",
            allow_subagents=False,
            methodology_intelligence=_runtime_methodology_intelligence(
                artifact="automation-candidate.md",
                safe_next_action="Promote this workflow to an active automation.",
            ),
        )
        route_errors = validate_route_packet(route)
        checks["runtime_automation_maturity_required"] = (
            route["recommended_skill"] == "learning-loop-maintainer"
            and "stage_proposal" not in route["finish_options"]
            and "automation:maturity_evidence_required" in route_errors
        )
        return "blocked", checks

    if path.name == "codex-runner-methodology-redaction":
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            methodology_intelligence=_runtime_methodology_intelligence(
                artifact="security-risk-review.md",
                safe_next_action="TOKEN=fixture-secret\nInspect C:\\Users\\person\\workspace\nraw private chat log.",
            ),
        )
        payload, _redactions = redact_payload({"route_packet": route})
        text = json.dumps(payload, sort_keys=True)
        checks["runtime_methodology_redaction_enforced"] = validate_redaction(text) == []
        return "blocked", checks

    if path.name == "codex-runner-malformed-methodology-packet":
        result = build_result(
            status="route_ready",
            workspace=str(path),
            lifecycle_state="quality_gate",
            route_packet={
                "write_policy": "read_only",
                "methodology_packet": {"write_policy": "staged_only"},
            },
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )
        errors = validate_runner_result(result)
        checks["runtime_malformed_methodology_packet_blocked"] = (
            "methodology_packet.safe_next_action:required" in errors
            and "methodology_packet.write_policy:must_be_read_only" in errors
        )
        return "blocked", checks

    return "not_applicable", {}


def _runtime_methodology_intelligence(
    *,
    artifact: str,
    safe_next_action: str,
) -> dict[str, Any]:
    return {
        "status": "present_unverified",
        "write_policy": "read_only",
        "methodology_domains": [{"id": "codex_agentic_workflow", "status": "applicable_missing"}],
        "recommendations": [
            {
                "domain": "codex_agentic_workflow",
                "artifact": artifact,
                "priority": "P1_high_risk",
                "safe_next_action": safe_next_action,
            }
        ],
        "recommendation_groups": [
            {
                "artifact": artifact,
                "owner_domain": "codex_agentic_workflow",
                "consumer_domains": ["delivery_release_operations"],
                "priority": "P1_high_risk",
                "safe_next_action": safe_next_action,
            }
        ],
        "questions_for_owner": ["Who owns the synthetic runtime methodology decision?"],
        "methodology_synthesis": {
            "safe_next_action": safe_next_action,
            "semantic_evidence_sufficiency": {"status": "present_unverified"},
            "source_artifact_ledger": [{"artifact": artifact, "decision": "canonical_template"}],
        },
    }


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
