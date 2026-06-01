import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_search_quality import evaluate_project_graph_search_quality  # noqa: E402


class ProjectGraphSearchQualityTest(unittest.TestCase):
    def test_search_quality_loop_records_thresholds_metrics_and_source_free_cases(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            packet = evaluate_project_graph_search_quality(
                graph,
                cases=[
                    {
                        "id": "symbol-worker",
                        "query": "search",
                        "text": "app.worker.run",
                        "expected_node_ids": ["function:app.worker.run"],
                        "top_k": 3,
                    },
                    {
                        "id": "trace-test-to-worker",
                        "query": "trace",
                        "source_id": "function:tests.test_worker.test_run",
                        "target_id": "function:app.worker.run",
                        "expected_status": "ok",
                    },
                    {
                        "id": "affected-tests-worker",
                        "query": "affected_tests",
                        "node_id": "function:app.worker.run",
                        "expected_test_ids": [
                            "file:tests/test_worker.py",
                            "function:tests.test_worker.test_run",
                        ],
                    },
                ],
                thresholds={
                    "min_symbol_recall": 1.0,
                    "min_top_k_mrr": 1.0,
                    "min_trace_success_rate": 1.0,
                    "min_affected_test_precision": 1.0,
                    "max_edge_density": 4.0,
                },
            )

            serialized = json.dumps(packet, sort_keys=True)
            self.assertEqual(packet["schema_version"], 1)
            self.assertEqual(packet["write_policy"], "read_only")
            self.assertEqual(packet["decision_status"], "passed")
            self.assertEqual(packet["approval_boundary"], "local_fixture_only_no_live_backend_or_model_calls")
            self.assertEqual(packet["quality_metrics"]["symbol_recall"], 1.0)
            self.assertEqual(packet["quality_metrics"]["top_k_mrr"], 1.0)
            self.assertEqual(packet["quality_metrics"]["trace_success_rate"], 1.0)
            self.assertEqual(packet["quality_metrics"]["affected_test_precision"], 1.0)
            self.assertLessEqual(packet["quality_metrics"]["edge_density"], 4.0)
            self.assertTrue(packet["thresholds"]["explicit_thresholds_required_before_closure"])
            self.assertTrue(all(case["status"] == "passed" for case in packet["cases"]))
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_search_quality_loop_labels_trace_failures_and_blocks_closure(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            packet = evaluate_project_graph_search_quality(
                graph,
                cases=[
                    {
                        "id": "missing-trace",
                        "query": "trace",
                        "source_id": "function:tests.test_worker.test_run",
                        "target_id": "function:app.worker.missing",
                        "expected_status": "ok",
                    }
                ],
                thresholds={"min_trace_success_rate": 1.0},
            )

            self.assertEqual(packet["decision_status"], "blocked")
            self.assertIn("trace_success_rate_below_threshold", packet["failed_thresholds"])
            self.assertEqual(packet["cases"][0]["trace_label"], "not_found")
            self.assertEqual(packet["cases"][0]["status"], "failed")

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
