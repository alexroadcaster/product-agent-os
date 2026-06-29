import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.agent_skill_metrics import (  # noqa: E402
    METRICS_PACKET_LIMITS,
    build_completion_skeptic_metrics_loop_record,
    build_daily_metrics_report,
    build_scorecard_ledger_record,
    build_weekly_verification_packet,
    build_metric_aggregation,
    build_evidence_packet,
    build_evidence_dataset,
    build_grader_run_summary,
    build_judge_calibration_summary,
    build_metrics_packet,
    build_metrics_run_record,
    build_trace_packet,
    calculate_repeatability_metrics,
    calculate_scorecards,
    collect_target_registry,
    enforce_metrics_redaction_gate,
    enforce_trace_data_classification_gate,
    evaluate_dataset_quality,
    evaluate_confidence_and_decision_gates,
    generate_modernization_candidates,
    prioritize_improvement_components,
    recommend_metrics_cadence,
    render_scorecard_ledger_markdown,
    source_priority_policy,
)
from product_agent_os.self_learning_metrics import (  # noqa: E402
    append_metrics_ledger_row,
    build_metric_taxonomy,
    build_paired_skill_utility_eval,
    build_process_control_safety_scorecard,
    build_self_learning_eval_report,
    build_skill_retrieval_composition_metrics,
    summarize_self_learning_metrics,
    validate_metric_taxonomy,
    validate_metrics_ledger_row,
)


class AgentSkillMetricsTest(unittest.TestCase):
    def test_self_learning_metrics_ledger_is_append_only_versioned_and_source_backed(self):
        row = {
            "schema_version": "self_learning_metrics_ledger_v1",
            "run_id": "sll-20260624T100000Z-demo",
            "evidence_window": {"started_at": "2026-06-24T09:00:00Z", "ended_at": "2026-06-24T10:00:00Z"},
            "baseline_version": "skill:planner@1.0.0",
            "current_version": "skill:planner@1.0.1",
            "candidate_version": "skill:planner@1.0.2-candidate",
            "metrics": {"task_success_rate": {"value": 0.8, "denominator": 10, "source": "fixture_eval", "confidence": "low"}},
            "confidence_intervals": {"task_success_rate": {"lower": 0.62, "upper": 0.91}},
            "cost_latency": {"median_latency_ms": 1200, "total_tokens": 2400},
            "user_effort": {"owner_minutes": 4, "manual_reviews": 1},
            "regression_flags": [],
            "accepted_gaps": ["real_owner_feedback_missing"],
            "report_paths": ["docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json"],
            "rollback_targets": ["skill:planner@1.0.1"],
            "source_status": "source_backed",
            "privacy_status": "synthetic_only",
            "append_only": True,
        }

        errors = validate_metrics_ledger_row(row)
        appended = append_metrics_ledger_row([], row)
        duplicate = append_metrics_ledger_row(appended["rows"], row)
        raw_chat = dict(row, run_id="sll-raw-chat", privacy_status="raw_private_chat_log")

        self.assertEqual(errors, [])
        self.assertEqual(appended["schema_version"], "self_learning_metrics_ledger_append_result_v1")
        self.assertEqual(appended["write_policy"], "append_only")
        self.assertEqual(len(appended["rows"]), 1)
        self.assertIn("duplicate_run_id", duplicate["errors"])
        self.assertIn("raw_private_content_not_allowed", validate_metrics_ledger_row(raw_chat))

    def test_self_learning_eval_report_separates_static_and_evolutionary_quality(self):
        report = build_self_learning_eval_report(
            static_records=[
                {"fixture_id": "s1", "passed": True, "split": "baseline"},
                {"fixture_id": "s2", "passed": False, "split": "holdout"},
            ],
            evolutionary_records=[
                {"fixture_id": "s1", "baseline_passed": False, "post_feedback_passed": True, "regression": False},
                {"fixture_id": "s2", "baseline_passed": True, "post_feedback_passed": False, "regression": True},
                {"fixture_id": "s3", "baseline_passed": False, "post_feedback_passed": True, "regression": False},
            ],
            satisfaction_report={"baseline_score": 3.0, "current_score": 4.0, "denominator": 2},
        )

        self.assertEqual(report["schema_version"], "self_learning_eval_report_v1")
        self.assertEqual(report["static_quality"]["denominator"], 2)
        self.assertEqual(report["static_quality"]["pass_rate"], 0.5)
        self.assertEqual(report["evolutionary_quality"]["denominator"], 3)
        self.assertAlmostEqual(report["evolutionary_quality"]["post_feedback_pass_rate"], 2 / 3, places=4)
        self.assertEqual(report["evolutionary_quality"]["regression_count"], 1)
        self.assertEqual(report["satisfaction_delta"], 1.0)
        self.assertEqual(report["real_user_value_claim"], "unsupported_without_real_owner_feedback")

    def test_metric_taxonomy_requires_denominator_source_confidence_and_privacy(self):
        taxonomy = build_metric_taxonomy()
        missing_denominator = build_metric_taxonomy(
            overrides={"outcome": [{"metric_id": "task_success_rate", "source": "fixture_eval", "confidence": "low", "privacy_status": "synthetic_only"}]}
        )

        self.assertEqual(taxonomy["schema_version"], "self_learning_metric_taxonomy_v1")
        self.assertEqual(validate_metric_taxonomy(taxonomy), [])
        self.assertEqual(
            set(taxonomy["families"]),
            {
                "outcome",
                "satisfaction",
                "skill_utility",
                "retrieval",
                "composition",
                "process_control",
                "professional_code_authoring",
                "memory_quality",
                "safety",
                "cost",
                "regression",
            },
        )
        professional_metrics = {item["metric_id"] for item in taxonomy["families"]["professional_code_authoring"]}
        self.assertIn("existing_capability_scan_rate", professional_metrics)
        self.assertIn("custom_code_avoidance_rate", professional_metrics)
        self.assertIn("unnecessary_dependency_avoidance_rate", professional_metrics)
        self.assertIn("outcome.task_success_rate.denominator_missing", validate_metric_taxonomy(missing_denominator))

    def test_paired_skill_utility_eval_requires_baseline_cost_and_regression_context(self):
        report = build_paired_skill_utility_eval(
            [
                {
                    "task_id": "t1",
                    "baseline_passed": False,
                    "with_skill_passed": True,
                    "baseline_tokens": 1000,
                    "with_skill_tokens": 1100,
                    "skill_version": "review@1.1.0",
                    "expected_skill_version": "review@1.1.0",
                    "accepted": True,
                },
                {
                    "task_id": "t2",
                    "baseline_passed": True,
                    "with_skill_passed": False,
                    "baseline_tokens": 1000,
                    "with_skill_tokens": 1500,
                    "skill_version": "review@old",
                    "expected_skill_version": "review@1.1.0",
                    "accepted": False,
                },
            ]
        )

        self.assertEqual(report["schema_version"], "paired_skill_utility_eval_v1")
        self.assertEqual(report["baseline_pass_rate"], 0.5)
        self.assertEqual(report["with_skill_pass_rate"], 0.5)
        self.assertEqual(report["skill_pass_rate_delta"], 0.0)
        self.assertEqual(report["negative_delta"], 1)
        self.assertEqual(report["version_mismatch_regression"], 1)
        self.assertEqual(report["skill_token_overhead"], 300.0)
        self.assertEqual(report["promotion_status"], "blocked")
        self.assertIn("negative_skill_delta", report["blockers"])

    def test_skill_retrieval_and_composition_metrics_compute_ndcg_top_k_precision_and_reuse(self):
        report = build_skill_retrieval_composition_metrics(
            [
                {
                    "query_id": "q1",
                    "expected_skills": ["requirements-author", "implementation-planner"],
                    "retrieved_skills": ["implementation-planner", "requirements-author", "docs-maintainer"],
                    "composed_tools": ["requirements-author", "implementation-planner"],
                    "composition_success": True,
                    "skill_reused": True,
                    "baseline_tokens": 2200,
                    "with_skill_tokens": 1600,
                },
                {
                    "query_id": "q2",
                    "expected_skills": ["risk-reviewer"],
                    "retrieved_skills": ["docs-maintainer"],
                    "composed_tools": [],
                    "composition_success": False,
                    "skill_reused": False,
                    "baseline_tokens": 1000,
                    "with_skill_tokens": 1200,
                },
            ]
        )

        self.assertEqual(report["schema_version"], "skill_retrieval_composition_metrics_v1")
        self.assertGreater(report["skill_retrieval_ndcg_at_10"], 0)
        self.assertEqual(report["top_k_hit_rate"], 0.5)
        self.assertEqual(report["tool_composition_success_rate"], 0.5)
        self.assertEqual(report["skill_reuse_rate"], 0.5)
        self.assertEqual(report["token_savings"], 400)
        self.assertEqual(report["large_catalog_scope"], "explicitly_not_claimed")

    def test_process_control_safety_scorecard_blocks_harmful_or_control_regressions(self):
        scorecard = build_process_control_safety_scorecard(
            [
                {
                    "fixture_id": "safe-approval-boundary",
                    "defect_type": "none",
                    "control_preserved": True,
                    "interruptible": True,
                    "correctable": True,
                    "reversible": True,
                    "authority_handoff": True,
                    "injection_attack_succeeded": False,
                    "harmful_skill_action": False,
                    "legitimate_instruction_complied": True,
                },
                {
                    "fixture_id": "negative-forbidden-action",
                    "defect_type": "approval_boundary_bypass",
                    "control_preserved": False,
                    "interruptible": False,
                    "correctable": True,
                    "reversible": False,
                    "authority_handoff": False,
                    "injection_attack_succeeded": True,
                    "harmful_skill_action": True,
                    "legitimate_instruction_complied": False,
                },
            ]
        )

        self.assertEqual(scorecard["schema_version"], "process_control_safety_scorecard_v1")
        self.assertEqual(scorecard["process_defect_rate"], 0.5)
        self.assertEqual(scorecard["control_preservation_rate"], 0.5)
        self.assertEqual(scorecard["injection_attack_success_rate"], 0.5)
        self.assertEqual(scorecard["harmful_skill_score"], 0.5)
        self.assertEqual(scorecard["promotion_status"], "blocked")
        self.assertIn("harmful_skill_action_detected", scorecard["blockers"])
        self.assertEqual(scorecard["fixture_execution_policy"], "synthetic_only_no_harmful_actions")

    def test_self_learning_run_packet_reads_metrics_ledger_without_generated_view_claims(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            ledger_row = {
                "schema_version": "self_learning_metrics_ledger_v1",
                "run_id": "sll-20260624T100000Z-demo",
                "evidence_window": {"started_at": "2026-06-24T09:00:00Z", "ended_at": "2026-06-24T10:00:00Z"},
                "baseline_version": "agent@1",
                "current_version": "agent@2",
                "candidate_version": "agent@3-candidate",
                "metrics": {"task_success_rate": {"value": 0.7, "denominator": 10, "source": "fixture_eval", "confidence": "low"}},
                "confidence_intervals": {},
                "cost_latency": {"median_latency_ms": 900},
                "user_effort": {"owner_minutes": 2},
                "regression_flags": ["latency_regression"],
                "accepted_gaps": ["real_owner_feedback_missing"],
                "report_paths": ["docs/superpowers/specs/report.json"],
                "rollback_targets": ["agent@2"],
                "source_status": "source_backed",
                "privacy_status": "synthetic_only",
                "append_only": True,
            }
            self._write(root / ".codex" / "eval-reports" / "agent-skill-metrics-ledger.jsonl", json.dumps(ledger_row) + "\n")

            summary = summarize_self_learning_metrics(root)

            self.assertEqual(summary["schema_version"], "self_learning_metrics_summary_v1")
            self.assertEqual(summary["status"], "available")
            self.assertEqual(summary["ledger_rows"], 1)
            self.assertEqual(summary["latest_run_id"], "sll-20260624T100000Z-demo")
            self.assertEqual(summary["quality_regression_claim"], "unsupported_without_current_verification")
            self.assertEqual(summary["generated_view_success_claim"], "never")

    def test_source_priority_policy_accepts_artifacts_and_rejects_generated_views(self):
        policy = source_priority_policy()

        self.assertEqual(policy["schema_version"], 1)
        self.assertEqual(policy["write_policy"], "read_only")
        self.assertEqual(
            policy["source_of_truth"],
            [
                "control_plane",
                "run_record",
                "trace_packet",
                "eval_packet",
                "accepted_gap",
            ],
        )
        self.assertIn("status_dashboard_html", policy["generated_review_only"])
        self.assertIn("metrics_report_html", policy["generated_review_only"])
        self.assertIn("memory", policy["rejected"])
        self.assertIn("raw_chat_log", policy["rejected"])
        self.assertIn("unsupported_community_claim", policy["rejected"])
        self.assertEqual(policy["generated_view_success_claim_policy"], "never")

    def test_target_registry_collects_agent_skill_policy_and_automation_targets_without_writes(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            self._write(root / ".codex" / "agents" / "reviewer.toml", 'name = "reviewer"\nowner = "Quality"\n')
            self._write(root / ".codex" / "skills" / "review-slice" / "SKILL.md", "---\nname: review-slice\n---\n")
            self._write(root / ".codex" / "artifact-templates" / "prompt-contract.md", "# Prompt Contract\n")
            self._write(root / ".codex" / "artifact-templates" / "model-reasoning-policy.md", "# Model Policy\n")
            self._write(root / ".codex" / "automation-candidates" / "daily-metrics.md", "# Automation Candidate\n")
            self._write(root / ".codex" / "config.toml", 'model = "gpt-5"\napproval_policy = "on-request"\n')
            before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))

            registry = collect_target_registry(root)

            after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*"))
            self.assertEqual(after, before)
            self.assertEqual(registry["schema_version"], 1)
            self.assertEqual(registry["write_policy"], "read_only")
            target_ids = {target["target_id"] for target in registry["targets"]}
            self.assertIn("agent:reviewer", target_ids)
            self.assertIn("skill:review-slice", target_ids)
            self.assertIn("prompt_pack:prompt-contract", target_ids)
            self.assertIn("policy_pack:model-reasoning-policy", target_ids)
            self.assertIn("automation_candidate:daily-metrics", target_ids)
            self.assertIn("policy_pack:codex-config", target_ids)
            for target in registry["targets"]:
                with self.subTest(target=target["target_id"]):
                    self.assertTrue(target["owner"])
                    self.assertTrue(target["version"])
                    self.assertIn(target["risk_level"], {"low", "medium", "high", "unknown"})
                    self.assertIsInstance(target["expected_artifacts"], list)
                    self.assertIsInstance(target["eval_suite"], list)
                    self.assertIsInstance(target["source_artifacts"], list)
                    self.assertTrue(target["maturity_level"])
                    self.assertTrue(target["usage_volume"])
                    self.assertTrue(target["tool_permission_level"])
                    self.assertIn(target["production_impact"], {True, False})
                    self.assertTrue(target["no_data_status"])

    def test_evidence_intake_uses_explicit_artifacts_and_excludes_dashboard_memory_and_raw_chat(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            self._write(
                root / "RUNLOG.md",
                "\n".join(
                    [
                        "# Runlog",
                        "- 2026-05-28 current run: python tools/check_docs.py exited 0.",
                        "- 2026-05-20 failed verification evidence: fixture eval failed.",
                        "- accepted gap: live trace unavailable until owner approval.",
                    ]
                ),
            )
            self._write(root / "TEST.md", "- fixture eval summary: 80 fixtures, 0 failures.\n")
            self._write(root / "EVALS.md", "- transcript eval summary: 10 sessions, 0 failures.\n")
            self._write(root / ".codex" / "artifact-templates" / "trace-evidence-packet.md", "# Trace Evidence Packet\n")
            self._write(root / ".codex" / "product-agent-os" / "status.html", "<html>Status</html>\n")
            self._write(root / ".codex" / "eval-reports" / "agent-skill-evaluation-report.html", "<html>Report</html>\n")
            self._write(root / "memory.md", "# Memory\n")
            self._write(root / "raw-chat.log", "raw private chat log\n")

            packet = build_evidence_packet(root, as_of_date="2026-05-28")
            serialized = json.dumps(packet, sort_keys=True)

            self.assertEqual(packet["schema_version"], 1)
            self.assertEqual(packet["write_policy"], "read_only")
            source_types = {record["source_type"] for record in packet["evidence_records"]}
            self.assertIn("control_plane", source_types)
            self.assertIn("trace_packet", source_types)
            self.assertIn("accepted_gap", source_types)
            self.assertIn("eval_packet", source_types)
            self.assertIn("failed_verification", source_types)
            excluded_types = {record["source_type"] for record in packet["excluded_records"]}
            self.assertIn("status_dashboard_html", excluded_types)
            self.assertIn("metrics_report_html", excluded_types)
            self.assertIn("memory", excluded_types)
            self.assertIn("raw_chat_log", excluded_types)
            self.assertNotIn(str(root), serialized)

    def test_evidence_intake_marks_stale_evidence_from_explicit_artifacts(self):
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            self._write(root / "RUNLOG.md", "- 2026-04-01 old verification: python tools/check_docs.py exited 0.\n")

            packet = build_evidence_packet(root, as_of_date="2026-05-28")

            stale_records = [
                record for record in packet["evidence_records"] if record["source_type"] == "stale_evidence"
            ]
            self.assertEqual(len(stale_records), 1)
            self.assertEqual(stale_records[0]["status"], "stale")
            self.assertEqual(stale_records[0]["recorded_at"], "2026-04-01")

    def test_metrics_packet_bounds_trim_deterministically_with_warnings(self):
        targets = [
            {"target_id": f"skill:target-{index}", "target_type": "skill"}
            for index in range(METRICS_PACKET_LIMITS["targets"] + 2)
        ]
        evidence = [
            {"record_id": f"evidence-{index}", "source_type": "control_plane"}
            for index in range(METRICS_PACKET_LIMITS["evidence_records"] + 2)
        ]
        questions = [{"id": f"question-{index}"} for index in range(METRICS_PACKET_LIMITS["questions"] + 2)]
        candidates = [
            {"candidate_id": f"candidate-{index}"}
            for index in range(METRICS_PACKET_LIMITS["update_candidates"] + 2)
        ]
        embedded_json = {"payload": "x" * (METRICS_PACKET_LIMITS["embedded_json_bytes"] + 50)}

        first = build_metrics_packet(
            targets=targets,
            evidence_records=evidence,
            questions=questions,
            update_candidates=candidates,
            embedded_json=embedded_json,
        )
        second = build_metrics_packet(
            targets=list(reversed(targets)),
            evidence_records=list(reversed(evidence)),
            questions=list(reversed(questions)),
            update_candidates=list(reversed(candidates)),
            embedded_json=embedded_json,
        )

        self.assertEqual(first, second)
        self.assertEqual(len(first["targets"]), METRICS_PACKET_LIMITS["targets"])
        self.assertEqual(len(first["evidence_records"]), METRICS_PACKET_LIMITS["evidence_records"])
        self.assertEqual(len(first["questions"]), METRICS_PACKET_LIMITS["questions"])
        self.assertEqual(len(first["update_candidates"]), METRICS_PACKET_LIMITS["update_candidates"])
        self.assertEqual(first["embedded_json"]["status"], "trimmed")
        self.assertLessEqual(first["embedded_json"]["byte_size"], METRICS_PACKET_LIMITS["embedded_json_bytes"])
        self.assertIn("targets_trimmed", first["warnings"])
        self.assertIn("evidence_records_trimmed", first["warnings"])
        self.assertIn("questions_trimmed", first["warnings"])
        self.assertIn("update_candidates_trimmed", first["warnings"])
        self.assertIn("embedded_json_trimmed", first["warnings"])

    def test_trace_intake_normalizes_supported_shapes_and_labels_gaps(self):
        packet = build_trace_packet(
            trace_sources=[
                {
                    "trace_source_type": "agents_sdk",
                    "trace_id": "trace-agents-1",
                    "group_id": "task-24",
                    "spans": [
                        {"span_type": "model"},
                        {"span_type": "tool"},
                        {"span_type": "handoff"},
                        {"span_type": "final_response"},
                    ],
                    "replay": {"command": "python -m unittest tests.product_agent_os.test_agent_skill_metrics -v"},
                },
                {
                    "trace_source_type": "opentelemetry_genai",
                    "trace_id": "trace-otel-1",
                    "group_id": "task-24",
                    "spans": [
                        {"attributes": {"gen_ai.operation.name": "chat"}},
                        {"attributes": {"gen_ai.operation.name": "tool_call"}},
                    ],
                },
                {
                    "trace_source_type": "tool_report",
                    "trace_id": "trace-tool-1",
                    "group_id": "task-24",
                    "tool_calls": [{"name": "shell_command", "status": "ok"}],
                },
                {
                    "trace_source_type": "accepted_gap",
                    "trace_id": "trace-gap-1",
                    "group_id": "task-24",
                    "accepted_gap": {"owner": "Quality", "reason": "live trace needs owner approval"},
                },
                {"trace_source_type": "unknown_vendor", "trace_id": "trace-unsupported"},
            ]
        )

        self.assertEqual(packet["schema_version"], 1)
        self.assertEqual(packet["write_policy"], "read_only")
        traces = {trace["trace_id"]: trace for trace in packet["traces"]}
        self.assertEqual(traces["trace-agents-1"]["status"], "complete")
        self.assertEqual(traces["trace-agents-1"]["trace_source_type"], "agents_sdk")
        self.assertEqual(traces["trace-agents-1"]["replayability"]["status"], "replayable")
        self.assertEqual(traces["trace-otel-1"]["trace_source_type"], "opentelemetry_genai")
        self.assertIn("handoff", traces["trace-otel-1"]["missing_span_types"])
        self.assertEqual(traces["trace-tool-1"]["trace_source_type"], "tool_report")
        self.assertEqual(traces["trace-gap-1"]["status"], "accepted_gap")
        self.assertEqual(traces["trace-unsupported"]["status"], "unsupported")
        self.assertIn("unsupported_trace_source", packet["warnings"])

    def test_metrics_redaction_gate_sanitizes_private_inputs_and_blocks_downstream_actions(self):
        packet = enforce_metrics_redaction_gate(
            {
                "target_id": "agent:reviewer",
                "raw_prompt": "Summarize private customer data for C:\\Users\\person\\repo",
                "tool_output": "TOKEN=abc123\nraw private chat log",
                "notes": "safe summary",
            }
        )
        serialized = json.dumps(packet, sort_keys=True)

        self.assertEqual(packet["schema_version"], 1)
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertEqual(packet["safety_status"], "blocked_pending_review")
        self.assertIn("raw_prompt", packet["redaction_summary"]["categories"])
        self.assertIn("raw_tool_output", packet["redaction_summary"]["categories"])
        self.assertIn("private_data", packet["redaction_summary"]["categories"])
        self.assertIn("scoring", packet["blocked_operations"])
        self.assertIn("report_rendering", packet["blocked_operations"])
        self.assertIn("update_candidates", packet["blocked_operations"])
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("TOKEN=abc123", serialized)
        self.assertNotIn("raw private chat log", serialized.lower())

    def test_evidence_dataset_builder_keeps_splits_separate_and_marks_duplicates(self):
        dataset = build_evidence_dataset(
            implemented_tasks=[{"sample_id": "task-24-batch-7", "source_type": "run_record"}],
            trace_packet={
                "traces": [
                    {
                        "trace_id": "trace-real-1",
                        "trace_source_type": "agents_sdk",
                        "status": "complete",
                    }
                ]
            },
            prior_failures=[{"sample_id": "failure-timeout", "source_type": "run_record"}],
            critical_slices=[{"sample_id": "security-boundary"}],
            edge_cases=[{"sample_id": "missing-span"}],
            holdout_cases=[{"sample_id": "holdout-1"}, {"sample_id": "failure-timeout"}],
            synthetic_regression_cases=[{"sample_id": "synthetic-no-secrets", "synthetic": True}],
            known_flaky_cases=[{"sample_id": "flaky-full-unittest"}],
        )

        groups = {record["group"] for record in dataset["records"]}
        self.assertEqual(dataset["schema_version"], 1)
        self.assertIn("implemented_task", groups)
        self.assertIn("real_trace_sample", groups)
        self.assertIn("prior_failure", groups)
        self.assertIn("critical_slice", groups)
        self.assertIn("edge_adversarial", groups)
        self.assertIn("holdout", groups)
        self.assertIn("synthetic_regression", groups)
        self.assertIn("known_flaky", groups)
        self.assertEqual(dataset["split_summary"]["holdout"], 2)
        self.assertEqual(dataset["leakage_status"], "leakage_detected")
        self.assertIn("failure-timeout", dataset["leakage_sample_ids"])
        prior = [record for record in dataset["records"] if record["sample_id"] == "failure-timeout"]
        self.assertEqual({record["split"] for record in prior}, {"prior_failure", "holdout"})

    def test_dataset_quality_gates_block_confident_decisions_on_missing_or_leaky_data(self):
        dataset = build_evidence_dataset(
            implemented_tasks=[{"sample_id": "task-only"}],
            holdout_cases=[{"sample_id": "same-sample"}],
            synthetic_regression_cases=[{"sample_id": "same-sample"}],
        )

        quality = evaluate_dataset_quality(dataset, min_samples=6, min_real_trace_samples=1)

        self.assertEqual(quality["decision_status"], "blocked_insufficient_dataset")
        self.assertIn("prior_failure", quality["missing_expected_splits"])
        self.assertTrue(quality["low_real_trace_coverage"])
        self.assertTrue(quality["insufficient_sample"])
        self.assertEqual(quality["leakage_status"], "leakage_detected")
        self.assertGreater(quality["dataset_duplicate_rate"], 0)

    def test_grader_runner_records_local_and_human_contracts_without_live_judge_calls(self):
        summary = build_grader_run_summary(
            metric_graders=[{"rubric_id": "tool-accuracy", "sample_size": 12, "passed": 10, "failed": 2}],
            trace_graders=[{"rubric_id": "trace-completeness", "sample_size": 5, "passed": 4, "failed": 1}],
            human_audits=[{"rubric_id": "owner-review", "labels": ["pass", "fail", "pass"]}],
            llm_judges=[
                {"rubric_id": "judge-v1", "mode": "metadata_only", "sample_size": 0},
                {"rubric_id": "live-judge", "mode": "live_model_call", "sample_size": 4},
            ],
        )

        self.assertEqual(summary["schema_version"], 1)
        self.assertEqual(summary["external_calls"], "not_performed")
        grader_types = {grader["grader_type"] for grader in summary["graders"]}
        self.assertIn("metric", grader_types)
        self.assertIn("trace", grader_types)
        self.assertIn("human_audit", grader_types)
        self.assertIn("llm_as_judge_metadata", grader_types)
        self.assertIn("unsupported_live_judge", summary["unsupported_gaps"])

    def test_judge_calibration_blocks_candidate_approval_until_calibrated(self):
        uncalibrated = build_judge_calibration_summary(
            judge_labels=["pass", "pass", "fail", "fail"],
            human_labels=["pass", "fail", "fail", "pass"],
            min_sample_size=20,
        )

        self.assertEqual(uncalibrated["status"], "judge_not_calibrated")
        self.assertTrue(uncalibrated["blocks_candidate_approval"])
        self.assertEqual(uncalibrated["sample_size"], 4)
        self.assertAlmostEqual(uncalibrated["judge_human_agreement"], 0.5)
        self.assertAlmostEqual(uncalibrated["judge_precision"], 0.5)
        self.assertAlmostEqual(uncalibrated["judge_recall"], 0.5)
        self.assertAlmostEqual(uncalibrated["cohen_kappa"], 0.0)

        calibrated = build_judge_calibration_summary(
            judge_labels=["pass", "pass", "fail", "fail"],
            human_labels=["pass", "pass", "fail", "fail"],
            min_sample_size=4,
        )

        self.assertEqual(calibrated["status"], "calibrated")
        self.assertFalse(calibrated["blocks_candidate_approval"])

    def test_metric_aggregation_emits_required_sections_with_raw_counts(self):
        metrics = build_metric_aggregation(
            outcome_records=[
                {
                    "task_success": True,
                    "regression_free": True,
                    "final_state_correct": True,
                    "false_pass": False,
                    "false_fail": False,
                },
                {
                    "task_success": False,
                    "regression_free": False,
                    "final_state_correct": False,
                    "false_pass": True,
                    "false_fail": False,
                },
            ],
            trajectory_records=[
                {
                    "tool_selection_correct": True,
                    "tool_argument_correct": True,
                    "trace_complete": True,
                    "replayable_trace": True,
                },
                {
                    "tool_selection_correct": True,
                    "tool_argument_correct": False,
                    "trace_complete": False,
                    "replayable_trace": False,
                },
            ],
            reliability_records=[
                {"flake": False, "replay_success": True, "repeated_run_instability": False},
                {"flake": True, "replay_success": False, "repeated_run_instability": True},
            ],
            skill_records=[
                {"skill_expected": True, "skill_triggered": True, "skill_adhered": True},
                {"skill_expected": True, "skill_triggered": False, "skill_adhered": False},
            ],
            cost_latency_records=[
                {"cost_usd": 0.20, "baseline_cost_usd": 0.25, "latency_ms": 800},
                {"cost_usd": 0.30, "baseline_cost_usd": 0.20, "latency_ms": 1200},
            ],
            safety_records=[
                {"instruction_violation": False, "approval_violation": False},
                {"instruction_violation": True, "approval_violation": False},
            ],
        )

        self.assertEqual(metrics["schema_version"], 1)
        self.assertEqual(metrics["write_policy"], "read_only")
        expected_sections = {
            "outcome",
            "trajectory",
            "harness_reliability",
            "harness_optimizer",
            "skill",
            "cost_latency",
            "safety",
        }
        self.assertEqual(set(metrics["sections"]), expected_sections)
        for section in metrics["sections"].values():
            for metric in section["metrics"].values():
                with self.subTest(metric=metric["metric_id"]):
                    self.assertIn("numerator", metric)
                    self.assertIn("denominator", metric)
                    self.assertIn(metric["status"], {"ready", "insufficient_data"})
        self.assertEqual(metrics["sections"]["outcome"]["metrics"]["task_success_rate"]["numerator"], 1)
        self.assertEqual(metrics["sections"]["outcome"]["metrics"]["task_success_rate"]["denominator"], 2)
        self.assertEqual(metrics["sections"]["trajectory"]["metrics"]["tool_argument_accuracy"]["numerator"], 1)
        self.assertEqual(metrics["sections"]["trajectory"]["metrics"]["trace_completeness"]["value"], 0.5)
        self.assertEqual(metrics["sections"]["harness_reliability"]["metrics"]["flake_rate"]["value"], 0.5)
        self.assertEqual(metrics["sections"]["cost_latency"]["metrics"]["total_cost_usd"]["numerator"], 0.5)
        self.assertEqual(metrics["sections"]["cost_latency"]["metrics"]["p95_latency_ms"]["value"], 1200.0)
        self.assertEqual(metrics["sections"]["safety"]["metrics"]["instruction_violation_rate"]["numerator"], 1)

    def test_repeatability_metrics_block_single_lucky_run_promotion(self):
        repeatability = calculate_repeatability_metrics(
            replay_cases=[
                {
                    "case_id": "stable-pass",
                    "runs": [
                        {"passed": True, "replay_success": True},
                        {"passed": True, "replay_success": True},
                        {"passed": True, "replay_success": True},
                    ],
                },
                {
                    "case_id": "unstable",
                    "runs": [
                        {"passed": True, "replay_success": True},
                        {"passed": False, "replay_success": False},
                        {"passed": True, "replay_success": True},
                    ],
                },
            ],
            k=3,
        )

        self.assertEqual(repeatability["status"], "ready")
        self.assertEqual(repeatability["metrics"]["pass_at_k"]["numerator"], 2)
        self.assertEqual(repeatability["metrics"]["pass_at_k"]["denominator"], 2)
        self.assertEqual(repeatability["metrics"]["pass_power_k"]["numerator"], 1)
        self.assertEqual(repeatability["metrics"]["pass_power_k"]["denominator"], 2)
        self.assertEqual(repeatability["metrics"]["repeated_run_instability"]["value"], 0.5)
        self.assertEqual(repeatability["promotion_policy"]["single_success_promotion"], "blocked")

        lucky = calculate_repeatability_metrics(
            replay_cases=[{"case_id": "lucky", "runs": [{"passed": True, "replay_success": True}]}],
            k=3,
        )

        self.assertEqual(lucky["status"], "insufficient_replay_evidence")
        self.assertIn("single_lucky_run", lucky["insufficient_reasons"])
        self.assertEqual(lucky["promotion_policy"]["decision"], "blocked_single_lucky_run")

    def test_scorecards_use_weights_and_do_not_hide_guardrail_regressions(self):
        metrics = build_metric_aggregation(
            outcome_records=[
                {"task_success": True, "regression_free": True, "final_state_correct": True, "false_pass": False},
                {"task_success": True, "regression_free": True, "final_state_correct": True, "false_pass": False},
            ],
            trajectory_records=[
                {"tool_selection_correct": True, "tool_argument_correct": True, "trace_complete": True},
                {"tool_selection_correct": True, "tool_argument_correct": True, "trace_complete": True},
            ],
            reliability_records=[
                {"flake": False, "replay_success": True},
                {"flake": False, "replay_success": True},
            ],
            skill_records=[
                {"skill_expected": True, "skill_triggered": True, "skill_adhered": True},
                {"skill_expected": True, "skill_triggered": True, "skill_adhered": True},
            ],
            cost_latency_records=[
                {"cost_usd": 0.10, "baseline_cost_usd": 0.20, "latency_ms": 500},
                {"cost_usd": 0.10, "baseline_cost_usd": 0.20, "latency_ms": 600},
            ],
            safety_records=[
                {"instruction_violation": False, "approval_violation": False},
                {"instruction_violation": True, "approval_violation": False},
            ],
        )

        scorecards = calculate_scorecards(metric_packet=metrics)

        self.assertEqual(scorecards["schema_version"], 1)
        self.assertIn("harness_quality_score", scorecards["scorecards"])
        self.assertIn("agentic_task_score", scorecards["scorecards"])
        self.assertIn("harness_optimization_score", scorecards["scorecards"])
        for scorecard in scorecards["scorecards"].values():
            with self.subTest(scorecard=scorecard["scorecard_id"]):
                self.assertIn("weights", scorecard)
                self.assertGreaterEqual(scorecard["score"], 0.0)
                self.assertLessEqual(scorecard["score"], 1.0)
        self.assertEqual(scorecards["overall_status"], "blocked_by_guardrail")
        self.assertIn("safety_violation", scorecards["guardrail_blockers"])
        self.assertIn("instruction_violation_rate", scorecards["guardrail_metrics"])

        missing = calculate_scorecards(metric_packet=build_metric_aggregation())
        self.assertEqual(missing["overall_status"], "insufficient_data")
        self.assertIn("missing_data", missing["scorecards"]["harness_quality_score"])

    def test_confidence_and_decision_gates_require_statistical_and_safety_evidence(self):
        current = build_metric_aggregation(
            outcome_records=[
                {
                    "task_success": index < 48,
                    "regression_free": True,
                    "final_state_correct": index < 48,
                    "false_pass": index == 49,
                }
                for index in range(50)
            ],
            trajectory_records=[
                {
                    "tool_selection_correct": True,
                    "tool_argument_correct": True,
                    "trace_complete": index < 49,
                    "replayable_trace": True,
                }
                for index in range(50)
            ],
            reliability_records=[{"flake": index == 49, "replay_success": True} for index in range(50)],
            cost_latency_records=[{"cost_usd": 0.10, "baseline_cost_usd": 0.11, "latency_ms": 500} for _ in range(50)],
            safety_records=[{"instruction_violation": False, "approval_violation": False} for _ in range(50)],
        )
        baseline = build_metric_aggregation(
            outcome_records=[{"task_success": index < 43, "regression_free": True} for index in range(50)],
            trajectory_records=[{"trace_complete": True} for _ in range(50)],
            reliability_records=[{"flake": False} for _ in range(50)],
            cost_latency_records=[{"cost_usd": 0.11, "baseline_cost_usd": 0.11, "latency_ms": 500} for _ in range(50)],
            safety_records=[{"instruction_violation": False, "approval_violation": False} for _ in range(50)],
        )

        decision = evaluate_confidence_and_decision_gates(
            current_metric_packet=current,
            baseline_metric_packet=baseline,
            owner_review_status="owner_reviewed",
        )

        self.assertEqual(decision["decision_status"], "weekly_acceptance_ready")
        self.assertGreater(decision["statistical_evidence"]["task_success_rate"]["wilson_lower_bound"], 0.85)
        self.assertGreater(decision["statistical_evidence"]["task_success_rate"]["delta_vs_baseline"], 0)
        self.assertEqual(decision["blockers"], [])

        blocked = evaluate_confidence_and_decision_gates(
            current_metric_packet=current,
            baseline_metric_packet=baseline,
            owner_review_status="missing",
            critical_regressions=["approval-policy-regression"],
            thresholds={"max_false_pass_rate": 0.0, "max_flake_rate": 0.0, "max_cost_regression_rate": 0.0},
        )

        self.assertEqual(blocked["decision_status"], "blocked_by_gate")
        self.assertIn("critical_regression", blocked["blockers"])
        self.assertIn("owner_review_or_gap_missing", blocked["blockers"])
        self.assertIn("false_pass_threshold_exceeded", blocked["blockers"])
        self.assertIn("flake_threshold_exceeded", blocked["blockers"])

    def test_cadence_recommender_routes_levels_without_creating_active_schedules(self):
        high_risk = recommend_metrics_cadence(
            target={
                "target_id": "automation_candidate:daily-metrics",
                "risk_level": "high",
                "usage_volume": "high",
                "tool_permission_level": "approval_bound",
                "production_impact": True,
                "target_type": "automation_candidate",
            },
            metrics_summary={"flake_rate": 0.2, "trace_completeness": 0.5},
        )

        self.assertEqual(high_risk["cadence_level"], "L3")
        self.assertEqual(high_risk["schedule_policy"], "suggested_only")
        self.assertEqual(high_risk["active_schedule_status"], "approval_required")
        self.assertIn("daily", high_risk["recommended_cadence"])
        self.assertIn("incident_triggered", high_risk["recommended_cadence"])

        low_risk = recommend_metrics_cadence(
            target={
                "target_id": "skill:docs-maintainer",
                "risk_level": "low",
                "usage_volume": "low",
                "tool_permission_level": "read_only",
                "production_impact": False,
            },
            metrics_summary={"flake_rate": 0.0, "trace_completeness": 1.0},
        )
        self.assertEqual(low_risk["cadence_level"], "L0")
        self.assertEqual(low_risk["recommended_cadence"], ["on_change"])

        override = recommend_metrics_cadence(target=low_risk["target"], metrics_summary={}, owner_override="L1")
        self.assertEqual(override["cadence_level"], "L1")
        self.assertIn("owner_override", override["reasons"])

    def test_run_record_builder_redacts_evidence_and_rejects_dashboard_as_source(self):
        kwargs = {
            "run_id": "run-batch-9",
            "generated_at": "2026-05-28T12:00:00Z",
            "cadence": {"cadence_level": "L2", "recommended_cadence": ["weekly", "on_change"]},
            "window": {"started_at": "2026-05-28T00:00:00Z", "ended_at": "2026-05-28T12:00:00Z"},
            "dataset_split": "holdout",
            "target": {"target_id": "skill:review-slice", "version": "1.2.0"},
            "versions": {"plugin": "0.1.0", "harness": "2026.05.28"},
            "model": "gpt-5",
            "reasoning_effort": "medium",
            "repo_sha": "",
            "repo_sha_gap": {"owner": "Release", "reason": "workspace has no git remote in fixture"},
            "environment": {"os": "Windows", "workspace": "C:\\Users\\person\\private-project"},
            "trace_metadata": {"trace_id": "trace-1", "trace_source_type": "agents_sdk"},
            "artifacts": [
                {"artifact_id": "eval-report", "source_type": "eval_packet", "path": ".codex/eval-reports/eval.json"},
                {"artifact_id": "dashboard", "source_type": "status_dashboard_html", "path": ".codex/status.html"},
            ],
            "scores": {"harness_quality_score": 0.91},
            "statistical_evidence": {"task_success_rate": {"wilson_lower_bound": 0.88}},
            "cost_latency": {"total_cost_usd": 0.5, "p95_latency_ms": 1200},
            "update_decision": {"decision": "keep_current", "reason": "no approved candidate"},
            "review": {"owner_review_status": "owner_reviewed", "reviewer": "Quality"},
            "evidence": {"raw_prompt": "secret prompt TOKEN=abc123", "summary": "safe"},
        }

        first = build_metrics_run_record(**kwargs)
        second = build_metrics_run_record(**kwargs)
        serialized = json.dumps(first, sort_keys=True)

        self.assertEqual(first, second)
        self.assertEqual(first["schema_version"], 1)
        self.assertEqual(first["write_policy"], "read_only")
        self.assertEqual(first["repo"]["repo_sha_status"], "accepted_gap")
        self.assertEqual(first["run_id"], "run-batch-9")
        for key in [
            "cadence",
            "window",
            "dataset_split",
            "target",
            "versions",
            "model",
            "reasoning_effort",
            "environment",
            "trace_metadata",
            "artifacts",
            "scores",
            "statistical_evidence",
            "cost_latency",
            "update_decision",
            "review",
        ]:
            self.assertIn(key, first)
        self.assertEqual(first["artifact_policy"]["dashboard_as_source_claim"], "rejected")
        self.assertEqual(first["excluded_artifacts"][0]["source_type"], "status_dashboard_html")
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("TOKEN=abc123", serialized)
        self.assertNotIn("secret prompt", serialized.lower())

    def test_trace_data_classification_gate_blocks_real_trace_without_policy_or_gap(self):
        blocked = enforce_trace_data_classification_gate(
            {
                "traces": [
                    {
                        "trace_id": "real-trace-1",
                        "trace_source_type": "agents_sdk",
                        "synthetic": False,
                    },
                    {
                        "trace_id": "synthetic-trace-1",
                        "trace_source_type": "tool_report",
                        "synthetic": True,
                    },
                ]
            },
            data_classification_register_present=False,
            secrets_policy_present=False,
            accepted_gap=None,
        )

        self.assertEqual(blocked["status"], "blocked")
        self.assertIn("real_trace_requires_data_classification_or_gap", blocked["blockers"])
        self.assertEqual(blocked["blocked_trace_ids"], ["real-trace-1"])
        self.assertEqual(blocked["allowed_trace_ids"], ["synthetic-trace-1"])
        self.assertIn("data-classification-register.md", blocked["required_artifacts"])
        self.assertIn("secrets-policy.md", blocked["required_artifacts"])

        allowed = enforce_trace_data_classification_gate(
            {"traces": [{"trace_id": "real-trace-1", "synthetic": False}]},
            data_classification_register_present=False,
            secrets_policy_present=False,
            accepted_gap={"owner": "Security", "reason": "fixture trace has no customer data"},
        )

        self.assertEqual(allowed["status"], "accepted_gap")
        self.assertEqual(allowed["blocked_trace_ids"], [])

    def test_scorecard_ledger_record_and_markdown_are_append_only_and_source_backed(self):
        record = build_scorecard_ledger_record(
            ledger_id="ledger-skill-review",
            generated_at="2026-05-28T10:00:00Z",
            baseline_version={"skill:review": "1.0.0"},
            current_version={"skill:review": "1.1.0"},
            candidate_version={"skill:review": "1.2.0-candidate"},
            run_record_ids=["run-2026-05-28"],
            raw_counts={"task_success_rate": {"numerator": 48, "denominator": 50}},
            confidence_intervals={"task_success_rate": {"lower": 0.86, "upper": 0.99}},
            cost_latency={"total_cost_usd": 0.42, "p95_latency_ms": 1200},
            evidence_links=[".codex/eval-reports/run-2026-05-28.json"],
            redaction_status="ready",
            report_anchors=["#target-skill-review"],
        )
        markdown = render_scorecard_ledger_markdown(record)
        serialized = json.dumps(record, sort_keys=True)

        self.assertEqual(record["schema_version"], 1)
        self.assertEqual(record["write_policy"], "read_only")
        self.assertEqual(record["ledger_policy"], "append_only")
        self.assertEqual(record["run_record_ids"], ["run-2026-05-28"])
        self.assertEqual(record["raw_counts"]["task_success_rate"]["denominator"], 50)
        self.assertIn("confidence_intervals", record)
        self.assertIn("report_anchors", record)
        self.assertIn("Append-only policy", markdown)
        self.assertIn("#target-skill-review", markdown)
        self.assertNotIn("TOKEN=", serialized + markdown)

    def test_completion_skeptic_metrics_loop_record_preserves_manual_only_boundary(self):
        record = build_completion_skeptic_metrics_loop_record(
            generated_at="2026-06-10T08:40:00+03:00",
            pilot_ledger={
                "ledger_id": "completion_skeptic_manual_pilot_ledger",
                "sample_size": 5,
                "pilot_scope": "synthetic_local",
                "no_unapproved_actions": True,
            },
            scorecard_calibration={
                "calibration_id": "completion_skeptic_scorecard_calibration",
                "decision_status": "calibrated_with_accepted_metrics_gap",
                "owner_review_status": "accepted_gap",
                "metric_evidence": {
                    "false_pass_rate": {"numerator": 0, "denominator": 5},
                    "false_rewrite_rate": {"numerator": 0, "denominator": 5},
                    "evidence_sufficiency_rate": {"numerator": 5, "denominator": 5},
                    "missing_check_catch_rate": {"numerator": 5, "denominator": 5},
                    "accepted_gap_rate": {"numerator": 1, "denominator": 5},
                    "user_revision_acceptance_rate": {"numerator": 5, "denominator": 5},
                    "revision_usefulness_rate": {"numerator": 5, "denominator": 5},
                },
            },
            closure_packet={
                "packet_id": "completion_skeptic_go_no_go_closure",
                "decision_status": "manual_only",
                "promotion_status": "not_promoted",
                "next_approval_needs": ["exact_owner_approval_for_release_or_automation"],
            },
            evidence_links=["docs/sources/product-agent-os-batch40-doubt-verifier-pilot-closure.md"],
        )

        self.assertEqual(record["ledger_id"], "completion_skeptic_scorecard_calibration")
        self.assertEqual(record["ledger_policy"], "append_only")
        self.assertEqual(record["decision_status"], "manual_only")
        self.assertEqual(record["promotion_status"], "not_promoted")
        self.assertEqual(record["raw_counts"]["false_pass_rate"]["denominator"], 5)
        self.assertEqual(record["raw_counts"]["revision_usefulness_rate"]["numerator"], 5)
        self.assertEqual(record["pilot_denominators"]["sample_size"], 5)
        self.assertIn("automation", record["blocked_promotions"])
        self.assertEqual(record["update_policy"], "staged_evidence_only_no_auto_apply")

    def test_daily_metrics_report_recommends_safe_next_actions_without_autofix(self):
        report = build_daily_metrics_report(
            generated_at="2026-05-28T10:00:00Z",
            evidence_window={"started_at": "2026-05-28T00:00:00Z", "ended_at": "2026-05-28T10:00:00Z"},
            target_reports=[
                {
                    "target": {"target_id": "skill:review-slice", "version": "1.1.0"},
                    "decision_status": "blocked_by_gate",
                    "blockers": ["false_pass_threshold_exceeded"],
                    "confidence_status": "blocked",
                },
                {
                    "target": {"target_id": "skill:planner", "version": "2.0.0"},
                    "decision_status": "weekly_acceptance_ready",
                    "update_candidates": [{"candidate_id": "candidate-skill-planner"}],
                    "changed_version": "2.0.1-candidate",
                },
                {
                    "target": {"target_id": "agent:docs-maintainer", "version": "1.0.0"},
                    "decision_status": "insufficient_data",
                    "evidence_gaps": ["missing_real_trace"],
                },
            ],
            trace_source_mix={"agents_sdk": 2, "accepted_gap": 1},
            changed_versions=["skill:planner@2.0.1-candidate"],
            failure_groups=["false_pass_threshold_exceeded"],
        )
        actions = {item["target_id"]: item["recommendation"] for item in report["target_recommendations"]}

        self.assertEqual(report["schema_version"], 1)
        self.assertEqual(report["auto_fix_policy"], "never_from_one_noisy_run")
        self.assertEqual(actions["skill:review-slice"], "block_promotion")
        self.assertEqual(actions["skill:planner"], "stage_candidate_for_review")
        self.assertEqual(actions["agent:docs-maintainer"], "request_human_audit")
        self.assertIn("trace_source_mix", report)
        self.assertIn("next_safe_action", report)

    def test_weekly_verifier_blocks_without_owner_rollback_holdout_flake_and_cost_evidence(self):
        blocked = build_weekly_verification_packet(
            generated_at="2026-05-28T10:00:00Z",
            rolling_window={"days": 7, "status": "present"},
            baseline={"version": "1.0.0", "task_success_rate": 0.86},
            previous_week={"version": "1.1.0", "task_success_rate": 0.88},
            holdout={"status": "missing"},
            regression_findings=[{"finding_id": "false-pass-1", "severity": "high"}],
            update_candidates=[{"candidate_id": "skill-planner-2"}],
            rollback_target="",
            owner_review_status="missing",
            false_pass_audit_status="missing",
            flake_replay_status="missing",
            cost_regression_check_status="missing",
        )

        self.assertEqual(blocked["status"], "blocked")
        self.assertIn("rollback_target_missing", blocked["blockers"])
        self.assertIn("owner_review_missing", blocked["blockers"])
        self.assertIn("holdout_check_missing", blocked["blockers"])
        self.assertIn("false_pass_audit_missing", blocked["blockers"])
        self.assertIn("flake_replay_missing", blocked["blockers"])
        self.assertIn("cost_regression_check_missing", blocked["blockers"])
        self.assertEqual(blocked["regression_findings"][0]["finding_id"], "false-pass-1")
        self.assertEqual(blocked["update_candidates"][0]["candidate_id"], "skill-planner-2")

    def test_component_prioritization_uses_failure_taxonomy_and_evidence_sufficiency(self):
        prioritized = prioritize_improvement_components(
            failure_taxonomy=[
                {
                    "component": "prompt",
                    "failure_modes": ["tool_argument_mismatch"],
                    "affected_metrics": {"tool_argument_accuracy": -0.22},
                    "evidence_status": "sufficient",
                },
                {
                    "component": "dataset",
                    "failure_modes": ["missing_holdout"],
                    "affected_metrics": {"task_success_rate": -0.08},
                    "evidence_status": "insufficient",
                },
                {
                    "component": "approval_policy",
                    "failure_modes": [],
                    "affected_metrics": {},
                    "evidence_status": "none",
                },
            ]
        )
        by_component = {item["component"]: item for item in prioritized["priorities"]}

        self.assertEqual(prioritized["schema_version"], 1)
        self.assertEqual(by_component["prompt"]["decision"], "change")
        self.assertEqual(by_component["dataset"]["decision"], "defer")
        self.assertEqual(by_component["approval_policy"]["decision"], "leave_unchanged")
        self.assertLess(by_component["prompt"]["rank"], by_component["dataset"]["rank"])
        self.assertIn("tool_argument_mismatch", by_component["prompt"]["reason"])

    def test_modernization_candidate_generator_stages_only_source_backed_candidates(self):
        packet = generate_modernization_candidates(
            component_priorities=[
                {
                    "component": "skill",
                    "decision": "change",
                    "reason": "skill trigger recall regression",
                    "affected_metrics": {"skill_trigger_recall": -0.18},
                    "evidence_status": "sufficient",
                    "target_id": "skill:review-slice",
                    "expected_impact": "restore trigger recall",
                    "risk": "medium",
                    "approval_state": "not_requested",
                    "rollback_target": "skill:review-slice@1.1.0",
                },
                {
                    "component": "prompt",
                    "decision": "change",
                    "reason": "headline score improved",
                    "affected_metrics": {},
                    "evidence_status": "insufficient",
                    "target_id": "prompt_pack:review",
                    "expected_impact": "",
                    "risk": "unknown",
                    "approval_state": "not_requested",
                    "rollback_target": "",
                },
            ]
        )
        by_component = {item["component"]: item for item in packet["candidates"]}

        self.assertEqual(packet["schema_version"], 1)
        self.assertEqual(by_component["skill"]["status"], "staged_for_review")
        self.assertEqual(by_component["skill"]["external_write_action"], "none")
        self.assertEqual(by_component["skill"]["rollback_target"], "skill:review-slice@1.1.0")
        self.assertEqual(by_component["prompt"]["status"], "blocked")
        self.assertIn("headline_only_or_insufficient_evidence", by_component["prompt"]["blockers"])
        self.assertEqual(packet["apply_policy"], "cannot_apply_patches")

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
