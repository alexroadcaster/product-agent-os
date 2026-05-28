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
    build_evidence_packet,
    build_evidence_dataset,
    build_grader_run_summary,
    build_judge_calibration_summary,
    build_metrics_packet,
    build_trace_packet,
    collect_target_registry,
    enforce_metrics_redaction_gate,
    evaluate_dataset_quality,
    source_priority_policy,
)


class AgentSkillMetricsTest(unittest.TestCase):
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

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
