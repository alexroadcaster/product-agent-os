import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "plugins" / "product-agent-os" / "scripts" / "scan_project_code_graph.py"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
PROJECT_GRAPH_TARGET = Path(".codex/product-agent-os/project-code-graph.json")


class ProjectGraphCliTest(unittest.TestCase):
    def test_cli_missing_workspace_returns_json_error_without_absolute_path_leak(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(FIXTURES / "missing-project-code-graph"), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertIn("workspace does not exist", payload["error"])
        self.assertNotIn(str(FIXTURES), result.stdout)

    def test_cli_non_directory_workspace_returns_json_error_without_absolute_path_leak(self):
        target = FIXTURES / "project-code-graph-minimal-python" / "pyproject.toml"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(target), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertIn("workspace is not a directory", payload["error"])
        self.assertNotIn(str(target), result.stdout)

    def test_stage_cli_existing_output_file_returns_json_error_without_absolute_path_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = FIXTURES / "project-code-graph-minimal-python"
            stage_file = Path(tmp) / "stage-file"
            stage_file.write_text("not a directory", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_file)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stderr, "")
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertIn("stage output path is not a directory", payload["error"])
            self.assertNotIn(str(stage_file), result.stdout)
            self.assertNotIn("Users", result.stdout)

    def test_stage_cli_unexpected_filesystem_error_is_generic_without_path_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = FIXTURES / "project-code-graph-minimal-python"
            stage_root = Path(tmp) / "stage"
            stage_root.mkdir()
            (stage_root / ".codex").write_text("blocks managed directory creation", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stderr, "")
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "error")
            self.assertEqual(payload["error"], "project graph scan failed")
            self.assertNotIn(str(stage_root), result.stdout)
            self.assertNotIn("Users", result.stdout)

    def test_dry_run_cli_prints_redacted_graph_without_workspace_writes(self):
        workspace = FIXTURES / "project-code-graph-minimal-python"
        before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))

        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(workspace), "--dry-run"],
            check=False,
            capture_output=True,
            text=True,
        )

        after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(after, before)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["write_policy"], "read_only")
        self.assertTrue(payload["validation"]["ok"], payload["validation"])
        self.assertNotIn(str(workspace), result.stdout)

    def test_stage_cli_writes_only_inside_explicit_stage_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp) / "stage"
            workspace = FIXTURES / "project-code-graph-mixed-docs-contracts"

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            payload = json.loads(result.stdout)
            staged_graph = stage_root / PROJECT_GRAPH_TARGET
            self.assertTrue(staged_graph.exists())
            self.assertTrue(staged_graph.resolve().is_relative_to(stage_root.resolve()))
            self.assertEqual(payload["rendered_artifacts"]["mode"], "stage")
            self.assertTrue(payload["rendered_artifacts"]["validation"]["ok"], payload)
            self.assertEqual(payload["rendered_artifacts"]["root_status"], "redacted")
            self.assertNotIn(str(stage_root), result.stdout)
            self.assertFalse((workspace / PROJECT_GRAPH_TARGET).exists())

    def test_cli_rejects_stage_directory_inside_workspace(self):
        workspace = FIXTURES / "project-code-graph-minimal-python"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(workspace),
                "--stage",
                str(workspace / ".codex" / "product-agent-os"),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "error")
        self.assertIn("outside workspace", payload["error"])

    def test_stage_cli_blocks_suspicious_shrink_without_silent_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage_root = Path(tmp) / "stage"
            target = stage_root / PROJECT_GRAPH_TARGET
            target.parent.mkdir(parents=True)
            target.write_text(
                json.dumps({"nodes": [{"id": f"node:{index}"} for index in range(100)], "edges": []}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(FIXTURES / "project-code-graph-minimal-python"),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["rendered_artifacts"]["status"], "blocked")
            self.assertIn("shrink_guard", payload["rendered_artifacts"]["validation"]["errors"])
            self.assertTrue((stage_root / ".codex/product-agent-os/project-code-graph.previous.json").exists())
            preserved = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(len(preserved["nodes"]), 100)

    def test_stage_cli_embeds_temporal_delta_from_existing_stage_graph(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            workspace.mkdir()
            (workspace / "keep.py").write_text("print('keep')\n", encoding="utf-8")
            (workspace / "remove.py").write_text("print('remove')\n", encoding="utf-8")

            first = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            (workspace / "remove.py").unlink()
            second = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            graph = json.loads((stage_root / PROJECT_GRAPH_TARGET).read_text(encoding="utf-8"))
            delta = graph["metadata"]["temporal_delta"]
            self.assertEqual(delta["status"], "changed")
            self.assertTrue(delta["invalidated_edges"])

    def test_stage_cli_backs_up_existing_graph_before_normal_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            workspace.mkdir()
            (workspace / "first.py").write_text("print('first')\n", encoding="utf-8")

            first = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            (workspace / "second.py").write_text("print('second')\n", encoding="utf-8")
            second = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            backup = stage_root / ".codex/product-agent-os/project-code-graph.previous.json"
            self.assertTrue(backup.exists())
            previous = json.loads(backup.read_text(encoding="utf-8"))
            self.assertIn("file:first.py", {node["id"] for node in previous["nodes"]})


if __name__ == "__main__":
    unittest.main()
