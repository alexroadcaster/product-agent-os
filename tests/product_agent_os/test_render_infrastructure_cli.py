import json
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "product-agent-os" / "scripts" / "render_infrastructure.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"


def load_cli():
    spec = importlib.util.spec_from_file_location("render_infrastructure", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RenderInfrastructureCliTest(unittest.TestCase):
    def test_dry_run_cli_prints_plan_json(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "node-app"), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        self.assertEqual(result.stderr, "", f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["infrastructure_plan"]["status"], "needs_approval")
        self.assertIn("rendered_artifacts", payload)

    def test_stage_cli_writes_output_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "stage"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURES / "python-app"), "--stage", str(out)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            self.assertEqual(result.stderr, "", f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}")
            payload = json.loads(result.stdout)
            self.assertTrue((out / "AGENTS.md").exists())
            self.assertTrue(payload["rendered_artifacts"]["validation"]["ok"])

    def test_invalid_workspace_cli_returns_clear_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "missing-workspace"), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("workspace does not exist", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_cli_rejects_missing_mode(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "node-app")],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("choose --dry-run or --stage", result.stderr)

    def test_cli_returns_nonzero_when_validation_fails(self):
        cli = load_cli()
        cli.render_infrastructure_plan = lambda workspace: {
            "infrastructure_plan": {"status": "blocked"},
            "rendered_artifacts": {"validation": {"ok": False}},
        }

        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = cli.main(["workspace", "--dry-run"])

        payload = json.loads(stdout.getvalue())
        self.assertNotEqual(exit_code, 0)
        self.assertFalse(payload["rendered_artifacts"]["validation"]["ok"])

    def test_stage_cli_existing_output_file_returns_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "stage-file"
            out.write_text("not a directory", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURES / "python-app"), "--stage", str(out)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith("error:"), result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
