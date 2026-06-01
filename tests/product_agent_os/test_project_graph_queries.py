import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_index import build_static_search_index  # noqa: E402
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph  # noqa: E402


class ProjectGraphQueriesTest(unittest.TestCase):
    def test_neighbors_search_path_hotspots_and_read_order_are_bounded_and_source_free(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            neighbors = query_project_graph(
                graph,
                {
                    "query": "neighbors",
                    "node_id": "function:app.main.main",
                    "max_results": 5,
                    "max_tokens": 1_200,
                },
            )
            search = query_project_graph(graph, {"query": "search", "text": "worker", "max_results": 5})
            path = query_project_graph(
                graph,
                {
                    "query": "path",
                    "node_id": "function:app.main.main",
                    "target_id": "function:app.worker.run",
                    "max_depth": 4,
                },
            )
            hotspots = query_project_graph(graph, {"query": "hotspots", "max_results": 3})
            read_order = query_project_graph(
                graph,
                {"query": "read_order", "node_id": "function:app.main.main", "max_results": 4},
            )
            serialized = json.dumps([neighbors, search, path, hotspots, read_order], sort_keys=True)

            self.assertEqual(neighbors["schema_version"], 1)
            self.assertEqual(neighbors["write_policy"], "read_only")
            self.assertEqual(neighbors["result_kind"], "neighbors")
            self.assertLessEqual(neighbors["budget"]["estimated_tokens"], 1_200)
            self.assertTrue(any(node["id"] == "function:app.worker.run" for node in neighbors["nodes"]))
            self.assertTrue(any(node["id"] == "function:app.worker.run" for node in search["nodes"]))
            self.assertEqual(path["status"], "ok")
            self.assertEqual(path["path"][0]["id"], "function:app.main.main")
            self.assertEqual(path["path"][-1]["id"], "function:app.worker.run")
            self.assertTrue(hotspots["hotspots"])
            self.assertEqual(read_order["read_order"][0]["id"], "function:app.main.main")
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_filters_budget_hub_suppression_and_query_validation(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            filtered = query_project_graph(
                graph,
                {
                    "query": "search",
                    "text": "run",
                    "node_types": ["function"],
                    "path_prefixes": ["app/"],
                    "confidence": ["verified"],
                    "max_results": 1,
                    "max_tokens": 300,
                },
            )
            hub = query_project_graph(
                graph,
                {"query": "neighbors", "node_id": next(node["id"] for node in graph["nodes"] if node["type"] == "workspace"), "hub_threshold": 1},
            )
            blocked = query_project_graph(graph, {"query": "search", "text": "x" * 200})

            self.assertEqual(filtered["status"], "ok")
            self.assertLessEqual(len(filtered["nodes"]), 1)
            self.assertTrue(filtered["budget"]["truncated"] or filtered["budget"]["omitted_count"] >= 0)
            self.assertEqual(hub["status"], "ok")
            self.assertIn("hub_suppressed", hub["budget"]["truncation_reasons"])
            self.assertEqual(blocked["status"], "blocked")
            self.assertIn("query:text_too_long", blocked["errors"])

    def test_query_budget_applies_after_query_specific_payloads_and_filter_values_are_validated(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-budget", "node_count": 60, "edge_count": 59, "observation_count": 0},
            "nodes": [
                {"id": f"function:module.fn{index}", "type": "function", "label": f"fn{index}", "status": "current", "language": "python", "path": f"module_{index}.py"}
                for index in range(60)
            ],
            "edges": [
                {
                    "id": f"edge:{index}",
                    "type": "calls",
                    "source": "function:module.fn0",
                    "target": f"function:module.fn{index}",
                    "confidence": "verified",
                    "status": "current",
                }
                for index in range(1, 60)
            ],
            "observations": [],
        }

        hotspots = query_project_graph(graph, {"query": "hotspots", "max_results": 60, "max_tokens": 500})
        invalid = query_project_graph(
            graph,
            {
                "query": "search",
                "text": "fn",
                "node_types": ["not_a_node_type"],
                "edge_types": ["not_an_edge_type"],
                "confidence": ["definitely"],
            },
        )

        self.assertLessEqual(len(json.dumps(hotspots, sort_keys=True)) // 4, 500)
        self.assertLessEqual(hotspots["budget"]["estimated_tokens"], 500)
        self.assertTrue(hotspots["budget"]["truncated"])
        self.assertEqual(invalid["status"], "blocked")
        self.assertIn("query:node_types:unknown", invalid["errors"])
        self.assertIn("query:edge_types:unknown", invalid["errors"])
        self.assertIn("query:confidence:unknown", invalid["errors"])

    def test_trace_delta_impact_and_affected_tests_packets_are_deterministic(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            first = build_project_code_graph(workspace)
            (workspace / "app" / "old.py").write_text("def removed():\n    return 'gone'\n", encoding="utf-8")
            second = build_project_code_graph(workspace, previous_graph=first)

            trace = query_project_graph(
                second,
                {
                    "query": "trace",
                    "node_id": "function:tests.test_worker.test_run",
                    "target_id": "function:app.worker.run",
                    "max_depth": 5,
                },
            )
            impact = query_project_graph(second, {"query": "impact", "node_id": "function:app.worker.run", "max_results": 5})
            affected = query_project_graph(
                second,
                {"query": "affected_tests", "node_id": "function:app.worker.run", "max_results": 5},
            )
            changed = query_project_graph(second, {"query": "changed_since", "max_results": 5})
            why = query_project_graph(second, {"query": "why_changed", "node_id": "file:app/old.py", "max_results": 5})

            self.assertEqual(trace["status"], "ok")
            self.assertTrue(trace["trace"])
            self.assertTrue(any(item["id"] == "function:app.main.main" for item in impact["nodes"]))
            self.assertTrue(any(item["id"] == "function:tests.test_worker.test_run" for item in affected["tests"]))
            self.assertEqual(changed["temporal_delta"]["status"], "changed")
            self.assertTrue(changed["temporal_delta"]["new_edges"])
            self.assertEqual(why["status"], "ok")
            self.assertIn("added", why["change_reasons"])

    def test_load_graph_artifact_accepts_json_and_jsonl_without_source_reads(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            graph_path = Path(tmp) / "graph.json"
            jsonl_path = Path(tmp) / "graph.jsonl"
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            jsonl_path.write_text(
                "\n".join(
                    json.dumps({"record_kind": record_kind, "payload": payload}, sort_keys=True)
                    for record_kind, payloads in [
                        ("metadata", [graph["metadata"]]),
                        ("node", graph["nodes"]),
                        ("edge", graph["edges"]),
                        ("observation", graph["observations"]),
                    ]
                    for payload in payloads
                ),
                encoding="utf-8",
            )

            self.assertEqual(load_graph_artifact(graph_path)["schema_version"], 1)
            self.assertEqual(load_graph_artifact(jsonl_path)["schema_version"], 1)

    def test_search_can_use_static_index_and_blocks_stale_index(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            static_index = build_static_search_index(graph)
            indexed = query_project_graph(
                graph,
                {"query": "search", "text": "worker run", "max_results": 5},
                static_index=static_index,
            )
            stale_graph = {
                **graph,
                "metadata": {
                    **graph["metadata"],
                    "scan_id": "scan-stale",
                    "node_count": graph["metadata"]["node_count"] + 1,
                },
            }
            stale = query_project_graph(
                stale_graph,
                {"query": "search", "text": "worker run", "max_results": 5},
                static_index=static_index,
            )

            self.assertEqual(indexed["status"], "ok")
            self.assertEqual(indexed["search_backend"], "static_index")
            self.assertEqual(indexed["nodes"][0]["id"], "function:app.worker.run")
            self.assertEqual(stale["status"], "blocked")
            self.assertIn("static_index:stale", stale["errors"])

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
