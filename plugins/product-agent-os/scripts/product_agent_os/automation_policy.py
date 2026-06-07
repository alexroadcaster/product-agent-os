from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from product_agent_os.validators import is_forbidden_secret_assignment


def validate_automation_candidate(candidate_file: str | Path) -> dict[str, Any]:
    """Validate an automation candidate packet without creating active automation."""
    path = Path(candidate_file)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return _report(
            "blocked",
            str(path),
            errors=[f"unable to read candidate file: {exc}"],
        )
    return from_text(text, str(path))


def from_text(text: str, candidate_file: str) -> dict[str, Any]:
    manual_success_count = _manual_success_count(text)
    metrics_automation_candidate = _is_metrics_automation_candidate(text, candidate_file)
    active_schedule_present = _active_schedule_present(text)
    external_workflow_present = _external_workflow_present(text)
    owner_present = "Accountable owner:" in text
    cadence_present = "## Cadence" in text and ("Trigger:" in text or "Frequency:" in text)
    stable_inputs_present = "## Stable Inputs" in text and "Inputs:" in text
    stable_outputs_present = "## Stable Outputs" in text and "Outputs:" in text
    verification_present = "## Verification" in text and "Deterministic checks:" in text
    failure_modes_present = "## Failure Modes" in text and "Known failure:" in text
    rollback_or_disable_present = "## Rollback Or Disable Path" in text and "Disable path:" in text
    write_policy_present = "## Explicit Write Policy" in text and "Allowed write targets:" in text
    explicit_approval_present = "## Explicit Approval" in text

    errors: list[str] = []
    warnings: list[str] = []
    if not owner_present:
        errors.append("owner is required")
    if not verification_present:
        errors.append("verification is required")
    if not rollback_or_disable_present:
        errors.append("rollback or disable path is required")
    if not write_policy_present:
        errors.append("write policy is required")
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        errors.append("secret-like literal is forbidden")
    if active_schedule_present:
        errors.append("active automation is forbidden")
    if external_workflow_present:
        errors.append("external workflow creation is forbidden")
    if metrics_automation_candidate and active_schedule_present:
        errors.append("active metrics automation is forbidden")
    if not stable_inputs_present:
        warnings.append("stable inputs are not documented")
    if not stable_outputs_present:
        warnings.append("stable outputs are not documented")
    if not cadence_present:
        warnings.append("cadence is not documented")
    if not failure_modes_present:
        warnings.append("failure modes are not documented")
    if not explicit_approval_present:
        warnings.append("explicit approval section is not documented")
    if manual_success_count < 2:
        warnings.append("manual success count is below 2")

    readiness_fields_present = all(
        [
            owner_present,
            cadence_present,
            stable_inputs_present,
            stable_outputs_present,
            verification_present,
            failure_modes_present,
            rollback_or_disable_present,
            write_policy_present,
            explicit_approval_present,
        ]
    )
    status = (
        "blocked"
        if errors
        else "candidate_only"
        if metrics_automation_candidate
        else "ready_for_manual_approval"
        if manual_success_count >= 2 and readiness_fields_present
        else "candidate_only"
    )
    return _report(
        status,
        candidate_file,
        manual_success_count=manual_success_count,
        owner_present=owner_present,
        cadence_present=cadence_present,
        stable_inputs_present=stable_inputs_present,
        stable_outputs_present=stable_outputs_present,
        verification_present=verification_present,
        failure_modes_present=failure_modes_present,
        rollback_or_disable_present=rollback_or_disable_present,
        write_policy_present=write_policy_present,
        explicit_approval_present=explicit_approval_present,
        metrics_automation_candidate=metrics_automation_candidate,
        active_schedule_status="detected" if active_schedule_present else "not_created",
        errors=errors,
        warnings=warnings,
    )


def _report(
    status: str,
    candidate_file: str,
    *,
    manual_success_count: int = 0,
    owner_present: bool = False,
    cadence_present: bool = False,
    stable_inputs_present: bool = False,
    stable_outputs_present: bool = False,
    verification_present: bool = False,
    failure_modes_present: bool = False,
    rollback_or_disable_present: bool = False,
    write_policy_present: bool = False,
    explicit_approval_present: bool = False,
    metrics_automation_candidate: bool = False,
    active_schedule_status: str = "not_applicable",
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    errors = errors or []
    warnings = warnings or []
    required_fields_present = not errors
    report = {
        "status": status,
        "candidate_file": candidate_file,
        "required_fields_present": required_fields_present,
        "manual_success_count": manual_success_count,
        "owner_present": owner_present,
        "cadence_present": cadence_present,
        "stable_inputs_present": stable_inputs_present,
        "stable_outputs_present": stable_outputs_present,
        "verification_present": verification_present,
        "failure_modes_present": failure_modes_present,
        "rollback_or_disable_present": rollback_or_disable_present,
        "write_policy_present": write_policy_present,
        "explicit_approval_present": explicit_approval_present,
        "metrics_automation_candidate": metrics_automation_candidate,
        "active_schedule_status": active_schedule_status,
        "errors": errors,
        "warnings": warnings,
    }
    return report | {"automation_promotion_report": dict(report)}


def _manual_success_count(text: str) -> int:
    match = re.search(r"Successful manual workflow runs:\s*(\d+)", text)
    if match:
        return int(match.group(1))
    match = re.search(r"Manual workflow runs:\s*(\d+)", text)
    if match and "Failures observed: none" in text:
        return int(match.group(1))
    return 0


def _is_metrics_automation_candidate(text: str, candidate_file: str) -> bool:
    lowered = f"{candidate_file}\n{text}".lower()
    return (
        "metrics-loop" in lowered
        or "agent skill metrics" in lowered
        or "agent-skill-metrics" in lowered
        or "daily-agent-skill-metrics" in lowered
        or "weekly-agent-skill-metrics" in lowered
    )


def _active_schedule_present(text: str) -> bool:
    lowered = text.lower()
    if "## active schedule" in lowered:
        return True
    return any(
        phrase in lowered
        for phrase in [
            "recurring schedule is active",
            "cron:",
            "rrule:",
            "codex app automation: active",
        ]
    )


def _external_workflow_present(text: str) -> bool:
    lowered = text.lower()
    return any(
        phrase in lowered
        for phrase in [
            "github actions workflow: active",
            "external workflow: active",
            "codex app automation: active",
        ]
    )


validate_automation_candidate.from_text = from_text
