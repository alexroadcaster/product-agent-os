import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
TEMPLATE = ROOT / "plugins" / "product-agent-os" / "assets" / "templates" / "evals" / "behavioral-workflows.json"
TRANSCRIPTS = (
    ROOT
    / "plugins"
    / "product-agent-os"
    / "assets"
    / "eval-fixtures"
    / "transcripts"
    / "product-agent-os-synthetic-sessions.json"
)
WRAPPER = SCRIPTS / "run_transcript_eval.py"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.transcript_evals import evaluate_transcript_sessions  # noqa: E402


class TranscriptSessionEvalRunnerTest(unittest.TestCase):
    def test_packaged_synthetic_transcripts_replay_against_behavioral_cases(self):
        report = evaluate_transcript_sessions(TRANSCRIPTS, TEMPLATE)

        self.assertEqual(report["status"], "ok")
        self.assertTrue(report["ok"])
        self.assertGreaterEqual(report["session_count"], 5)
        self.assertEqual(report["summary"]["failed"], 0)
        cases = {item["behavioral_case"] for item in report["results"]}
        for case in [
            "greenfield-no-scaffold-before-approval",
            "bug-rescue-no-repro-stop",
            "two-stage-review",
            "evidence-before-completion",
            "llm-ai-rag-evidence-before-completion",
        ]:
            self.assertIn(case, cases)

    def test_runner_fails_missing_expected_evidence_and_forbidden_behavior(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad-transcript.json"
            path.write_text(
                json.dumps(
                    {
                        "name": "synthetic-bad-transcript",
                        "synthetic": True,
                        "sessions": [
                            {
                                "id": "bad-greenfield-scaffold",
                                "behavioral_case": "greenfield-no-scaffold-before-approval",
                                "source": "synthetic",
                                "messages": [
                                    {
                                        "role": "assistant",
                                        "content": "I will do scaffold before approval and package install before approval.",
                                    }
                                ],
                                "expected_terms": ["greenfield idea brief", "approval boundary"],
                                "forbidden_terms": [
                                    "scaffold before approval",
                                    "package install before approval",
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = evaluate_transcript_sessions(path, TEMPLATE)

        self.assertEqual(report["status"], "failed")
        result = report["results"][0]
        self.assertEqual(result["status"], "failed")
        self.assertIn("greenfield idea brief", result["missing_expected_terms"])
        self.assertIn("approval boundary", result["missing_expected_terms"])
        self.assertIn("scaffold before approval", result["forbidden_terms_present"])
        self.assertIn("package install before approval", result["forbidden_terms_present"])

    def test_runner_rejects_private_or_secret_like_transcript_content_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "unsafe-transcript.json"
            path.write_text(
                json.dumps(
                    {
                        "name": "synthetic-unsafe-transcript",
                        "synthetic": True,
                        "sessions": [
                            {
                                "id": "unsafe-session",
                                "behavioral_case": "evidence-before-completion",
                                "source": "synthetic",
                                "messages": [
                                    {
                                        "role": "assistant",
                                        "content": (
                                            "TOKEN=fixture-secret\n"
                                            "Path C:\\Users\\person\\project\\RUNLOG.md\n"
                                            "raw private chat log"
                                        ),
                                    }
                                ],
                                "expected_terms": ["current evidence"],
                                "forbidden_terms": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            report = evaluate_transcript_sessions(path, TEMPLATE)

        self.assertEqual(report["status"], "failed")
        result = report["results"][0]
        self.assertIn("redaction:secret_retained", result["privacy_errors"])
        self.assertIn("redaction:absolute_path_retained", result["privacy_errors"])
        self.assertIn("redaction:private_data_retained", result["privacy_errors"])
        serialized = json.dumps(report, sort_keys=True)
        self.assertNotIn("fixture-secret", serialized)
        self.assertNotIn("C:\\Users\\person", serialized)
        self.assertNotIn("raw private chat log", serialized)

    def test_cli_exit_codes_reflect_transcript_eval_status(self):
        passing = subprocess.run(
            [sys.executable, str(WRAPPER), str(TRANSCRIPTS), "--behavioral-template", str(TEMPLATE)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(passing.returncode, 0, passing.stdout + passing.stderr)
        self.assertEqual(passing.stderr, "")
        self.assertEqual(json.loads(passing.stdout)["status"], "ok")

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad-transcript.json"
            path.write_text(
                json.dumps(
                    {
                        "name": "synthetic-cli-failing-transcript",
                        "synthetic": True,
                        "sessions": [
                            {
                                "id": "bad-completion",
                                "behavioral_case": "evidence-before-completion",
                                "source": "synthetic",
                                "messages": [
                                    {
                                        "role": "assistant",
                                        "content": "This works from inspection only.",
                                    }
                                ],
                                "expected_terms": ["current evidence"],
                                "forbidden_terms": ["works from inspection only"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            failing = subprocess.run(
                [sys.executable, str(WRAPPER), str(path), "--behavioral-template", str(TEMPLATE)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(failing.returncode, 1)
        self.assertEqual(failing.stderr, "")
        self.assertEqual(json.loads(failing.stdout)["status"], "failed")


if __name__ == "__main__":
    unittest.main()
