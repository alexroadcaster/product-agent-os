import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class MethodologyReportTest(unittest.TestCase):
    def test_report_contains_required_sections(self):
        from product_agent_os.methodology_audit import build_methodology_audit
        from product_agent_os.methodology_report import render_methodology_audit_report

        with tempfile.TemporaryDirectory() as tmp:
            workspace = self._workspace(Path(tmp))
            report = render_methodology_audit_report(build_methodology_audit(workspace, intent_hint="ship API feature"))

        self.assertIn("# Product-Agent OS Methodology Audit", report)
        for heading in [
            "Maturity Level",
            "Complexity Profile",
            "Delivery Map",
            "Recommendations",
            "Questions For Owner",
            "Provisional Assumptions",
            "Safe Next Action",
        ]:
            self.assertIn(heading, report)

    def test_report_redacts_raw_absolute_local_paths(self):
        from product_agent_os.methodology_report import render_methodology_audit_report

        audit = {
            "maturity_level": {"selected": "team", "confidence": "medium", "reasons": []},
            "complexity_profile": {"selected": "standard", "confidence": "medium", "reasons": []},
            "delivery_map": {"surface_map": {"workspace": "C:\\Users\\person\\project\\repo"}},
            "methodology_domains": [],
            "recommendations": [],
            "questions_for_owner": ["Review C:\\Users\\person\\project\\repo before writes"],
            "provisional_assumptions": [],
            "safe_next_action": "Inspect C:\\Users\\person\\project\\repo",
        }

        report = render_methodology_audit_report(audit)

        self.assertNotIn("C:\\Users\\person", report)

    def test_cli_prints_json_when_requested(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = self._workspace(Path(tmp))
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_methodology_audit.py"),
                    str(workspace),
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        data = json.loads(completed.stdout)
        self.assertIn("maturity_level", data)
        self.assertEqual(data["write_policy"], "read_only")

    def _workspace(self, root: Path) -> Path:
        (root / "package.json").write_text('{"scripts":{"test":"vitest"}}\n', encoding="utf-8")
        (root / "openapi.yaml").write_text(
            "openapi: 3.1.0\ninfo:\n  title: API\n  version: 1.0.0\npaths: {}\n",
            encoding="utf-8",
        )
        return root


if __name__ == "__main__":
    unittest.main()
