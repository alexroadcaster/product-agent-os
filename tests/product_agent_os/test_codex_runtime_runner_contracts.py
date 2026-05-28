import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.contracts import (  # noqa: E402
    AGENT_SKILL_METRICS_LOOP_LIMITS,
    ALLOWED_RUNNER_STATUSES,
    ALLOWED_RUNTIME_SURFACES,
    ALLOWED_WRITE_POLICIES,
    METHODOLOGY_HIGH_RISK_ACTIONS,
    METHODOLOGY_PACKET_LIMITS,
    REQUIRED_RESULT_FIELDS,
    REQUIRED_METHODOLOGY_PACKET_KEYS,
    build_methodology_packet,
    build_result,
    classify_methodology_high_risk_actions,
    validate_agent_skill_metrics_loop_packet,
    validate_methodology_packet,
    validate_runner_request,
    validate_runner_result,
)
from product_agent_os.question_protocol import MAX_TOTAL_QUESTIONS  # noqa: E402


class CodexRuntimeRunnerContractsTest(unittest.TestCase):
    def test_contract_enums_are_codex_only(self):
        self.assertIn("Codex App", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("CLI", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("IDE extension", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("subagent", ALLOWED_RUNTIME_SURFACES)
        self.assertIn("skill", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("Agents SDK", ALLOWED_RUNTIME_SURFACES)
        self.assertNotIn("api", {item.lower() for item in ALLOWED_RUNTIME_SURFACES})
        self.assertEqual(ALLOWED_WRITE_POLICIES, ["read_only", "staged_only", "approved_write", "blocked"])
        self.assertIn("route_ready", ALLOWED_RUNNER_STATUSES)

    def test_valid_runner_request_passes(self):
        request = self._valid_request()

        self.assertEqual(validate_runner_request(request), [])

    def test_runner_request_rejects_unknown_surface_and_writes_without_approval(self):
        request = self._valid_request()
        request["routing"]["preferred_surface"] = "external service"
        request["routing"]["allow_workspace_writes"] = True
        request["approval"]["approval_status"] = "required"

        errors = validate_runner_request(request)

        self.assertIn("routing.preferred_surface:unknown", errors)
        self.assertIn("routing.allow_workspace_writes:approval_required", errors)

    def test_build_result_returns_complete_shape(self):
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(list(result.keys()), REQUIRED_RESULT_FIELDS)
        self.assertEqual(validate_runner_result(result), [])
        self.assertEqual(result["redactions"], {"count": 0, "categories": []})

    def test_route_packet_accepts_compact_methodology_packet_without_result_shape_change(self):
        packet = build_methodology_packet(self._methodology_intelligence())
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only", "methodology_packet": packet},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(list(result.keys()), REQUIRED_RESULT_FIELDS)
        self.assertEqual(list(packet.keys()), REQUIRED_METHODOLOGY_PACKET_KEYS)
        self.assertEqual(validate_runner_result(result), [])
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertLessEqual(len(packet["recommendation_groups"]), METHODOLOGY_PACKET_LIMITS["recommendation_groups"])
        self.assertLessEqual(len(packet["questions_for_owner"]), METHODOLOGY_PACKET_LIMITS["questions_for_owner"])
        self.assertEqual(packet["safe_next_action"], "Stage security-risk-review.md before implementation.")

    def test_methodology_packet_validation_rejects_invalid_missing_oversized_and_non_read_only(self):
        self.assertIn("methodology_packet:invalid", validate_methodology_packet("not a packet"))

        missing = self._valid_methodology_packet()
        del missing["safe_next_action"]
        self.assertIn("methodology_packet.safe_next_action:required", validate_methodology_packet(missing))

        oversized = self._valid_methodology_packet()
        oversized["recommendation_groups"] = [{}] * (METHODOLOGY_PACKET_LIMITS["recommendation_groups"] + 1)
        self.assertIn(
            "methodology_packet.recommendation_groups:too_many",
            validate_methodology_packet(oversized),
        )

        write_attempt = self._valid_methodology_packet()
        write_attempt["write_policy"] = "staged_only"
        self.assertIn("methodology_packet.write_policy:must_be_read_only", validate_methodology_packet(write_attempt))

    def test_result_rejects_completion_claim_without_evidence(self):
        result = build_result(
            status="completed",
            workspace="C:/workspace/synthetic",
            lifecycle_state="review_ready",
            route_packet={"write_policy": "staged_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="No action.",
        )

        errors = validate_runner_result(result)

        self.assertIn("verification_evidence:required_for_completed", errors)

    def test_result_rejects_detection_only_methodology_packet_as_completion_evidence(self):
        packet = self._valid_methodology_packet()
        packet["status"] = "present_unverified"
        result = build_result(
            status="completed",
            workspace="C:/workspace/synthetic",
            lifecycle_state="review_ready",
            route_packet={"write_policy": "staged_only", "methodology_packet": packet},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="No action.",
        )

        errors = validate_runner_result(result)

        self.assertIn("verification_evidence:required_for_completed", errors)
        self.assertIn("methodology_packet:detection_not_completion", errors)

    def test_result_rejects_malformed_methodology_packet_with_stable_errors(self):
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={
                "write_policy": "read_only",
                "methodology_packet": {"write_policy": "staged_only"},
            },
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        errors = validate_runner_result(result)

        self.assertIn("methodology_packet.safe_next_action:required", errors)
        self.assertIn("methodology_packet.write_policy:must_be_read_only", errors)

    def test_old_schema_v1_result_without_methodology_packet_remains_valid(self):
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(validate_runner_result(result), [])

    def test_additive_route_fields_stay_schema_v1_and_invalid_finish_options_fail_stably(self):
        question_queue = self._valid_question_queue()
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={
                "write_policy": "read_only",
                "methodology_packet": self._valid_methodology_packet(),
                "question_queue": question_queue,
                "status_snapshot_ref": {
                    "kind": "staged_artifact",
                    "path": ".codex/product-agent-os/status.json",
                    "digest": "sha256:synthetic",
                },
                "finish_options": ["read_only_audit", "ask_owner", "run_verification", "stop_blocked"],
                "first_response_contract": {
                    "next_blocking_question": question_queue["next_blocking_question"],
                    "question_counts": question_queue["summary"],
                    "question_summary": ["1 blocking", "0 recommended", "0 optional"],
                    "safe_next_action": "Stage security-risk-review.md before implementation.",
                    "evidence_gaps": ["owner-reviewed evidence"],
                    "approval_boundary": "read_only",
                    "finish_options": ["read_only_audit", "ask_owner", "run_verification", "stop_blocked"],
                },
            },
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )
        malformed = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only", "finish_options": "stage_proposal"},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(validate_runner_result(result), [])
        self.assertNotIn("questions", result["route_packet"]["first_response_contract"])
        self.assertIn("route_packet.finish_options:invalid", validate_runner_result(malformed))

    def test_route_packet_accepts_bounded_agent_skill_metrics_loop_without_schema_break(self):
        metrics_loop = self._valid_metrics_loop_packet()
        result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={
                "write_policy": "read_only",
                "agent_skill_metrics_loop": metrics_loop,
                "finish_options": [
                    "read_only_audit",
                    "ask_owner",
                    "stage_metrics_report",
                    "request_owner_review",
                    "block_automation_promotion",
                    "investigate_regression",
                    "run_verification",
                    "stop_blocked",
                ],
                "first_response_contract": {
                    "safe_next_action": "Stage metrics report for owner review.",
                    "finish_options": [
                        "read_only_audit",
                        "ask_owner",
                        "stage_metrics_report",
                        "request_owner_review",
                        "block_automation_promotion",
                        "investigate_regression",
                        "run_verification",
                        "stop_blocked",
                    ],
                },
            },
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Stage metrics report for owner review.",
        )

        self.assertEqual(result["schema_version"], 1)
        self.assertEqual(validate_runner_result(result), [])
        self.assertEqual(validate_agent_skill_metrics_loop_packet(metrics_loop), [])
        self.assertLessEqual(
            len(metrics_loop["report_refs"]),
            AGENT_SKILL_METRICS_LOOP_LIMITS["report_refs"],
        )

    def test_metrics_loop_packet_validation_rejects_oversized_external_or_apply_actions(self):
        oversized = self._valid_metrics_loop_packet()
        oversized["report_refs"] = [
            {"kind": "staged_artifact", "path": f".codex/eval-reports/report-{index}.html"}
            for index in range(AGENT_SKILL_METRICS_LOOP_LIMITS["report_refs"] + 1)
        ]
        external = self._valid_metrics_loop_packet()
        external["report_refs"] = [{"kind": "external_ref", "path": "https://example.invalid/report.html"}]
        apply_action = self._valid_metrics_loop_packet()
        apply_action["update_candidate_summary"]["top_candidates"] = [
            {"candidate_id": "unsafe", "action": "apply_patch", "requires_rollback": True}
        ]

        self.assertIn(
            "agent_skill_metrics_loop.report_refs:too_many",
            validate_agent_skill_metrics_loop_packet(oversized),
        )
        self.assertIn(
            "agent_skill_metrics_loop.report_refs[0].kind:forbidden_external_ref",
            validate_agent_skill_metrics_loop_packet(external),
        )
        self.assertIn(
            "agent_skill_metrics_loop.update_candidate_summary.top_candidates[0].action:apply_forbidden",
            validate_agent_skill_metrics_loop_packet(apply_action),
        )

    def test_route_packet_rejects_invalid_question_queue_without_relaxing_methodology_packet(self):
        oversized = self._valid_question_queue()
        oversized["questions"] = oversized["questions"] * (MAX_TOTAL_QUESTIONS + 1)
        invalid_answer_type = self._valid_question_queue()
        invalid_answer_type["questions"][0]["answer_type"] = "freeform_secret"
        methodology_with_unknown = self._valid_methodology_packet()
        methodology_with_unknown["question_queue"] = self._valid_question_queue()

        oversized_result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only", "question_queue": oversized},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )
        invalid_answer_type_result = build_result(
            status="route_ready",
            workspace="C:/workspace/synthetic",
            lifecycle_state="quality_gate",
            route_packet={"write_policy": "read_only", "question_queue": invalid_answer_type},
            source_policy_status="ok",
            approval_status="not_required",
            next_action="Run risk-reviewer.",
        )

        self.assertIn("route_packet.question_queue.questions:too_many", validate_runner_result(oversized_result))
        self.assertIn(
            "route_packet.question_queue.questions[0].answer_type:unknown",
            validate_runner_result(invalid_answer_type_result),
        )
        self.assertIn("methodology_packet.question_queue:unknown", validate_methodology_packet(methodology_with_unknown))

    def test_methodology_high_risk_action_taxonomy_is_structured_and_false_positive_safe(self):
        packet = self._valid_methodology_packet()
        packet["safe_next_action"] = (
            "Create release, push branch, run security scan, access production data, "
            "run DB migration and activate automation."
        )
        safe_packet = self._valid_methodology_packet()
        safe_packet["safe_next_action"] = "Review deployment-plan.md as a read-only proposal."

        self.assertEqual(
            METHODOLOGY_HIGH_RISK_ACTIONS,
            [
                "publish",
                "deploy",
                "tag",
                "release_create",
                "pr_or_push",
                "package_registry_mutation",
                "marketplace_submission",
                "security_scan",
                "production_data_access",
                "db_migration",
                "automation_activation",
                "external_system_mutation",
            ],
        )
        self.assertEqual(
            classify_methodology_high_risk_actions(packet),
            [
                "release_create",
                "pr_or_push",
                "security_scan",
                "production_data_access",
                "db_migration",
                "automation_activation",
            ],
        )
        self.assertEqual(classify_methodology_high_risk_actions(safe_packet), [])

    def _valid_request(self):
        return {
            "schema_version": 1,
            "workspace": "C:/workspace/synthetic",
            "task": {
                "goal": "Prepare next Product-Agent OS action.",
                "lifecycle_state": "quality_gate",
                "constraints": ["Do not write files."],
                "allowed_sources": ["official docs", "repo artifacts"],
                "expected_artifacts": ["codex_runner_result"],
            },
            "routing": {
                "preferred_surface": "CLI",
                "allow_subagents": False,
                "allow_workspace_writes": False,
            },
            "approval": {
                "required": False,
                "approval_file": "",
                "approval_status": "not_required",
            },
        }

    def _valid_methodology_packet(self):
        return {
            "methodology_domains": [{"id": "security", "status": "applicable_missing"}],
            "methodology_recommendations": [
                {
                    "domain": "security",
                    "artifact": "security-risk-review.md",
                    "priority": "P1_high_risk",
                    "safe_next_action": "Stage security-risk-review.md before implementation.",
                }
            ],
            "recommendation_groups": [
                {
                    "artifact": "security-risk-review.md",
                    "owner_domain": "security",
                    "consumer_domains": ["quality_testing_evals"],
                    "priority": "P1_high_risk",
                    "safe_next_action": "Stage security-risk-review.md before implementation.",
                }
            ],
            "questions_for_owner": ["Who owns the security review?"],
            "safe_next_action": "Stage security-risk-review.md before implementation.",
            "semantic_evidence_sufficiency": {
                "status": "present_unverified",
                "required_evidence": ["owner-reviewed evidence"],
            },
            "source_artifact_ledger": [{"artifact": "security-risk-review.md", "decision": "canonical_template"}],
            "write_policy": "read_only",
            "status": "present_unverified",
        }

    def _valid_metrics_loop_packet(self):
        return {
            "schema_version": 1,
            "write_policy": "read_only",
            "status": "present_unverified",
            "summary": {
                "target_count": 2,
                "overall_status": "blocked_by_guardrail",
                "cadence_level": "L1",
            },
            "report_refs": [
                {
                    "kind": "staged_artifact",
                    "path": ".codex/eval-reports/agent-skill-evaluation-report.html",
                    "digest": "sha256:" + "a" * 64,
                }
            ],
            "cadence": {"level": "L1", "recommended": ["weekly"]},
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
        }

    def _valid_question_queue(self):
        return {
            "schema_version": 1,
            "write_policy": "read_only",
            "runtime_status": "route_ready",
            "policy": {
                "max_total_questions": 8,
                "max_blocking_questions_in_first_response": 1,
                "supported_priorities": ["blocking", "recommended", "optional"],
                "supported_categories": ["scope", "product", "verification", "approval", "ownership", "risk", "release"],
                "supported_answer_types": [
                    "text",
                    "single_choice",
                    "single_choice_or_text",
                    "multi_choice",
                    "approval",
                    "not_applicable_or_gap",
                ],
            },
            "questions": [
                {
                    "id": "q_ownership_synthetic",
                    "text": "Who owns the security review?",
                    "priority": "blocking",
                    "category": "ownership",
                    "answer_type": "text",
                    "artifact": "security-risk-review.md",
                    "owner_domain": "security",
                    "source": {
                        "kind": "methodology_packet",
                        "key": "methodology_gate_owner",
                        "block": "questions_for_owner",
                        "artifact": "security-risk-review.md",
                    },
                    "sequence": 1,
                }
            ],
            "next_blocking_question": {
                "id": "q_ownership_synthetic",
                "text": "Who owns the security review?",
                "priority": "blocking",
                "category": "ownership",
                "answer_type": "text",
                "artifact": "security-risk-review.md",
                "owner_domain": "security",
                "source": {
                    "kind": "methodology_packet",
                    "key": "methodology_gate_owner",
                    "block": "questions_for_owner",
                    "artifact": "security-risk-review.md",
                },
                "sequence": 1,
            },
            "summary": {"total": 1, "blocking": 1, "recommended": 0, "optional": 0, "remaining": 0},
        }

    def _methodology_intelligence(self):
        return {
            "status": "present_unverified",
            "write_policy": "read_only",
            "methodology_domains": [
                {"id": "security", "status": "applicable_missing"},
                {"id": "delivery_release_operations", "status": "applicable_missing"},
            ],
            "recommendations": [
                {
                    "domain": "security",
                    "artifact": "security-risk-review.md",
                    "priority": "P1_high_risk",
                    "safe_next_action": "Stage security-risk-review.md before implementation.",
                }
                for _ in range(METHODOLOGY_PACKET_LIMITS["methodology_recommendations"] + 3)
            ],
            "recommendation_groups": [
                {
                    "artifact": f"artifact-{index}.md",
                    "owner_domain": "security",
                    "consumer_domains": ["quality_testing_evals"],
                    "priority": "P1_high_risk",
                    "safe_next_action": "Stage security-risk-review.md before implementation.",
                }
                for index in range(METHODOLOGY_PACKET_LIMITS["recommendation_groups"] + 3)
            ],
            "questions_for_owner": [
                f"Who owns methodology decision {index}?"
                for index in range(METHODOLOGY_PACKET_LIMITS["questions_for_owner"] + 3)
            ],
            "methodology_synthesis": {
                "safe_next_action": "Stage security-risk-review.md before implementation.",
                "semantic_evidence_sufficiency": {
                    "status": "present_unverified",
                    "required_evidence": ["owner-reviewed evidence"],
                },
                "source_artifact_ledger": [
                    {"artifact": "security-risk-review.md", "decision": "canonical_template"}
                ],
            },
        }


if __name__ == "__main__":
    unittest.main()
