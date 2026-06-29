import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE_ROOT = ROOT / "plugins" / "product-agent-os" / "assets" / "templates"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.routes import plan_route  # noqa: E402
from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: E402
from product_agent_os.behavioral_evals import validate_behavioral_eval_template  # noqa: E402
from product_agent_os.discovery import analyze_workspace  # noqa: E402
from product_agent_os.first_run_analysis import (  # noqa: E402
    build_first_run_analysis_packet,
    validate_first_run_analysis_packet,
)
from product_agent_os.methodology_catalog import load_methodology_catalog  # noqa: E402
from product_agent_os.status_dashboard import render_status_dashboard  # noqa: E402


PROFESSIONAL_CASES = {
    "professional-code-authoring-custom-code-bloat",
    "professional-code-authoring-unnecessary-dependency",
    "professional-code-authoring-missing-existing-capability-scan",
    "professional-code-authoring-comment-noise",
    "professional-code-authoring-shallow-wrapper",
    "professional-code-authoring-unsupported-legacy-rewrite",
}


class Batch45S3ProfessionalCodeAuthoringTest(unittest.TestCase):
    def test_behavioral_context_and_readiness_contracts_include_professional_code_authoring(self):
        behavioral_path = TEMPLATE_ROOT / "evals" / "behavioral-workflows.json"
        report = validate_behavioral_eval_template(behavioral_path)
        behavioral = json.loads(behavioral_path.read_text(encoding="utf-8"))
        cases = {case["name"]: case for case in behavioral["cases"]}

        self.assertEqual(report["status"], "ok")
        self.assertTrue(PROFESSIONAL_CASES.issubset(set(report["required_cases"])))
        self.assertTrue(PROFESSIONAL_CASES.issubset(set(cases)))
        for case_name in PROFESSIONAL_CASES:
            payload = json.dumps(cases[case_name], sort_keys=True)
            with self.subTest(case=case_name):
                self.assertIn("coding-standard-checklist.md", payload)
                self.assertIn("professional_code_authoring", payload)
                self.assertIn("existing", payload)

        agent_context = json.loads((TEMPLATE_ROOT / "evals" / "agent-context-contract.json").read_text(encoding="utf-8"))
        for expected in [
            "local_style_conventions",
            "coding_standards_workflow",
            "coding_standard_checklist",
            "existing_capability_scan_before_custom_code",
            "professional_code_authoring_not_applicable_reason",
            "no_raw_source_leakage",
        ]:
            self.assertIn(expected, agent_context["required_agent_context"])

        readiness = json.loads((TEMPLATE_ROOT / "evals" / "project-readiness.json").read_text(encoding="utf-8"))
        expected = readiness["cases"][0]["expected"]
        self.assertIn("professional_code_authoring", expected["methodology_gates"])
        self.assertIn("professional_code_authoring", expected["methodology_signals"])
        gate = expected["conditional_readiness_gates"]["professional_code_authoring"]
        self.assertIn("one_line_candidate", json.dumps(gate, sort_keys=True))
        self.assertIn("present_unverified", gate["pass_condition"])

    def test_local_code_owning_agents_reference_coding_standard_contract(self):
        for relative in [
            ".codex/agents/builder.toml",
            ".codex/agents/reviewer.toml",
            ".codex/agents/architect.toml",
        ]:
            with self.subTest(agent=relative):
                text = ROOT.joinpath(relative).read_text(encoding="utf-8")
                self.assertIn(".codex/workflows/coding-standards.md", text)
                self.assertIn(".codex/artifact-templates/coding-standard-checklist.md", text)
                self.assertIn("Professional Code Authoring", text)
                self.assertIn("existing", text)

    def test_methodology_discovery_and_runtime_route_surface_status_without_activation(self):
        catalog = load_methodology_catalog()
        quality = {domain["id"]: domain for domain in catalog["domains"]}["quality_testing_evals"]
        workflow = {domain["id"]: domain for domain in catalog["domains"]}["codex_agentic_workflow"]
        shared_gate = catalog["synthesis"]["shared_gates"]["professional_code_authoring_evidence_present"]

        self.assertEqual(shared_gate["owner_domain"], "quality_testing_evals")
        self.assertIn("codex_agentic_workflow", shared_gate["consumer_domains"])
        self.assertIn("professional_code_authoring_evidence_present", quality["gates"])
        self.assertIn("coding-standard-checklist.md", quality["artifacts"])
        self.assertIn("professional_code_authoring_evidence_present", workflow["gates"])

        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "src/app.py": "def clean(value):\n    return value.strip()\n",
                    ".codex/workflows/coding-standards.md": "# Coding Standards\n",
                    ".codex/artifact-templates/coding-standard-checklist.md": "# Checklist\n",
                },
            )
            discovery = analyze_workspace(workspace)

        methodology_intelligence = dict(discovery["methodology_intelligence"])
        methodology_intelligence["methodology_applicability"] = discovery["methodology_applicability"]
        route = plan_route("plan_ready", allow_subagents=False, methodology_intelligence=methodology_intelligence)

        self.assertEqual(discovery["methodology_applicability"]["professional_code_authoring"]["status"], "present_unverified")
        self.assertEqual(route["professional_code_authoring"]["status"], "present_unverified")
        self.assertEqual(route["professional_code_authoring"]["activation"], "present_unverified_until_current_evidence")
        self.assertIn("coding-standard-checklist", json.dumps(route["first_response_contract"], sort_keys=True))
        self.assertNotIn("present_verified", json.dumps(route["professional_code_authoring"], sort_keys=True))

    def test_html_dashboard_and_hook_governance_show_visibility_without_activation(self):
        professional_summary = {
            "schema_version": "first_run_professional_code_authoring_summary_v1",
            "status": "present_unverified",
            "gate": "professional_code_authoring_evidence_present",
            "workflow": ".codex/workflows/coding-standards.md",
            "checklist": ".codex/artifact-templates/coding-standard-checklist.md",
            "required_evidence": ["existing_capability_scan", "one_line_candidate", "dependency_decision"],
            "evidence": ["professional_code_authoring"],
            "next_action": "Record coding-standard-checklist.md before code-quality claims.",
            "generated_view_policy": "orientation_only_not_proof",
            "completion_claim": "not_claimed",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "workspace"
            stage = Path(tmpdir) / "stage"
            workspace.mkdir()
            packet = build_first_run_analysis_packet(
                target_label="synthetic-code-target",
                generated_at="2026-06-29T10:00:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "coding_standard",
                        "path": ".codex/artifact-templates/coding-standard-checklist.md",
                        "digest": "sha256:" + "1" * 64,
                        "provenance": "synthetic_fixture",
                    }
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "present_unverified", "source_artifact": "coding_standard"},
                    "runtime_route": {"status": "present_unverified", "source_artifact": "coding_standard"},
                    "methodology_audit": {"status": "present_unverified", "source_artifact": "coding_standard"},
                    "control_plane": {"status": "present_unverified", "source_artifact": "coding_standard"},
                    "source_policy": {"status": "current", "source_artifact": "coding_standard"},
                    "graph": {"status": "inspection_only", "source_artifact": "coding_standard"},
                    "status_snapshot": {"status": "inspection_only", "source_artifact": "coding_standard"},
                },
                professional_code_authoring_summary=professional_summary,
                safe_next_action="Record coding-standard-checklist.md before code-quality claims.",
            )
            self.assertEqual(validate_first_run_analysis_packet(packet), [])
            render_first_run_analysis_artifact(packet, workspace, output_dir=stage)

            for page_name in [
                "methodology.html",
                "runtime-route.html",
                "code-flow.html",
                "quality-evals.html",
                "risks.html",
                "recommendations.html",
            ]:
                html = stage.joinpath(page_name).read_text(encoding="utf-8")
                with self.subTest(page=page_name):
                    self.assertIn("Professional Code Authoring", html)
                    self.assertIn("professional_code_authoring_evidence_present", html)
                    self.assertIn("orientation_only_not_proof", html)

        dashboard = render_status_dashboard(
            {
                "schema_version": 1,
                "generated_at": "2026-06-29T10:00:00+03:00",
                "professional_code_authoring": professional_summary,
                "dashboard_policy": {
                    "source_of_truth": "generated view only",
                    "write_policy": "read_only",
                    "success_claim_policy": "not_claimed",
                },
            }
        )
        self.assertIn('id="section-professional-code-authoring"', dashboard["html"])
        self.assertIn("professional_code_authoring_evidence_present", dashboard["html"])

        hook_governance = (TEMPLATE_ROOT / "artifact-templates" / "hook-governance.md").read_text(encoding="utf-8")
        pre_hook = (TEMPLATE_ROOT / "hooks" / "pre_tool_use_policy.py").read_text(encoding="utf-8")
        stop_hook = (TEMPLATE_ROOT / "hooks" / "stop_runlog_reminder.py").read_text(encoding="utf-8")
        self.assertIn("Candidate-only status", hook_governance)
        self.assertIn("Approval required before turning a professional-code reminder into an active blocking hook", hook_governance)
        self.assertIn("coding-standards.md", pre_hook)
        self.assertIn("professional_code_authoring_not_applicable_reason", stop_hook)

    def _write_files(self, root: Path, files: dict[str, str]) -> None:
        for relative, text in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
