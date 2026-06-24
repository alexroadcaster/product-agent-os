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

    def test_b44_s1_first_launch_help_discloses_self_learning_loop_cadence_and_manual_trigger(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "run_first_project_analysis.py")],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self_learning = payload["welcome_message"]["self_learning_loop"]

        self.assertEqual(self_learning["schema_version"], "self_learning_loop_disclosure_v1")
        self.assertEqual(self_learning["default_approval_state"], "manual_only")
        self.assertIn("manual_now", {trigger["id"] for trigger in self_learning["triggers"]})
        self.assertIn("weekly_due_check", {trigger["id"] for trigger in self_learning["triggers"]})
        self.assertIn("manual_only", {option["id"] for option in self_learning["cadence_options"]})
        self.assertIn("weekly", {option["id"] for option in self_learning["cadence_options"]})
        self.assertEqual(self_learning["schedule_status"], "not_created")
        self.assertEqual(self_learning["auto_apply_status"], "not_enabled")
        self.assertIn("check_self_learning_due.py", self_learning["manual_commands"]["check_due"])
        self.assertIn("run_self_learning_loop.py", self_learning["manual_commands"]["run_now"])
        self.assertEqual(self_learning["manual_runner"]["status"], "available_manual_only")
        self.assertIn("run_self_learning_loop.py", self_learning["manual_runner"]["dry_run_command"])
        self.assertFalse(self_learning["actions_performed"]["active_automation"])
        self.assertFalse(self_learning["actions_performed"]["provider_api_call"])

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

    def test_b41_s8_m42_cockpit_renders_static_architecture_diagram_layer(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s8-diagram-target"
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
                    "2026-06-19T03:10:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            view_model = manifest["primary_cockpit"]["view_model"]
            diagram_layer = view_model["architecture_diagrams"]
            diagram_ids = {diagram["id"] for diagram in diagram_layer["diagrams"]}

            self.assertEqual(manifest["cockpit_contract"]["architecture_diagram_layer"]["status"], "static_fallback_ready")
            self.assertEqual(
                manifest["cockpit_contract"]["architecture_diagram_layer"]["diagram_ids"],
                [
                    "system-context",
                    "first-run-pipeline",
                    "trust-boundary",
                    "artifact-data-model",
                    "graph-rendering",
                    "runtime-approval-path",
                    "evidence-lifecycle",
                ],
            )
            self.assertEqual(diagram_layer["schema_version"], "first_run_architecture_diagram_layer_v1")
            self.assertEqual(diagram_layer["status"], "static_fallback_ready")
            self.assertEqual(diagram_layer["diagram_count"], 7)
            self.assertEqual(diagram_layer["diagram_ids"], manifest["cockpit_contract"]["architecture_diagram_layer"]["diagram_ids"])
            self.assertEqual(diagram_layer["external_assets"], "forbidden")
            self.assertEqual(
                diagram_ids,
                {
                    "system-context",
                    "first-run-pipeline",
                    "trust-boundary",
                    "artifact-data-model",
                    "graph-rendering",
                    "runtime-approval-path",
                    "evidence-lifecycle",
                },
            )
            for diagram in diagram_layer["diagrams"]:
                self.assertTrue(diagram["question_answered"])
                self.assertEqual(diagram["generated_view_boundary"], "generated-view-only")
                self.assertEqual(diagram["required_boundary"], "source files and current command evidence remain source truth")
                self.assertEqual(diagram["source_boundary"].split(";")[0], "generated-view-only")
                self.assertEqual(diagram["static_fallback"]["status"], "rendered_static_fallback")
                self.assertEqual(diagram["raw_mermaid_fallback"]["status"], "available_collapsed")
                self.assertEqual(diagram["raw_mermaid_fallback"]["runtime_status"], "not_executed_no_mermaid_runtime")
                self.assertIn("flowchart", diagram["raw_mermaid_fallback"]["source"])
                self.assertEqual(
                    diagram["rendering_acceptance"],
                    {
                        "static_fallback_present": True,
                        "raw_mermaid_present": True,
                        "external_assets_forbidden": True,
                        "runtime_not_executed": True,
                    },
                )

            self.assertIn('class="cockpit-band architecture-diagram-layer diagram-workbench"', index_html)
            self.assertEqual(index_html.count('id="architecture-diagram-layer"'), 1)
            self.assertIn('id="architecture-diagram-summary"', index_html)
            self.assertEqual(index_html.count('class="diagram-panel"'), 10)
            self.assertEqual(index_html.count('class="architecture-diagram-svg"'), 10)
            self.assertIn('id="diagram-system-context"', index_html)
            self.assertEqual(index_html.count('id="diagram-system-context"'), 1)
            self.assertIn('id="diagram-summary-system-context"', index_html)
            self.assertIn('id="diagram-first-run-pipeline"', index_html)
            self.assertIn('id="diagram-trust-boundary"', index_html)
            self.assertIn('id="diagram-artifact-data-model"', index_html)
            self.assertIn('id="diagram-graph-rendering"', index_html)
            self.assertIn('id="diagram-runtime-approval-path"', index_html)
            self.assertIn('id="diagram-evidence-lifecycle"', index_html)
            self.assertIn('class="architecture-diagram-svg"', index_html)
            self.assertIn("Raw Mermaid fallback", index_html)
            self.assertIn("Source/Trust Boundary", index_html)
            self.assertIn("generated-view-only", index_html)
            self.assertIn("not_executed_no_mermaid_runtime", index_html)
            self.assertNotIn("mermaid.min", index_html.lower())
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn("<pre", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s8_m43_cockpit_shell_uses_architecture_dossier_layout(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s8-shell-target"
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
                    "2026-06-19T04:00:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")

            self.assertIn('class="cockpit-hero dossier-hero"', index_html)
            self.assertIn('data-shell="architecture-dossier"', index_html)
            self.assertIn("Product-Agent OS First-Run Architecture Cockpit", index_html)
            self.assertIn("Architecture dossier / operational cockpit", index_html)
            self.assertIn("Welcome to Product-Agent OS", index_html)
            self.assertIn("What Product-Agent OS does", index_html)
            self.assertIn("Self-Learning Loop", index_html)
            self.assertIn("manual_only", index_html)
            self.assertIn("draft_only", index_html)
            self.assertIn("eligible Product-Agent OS projects only", index_html)
            self.assertIn('class="next-route-panel"', index_html)
            self.assertIn("Next Safe Route", index_html)
            self.assertIn('class="hero-grid dossier-grid"', index_html)
            self.assertIn("Architecture diagrams", index_html)
            self.assertIn('class="architecture-signal"', index_html)
            self.assertIn("Architecture signal:", index_html)
            self.assertIn("Runtime boundary:", index_html)
            self.assertIn('class="proof-strip"', index_html)
            self.assertIn("source truth stays in files and current commands", index_html)
            self.assertIn("no external diagram assets", index_html)
            self.assertIn("no target mutation by default", index_html)
            self.assertIn("completion claim: not_claimed", index_html)
            self.assertIn("dossier-grid", index_html)
            self.assertIn("proof-strip", index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html)

    def test_b41_s8_m44_cockpit_renders_evidence_decision_risk_source_blueprint_sections(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s8-evidence-target"
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
                    "2026-06-19T04:30:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            layer = manifest["primary_cockpit"]["view_model"]["evidence_decision_layer"]

            self.assertEqual(layer["schema_version"], "first_run_evidence_decision_layer_v1")
            self.assertEqual(layer["status"], "visible_acceptance_surfaces_ready")
            self.assertEqual(layer["generated_view_policy"], "orientation_only_not_proof")
            self.assertGreaterEqual(len(layer["supported_claims"]), 4)
            self.assertGreaterEqual(len(layer["unsupported_claims"]), 1)
            self.assertGreaterEqual(len(layer["blockers"]), 1)
            self.assertGreaterEqual(len(layer["decision_grid"]), 3)
            self.assertGreaterEqual(len(layer["owner_actions"]), 3)
            self.assertGreaterEqual(len(layer["codex_actions"]), 3)
            self.assertGreaterEqual(len(layer["risk_ledger"]), 6)
            self.assertGreaterEqual(len(layer["source_blueprints"]), 1)
            self.assertGreaterEqual(len(layer["proof_refs"]), 2)
            for decision in layer["decision_grid"]:
                self.assertIn("owner_action", decision)
                self.assertIn("codex_action", decision)
                self.assertIn("approval_requirement", decision)
                self.assertIn("next_safe_step", decision)

            required_markers = [
                'id="evidence-decision-layer"',
                'data-acceptance-surface="m44"',
                'id="supported-claims"',
                'id="unsupported-claims"',
                'id="blocker-ledger"',
                'id="decision-grid"',
                'id="owner-codex-actions"',
                'id="risk-ledger"',
                'id="future-gates"',
                'id="proof-evidence-strip"',
                'id="source-blueprint"',
                "Supported Claims",
                "Unsupported Claims",
                "Blocker Ledger",
                "Decision Grid",
                "Owner Actions",
                "Codex Actions",
                "Risk Ledger",
                "Source Blueprint",
                "Approval requirement:",
                "Next safe step:",
                "output/playwright/b41-s8-m42/playwright-diagram-proof.json",
                "output/playwright/b41-s8-m43/playwright-shell-proof.json",
            ]
            for marker in required_markers:
                self.assertIn(marker, index_html)

            self.assertEqual(index_html.count('id="supported-claims"'), 1)
            self.assertEqual(index_html.count('id="unsupported-claims"'), 1)
            self.assertIn("release readiness", index_html)
            self.assertIn("target apply safety", index_html)
            self.assertIn("Cosmos.gl/WebGL runtime execution is not claimed", index_html)
            self.assertIn("Generated artifacts must not mutate target source", index_html)
            self.assertIn("generated-view-only", index_html)
            self.assertIn("orientation_only_not_proof", index_html)
            self.assertNotIn("release-ready", index_html.lower())
            self.assertNotIn("wcag certified", index_html.lower())
            self.assertNotIn("raw_source", index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s8_m45_cockpit_labels_graph_runtime_static_fallback_boundary(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s8-graph-runtime-target"
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
                    "2026-06-19T05:20:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            view_model = manifest["primary_cockpit"]["view_model"]
            layer = view_model["graph_runtime_layer"]

            self.assertEqual(layer["schema_version"], "first_run_graph_runtime_layer_v1")
            self.assertEqual(layer["status"], "runtime_webgl_blocked_static_fallback_ready")
            self.assertEqual(layer["runtime_execution_claim"], "not_claimed")
            self.assertEqual(
                layer["required_labels"],
                ["adapter_ready", "static_fallback", "not_available", "runtime_webgl_blocked"],
            )
            self.assertEqual(layer["graphology_payload"]["status"], "adapter_ready")
            self.assertTrue(layer["graphology_payload"]["compatible"])
            self.assertEqual(layer["cosmos_adapter"]["runtime_webgl_status"], "runtime_webgl_blocked")
            self.assertEqual(layer["cosmos_adapter"]["execution_evidence"], "not_available")
            self.assertEqual(layer["runtime_blocker_banner"]["status"], "runtime_webgl_blocked")
            self.assertEqual(layer["fallback_explanation"]["status"], "static_fallback")
            self.assertGreaterEqual(len(layer["rendered_states"]), 2)

            required_markers = [
                'id="graph-runtime-layer"',
                'data-runtime-status="runtime_webgl_blocked"',
                "Graphology / Cosmos.gl Runtime Boundary",
                "Graphology-compatible payload",
                "Cosmos.gl-ready adapter",
                "Cosmos.gl WebGL runtime execution is not claimed",
                "adapter_ready",
                "static_fallback",
                "not_available",
                "runtime_webgl_blocked",
                "Runtime Blocker",
                "Selected Node UX",
                "Static Fallback Explanation",
                'id="source-file-graph-canvas"',
                'id="source-file-graph-selected-file-panel"',
                'class="graph-fallback-table"',
                "Runtime WebGL",
            ]
            for marker in required_markers:
                self.assertIn(marker, index_html)

            self.assertIn("runtime_webgl_blocked is the current execution boundary", index_html)
            self.assertIn("Code graph data is not available for this packet.", index_html)
            self.assertNotIn("WebGL runtime passed", index_html)
            self.assertNotIn("Cosmos.gl runtime passed", index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m48_cockpit_declares_architecture_intelligence_design_contract(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-design-contract-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"test": "pytest", "lint": "ruff check ."}}),
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
                    "2026-06-19T13:40:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            view_model = manifest["primary_cockpit"]["view_model"]
            contract = manifest["cockpit_contract"]["architecture_intelligence_design_contract"]

            self.assertEqual(contract["schema_version"], "architecture_intelligence_design_contract_v1")
            self.assertEqual(contract["artifact_family"], "self_contained_architecture_intelligence_cockpit")
            self.assertEqual(contract["generated_view_boundary"], "generated-view-only")
            self.assertEqual(contract["first_viewport"]["layout"], "identity_status_architecture_next_route")
            self.assertIn("overview", contract["navigation_modes"]["primary_tabs"])
            self.assertIn("local_search", contract["navigation_modes"]["approved_enhancements"])
            self.assertIn("diagram_zoom", contract["navigation_modes"]["approved_enhancements"])
            self.assertEqual(contract["local_js_boundary"]["status"], "approved_for_b41_s9_m50")
            self.assertFalse(contract["local_js_boundary"]["external_requests_allowed"])
            self.assertFalse(contract["local_js_boundary"]["live_runtime_allowed"])
            self.assertIn("shadcn_card", contract["component_grammar"]["mapped_components"])
            self.assertIn("shadcn_tabs", contract["component_grammar"]["mapped_components"])
            self.assertEqual(contract["typography"]["body_min_px"], 15)
            self.assertEqual(contract["typography"]["letter_spacing"], "0")
            self.assertIn("approval_required", contract["status_semantics"])
            self.assertEqual(contract["diagram_modes"]["mermaid_runtime"], "not_included")
            self.assertIn("release readiness", contract["non_goals"])
            self.assertIn("full WCAG certification", contract["non_goals"])
            self.assertEqual(view_model["design_contract"], contract)

    def test_b41_s9_m49_first_viewport_uses_operator_architecture_shell(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-operator-shell-target"
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
                    "2026-06-19T14:05:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            shell = manifest["primary_cockpit"]["view_model"]["first_viewport_shell"]

            self.assertEqual(shell["schema_version"], "first_run_first_viewport_shell_v1")
            self.assertEqual(shell["status"], "architecture_intelligence_operator_shell_ready")
            self.assertEqual(shell["layout"], "identity_status_architecture_next_route")
            self.assertEqual(shell["generated_view_label"], "generated-view-only")
            self.assertEqual(shell["source_boundary"]["status"], "source_truth_required")
            self.assertEqual(shell["next_route"]["status"], "owner_review_required")
            self.assertGreaterEqual(len(shell["status_strip"]), 4)
            self.assertIn("overview", shell["mode_navigation"])
            self.assertIn("operations-risk", shell["mode_navigation"])
            self.assertEqual(shell["responsive_contract"]["mobile_order"][0], "identity")
            self.assertIn("minmax(0,1fr)", shell["responsive_contract"]["css_guards"])

            required_markers = [
                'data-shell-version="architecture-intelligence-v2"',
                'data-shell-role="architecture-intelligence-hero"',
                'class="cockpit-hero dossier-hero"',
                'id="first-viewport-status-strip"',
                'class="status-strip-item"',
                'class="operator-rail source-boundary-rail"',
                'data-route-role="review-route-card"',
                'class="mode-navigation"',
                "Architecture Intelligence Cockpit",
                "Source Boundary",
                "Evidence State",
                "No target mutation",
                "Review route",
                "generated-view-only",
            ]
            for marker in required_markers:
                self.assertIn(marker, index_html)
            self.assertIn("grid-template-columns:minmax(0,1.5fr) minmax(280px,.65fr)", index_html)
            self.assertIn(".status-strip", index_html)
            self.assertIn(".mode-navigation", index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m50_cockpit_embeds_approved_local_interaction_layer_only(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-local-js-target"
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
                    "2026-06-19T14:40:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            layer = manifest["primary_cockpit"]["view_model"]["local_interaction_layer"]

            self.assertEqual(layer["schema_version"], "first_run_local_interaction_layer_v1")
            self.assertEqual(layer["status"], "approved_inline_js_ready")
            self.assertEqual(layer["script_id"], "cockpit-local-interactions")
            self.assertEqual(layer["fallback"], "readable_anchor_navigation_without_javascript")
            self.assertEqual(
                layer["approved_features"],
                ["tabs", "local_search_filter", "collapsible_panels", "diagram_zoom_fullscreen", "selected_node_focus"],
            )
            self.assertFalse(layer["external_script_src_allowed"])
            self.assertFalse(layer["external_requests_allowed"])
            self.assertFalse(layer["fetch_allowed"])
            self.assertFalse(layer["target_mutation_allowed"])
            self.assertFalse(layer["webgl_execution_allowed"])

            self.assertIn('<script id="cockpit-local-interactions">', index_html)
            self.assertIn('data-interaction-layer="approved-local-js"', index_html)
            self.assertIn('data-diagram-action="zoom-in"', index_html)
            self.assertIn('data-diagram-action="zoom-out"', index_html)
            self.assertIn('data-diagram-action="reset"', index_html)
            self.assertIn('data-diagram-action="fullscreen"', index_html)
            for marker in [
                "applyCockpitSearch",
                "activateCockpitMode",
                "setDiagramScale",
                "requestFullscreen",
                "focusSelectedNode",
            ]:
                self.assertIn(marker, index_html)
            unsafe_markers = [
                "<script src",
                "fetch(",
                "xmlhttprequest",
                "websocket",
                "eval(",
                "localstorage",
                "http://",
                "https://",
            ]
            for marker in unsafe_markers:
                self.assertNotIn(marker, index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m51_cockpit_exposes_static_diagram_workbench_contract(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-diagram-workbench-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"test": "vitest", "build": "vite build"}}),
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
                    "2026-06-19T15:10:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            diagram_layer = manifest["primary_cockpit"]["view_model"]["architecture_diagrams"]
            workbench = diagram_layer["diagram_workbench"]

            self.assertEqual(workbench["schema_version"], "first_run_static_diagram_workbench_v1")
            self.assertEqual(workbench["status"], "zoom_ready_static_svg_workbench")
            self.assertEqual(workbench["rendering_mode"], "inline_static_svg_plus_collapsed_mermaid_source")
            self.assertEqual(workbench["runtime_boundary"], "no_mermaid_runtime_no_external_assets")
            self.assertTrue(workbench["local_zoom_controls"])
            self.assertFalse(workbench["external_assets_allowed"])
            self.assertFalse(workbench["runtime_execution_claimed"])
            self.assertEqual(len(workbench["diagram_cards"]), diagram_layer["diagram_count"])
            self.assertIn("system-context", {card["diagram_id"] for card in workbench["diagram_cards"]})
            for card in workbench["diagram_cards"]:
                self.assertEqual(card["zoom_state"], "local_js_optional")
                self.assertEqual(card["source_truth_boundary"], "source_files_and_current_commands")

            for marker in [
                'class="cockpit-band architecture-diagram-layer diagram-workbench"',
                'data-diagram-workbench="static-svg-local-zoom"',
                'class="diagram-workbench-summary"',
                'class="diagram-boundary-badges"',
                'data-diagram-source-boundary="source_files_and_current_commands"',
                "Static SVG Workbench",
                "No Mermaid runtime",
                "Zoom-ready",
            ]:
                self.assertIn(marker, index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m52_cockpit_exposes_db_schema_and_contract_surface(self) -> None:
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415
        from product_agent_os.first_run_analysis import build_first_run_analysis_packet, validate_first_run_analysis_packet  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-schema-contract-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            packet = build_first_run_analysis_packet(
                target_label="schema-contract-target",
                generated_at="2026-06-19T15:35:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "db_schema",
                        "path": "prisma/schema.prisma",
                        "digest": "sha256:" + "1" * 64,
                        "provenance": "synthetic_fixture",
                    },
                    {
                        "artifact_id": "db_migration",
                        "path": "migrations/001_init.sql",
                        "digest": "sha256:" + "2" * 64,
                        "provenance": "synthetic_fixture",
                    },
                    {
                        "artifact_id": "api_contract",
                        "path": "openapi.yaml",
                        "digest": "sha256:" + "3" * 64,
                        "provenance": "synthetic_fixture",
                    },
                    {
                        "artifact_id": "config_contract",
                        "path": ".env.example",
                        "digest": "sha256:" + "4" * 64,
                        "provenance": "synthetic_fixture",
                    },
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "source_artifact": "db_schema"},
                    "runtime_route": {"status": "approval_required", "source_artifact": "api_contract"},
                    "methodology_audit": {"status": "present_unverified", "source_artifact": "api_contract"},
                    "control_plane": {"status": "present_unverified", "source_artifact": "config_contract"},
                    "source_policy": {"status": "current", "source_artifact": "db_schema"},
                    "graph": {"status": "inspection_only", "source_artifact": "db_schema"},
                    "status_snapshot": {"status": "inspection_only", "source_artifact": "config_contract"},
                },
                safe_next_action="Read schema and API contract source files before DB or API changes.",
            )

            self.assertEqual(validate_first_run_analysis_packet(packet), [])
            render_first_run_analysis_artifact(packet, workspace, output_dir=stage)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            surface = manifest["primary_cockpit"]["view_model"]["schema_contract_surface"]

            self.assertEqual(surface["schema_version"], "first_run_schema_contract_surface_v1")
            self.assertEqual(surface["status"], "contract_inventory_ready")
            self.assertEqual(surface["source_boundary"], "path_and_digest_inventory_only")
            self.assertFalse(surface["runtime_introspection_performed"])
            self.assertFalse(surface["migration_execution_performed"])
            self.assertIn("prisma/schema.prisma", [item["path"] for item in surface["db_schema_candidates"]])
            self.assertIn("migrations/001_init.sql", [item["path"] for item in surface["migration_candidates"]])
            self.assertIn("openapi.yaml", [item["path"] for item in surface["api_contract_candidates"]])
            self.assertIn(".env.example", [item["path"] for item in surface["config_contract_candidates"]])
            self.assertEqual(surface["empty_state_policy"], "show explicit not_available state, do not hide missing schemas")

            for marker in [
                'id="schema-contract-surface"',
                'class="schema-contract-surface"',
                'data-contract-surface="db-schema-api-config"',
                "DB / Schema / Contract Surface",
                "path_and_digest_inventory_only",
                "prisma/schema.prisma",
                "migrations/001_init.sql",
                "openapi.yaml",
                ".env.example",
            ]:
                self.assertIn(marker, index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m53_cockpit_exposes_graph_file_code_surface(self) -> None:
        from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: PLC0415
        from product_agent_os.first_run_analysis import build_first_run_analysis_packet, validate_first_run_analysis_packet  # noqa: PLC0415

        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-graph-code-surface-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            packet = build_first_run_analysis_packet(
                target_label="graph-code-surface-target",
                generated_at="2026-06-19T16:05:00+03:00",
                source_artifacts=[
                    {
                        "artifact_id": "project_graph",
                        "path": ".codex/product-agent-os/project-code-graph.json",
                        "digest": "sha256:" + "5" * 64,
                        "provenance": "scan_project_code_graph",
                    },
                    {
                        "artifact_id": "agent_packet",
                        "path": ".codex/product-agent-os/agent-reading-packet.json",
                        "digest": "sha256:" + "6" * 64,
                        "provenance": "scan_project_code_graph",
                    },
                ],
                generated_pages=[],
                section_summaries={
                    "discovery": {"status": "current", "source_artifact": "project_graph"},
                    "runtime_route": {"status": "approval_required", "source_artifact": "project_graph"},
                    "methodology_audit": {"status": "present_unverified", "source_artifact": "agent_packet"},
                    "control_plane": {"status": "present_unverified", "source_artifact": "agent_packet"},
                    "source_policy": {"status": "current", "source_artifact": "project_graph"},
                    "graph": {"status": "inspection_only", "source_artifact": "project_graph"},
                    "status_snapshot": {"status": "inspection_only", "source_artifact": "agent_packet"},
                },
                safe_next_action="Use graph surfaces for navigation; read source files before edits.",
                graph_artifact_summary={
                    "status": "inspection_only",
                    "graph_packet_digest": "sha256:" + "7" * 64,
                    "agent_packet_refs": [
                        {
                            "kind": "agent_reading_packet",
                            "path": ".codex/product-agent-os/agent-reading-packet.json",
                            "digest": "sha256:" + "8" * 64,
                        }
                    ],
                    "coverage": {"status": "partial_static", "covered_files": 4, "partial_files": 1},
                    "freshness": {
                        "status": "current",
                        "blocks_action_claims": False,
                        "safe_next_action": "Read listed spans before editing.",
                    },
                    "rejected_link_summary": {"total": 1, "by_reason": {"weak_name_similarity": 1}},
                    "framework_semantic_summary": {"total": 1, "frameworks": {"react": 1}},
                    "guided_tour": [{"page": "code-intelligence", "safe_next_action": "Start with graph hotspots."}],
                },
            )

            self.assertEqual(validate_first_run_analysis_packet(packet), [])
            render_first_run_analysis_artifact(packet, workspace, output_dir=stage)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            surface = manifest["primary_cockpit"]["view_model"]["graph_code_surface"]

            self.assertEqual(surface["schema_version"], "first_run_graph_file_code_surface_v1")
            self.assertEqual(surface["status"], "graph_code_surface_ready")
            self.assertEqual(surface["renderer"], "Cosmos.gl")
            self.assertEqual(surface["runtime_boundary"], "static_svg_table_fallback_no_webgl_execution")
            self.assertTrue(surface["selected_node_panel"])
            self.assertTrue(surface["table_fallback"])
            self.assertTrue(surface["source_read_required"])
            self.assertFalse(surface["webgl_execution_claimed"])
            self.assertEqual(surface["safe_interactions"], ["local_search_filter", "selected_node_focus", "table_fallback_scan"])
            self.assertGreaterEqual(surface["surface_cards"][0]["node_count"], 1)
            self.assertGreaterEqual(surface["surface_cards"][1]["node_count"], 1)

            for marker in [
                'id="graph-file-code-surface"',
                'class="graph-code-surface"',
                'data-graph-code-surface="static-navigation"',
                "Graph / File / Code Surface",
                "static_svg_table_fallback_no_webgl_execution",
                "selected_node_focus",
                "table_fallback_scan",
                "Read source files before graph-backed edits",
            ]:
                self.assertIn(marker, index_html)
            self.assertNotIn("WebGL runtime passed", index_html)
            self.assertNotIn("Cosmos.gl runtime passed", index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m54_cockpit_exposes_guided_review_route_and_read_order(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-guided-route-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(
                json.dumps({"scripts": {"test": "pytest", "build": "mkdocs build --strict"}}),
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
                    "2026-06-19T16:30:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            route = manifest["primary_cockpit"]["view_model"]["guided_tour_surface"]

            self.assertEqual(route["schema_version"], "first_run_guided_tour_surface_v1")
            self.assertEqual(route["status"], "guided_read_order_ready")
            self.assertEqual(route["interaction_mode"], "anchor_links_with_optional_local_tab_activation")
            self.assertFalse(route["completion_tracking_enabled"])
            self.assertGreaterEqual(len(route["steps"]), 7)
            self.assertEqual(route["steps"][0]["target"], "#main-content")
            self.assertIn("#architecture-diagram-layer", {step["target"] for step in route["steps"]})
            self.assertIn("#schema-contract-surface", {step["target"] for step in route["steps"]})
            self.assertIn("#graph-file-code-surface", {step["target"] for step in route["steps"]})
            for step in route["steps"]:
                self.assertEqual(step["source_boundary"], "generated_orientation_requires_source_check")

            for marker in [
                'id="guided-review-route"',
                'class="cockpit-band guided-tour-surface"',
                'data-guided-tour="read-order"',
                "Guided Review Route",
                "Start With Boundary",
                "Read Architecture Diagrams",
                "Inspect DB / Schema / Contract Surface",
                "Use Graph / File / Code Surface",
                "Check Evidence And Risk",
            ]:
                self.assertIn(marker, index_html)
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m55_cockpit_exposes_evidence_risk_hierarchy(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-evidence-risk-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(json.dumps({"scripts": {"test": "pytest"}}), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T17:00:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            hierarchy = manifest["primary_cockpit"]["view_model"]["evidence_risk_hierarchy"]

            self.assertEqual(hierarchy["schema_version"], "first_run_evidence_risk_hierarchy_v1")
            self.assertEqual(hierarchy["status"], "risk_hierarchy_ready")
            self.assertEqual(hierarchy["claim_ceiling"], "orientation_only_not_proof")
            self.assertFalse(hierarchy["release_ready_claim_allowed"])
            self.assertFalse(hierarchy["runtime_proof_claim_allowed"])
            self.assertFalse(hierarchy["target_apply_allowed"])
            self.assertEqual([lane["id"] for lane in hierarchy["priority_lanes"]], ["supported", "blocked", "approval", "future"])
            self.assertTrue(any(item["id"] == "runtime_browser_proof" for item in hierarchy["blocked_claims"]))
            self.assertTrue(any(item["id"] == "release_readiness" for item in hierarchy["blocked_claims"]))

            for marker in [
                'id="evidence-risk-hierarchy"',
                'class="evidence-risk-hierarchy"',
                'data-risk-hierarchy="claim-ceiling"',
                "Evidence / Risk Hierarchy",
                "orientation_only_not_proof",
                "runtime_browser_proof",
                "release_readiness",
                "target_apply",
            ]:
                self.assertIn(marker, index_html)
            self.assertNotIn("release-ready", index_html.lower())
            self.assertNotIn("runtime proof passed", index_html.lower())
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn(str(workspace), result.stdout + index_html + json.dumps(manifest, sort_keys=True))

    def test_b41_s9_m56_cockpit_exposes_static_visual_accessibility_acceptance_gate(self) -> None:
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "s9-visual-a11y-target"
            stage = Path(tmp) / "stage-output"
            workspace.mkdir()
            (workspace / "README.md").write_text("Source status: `synthetic_fixture`\n", encoding="utf-8")
            (workspace / "package.json").write_text(json.dumps({"scripts": {"test": "pytest"}}), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_first_project_analysis.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--generated-at",
                    "2026-06-19T17:35:00+03:00",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            manifest = json.loads(stage.joinpath("analysis-manifest.json").read_text(encoding="utf-8"))
            index_html = stage.joinpath("index.html").read_text(encoding="utf-8")
            gate = manifest["primary_cockpit"]["view_model"]["visual_accessibility_acceptance"]

            self.assertEqual(gate["schema_version"], "first_run_visual_accessibility_acceptance_v1")
            self.assertEqual(gate["status"], "static_gate_ready_browser_gap_recorded")
            self.assertEqual(gate["certification_status"], "not_certified_static_orientation_only")
            self.assertEqual(gate["browser_visual_proof_status"], "not_run_approval_required")
            self.assertFalse(gate["wcag_certification_claimed"])
            self.assertFalse(gate["runtime_interaction_proof_claimed"])
            self.assertIn("responsive_css_guards", {item["id"] for item in gate["static_checks"]})
            self.assertIn("keyboard_reachable_controls", {item["id"] for item in gate["static_checks"]})
            self.assertIn("no_external_network", {item["id"] for item in gate["static_checks"]})
            self.assertIn("browser screenshot proof", gate["accepted_gaps"])

            for marker in [
                'id="visual-accessibility-acceptance"',
                'class="visual-accessibility-acceptance"',
                'data-visual-a11y-gate="static-only"',
                "Visual / Responsive / Accessibility Gate",
                "not_certified_static_orientation_only",
                "browser_visual_proof_status",
                "responsive_css_guards",
                "keyboard_reachable_controls",
                "no_external_network",
            ]:
                self.assertIn(marker, index_html)
            self.assertIn("@media(max-width:760px)", index_html)
            self.assertIn("overflow-wrap:anywhere", index_html)
            self.assertNotIn("wcag certified", index_html.lower())
            self.assertNotIn("full wcag certification", index_html.lower())
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
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
            self.assertNotIn("<script src", index_html.lower())
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
            self.assertTrue(safety["offline_policy"]["script_tags_allowed"])
            self.assertTrue(safety["offline_policy"]["inline_local_script_allowed"])
            self.assertFalse(safety["offline_policy"]["external_script_src_allowed"])
            self.assertEqual(safety["offline_policy"]["script_policy"], "approved_inline_local_only_no_script_src")
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
            self.assertNotIn("<script src", index_html.lower())
            self.assertNotIn("fetch(", index_html.lower())
            self.assertNotIn("http://", index_html.lower())
            self.assertNotIn("https://", index_html.lower())
            self.assertNotIn("raw_source", index_html.lower())

            ids = re.findall(r'id="([^"]+)"', index_html)
            self.assertEqual(len(ids), len(set(ids)))
            nav_targets = re.findall(r'<a href="#([^"]+)">', index_html)
            page_targets = [target for target in nav_targets if target.startswith("page-")]
            self.assertEqual(len(set(page_targets)), view_model["page_count"])
            for target in set(page_targets):
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
            welcome = first_response["welcome_message"]
            self.assertEqual(welcome["schema_version"], "first_run_welcome_message_v1")
            self.assertEqual(welcome["title"], "Welcome to Product-Agent OS")
            self.assertIn("Product-Agent OS", welcome["summary"])
            self.assertEqual(welcome["self_learning_loop"]["status"], "disclosed_planned_manual_first")
            self.assertEqual(welcome["self_learning_loop"]["default_settings"]["cadence"], "manual_only")
            self.assertEqual(welcome["self_learning_loop"]["default_settings"]["apply_mode"], "draft_only")
            self.assertIn("weekly", {option["id"] for option in welcome["self_learning_loop"]["cadence_options"]})
            self.assertIn("weekly_due_check", {trigger["id"] for trigger in welcome["self_learning_loop"]["triggers"]})
            self.assertIn("approval_required", {mode["id"] for mode in welcome["self_learning_loop"]["apply_modes"]})
            self.assertIn("does not activate it", welcome["self_learning_loop"]["manual_activation"])
            self.assertEqual(welcome["self_learning_loop"]["manual_runner"]["status"], "available_manual_only")
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

    def test_b41_s5_m21_no_args_help_discloses_product_agent_os_and_self_learning_loop(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "run_first_project_analysis.py"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        welcome = payload["welcome_message"]

        self.assertEqual(payload["status"], "help")
        self.assertEqual(welcome["schema_version"], "first_run_welcome_message_v1")
        self.assertIn("Product-Agent OS", welcome["summary"])
        self.assertEqual(welcome["self_learning_loop"]["default_settings"]["cadence"], "manual_only")
        self.assertEqual(welcome["self_learning_loop"]["default_settings"]["apply_mode"], "draft_only")
        self.assertIn("weekly", {option["id"] for option in welcome["self_learning_loop"]["cadence_options"]})
        self.assertIn("weekly_due_check", {trigger["id"] for trigger in welcome["self_learning_loop"]["triggers"]})
        self.assertIn("run_self_learning_loop.py", welcome["self_learning_loop"]["manual_commands"]["run_now"])
        self.assertIn(
            "auto_apply_limited_future_after_explicit_approval",
            {mode["id"] for mode in welcome["self_learning_loop"]["apply_modes"]},
        )
        self.assertFalse(payload["actions_performed"]["active_automation"])
        self.assertFalse(payload["actions_performed"]["target_workspace_mutation"])

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
