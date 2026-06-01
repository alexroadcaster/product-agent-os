import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_backend import (  # noqa: E402
    LOCAL_BACKEND_TARGET,
    build_local_query_backend_store,
    disable_local_query_backend,
    evaluate_backend_query_contract,
    handle_backend_api_request,
    load_local_query_backend_store,
    stage_local_query_backend,
    validate_backend_approval,
    validate_local_query_backend_store,
)
from product_agent_os.project_graph_index import build_static_search_index  # noqa: E402
from product_agent_os.project_graph_queries import query_project_graph  # noqa: E402


class ProjectGraphBackendTest(unittest.TestCase):
    def test_backend_store_requires_explicit_approval_and_stays_disabled_by_default(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            index = build_static_search_index(graph)

            missing = build_local_query_backend_store(graph, static_index=index, approval=None)
            store = build_local_query_backend_store(graph, static_index=index, approval=self._approval())
            serialized = json.dumps(store, sort_keys=True).lower()

            self.assertEqual(missing["status"], "approval_required")
            self.assertIn("backend_approval:missing", missing["validation"]["errors"])
            self.assertEqual(store["schema_version"], 1)
            self.assertEqual(store["artifact_kind"], "project_graph_local_query_backend")
            self.assertEqual(store["write_policy"], "read_only")
            self.assertEqual(store["source_boundary"], "graph_and_static_index_artifacts_only_raw_source_excluded")
            self.assertEqual(store["server_lifecycle"]["server_status"], "disabled_by_default")
            self.assertFalse(store["server_lifecycle"]["active_process"])
            self.assertEqual(store["server_lifecycle"]["host"], "127.0.0.1")
            self.assertEqual(store["storage"]["storage_kind"], "local_file_store")
            self.assertEqual(store["rollback"]["disable_path"], f"delete {LOCAL_BACKEND_TARGET}")
            self.assertTrue(validate_backend_approval(self._approval())["ok"])
            malformed_port_approval = self._approval()
            malformed_port_approval["port_policy"]["port"] = "not-a-port"
            malformed = validate_backend_approval(malformed_port_approval)
            self.assertFalse(malformed["ok"])
            self.assertIn("backend_approval:port_policy:disabled_port", malformed["errors"])
            self.assertTrue(validate_local_query_backend_store(store)["ok"])
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)
            self.assertNotIn("c:\\users\\", serialized)

    def test_backend_api_is_read_only_bounded_and_has_stable_errors(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            store = build_local_query_backend_store(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._approval(),
            )

            query = handle_backend_api_request(
                store,
                {
                    "method": "POST",
                    "path": "/query",
                    "body": {"query": "search", "text": "worker run", "max_results": 5},
                },
            )
            status = handle_backend_api_request(store, {"method": "GET", "path": "/status"})
            blocked_write = handle_backend_api_request(
                store,
                {"method": "POST", "path": "/write", "body": {"node_id": "file:app/worker.py"}},
            )
            unsafe_path = handle_backend_api_request(store, {"method": "GET", "path": "C:\\Users\\person\\graph"})

            self.assertEqual(query["status"], "ok")
            self.assertEqual(query["query_backend"], "local_file_store")
            self.assertEqual(query["search_backend"], "static_index")
            self.assertEqual(query["nodes"][0]["id"], "function:app.worker.run")
            self.assertTrue(query["request_id"].startswith("backend-request:"))
            self.assertEqual(status["status"], "ok")
            self.assertEqual(status["backend_status"]["server_status"], "disabled_by_default")
            self.assertEqual(blocked_write["status"], "blocked")
            self.assertIn("backend_api:read_only", blocked_write["errors"])
            self.assertEqual(unsafe_path["status"], "blocked")
            self.assertNotIn("C:\\Users\\person", json.dumps(unsafe_path))

    def test_backend_stage_and_disable_are_workspace_safe_and_graph_only_fallback_remains(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")

            result = stage_local_query_backend(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._approval(),
            )
            target = stage_root / LOCAL_BACKEND_TARGET
            self.assertTrue(target.exists())
            loaded = load_local_query_backend_store(target)
            disabled = disable_local_query_backend(stage_root, workspace=workspace)
            fallback = query_project_graph(graph, {"query": "search", "text": "worker run", "max_results": 5})

            self.assertEqual(result["rendered_artifacts"]["status"], "ready")
            self.assertEqual(result["rendered_artifacts"]["mode"], "build-backend")
            self.assertTrue(validate_local_query_backend_store(loaded)["ok"])
            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse(target.exists())
            self.assertEqual(disabled["rendered_artifacts"]["fallback"], "graph_only_query_mode")
            self.assertEqual(fallback["status"], "ok")
            self.assertEqual(fallback["nodes"][0]["id"], "function:app.worker.run")
            with self.assertRaises(ValueError):
                stage_local_query_backend(
                    graph_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._approval(),
                )

    def test_backend_query_eval_records_performance_concurrency_and_rollback_thresholds(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            store = build_local_query_backend_store(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._approval(),
            )

            packet = evaluate_backend_query_contract(
                store,
                [{"query": "search", "text": "worker", "max_results": 5}],
                thresholds={"max_query_ms": 250, "max_payload_tokens": 4000},
            )

            self.assertEqual(packet["status"], "ok")
            self.assertEqual(packet["approval_boundary"], "batch20_explicit_local_backend_gate_no_active_server_default")
            self.assertEqual(packet["query_backend"], "local_file_store")
            self.assertTrue(packet["concurrency"]["deterministic_read_results"])
            self.assertEqual(packet["rollback"]["fallback"], "graph_only_query_mode")
            self.assertLessEqual(packet["performance"]["max_query_ms"], 250)

    def _approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": LOCAL_BACKEND_TARGET,
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
            "rollback_path": f"delete {LOCAL_BACKEND_TARGET}",
        }

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
