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

    def test_security_privacy_report_renders_scan_status_approvals_gaps_and_redacts_sensitive_terms(self):
        from product_agent_os.methodology_report import render_methodology_audit_report

        audit = {
            "maturity_level": {"selected": "regulated", "confidence": "medium", "reasons": []},
            "complexity_profile": {"selected": "high_risk", "confidence": "medium", "reasons": []},
            "delivery_map": {"surface_map": {"workspace": "C:\\Users\\person\\project\\repo"}},
            "methodology_domains": [{"id": "security_privacy_compliance", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "priority": "P1_high_risk",
                    "domain": "security_privacy_compliance",
                    "gate": "codex_security_scan_status_present",
                    "artifact": "security-risk-review.md",
                    "reason": "Codex Security scan status must be explicit: run with evidence, not requested or blocked.",
                    "evidence_required": [
                        "Codex Security scan status",
                        "approval_boundary",
                        "accepted_gap_option",
                    ],
                    "evidence_owner": "security or product owner",
                    "approval_boundary": "approval_required before external security-system mutation",
                    "accepted_gap_option": "explicit_gap_accepted with owner and review date",
                    "residual_risk": "raw private chat log, private customer data, payment data and raw PII can leak in security evidence.",
                    "safe_next_action": "Stage security-risk-review.md before completion claim.",
                }
            ],
            "questions_for_owner": ["Should review C:\\Users\\person\\project\\repo security evidence?"],
            "provisional_assumptions": [],
            "safe_next_action": "Stage security-risk-review.md",
        }

        report = render_methodology_audit_report(audit)

        for expected in [
            "security_privacy_compliance",
            "codex_security_scan_status_present",
            "Codex Security scan status",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, report)
        self.assertNotIn("C:\\Users\\person", report)
        self.assertNotIn("raw private chat log", report.lower())
        self.assertNotIn("private customer data", report.lower())
        self.assertNotIn("payment data", report.lower())
        self.assertNotIn("raw pii", report.lower())

    def test_delivery_report_renders_boundaries_without_implying_external_action(self):
        from product_agent_os.methodology_report import render_methodology_audit_report

        audit = {
            "maturity_level": {"selected": "production", "confidence": "medium", "reasons": []},
            "complexity_profile": {"selected": "complex", "confidence": "medium", "reasons": []},
            "delivery_map": {"surface_map": {"workspace": "C:\\Users\\person\\project\\repo"}},
            "methodology_domains": [{"id": "delivery_release_operations", "status": "applicable_missing"}],
            "recommendations": [
                {
                    "priority": "P0_blocker",
                    "domain": "delivery_release_operations",
                    "gate": "external_release_approval_present",
                    "artifact": "approval-record.md",
                    "reason": "External release actions need explicit approval and rollback/unpublish path.",
                    "evidence_required": ["approval_required", "rollback/unpublish"],
                    "evidence_owner": "release operator",
                    "approval_boundary": "approval_required before publish, tag, deployment or package registry mutation",
                    "accepted_gap_option": "explicit_gap_accepted with owner and review date",
                    "residual_risk": "External release action can be implied without approval.",
                    "safe_next_action": "Stage approval-record.md before external action.",
                },
                {
                    "priority": "P1_high_risk",
                    "domain": "delivery_release_operations",
                    "gate": "delivery_unsupported_claims_rejected",
                    "artifact": "release-readiness.md",
                    "reason": "Unsupported delivery claim appeared as evidence.",
                    "evidence_required": ["automation is safer because it is repeatable", "claim disposition"],
                    "evidence_owner": "release operator",
                    "approval_boundary": "approval_required before automation activation",
                    "accepted_gap_option": "explicit_gap_accepted with owner and residual risk",
                    "residual_risk": "Repeatable operations can repeat damage without disable path.",
                    "safe_next_action": "Replace unsupported claim with release evidence.",
                },
            ],
            "questions_for_owner": [],
            "provisional_assumptions": [],
            "safe_next_action": "Stage release readiness evidence.",
        }

        report = render_methodology_audit_report(audit)

        for expected in [
            "delivery_release_operations",
            "external_release_approval_present",
            "delivery_unsupported_claims_rejected",
            "approval_boundary",
            "accepted_gap_option",
            "residual_risk",
            "safe_next_action",
            "automation is safer because it is repeatable",
            "no external actions are implied by this report",
            "recommendations remain staged/read-only until explicit approval evidence is recorded",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, report)
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
