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
STATIC_SEARCH_INDEX_TARGET = Path(".codex/product-agent-os/project-code-graph-search-index.json")
SEMANTIC_RETRIEVAL_TARGET = Path(".codex/product-agent-os/project-code-graph-semantic-index.json")


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

    def test_query_cli_reads_staged_graph_without_workspace_writes_or_source_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "app" / "main.py").write_text(
                "from app.worker import run\n\n"
                "def main():\n"
                "    return run()\n",
                encoding="utf-8",
            )

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))
            query = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--query",
                    "neighbors",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--node-id",
                    "function:app.main.main",
                    "--max-results",
                    "5",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
            self.assertEqual(query.stderr, "")
            self.assertEqual(after, before)
            payload = json.loads(query.stdout)
            self.assertEqual(payload["result_kind"], "neighbors")
            self.assertTrue(any(node["id"] == "function:app.worker.run" for node in payload["nodes"]))
            self.assertNotIn("return 'ok'", query.stdout)
            self.assertNotIn(str(workspace), query.stdout)

    def test_query_cli_requires_graph_artifact_and_rejects_mixed_modes(self):
        workspace = FIXTURES / "project-code-graph-minimal-python"
        missing_graph = subprocess.run(
            [sys.executable, str(SCRIPT), str(workspace), "--query", "status"],
            check=False,
            capture_output=True,
            text=True,
        )
        mixed = subprocess.run(
            [sys.executable, str(SCRIPT), str(workspace), "--dry-run", "--query", "status", "--graph", "graph.json"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(missing_graph.returncode, 2)
        self.assertEqual(json.loads(missing_graph.stdout)["error"], "query mode requires --graph")
        self.assertEqual(mixed.returncode, 2)
        self.assertIn("choose exactly one mode", json.loads(mixed.stdout)["error"])

    def test_build_index_cli_writes_static_index_and_query_cli_uses_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            index = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            query = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--query",
                    "search",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--text",
                    "worker run",
                    "--max-results",
                    "5",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(index.returncode, 0, index.stdout + index.stderr)
            self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
            self.assertEqual(index.stderr, "")
            self.assertEqual(query.stderr, "")
            self.assertTrue((stage_root / STATIC_SEARCH_INDEX_TARGET).exists())
            index_payload = json.loads(index.stdout)
            query_payload = json.loads(query.stdout)
            self.assertEqual(index_payload["rendered_artifacts"]["cache_status"], "miss")
            self.assertEqual(query_payload["search_backend"], "static_index")
            self.assertEqual(query_payload["nodes"][0]["id"], "function:app.worker.run")
            self.assertNotIn("return 'ok'", query.stdout)
            self.assertNotIn(str(workspace), index.stdout + query.stdout)

    def test_query_cli_blocks_stale_static_index_without_serving_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")

            first_stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            index = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            (workspace / "app" / "extra.py").write_text("def extra():\n    return 'new'\n", encoding="utf-8")
            second_stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            query = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--query",
                    "search",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--text",
                    "worker",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(first_stage.returncode, 0, first_stage.stdout + first_stage.stderr)
            self.assertEqual(index.returncode, 0, index.stdout + index.stderr)
            self.assertEqual(second_stage.returncode, 0, second_stage.stdout + second_stage.stderr)
            self.assertEqual(query.returncode, 1)
            payload = json.loads(query.stdout)
            self.assertEqual(payload["status"], "blocked")
            self.assertIn("static_index:stale", payload["errors"])

    def test_build_backend_cli_requires_approval_and_query_cli_uses_backend_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._backend_approval()), encoding="utf-8")

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-backend",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            backend = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-backend",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--backend-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            query = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--query",
                    "search",
                    "--backend",
                    str(stage_root / ".codex" / "product-agent-os" / "project-code-graph-backend.json"),
                    "--text",
                    "worker run",
                    "--max-results",
                    "5",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(backend.returncode, 0, backend.stdout + backend.stderr)
            self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
            missing_payload = json.loads(missing_approval.stdout)
            backend_payload = json.loads(backend.stdout)
            query_payload = json.loads(query.stdout)
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(backend_payload["rendered_artifacts"]["mode"], "build-backend")
            self.assertEqual(backend_payload["rendered_artifacts"]["server_status"], "disabled_by_default")
            self.assertEqual(query_payload["query_backend"], "local_file_store")
            self.assertEqual(query_payload["nodes"][0]["id"], "function:app.worker.run")
            self.assertNotIn(str(workspace), backend.stdout + query.stdout)

    def test_disable_backend_cli_removes_generated_store_without_touching_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._backend_approval()), encoding="utf-8")

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            backend = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-backend",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--backend-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            disable = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--disable-backend", "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(backend.returncode, 0, backend.stdout + backend.stderr)
            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            payload = json.loads(disable.stdout)
            self.assertEqual(payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(payload["rendered_artifacts"]["fallback"], "graph_only_query_mode")
            self.assertFalse((stage_root / ".codex" / "product-agent-os" / "project-code-graph-backend.json").exists())

    def test_build_semantic_cli_requires_approval_and_query_cli_uses_semantic_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "semantic-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-semantic-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            semantic = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-semantic-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            query = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--query",
                    "search",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--text",
                    "worker run",
                    "--max-results",
                    "5",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(semantic.returncode, 0, semantic.stdout + semantic.stderr)
            self.assertEqual(query.returncode, 0, query.stdout + query.stderr)
            missing_payload = json.loads(missing_approval.stdout)
            semantic_payload = json.loads(semantic.stdout)
            query_payload = json.loads(query.stdout)
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(semantic_payload["rendered_artifacts"]["mode"], "build-semantic-index")
            self.assertEqual(semantic_payload["rendered_artifacts"]["cache_status"], "miss")
            self.assertEqual(query_payload["search_backend"], "semantic_retrieval")
            self.assertEqual(query_payload["nodes"][0]["id"], "function:app.worker.run")
            self.assertEqual(query_payload["nodes"][0]["confidence"], "present_unverified")
            self.assertNotIn(str(workspace), semantic.stdout + query.stdout)

    def test_disable_semantic_cli_removes_generated_index_without_touching_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "semantic-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")

            stage = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )
            semantic = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-semantic-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            disable = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--disable-semantic-index", "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(semantic.returncode, 0, semantic.stdout + semantic.stderr)
            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            payload = json.loads(disable.stdout)
            self.assertEqual(payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(payload["rendered_artifacts"]["fallback"], "lexical_or_graph_search")
            self.assertFalse((stage_root / SEMANTIC_RETRIEVAL_TARGET).exists())

    def _backend_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": ".codex/product-agent-os/project-code-graph-backend.json",
            "port_policy": {"host": "127.0.0.1", "port": 0, "mode": "disabled_by_default"},
            "process_lifecycle": {
                "server_enabled_by_default": False,
                "start_requires_explicit_command": True,
                "pid_path": ".codex/product-agent-os/project-code-graph-backend.pid",
            },
            "auth_boundary": {"local_only": True, "write_controls": False},
            "cleanup": {"delete_generated_store": True},
            "logging": {
                "log_path": ".codex/product-agent-os/project-code-graph-backend.log",
                "redacted": True,
            },
            "performance_threshold": {"max_query_ms": 250, "max_payload_tokens": 4000},
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-backend.json",
        }

    def _semantic_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": ".codex/product-agent-os/project-code-graph-semantic-index.json",
            "embedding_provider": "local_deterministic",
            "embedding_model": {
                "name": "local-hash-embedding-v1",
                "version": "1",
                "dimension": 64,
                "external_model_calls_allowed": False,
            },
            "cross_encoder": {
                "provider": "local_deterministic",
                "model": "local-lexical-cross-encoder-v1",
                "enabled": True,
                "external_model_calls_allowed": False,
            },
            "data_classification": {
                "allowed_inputs": ["redacted_graph_labels", "static_index_terms", "observation_ids"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "redaction_policy": {
                "raw_source_excluded": True,
                "secrets_redacted": True,
                "absolute_paths_redacted": True,
            },
            "cache_policy": {
                "cache_status": "generated",
                "fingerprint_scope": "canonical_redacted_graph_and_static_index",
                "stale_policy": "block_if_graph_fingerprint_mismatch",
                "ttl_days": 30,
            },
            "token_budget": {"max_query_tokens": 1200, "max_corpus_record_tokens": 120},
            "eval_threshold": {
                "min_recall_at_k": 1.0,
                "min_mrr": 1.0,
                "min_cross_encoder_mrr_delta": 0.0,
                "max_false_positive_rate": 0.0,
                "max_query_ms": 250,
                "max_payload_tokens": 1200,
            },
            "failure_handling": {"on_stale_or_failed_eval": "block_and_fallback_to_lexical_or_graph"},
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-semantic-index.json",
        }


if __name__ == "__main__":
    unittest.main()
