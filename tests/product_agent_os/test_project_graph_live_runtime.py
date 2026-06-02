import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
SCRIPT = SCRIPTS / "scan_project_code_graph.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_code_graph import build_project_code_graph  # noqa: E402
from product_agent_os.project_graph_live_governance import build_live_governance_packet  # noqa: E402
from product_agent_os.project_graph_live_runtime import (  # noqa: E402
    LIVE_RUNTIME_LOG_TARGET,
    LIVE_RUNTIME_PID_TARGET,
    LIVE_RUNTIME_TARGET,
    build_live_runtime_contract,
    disable_live_runtime_contract,
    handle_live_runtime_request,
    stage_live_runtime_contract,
    validate_live_runtime_contract,
    validate_live_runtime_contract_approval,
)


class ProjectGraphLiveRuntimeTest(unittest.TestCase):
    def test_runtime_contract_requires_batch24_governance_and_has_no_write_endpoints(self):
        graph = build_project_code_graph(self._write_query_workspace(Path(self._tmp()) / "workspace"))

        missing = build_live_runtime_contract(graph, approval=None, governance_packet=None)
        contract = build_live_runtime_contract(
            graph,
            approval=self._runtime_approval(),
            governance_packet=self._governance_packet(),
        )
        malformed = self._runtime_approval()
        malformed["allowed_surfaces"].append("canonical_graph_mutation")
        malformed_result = validate_live_runtime_contract_approval(malformed, self._governance_packet())

        self.assertEqual(missing["status"], "approval_required")
        self.assertIn("live_runtime_approval:missing", missing["validation"]["errors"])
        self.assertFalse(malformed_result["ok"])
        self.assertIn("live_runtime_approval:allowed_surfaces:canonical_graph_mutation", malformed_result["errors"])
        self.assertEqual(contract["artifact_kind"], "project_graph_live_runtime_contract")
        self.assertEqual(contract["approval_boundary"], "batch25_local_read_only_runtime_auth_fallback")
        self.assertEqual(contract["runtime_status"], "disabled_by_default_not_started")
        self.assertFalse(contract["server_lifecycle"]["server_started"])
        self.assertEqual(contract["server_contract"]["write_endpoints"], [])
        self.assertIn("canonical_graph_mutation", contract["blocked_surfaces"])
        self.assertTrue(validate_live_runtime_contract(contract)["ok"])
        rendered = json.dumps(contract, sort_keys=True).lower()
        self.assertNotIn("c:\\users\\", rendered)
        self.assertNotIn("return 'ok'", rendered)

    def test_auth_policy_rejects_unauthorized_public_and_mutation_requests(self):
        graph = build_project_code_graph(self._write_query_workspace(Path(self._tmp()) / "workspace"))
        contract = build_live_runtime_contract(
            graph,
            approval=self._runtime_approval(),
            governance_packet=self._governance_packet(),
        )

        unauthorized = handle_live_runtime_request(
            contract,
            {"method": "GET", "path": "/status", "headers": {}},
        )
        public_host = handle_live_runtime_request(
            contract,
            {"method": "GET", "path": "/status", "host": "0.0.0.0", "headers": {"authorization": "env-token"}},
        )
        mutation = handle_live_runtime_request(
            contract,
            {"method": "POST", "path": "/mutate", "headers": {"authorization": "env-token"}, "body": {}},
        )
        query = handle_live_runtime_request(
            contract,
            {
                "method": "POST",
                "path": "/query",
                "headers": {"authorization": "env-token"},
                "body": {"query": "search", "text": "worker run", "max_results": 5},
            },
        )

        self.assertEqual(unauthorized["status"], "blocked")
        self.assertIn("live_runtime_auth:unauthorized", unauthorized["errors"])
        self.assertEqual(public_host["status"], "blocked")
        self.assertIn("live_runtime_auth:public_bind", public_host["errors"])
        self.assertEqual(mutation["status"], "blocked")
        self.assertIn("live_runtime_contract:read_only", mutation["errors"])
        self.assertEqual(query["status"], "ok")
        self.assertEqual(query["runtime_backend"], "local_read_only_contract")
        self.assertEqual(query["fallback"], "graph_only_query_mode")
        self.assertEqual(query["nodes"][0]["id"], "function:app.worker.run")

    def test_stage_disable_and_fallback_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            governance_path = Path(tmp) / "governance.json"
            graph = build_project_code_graph(workspace)
            graph_path.write_text(json.dumps(graph), encoding="utf-8")
            governance_path.write_text(json.dumps(self._governance_packet()), encoding="utf-8")

            result = stage_live_runtime_contract(
                graph_path,
                stage_root,
                workspace=workspace,
                approval=self._runtime_approval(),
                governance_artifact=governance_path,
            )
            target = stage_root / LIVE_RUNTIME_TARGET
            self.assertEqual(result["rendered_artifacts"]["status"], "ready")
            self.assertEqual(result["rendered_artifacts"]["mode"], "validate-live-runtime")
            self.assertTrue(target.exists())
            self.assertFalse((stage_root / LIVE_RUNTIME_PID_TARGET).exists())
            self.assertFalse((stage_root / LIVE_RUNTIME_LOG_TARGET).exists())

            disabled = disable_live_runtime_contract(stage_root, workspace=workspace)
            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertEqual(disabled["rendered_artifacts"]["fallback"], "graph_only_query_mode")
            self.assertFalse(target.exists())
            self.assertIn(LIVE_RUNTIME_TARGET, disabled["rendered_artifacts"]["deletion_proof"]["targets_checked"])

            with self.assertRaises(ValueError):
                stage_live_runtime_contract(
                    graph_path,
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._runtime_approval(),
                    governance_artifact=governance_path,
                )

    def test_cli_stages_live_runtime_contract_and_redacts_output(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_query_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            graph_path = Path(tmp) / "graph.json"
            governance_path = Path(tmp) / "governance.json"
            approval_path = Path(tmp) / "approval.json"
            graph_path.write_text(json.dumps(build_project_code_graph(workspace)), encoding="utf-8")
            governance_path.write_text(json.dumps(self._governance_packet()), encoding="utf-8")
            approval_path.write_text(json.dumps(self._runtime_approval()), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-runtime",
                    "--graph",
                    str(graph_path),
                    "--live-governance",
                    str(governance_path),
                    "--live-runtime-approval",
                    str(approval_path),
                    "--stage",
                    str(stage_root),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(result.stderr, "")
            payload = json.loads(result.stdout)
            self.assertEqual(payload["rendered_artifacts"]["status"], "ready")
            self.assertFalse(payload["rendered_artifacts"]["server_started"])
            self.assertTrue((stage_root / LIVE_RUNTIME_TARGET).exists())
            self.assertNotIn(str(workspace), result.stdout)
            self.assertNotIn(str(stage_root), result.stdout)

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
                "residual_risks": ["provider drift remains blocked until later Task 26 batches"],
            }
        )

    def _runtime_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "Product-Agent OS Maintainer",
            "allowed_surfaces": [
                "local_read_only_runtime",
                "server_lifecycle",
                "local_auth_policy",
                "graph_only_fallback",
            ],
            "server_contract": {
                "read_endpoints": ["GET /status", "POST /query"],
                "write_endpoints": [],
                "canonical_mutation_allowed": False,
                "stable_json_errors": True,
                "max_payload_tokens": 4000,
            },
            "lifecycle_controls": {
                "server_enabled_by_default": False,
                "start_requires_explicit_command": True,
                "server_started_in_batch": False,
                "pid_path": ".codex/product-agent-os/project-code-graph-live-runtime.pid",
                "log_path": ".codex/product-agent-os/project-code-graph-live-runtime.log",
                "cleanup_required": True,
                "shutdown_required": True,
            },
            "auth_policy": {
                "bind_host": "127.0.0.1",
                "public_network": False,
                "token_required": True,
                "token_source": "environment",
                "token_env_var": "PRODUCT_AGENT_OS_LOCAL_RUNTIME_TOKEN",
                "cors_policy": "local_only",
                "offline_assets_only": True,
            },
            "fallback_policy": {
                "fallback": "graph_only_query_mode",
                "disable_deletes_runtime_artifacts": True,
            },
            "rollback_path": "delete .codex/product-agent-os/project-code-graph-live-runtime.json",
            "residual_risks": ["actual process startup remains outside Batch 25 contract tests"],
        }

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

    def _tmp(self) -> str:
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return tmp.name


if __name__ == "__main__":
    unittest.main()
