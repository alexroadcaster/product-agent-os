"""Typed guided-question protocol helpers for Product-Agent OS."""

from __future__ import annotations

import hashlib
import re
from typing import Any

from product_agent_os.methodology_synthesis import dedupe_owner_questions


QUESTION_PRIORITIES = ["blocking", "recommended", "optional"]
QUESTION_CATEGORIES = ["scope", "product", "verification", "approval", "ownership", "risk", "release"]
QUESTION_ANSWER_TYPES = [
    "text",
    "single_choice",
    "single_choice_or_text",
    "multi_choice",
    "approval",
    "not_applicable_or_gap",
]
MAX_TOTAL_QUESTIONS = 8
MAX_FIRST_RESPONSE_BLOCKING = 1

_PRIORITY_RANK = {"blocking": 0, "recommended": 1, "optional": 2}
_METHODOLOGY_PRIORITY_MAP = {
    "P0_blocker": "blocking",
    "P1_high_risk": "recommended",
    "P2_recommended": "recommended",
    "P3_optional_maturity": "optional",
    "not_applicable": "optional",
}


def build_question_queue(
    *,
    owner_questions: list[Any] | None = None,
    unknowns: list[Any] | None = None,
    recommendation_groups: list[dict[str, Any]] | None = None,
    usage_mode: dict[str, Any] | str | None = None,
    runtime_gaps: list[Any] | None = None,
    agent_skill_metrics_loop: dict[str, Any] | None = None,
    runtime_status: str = "",
) -> dict[str, Any]:
    """Build a bounded typed question queue from existing audit/runtime packets."""

    candidates: list[dict[str, Any]] = []
    candidates.extend(_owner_question_candidates(owner_questions or []))
    candidates.extend(_unknown_candidates(unknowns or []))
    candidates.extend(_recommendation_group_candidates(recommendation_groups or []))
    candidates.extend(_runtime_gap_candidates(runtime_gaps or []))
    candidates.extend(_agent_skill_metrics_loop_candidates(agent_skill_metrics_loop))
    candidates.extend(_usage_mode_candidates(usage_mode))

    questions = _dedupe_questions(candidates)
    questions = sorted(questions, key=_sort_key)
    questions = _limit_first_response_blocking(questions)
    questions = questions[:MAX_TOTAL_QUESTIONS]
    questions = [_with_sequence(question, index) for index, question in enumerate(questions, start=1)]
    blocking = [question for question in questions if question["priority"] == "blocking"]

    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "runtime_status": runtime_status,
        "policy": {
            "max_total_questions": MAX_TOTAL_QUESTIONS,
            "max_blocking_questions_in_first_response": MAX_FIRST_RESPONSE_BLOCKING,
            "supported_priorities": list(QUESTION_PRIORITIES),
            "supported_categories": list(QUESTION_CATEGORIES),
            "supported_answer_types": list(QUESTION_ANSWER_TYPES),
        },
        "questions": questions,
        "next_blocking_question": blocking[0] if blocking else None,
        "summary": {
            "total": len(questions),
            "blocking": len(blocking),
            "recommended": sum(1 for question in questions if question["priority"] == "recommended"),
            "optional": sum(1 for question in questions if question["priority"] == "optional"),
            "remaining": max(0, len(questions) - len(blocking[:MAX_FIRST_RESPONSE_BLOCKING])),
        },
    }


def _owner_question_candidates(owner_questions: list[Any]) -> list[dict[str, Any]]:
    normalized = []
    raw_strings = [item for item in owner_questions if isinstance(item, str)]
    string_questions = dedupe_owner_questions([str(item) for item in raw_strings])
    for question in string_questions:
        category = _category_from_text(question)
        normalized.append(
            _question(
                text=question,
                priority="blocking",
                category=category,
                answer_type=_answer_type_for_category(category),
                source_kind="methodology_packet",
                source_key=_source_key_from_owner_text(question, category),
                block="questions_for_owner",
            )
        )
    for item in owner_questions:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text") or item.get("question") or "").strip()
        if not text:
            continue
        category = _valid_category(str(item.get("category") or _category_from_text(text)))
        normalized.append(
            _question(
                text=text,
                priority=_valid_priority(str(item.get("priority") or "blocking")),
                category=category,
                answer_type=_valid_answer_type(str(item.get("answer_type") or _answer_type_for_category(category))),
                source_kind=str(item.get("source_kind") or "methodology_packet"),
                source_key=str(item.get("source_key") or _source_key_from_owner_text(text, category)),
                block=str(item.get("block") or "questions_for_owner"),
                artifact=str(item.get("artifact") or ""),
                choices=list(item.get("choices") or []),
            )
        )
    return normalized


def _unknown_candidates(unknowns: list[Any]) -> list[dict[str, Any]]:
    candidates = []
    for item in unknowns:
        text = str(item.get("text") or item.get("question")) if isinstance(item, dict) else str(item)
        text = text.strip()
        if not text:
            continue
        category = _valid_category(str(item.get("category"))) if isinstance(item, dict) else _category_from_text(text)
        source_key = str(item.get("source_key")) if isinstance(item, dict) and item.get("source_key") else _slug(text)
        candidates.append(
            _question(
                text=f"Can the owner provide or accept a gap for: {text}?",
                priority=_valid_priority(str(item.get("priority"))) if isinstance(item, dict) else "recommended",
                category=category,
                answer_type="not_applicable_or_gap",
                source_kind="methodology_audit",
                source_key=source_key,
                block="unknowns",
            )
        )
    return candidates


def _recommendation_group_candidates(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = []
    for group in groups:
        artifact = str(group.get("artifact") or "").strip()
        if not artifact:
            continue
        category = _category_from_group(group)
        candidates.append(
            _question(
                text=_recommendation_question_text(group, category, artifact),
                priority=_METHODOLOGY_PRIORITY_MAP.get(str(group.get("priority")), "recommended"),
                category=category,
                answer_type=_answer_type_for_category(category),
                source_kind="methodology_synthesis",
                source_key=",".join(str(gate) for gate in group.get("gates", []) if gate) or artifact,
                block="recommendation_groups",
                artifact=artifact,
                owner_domain=str(group.get("owner_domain") or ""),
            )
        )
    return candidates


def _runtime_gap_candidates(runtime_gaps: list[Any]) -> list[dict[str, Any]]:
    candidates = []
    for item in runtime_gaps:
        text = str(item.get("question") or item.get("text")) if isinstance(item, dict) else str(item)
        text = text.strip()
        if not text:
            continue
        category = _valid_category(str(item.get("category"))) if isinstance(item, dict) else _category_from_text(text)
        source_key = str(item.get("source_key")) if isinstance(item, dict) and item.get("source_key") else _slug(text)
        candidates.append(
            _question(
                text=text,
                priority=_valid_priority(str(item.get("priority"))) if isinstance(item, dict) else "recommended",
                category=category,
                answer_type=(
                    _valid_answer_type(str(item.get("answer_type")))
                    if isinstance(item, dict)
                    else _answer_type_for_category(category)
                ),
                source_kind="codex_runtime_runner",
                source_key=source_key,
                block="runtime_gaps",
            )
        )
    return candidates


def _usage_mode_candidates(usage_mode: dict[str, Any] | str | None) -> list[dict[str, Any]]:
    if usage_mode is None:
        return []
    primary = str(usage_mode.get("primary") if isinstance(usage_mode, dict) else usage_mode)
    if primary in {"", "None", "inspection_only", "docs_only"}:
        return []
    if primary == "greenfield_idea":
        return [
            _question(
                text="What is the smallest accepted product outcome for the first implementation slice?",
                priority="recommended",
                category="product",
                answer_type="text",
                source_kind="workspace_discovery",
                source_key="greenfield_idea_product_outcome",
                block="usage_mode",
            )
        ]
    return []


def _agent_skill_metrics_loop_candidates(packet: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(packet, dict):
        return []
    missing = packet.get("missing") if isinstance(packet.get("missing"), list) else []
    if not missing and str(packet.get("status", "")) in {"", "not_applicable", "ready"}:
        return []
    requested = {str(item).strip().lower().replace("_", " ") for item in missing if str(item).strip()}
    if not requested:
        requested = {
            "owner",
            "evidence source",
            "trace source",
            "cadence",
            "approval",
            "rollback",
            "accepted gap",
        }
    question_specs = [
        (
            "owner",
            "Who owns the agent_skill_metrics_loop scorecard ledger and owner review?",
            "blocking",
            "ownership",
            "text",
            "metrics_loop_owner",
        ),
        (
            "evidence source",
            "Which evidence source artifact provides current metrics evidence for the agent_skill_metrics_loop?",
            "recommended",
            "verification",
            "text",
            "metrics_loop_evidence_source",
        ),
        (
            "trace source",
            "Which trace source is approved for metrics-loop scoring and redaction?",
            "recommended",
            "verification",
            "text",
            "metrics_loop_trace_source",
        ),
        (
            "cadence",
            "What cadence is accepted for the metrics loop, or what explicit gap applies?",
            "recommended",
            "verification",
            "not_applicable_or_gap",
            "metrics_loop_cadence",
        ),
        (
            "approval",
            "Who owns approval for any metrics-loop modernization candidate before changes or automation?",
            "recommended",
            "approval",
            "approval",
            "metrics_loop_approval",
        ),
        (
            "rollback",
            "What rollback evidence is required before a metrics-loop update candidate can be reviewed?",
            "recommended",
            "risk",
            "text",
            "metrics_loop_rollback",
        ),
        (
            "accepted gap",
            "Is there an accepted gap for missing metrics-loop evidence, with owner and residual risk?",
            "optional",
            "risk",
            "not_applicable_or_gap",
            "metrics_loop_accepted_gap",
        ),
    ]
    candidates = []
    for key, text, priority, category, answer_type, source_key in question_specs:
        if key not in requested and key != "accepted gap":
            continue
        candidates.append(
            _question(
                text=text,
                priority=priority,
                category=category,
                answer_type=answer_type,
                source_kind="agent_skill_metrics_loop",
                source_key=source_key,
                block="metrics_loop_gaps",
                artifact="agent-skill-scorecard-ledger.md",
                owner_domain="codex_agentic_workflow",
            )
        )
    return candidates


def _question(
    *,
    text: str,
    priority: str,
    category: str,
    answer_type: str,
    source_kind: str,
    source_key: str,
    block: str,
    artifact: str = "",
    owner_domain: str = "",
    choices: list[Any] | None = None,
) -> dict[str, Any]:
    category = _valid_category(category)
    priority = _valid_priority(priority)
    answer_type = _valid_answer_type(answer_type)
    source = {
        "kind": source_kind or "unknown",
        "key": source_key or category,
        "block": block or "unknown",
    }
    if artifact:
        source["artifact"] = artifact
    question = {
        "id": _stable_question_id(source, category),
        "text": text,
        "priority": priority,
        "category": category,
        "answer_type": answer_type,
        "artifact": artifact,
        "owner_domain": owner_domain,
        "source": source,
    }
    if choices:
        question["choices"] = [str(choice) for choice in choices if str(choice).strip()]
    return question


def _stable_question_id(source: dict[str, str], category: str) -> str:
    parts = [
        source.get("kind", ""),
        source.get("key", ""),
        source.get("block", ""),
        source.get("artifact", ""),
        category,
    ]
    canonical = "|".join(_slug(part) for part in parts if part)
    digest = hashlib.sha1(canonical.encode("utf-8")).hexdigest()[:10]
    prefix = _slug(category) or "question"
    return f"q_{prefix}_{digest}"


def _dedupe_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result = []
    for question in questions:
        question_id = question["id"]
        if question_id in seen:
            continue
        seen.add(question_id)
        result.append(question)
    return result


def _limit_first_response_blocking(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocking_seen = 0
    adjusted = []
    for question in questions:
        item = dict(question)
        if item["priority"] == "blocking":
            blocking_seen += 1
            if blocking_seen > MAX_FIRST_RESPONSE_BLOCKING:
                item["priority"] = "recommended"
        adjusted.append(item)
    return sorted(adjusted, key=_sort_key)


def _with_sequence(question: dict[str, Any], index: int) -> dict[str, Any]:
    item = dict(question)
    item["sequence"] = index
    return item


def _sort_key(question: dict[str, Any]) -> tuple[int, str, str, str]:
    return (
        _PRIORITY_RANK.get(str(question.get("priority")), 99),
        str(question.get("category", "")),
        str(question.get("artifact", "")),
        str(question.get("id", "")),
    )


def _category_from_group(group: dict[str, Any]) -> str:
    artifact = str(group.get("artifact") or "").lower()
    gates = " ".join(str(gate) for gate in group.get("gates", [])).lower()
    evidence = " ".join(str(item) for item in group.get("evidence_required", [])).lower()
    text = f"{artifact} {gates} {evidence}"
    return _category_from_text(text)


def _category_from_text(text: str) -> str:
    normalized = text.lower()
    if any(token in normalized for token in ["verification", "test", "evidence", "command"]):
        return "verification"
    if any(token in normalized for token in ["approval", "permission", "external write"]):
        return "approval"
    if any(token in normalized for token in ["owner", "owns", "ownership"]):
        return "ownership"
    if any(token in normalized for token in ["release", "deploy", "publish", "rollback"]):
        return "release"
    if any(token in normalized for token in ["risk", "security", "threat", "privacy"]):
        return "risk"
    if any(token in normalized for token in ["product", "outcome", "metric", "user"]):
        return "product"
    return "scope"


def _answer_type_for_category(category: str) -> str:
    if category == "approval":
        return "approval"
    if category == "scope":
        return "single_choice_or_text"
    return "text"


def _source_key_from_owner_text(text: str, category: str) -> str:
    normalized = text.lower()
    if "verification" in normalized or "command" in normalized:
        return "verification_command"
    if "highest-priority" in normalized or "highest priority" in normalized or "owner" in normalized:
        return "methodology_gate_owner"
    return f"owner_{category}"


def _recommendation_question_text(group: dict[str, Any], category: str, artifact: str) -> str:
    if category == "approval":
        return f"Who can approve or explicitly reject the gap for {artifact}?"
    if category == "release":
        return f"What release evidence or accepted gap should be recorded for {artifact}?"
    if category == "risk":
        return f"Who owns the risk evidence or accepted gap for {artifact}?"
    return f"What owner-reviewed evidence or accepted gap should be recorded for {artifact}?"


def _valid_priority(value: str) -> str:
    return value if value in QUESTION_PRIORITIES else "recommended"


def _valid_category(value: str) -> str:
    return value if value in QUESTION_CATEGORIES else "scope"


def _valid_answer_type(value: str) -> str:
    return value if value in QUESTION_ANSWER_TYPES else "text"


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return normalized.strip("-")
