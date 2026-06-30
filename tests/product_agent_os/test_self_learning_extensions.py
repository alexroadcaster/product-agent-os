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


class SelfLearningExtensionTests(unittest.TestCase):
    def test_state_initializer_stages_state_without_workspace_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as stagedir:
            workspace = Path(tmpdir) / "workspace"
            stage = Path(stagedir) / "stage"
            self._write_files(workspace, {".codex/product-agent-os/lifecycle-state.json": "{}\n"})

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "init_self_learning_state.py"),
                    str(workspace),
                    "--stage",
                    str(stage),
                    "--now",
                    "2026-06-30T00:00:00Z",
                    "--installed-at",
                    "2026-06-01T00:00:00Z",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            workspace_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            stage_files = sorted(path.relative_to(stage).as_posix() for path in stage.rglob("*") if path.is_file())
            state = json.loads((stage / ".codex/product-agent-os/self-learning-state.json").read_text(encoding="utf-8"))
            manifest = json.loads((stage / "product-agent-os-stage-manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "self_learning_state_initializer_packet_v1")
        self.assertEqual(payload["status"], "ready_for_owner_review")
        self.assertFalse(payload["state_written"])
        self.assertEqual(payload["target_workspace_writes"], "not_performed")
        self.assertEqual(payload["auto_apply"], "disabled")
        self.assertEqual(state["schema_version"], "self_learning_state_v1")
        self.assertEqual(state["installed_at"], "2026-06-01T00:00:00Z")
        self.assertIn(".codex/product-agent-os/self-learning-state.json", stage_files)
        self.assertIn(".codex/product-agent-os/self-learning/state-initializer-packet.json", stage_files)
        self.assertEqual(workspace_files, [".codex/product-agent-os/lifecycle-state.json"])
        self.assertEqual(manifest["schema_version"], "self_learning_state_initializer_manifest_v1")
        self.assertFalse(manifest["raw_workspace_path_included"])
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_uses_staged_state_and_redacted_ledgers(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as stagedir:
            root = Path(tmpdir)
            workspace = root / "workspace"
            state_stage = root / "state-stage"
            run_stage = Path(stagedir) / "run-stage"
            feedback_ledger = root / "feedback.jsonl"
            metrics_ledger = root / "metrics.jsonl"
            self._write_files(workspace, {".codex/product-agent-os/lifecycle-state.json": "{}\n"})
            feedback_ledger.write_text(json.dumps(self._feedback_row(), sort_keys=True) + "\n", encoding="utf-8")
            metrics_ledger.write_text(json.dumps(self._metrics_row(), sort_keys=True) + "\n", encoding="utf-8")

            init_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "init_self_learning_state.py"),
                    str(workspace),
                    "--stage",
                    str(state_stage),
                    "--now",
                    "2026-06-30T00:00:00Z",
                    "--installed-at",
                    "2026-06-01T00:00:00Z",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(init_result.returncode, 0, init_result.stderr + init_result.stdout)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-30T00:00:00Z",
                    "--state-file",
                    str(state_stage / ".codex/product-agent-os/self-learning-state.json"),
                    "--metrics-ledger",
                    str(metrics_ledger),
                    "--feedback-ledger",
                    str(feedback_ledger),
                    "--stage",
                    str(run_stage),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            workspace_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            stage_files = sorted(path.relative_to(run_stage).as_posix() for path in run_stage.rglob("*") if path.is_file())

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ready_for_owner_review")
        self.assertEqual(payload["due_check"]["state_source"], "explicit_state_file")
        self.assertFalse(payload["state_written"])
        self.assertEqual(payload["provider_calls"], "not_performed")
        self.assertEqual(payload["feedback_summary"]["status"], "available")
        self.assertEqual(payload["feedback_summary"]["ledger_source"], "explicit_redacted_override")
        self.assertEqual(payload["metrics_summary"]["status"], "available")
        self.assertEqual(payload["metrics_summary"]["ledger_path"], "explicit_redacted_override")
        self.assertGreaterEqual(payload["candidate_summary"]["candidate_count"], 2)
        self.assertEqual(workspace_files, [".codex/product-agent-os/lifecycle-state.json"])
        self.assertIn(".codex/product-agent-os/self-learning/self-learning-progress.html", stage_files)
        self.assertNotIn(str(workspace), result.stdout)
        self.assertNotIn(str(metrics_ledger), result.stdout)
        self.assertNotIn(str(feedback_ledger), result.stdout)

    def test_eval_taxonomy_promptfoo_and_halo_packets_are_review_only(self) -> None:
        from product_agent_os.self_learning_evals import (
            build_halo_recommendation_packet,
            build_promptfoo_export_packet,
            build_self_learning_eval_cases,
            build_self_learning_failure_taxonomy,
            validate_self_learning_eval_cases,
            validate_self_learning_failure_taxonomy,
        )

        taxonomy = build_self_learning_failure_taxonomy()
        cases = build_self_learning_eval_cases()
        promptfoo = build_promptfoo_export_packet(eval_cases=cases, generated_at="2026-06-30T00:00:00Z")
        halo = build_halo_recommendation_packet(
            eval_cases=cases,
            taxonomy=taxonomy,
            generated_at="2026-06-30T00:00:00Z",
        )

        self.assertEqual(validate_self_learning_failure_taxonomy(taxonomy), [])
        self.assertEqual(validate_self_learning_eval_cases(cases), [])
        self.assertEqual(promptfoo["schema_version"], "self_learning_promptfoo_export_v1")
        self.assertEqual(promptfoo["provider_calls"], "not_performed")
        self.assertTrue(promptfoo["approval_required_before_promptfoo_run"])
        self.assertEqual(promptfoo["auto_apply"], "disabled")
        self.assertGreaterEqual(promptfoo["case_count"], 8)
        self.assertIn("tests:", promptfoo["promptfoo_config_yaml"])
        self.assertEqual(halo["schema_version"], "self_learning_halo_recommendation_packet_v1")
        self.assertEqual(halo["halo_engine_calls"], "not_performed")
        self.assertEqual(halo["auto_apply"], "disabled")
        self.assertGreaterEqual(halo["recommendation_count"], 1)

    def test_repair_worker_contract_blocks_auto_apply_and_out_of_allowlist_changes(self) -> None:
        from product_agent_os.self_learning_repair import (
            build_staged_repair_result_packet,
            build_staged_repair_task_contract,
            validate_staged_repair_result_packet,
            validate_staged_repair_task_contract,
        )

        contract = build_staged_repair_task_contract(
            candidate_id="sll-candidate-docs",
            objective="Update Self-Learning docs and eval fixture references.",
            allowed_files=["docs/product-agent-os/self-learning-loop.md", "EVALS.md"],
            forbidden_files=[".codex/config.toml"],
            validation_commands=["python tools\\check_docs.py"],
            change_surface="docs",
            expected_behavior=["docs explain stage-only boundaries"],
            generated_at="2026-06-30T00:00:00Z",
        )
        result = build_staged_repair_result_packet(
            task_contract=contract,
            changed_files=["docs/product-agent-os/self-learning-loop.md"],
            validation_results=[{"command": "python tools\\check_docs.py", "status": "not_run"}],
            summary="Staged docs update only.",
            generated_at="2026-06-30T00:00:00Z",
        )
        bad_result = build_staged_repair_result_packet(
            task_contract=contract,
            changed_files=["README.md"],
            validation_results=[{"command": "python tools\\check_docs.py", "status": "not_run"}],
            summary="Outside allowlist.",
            generated_at="2026-06-30T00:00:00Z",
        )

        self.assertEqual(validate_staged_repair_task_contract(contract), [])
        self.assertEqual(contract["auto_apply"], "disabled")
        self.assertEqual(contract["target_workspace_writes"], "not_performed")
        self.assertEqual(validate_staged_repair_result_packet(result), [])
        self.assertIn("README.md:outside_allowed_files", validate_staged_repair_result_packet(bad_result))

    def _write_files(self, workspace: Path, files: dict[str, str]) -> None:
        for relative, text in files.items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def _feedback_row(self) -> dict:
        return {
            "schema_version": "owner_feedback_ledger_v1",
            "feedback_id": "fb-b44-s7-redacted",
            "session_ref": {"session_id_hash": "sha256:b44s7", "raw_session_id_included": False},
            "task_ref": {"task_id": "B44-S7", "slice_id": "manual-pilot"},
            "explicit_rating": "dissatisfied",
            "revision_requested": True,
            "revision_accepted": False,
            "usefulness": "low",
            "user_effort": "high",
            "outcome": "reopened",
            "evidence_links": ["docs/superpowers/specs/batch44-self-learning-loop-current-gap-audit.json"],
            "redaction_status": "redacted",
            "owner_review": "owner_labeled",
            "privacy": {
                "consent": "owner_provided_redacted_summary",
                "raw_chat_body_stored": False,
                "contains_pii": False,
            },
            "preference_signals": [
                {
                    "category": "self_learning_loop",
                    "summary": "Initialize state through staged proposal before running the loop.",
                    "scope": "product_agent_os",
                }
            ],
        }

    def _metrics_row(self) -> dict:
        return {
            "schema_version": "self_learning_metrics_ledger_v1",
            "run_id": "sll-20260630T000000Z-b44s7",
            "evidence_window": {"started_at": "2026-06-30T00:00:00Z", "ended_at": "2026-06-30T00:10:00Z"},
            "baseline_version": "self-learning-loop@B44-S6",
            "current_version": "self-learning-loop@B44-S7",
            "candidate_version": "self-learning-loop@B44-S7-candidate",
            "metrics": {
                "state_initializer_recovery": {
                    "value": 1,
                    "denominator": 1,
                    "source": "manual_pilot",
                    "confidence": "low_single_run",
                }
            },
            "confidence_intervals": {},
            "cost_latency": {"median_latency_ms": 0},
            "user_effort": {"owner_minutes": 5},
            "regression_flags": ["state_file_missing_recovery_gap"],
            "accepted_gaps": ["single_manual_pilot_only"],
            "report_paths": ["docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json"],
            "rollback_targets": ["self-learning-loop@B44-S6"],
            "source_status": "source_backed",
            "privacy_status": "redacted_summary_only",
            "append_only": True,
        }


if __name__ == "__main__":
    unittest.main()
