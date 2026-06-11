from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


BATCH39_ROLLUP_SCHEMA_VERSION = "batch39_rollup_v1"
TASK_STATUSES = ("passed", "failed", "blocked", "planned", "in_progress", "partial_pass_m04")


def build_batch39_rollup(
    *,
    test_id: str,
    attempt_id: str,
    task_rows: list[dict[str, Any]],
    generated_at: str | None = None,
) -> dict[str, Any]:
    counts = {status: 0 for status in TASK_STATUSES}
    total_attempts = 0
    rows = []
    blockers: list[str] = []
    for row in task_rows:
        status = str(row.get("status", "planned"))
        if status not in counts:
            status = "blocked"
        attempts = _int(row.get("attempts"))
        total_attempts += attempts
        test_ref = str(row.get("test_id", "")).strip()
        evidence_refs = [_safe_ref(str(ref)) for ref in row.get("evidence_refs", []) if str(ref).strip()]
        counts[status] += 1
        if status in {"failed", "blocked"}:
            blockers.append(test_ref)
        rows.append({"test_id": test_ref, "status": status, "attempts": attempts, "evidence_refs": evidence_refs})
    rollup = {
        "schema_version": BATCH39_ROLLUP_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "counts": counts,
        "total_tasks": len(rows),
        "total_attempts": total_attempts,
        "blockers": blockers,
        "task_rows": rows,
        "generated_view_policy": "orientation_only_not_proof",
        "source_policy": "generated view is not proof",
        "safe_next_action": "resolve_blockers" if blockers else "continue_pending_tests" if counts["planned"] or counts["in_progress"] else "run_final_verification",
    }
    rollup["rollup_digest"] = content_digest(canonical_json(rollup))
    return rollup


def validate_batch39_rollup(rollup: dict[str, Any]) -> list[str]:
    if not isinstance(rollup, dict):
        return ["batch39 rollup must be an object"]
    errors: list[str] = []
    if rollup.get("schema_version") != BATCH39_ROLLUP_SCHEMA_VERSION:
        errors.append(f"schema_version must be {BATCH39_ROLLUP_SCHEMA_VERSION}")
    if rollup.get("batch") != "B39":
        errors.append("batch must be B39")
    if rollup.get("generated_view_policy") != "orientation_only_not_proof":
        errors.append("generated_view_policy must be orientation_only_not_proof")
    if rollup.get("source_policy") != "generated view is not proof":
        errors.append("source_policy must mark generated view as not proof")
    if not str(rollup.get("rollup_digest", "")).startswith("sha256:"):
        errors.append("rollup_digest must be a sha256 digest")
    counts = rollup.get("counts")
    rows = rollup.get("task_rows")
    if not isinstance(counts, dict):
        errors.append("counts must be an object")
        counts = {}
    if not isinstance(rows, list):
        errors.append("task_rows must be list")
        rows = []
    if isinstance(rollup.get("total_tasks"), int) and rollup.get("total_tasks") != len(rows):
        errors.append("total_tasks must match task_rows length")
    for status in TASK_STATUSES:
        if not isinstance(counts.get(status), int):
            errors.append(f"counts.{status} must be integer")
    return errors


def _int(value: Any) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _safe_ref(value: str) -> str:
    normalized = value.replace("\\", "/")
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] == "/":
        return "[REDACTED_LOCAL_PATH]"
    return normalized


__all__ = [
    "BATCH39_ROLLUP_SCHEMA_VERSION",
    "build_batch39_rollup",
    "validate_batch39_rollup",
]
