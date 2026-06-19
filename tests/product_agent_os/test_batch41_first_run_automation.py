from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


class Batch41FirstRunAutomationTests(unittest.TestCase):
    def test_b41_m01_contract_names_modes_boundaries_and_unsupported_claims(self) -> None:
        from product_agent_os.first_run_analysis import (  # noqa: PLC0415
            build_first_run_automation_contract,
            validate_first_run_automation_contract,
        )

        contract = build_first_run_automation_contract()
        modes = {mode["id"]: mode for mode in contract["modes"]}

        self.assertEqual(contract["schema_version"], "first_run_orchestrator_contract_v1")
        for mode in ["read_only", "stage", "write_analysis", "render_html", "ask", "compare"]:
            self.assertIn(mode, modes)
        self.assertFalse(modes["read_only"]["target_mutation_allowed"])
        self.assertFalse(modes["stage"]["target_mutation_allowed"])
        self.assertTrue(modes["write_analysis"]["target_mutation_allowed"])
        self.assertIn(".codex/product-agent-os/analysis", modes["write_analysis"]["allowed_write_roots"])
        self.assertIn("release readiness", contract["unsupported_claims"])
        self.assertIn("runtime/browser proof", contract["unsupported_claims"])
        self.assertEqual(validate_first_run_automation_contract(contract), [])

    def test_b41_m02_no_args_prints_first_launch_help_without_parser_error(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_first_project_analysis.py")],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "help")
        self.assertEqual(payload["schema_version"], "first_run_orchestrator_help_v1")
        self.assertIn("--full-dry-run", payload["next_safe_command"])
        self.assertIn("write_analysis", {mode["id"] for mode in payload["contract"]["modes"]})
        self.assertFalse(payload["actions_performed"]["target_workspace_mutation"])
        self.assertFalse(payload["actions_performed"]["live_server"])
        self.assertFalse(payload["actions_performed"]["browser_automation"])

    def test_b41_m03_full_dry_run_returns_packet_without_writing_target(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--full-dry-run",
                    "--generated-at",
                    "2026-06-18T23:00:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "full_dry_run")
            self.assertEqual(payload["packet"]["schema_version"], "first_run_analysis_packet_v1")
            self.assertEqual(payload["orchestration_contract"]["schema_version"], "first_run_orchestrator_contract_v1")
            self.assertFalse((workspace / ".codex" / "product-agent-os" / "analysis").exists())
            self.assertEqual(payload["written_files"], [])
            self.assertNotIn(str(workspace), result.stdout)

    def test_b41_m04_stage_mode_writes_packet_and_html_only_under_stage_root(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")

            before_target_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-18T23:05:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            after_target_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "stage")
            self.assertEqual(before_target_files, after_target_files)
            self.assertTrue(stage.joinpath("first-run-analysis-packet.json").exists())
            self.assertTrue(stage.joinpath("index.html").exists())
            self.assertTrue(stage.joinpath("analysis-manifest.json").exists())
            self.assertEqual(payload["actions_performed"]["target_workspace_mutation"], False)
            self.assertNotIn(str(workspace), result.stdout)

    def test_b41_m04_stage_inside_target_requires_write_analysis_mode(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            stage_inside_target = workspace / ".codex" / "product-agent-os" / "analysis"

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage_inside_target),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("stage path is inside target", payload["error"])
            self.assertFalse(stage_inside_target.exists())

    def test_b41_m05_write_analysis_writes_only_allowed_analysis_artifacts(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "sample-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            before_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--write-analysis",
                    "--generated-at",
                    "2026-06-18T23:10:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            after_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            added_files = sorted(set(after_files) - set(before_files))

            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "write_analysis")
            self.assertTrue(payload["actions_performed"]["target_workspace_mutation"])
            self.assertIn(".codex/product-agent-os/analysis/first-run-analysis-packet.json", added_files)
            self.assertIn(".codex/product-agent-os/analysis/index.html", added_files)
            self.assertIn(".codex/product-agent-os/analysis/analysis-manifest.json", added_files)
            self.assertTrue(all(path.startswith(".codex/product-agent-os/analysis/") for path in added_files))
            self.assertNotIn(str(workspace), result.stdout)

    def test_b41_m06_script_registry_covers_all_top_level_scripts_with_risk_classification(self) -> None:
        from product_agent_os.first_run_analysis import (  # noqa: PLC0415
            build_first_run_script_registry,
            validate_first_run_script_registry,
        )

        registry = build_first_run_script_registry(SCRIPTS)
        script_names = {row["script"] for row in registry["scripts"]}
        top_level_scripts = {path.name for path in SCRIPTS.glob("*.py")}

        self.assertEqual(registry["schema_version"], "first_run_script_registry_v1")
        self.assertEqual(script_names, top_level_scripts)
        self.assertEqual(validate_first_run_script_registry(registry), [])
        for row in registry["scripts"]:
            self.assertIn(row["risk_class"], {"safe_read_only", "approval_required", "blocked_live"})
            self.assertIn(row["help_contract"], {"present", "missing"})
            self.assertIn(row["execution_mode"], {"help_only", "skip"})
            self.assertNotIn(str(ROOT), json.dumps(row, sort_keys=True))
        by_script = {row["script"]: row for row in registry["scripts"]}
        self.assertEqual(by_script["run_first_project_analysis.py"]["risk_class"], "safe_read_only")
        self.assertEqual(by_script["merge_infrastructure.py"]["risk_class"], "approval_required")
        self.assertEqual(by_script["run_codex_runtime_runner.py"]["risk_class"], "blocked_live")

    def test_b41_m07_executes_only_safe_help_matrix_and_keeps_redacted_digests(self) -> None:
        from product_agent_os.first_run_analysis import execute_first_run_safe_script_matrix  # noqa: PLC0415

        registry = {
            "schema_version": "first_run_script_registry_v1",
            "scripts": [
                {
                    "script": "safe_tool.py",
                    "risk_class": "safe_read_only",
                    "execution_mode": "help_only",
                    "safe_to_execute": True,
                    "safe_command": ["python", "safe_tool.py", "--help"],
                    "timeout_seconds": 10,
                },
                {
                    "script": "merge_infrastructure.py",
                    "risk_class": "approval_required",
                    "execution_mode": "skip",
                    "safe_to_execute": False,
                    "safe_command": ["python", "merge_infrastructure.py", "--help"],
                    "timeout_seconds": 10,
                },
            ],
        }
        calls: list[str] = []

        def fake_executor(row: dict) -> dict:
            calls.append(row["script"])
            return {
                "exit_code": 0,
                "duration_ms": 12,
                "stdout": "usage: safe_tool.py C:/Users/user/Desktop/project/codex_docs\n",
                "stderr": "",
            }

        matrix = execute_first_run_safe_script_matrix(registry, executor=fake_executor)
        by_script = {row["script"]: row for row in matrix["commands"]}

        self.assertEqual(calls, ["safe_tool.py"])
        self.assertEqual(by_script["safe_tool.py"]["status"], "passed")
        self.assertEqual(by_script["merge_infrastructure.py"]["status"], "skipped_approval_required")
        self.assertIn("stdout_digest", by_script["safe_tool.py"])
        self.assertNotIn("stdout", by_script["safe_tool.py"])
        self.assertNotIn(str(ROOT), json.dumps(matrix, sort_keys=True))

    def test_b41_m08_normalizes_command_outputs_without_hiding_failures(self) -> None:
        from product_agent_os.first_run_analysis import normalize_first_run_command_outputs  # noqa: PLC0415

        matrix = {
            "schema_version": "first_run_command_matrix_v1",
            "commands": [
                {"script": "detect_project.py", "status": "passed", "exit_code": 0, "risk_class": "safe_read_only"},
                {"script": "scan_project_code_graph.py", "status": "failed", "exit_code": 1, "risk_class": "safe_read_only"},
                {"script": "merge_infrastructure.py", "status": "skipped_approval_required", "exit_code": None, "risk_class": "approval_required"},
            ],
        }

        summary = normalize_first_run_command_outputs(matrix)

        self.assertEqual(summary["schema_version"], "first_run_evidence_summary_v1")
        self.assertEqual(summary["counts"]["passed"], 1)
        self.assertEqual(summary["counts"]["failed"], 1)
        self.assertEqual(summary["counts"]["skipped_approval_required"], 1)
        self.assertEqual(summary["completion_claim"], "not_claimed")
        self.assertIn("scan_project_code_graph.py", summary["failed_commands"])
        self.assertEqual(summary["overall_status"], "partial_failure")

    def test_b41_m09_resume_ledger_records_partial_failure_and_safe_rerun_hints(self) -> None:
        from product_agent_os.first_run_analysis import build_first_run_resume_ledger  # noqa: PLC0415

        matrix = {
            "schema_version": "first_run_command_matrix_v1",
            "commands": [
                {
                    "script": "detect_project.py",
                    "status": "passed",
                    "exit_code": 0,
                    "risk_class": "safe_read_only",
                    "safe_command": ["python", "detect_project.py", "--help"],
                },
                {
                    "script": "scan_project_code_graph.py",
                    "status": "failed",
                    "exit_code": 1,
                    "risk_class": "safe_read_only",
                    "safe_command": ["python", "scan_project_code_graph.py", "--help"],
                },
                {
                    "script": "merge_infrastructure.py",
                    "status": "skipped_approval_required",
                    "exit_code": None,
                    "risk_class": "approval_required",
                    "safe_command": ["python", "merge_infrastructure.py", "--help"],
                },
            ],
        }

        ledger = build_first_run_resume_ledger(matrix)

        self.assertEqual(ledger["schema_version"], "first_run_resume_ledger_v1")
        self.assertEqual(ledger["status"], "partial_failure")
        self.assertEqual(ledger["completion_claim"], "not_claimed")
        self.assertIn("scan_project_code_graph.py", ledger["resume_required_for"])
        self.assertIn("merge_infrastructure.py", ledger["approval_required_for"])
        self.assertIn("--help", ledger["resume_commands"][0]["command"])

    def test_b41_s3_m10_m16_full_dry_run_projects_bounded_project_analysis_summaries(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s3-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            docs = workspace / "docs"
            docs.mkdir()
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior can change.\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {"dev": "vite --host 127.0.0.1", "test": "vitest"},
                        "dependencies": {"@vitejs/plugin-react": "latest"},
                    }
                ),
                encoding="utf-8",
            )
            (workspace / "package-lock.json").write_text("{}", encoding="utf-8")
            (workspace / "src").mkdir()
            (workspace / "src" / "main.ts").write_text("export const answer = 42;\n", encoding="utf-8")
            (workspace / "tests").mkdir()
            (workspace / "tests" / "app.test.ts").write_text("test('x', () => {});\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--full-dry-run",
                    "--generated-at",
                    "2026-06-18T23:50:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            packet = payload["packet"]

            self.assertEqual(packet["project_analysis_summary"]["schema_version"], "first_run_project_analysis_summary_v1")
            self.assertIn(packet["project_analysis_summary"]["usage_mode"]["primary"], {"standard_feature", "maintenance", "docs_only"})
            self.assertTrue(packet["project_analysis_summary"]["route_reasons"])
            self.assertFalse(packet["project_analysis_summary"]["generated_artifact_inputs"]["source_truth_allowed"])

            self.assertEqual(packet["methodology_audit_summary"]["schema_version"], "first_run_methodology_audit_summary_v1")
            self.assertLessEqual(len(packet["methodology_audit_summary"]["top_recommendations"]), 5)
            self.assertTrue(packet["methodology_audit_summary"]["first_safe_action"])

            self.assertEqual(packet["source_policy_summary"]["schema_version"], "first_run_source_policy_summary_v1")
            self.assertEqual(packet["source_policy_summary"]["status"], "blocked")
            self.assertTrue(packet["source_policy_summary"]["registry_update_required_count"] >= 1)

            self.assertEqual(packet["graph_dry_run_summary"]["schema_version"], "first_run_graph_dry_run_summary_v1")
            self.assertGreaterEqual(packet["graph_dry_run_summary"]["node_count"], 1)
            self.assertEqual(packet["graph_dry_run_summary"]["source_policy"], "generated graph is not source truth")
            self.assertEqual(packet["graph_dry_run_summary"]["completion_claim"], "not_claimed")

            self.assertEqual(packet["docs_logging_summary"]["schema_version"], "first_run_docs_logging_summary_v1")
            self.assertIn("markdown_docs", packet["docs_logging_summary"]["docs_systems"])
            self.assertIn("package_test_script", packet["docs_logging_summary"]["logging_or_test_signals"])

            self.assertEqual(packet["dependency_readiness_summary"]["schema_version"], "first_run_dependency_readiness_summary_v1")
            self.assertEqual(packet["dependency_readiness_summary"]["install_or_dependency_mutation_performed"], False)
            self.assertIn("package.json", packet["dependency_readiness_summary"]["product_manifests"])

            self.assertEqual(packet["runtime_browser_boundary"]["schema_version"], "first_run_runtime_browser_boundary_v1")
            self.assertEqual(packet["runtime_browser_boundary"]["status"], "approval_required")
            self.assertFalse(packet["runtime_browser_boundary"]["runtime_executed"])
            self.assertFalse(packet["runtime_browser_boundary"]["browser_automation_performed"])
            self.assertNotIn(str(workspace), json.dumps(packet, sort_keys=True))

    def test_b41_s3_m12_source_policy_block_updates_section_without_success_claim(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "source-policy-target"
            docs = workspace / "docs"
            docs.mkdir(parents=True)
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior can change.\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--full-dry-run",
                    "--generated-at",
                    "2026-06-18T23:55:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            packet = json.loads(result.stdout)["packet"]
            self.assertEqual(packet["section_summaries"]["source_policy"]["status"], "approval_required")
            self.assertIn("source policy blocked", " ".join(packet["section_summaries"]["source_policy"]["unsupported_claims"]))
            self.assertEqual(packet["evidence_status"]["completion_claim"], "not_claimed")

    def test_b41_s4_m17_m20_stage_renders_complete_html_baseline_and_cleanup_guidance(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s4-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"dev": "vite --host 127.0.0.1", "test": "vitest"}}),
                encoding="utf-8",
            )

            first = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T00:10:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)

            (workspace / "docs").mkdir()
            (workspace / "docs" / "guide.md").write_text("# Guide\n\nSource status: `synthetic_fixture`\n", encoding="utf-8")
            second = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T00:11:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            payload = json.loads(second.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")

            self.assertEqual(payload["mode"], "stage")
            self.assertEqual(payload["render_result"]["status"], "ready")
            self.assertEqual(payload["render_result"]["page_count"], 11)
            for page_name in [
                "index.html",
                "inventory.html",
                "architecture.html",
                "methodology.html",
                "runtime-route.html",
                "control-plane.html",
                "graph.html",
                "code-flow.html",
                "quality-evals.html",
                "risks.html",
                "recommendations.html",
                "analysis-manifest.json",
            ]:
                self.assertIn(page_name, payload["written_files"])
                self.assertTrue(stage.joinpath(page_name).exists(), page_name)

            self.assertEqual(payload["baseline_comparison"]["status"], "compared")
            self.assertEqual(manifest["previous_baseline"]["status"], "compared")
            self.assertIn("docs/guide.md", manifest["change_summary"]["added_sources"])
            self.assertIn("Baseline Comparison", index_html)
            self.assertIn("Artifact Cleanup And Rollback", index_html)
            self.assertEqual(manifest["cleanup_guidance"]["deletion_performed"], False)
            self.assertEqual(manifest["cleanup_guidance"]["approval_required"], True)
            self.assertTrue(all(path.startswith(".") is False for path in manifest["cleanup_guidance"]["generated_files"]))
            self.assertNotIn(str(workspace), second.stdout)

    def test_b41_s4_m18_html_pages_surface_project_analysis_without_source_truth_claim(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s4-html-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"dev": "vite --host 127.0.0.1", "test": "vitest"}}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T00:15:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            inventory_html = stage.joinpath("inventory.html").read_text(encoding="utf-8")
            methodology_html = stage.joinpath("methodology.html").read_text(encoding="utf-8")
            runtime_html = stage.joinpath("runtime-route.html").read_text(encoding="utf-8")
            graph_html = stage.joinpath("graph.html").read_text(encoding="utf-8")

            self.assertIn("Project Analysis", inventory_html)
            self.assertIn("Docs And Logging", inventory_html)
            self.assertIn("Dependency Readiness", inventory_html)
            self.assertIn("Methodology Audit", methodology_html)
            self.assertIn("Runtime Browser Boundary", runtime_html)
            self.assertIn("approval_required", runtime_html)
            self.assertIn("Graph Dry Run", graph_html)
            self.assertIn("generated graph is not source truth", graph_html)
            self.assertIn("generated-view-only", inventory_html)
            self.assertNotIn(str(workspace), inventory_html + methodology_html + runtime_html + graph_html)

    def test_b41_s7_m31_m33_stage_renders_primary_cockpit_contract_shell_and_view_model(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s7-cockpit-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "docs").mkdir()
            (workspace / "docs" / "guide.md").write_text("# Guide\n\nSource status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"dev": "vite --host 127.0.0.1", "test": "vitest"}}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T02:10:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            primary = manifest["primary_cockpit"]
            contract = manifest["cockpit_contract"]
            view_model = primary["view_model"]

            self.assertEqual(payload["render_result"]["primary_cockpit"]["schema_version"], "first_run_cockpit_artifact_v1")
            self.assertEqual(primary["schema_version"], "first_run_cockpit_artifact_v1")
            self.assertEqual(primary["path"], "index.html")
            self.assertEqual(contract["schema_version"], "first_run_cockpit_artifact_contract_v1")
            self.assertEqual(contract["primary_artifact"], "index.html")
            self.assertEqual(contract["artifact_mode"], "single_self_contained_index_html")
            self.assertEqual(contract["selected_graph_renderer"], "Cosmos.gl")
            self.assertEqual(contract["legacy_diagnostics_policy"], "separate first-run pages are diagnostic/raw evidence only")
            self.assertEqual(len(contract["primary_pages"]), 8)
            self.assertEqual(len(view_model["cockpit"]["pages"]), 8)
            self.assertEqual(view_model["source_file_graph"]["status"], "adapter_ready")
            self.assertEqual(view_model["source_file_graph"]["renderer"], "Cosmos.gl")
            self.assertTrue(view_model["source_file_graph"]["graphology_compatible_payload"])
            self.assertIn("cosmos_payload", view_model["source_file_graph"])
            self.assertIn("visual_projection", view_model["source_file_graph"])
            self.assertIn("legend", view_model["source_file_graph"])
            self.assertIn("selected_file_panel", view_model["source_file_graph"])
            self.assertEqual(view_model["source_file_graph"]["table_fallback"]["status"], "available")
            self.assertIn("omitted_edge_count", view_model["source_file_graph"])
            self.assertEqual(view_model["code_graph"]["status"], "not_available")
            self.assertEqual(view_model["code_graph"]["node_count"], 0)
            self.assertEqual(view_model["code_graph"]["hotspot_count"], 0)
            self.assertEqual(view_model["code_graph"]["table_fallback"]["status"], "empty")

            self.assertIn('class="first-run-cockpit cockpit-shell"', index_html)
            self.assertIn('id="page-overview"', index_html)
            self.assertIn('id="page-project-map"', index_html)
            self.assertIn('id="page-code-intelligence"', index_html)
            self.assertIn('id="source-file-graph-canvas"', index_html)
            self.assertIn('id="source-file-graph-selected-file-panel"', index_html)
            self.assertIn('class="graph-fallback-table"', index_html)
            self.assertIn('id="code-graph-canvas"', index_html)
            self.assertIn("not_available", index_html)
            self.assertIn("Cosmos.gl", index_html)
            self.assertIn("generated-view-only", index_html)
            self.assertIn("Baseline Comparison", index_html)
            self.assertIn("Artifact Cleanup And Rollback", index_html)
            self.assertNotIn("<pre", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s7_m34_m35_cockpit_renders_source_graph_and_code_graph_summary_payloads(self) -> None:
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415
        from product_agent_os.first_run_analysis import build_first_run_analysis_packet, validate_first_run_analysis_packet  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s7-graph-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")

            packet = build_first_run_analysis_packet(
                target_label="synthetic-graph-target",
                generated_at="2026-06-19T02:30:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "project_graph",
                        "path": ".codex/product-agent-os/project-code-graph.json",
                        "digest": "sha256:" + "1" * 64,
                        "provenance": "scan_project_code_graph",
                    },
                    {
                        "artifact_id": "analysis_manifest",
                        "path": ".codex/product-agent-os/analysis/analysis-manifest.json",
                        "digest": "sha256:" + "2" * 64,
                        "provenance": "render_first_run_analysis_artifact",
                    },
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "source_artifact": "analysis_manifest"},
                    "runtime_route": {"status": "approval_required", "source_artifact": "analysis_manifest"},
                    "methodology_audit": {"status": "present_unverified", "source_artifact": "analysis_manifest"},
                    "control_plane": {"status": "present_unverified", "source_artifact": "analysis_manifest"},
                    "source_policy": {"status": "approval_required", "source_artifact": "analysis_manifest"},
                    "graph": {"status": "inspection_only", "source_artifact": "project_graph"},
                    "status_snapshot": {"status": "inspection_only", "source_artifact": "analysis_manifest"},
                },
                safe_next_action="Use graph packet as orientation only; read source files before edits.",
                graph_artifact_summary={
                    "status": "inspection_only",
                    "graph_packet_digest": "sha256:" + "3" * 64,
                    "agent_packet_refs": [
                        {
                            "kind": "agent_reading_packet",
                            "path": ".codex/product-agent-os/agent-reading-packet.json",
                            "digest": "sha256:" + "4" * 64,
                        }
                    ],
                    "coverage": {
                        "status": "partial_static",
                        "covered_files": 6,
                        "partial_files": 2,
                        "unsupported_languages": {"ruby": "unsupported"},
                    },
                    "freshness": {
                        "status": "stale",
                        "blocks_action_claims": True,
                        "safe_next_action": "Refresh graph or read source first.",
                    },
                    "rejected_link_summary": {"total": 3, "by_reason": {"weak_name_similarity": 3}},
                    "framework_semantic_summary": {"total": 2, "frameworks": {"react": 2}},
                    "guided_tour": [{"page": "code-intelligence", "safe_next_action": "Read listed spans before editing."}],
                    "unsupported_claims": ["runtime_routing", "source_read_completion"],
                },
            )

            self.assertEqual(validate_first_run_analysis_packet(packet), [])
            render_first_run_analysis_artifact(packet, workspace, output_dir=stage)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            view_model = manifest["primary_cockpit"]["view_model"]
            source_graph = view_model["source_file_graph"]
            code_graph = view_model["code_graph"]

            self.assertEqual(source_graph["status"], "adapter_ready")
            self.assertEqual(source_graph["renderer"], "Cosmos.gl")
            self.assertEqual(source_graph["cosmos_payload"]["schema_version"], "cosmos_gl_static_adapter_v1")
            self.assertTrue(source_graph["visual_projection"]["graphology_compatible"])
            self.assertGreaterEqual(source_graph["node_count"], 2)
            self.assertGreaterEqual(source_graph["edge_count"], 1)
            self.assertIn("omitted_node_count", source_graph)
            self.assertIn("omitted_edge_count", source_graph)
            self.assertEqual(source_graph["table_fallback"]["status"], "available")

            self.assertEqual(code_graph["status"], "available")
            self.assertEqual(code_graph["availability_detail"], "summary_available")
            self.assertEqual(code_graph["renderer"], "Cosmos.gl")
            self.assertEqual(code_graph["cosmos_payload"]["schema_version"], "cosmos_gl_static_adapter_v1")
            self.assertTrue(code_graph["source_read_required"])
            self.assertGreaterEqual(code_graph["node_count"], 4)
            self.assertGreaterEqual(code_graph["hotspot_count"], 3)
            self.assertEqual(code_graph["relationships"]["read_order"]["status"], "summary_available")
            self.assertIn("omitted_edge_count", code_graph)

            self.assertIn('data-graph-kind="source-file-graph"', index_html)
            self.assertIn('data-graph-kind="code-graph"', index_html)
            self.assertIn("Selected File Panel", index_html)
            self.assertIn("Code Graph And Hotspots", index_html)
            self.assertIn("Refresh graph or read source first.", index_html)
            self.assertNotIn("<script", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s7_m36_m39_cockpit_has_static_navigation_diagnostics_visual_qa_and_safety_contracts(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s7-ux-safety-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "docs").mkdir()
            (workspace / "docs" / "guide.md").write_text("# Guide\n\nSource status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"dev": "vite --host 127.0.0.1", "test": "vitest"}}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T02:45:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            view_model = manifest["primary_cockpit"]["view_model"]

            navigation = view_model["navigation_search"]
            self.assertEqual(navigation["schema_version"], "first_run_cockpit_navigation_search_v1")
            self.assertEqual(navigation["status"], "static_controls_ready")
            self.assertTrue(navigation["persistent_navigation"])
            self.assertEqual(navigation["filter_state"]["script_required"], False)
            self.assertGreaterEqual(navigation["search_index_count"], 8)
            self.assertEqual(len(navigation["filters"]), 4)
            self.assertTrue(any(item["id"] == "cockpit-diagnostics" for item in navigation["detail_panels"]))

            diagnostics = view_model["progressive_diagnostics"]
            self.assertEqual(diagnostics["schema_version"], "first_run_progressive_diagnostics_v1")
            self.assertEqual(diagnostics["raw_json_policy"], "collapsed_only_or_packet_ref")
            self.assertIn("details", diagnostics["html_elements"])

            visual_qa = view_model["visual_qa"]
            self.assertEqual(visual_qa["schema_version"], "first_run_cockpit_static_visual_qa_v1")
            self.assertEqual(visual_qa["browser_screenshot_status"], "not_run_approval_required")
            self.assertIn("cockpit-shell-not-default-browser", {item["id"] for item in visual_qa["checks"]})

            safety = view_model["safety_accessibility"]
            self.assertEqual(safety["schema_version"], "first_run_cockpit_safety_accessibility_v1")
            self.assertFalse(safety["offline_policy"]["external_urls_allowed"])
            self.assertFalse(safety["offline_policy"]["script_tags_allowed"])
            self.assertFalse(safety["privacy_policy"]["absolute_local_paths_allowed"])
            self.assertTrue(safety["accessibility_contract"]["labels_required"])

            self.assertIn('class="skip-link"', index_html)
            self.assertIn("generated-view-only", index_html)
            self.assertIn('id="main-content"', index_html)
            self.assertIn('role="search"', index_html)
            self.assertIn('for="cockpit-search"', index_html)
            self.assertIn('id="section-visual-projection"', index_html)
            self.assertIn('data-filter-state="static-default-all-visible"', index_html)
            self.assertIn('id="cockpit-diagnostics"', index_html)
            self.assertIn("<details>", index_html)
            self.assertIn("<summary>Raw Diagnostics Boundary</summary>", index_html)
            self.assertIn('id="static-visual-qa"', index_html)
            self.assertIn('id="offline-privacy-accessibility"', index_html)
            self.assertIn("Arial,Helvetica,sans-serif", index_html)
            self.assertIn("overflow-wrap:anywhere", index_html)
            self.assertIn("@media(max-width:760px)", index_html)
            self.assertNotIn("font-family:serif", index_html.replace(" ", "").lower())
            self.assertNotIn("<pre", index_html.lower())
            self.assertNotIn("<script", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn("raw_source", index_html.lower())

            ids = re.findall(r'id="([^"]+)"', index_html)
            self.assertEqual(len(ids), len(set(ids)))
            nav_targets = re.findall(r'<a href="#([^"]+)">', index_html)
            page_targets = [target for target in nav_targets if target.startswith("page-")]
            self.assertEqual(len(page_targets), 8)
            for target in page_targets:
                self.assertEqual(ids.count(target), 1, target)
            self.assertNotIn(str(workspace), index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s5_m21_first_response_exposes_one_blocking_question_and_keeps_queue_in_packet(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s5-question-target"
            docs = workspace / "docs"
            docs.mkdir(parents=True)
            (docs / "guide.md").write_text("# Guide\n\nOpenAI Codex behavior can change.\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--full-dry-run",
                    "--generated-at",
                    "2026-06-19T00:20:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            packet = payload["packet"]
            first_response = payload["first_response"]
            question_queue = packet["question_queue"]

            self.assertEqual(first_response["schema_version"], "first_run_guided_response_v1")
            self.assertEqual(first_response["mode"], "guided_first_response")
            self.assertEqual(first_response["blocking_question_count"], 1)
            self.assertIsInstance(first_response["blocking_question"], dict)
            self.assertEqual(
                question_queue["policy"]["max_blocking_questions_in_first_response"],
                1,
            )
            self.assertEqual(question_queue["summary"]["blocking"], 1)
            self.assertGreaterEqual(question_queue["summary"]["remaining"], 1)
            self.assertIn("deferred_question_count", first_response)
            self.assertLessEqual(first_response["deferred_question_preview_count"], 2)
            self.assertNotIn("questions", first_response)
            self.assertEqual(first_response["completion_claim"], "not_claimed")
            self.assertNotIn(str(workspace), result.stdout)

    def test_b41_s5_m22_stage_writes_answer_ledger_template_without_target_mutation(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s5-ledger-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            before_target_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T00:25:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            packet = payload["packet"]
            routing = packet["answer_ledger_routing"]
            after_target_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            ledger_template = json.loads(stage.joinpath("answer-ledger-template.json").read_text(encoding="utf-8"))

            self.assertEqual(before_target_files, after_target_files)
            self.assertIn("answer-ledger-template.json", payload["written_files"])
            self.assertEqual(routing["schema_version"], "first_run_answer_ledger_routing_v1")
            self.assertEqual(routing["write_policy"], "staged_only")
            self.assertFalse(routing["target_workspace_mutation_performed"])
            self.assertFalse(routing["unreviewed_answers_mutate_source_docs"])
            self.assertEqual(routing["ledger_template"]["schema_version"], 1)
            self.assertEqual(ledger_template["write_policy"], "staged_only")
            self.assertIn("entries", ledger_template)
            self.assertEqual(payload["answer_ledger_routing"]["validation_errors"], [])
            self.assertNotIn("chat_memory", json.dumps(routing, sort_keys=True))
            self.assertNotIn(str(workspace), result.stdout)

    def test_b41_s5_m23_ambiguous_intake_returns_route_options_without_blocking_analysis(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s5-ambiguous-target"
            workspace.mkdir()
            (workspace / "README.md").write_text("# Idea\n\nSource status: `synthetic_fixture`\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--full-dry-run",
                    "--generated-at",
                    "2026-06-19T00:30:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            payload = json.loads(result.stdout)
            first_response = payload["first_response"]
            route_options = first_response["route_options"]

            self.assertEqual(payload["status"], "ok")
            self.assertEqual(payload["mode"], "full_dry_run")
            self.assertIn("command_matrix", payload)
            self.assertGreaterEqual(len(route_options), 2)
            self.assertLessEqual(len(route_options), 3)
            for option in route_options:
                self.assertIn("id", option)
                self.assertIn("label", option)
                self.assertIn("safe_next_action", option)
                self.assertIn("write_boundary", option)
            self.assertEqual(first_response["blocking_question_count"], 1)
            self.assertFalse(payload["actions_performed"]["target_workspace_mutation"])
            self.assertNotIn(str(workspace), result.stdout)


if __name__ == "__main__":
    unittest.main()
