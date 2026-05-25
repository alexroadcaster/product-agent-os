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


if __name__ == "__main__":
    unittest.main()
