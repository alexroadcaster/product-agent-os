"""Canonical B1 wire contract for a read-only methodology recommendation."""

from __future__ import annotations

import re
from typing import Any

from product_agent_os.methodology_policy import METHODS


SCHEMA_VERSION = "paos_methodology_decision_v1"
SCOPE_FIELDS = "project_id task_id source_revision task_revision"
PACKET_FIELDS = "schema_version scope facts evidence decisions requirements plan execution acceptance authority"
FACT_FIELDS = "lifecycle surface scale coupling risk change_mode ui_scope stack check_count test_paths environment provenance"
ROW_FIELDS = "method owner applicability depth reason next_action evidence_refs"
REQUIREMENT_FIELDS = "owner depth changed_paths invariants non_goals criteria"
CRITERION_FIELDS = "id criterion scenario owner trace check evidence_refs"
PLAN_FIELDS = "next_step assumptions gaps blocking_question"
STEP_FIELDS = "kind action target evidence_refs"
STEP_KINDS = (
    "run_regression", "check_source", "run_characterization", "check_configuration",
    "review_evaluation", "clarify", "review_scope",
)
DIGEST = re.compile(r"[0-9a-f]{64}")


def _shape(value: Any, fields: str) -> bool:
    return isinstance(value, dict) and set(value) == set(fields.split())


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and "\0" not in value


def _texts(value: Any) -> bool:
    return isinstance(value, list) and all(_text(item) for item in value)


def _digest(value: Any) -> bool:
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None


def _path(value: Any) -> bool:
    return (
        _text(value) and not re.search(r"[\x00-\x1f:\\]", value)
        and all(part not in {"", ".", ".."} for part in value.split("/"))
    )


def _unchanged_scope(scope: Any, expected: dict[str, str] | None) -> bool:
    return (
        _shape(scope, SCOPE_FIELDS) and _text(scope["task_id"])
        and all(_digest(scope[key]) for key in ("project_id", "source_revision", "task_revision"))
        and (expected is None or scope == expected)
    )


def _evidence_ids(evidence: Any, scope: dict[str, str]) -> set[str]:
    ids: set[str] = set()
    if not isinstance(evidence, list):
        return ids
    for row in evidence:
        if not _shape(row, "id kind path revision") or not _text(row["id"]) or not _digest(row["revision"]):
            return set()
        ref, kind, path = row["id"], row["kind"], row["path"]
        if ref in ids:
            return set()
        if kind == "file":
            if not _path(path) or ref != f"file:{path}":
                return set()
        elif (kind, path, row["revision"]) not in (
            ("task", None, scope["task_revision"]), ("workspace", None, scope["source_revision"]),
        ) or ref != kind:
            return set()
        ids.add(ref)
    return ids


def _facts(value: Any) -> bool:
    if not _shape(value, FACT_FIELDS):
        return False
    return (
        value["lifecycle"] in ("greenfield_candidate", "legacy_candidate", "existing_code_observed")
        and value["surface"] in ("frontend", "backend", "native", "mixed", "docs", "unknown")
        and value["scale"] in ("small", "medium")
        and value["coupling"] in ("cross_surface", "multiple_frontend_areas", "local_scope", "unknown")
        and value["risk"] in ("low", "medium", "high", "unknown")
        and _text(value["change_mode"]) and type(value["ui_scope"]) is bool and _texts(value["stack"])
        and type(value["check_count"]) is int and value["check_count"] >= 0
        and _texts(value["test_paths"]) and all(_path(path) for path in value["test_paths"])
        and value["environment"] in ("not_observed", "caller_reported")
        and _shape(value["provenance"], "lifecycle_scale_stack surface_coupling intent_acceptance_risk checks")
        and all(_text(item) for item in value["provenance"].values())
    )


def _refs(value: Any, evidence: set[str]) -> bool:
    return _texts(value) and bool(value) and len(set(value)) == len(value) and set(value) <= evidence


def _decisions(value: Any, evidence: set[str]) -> bool:
    if not isinstance(value, list) or len(value) != len(METHODS):
        return False
    return all(
        _shape(row, ROW_FIELDS) and row["method"] == method
        and all(_text(row[field]) for field in ("owner", "reason", "next_action"))
        and row["applicability"] in ("applicable", "needs_context", "not_applicable")
        and row["depth"] in ("compact", "full", "none") and _refs(row["evidence_refs"], evidence)
        for row, method in zip(value, METHODS, strict=True)
    )


def _requirements(value: Any, evidence: set[str]) -> bool:
    if not _shape(value, REQUIREMENT_FIELDS):
        return False
    criteria = value["criteria"]
    return (
        value["owner"] == "requirements-author" and value["depth"] in ("compact", "full")
        and _texts(value["changed_paths"]) and all(_path(path) for path in value["changed_paths"])
        and _texts(value["invariants"]) and _texts(value["non_goals"])
        and isinstance(criteria, list) and bool(criteria)
        and all(
            _shape(row, CRITERION_FIELDS) and row["id"] == f"AC-{index}"
            and all(_text(row[field]) for field in ("criterion", "scenario", "owner"))
            and row["trace"] in ("proposed", "gap") and _refs(row["evidence_refs"], evidence)
            and row["check"] == ("plan.next_step" if row["trace"] == "proposed" else None)
            for index, row in enumerate(criteria, 1)
        )
    )


def _plan(value: Any, evidence: set[str]) -> bool:
    if not _shape(value, PLAN_FIELDS):
        return False
    step = value["next_step"]
    return (
        _texts(value["assumptions"]) and _texts(value["gaps"])
        and (_text(value["blocking_question"]) if value["gaps"] else value["blocking_question"] is None)
        and _shape(step, STEP_FIELDS) and step["kind"] in STEP_KINDS and _text(step["action"])
        and _refs(step["evidence_refs"], evidence)
        and (step["target"] is None if step["kind"] in ("clarify", "review_scope") else _text(step["target"]))
        and (
            f'file:{step["target"]}' in step["evidence_refs"]
            if step["kind"] in ("check_source", "check_configuration", "review_evaluation") else
            any(ref.startswith("file:") for ref in step["evidence_refs"])
            if step["kind"] in ("run_regression", "run_characterization") else True
        )
    )


def read_methodology_decision(
    value: Any, expected_scope: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Validate v1 shape and refs, optionally against independently supplied scope."""
    if not _shape(value, PACKET_FIELDS) or value["schema_version"] != SCHEMA_VERSION:
        raise ValueError("methodology_decision:unsupported_version_or_shape")
    if not _unchanged_scope(value["scope"], expected_scope):
        raise ValueError("methodology_decision:scope_mismatch")
    evidence = _evidence_ids(value["evidence"], value["scope"])
    if not {"task", "workspace"} <= evidence:
        raise ValueError("methodology_decision:invalid_evidence")
    if not (
        _facts(value["facts"]) and _decisions(value["decisions"], evidence)
        and _requirements(value["requirements"], evidence) and _plan(value["plan"], evidence)
        and value["execution"] == "not_started" and value["acceptance"] == "not_evaluated"
        and value["authority"] == "read_only"
    ):
        raise ValueError("methodology_decision:invalid_projection")
    return value
