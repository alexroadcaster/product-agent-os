from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from codex_runtime_runner.context_loader import load_control_plane_context
from codex_runtime_runner.contracts import build_result, validate_runner_result
from codex_runtime_runner.guards import validate_approval_boundary, validate_route_packet
from codex_runtime_runner.redaction import redact_payload, validate_redaction
from codex_runtime_runner.routes import plan_route
from codex_runtime_runner.state import infer_lifecycle_state
from product_agent_os.discovery import analyze_workspace
from product_agent_os.source_policy import validate_source_policy


def run_contract(
    workspace: str | Path,
    *,
    allow_subagents: bool = False,
    approval_status: str = "not_required",
    intent_hint: str = "",
) -> dict[str, Any]:
    context = load_control_plane_context(workspace)
    request = {
        "task": {"lifecycle_state": ""},
        "routing": {"allow_subagents": allow_subagents, "allow_workspace_writes": False},
        "approval": {"approval_status": approval_status},
    }
    state = infer_lifecycle_state(context, request)
    audit = analyze_workspace(workspace, intent_hint=intent_hint)
    route = plan_route(
        state,
        allow_subagents=allow_subagents,
        usage_mode=audit["usage_mode"],
        behavioral_route_inputs=audit["route_inputs"],
        methodology_intelligence=audit["methodology_intelligence"],
    )
    errors: list[str] = []
    warnings: list[str] = []

    if context["unreadable"]:
        errors.extend(f"context:unreadable:{name}" for name in context["unreadable"])
    source_policy_report = validate_source_policy(workspace)
    source_policy_status = str(source_policy_report["status"])
    if source_policy_status == "blocked":
        errors.append("source_policy:blocked")
    elif source_policy_status == "needs_review":
        warnings.append("source_policy:needs_review")
    route_errors = validate_route_packet(route)
    approval_errors = validate_approval_boundary(route, {"approval_status": approval_status})
    errors.extend(route_errors)
    if approval_errors:
        warnings.extend(approval_errors)

    status = _status_for(context, route, errors, approval_errors)
    result = build_result(
        status=status,
        workspace=str(workspace),
        lifecycle_state=state,
        route_packet=route,
        source_policy_status=source_policy_status,
        approval_status=approval_status,
        next_action=route["next_action"],
        files_proposed=[] if route["write_policy"] == "read_only" else ["staged handoff packet"],
        verification_evidence=["codex_runtime_runner contract mode completed"] if status == "route_ready" else [],
        errors=errors,
        warnings=warnings,
    )
    result, redactions = redact_payload(result)
    result["redactions"] = redactions
    result["errors"].extend(validate_redaction(json.dumps(result, sort_keys=True)))
    result["errors"].extend(validate_runner_result(result))
    if result["errors"] and result["status"] == "route_ready":
        result["status"] = "blocked"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Product-Agent OS Codex runtime runner in contract mode.")
    parser.add_argument("workspace")
    parser.add_argument("--contract", action="store_true", help="Run deterministic offline contract mode.")
    parser.add_argument("--allow-subagents", action="store_true", help="Allow subagent route recommendations.")
    parser.add_argument("--approval-status", default="not_required")
    parser.add_argument("--intent-hint", default="", help="Optional prompt-like routing hint for contract mode.")
    parser.add_argument("--output", help="Optional JSON output file.")
    args = parser.parse_args(argv)
    if not args.contract:
        print("error: choose --contract", file=sys.stderr)
        return 2

    result = run_contract(
        args.workspace,
        allow_subagents=args.allow_subagents,
        approval_status=args.approval_status,
        intent_hint=args.intent_hint,
    )
    text = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if result["status"] == "route_ready" else 1


def _status_for(
    context: dict[str, Any],
    route: dict[str, Any],
    errors: list[str],
    approval_errors: list[str],
) -> str:
    if errors:
        return "blocked"
    if context["missing"] and route["lifecycle_state"] != "uninitialized":
        return "needs_context"
    if approval_errors:
        return "needs_approval"
    return "route_ready"
