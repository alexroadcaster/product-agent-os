import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class MethodologyAuditContractTest(unittest.TestCase):
    def _domain_status(self, result, domain_id):
        domains = {domain["id"]: domain for domain in result["methodology_domains"]}
        return domains[domain_id]["status"]

    def _recommendation_by_gate(self, result, gate):
        for recommendation in result["recommendations"]:
            if recommendation["gate"] == gate:
                return recommendation
        self.fail(f"missing recommendation for gate {gate}")

    def test_empty_workspace_returns_baseline_simple_with_questions(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            result = build_methodology_audit(Path(tmp), intent_hint="new MVP idea")

        self.assertEqual(result["maturity_level"]["selected"], "baseline")
        self.assertEqual(result["complexity_profile"]["selected"], "simple")
        self.assertIn("delivery_map", result)
        self.assertIn("questions_for_owner", result)
        self.assertIn("safe_next_action", result)
        self.assertEqual(result["write_policy"], "read_only")

    def test_workspace_with_api_database_and_ci_routes_complex(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (root / "migrations").mkdir()
            (root / "migrations" / "001_init.sql").write_text(
                "create table accounts(id text primary key);\n",
                encoding="utf-8",
            )
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: ci\n", encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="prepare for production API release")

        self.assertIn(result["maturity_level"]["selected"], ["team", "production"])
        self.assertIn(result["complexity_profile"]["selected"], ["complex", "high_risk"])
        domain_ids = [domain["id"] for domain in result["methodology_domains"] if domain["status"] != "not_applicable"]
        self.assertIn("api_integrations", domain_ids)
        self.assertIn("database_data", domain_ids)
        self.assertIn("delivery_release_operations", domain_ids)

    def test_recommendations_have_stable_shape(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="ship frontend feature")

        required_keys = {
            "priority",
            "reason",
            "domain",
            "gate",
            "artifact",
            "evidence_required",
            "evidence_owner",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
        }
        self.assertGreaterEqual(len(result["recommendations"]), 1)
        for recommendation in result["recommendations"]:
            self.assertEqual(set(recommendation), required_keys)

    def test_business_product_intent_routes_domain_and_product_hypothesis_priority(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            discovery_result = build_methodology_audit(Path(tmp), intent_hint="new MVP idea")
            implementation_root = Path(tmp) / "implementation"
            implementation_root.mkdir()
            (implementation_root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            implementation_result = build_methodology_audit(
                implementation_root,
                intent_hint="ship MVP product metric experiment",
            )

        self.assertNotEqual(self._domain_status(discovery_result, "business_product"), "not_applicable")
        self.assertNotEqual(self._domain_status(implementation_result, "business_product"), "not_applicable")
        self.assertEqual(
            self._recommendation_by_gate(discovery_result, "product_hypothesis_present")["priority"],
            "P2_recommended",
        )
        self.assertEqual(
            self._recommendation_by_gate(implementation_result, "product_hypothesis_present")["priority"],
            "P1_high_risk",
        )

    def test_business_product_metric_ai_analytics_and_release_claims_create_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "ship AI product analytics dashboard with usage events and product success "
                    "metric after release without telemetry and workflow promotion"
                ),
            )

        expected = {
            "metric_hardening_when_product_behavior_changes": ("P1_high_risk", "metric-spec.md"),
            "ai_product_eval_when_ai_behavior_changes": ("P1_high_risk", "ai-eval-spec.md"),
            "analytics_tracking_plan_present": ("P1_high_risk", "tracking-plan.md"),
            "release_measurement_evidence_present": ("P1_high_risk", "RUNLOG.md"),
            "decision_horizon_present": ("P2_recommended", "product-brief.md"),
            "outcome_metric_level_separated": ("P2_recommended", "metric-spec.md"),
            "metric_scope_classified": ("P1_high_risk", "REQUIREMENTS.md"),
            "workflow_promotion_value_evidence_present": ("P2_recommended", "skill-promotion-record.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_business_product_false_positive_intents_are_not_applicable(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "dependency pin without behavior impact",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "business_product"), "not_applicable")

    def test_requirements_domain_behavior_intent_routes_domain_and_blocks_missing_scenarios(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
            result = build_methodology_audit(root, intent_hint="ship user behavior change")

        self.assertNotEqual(self._domain_status(result, "requirements_domain"), "not_applicable")
        recommendation = self._recommendation_by_gate(result, "acceptance_scenarios_when_behavior_changes")
        self.assertEqual(recommendation["priority"], "P0_blocker")
        self.assertEqual(recommendation["artifact"], "acceptance-scenarios.md")

    def test_requirements_domain_risky_public_contract_work_requires_ids_quality_and_constraints(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            result = build_methodology_audit(
                root,
                intent_hint="regulatory multi-slice public API requirement with privacy rollback constraints",
            )

        expected = {
            "requirement_quality_present": ("P1_high_risk", "requirement-registry.md"),
            "requirement_ids_present": ("P1_high_risk", "requirement-registry.md"),
            "constraints_traceability_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
            "api_ui_data_traceability_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_story_domain_event_and_owner_review_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "unclear large disputed user story with MVP deferred slices and business rule "
                    "for payment domain event across boundary from AI generated finance legal claim"
                ),
            )

        expected = {
            "stakeholder_owner_map_present": ("P2_recommended", "stakeholder-owner-map.md"),
            "story_slice_map_present": ("P2_recommended", "story-slice-map.md"),
            "example_mapping_when_unclear_story": ("P2_recommended", "example-map.md"),
            "business_rules_present": ("P1_high_risk", "business-rules.md"),
            "domain_event_contracts_present": ("P1_high_risk", "requirements-traceability-matrix.md"),
            "domain_expert_review_present": ("P1_high_risk", "domain-review-record.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_change_impact_accepted_gap_and_declarative_scenario_recommendations(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
            result = build_methodology_audit(
                root,
                intent_hint=(
                    "requirement changed after planning with accepted gap missing review date "
                    "and acceptance scenario using css selector database table function name test harness"
                ),
            )

        expected = {
            "requirement_change_impact_review_present": ("P1_high_risk", "requirement-change-impact.md"),
            "accepted_gap_recorded": ("P1_high_risk", "domain-review-record.md"),
            "declarative_acceptance_scenarios_present": ("P1_high_risk", "acceptance-scenarios.md"),
        }
        for gate, (priority, artifact) in expected.items():
            with self.subTest(gate=gate):
                recommendation = self._recommendation_by_gate(result, gate)
                self.assertEqual(recommendation["priority"], priority)
                self.assertEqual(recommendation["artifact"], artifact)

    def test_requirements_domain_false_positive_intents_are_not_applicable_for_readme_only_work(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        for intent in [
            "typo-only docs edit",
            "formatting-only markdown cleanup",
            "dependency metadata without behavior impact",
        ]:
            with self.subTest(intent=intent):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=intent)

                self.assertEqual(self._domain_status(result, "requirements_domain"), "not_applicable")

    def test_requirements_domain_rejects_unsupported_methodology_claims_as_evidence(self):
        from product_agent_os.methodology_audit import build_methodology_audit

        unsupported_claims = [
            "BDD replaces testing",
            "Gherkin is mandatory",
            "user story template is complete requirement",
            "glossary is ubiquitous language",
            "OpenAPI is requirements source of truth",
        ]
        for claim in unsupported_claims:
            with self.subTest(claim=claim):
                with tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp)
                    (root / "package.json").write_text('{"scripts":{"test":"pytest"}}\n', encoding="utf-8")
                    result = build_methodology_audit(root, intent_hint=claim)

                recommendation = self._recommendation_by_gate(result, "unsupported_claims_rejected")
                self.assertEqual(recommendation["priority"], "P1_high_risk")
                self.assertEqual(recommendation["artifact"], "domain-review-record.md")


if __name__ == "__main__":
    unittest.main()
