import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
FIXTURES = ROOT / "plugins" / "product-agent-os" / "assets" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.agent_skill_metrics_report import (  # noqa: E402
    METRICS_REPORT_TARGET,
    build_agent_skill_metrics_report_manifest,
    render_agent_skill_metrics_report,
    render_agent_skill_metrics_report_plan,
    stage_agent_skill_metrics_report,
    validate_agent_skill_metrics_report_manifest,
)
from product_agent_os.offline_artifact_safety import GENERATED_VIEW_ONLY_TEXT  # noqa: E402
from product_agent_os.stage_manifest import MANIFEST_NAME  # noqa: E402


class AgentSkillMetricsReportTest(unittest.TestCase):
    def test_report_manifest_records_sources_redaction_and_archive_policy(self):
        manifest = build_agent_skill_metrics_report_manifest(
            report_id="agent-skill-report-2026-05-28",
            generated_at="2026-05-28T10:00:00Z",
            project_id="C:\\Users\\person\\private-project",
            eval_window={"started_at": "2026-05-28T00:00:00Z", "ended_at": "2026-05-28T10:00:00Z"},
            cadence={"level": "L2", "recommended": ["daily", "weekly"]},
            source_datasets=[".codex/eval-reports/run-2026-05-28.json"],
            trace_sources=["agents_sdk", "accepted_gap"],
            redaction_status="ready",
            archive=True,
        )
        serialized = json.dumps(manifest, sort_keys=True)

        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["write_policy"], "read_only")
        self.assertEqual(manifest["report_id"], "agent-skill-report-2026-05-28")
        self.assertEqual(manifest["current_report_path"], METRICS_REPORT_TARGET)
        self.assertEqual(manifest["redaction_status"], "ready")
        self.assertEqual(manifest["archive_policy"]["status"], "enabled")
        self.assertIn("archive", manifest["archive_policy"]["archive_report_path"])
        self.assertNotIn("C:\\Users\\person", serialized)

    def test_renderer_outputs_offline_report_with_redacted_bounded_json_and_no_approval_claim(self):
        result = render_agent_skill_metrics_report(_report_packet())
        html = result["html"]
        lower = html.lower()

        self.assertEqual(result["status"], "ready")
        self.assertTrue(lower.startswith("<!doctype html>"))
        self.assertIn('<meta name="viewport"', lower)
        self.assertNotIn("http://", lower)
        self.assertNotIn("https://", lower)
        self.assertNotIn("<script src=", lower)
        self.assertIn(GENERATED_VIEW_ONLY_TEXT, html)
        self.assertIn('id="target-skill-review-slice"', html)
        self.assertIn('id="metric-task_success_rate"', html)
        self.assertIn('id="execution-loop-metrics"', html)
        self.assertIn("intervention_required", html)
        self.assertIn("repeated_unchanged_commands_budget_exceeded", html)
        self.assertIn("48 / 50", html)
        self.assertIn("Insufficient data", html)
        self.assertIn("summary-grid", html)
        self.assertIn("summary-card", html)
        self.assertIn("generated-view-policy", html)
        self.assertIn("current", lower)
        self.assertIn("candidate", lower)
        self.assertIn('<script type="application/json" id="agent-skill-report-data">', html)
        self.assertNotIn("</script><script", html)
        self.assertNotIn("TOKEN=abc123", html + result["json"])
        self.assertNotIn("C:\\Users\\person", html + result["json"])
        self.assertEqual(result["validation"]["errors"], [])
        self.assertLessEqual(result["embedded_json_bytes"], 12_000)

    def test_report_staging_is_explicit_opt_in_and_preserves_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "workspace"
            stage_root = Path(tmp) / "stage"
            shutil.copytree(FIXTURES / "empty-repo", workspace)
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))

            dry_run = render_agent_skill_metrics_report_plan(workspace, _report_packet())
            result = stage_agent_skill_metrics_report(workspace, stage_root, _report_packet(), archive=True)
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*"))

            self.assertEqual(before, after)
            self.assertEqual(dry_run["rendered_artifacts"]["mode"], "dry-run")
            self.assertEqual(result["rendered_artifacts"]["mode"], "stage")
            by_target = {item["target_path"]: item for item in result["rendered_artifacts"]["files"]}
            self.assertIn(METRICS_REPORT_TARGET, by_target)
            self.assertTrue((stage_root / METRICS_REPORT_TARGET).exists())
            self.assertTrue((stage_root / MANIFEST_NAME).exists())
            self.assertEqual(validate_agent_skill_metrics_report_manifest(stage_root), [])
            archive_targets = [
                target
                for target in by_target
                if target.startswith(".codex/eval-reports/archive/")
            ]
            self.assertEqual(len(archive_targets), 1)
            self.assertTrue((stage_root / archive_targets[0]).exists())
            self.assertFalse((workspace / METRICS_REPORT_TARGET).exists())


def _report_packet():
    return {
        "report_id": "agent-skill-report-2026-05-28",
        "generated_at": "2026-05-28T10:00:00Z",
        "project_id": "product-agent-os",
        "eval_window": {"started_at": "2026-05-28T00:00:00Z", "ended_at": "2026-05-28T10:00:00Z"},
        "cadence": {"level": "L2", "recommended": ["daily", "weekly"]},
        "target_inventory": [
            {"target_id": "skill:review-slice", "target_type": "skill", "version": "1.1.0"}
        ],
        "metrics": {
            "sections": {
                "outcome": {
                    "metrics": {
                        "task_success_rate": {
                            "metric_id": "task_success_rate",
                            "numerator": 48,
                            "denominator": 50,
                            "value": 0.96,
                            "status": "ready",
                        },
                        "final_state_accuracy": {
                            "metric_id": "final_state_accuracy",
                            "numerator": 0,
                            "denominator": 0,
                            "value": None,
                            "status": "insufficient_data",
                        },
                    }
                }
            }
        },
        "execution_loop_metrics": {
            "status": "intervention_required",
            "evidence_ceiling": "manual_local_diagnostic_only",
            "stop_triggers": ["repeated_unchanged_commands_budget_exceeded"],
            "recommendations": ["do not rerun a command until a named input changes"],
        },
        "version_comparison": {
            "baseline": {"skill:review-slice": "1.0.0"},
            "current": {"skill:review-slice": "1.1.0"},
            "candidate": {"skill:review-slice": "1.2.0-candidate"},
        },
        "scorecards": {"overall_status": "ready", "scorecards": {}},
        "trace_evidence": {"trace_sources": ["agents_sdk"], "raw_path": "C:\\Users\\person\\private-project"},
        "update_candidates": [{"candidate_id": "skill-review-1", "approval_state": "not_requested"}],
        "raw_appendix": {"tool_output": "TOKEN=abc123"},
        "source_datasets": [".codex/eval-reports/run-2026-05-28.json"],
        "redaction_status": "ready",
    }


if __name__ == "__main__":
    unittest.main()
