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
LOCAL_BACKEND_TARGET = Path(".codex/product-agent-os/project-code-graph-backend.json")
SEMANTIC_RETRIEVAL_TARGET = Path(".codex/product-agent-os/project-code-graph-semantic-index.json")
LLM_EXTRACTION_TARGET = Path(".codex/product-agent-os/project-code-graph-llm-proposals.json")
EXTENSION_CLOSURE_TARGET = Path(".codex/product-agent-os/project-code-graph-extension-closure.json")
EMBEDDING_PROVIDER_TARGET = Path(".codex/product-agent-os/project-code-graph-embedding-provider.json")
RERANKER_PROVIDER_TARGET = Path(".codex/product-agent-os/project-code-graph-reranker-provider.json")
HYBRID_RETRIEVAL_TARGET = Path(".codex/product-agent-os/project-code-graph-hybrid-retrieval.json")
LLM_PROPOSAL_PROVIDER_TARGET = Path(".codex/product-agent-os/project-code-graph-llm-proposal-provider.json")
LLM_PROPOSAL_EVAL_TARGET = Path(".codex/product-agent-os/project-code-graph-llm-proposal-eval.json")
REVIEW_LEDGER_TARGET = Path(".codex/product-agent-os/project-code-graph-review-ledger.json")
PROPOSAL_DIFF_TARGET = Path(".codex/product-agent-os/project-code-graph-proposal-diff.json")
MUTATION_PLAN_TARGET = Path(".codex/product-agent-os/project-code-graph-mutation-plan.json")
MUTATED_GRAPH_TARGET = Path(".codex/product-agent-os/project-code-graph-canonical-mutated.json")
MUTATION_JOURNAL_TARGET = Path(".codex/product-agent-os/project-code-graph-mutation-journal.jsonl")
ROLLBACK_PROOF_TARGET = Path(".codex/product-agent-os/project-code-graph-rollback-proof.json")


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

    def test_validate_embedding_provider_cli_requires_approval_and_stages_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            live_approval_path = Path(tmp) / "live-approval.json"
            embedding_approval_path = Path(tmp) / "embedding-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            live_approval_path.write_text(json.dumps(self._live_governance_approval()), encoding="utf-8")
            embedding_approval_path.write_text(json.dumps(self._embedding_provider_approval()), encoding="utf-8")

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
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            governance = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
                    str(live_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-embedding-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            provider = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-embedding-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--embedding-provider-approval",
                    str(embedding_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(semantic.returncode, 0, semantic.stdout + semantic.stderr)
            self.assertEqual(governance.returncode, 0, governance.stdout + governance.stderr)
            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(provider.returncode, 0, provider.stdout + provider.stderr)
            missing_payload = json.loads(missing_approval.stdout)
            provider_payload = json.loads(provider.stdout)
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(provider_payload["rendered_artifacts"]["mode"], "validate-embedding-provider")
            self.assertFalse(provider_payload["rendered_artifacts"]["provider_call_allowed"])
            self.assertTrue((stage_root / EMBEDDING_PROVIDER_TARGET).exists())

            disable = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-embedding-provider",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            disable_payload = json.loads(disable.stdout)
            self.assertEqual(disable_payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(disable_payload["rendered_artifacts"]["fallback"], "semantic_retrieval_or_graph_only")
            self.assertFalse((stage_root / EMBEDDING_PROVIDER_TARGET).exists())
            self.assertNotIn(str(workspace), provider.stdout + disable.stdout)

    def test_validate_reranker_and_hybrid_cli_stage_query_disable_without_provider_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            live_approval_path = Path(tmp) / "live-approval.json"
            reranker_approval_path = Path(tmp) / "reranker-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            (workspace / "tests").mkdir()
            (workspace / "tests" / "test_worker.py").write_text(
                "from app.worker import run\n\n"
                "def test_run():\n"
                "    assert run() == 'ok'\n",
                encoding="utf-8",
            )
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            live_approval_path.write_text(json.dumps(self._live_governance_approval()), encoding="utf-8")
            reranker_approval_path.write_text(json.dumps(self._reranker_provider_approval()), encoding="utf-8")

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
            semantic = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-semantic-index",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-approval",
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            governance = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
                    str(live_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-reranker-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            reranker = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-reranker-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--reranker-provider-approval",
                    str(reranker_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            hybrid = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-hybrid-retrieval",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--reranker-provider",
                    str(stage_root / RERANKER_PROVIDER_TARGET),
                    "--reranker-provider-approval",
                    str(reranker_approval_path),
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
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--hybrid-retrieval",
                    str(stage_root / HYBRID_RETRIEVAL_TARGET),
                    "--text",
                    "worker run",
                    "--max-results",
                    "5",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            for result in [stage, index, semantic, governance, reranker, hybrid, query]:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn(str(workspace), result.stdout)
            self.assertEqual(missing_approval.returncode, 1)
            missing_payload = json.loads(missing_approval.stdout)
            reranker_payload = json.loads(reranker.stdout)
            hybrid_payload = json.loads(hybrid.stdout)
            query_payload = json.loads(query.stdout)
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(reranker_payload["rendered_artifacts"]["mode"], "validate-reranker-provider")
            self.assertFalse(reranker_payload["rendered_artifacts"]["provider_call_allowed"])
            self.assertEqual(hybrid_payload["rendered_artifacts"]["mode"], "build-hybrid-retrieval")
            self.assertFalse(hybrid_payload["rendered_artifacts"]["provider_call_allowed"])
            self.assertEqual(query_payload["search_backend"], "hybrid_retrieval")
            self.assertEqual(query_payload["nodes"][0]["id"], "function:app.worker.run")
            self.assertEqual(query_payload["nodes"][0]["confidence"], "present_unverified")
            self.assertIn("component_scores", query_payload["nodes"][0])
            self.assertFalse(query_payload["provider_policy"]["provider_call_allowed"])
            self.assertFalse(query_payload["provider_policy"]["external_call_performed"])
            self.assertTrue((stage_root / RERANKER_PROVIDER_TARGET).exists())
            self.assertTrue((stage_root / HYBRID_RETRIEVAL_TARGET).exists())

            disable_hybrid = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-hybrid-retrieval",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            disable_reranker = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-reranker-provider",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(disable_hybrid.returncode, 0, disable_hybrid.stdout + disable_hybrid.stderr)
            self.assertEqual(disable_reranker.returncode, 0, disable_reranker.stdout + disable_reranker.stderr)
            self.assertEqual(json.loads(disable_hybrid.stdout)["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(json.loads(disable_reranker.stdout)["rendered_artifacts"]["status"], "disabled")
            self.assertFalse((stage_root / HYBRID_RETRIEVAL_TARGET).exists())
            self.assertFalse((stage_root / RERANKER_PROVIDER_TARGET).exists())

    def test_build_llm_proposals_cli_requires_approval_and_stages_proposals(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "llm-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")

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
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            proposals = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(semantic.returncode, 0, semantic.stdout + semantic.stderr)
            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(proposals.returncode, 0, proposals.stdout + proposals.stderr)
            missing_payload = json.loads(missing_approval.stdout)
            proposal_payload = json.loads(proposals.stdout)
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(proposal_payload["rendered_artifacts"]["mode"], "build-llm-proposals")
            self.assertEqual(proposal_payload["rendered_artifacts"]["cache_status"], "miss")
            self.assertTrue((stage_root / LLM_EXTRACTION_TARGET).exists())
            self.assertNotIn("return 'ok'", proposals.stdout)
            self.assertNotIn(str(workspace), proposals.stdout)

    def test_validate_llm_proposal_provider_cli_stage_disable_without_provider_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            llm_approval_path = Path(tmp) / "llm-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            live_approval_path = Path(tmp) / "live-approval.json"
            provider_approval_path = Path(tmp) / "llm-provider-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            llm_approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            live_approval_path.write_text(json.dumps(self._live_governance_approval()), encoding="utf-8")
            provider_approval_path.write_text(json.dumps(self._llm_proposal_provider_approval()), encoding="utf-8")

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
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            proposals = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(llm_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            governance = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
                    str(live_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-llm-proposal-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            provider = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-llm-proposal-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--llm-proposal-provider-approval",
                    str(provider_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            for result in [stage, semantic, proposals, governance, provider]:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn(str(workspace), result.stdout)
                self.assertNotIn("return 'ok'", result.stdout)
            self.assertEqual(missing_approval.returncode, 1)
            missing_payload = json.loads(missing_approval.stdout)
            provider_payload = json.loads(provider.stdout)
            provider_gate = json.loads((stage_root / LLM_PROPOSAL_PROVIDER_TARGET).read_text(encoding="utf-8"))
            safety_eval = json.loads((stage_root / LLM_PROPOSAL_EVAL_TARGET).read_text(encoding="utf-8"))
            self.assertEqual(missing_payload["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(provider_payload["rendered_artifacts"]["mode"], "validate-llm-proposal-provider")
            self.assertFalse(provider_payload["rendered_artifacts"]["provider_call_allowed"])
            self.assertFalse(provider_payload["rendered_artifacts"]["provider_enabled_by_default"])
            self.assertFalse(provider_payload["rendered_artifacts"]["accepted_for_canonical_graph"])
            self.assertEqual(provider_gate["provider_policy"]["provider"], "external_llm")
            self.assertFalse(provider_gate["provider_policy"]["provider_call_allowed"])
            self.assertFalse(provider_gate["provider_policy"]["external_call_performed"])
            self.assertEqual(provider_gate["prompt_contract"]["output_format"], "structured_json")
            self.assertTrue(provider_gate["prompt_contract"]["proposal_only"])
            self.assertEqual(provider_gate["canonical_graph_mutation"], "forbidden")
            self.assertEqual(safety_eval["decision_status"], "disabled_fallback")
            self.assertIn("llm_proposal_eval:missing", safety_eval["failed_thresholds"])
            self.assertFalse(safety_eval["external_call_performed"])
            self.assertFalse(safety_eval["accepted_for_canonical_graph"])
            self.assertTrue((stage_root / LLM_PROPOSAL_PROVIDER_TARGET).exists())
            self.assertTrue((stage_root / LLM_PROPOSAL_EVAL_TARGET).exists())

            disable = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-llm-proposal-provider",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            disable_payload = json.loads(disable.stdout)
            self.assertEqual(disable_payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(
                disable_payload["rendered_artifacts"]["fallback"],
                "local_llm_proposals_or_semantic_retrieval_or_graph_only",
            )
            self.assertFalse((stage_root / LLM_PROPOSAL_PROVIDER_TARGET).exists())
            self.assertFalse((stage_root / LLM_PROPOSAL_EVAL_TARGET).exists())

    def test_build_review_ledger_cli_stage_disable_without_canonical_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            llm_approval_path = Path(tmp) / "llm-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            live_approval_path = Path(tmp) / "live-approval.json"
            provider_approval_path = Path(tmp) / "llm-provider-approval.json"
            review_approval_path = Path(tmp) / "review-ledger-approval.json"
            decisions_path = Path(tmp) / "review-decisions.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            llm_approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            live_approval_path.write_text(json.dumps(self._live_governance_approval()), encoding="utf-8")
            provider_approval_path.write_text(json.dumps(self._llm_proposal_provider_approval()), encoding="utf-8")
            review_approval_path.write_text(json.dumps(self._review_ledger_approval()), encoding="utf-8")

            commands = [
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--stage",
                    str(stage_root),
                ],
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
                    str(semantic_approval_path),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(llm_approval_path),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
                    str(live_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-llm-proposal-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--llm-proposal-provider-approval",
                    str(provider_approval_path),
                    "--stage",
                    str(stage_root),
                ],
            ]
            results = [
                subprocess.run(command, check=False, capture_output=True, text=True)
                for command in commands
            ]
            for result in results:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn(str(workspace), result.stdout)
                self.assertNotIn("return 'ok'", result.stdout)

            proposals = json.loads((stage_root / LLM_EXTRACTION_TARGET).read_text(encoding="utf-8"))
            decisions_path.write_text(json.dumps(self._review_decisions(proposals)), encoding="utf-8")

            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-review-ledger",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--llm-proposal-provider",
                    str(stage_root / LLM_PROPOSAL_PROVIDER_TARGET),
                    "--llm-proposal-eval",
                    str(stage_root / LLM_PROPOSAL_EVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--review-decisions",
                    str(decisions_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            review = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-review-ledger",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--llm-proposal-provider",
                    str(stage_root / LLM_PROPOSAL_PROVIDER_TARGET),
                    "--llm-proposal-eval",
                    str(stage_root / LLM_PROPOSAL_EVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--review-ledger-approval",
                    str(review_approval_path),
                    "--review-decisions",
                    str(decisions_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(review.returncode, 0, review.stdout + review.stderr)
            payload = json.loads(review.stdout)
            ledger = json.loads((stage_root / REVIEW_LEDGER_TARGET).read_text(encoding="utf-8"))
            diff = json.loads((stage_root / PROPOSAL_DIFF_TARGET).read_text(encoding="utf-8"))
            self.assertEqual(payload["rendered_artifacts"]["mode"], "build-review-ledger")
            self.assertFalse(payload["rendered_artifacts"]["accepted_for_canonical_graph"])
            self.assertEqual(payload["rendered_artifacts"]["canonical_graph_mutation"], "forbidden")
            self.assertFalse(payload["rendered_artifacts"]["provider_call_allowed"])
            self.assertFalse(payload["rendered_artifacts"]["external_call_performed"])
            self.assertEqual(ledger["artifact_kind"], "project_graph_human_review_ledger")
            self.assertEqual(ledger["decision_summary"]["accepted"], 1)
            self.assertFalse(ledger["accepted_for_canonical_graph"])
            self.assertEqual(diff["artifact_kind"], "project_graph_proposal_diff_preview")
            self.assertTrue(diff["human_can_inspect_before_mutation"])
            self.assertTrue(diff["mutation_plan_required_for_apply"])
            self.assertFalse(diff["mutated_canonical_graph"])
            self.assertNotIn(str(workspace), review.stdout)
            self.assertNotIn("return 'ok'", review.stdout)

            disable = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-review-ledger",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            self.assertFalse((stage_root / REVIEW_LEDGER_TARGET).exists())
            self.assertFalse((stage_root / PROPOSAL_DIFF_TARGET).exists())

    def test_build_canonical_mutation_cli_stage_disable_with_journal_and_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            llm_approval_path = Path(tmp) / "llm-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            live_approval_path = Path(tmp) / "live-approval.json"
            provider_approval_path = Path(tmp) / "llm-provider-approval.json"
            review_approval_path = Path(tmp) / "review-ledger-approval.json"
            mutation_approval_path = Path(tmp) / "canonical-mutation-approval.json"
            decisions_path = Path(tmp) / "review-decisions.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            llm_approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            live_approval_path.write_text(json.dumps(self._live_governance_approval()), encoding="utf-8")
            provider_approval_path.write_text(json.dumps(self._llm_proposal_provider_approval()), encoding="utf-8")
            review_approval_path.write_text(json.dumps(self._review_ledger_approval()), encoding="utf-8")
            mutation_approval_path.write_text(json.dumps(self._canonical_mutation_approval()), encoding="utf-8")

            commands = [
                [sys.executable, str(SCRIPT), str(workspace), "--stage", str(stage_root)],
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
                    str(semantic_approval_path),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(llm_approval_path),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
                    str(live_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-llm-proposal-provider",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--llm-proposal-provider-approval",
                    str(provider_approval_path),
                    "--stage",
                    str(stage_root),
                ],
            ]
            results = [subprocess.run(command, check=False, capture_output=True, text=True) for command in commands]
            for result in results:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn(str(workspace), result.stdout)
                self.assertNotIn("return 'ok'", result.stdout)

            proposals = json.loads((stage_root / LLM_EXTRACTION_TARGET).read_text(encoding="utf-8"))
            decisions_path.write_text(json.dumps(self._review_decisions(proposals)), encoding="utf-8")
            review = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-review-ledger",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--llm-proposals",
                    str(stage_root / LLM_EXTRACTION_TARGET),
                    "--llm-proposal-provider",
                    str(stage_root / LLM_PROPOSAL_PROVIDER_TARGET),
                    "--llm-proposal-eval",
                    str(stage_root / LLM_PROPOSAL_EVAL_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--review-ledger-approval",
                    str(review_approval_path),
                    "--review-decisions",
                    str(decisions_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(review.returncode, 0, review.stdout + review.stderr)

            missing_approval = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-canonical-mutation",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--review-ledger",
                    str(stage_root / REVIEW_LEDGER_TARGET),
                    "--proposal-diff",
                    str(stage_root / PROPOSAL_DIFF_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            mutation = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-canonical-mutation",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--review-ledger",
                    str(stage_root / REVIEW_LEDGER_TARGET),
                    "--proposal-diff",
                    str(stage_root / PROPOSAL_DIFF_TARGET),
                    "--live-governance",
                    str(stage_root / ".codex/product-agent-os/project-code-graph-live-governance.json"),
                    "--canonical-mutation-approval",
                    str(mutation_approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(missing_approval.returncode, 1)
            self.assertEqual(mutation.returncode, 0, mutation.stdout + mutation.stderr)
            payload = json.loads(mutation.stdout)
            plan = json.loads((stage_root / MUTATION_PLAN_TARGET).read_text(encoding="utf-8"))
            rollback = json.loads((stage_root / ROLLBACK_PROOF_TARGET).read_text(encoding="utf-8"))
            journal_lines = (stage_root / MUTATION_JOURNAL_TARGET).read_text(encoding="utf-8").splitlines()
            journal_entry = json.loads(journal_lines[0])
            self.assertEqual(payload["rendered_artifacts"]["mode"], "build-canonical-mutation")
            self.assertEqual(payload["rendered_artifacts"]["status"], "ready")
            self.assertEqual(payload["rendered_artifacts"]["canonical_graph_mutation"], "stage_root_generated_graph_copy_only")
            self.assertTrue(payload["rendered_artifacts"]["only_accepted_proposals_mutate_graph"])
            self.assertTrue(payload["rendered_artifacts"]["accepted_gap_remains_non_mutating"])
            self.assertTrue(payload["rendered_artifacts"]["rollback_restores_previous_graph_digest"])
            self.assertEqual(plan["artifact_kind"], "project_graph_canonical_mutation_plan")
            self.assertTrue(plan["no_mutation_without_dry_run_plan"])
            self.assertEqual(plan["dry_run"]["status"], "passed")
            self.assertEqual(len(plan["operations"]), 1)
            self.assertEqual(journal_entry["artifact_kind"], "project_graph_mutation_journal")
            self.assertTrue(journal_entry["append_only"])
            self.assertTrue(journal_entry["inverse_patch"])
            self.assertEqual(rollback["artifact_kind"], "project_graph_rollback_proof")
            self.assertTrue(rollback["rollback_restores_previous_graph_digest"])
            self.assertTrue((stage_root / MUTATED_GRAPH_TARGET).exists())
            self.assertNotIn(str(workspace), mutation.stdout)
            self.assertNotIn("return 'ok'", mutation.stdout)

            disable = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-canonical-mutation",
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            self.assertFalse((stage_root / MUTATION_PLAN_TARGET).exists())
            self.assertFalse((stage_root / MUTATED_GRAPH_TARGET).exists())
            self.assertFalse((stage_root / MUTATION_JOURNAL_TARGET).exists())
            self.assertFalse((stage_root / ROLLBACK_PROOF_TARGET).exists())

    def test_disable_llm_proposals_cli_removes_generated_proposals_without_touching_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "llm-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")

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
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            proposals = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            disable = subprocess.run(
                [sys.executable, str(SCRIPT), str(workspace), "--disable-llm-proposals", "--stage", str(stage_root)],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(stage.returncode, 0, stage.stdout + stage.stderr)
            self.assertEqual(semantic.returncode, 0, semantic.stdout + semantic.stderr)
            self.assertEqual(proposals.returncode, 0, proposals.stdout + proposals.stderr)
            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            payload = json.loads(disable.stdout)
            self.assertEqual(payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(payload["rendered_artifacts"]["fallback"], "semantic_retrieval_or_graph_only")
            self.assertFalse((stage_root / LLM_EXTRACTION_TARGET).exists())

    def test_verify_and_disable_extensions_cli_records_batch23_closure_and_deletion_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            backend_approval_path = Path(tmp) / "backend-approval.json"
            semantic_approval_path = Path(tmp) / "semantic-approval.json"
            llm_approval_path = Path(tmp) / "llm-approval.json"
            evidence_path = Path(tmp) / "verification-evidence.json"
            (workspace / "app").mkdir(parents=True)
            (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
            backend_approval_path.write_text(json.dumps(self._backend_approval()), encoding="utf-8")
            semantic_approval_path.write_text(json.dumps(self._semantic_approval()), encoding="utf-8")
            llm_approval_path.write_text(json.dumps(self._llm_approval()), encoding="utf-8")
            evidence_path.write_text(
                json.dumps(
                    {
                        "focused_suites": {
                            "static_index": "passed",
                            "backend": "passed",
                            "semantic": "passed",
                            "llm_proposals": "passed",
                        },
                        "full_verification_required": True,
                        "timeout_ms": 1_200_000,
                        "docs_check_required": True,
                        "strict_mkdocs_required": True,
                        "diff_hygiene_required": True,
                    }
                ),
                encoding="utf-8",
            )

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
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--backend-approval",
                    str(backend_approval_path),
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
                    "--index",
                    str(stage_root / STATIC_SEARCH_INDEX_TARGET),
                    "--semantic-approval",
                    str(semantic_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            proposals = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--build-llm-proposals",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--semantic-index",
                    str(stage_root / SEMANTIC_RETRIEVAL_TARGET),
                    "--llm-approval",
                    str(llm_approval_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            verify = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--verify-extensions",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                    "--verification-evidence",
                    str(evidence_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            disable = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--disable-extensions",
                    "--graph",
                    str(stage_root / PROJECT_GRAPH_TARGET),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            for result in [stage, index, backend, semantic, proposals, verify, disable]:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stderr, "")
                self.assertNotIn(str(workspace), result.stdout)
            verify_payload = json.loads(verify.stdout)
            disable_payload = json.loads(disable.stdout)
            self.assertEqual(verify_payload["rendered_artifacts"]["mode"], "verify-extensions")
            self.assertEqual(verify_payload["rendered_artifacts"]["status"], "ready")
            self.assertEqual(verify_payload["rendered_artifacts"]["files"][0]["action"], "create")
            self.assertEqual(disable_payload["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(disable_payload["rendered_artifacts"]["graph_only_fallback"]["status"], "ok")
            for target in [
                STATIC_SEARCH_INDEX_TARGET,
                LOCAL_BACKEND_TARGET,
                SEMANTIC_RETRIEVAL_TARGET,
                LLM_EXTRACTION_TARGET,
                EXTENSION_CLOSURE_TARGET,
            ]:
                self.assertFalse((stage_root / target).exists())

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

    def _live_governance_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": [
                "approval_packet",
                "data_classification",
                "redaction_pipeline",
                "credential_boundary",
                "cache_policy",
                "budget_policy",
            ],
            "data_classification": {
                "allowed_fields": ["node_id", "label", "type", "observation_ids", "redacted_summary"],
                "redacted_fields": ["relative_path", "source_span", "review_comment"],
                "blocked_fields": ["absolute_local_paths", "raw_source_bodies", "secrets"],
            },
            "redaction_boundary": {
                "raw_source_excluded": True,
                "absolute_paths_redacted": True,
                "secrets_redacted": True,
                "provider_payload_validation_required": True,
            },
            "provider_policy": {
                "external_provider_calls_allowed": False,
                "approved_providers": ["external_embedding", "external_reranker", "external_llm"],
                "requires_batch_specific_approval": True,
            },
            "credential_policy": {
                "storage": "environment_only",
                "secret_material_stored": False,
                "providers": [
                    {
                        "provider": "external_embedding",
                        "credential_source": "environment",
                        "env_var": "PRODUCT_AGENT_OS_EMBEDDING_API_KEY",
                    }
                ],
            },
            "cache_policy": {
                "storage_path": ".codex/product-agent-os/project-code-graph-live-cache.json",
                "ttl_days": 7,
                "fingerprint_scope": "redacted_graph_and_live_governance_policy",
                "stale_policy": "block_if_graph_or_policy_fingerprint_mismatch",
                "deletion_proof_required": True,
            },
            "budget_policy": {
                "max_run_tokens": 1500,
                "max_query_tokens": 600,
                "max_mutation_tokens": 0,
                "max_cost_units": 0,
                "max_latency_ms": 250,
                "on_exceed": "blocked_or_degraded_graph_only",
            },
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-live-governance.json",
            "residual_risks": ["provider drift remains blocked until provider gate eval passes"],
        }

    def _embedding_provider_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": ["external_embedding_adapter", "embedding_eval_baseline"],
            "provider": {
                "provider": "external_embedding",
                "model": "approved-embedding-model-v1",
                "credential_source": "environment",
                "credential_env_var": "PRODUCT_AGENT_OS_EMBEDDING_API_KEY",
                "external_calls_allowed": False,
                "batching": {"max_batch_size": 16, "max_batch_tokens": 1200},
            },
            "data_classification": {
                "allowed_inputs": ["redacted_graph_labels", "semantic_record_terms", "observation_ids"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "redaction_policy": {
                "raw_source_excluded": True,
                "secrets_redacted": True,
                "absolute_paths_redacted": True,
                "provider_payload_validation_required": True,
            },
            "cache_policy": {
                "storage_path": ".codex/product-agent-os/project-code-graph-embedding-provider.json",
                "cache_target": ".codex/product-agent-os/project-code-graph-embedding-provider-cache.json",
                "fingerprint_scope": "redacted_graph_semantic_index_provider_policy",
                "stale_policy": "block_if_graph_or_semantic_or_policy_fingerprint_mismatch",
                "ttl_days": 7,
                "deletion_proof_required": True,
            },
            "budget_policy": {
                "max_query_tokens": 600,
                "max_batch_tokens": 1200,
                "max_cost_units": 0,
                "max_latency_ms": 250,
                "on_exceed": "block_and_fallback_to_semantic_or_graph",
            },
            "eval_threshold": {
                "min_recall_at_k": 1.0,
                "min_mrr": 1.0,
                "min_provider_recall_delta": 0.0,
                "min_provider_mrr_delta": 0.0,
                "max_false_positive_rate": 0.0,
                "max_query_ms": 250,
                "max_payload_tokens": 1200,
            },
            "failure_handling": {
                "on_missing_provider_eval": "disabled_fallback_to_semantic_or_graph",
                "on_failed_eval": "disabled_fallback_to_semantic_or_graph",
            },
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-embedding-provider.json",
            "residual_risks": ["provider drift requires fresh eval before enablement"],
        }

    def _reranker_provider_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": ["external_reranker_adapter", "reranker_eval_baseline", "hybrid_retrieval_pipeline"],
            "provider": {
                "provider": "external_reranker",
                "model": "approved-reranker-model-v1",
                "credential_source": "environment",
                "credential_env_var": "PRODUCT_AGENT_OS_RERANKER_API_KEY",
                "external_calls_allowed": False,
                "candidate_policy": {"max_candidates": 20, "max_candidate_tokens": 1200},
            },
            "data_classification": {
                "allowed_inputs": ["redacted_query_text", "candidate_node_ids", "scores", "observation_counts"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "redaction_policy": {
                "raw_source_excluded": True,
                "secrets_redacted": True,
                "absolute_paths_redacted": True,
                "provider_payload_validation_required": True,
            },
            "cache_policy": {
                "storage_path": ".codex/product-agent-os/project-code-graph-reranker-provider.json",
                "cache_target": ".codex/product-agent-os/project-code-graph-reranker-provider-cache.json",
                "fingerprint_scope": "redacted_graph_semantic_static_provider_policy",
                "stale_policy": "block_if_graph_or_semantic_or_static_or_policy_fingerprint_mismatch",
                "ttl_days": 7,
                "deletion_proof_required": True,
            },
            "budget_policy": {
                "max_query_tokens": 600,
                "max_candidate_tokens": 1200,
                "max_cost_units": 0,
                "max_latency_ms": 250,
                "on_exceed": "block_and_fallback_to_semantic_or_graph",
            },
            "eval_threshold": {
                "min_precision_at_k": 1.0,
                "min_mrr": 1.0,
                "min_ndcg_at_k": 1.0,
                "min_provider_mrr_delta": 0.0,
                "max_false_positive_rate": 0.0,
                "max_query_ms": 250,
                "max_payload_tokens": 1200,
            },
            "failure_handling": {
                "on_missing_provider_eval": "disabled_fallback_to_semantic_or_graph",
                "on_failed_eval": "disabled_fallback_to_semantic_or_graph",
            },
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-reranker-provider.json",
            "residual_risks": ["reranker provider drift requires fresh eval before enablement"],
        }

    def _llm_proposal_provider_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": ["external_llm_proposal_adapter", "llm_proposal_safety_eval"],
            "provider": {
                "provider": "external_llm",
                "model": "approved-proposal-model-v1",
                "credential_source": "environment",
                "credential_env_var": "PRODUCT_AGENT_OS_LLM_API_KEY",
                "external_calls_allowed": False,
                "prompt_policy": {"max_prompt_tokens": 1200, "max_output_tokens": 1200},
            },
            "data_classification": {
                "allowed_inputs": ["redacted_graph_labels", "source_node_ids", "observation_ids", "schema"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "redaction_policy": {
                "raw_source_excluded": True,
                "private_comments_excluded": True,
                "secrets_redacted": True,
                "absolute_paths_redacted": True,
                "unsupported_claims_labelled": True,
                "provider_payload_validation_required": True,
            },
            "cache_policy": {
                "storage_path": ".codex/product-agent-os/project-code-graph-llm-proposal-provider.json",
                "cache_target": ".codex/product-agent-os/project-code-graph-llm-proposal-eval.json",
                "fingerprint_scope": "redacted_graph_semantic_local_proposals_prompt_policy",
                "stale_policy": "block_if_graph_or_semantic_or_local_proposal_or_policy_fingerprint_mismatch",
                "ttl_days": 7,
                "deletion_proof_required": True,
            },
            "budget_policy": {
                "max_prompt_tokens": 1200,
                "max_output_tokens": 1200,
                "max_cost_units": 0,
                "max_latency_ms": 250,
                "on_exceed": "block_and_fallback_to_local_proposals_or_graph",
            },
            "eval_threshold": {
                "min_grounded_proposal_rate": 1.0,
                "max_unsupported_claim_rate": 0.0,
                "max_privacy_violations": 0,
                "max_stale_context_results": 0,
                "max_query_ms": 250,
                "max_payload_tokens": 1200,
            },
            "failure_handling": {
                "on_missing_provider_eval": "disabled_fallback_to_local_proposals_or_graph",
                "on_failed_eval": "incident_blocked_and_fallback",
            },
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-llm-proposal-provider.json",
            "incident_path": "disable provider and record AI incident workflow",
            "residual_risks": ["provider hallucination remains blocked until owner review"],
        }

    def _review_ledger_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": ["human_review_ledger", "proposal_diff_preview"],
            "review_policy": {
                "owner_decision_required": True,
                "evidence_refs_required": True,
                "allowed_decisions": ["accepted", "rejected", "accepted_gap"],
                "accepted_gap_requires_risk": True,
                "safety_eval_required": True,
            },
            "diff_policy": {
                "preview_nodes_edges_rationale_comments": True,
                "canonical_mutation_allowed": False,
                "batch30_dry_run_required": True,
            },
            "data_classification": {
                "allowed_inputs": ["proposal_ids", "source_node_ids", "observation_ids", "owner_decisions"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "rollback_path": f"delete {REVIEW_LEDGER_TARGET.as_posix()}",
            "residual_risks": ["accepted proposals still require Batch 30 dry-run before mutation"],
        }

    def _canonical_mutation_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": [
                "canonical_mutation_dry_run",
                "mutation_journal",
                "accepted_mutation_apply",
                "rollback_engine",
            ],
            "mutation_policy": {
                "dry_run_required": True,
                "conflict_check_required": True,
                "graph_digest_check_required": True,
                "accepted_only": True,
                "stage_root_only": True,
                "review_ledger_required": True,
                "proposal_diff_required": True,
            },
            "journal_policy": {
                "append_only": True,
                "jsonl_required": True,
                "inverse_patch_required": True,
            },
            "rollback_policy": {
                "restore_prior_digest": True,
                "delete_generated_caches": True,
                "stage_root_only": True,
                "rollback_proof_required": True,
            },
            "data_classification": {
                "allowed_inputs": ["reviewed_proposal_ids", "source_node_ids", "observation_ids", "owner_decisions"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "rollback_path": "delete generated Batch 30 mutation artifacts under stage root",
            "residual_risks": ["accepted proposals can still represent incorrect semantics until rollback proof is inspected"],
        }

    def _review_decisions(self, proposals: dict) -> dict:
        decisions = []
        for proposal, decision in [
            (self._proposal_by_kind(proposals, "semantic_node", index=0), "accepted"),
            (self._proposal_by_kind(proposals, "semantic_edge", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "rationale_comment", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "semantic_node", index=1), "rejected"),
        ]:
            record = {
                "proposal_id": proposal["proposal_id"],
                "decision": decision,
                "decision_by": "Product-Agent OS Maintainer",
                "evidence_refs": proposal["source_observation_ids"],
                "rationale": f"Owner reviewed {proposal['proposal_kind']} proposal.",
            }
            if decision == "accepted_gap":
                record["accepted_gap_risk"] = "Accepted as a bounded gap pending Batch 30 dry-run proof."
                record["follow_up_condition"] = "Batch 30 mutation dry run must preserve graph digest expectations."
            decisions.append(record)
        return {"schema_version": 1, "owner": "Product-Agent OS Maintainer", "decisions": decisions}

    def _proposal_by_kind(self, proposals: dict, kind: str, *, index: int = 0) -> dict:
        matches = []
        for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
            for proposal in proposals.get(key, []):
                if proposal.get("proposal_kind") == kind:
                    matches.append(proposal)
        if len(matches) > index:
            return matches[index]
        if matches:
            return matches[0]
        self.fail(f"missing proposal kind {kind}")

    def _llm_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": ".codex/product-agent-os/project-code-graph-llm-proposals.json",
            "extraction_schema": {
                "semantic_nodes": True,
                "semantic_edges": True,
                "rationale_comments": True,
                "review_required": True,
            },
            "prompt_model_policy": {
                "provider": "local_deterministic",
                "model": "local-proposal-extractor-v1",
                "version": "1",
                "sampling": {"temperature": 0},
                "external_model_calls_allowed": False,
                "approved_context": ["redacted_graph_artifact", "semantic_retrieval_index"],
                "output_format": "structured_json",
            },
            "redaction_policy": {
                "raw_source_excluded": True,
                "private_comments_excluded": True,
                "secrets_redacted": True,
                "absolute_paths_redacted": True,
                "unsupported_claims_labelled": True,
            },
            "cache_policy": {
                "cache_status": "generated",
                "fingerprint_scope": "redacted_graph_semantic_index_prompt_policy",
                "stale_policy": "block_if_graph_or_semantic_fingerprint_mismatch",
                "ttl_days": 30,
            },
            "token_budget": {"max_prompt_tokens": 1500, "max_output_tokens": 1500, "max_cost_units": 0},
            "eval_threshold": {
                "min_precision": 1.0,
                "max_unsupported_claim_rate": 0.0,
                "max_privacy_violations": 0,
                "max_latency_ms": 250,
            },
            "incident_path": "disable extraction and record AI incident workflow",
            "owner": "product-agent-owner",
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-llm-proposals.json",
        }


if __name__ == "__main__":
    unittest.main()
