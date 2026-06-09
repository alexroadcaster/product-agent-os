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
    DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
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


if __name__ == "__main__":
    unittest.main()
