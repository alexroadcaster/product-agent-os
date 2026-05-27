"""Answer ledger helpers for Product-Agent OS guided questions."""

from __future__ import annotations

import json
import re
from datetime import date
from typing import Any

from codex_runtime_runner.redaction import redact_text, validate_redaction


PRIVATE_DATA_STATUSES = ["synthetic_or_none", "redacted", "not_applicable", "raw_private_customer_data"]
BLOCKED_PRIVATE_DATA_STATUSES = {"raw_private_customer_data"}
DEFAULT_MAX_ANSWER_AGE_DAYS = 30
MALICIOUS_INSTRUCTION_PATTERN = re.compile(
    r"(?i)(ignore previous instructions|write outside workspace|exfiltrate|disable safety|bypass approval)"
)


def build_answer_ledger(
    question_queue: dict[str, Any],
    answers: dict[str, Any],
    *,
    as_of_date: str | date,
    max_answer_age_days: int = DEFAULT_MAX_ANSWER_AGE_DAYS,
) -> dict[str, Any]:
    """Build a staged-only answer ledger from typed question packets and owner answers."""

    today = _parse_date(as_of_date)
    entries = []
    for question in question_queue.get("questions", []):
        question_id = str(question.get("id", ""))
        answer_record = answers.get(question_id)
        if answer_record is None:
            entries.append(_unanswered_entry(question))
            continue
        entries.append(_answer_entry(question, answer_record, today, max_answer_age_days))

    artifact_updates = _artifact_updates(entries)
    return {
        "schema_version": 1,
        "write_policy": "staged_only",
        "as_of_date": today.isoformat(),
        "policy": {
            "max_answer_age_days": max_answer_age_days,
            "private_data_statuses": list(PRIVATE_DATA_STATUSES),
            "blocked_private_data_statuses": sorted(BLOCKED_PRIVATE_DATA_STATUSES),
            "malicious_instruction_guard": "enabled",
        },
        "entries": entries,
        "artifact_updates": artifact_updates,
        "summary": {
            "total": len(entries),
            "accepted": sum(1 for entry in entries if entry["status"] == "accepted"),
            "blocked": sum(1 for entry in entries if entry["status"] == "blocked"),
            "unanswered": sum(1 for entry in entries if entry["status"] == "unanswered"),
        },
    }


def validate_answer_ledger(ledger: dict[str, Any]) -> list[str]:
    """Return stable validation errors for a rendered or in-memory answer ledger."""

    errors: list[str] = []
    if not isinstance(ledger, dict):
        return ["question_ledger:invalid"]
    if ledger.get("schema_version") != 1:
        errors.append("question_ledger.schema_version:unsupported")
    if ledger.get("write_policy") != "staged_only":
        errors.append("question_ledger.write_policy:must_be_staged_only")
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        errors.append("question_ledger.entries:required")
        entries = []
    if any(entry.get("status") == "blocked" for entry in entries if isinstance(entry, dict)):
        errors.append("question_ledger:blocked_entries_present")
    rendered = json.dumps(ledger, sort_keys=True)
    errors.extend(validate_redaction(rendered))
    return sorted(set(errors))


def render_answer_ledger_json(ledger: dict[str, Any]) -> str:
    """Render a deterministic JSON answer ledger artifact."""

    return json.dumps(ledger, indent=2, sort_keys=True)


def render_answer_ledger_markdown(ledger: dict[str, Any]) -> str:
    """Render a compact Markdown proposal artifact for staged review."""

    lines = [
        "# Question Ledger",
        "",
        "Source status: `local-generated`",
        "",
        f"Write policy: `{ledger.get('write_policy', 'staged_only')}`",
        f"As of date: `{ledger.get('as_of_date', '')}`",
        "",
        "## Summary",
        "",
        f"- Total: {ledger.get('summary', {}).get('total', 0)}",
        f"- Accepted: {ledger.get('summary', {}).get('accepted', 0)}",
        f"- Blocked: {ledger.get('summary', {}).get('blocked', 0)}",
        f"- Unanswered: {ledger.get('summary', {}).get('unanswered', 0)}",
        "",
        "## Entries",
        "",
    ]
    for entry in ledger.get("entries", []):
        lines.extend(
            [
                f"### {entry.get('question_id', '')}",
                "",
                f"- Status: `{entry.get('status', '')}`",
                f"- Category: `{entry.get('category', '')}`",
                f"- Target artifact: `{entry.get('target_artifact', '')}`",
                f"- Artifact action: `{entry.get('artifact_action', '')}`",
                f"- Private data status: `{entry.get('private_data_status', '')}`",
                f"- Answered at: `{entry.get('answered_at', '')}`",
                f"- Answer: {_markdown_inline(entry.get('answer', ''))}",
                f"- Validation errors: {_render_list(entry.get('validation_errors', []))}",
                "",
            ]
        )
    lines.extend(
        [
            "## Artifact Updates",
            "",
        ]
    )
    for update in ledger.get("artifact_updates", []):
        lines.append(
            f"- `{update.get('artifact', '')}` from {_render_list(update.get('question_ids', []))}: "
            f"{_render_list(update.get('actions', []))}"
        )
    lines.extend(
        [
            "",
            "Do not treat this ledger as approval by itself. Apply answers only through staged artifacts and existing approval flow.",
            "Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _answer_entry(
    question: dict[str, Any],
    answer_record: Any,
    as_of_date: date,
    max_answer_age_days: int,
) -> dict[str, Any]:
    record = answer_record if isinstance(answer_record, dict) else {"answer": str(answer_record)}
    answer_text = str(record.get("answer", ""))
    redacted_answer, redaction = redact_text(answer_text)
    answered_at = str(record.get("answered_at", ""))
    private_data_status = str(record.get("private_data_status", "not_applicable"))
    validation_errors = _answer_errors(
        answer_text=answer_text,
        redaction=redaction,
        answered_at=answered_at,
        as_of_date=as_of_date,
        max_answer_age_days=max_answer_age_days,
        private_data_status=private_data_status,
    )
    return {
        "question_id": str(question.get("id", "")),
        "question_text": str(question.get("text", "")),
        "category": str(question.get("category", "")),
        "answer_type": str(question.get("answer_type", "")),
        "target_artifact": _target_artifact(question),
        "artifact_action": str(record.get("artifact_action", "record_answer")),
        "answer": redacted_answer,
        "answered_at": answered_at,
        "private_data_status": private_data_status,
        "redaction": redaction,
        "validation_errors": validation_errors,
        "status": "blocked" if validation_errors else "accepted",
    }


def _unanswered_entry(question: dict[str, Any]) -> dict[str, Any]:
    return {
        "question_id": str(question.get("id", "")),
        "question_text": str(question.get("text", "")),
        "category": str(question.get("category", "")),
        "answer_type": str(question.get("answer_type", "")),
        "target_artifact": _target_artifact(question),
        "artifact_action": "none",
        "answer": "",
        "answered_at": "",
        "private_data_status": "not_applicable",
        "redaction": {"count": 0, "categories": []},
        "validation_errors": [],
        "status": "unanswered",
    }


def _answer_errors(
    *,
    answer_text: str,
    redaction: dict[str, Any],
    answered_at: str,
    as_of_date: date,
    max_answer_age_days: int,
    private_data_status: str,
) -> list[str]:
    errors: list[str] = []
    categories = set(str(category) for category in redaction.get("categories", []))
    if "secret" in categories:
        errors.append("answer:secret_like_value")
    if private_data_status in BLOCKED_PRIVATE_DATA_STATUSES:
        errors.append("answer:private_data_status_blocked")
    if private_data_status not in PRIVATE_DATA_STATUSES:
        errors.append("answer:private_data_status_invalid")
    answer_date = _parse_optional_date(answered_at)
    if answer_date is None:
        errors.append("answer:answered_at_invalid")
    elif (as_of_date - answer_date).days > max_answer_age_days:
        errors.append("answer:stale")
    if MALICIOUS_INSTRUCTION_PATTERN.search(answer_text):
        errors.append("answer:malicious_instruction")
    return sorted(set(errors))


def _artifact_updates(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    updates: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if entry.get("status") != "accepted":
            continue
        artifact = str(entry.get("target_artifact", ""))
        if not artifact:
            continue
        update = updates.setdefault(artifact, {"artifact": artifact, "question_ids": [], "actions": []})
        _append_unique(update["question_ids"], str(entry.get("question_id", "")))
        _append_unique(update["actions"], str(entry.get("artifact_action", "")))
    return [updates[key] for key in sorted(updates)]


def _target_artifact(question: dict[str, Any]) -> str:
    artifact = str(question.get("artifact") or "")
    if artifact:
        return artifact
    source = question.get("source", {})
    if isinstance(source, dict):
        return str(source.get("artifact") or "")
    return ""


def _parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _parse_optional_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _render_list(items: Any) -> str:
    if not items:
        return "`none`"
    if not isinstance(items, list):
        return f"`{_markdown_inline(str(items))}`"
    return ", ".join(f"`{_markdown_inline(str(item))}`" for item in items)


def _markdown_inline(value: Any) -> str:
    return str(value).replace("`", "'").replace("\r", " ").replace("\n", " ")
