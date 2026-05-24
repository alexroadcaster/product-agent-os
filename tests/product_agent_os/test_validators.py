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


if __name__ == "__main__":
    unittest.main()
