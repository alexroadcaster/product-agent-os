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
from product_agent_os.project_graph_llm_extraction import (  # noqa: E402
    LLM_EXTRACTION_TARGET,
    apply_llm_proposal_review,
    build_llm_extraction_proposals,
    disable_llm_extraction_proposals,
    evaluate_llm_extraction_proposals,
    stage_llm_extraction_proposals,
    validate_llm_extraction_approval,
    validate_llm_extraction_proposals,
)
from product_agent_os.project_graph_semantic import build_semantic_retrieval_index  # noqa: E402


class ProjectGraphLlmExtractionTest(unittest.TestCase):
    def test_llm_extraction_requires_explicit_approval_packet_and_records_prompt_policy(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)

            missing = build_llm_extraction_proposals(graph, approval=None)
            approved = build_llm_extraction_proposals(
                graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )

            self.assertEqual(missing["status"], "approval_required")
            self.assertIn("llm_extraction_approval:missing", missing["validation"]["errors"])
            self.assertTrue(validate_llm_extraction_approval(self._llm_approval())["ok"])
            self.assertEqual(approved["artifact_kind"], "project_graph_llm_extraction_proposals")
            self.assertEqual(approved["approval_boundary"], "batch22_explicit_llm_semantic_extraction_gate")
            self.assertEqual(approved["model_policy"]["provider"], "local_deterministic")
            self.assertFalse(approved["model_policy"]["external_model_calls_allowed"])
            self.assertEqual(approved["prompt_contract"]["output_format"], "structured_json")
            self.assertIn("unsupported_claim", approved["prompt_contract"]["required_labels"])

    def test_generated_semantic_nodes_edges_are_staged_proposals_not_canonical_graph_facts(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            original_edges = list(graph["edges"])
            proposals = build_llm_extraction_proposals(
                graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )
            serialized = json.dumps(proposals, sort_keys=True).lower()

            self.assertTrue(validate_llm_extraction_proposals(proposals)["ok"])
            self.assertEqual(graph["edges"], original_edges)
            self.assertEqual(proposals["generated_view_policy"], "llm_extraction_proposals_are_generated_not_source_of_truth")
            self.assertEqual(proposals["canonical_graph_mutation"], "forbidden")
            self.assertTrue(proposals["semantic_node_proposals"])
            self.assertTrue(proposals["semantic_edge_proposals"])
            node = proposals["semantic_node_proposals"][0]
            edge = proposals["semantic_edge_proposals"][0]
            self.assertEqual(node["review_status"], "proposed")
            self.assertEqual(edge["review_status"], "proposed")
            self.assertEqual(node["confidence"], "inferred_unverified")
            self.assertIn("source_observation_ids", node)
            self.assertIn("rationale", node)
            self.assertNotIn("return 'ok'", serialized)
            self.assertNotIn(str(workspace).lower(), serialized)

    def test_rationale_and_comment_proposals_redact_private_inputs_and_block_unsupported_claims(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            graph["nodes"].append(
                {
                    "id": "file:unsafe.py",
                    "type": "module",
                    "label": "comment says TOKEN=fixture-secret in C:\\Users\\person\\private.py",
                    "status": "current",
                    "language": "python",
                    "path": "C:\\Users\\person\\private.py",
                    "observation_ids": ["obs:unsafe"],
                }
            )

            proposals = build_llm_extraction_proposals(
                graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )
            serialized = json.dumps(proposals, sort_keys=True).lower()

            self.assertTrue(proposals["rationale_comment_proposals"])
            self.assertTrue(proposals["blocked_records"])
            self.assertIn("private_or_secret_like_input", proposals["blocked_records"][0]["reason"])
            self.assertNotIn("fixture-secret", serialized)
            self.assertNotIn("c:\\users\\person", serialized)
            for proposal in proposals["rationale_comment_proposals"]:
                self.assertEqual(proposal["truth_status"], "unverified_inference")
                self.assertEqual(proposal["source_boundary"], "approved_redacted_spans_only")

    def test_human_review_accept_reject_gap_and_incident_workflow_are_staged_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            proposals = build_llm_extraction_proposals(
                graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )
            proposal_id = proposals["semantic_node_proposals"][0]["proposal_id"]

            accepted = apply_llm_proposal_review(
                proposals,
                proposal_id=proposal_id,
                decision="accepted_gap",
                owner="product-agent-owner",
                rationale="Owner accepts as advisory orientation only.",
            )
            unsafe = {**proposals, "rationale_comment_proposals": [{"summary": "unsupported source of truth"}]}
            incident = evaluate_llm_extraction_proposals(
                unsafe,
                cases=[{"id": "unsafe", "expected_proposal_kinds": ["semantic_node"]}],
                thresholds={"min_precision": 1.0, "max_unsupported_claim_rate": 0.0, "max_privacy_violations": 0},
            )

            reviewed = next(item for item in accepted["review_ledger"] if item["proposal_id"] == proposal_id)
            self.assertEqual(reviewed["decision"], "accepted_gap")
            self.assertEqual(reviewed["owner"], "product-agent-owner")
            self.assertEqual(accepted["canonical_graph_mutation"], "forbidden")
            self.assertEqual(incident["decision_status"], "blocked")
            self.assertEqual(incident["incident_workflow"]["status"], "disabled_until_fixed")

    def test_stage_records_cache_invalidation_and_disable_path(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            semantic_path = Path(tmp) / "semantic.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            semantic_path.write_text(json.dumps(self._semantic_index(graph)), encoding="utf-8")

            first = stage_llm_extraction_proposals(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._llm_approval(),
                semantic_index_artifact=semantic_path,
            )
            second = stage_llm_extraction_proposals(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._llm_approval(),
                semantic_index_artifact=semantic_path,
            )
            graph["nodes"].append(
                {
                    "id": "function:app.extra.explain",
                    "type": "function",
                    "label": "explain",
                    "status": "current",
                    "language": "python",
                    "path": "app/extra.py",
                    "observation_ids": ["obs:extra"],
                }
            )
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            third = stage_llm_extraction_proposals(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._llm_approval(),
                semantic_index_artifact=semantic_path,
            )
            disabled = disable_llm_extraction_proposals(stage_root, workspace=workspace)

            target = stage_root / LLM_EXTRACTION_TARGET
            backup = target.with_name("project-code-graph-llm-proposals.previous.json")
            self.assertEqual(first["rendered_artifacts"]["cache_status"], "miss")
            self.assertEqual(second["rendered_artifacts"]["cache_status"], "hit")
            self.assertEqual(third["rendered_artifacts"]["cache_status"], "miss_invalidated")
            self.assertTrue(backup.exists())
            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse(target.exists())

    def test_llm_extraction_eval_blocks_hallucination_privacy_and_stale_context(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            proposals = build_llm_extraction_proposals(
                graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )

            passed = evaluate_llm_extraction_proposals(
                proposals,
                cases=[
                    {
                        "id": "worker-proposal",
                        "expected_proposal_kinds": ["semantic_node", "semantic_edge", "rationale_comment"],
                        "expected_source_node_ids": ["function:app.worker.run"],
                    }
                ],
                thresholds={
                    "min_precision": 1.0,
                    "max_unsupported_claim_rate": 0.0,
                    "max_privacy_violations": 0,
                    "max_cost_units": 0,
                    "max_latency_ms": 250,
                },
            )
            stale_graph = {**graph, "nodes": [*graph["nodes"], {"id": "file:changed.py", "type": "module"}]}
            stale = build_llm_extraction_proposals(
                stale_graph,
                semantic_index=self._semantic_index(graph),
                approval=self._llm_approval(),
            )

            self.assertEqual(passed["decision_status"], "passed")
            self.assertEqual(passed["failed_thresholds"], [])
            self.assertEqual(passed["quality_metrics"]["precision"], 1.0)
            self.assertEqual(stale["status"], "blocked")
            self.assertIn("semantic_index:stale", stale["validation"]["errors"])

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
            "def test_run():\n    assert run() == 'ok'\n",
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
