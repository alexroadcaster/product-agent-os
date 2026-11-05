import json
import sys
import unittest
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.codex_compatibility import validate_codex_compatibility  # noqa: E402


class CodexCompatibilityTest(unittest.TestCase):
    def test_current_flat_mcp_is_observed_but_requires_schema_review(self):
        report = validate_codex_compatibility(PLUGIN_ROOT)

        self.assertEqual(report["status"], "needs_review")
        self.assertEqual(report["component_inventory"]["mcp"]["server_names"], ["context7"])
        self.assertEqual(report["component_inventory"]["mcp"]["format"], "legacy_flat_observed")
        self.assertEqual(report["component_inventory"]["status"], "needs_review")
        self.assertEqual(report["supported_surfaces"], ["Codex App", "CLI", "IDE extension"])
        self.assertFalse(report["requires_non_codex_adapters"])
        self.assertEqual(report["forbidden_required_adapters"], [])
        self.assertEqual(report["non_codex_adapter_paths_present"], [])

        checks = report["checks"]
        for key in [
            "codex_manifest",
            "bundled_skills",
            "staged_hooks",
            "readme_codex_scope",
            "non_codex_adapters_absent",
        ]:
            with self.subTest(key=key):
                self.assertEqual(checks[key]["status"], "ok")
        self.assertEqual(checks["context7_mcp"]["status"], "needs_review")

    def test_component_resolution_preserves_portable_precedence_without_merging(self):
        from product_agent_os.plugin_components import resolve_plugin_components
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex-plugin").mkdir()
            (root / ".codex-plugin/plugin.json").write_text(json.dumps({"name": "legacy", "skills": "./other", "mcpServers": "./.mcp.json", "hooks": "./legacy-hooks.json"}), encoding="utf-8")
            (root / "plugin.json").write_text(json.dumps({"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": "portable", "extensions": {"com.openai": {}}}), encoding="utf-8")
            (root / "mcp.json").write_text(json.dumps({"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json", "mcpServers": {"docs": {"type": "streamable-http", "url": "https://example.test/mcp"}}}), encoding="utf-8")
            report = resolve_plugin_components(root)
            self.assertEqual(report["format"], "agent_plugins_1.0.0")
            self.assertEqual(report["status"], "present_unverified")
            self.assertEqual(report["settings_source"], "plugin.json:extensions.com.openai")
            self.assertEqual(report["skills"]["paths"], ["skills"])
            self.assertEqual(report["mcp"]["server_names"], ["docs"])
            self.assertNotIn("legacy-hooks.json", json.dumps(report))

    def test_component_resolution_rejects_unsupported_malformed_and_escaped_inputs(self):
        from product_agent_os.plugin_components import resolve_plugin_components
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(resolve_plugin_components(root)["status"], "absent")
            for value in ([], {"$schema": "https://example.test/unknown", "name": "x"}, {"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "name": "x", "extensions": []}):
                (root / "plugin.json").write_text(json.dumps(value), encoding="utf-8")
                self.assertEqual(resolve_plugin_components(root)["status"], "needs_review")
            (root / "plugin.json").unlink()
            (root / ".codex-plugin").mkdir()
            for path in ("../outside.json", "C:/outside.json", "./../outside.json"):
                (root / ".codex-plugin/plugin.json").write_text(json.dumps({"name": "x", "mcpServers": path}), encoding="utf-8")
                self.assertEqual(resolve_plugin_components(root)["status"], "needs_review")

    def test_component_inventory_agrees_across_consumers(self):
        from product_agent_os.batch39_inventory import build_batch39_inventory
        from product_agent_os.discovery import analyze_workspace
        from product_agent_os.plugin_components import resolve_plugin_components
        from product_agent_os.methodology_audit import build_methodology_audit
        expected = resolve_plugin_components(PLUGIN_ROOT)
        package = build_batch39_inventory(workspace=ROOT, plugin_root=PLUGIN_ROOT)["inventory"]["package"]
        audit = analyze_workspace(PLUGIN_ROOT)
        self.assertEqual(package["component_inventory"], expected)
        self.assertEqual(package["mcp_server_keys"], expected["mcp"]["server_names"])
        self.assertEqual(audit["plugin_components"][0]["inventory"], expected)
        self.assertEqual(build_methodology_audit(PLUGIN_ROOT)["plugin_components"][0]["inventory"], expected)

    def test_portable_metadata_and_transport_values_fail_closed(self):
        from product_agent_os.plugin_components import PLUGIN_SCHEMA, MCP_SCHEMA, resolve_plugin_components
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = {"$schema": PLUGIN_SCHEMA, "name": "sample"}
            for extra in ({"version": 1}, {"author": "unknown"}, {"keywords": {}}, {"author": {"token": "hidden"}}):
                (root / "plugin.json").write_text(json.dumps({**base, **extra}), encoding="utf-8")
                self.assertEqual(resolve_plugin_components(root)["status"], "needs_review", extra)
            (root / "plugin.json").write_text(json.dumps(base), encoding="utf-8")
            for server in ({"type": "stdio", "command": [], "args": 1}, {"type": "streamable-http", "url": "https://host.test:bad/mcp"}):
                (root / "mcp.json").write_text(json.dumps({"$schema": MCP_SCHEMA, "mcpServers": {"test": server}}), encoding="utf-8")
                report = resolve_plugin_components(root)
                self.assertEqual(report["status"], "needs_review")
                self.assertNotIn("host.test", json.dumps(report))

    def test_codex_compatibility_report_is_json_serializable(self):
        report = validate_codex_compatibility(PLUGIN_ROOT)

        payload = json.loads(json.dumps(report, sort_keys=True))

        self.assertIn(".codex-plugin/plugin.json", payload["evidence"]["files"])
        self.assertIn("skills", payload["evidence"]["directories"])
        self.assertIn("assets/templates/hooks/hooks.json", payload["evidence"]["files"])


if __name__ == "__main__":
    unittest.main()
