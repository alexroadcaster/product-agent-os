import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.task_plan_lifecycle import (  # noqa: E402
    TaskCompletion,
    TaskPlanRequest,
    build_planned_task_matrix,
    mark_task_implemented,
)
from product_agent_os.validators import validate_task_matrix_text  # noqa: E402
from validate_task_state_consistency import validate_workspace  # noqa: E402


class TaskPlanLifecycleTest(unittest.TestCase):
    def test_report_authoring_builder_declares_previous_digest_and_whole_file(self):
        import hashlib
        from product_agent_os.task_plan_lifecycle import build_report_authoring_call
        from product_agent_os.validators import validate_report_authoring_request
        previous = b"first\n"
        call = build_report_authoring_call("reports/result.md", previous, "second\n")
        self.assertTrue(call.startswith("// paos-report-previous-sha256: " + hashlib.sha256(previous).hexdigest()))
        patch = json.loads(call.split("await tools.apply_patch(", 1)[1][:-2])
        self.assertIn("@@\n-first\n+second\n*** End of File", patch)
        self.assertIn("absent", build_report_authoring_call("result.md", None, "first\n"))
        for name in ("../result.md", "./result.md", "PLAN.md", ".codex/result.md", "result.md:stream", "result.py"):
            self.assertTrue(validate_report_authoring_request(name, previous, "second\n"))
        self.assertTrue(validate_report_authoring_request("result.md", previous, "unterminated"))

    def test_lifecycle_uses_explicit_plan_with_bounded_local_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            group = root / "docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json"
            group.parent.mkdir(parents=True)
            group.write_text(json.dumps({"tasks": [], "latest_execution_evidence_id": "B45-CQRR-A06"}), encoding="utf-8")
            marker = root / ".codex/product-agent-os/lifecycle-state.json"
            marker.parent.mkdir(parents=True)
            plan = root / "current-plan.md"
            plan.write_text("### Task `CURRENT`", encoding="utf-8")
            for name in ("PLAN.md", "RUNLOG.md", "TEST.md"):
                (root / name).write_text("A04-A06 locally implement/focused-verify T23-T29", encoding="utf-8")
            marker.write_text(json.dumps({"task_id": "CURRENT", "plan_path": "current-plan.md"}), encoding="utf-8")
            self.assertEqual(validate_workspace(root), [])
            group.write_text(json.dumps({"tasks": [], "latest_execution_evidence_id": "B45-CQRR-A07"}), encoding="utf-8")
            self.assertEqual(validate_workspace(root), [])
            group.write_text(json.dumps({"tasks": [], "latest_execution_evidence_id": "UNKNOWN"}), encoding="utf-8")
            self.assertIn("task_group_latest_evidence_unknown", validate_workspace(root))
            group.write_text(json.dumps({"tasks": [], "latest_execution_evidence_id": "B45-CQRR-A07"}), encoding="utf-8")
            plan.write_text("Different task", encoding="utf-8")
            self.assertIn("lifecycle_task_missing_from_active_plan", validate_workspace(root))
            for invalid in ("../outside.md", str(root.parent / "outside.md"), 42):
                marker.write_text(json.dumps({"task_id": "CURRENT", "plan_path": invalid}), encoding="utf-8")
                self.assertIn("lifecycle_plan_path_invalid", validate_workspace(root))

    def test_current_task_state_projections_are_consistent(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "validate_task_state_consistency.py"), str(ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_current_project_system_files_require_user_visible_briefs(self):
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        workflow = (ROOT / ".codex" / "workflows" / "task-plan-lifecycle.md").read_text(encoding="utf-8")
        control_plane_sync = (ROOT / ".codex" / "workflows" / "control-plane-sync.md").read_text(encoding="utf-8")
        eval_contract = (ROOT / ".codex" / "evals" / "agent-context-contract.json").read_text(encoding="utf-8")

        workflows = config["workflows"]
        lifecycle_contract = config["product_agent_os"]["lifecycle_contract"]
        fresh_context_files = config["product_agent_os"]["autonomy"]["fresh_context_files"]
        self.assertEqual(workflows["task_plan_lifecycle"], ".codex/workflows/task-plan-lifecycle.md")
        self.assertEqual(workflows["control_plane_sync"], ".codex/workflows/control-plane-sync.md")
        self.assertEqual(lifecycle_contract["task_plan_lifecycle"], ".codex/workflows/task-plan-lifecycle.md")
        self.assertEqual(lifecycle_contract["control_plane_sync"], ".codex/workflows/control-plane-sync.md")
        self.assertEqual(lifecycle_contract["agent_context_contract"], ".codex/evals/agent-context-contract.json")
        self.assertEqual(lifecycle_contract["chat_visibility"], "required")
        self.assertEqual(lifecycle_contract["required_for"], "large_high_risk_material_implementation_release_or_explicit_packet")
        self.assertEqual(lifecycle_contract["agent_instruction_policy"], "root_only_lifecycle_subagents_return_result_packet")
        self.assertEqual(
            fresh_context_files,
            [
                ".codex/workflows/source-context-pack.md",
                ".codex/workflows/worktree-ownership.md",
                ".codex/workflows/task-plan-lifecycle.md",
                ".codex/workflows/control-plane-sync.md",
            ],
        )

        for expected in [
            "Task Start Brief",
            "Completion Ledger",
            "Show the Task Start Brief",
            "Show the Completion Ledger",
            "user-visible",
            "config-routed lifecycle workflow contract",
        ]:
            with self.subTest(workflow=expected):
                self.assertIn(expected, workflow)

        after_execution = workflow.split("## After Execution", 1)[1]
        self.assertLess(
            after_execution.index("Update the same task block"),
            after_execution.index("Show the Completion Ledger"),
        )
        self.assertIn("terminal final response", workflow)
        self.assertIn("No tool calls are allowed after the Completion Ledger", workflow)
        self.assertIn("ready_for_completion_brief", workflow)
        self.assertIn("stopped_repair_required", workflow)
        self.assertIn("The root owns", workflow)
        self.assertIn("Subagent Result Packet", workflow)

        for expected in [
            "config_routed_task_plan_lifecycle",
            "config_routed_control_plane_sync",
            ".codex/workflows/task-plan-lifecycle.md",
            ".codex/workflows/control-plane-sync.md",
            "scoped_task_start_brief_before_execution",
            "scoped_completion_ledger_after_execution",
            "control_plane_sync_before_completion",
            "control_plane_overflow_refactor",
            "overflow_refactor_required",
            "Task Start Brief",
            "Completion Ledger",
            "Control-Plane Sync",
            "not_applicable",
            "handoff_required",
        ]:
            with self.subTest(eval_contract=expected):
                self.assertIn(expected, eval_contract)

        for expected in [
            "REQUIREMENTS.md",
            "PLAN.md",
            "TEST.md",
            "EVALS.md",
            "RUNLOG.md",
            "prod_test.md",
            "update_required",
            "not_applicable",
            "handoff_required",
            "overflow_refactor_required",
            "budget crossing is a compaction trigger",
            "not permission to skip",
            "before the Completion Ledger",
        ]:
            with self.subTest(control_plane_sync=expected):
                self.assertIn(expected, control_plane_sync)

        for path in (ROOT / ".codex" / "agents").glob("*.toml"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(agent=path.name):
                self.assertIn(".codex/config.toml", text)
                self.assertIn("root agent owns the user-visible Task Start Brief", text)
                self.assertIn("Subagent Result Packet", text)
                self.assertIn("never start or close a nested lifecycle", text)
                self.assertNotIn("show the required Task Start Brief and Completion Ledger", text)

    def test_build_planned_task_matrix_creates_valid_pre_execution_block(self):
        text = build_planned_task_matrix(
            TaskPlanRequest(
                task_id="B39-PLAN-M01",
                task="B39-PLAN-M01",
                plan_trigger="user-requested task plan",
                source="owner request",
                short_description="Create task plan lifecycle generator.",
                technical_value="Agents get a repeatable pre-execution task contract.",
                product_value="Users see what will be done before execution starts.",
                scope="Generator and validator-compatible Markdown output.",
                non_goals="No automation activation or git mutation.",
                expected_result="A valid planned detailed task block exists.",
                acceptance_criteria="Validator accepts the generated planned block.",
                verification_gates="python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v",
                risks_approval_gates="Generated plan is not execution evidence.",
                complexity="medium",
                estimated_execution_time="30m",
                agents="Product Manager, Builder, Tester",
                skills="implementation-planner, test-driven-development",
                output_artifacts="task plan Markdown",
                next_step="execute approved slice",
                depends_on="none",
                blocks="execution without plan",
            )
        )

        self.assertIn("### Task `B39-PLAN-M01`", text)
        self.assertNotIn("## Task Brief", text)
        self.assertNotIn("## Task Start Brief", text)
        self.assertNotIn("- User-visible moment:", text)
        self.assertIn("- Product value: Users see what will be done before execution starts.", text)
        self.assertIn("- Technical value: Agents get a repeatable pre-execution task contract.", text)
        self.assertIn("- Complexity: medium", text)
        self.assertIn("- Estimated execution time: 30m", text)
        self.assertNotIn("- Goal:", text)
        self.assertIn("- Verification gates: python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v", text)
        self.assertIn("- Risks / approval gates: Generated plan is not execution evidence.", text)
        self.assertIn("- Status: planned", text)
        self.assertIn("- Date and time of task implementation: pending_execution_timestamp", text)
        self.assertIn("- actual implementation date and time: pending_execution_timestamp", text)
        self.assertEqual(validate_task_matrix_text(text), [])

    def test_mark_task_implemented_updates_completion_report_and_remains_valid(self):
        planned = build_planned_task_matrix(
            TaskPlanRequest(
                task_id="B39-PLAN-M02",
                task="B39-PLAN-M02",
                plan_trigger="user-requested task plan",
                source="owner request",
                short_description="Record post-execution evidence.",
                technical_value="Completion rows become evidence-bound.",
                product_value="Users can distinguish planned work from implemented work.",
                scope="One task block.",
                non_goals="No release claim.",
                expected_result="Implemented row records current evidence.",
                acceptance_criteria="Validator accepts implemented completion fields.",
                verification_gates="python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v",
                risks_approval_gates="Evidence must not be inspection-only.",
                complexity="low",
                estimated_execution_time="15m",
                agents="Tester",
                skills="verification-before-completion",
                output_artifacts="updated task plan Markdown",
                next_step="review slice",
            )
        )

        updated = mark_task_implemented(
            planned,
            "B39-PLAN-M02",
            TaskCompletion(
                timestamp="11-06-2026 14:20",
                what_was_done="added lifecycle generator tests",
                files_touched="tests/product_agent_os/test_task_plan_lifecycle.py",
                technical_value_delivered="post-execution rows are validator-compatible",
                product_value_delivered="users get visible execution evidence",
                verification_evidence="python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v",
                residual_risks="CLI coverage remains focused",
                follow_up="wire CLI wrapper",
            ),
        )

        self.assertIn("- Status: implemented", updated)
        self.assertNotIn("## Completion Brief", updated)
        self.assertNotIn("## Completion Ledger", updated)
        self.assertIn("- what was done: added lifecycle generator tests", updated)
        self.assertIn("- verification evidence: python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v", updated)
        self.assertIn("- Date and time of task implementation: 11-06-2026 14:20", updated)
        self.assertIn("- actual implementation date and time: 11-06-2026 14:20", updated)
        self.assertEqual(validate_task_matrix_text(updated), [])

    def test_create_task_plan_cli_new_and_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "plan.md"
            new_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_task_plan.py"),
                    "new",
                    "--output",
                    str(path),
                    "--task-id",
                    "B39-PLAN-M03",
                    "--task",
                    "B39-PLAN-M03",
                    "--plan-trigger",
                    "cli smoke",
                    "--source",
                    "unit test",
                    "--short-description",
                    "Generate a plan from CLI.",
                    "--technical-value",
                    "CLI writes validator-compatible planned rows.",
                    "--product-value",
                    "Users can create task plans consistently.",
                    "--scope",
                    "CLI output only.",
                    "--non-goals",
                    "No execution.",
                    "--expected-result",
                    "Plan file exists.",
                    "--acceptance-criteria",
                    "Validator accepts generated file.",
                    "--verification-gates",
                    "python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v",
                    "--risks-approval-gates",
                    "None beyond local file write.",
                    "--complexity",
                    "low",
                    "--estimated-execution-time",
                    "10m",
                    "--agents",
                    "Builder",
                    "--skills",
                    "test-driven-development",
                    "--output-artifacts",
                    "plan.md",
                    "--next-step",
                    "complete after execution",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(new_result.returncode, 0, new_result.stderr)
            self.assertEqual(validate_task_matrix_text(path.read_text(encoding="utf-8")), [])

            complete_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "create_task_plan.py"),
                    "complete",
                    "--path",
                    str(path),
                    "--task-id",
                    "B39-PLAN-M03",
                    "--timestamp",
                    "11-06-2026 14:30",
                    "--what-was-done",
                    "created CLI-generated task plan",
                    "--files-touched",
                    "plugins/product-agent-os/scripts/create_task_plan.py",
                    "--technical-value-delivered",
                    "CLI can close task rows",
                    "--product-value-delivered",
                    "Users get a standard post-execution report",
                    "--verification-evidence",
                    "python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v",
                    "--residual-risks",
                    "No multi-task merge support yet",
                    "--follow-up",
                    "use task matrix for larger batches",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(complete_result.returncode, 0, complete_result.stderr)
            self.assertEqual(validate_task_matrix_text(path.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()
