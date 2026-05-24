from __future__ import annotations

import re
from typing import Any

from codex_runtime_runner.routes import ROUTES


ACTIVE_AUTOMATION_PATTERN = re.compile(r"(?i)\b(active|recurring|scheduled)\s+automation\b|\bcreate\s+.*automation\b")


def validate_route_packet(route: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    state = route.get("lifecycle_state")
    expected = ROUTES.get(str(state))
    if not expected:
        return ["route:lifecycle_state_unknown"]

    expected_skill, expected_subagent, expected_write_policy, _action = expected
    if route.get("write_policy") != expected_write_policy:
        errors.append("route:unexpected_write_policy_for_state")
    if expected_skill and route.get("recommended_skill") != expected_skill:
        errors.append("route:unexpected_skill_for_state")
    if expected_subagent and route.get("recommended_subagent_role") not in {expected_subagent, ""}:
        errors.append("route:unexpected_subagent_for_state")
    return errors


def validate_approval_boundary(route: dict[str, Any], approval: dict[str, Any]) -> list[str]:
    if route.get("write_policy") == "approved_write" and approval.get("approval_status") != "approved":
        return ["approval:required_for_write"]
    return []


def validate_codex_handoff(handoff: dict[str, Any]) -> list[str]:
    required = [
        "lifecycle_state",
        "role",
        "goal",
        "constraints",
        "sources_used",
        "assumptions",
        "verified_claims",
        "unsupported_claims",
        "files_touched",
        "files_proposed",
        "commands_run",
        "verification_evidence",
        "approval_requirements",
        "open_risks",
        "recommended_next_role",
        "stop_reason",
    ]
    errors = [field for field in required if field not in handoff]

    for field in ["constraints", "verification_evidence"]:
        value = handoff.get(field)
        if value is not None and not isinstance(value, list):
            errors.append(f"{field}:invalid")
        elif value == []:
            errors.append(f"{field}:empty")

    for field in ["files_touched", "files_proposed"]:
        if field in handoff and not isinstance(handoff[field], list):
            errors.append(f"{field}:invalid")

    if handoff.get("files_touched") == [] and handoff.get("files_proposed") == []:
        errors.append("files:empty")
    return errors


def validate_automation_boundary(text: str) -> list[str]:
    if ACTIVE_AUTOMATION_PATTERN.search(text):
        return ["automation:active_request_blocked"]
    return []
