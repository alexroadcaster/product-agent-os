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

        self.assertNotIn("mcpServers", data)
        self.assertIn("context7", data)
        context7 = data["context7"]
        self.assertEqual(context7["command"], "npx")
        self.assertEqual(context7["args"], ["-y", "@upstash/context7-mcp"])
        self.assertEqual(context7["startup_timeout_sec"], 20)
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

    def test_main_spec_classifies_track_three_workflow_templates_explicitly(self):
        text = SPEC.read_text(encoding="utf-8")

        self.assertNotIn("    source-context-researcher/", text)
        self.assertNotIn("    worktree-ownership-planner/", text)
        self.assertNotIn("    build-slice-runner/", text)
        self.assertIn("Track 3 workflow templates", text)
        self.assertIn("source-context-pack.md", text)
        self.assertIn("worktree-ownership.md", text)
        self.assertIn("build-slice.md", text)
        self.assertIn("development-standards.md", text)
        self.assertIn("documentation-system.md", text)
        self.assertIn("artifact templates", text)
        self.assertIn("domain-modeling.md", text)
        self.assertIn("metric-spec.md", text)

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
