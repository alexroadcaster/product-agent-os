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
from codex_runtime_runner.routes import apply_runner_status_to_route, plan_route
from codex_runtime_runner.state import infer_lifecycle_state, resolve_task_state
from product_agent_os.discovery import analyze_workspace
from product_agent_os.source_policy import validate_source_policy
from product_agent_os.task_routing import (
    TaskContextError, build_task_routing, validate_task_context,
    add_task_intake_arguments, task_context_from_args, intake_receipt,
)


def run_contract(
    workspace: str | Path,
    *,
    allow_subagents: bool = False,
    approval_status: str = "not_required",
    intent_hint: str = "",
    task_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if task_context is not None:
        validate_task_context(Path(workspace).resolve(), task_context)
    context = load_control_plane_context(workspace)
    request = {
        "task": {"lifecycle_state": ""},
        "routing": {"allow_subagents": allow_subagents, "allow_workspace_writes": False},
        "approval": {"approval_status": approval_status},
    }
    state = infer_lifecycle_state(context, request) if task_context is None else "maintenance"
    audit = analyze_workspace(workspace, intent_hint=intent_hint or (task_context or {}).get("intent", ""))
    task_routing = None
    if task_context is not None:
        effective_task = dict(task_context)
        if intent_hint:
            effective_task["intent"] = task_context["intent"] + "\n" + intent_hint
        task_routing = build_task_routing(workspace, audit, effective_task)
        state_resolution = resolve_task_state(context, task_context)
        state = state_resolution["recommendation"]
        task_routing["state_resolution"] = state_resolution
        task_routing["gaps"].extend(state_resolution["gaps"])
        if state in {"review_ready", "release_ready", "learning_ready"}:
            task_routing["full_reasons"].append("release_or_review_state")
            task_routing["mode"] = "full"
        if task_routing["gaps"] and task_routing["mode"] == "ordinary":
            task_routing["mode"] = "needs_context"
    route = plan_route(
        state,
        allow_subagents=allow_subagents,
        usage_mode=audit["usage_mode"],
        behavioral_route_inputs=audit["route_inputs"],
        methodology_intelligence=audit["methodology_intelligence"],
        task_routing=task_routing,
    )
    errors: list[str] = []
    route["intake"] = intake_receipt(task_context)
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
    route = apply_runner_status_to_route(route, status)
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
    add_task_intake_arguments(parser)
    parser.add_argument("--output", help="Optional JSON output file.")
    args = parser.parse_args(argv)
    if not args.contract:
        print("error: choose --contract", file=sys.stderr)
        return 2

    try:
        task_context = task_context_from_args(args.workspace, args)
        result = run_contract(
            args.workspace,
            allow_subagents=args.allow_subagents,
            approval_status=args.approval_status,
            intent_hint=args.intent_hint,
            task_context=task_context,
        )
    except TaskContextError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
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
    scoped = route.get("task_routing")
    if isinstance(scoped, dict) and scoped["gaps"]:
        return "needs_context"
    missing = [name for name in context["missing"] if name in route["required_inputs"]]
    if missing and (scoped is not None or route["lifecycle_state"] != "uninitialized"):
        return "needs_context"
    if approval_errors:
        return "needs_approval"
    return "route_ready"
