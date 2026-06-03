import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_canonical_mutation import (  # noqa: E402
    MUTATED_GRAPH_TARGET,
    MUTATION_JOURNAL_TARGET,
    MUTATION_PLAN_TARGET,
    ROLLBACK_PROOF_TARGET,
    apply_accepted_mutations_to_graph,
    build_canonical_mutation_plan,
    build_graph_rollback_proof,
    disable_canonical_graph_mutation,
    stage_canonical_graph_mutation,
    validate_canonical_mutation_approval,
    validate_canonical_mutation_plan,
    validate_graph_rollback_proof,
)
from product_agent_os.project_graph_index import build_static_search_index, graph_content_fingerprint  # noqa: E402
from product_agent_os.project_graph_live_governance import build_live_governance_packet  # noqa: E402
from product_agent_os.project_graph_llm_extraction import build_llm_extraction_proposals  # noqa: E402
from product_agent_os.project_graph_llm_proposal_provider import (  # noqa: E402
    build_llm_proposal_provider_gate,
    evaluate_llm_proposal_safety,
)
from product_agent_os.project_graph_review_ledger import (  # noqa: E402
    PROPOSAL_DIFF_TARGET,
    REVIEW_LEDGER_TARGET,
    build_human_review_ledger,
    build_proposal_diff_preview,
)
from product_agent_os.project_graph_semantic import build_semantic_retrieval_index  # noqa: E402


class ProjectGraphCanonicalMutationTest(unittest.TestCase):
    def test_canonical_mutation_requires_batch30_approval_before_dry_run_apply(self):
        graph, governance, ledger, diff = self._batch30_inputs()

        plan = build_canonical_mutation_plan(
            graph,
            review_ledger=ledger,
            proposal_diff=diff,
            approval=None,
            governance_packet=governance,
        )

        self.assertEqual(plan["status"], "approval_required")
        self.assertEqual(plan["artifact_kind"], "project_graph_canonical_mutation_plan")
        self.assertTrue(plan["no_mutation_without_dry_run_plan"])
        self.assertTrue(plan["mutation_plan_required_for_apply"])
        self.assertFalse(plan["provider_call_allowed"])
        self.assertFalse(plan["external_call_performed"])
        self.assertIn("canonical_mutation_approval:missing", plan["validation"]["errors"])

    def test_plan_apply_journal_and_rollback_are_accepted_only_and_digest_verified(self):
        graph, governance, ledger, diff = self._batch30_inputs()

        plan = build_canonical_mutation_plan(
            graph,
            review_ledger=ledger,
            proposal_diff=diff,
            approval=self._canonical_mutation_approval(),
            governance_packet=governance,
        )
        result = apply_accepted_mutations_to_graph(graph, plan)
        rollback = build_graph_rollback_proof(graph, result["mutated_graph"], result["journal_entries"])

        self.assertEqual(plan["status"], "ready", plan["validation"])
        self.assertTrue(validate_canonical_mutation_approval(self._canonical_mutation_approval(), governance)["ok"])
        self.assertTrue(validate_canonical_mutation_plan(plan)["ok"], validate_canonical_mutation_plan(plan))
        self.assertEqual(plan["canonical_graph_mutation"], "dry_run_only")
        self.assertEqual(plan["mutation_write_policy"], "stage_root_generated_graph_copy_only")
        self.assertTrue(plan["only_accepted_proposals_mutate_graph"])
        self.assertTrue(plan["accepted_gap_remains_non_mutating"])
        self.assertEqual(len(plan["operations"]), 1)
        self.assertEqual(plan["operations"][0]["review_decision"], "accepted")
        self.assertGreaterEqual(len(plan["skipped_review_decisions"]), 1)
        self.assertTrue(
            any(item["reason"] == "accepted_gap_not_mutation_eligible" for item in plan["skipped_review_decisions"])
        )
        self.assertEqual(result["status"], "ready", result["validation"])
        self.assertEqual(result["canonical_graph_mutation"], "stage_root_generated_graph_copy_only")
        self.assertEqual(result["applied_operation_count"], 1)
        self.assertEqual(result["journal_entry_count"], 1)
        self.assertEqual(result["journal_entries"][0]["artifact_kind"], "project_graph_mutation_journal")
        self.assertTrue(result["journal_entries"][0]["append_only"])
        self.assertTrue(result["journal_entries"][0]["rollback_patch_present"])
        self.assertIn("inverse_patch", result["journal_entries"][0])
        self.assertNotEqual(graph_content_fingerprint(graph), result["post_graph_digest"])
        self.assertEqual(rollback["status"], "ready", rollback["validation"])
        self.assertTrue(rollback["rollback_restores_previous_graph_digest"])
        self.assertEqual(rollback["pre_graph_digest"], rollback["restored_graph_digest"])
        self.assertTrue(rollback["delete_generated_caches"])
        self.assertTrue(validate_graph_rollback_proof(rollback)["ok"], validate_graph_rollback_proof(rollback))

    def test_stage_and_disable_canonical_mutation_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph, governance, ledger, diff = self._batch30_inputs(workspace=workspace)
            graph_path = Path(tmp) / "graph.json"
            governance_path = Path(tmp) / "governance.json"
            ledger_path = Path(tmp) / "ledger.json"
            diff_path = Path(tmp) / "diff.json"
            for path, payload in [
                (graph_path, graph),
                (governance_path, governance),
                (ledger_path, ledger),
                (diff_path, diff),
            ]:
                path.write_text(json.dumps(payload), encoding="utf-8")

            missing_approval = stage_canonical_graph_mutation(
                graph_path,
                ledger_path,
                diff_path,
                stage_root,
                workspace=workspace,
                approval=None,
                governance_artifact=governance_path,
            )
            staged = stage_canonical_graph_mutation(
                graph_path,
                ledger_path,
                diff_path,
                stage_root,
                workspace=workspace,
                approval=self._canonical_mutation_approval(),
                governance_artifact=governance_path,
            )

            self.assertEqual(missing_approval["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(staged["rendered_artifacts"]["status"], "ready", staged["rendered_artifacts"]["validation"])
            self.assertTrue((stage_root / MUTATION_PLAN_TARGET).exists())
            self.assertTrue((stage_root / MUTATED_GRAPH_TARGET).exists())
            self.assertTrue((stage_root / MUTATION_JOURNAL_TARGET).exists())
            self.assertTrue((stage_root / ROLLBACK_PROOF_TARGET).exists())
            journal_lines = (stage_root / MUTATION_JOURNAL_TARGET).read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(journal_lines), 1)
            self.assertTrue(json.loads(journal_lines[0])["inverse_patch"])
            self.assertFalse((workspace / MUTATION_PLAN_TARGET).exists())

            disabled = disable_canonical_graph_mutation(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertTrue(disabled["rendered_artifacts"]["deletion_proof"]["delete_generated_caches"])
            self.assertFalse((stage_root / MUTATION_PLAN_TARGET).exists())
            self.assertFalse((stage_root / MUTATED_GRAPH_TARGET).exists())
            self.assertFalse((stage_root / MUTATION_JOURNAL_TARGET).exists())
            self.assertFalse((stage_root / ROLLBACK_PROOF_TARGET).exists())

            with self.assertRaises(ValueError):
                stage_canonical_graph_mutation(
                    graph_path,
                    ledger_path,
                    diff_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._canonical_mutation_approval(),
                    governance_artifact=governance_path,
                )

    def _batch30_inputs(self, workspace: Path | None = None) -> tuple[dict, dict, dict, dict]:
        workspace_path = workspace or self._write_workspace(Path(self._tmp()) / "workspace")
        graph = build_project_code_graph(workspace_path)
        semantic_index = build_semantic_retrieval_index(
            graph,
            static_index=build_static_search_index(graph),
            approval=self._semantic_approval(),
        )
        proposals = build_llm_extraction_proposals(
            graph,
            semantic_index=semantic_index,
            approval=self._local_llm_approval(),
        )
        governance = self._governance_packet()
        provider_gate = build_llm_proposal_provider_gate(
            graph,
            semantic_index=semantic_index,
            local_proposals=proposals,
            approval=self._llm_provider_approval(),
            governance_packet=governance,
        )
        safety_eval = evaluate_llm_proposal_safety(
            provider_gate,
            graph=graph,
            semantic_index=semantic_index,
            cases=[],
            provider_results=None,
        )
        ledger = build_human_review_ledger(
            graph,
            local_proposals=proposals,
            provider_gate=provider_gate,
            safety_eval=safety_eval,
            approval=self._review_approval(),
            governance_packet=governance,
            review_decisions=self._review_decisions(proposals),
        )
        diff = build_proposal_diff_preview(graph, local_proposals=proposals, review_ledger=ledger)
        return graph, governance, ledger, diff

    def _tmp(self) -> str:
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        return temp.name

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

    def _review_decisions(self, proposals: dict) -> dict:
        decisions = []
        for proposal, decision in [
            (self._proposal_by_kind(proposals, "semantic_node", index=0), "accepted"),
            (self._proposal_by_kind(proposals, "semantic_edge", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "rationale_comment", index=0), "accepted_gap"),
            (self._proposal_by_kind(proposals, "semantic_node", index=1), "rejected"),
        ]:
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
        if matches:
            return matches[0]
        self.fail(f"missing proposal kind {kind}")

    def _canonical_mutation_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": [
                "canonical_mutation_dry_run",
                "mutation_journal",
                "accepted_mutation_apply",
                "rollback_engine",
            ],
            "mutation_policy": {
                "dry_run_required": True,
                "conflict_check_required": True,
                "graph_digest_check_required": True,
                "accepted_only": True,
                "stage_root_only": True,
                "review_ledger_required": True,
                "proposal_diff_required": True,
            },
            "journal_policy": {
                "append_only": True,
                "jsonl_required": True,
                "inverse_patch_required": True,
            },
            "rollback_policy": {
                "restore_prior_digest": True,
                "delete_generated_caches": True,
                "stage_root_only": True,
                "rollback_proof_required": True,
            },
            "data_classification": {
                "allowed_inputs": ["reviewed_proposal_ids", "source_node_ids", "observation_ids", "owner_decisions"],
                "forbidden_inputs": ["raw_source_bodies", "secrets", "absolute_local_paths", "private_text"],
            },
            "rollback_path": "delete generated Batch 30 mutation artifacts under stage root",
            "residual_risks": ["accepted proposals can still represent incorrect semantics until rollback proof is inspected"],
        }

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
            "incident_path": "disable generated proposal artifact and log AI incident workflow",
            "owner": "product-agent-owner",
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-llm-proposals.json",
        }


if __name__ == "__main__":
    unittest.main()
