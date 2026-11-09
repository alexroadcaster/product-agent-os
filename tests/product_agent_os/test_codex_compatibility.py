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
    def test_current_package_is_locally_compatible_with_distribution_gated(self):
        report = validate_codex_compatibility(PLUGIN_ROOT)

        self.assertEqual(report["status"], "compatible")
        self.assertEqual(report["component_inventory"]["mcp"]["server_names"], ["context7"])
        self.assertEqual(report["component_inventory"]["mcp"]["format"], "codex_wrapped")
        self.assertEqual(report["component_inventory"]["status"], "present_unverified")
        self.assertEqual(report["distribution"]["status"], "gated")
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
        self.assertEqual(checks["context7_mcp"]["status"], "ok")

    def test_unsupported_surface_cannot_be_promoted_by_observation(self):
        report = validate_codex_compatibility(PLUGIN_ROOT, observations={"surface": "IDE extension", "native_plugin_observed": True})
        matrix = report["capability_matrix"]
        self.assertEqual(matrix["IDE extension"]["native_plugin"]["support"], "unsupported")
        self.assertEqual(matrix["IDE extension"]["native_plugin"]["observation"], "conflicts_with_documented_support")
        self.assertEqual(matrix["CLI"]["native_plugin"]["support"], "documented")
        self.assertEqual(matrix["CLI"]["native_plugin"]["observation"], "not_verified")
        self.assertEqual(matrix["IDE extension"]["standalone_skills"]["support"], "documented")

    def test_missing_unknown_old_and_surface_specific_version(self):
        cases = [({}, "missing"), ({"surface": "CLI", "client_version": "old"}, "unknown"),
                 ({"surface": "CLI", "client_version": "0.158.0"}, "below_documented_minimum"),
                 ({"surface": "CLI", "client_version": "0.159.0"}, "meets_documented_minimum"),
                 ({"surface": "Codex App", "client_version": "0.158.0"}, "minimum_not_documented"),
                 ({"surface": "other", "client_version": "0.159.0"}, "unknown_surface")]
        for inputs, expected in cases:
            with self.subTest(inputs=inputs):
                report = validate_codex_compatibility(PLUGIN_ROOT, observations={"configured_model": "gpt-6.1-terra", **inputs})
                self.assertEqual(report["host_diagnostics"]["client"]["status"], expected)
                self.assertEqual(report["host_diagnostics"]["model"]["status"], "not_verified")
                self.assertEqual(report["host_diagnostics"]["trust"]["status"], "unknown")

    def test_observations_are_allowlisted_and_do_not_certify_access(self):
        report = validate_codex_compatibility(PLUGIN_ROOT, observations={"surface": "CLI", "configured_model": "gpt-6.1-sol", "observed_model": "gpt-6.1-terra", "trust": "trusted", "token": "secret-canary", "client_version": "secret-canary"})
        self.assertEqual(report["host_diagnostics"]["model"]["status"], "mismatch")
        self.assertEqual(report["host_diagnostics"]["trust"]["status"], "observed")
        self.assertEqual(report["host_diagnostics"]["account_access"], "not_verified")
        self.assertNotIn("secret-canary", json.dumps(report))
        self.assertIn("unrecognized_observation_fields", report["host_diagnostics"]["issues"])

    def test_canonical_cache_missing_match_drift_and_invalid(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical, cache = root / "canonical", root / "cache"
            (canonical / "skills/sample").mkdir(parents=True)
            (canonical / "skills/sample/SKILL.md").write_text("baseline", encoding="utf-8")
            def provenance(cache_path=None):
                return validate_codex_compatibility(canonical, cache_root=cache_path)["host_diagnostics"]["provenance"]
            self.assertEqual(provenance()["status"], "cache_not_provided")
            self.assertEqual(provenance(cache)["status"], "needs_review")
            shutil.copytree(canonical, cache)
            self.assertEqual(provenance(cache)["status"], "match")
            (cache / "skills/sample/SKILL.md").write_text("changed", encoding="utf-8")
            self.assertEqual(provenance(cache)["status"], "drift")
            self.assertNotIn(str(root), json.dumps(provenance(cache)))

    def test_ambiguous_legacy_mcp_and_duplicate_json_fail_closed(self):
        from product_agent_os.plugin_components import resolve_plugin_components
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex-plugin").mkdir()
            (root / ".codex-plugin/plugin.json").write_text('{"name":"sample"}', encoding="utf-8")
            for server in ({"command": "npx", "url": "https://example.test"}, {"command": "npx", "mystery": True}, {"type": "sse", "url": "https://example.test", "command": "npx"}, {"command": "npx", "startup_timeout_sec": True}):
                (root / ".mcp.json").write_text(json.dumps({"mcpServers": {"sample": server}}), encoding="utf-8")
                self.assertEqual(resolve_plugin_components(root)["mcp"]["status"], "needs_review", server)
            (root / ".mcp.json").write_text('{"mcpServers":{},"mcpServers":{"sample":{"command":"npx"}}}', encoding="utf-8")
            self.assertEqual(resolve_plugin_components(root)["status"], "needs_review")

    def test_cli_projects_input_without_mutating_files(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inputs = root / "observations.json"
            for payload, expected_code in [('[]', 2), ('{"surface":"CLI","surface":"Codex App"}', 2),
                                           ('{"surface":"CLI","client_version":"0.159.0","configured_model":"gpt-6.1-terra","observed_model":"gpt-6.1-terra"}', 0)]:
                inputs.write_text(payload, encoding="utf-8")
                result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "validate_codex_compatibility.py"), "--observations", str(inputs)], capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, expected_code, result.stderr)
                report = json.loads(result.stdout)
                if expected_code == 0:
                    self.assertEqual(report["host_diagnostics"]["model"]["status"], "match")
                    self.assertEqual(report["host_diagnostics"]["account_access"], "not_verified")
                self.assertEqual(inputs.read_text(encoding="utf-8"), payload)
                self.assertEqual(list(root.iterdir()), [inputs])

    def test_invalid_observation_types_and_oversized_component_are_not_evidence(self):
        for inputs in ([], {"surface": {}, "configured_model": [], "observed_model": {}, "trust": [], "native_plugin_observed": "true"}):
            report = validate_codex_compatibility(PLUGIN_ROOT, observations=inputs)
            self.assertEqual(report["host_diagnostics"]["surface"], "unknown")
            self.assertEqual(report["host_diagnostics"]["model"]["status"], "not_verified")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skills/sample").mkdir(parents=True)
            (root / "skills/sample/SKILL.md").write_bytes(b"x" * (1024 * 1024 + 1))
            report = validate_codex_compatibility(PLUGIN_ROOT, cache_root=root)
            self.assertEqual(report["host_diagnostics"]["provenance"]["status"], "needs_review")

    def test_cache_junction_is_not_followed(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp)
            (cache / "plugin.json").write_text('{}', encoding="utf-8")
            with patch.object(Path, "is_junction", return_value=True, create=True):
                report = validate_codex_compatibility(PLUGIN_ROOT, cache_root=cache)
            self.assertEqual(report["host_diagnostics"]["provenance"]["cache"]["status"], "needs_review")

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
