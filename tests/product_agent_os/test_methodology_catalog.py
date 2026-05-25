import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class MethodologyCatalogContractTest(unittest.TestCase):
    def test_catalog_loader_exists_and_exposes_vocabularies(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        self.assertEqual(catalog["version"], 1)
        self.assertEqual(
            catalog["readiness_statuses"],
            [
                "not_applicable",
                "applicable_missing",
                "present_unverified",
                "present_verified",
                "proposal_staged",
                "explicit_gap_accepted",
                "approval_required",
            ],
        )
        self.assertEqual(
            catalog["recommendation_priorities"],
            [
                "P0_blocker",
                "P1_high_risk",
                "P2_recommended",
                "P3_optional_maturity",
                "not_applicable",
            ],
        )
        self.assertEqual(catalog["maturity_levels"], ["baseline", "team", "production", "regulated"])
        self.assertEqual(catalog["complexity_profiles"], ["simple", "standard", "complex", "high_risk"])

    def test_catalog_contains_all_track_nine_domains_in_order(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        self.assertEqual(
            [domain["id"] for domain in catalog["domains"]],
            [
                "business_product",
                "requirements_domain",
                "solution_architecture",
                "quality_testing_evals",
                "codex_agentic_workflow",
                "frontend",
                "backend",
                "api_integrations",
                "database_data",
                "llm_ai_rag",
                "security_privacy_compliance",
                "delivery_release_operations",
            ],
        )

    def test_catalog_source_files_exist(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        repo_root = Path(__file__).resolve().parents[2]
        catalog = load_methodology_catalog()
        for domain in catalog["domains"]:
            with self.subTest(domain=domain["id"]):
                self.assertTrue((repo_root / domain["source_file"]).is_file())

    def test_each_domain_has_required_contract_fields(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        required_keys = {
            "id",
            "title",
            "source_file",
            "purpose",
            "applies_when",
            "not_applicable_when",
            "maturity_impact",
            "complexity_impact",
            "track8_scenarios",
            "decision_horizons",
            "artifacts",
            "gates",
            "eval_fields",
            "overlaps",
        }
        catalog = load_methodology_catalog()
        for domain in catalog["domains"]:
            with self.subTest(domain=domain["id"]):
                self.assertEqual(set(domain), required_keys)
                self.assertIsInstance(domain["applies_when"], list)
                self.assertIsInstance(domain["not_applicable_when"], list)
                self.assertIsInstance(domain["decision_horizons"], list)
                self.assertIsInstance(domain["artifacts"], list)
                self.assertIsInstance(domain["gates"], list)
                self.assertIsInstance(domain["eval_fields"], list)

    def test_business_product_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        business_product = domains["business_product"]

        expected_gates = [
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
        ]
        expected_artifacts = [
            "product-brief.md",
            "value-proposition.md",
            "opportunity-tree.md",
            "experiment-plan.md",
            "tracking-plan.md",
            "metric-spec.md",
            "acceptance-scenarios.md",
        ]
        expected_eval_fields = [
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
        ]

        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, business_product["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, business_product["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, business_product["eval_fields"])
        self.assertEqual(
            business_product["decision_horizons"],
            ["discovery", "MVP", "beta", "production", "scale"],
        )

    def test_requirements_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        requirements_domain = domains["requirements_domain"]

        expected_gates = [
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
        ]
        expected_artifacts = [
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
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "behavior-changing work",
            "domain terms or business rules",
            "API/UI/data contract change",
            "AI behavior change",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, requirements_domain["applies_when"])
        for term in [
            "typo-only docs edit",
            "formatting-only edit",
            "pure dependency metadata without behavior impact",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, requirements_domain["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, requirements_domain["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, requirements_domain["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, requirements_domain["eval_fields"])

    def test_solution_architecture_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        solution_architecture = domains["solution_architecture"]

        expected_gates = [
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
        ]
        expected_artifacts = [
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
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "complex or multi-surface system",
            "public API, event contract or generated client",
            "persistent data, PII, migration or retention change",
            "runtime, deployment, observability or rollback change",
            "parallel agent ownership or team boundary",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, solution_architecture["applies_when"])
        for term in [
            "typo-only docs edit",
            "formatting-only edit",
            "docs-light prototype without reviewed/diffable diagrams",
            "non-cloud work without Well-Architected review",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, solution_architecture["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, solution_architecture["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, solution_architecture["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, solution_architecture["eval_fields"])
        self.assertIn("requirements and domain traceability", solution_architecture["overlaps"])
        self.assertIn("agent team ownership", solution_architecture["overlaps"])

    def test_quality_testing_evals_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        quality = domains["quality_testing_evals"]

        expected_gates = [
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
        ]
        expected_artifacts = [
            "test-eval-matrix.md",
            "quality-strategy.md",
            "ci-evidence-record.md",
            "flaky-test-policy.md",
            "manual-qa-evidence.md",
            "TEST.md",
            "EVALS.md",
            "RUNLOG.md",
            "ai-eval-spec.md",
            "api-contract-review.md",
            "bug-rescue-report.md",
            "ci-stabilization-report.md",
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "non-trivial product or engineering work",
            "behavior-changing work",
            "bugfix, refactor, migration or dependency update",
            "API, event, schema or public package change",
            "AI, RAG, docs, UX, search or subjective quality change",
            "completion, readiness, release or quality claim",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, quality["applies_when"])
        for term in [
            "typo-only docs edit",
            "formatting-only edit",
            "docs-only source cleanup",
            "pure dependency metadata without behavior impact",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, quality["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, quality["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, quality["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, quality["eval_fields"])
        for overlap in [
            "requirements traceability",
            "solution architecture contracts",
            "frontend visual and accessibility evidence",
            "backend runtime evidence",
            "API contract compatibility",
            "database and security test data privacy",
            "LLM/AI/RAG eval baselines",
            "delivery and release CI gates",
            "agent workflow evidence-before-completion",
        ]:
            with self.subTest(overlap=overlap):
                self.assertIn(overlap, quality["overlaps"])
        self.assertIn("baseline", quality["maturity_impact"])
        self.assertIn("high_risk", quality["complexity_impact"])

    def test_codex_agentic_workflow_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        workflow = domains["codex_agentic_workflow"]

        expected_gates = [
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
        ]
        expected_artifacts = [
            "AGENTS.md",
            "REQUIREMENTS.md",
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
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "Product-Agent OS, Codex App, CLI or IDE extension project work",
            "subagents, skills, MCP, hooks, plugins or automation are configured",
            "parallel agent work, external writes or approval boundaries exist",
            "workflow is repeated and may become playbook, skill, plugin or automation",
            "Agents SDK app orchestration is proposed",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, workflow["applies_when"])
        for term in [
            "typo-only docs edit without Codex workflow change",
            "single local deterministic command without agent delegation",
            "read-only research without staged artifacts or external writes",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, workflow["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, workflow["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, workflow["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, workflow["eval_fields"])
        for overlap in [
            "quality evidence before completion",
            "delivery and release approval boundaries",
            "security and privacy trust boundaries",
            "LLM/AI/RAG tool and eval governance",
            "plugin and automation promotion",
            "parallel ownership and worktree safety",
        ]:
            with self.subTest(overlap=overlap):
                self.assertIn(overlap, workflow["overlaps"])
        self.assertIn("team", workflow["maturity_impact"])
        self.assertIn("high_risk", workflow["complexity_impact"])

    def test_frontend_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        frontend = domains["frontend"]

        expected_gates = [
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
        ]
        expected_artifacts = [
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
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "user-visible UI change",
            "route, page, screen or component work",
            "reusable component or design-system primitive",
            "browser-rendered runtime behavior",
            "frontend stack, Storybook, Playwright or visual evidence signal",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, frontend["applies_when"])
        for term in [
            "backend-only work",
            "data-only work",
            "CLI-only work",
            "docs-only work",
            "native-only work",
            "dependency metadata without UI behavior impact",
            "simple CRUD without non-trivial frontend state",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, frontend["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, frontend["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, frontend["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, frontend["eval_fields"])
        for overlap in [
            "requirements acceptance scenarios",
            "quality visual and accessibility evidence",
            "API contract alignment",
            "release runtime evidence",
            "agent workflow evidence-before-completion",
        ]:
            with self.subTest(overlap=overlap):
                self.assertIn(overlap, frontend["overlaps"])
        self.assertIn("team", frontend["maturity_impact"])
        self.assertIn("standard", frontend["complexity_impact"])

    def test_backend_domain_has_track_nine_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        domains = {domain["id"]: domain for domain in catalog["domains"]}
        backend = domains["backend"]

        expected_gates = [
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
        ]
        expected_artifacts = [
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
        ]
        expected_eval_fields = [
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
        ]

        for term in [
            "server, API, service, worker, queue or backend framework signal",
            "new service/module/worker or changed backend responsibility",
            "runtime behavior, remote dependency, job or queue change",
            "production or user-facing backend service",
            "auth, secrets, sensitive data, money, privileged operation or irreversible side effect",
        ]:
            with self.subTest(applies_when=term):
                self.assertIn(term, backend["applies_when"])
        for term in [
            "frontend-only work",
            "docs-only work",
            "CLI-only work",
            "native-only work",
            "dependency metadata without backend runtime behavior",
            "package-name-only service folder without runtime evidence",
        ]:
            with self.subTest(not_applicable_when=term):
                self.assertIn(term, backend["not_applicable_when"])
        for gate in expected_gates:
            with self.subTest(gate=gate):
                self.assertIn(gate, backend["gates"])
        for artifact in expected_artifacts:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, backend["artifacts"])
        for eval_field in expected_eval_fields:
            with self.subTest(eval_field=eval_field):
                self.assertIn(eval_field, backend["eval_fields"])
        for overlap in [
            "architecture service boundaries",
            "quality runtime evidence",
            "API and event contracts",
            "database data consistency",
            "security secrets and privacy",
            "delivery release operations",
            "agent workflow evidence-before-completion",
        ]:
            with self.subTest(overlap=overlap):
                self.assertIn(overlap, backend["overlaps"])
        self.assertIn("team", backend["maturity_impact"])
        self.assertIn("production", backend["maturity_impact"])
        self.assertIn("standard", backend["complexity_impact"])
        self.assertIn("high_risk", backend["complexity_impact"])


if __name__ == "__main__":
    unittest.main()
