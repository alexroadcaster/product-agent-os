import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.templates import required_templates, template_by_target  # noqa: E402


class Batch45CodingStandardsTemplateTest(unittest.TestCase):
    def test_templates_are_registered_to_canonical_staging_targets(self):
        expected = {
            ".codex/workflows/coding-standards.md": (
                "workflow-coding-standards",
                "workflows",
                "workflows/coding-standards.md",
            ),
            ".codex/artifact-templates/coding-standard-checklist.md": (
                "artifact-coding-standard-checklist",
                "artifact-templates",
                "artifact-templates/coding-standard-checklist.md",
            ),
        }
        targets = {item.target_path for item in required_templates()}

        for target, (key, category, source_suffix) in expected.items():
            with self.subTest(target=target):
                self.assertIn(target, targets)
                item = template_by_target(target)
                self.assertEqual(item.key, key)
                self.assertEqual(item.category, category)
                self.assertTrue(str(item.source_path).replace("\\", "/").endswith(source_suffix))
                self.assertNotIn("assets/templates/artifacts", str(item.source_path).replace("\\", "/"))

    def test_coding_standard_checklist_carries_professional_authoring_gates(self):
        text = self._template_text("artifact-templates", "coding-standard-checklist.md")
        expected_terms = [
            "enterprise_leverage_check",
            "existing_capability_scan",
            "one_line_candidate",
            "negative_dependency_rule",
            "deep_module_check",
            "legacy_seam_check",
            "comment_policy",
            "cleverness_budget",
            "unsupported_code_quality_claims",
            "standard library or language construct option",
            "project helper or existing abstraction",
            "selected leverage path",
            "new dependency count",
            "characterization test",
            "not_applicable",
            "closure level",
        ]
        for expected in expected_terms:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("assets/templates/artifacts", text)

    def test_coding_standards_workflow_routes_to_checklist_without_activation_claims(self):
        text = self._template_text("workflows", "coding-standards.md")
        expected_terms = [
            ".codex/artifact-templates/coding-standard-checklist.md",
            ".codex/artifact-templates/agent-task-packet.md",
            "enterprise_leverage_check",
            "existing_capability_scan",
            "one_line_candidate",
            "negative_dependency_rule",
            "deep_module_check",
            "legacy_seam_check",
            "comment_policy",
            "cleverness_budget",
            "evidence ceiling",
            "template registration proves the workflow can be staged",
            "does not prove runtime activation",
            "not_applicable",
        ]
        for expected in expected_terms:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("assets/templates/artifacts", text)

    def test_agent_task_packet_carries_compact_handoff_contract(self):
        text = self._template_text("artifact-templates", "agent-task-packet.md")
        expected_terms = [
            "professional code authoring contract",
            ".codex/workflows/coding-standards.md",
            ".codex/artifact-templates/coding-standard-checklist.md",
            "enterprise_leverage_check",
            "existing_capability_scan",
            "one_line_candidate",
            "negative_dependency_rule",
            "deep_module_check",
            "legacy_seam_check",
            "cleverness_budget",
            "unsupported code-quality claims",
            "raw research body or raw conversation history included: forbidden",
        ]
        for expected in expected_terms:
            with self.subTest(expected=expected):
                self.assertIn(expected, text)
        self.assertNotIn("ai-agent-coding-standards-research.md", text)
        self.assertNotIn("ai-agent-coding-literature-research.md", text)

    @staticmethod
    def _template_text(category: str, name: str) -> str:
        return (TEMPLATE_ROOT / category / name).read_text(encoding="utf-8").lower()


if __name__ == "__main__":
    unittest.main()
