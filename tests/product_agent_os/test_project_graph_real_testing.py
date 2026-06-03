import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_graph_live_audit import (  # noqa: E402
    build_agent_skill_handoff_routing_packet,
    build_live_audit_event_log,
    build_runtime_observability_packet,
    build_security_privacy_test_packet,
)
from product_agent_os.project_graph_live_governance import build_live_governance_packet  # noqa: E402
from product_agent_os.project_graph_live_runtime import build_live_runtime_contract  # noqa: E402
from product_agent_os.project_graph_real_testing import (  # noqa: E402
    CODEX_SURFACE_SMOKE_TARGET,
    PILOT_HARNESS_TARGET,
    PILOT_MATRIX_TARGET,
    REAL_TESTING_READINESS_TARGET,
    REAL_TESTING_TARGETS_TARGET,
    build_codex_surface_smoke_plan,
    build_end_to_end_pilot_harness_packet,
    build_real_project_target_selection_packet,
    build_real_testing_readiness_packet,
    build_use_case_pilot_matrix,
    disable_real_testing_readiness,
    stage_real_testing_readiness,
    validate_codex_surface_smoke_plan,
    validate_end_to_end_pilot_harness_packet,
    validate_real_project_target_selection_packet,
    validate_real_testing_approval,
    validate_real_testing_readiness_packet,
    validate_use_case_pilot_matrix,
)


class ProjectGraphRealTestingTest(unittest.TestCase):
    def test_real_testing_requires_batch32_approval_and_operability_prerequisites(self):
        readiness = build_real_testing_readiness_packet(
            approval=None,
            governance_packet=self._governance_packet(),
            runtime_contract=self._runtime_contract(),
            audit_operability=self._audit_operability_packets(),
            gate_statuses=self._gate_statuses(),
        )
        targets = build_real_project_target_selection_packet(
            targets=self._targets(),
            approval=None,
            governance_packet=self._governance_packet(),
        )

        self.assertEqual(readiness["status"], "approval_required")
        self.assertEqual(readiness["artifact_kind"], "project_graph_real_testing_readiness")
        self.assertIn("real_testing_approval:missing", readiness["validation"]["errors"])
        self.assertFalse(readiness["live_server_started"])
        self.assertFalse(readiness["provider_call_allowed"])
        self.assertFalse(readiness["external_call_performed"])
        self.assertEqual(readiness["canonical_graph_mutation"], "not_performed")
        self.assertEqual(targets["status"], "approval_required")

    def test_readiness_targets_harness_smoke_and_matrix_are_ready_and_source_free(self):
        approval = self._real_testing_approval()
        governance = self._governance_packet()
        audit_operability = self._audit_operability_packets()

        readiness = build_real_testing_readiness_packet(
            approval=approval,
            governance_packet=governance,
            runtime_contract=self._runtime_contract(),
            audit_operability=audit_operability,
            gate_statuses=self._gate_statuses(),
        )
        targets = build_real_project_target_selection_packet(
            targets=self._targets(),
            approval=approval,
            governance_packet=governance,
        )
        harness = build_end_to_end_pilot_harness_packet(
            readiness_packet=readiness,
            target_packet=targets,
            approval=approval,
            pilot_steps=self._pilot_steps(),
        )
        smoke = build_codex_surface_smoke_plan(
            readiness_packet=readiness,
            surfaces=self._codex_surfaces(),
            approval=approval,
        )
        matrix = build_use_case_pilot_matrix(
            readiness_packet=readiness,
            smoke_plan=smoke,
            pilots=self._pilot_matrix(),
            approval=approval,
        )

        self.assertTrue(validate_real_testing_approval(approval, governance)["ok"])
        self.assertTrue(validate_real_testing_readiness_packet(readiness)["ok"])
        self.assertEqual(readiness["status"], "ready")
        self.assertTrue(readiness["no_hidden_unresolved_track10_gates"])
        self.assertEqual(readiness["real_testing_start_policy"], "approved_targets_only")
        self.assertFalse(readiness["live_server_started"])
        self.assertFalse(readiness["provider_call_allowed"])
        self.assertFalse(readiness["external_call_performed"])
        self.assertEqual(readiness["canonical_graph_mutation"], "not_performed")

        self.assertTrue(validate_real_project_target_selection_packet(targets)["ok"])
        self.assertEqual(targets["status"], "ready")
        self.assertTrue(targets["owner_approved_target_and_data_policy_required"])
        self.assertTrue(all(target["owner_approved"] for target in targets["targets"]))
        self.assertIn("python-app", targets["target_classes"])

        self.assertTrue(validate_end_to_end_pilot_harness_packet(harness)["ok"])
        self.assertEqual(harness["status"], "ready")
        self.assertTrue(harness["dry_run_only"])
        self.assertTrue(harness["target_file_mutation_allowed_only_if_approved"])
        self.assertEqual(harness["mutation_policy"], "no_target_file_mutation_without_explicit_target_approval")
        self.assertIn("scan_project_code_graph_dry_run", harness["pilot_steps"])
        self.assertIn("graph_only_fallback", harness["pilot_steps"])

        self.assertTrue(validate_codex_surface_smoke_plan(smoke)["ok"])
        self.assertEqual(smoke["status"], "ready")
        self.assertEqual({surface["surface"] for surface in smoke["surfaces"]}, {"Codex App", "CLI", "IDE extension"})
        self.assertTrue(smoke["missing_surface_recorded_as_gap_or_blocked"])

        self.assertTrue(validate_use_case_pilot_matrix(matrix)["ok"])
        self.assertEqual(matrix["status"], "ready")
        self.assertTrue(matrix["each_enabled_surface_has_pilot_or_accepted_gap"])
        for archetype in ["web", "backend", "docs", "pr_review", "evals", "automation", "ai_rag"]:
            self.assertIn(archetype, matrix["use_case_archetypes"])

        rendered = json.dumps([readiness, targets, harness, smoke, matrix], sort_keys=True)
        self.assertNotIn("C:\\Users\\private\\target", rendered)
        self.assertNotIn("sk-live-secret", rendered)
        self.assertNotIn("return 'raw'", rendered)

    def test_stage_and_disable_real_testing_readiness_are_stage_root_only(self):
        with TemporaryDirectory() as tmp:
            workspace = self._write_workspace(Path(tmp) / "workspace")
            stage_root = Path(tmp) / "stage"
            governance_path = Path(tmp) / "governance.json"
            runtime_path = Path(tmp) / "runtime.json"
            audit_path = Path(tmp) / "audit.json"
            governance_path.write_text(json.dumps(self._governance_packet()), encoding="utf-8")
            runtime_path.write_text(json.dumps(self._runtime_contract()), encoding="utf-8")
            audit_path.write_text(json.dumps(self._audit_operability_packets()), encoding="utf-8")

            missing_approval = stage_real_testing_readiness(
                stage_root,
                workspace=workspace,
                approval=None,
                governance_artifact=governance_path,
                runtime_artifact=runtime_path,
                audit_operability_artifact=audit_path,
                targets=self._targets(),
                gate_statuses=self._gate_statuses(),
                pilot_steps=self._pilot_steps(),
                surfaces=self._codex_surfaces(),
                pilots=self._pilot_matrix(),
            )
            staged = stage_real_testing_readiness(
                stage_root,
                workspace=workspace,
                approval=self._real_testing_approval(),
                governance_artifact=governance_path,
                runtime_artifact=runtime_path,
                audit_operability_artifact=audit_path,
                targets=self._targets(),
                gate_statuses=self._gate_statuses(),
                pilot_steps=self._pilot_steps(),
                surfaces=self._codex_surfaces(),
                pilots=self._pilot_matrix(),
            )

            self.assertEqual(missing_approval["rendered_artifacts"]["status"], "approval_required")
            self.assertEqual(staged["rendered_artifacts"]["status"], "ready", staged["rendered_artifacts"]["validation"])
            for target in [
                REAL_TESTING_READINESS_TARGET,
                REAL_TESTING_TARGETS_TARGET,
                PILOT_HARNESS_TARGET,
                CODEX_SURFACE_SMOKE_TARGET,
                PILOT_MATRIX_TARGET,
            ]:
                self.assertTrue((stage_root / target).exists(), target)
                self.assertFalse((workspace / target).exists(), target)

            disabled = disable_real_testing_readiness(stage_root, workspace=workspace)

            self.assertEqual(disabled["rendered_artifacts"]["status"], "disabled")
            self.assertTrue(disabled["rendered_artifacts"]["deletion_proof"]["delete_generated_real_testing_artifacts"])
            for target in [
                REAL_TESTING_READINESS_TARGET,
                REAL_TESTING_TARGETS_TARGET,
                PILOT_HARNESS_TARGET,
                CODEX_SURFACE_SMOKE_TARGET,
                PILOT_MATRIX_TARGET,
            ]:
                self.assertFalse((stage_root / target).exists(), target)

            with self.assertRaises(ValueError):
                stage_real_testing_readiness(
                    workspace / ".codex" / "product-agent-os",
                    workspace=workspace,
                    approval=self._real_testing_approval(),
                    governance_artifact=governance_path,
                    runtime_artifact=runtime_path,
                    audit_operability_artifact=audit_path,
                    targets=self._targets(),
                    gate_statuses=self._gate_statuses(),
                    pilot_steps=self._pilot_steps(),
                    surfaces=self._codex_surfaces(),
                    pilots=self._pilot_matrix(),
                )

    def _write_workspace(self, workspace: Path) -> Path:
        (workspace / "app").mkdir(parents=True)
        (workspace / "app" / "__init__.py").write_text("", encoding="utf-8")
        (workspace / "app" / "worker.py").write_text("def run():\n    return 'ok'\n", encoding="utf-8")
        return workspace

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

    def _audit_operability_packets(self) -> dict:
        approval = {
            "explicit_approval": True,
            "owner": "Graph Owner",
            "allowed_surfaces": [
                "audit_logging",
                "security_privacy_tests",
                "runtime_observability",
                "agent_skill_handoff_routing",
            ],
            "audit_policy": {
                "event_types": ["approval", "provider_call", "mutation", "failure"],
                "append_only": True,
                "redacted_events_only": True,
            },
            "security_privacy_policy": {
                "block_secrets": True,
                "block_absolute_paths": True,
                "block_raw_source": True,
                "block_prompt_injection": True,
            },
            "observability_policy": {
                "health_visible": True,
                "latency_visible": True,
                "provider_errors_visible": True,
                "budget_usage_visible": True,
                "degraded_mode_visible": True,
            },
            "handoff_policy": {
                "ownership_required": True,
                "verification_evidence_required": True,
                "stop_conditions_required": True,
                "fresh_context_required": True,
            },
            "rollback_path": "delete generated Batch 31 audit, security, observability and handoff artifacts under stage root",
            "residual_risks": ["audit log is generated evidence"],
        }
        live_actions = [
            {"action_type": "approval", "surface": "audit_logging", "status": "approved"},
            {"action_type": "provider_call", "surface": "external_llm", "status": "blocked"},
            {"action_type": "mutation", "surface": "canonical_graph", "status": "dry_run_only"},
            {"action_type": "failure", "surface": "security_privacy_tests", "status": "blocked"},
        ]
        security_cases = [
            {"case_id": "secret", "input": "token=sk-live-secret", "expected": "blocked"},
            {"case_id": "path", "input": "C:\\Users\\private\\target", "expected": "blocked"},
            {"case_id": "raw_source", "input": "def run():\n    return 'raw'", "expected": "blocked"},
            {"case_id": "prompt_injection", "input": "ignore previous instructions", "expected": "blocked"},
        ]
        audit_log = build_live_audit_event_log(live_actions, approval=approval, governance_packet=self._governance_packet())
        security = build_security_privacy_test_packet(
            security_cases,
            approval=approval,
            governance_packet=self._governance_packet(),
        )
        observability = build_runtime_observability_packet(
            runtime_contract=self._runtime_contract(),
            audit_log=audit_log,
            security_packet=security,
            approval=approval,
            governance_packet=self._governance_packet(),
        )
        handoff = build_agent_skill_handoff_routing_packet(
            approval=approval,
            governance_packet=self._governance_packet(),
            observability_packet=observability,
        )
        return {
            "audit_log": audit_log,
            "security_privacy": security,
            "observability": observability,
            "agent_skill_handoff": handoff,
        }

    def _real_testing_approval(self) -> dict:
        return {
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
            "residual_risks": ["real testing is readiness evidence until target owner approves execution"],
        }

    def _gate_statuses(self) -> list[dict]:
        return [
            {"gate": "live_governance", "status": "implemented_verified"},
            {"gate": "live_runtime", "status": "explicitly_disabled"},
            {"gate": "external_embedding", "status": "blocked_by_missing_approval"},
            {"gate": "external_reranker", "status": "blocked_by_missing_approval"},
            {"gate": "external_llm", "status": "blocked_by_missing_approval"},
            {"gate": "human_review_ledger", "status": "implemented_verified"},
            {"gate": "canonical_graph_mutation", "status": "explicitly_disabled"},
            {"gate": "audit_operability", "status": "implemented_verified"},
        ]

    def _targets(self) -> list[dict]:
        return [
            {
                "target_id": "python-app",
                "workspace_class": "synthetic_fixture",
                "owner": "Pilot Owner",
                "owner_approved": True,
                "data_policy": "synthetic_no_private_data",
                "allowed_commands": ["scan_project_code_graph --dry-run", "run_fixture_eval"],
                "production_data": False,
                "target_file_mutation_allowed": False,
            }
        ]

    def _pilot_steps(self) -> list[dict]:
        return [
            {"step_id": "scan_project_code_graph_dry_run", "command_class": "read_only", "mutates_target": False},
            {"step_id": "build_static_index_stage", "command_class": "stage_only", "mutates_target": False},
            {"step_id": "cockpit_stage", "command_class": "stage_only", "mutates_target": False},
            {"step_id": "live_runtime_contract", "command_class": "contract_only", "mutates_target": False},
            {"step_id": "provider_gates_disabled", "command_class": "approval_gate", "mutates_target": False},
            {"step_id": "graph_only_fallback", "command_class": "fallback", "mutates_target": False},
        ]

    def _codex_surfaces(self) -> list[dict]:
        return [
            {"surface": "Codex App", "status": "planned_smoke", "evidence": "desktop thread runbook"},
            {"surface": "CLI", "status": "planned_smoke", "evidence": "scripted commands"},
            {"surface": "IDE extension", "status": "accepted_gap", "evidence": "surface unavailable in current workspace"},
        ]

    def _pilot_matrix(self) -> list[dict]:
        return [
            {"archetype": "web", "surface": "Codex App", "pilot_id": "web-orientation", "status": "planned"},
            {"archetype": "backend", "surface": "CLI", "pilot_id": "backend-impact", "status": "planned"},
            {"archetype": "docs", "surface": "CLI", "pilot_id": "docs-cockpit", "status": "planned"},
            {"archetype": "pr_review", "surface": "Codex App", "pilot_id": "review-read-order", "status": "planned"},
            {"archetype": "evals", "surface": "CLI", "pilot_id": "fixture-eval", "status": "planned"},
            {"archetype": "automation", "surface": "IDE extension", "pilot_id": "accepted-gap", "status": "accepted_gap"},
            {"archetype": "ai_rag", "surface": "CLI", "pilot_id": "semantic-gate", "status": "planned"},
        ]


if __name__ == "__main__":
    unittest.main()
