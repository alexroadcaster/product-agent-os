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
)
from product_agent_os.project_graph_extension_closure import (  # noqa: E402
    EXTENSION_CLOSURE_TARGET,
    build_future_extension_closure_packet,
    disable_future_extensions,
    stage_future_extension_closure,
    validate_future_extension_closure_packet,
)
from product_agent_os.project_graph_index import (  # noqa: E402
    STATIC_SEARCH_INDEX_TARGET,
    build_static_search_index,
)
from product_agent_os.project_graph_llm_extraction import (  # noqa: E402
    LLM_EXTRACTION_TARGET,
    build_llm_extraction_proposals,
)
from product_agent_os.project_graph_semantic import (  # noqa: E402
    SEMANTIC_RETRIEVAL_TARGET,
    build_semantic_retrieval_index,
)


class ProjectGraphExtensionClosureTest(unittest.TestCase):
    def test_closure_packet_verifies_only_approved_surfaces_and_blocks_future_runtime(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            artifacts = self._approved_artifacts(graph)

            packet = build_future_extension_closure_packet(
                workspace=workspace,
                stage_root=Path(tmp) / "stage",
                graph=graph,
                artifacts=artifacts,
                verification_evidence=self._verification_evidence(),
            )

            self.assertTrue(validate_future_extension_closure_packet(packet)["ok"])
            self.assertEqual(packet["artifact_kind"], "project_graph_future_extension_closure")
            self.assertEqual(packet["approval_boundary"], "batch23_future_extension_verification_rollback_closure")
            self.assertEqual(packet["status"], "ready")
            self.assertEqual(packet["full_verification_contract"]["timeout_ms"], 1_200_000)
            self.assertEqual(packet["git_boundary"], "explicit_only")
            self.assertEqual(packet["runtime_visual_qa"]["backend_server_status"], "disabled_by_default")
            self.assertEqual(packet["runtime_visual_qa"]["live_server_started"], False)
            self.assertEqual(packet["runtime_visual_qa"]["external_requests_allowed"], False)
            self.assertEqual(packet["graph_only_fallback"]["status"], "ok")
            self.assertEqual(
                packet["deferred_surface_status"]["live_external_llm_semantic_extraction"],
                "blocked_without_new_explicit_approval",
            )
            self.assertEqual(
                packet["deferred_surface_status"]["canonical_graph_mutation_from_generated_proposals"],
                "blocked_without_new_explicit_approval",
            )
            self.assertNotIn(str(workspace), json.dumps(packet, sort_keys=True))

    def test_closure_blocks_active_backend_external_models_and_canonical_mutation(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            graph = build_project_code_graph(workspace)
            artifacts = self._approved_artifacts(graph)
            artifacts["backend"]["server_lifecycle"]["active_process"] = True
            artifacts["backend"]["server_lifecycle"]["server_status"] = "running"
            artifacts["semantic"]["model_decision"]["external_model_calls_allowed"] = True
            artifacts["llm_proposals"]["model_policy"]["external_model_calls_allowed"] = True
            artifacts["llm_proposals"]["canonical_graph_mutation"] = "allowed"

            packet = build_future_extension_closure_packet(
                workspace=workspace,
                stage_root=Path(tmp) / "stage",
                graph=graph,
                artifacts=artifacts,
                verification_evidence=self._verification_evidence(),
            )

            self.assertEqual(packet["status"], "blocked")
            self.assertIn("backend:live_server_active", packet["validation"]["errors"])
            self.assertIn("semantic:external_model_calls", packet["validation"]["errors"])
            self.assertIn("llm_proposals:external_model_calls", packet["validation"]["errors"])
            self.assertIn("llm_proposals:canonical_graph_mutation", packet["validation"]["errors"])
            self.assertEqual(packet["safe_next_action"], "Disable generated extension artifacts and rerun graph-only verification.")

    def test_disable_extensions_deletes_generated_artifacts_and_preserves_graph_only_fallback(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph = build_project_code_graph(workspace)
            for relative in [
                STATIC_SEARCH_INDEX_TARGET,
                ".codex/product-agent-os/project-code-graph-search-index.previous.json",
                LOCAL_BACKEND_TARGET,
                ".codex/product-agent-os/project-code-graph-backend.previous.json",
                ".codex/product-agent-os/project-code-graph-backend.log",
                ".codex/product-agent-os/project-code-graph-backend.pid",
                SEMANTIC_RETRIEVAL_TARGET,
                ".codex/product-agent-os/project-code-graph-semantic-index.previous.json",
                LLM_EXTRACTION_TARGET,
                ".codex/product-agent-os/project-code-graph-llm-proposals.previous.json",
                EXTENSION_CLOSURE_TARGET,
            ]:
                target = stage_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("generated\n", encoding="utf-8")

            result = disable_future_extensions(stage_root, workspace=workspace, graph=graph)
            remaining = [
                relative
                for relative in result["rendered_artifacts"]["deletion_proof"]["targets_checked"]
                if (stage_root / relative).exists()
            ]

            self.assertEqual(result["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(result["rendered_artifacts"]["fallback"], "graph_only_query_mode")
            self.assertEqual(result["rendered_artifacts"]["graph_only_fallback"]["status"], "ok")
            self.assertEqual(remaining, [])

    def test_stage_closure_report_writes_source_free_artifact_under_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")

            result = stage_future_extension_closure(
                stage_root,
                workspace=workspace,
                graph_artifact=graph_path,
                artifacts=self._approved_artifacts(graph),
                verification_evidence=self._verification_evidence(),
            )
            report = json.loads((stage_root / EXTENSION_CLOSURE_TARGET).read_text(encoding="utf-8"))

            self.assertEqual(result["rendered_artifacts"]["status"], "ready")
            self.assertEqual(result["rendered_artifacts"]["mode"], "verify-extensions")
            self.assertEqual(report["status"], "ready")
            self.assertNotIn(str(workspace), json.dumps(report, sort_keys=True))

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

    def _approved_artifacts(self, graph: dict) -> dict:
        static_index = build_static_search_index(graph)
        backend = build_local_query_backend_store(
            graph,
            static_index=static_index,
            approval=self._backend_approval(),
        )
        semantic = build_semantic_retrieval_index(
            graph,
            static_index=static_index,
            approval=self._semantic_approval(),
        )
        llm_proposals = build_llm_extraction_proposals(
            graph,
            semantic_index=semantic,
            approval=self._llm_approval(),
        )
        return {
            "static_index": static_index,
            "backend": backend,
            "semantic": semantic,
            "llm_proposals": llm_proposals,
        }

    def _verification_evidence(self) -> dict:
        return {
            "focused_suites": {
                "static_index": "passed",
                "backend": "passed",
                "semantic": "passed",
                "llm_proposals": "passed",
            },
            "full_verification_required": True,
            "timeout_ms": 1_200_000,
            "docs_check_required": True,
            "strict_mkdocs_required": True,
            "diff_hygiene_required": True,
        }

    def _backend_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "storage_path": ".codex/product-agent-os/project-code-graph-backend.json",
            "port_policy": {"host": "127.0.0.1", "port": 0, "mode": "disabled_by_default"},
            "process_lifecycle": {
                "server_enabled_by_default": False,
                "start_requires_explicit_command": True,
                "pid_path": ".codex/product-agent-os/project-code-graph-backend.pid",
            },
            "auth_boundary": {"local_only": True, "write_controls": False},
            "cleanup": {"delete_generated_store": True},
            "logging": {"log_path": ".codex/product-agent-os/project-code-graph-backend.log", "redacted": True},
            "performance_threshold": {"max_query_ms": 250, "max_payload_tokens": 4000},
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-backend.json",
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
