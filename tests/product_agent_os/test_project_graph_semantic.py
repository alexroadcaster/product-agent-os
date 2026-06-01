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
from product_agent_os.project_graph_semantic import (  # noqa: E402
    SEMANTIC_RETRIEVAL_TARGET,
    build_semantic_retrieval_index,
    disable_semantic_retrieval_index,
    evaluate_semantic_retrieval_quality,
    query_semantic_retrieval,
    stage_semantic_retrieval_index,
    validate_semantic_retrieval_approval,
    validate_semantic_retrieval_index,
)


class ProjectGraphSemanticRetrievalTest(unittest.TestCase):
    def test_semantic_retrieval_requires_explicit_approval_packet(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            missing = build_semantic_retrieval_index(graph, approval=None)
            approved = build_semantic_retrieval_index(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._semantic_approval(),
            )

            self.assertEqual(missing["status"], "approval_required")
            self.assertIn("semantic_approval:missing", missing["validation"]["errors"])
            self.assertTrue(validate_semantic_retrieval_approval(self._semantic_approval())["ok"])
            self.assertEqual(approved["artifact_kind"], "project_graph_semantic_retrieval_index")
            self.assertEqual(approved["approval_boundary"], "batch21_explicit_semantic_retrieval_gate")
            self.assertEqual(approved["model_decision"]["embedding_provider"], "local_deterministic")
            self.assertEqual(approved["model_decision"]["cross_encoder_provider"], "local_deterministic")
            self.assertTrue(approved["model_decision"]["external_model_calls_allowed"] is False)

    def test_semantic_corpus_embeddings_are_redacted_generated_cache_from_graph_only(self):
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

            semantic_index = build_semantic_retrieval_index(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._semantic_approval(),
            )
            serialized = json.dumps(semantic_index, sort_keys=True).lower()
            worker_record = next(
                record
                for record in semantic_index["corpus_records"]
                if record["node_id"] == "function:app.worker.run"
            )

            self.assertTrue(validate_semantic_retrieval_index(semantic_index)["ok"])
            self.assertEqual(semantic_index["write_policy"], "read_only")
            self.assertEqual(
                semantic_index["source_boundary"],
                "graph_and_static_index_artifacts_only_redacted_corpus_raw_source_excluded",
            )
            self.assertEqual(
                semantic_index["generated_view_policy"],
                "semantic_retrieval_index_is_generated_cache_not_source_of_truth",
            )
            self.assertIn("obs:", worker_record["observation_ids"][0])
            self.assertEqual(len(worker_record["embedding"]), semantic_index["embedding"]["dimension"])
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn("fixture-secret", serialized)
            self.assertNotIn("c:\\users\\person", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)

    def test_semantic_query_uses_local_embeddings_and_cross_encoder_rerank_without_completion_claims(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            semantic_index = build_semantic_retrieval_index(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._semantic_approval(),
            )

            packet = query_semantic_retrieval(
                semantic_index,
                {
                    "query": "search",
                    "text": "worker run",
                    "node_types": ["function"],
                    "path_prefixes": ["app/"],
                    "max_results": 3,
                    "max_tokens": 900,
                },
                graph=graph,
            )
            serialized = json.dumps(packet, sort_keys=True)

            self.assertEqual(packet["status"], "ok")
            self.assertEqual(packet["search_backend"], "semantic_retrieval")
            self.assertEqual(packet["reranker"], "local_cross_encoder_eval_only")
            self.assertEqual(packet["nodes"][0]["id"], "function:app.worker.run")
            self.assertEqual(packet["nodes"][0]["confidence"], "present_unverified")
            self.assertIn("semantic matches alone", packet["safe_next_action"])
            self.assertLessEqual(packet["budget"]["estimated_tokens"], 900)
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace), serialized)

    def test_semantic_stage_records_cache_invalidation_and_disable_path(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")

            first = stage_semantic_retrieval_index(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._semantic_approval(),
            )
            second = stage_semantic_retrieval_index(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._semantic_approval(),
            )
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
            third = stage_semantic_retrieval_index(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._semantic_approval(),
            )
            disabled = disable_semantic_retrieval_index(stage_root, workspace=workspace)

            target = stage_root / SEMANTIC_RETRIEVAL_TARGET
            backup = target.with_name("project-code-graph-semantic-index.previous.json")
            self.assertEqual(first["rendered_artifacts"]["cache_status"], "miss")
            self.assertEqual(second["rendered_artifacts"]["cache_status"], "hit")
            self.assertEqual(second["rendered_artifacts"]["files"][0]["action"], "leave_unchanged")
            self.assertEqual(third["rendered_artifacts"]["cache_status"], "miss_invalidated")
            self.assertTrue(backup.exists())
            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse(target.exists())

    def test_semantic_eval_blocks_stale_or_low_quality_results_against_thresholds(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            semantic_index = build_semantic_retrieval_index(
                graph,
                static_index=build_static_search_index(graph),
                approval=self._semantic_approval(),
            )

            passed = evaluate_semantic_retrieval_quality(
                semantic_index,
                graph=graph,
                cases=[
                    {
                        "id": "semantic-worker",
                        "text": "worker run",
                        "expected_node_ids": ["function:app.worker.run"],
                        "unexpected_node_ids": ["function:tests.test_worker.test_run"],
                        "top_k": 3,
                    }
                ],
                thresholds={
                    "min_recall_at_k": 1.0,
                    "min_mrr": 1.0,
                    "min_cross_encoder_mrr_delta": 0.0,
                    "max_false_positive_rate": 0.0,
                    "max_query_ms": 250,
                    "max_payload_tokens": 1200,
                },
            )
            stale_graph = {**graph, "nodes": [*graph["nodes"], {"id": "file:changed.py", "type": "module"}]}
            stale = query_semantic_retrieval(
                semantic_index,
                {"query": "search", "text": "worker run"},
                graph=stale_graph,
            )

            self.assertEqual(passed["decision_status"], "passed")
            self.assertEqual(passed["failed_thresholds"], [])
            self.assertEqual(passed["quality_metrics"]["recall_at_k"], 1.0)
            self.assertEqual(passed["quality_metrics"]["mrr"], 1.0)
            self.assertEqual(stale["status"], "blocked")
            self.assertIn("semantic_index:stale", stale["errors"])

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
