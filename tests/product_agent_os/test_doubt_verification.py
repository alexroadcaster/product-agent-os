import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.doubt_verification import (  # noqa: E402
    COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS,
    COMPLETION_SKEPTIC_SCORECARD_THRESHOLDS,
    DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
    build_completion_skeptic_go_no_go_packet,
    build_completion_skeptic_pilot_ledger,
    build_completion_skeptic_scorecard_calibration,
    evaluate_completion_skeptic_scorecard,
    validate_completion_skeptic_recommendation_packet,
    validate_doubt_verification_packet,
    validate_doubt_verification_packet_file,
)


class DoubtVerificationTest(unittest.TestCase):
    def test_doubt_packet_accepts_supported_claims_current_evidence_and_handoff_mapping(self):
        packet = _valid_doubt_packet()

        self.assertEqual(validate_doubt_verification_packet(packet), [])
        self.assertEqual(validate_doubt_verification_packet_file(_write_packet(packet)), [])

    def test_doubt_packet_rejects_pass_with_unsupported_claim_generated_view_proof_or_missing_provenance(self):
        packet = _valid_doubt_packet()
        packet["claim_ledger"][0]["status"] = "unsupported"
        packet["evidence_ledger"][0]["evidence_provider"] = "status_dashboard"
        packet["evidence_ledger"][0]["evidence_role"] = "proof"
        del packet["evidence_ledger"][0]["provenance"]
        packet["artifact_under_review"]["path"] = "C:/Users/person/private-project/RUNLOG.md"

        errors = validate_doubt_verification_packet(packet)

        self.assertIn("claim_ledger[0].status:blocks_pass_verdict", errors)
        self.assertIn("evidence_ledger[0].provider:generated_view_not_completion_proof", errors)
        self.assertIn("evidence_ledger[0].provenance:required", errors)
        self.assertIn("doubt_verification_packet:contains_local_path", errors)

    def test_completion_skeptic_recommendation_is_bounded_route_guidance_not_source_truth(self):
        packet = _valid_recommendation()

        self.assertEqual(validate_completion_skeptic_recommendation_packet(packet), [])
        self.assertLessEqual(
            len(packet["required_evidence"]),
            COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["required_evidence"],
        )

    def test_completion_skeptic_recommendation_rejects_external_refs_paths_and_apply_actions(self):
        packet = _valid_recommendation()
        packet["write_policy"] = "staged_only"
        packet["status"] = "forced"
        packet["trigger_level"] = "forced"
        packet["artifact_under_review"]["path"] = "https://example.invalid/report.html"
        packet["packet_ref"] = {"kind": "staged_artifact", "path": "D:/private/doubt.json"}
        packet["required_evidence"] = ["command"] * (
            COMPLETION_SKEPTIC_RECOMMENDATION_LIMITS["required_evidence"] + 1
        )
        packet["safe_next_action"] = ""

        errors = validate_completion_skeptic_recommendation_packet(packet)

        self.assertIn("completion_skeptic_recommendation.write_policy:must_be_read_only", errors)
        self.assertIn("completion_skeptic_recommendation.status:invalid", errors)
        self.assertIn("completion_skeptic_recommendation.trigger_level:invalid", errors)
        self.assertIn("completion_skeptic_recommendation.artifact_under_review.path:external_url_forbidden", errors)
        self.assertIn("completion_skeptic_recommendation.packet_ref.path:absolute_or_unsafe", errors)
        self.assertIn("completion_skeptic_recommendation.required_evidence:too_many", errors)
        self.assertIn("completion_skeptic_recommendation.safe_next_action:required", errors)

    def test_doubt_packet_cli_returns_json_without_traceback(self):
        invalid_path = _write_packet({"schema_version": DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION})

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_doubt_verification_packet.py"),
                str(invalid_path),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stderr, "")
        self.assertFalse(payload["ok"])
        self.assertIn("verdict:required", payload["errors"])

    def test_doubt_packet_rejects_fake_evidence_approval_blocked_pass_and_missing_code_tool_evidence(self):
        packet = _valid_doubt_packet()
        packet["approval_boundary"] = {
            "status": "approval_blocked",
            "hits": ["browser/runtime evidence needs owner approval"],
        }
        packet["claim_ledger"][0]["claim_type"] = "code_behavior"
        packet["evidence_ledger"][0]["evidence_provider"] = "local_file"
        packet["evidence_ledger"][0]["evidence_ref"] = "user says the command passed"
        packet["evidence_ledger"][0]["provenance"]["kind"] = "user_claim"

        errors = validate_doubt_verification_packet(packet)

        self.assertIn("approval_boundary.status:blocks_pass_verdict", errors)
        self.assertIn("claim_ledger[0].claim_type:code_behavior_requires_command_evidence", errors)
        self.assertIn("evidence_ledger[0].provenance.kind:invalid", errors)
        self.assertIn("evidence_ledger[0].evidence_ref:fake_or_unverified_command_claim", errors)

    def test_doubt_packet_requires_accepted_gap_owner_reason_residual_risk_and_follow_up(self):
        packet = _valid_doubt_packet()
        packet["claim_ledger"][0]["status"] = "accepted_gap"
        packet["requirement_ledger"][0]["status"] = "accepted_gap"
        packet["evidence_ledger"][0]["status"] = "accepted_gap"
        packet["gap_ledger"] = [{"gap_id": "gap-no-owner"}]

        errors = validate_doubt_verification_packet(packet)

        for expected in [
            "claim_ledger[0].accepted_gap:required",
            "requirement_ledger[0].accepted_gap:required",
            "evidence_ledger[0].accepted_gap:required",
            "gap_ledger[0].owner:required",
            "gap_ledger[0].reason:required",
            "gap_ledger[0].residual_risk:required",
            "gap_ledger[0].follow_up:required",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, errors)

    def test_completion_skeptic_scorecard_blocks_false_pass_false_rewrite_and_low_catch_rates(self):
        good_records = [
            {
                "false_pass": False,
                "false_rewrite": False,
                "unsupported_claim_present": True,
                "unsupported_claim_caught": True,
                "missing_check_present": True,
                "missing_check_caught": True,
                "accepted_gap": index == 0,
                "user_revision_offered": True,
                "user_revision_accepted": True,
            }
            for index in range(COMPLETION_SKEPTIC_SCORECARD_THRESHOLDS["min_sample_size"])
        ]

        passed = evaluate_completion_skeptic_scorecard(
            good_records,
            owner_review_status="owner_reviewed",
        )

        self.assertEqual(passed["schema_version"], 1)
        self.assertEqual(passed["scorecard_id"], "completion_skeptic_quality_scorecard")
        self.assertEqual(passed["decision_status"], "scorecard_passed")
        self.assertEqual(passed["blockers"], [])

        bad_records = [
            {
                "false_pass": True,
                "false_rewrite": True,
                "unsupported_claim_present": True,
                "unsupported_claim_caught": False,
                "missing_check_present": True,
                "missing_check_caught": False,
                "accepted_gap": True,
                "user_revision_offered": True,
                "user_revision_accepted": False,
            }
            for _ in range(COMPLETION_SKEPTIC_SCORECARD_THRESHOLDS["min_sample_size"])
        ]

        blocked = evaluate_completion_skeptic_scorecard(
            bad_records,
            owner_review_status="missing",
        )

        self.assertEqual(blocked["decision_status"], "blocked_by_scorecard")
        for expected in [
            "owner_review_or_gap_missing",
            "false_pass_rate_above_threshold",
            "false_rewrite_rate_above_threshold",
            "unsupported_claim_catch_rate_below_threshold",
            "missing_check_catch_rate_below_threshold",
            "accepted_gap_rate_above_threshold",
            "user_revision_acceptance_rate_below_threshold",
        ]:
            with self.subTest(expected=expected):
                self.assertIn(expected, blocked["blockers"])

    def test_completion_skeptic_pilot_ledger_calibration_and_go_no_go_keep_manual(self):
        records = _completion_skeptic_pilot_records()

        ledger = build_completion_skeptic_pilot_ledger(
            records,
            pilot_scope="synthetic_local",
            owner_review_status="accepted_gap",
        )

        self.assertEqual(ledger["schema_version"], 1)
        self.assertEqual(ledger["ledger_id"], "completion_skeptic_manual_pilot_ledger")
        self.assertEqual(ledger["decision_status"], "pilot_evidence_recorded")
        self.assertTrue(ledger["no_unapproved_actions"])
        self.assertEqual(ledger["sample_size"], COMPLETION_SKEPTIC_SCORECARD_THRESHOLDS["min_sample_size"])
        self.assertEqual(ledger["missing_required_archetypes"], [])
        for expected in ["docs_research", "code_check", "expected_block"]:
            with self.subTest(archetype=expected):
                self.assertIn(expected, ledger["archetype_counts"])
        for expected in [
            "attempt_count",
            "failure_count",
            "fix_count",
            "retest_count",
            "false_positive_count",
            "false_rewrite_count",
            "evidence_sufficient_count",
            "owner_accepted_gap_count",
        ]:
            with self.subTest(summary_count=expected):
                self.assertIn(expected, ledger["summary"])
        self.assertEqual(ledger["promotion_boundary"], "manual_only_synthetic_pilots_do_not_prove_release")

        calibration = build_completion_skeptic_scorecard_calibration(
            records,
            owner_review_status="accepted_gap",
            pilot_scope=ledger["pilot_scope"],
        )

        self.assertEqual(calibration["schema_version"], 1)
        self.assertEqual(calibration["calibration_id"], "completion_skeptic_scorecard_calibration")
        self.assertEqual(calibration["decision_status"], "calibrated_with_accepted_metrics_gap")
        self.assertEqual(calibration["scorecard"]["decision_status"], "scorecard_passed")
        for metric_name in [
            "false_pass_rate",
            "false_rewrite_rate",
            "evidence_sufficiency_rate",
            "missing_check_catch_rate",
            "accepted_gap_rate",
            "user_revision_acceptance_rate",
            "revision_usefulness_rate",
        ]:
            with self.subTest(metric_name=metric_name):
                metric_evidence = calibration["metric_evidence"][metric_name]
                self.assertIn("numerator", metric_evidence)
                self.assertIn("denominator", metric_evidence)

        closure = build_completion_skeptic_go_no_go_packet(
            pilot_ledger=ledger,
            scorecard_calibration=calibration,
            implemented_rows=["B40-DVL-M22", "B40-DVL-M23", "B40-DVL-M24"],
            verification_evidence=[
                "python -m unittest tests.product_agent_os.test_doubt_verification -v",
            ],
            docs_site_state={
                "source_docs_synced": True,
                "site_rebuild_required": False,
                "generated_site_is_source_of_truth": False,
            },
            no_unapproved_actions=True,
            owner_review_status="accepted_gap",
        )

        self.assertEqual(closure["schema_version"], 1)
        self.assertEqual(closure["packet_id"], "completion_skeptic_go_no_go_closure")
        self.assertEqual(closure["decision_status"], "manual_only")
        self.assertEqual(closure["promotion_status"], "not_promoted")
        self.assertEqual(closure["missing_rows"], [])
        self.assertTrue(closure["no_unapproved_actions_proof"]["status"])
        self.assertIn("rollback_disable_path", closure)
        self.assertIn("exact_owner_approval_for_release_or_automation", closure["next_approval_needs"])


def _write_packet(packet):
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
    with tmp:
        json.dump(packet, tmp)
    return Path(tmp.name)


def _valid_recommendation():
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "status": "recommended",
        "recommended_skill": "completion-skeptic",
        "trigger_level": "recommended",
        "trigger_sources": ["completion_claim"],
        "risk_classes": ["verification_gap"],
        "reasons": ["completion claim needs a second-pass evidence check"],
        "skip_reasons": [],
        "artifact_under_review": {
            "kind": "runtime_result",
            "path": ".codex/product-agent-os/status.json",
            "label": "status snapshot",
        },
        "artifact_type": "plugin_skill",
        "required_evidence": ["current command evidence", "source artifact ledger", "accepted gaps"],
        "evidence_summary": {
            "required": 3,
            "available": 1,
            "missing": 1,
            "stale": 0,
            "approval_required": 0,
            "accepted_gap": 1,
        },
        "approval_boundary": {"status": "not_required", "hits": []},
        "packet_ref": {"kind": "not_available", "path": "", "digest": ""},
        "safe_next_action": "Run completion-skeptic before claiming completion.",
        "source_policy": "completion skeptic recommendation is generated routing guidance, not source of truth",
        "redaction_status": {"status": "clean", "categories": []},
    }


def _valid_doubt_packet():
    return {
        "schema_version": DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
        "verdict": "pass",
        "artifact_under_review": {
            "kind": "task_row",
            "path": "docs/sources/product-agent-os-track-10-backlog.md",
            "label": "B40-S2",
        },
        "claim_ledger": [
            {
                "claim_id": "claim-current-evidence",
                "claim": "Focused validator tests ran in the current run.",
                "status": "supported",
                "provenance": {
                    "kind": "command",
                    "ref": "python -m unittest tests.product_agent_os.test_doubt_verification -v",
                    "checked_at": "2026-06-09T12:00:00+03:00",
                },
            }
        ],
        "requirement_ledger": [
            {
                "requirement_id": "req-no-generated-proof",
                "requirement": "Generated dashboards cannot be completion proof.",
                "status": "covered",
                "provenance": {
                    "kind": "source",
                    "ref": "AGENTS.md generated dashboard policy",
                    "checked_at": "2026-06-09T12:00:00+03:00",
                },
            }
        ],
        "evidence_ledger": [
            {
                "evidence_id": "ev-current-unittest",
                "evidence_provider": "command",
                "evidence_role": "proof",
                "status": "available",
                "evidence_ref": "python -m unittest tests.product_agent_os.test_doubt_verification -v",
                "provenance": {
                    "kind": "command",
                    "ref": "focused unit test",
                    "checked_at": "2026-06-09T12:00:00+03:00",
                },
            }
        ],
        "approval_boundary": {"status": "not_required", "hits": []},
        "gap_ledger": [],
        "handoff": {
            "verified_claims": ["claim-current-evidence"],
            "unsupported_claims": [],
            "verification_evidence": ["ev-current-unittest"],
            "stop_reason": "doubt_verification_passed",
            "recommended_next_role": "risk-reviewer",
        },
        "source_policy": "doubt verification packet is evidence ledger, not generated dashboard proof",
        "redaction_status": {"status": "clean", "categories": []},
    }


def _completion_skeptic_pilot_records():
    records = []
    archetypes = [
        "docs_research",
        "code_check",
        "expected_block",
        "docs_research",
        "code_check",
    ]
    for index, archetype in enumerate(archetypes):
        records.append(
            {
                "pilot_id": f"synthetic-pilot-{index + 1}",
                "archetype": archetype,
                "attempt_recorded": True,
                "failure_recorded": index in {1, 2},
                "fix_recorded": index in {1, 2},
                "retest_recorded": True,
                "false_pass": False,
                "false_positive": index == 3,
                "false_rewrite": False,
                "unsupported_claim_present": True,
                "unsupported_claim_caught": True,
                "missing_check_present": True,
                "missing_check_caught": True,
                "evidence_sufficient": True,
                "accepted_gap": index == 0,
                "owner_accepted_gap": index == 0,
                "user_revision_offered": True,
                "user_revision_accepted": True,
                "revision_useful": True,
                "unapproved_action_performed": False,
            }
        )
    return records


if __name__ == "__main__":
    unittest.main()
