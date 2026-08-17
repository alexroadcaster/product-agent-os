from __future__ import annotations

from copy import deepcopy
from typing import Any


METRICS_SCHEMA_VERSION = "product_agent_os_code_quality_metrics_v1"
EVIDENCE_STATUSES = {"passed", "failed", "missing", "not_applicable"}
REQUIRED_GATES = ("acceptance", "regression", "seeded_faults", "reviewer", "dependency")
CONDITIONAL_GATES = ("performance", "cost_latency")


class MetricsContractError(ValueError):
    """Raised when metric evidence is malformed rather than merely missing."""


def evaluate_code_quality_metrics(evidence: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic promotion decision from current technical evidence.

    Model-emitted scores are copied into diagnostics and never participate in the
    decision. Missing required evidence is a blocker, not a numeric zero.
    """
    if not isinstance(evidence, dict):
        raise MetricsContractError("evidence:expected_object")

    blockers: list[str] = []
    normalized: dict[str, dict[str, Any]] = {}
    for gate in REQUIRED_GATES:
        item = _required_gate(evidence, gate)
        status = _status(item, gate)
        if status == "not_applicable":
            raise MetricsContractError(f"{gate}.status:not_applicable_for_required_gate")
        normalized[gate] = {"status": status}
        if gate == "reviewer":
            verdict = item.get("verdict")
            if verdict not in {"approve", "changes_requested", "blocked", "missing"}:
                raise MetricsContractError(f"{gate}.verdict:invalid")
            normalized[gate]["verdict"] = verdict
            if verdict != "approve":
                blockers.append(f"reviewer:{verdict}")
        if status != "passed":
            blockers.append(f"{gate}:{status}")

    applicability: dict[str, bool] = {}
    for gate in CONDITIONAL_GATES:
        item = _required_gate(evidence, gate)
        applicable = item.get("applicable")
        if not isinstance(applicable, bool):
            raise MetricsContractError(f"{gate}.applicable:expected_boolean")
        status = _status(item, gate)
        if applicable and status != "passed":
            blockers.append(f"{gate}:{status}")
        if not applicable and status != "not_applicable":
            raise MetricsContractError(f"{gate}.status:must_be_not_applicable")
        normalized[gate] = {"applicable": applicable, "status": status}
        applicability[gate] = applicable

    patch = _patch_metrics(evidence.get("patch"))
    warnings: list[str] = []
    if patch["changed_lines"] > 500:
        warnings.append("patch_size_anomaly")
    if patch["changed_lines"] and patch["test_changed_lines"] > patch["changed_lines"] * 2:
        warnings.append("test_churn_anomaly")
    if patch["dependency_delta_count"] > 0 and normalized["dependency"]["status"] != "passed":
        blockers.append("dependency_delta_without_passed_evidence")

    unique_blockers = tuple(dict.fromkeys(blockers))
    return {
        "schema_version": METRICS_SCHEMA_VERSION,
        "promotion_allowed": not unique_blockers,
        "decision": "promotion_evidence_ready" if not unique_blockers else "blocked_by_evidence",
        "blockers": list(unique_blockers),
        "signals": normalized,
        "applicability": applicability,
        "patch": patch,
        "warnings": warnings,
        "diagnostics": {
            "model_self_scores": deepcopy(evidence.get("diagnostic_self_scores")),
            "self_scores_affect_promotion": False,
        },
    }


def _required_gate(evidence: dict[str, Any], name: str) -> dict[str, Any]:
    value = evidence.get(name)
    if value is None:
        return {"status": "missing"}
    if not isinstance(value, dict):
        raise MetricsContractError(f"{name}:expected_object")
    return value


def _status(item: dict[str, Any], path: str) -> str:
    value = item.get("status", "missing")
    if value not in EVIDENCE_STATUSES:
        raise MetricsContractError(f"{path}.status:invalid")
    return value


def _patch_metrics(value: Any) -> dict[str, int]:
    if not isinstance(value, dict):
        raise MetricsContractError("patch:expected_object")
    result: dict[str, int] = {}
    for field in ("changed_lines", "test_changed_lines", "dependency_delta_count"):
        item = value.get(field)
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise MetricsContractError(f"patch.{field}:expected_non_negative_integer")
        result[field] = item
    return result
