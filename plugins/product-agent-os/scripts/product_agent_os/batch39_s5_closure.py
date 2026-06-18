from __future__ import annotations

from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


SCHEMA_VERSION = "batch39_s5_closure_packet_v1"
ATTEMPT_ID = "B39-S5-CLOSURE-A01"
NO_ACTIONS_PERFORMED = {
    "target_workspace_mutation": False,
    "dependency_install": False,
    "live_server": False,
    "browser_automation": False,
    "provider_api_call": False,
    "mcp_external_call": False,
    "git_stage_commit_push_pr": False,
    "release_deploy_publish": False,
    "active_automation": False,
}


def build_b39_s5_closure_packet(
    *,
    generated_at: str,
    s4_closure_matrix: dict[str, Any],
    verification_evidence: dict[str, Any],
) -> dict[str, Any]:
    """Build the Batch 39 S5 closure packet without promoting release readiness."""

    owner_feedback_plan = build_owner_feedback_test_plan()
    no_action_proof = build_no_unapproved_actions_proof(generated_at=generated_at)
    s4_blockers = _s4_blockers(s4_closure_matrix)
    tasks = {
        "B39-TEST-M34": {
            "status": "passed_source_docs_sync",
            "technical_value": "aligns control-plane and source-owned ledgers after S4 execution evidence",
            "product_value": "gives the owner one current route into feedback testing without reading stale S4 rows",
            "evidence_refs": [
                "AGENTS.md",
                "PLAN.md",
                "TEST.md",
                "EVALS.md",
                "RUNLOG.md",
                "prod_test.md",
                "docs/superpowers/specs/batch39-s5-closure-summary.json",
            ],
            "docs_sync_scope": "control_plane_and_batch39_ledger",
            "readiness_claim": "not_claimed",
        },
        "B39-TEST-M35": {
            "status": "conditional_go_owner_feedback_testing_not_release",
            "decision": "conditional_go_owner_feedback_testing",
            "release_go": False,
            "owner_feedback_testing_go": True,
            "technical_value": "consumes S4 blockers into an explicit go/no-go decision instead of hidden residual risk",
            "product_value": "unblocks structured owner feedback while preventing accidental release or promotion",
            "go_conditions": [
                "owner feedback testing stays manual and local/read-only by default",
                "runtime/browser pilot remains separate and approval-gated",
                "no release, deploy, publish, package registry, marketplace or automation promotion occurs",
            ],
            "blocking_reasons": s4_blockers,
            "evidence_refs": [
                "docs/superpowers/specs/batch39-s4-closure-readiness-matrix.json",
                "docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json",
            ],
            "readiness_claim": "not_claimed",
        },
        "B39-TEST-M36": {
            "status": "passed_no_unapproved_actions_proof",
            "technical_value": "records all high-impact surfaces as not performed in S5",
            "product_value": "keeps trust boundary intact before owner-facing testing begins",
            "evidence_refs": ["docs/superpowers/specs/batch39-s5-no-unapproved-actions-proof.json"],
            "proof_ref": no_action_proof["proof_id"],
            "readiness_claim": "not_claimed",
        },
    }
    packet = {
        "schema_version": SCHEMA_VERSION,
        "attempt_id": ATTEMPT_ID,
        "generated_at": generated_at,
        "slice": "B39-S5",
        "slice_status": "closed_for_owner_feedback_testing_not_release_ready",
        "covered_tasks": sorted(tasks),
        "tasks": tasks,
        "go_no_go": {
            "release": "no_go",
            "owner_feedback_testing": "conditional_go",
            "runtime_browser_pilot": "approval_required",
            "reason": "S4 blockers are explicit and bounded; owner feedback can start manually, but release/runtime/browser promotion remains blocked.",
        },
        "owner_feedback_test_plan": owner_feedback_plan,
        "no_unapproved_actions_proof": no_action_proof,
        "s4_closure_input": _bounded_s4_input(s4_closure_matrix),
        "verification_evidence": dict(sorted((verification_evidence or {}).items())),
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
        "unsupported_claims": [
            "release readiness is not claimed",
            "runtime/browser behavior is not claimed",
            "target apply safety is not claimed",
            "public docs/site acceptance is not claimed while MkDocs is unavailable",
            "owner-feedback results do not exist until the owner performs the next testing loop",
            "automation, deployment, publication and git release actions were not performed",
        ],
        "next_actions": [
            "start owner-feedback testing with the manual scenarios in batch39-s5-owner-feedback-test-plan.json",
            "collect owner scores, confusion points, task outcomes and accepted gaps as new evidence",
            "request exact approval before any runtime/browser/provider/MCP/git/release/deploy/publish/automation action",
        ],
    }
    packet["summary_digest"] = content_digest(canonical_json(packet))
    return packet


def build_owner_feedback_test_plan() -> dict[str, Any]:
    scenarios = [
        _scenario(
            scenario_id="owner-first-run-orientation",
            question="Can the owner understand the first safe action from the generated first-run packet without extra explanation?",
            evidence=["owner verdict", "time to first safe action", "confusing artifact names", "missing context"],
        ),
        _scenario(
            scenario_id="owner-sol-static-readiness-review",
            question="Does the SOL 0.6 static readiness packet separate useful evidence from runtime/browser blockers clearly?",
            evidence=["owner verdict", "blocker clarity score", "untrusted claim notes"],
        ),
        _scenario(
            scenario_id="owner-neural-flow-expected-block-review",
            question="Does the Neural_Flow expected-block path feel honest and useful for a docs/research-only target?",
            evidence=["owner verdict", "expected-block clarity", "missing next action"],
        ),
        _scenario(
            scenario_id="owner-cli-matrix-usability",
            question="Does the all-script CLI matrix make it clear which commands are safe to inspect and which require approval?",
            evidence=["owner verdict", "unsafe-command confusion points", "help text gaps"],
        ),
        _scenario(
            scenario_id="owner-go-no-go-decision-review",
            question="Is the conditional-go/no-go decision strict enough to prevent accidental release while allowing feedback testing?",
            evidence=["owner verdict", "accepted residual risks", "requested approval-gated pilots"],
        ),
    ]
    return {
        "schema_version": "batch39_s5_owner_feedback_test_plan_v1",
        "status": "ready_for_manual_owner_feedback_testing",
        "promotion_status": "manual_only_not_promoted",
        "scenarios": scenarios,
        "score_fields": [
            "clarity_1_to_5",
            "trust_1_to_5",
            "actionability_1_to_5",
            "missing_evidence",
            "false_or_overstated_claims",
            "next_owner_action",
        ],
        "approval_required_followups": [
            "runtime/browser pilot",
            "provider/API or live model calls",
            "MCP/Context7 live calls",
            "target workspace writes",
            "git stage/commit/push/PR",
            "release/deploy/publish/package registry/marketplace",
            "automation activation",
        ],
    }


def build_no_unapproved_actions_proof(*, generated_at: str) -> dict[str, Any]:
    proof = {
        "schema_version": "batch39_s5_no_unapproved_actions_proof_v1",
        "proof_id": "B39-TEST-M36-A01",
        "generated_at": generated_at,
        "actions_performed": dict(NO_ACTIONS_PERFORMED),
        "allowed_writes": [
            "local codex_docs code/test/docs artifacts",
            "docs/superpowers/specs/batch39-s5-*.json generated evidence",
        ],
        "forbidden_without_exact_approval": sorted(NO_ACTIONS_PERFORMED),
        "status": "passed_no_unapproved_actions_proof",
    }
    proof["proof_digest"] = content_digest(canonical_json(proof))
    return proof


def build_go_no_go_decision_packet(closure_packet: dict[str, Any]) -> dict[str, Any]:
    packet = {
        "schema_version": "batch39_s5_go_no_go_decision_packet_v1",
        "attempt_id": closure_packet["attempt_id"],
        "generated_at": closure_packet["generated_at"],
        "decision": closure_packet["go_no_go"],
        "blocking_reasons": closure_packet["tasks"]["B39-TEST-M35"]["blocking_reasons"],
        "conditions": closure_packet["tasks"]["B39-TEST-M35"]["go_conditions"],
        "unsupported_claims": closure_packet["unsupported_claims"],
        "next_actions": closure_packet["next_actions"],
    }
    packet["decision_digest"] = content_digest(canonical_json(packet))
    return packet


def _scenario(*, scenario_id: str, question: str, evidence: list[str]) -> dict[str, Any]:
    return {
        "id": scenario_id,
        "question_for_owner": question,
        "evidence_to_collect": evidence,
        "external_action_required": False,
        "target_mutation_required": False,
        "pass_condition": "owner can make a bounded next decision without release/readiness overclaim",
    }


def _s4_blockers(s4_closure_matrix: dict[str, Any]) -> list[str]:
    blocked = list(s4_closure_matrix.get("blocked_expected_tasks") or [])
    approval = list(s4_closure_matrix.get("approval_required_tasks") or [])
    reasons = []
    if "B39-TEST-M37" in blocked:
        reasons.append("fresh public docs/site acceptance blocked because MkDocs is unavailable")
    if "B39-TEST-M42" in blocked:
        reasons.append("runtime/browser proof requires exact disposable target approval")
    if "B39-TEST-M46" in approval:
        reasons.append("MCP/Context7 live/external calls require approval")
    if "B39-TEST-M54" in approval:
        reasons.append("release/distribution governance requires owner approval")
    if not reasons:
        reasons.append("S4 closure matrix did not prove release readiness")
    return reasons


def _bounded_s4_input(s4_closure_matrix: dict[str, Any]) -> dict[str, Any]:
    return {
        "closure_status": str(s4_closure_matrix.get("closure_status") or "unknown"),
        "task_counts": s4_closure_matrix.get("task_counts") if isinstance(s4_closure_matrix.get("task_counts"), dict) else {},
        "blocked_expected_tasks": list(s4_closure_matrix.get("blocked_expected_tasks") or []),
        "approval_required_tasks": list(s4_closure_matrix.get("approval_required_tasks") or []),
    }
