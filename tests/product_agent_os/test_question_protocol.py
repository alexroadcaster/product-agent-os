import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.question_protocol import (  # noqa: E402
    MAX_FIRST_RESPONSE_BLOCKING,
    MAX_TOTAL_QUESTIONS,
    QUESTION_ANSWER_TYPES,
    QUESTION_CATEGORIES,
    QUESTION_PRIORITIES,
    build_question_queue,
)


class QuestionProtocolTest(unittest.TestCase):
    def test_question_queue_limits_first_response_to_one_blocking_question(self):
        packet = build_question_queue(
            owner_questions=[
                "Which local command is the source of truth for verification?",
                "Who owns the highest-priority missing methodology gate?",
            ],
            unknowns=["current verification command"],
            runtime_status="route_ready",
        )

        blocking = [item for item in packet["questions"] if item["priority"] == "blocking"]

        self.assertEqual(packet["schema_version"], 1)
        self.assertEqual(packet["write_policy"], "read_only")
        self.assertEqual(
            packet["policy"]["max_blocking_questions_in_first_response"],
            MAX_FIRST_RESPONSE_BLOCKING,
        )
        self.assertEqual(MAX_FIRST_RESPONSE_BLOCKING, 1)
        self.assertEqual(len(blocking), 1)
        self.assertEqual(packet["next_blocking_question"], blocking[0])
        self.assertEqual(packet["summary"]["blocking"], 1)
        self.assertGreaterEqual(packet["summary"]["remaining"], 1)

    def test_question_queue_uses_supported_priorities_categories_and_answer_types(self):
        packet = build_question_queue(
            owner_questions=[
                {
                    "text": "Who owns the security review?",
                    "source_kind": "methodology_packet",
                    "source_key": "questions_for_owner",
                    "category": "ownership",
                    "answer_type": "text",
                    "artifact": "security-risk-review.md",
                }
            ],
            unknowns=["artifact owners and approval boundaries"],
            recommendation_groups=[
                {
                    "priority": "P0_blocker",
                    "artifact": "approval-record.md",
                    "owner_domain": "security_privacy_compliance",
                    "gates": ["external_write_approval_present"],
                    "evidence_required": ["owner approval"],
                    "safe_next_action": "Record approval_required before external mutation.",
                }
            ],
            usage_mode={"primary": "security_sensitive_change"},
            runtime_gaps=[
                {
                    "category": "verification",
                    "question": "Which local verification command should run before completion?",
                    "answer_type": "text",
                    "source_key": "runtime_verification_command",
                }
            ],
            runtime_status="route_ready",
        )

        self.assertLessEqual(len(packet["questions"]), MAX_TOTAL_QUESTIONS)
        for question in packet["questions"]:
            with self.subTest(question=question["id"]):
                self.assertIn(question["priority"], QUESTION_PRIORITIES)
                self.assertIn(question["category"], QUESTION_CATEGORIES)
                self.assertIn(question["answer_type"], QUESTION_ANSWER_TYPES)
                self.assertTrue(question["source"]["kind"])
                self.assertTrue(question["source"]["key"])

        categories = {question["category"] for question in packet["questions"]}
        self.assertIn("approval", categories)
        self.assertIn("ownership", categories)
        self.assertIn("verification", categories)

    def test_question_ids_use_source_metadata_not_prompt_wording(self):
        first = build_question_queue(
            owner_questions=[
                {
                    "text": "Which local command is the source of truth for verification?",
                    "source_kind": "methodology_packet",
                    "source_key": "verification_command",
                    "category": "verification",
                    "artifact": "TEST.md",
                    "block": "local_verification",
                }
            ]
        )
        second = build_question_queue(
            owner_questions=[
                {
                    "text": "What exact local verification command should Codex run?",
                    "source_kind": "methodology_packet",
                    "source_key": "verification_command",
                    "category": "verification",
                    "artifact": "TEST.md",
                    "block": "local_verification",
                }
            ]
        )

        self.assertEqual(first["questions"][0]["id"], second["questions"][0]["id"])
        self.assertNotIn("which-local-command", first["questions"][0]["id"])
        self.assertNotIn("what-exact-local", second["questions"][0]["id"])

    def test_question_queue_trims_by_priority_and_is_deterministic(self):
        owner_questions = [
            {
                "text": f"Optional owner context {index}?",
                "source_kind": "methodology_packet",
                "source_key": f"optional_owner_{index}",
                "category": "scope",
                "priority": "optional",
            }
            for index in range(10)
        ]
        recommendation_groups = [
            {
                "priority": "P0_blocker",
                "artifact": "approval-record.md",
                "gates": ["external_write_approval_present"],
                "evidence_required": ["owner approval"],
            },
            {
                "priority": "P1_high_risk",
                "artifact": "release-readiness.md",
                "gates": ["release_evidence_present"],
                "evidence_required": ["release scope"],
            },
        ]

        first = build_question_queue(
            owner_questions=owner_questions,
            recommendation_groups=recommendation_groups,
            unknowns=["accepted scope and implementation plan"],
        )
        second = build_question_queue(
            owner_questions=owner_questions,
            recommendation_groups=recommendation_groups,
            unknowns=["accepted scope and implementation plan"],
        )

        self.assertEqual(first, second)
        self.assertEqual(len(first["questions"]), MAX_TOTAL_QUESTIONS)
        self.assertEqual(first["questions"][0]["priority"], "blocking")
        self.assertEqual(first["questions"][0]["artifact"], "approval-record.md")
        self.assertIn(
            "release-readiness.md",
            [question["artifact"] for question in first["questions"]],
        )


if __name__ == "__main__":
    unittest.main()
