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

    def test_query_validation_blocks_invalid_depth_and_unbounded_limits(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-limits", "node_count": 2, "edge_count": 1, "observation_count": 0},
            "nodes": [
                {"id": "function:app.main.main", "type": "function", "label": "main", "status": "current", "language": "python", "path": "app/main.py"},
                {"id": "function:app.worker.run", "type": "function", "label": "run", "status": "current", "language": "python", "path": "app/worker.py"},
            ],
            "edges": [
                {
                    "id": "edge:main-worker",
                    "type": "calls",
                    "source": "function:app.main.main",
                    "target": "function:app.worker.run",
                    "confidence": "verified",
                    "status": "current",
                }
            ],
            "observations": [],
        }

        invalid_depth = query_project_graph(
            graph,
            {
                "query": "path",
                "node_id": "function:app.main.main",
                "target_id": "function:app.worker.run",
                "max_depth": 0,
            },
        )
        excessive_depth = query_project_graph(
            graph,
            {
                "query": "path",
                "node_id": "function:app.main.main",
                "target_id": "function:app.worker.run",
                "max_depth": 10_000,
            },
        )
        excessive_budget = query_project_graph(
            graph,
            {
                "query": "neighbors",
                "node_id": "function:app.main.main",
                "max_results": 10_000,
                "max_tokens": 1_000_000,
            },
        )

        self.assertEqual(invalid_depth["status"], "blocked")
        self.assertIn("query:max_depth:invalid", invalid_depth["errors"])
        self.assertEqual(excessive_depth["status"], "blocked")
        self.assertIn("query:max_depth:too_large", excessive_depth["errors"])
        self.assertEqual(excessive_budget["status"], "blocked")
        self.assertIn("query:max_results:too_large", excessive_budget["errors"])
        self.assertIn("query:max_tokens:too_large", excessive_budget["errors"])

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

    def test_agent_reading_packet_is_bounded_source_first_and_not_readiness_proof(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            first = build_project_code_graph(workspace)
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'changed'\n", encoding="utf-8")
            graph = build_project_code_graph(workspace, previous_graph=first)

            packet = query_project_graph(
                graph,
                {
                    "query": "agent_reading_packet",
                    "node_id": "function:app.worker.run",
                    "max_depth": 3,
                    "max_results": 4,
                    "max_tokens": 1_200,
                },
            )
            serialized = json.dumps(packet, sort_keys=True).lower()

            self.assertEqual(packet["status"], "ok")
            self.assertEqual(packet["result_kind"], "agent_reading_packet")
            self.assertEqual(packet["write_policy"], "read_only")
            self.assertTrue(packet["source_read_required"])
            self.assertTrue(packet["must_read_source_before_edit"])
            self.assertEqual(packet["source_boundary"], "graph_artifact_only_raw_source_excluded")
            self.assertEqual(packet["generated_view_policy"], "graph_packets_are_orientation_evidence_only")
            self.assertEqual(packet["target_entity"]["id"], "function:app.worker.run")
            self.assertTrue(packet["related_entities"])
            self.assertEqual(packet["read_order"][0]["id"], "function:app.worker.run")
            self.assertTrue(packet["source_spans"])
            self.assertIn("verified_edges", packet["confidence_summary"])
            self.assertTrue(any(item["id"] == "function:tests.test_worker.test_run" for item in packet["affected_tests"]))
            self.assertIn(packet["stale_status"]["status"], {"fresh", "partial", "stale", "unknown"})
            self.assertIsInstance(packet["rejected_links"], list)
            self.assertIn("release_readiness", packet["unsupported_claims"])
            self.assertIn("read source", packet["safe_next_action"].lower())
            self.assertLessEqual(packet["budget"]["estimated_tokens"], 1_200)
            self.assertNotIn("return 'changed'", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)
            self.assertNotIn("production-ready", serialized)
            self.assertNotIn("release-ready", serialized)
            self.assertNotIn("verified complete", serialized)

    def test_status_and_agent_packet_surface_coverage_and_freshness_gates(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            first = build_project_code_graph(workspace)
            (workspace / "app" / "worker.py").write_text("def run():\n    return 'changed'\n", encoding="utf-8")
            graph = build_project_code_graph(workspace, previous_graph=first)

            status = query_project_graph(graph, {"query": "status", "max_results": 5})
            packet = query_project_graph(
                graph,
                {
                    "query": "agent_reading_packet",
                    "node_id": "function:app.worker.run",
                    "max_results": 5,
                    "max_tokens": 1_600,
                },
            )
            serialized = json.dumps([status, packet], sort_keys=True).lower()

            self.assertEqual(status["graph_status"]["freshness_status"]["status"], "stale")
            self.assertTrue(status["graph_status"]["freshness_status"]["blocks_action_claims"])
            self.assertEqual(status["graph_status"]["coverage_map"]["source_boundary"], "raw_source_bodies_excluded")
            self.assertIn("python", status["graph_status"]["coverage_map"]["by_language"])
            self.assertEqual(packet["freshness_status"]["status"], "stale")
            self.assertTrue(packet["freshness_status"]["blocks_action_claims"])
            self.assertTrue(packet["stale_status"]["blocks_action_claims"])
            self.assertIn("refresh", packet["safe_next_action"].lower())
            self.assertIn("read source", packet["safe_next_action"].lower())
            self.assertNotIn(str(workspace).lower(), serialized)
            self.assertNotIn("release-ready", serialized)
            self.assertNotIn("production-ready", serialized)

    def test_packets_surface_rejected_links_without_dependency_or_readiness_claims(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {
                "scan_id": "scan-rejected",
                "node_count": 2,
                "edge_count": 0,
                "observation_count": 0,
                "source_boundary": "raw_source_bodies_excluded",
                "generated_view_policy": "html_is_review_only",
                "rejected_links": [
                    {
                        "schema_version": 1,
                        "source": "function:web.apiClient.listUserSettings",
                        "target_candidate": "chunk:openapi.yaml:operation:listUsers",
                        "rule": "conservative_static_linker_exact_match_only",
                        "reason": "weak_name_similarity",
                        "confidence": "unsupported",
                        "status": "unsupported",
                        "source_read_required": True,
                        "future_parser_or_linker_task": "explicit_route_or_contract_mapping_required",
                    }
                ],
            },
            "nodes": [
                {
                    "id": "function:web.apiClient.listUserSettings",
                    "type": "function",
                    "label": "listUserSettings",
                    "status": "current",
                    "language": "typescript",
                    "path": "web/apiClient.ts",
                    "source_spans": [
                        {
                            "relative_path": "web/apiClient.ts",
                            "start_line": 1,
                            "end_line": 2,
                            "fingerprint": "sha256:" + "1" * 64,
                        }
                    ],
                },
                {
                    "id": "chunk:openapi.yaml:operation:listUsers",
                    "type": "contract",
                    "label": "listUsers",
                    "status": "current",
                    "language": "yaml",
                    "path": "openapi.yaml",
                },
            ],
            "edges": [],
            "observations": [],
        }

        packet = query_project_graph(
            graph,
            {"query": "agent_reading_packet", "node_id": "function:web.apiClient.listUserSettings", "max_results": 5},
        )
        status = query_project_graph(graph, {"query": "status", "max_results": 5})
        serialized = json.dumps([packet, status], sort_keys=True).lower()

        self.assertEqual(packet["rejected_links"][0]["target_candidate"], "chunk:openapi.yaml:operation:listUsers")
        self.assertEqual(packet["rejected_links"][0]["rule"], "conservative_static_linker_exact_match_only")
        self.assertTrue(packet["rejected_links"][0]["source_read_required"])
        self.assertEqual(status["graph_status"]["rejected_link_summary"]["total"], 1)
        self.assertEqual(status["graph_status"]["rejected_link_summary"]["by_reason"]["weak_name_similarity"], 1)
        self.assertNotIn("hidden dependency", serialized)
        self.assertNotIn("production-ready", serialized)
        self.assertNotIn("release-ready", serialized)

    def test_impact_and_affected_tests_respect_max_depth_for_reverse_reachability(self):
        graph = {
            "schema_version": 1,
            "write_policy": "read_only",
            "metadata": {"scan_id": "scan-depth", "node_count": 4, "edge_count": 3, "observation_count": 0},
            "nodes": [
                {"id": "function:tests.test_worker.test_run", "type": "function", "label": "test_run", "status": "current", "language": "python", "path": "tests/test_worker.py"},
                {"id": "function:app.api.handle", "type": "function", "label": "handle", "status": "current", "language": "python", "path": "app/api.py"},
                {"id": "function:app.service.run", "type": "function", "label": "run", "status": "current", "language": "python", "path": "app/service.py"},
                {"id": "function:app.worker.work", "type": "function", "label": "work", "status": "current", "language": "python", "path": "app/worker.py"},
            ],
            "edges": [
                {"id": "edge:test-api", "type": "calls", "source": "function:tests.test_worker.test_run", "target": "function:app.api.handle", "confidence": "verified", "status": "current"},
                {"id": "edge:api-service", "type": "calls", "source": "function:app.api.handle", "target": "function:app.service.run", "confidence": "verified", "status": "current"},
                {"id": "edge:service-worker", "type": "calls", "source": "function:app.service.run", "target": "function:app.worker.work", "confidence": "verified", "status": "current"},
            ],
            "observations": [],
        }

        shallow_impact = query_project_graph(
            graph,
            {"query": "impact", "node_id": "function:app.worker.work", "max_depth": 1, "max_results": 10},
        )
        shallow_tests = query_project_graph(
            graph,
            {"query": "affected_tests", "node_id": "function:app.worker.work", "max_depth": 2, "max_results": 10},
        )
        deep_tests = query_project_graph(
            graph,
            {"query": "affected_tests", "node_id": "function:app.worker.work", "max_depth": 3, "max_results": 10},
        )

        self.assertEqual([node["id"] for node in shallow_impact["nodes"]], ["function:app.service.run"])
        self.assertEqual(shallow_tests["tests"], [])
        self.assertEqual(deep_tests["tests"][0]["id"], "function:tests.test_worker.test_run")

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
