import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
PRODUCT_AGENT_OS = DOCS / "product-agent-os"
MKDOCS = ROOT / "mkdocs.yml"
CHECK_DOCS = ROOT / "tools" / "check_docs.py"
SOURCE_REGISTRY = DOCS / "sources" / "registry.md"
TRACK_BACKLOG = DOCS / "sources" / "product-agent-os-track-8-detailed-backlog.md"


class ProductAgentOsDocsTest(unittest.TestCase):
    def test_t8h_dedicated_docs_pages_exist_with_operating_contracts(self):
        expected_pages = {
            "scenarios.md": [
                "usage_mode",
                "first response",
                "minimum artifacts",
                "approval boundary",
                "verification gates",
                "bug_rescue",
                "greenfield_idea",
                "complex_system_acceleration",
                "release_packaging",
            ],
            "behavioral-evals.md": [
                "behavioral-workflows.json",
                "expected behavior",
                "forbidden behavior",
                "fixture eval",
                "transcript/session eval runner",
                "evidence-before-completion",
                "residual risk",
            ],
            "codex-compatibility.md": [
                "Codex App",
                "CLI",
                "IDE extension",
                ".codex-plugin/plugin.json",
                "skills",
                "MCP",
                "staged hooks",
                "validate_codex_compatibility.py",
                "no standalone Agents SDK",
                "no separate OpenAI API key",
            ],
        }

        for filename, terms in expected_pages.items():
            with self.subTest(filename=filename):
                path = PRODUCT_AGENT_OS / filename
                self.assertTrue(path.exists(), path)
                text = path.read_text(encoding="utf-8")
                self.assertIn("Source status:", text)
                self.assertIn("Inputs", text)
                self.assertIn("Outputs", text)
                self.assertIn("Verification", text)
                self.assertIn("Risks", text)
                for term in terms:
                    self.assertIn(term, text)

    def test_t8h_docs_are_in_nav_and_required_docs_check(self):
        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")

        for path in [
            "product-agent-os/scenarios.md",
            "product-agent-os/behavioral-evals.md",
            "product-agent-os/codex-compatibility.md",
        ]:
            with self.subTest(path=path):
                self.assertIn(path, nav)
                self.assertIn(path.replace("/", '" / "'), check_docs)

    def test_track9_methodology_intelligence_docs_exist(self):
        path = PRODUCT_AGENT_OS / "methodology-intelligence.md"
        self.assertTrue(path.exists(), path)

        text = path.read_text(encoding="utf-8")
        self.assertIn("Source status:", text)
        self.assertIn("Inputs", text)
        self.assertIn("Outputs", text)
        self.assertIn("Verification", text)
        self.assertIn("Risks", text)

        nav = MKDOCS.read_text(encoding="utf-8")
        check_docs = CHECK_DOCS.read_text(encoding="utf-8")
        self.assertIn("methodology-intelligence.md", nav)
        self.assertIn('product-agent-os" / "methodology-intelligence.md', check_docs)

    def test_t8h_and_t8gy_source_and_backlog_closure_are_documented(self):
        registry = SOURCE_REGISTRY.read_text(encoding="utf-8")
        backlog = TRACK_BACKLOG.read_text(encoding="utf-8")

        self.assertIn("Product-Agent OS Track 8 scenario, eval and transcript docs", registry)
        self.assertIn("docs/product-agent-os/scenarios.md", registry)
        self.assertIn("docs/product-agent-os/behavioral-evals.md", registry)
        self.assertIn("docs/product-agent-os/codex-compatibility.md", registry)
        self.assertIn("plugins/product-agent-os/scripts/product_agent_os/discovery.py", registry)
        self.assertIn("plugins/product-agent-os/scripts/run_transcript_eval.py", registry)
        self.assertIn("T8-D", registry)
        self.assertIn("verification_status:", registry)

        self.assertIn("| `done` | `T8-H` system docs and control-plane sync |", backlog)
        self.assertIn("dedicated scenario, behavioral eval and Codex compatibility docs", backlog)
        self.assertIn("| `T8-GY` behavioral workflow evals | `done` |", backlog)
        self.assertIn("deterministic transcript/session runner", backlog)
        self.assertIn("| `T8-D` discovery model | `done` |", backlog)
        self.assertIn("methodology_applicability", backlog)


if __name__ == "__main__":
    unittest.main()
