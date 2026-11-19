from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from codex_runtime_runner.context_loader import load_control_plane_context
from codex_runtime_runner.contracts import build_result, validate_runner_result, ALLOWED_LIFECYCLE_STATES
from codex_runtime_runner.guards import validate_approval_boundary, validate_route_packet
from codex_runtime_runner.methodology_delivery import build_delivery_plan
from codex_runtime_runner.methodology_execution import (
    build_execution_assignment, project_criterion_evidence, review_execution_handoff,
)
from codex_runtime_runner.redaction import redact_payload, validate_redaction
from codex_runtime_runner.routes import apply_runner_status_to_route, plan_route
from codex_runtime_runner.state import infer_lifecycle_state, resolve_task_state
from product_agent_os.discovery import analyze_workspace
from product_agent_os.methodology_context import compare_context
from product_agent_os.methodology_decision import build_methodology_decision
from product_agent_os.source_policy import validate_source_policy
from product_agent_os.task_routing import (
    TaskContextError, build_task_routing, normalize_task_intent,
    add_task_intake_arguments, task_context_from_args, intake_receipt,
)


def run_contract(
    workspace: str | Path,
    *,
    allow_subagents: bool = False,
    approval_status: str = "not_required",
    intent_hint: str = "",
    requested_state: str = "",
    task_context: dict[str, Any] | None = None,
    previous_methodology_context: dict[str, Any] | None = None,
    methodology_handoff: dict[str, Any] | None = None,
    include_delivery_plan: bool = False,
) -> dict[str, Any]:
    task_context, effective_intent = normalize_task_intent(Path(workspace).resolve(), task_context, intent_hint)
    if (previous_methodology_context is not None or methodology_handoff is not None or include_delivery_plan) and task_context is None:
        raise TaskContextError("methodology_context:task_required")
    context = load_control_plane_context(workspace)
    request = {
        "task": {"lifecycle_state": requested_state},
        "routing": {"allow_subagents": allow_subagents, "allow_workspace_writes": False},
        "approval": {"approval_status": approval_status},
    }
    state = infer_lifecycle_state(context, request) if task_context is None else "maintenance"
    audit = analyze_workspace(workspace, intent_hint=effective_intent)
    task_routing = None
    methodology_context = None
    methodology_decision = None
    if task_context is not None:
        task_routing = build_task_routing(workspace, audit, task_context, include_revision_sources=True)
        revision_sources = task_routing.pop("revision_sources")
        state_resolution = resolve_task_state(context, task_context)
        state = state_resolution["recommendation"]
        task_routing["state_resolution"] = state_resolution
        task_routing["gaps"].extend(state_resolution["gaps"])
        if state in {"review_ready", "release_ready", "learning_ready"}:
            task_routing["full_reasons"].append("release_or_review_state")
            task_routing["mode"] = "full"
        methodology_decision = build_methodology_decision(
            workspace, audit, task_context, task_routing, revision_sources,
        )
        methodology_context = compare_context(
            methodology_decision, task_routing, revision_sources, previous_methodology_context,
        )
        if methodology_context["impact"] and methodology_context["impact"]["status"] == "review_required":
            gap = "Previous methodology context is stale; review affected owners and refresh evidence"
            task_routing["gaps"].append(gap)
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
    if task_context is not None:
        if methodology_context["impact"] and methodology_context["impact"]["status"] == "review_required":
            methodology_decision = build_methodology_decision(
                workspace, audit, task_context, task_routing, revision_sources,
            )
        route["methodology_decision"] = methodology_decision
        route["methodology_context"] = methodology_context
        route["methodology_execution"] = build_execution_assignment(
            methodology_decision, task_routing, parallel_requested=allow_subagents,
        )
        route["methodology_criterion_evidence"] = project_criterion_evidence(methodology_decision, task_routing)
        if methodology_handoff is not None:
            route["methodology_execution"]["handoff_review"] = review_execution_handoff(
                route["methodology_execution"], methodology_handoff,
            )
        if include_delivery_plan:
            try:
                route["methodology_delivery_plan"] = build_delivery_plan(
                    Path(workspace).resolve(), audit, task_context, methodology_decision, route["methodology_execution"],
                )
            except ValueError as exc:
                raise TaskContextError("methodology_delivery:formation_inputs_unavailable") from exc
            if methodology_context["impact"] and methodology_context["impact"]["status"] == "review_required":
                methodology_context["impact"]["affected_slices"] = [
                    {"id": row["id"], "owner": row["owner"]}
                    for row in route["methodology_delivery_plan"]["slices"]
                ]
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
    parser.add_argument("--intent-hint", default="", help="Legacy audit hint; must agree with explicit task intent.")
    parser.add_argument("--requested-state", default="", choices=sorted(ALLOWED_LIFECYCLE_STATES),
                        help="Explicit route intent, not verified task readiness or write authority.")
    add_task_intake_arguments(parser)
    inbound = parser.add_mutually_exclusive_group()
    inbound.add_argument("--compare-methodology-context", action="store_true",
                         help="Read the previous methodology_context.snapshot JSON from stdin.")
    inbound.add_argument("--review-methodology-handoff", action="store_true",
                         help="Read one methodology handoff JSON object from stdin for review.")
    parser.add_argument("--methodology-delivery-plan", action="store_true",
                        help="Propose one read-only dependency graph for the scoped task.")
    parser.add_argument("--output", help="Optional JSON output file for repository-only contract mode.")
    args = parser.parse_args(argv)
    if not args.contract:
        print("error: choose --contract", file=sys.stderr)
        return 2

    try:
        task_context = task_context_from_args(args.workspace, args)
        if task_context is not None and args.output:
            raise TaskContextError("task_context:read_only_stdout")
        inbound_payload = None
        if args.compare_methodology_context or args.review_methodology_handoff:
            if task_context is None:
                raise TaskContextError("methodology_context:task_required")
            try:
                raw = sys.stdin.buffer.read(1024 * 1024 + 1)
                inbound_payload = json.loads(raw) if len(raw) <= 1024 * 1024 else None
            except (UnicodeDecodeError, ValueError, RecursionError):
                pass
            if not isinstance(inbound_payload, dict):
                raise TaskContextError("methodology_context:invalid_inbound_packet")
        result = run_contract(
            args.workspace,
            allow_subagents=args.allow_subagents,
            approval_status=args.approval_status,
            intent_hint=args.intent_hint,
            requested_state=args.requested_state,
            task_context=task_context,
            previous_methodology_context=inbound_payload if args.compare_methodology_context else None,
            methodology_handoff=inbound_payload if args.review_methodology_handoff else None,
            include_delivery_plan=args.methodology_delivery_plan,
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
    if "handoff_review" in route.get("methodology_execution", {}):
        return "needs_context"
    if route.get("methodology_delivery_plan", {}).get("status") == "review_required":
        return "needs_context"
    missing = [name for name in context["missing"] if name in route["required_inputs"]]
    if missing and (scoped is not None or route["lifecycle_state"] != "uninitialized"):
        return "needs_context"
    if approval_errors:
        return "needs_approval"
    return "route_ready"
