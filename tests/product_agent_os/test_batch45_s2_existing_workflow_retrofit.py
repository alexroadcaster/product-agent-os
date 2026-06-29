import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class Batch45S2ExistingWorkflowRetrofitTest(unittest.TestCase):
    def test_core_workflows_reference_professional_code_authoring_contract(self):
        expectations = {
            "plugins/product-agent-os/assets/templates/workflows/development-standards.md": [
                "professional code authoring",
                ".codex/workflows/coding-standards.md",
                ".codex/artifact-templates/coding-standard-checklist.md",
                "one_line_candidate",
                "negative_dependency_rule",
                "deep_module_check",
                "legacy_seam_check",
                "not_applicable",
            ],
            "plugins/product-agent-os/assets/templates/workflows/build-slice.md": [
                ".codex/workflows/coding-standards.md",
                "existing-capability scan",
                "selected leverage path",
                "negative_dependency_rule",
                "not_applicable",
            ],
            "plugins/product-agent-os/assets/templates/workflows/review-slice.md": [
                "professional code authoring risk",
                "unnecessary custom code",
                "dependency debt",
                "low-signal comments",
                "unsupported code-quality claims",
            ],
            "plugins/product-agent-os/assets/templates/workflows/legacy-onboarding.md": [
                "legacy_seam_check",
                "characterization evidence",
                "no-big-rewrite boundary",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

    def test_high_risk_domain_workflows_have_leverage_and_debt_gates(self):
        expectations = {
            "plugins/product-agent-os/assets/templates/workflows/bug-rescue.md": [
                "existing-capability scan",
                "smallest-fix leverage path",
                "one-line existing api/helper/config fix",
            ],
            "plugins/product-agent-os/assets/templates/workflows/api-migration.md": [
                "framework-native",
                "current clients",
                "idempotency/error/retry/timeout decision",
                "custom protocol",
            ],
            "plugins/product-agent-os/assets/templates/workflows/data-migration.md": [
                "existing migration tooling",
                "database-native operations",
                "custom migration code",
            ],
            "plugins/product-agent-os/assets/templates/workflows/security-sensitive-change.md": [
                "secure-default leverage decision",
                "custom security logic",
                "project security helpers",
            ],
            "plugins/product-agent-os/assets/templates/workflows/ci-stabilization.md": [
                "existing ci/tooling leverage decision",
                "custom ci scripts",
                "dependency updates",
            ],
            "plugins/product-agent-os/assets/templates/workflows/desktop-local-first.md": [
                "platform-native",
                "current-helper alternatives",
                "custom desktop filesystem",
            ],
            "plugins/product-agent-os/assets/templates/workflows/complex-system-acceleration.md": [
                "coding-standard sub-gate per code-owning slice",
                "existing-capability scan",
                "unsupported code-quality claims",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

    def test_api_dependency_and_quality_artifacts_carry_professional_rules(self):
        expectations = {
            "plugins/product-agent-os/assets/templates/artifact-templates/api-style-guide.md": [
                "professional coding decisions",
                "framework-native option",
                "idempotency rule",
                "retry behavior",
                "timeout behavior",
                "dependency decision",
            ],
            "plugins/product-agent-os/assets/templates/artifact-templates/supply-chain-review.md": [
                "negative_dependency_rule",
                "rejected no-new-dependency alternatives",
                "rollback/removal path",
            ],
            "plugins/product-agent-os/assets/templates/artifact-templates/quality-strategy.md": [
                "professional_code_authoring_evidence_present",
                "unsupported code-quality claims",
                "cleverness budget",
            ],
            "plugins/product-agent-os/assets/templates/artifact-templates/plan-quality-check.md": [
                "professional code authoring check",
                "one_line_candidate",
                "negative_dependency_rule",
                "legacy_seam_check",
                "unsupported code-quality claims",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

    def test_agent_profiles_and_subagent_packets_carry_code_authoring_handoff_fields(self):
        expectations = {
            "plugins/product-agent-os/assets/templates/agents/builder.toml": [
                ".codex/workflows/coding-standards.md",
                "existing-capability scan",
                "one_line_candidate",
                "unsupported code-quality claims",
            ],
            "plugins/product-agent-os/assets/templates/agents/reviewer.toml": [
                "professional coding failures",
                "dependency debt",
                "low-signal comments",
                "unsupported code-quality claims",
            ],
            "plugins/product-agent-os/assets/templates/agents/architect.toml": [
                "professional coding sub-gate",
                "selected leverage path",
                "dependency decision",
                "legacy seam check",
            ],
            "plugins/product-agent-os/assets/templates/agents/tester.toml": [
                "code-quality evidence status",
                "unsupported code-quality claims",
            ],
            "plugins/product-agent-os/assets/templates/artifact-templates/subagent-context-packet.md": [
                "coding-standard workflow/checklist included",
                "existing-capability scan required",
                "selected leverage path required",
                "unsupported code-quality claims required",
            ],
            "plugins/product-agent-os/assets/templates/artifact-templates/subagent-result-packet.md": [
                "coding-standard workflow/checklist used",
                "existing-capability scan",
                "code-quality evidence",
                "unsupported code-quality claims",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

        handoff_eval = self.read_json("plugins/product-agent-os/assets/templates/evals/handoff-completeness.json")
        case = next(item for item in handoff_eval["cases"] if item["id"] == "professional-code-authoring-handoff")
        self.assertIn("coding-standard workflow/checklist", case["expected"]["fields"])
        self.assertIn("unsupported code-quality claims", case["expected"]["fields"])
        self.assertIn("without raw research body or raw conversation history", case["expected"]["result"].lower())

    def test_local_plugin_skills_reference_s2_contract_without_dispatch_claims(self):
        expectations = {
            "plugins/product-agent-os/skills/implementation-planner/SKILL.md": [
                "professional code authoring input",
                ".codex/workflows/coding-standards.md",
                "existing_capability_scan",
                "negative_dependency_rule",
                "not_applicable",
            ],
            "plugins/product-agent-os/skills/agent-team-designer/SKILL.md": [
                "professional code authoring handoff inputs",
                "coding-standard workflow/checklist status",
                "unsupported code-quality claims",
                "do not auto-dispatch subagents",
            ],
            "plugins/product-agent-os/skills/docs-maintainer/SKILL.md": [
                "professional code authoring docs inputs",
                "unsupported activation claims",
                "do not imply hooks, runtime routes, html, subagent execution, or automation are active",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

        process = self.text("plugins/product-agent-os/skills/agent-team-designer/SKILL.md").split("## outputs")[0]
        process = process.split("## process", 1)[1]
        numbers = [int(match.group(1)) for match in re.finditer(r"(?m)^(\d+)\. ", process)]
        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))

    def test_public_docs_and_review_playbooks_are_synced(self):
        expectations = {
            "docs/product-agent-os/development-standards.md": [
                "профессиональное написание кода",
                ".codex/workflows/coding-standards.md",
                ".codex/artifact-templates/coding-standard-checklist.md",
                "наличие шаблонов не является",
            ],
            "docs/product-agent-os/development-standards.en.md": [
                "professional code authoring",
                ".codex/workflows/coding-standards.md",
                ".codex/artifact-templates/coding-standard-checklist.md",
                "template availability is not runtime enforcement",
            ],
            "docs/playbooks/code-review.md": [
                "профессиональный review кода",
                "unnecessary custom code",
                "negative_dependency_rule",
                "предпочтения только по стилю",
            ],
            "docs/playbooks/code-review.en.md": [
                "professional coding review",
                "unnecessary custom code",
                "negative_dependency_rule",
                "style-only preferences are not blockers",
            ],
        }

        for rel_path, terms in expectations.items():
            with self.subTest(rel_path=rel_path):
                self.assert_terms(rel_path, terms)

    def assert_terms(self, rel_path: str, terms: list[str]) -> None:
        text = self.text(rel_path)
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term.lower(), text)

    @staticmethod
    def text(rel_path: str) -> str:
        return (ROOT / rel_path).read_text(encoding="utf-8").lower()

    @staticmethod
    def read_json(rel_path: str) -> dict:
        return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
