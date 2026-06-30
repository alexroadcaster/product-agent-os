from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any


OWNER_FEEDBACK_LEDGER_SCHEMA_VERSION = "owner_feedback_ledger_v1"
FEEDBACK_IMPORT_CONTRACT_SCHEMA_VERSION = "codex_session_feedback_import_v1"
SATISFACTION_REPORT_SCHEMA_VERSION = "self_learning_satisfaction_report_v1"
PREFERENCE_MEMORY_SCHEMA_VERSION = "preference_memory_v1"
OWNER_FEEDBACK_LEDGER_RELATIVE_PATH = ".codex/product-agent-os/owner-feedback-ledger.jsonl"


_RAW_CONTENT_KEYS = {
    "raw_chat",
    "raw_chat_body",
    "raw_transcript",
    "transcript_body",
    "message_body",
    "private_source_body",
}
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def validate_owner_feedback_row(row: Any) -> list[str]:
    if not isinstance(row, dict):
        return ["row:not_object"]
    errors: list[str] = []
    required = [
        "schema_version",
        "feedback_id",
        "session_ref",
        "task_ref",
        "explicit_rating",
        "revision_requested",
        "revision_accepted",
        "usefulness",
        "user_effort",
        "outcome",
        "evidence_links",
        "redaction_status",
        "owner_review",
        "privacy",
    ]
    for field in required:
        if field not in row:
            errors.append(f"{field}:required")
    if row.get("schema_version") != OWNER_FEEDBACK_LEDGER_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    if row.get("redaction_status") != "redacted":
        errors.append("redaction_status:must_be_redacted")
    if not isinstance(row.get("session_ref"), dict):
        errors.append("session_ref:must_be_redacted_object")
    else:
        session_ref = row["session_ref"]
        if session_ref.get("raw_session_id_included") is not False:
            errors.append("session_ref.raw_session_id_included:must_be_false")
        if not isinstance(session_ref.get("session_id_hash"), str) or not session_ref.get("session_id_hash"):
            errors.append("session_ref.session_id_hash:required")
    privacy = row.get("privacy")
    if not isinstance(privacy, dict):
        errors.append("privacy:required")
    else:
        if privacy.get("consent") != "owner_provided_redacted_summary":
            errors.append("privacy.consent:missing_owner_redacted_summary_consent")
        if privacy.get("raw_chat_body_stored") is not False:
            errors.append("privacy.raw_chat_body_stored:must_be_false")
        if privacy.get("contains_pii") is True:
            errors.append("privacy.contains_pii:must_be_false")
    if row.get("explicit_rating") not in {None, "satisfied", "neutral", "dissatisfied"}:
        errors.append("explicit_rating:invalid")
    if row.get("usefulness") not in {None, "high", "medium", "low", "unknown"}:
        errors.append("usefulness:invalid")
    if row.get("user_effort") not in {None, "low", "medium", "high", "very_high", "unknown"}:
        errors.append("user_effort:invalid")
    if row.get("outcome") not in {None, "accepted", "partial", "reopened", "rejected", "needs_rework", "unknown"}:
        errors.append("outcome:invalid")
    if _contains_raw_private_content(row):
        errors.append("raw_private_content:blocked")
    return errors


def build_feedback_import_contract(*, scope_packet: dict[str, Any], summaries: list[dict[str, Any]]) -> dict[str, Any]:
    scope_ref = scope_packet.get("workspace_ref") if isinstance(scope_packet.get("workspace_ref"), dict) else {}
    expected_scope_id = scope_ref.get("path_hash")
    imported: list[str] = []
    skipped: list[dict[str, str]] = []
    for summary in summaries:
        summary_id = str(summary.get("summary_id") or "unknown")
        reason = _import_skip_reason(
            scope_packet=scope_packet,
            summary=summary,
            expected_scope_id=expected_scope_id,
        )
        if reason:
            skipped.append({"summary_id": summary_id, "reason": reason})
        else:
            imported.append(summary_id)
    return {
        "schema_version": FEEDBACK_IMPORT_CONTRACT_SCHEMA_VERSION,
        "product_agent_os_scope": {
            "eligible": bool(scope_packet.get("eligible")),
            "project_scope_id": expected_scope_id,
        },
        "raw_session_ingestion": "not_performed",
        "hidden_app_telemetry": "not_performed",
        "provider_calls": "not_performed",
        "imported_summary_ids": imported,
        "skipped_summaries": skipped,
        "consent_required": "owner_provided_redacted_summary",
        "redaction_required": "redacted",
    }


def evaluate_satisfaction(rows: list[dict[str, Any]]) -> dict[str, Any]:
    labels = [_label_feedback(row) for row in rows]
    human_label_count = sum(1 for item in labels if item["source_type"] == "owner_label")
    dissatisfied = sum(1 for item in labels if item["label"] == "dissatisfied")
    low_confidence = any(item["source_type"] == "pseudo_label" and item["confidence"] == "low" for item in labels)
    return {
        "schema_version": SATISFACTION_REPORT_SCHEMA_VERSION,
        "denominator": len(rows),
        "human_label_count": human_label_count,
        "human_label_coverage": _ratio(human_label_count, len(rows)),
        "dissatisfied_count": dissatisfied,
        "labels": labels,
        "promotion_signal": "blocked_low_confidence" if low_confidence else "owner_label_supported",
        "unsupported_claims": [
            "private emotions inferred",
            "real user satisfaction known without owner feedback",
            "pseudo-labels override explicit owner labels",
        ],
    }


def build_preference_memory(
    rows: list[dict[str, Any]],
    *,
    generated_at: str | None = None,
    disabled_categories: set[str] | None = None,
) -> dict[str, Any]:
    disabled = disabled_categories or set()
    grouped: dict[str, dict[str, Any]] = {}
    feedback_ids_by_category: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        feedback_id = str(row.get("feedback_id") or "unknown")
        for signal in row.get("preference_signals", []):
            if not isinstance(signal, dict):
                continue
            category = str(signal.get("category") or "").strip()
            summary = str(signal.get("summary") or "").strip()
            if not category or not summary or category in disabled:
                continue
            if _contains_raw_private_content(signal):
                continue
            grouped[category] = {
                "category": category,
                "summary": summary,
                "scope": signal.get("scope") or "product_agent_os",
                "source_feedback_ids": [],
                "status": "active",
                "owner_editable": True,
            }
            feedback_ids_by_category[category].append(feedback_id)
    recent = []
    for category, item in sorted(grouped.items()):
        item["source_feedback_ids"] = sorted(set(feedback_ids_by_category[category]))
        recent.append(item)
    return {
        "schema_version": PREFERENCE_MEMORY_SCHEMA_VERSION,
        "generated_at": generated_at or _now(),
        "owner_editable": True,
        "raw_chat_stored": False,
        "source_policy": "feedback_ids_only_no_raw_chat",
        "preferences": {
            "long_term": [],
            "recent": recent,
            "disabled": sorted(disabled),
        },
        "unsupported_claims": [
            "preference memory is source truth",
            "preference memory overrides system or project instructions",
            "raw chat is retained",
        ],
    }


def validate_preference_memory(memory: Any) -> list[str]:
    if not isinstance(memory, dict):
        return ["memory:not_object"]
    errors: list[str] = []
    if memory.get("schema_version") != PREFERENCE_MEMORY_SCHEMA_VERSION:
        errors.append("schema_version:invalid")
    if memory.get("owner_editable") is not True:
        errors.append("owner_editable:must_be_true")
    if memory.get("raw_chat_stored") is not False:
        errors.append("raw_chat_stored:must_be_false")
    if _contains_raw_private_content(memory):
        errors.append("raw_private_content:blocked")
    preferences = memory.get("preferences")
    if not isinstance(preferences, dict):
        errors.append("preferences:required")
    else:
        for section in ("long_term", "recent", "disabled"):
            if section not in preferences:
                errors.append(f"preferences.{section}:required")
    return errors


def load_owner_feedback_ledger(
    workspace: str | Path,
    *,
    ledger_path: str | Path | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    path = Path(ledger_path) if ledger_path is not None else Path(workspace) / OWNER_FEEDBACK_LEDGER_RELATIVE_PATH
    if not path.exists():
        return [], []
    rows: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except ValueError:
            rejected.append({"line": index, "errors": ["json:invalid"]})
            continue
        errors = validate_owner_feedback_row(payload)
        if errors:
            rejected.append({"line": index, "feedback_id": payload.get("feedback_id"), "errors": errors})
        else:
            rows.append(payload)
    return rows, rejected


def summarize_owner_feedback_ledger(
    workspace: str | Path,
    *,
    ledger_path: str | Path | None = None,
) -> dict[str, Any]:
    rows, rejected = load_owner_feedback_ledger(workspace, ledger_path=ledger_path)
    if not rows and not rejected:
        return {
            "status": "no_owner_feedback_ledger",
            "ledger_source": _ledger_source(ledger_path),
            "owner_feedback_rows": 0,
            "rejected_rows": 0,
            "raw_session_ingestion": "not_performed",
            "satisfaction_report": evaluate_satisfaction([]),
            "preference_memory": build_preference_memory([]),
        }
    return {
        "status": "available",
        "ledger_source": _ledger_source(ledger_path),
        "owner_feedback_rows": len(rows),
        "rejected_rows": len(rejected),
        "raw_session_ingestion": "not_performed",
        "hidden_app_telemetry": "not_performed",
        "provider_calls": "not_performed",
        "satisfaction_report": evaluate_satisfaction(rows),
        "preference_memory": build_preference_memory(rows),
        "rejected_row_errors": rejected,
    }


def _import_skip_reason(
    *,
    scope_packet: dict[str, Any],
    summary: dict[str, Any],
    expected_scope_id: str | None,
) -> str | None:
    if not scope_packet.get("eligible"):
        return "product_agent_os_scope_not_eligible"
    if summary.get("product_agent_os_detected") is not True:
        return "missing_product_agent_os_scope"
    scope_values = {summary.get("project_scope_id"), summary.get("workspace_path_hash")}
    if expected_scope_id and expected_scope_id not in scope_values:
        return "out_of_scope"
    if summary.get("evidence_consent") != "owner_provided_redacted_summary":
        return "missing_consent"
    if summary.get("redaction_status") != "redacted":
        return "unredacted"
    if summary.get("contains_raw_transcript") is True:
        return "raw_transcript_blocked"
    return None


def _label_feedback(row: dict[str, Any]) -> dict[str, Any]:
    feedback_id = str(row.get("feedback_id") or "unknown")
    explicit = row.get("explicit_rating")
    if explicit in {"satisfied", "neutral", "dissatisfied"}:
        return {
            "feedback_id": feedback_id,
            "label": explicit,
            "source_type": "owner_label",
            "confidence": "high",
            "signals": ["explicit_rating"],
        }
    signals = []
    if row.get("revision_requested") is True:
        signals.append("revision_requested")
    if row.get("revision_accepted") is False:
        signals.append("revision_not_accepted")
    if row.get("usefulness") == "low":
        signals.append("low_usefulness")
    if row.get("user_effort") in {"high", "very_high"}:
        signals.append("high_user_effort")
    if row.get("outcome") in {"reopened", "rejected", "needs_rework"}:
        signals.append("negative_outcome")
    label = "dissatisfied" if len(signals) >= 2 else "unknown"
    return {
        "feedback_id": feedback_id,
        "label": label,
        "source_type": "pseudo_label",
        "confidence": "low",
        "signals": signals,
    }


def _contains_raw_private_content(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in _RAW_CONTENT_KEYS:
                return True
            if _contains_raw_private_content(item):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_raw_private_content(item) for item in value)
    if isinstance(value, str):
        return _looks_like_private_path(value) or bool(_EMAIL_RE.search(value))
    return False


def _looks_like_private_path(value: str) -> bool:
    if PureWindowsPath(value).is_absolute():
        return True
    normalized = value.replace("\\", "/")
    return normalized.startswith("/Users/") or normalized.startswith("/home/")


def _ratio(part: int, whole: int) -> float:
    if whole <= 0:
        return 0.0
    return round(part / whole, 4)


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ledger_source(ledger_path: str | Path | None) -> str:
    return "explicit_redacted_override" if ledger_path is not None else OWNER_FEEDBACK_LEDGER_RELATIVE_PATH
