import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.validators import (  # noqa: E402
    validate_agent_file,
    validate_control_plane,
    validate_hook_file,
    validate_task_matrix_file,
    validate_task_matrix_text,
)


class ValidatorsTest(unittest.TestCase):
    def test_control_plane_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = validate_control_plane(Path(tmp))
        self.assertIn("AGENTS.md", result["missing"])
        self.assertFalse(result["ok"])

    def test_agent_file_accepts_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews correctness and missing tests."\n'
                'developer_instructions = "Return findings by severity."\n'
                'ownership = "Review findings"\n'
                'inputs = "Diff and verification evidence"\n'
                'outputs = "Findings and risks"\n'
                'stop_conditions = "Stop when evidence is missing."\n'
                'model_policy = "Use stronger reasoning for review."\n'
                'handoff_requirements = "Return files reviewed and open risks."\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_agent_file(path), [])

    def test_hook_file_rejects_secret_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text('TOKEN = "secret-value"\n', encoding="utf-8")
            errors = validate_hook_file(path)
        self.assertIn("contains forbidden secret-like literal", errors)

    def test_hook_file_rejects_supported_secret_assignment_styles(self):
        samples = [
            'TOKEN = "synthetic-secret"\n',
            'os.environ["API_KEY"] = "synthetic-secret"\n',
            'api_key: "synthetic-secret"\n',
            "PASSWORD=synthetic-secret\n",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for index, text in enumerate(samples):
                path = Path(tmp) / f"hook-{index}.txt"
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text):
                    errors = validate_hook_file(path)
                self.assertIn("contains forbidden secret-like literal", errors)

    def test_hook_file_ignores_secret_mentions_in_prose_and_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                "# TOKEN should be configured by the operator.\n"
                'print("PASSWORD must not be hardcoded")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_hook_file_allows_os_getenv_secret_name_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                'import os\nAPI_KEY = os.getenv("API_KEY")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_hook_file_allows_os_environ_get_secret_name_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hook.py"
            path.write_text(
                'TOKEN = os.environ.get("TOKEN")\n',
                encoding="utf-8",
            )
            self.assertEqual(validate_hook_file(path), [])

    def test_task_matrix_validator_accepts_planned_and_implemented_detailed_blocks(self):
        errors = validate_task_matrix_text(VALID_TASK_MATRIX)

        self.assertEqual(errors, [])

    def test_task_matrix_validator_rejects_summary_table_without_detailed_blocks(self):
        errors = validate_task_matrix_text(
            "# Task Matrix\n\n"
            "| Task | Status | Completion report |\n"
            "| --- | --- | --- |\n"
            "| `T10-PLAN-M06` | `implemented` | looked ok |\n"
        )

        self.assertIn("no detailed task blocks found", errors)

    def test_task_matrix_validator_rejects_fake_implemented_completion(self):
        invalid = VALID_TASK_MATRIX.replace(
            "- Date and time of task implementation: 07-06-2026 21:14",
            "- Date and time of task implementation: pending_execution_timestamp",
            1,
        ).replace(
            "- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/validators.py",
            "- files touched / work locations:",
            1,
        ).replace(
            "- verification evidence: python -m unittest tests.product_agent_os.test_validators -v",
            "- verification evidence: inspection-only review",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn("T10-PLAN-M06: implemented requires actual DD-MM-YYYY HH:mm timestamp", errors)
        self.assertIn("T10-PLAN-M06: implemented requires files touched / work locations", errors)
        self.assertIn("T10-PLAN-M06: implemented cannot use inspection-only verification evidence", errors)

    def test_task_matrix_validator_rejects_planned_rows_with_fake_actual_completion_time(self):
        invalid = VALID_TASK_MATRIX.replace(
            "- actual implementation date and time: pending_execution_timestamp",
            "- actual implementation date and time: 07-06-2026 21:14",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn(
            "T10-PLAN-M10: planned rows must not contain actual implementation date/time",
            errors,
        )

    def test_task_matrix_validator_rejects_unresolved_placeholders_and_missing_completion_report_fields(self):
        invalid = VALID_TASK_MATRIX.replace("Task `T10-PLAN-M10`", "Task `<task_id>`", 1).replace(
            "- residual risks: pending",
            "",
            1,
        )

        errors = validate_task_matrix_text(invalid)

        self.assertIn("<task_id>: unresolved placeholder in task block", errors)
        self.assertIn("<task_id>: missing completion report field: residual risks", errors)

    def test_task_matrix_file_and_cli_return_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            valid_path = Path(tmp) / "task-matrix.md"
            invalid_path = Path(tmp) / "invalid-task-matrix.md"
            valid_path.write_text(VALID_TASK_MATRIX, encoding="utf-8")
            invalid_path.write_text("# no tasks\n", encoding="utf-8")

            self.assertEqual(validate_task_matrix_file(valid_path), [])

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_task_matrix.py"),
                    str(invalid_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["no detailed task blocks found"])

    def test_agent_file_reports_invalid_toml(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.toml"
            path.write_text('name = "reviewer"\n[broken\n', encoding="utf-8")
            errors = validate_agent_file(path)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("invalid toml: "))

    def test_agent_file_reports_missing_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "incomplete.toml"
            path.write_text('name = "reviewer"\n', encoding="utf-8")
            errors = validate_agent_file(path)
        self.assertEqual(
            errors,
            [
                "missing required field: description",
                "missing required field: developer_instructions",
                "missing required field: ownership",
                "missing required field: inputs",
                "missing required field: outputs",
                "missing required field: stop_conditions",
                "missing required field: model_policy",
                "missing required field: handoff_requirements",
            ],
        )

    def test_agent_file_reports_non_utf8_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.toml"
            path.write_bytes(b"\xff\xfe\x00")
            errors = validate_agent_file(path)
        self.assertEqual(errors, ["unable to read file as utf-8 text"])

    def test_hook_file_reports_non_utf8_file_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.py"
            path.write_bytes(b"\xff\xfe\x00")
            errors = validate_hook_file(path)
        self.assertEqual(errors, ["unable to read file as utf-8 text"])

    def test_agents_wrapper_fails_clearly_when_directory_is_missing(self):
        missing = FIXTURES / "empty-repo" / ".codex" / "agents"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_agents.py"),
                str(missing),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["agent directory does not exist"])

    def test_agents_wrapper_returns_json_for_non_utf8_file_without_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.toml").write_bytes(b"\xff\xfe\x00")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_agents.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(
            payload["file_errors"],
            {str(root / "bad.toml"): ["unable to read file as utf-8 text"]},
        )

    def test_agents_wrapper_returns_zero_for_valid_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "reviewer.toml"
            path.write_text(
                'name = "reviewer"\n'
                'description = "Reviews correctness and missing tests."\n'
                'developer_instructions = "Return findings by severity."\n'
                'ownership = "Review findings"\n'
                'inputs = "Diff and verification evidence"\n'
                'outputs = "Findings and risks"\n'
                'stop_conditions = "Stop when evidence is missing."\n'
                'model_policy = "Use stronger reasoning for review."\n'
                'handoff_requirements = "Return files reviewed and open risks."\n',
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_agents.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["file_errors"], {str(path): []})

    def test_hooks_wrapper_fails_clearly_when_directory_is_missing(self):
        missing = FIXTURES / "empty-repo" / ".codex" / "hooks"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_hooks.py"),
                str(missing),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["errors"], ["hook directory does not exist"])

    def test_hooks_wrapper_returns_json_for_non_utf8_file_without_stderr(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bad.py").write_bytes(b"\xff\xfe\x00")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "validate_hooks.py"),
                    str(root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertEqual(
            payload["file_errors"],
            {str(root / "bad.py"): ["unable to read file as utf-8 text"]},
        )


VALID_TASK_MATRIX = """# Task Matrix

Source status: local implementation planning

### Task `T10-PLAN-M10`

- Task: T10-PLAN-M10
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: methodology-heavy eval guard
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: T10-PLAN-M04, T10-PLAN-M05, T10-PLAN-M06
- Blocks: T10-PLAN-M14
- Source: Batch 37 task matrix
- Short description: Add behavioral and fixture coverage.
- Technical value: Regression coverage for task-matrix behavior.
- Product value: Users can trust task reports are evidence-bound.
- Scope: Behavioral eval, fixture eval, transcript eval.
- Non-goals: No live model/API eval.
- Expected result: Synthetic evals cover task matrix behavior.
- Acceptance criteria: Detection-only is not completion evidence.
- Verification gates: python -m unittest tests.product_agent_os.test_behavioral_workflow_evals -v
- Risks / approval gates: Synthetic-only coverage.
- Complexity: medium
- Estimated execution time: 1h
- Agents: Tester
- Skills: test-driven-development, verification-before-completion
- Output artifacts: behavioral-workflows.json
- Next step: implement validator

#### Completion Report

- status: planned
- what was done: pending
- files touched / work locations: pending
- technical value delivered: pending
- product value delivered: pending
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending
- residual risks: pending
- follow-up: pending

### Task `T10-PLAN-M06`

- Task: T10-PLAN-M06
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: methodology-heavy validator guard
- Validator target: detailed task blocks
- Date and time of task implementation: 07-06-2026 21:14
- Depends on: T10-PLAN-M01, T10-PLAN-M02, T10-PLAN-M04
- Blocks: T10-PLAN-M10, T10-PLAN-M13
- Source: Batch 37 task matrix
- Short description: Add deterministic task-matrix validator.
- Technical value: Enforce evidence-before-completion.
- Product value: Users get factual task reports.
- Scope: Validator and CLI.
- Non-goals: No discovery routing.
- Expected result: Invalid implemented rows fail.
- Acceptance criteria: Validator rejects fake completion.
- Verification gates: python -m unittest tests.product_agent_os.test_validators -v
- Risks / approval gates: Markdown parsing stays conservative.
- Complexity: medium
- Estimated execution time: 2h
- Agents: Builder, Tester
- Skills: test-driven-development, verification-before-completion
- Output artifacts: validate_task_matrix.py
- Next step: add eval guard

#### Completion Report

- status: implemented
- what was done: implemented deterministic validator
- files touched / work locations: plugins/product-agent-os/scripts/product_agent_os/validators.py
- technical value delivered: validator rejects fake completion
- product value delivered: task reports become reviewable
- actual implementation date and time: 07-06-2026 21:14
- verification evidence: python -m unittest tests.product_agent_os.test_validators -v
- residual risks: validator is conservative for Markdown
- follow-up: add behavioral eval guard
"""


if __name__ == "__main__":
    unittest.main()
