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

from product_agent_os.project_graph_live_governance import (  # noqa: E402
    LIVE_GOVERNANCE_TARGET,
    build_live_governance_packet,
    disable_live_governance,
    enforce_live_budget,
    sanitize_live_provider_payload,
    stage_live_governance,
    validate_live_runtime_approval,
)


class ProjectGraphLiveGovernanceTest(unittest.TestCase):
    def test_approval_packet_covers_batch24_governance_and_blocks_live_surfaces(self):
        valid = validate_live_runtime_approval(self._approval())
        self.assertTrue(valid["ok"], valid)

        approval = self._approval()
        approval["allowed_surfaces"].append("live_server_start")
        approval["provider_policy"]["external_provider_calls_allowed"] = True
        invalid = validate_live_runtime_approval(approval)

        self.assertFalse(invalid["ok"])
        self.assertIn("live_governance_approval:allowed_surfaces:live_server_start", invalid["errors"])
        self.assertIn("live_governance_approval:provider_policy:external_calls", invalid["errors"])

    def test_redaction_guard_blocks_raw_source_secrets_and_absolute_paths_before_provider_use(self):
        payload = {
            "query": "find worker",
            "path": r"C:\Users\user\Desktop\project\private\app.py",
            "raw_source_body": "OPENAI_API_KEY=sk-test-secret",
            "metadata": {"api_key": "sk-test-secret"},
        }

        result = sanitize_live_provider_payload(payload, approval=self._approval())
        rendered = json.dumps(result, sort_keys=True)

        self.assertEqual(result["status"], "blocked")
        self.assertFalse(result["provider_call_allowed"])
        self.assertIn("blocked_input:absolute_local_paths", result["validation"]["errors"])
        self.assertIn("blocked_input:raw_source_bodies", result["validation"]["errors"])
        self.assertIn("blocked_input:secrets", result["validation"]["errors"])
        self.assertNotIn("sk-test-secret", rendered)
        self.assertNotIn(r"C:\Users\user", rendered)

    def test_credentials_policy_is_environment_only_and_never_stores_secret_values(self):
        approval = self._approval()
        approval["credential_policy"]["providers"][0]["credential_value"] = "sk-test-secret"

        packet = build_live_governance_packet(approval)
        rendered = json.dumps(packet, sort_keys=True)

        self.assertEqual(packet["status"], "blocked")
        self.assertIn("credential_policy:stored_secret", packet["validation"]["errors"])
        self.assertNotIn("sk-test-secret", rendered)
        self.assertEqual(packet["credential_policy"]["providers"][0]["credential_source"], "environment")
        self.assertEqual(packet["credential_policy"]["secret_material_stored"], False)

    def test_cache_budget_and_deletion_policy_are_source_free_and_budget_blocks_overrun(self):
        packet = build_live_governance_packet(self._approval())
        budget_result = enforce_live_budget(
            {
                "provider": "external_embedding",
                "estimated_tokens": 1_501,
                "estimated_cost_units": 1,
                "estimated_latency_ms": 251,
            },
            packet["budget_policy"],
        )

        self.assertEqual(packet["status"], "ready")
        self.assertEqual(packet["artifact_kind"], "project_graph_live_governance")
        self.assertEqual(packet["approval_boundary"], "batch24_live_governance_only_no_live_calls")
        self.assertEqual(packet["data_classification"]["blocked_fields"], ["absolute_local_paths", "raw_source_bodies", "secrets"])
        self.assertEqual(packet["cache_policy"]["ttl_days"], 7)
        self.assertEqual(packet["cache_policy"]["stale_policy"], "block_if_graph_or_policy_fingerprint_mismatch")
        self.assertEqual(packet["cache_policy"]["deletion_proof_required"], True)
        self.assertEqual(packet["rollback"]["disable_path"], f"delete {LIVE_GOVERNANCE_TARGET}")
        self.assertEqual(budget_result["status"], "blocked")
        self.assertIn("budget:estimated_tokens", budget_result["errors"])
        self.assertIn("budget:estimated_latency_ms", budget_result["errors"])

    def test_stage_and_disable_live_governance_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            stage_root = Path(tmp) / "stage"

            result = stage_live_governance(stage_root, workspace=workspace, approval=self._approval())
            target = stage_root / LIVE_GOVERNANCE_TARGET
            staged = json.loads(target.read_text(encoding="utf-8"))

            self.assertEqual(result["rendered_artifacts"]["status"], "ready")
            self.assertEqual(result["rendered_artifacts"]["mode"], "validate-live-governance")
            self.assertTrue(target.exists())
            self.assertNotIn(str(workspace), json.dumps(staged, sort_keys=True))

            disabled = disable_live_governance(stage_root, workspace=workspace)
            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertFalse(target.exists())

    def test_cli_stages_live_governance_and_redacts_output(self):
        with TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            workspace.mkdir()
            stage_root = Path(tmp) / "stage"
            approval_path = Path(tmp) / "approval.json"
            approval_path.write_text(json.dumps(self._approval()), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(workspace),
                    "--validate-live-governance",
                    "--live-approval",
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
            self.assertTrue((stage_root / LIVE_GOVERNANCE_TARGET).exists())
            self.assertNotIn(str(workspace), result.stdout)
            self.assertNotIn(str(stage_root), result.stdout)

    def _approval(self) -> dict:
        return {
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
