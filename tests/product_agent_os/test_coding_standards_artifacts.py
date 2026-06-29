import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
SUMMARY = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-professional-code-s4-public-docs-closure-summary.json"
)
S5_SUMMARY = (
    DOCS
    / "superpowers"
    / "specs"
    / "batch45-professional-code-s5-learning-automation-summary.json"
)
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.templates import required_templates, template_by_target  # noqa: E402


class CodingStandardsArtifactsTest(unittest.TestCase):
    def test_public_docs_are_source_bound_and_nav_registered(self):
        ru = (PRODUCT_AGENT_OS / "coding-standards.md").read_text(encoding="utf-8")
        en = (PRODUCT_AGENT_OS / "coding-standards.en.md").read_text(encoding="utf-8")
        combined = (ru + "\n" + en).lower()

        for expected in [
            "source status:",
            "professional code authoring",
            "existing_capability_scan",
            "one_line_candidate",
            "negative_dependency_rule",
            "deep_module_check",
            "legacy_seam_check",
            "comment_policy",
            "cleverness_budget",
            "minimum_manual_successful_runs: 3",
            "candidate-only learning-loop/automation policy",
            "orientation_only_not_proof",
            "does not prove that ai agents now write enterprise-quality code in real projects",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, combined)

        forbidden_claims = [
            "hooks are active",
            "automation is active",
            "provider call performed",
            "browser verified",
            "plugin cache refreshed",
            "target workspace mutated",
            "release ready",
        ]
        for forbidden in forbidden_claims:
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)

        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        check_docs = (ROOT / "tools" / "check_docs.py").read_text(encoding="utf-8")
        self.assertIn("product-agent-os/coding-standards.md", mkdocs)
        self.assertIn("DOCS / \"product-agent-os\" / \"coding-standards.md\"", check_docs)
        self.assertIn("\"product-agent-os/coding-standards.md\"", check_docs)

    def test_cross_links_route_standards_from_public_docs(self):
        required_links = {
            "index.md": "coding-standards.md",
            "index.en.md": "coding-standards.md",
            "technical.md": "coding-standards.md",
            "technical.en.md": "coding-standards.md",
            "development-standards.md": "coding-standards.md",
            "development-standards.en.md": "coding-standards.md",
            "artifact-contracts.md": "coding-standards.md",
            "artifact-contracts.en.md": "coding-standards.md",
            "behavioral-evals.md": "coding-standards.md",
            "behavioral-evals.en.md": "coding-standards.md",
            "scenarios.md": "coding-standards.md",
            "scenarios.en.md": "coding-standards.md",
            "architecture.md": "coding-standards.md",
            "architecture.en.md": "coding-standards.md",
        }
        for filename, expected in required_links.items():
            with self.subTest(filename=filename):
                self.assertIn(expected, (PRODUCT_AGENT_OS / filename).read_text(encoding="utf-8"))

        for relative in ["code-review.md", "code-review.en.md"]:
            with self.subTest(playbook=relative):
                self.assertIn(
                    "../product-agent-os/coding-standards.md",
                    (DOCS / "playbooks" / relative).read_text(encoding="utf-8"),
                )

    def test_templates_and_eval_cases_remain_registered_without_stale_paths(self):
        expected_targets = {
            ".codex/workflows/coding-standards.md": "workflow-coding-standards",
            ".codex/artifact-templates/coding-standard-checklist.md": "artifact-coding-standard-checklist",
        }
        registered_targets = {template.target_path for template in required_templates()}
        for target, key in expected_targets.items():
            with self.subTest(target=target):
                self.assertIn(target, registered_targets)
                template = template_by_target(target)
                self.assertEqual(key, template.key)
                self.assertNotIn("assets/templates/artifacts", template.source_path.as_posix())

        behavioral = json.loads(
            (TEMPLATE_ROOT / "evals" / "behavioral-workflows.json").read_text(encoding="utf-8")
        )
        cases = {case["name"]: case for case in behavioral["cases"]}
        for case_name in [
            "professional-code-authoring-custom-code-bloat",
            "professional-code-authoring-unnecessary-dependency",
            "professional-code-authoring-missing-existing-capability-scan",
            "professional-code-authoring-comment-noise",
            "professional-code-authoring-shallow-wrapper",
            "professional-code-authoring-unsupported-legacy-rewrite",
        ]:
            with self.subTest(case=case_name):
                payload = json.dumps(cases[case_name], sort_keys=True).lower()
                self.assertIn("professional_code_authoring", payload)
                self.assertIn("coding-standard-checklist.md", payload)

    def test_s4_closure_packet_records_scope_and_claim_ceiling(self):
        packet = json.loads(SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual("batch45_professional_code_s4_public_docs_closure_v1", packet["schema_version"])
        self.assertEqual("B45-S4-M12-M13-M19-M14-A01", packet["evidence_id"])
        self.assertEqual("implemented_s4_docs_contract_ready", packet["status"])

        self.assertEqual(
            {
                "B45-PCA-M12": "implemented_docs_contract_ready",
                "B45-PCA-M13": "implemented_docs_contract_ready",
                "B45-PCA-M19": "implemented_docs_contract_ready",
                "B45-PCA-M14": "closure_through_s4_pending_b45_pca_m23",
            },
            packet["row_status"],
        )
        self.assertEqual("planned_B45_S5", packet["remaining_rows"]["B45-PCA-M23"])
        self.assertIn("docs/product-agent-os/coding-standards.md", packet["source_docs"])
        self.assertIn("tests/product_agent_os/test_coding_standards_artifacts.py", packet["tests_added"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertIn("root_site_freshness_for_new_page_not_claimed", packet["accepted_gaps"])

    def test_s5_learning_automation_packet_closes_m23_without_activation(self):
        packet = json.loads(S5_SUMMARY.read_text(encoding="utf-8"))
        self.assertEqual(
            "batch45_professional_code_s5_learning_automation_summary_v1",
            packet["schema_version"],
        )
        self.assertEqual("B45-S5-M23-M14-A01", packet["evidence_id"])
        self.assertEqual("implemented_s5_synthetic_green", packet["status"])
        self.assertEqual(
            "implemented_candidate_only_synthetic_green",
            packet["row_status"]["B45-PCA-M23"],
        )
        self.assertEqual(
            "implemented_full_batch45_closure_after_m23",
            packet["row_status"]["B45-PCA-M14"],
        )
        self.assertEqual("candidate_only", packet["candidate_policy"]["status"])
        self.assertEqual(3, packet["candidate_policy"]["minimum_manual_successful_runs"])
        self.assertTrue(packet["candidate_policy"]["future_activation_handoff_required"])

        for required in [
            "owner_review",
            "rollback_or_disable_path",
            "false_positive_audit",
            "flake_replay",
            "cost_check",
            "no_hidden_telemetry_or_raw_private_chat",
        ]:
            self.assertIn(required, packet["candidate_policy"]["required_review_gates"])

        for action, performed in packet["no_unapproved_actions"].items():
            with self.subTest(action=action):
                self.assertFalse(performed)

        self.assertIn("real_project_manual_pilot_not_run", packet["accepted_gaps"])


if __name__ == "__main__":
    unittest.main()
