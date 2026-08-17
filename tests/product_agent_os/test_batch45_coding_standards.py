import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.infrastructure import render_infrastructure_plan  # noqa: E402
from product_agent_os.templates import required_templates, template_by_target  # noqa: E402


class Batch45CodingStandardsTemplateTest(unittest.TestCase):
    def test_compact_code_change_contract_is_the_default_registered_authoring_context(self):
        target = ".codex/artifact-templates/code-change-contract.md"
        expected_fields = [
            "existing_capability",
            "smallest_safe_patch",
            "invariants",
            "dependency_decision",
            "risk_selected_tests",
            "comment_decision",
            "performance_applicability",
            "evidence_and_gaps",
        ]
        checklist_headings = [
            "## Enterprise Leverage Check",
            "## Dependency Decision",
            "## Module And Legacy Safety",
            "## Code Style And Comments",
            "## Test And Evidence",
            "## Completion Gate",
        ]

        targets = [item.target_path for item in required_templates()]
        self.assertIn(target, targets)
        self.assertEqual(targets.count(target), 1)

        item = template_by_target(target)
        self.assertEqual(item.key, "artifact-code-change-contract")
        self.assertEqual(item.category, "artifact-templates")
        self.assertTrue(
            str(item.source_path).replace("\\", "/").endswith(
                "artifact-templates/code-change-contract.md"
            )
        )

        rendered = render_infrastructure_plan(FIXTURES / "empty-repo")
        rendered_targets = [
            artifact["target_path"] for artifact in rendered["rendered_artifacts"]["files"]
        ]
        self.assertEqual(rendered_targets.count(target), 1)

        contract_bytes = item.source_path.read_bytes()
        contract_text = contract_bytes.decode("utf-8")
        fields = re.findall(r"^- `?([a-z][a-z0-9_]*)`?:", contract_text, re.MULTILINE)
        self.assertEqual(fields, expected_fields)
        self.assertEqual(len(fields), 8)
        self.assertEqual(len(set(fields)), 8)

        workflow_text = self._template_text("workflows", "coding-standards.md")
        checklist_path = TEMPLATE_ROOT / "artifact-templates" / "coding-standard-checklist.md"
        checklist_bytes = checklist_path.read_bytes()
        checklist_text = checklist_bytes.decode("utf-8")
        lower_contract = contract_text.lower()
        lower_checklist = checklist_text.lower()

        for heading in checklist_headings:
            with self.subTest(heading=heading):
                self.assertNotIn(heading.lower(), lower_contract)
                self.assertNotIn(heading.lower(), workflow_text)

        self.assertIn(target, workflow_text)
        self.assertIn("default generation context", workflow_text)
        default_context_block = next(
            block
            for block in re.split(r"\n\s*\n", workflow_text)
            if "default generation context" in block
        )
        self.assertIn(target, default_context_block)
        self.assertNotIn(
            ".codex/artifact-templates/coding-standard-checklist.md",
            default_context_block,
        )
        self.assertIn(".codex/workflows/coding-standards.md", lower_contract)
        self.assertIn(".codex/artifact-templates/coding-standard-checklist.md", lower_contract)
        self.assertIn(target, lower_checklist)
        self.assertIn(".codex/workflows/coding-standards.md", lower_checklist)
        self.assertIn("reviewer", lower_checklist)
        self.assertIn("reference-only", lower_checklist)

        self.assertEqual(contract_text.encode("utf-8"), contract_bytes)
        self.assertFalse(contract_bytes.startswith(b"\xef\xbb\xbf"))
        self.assertLess(
            len(contract_bytes),
            len(checklist_bytes),
            f"compact/checklist UTF-8 byte delta: {len(contract_bytes) - len(checklist_bytes)}",
        )
        self.assertLess(
            len(contract_text.splitlines()),
            len(checklist_text.splitlines()),
            "compact contract must use fewer line-context units than the retained checklist",
        )

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

    def test_code_quality_profile_has_one_canonical_registration_and_dry_run_render(self):
        target = ".codex/artifact-templates/code-quality-profile.md"
        targets = [item.target_path for item in required_templates()]
        self.assertEqual(targets.count(target), 1)

        item = template_by_target(target)
        self.assertEqual(item.key, "artifact-code-quality-profile")
        self.assertEqual(item.category, "artifact-templates")
        self.assertTrue(
            str(item.source_path).replace("\\", "/").endswith(
                "artifact-templates/code-quality-profile.md"
            )
        )

        rendered = render_infrastructure_plan(FIXTURES / "empty-repo")
        rendered_targets = [
            artifact["target_path"]
            for artifact in rendered["rendered_artifacts"]["files"]
        ]
        self.assertEqual(rendered_targets.count(target), 1)

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
