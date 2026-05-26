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

    def test_ai_rag_report_renders_evidence_approvals_gaps_and_redacts_sensitive_terms(self):
        from product_agent_os.methodology_report import render_methodology_audit_report

        audit = {
            "maturity_level": {"selected": "production", "confidence": "medium", "reasons": []},
            "complexity_profile": {"selected": "high_risk", "confidence": "medium", "reasons": []},
            "delivery_map": {"surface_map": {"workspace": "C:\\Users\\person\\project\\repo"}},
            "methodology_domains": [{"id": "llm_ai_rag", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "priority": "P1_high_risk",
                    "domain": "llm_ai_rag",
                    "gate": "ai_incident_workflow_present",
                    "artifact": "guardrail-matrix.md",
                    "reason": "Failed eval, hallucination report or tool misuse needs an AI incident workflow.",
                    "evidence_required": [
                        "owner",
                        "severity",
                        "mitigation",
                        "follow-up eval",
                        "Security/Privacy handoff",
                    ],
                    "evidence_owner": "AI product owner",
                    "approval_boundary": "approval_required before external release",
                    "accepted_gap_option": "explicit_gap_accepted with owner and review date",
                    "residual_risk": "raw private chat log and private customer data can leak in incident evidence.",
                    "safe_next_action": "Stage guardrail-matrix.md before release.",
                }
            ],
            "questions_for_owner": ["Should review C:\\Users\\person\\project\\repo trace evidence?"],
            "provisional_assumptions": [],
            "safe_next_action": "Stage guardrail-matrix.md",
        }

        report = render_methodology_audit_report(audit)

        for expected in [
            "llm_ai_rag",
            "ai_incident_workflow_present",
            "evidence_required",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
            "Security/Privacy handoff",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, report)
        self.assertNotIn("C:\\Users\\person", report)
        self.assertNotIn("raw private chat log", report.lower())
        self.assertNotIn("private customer data", report.lower())

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
