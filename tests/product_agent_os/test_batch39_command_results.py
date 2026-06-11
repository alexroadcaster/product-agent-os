from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))


from product_agent_os.batch39_command_results import (  # noqa: E402
    COMMAND_RESULT_EVIDENCE_CLASSES,
    build_command_result_entry,
    parse_command_results_jsonl,
    validate_command_result_entry,
    validate_command_results_jsonl,
)


class Batch39CommandResultsTests(unittest.TestCase):
    def test_builds_current_command_result_entry_without_raw_output_or_path_leaks(self) -> None:
        entry = build_command_result_entry(
            test_id="B39-TEST-M03",
            attempt_id="B39-TEST-M03-A01",
            manifest_ref="docs/superpowers/specs/pilot-run-manifest.example.json",
            command_id="cmd-001",
            command="python -m unittest tests.product_agent_os.test_batch39_command_results -v",
            exit_code=0,
            started_at="2026-06-11T00:00:00+00:00",
            finished_at="2026-06-11T00:00:02+00:00",
            stdout="OK\nRan 4 tests",
            stderr="",
            evidence_class="current_command",
            evidence_source="local_command_run",
        )

        self.assertEqual(entry["schema_version"], "command_result_v1")
        self.assertEqual(entry["test_id"], "B39-TEST-M03")
        self.assertEqual(entry["attempt_id"], "B39-TEST-M03-A01")
        self.assertEqual(entry["status"], "passed")
        self.assertEqual(entry["evidence"]["class"], "current_command")
        self.assertEqual(entry["evidence"]["trust_level"], "current_run")
        self.assertEqual(entry["approval_boundary"]["provider_or_api_calls"], "not_performed")
        self.assertFalse(entry["redaction"]["raw_stdout_stored"])
        self.assertTrue(entry["output"]["stdout_digest"].startswith("sha256:"))
        self.assertNotIn("stdout", entry)
        self.assertEqual(validate_command_result_entry(entry), [])

        encoded = json.dumps(entry, ensure_ascii=False)
        self.assertNotIn("C:\\", encoded)
        self.assertNotIn("Users/user", encoded)

    def test_evidence_classes_include_fake_generated_stale_and_user_claimed(self) -> None:
        for evidence_class in [
            "current_command",
            "user_claimed",
            "fake_evidence",
            "generated_view",
            "stale_evidence",
        ]:
            self.assertIn(evidence_class, COMMAND_RESULT_EVIDENCE_CLASSES)

    def test_validation_rejects_fake_evidence_as_command_proof(self) -> None:
        entry = build_command_result_entry(
            test_id="B39-TEST-M03",
            attempt_id="B39-TEST-M03-A01",
            manifest_ref="docs/superpowers/specs/pilot-run-manifest.example.json",
            command_id="cmd-002",
            command="claimed: tests passed",
            exit_code=None,
            started_at="2026-06-11T00:00:00+00:00",
            finished_at="2026-06-11T00:00:00+00:00",
            evidence_class="fake_evidence",
            evidence_source="unverified_user_claim",
        )

        errors = validate_command_result_entry(entry)

        self.assertIn("fake_evidence cannot satisfy command proof", errors)
        self.assertEqual(entry["evidence"]["trust_level"], "rejected")
        self.assertEqual(entry["status"], "rejected")

    def test_jsonl_parser_and_validator_accept_multiple_entries(self) -> None:
        passed = build_command_result_entry(
            test_id="B39-TEST-M03",
            attempt_id="B39-TEST-M03-A01",
            manifest_ref="docs/superpowers/specs/pilot-run-manifest.example.json",
            command_id="cmd-001",
            command="python -m unittest tests.product_agent_os.test_batch39_command_results -v",
            exit_code=0,
            started_at="2026-06-11T00:00:00+00:00",
            finished_at="2026-06-11T00:00:02+00:00",
            evidence_class="current_command",
            evidence_source="local_command_run",
        )
        stale = build_command_result_entry(
            test_id="B39-TEST-M03",
            attempt_id="B39-TEST-M03-A01",
            manifest_ref="docs/superpowers/specs/pilot-run-manifest.example.json",
            command_id="cmd-003",
            command="historical docs check",
            exit_code=0,
            started_at="2026-06-10T00:00:00+00:00",
            finished_at="2026-06-10T00:00:02+00:00",
            evidence_class="stale_evidence",
            evidence_source="prior_run_log",
        )
        text = "\n".join(json.dumps(item, sort_keys=True) for item in [passed, stale]) + "\n"

        parsed = parse_command_results_jsonl(text)

        self.assertEqual([item["command_id"] for item in parsed], ["cmd-001", "cmd-003"])
        self.assertEqual(validate_command_results_jsonl(text), [])

    def test_cli_writes_jsonl_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "command-results.example.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "collect_command_result.py"),
                    "--output",
                    str(output),
                    "--test-id",
                    "B39-TEST-M03",
                    "--attempt-id",
                    "B39-TEST-M03-A01",
                    "--manifest-ref",
                    "docs/superpowers/specs/pilot-run-manifest.example.json",
                    "--command-id",
                    "cmd-001",
                    "--command",
                    "python -m unittest tests.product_agent_os.test_batch39_command_results -v",
                    "--exit-code",
                    "0",
                    "--started-at",
                    "2026-06-11T00:00:00+00:00",
                    "--finished-at",
                    "2026-06-11T00:00:02+00:00",
                    "--stdout",
                    "OK",
                    "--evidence-class",
                    "current_command",
                    "--evidence-source",
                    "local_command_run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            text = output.read_text(encoding="utf-8")
            self.assertEqual(validate_command_results_jsonl(text), [])
            self.assertIn('"status": "ok"', result.stdout)


if __name__ == "__main__":
    unittest.main()
