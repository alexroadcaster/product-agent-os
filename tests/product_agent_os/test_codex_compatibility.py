import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
PLUGIN_ROOT = ROOT / "plugins" / "product-agent-os"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.codex_compatibility import validate_codex_compatibility  # noqa: E402


class CodexCompatibilityTest(unittest.TestCase):
    def test_product_agent_os_package_is_codex_only_compatible(self):
        report = validate_codex_compatibility(PLUGIN_ROOT)

        self.assertEqual(report["status"], "compatible")
        self.assertEqual(report["supported_surfaces"], ["Codex App", "CLI", "IDE extension"])
        self.assertFalse(report["requires_non_codex_adapters"])
        self.assertEqual(report["forbidden_required_adapters"], [])
        self.assertEqual(report["non_codex_adapter_paths_present"], [])

        checks = report["checks"]
        for key in [
            "codex_manifest",
            "bundled_skills",
            "context7_mcp",
            "staged_hooks",
            "readme_codex_scope",
            "non_codex_adapters_absent",
        ]:
            with self.subTest(key=key):
                self.assertEqual(checks[key]["status"], "ok")

    def test_codex_compatibility_report_is_json_serializable(self):
        report = validate_codex_compatibility(PLUGIN_ROOT)

        payload = json.loads(json.dumps(report, sort_keys=True))

        self.assertIn(".codex-plugin/plugin.json", payload["evidence"]["files"])
        self.assertIn("skills", payload["evidence"]["directories"])
        self.assertIn("assets/templates/hooks/hooks.json", payload["evidence"]["files"])


if __name__ == "__main__":
    unittest.main()
