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
from product_agent_os.project_graph_live_governance import build_live_governance_packet  # noqa: E402
from product_agent_os.project_graph_semantic import build_semantic_retrieval_index  # noqa: E402
from product_agent_os.project_graph_embedding_provider import (  # noqa: E402
    EMBEDDING_PROVIDER_CACHE_TARGET,
    EMBEDDING_PROVIDER_TARGET,
    build_embedding_provider_gate,
    disable_embedding_provider_gate,
    evaluate_embedding_provider_baseline,
    stage_embedding_provider_gate,
    validate_embedding_provider_approval,
    validate_embedding_provider_gate,
)


class ProjectGraphEmbeddingProviderTest(unittest.TestCase):
    def test_provider_gate_requires_batch24_governance_redaction_cache_and_budget(self):
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        semantic_index = self._semantic_index(graph)

        missing = build_embedding_provider_gate(
            graph,
            semantic_index=semantic_index,
            approval=None,
            governance_packet=None,
        )
        gate = build_embedding_provider_gate(
            graph,
            semantic_index=semantic_index,
            approval=self._embedding_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        malformed = self._embedding_provider_approval()
        malformed["allowed_surfaces"].append("canonical_graph_mutation")
        malformed_result = validate_embedding_provider_approval(malformed, self._governance_packet())

        self.assertEqual(missing["status"], "approval_required")
        self.assertIn("embedding_provider_approval:missing", missing["validation"]["errors"])
        self.assertFalse(malformed_result["ok"])
        self.assertIn(
            "embedding_provider_approval:allowed_surfaces:canonical_graph_mutation",
            malformed_result["errors"],
        )
        self.assertEqual(gate["artifact_kind"], "project_graph_external_embedding_provider_gate")
        self.assertEqual(gate["approval_boundary"], "batch26_external_embedding_provider_gate_and_eval")
        self.assertEqual(gate["provider_policy"]["provider"], "external_embedding")
        self.assertEqual(gate["provider_policy"]["credential_source"], "environment")
        self.assertFalse(gate["provider_policy"]["provider_call_allowed"])
        self.assertFalse(gate["provider_policy"]["external_call_performed"])
        self.assertEqual(gate["status"], "ready")
        self.assertTrue(validate_embedding_provider_gate(gate)["ok"])

    def test_provider_payload_is_redacted_and_source_free_before_any_external_call(self):
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        graph["nodes"].append(
            {
                "id": "file:unsafe.py",
                "type": "module",
                "label": "TOKEN=sk-test-secret C:\\Users\\person\\private.py",
                "status": "current",
                "language": "python",
                "path": "C:\\Users\\person\\private.py",
                "observation_ids": ["obs:unsafe"],
            }
        )
        semantic_index = self._semantic_index(graph)

        gate = build_embedding_provider_gate(
            graph,
            semantic_index=semantic_index,
            approval=self._embedding_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        serialized = json.dumps(gate, sort_keys=True).lower()

        self.assertTrue(validate_embedding_provider_gate(gate)["ok"])
        self.assertEqual(gate["source_boundary"], "redacted_graph_and_semantic_index_only_no_raw_source")
        self.assertEqual(gate["redaction_policy"]["raw_source_excluded"], True)
        self.assertEqual(gate["cache_policy"]["stale_policy"], "block_if_graph_or_semantic_or_policy_fingerprint_mismatch")
        self.assertEqual(gate["budget_policy"]["max_cost_units"], 0)
        self.assertNotIn("return 'ok'", serialized)
        self.assertNotIn("sk-test-secret", serialized)
        self.assertNotIn("c:\\users\\person", serialized)

    def test_embedding_eval_must_beat_threshold_or_remain_disabled_with_fallback(self):
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        semantic_index = self._semantic_index(graph)
        gate = build_embedding_provider_gate(
            graph,
            semantic_index=semantic_index,
            approval=self._embedding_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        cases = [
            {
                "id": "provider-worker",
                "text": "worker run",
                "expected_node_ids": ["function:app.worker.run"],
                "unexpected_node_ids": ["function:tests.test_worker.test_run"],
                "top_k": 3,
            }
        ]

        missing_provider = evaluate_embedding_provider_baseline(
            gate,
            semantic_index=semantic_index,
            graph=graph,
            cases=cases,
            provider_results=None,
        )
        passed_provider = evaluate_embedding_provider_baseline(
            gate,
            semantic_index=semantic_index,
            graph=graph,
            cases=cases,
            provider_results={
                "provider-worker": {
                    "result_node_ids": ["function:app.worker.run"],
                    "query_ms": 120,
                    "payload_tokens": 500,
                }
            },
        )

        self.assertEqual(missing_provider["decision_status"], "disabled_fallback")
        self.assertFalse(missing_provider["provider_enabled"])
        self.assertIn("provider_eval:missing", missing_provider["failed_thresholds"])
        self.assertEqual(missing_provider["fallback"], "semantic_retrieval_or_graph_only")
        self.assertEqual(passed_provider["decision_status"], "passed")
        self.assertFalse(passed_provider["provider_enabled_by_default"])
        self.assertFalse(passed_provider["external_call_performed"])
        self.assertEqual(passed_provider["provider_quality_metrics"]["recall_at_k"], 1.0)
        self.assertEqual(passed_provider["baseline_quality_metrics"]["recall_at_k"], 1.0)

    def test_stage_disable_provider_gate_are_stage_root_only_and_keep_semantic_fallback(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            semantic_path = Path(tmp) / "semantic.json"
            governance_path = Path(tmp) / "governance.json"
            graph = build_project_code_graph(workspace)
            semantic_index = self._semantic_index(graph)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            semantic_path.write_text(json.dumps(semantic_index), encoding="utf-8")
            governance_path.write_text(json.dumps(self._governance_packet()), encoding="utf-8")

            result = stage_embedding_provider_gate(
                graph_path,
                semantic_path,
                stage_root,
                workspace=workspace,
                approval=self._embedding_provider_approval(),
                governance_artifact=governance_path,
            )
            target = stage_root / EMBEDDING_PROVIDER_TARGET
            cache = stage_root / EMBEDDING_PROVIDER_CACHE_TARGET

            self.assertEqual(result["rendered_artifacts"]["status"], "ready")
            self.assertEqual(result["rendered_artifacts"]["mode"], "validate-embedding-provider")
            self.assertTrue(target.exists())
            self.assertFalse(cache.exists())

            disabled = disable_embedding_provider_gate(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(disabled["rendered_artifacts"]["fallback"], "semantic_retrieval_or_graph_only")
            self.assertFalse(target.exists())
            self.assertIn(EMBEDDING_PROVIDER_TARGET, disabled["rendered_artifacts"]["deletion_proof"]["targets_checked"])

            with self.assertRaises(ValueError):
                stage_embedding_provider_gate(
                    graph_path,
                    semantic_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._embedding_provider_approval(),
                    governance_artifact=governance_path,
                )

    def _write_workspace(self, workspace: Path) -> Path:
        (workspace / "app").mkdir(parents=True)
        (workspace / "tests").mkdir()
        (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
        (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        (workspace / "tests" / "test_worker.py").write_text(
            "from app.worker import run\n\n"
            "def test_run():\n"
            "    assert run() == 'ok'\n",
            encoding="utf-8",
        )
        return workspace

    def _semantic_index(self, graph: dict) -> dict:
        return build_semantic_retrieval_index(
            graph,
            static_index=build_static_search_index(graph),
            approval={
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
            },
        )

    def _governance_packet(self) -> dict:
        return build_live_governance_packet(
            {
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
        )

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

    def _tmp(self) -> str:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return tmp.name


if __name__ == "__main__":
    unittest.main()
