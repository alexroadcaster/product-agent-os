import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.agent_skill_metrics import build_execution_loop_metrics  # noqa: E402


def run_record(**overrides):
    record = {
        "time_to_first_target_diff_seconds": 300,
        "agent_count": 1,
        "review_cycles": 1,
        "repeated_unchanged_commands": 0,
        "control_plane_writes_before_acceptance": 1,
        "target_churn_lines": 100,
        "test_churn_lines": 80,
        "compaction_count": 0,
        "stale_lifecycle_markers": 0,
        "mixed_skill_source_events": 0,
        "projection_conflicts": 0,
    }
    record.update(overrides)
    return record


class ExecutionLoopMetricsTest(unittest.TestCase):
    def test_within_budget_run_is_diagnostic_only(self):
        result = build_execution_loop_metrics([run_record()])
        self.assertEqual("within_budget", result["status"])
        self.assertEqual([], result["stop_triggers"])
        self.assertFalse(result["automation_allowed"])
        self.assertEqual("manual_local_diagnostic_only", result["evidence_ceiling"])

    def test_loop_regressions_create_stop_triggers(self):
        result = build_execution_loop_metrics(
            [
                run_record(
                    time_to_first_target_diff_seconds=1900,
                    agent_count=6,
                    review_cycles=3,
                    repeated_unchanged_commands=4,
                    target_churn_lines=100,
                    test_churn_lines=300,
                    stale_lifecycle_markers=1,
                    mixed_skill_source_events=1,
                    projection_conflicts=1,
                )
            ]
        )
        self.assertEqual("intervention_required", result["status"])
        self.assertIn("agent_count_budget_exceeded", result["stop_triggers"])
        self.assertIn("repeated_unchanged_commands_budget_exceeded", result["stop_triggers"])
        self.assertIn("test_churn_exceeds_2x_target_churn", result["stop_triggers"])
        self.assertIn("repair canonical state or skill provenance before resuming", result["recommendations"])

    def test_missing_records_are_not_success(self):
        result = build_execution_loop_metrics([])
        self.assertEqual("insufficient_evidence", result["status"])
        self.assertEqual(["missing_execution_records"], result["stop_triggers"])

    def test_malformed_values_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "expected_non_negative_integer"):
            build_execution_loop_metrics([run_record(agent_count=-1)])


if __name__ == "__main__":
    unittest.main()
