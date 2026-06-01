import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.context_loader import load_control_plane_context  # noqa: E402
from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.guards import validate_approval_boundary, validate_route_packet  # noqa: E402
from codex_runtime_runner.routes import apply_runner_status_to_route, plan_route  # noqa: E402
from codex_runtime_runner.state import infer_lifecycle_state  # noqa: E402
from product_agent_os.question_protocol import MAX_TOTAL_QUESTIONS  # noqa: E402


class CodexRuntimeRunnerStateRoutesTest(unittest.TestCase):
    def test_missing_agents_is_uninitialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            context = load_control_plane_context(Path(tmp))

        self.assertEqual(infer_lifecycle_state(context, {}), "uninitialized")

    def test_missing_plan_after_requirements_is_requirements_ready(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace, omit={"PLAN.md"})
            context = load_control_plane_context(workspace)

        self.assertEqual(infer_lifecycle_state(context, {}), "requirements_ready")

    def test_request_lifecycle_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace)
            context = load_control_plane_context(workspace)

        self.assertEqual(
            infer_lifecycle_state(context, {"task": {"lifecycle_state": "quality_gate"}}),
            "quality_gate",
        )

    def test_route_maps_quality_gate_to_risk_reviewer(self):
        route = plan_route("quality_gate", allow_subagents=False)

        self.assertEqual(route["recommended_skill"], "risk-reviewer")
        self.assertEqual(route["recommended_subagent_role"], "")
        self.assertEqual(route["write_policy"], "read_only")
        self.assertIn("python", " ".join(route["verification"]))

    def test_route_can_carry_usage_mode_and_first_response_contract(self):
        usage_mode = {
            "primary": "greenfield_idea",
            "secondary": [],
            "confidence": "high",
            "reasons": ["workspace has no implementation files"],
            "fallback": "standard_feature",
            "first_response_contract": [
                "mode",
                "confidence",
                "next smallest action",
                "minimum artifacts",
                "evidence gaps",
                "approval boundary",
            ],
            "minimum_artifacts": ["greenfield idea brief"],
            "behavioral_eval_cases": ["first-run-response"],
        }

        route = plan_route("uninitialized", allow_subagents=False, usage_mode=usage_mode)

        self.assertEqual(route["usage_mode"]["primary"], "greenfield_idea")
        self.assertEqual(route["first_response_contract"]["mode"], "greenfield_idea")
        self.assertEqual(route["first_response_contract"]["minimum_artifacts"], ["greenfield idea brief"])
        self.assertEqual(route["first_response_contract"]["approval_boundary"], "read_only")
        self.assertEqual(route["first_response_contract"]["required_fields"], usage_mode["first_response_contract"])
        self.assertIn("evidence gaps", route["first_response_contract"]["required_fields"])

    def test_route_carries_compact_methodology_packet_and_finish_options(self):
        route = plan_route(
            "requirements_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )

        packet = route["methodology_packet"]
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertEqual(packet["safe_next_action"], "Stage security-risk-review.md before implementation.")
        self.assertTrue(packet["recommendation_groups"])
        self.assertTrue(packet["questions_for_owner"])
        self.assertEqual(route["finish_options"], ["read_only_audit", "ask_owner", "stage_proposal", "run_verification", "stop_blocked"])
        self.assertIn("question_queue", route)
        self.assertLessEqual(len(route["question_queue"]["questions"]), MAX_TOTAL_QUESTIONS)
        self.assertEqual(route["first_response_contract"]["next_blocking_question"], route["question_queue"]["next_blocking_question"])
        self.assertEqual(route["first_response_contract"]["question_counts"], route["question_queue"]["summary"])
        self.assertEqual(route["first_response_contract"]["safe_next_action"], packet["safe_next_action"])
        self.assertEqual(route["first_response_contract"]["finish_options"], route["finish_options"])

    def test_first_response_contract_exposes_compact_methodology_fields_without_gate_dump(self):
        route = plan_route(
            "requirements_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )
        first_response = route["first_response_contract"]

        self.assertEqual(first_response["next_blocking_question"]["text"], "Who owns the security review?")
        self.assertEqual(first_response["question_counts"]["blocking"], 1)
        self.assertEqual(first_response["question_summary"][0], "1 blocking question")
        self.assertEqual(first_response["safe_next_action"], "Stage security-risk-review.md before implementation.")
        self.assertIn("owner-reviewed evidence", first_response["evidence_gaps"])
        self.assertIn("finish_options", first_response)
        self.assertIn("approval_boundary", first_response)
        self.assertNotIn("owner_questions", first_response)
        self.assertNotIn("questions", first_response)
        self.assertNotIn("methodology_domains", first_response)
        self.assertNotIn("methodology_gates", first_response)

    def test_read_only_route_does_not_stage_from_recommendation_only_methodology_packet(self):
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )

        self.assertEqual(route["write_policy"], "read_only")
        self.assertNotIn("stage_proposal", route["finish_options"])
        self.assertNotIn("security-risk-review.md", route["expected_outputs"])

    def test_high_risk_methodology_action_requires_approval_without_external_output(self):
        route = plan_route(
            "review_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(
                artifact="release-readiness.md",
                safe_next_action="Publish package to the package registry.",
            ),
        )

        approval_errors = validate_approval_boundary(route, {"approval_status": "not_required"})

        self.assertIn("request_approval", route["finish_options"])
        self.assertIn("approval:required_for_methodology_action", approval_errors)
        self.assertTrue(route["approval_requirements"])
        self.assertNotIn("publish", " ".join(route["expected_outputs"]).lower())

    def test_runner_status_maps_finish_options_without_staging_for_blocked_or_context_states(self):
        staged_route = plan_route(
            "requirements_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(),
        )

        needs_context = apply_runner_status_to_route(staged_route, "needs_context")
        blocked = apply_runner_status_to_route(staged_route, "blocked")
        needs_approval = apply_runner_status_to_route(staged_route, "needs_approval")

        self.assertEqual(needs_context["finish_options"], ["read_only_audit", "ask_owner", "stop_blocked"])
        self.assertNotIn("stage_proposal", blocked["finish_options"])
        self.assertNotIn("stage_proposal", needs_context["finish_options"])
        self.assertIn("request_approval", needs_approval["finish_options"])
        self.assertEqual(
            needs_context["next_action"],
            "Collect missing control-plane context before staging proposals.",
        )
        self.assertEqual(needs_context["first_response_contract"]["finish_options"], needs_context["finish_options"])

    def test_automation_maturity_blocks_automation_promoter_route(self):
        route = plan_route(
            "learning_ready",
            allow_subagents=False,
            methodology_intelligence=self._methodology_intelligence(
                artifact="automation-candidate.md",
                safe_next_action="Promote this workflow to an active automation.",
            ),
        )

        errors = validate_route_packet(route)

        self.assertEqual(route["recommended_skill"], "learning-loop-maintainer")
        self.assertNotIn("stage_proposal", route["finish_options"])
        self.assertIn("automation:maturity_evidence_required", errors)

    def test_metrics_loop_route_options_are_review_only_and_block_automation(self):
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            agent_skill_metrics_loop={
                "schema_version": 1,
                "write_policy": "read_only",
                "status": "regression_detected",
                "summary": {
                    "target_count": 2,
                    "overall_status": "blocked_by_guardrail",
                    "cadence_level": "L2",
                },
                "report_refs": [
                    {
                        "kind": "staged_artifact",
                        "path": ".codex/eval-reports/agent-skill-evaluation-report.html",
                    }
                ],
                "cadence": {"level": "L2", "recommended": ["daily"]},
                "update_candidate_summary": {
                    "candidate_count": 1,
                    "top_candidates": [
                        {
                            "candidate_id": "candidate-skill-review",
                            "priority": "high",
                            "requires_rollback": True,
                        }
                    ],
                },
                "automation_policy": "candidate_only",
                "source_policy": "generated summaries are not source of truth",
            },
        )

        self.assertIn("stage_metrics_report", route["finish_options"])
        self.assertIn("request_owner_review", route["finish_options"])
        self.assertIn("block_automation_promotion", route["finish_options"])
        self.assertIn("investigate_regression", route["finish_options"])
        self.assertNotIn("apply_update", route["finish_options"])
        self.assertNotIn("activate_automation", route["finish_options"])
        self.assertEqual(route["agent_skill_metrics_loop"]["automation_policy"], "candidate_only")
        self.assertIn(
            "metrics loop reports are staged evidence only",
            route["stop_conditions"],
        )
        self.assertEqual(route["first_response_contract"]["finish_options"], route["finish_options"])

    def test_stale_or_unsupported_graph_routes_to_source_reads_or_owner_question(self):
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            project_graph_status={
                "schema_version": 1,
                "write_policy": "read_only",
                "status": "stale",
                "freshness": {"status": "stale", "scan_id": "scan-old"},
                "counts": {"nodes": 25, "edges": 10, "observations": 40, "omitted_nodes": 0},
                "unsupported_languages": [{"language": "typescript", "file_count": 20, "status": "file_only"}],
                "artifact_refs": [
                    {"kind": "staged_artifact", "path": ".codex/product-agent-os/project-code-graph.json"}
                ],
                "top_gaps": [
                    {
                        "id": "unsupported-typescript",
                        "severity": "high",
                        "safe_next_action": "Read source files before impact claims.",
                    }
                ],
                "safe_next_action": "Read source files before acting on stale graph output.",
                "source_policy": "generated graph is not source of truth",
            },
        )
        errors = validate_route_packet(route)

        self.assertEqual(errors, [])
        self.assertEqual(route["write_policy"], "read_only")
        self.assertNotIn("stage_proposal", route["finish_options"])
        self.assertIn("Read source files", route["next_action"])
        self.assertEqual(route["project_graph_status"]["status"], "stale")
        self.assertEqual(route["first_response_contract"]["project_graph_summary"]["status"], "stale")
        self.assertEqual(route["first_response_contract"]["project_graph_summary"]["top_gap_count"], 1)
        self.assertNotIn("nodes", route["first_response_contract"]["project_graph_summary"])

    def test_current_graph_with_low_severity_gap_does_not_override_route_action(self):
        route = plan_route(
            "quality_gate",
            allow_subagents=False,
            project_graph_status={
                "schema_version": 1,
                "write_policy": "read_only",
                "status": "current",
                "freshness": {"status": "current", "scan_id": "scan-current"},
                "counts": {"nodes": 25, "edges": 10, "observations": 40, "omitted_nodes": 0},
                "unsupported_languages": [],
                "artifact_refs": [
                    {"kind": "staged_artifact", "path": ".codex/product-agent-os/project-code-graph.json"}
                ],
                "top_gaps": [
                    {
                        "id": "small-generated-file-note",
                        "severity": "low",
                        "safe_next_action": "Read source files before edits.",
                    }
                ],
                "safe_next_action": "Use graph as orientation only.",
                "source_policy": "generated graph is not source of truth",
            },
        )

        self.assertEqual(route["next_action"], "Review risks and verification evidence.")
        self.assertEqual(route["first_response_contract"]["project_graph_summary"]["top_gap_count"], 1)

    def test_ownership_conflict_routes_parallel_builder_to_agent_team_designer(self):
        route = plan_route(
            "build_active",
            allow_subagents=True,
            methodology_intelligence=self._methodology_intelligence(
                owner_domain="security_privacy_compliance",
                extra_group={
                    "artifact": "release-readiness.md",
                    "owner_domain": "delivery_release_operations",
                    "consumer_domains": ["security_privacy_compliance"],
                    "priority": "P1_high_risk",
                    "safe_next_action": "Resolve release and security ownership before build.",
                },
            ),
        )
        errors = validate_route_packet(route)

        self.assertEqual(route["recommended_skill"], "agent-team-designer")
        self.assertEqual(route["recommended_subagent_role"], "")
        self.assertEqual(route["write_policy"], "staged_only")
        self.assertIn("fresh_context_handoff", route["required_inputs"])
        self.assertIn("ownership:parallelism_requires_handoff", errors)
        self.assertIn("stage_proposal", route["finish_options"])

    def test_run_contract_preserves_methodology_intelligence_from_workspace_discovery(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self._write_control_plane(workspace)
            src = workspace / "src"
            src.mkdir()
            (src / "payment_api.py").write_text("def charge(): pass\n", encoding="utf-8")
            result = run_contract(
                workspace,
                intent_hint="security-sensitive payment release",
            )

        packet = result["route_packet"]["methodology_packet"]
        self.assertTrue(packet["methodology_domains"])
        self.assertTrue(packet["recommendation_groups"])
        self.assertTrue(packet["questions_for_owner"])
        self.assertTrue(packet["safe_next_action"])
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertIn("finish_options", result["route_packet"])

    def test_build_active_uses_builder_subagent_and_requires_approval(self):
        route = plan_route("build_active", allow_subagents=True)

        self.assertEqual(route["recommended_skill"], "")
        self.assertEqual(route["recommended_subagent_role"], "builder")
        self.assertEqual(route["write_policy"], "approved_write")
        self.assertTrue(route["approval_requirements"])

    def _methodology_intelligence(
        self,
        *,
        artifact: str = "security-risk-review.md",
        safe_next_action: str = "Stage security-risk-review.md before implementation.",
        owner_domain: str = "security",
        extra_group: dict | None = None,
    ):
        groups = [
            {
                "artifact": artifact,
                "owner_domain": owner_domain,
                "consumer_domains": ["quality_testing_evals"],
                "priority": "P1_high_risk",
                "safe_next_action": safe_next_action,
            }
        ]
        if extra_group:
            groups.append(extra_group)
        return {
            "status": "present_unverified",
            "write_policy": "read_only",
            "methodology_domains": [{"id": owner_domain, "status": "applicable_missing"}],
            "recommendations": [
                {
                    "domain": owner_domain,
                    "artifact": artifact,
                    "priority": "P1_high_risk",
                    "safe_next_action": safe_next_action,
                }
            ],
            "recommendation_groups": groups,
            "questions_for_owner": ["Who owns the security review?"],
            "methodology_synthesis": {
                "safe_next_action": safe_next_action,
                "semantic_evidence_sufficiency": {
                    "status": "present_unverified",
                    "required_evidence": ["owner-reviewed evidence"],
                },
                "source_artifact_ledger": [
                    {"artifact": artifact, "decision": "canonical_template"}
                ],
            },
        }

    def _write_control_plane(self, workspace: Path, omit: set[str] | None = None) -> None:
        omit = omit or set()
        content = {
            "AGENTS.md": "# Rules\n",
            "REQUIREMENTS.md": "# Requirements\n\n## Acceptance Criteria\n\n- Synthetic acceptance.\n",
            "PLAN.md": "# Plan\n\n## Verification\n\n- Run unit tests.\n",
            "TEST.md": "# Test\n\nQuality gates: unit tests.\n",
            "EVALS.md": "# Evals\n\nQuality gates: fixture eval.\n",
            "RUNLOG.md": "# Runlog\n\nNo active lifecycle marker.\n",
        }
        for name, text in content.items():
            if name not in omit:
                (workspace / name).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
