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
    evaluate_llm_proposal_safety,
)
from product_agent_os.project_graph_review_ledger import (  # noqa: E402
    PROPOSAL_DIFF_TARGET,
    REVIEW_LEDGER_TARGET,
    build_human_review_ledger,
    build_proposal_diff_preview,
    disable_review_ledger,
    stage_review_ledger,
    validate_human_review_ledger,
    validate_review_ledger_approval,
    validate_proposal_diff_preview,
)
from product_agent_os.project_graph_semantic import build_semantic_retrieval_index  # noqa: E402


class ProjectGraphReviewLedgerTest(unittest.TestCase):
    def test_review_ledger_requires_owner_decisions_and_keeps_acceptance_non_canonical(self):
        graph, semantic_index, proposals, governance, gate, safety_eval = self._batch29_inputs()
        first_proposal = self._first_proposal(proposals, "semantic_node")

        missing = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=gate,
            safety_eval=safety_eval,
            approval=None,
            governance_packet=governance,
            review_decisions=None,
        )
        invalid_decision = self._review_decisions(
            proposals,
            overrides={
                first_proposal["proposal_id"]: {
                    "decision": "accepted",
                    "decision_by": "",
                    "evidence_refs": first_proposal["source_observation_ids"],
                    "rationale": "Missing owner decision must not count as accepted.",
                }
            },
        )
        invalid = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=gate,
            safety_eval=safety_eval,
            approval=self._review_approval(),
            governance_packet=governance,
            review_decisions=invalid_decision,
        )
        ledger = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=gate,
            safety_eval=safety_eval,
            approval=self._review_approval(),
            governance_packet=governance,
            review_decisions=self._review_decisions(proposals),
        )

        self.assertEqual(missing["status"], "approval_required")
        self.assertIn("review_ledger_approval:missing", missing["validation"]["errors"])
        self.assertEqual(invalid["status"], "blocked")
        self.assertIn("review_decision:accepted:owner_decision", invalid["validation"]["errors"])
        self.assertEqual(ledger["artifact_kind"], "project_graph_human_review_ledger")
        self.assertEqual(ledger["approval_boundary"], "batch29_human_review_ledger_and_proposal_diff_preview")
        self.assertEqual(ledger["source_boundary"], "redacted_proposal_ids_and_evidence_refs_only_no_raw_source")
        self.assertTrue(ledger["review_policy"]["human_review_required"])
        self.assertIn("accepted_gap", ledger["review_policy"]["allowed_decisions"])
        self.assertFalse(ledger["provider_call_allowed"])
        self.assertFalse(ledger["external_call_performed"])
        self.assertFalse(ledger["accepted_for_canonical_graph"])
        self.assertEqual(ledger["canonical_graph_mutation"], "forbidden")
        self.assertGreaterEqual(ledger["decision_summary"]["accepted"], 1)
        self.assertGreaterEqual(ledger["decision_summary"]["rejected"], 1)
        self.assertGreaterEqual(ledger["decision_summary"]["accepted_gap"], 1)
        self.assertTrue(validate_review_ledger_approval(self._review_approval(), governance)["ok"])
        self.assertTrue(validate_human_review_ledger(ledger)["ok"], validate_human_review_ledger(ledger))
        self.assertIsNot(semantic_index, None)

    def test_proposal_diff_preview_is_inspectable_before_mutation_and_never_applies(self):
        graph, _semantic_index, proposals, governance, gate, safety_eval = self._batch29_inputs()
        ledger = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=gate,
            safety_eval=safety_eval,
            approval=self._review_approval(),
            governance_packet=governance,
            review_decisions=self._review_decisions(proposals),
        )

        diff = build_proposal_diff_preview(graph, local_proposals=proposals, review_ledger=ledger)
        payload = json.dumps(diff, sort_keys=True).lower()

        self.assertEqual(diff["artifact_kind"], "project_graph_proposal_diff_preview")
        self.assertEqual(diff["status"], "preview_ready")
        self.assertTrue(diff["human_can_inspect_before_mutation"])
        self.assertTrue(diff["mutation_plan_required_for_apply"])
        self.assertEqual(diff["canonical_graph_mutation"], "forbidden")
        self.assertFalse(diff["mutated_canonical_graph"])
        self.assertGreaterEqual(len(diff["diff"]["added_nodes"]), 1)
        self.assertGreaterEqual(len(diff["diff"]["added_edges"]), 1)
        self.assertGreaterEqual(len(diff["diff"]["rationale_comments"]), 1)
        self.assertNotIn("return 'ok'", payload)
        self.assertNotIn("c:\\users", payload)
        self.assertTrue(validate_proposal_diff_preview(diff, ledger)["ok"], validate_proposal_diff_preview(diff, ledger))

    def test_incident_safety_eval_blocks_review_acceptance(self):
        graph, semantic_index, proposals, governance, gate, _safety_eval = self._batch29_inputs()
        incident_eval = evaluate_llm_proposal_safety(
            gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=[
                {
                    "id": "worker-proposal",
                    "expected_proposal_kinds": ["semantic_node"],
                    "expected_source_node_ids": ["function:app.worker.run"],
                }
            ],
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
                            "canonical_graph_mutation": "allowed",
                        }
                    ],
                    "query_ms": 300,
                    "payload_tokens": 1500,
                }
            },
        )

        ledger = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=gate,
            safety_eval=incident_eval,
            approval=self._review_approval(),
            governance_packet=governance,
            review_decisions=self._review_decisions(proposals),
        )

        self.assertEqual(incident_eval["decision_status"], "incident_blocked")
        self.assertEqual(ledger["status"], "blocked")
        self.assertIn("llm_proposal_safety_eval:incident_blocked", ledger["validation"]["errors"])
        self.assertEqual(ledger["decision_summary"]["accepted"], 0)
        self.assertFalse(ledger["accepted_for_canonical_graph"])

    def test_stage_disable_review_ledger_and_diff_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph = build_project_code_graph(workspace)
            semantic_index = self._semantic_index(graph)
            proposals = self._local_proposals(graph, semantic_index)
            governance = self._governance_packet()
            gate = build_llm_proposal_provider_gate(
                graph,
                semantic_index=semantic_index,
                local_proposals=proposals,
                approval=self._llm_provider_approval(),
                governance_packet=governance,
            )
            safety_eval = evaluate_llm_proposal_safety(
                gate,
                graph=graph,
                semantic_index=semantic_index,
                cases=[],
                provider_results=None,
            )
            graph_path = Path(tmp) / "graph.json"
            proposals_path = Path(tmp) / "proposals.json"
            gate_path = Path(tmp) / "gate.json"
            eval_path = Path(tmp) / "eval.json"
            governance_path = Path(tmp) / "governance.json"
            decisions_path = Path(tmp) / "review-decisions.json"
            for path, payload in [
                (graph_path, graph),
                (proposals_path, proposals),
                (gate_path, gate),
                (eval_path, safety_eval),
                (governance_path, governance),
                (decisions_path, self._review_decisions(proposals)),
            ]:
                path.write_text(json.dumps(payload), encoding="utf-8")

            staged = stage_review_ledger(
                graph_path,
                proposals_path,
                gate_path,
                eval_path,
                stage_root,
                workspace=workspace,
                approval=self._review_approval(),
                governance_artifact=governance_path,
                review_decisions_artifact=decisions_path,
            )

            self.assertEqual(staged["rendered_artifacts"]["status"], "ready")
            self.assertTrue((stage_root / REVIEW_LEDGER_TARGET).exists())
            self.assertTrue((stage_root / PROPOSAL_DIFF_TARGET).exists())

            disabled = disable_review_ledger(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse((stage_root / REVIEW_LEDGER_TARGET).exists())
            self.assertFalse((stage_root / PROPOSAL_DIFF_TARGET).exists())

            with self.assertRaises(ValueError):
                stage_review_ledger(
                    graph_path,
                    proposals_path,
                    gate_path,
                    eval_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._review_approval(),
                    governance_artifact=governance_path,
                    review_decisions_artifact=decisions_path,
                )

    def _batch29_inputs(self) -> tuple[dict, dict, dict, dict, dict, dict]:
        graph = build_project_code_graph(self._write_workspace(Path(self._tmp()) / "workspace"))
        semantic_index = self._semantic_index(graph)
        proposals = self._local_proposals(graph, semantic_index)
        governance = self._governance_packet()
        gate = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=proposals,
            approval=self._llm_provider_approval(),
            governance_packet=governance,
        )
        safety_eval = evaluate_llm_proposal_safety(
            gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=[],
            provider_results=None,
        )
        return graph, semantic_index, proposals, governance, gate, safety_eval

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

    def _first_proposal(self, proposals: dict, kind: str) -> dict:
        for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
            for proposal in proposals.get(key, []):
                if proposal.get("proposal_kind") == kind:
                    return proposal
        self.fail(f"missing proposal kind {kind}")

    def _review_decisions(self, proposals: dict, *, overrides: dict[str, dict] | None = None) -> dict:
        decisions = []
        overrides = overrides or {}
        plan = [
            (self._proposal_by_kind(proposals, "semantic_node", index=0), "accepted"),
            (self._proposal_by_kind(proposals, "semantic_edge", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "rationale_comment", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "semantic_node", index=1), "rejected"),
        ]
        for proposal, decision in plan:
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
            record.update(overrides.get(proposal["proposal_id"], {}))
            decisions.append(record)
        return {"schema_version": 1, "owner": "Product-Agent OS Maintainer", "decisions": decisions}

    def _proposal_by_kind(self, proposals: dict, kind: str, *, index: int) -> dict:
        matches = []
        for key in ["semantic_node_proposals", "semantic_edge_proposals", "rationale_comment_proposals"]:
            for proposal in proposals.get(key, []):
                if proposal.get("proposal_kind") == kind:
                    matches.append(proposal)
        if len(matches) > index:
            return matches[index]
        return matches[0] if matches else self._first_proposal(proposals, kind)

    def _review_approval(self) -> dict:
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
            "rollback_path": f"delete {REVIEW_LEDGER_TARGET}",
            "residual_risks": ["accepted proposals still require Batch 30 dry-run before mutation"],
        }

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
                "residual_risks": ["Review decisions still need Batch 30 dry-run before mutation"],
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
                "storage_path": LLM_PROPOSAL_PROVIDER_TARGET,
                "cache_target": LLM_PROPOSAL_EVAL_TARGET,
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
            "rollback_path": f"delete {LLM_PROPOSAL_PROVIDER_TARGET}",
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

    def _tmp(self) -> str:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return tmp.name


if __name__ == "__main__":
    unittest.main()
