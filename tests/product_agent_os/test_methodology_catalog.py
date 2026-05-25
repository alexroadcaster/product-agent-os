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


if __name__ == "__main__":
    unittest.main()
