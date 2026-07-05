import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
DOCS = ROOT / "docs"
sys.path.insert(0, str(SCRIPTS))

from codex_runtime_runner.model_output import (  # noqa: E402
    classify_live_run,
    classify_pair,
    extract_strict_json,
    validate_live_run_payload,
    validate_paired_live_eval_result,
)


T12_RESULTS = DOCS / "superpowers" / "specs" / "batch45-postq4-t12-paired-live-model-rerun-results.json"


class CodexRuntimeRunnerModelOutputTest(unittest.TestCase):
    def test_strict_final_json_parser_rejects_invalid_nested_json_string(self):
        output = 'progress\nFINAL_JSON: {"summary": "bad nested {"not": "escaped"}"}'

        result = extract_strict_json(output)

        self.assertFalse(result.ok)
        self.assertEqual("final_json:invalid_json", result.error)

    def test_strict_final_json_parser_rejects_trailing_or_multiple_objects(self):
        trailing = extract_strict_json('FINAL_JSON: {"ok": true}\n{"second": true}')
        multiple_markers = extract_strict_json('FINAL_JSON: {"ok": true}\nFINAL_JSON: {"second": true}')

        self.assertEqual("final_json:trailing_content", trailing.error)
        self.assertEqual("final_json:multiple_markers", multiple_markers.error)

    def test_no_op_detection_ignores_temp_probe_pycache_and_empty_diff(self):
        payload = self._valid_run(
            status="completed",
            changed_file_count=3,
            sanitized_changed_files=[
                {"path": "tmp_root_write_check.txt", "change_type": "A"},
                {"path": "pkg/__pycache__/module.cpython-312.pyc", "change_type": "A"},
                {"path": "copy_log.txt", "change_type": "A"},
            ],
        )

        classification = classify_live_run(payload)

        self.assertEqual("no_op", classification.status)
        self.assertEqual(0, classification.changed_file_count)
        self.assertEqual([], classification.sanitized_changed_files)

    def test_completed_run_requires_strict_schema_and_allowed_status(self):
        payload = self._valid_run()
        self.assertEqual([], validate_live_run_payload(payload))

        missing = copy.deepcopy(payload)
        del missing["raw_output_hashes"]
        unknown = copy.deepcopy(payload)
        unknown["status"] = "model_said_ok"

        self.assertIn("run.raw_output_hashes:missing", validate_live_run_payload(missing))
        self.assertIn("run.status:unknown", validate_live_run_payload(unknown))

    def test_pair_rollup_quarantines_invalid_json_and_no_op(self):
        result = json.loads(T12_RESULTS.read_text(encoding="utf-8"))

        errors = validate_paired_live_eval_result(result)
        invalid_pairs = {pair["task_id"]: pair["invalid_reason"] for pair in result["pairs"] if not pair["pair_valid_for_scoring"]}

        self.assertEqual([], errors)
        self.assertEqual(6, result["aggregate_result"]["valid_pair_count"])
        self.assertEqual(2, result["aggregate_result"]["invalid_pair_count"])
        self.assertEqual("treatment_invalid_json", invalid_pairs["B45-HELDOUT-01"])
        self.assertEqual("treatment_no_op", invalid_pairs["B45-HELDOUT-07"])
        self.assertFalse(result["aggregate_result"]["promotion_threshold_met"])

    def test_reviewer_is_blocked_until_all_pairs_schema_valid(self):
        result = json.loads(T12_RESULTS.read_text(encoding="utf-8"))
        result["execution_summary"]["reviewer_calls_started"] = 1
        result["execution_summary"]["reviewer_status"] = "reviewed"
        result["aggregate_result"]["promotion_threshold_met"] = True

        errors = validate_paired_live_eval_result(result)

        self.assertIn("execution_summary.reviewer_calls_started:must_be_zero_when_invalid_pairs", errors)
        self.assertIn("execution_summary.reviewer_status:expected_not_run_due_invalid_pair_count", errors)
        self.assertIn("aggregate_result.promotion_threshold_met:must_be_false_when_invalid_pairs", errors)

    def test_rollup_retention_stores_hashes_not_raw_outputs(self):
        result = json.loads(T12_RESULTS.read_text(encoding="utf-8"))
        result["raw_stdout"] = "raw output body"
        result["cost_and_retention"]["temp_root_pattern"] = "C:\\Users\\user\\AppData\\Local\\Temp\\codex-b45-postq4-t12-123"

        errors = validate_paired_live_eval_result(result)

        self.assertIn("packet.raw_stdout:raw_output_field_forbidden", errors)
        self.assertIn("redaction:absolute_path_retained", errors)
        self.assertIn("cost_and_retention.temp_root_pattern:concrete_path_forbidden", errors)

    def test_pair_classification_uses_arm_specific_invalid_reason(self):
        baseline = self._valid_run(status="completed")
        treatment = self._valid_run(status="invalid_json", arm="treatment", final_json_parse_ok=False)

        pair = classify_pair(baseline, treatment)

        self.assertFalse(pair["pair_valid_for_scoring"])
        self.assertEqual("treatment_invalid_json", pair["invalid_reason"])

    def _valid_run(
        self,
        *,
        status: str = "completed",
        arm: str = "baseline",
        final_json_parse_ok: bool = True,
        changed_file_count: int = 1,
        sanitized_changed_files: list[dict[str, str]] | None = None,
    ) -> dict[str, object]:
        return {
            "task_id": "B45-HELDOUT-X",
            "arm": arm,
            "pair_id": "B45-HELDOUT-X",
            "attempt_id": f"B45-HELDOUT-X-{arm}",
            "status": status,
            "timed_out": status == "timeout",
            "final_json_parse_ok": final_json_parse_ok,
            "changed_file_count": changed_file_count,
            "sanitized_changed_files": sanitized_changed_files
            if sanitized_changed_files is not None
            else [{"path": "tests/product_agent_os/test_example.py", "change_type": "M"}],
            "behavior_score": 1.0 if status == "completed" else None,
            "raw_output_hashes": {
                "prompt_sha256": "A" * 64,
                "stdout_sha256": "B" * 64,
                "stderr_sha256": "C" * 64,
                "stdout_length_bytes": 120,
                "stderr_length_bytes": 0,
            },
            "retention_status": "raw_temp_only_repo_sanitized_rollup",
        }


if __name__ == "__main__":
    unittest.main()
