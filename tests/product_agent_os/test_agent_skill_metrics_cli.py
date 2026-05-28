import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
WRAPPER = SCRIPTS / "render_agent_skill_metrics_report.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.agent_skill_metrics_report import METRICS_REPORT_TARGET  # noqa: E402


class AgentSkillMetricsCliTest(unittest.TestCase):
    def test_cli_dry_run_and_stage_emit_json_without_workspace_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "metrics-stage"
            workspace.mkdir()
            _write_control_plane(workspace)

            dry_run = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    "--dry-run",
                    "--window",
                    "2026-05-28",
                    "--cadence",
                    "weekly",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            staged = subprocess.run(
                [
                    sys.executable,
                    str(WRAPPER),
                    str(workspace),
                    "--stage",
                    str(stage_root),
                    "--window",
                    "2026-05-28",
                    "--cadence",
                    "weekly",
                    "--archive",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(dry_run.returncode, 0, dry_run.stdout + dry_run.stderr)
            self.assertEqual(staged.returncode, 0, staged.stdout + staged.stderr)
            self.assertEqual(dry_run.stderr, "")
            self.assertEqual(staged.stderr, "")
            dry_payload = json.loads(dry_run.stdout)
            staged_payload = json.loads(staged.stdout)
            self.assertEqual(dry_payload["rendered_artifacts"]["mode"], "dry-run")
            self.assertEqual(staged_payload["rendered_artifacts"]["mode"], "stage")
            self.assertFalse((workspace / METRICS_REPORT_TARGET).exists())
            self.assertTrue((stage_root / METRICS_REPORT_TARGET).exists())
            self.assertNotIn(str(workspace), dry_run.stdout)
            self.assertNotIn(str(workspace), staged.stdout)

    def test_cli_missing_workspace_returns_json_error_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing-workspace"

            result = subprocess.run(
                [sys.executable, str(WRAPPER), str(missing), "--dry-run"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertIn("workspace", payload["error"])


def _write_control_plane(workspace: Path) -> None:
    for filename in ["AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"]:
        (workspace / filename).write_text(
            f"# {filename}\n\n- 2026-05-28 verification evidence: python tools/check_docs.py exited 0.\n",
            encoding="utf-8",
        )
    skill = workspace / ".codex" / "skills" / "review-slice" / "SKILL.md"
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text("---\nname: review-slice\n---\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
