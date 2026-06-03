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
from product_agent_os.project_graph_llm_extraction import (  # noqa: E402
    LLM_EXTRACTION_TARGET,
    build_llm_extraction_proposals,
)
from product_agent_os.project_graph_llm_proposal_provider import (  # noqa: E402
    LLM_PROPOSAL_EVAL_TARGET,
    LLM_PROPOSAL_PROVIDER_TARGET,
    build_llm_proposal_provider_gate,
    disable_llm_proposal_provider_gate,
    evaluate_llm_proposal_safety,
    stage_llm_proposal_provider_gate,
    validate_llm_proposal_provider_approval,
    validate_llm_proposal_provider_gate,
)
from product_agent_os.project_graph_semantic import build_semantic_retrieval_index  # noqa: E402


class ProjectGraphLlmProposalProviderTest(unittest.TestCase):
    def test_llm_provider_gate_requires_governance_prompt_schema_redaction_and_budget(self):
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        semantic_index = self._semantic_index(graph)
        local_proposals = self._local_proposals(graph, semantic_index)

        missing = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=local_proposals,
            approval=None,
            governance_packet=None,
        )
        gate = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=local_proposals,
            approval=self._llm_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        malformed = self._llm_provider_approval()
        malformed["allowed_surfaces"].append("canonical_graph_mutation")
        malformed_result = validate_llm_proposal_provider_approval(malformed, self._governance_packet())

        self.assertEqual(missing["status"], "approval_required")
        self.assertIn("llm_proposal_provider_approval:missing", missing["validation"]["errors"])
        self.assertFalse(malformed_result["ok"])
        self.assertIn(
            "llm_proposal_provider_approval:allowed_surfaces:canonical_graph_mutation",
            malformed_result["errors"],
        )
        self.assertEqual(gate["artifact_kind"], "project_graph_live_llm_proposal_provider_gate")
        self.assertEqual(gate["approval_boundary"], "batch28_live_llm_proposal_adapter_and_safety_eval")
        self.assertEqual(gate["provider_policy"]["provider"], "external_llm")
        self.assertEqual(gate["provider_policy"]["credential_source"], "environment")
        self.assertFalse(gate["provider_policy"]["provider_call_allowed"])
        self.assertFalse(gate["provider_policy"]["external_call_performed"])
        self.assertEqual(gate["prompt_contract"]["output_format"], "structured_json")
        self.assertTrue(gate["prompt_contract"]["proposal_only"])
        self.assertEqual(gate["canonical_graph_mutation"], "forbidden")
        self.assertEqual(gate["fallback"], "local_llm_proposals_or_semantic_retrieval_or_graph_only")
        self.assertTrue(validate_llm_proposal_provider_gate(gate)["ok"])

    def test_llm_provider_payload_is_source_free_proposal_only_and_never_canonical(self):
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
        gate = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=self._local_proposals(graph, semantic_index),
            approval=self._llm_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        serialized = json.dumps(gate, sort_keys=True).lower()

        self.assertTrue(validate_llm_proposal_provider_gate(gate)["ok"])
        self.assertEqual(gate["source_boundary"], "redacted_prompt_schema_and_evidence_ids_only_no_raw_source")
        self.assertIn("raw_source_bodies", gate["data_classification"]["forbidden_inputs"])
        self.assertTrue(gate["redaction_policy"]["unsupported_claims_labelled"])
        self.assertEqual(gate["cache_policy"]["cache_target"], LLM_PROPOSAL_EVAL_TARGET)
        self.assertEqual(gate["budget_policy"]["max_cost_units"], 0)
        self.assertIn("unsupported_claim", gate["prompt_contract"]["required_labels"])
        self.assertIn("canonical_graph_mutation", gate["blocked_surfaces"])
        self.assertNotIn("return 'ok'", serialized)
        self.assertNotIn("sk-test-secret", serialized)
        self.assertNotIn("c:\\users\\person", serialized)

    def test_llm_safety_eval_blocks_unsafe_hallucinated_or_stale_outputs(self):
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        semantic_index = self._semantic_index(graph)
        gate = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=self._local_proposals(graph, semantic_index),
            approval=self._llm_provider_approval(),
            governance_packet=self._governance_packet(),
        )
        cases = self._llm_eval_cases()

        missing = evaluate_llm_proposal_safety(
            gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=cases,
            provider_results=None,
        )
        unsafe = evaluate_llm_proposal_safety(
            gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=cases,
            provider_results={
                "worker-proposal": {
                    "graph_fingerprint": "stale",
                    "proposals": [
                        {
                            "proposal_id": "unsafe",
                            "proposal_kind": "semantic_node",
                            "source_node_id": "function:not.real",
                            "source_observation_ids": [],
                            "rationale": "Use sk-test-secret from C:\\Users\\person\\private.py",
                            "unsupported_claim_labels": [],
                            "canonical_graph_mutation": "allowed",
                        }
                    ],
                    "query_ms": 300,
                    "payload_tokens": 1500,
                }
            },
        )
        safe = evaluate_llm_proposal_safety(
            gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=cases,
            provider_results={
                "worker-proposal": {
                    "graph_fingerprint": gate["graph_fingerprint"],
                    "proposals": [
                        {
                            "proposal_id": "provider-semantic-node-worker",
                            "proposal_kind": "semantic_node",
                            "source_node_id": "function:app.worker.run",
                            "source_observation_ids": ["obs:function:app.worker.run"],
                            "rationale": "Generated proposal from approved redacted graph evidence.",
                            "unsupported_claim_labels": [],
                            "review_status": "proposed",
                            "confidence": "inferred_unverified",
                            "canonical_graph_mutation": "forbidden",
                        },
                        {
                            "proposal_id": "provider-rationale-worker",
                            "proposal_kind": "rationale_comment",
                            "source_node_id": "function:app.worker.run",
                            "source_observation_ids": ["obs:function:app.worker.run"],
                            "rationale": "Rationale is tied to approved source evidence id.",
                            "unsupported_claim_labels": [],
                            "review_status": "proposed",
                            "confidence": "inferred_unverified",
                            "canonical_graph_mutation": "forbidden",
                        },
                    ],
                    "query_ms": 100,
                    "payload_tokens": 400,
                }
            },
        )

        self.assertEqual(missing["decision_status"], "disabled_fallback")
        self.assertIn("llm_proposal_eval:missing", missing["failed_thresholds"])
        self.assertEqual(unsafe["decision_status"], "incident_blocked")
        self.assertIn("stale_context", unsafe["failed_thresholds"])
        self.assertIn("privacy_violation", unsafe["failed_thresholds"])
        self.assertIn("hallucinated_or_ungrounded_proposal", unsafe["failed_thresholds"])
        self.assertIn("canonical_graph_mutation_attempt", unsafe["failed_thresholds"])
        self.assertEqual(unsafe["incident_workflow"]["status"], "active")
        self.assertEqual(safe["decision_status"], "passed")
        self.assertFalse(safe["provider_enabled_by_default"])
        self.assertFalse(safe["external_call_performed"])
        self.assertEqual(safe["quality_metrics"]["grounded_proposal_rate"], 1.0)
        self.assertEqual(safe["accepted_for_canonical_graph"], False)
        self.assertEqual(safe["safe_next_action"], "Stage proposals for human review; never treat provider output as canonical fact.")

    def test_stage_disable_llm_provider_and_eval_artifacts_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            semantic_path = Path(tmp) / "semantic.json"
            proposals_path = Path(tmp) / "llm-proposals.json"
            governance_path = Path(tmp) / "governance.json"
            graph = build_project_code_graph(workspace)
            semantic_index = self._semantic_index(graph)
            local_proposals = self._local_proposals(graph, semantic_index)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            semantic_path.write_text(json.dumps(semantic_index), encoding="utf-8")
            proposals_path.write_text(json.dumps(local_proposals), encoding="utf-8")
            governance_path.write_text(json.dumps(self._governance_packet()), encoding="utf-8")

            staged = stage_llm_proposal_provider_gate(
                graph_path,
                semantic_path,
                proposals_path,
                stage_root,
                workspace=workspace,
                approval=self._llm_provider_approval(),
                governance_artifact=governance_path,
            )

            self.assertEqual(staged["rendered_artifacts"]["status"], "ready")
            self.assertTrue((stage_root / LLM_PROPOSAL_PROVIDER_TARGET).exists())
            self.assertTrue((stage_root / LLM_PROPOSAL_EVAL_TARGET).exists())

            disabled = disable_llm_proposal_provider_gate(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse((stage_root / LLM_PROPOSAL_PROVIDER_TARGET).exists())
            self.assertFalse((stage_root / LLM_PROPOSAL_EVAL_TARGET).exists())

            with self.assertRaises(ValueError):
                stage_llm_proposal_provider_gate(
                    graph_path,
                    semantic_path,
                    proposals_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._llm_provider_approval(),
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
            approval=self._semantic_approval(),
        )

    def _local_proposals(self, graph: dict, semantic_index: dict) -> dict:
        return build_llm_extraction_proposals(
            graph,
            semantic_index=semantic_index,
            approval=self._local_llm_approval(),
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
                            "provider": "external_llm",
                            "credential_source": "environment",
                            "env_var": "PRODUCT_AGENT_OS_LLM_API_KEY",
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
                "residual_risks": ["LLM provider drift remains blocked until safety eval passes"],
            }
        )

    def _llm_provider_approval(self) -> dict:
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

    def _local_llm_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": LLM_EXTRACTION_TARGET,
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
            "rollback_path": f"delete {LLM_EXTRACTION_TARGET}",
        }

    def _llm_eval_cases(self) -> list[dict]:
        return [
            {
                "id": "worker-proposal",
                "expected_proposal_kinds": ["semantic_node", "rationale_comment"],
                "expected_source_node_ids": ["function:app.worker.run"],
                "top_k": 2,
            }
        ]

    def _tmp(self) -> str:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return tmp.name


if __name__ == "__main__":
    unittest.main()
