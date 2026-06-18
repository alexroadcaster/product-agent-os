from __future__ import annotations

import json
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


if __name__ == "__main__":
    unittest.main()
