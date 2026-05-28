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
    build_metrics_packet,
    collect_target_registry,
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

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
