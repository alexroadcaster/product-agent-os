import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class MethodologySynthesisContractTest(unittest.TestCase):
    def test_backlog_records_current_cross_domain_baseline(self):
        backlog = (ROOT / "docs" / "sources" / "product-agent-os-track-9-backlog.md").read_text(
            encoding="utf-8"
        )

        for expected in [
            "Task 20 Cross-Domain Synthesis Baseline",
            "accepted_gap_recorded",
            "automation_manual_stability_present",
            "bounded_context_architecture_boundary_trace",
            "external_write_approval_present",
            "approval-record.md",
            "security-risk-review.md",
            "api-contract-review.md",
            "test-eval-matrix.md",
            "release-readiness.md",
            "architecture-overview.md",
            "backend FSD-like directories can trigger frontend",
            "security/payment can be ordered behind generic quality strategy",
            "RAG ingestion can miss AI/RAG routing",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, backlog)

    def test_synthesis_catalog_records_shared_ownership_and_supported_packets(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        catalog = load_methodology_catalog()
        synthesis = catalog["synthesis"]

        self.assertEqual(synthesis["schema_version"], 1)
        self.assertIn("recommendation_groups", synthesis["output_packet_keys"])
        self.assertIn("methodology_synthesis", synthesis["output_packet_keys"])

        shared_gates = synthesis["shared_gates"]
        self.assertEqual(shared_gates["accepted_gap_recorded"]["owner_domain"], "requirements_domain")
        self.assertIn("solution_architecture", shared_gates["accepted_gap_recorded"]["consumer_domains"])
        self.assertEqual(
            shared_gates["external_write_approval_present"]["owner_domain"],
            "security_privacy_compliance",
        )
        self.assertIn(
            "api_integrations",
            shared_gates["external_write_approval_present"]["consumer_domains"],
        )

        artifact = synthesis["artifact_owners"]["security-risk-review.md"]
        self.assertEqual(artifact["owner_domain"], "security_privacy_compliance")
        for consumer in ["backend", "api_integrations", "database_data", "llm_ai_rag"]:
            with self.subTest(consumer=consumer):
                self.assertIn(consumer, artifact["consumer_domains"])

    def test_semantic_evidence_sufficiency_is_shared_owner_review_contract(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog

        semantic = load_methodology_catalog()["synthesis"]["semantic_evidence_sufficiency"]

        self.assertEqual(semantic["owner_domain"], "quality_testing_evals")
        for consumer in [
            "security_privacy_compliance",
            "delivery_release_operations",
            "llm_ai_rag",
            "api_integrations",
            "database_data",
        ]:
            with self.subTest(consumer=consumer):
                self.assertIn(consumer, semantic["consumer_domains"])
        self.assertEqual(
            semantic["accepted_gap_required_fields"],
            ["owner", "reason", "review_date", "downstream_risk", "follow_up_condition"],
        )

    def test_source_artifact_ledger_classifies_methodology_mentions(self):
        from product_agent_os.methodology_synthesis import classify_source_artifact

        source_mentions = set()
        for path in (ROOT / "docs" / "methodologies").glob("*.md"):
            if path.name == "index.md":
                continue
            source_mentions.update(re.findall(r"`([^`]+\.md)`", path.read_text(encoding="utf-8")))

        for artifact in sorted(source_mentions):
            with self.subTest(artifact=artifact):
                decision = classify_source_artifact(artifact)
                self.assertIn(decision["decision"], {"canonical_template", "alias", "existing_non_template", "deferred"})
                if decision["decision"] == "alias":
                    self.assertTrue(decision["target"])
                if decision["decision"] == "deferred":
                    self.assertTrue(decision["reason"])

    def test_template_alias_constants_are_represented_in_synthesis_catalog(self):
        from product_agent_os.methodology_catalog import load_methodology_catalog
        from product_agent_os.templates import SOURCE_ARTIFACT_TEMPLATE_ALIASES

        aliases = load_methodology_catalog()["synthesis"]["artifact_aliases"]

        for source_name, canonical in SOURCE_ARTIFACT_TEMPLATE_ALIASES.items():
            with self.subTest(source_name=source_name):
                self.assertIn(source_name, aliases)
                self.assertEqual(aliases[source_name]["target"], canonical)

    def test_task_matrix_plan_template_path_is_canonical_owned_template(self):
        from product_agent_os.methodology_synthesis import classify_source_artifact

        decision = classify_source_artifact(".codex/artifact-templates/task-matrix-plan.md")

        self.assertEqual(decision["decision"], "canonical_template")
        self.assertEqual(decision["target"], "task-matrix-plan.md")
        self.assertEqual(decision["owner_domain"], "codex_agentic_workflow")
        self.assertIn("packaged templates", decision["reason"])
        self.assertNotEqual(decision["decision"], "deferred")

    def test_group_recommendations_merges_artifacts_and_preserves_source_domains(self):
        from product_agent_os.methodology_synthesis import build_methodology_synthesis

        recommendations = [
            {
                "priority": "P1_high_risk",
                "domain": "backend",
                "gate": "backend_security_boundary_present",
                "artifact": "security-risk-review.md",
                "reason": "Backend payment path touches secrets.",
                "evidence_required": ["secret boundary", "payment path"],
                "safe_next_action": "Stage backend security review.",
            },
            {
                "priority": "P0_blocker",
                "domain": "security_privacy_compliance",
                "gate": "security_risk_review_present",
                "artifact": "security-risk-review.md",
                "reason": "Payment flow needs security owner review.",
                "evidence_required": ["payment path", "owner approval"],
                "safe_next_action": "Stage security-risk-review.md before implementation.",
            },
            {
                "priority": "P2_recommended",
                "domain": "quality_testing_evals",
                "gate": "quality_strategy_present",
                "artifact": "quality-strategy.md",
                "reason": "Quality strategy is missing.",
                "evidence_required": ["local verification command"],
                "safe_next_action": "Stage quality-strategy.md.",
            },
        ]

        packet = build_methodology_synthesis(recommendations)
        groups = {group["artifact"]: group for group in packet["recommendation_groups"]}

        security = groups["security-risk-review.md"]
        self.assertEqual(security["priority"], "P0_blocker")
        self.assertEqual(security["owner_domain"], "security_privacy_compliance")
        self.assertEqual(security["source_domains"], ["backend", "security_privacy_compliance"])
        self.assertEqual(security["gates"], ["backend_security_boundary_present", "security_risk_review_present"])
        self.assertEqual(security["evidence_required"], ["secret boundary", "payment path", "owner approval"])
        self.assertEqual(packet["safe_next_action"], "Stage security-risk-review.md before implementation.")

    def test_risk_aware_synthesis_prioritizes_security_and_release_over_generic_quality(self):
        from product_agent_os.methodology_synthesis import build_methodology_synthesis

        recommendations = [
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
                "reason": "Payment and external write work needs explicit approval.",
                "evidence_required": ["payment path", "approval boundary"],
                "safe_next_action": "Record approval_required before the external write.",
            },
            {
                "priority": "P1_high_risk",
                "domain": "delivery_release_operations",
                "gate": "release_evidence_present",
                "artifact": "release-readiness.md",
                "reason": "Package publish work needs release readiness evidence.",
                "evidence_required": ["release scope", "publish approval"],
                "safe_next_action": "Stage release-readiness.md before publish.",
            },
        ]

        packet = build_methodology_synthesis(recommendations)
        ordered_artifacts = [group["artifact"] for group in packet["recommendation_groups"]]

        self.assertEqual(ordered_artifacts[:2], ["approval-record.md", "release-readiness.md"])
        self.assertIn("quality-strategy.md", ordered_artifacts)
        self.assertLess(ordered_artifacts.index("release-readiness.md"), ordered_artifacts.index("quality-strategy.md"))
        self.assertEqual(packet["safe_next_action"], "Record approval_required before the external write.")

    def test_owner_questions_are_deduped_in_synthesis_packet(self):
        from product_agent_os.methodology_synthesis import dedupe_owner_questions

        questions = [
            "Who owns the highest-priority missing methodology gate?",
            "Who owns the highest priority missing methodology gate?",
            "Which local command is the source of truth for verification?",
        ]

        self.assertEqual(
            dedupe_owner_questions(questions),
            [
                "Who owns the highest-priority missing methodology gate?",
                "Which local command is the source of truth for verification?",
            ],
        )


if __name__ == "__main__":
    unittest.main()
