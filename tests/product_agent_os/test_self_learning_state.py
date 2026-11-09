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


class SelfLearningStateTests(unittest.TestCase):
    def test_owner_feedback_ledger_accepts_redacted_owner_review_rows(self) -> None:
        from product_agent_os.self_learning_feedback import validate_owner_feedback_row

        row = {
            "schema_version": "owner_feedback_ledger_v1",
            "feedback_id": "fb-001",
            "session_ref": {
                "session_id_hash": "sha256:abc123",
                "raw_session_id_included": False,
            },
            "task_ref": {
                "task_id": "B44-SLL-M07",
                "slice_id": "B44-S3-Feedback-And-Preferences",
            },
            "explicit_rating": "dissatisfied",
            "revision_requested": True,
            "revision_accepted": False,
            "usefulness": "low",
            "user_effort": "high",
            "outcome": "reopened",
            "evidence_links": [
                "docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md"
            ],
            "redaction_status": "redacted",
            "owner_review": "owner_labeled",
            "privacy": {
                "consent": "owner_provided_redacted_summary",
                "raw_chat_body_stored": False,
                "contains_pii": False,
            },
            "preference_signals": [
                {
                    "category": "verification_expectations",
                    "summary": "Do not claim completion without current command evidence.",
                    "scope": "product_agent_os",
                }
            ],
        }

        self.assertEqual(validate_owner_feedback_row(row), [])

    def test_owner_feedback_ledger_rejects_raw_chat_pii_and_absolute_paths(self) -> None:
        from product_agent_os.self_learning_feedback import validate_owner_feedback_row

        row = {
            "schema_version": "owner_feedback_ledger_v1",
            "feedback_id": "fb-raw",
            "session_ref": "C:\\Users\\user\\secret\\raw-session.json",
            "task_ref": {"task_id": "B44-SLL-M07"},
            "explicit_rating": "dissatisfied",
            "revision_requested": True,
            "revision_accepted": False,
            "usefulness": "low",
            "user_effort": "high",
            "outcome": "reopened",
            "evidence_links": ["C:\\Users\\user\\Desktop\\project\\private.txt"],
            "redaction_status": "unredacted",
            "owner_review": "owner_labeled",
            "privacy": {
                "consent": "missing",
                "raw_chat_body_stored": True,
                "contains_pii": True,
            },
            "raw_chat": "email alex@example.com and raw transcript body",
        }

        errors = validate_owner_feedback_row(row)

        self.assertIn("redaction_status:must_be_redacted", errors)
        self.assertIn("privacy.raw_chat_body_stored:must_be_false", errors)
        self.assertIn("privacy.consent:missing_owner_redacted_summary_consent", errors)
        self.assertIn("raw_private_content:blocked", errors)

    def test_feedback_import_contract_filters_scope_consent_redaction_and_raw_transcripts(self) -> None:
        from product_agent_os.self_learning_feedback import build_feedback_import_contract

        scope_packet = {
            "eligible": True,
            "status": "eligible",
            "workspace_ref": {"path_hash": "sha256:scope-ok", "raw_path_included": False},
        }
        summaries = [
            {
                "summary_id": "s-ok",
                "project_scope_id": "sha256:scope-ok",
                "workspace_path_hash": "sha256:scope-ok",
                "product_agent_os_detected": True,
                "evidence_consent": "owner_provided_redacted_summary",
                "redaction_status": "redacted",
                "contains_raw_transcript": False,
                "feedback_row": {"feedback_id": "fb-ok"},
            },
            {
                "summary_id": "s-other",
                "project_scope_id": "sha256:other",
                "workspace_path_hash": "sha256:other",
                "product_agent_os_detected": True,
                "evidence_consent": "owner_provided_redacted_summary",
                "redaction_status": "redacted",
                "contains_raw_transcript": False,
            },
            {
                "summary_id": "s-raw",
                "project_scope_id": "sha256:scope-ok",
                "workspace_path_hash": "sha256:scope-ok",
                "product_agent_os_detected": True,
                "evidence_consent": "owner_provided_redacted_summary",
                "redaction_status": "redacted",
                "contains_raw_transcript": True,
            },
            {
                "summary_id": "s-no-consent",
                "project_scope_id": "sha256:scope-ok",
                "workspace_path_hash": "sha256:scope-ok",
                "product_agent_os_detected": True,
                "evidence_consent": "missing",
                "redaction_status": "redacted",
                "contains_raw_transcript": False,
            },
        ]

        contract = build_feedback_import_contract(scope_packet=scope_packet, summaries=summaries)

        self.assertEqual(contract["schema_version"], "codex_session_feedback_import_v1")
        self.assertEqual(contract["raw_session_ingestion"], "not_performed")
        self.assertEqual(contract["imported_summary_ids"], ["s-ok"])
        skipped = {item["summary_id"]: item["reason"] for item in contract["skipped_summaries"]}
        self.assertEqual(skipped["s-other"], "out_of_scope")
        self.assertEqual(skipped["s-raw"], "raw_transcript_blocked")
        self.assertEqual(skipped["s-no-consent"], "missing_consent")

    def test_satisfaction_without_owner_labels_is_insufficient(self) -> None:
        from product_agent_os.self_learning_feedback import evaluate_satisfaction
        for rows in ([], [{"feedback_id": "synthetic", "explicit_rating": None, "revision_requested": True, "revision_accepted": False}]):
            result = evaluate_satisfaction(rows)
            self.assertEqual(result['promotion_signal'], 'insufficient_evidence')
            self.assertEqual(result['human_label_count'], 0)
            self.assertEqual(result['owner_sentiment'], 'unknown')

    def test_satisfaction_separates_label_support_and_sentiment(self) -> None:
        from product_agent_os.self_learning_feedback import evaluate_satisfaction
        for ratings, sentiment in [(['satisfied'], 'positive'), (['dissatisfied'], 'negative'), (['neutral'], 'neutral'), (['satisfied', 'dissatisfied'], 'mixed')]:
            result = evaluate_satisfaction([{'feedback_id': str(i), 'explicit_rating': r} for i,r in enumerate(ratings)])
            self.assertEqual(result['owner_sentiment'], sentiment)
            self.assertEqual(result['human_label_count'], len(ratings))
            self.assertEqual(result['denominator'], len(ratings))
            self.assertEqual(result['promotion_signal'], 'owner_label_supported')

    def test_satisfaction_evaluator_prefers_owner_labels_and_keeps_pseudo_labels_low_confidence(self) -> None:
        from product_agent_os.self_learning_feedback import evaluate_satisfaction

        rows = [
            {
                "feedback_id": "fb-owner",
                "explicit_rating": "satisfied",
                "revision_requested": True,
                "revision_accepted": True,
                "usefulness": "high",
                "user_effort": "low",
                "outcome": "accepted",
                "owner_review": "owner_labeled",
            },
            {
                "feedback_id": "fb-pseudo",
                "explicit_rating": None,
                "revision_requested": True,
                "revision_accepted": False,
                "usefulness": "low",
                "user_effort": "high",
                "outcome": "reopened",
                "owner_review": "inferred_from_redacted_summary",
            },
        ]

        report = evaluate_satisfaction(rows)

        self.assertEqual(report["schema_version"], "self_learning_satisfaction_report_v1")
        self.assertEqual(report["denominator"], 2)
        self.assertEqual(report["human_label_count"], 1)
        by_id = {item["feedback_id"]: item for item in report["labels"]}
        self.assertEqual(by_id["fb-owner"]["label"], "satisfied")
        self.assertEqual(by_id["fb-owner"]["source_type"], "owner_label")
        self.assertEqual(by_id["fb-pseudo"]["label"], "dissatisfied")
        self.assertEqual(by_id["fb-pseudo"]["source_type"], "pseudo_label")
        self.assertEqual(by_id["fb-pseudo"]["confidence"], "low")
        self.assertEqual(report["promotion_signal"], "blocked_low_confidence")

    def test_preference_memory_is_compact_traceable_and_owner_editable(self) -> None:
        from product_agent_os.self_learning_feedback import build_preference_memory, validate_preference_memory

        rows = [
            {
                "feedback_id": "fb-verify",
                "preference_signals": [
                    {
                        "category": "verification_expectations",
                        "summary": "Report command evidence and unsupported claims separately.",
                        "scope": "product_agent_os",
                    }
                ],
            },
            {
                "feedback_id": "fb-language",
                "preference_signals": [
                    {
                        "category": "response_language",
                        "summary": "Use Russian prose and keep canonical Codex terms in English.",
                        "scope": "global_style",
                    }
                ],
            },
        ]

        memory = build_preference_memory(rows, generated_at="2026-06-24T00:00:00Z")

        self.assertEqual(memory["schema_version"], "preference_memory_v1")
        self.assertTrue(memory["owner_editable"])
        self.assertFalse(memory["raw_chat_stored"])
        self.assertEqual(validate_preference_memory(memory), [])
        categories = {item["category"]: item for item in memory["preferences"]["recent"]}
        self.assertEqual(categories["verification_expectations"]["source_feedback_ids"], ["fb-verify"])
        self.assertEqual(categories["response_language"]["source_feedback_ids"], ["fb-language"])
        self.assertNotIn("raw transcript body", json.dumps(memory, ensure_ascii=False))

    def test_candidate_packet_stages_review_only_modernization_from_metrics_and_feedback(self) -> None:
        from product_agent_os.self_learning_candidates import (
            build_self_learning_candidate_packet,
            validate_candidate_packet,
        )

        packet = build_self_learning_candidate_packet(
            metrics_summary={
                "status": "available",
                "latest_run_id": "sll-20260624T100000Z-demo",
                "latest_report_paths": ["docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json"],
                "regression_flags": ["skill_trigger_recall_regression"],
                "metric_delta_count": 2,
            },
            feedback_summary={
                "status": "available",
                "owner_feedback_rows": 1,
                "satisfaction_report": {
                    "denominator": 1,
                    "dissatisfied_count": 1,
                    "promotion_signal": "blocked_low_confidence",
                },
            },
            generated_at="2026-06-24T10:00:00Z",
        )

        self.assertEqual(packet["schema_version"], "self_learning_candidate_packet_v1")
        self.assertEqual(packet["candidate_policy"], "candidate_only")
        self.assertEqual(packet["apply_policy"], "cannot_apply")
        self.assertEqual(packet["auto_apply"], "disabled")
        self.assertEqual(packet["provider_calls"], "not_performed")
        self.assertEqual(packet["target_workspace_writes"], "not_performed")
        self.assertGreaterEqual(packet["candidate_count"], 2)
        self.assertEqual(packet["safety_report"]["promotion_status"], "review_ready")
        for candidate in packet["candidates"]:
            with self.subTest(candidate=candidate["candidate_id"]):
                self.assertEqual(candidate["status"], "staged_for_review")
                self.assertEqual(candidate["external_write_action"], "none")
                self.assertEqual(candidate["approval_state"], "not_requested")
                self.assertEqual(candidate["auto_apply"], "disabled")
                self.assertTrue(candidate["rollback_target"])
                self.assertTrue(candidate["tests_required"])
                self.assertTrue(candidate["evidence_refs"])
        self.assertEqual(validate_candidate_packet(packet), [])

    def test_professional_code_candidate_packet_stages_review_only_improvements(self) -> None:
        from product_agent_os.self_learning_candidates import (
            build_self_learning_candidate_packet,
            validate_candidate_packet,
        )

        packet = build_self_learning_candidate_packet(
            metrics_summary={
                "status": "available",
                "latest_run_id": "sll-20260629T100000Z-professional-code",
                "latest_report_paths": ["docs/superpowers/specs/batch45-professional-code-s3-evals-visibility-summary.json"],
                "regression_flags": ["professional_code_authoring_custom_code_bloat"],
                "metric_delta_count": 1,
                "professional_code_authoring_findings": [
                    {
                        "finding_type": "missing_existing_capability_scan",
                        "target_id": "workflow:coding-standards",
                        "reason": "Agents skipped the reuse-first scan before proposing custom code.",
                        "evidence_refs": ["eval:professional-code-authoring-missing-existing-capability-scan"],
                        "feedback_refs": ["owner_feedback:professional-code"],
                    }
                ],
            },
            feedback_summary={"status": "available"},
            generated_at="2026-06-29T10:00:00Z",
        )

        candidates = [
            candidate
            for candidate in packet["candidates"]
            if candidate.get("candidate_kind") == "professional_code_authoring_improvement"
        ]

        self.assertGreaterEqual(len(candidates), 1)
        self.assertEqual(packet["candidate_policy"], "candidate_only")
        self.assertEqual(packet["apply_policy"], "cannot_apply")
        self.assertEqual(packet["auto_apply"], "disabled")
        self.assertEqual(packet["provider_calls"], "not_performed")
        self.assertEqual(packet["target_workspace_writes"], "not_performed")
        self.assertEqual(packet["external_write_action"], "none")
        self.assertEqual(packet["safety_report"]["promotion_status"], "review_ready")
        for candidate in candidates:
            with self.subTest(candidate=candidate["candidate_id"]):
                self.assertEqual(candidate["component"], "professional_code_authoring")
                self.assertEqual(candidate["status"], "staged_for_review")
                self.assertEqual(candidate["approval_state"], "not_requested")
                self.assertEqual(candidate["auto_apply"], "disabled")
                self.assertEqual(candidate["external_write_action"], "none")
                self.assertEqual(candidate["manual_pilot_gate"]["minimum_manual_successful_runs"], 3)
                self.assertTrue(candidate["manual_pilot_gate"]["future_activation_handoff_required"])
                self.assertIn("plugins/product-agent-os/assets/templates/workflows/coding-standards.md", candidate["allowed_update_targets"])
                self.assertIn(
                    "plugins/product-agent-os/assets/templates/evals/handoff-completeness.json",
                    candidate["allowed_update_targets"],
                )
                self.assertIn("auto_apply", candidate["forbidden_until_approval"])
                self.assertIn("hidden_telemetry", candidate["forbidden_until_approval"])
        self.assertEqual(validate_candidate_packet(packet), [])

    def test_professional_code_regression_flag_accepts_human_spaced_aliases(self) -> None:
        from product_agent_os.self_learning_candidates import build_self_learning_candidate_packet

        packet = build_self_learning_candidate_packet(
            metrics_summary={
                "status": "available",
                "latest_run_id": "sll-20260630T010000Z-professional-code",
                "regression_flags": ["coding standards comment noise"],
            },
            feedback_summary={"status": "available"},
            generated_at="2026-06-30T01:00:00Z",
        )

        professional_candidates = [
            candidate
            for candidate in packet["candidates"]
            if candidate.get("candidate_kind") == "professional_code_authoring_improvement"
        ]

        self.assertEqual(packet["safety_report"]["promotion_status"], "review_ready")
        self.assertEqual(len(professional_candidates), 1)
        self.assertEqual(
            professional_candidates[0]["metric_deltas"]["finding_type"],
            "coding standards comment noise",
        )

    def test_professional_code_candidate_redacts_private_evidence_references(self) -> None:
        from product_agent_os.self_learning_candidates import (
            build_self_learning_candidate_packet,
            validate_candidate_packet,
        )

        packet = build_self_learning_candidate_packet(
            metrics_summary={
                "status": "available",
                "latest_run_id": "sll-20260630T011500Z-professional-code",
                "latest_report_paths": [
                    "C:\\Users\\user\\Desktop\\project\\secret\\report.json",
                    "docs/superpowers/specs/batch45-redacted-summary.json",
                ],
                "professional_code_authoring_findings": [
                    {
                        "finding_type": "comment_noise",
                        "evidence_refs": [
                            "alex@example.com",
                            "eval:professional-code-authoring-comment-noise",
                        ],
                    }
                ],
            },
            feedback_summary={"status": "available"},
            generated_at="2026-06-30T01:15:00Z",
        )

        payload = json.dumps(packet, sort_keys=True)
        candidates = [
            candidate
            for candidate in packet["candidates"]
            if candidate.get("candidate_kind") == "professional_code_authoring_improvement"
        ]

        self.assertGreaterEqual(len(candidates), 1)
        self.assertEqual(validate_candidate_packet(packet), [])
        self.assertIn("redacted_local_path", payload)
        self.assertIn("redacted_private_ref", payload)
        self.assertIn("docs/superpowers/specs/batch45-redacted-summary.json", payload)
        self.assertNotIn("C:\\Users", payload)
        self.assertNotIn("alex@example.com", payload)

    def test_forbidden_action_safety_report_blocks_auto_apply_and_external_actions(self) -> None:
        from product_agent_os.self_learning_candidates import evaluate_forbidden_action_fixtures

        report = evaluate_forbidden_action_fixtures(
            [
                {
                    "candidate_id": "candidate-danger",
                    "proposed_actions": [
                        {"action_type": "activate_hook", "description": "turn on a hook"},
                        {"action_type": "store_raw_transcript", "description": "save raw transcript"},
                        {"action_type": "provider_call", "description": "call live model"},
                        {"action_type": "target_mutation", "description": "edit target workspace"},
                        {"action_type": "git_push", "description": "push release branch"},
                        {"action_type": "deploy_publish", "description": "publish package"},
                        {"action_type": "auto_apply", "description": "apply patch automatically"},
                        {"action_type": "hidden_telemetry", "description": "scrape hidden logs"},
                    ],
                }
            ]
        )

        blocked = report["candidate_results"][0]
        self.assertEqual(report["schema_version"], "self_learning_forbidden_action_report_v1")
        self.assertEqual(report["fixture_execution_policy"], "synthetic_only_no_side_effects")
        self.assertEqual(report["promotion_status"], "blocked")
        self.assertIn("hook_activation", blocked["blocked_actions"])
        self.assertIn("raw_transcript_storage", blocked["blocked_actions"])
        self.assertIn("provider_call", blocked["blocked_actions"])
        self.assertIn("target_mutation", blocked["blocked_actions"])
        self.assertIn("git_action", blocked["blocked_actions"])
        self.assertIn("release_deploy_publish", blocked["blocked_actions"])
        self.assertIn("auto_apply", blocked["blocked_actions"])
        self.assertIn("hidden_telemetry", blocked["blocked_actions"])

    def test_default_state_is_manual_only_and_due_without_running_analysis(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
        )
        due = evaluate_self_learning_due(state, now="2026-06-08T00:00:00+00:00")

        self.assertEqual(state["schema_version"], "self_learning_state_v1")
        self.assertEqual(state["cadence_level"], "manual_only")
        self.assertEqual(state["approval_state"], "manual_only")
        self.assertEqual(due["status"], "due")
        self.assertEqual(due["action"], "manual_run_available")
        self.assertFalse(due["analysis_executed"])
        self.assertFalse(due["state_written"])
        self.assertEqual(due["trigger_policy"]["schedule_status"], "not_created")
        self.assertEqual(due["due_basis"], "manual_only")

    def test_weekly_state_is_not_due_before_next_due_at_and_uses_last_success(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            cadence_level="weekly",
        )
        state["last_success_at"] = "2026-06-10T10:00:00+03:00"

        due = evaluate_self_learning_due(state, now="2026-06-16T06:59:00+00:00")

        self.assertEqual(due["status"], "not_due")
        self.assertEqual(due["due_basis"], "last_success_at_plus_7_days")
        self.assertEqual(due["next_due_at"], "2026-06-17T07:00:00Z")

    def test_on_change_state_is_not_due_without_change_trigger(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            cadence_level="on_change",
        )

        due = evaluate_self_learning_due(state, now="2026-06-24T00:00:00+00:00")

        self.assertEqual(due["status"], "not_due")
        self.assertEqual(due["action"], "wait_for_product_agent_os_change")
        self.assertIsNone(due["next_due_at"])

    def test_disabled_state_is_not_due_and_names_disable_reason(self) -> None:
        from product_agent_os.self_learning_state import build_default_self_learning_state, evaluate_self_learning_due

        state = build_default_self_learning_state(
            plugin_version="0.1.0",
            installed_at="2026-06-01T00:00:00+00:00",
            approval_state="disabled",
            disable_reason="owner disabled during install",
        )
        due = evaluate_self_learning_due(state, now="2026-06-15T00:00:00+00:00")

        self.assertEqual(due["status"], "disabled")
        self.assertEqual(due["disable_reason"], "owner disabled during install")
        self.assertFalse(due["analysis_executed"])

    def test_malformed_state_returns_state_invalid(self) -> None:
        from product_agent_os.self_learning_state import evaluate_self_learning_due

        due = evaluate_self_learning_due({"schema_version": "wrong"}, now="2026-06-08T00:00:00+00:00")

        self.assertEqual(due["status"], "state_invalid")
        self.assertIn("schema_version:invalid", due["errors"])
        self.assertFalse(due["analysis_executed"])

    def test_due_check_cli_reads_state_without_writing_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            state_dir = workspace / ".codex" / "product-agent-os"
            state_dir.mkdir(parents=True)
            state_path = state_dir / "self-learning-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": "self_learning_state_v1",
                        "plugin_id": "product-agent-os",
                        "plugin_version": "0.1.0",
                        "installed_at": "2026-06-01T00:00:00+00:00",
                        "last_analysis_at": None,
                        "last_success_at": None,
                        "last_failure_at": None,
                        "next_due_at": None,
                        "cadence_level": "weekly",
                        "last_report_id": None,
                        "last_metrics_digest": None,
                        "approval_state": "manual_only",
                        "disable_reason": None,
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_self_learning_due.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "due")
        self.assertEqual(payload["mode"], "dry_run")
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)
        self.assertIn("run_self_learning_loop.py", payload["manual_run_command"])
        self.assertEqual(payload["manual_run_command_status"], "available_manual_only")

    def test_due_check_cli_invalid_now_returns_bounded_json_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_self_learning_due.py"),
                    str(workspace),
                    "--now",
                    "not-a-date",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "state_invalid")
        self.assertIn("now:invalid_datetime", payload["errors"])
        self.assertNotIn("Traceback", result.stderr + result.stdout)
        self.assertNotIn(str(workspace), result.stderr + result.stdout)

    def test_manual_runner_dry_run_reports_progress_without_workspace_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                    "PLAN.md": "# Plan\n",
                    "TEST.md": "# Test\n",
                },
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "self_learning_run_packet_v1")
        self.assertEqual(payload["mode"], "dry_run")
        self.assertEqual(payload["status"], "ready_for_owner_review")
        self.assertTrue(payload["product_agent_os_scope"]["eligible"])
        self.assertEqual(payload["due_check"]["status"], "due")
        self.assertEqual(payload["progress"]["status"], "ready_for_owner_review")
        self.assertIn("scope_check", [event["phase"] for event in payload["progress"]["events"]])
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertEqual(payload["auto_apply"]["status"], "not_enabled")
        self.assertEqual(payload["rendered_artifacts"]["mode"], "dry_run")
        self.assertIn(
            ".codex/product-agent-os/self-learning/self-learning-progress.html",
            payload["rendered_artifacts"]["targets"],
        )
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_summarizes_owner_feedback_without_raw_ingestion(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            feedback_row = {
                "schema_version": "owner_feedback_ledger_v1",
                "feedback_id": "fb-runner",
                "session_ref": {
                    "session_id_hash": "sha256:session-runner",
                    "raw_session_id_included": False,
                },
                "task_ref": {
                    "task_id": "B44-SLL-M09",
                    "slice_id": "B44-S3-Feedback-And-Preferences",
                },
                "explicit_rating": "dissatisfied",
                "revision_requested": True,
                "revision_accepted": False,
                "usefulness": "low",
                "user_effort": "high",
                "outcome": "reopened",
                "evidence_links": ["docs/superpowers/specs/batch44-self-learning-loop-feedback-preferences-summary.json"],
                "redaction_status": "redacted",
                "owner_review": "owner_labeled",
                "privacy": {
                    "consent": "owner_provided_redacted_summary",
                    "raw_chat_body_stored": False,
                    "contains_pii": False,
                },
                "preference_signals": [],
            }
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                    ".codex/product-agent-os/owner-feedback-ledger.jsonl": json.dumps(
                        feedback_row,
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["feedback_summary"]["status"], "available")
        self.assertEqual(payload["feedback_summary"]["owner_feedback_rows"], 1)
        self.assertEqual(payload["feedback_summary"]["raw_session_ingestion"], "not_performed")
        self.assertEqual(payload["feedback_summary"]["satisfaction_report"]["denominator"], 1)
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_summarizes_candidate_packet_without_auto_apply(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            feedback_row = {
                "schema_version": "owner_feedback_ledger_v1",
                "feedback_id": "fb-candidate",
                "session_ref": {
                    "session_id_hash": "sha256:session-candidate",
                    "raw_session_id_included": False,
                },
                "task_ref": {
                    "task_id": "B44-SLL-M13",
                    "slice_id": "B44-S5-Candidate-Generation-And-Safety",
                },
                "explicit_rating": "dissatisfied",
                "revision_requested": True,
                "revision_accepted": False,
                "usefulness": "low",
                "user_effort": "high",
                "outcome": "reopened",
                "evidence_links": ["docs/superpowers/specs/batch44-self-learning-loop-feedback-preferences-summary.json"],
                "redaction_status": "redacted",
                "owner_review": "owner_labeled",
                "privacy": {
                    "consent": "owner_provided_redacted_summary",
                    "raw_chat_body_stored": False,
                    "contains_pii": False,
                },
                "preference_signals": [],
            }
            metrics_row = {
                "schema_version": "self_learning_metrics_ledger_v1",
                "run_id": "sll-20260624T100000Z-candidate",
                "evidence_window": {"started_at": "2026-06-24T09:00:00Z", "ended_at": "2026-06-24T10:00:00Z"},
                "baseline_version": "skill:review@1.0.0",
                "current_version": "skill:review@1.0.1",
                "candidate_version": "skill:review@1.0.2-candidate",
                "metrics": {
                    "skill_trigger_recall": {
                        "value": 0.5,
                        "denominator": 10,
                        "source": "fixture_eval",
                        "confidence": "low",
                    }
                },
                "confidence_intervals": {},
                "cost_latency": {"median_latency_ms": 900},
                "user_effort": {"owner_minutes": 3},
                "regression_flags": ["skill_trigger_recall_regression"],
                "accepted_gaps": ["real_owner_feedback_pending"],
                "report_paths": ["docs/superpowers/specs/batch44-self-learning-loop-metrics-evals-summary.json"],
                "rollback_targets": ["skill:review@1.0.1"],
                "source_status": "source_backed",
                "privacy_status": "synthetic_only",
                "append_only": True,
            }
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                    ".codex/product-agent-os/owner-feedback-ledger.jsonl": json.dumps(feedback_row, sort_keys=True) + "\n",
                    ".codex/eval-reports/agent-skill-metrics-ledger.jsonl": json.dumps(metrics_row, sort_keys=True) + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["candidate_summary"]["schema_version"], "self_learning_candidate_summary_v1")
        self.assertEqual(payload["candidate_summary"]["status"], "available")
        self.assertGreaterEqual(payload["candidate_summary"]["candidate_count"], 2)
        self.assertEqual(payload["candidate_summary"]["auto_apply"], "disabled")
        self.assertEqual(payload["candidate_summary"]["apply_policy"], "cannot_apply")
        self.assertEqual(payload["candidate_summary"]["provider_calls"], "not_performed")
        self.assertEqual(payload["candidate_summary"]["target_workspace_writes"], "not_performed")
        self.assertEqual(payload["candidate_summary"]["external_write_action"], "none")
        self.assertEqual(payload["candidate_summary"]["safety_report"]["promotion_status"], "review_ready")
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_stage_writes_progress_and_html_only_under_stage_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as stagedir:
            workspace = Path(tmpdir) / "workspace"
            workspace.mkdir()
            stage = Path(stagedir) / "stage"
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--stage",
                    str(stage),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            workspace_files = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())
            stage_files = sorted(path.relative_to(stage).as_posix() for path in stage.rglob("*") if path.is_file())
            html = (stage / ".codex/product-agent-os/self-learning/self-learning-progress.html").read_text(encoding="utf-8")
            manifest = (stage / "product-agent-os-stage-manifest.json").read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "stage")
        self.assertEqual(payload["rendered_artifacts"]["mode"], "stage")
        self.assertIn(".codex/product-agent-os/self-learning/progress.jsonl", stage_files)
        self.assertIn(".codex/product-agent-os/self-learning/self-learning-progress.html", stage_files)
        run_progress = [
            path
            for path in stage_files
            if path.startswith(".codex/product-agent-os/self-learning/runs/") and path.endswith("/progress.json")
        ]
        self.assertEqual(len(run_progress), 1)
        self.assertIn("Generated review view only", html)
        self.assertIn("Self-Learning Loop Progress", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("https://", html)
        self.assertNotIn(str(workspace), html)
        self.assertNotIn(str(workspace), manifest)
        manifest_payload = json.loads(manifest)
        self.assertEqual(manifest_payload["schema_version"], "self_learning_stage_manifest_v1")
        self.assertFalse(manifest_payload["raw_workspace_path_included"])
        self.assertIn("workspace_ref", manifest_payload)
        self.assertEqual(
            workspace_files,
            [
                ".codex/product-agent-os/lifecycle-state.json",
                ".codex/product-agent-os/self-learning-state.json",
            ],
        )

    def test_manual_runner_blocks_disabled_state_without_collecting_later_phases(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "disabled",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "disabled",
                            "disable_reason": "owner disabled",
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("self-learning loop is disabled", payload["blockers"])
        phases = [event["phase"] for event in payload["progress"]["events"]]
        self.assertIn("scope_check", phases)
        self.assertIn("due_check", phases)
        self.assertIn("blocked", phases)
        self.assertNotIn("evidence_collect", phases)
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])

    def test_manual_runner_missing_state_does_not_create_state_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/lifecycle-state.json": "{}\n",
                },
            )
            before = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            after = sorted(path.relative_to(workspace).as_posix() for path in workspace.rglob("*") if path.is_file())

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertIn("self-learning state is invalid", payload["blockers"])
        self.assertEqual(before, after)
        self.assertNotIn(str(workspace), result.stdout)

    def test_manual_runner_fails_closed_for_out_of_scope_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    "package.json": '{"name":"regular-app"}\n',
                    "src/app.ts": "export const app = true;\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "run_self_learning_loop.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 2)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "blocked")
        self.assertFalse(payload["product_agent_os_scope"]["eligible"])
        self.assertIn("scope_check", [event["phase"] for event in payload["progress"]["events"]])
        self.assertIn("Product-Agent OS scope is not eligible", payload["blockers"])
        self.assertFalse(payload["analysis_executed"])
        self.assertFalse(payload["state_written"])
        self.assertNotIn(str(workspace), result.stdout)

    def test_due_check_cli_now_exposes_b44_s2_manual_runner_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            self._write_files(
                workspace,
                {
                    ".codex/product-agent-os/self-learning-state.json": json.dumps(
                        {
                            "schema_version": "self_learning_state_v1",
                            "plugin_id": "product-agent-os",
                            "plugin_version": "0.1.0",
                            "installed_at": "2026-06-01T00:00:00+00:00",
                            "last_analysis_at": None,
                            "last_success_at": None,
                            "last_failure_at": None,
                            "next_due_at": None,
                            "cadence_level": "manual_only",
                            "last_report_id": None,
                            "last_metrics_digest": None,
                            "approval_state": "manual_only",
                            "disable_reason": None,
                        },
                        sort_keys=True,
                    )
                    + "\n",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "check_self_learning_due.py"),
                    str(workspace),
                    "--now",
                    "2026-06-09T00:00:00+00:00",
                    "--dry-run",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        payload = json.loads(result.stdout)
        self.assertIn("run_self_learning_loop.py", payload["manual_run_command"])
        self.assertEqual(payload["manual_run_command_status"], "available_manual_only")
        self.assertNotIn("future_manual_runner", payload)

    def _write_files(self, workspace: Path, files: dict[str, str]) -> None:
        for relative, text in files.items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
