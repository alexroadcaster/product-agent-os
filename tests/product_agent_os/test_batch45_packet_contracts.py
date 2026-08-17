import copy
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs" / "superpowers" / "specs"
REGISTRY_DOCUMENTS = {
    "registry_ru": ROOT / "docs" / "sources" / "registry.md",
    "registry_en": ROOT / "docs" / "sources" / "registry.en.md",
}


def _registry_needles(evidence_id, filename):
    needles = (evidence_id, filename)
    return {"registry_ru": needles, "registry_en": needles}


PACKET_CASES = (
    {
        "name": "m37_review_remediation",
        "path": SPECS / "batch45-review-remediation-summary.json",
        "identity": {
            "task_id": "B45-PCA-M37",
            "evidence_id": "B45-PCA-M37-A01",
        },
        "required": {
            ("status",): "implemented_local_advisory_hardening_docs_sync_only",
            ("scope", "closure_level"): "local_synthetic_hardening_no_promotion_claim",
        },
        "all_false": (("no_unapproved_actions",),),
    },
    {
        "name": "t18_promotion_grade_eval_design",
        "path": SPECS / "batch45-postq4-t18-promotion-grade-eval-design.json",
        "identity": {
            "task_id": "B45-POSTQ4-T18-EVAL-DESIGN-AND-STRICT-SCHEMA",
            "evidence_id": "B45-POSTQ4-T18-A01",
        },
        "required": {
            ("schema_version",): "batch45_postq4_t18_promotion_grade_eval_design_v1",
            ("status",): "implemented_eval_design_strict_schema_no_run",
            ("closure_level",): "docs_contract_ready",
            ("comparison_design", "selected_promotion_grade_comparison_mode"): (
                "same_model_baseline_treatment"
            ),
            (
                "comparison_design",
                "promotion_grade_model_policy",
                "same_model_required_for_baseline_and_treatment",
            ): True,
            (
                "comparison_design",
                "promotion_grade_model_policy",
                "same_reasoning_effort_required_for_baseline_and_treatment",
            ): True,
            (
                "comparison_design",
                "promotion_grade_model_policy",
                "same_tooling_and_runner_required_for_baseline_and_treatment",
            ): True,
            ("comparison_design", "corpus_binding", "task_count"): 8,
            ("strict_output_schema", "schema_id"): (
                "batch45_postq4_promotion_grade_primary_result_v1"
            ),
            ("strict_output_schema", "root_schema", "type"): "object",
            ("scoring_rubric", "promotion_threshold", "minimum_average_score_delta_percent"): 20,
            ("scoring_rubric", "promotion_threshold", "valid_pair_count_required"): 8,
            ("scoring_rubric", "promotion_threshold", "invalid_pair_count_required"): 0,
            ("scoring_rubric", "promotion_threshold", "timeout_count_required"): 0,
            ("reviewer_rubric", "promotion_requires_reviewer_decision"): "promotion_go",
            (
                "invalid_output_handling",
                "pair_policy",
                "reviewer_not_called_for_invalid_pairs",
            ): True,
        },
        "negative": (
            ("approval_and_execution_boundary", "packet_authorizes_future_run"),
            ("approval_and_execution_boundary", "baseline_or_treatment_run_started"),
            ("approval_and_execution_boundary", "reviewer_gate_satisfied"),
            ("scoring_rubric", "promotion_threshold", "critical_privacy_or_unsupported_claim_failures_allowed"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("approval_and_execution_boundary", "next_required_task"): (
                "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY"
            ),
            ("comparison_design", "corpus_binding", "corpus_id"): (
                "B45-POSTQ4-FROZEN-HELDOUT-CORPUS-V1"
            ),
            ("comparison_design", "corpus_binding", "corpus_version"): "v1",
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T18-A01",
            "batch45-postq4-t18-promotion-grade-eval-design.json",
        ),
    },
    {
        "name": "t19_cost_timeout_retention_policy",
        "path": SPECS / "batch45-postq4-t19-cost-timeout-retention-policy.json",
        "identity": {
            "task_id": "B45-POSTQ4-T19-COST-TIMEOUT-RETENTION-POLICY",
            "evidence_id": "B45-POSTQ4-T19-A01",
        },
        "required": {
            ("schema_version",): "batch45_postq4_t19_cost_timeout_retention_policy_v1",
            ("status",): "implemented_cost_timeout_retention_policy_no_run",
            ("closure_level",): "docs_contract_ready",
            ("run_budget_policy", "max_baseline_primary_calls"): 8,
            ("run_budget_policy", "max_treatment_primary_calls"): 8,
            ("run_budget_policy", "max_primary_model_calls"): 16,
            ("run_budget_policy", "max_reviewer_calls_after_valid_pairs"): 1,
            ("run_budget_policy", "max_total_model_or_reviewer_calls"): 17,
            ("run_budget_policy", "max_setup_or_smoke_calls"): 0,
            ("timeout_policy", "per_primary_call_timeout_seconds"): 600,
            ("timeout_policy", "per_reviewer_call_timeout_seconds"): 600,
            ("timeout_policy", "max_total_wall_clock_seconds"): 12000,
            ("timeout_policy", "timeout_count_required_for_promotion"): 0,
            ("timeout_policy", "stop_on_first_primary_timeout"): True,
            ("cost_policy", "concrete_usd_cap_status"): (
                "owner_fill_required_in_T20_exact_approval"
            ),
            ("cost_policy", "abort_when_cost_unknown"): True,
            ("cost_policy", "cost_cap_breach_blocks_promotion"): True,
            ("cost_policy", "approval_not_executable_without_usd_cap"): True,
            ("retry_and_abort_policy", "manual_rerun_requires_new_exact_approval"): True,
            ("retry_and_abort_policy", "aborted_run_cannot_support_promotion"): True,
            ("raw_temp_only_retention_policy", "raw_outputs_temp_only"): True,
            ("raw_temp_only_retention_policy", "repo_raw_retention_bytes_allowed"): 0,
            ("raw_temp_only_retention_policy", "raw_retention_max_hours"): 24,
            ("raw_temp_only_retention_policy", "delete_raw_on_success"): True,
            ("raw_temp_only_retention_policy", "delete_raw_on_abort"): True,
            ("raw_temp_only_retention_policy", "delete_raw_before_git_stage_or_commit"): True,
        },
        "negative": (
            ("run_budget_policy", "max_total_retries"),
            ("timeout_policy", "timed_out_pair_valid_for_scoring"),
            ("retry_and_abort_policy", "automatic_retries_allowed"),
            (
                "t20_exact_approval_requirements",
                "approval_reuse_after_consumed_or_aborted_run_allowed",
            ),
            ("raw_temp_only_retention_policy", "raw_outputs_repo_retention_allowed"),
            ("approval_and_execution_boundary", "packet_authorizes_future_run"),
            ("approval_and_execution_boundary", "baseline_or_treatment_run_started"),
            ("approval_and_execution_boundary", "reviewer_gate_satisfied"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("approval_and_execution_boundary", "next_required_task"): (
                "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET"
            ),
            ("t20_exact_approval_requirements", "next_required_task"): (
                "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET"
            ),
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T19-A01",
            "batch45-postq4-t19-cost-timeout-retention-policy.json",
        ),
    },
    {
        "name": "t20_exact_approval_packet",
        "path": SPECS / "batch45-postq4-t20-promotion-grade-eval-approval-packet.json",
        "identity": {
            "task_id": "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET",
            "evidence_id": "B45-POSTQ4-T20-A01",
        },
        "required": {
            ("schema_version",): "batch45_postq4_t20_promotion_grade_eval_approval_packet_v1",
            ("status",): "exact_approval_packet_ready_for_owner_confirmation_not_run",
            ("closure_level",): "approval_packet_only_not_run",
            ("route",): "exact_approval_packet_only",
            ("approved_if_owner_confirms_exact_text", "model_id"): "gpt-5.5",
            ("approved_if_owner_confirms_exact_text", "model_reasoning_effort"): "high",
            ("approved_if_owner_confirms_exact_text", "comparison_mode"): (
                "same_model_baseline_treatment"
            ),
            ("approved_if_owner_confirms_exact_text", "corpus_id"): (
                "B45-POSTQ4-FROZEN-HELDOUT-CORPUS-V1"
            ),
            ("approved_if_owner_confirms_exact_text", "corpus_version"): "v1",
            ("approved_if_owner_confirms_exact_text", "primary_model_call_cap", "baseline"): 8,
            ("approved_if_owner_confirms_exact_text", "primary_model_call_cap", "treatment"): 8,
            ("approved_if_owner_confirms_exact_text", "primary_model_call_cap", "total_primary"): 16,
            ("approved_if_owner_confirms_exact_text", "reviewer_call_cap"): 1,
            ("approved_if_owner_confirms_exact_text", "max_total_model_or_reviewer_calls"): 17,
            ("approved_if_owner_confirms_exact_text", "max_total_retries"): 0,
            ("approved_if_owner_confirms_exact_text", "per_primary_call_timeout_seconds"): 600,
            ("approved_if_owner_confirms_exact_text", "per_reviewer_call_timeout_seconds"): 600,
            ("approved_if_owner_confirms_exact_text", "max_total_wall_clock_seconds"): 12000,
            ("approved_if_owner_confirms_exact_text", "usd_cost_cap"): 25.0,
            (
                "approved_if_owner_confirms_exact_text",
                "cost_accounting_policy",
                "cost_cap_breach_blocks_promotion",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "cost_accounting_policy",
                "abort_before_next_call_when_estimated_cap_would_be_exceeded",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "valid_pair_count",
            ): 8,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "invalid_pair_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "timeout_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "no_op_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "invalid_json_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "sanitized_rollup_validates",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "raw_outputs_deleted",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "retention",
                "raw_outputs_temp_only",
            ): True,
            ("approved_if_owner_confirms_exact_text", "retention", "repo_raw_retention_bytes_allowed"): 0,
            ("approved_if_owner_confirms_exact_text", "retention", "raw_retention_max_hours"): 24,
            ("approved_if_owner_confirms_exact_text", "retention", "delete_raw_on_success"): True,
            ("approved_if_owner_confirms_exact_text", "retention", "delete_raw_on_abort"): True,
            (
                "approved_if_owner_confirms_exact_text",
                "retention",
                "delete_raw_before_git_stage_or_commit",
            ): True,
            ("promotion_gate_carried_forward", "minimum_valid_pairs"): 8,
            ("promotion_gate_carried_forward", "invalid_pair_count_required"): 0,
            ("promotion_gate_carried_forward", "timeout_count_required"): 0,
            ("promotion_gate_carried_forward", "minimum_average_score_delta_percent"): 20,
            ("promotion_gate_carried_forward", "reviewer_gate_required"): True,
        },
        "negative": (
            ("approval_state", "owner_confirmed"),
            ("approval_state", "run_authorized_by_this_artifact"),
            ("approval_state", "approval_reuse_after_consumed_or_aborted_run_allowed"),
            (
                "approved_if_owner_confirms_exact_text",
                "approval_reuse_after_consumed_or_aborted_run_allowed",
            ),
            ("promotion_gate_carried_forward", "static_warning_delta_can_promote"),
            ("approval_and_execution_boundary", "packet_authorizes_future_run"),
            ("approval_and_execution_boundary", "baseline_or_treatment_run_started"),
            ("approval_and_execution_boundary", "reviewer_gate_satisfied"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("approval_and_execution_boundary", "next_required_task"): (
                "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN"
            ),
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T20-A01",
            "batch45-postq4-t20-promotion-grade-eval-approval-packet.json",
        ),
    },
    {
        "name": "t20_exact_approval_1000s_revision",
        "path": SPECS
        / "batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json",
        "identity": {
            "task_id": "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET",
            "evidence_id": "B45-POSTQ4-T20-A02",
        },
        "required": {
            ("status",): (
                "exact_approval_packet_revision_1000s_ready_for_owner_"
                "confirmation_not_run"
            ),
            ("closure_level",): "approval_packet_only_not_run",
            ("schema_version",): (
                "batch45_postq4_t20_promotion_grade_eval_approval_packet_revision_v1"
            ),
            ("route",): "exact_approval_packet_revision_only",
            ("revision_delta", "previous_per_primary_call_timeout_seconds"): 600,
            ("revision_delta", "new_per_primary_call_timeout_seconds"): 1000,
            ("revision_delta", "previous_per_reviewer_call_timeout_seconds"): 600,
            ("revision_delta", "new_per_reviewer_call_timeout_seconds"): 1000,
            ("revision_delta", "max_total_wall_clock_seconds_unchanged"): 12000,
            ("revision_delta", "max_calls_unchanged"): 17,
            ("revision_delta", "max_retries_unchanged"): 0,
            ("approved_if_owner_confirms_exact_text", "model_id"): "gpt-5.5",
            ("approved_if_owner_confirms_exact_text", "model_reasoning_effort"): "high",
            ("approved_if_owner_confirms_exact_text", "max_total_model_or_reviewer_calls"): 17,
            ("approved_if_owner_confirms_exact_text", "max_total_retries"): 0,
            ("approved_if_owner_confirms_exact_text", "per_primary_call_timeout_seconds"): 1000,
            ("approved_if_owner_confirms_exact_text", "per_reviewer_call_timeout_seconds"): 1000,
            ("approved_if_owner_confirms_exact_text", "usd_cost_cap"): 25.0,
            (
                "approved_if_owner_confirms_exact_text",
                "cost_accounting_policy",
                "cost_cap_breach_blocks_promotion",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "cost_accounting_policy",
                "abort_before_next_call_when_estimated_cap_would_be_exceeded",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "valid_pair_count",
            ): 8,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "invalid_pair_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "timeout_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "no_op_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "invalid_json_count",
            ): 0,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "sanitized_rollup_validates",
            ): True,
            (
                "approved_if_owner_confirms_exact_text",
                "reviewer_call_allowed_only_after",
                "raw_outputs_deleted",
            ): True,
            ("promotion_gate_carried_forward", "reviewer_gate_required"): True,
            ("approved_if_owner_confirms_exact_text", "retention", "repo_raw_retention_bytes_allowed"): 0,
        },
        "relations": {
            ("supersedes_evidence_id",): "B45-POSTQ4-T20-A01",
        },
        "negative": (
            ("approval_state", "owner_confirmed"),
            ("approval_state", "run_authorized_by_this_artifact"),
            ("approval_and_execution_boundary", "packet_authorizes_future_run"),
            ("approval_and_execution_boundary", "baseline_or_treatment_run_started"),
            ("approval_and_execution_boundary", "reviewer_gate_satisfied"),
            (
                "approved_if_owner_confirms_exact_text",
                "approval_reuse_after_consumed_or_aborted_run_allowed",
            ),
        ),
        "all_false": (("no_unapproved_actions",),),
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T20-A02",
            "batch45-postq4-t20-promotion-grade-eval-approval-packet-1000s.json",
        ),
    },
    {
        "name": "t20_cost_waived_approval",
        "path": SPECS
        / "batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json",
        "identity": {
            "task_id": "B45-POSTQ4-T20-EXACT-APPROVAL-PACKET",
            "evidence_id": "B45-POSTQ4-T20-A03",
        },
        "required": {
            ("schema_version",): (
                "batch45_postq4_t20_promotion_grade_eval_approval_packet_"
                "cost_waived_v1"
            ),
            ("closure_level",): "approval_consumed_by_aborted_run",
            ("approved_run_contract", "model_id"): "gpt-5.5",
            ("approved_run_contract", "model_reasoning_effort"): "high",
            ("approved_run_contract", "comparison_mode"): "same_model_baseline_treatment",
            ("approved_run_contract", "max_total_model_or_reviewer_calls"): 17,
            ("approved_run_contract", "max_total_retries"): 0,
            ("approved_run_contract", "per_primary_or_reviewer_timeout_seconds"): 1000,
            ("approved_run_contract", "cost_policy"): (
                "owner_accepts_unknown_unbounded_actual_provider_cost_for_this_run"
            ),
            ("consumption_result", "primary_calls_started"): 1,
            ("consumption_result", "status"): (
                "aborted_invalid_json_or_schema_B45_HELDOUT_01_baseline_"
                "test_check_status_invalid"
            ),
        },
        "negative": (
            ("consumption_result", "reviewer_calls_started"),
            ("consumption_result", "raw_outputs_written_to_repo"),
            ("consumption_result", "approval_reuse_allowed"),
            ("consumption_result", "raw_files_present_after_cleanup"),
            ("approved_run_contract", "repo_raw_retention_bytes_allowed"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("supersedes_evidence_id",): "B45-POSTQ4-T20-A02",
            ("consumption_result", "consumed_evidence_id"): (
                "B45-POSTQ4-T21-COST-WAIVED-RUN-A01"
            ),
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T20-A03",
            "batch45-postq4-t20-promotion-grade-eval-approval-packet-cost-waived.json",
        ),
    },
    {
        "name": "t21_cost_waived_run_result",
        "path": SPECS / "batch45-postq4-t21-promotion-grade-eval-results.json",
        "identity": {
            "task_id": "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN",
            "evidence_id": "B45-POSTQ4-T21-COST-WAIVED-RUN-A01",
        },
        "required": {
            ("schema_version",): "batch45_postq4_t21_promotion_grade_eval_results_v1",
            ("status",): (
                "aborted_invalid_json_or_schema_B45_HELDOUT_01_baseline_"
                "test_check_status_invalid"
            ),
            ("approval_basis", "approval_kind"): "exact_owner_approval_cost_waived",
            ("model_policy", "model_id"): "gpt-5.5",
            ("model_policy", "model_reasoning_effort"): "high",
            ("comparison_mode",): "same_model_baseline_treatment",
            ("call_budget", "primary_calls_started"): 1,
            ("call_budget", "max_calls"): 17,
            ("call_budget", "max_retries"): 0,
            ("aggregate_scores", "invalid_pair_count"): 8,
            ("aggregate_scores", "schema_failure_count"): 1,
            ("invalid_output_summary", "first_abort_class"): "schema_validation_failed",
            ("reviewer_gate", "status"): "not_run",
        },
        "negative": (
            ("call_budget", "reviewer_calls_started"),
            ("aggregate_scores", "valid_pair_count"),
            ("aggregate_scores", "promotion_threshold_met"),
            ("aggregate_scores", "m26_reversed"),
            ("aggregate_scores", "m35_reversed"),
            ("aggregate_scores", "t15_reversed"),
            ("cost_timeout_retention", "usage_or_cost_metadata_available"),
            ("cost_timeout_retention", "repo_raw_retention_bytes_allowed"),
            ("cost_timeout_retention", "raw_files_present_after_cleanup"),
            ("cost_timeout_retention", "raw_files_present_after_rollup"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T21-COST-WAIVED-RUN-A01",
            "batch45-postq4-t21-promotion-grade-eval-results.json",
        ),
    },
    {
        "name": "t21_missing_approval_preflight",
        "path": SPECS
        / "batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json",
        "identity": {
            "task_id": "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN",
            "evidence_id": "B45-POSTQ4-T21-PREFLIGHT-A01",
        },
        "required": {
            ("schema_version",): (
                "batch45_postq4_t21_promotion_grade_eval_run_preflight_blocked_v1"
            ),
            ("status",): "blocked_missing_exact_t20_owner_confirmation_not_run",
            ("closure_level",): "blocked_before_execution_no_run",
            ("route",): "approval_required_preflight_block",
            ("approval_preflight", "required_first_line"): (
                "Подтверждаю B45-POSTQ4-T20 exact approval:"
            ),
            ("approval_preflight", "block_reason"): (
                "owner_has_not_restated_exact_approval_text"
            ),
            ("approval_preflight", "preflight_result"): "blocked_before_first_call",
            ("calls_started", "actual_model_or_reviewer_calls_started"): 0,
            ("cost_preflight", "estimated_total_cost_usd"): 0,
        },
        "negative": (
            ("approval_preflight", "owner_confirmed"),
            ("approval_preflight", "run_authorized"),
            ("result_contract_status", "promotion_grade_eval_result_exists"),
            ("result_contract_status", "valid_pair_count"),
            ("result_contract_status", "invalid_pair_count"),
            ("result_contract_status", "timeout_count"),
            ("result_contract_status", "no_op_count"),
            ("result_contract_status", "invalid_json_count"),
            ("result_contract_status", "sanitized_rollup_created"),
            ("result_contract_status", "reviewer_gate_satisfied"),
            ("result_contract_status", "promotion_threshold_evaluated"),
            ("result_contract_status", "promotion_allowed"),
            ("privacy_and_retention_boundary", "raw_outputs_created"),
            ("privacy_and_retention_boundary", "raw_outputs_written_to_repo"),
            ("privacy_and_retention_boundary", "temp_root_created"),
            ("privacy_and_retention_boundary", "repo_raw_retention_bytes"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("approval_preflight", "required_packet"): (
                "docs/superpowers/specs/"
                "batch45-postq4-t20-promotion-grade-eval-approval-packet.json"
            ),
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T21-PREFLIGHT-A01",
            "batch45-postq4-t21-promotion-grade-eval-run-preflight-blocked.json",
        ),
    },
    {
        "name": "t21_timeout_mismatch_preflight",
        "path": SPECS
        / "batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json",
        "identity": {
            "task_id": "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN",
            "evidence_id": "B45-POSTQ4-T21-PREFLIGHT-A02",
        },
        "required": {
            ("schema_version",): (
                "batch45_postq4_t21_promotion_grade_eval_run_preflight_"
                "timeout_mismatch_v1"
            ),
            ("status",): "blocked_exact_approval_timeout_mismatch_not_run",
            ("closure_level",): "blocked_before_execution_no_run",
            ("trigger_message_observed", "requested_timeout_seconds"): 1000,
            ("trigger_message_observed", "required_timeout_seconds"): 600,
            ("approval_preflight", "block_reason"): "approval_text_differs_from_packet",
            ("approval_preflight", "preflight_result"): "blocked_before_first_call",
            ("approval_preflight", "mismatches", 0, "field"): "timeout",
            ("approval_preflight", "mismatches", 0, "required_per_call_timeout_seconds"): 600,
            ("approval_preflight", "mismatches", 0, "observed_per_call_timeout_seconds"): 1000,
            ("would_have_used_if_exactly_approved", "max_total_model_or_reviewer_calls"): 17,
            ("would_have_used_if_exactly_approved", "usd_cost_cap"): 25.0,
        },
        "negative": (
            ("approval_preflight", "approval_text_exact_match"),
            ("approval_preflight", "owner_confirmed"),
            ("approval_preflight", "run_authorized"),
            ("result_contract_status", "promotion_grade_eval_result_exists"),
            ("result_contract_status", "promotion_allowed"),
            ("privacy_and_retention_boundary", "repo_raw_retention_bytes"),
        ),
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T21-PREFLIGHT-A02",
            "batch45-postq4-t21-promotion-grade-eval-run-preflight-timeout-mismatch.json",
        ),
    },
    {
        "name": "t21_cost_unknown_preflight",
        "path": SPECS
        / "batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json",
        "identity": {
            "task_id": "B45-POSTQ4-T21-APPROVED-PROMOTION-GRADE-EVAL-RUN",
            "evidence_id": "B45-POSTQ4-T21-PREFLIGHT-A03",
        },
        "required": {
            ("schema_version",): (
                "batch45_postq4_t21_promotion_grade_eval_run_preflight_cost_unknown_v1"
            ),
            ("status",): "aborted_before_first_call_cost_unknown_not_run",
            ("closure_level",): "blocked_before_execution_no_run",
            ("trigger_message_observed", "model_id"): "gpt-5.5",
            ("trigger_message_observed", "model_reasoning_effort"): "high",
            ("trigger_message_observed", "timeout_seconds"): 1000,
            ("trigger_message_observed", "usd_cost_cap"): 25.0,
            ("approval_preflight", "abort_gate_triggered"): "cost_unknown_before_first_call",
            ("pricing_source_check", "standard_short_context_gpt55_input_usd_per_1m_tokens"): 5.0,
            ("pricing_source_check", "standard_short_context_gpt55_output_usd_per_1m_tokens"): 30.0,
            ("pricing_source_check", "standard_long_context_gpt55_output_usd_per_1m_tokens"): 45.0,
            ("cost_preflight", "estimated_cap_would_be_exceeded"): "not_evaluated_cost_unknown",
            ("cost_preflight", "abort_when_cost_unknown"): True,
            ("command_surface_preflight", "codex_version_checked"): "codex-cli 0.142.5",
            ("would_have_used_if_cost_known", "max_total_model_or_reviewer_calls"): 17,
            ("would_have_used_if_cost_known", "per_primary_call_timeout_seconds"): 1000,
        },
        "negative": (
            ("approval_preflight", "run_authorized_after_abort_gate"),
            ("approval_preflight", "approval_reuse_allowed"),
            ("cost_preflight", "cost_known_before_first_call"),
            ("cost_preflight", "actual_model_or_reviewer_calls_started"),
            ("cost_preflight", "cost_cap_consumed"),
            ("command_surface_preflight", "model_call_command_started"),
            ("result_contract_status", "promotion_grade_eval_result_exists"),
            ("result_contract_status", "promotion_allowed"),
            ("privacy_and_retention_boundary", "raw_outputs_created"),
            ("privacy_and_retention_boundary", "repo_raw_retention_bytes"),
        ),
        "relations": {
            ("previous_evidence_id",): "B45-POSTQ4-T21-PREFLIGHT-A02",
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T21-PREFLIGHT-A03",
            "batch45-postq4-t21-promotion-grade-eval-run-preflight-cost-unknown.json",
        ),
    },
    {
        "name": "t22_reviewer_gate_decision",
        "path": SPECS / "batch45-postq4-t22-promotion-grade-decision-packet.json",
        "identity": {
            "task_id": "B45-POSTQ4-T22-REVIEWER-GATE-AND-DECISION",
            "evidence_id": "B45-POSTQ4-T22-A02",
        },
        "required": {
            ("schema_version",): "batch45_postq4_t22_promotion_grade_decision_packet_v1",
            ("status",): (
                "implemented_reviewer_gate_blocked_t21_invalid_schema_"
                "abort_no_promotion"
            ),
            ("closure_level",): "blocked_before_reviewer_no_run",
            ("precondition_check", "t21_status"): (
                "aborted_invalid_json_or_schema_B45_HELDOUT_01_baseline_"
                "test_check_status_invalid"
            ),
            ("precondition_check", "t21_valid_pair_count"): 0,
            ("precondition_check", "t21_invalid_pair_count"): 8,
            ("precondition_check", "t21_schema_failure_count"): 1,
            ("precondition_check", "t21_primary_calls_started"): 1,
            ("precondition_check", "t21_reviewer_calls_started"): 0,
            ("reviewer_gate", "status"): "not_run_due_t21_invalid_schema_abort",
            ("reviewer_gate", "reviewer_verdict"): "not_applicable_invalid_t21_result",
            ("decision", "status"): (
                "no_go_t21_invalid_schema_abort_missing_valid_pairs_and_reviewer_gate"
            ),
            ("decision", "valid_pair_count_required"): 8,
            ("cost_and_retention", "cost_policy"): (
                "cost_waived_by_owner_unknown_unbounded_actual_provider_cost_accepted"
            ),
        },
        "negative": (
            ("precondition_check", "t21_promotion_grade_eval_result_exists"),
            ("reviewer_gate", "reviewer_input_available"),
            ("reviewer_gate", "reviewer_model_call_authorized"),
            ("reviewer_gate", "reviewer_model_call_started"),
            ("reviewer_gate", "reviewer_calls_started"),
            ("reviewer_gate", "independent_reviewer_verdict_exists"),
            ("reviewer_gate", "gate_satisfied"),
            ("decision", "promotion_allowed"),
            ("decision", "m26_no_go_reversed"),
            ("decision", "m35_no_go_reversed"),
            ("decision", "t15_no_go_reversed"),
            ("decision", "valid_pair_count"),
            ("decision", "reviewer_gate_satisfied"),
            ("cost_and_retention", "raw_outputs_written_to_repo"),
            ("cost_and_retention", "repo_raw_retention_bytes"),
            ("cost_and_retention", "raw_files_present_after_cleanup"),
        ),
        "all_false": (("no_unapproved_actions",),),
        "relations": {
            ("supersedes_evidence_id",): "B45-POSTQ4-T22-A01",
            ("basis", "t21_result"): (
                "docs/superpowers/specs/"
                "batch45-postq4-t21-promotion-grade-eval-results.json"
            ),
        },
        "registry_needles": _registry_needles(
            "B45-POSTQ4-T22-A02",
            "batch45-postq4-t22-promotion-grade-decision-packet.json",
        ),
    },
)


RETAINED_DEBT_EXCEPTIONS = (
    {
        "family_id": "B45-T28-EXACT-NONBLOCKING-STRINGS",
        "source": (
            "removed T18-T22 per-packet assertions in "
            "tests/product_agent_os/test_coding_standards_artifacts.py"
        ),
        "protected_fault": "non-blocking explanatory or approval-copy wording drift",
        "reason": (
            "Only reviewer-named paths in REVIEWER_NAMED_OPERATIONAL_PATHS are "
            "asserted as mapped; this exception does not claim that unenumerated "
            "operational gates are covered. Duplicating every explanatory string "
            "would recreate repeated-family debt without adding a blocking gate."
        ),
        "owner": "tester",
        "follow_up": (
            "Add a literal path only when a source-owned packet promotes the wording "
            "to an operational selector, approval boundary or claim gate."
        ),
    },
    {
        "family_id": "B45-T28-HISTORICAL-SOURCE-HASHES",
        "source": "T20/T21 historical source_freeze sha256 assertions",
        "protected_fault": "historical source snapshot drift",
        "reason": (
            "The hashes describe frozen historical snapshots rather than current "
            "packet behavior; identity, supersession and approval links remain checked."
        ),
        "owner": "docs-maintainer",
        "follow_up": (
            "Create or reuse a source-owned hash manifest before restoring hash checks "
            "if snapshot integrity becomes an active release or rerun prerequisite."
        ),
    },
    {
        "family_id": "B45-T28-REPEATED-CONTROL-PLANE-NEEDLES",
        "source": "repeated PLAN/RUNLOG/TEST/EVALS/current-state packet needles",
        "protected_fault": "packet discoverability regression",
        "reason": (
            "RU and EN source registries are the stable traceability seam; volatile root "
            "control-plane repetition is outside T28 ownership and is not runtime proof."
        ),
        "owner": "docs-maintainer",
        "follow_up": (
            "Reassess exact root-document needles during post-review control-plane sync."
        ),
    },
)


REVIEWER_NAMED_OPERATIONAL_PATHS = (
    ("t19_cost_timeout_retention_policy", ("no_unapproved_actions",)),
    (
        "t18_promotion_grade_eval_design",
        (
            "comparison_design",
            "promotion_grade_model_policy",
            "same_model_required_for_baseline_and_treatment",
        ),
    ),
    ("t19_cost_timeout_retention_policy", ("cost_policy", "abort_when_cost_unknown")),
    (
        "t19_cost_timeout_retention_policy",
        ("timeout_policy", "stop_on_first_primary_timeout"),
    ),
    (
        "t20_exact_approval_packet",
        (
            "approved_if_owner_confirms_exact_text",
            "reviewer_call_allowed_only_after",
            "valid_pair_count",
        ),
    ),
    (
        "t20_exact_approval_packet",
        (
            "approved_if_owner_confirms_exact_text",
            "reviewer_call_allowed_only_after",
            "invalid_json_count",
        ),
    ),
    (
        "t21_missing_approval_preflight",
        ("result_contract_status", "valid_pair_count"),
    ),
    (
        "t22_reviewer_gate_decision",
        ("reviewer_gate", "reviewer_input_available"),
    ),
    (
        "t19_cost_timeout_retention_policy",
        ("cost_policy", "cost_cap_breach_blocks_promotion"),
    ),
    (
        "t20_exact_approval_packet",
        (
            "approved_if_owner_confirms_exact_text",
            "cost_accounting_policy",
            "cost_cap_breach_blocks_promotion",
        ),
    ),
    (
        "t20_exact_approval_packet",
        (
            "approved_if_owner_confirms_exact_text",
            "cost_accounting_policy",
            "abort_before_next_call_when_estimated_cap_would_be_exceeded",
        ),
    ),
    (
        "t21_cost_unknown_preflight",
        ("cost_preflight", "abort_when_cost_unknown"),
    ),
    (
        "t18_promotion_grade_eval_design",
        (
            "invalid_output_handling",
            "pair_policy",
            "reviewer_not_called_for_invalid_pairs",
        ),
    ),
    (
        "t20_exact_approval_packet",
        ("promotion_gate_carried_forward", "reviewer_gate_required"),
    ),
)
OPERATIONAL_OMISSION_MAP = ()


DELETE_PATH = object()
SEEDED_FAULT_FAMILIES = (
    {
        "family_id": "budget",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("run_budget_policy", "max_total_model_or_reviewer_calls"),
        "replacement": 18,
        "expected_error": (
            "schema_required_path:run_budget_policy.max_total_model_or_reviewer_calls"
        ),
    },
    {
        "family_id": "timeout",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("timeout_policy", "stop_on_first_primary_timeout"),
        "replacement": False,
        "expected_error": "schema_required_path:timeout_policy.stop_on_first_primary_timeout",
    },
    {
        "family_id": "cost",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("cost_policy", "abort_when_cost_unknown"),
        "replacement": False,
        "expected_error": "schema_required_path:cost_policy.abort_when_cost_unknown",
    },
    {
        "family_id": "schema_comparability",
        "case": "t18_promotion_grade_eval_design",
        "path": (
            "comparison_design",
            "promotion_grade_model_policy",
            "same_model_required_for_baseline_and_treatment",
        ),
        "replacement": False,
        "expected_error": (
            "schema_required_path:comparison_design.promotion_grade_model_policy."
            "same_model_required_for_baseline_and_treatment"
        ),
    },
    {
        "family_id": "abort",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("retry_and_abort_policy", "aborted_run_cannot_support_promotion"),
        "replacement": False,
        "expected_error": (
            "schema_required_path:retry_and_abort_policy."
            "aborted_run_cannot_support_promotion"
        ),
    },
    {
        "family_id": "reviewer_no_go",
        "case": "t22_reviewer_gate_decision",
        "path": ("decision", "status"),
        "replacement": "promotion_go",
        "expected_error": "schema_required_path:decision.status",
    },
    {
        "family_id": "whole_section_deletion",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("no_unapproved_actions",),
        "replacement": DELETE_PATH,
        "expected_error": "claim_ceiling_negative_invariant:no_unapproved_actions",
    },
    {
        "family_id": "retention_cleanup",
        "case": "t21_cost_waived_run_result",
        "path": ("cost_timeout_retention", "raw_files_present_after_cleanup"),
        "replacement": 1,
        "expected_error": (
            "claim_ceiling_negative_invariant:cost_timeout_retention."
            "raw_files_present_after_cleanup"
        ),
    },
    {
        "family_id": "cost_cap_breach",
        "case": "t19_cost_timeout_retention_policy",
        "path": ("cost_policy", "cost_cap_breach_blocks_promotion"),
        "replacement": False,
        "expected_error": (
            "schema_required_path:cost_policy.cost_cap_breach_blocks_promotion"
        ),
    },
    {
        "family_id": "over_cap_abort",
        "case": "t20_exact_approval_packet",
        "path": (
            "approved_if_owner_confirms_exact_text",
            "cost_accounting_policy",
            "abort_before_next_call_when_estimated_cap_would_be_exceeded",
        ),
        "replacement": False,
        "expected_error": (
            "schema_required_path:approved_if_owner_confirms_exact_text."
            "cost_accounting_policy."
            "abort_before_next_call_when_estimated_cap_would_be_exceeded"
        ),
    },
    {
        "family_id": "t21_cost_abort",
        "case": "t21_cost_unknown_preflight",
        "path": ("cost_preflight", "abort_when_cost_unknown"),
        "replacement": False,
        "expected_error": (
            "schema_required_path:cost_preflight.abort_when_cost_unknown"
        ),
    },
    {
        "family_id": "invalid_pair_reviewer_prohibition",
        "case": "t18_promotion_grade_eval_design",
        "path": (
            "invalid_output_handling",
            "pair_policy",
            "reviewer_not_called_for_invalid_pairs",
        ),
        "replacement": False,
        "expected_error": (
            "schema_required_path:invalid_output_handling.pair_policy."
            "reviewer_not_called_for_invalid_pairs"
        ),
    },
    {
        "family_id": "mandatory_reviewer_gate",
        "case": "t20_exact_approval_packet",
        "path": ("promotion_gate_carried_forward", "reviewer_gate_required"),
        "replacement": False,
        "expected_error": (
            "schema_required_path:promotion_gate_carried_forward."
            "reviewer_gate_required"
        ),
    },
)


def _case(name):
    return next(case for case in PACKET_CASES if case["name"] == name)


def _path_label(path):
    return ".".join(str(segment) for segment in path)


def evaluate_packet_case(packet, case, documents):
    errors = [
        f"identity_exact:{key}"
        for key, expected in case.get("identity", {}).items()
        if packet.get(key) != expected
    ]
    for path, expected in case.get("required", {}).items():
        current = packet
        try:
            for segment in path:
                current = current[segment]
        except (KeyError, TypeError):
            current = object()
        if current != expected:
            errors.append(f"schema_required_path:{_path_label(path)}")
    for path in case.get("all_false", ()):
        current = packet
        try:
            for segment in path:
                current = current[segment]
        except (KeyError, TypeError):
            current = None
        if not isinstance(current, dict) or not current:
            errors.append(
                f"claim_ceiling_negative_invariant:{_path_label(path)}"
            )
            continue
        for key, value in current.items():
            if value is not False:
                errors.append(
                    "claim_ceiling_negative_invariant:"
                    f"{_path_label((*path, key))}"
                )
    for path in case.get("negative", ()):
        current = packet
        try:
            for segment in path:
                current = current[segment]
        except (KeyError, TypeError):
            current = object()
        if current is not False and current != 0:
            errors.append(
                f"claim_ceiling_negative_invariant:{_path_label(path)}"
            )
    for path, expected in case.get("relations", {}).items():
        current = packet
        try:
            for segment in path:
                current = current[segment]
        except (KeyError, TypeError):
            current = object()
        if current != expected:
            errors.append(f"relationship_traceability:{_path_label(path)}")
    for document_name, needles in case.get("registry_needles", {}).items():
        document = documents.get(document_name, "")
        for needle in needles:
            if needle not in document:
                errors.append(
                    f"registry_traceability:{document_name}:{needle}"
                )
    return errors


class Batch45PacketContractEvaluatorTest(unittest.TestCase):
    def test_seeded_fault_families_are_detected(self):
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }
        for seed in SEEDED_FAULT_FAMILIES:
            with self.subTest(family=seed["family_id"]):
                case = _case(seed["case"])
                packet = json.loads(case["path"].read_text(encoding="utf-8"))
                corrupted = copy.deepcopy(packet)
                current = corrupted
                for segment in seed["path"][:-1]:
                    current = current[segment]
                if seed["replacement"] is DELETE_PATH:
                    del current[seed["path"][-1]]
                else:
                    current[seed["path"][-1]] = seed["replacement"]
                self.assertEqual(
                    [seed["expected_error"]],
                    evaluate_packet_case(corrupted, case, documents),
                )

    def test_retained_debt_exceptions_are_owned_and_actionable(self):
        required_fields = {
            "family_id",
            "source",
            "protected_fault",
            "reason",
            "owner",
            "follow_up",
        }
        self.assertEqual(
            len(RETAINED_DEBT_EXCEPTIONS),
            len({item["family_id"] for item in RETAINED_DEBT_EXCEPTIONS}),
        )
        for exception in RETAINED_DEBT_EXCEPTIONS:
            with self.subTest(family=exception["family_id"]):
                self.assertEqual(required_fields, set(exception))
                self.assertTrue(all(exception[field] for field in required_fields))
        registered_paths = {
            (case["name"], path)
            for case in PACKET_CASES
            for group in ("required", "negative", "all_false")
            for path in case.get(group, ())
        }
        named_paths = set(REVIEWER_NAMED_OPERATIONAL_PATHS)
        mapped_omissions = set(OPERATIONAL_OMISSION_MAP)
        omissions = named_paths - registered_paths
        self.assertEqual(set(), omissions - mapped_omissions)
        self.assertEqual(set(), mapped_omissions - omissions)

    def test_registered_packets_satisfy_generic_contracts(self):
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }
        for case in PACKET_CASES:
            with self.subTest(case=case["name"]):
                packet = json.loads(case["path"].read_text(encoding="utf-8"))
                self.assertEqual([], evaluate_packet_case(packet, case, documents))

    def test_task_and_evidence_identity_corruptions_are_reported(self):
        case = PACKET_CASES[0]
        packet = json.loads(case["path"].read_text(encoding="utf-8"))

        self.assertEqual([], evaluate_packet_case(packet, case, {}))

        for key in ("task_id", "evidence_id"):
            with self.subTest(key=key):
                corrupted = copy.deepcopy(packet)
                corrupted[key] = f"{packet[key]}-CORRUPTED"
                self.assertEqual(
                    [f"identity_exact:{key}"],
                    evaluate_packet_case(corrupted, case, {}),
                )

    def test_required_status_and_closure_corruptions_are_reported(self):
        case = PACKET_CASES[0]
        packet = json.loads(case["path"].read_text(encoding="utf-8"))

        for path in (("status",), ("scope", "closure_level")):
            with self.subTest(path=path):
                corrupted = copy.deepcopy(packet)
                current = corrupted
                for segment in path[:-1]:
                    current = current[segment]
                del current[path[-1]]
                self.assertEqual(
                    [f"schema_required_path:{_path_label(path)}"],
                    evaluate_packet_case(corrupted, case, {}),
                )

    def test_claim_ceiling_corruption_is_reported_at_the_exact_path(self):
        case = PACKET_CASES[0]
        packet = json.loads(case["path"].read_text(encoding="utf-8"))

        corrupted = copy.deepcopy(packet)
        corrupted["no_unapproved_actions"]["provider_or_live_api_called"] = True
        self.assertEqual(
            [
                "claim_ceiling_negative_invariant:"
                "no_unapproved_actions.provider_or_live_api_called"
            ],
            evaluate_packet_case(corrupted, case, {}),
        )

    def test_relationship_corruption_is_reported_at_the_exact_path(self):
        case = _case("t20_exact_approval_1000s_revision")
        packet = json.loads(case["path"].read_text(encoding="utf-8"))
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }

        corrupted = copy.deepcopy(packet)
        corrupted["supersedes_evidence_id"] = "B45-POSTQ4-T20-CORRUPTED"
        self.assertEqual(
            ["relationship_traceability:supersedes_evidence_id"],
            evaluate_packet_case(corrupted, case, documents),
        )

    def test_registry_corruption_is_reported_for_ru_or_en_document(self):
        case = _case("t20_exact_approval_1000s_revision")
        packet = json.loads(case["path"].read_text(encoding="utf-8"))
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }

        for document_name in ("registry_ru", "registry_en"):
            with self.subTest(document=document_name):
                corrupted = copy.deepcopy(documents)
                corrupted[document_name] = corrupted[document_name].replace(
                    "B45-POSTQ4-T20-A02",
                    "B45-POSTQ4-T20-CORRUPTED",
                )
                self.assertEqual(
                    [
                        "registry_traceability:"
                        f"{document_name}:B45-POSTQ4-T20-A02"
                    ],
                    evaluate_packet_case(packet, case, corrupted),
                )

    def test_promotion_run_and_reviewer_corruptions_are_reported(self):
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }
        corruptions = (
            (
                "t22_reviewer_gate_decision",
                ("decision", "promotion_allowed"),
            ),
            (
                "t21_missing_approval_preflight",
                ("approval_preflight", "run_authorized"),
            ),
            (
                "t22_reviewer_gate_decision",
                ("reviewer_gate", "reviewer_model_call_started"),
            ),
        )
        for case_name, path in corruptions:
            with self.subTest(case=case_name, path=path):
                case = _case(case_name)
                packet = json.loads(case["path"].read_text(encoding="utf-8"))
                corrupted = copy.deepcopy(packet)
                current = corrupted
                for segment in path[:-1]:
                    current = current[segment]
                current[path[-1]] = True
                self.assertEqual(
                    [
                        "claim_ceiling_negative_invariant:"
                        f"{'.'.join(path)}"
                    ],
                    evaluate_packet_case(corrupted, case, documents),
                )

    def test_reviewer_proven_missed_corruptions_are_detected(self):
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }
        delete_section = object()
        corruptions = (
            (
                "t19_cost_timeout_retention_policy",
                ("no_unapproved_actions",),
                delete_section,
                "claim_ceiling_negative_invariant:no_unapproved_actions",
            ),
            (
                "t18_promotion_grade_eval_design",
                (
                    "comparison_design",
                    "promotion_grade_model_policy",
                    "same_model_required_for_baseline_and_treatment",
                ),
                False,
                "schema_required_path:comparison_design.promotion_grade_model_policy."
                "same_model_required_for_baseline_and_treatment",
            ),
            (
                "t19_cost_timeout_retention_policy",
                ("cost_policy", "abort_when_cost_unknown"),
                False,
                "schema_required_path:cost_policy.abort_when_cost_unknown",
            ),
            (
                "t19_cost_timeout_retention_policy",
                ("timeout_policy", "stop_on_first_primary_timeout"),
                False,
                "schema_required_path:timeout_policy.stop_on_first_primary_timeout",
            ),
            (
                "t20_exact_approval_packet",
                (
                    "approved_if_owner_confirms_exact_text",
                    "reviewer_call_allowed_only_after",
                    "valid_pair_count",
                ),
                0,
                "schema_required_path:approved_if_owner_confirms_exact_text."
                "reviewer_call_allowed_only_after.valid_pair_count",
            ),
            (
                "t20_exact_approval_packet",
                (
                    "approved_if_owner_confirms_exact_text",
                    "reviewer_call_allowed_only_after",
                    "invalid_json_count",
                ),
                1,
                "schema_required_path:approved_if_owner_confirms_exact_text."
                "reviewer_call_allowed_only_after.invalid_json_count",
            ),
            (
                "t21_missing_approval_preflight",
                ("result_contract_status", "valid_pair_count"),
                1,
                "claim_ceiling_negative_invariant:result_contract_status."
                "valid_pair_count",
            ),
            (
                "t22_reviewer_gate_decision",
                ("reviewer_gate", "reviewer_input_available"),
                True,
                "claim_ceiling_negative_invariant:reviewer_gate."
                "reviewer_input_available",
            ),
        )
        for case_name, path, replacement, expected_error in corruptions:
            with self.subTest(case=case_name, path=path):
                case = _case(case_name)
                packet = json.loads(case["path"].read_text(encoding="utf-8"))
                corrupted = copy.deepcopy(packet)
                current = corrupted
                for segment in path[:-1]:
                    current = current[segment]
                if replacement is delete_section:
                    del current[path[-1]]
                else:
                    current[path[-1]] = replacement
                self.assertEqual(
                    [expected_error],
                    evaluate_packet_case(corrupted, case, documents),
                )

    def test_second_review_operational_misses_are_detected(self):
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in REGISTRY_DOCUMENTS.items()
        }
        corruptions = (
            (
                "t19_cost_timeout_retention_policy",
                ("cost_policy", "cost_cap_breach_blocks_promotion"),
            ),
            (
                "t20_exact_approval_packet",
                (
                    "approved_if_owner_confirms_exact_text",
                    "cost_accounting_policy",
                    "cost_cap_breach_blocks_promotion",
                ),
            ),
            (
                "t20_exact_approval_packet",
                (
                    "approved_if_owner_confirms_exact_text",
                    "cost_accounting_policy",
                    "abort_before_next_call_when_estimated_cap_would_be_exceeded",
                ),
            ),
            (
                "t21_cost_unknown_preflight",
                ("cost_preflight", "abort_when_cost_unknown"),
            ),
            (
                "t18_promotion_grade_eval_design",
                (
                    "invalid_output_handling",
                    "pair_policy",
                    "reviewer_not_called_for_invalid_pairs",
                ),
            ),
            (
                "t20_exact_approval_packet",
                ("promotion_gate_carried_forward", "reviewer_gate_required"),
            ),
        )
        for case_name, path in corruptions:
            with self.subTest(case=case_name, path=path):
                case = _case(case_name)
                packet = json.loads(case["path"].read_text(encoding="utf-8"))
                corrupted = copy.deepcopy(packet)
                current = corrupted
                for segment in path[:-1]:
                    current = current[segment]
                current[path[-1]] = False
                self.assertEqual(
                    [f"schema_required_path:{_path_label(path)}"],
                    evaluate_packet_case(corrupted, case, documents),
                )


if __name__ == "__main__":
    unittest.main()
