import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_index import (  # noqa: E402
    STATIC_SEARCH_INDEX_TARGET,
    build_static_search_index,
    load_static_search_index,
    query_static_search_index,
    stage_project_graph_search_index,
    validate_static_search_index,
)


class ProjectGraphStaticSearchIndexTest(unittest.TestCase):
    def test_static_index_is_redacted_generated_cache_from_graph_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            graph["nodes"].append(
                {
                    "id": "file:unsafe.py",
                    "type": "module",
                    "label": "TOKEN=fixture-secret C:\\Users\\person\\private.py",
                    "status": "current",
                    "language": "python",
                    "path": "C:\\Users\\person\\private.py",
                    "observation_ids": ["obs:unsafe"],
                }
            )

            index = build_static_search_index(graph)
            serialized = json.dumps(index, sort_keys=True).lower()
            function_record = next(
                record
                for record in index["records"]
                if record["node_id"] == "function:app.worker.run"
            )

            self.assertEqual(index["schema_version"], 1)
            self.assertEqual(index["write_policy"], "read_only")
            self.assertEqual(index["artifact_kind"], "project_graph_static_search_index")
            self.assertEqual(index["source_boundary"], "graph_artifact_only_raw_source_excluded")
            self.assertEqual(
                index["generated_view_policy"],
                "static_search_index_is_generated_cache_not_source_of_truth",
            )
            self.assertEqual(
                index["approval_boundary"],
                "batch19_explicit_offline_static_index_no_live_backend_model_or_database",
            )
            self.assertEqual(index["cache_policy"]["cache_status"], "built")
            self.assertEqual(index["rollback"]["disable_path"], f"delete {STATIC_SEARCH_INDEX_TARGET}")
            self.assertIn("app", function_record["partitions"])
            self.assertIn("workspace", function_record["partitions"])
            self.assertEqual(function_record["confidence"], "verified")
            self.assertEqual(function_record["stale_status"], "current")
            self.assertTrue(function_record["observation_ids"])
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn("fixture-secret", serialized)
            self.assertNotIn("c:\\users\\person", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)
            self.assertTrue(validate_static_search_index(index)["ok"])

    def test_static_index_query_is_ranked_bounded_filtered_and_source_free(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            index = build_static_search_index(graph)

            packet = query_static_search_index(
                index,
                {
                    "text": "worker run",
                    "node_types": ["function"],
                    "path_prefixes": ["app/"],
                    "max_results": 3,
                    "max_tokens": 800,
                },
            )
            serialized = json.dumps(packet, sort_keys=True)

            self.assertEqual(packet["schema_version"], 1)
            self.assertEqual(packet["write_policy"], "read_only")
            self.assertEqual(packet["result_kind"], "search")
            self.assertEqual(packet["search_backend"], "static_index")
            self.assertEqual(packet["status"], "ok")
            self.assertEqual(packet["nodes"][0]["id"], "function:app.worker.run")
            self.assertLessEqual(packet["budget"]["estimated_tokens"], 800)
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_static_index_cache_records_hit_miss_and_invalidates_changed_graph(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")

            first = stage_project_graph_search_index(graph_path, stage_root, workspace=workspace)
            second = stage_project_graph_search_index(graph_path, stage_root, workspace=workspace)
            graph["nodes"].append(
                {
                    "id": "function:app.extra.run_extra",
                    "type": "function",
                    "label": "run_extra",
                    "status": "current",
                    "language": "python",
                    "path": "app/extra.py",
                    "observation_ids": ["obs:extra"],
                }
            )
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            third = stage_project_graph_search_index(graph_path, stage_root, workspace=workspace)

            target = stage_root / STATIC_SEARCH_INDEX_TARGET
            backup = target.with_name("project-code-graph-search-index.previous.json")
            self.assertEqual(first["rendered_artifacts"]["cache_status"], "miss")
            self.assertEqual(second["rendered_artifacts"]["cache_status"], "hit")
            self.assertEqual(second["rendered_artifacts"]["files"][0]["action"], "leave_unchanged")
            self.assertEqual(third["rendered_artifacts"]["cache_status"], "miss_invalidated")
            self.assertTrue(target.exists())
            self.assertTrue(backup.exists())
            self.assertTrue(load_static_search_index(target)["validation"]["ok"])

    def test_static_index_stage_rejects_workspace_internal_stage_root(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph_path = Path(tmp) / "graph.json"
            graph_path.write_text(json.dumps(build_project_code_graph(workspace)), encoding="utf-8")

            with self.assertRaises(ValueError) as raised:
                stage_project_graph_search_index(
                    graph_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                )

            self.assertIn("outside workspace", str(raised.exception))

    def _write_query_workspace(self, workspace: Path) -> Path:
        (workspace / "app").mkdir(parents=True)
        (workspace / "tests").mkdir()
        (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
        (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        (workspace / "app" / "main.py").write_text(
            "from app.worker import run\n\n"
            "def main():\n"
            "    return run()\n",
            encoding="utf-8",
        )
        (workspace / "tests" / "test_worker.py").write_text(
            "from app.worker import run\n\n"
            "def test_run():\n"
            "    assert run() == 'ok'\n",
            encoding="utf-8",
        )
        return workspace


if __name__ == "__main__":
    unittest.main()
