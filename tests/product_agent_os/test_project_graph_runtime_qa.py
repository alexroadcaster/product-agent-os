import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_graph_live_governance import build_live_governance_packet  # noqa: E402
from product_agent_os.project_graph_live_runtime import build_live_runtime_contract  # noqa: E402
from product_agent_os.project_graph_real_testing import (  # noqa: E402
    CODEX_SURFACE_SMOKE_TARGET,
    build_codex_surface_smoke_plan,
    validate_codex_surface_smoke_plan,
    validate_real_testing_readiness_packet,
)
from product_agent_os.project_graph_runtime_qa import (  # noqa: E402
    PERFORMANCE_BUDGET_TARGET,
    RUNTIME_BROWSER_QA_TARGET,
    STABILIZATION_LEDGER_TARGET,
    build_performance_budget_packet,
    build_runtime_browser_qa_packet,
    build_stabilization_ledger_packet,
    disable_runtime_qa,
    stage_runtime_qa,
    validate_performance_budget_packet,
    validate_runtime_browser_qa_packet,
    validate_runtime_qa_approval,
    validate_stabilization_ledger_packet,
)


class ProjectGraphRuntimeQaTest(unittest.TestCase):
    def test_runtime_qa_requires_batch33_approval_and_batch32_readiness(self):
        packet = build_runtime_browser_qa_packet(
            readiness_packet=self._readiness_packet(),
            smoke_plan=self._smoke_plan(),
            runtime_contract=self._runtime_contract(),
            approval=None,
            browser_checks=self._browser_checks(),
        )

        self.assertEqual(packet["status"], "approval_required")
        self.assertEqual(packet["artifact_kind"], "project_graph_runtime_browser_qa")
        self.assertIn("runtime_qa_approval:missing", packet["validation"]["errors"])
        self.assertFalse(packet["provider_call_allowed"])
        self.assertFalse(packet["external_call_performed"])
        self.assertFalse(packet["live_server_started"])
        self.assertEqual(packet["canonical_graph_mutation"], "not_performed")

    def test_qa_performance_and_stabilization_are_ready_and_source_free(self):
        approval = self._runtime_qa_approval()
        qa = build_runtime_browser_qa_packet(
            readiness_packet=self._readiness_packet(),
            smoke_plan=self._smoke_plan(),
            runtime_contract=self._runtime_contract(),
            approval=approval,
            browser_checks=self._browser_checks(),
        )
        performance = build_performance_budget_packet(
            readiness_packet=self._readiness_packet(),
            runtime_contract=self._runtime_contract(),
            approval=approval,
            measurements=self._performance_measurements(),
        )
        stabilization = build_stabilization_ledger_packet(
            qa_packet=qa,
            performance_packet=performance,
            approval=approval,
            defects=self._defects(),
        )

        self.assertTrue(validate_runtime_qa_approval(approval, self._readiness_packet())["ok"])
        self.assertTrue(validate_runtime_browser_qa_packet(qa)["ok"])
        self.assertEqual(qa["status"], "ready")
        self.assertTrue(qa["console_network_checks_present"])
        self.assertTrue(qa["mobile_overflow_check_present"])
        self.assertTrue(qa["source_boundary_labels_visible"])
        self.assertTrue(qa["generated_view_labels_visible"])
        self.assertTrue(qa["no_external_requests_beyond_approved_providers"])
        self.assertFalse(qa["browser_automation_started"])
        self.assertFalse(qa["live_server_started"])

        self.assertTrue(validate_performance_budget_packet(performance)["ok"])
        self.assertEqual(performance["status"], "ready")
        self.assertTrue(performance["node_edge_search_provider_latency_caps_present"])
        self.assertTrue(performance["memory_bounds_present"])
        self.assertTrue(performance["budget_breach_disables_live_layer_or_records_accepted_gap"])
        self.assertEqual(performance["breach_summary"]["breaches"], 1)

        self.assertTrue(validate_stabilization_ledger_packet(stabilization)["ok"])
        self.assertEqual(stabilization["status"], "ready")
        self.assertTrue(stabilization["severity_policy_present"])
        self.assertTrue(stabilization["fix_or_accepted_gap_ledger_present"])
        self.assertTrue(stabilization["rerun_plan_present"])
        self.assertTrue(stabilization["no_open_p0_p1"])
        self.assertTrue(stabilization["remaining_issues_have_owner_risk_follow_up"])

        rendered = json.dumps([qa, performance, stabilization], sort_keys=True)
        self.assertNotIn("sk-runtime-secret", rendered)
        self.assertNotIn("C:\\Users\\private\\target", rendered)
        self.assertNotIn("return 'raw'", rendered)

    def test_stage_and_disable_runtime_qa_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            readiness_path = Path(tmp) / "readiness.json"
            smoke_path = Path(tmp) / "smoke.json"
            runtime_path = Path(tmp) / "runtime.json"
            readiness_path.write_text(json.dumps(self._readiness_packet()), encoding="utf-8")
            smoke_path.write_text(json.dumps(self._smoke_plan()), encoding="utf-8")
            runtime_path.write_text(json.dumps(self._runtime_contract()), encoding="utf-8")

            missing_approval = stage_runtime_qa(
                stage_root,
                workspace=workspace,
                approval=None,
                readiness_artifact=readiness_path,
                smoke_artifact=smoke_path,
                runtime_artifact=runtime_path,
                browser_checks=self._browser_checks(),
                performance_measurements=self._performance_measurements(),
                defects=self._defects(),
            )
            staged = stage_runtime_qa(
                stage_root,
                workspace=workspace,
                approval=self._runtime_qa_approval(),
                readiness_artifact=readiness_path,
                smoke_artifact=smoke_path,
                runtime_artifact=runtime_path,
                browser_checks=self._browser_checks(),
                performance_measurements=self._performance_measurements(),
                defects=self._defects(),
            )

            self.assertEqual(missing_approval["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(staged["rendered_artifacts"]["status"], "ready", staged["rendered_artifacts"]["validation"])
            for target in [RUNTIME_BROWSER_QA_TARGET, PERFORMANCE_BUDGET_TARGET, STABILIZATION_LEDGER_TARGET]:
                self.assertTrue((stage_root / target).exists(), target)
                self.assertFalse((workspace / target).exists(), target)

            disabled = disable_runtime_qa(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertTrue(disabled["rendered_artifacts"]["deletion_proof"]["delete_generated_runtime_qa_artifacts"])
            for target in [RUNTIME_BROWSER_QA_TARGET, PERFORMANCE_BUDGET_TARGET, STABILIZATION_LEDGER_TARGET]:
                self.assertFalse((stage_root / target).exists(), target)

            with self.assertRaises(ValueError):
                stage_runtime_qa(
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._runtime_qa_approval(),
                    readiness_artifact=readiness_path,
                    smoke_artifact=smoke_path,
                    runtime_artifact=runtime_path,
                    browser_checks=self._browser_checks(),
                    performance_measurements=self._performance_measurements(),
                    defects=self._defects(),
                )

    def _write_workspace(self, workspace: Path) -> Path:
        (workspace / "app").mkdir(parents=True)
        (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
        (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        return workspace

    def _runtime_qa_approval(self) -> dict:
        return {
            "explicit_approval": True,
            "owner": "QA Owner",
            "allowed_surfaces": [
                "runtime_browser_qa",
                "runtime_performance_budget",
                "runtime_stabilization_loop",
            ],
            "qa_policy": {
                "browser_smoke_required": True,
                "console_network_checks_required": True,
                "mobile_overflow_check_required": True,
                "generated_view_labels_required": True,
                "source_boundary_labels_required": True,
                "external_requests_require_approved_provider": True,
            },
            "performance_policy": {
                "max_nodes": 10000,
                "max_edges": 30000,
                "max_search_latency_ms": 250,
                "max_provider_latency_ms": 0,
                "max_memory_mb": 512,
                "breach_policy": "disable_live_layer_or_accepted_gap",
            },
            "stabilization_policy": {
                "severity_policy_required": True,
                "no_open_p0_p1": True,
                "remaining_issue_owner_required": True,
                "rerun_plan_required": True,
            },
            "rollback_path": "delete generated Batch 33 runtime QA, performance and stabilization artifacts under stage root",
            "residual_risks": ["browser evidence remains staged until owner approves real testing execution"],
        }

    def _readiness_packet(self) -> dict:
        packet = {
            "schema_version": 1,
            "artifact_kind": "project_graph_real_testing_readiness",
            "status": "ready",
            "approval_boundary": "batch32_real_testing_readiness_target_consent_pilot_harness_codex_surface_smoke",
            "target": ".codex/product-agent-os/project-code-graph-real-testing-readiness.json",
            "real_testing_start_policy": "approved_targets_only",
            "no_hidden_unresolved_track10_gates": True,
            "provider_call_allowed": False,
            "external_call_performed": False,
            "live_server_started": False,
            "canonical_graph_mutation": "not_performed",
            "gate_statuses": [
                {"gate": "live_governance", "status": "implemented_verified"},
                {"gate": "live_runtime", "status": "explicitly_disabled"},
                {"gate": "external_embedding", "status": "blocked_by_missing_approval"},
                {"gate": "external_reranker", "status": "blocked_by_missing_approval"},
                {"gate": "external_llm", "status": "blocked_by_missing_approval"},
                {"gate": "human_review_ledger", "status": "implemented_verified"},
                {"gate": "canonical_graph_mutation", "status": "explicitly_disabled"},
                {"gate": "audit_operability", "status": "implemented_verified"},
            ],
            "validation": {"ok": True, "errors": [], "context": "project_graph_real_testing_readiness"},
        }
        self.assertTrue(validate_real_testing_readiness_packet(packet)["ok"])
        return packet

    def _smoke_plan(self) -> dict:
        smoke = build_codex_surface_smoke_plan(
            readiness_packet=self._readiness_packet(),
            surfaces=[
                {"surface": "Codex App", "status": "planned_smoke", "evidence": "desktop thread runbook"},
                {"surface": "CLI", "status": "planned_smoke", "evidence": "scripted commands"},
                {"surface": "IDE extension", "status": "accepted_gap", "evidence": "surface unavailable"},
            ],
            approval={
                "explicit_approval": True,
                "owner": "Pilot Owner",
                "allowed_surfaces": [
                    "real_testing_readiness",
                    "real_project_target_selection",
                    "pilot_harness",
                    "codex_surface_smoke",
                    "use_case_pilot_matrix",
                ],
                "readiness_policy": {
                    "entry_criteria_required": True,
                    "exit_criteria_required": True,
                    "accepted_gaps_allowed_with_owner": True,
                    "hidden_unresolved_gates_blocked": True,
                },
                "target_policy": {
                    "owner_approved_targets_only": True,
                    "data_policy_required": True,
                    "allowed_commands_required": True,
                    "production_targets_blocked_without_separate_approval": True,
                },
                "pilot_harness_policy": {
                    "dry_run_first": True,
                    "target_file_mutation_requires_explicit_target_approval": True,
                    "provider_calls_require_batch_approval": True,
                    "fallback_required": True,
                },
                "surface_smoke_policy": {
                    "codex_app_required": True,
                    "cli_required": True,
                    "ide_extension_required": True,
                    "missing_surface_recorded_as_gap_or_blocked": True,
                },
                "pilot_matrix_policy": {
                    "track8_archetypes_required": ["web", "backend", "docs", "pr_review", "evals", "automation", "ai_rag"],
                    "enabled_surface_requires_pilot_or_gap": True,
                },
                "rollback_path": "delete generated Batch 32 real testing readiness and pilot artifacts under stage root",
                "residual_risks": ["real testing is readiness evidence"],
            },
        )
        self.assertEqual(smoke["target"], CODEX_SURFACE_SMOKE_TARGET)
        self.assertTrue(validate_codex_surface_smoke_plan(smoke)["ok"])
        return smoke

    def _governance_packet(self) -> dict:
        return build_live_governance_packet(
            {
                "explicit_approval": True,
                "owner": "Graph Owner",
                "allowed_surfaces": [
                    "approval_packet",
                    "data_classification",
                    "redaction_pipeline",
                    "credential_boundary",
                    "cache_policy",
                    "budget_policy",
                ],
                "data_classification": {
                    "allowed_fields": ["node_id", "label", "type"],
                    "redacted_fields": ["relative_path", "review_comment"],
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
                    "providers": [{"provider": "external_llm", "credential_source": "environment", "env_var": "PRODUCT_AGENT_OS_LLM_API_KEY"}],
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
                "residual_risks": ["external providers remain disabled"],
            }
        )

    def _runtime_contract(self) -> dict:
        return build_live_runtime_contract(
            {"schema_version": 1, "nodes": [], "edges": []},
            approval={
                "explicit_approval": True,
                "owner": "Graph Owner",
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
                    "max_payload_tokens": 1200,
                },
                "lifecycle_controls": {
                    "server_enabled_by_default": False,
                    "server_started_in_batch": False,
                    "start_requires_explicit_command": True,
                    "cleanup_required": True,
                    "shutdown_required": True,
                    "pid_path": ".codex/product-agent-os/project-code-graph-live-runtime.pid",
                    "log_path": ".codex/product-agent-os/project-code-graph-live-runtime.log",
                },
                "auth_policy": {
                    "bind_host": "127.0.0.1",
                    "public_network": False,
                    "token_required": True,
                    "token_source": "environment",
                    "token_env_var": "PRODUCT_AGENT_OS_RUNTIME_TOKEN",
                    "cors_policy": "local_only",
                    "offline_assets_only": True,
                },
                "fallback_policy": {
                    "fallback": "graph_only_query_mode",
                    "disable_deletes_runtime_artifacts": True,
                },
                "rollback_path": "delete .codex/product-agent-os/project-code-graph-live-runtime.json",
                "residual_risks": ["server startup remains out of scope"],
            },
            governance_packet=self._governance_packet(),
        )

    def _browser_checks(self) -> dict:
        return {
            "browser_smoke": {"status": "passed", "browser_automation_started": False},
            "console": {"errors": []},
            "network": {
                "requests": [
                    {"url": "local://project-cockpit", "external": False, "approved_provider": False},
                ]
            },
            "mobile": [{"viewport": "390x844", "status": "passed", "horizontal_overflow": False}],
            "labels": {
                "generated_view_label_visible": True,
                "source_boundary_label_visible": True,
                "not_source_of_truth_label_visible": True,
            },
            "unsafe_fixture": "C:\\Users\\private\\target def run():\n    return 'raw'",
        }

    def _performance_measurements(self) -> list[dict]:
        return [
            {
                "scenario": "synthetic-large-graph",
                "node_count": 9000,
                "edge_count": 22000,
                "search_latency_ms": 180,
                "provider_latency_ms": 0,
                "memory_mb": 420,
                "breach_mitigation": "not_needed",
            },
            {
                "scenario": "accepted-gap-provider-latency",
                "node_count": 1000,
                "edge_count": 1200,
                "search_latency_ms": 80,
                "provider_latency_ms": 50,
                "memory_mb": 120,
                "breach_mitigation": "accepted_gap",
                "owner": "QA Owner",
                "risk": "Provider path remains disabled until approved real testing.",
                "follow_up_condition": "Separate provider approval must define latency budget before use.",
            },
        ]

    def _defects(self) -> list[dict]:
        return [
            {
                "defect_id": "B33-P2-001",
                "severity": "P2",
                "status": "accepted_gap",
                "owner": "QA Owner",
                "risk": "IDE extension smoke unavailable in current workspace.",
                "follow_up_condition": "Run IDE smoke when surface is available.",
                "rerun_plan": ["focused Batch 33 tests", "fixture eval"],
            }
        ]


if __name__ == "__main__":
    unittest.main()
