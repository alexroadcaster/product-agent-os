import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"
SPEC = ROOT / "docs" / "product-agent" / "product-agent-os-plugin-spec.md"


class PluginStructureTest(unittest.TestCase):
    def test_manifest_exists_and_points_to_packaged_assets(self):
        manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.exists(), "plugin.json must exist")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "product-agent-os")
        self.assertEqual(data["skills"], "./skills/")
        self.assertEqual(data["mcpServers"], "./.mcp.json")
        self.assertEqual(data["interface"]["displayName"], "Product-Agent OS")
        self.assertIn("Write", data["interface"]["capabilities"])

    def test_bundled_mcp_config_registers_context7_without_secret_placeholder(self):
        mcp_path = PLUGIN_ROOT / ".mcp.json"
        self.assertTrue(mcp_path.exists(), ".mcp.json must exist")
        data = json.loads(mcp_path.read_text(encoding="utf-8"))

        self.assertEqual(set(data), {"mcpServers"})
        self.assertIn("context7", data["mcpServers"])
        context7 = data["mcpServers"]["context7"]
        self.assertEqual(context7["command"], "npx")
        self.assertEqual(context7["args"], ["-y", "@upstash/context7-mcp"])
        self.assertNotIn("startup_timeout_sec", context7)
        self.assertNotIn("YOUR_API_KEY", json.dumps(data))
        self.assertNotIn("CONTEXT7_API_KEY", json.dumps(data))

    def test_required_package_directories_exist(self):
        required = [
            ".codex-plugin",
            "skills",
            "hooks",
            "scripts",
            "assets",
        ]
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((PLUGIN_ROOT / relative).exists())

    def test_methodology_catalog_is_packaged(self):
        catalog = PLUGIN_ROOT / "assets" / "methodology" / "methodology-catalog.json"

        self.assertTrue(catalog.is_file())

    def test_methodology_audit_report_template_is_packaged(self):
        template = PLUGIN_ROOT / "assets" / "templates" / "reports" / "methodology-audit-report.md"

        self.assertTrue(template.is_file())

    def test_main_spec_uses_product_facing_public_contract_without_track_terms(self):
        text = SPEC.read_text(encoding="utf-8")

        self.assertNotIn("    source-context-researcher/", text)
        self.assertNotIn("    worktree-ownership-planner/", text)
        self.assertNotIn("    build-slice-runner/", text)
        self.assertNotRegex(text, r"\b(Task|Track|Batch)\b|T[0-9]+-|B[0-9]+-")
        self.assertIn("Source status:", text)
        self.assertIn("Product capability areas", text)
        self.assertIn("lifecycle routing", text)
        self.assertIn("control-plane artifacts", text)
        self.assertIn("staged infrastructure", text)
        self.assertIn("methodology routing", text)
        self.assertIn("behavioral и transcript evals", text)
        self.assertIn("Codex compatibility checks", text)
        self.assertIn("approval-bound real testing", text)
        self.assertIn("artifact templates", text)
        self.assertIn("Generated files являются proposals или managed artifacts", text)
        self.assertIn("REQUIREMENTS.md", text)
        self.assertIn("PLAN.md", text)
        self.assertIn("TEST.md", text)
        self.assertIn("EVALS.md", text)
        self.assertIn("RUNLOG.md", text)

    def test_optional_agents_sdk_runner_design_is_documented_but_not_activated(self):
        runner_design = (
            ROOT
            / "docs"
            / "superpowers"
            / "specs"
            / "2026-05-14-product-agent-os-agents-sdk-runner-design.md"
        )

        self.assertTrue(runner_design.exists())
        text = runner_design.read_text(encoding="utf-8")
        self.assertIn("Source status:", text)
        self.assertIn("Codex MCP", text)
        self.assertIn("model and reasoning", text)
        self.assertIn("redaction", text)
        self.assertFalse((PLUGIN_ROOT / "scripts" / "agents_sdk_runner").exists())

    def test_codex_runtime_runner_exists_but_is_not_default_activated(self):
        runner_package = PLUGIN_ROOT / "scripts" / "codex_runtime_runner"
        runner_wrapper = PLUGIN_ROOT / "scripts" / "run_codex_runtime_runner.py"
        manifest_path = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
        manifest_text = manifest_path.read_text(encoding="utf-8")
        mcp_text = (PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8")

        self.assertTrue(runner_package.is_dir())
        self.assertTrue(runner_wrapper.exists())
        self.assertNotIn("run_codex_runtime_runner.py", manifest_text)
        self.assertNotIn("codex_runtime_runner", manifest_text)
        self.assertNotIn("codex_runtime_runner", mcp_text)


if __name__ == "__main__":
    unittest.main()
