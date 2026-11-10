"""Read-only adapter from workspace evidence to the existing T26/T27 selectors.

Task context is a routing proposal, never an authority or command executor.
Source hashes bind observations to files; they do not certify semantic truth.
"""

from __future__ import annotations

import hashlib
import json
import re
import tomllib
import sys
from dataclasses import replace
from pathlib import Path, PurePosixPath
from typing import Any

from product_agent_os.code_quality_selector import (
    TOOL_TRACERS, DeclaredToolSignal, ProjectCommandSignal, ProjectInventory,
    capability_summary, code_quality_profile_as_dict, select_code_quality_profile,
)
from product_agent_os.test_strategy_selector import (
    CHANGE_MODES, TEST_KINDS, ChangeRisk, CommentSignal, TestStrategyRequest,
    quality_strategy_as_dict, select_test_strategy,
)


TASK_FIELDS = {
    "schema_version", "task_id", "intent", "change_mode", "changed_paths",
    "risk_level", "risks", "acceptance", "checks", "executable_test_seam",
    "test_seam_reason", "comment_signals", "state", "check_results",
    "financially_material", "release_or_readiness", "explicit_full_packet",
    "verification_paths", "verification_environment",
    "documents", "evals_required",
}
EXTRA_MODES = {"docs_only", "no_op", "reuse", "deletion"}
SENSITIVE_PATH = re.compile(
    r"(?i)(^|[/_.-])(auth\w*|secrets?|permission\w*|payments?|billing|migrat\w*|security|hooks?)([/_.-]|$)"
)
SENSITIVE_INTENT = re.compile(
    r"(?i)\b(security|authorization|authentication|payment|billing|data.loss|release|deploy|publish)\b"
    r"|безопас|авторизац|аутентификац|платеж|платёж|потер[яи].данных|публикац|релиз"
)
UNSAFE_COMMAND = re.compile(
    r"[;&|<>`\r\n\x00]|\$\(|(?i:\b(curl|wget|invoke-webrequest|remove-item|rm|del)\b"
    r"|\b(npm|pip|uv)\s+(install|add)|\bgit\s+(push|reset|clean))"
)
COMMAND_START = re.compile(r"^(?:python(?:3|\.exe)?|pytest|npm|pnpm|yarn|go|cargo|dotnet|mvn|ruff|git)\s")


class TaskContextError(ValueError):
    """Malformed or out-of-bound task data; callers must not silently fall back."""


def add_task_intake_arguments(parser: Any) -> None:
    """Share the explicit, file-free intake across the two public entrypoints."""
    parser.add_argument("--task-context", help="Workspace-relative task context v1 JSON; mutually exclusive with inline intake.")
    parser.add_argument("--task", help="Task intent; opt in to scoped routing without a JSON file.")
    parser.add_argument("--task-id", help="Optional routing label; never authority or a completion receipt.")
    parser.add_argument("--change-mode", choices=sorted(CHANGE_MODES | EXTRA_MODES))
    parser.add_argument("--changed-path", action="append", help="Changed workspace-relative path; repeat as needed.")
    parser.add_argument("--acceptance", action="append", help="Observable acceptance criterion; repeat as needed.")
    parser.add_argument("--risk-level", choices=("low", "medium", "high", "unknown"))


def task_context_from_args(workspace: str | Path, args: Any) -> dict[str, Any] | None:
    """Normalize explicit intake; partial input fails closed, never legacy fallback.

    Rich risks, checks and state receipts use the existing JSON contract. Inline
    input does not infer invariants, executable seams, verification or authority.
    """
    inline = any(getattr(args, name) is not None for name in
                 ("task", "task_id", "change_mode", "changed_path", "acceptance", "risk_level"))
    if args.task_context is not None:
        if inline:
            raise TaskContextError("task_context:mixed_inline_and_file")
        return load_task_context(workspace, args.task_context)
    if not inline:
        return None
    return validate_task_context(Path(workspace).resolve(), {
        "schema_version": 1, "task_id": args.task_id if args.task_id is not None else "inline-task", "intent": args.task,
        "change_mode": args.change_mode, "changed_paths": args.changed_path or [],
        "acceptance": args.acceptance or [], "risk_level": args.risk_level or "unknown", "risks": [],
    })


def intake_receipt(task_context: dict[str, Any] | None) -> dict[str, str]:
    """Make compatibility fallback visible without changing legacy defaults."""
    return {
        "mode": "legacy_fallback" if task_context is None else "explicit_task_context",
        "reason": "no_explicit_task_context" if task_context is None else "existing_selectors_with_task_scope",
        "next_action": "Use --task with scope/acceptance/risk, or --task-context for rich risks/checks/state.",
        "authority": "routing_only_not_write_permission",
    }


def workspace_path(root: Path, name: str) -> Path:
    """Resolve a workspace-relative path, rejecting traversal, drives and symlinks out."""
    if not isinstance(name, str) or not name.strip() or name != name.strip():
        raise TaskContextError("task_context:path_invalid")
    normalized = name.replace("\\", "/")
    parts = PurePosixPath(normalized).parts
    if not parts or normalized.startswith("/") or ":" in normalized or ".." in parts or any(ord(c) < 32 for c in normalized):
        raise TaskContextError("task_context:path_outside_workspace")
    try:
        path = root.joinpath(*parts).resolve()
    except (OSError, ValueError) as exc:
        raise TaskContextError("task_context:path_invalid") from exc
    if not path.is_relative_to(root.resolve()):
        raise TaskContextError("task_context:path_outside_workspace")
    return path


def _source(root: Path, name: str) -> tuple[str, str]:
    path = workspace_path(root, name)
    try:
        if path.stat().st_size > 1024 * 1024:
            raise TaskContextError("task_context:source_too_large")
        raw = path.read_bytes()
        return raw.decode("utf-8-sig"), hashlib.sha256(raw).hexdigest()
    except (OSError, UnicodeDecodeError) as exc:
        raise TaskContextError("task_context:source_unreadable") from exc


def load_task_context(workspace: str | Path, filename: str) -> dict[str, Any]:
    """Load a bounded JSON file inside the target, without granting its requests."""
    text, _digest = _source(Path(workspace).resolve(), filename)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        raise TaskContextError("task_context:invalid_json") from exc
    return validate_task_context(Path(workspace).resolve(), value)


def _strings(value: Any, field: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or len(value) > 200 or (nonempty and not value):
        raise TaskContextError(f"task_context:{field}_invalid")
    if any(not isinstance(x, str) or not x.strip() or "\0" in x for x in value):
        raise TaskContextError(f"task_context:{field}_invalid")
    return value


def validate_task_context(root: Path, task: Any) -> dict[str, Any]:
    """Validate the opt-in contract before discovery or staging side effects."""
    if not isinstance(task, dict) or set(task) - TASK_FIELDS:
        raise TaskContextError("task_context:unknown_fields_or_shape")
    if type(task.get("schema_version")) is not int or task["schema_version"] != 1:
        raise TaskContextError("task_context:unsupported_schema_version")
    for key in ("task_id", "intent"):
        if not isinstance(task.get(key), str) or not task[key].strip() or "\0" in task[key]:
            raise TaskContextError(f"task_context:{key}_required")
    if not isinstance(task.get("change_mode"), str) or task["change_mode"] not in CHANGE_MODES | EXTRA_MODES:
        raise TaskContextError("task_context:change_mode_invalid")
    if not isinstance(task.get("risk_level"), str) or task["risk_level"] not in {"low", "medium", "high", "unknown"}:
        raise TaskContextError("task_context:risk_level_required")
    for name in _strings(task.get("changed_paths"), "changed_paths", nonempty=task["change_mode"] != "no_op"):
        workspace_path(root, name)
    for name in _strings(task.get("verification_paths", []), "verification_paths"):
        workspace_path(root, name)
    environment = task.get("verification_environment", {})
    if (not isinstance(environment, dict) or set(environment) - {"tool_versions", "runner", "environment_digest"}
            or any(not isinstance(v, str) or len(v) > 1000 for v in environment.values())):
        raise TaskContextError("task_context:verification_environment_invalid")
    _strings(task.get("acceptance"), "acceptance", nonempty=True)
    for key in ("risks", "checks", "comment_signals", "check_results"):
        value = task.get(key, [])
        if not isinstance(value, list) or len(value) > 200 or any(not isinstance(x, dict) for x in value):
            raise TaskContextError(f"task_context:{key}_invalid")
    if "risks" not in task:
        raise TaskContextError("task_context:risks_required")
    for key in ("executable_test_seam", "financially_material", "release_or_readiness", "explicit_full_packet", "evals_required"):
        if key in task and type(task[key]) is not bool:
            raise TaskContextError(f"task_context:{key}_must_be_boolean")
    if "test_seam_reason" in task and not isinstance(task["test_seam_reason"], str):
        raise TaskContextError("task_context:test_seam_reason_invalid")
    if task["change_mode"] == "docs_only" and any(
        Path(x).suffix.lower() not in {".md", ".rst", ".txt"} for x in task["changed_paths"]
    ):
        raise TaskContextError("task_context:docs_only_contains_non_docs")
    if "documents" in task:
        from product_agent_os.control_plane_documents import DOCUMENT_CONTRACTS, populate_document
        documents = task["documents"]
        if not isinstance(documents, dict) or set(documents) - set(DOCUMENT_CONTRACTS):
            raise TaskContextError("task_context:documents_invalid")
        for name, packet in documents.items():
            if not isinstance(packet, dict):
                raise TaskContextError("task_context:document_packet_invalid")
            try:
                populate_document(name, packet)
            except (TypeError, ValueError) as exc:
                raise TaskContextError("task_context:document_packet_invalid") from exc
    return task


def _risk_inputs(task: dict[str, Any]) -> tuple[tuple[ChangeRisk, ...], tuple[CommentSignal, ...]]:
    expected = {"risk_id", "kind", "description", "protected_invariants", "languages"}
    if any(set(risk) != expected for risk in task["risks"]):
        raise TaskContextError("task_context:risk_shape")
    try:
        risks = tuple(ChangeRisk(
            risk_id=r["risk_id"], kind=r["kind"], description=r["description"],
            protected_invariants=tuple(_strings(r["protected_invariants"], "invariants", nonempty=True)),
            languages=tuple(_strings(r["languages"], "languages", nonempty=True)),
        ) for r in task["risks"])
        comments = tuple(CommentSignal(**r) for r in task.get("comment_signals", []))
    except (KeyError, TypeError) as exc:
        raise TaskContextError("task_context:risk_or_comment_shape") from exc
    return risks, comments


def _mandatory_sources(root: Path, changed: list[str]) -> list[str]:
    names = {"AGENTS.md", "AGENTS.override.md", "TEST.md"}
    for name in changed:
        parent = PurePosixPath(name.replace("\\", "/")).parent
        for ancestor in (parent, *parent.parents):
            for filename in ("AGENTS.md", "AGENTS.override.md"):
                names.add(str(ancestor / filename))
    return sorted(name for name in names if workspace_path(root, name).is_file())


def _checks(root: Path, task: dict[str, Any], required_kinds: set[str],
            mandatory_sources: list[str]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """Keep project-owned checks mandatory; every command remains inert and unverified."""
    records: dict[str, dict[str, Any]] = {}
    source_hashes: dict[str, str] = {}
    candidates = []
    for check in task.get("checks", []):
        if set(check) != {"command", "source", "test_kinds"}:
            raise TaskContextError("task_context:check_shape")
        command = check["command"]
        if not isinstance(command, str) or not command.strip():
            raise TaskContextError("task_context:check_command_invalid")
        kinds = _strings(check["test_kinds"], "test_kinds")
        if set(kinds) - set(TEST_KINDS) - {"docs", "project"}:
            raise TaskContextError("task_context:check_kind_invalid")
        text, digest = _source(root, check["source"])
        if command not in text:
            raise TaskContextError("task_context:command_not_in_source")
        source_hashes[check["source"]] = digest
        if set(kinds) & (required_kinds | {"docs"} if task["change_mode"] == "docs_only" else required_kinds):
            candidates.append((command, check["source"], "selected_risk", kinds))
    for name in mandatory_sources:
        text, digest = _source(root, name)
        source_hashes[name] = digest
        # Conservative extraction, not semantic interpretation of project policy.
        # All source instructions remain required even if no command can be extracted.
        for line in text.splitlines():
            values = re.findall(r"`([^`\n]+)`", line) + [line.strip()]
            for value in values:
                if COMMAND_START.match(value):
                    candidates.append((value, name, "project_mandatory_review", ["project"]))
    for command, source, reason, kinds in candidates:
        record = records.setdefault(command, {
            "command": command, "sources": [], "reasons": [], "test_kinds": [],
            "status": "blocked" if UNSAFE_COMMAND.search(command) else "present_unverified",
            "execution_policy": "proposal_only_review_before_execution",
        })
        for key, values in (("sources", [source]), ("reasons", [reason]), ("test_kinds", kinds)):
            record[key] = sorted(set(record[key]) | set(values))
    return list(records.values()), source_hashes


def _inventory(root: Path, audit: dict[str, Any], checks: list[dict[str, Any]]) -> ProjectInventory:
    """Read configured tool names only; presence is not installation or execution."""
    paths = tuple(audit.get("detected_files", []))
    tools = []
    for name in paths:
        if Path(name).name not in {"package.json", "pyproject.toml"}:
            continue
        text, _digest = _source(root, name)
        try:
            data = json.loads(text) if name.endswith(".json") else tomllib.loads(text)
        except (json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
            raise TaskContextError("task_context:manifest_invalid") from exc
        if not isinstance(data, dict):
            raise TaskContextError("task_context:manifest_invalid")
        for section in ("dependencies", "devDependencies", "tool"):
            declared = data.get(section, {})
            if isinstance(declared, dict):
                tools.extend(DeclaredToolSignal(tool, name) for tool in declared if tool in TOOL_TRACERS)
    commands = tuple(ProjectCommandSignal(f"check-{i}", item["command"], source)
                     for i, item in enumerate(checks) for source in item["sources"]
                     if item["status"] != "blocked")
    return ProjectInventory(paths, tuple(tools), commands)


def _input_digest(root: Path, task: dict[str, Any], sources: dict[str, str],
                  audit: dict[str, Any]) -> str:
    hashes = dict(sources)
    relevant = {"pyproject.toml", "package.json", "go.mod", "Cargo.toml", "pom.xml", "uv.lock",
                "poetry.lock", "requirements.txt", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
                "Cargo.lock", "go.sum", "tsconfig.json", "ruff.toml", ".ruff.toml", ".importlinter",
                ".dependency-cruiser.cjs", "stryker.config.json"}
    names = set(task["changed_paths"]) | set(task.get("verification_paths", [])) | relevant | {
        name for name in audit.get("detected_files", []) if Path(name).name in relevant}
    for name in sorted(names):
        path = workspace_path(root, name)
        try:
            hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"
        except OSError as exc:
            raise TaskContextError("task_context:digest_input_unreadable") from exc
    payload = {"task": {k: v for k, v in task.items() if k != "check_results"}, "files": hashes,
               "inventory_paths": sorted(audit.get("detected_files", [])),
               "interpreter": sys.version, "platform": sys.platform}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def _observations(task: dict[str, Any], checks: list[dict[str, Any]], digest: str) -> list[dict[str, Any]]:
    """Check receipt consistency/freshness without trusting caller-reported success."""
    results = []
    commands = {item["command"] for item in checks if item["status"] != "blocked"}
    for receipt in task.get("check_results", []):
        if set(receipt) != {"command", "input_digest", "status", "exit_code"}:
            raise TaskContextError("task_context:check_result_shape")
        if not all(isinstance(receipt[key], str) for key in ("command", "input_digest", "status")):
            raise TaskContextError("task_context:check_result_text")
        if receipt["status"] not in {"passed", "failed", "skipped", "not_run_with_gap"}:
            raise TaskContextError("task_context:check_result_status")
        code = receipt["exit_code"]
        if code is not None and type(code) is not int:
            raise TaskContextError("task_context:check_result_exit_code")
        if receipt["status"] == "passed" and code != 0:
            raise TaskContextError("task_context:passed_requires_zero_exit")
        if receipt["status"] == "failed" and (code is None or code == 0):
            raise TaskContextError("task_context:failed_requires_nonzero_exit")
        if receipt["status"] in {"skipped", "not_run_with_gap"} and code is not None:
            raise TaskContextError("task_context:unexecuted_requires_null_exit")
        if receipt["command"] not in commands:
            raise TaskContextError("task_context:check_result_unknown_command")
        results.append({**receipt, "freshness": "current" if receipt["input_digest"] == digest else "stale",
                        "provenance": "caller_reported_not_independently_verified"})
    return results


def build_task_routing(workspace: str | Path, audit: dict[str, Any], task: dict[str, Any]) -> dict[str, Any]:
    """Select task-scoped guidance; missing information stays a gap, never success."""
    root = Path(workspace).resolve()
    validate_task_context(root, task)
    risks, comments = _risk_inputs(task)
    required_sources = _mandatory_sources(root, task["changed_paths"])
    # T26 consumes real discovery paths and configured tools, not invented tools.
    inventory = _inventory(root, audit, [])
    profile = select_code_quality_profile(inventory)
    mode = task["change_mode"]
    strategy = None
    if mode != "docs_only":
        try:
            strategy = select_test_strategy(TestStrategyRequest(
                profile=profile, change_mode=mode if mode in CHANGE_MODES else "refactor" if mode == "deletion" else "configuration",
                executable_test_seam=task.get("executable_test_seam", False),
                test_seam_reason="" if task.get("executable_test_seam", False)
                else task.get("test_seam_reason", "No executable seam declared"),
                risks=risks, comment_signals=comments,
            ))
        except (TypeError, ValueError) as exc:
            raise TaskContextError("task_context:strategy_invalid:" + str(exc)) from exc
    elif risks or comments:
        raise TaskContextError("task_context:docs_only_has_behavior_risks")
    required_kinds = {d.test_kind for d in strategy.test_decisions if d.status == "required"} if strategy else set()
    checks, hashes = _checks(root, task, required_kinds, required_sources)
    # Include project commands in T26's inventory; selection stays pure/unexecuted.
    commands = tuple(ProjectCommandSignal(f"check-{i}", item["command"], source)
                     for i, item in enumerate(checks) for source in item["sources"] if item["status"] != "blocked")
    inventory = replace(inventory, project_commands=commands)
    profile = select_code_quality_profile(inventory)
    full_reasons = []
    if task["risk_level"] in {"high", "medium"}:
        full_reasons.append("declared_risk:" + task["risk_level"])
    if any(r.kind in {"high_risk_rule", "critical_user_flow", "external_boundary"} for r in risks):
        full_reasons.append("sensitive_change_risk")
    # Classify canonical paths so Windows separators and leading './' cannot
    # downgrade the same sensitive file to an ordinary route.
    changed_names = [str(PurePosixPath(p.replace("\\", "/"))).lower() for p in task["changed_paths"]]
    if any(SENSITIVE_PATH.search(p) or p.startswith((".codex/", ".github/")) for p in changed_names):
        full_reasons.append("sensitive_changed_path")
    if SENSITIVE_INTENT.search(task["intent"]):
        full_reasons.append("sensitive_intent")
    full_reasons.extend(key for key in ("financially_material", "release_or_readiness", "explicit_full_packet") if task.get(key))
    gaps = []
    if task["risk_level"] == "unknown":
        gaps.append("Specify changed risks before selecting an ordinary route")
    if mode not in {"docs_only", "no_op", "configuration"} and not risks:
        gaps.append("Changed behavior requires explicit risk and invariant evidence")
    if strategy:
        gaps.extend(g for g in strategy.gaps if g != "no_changed_risks")
    covered = {kind for check in checks if check["status"] != "blocked" for kind in check["test_kinds"]}
    gaps.extend("No source-backed check mapped to required test kind: " + kind
                for kind in sorted(required_kinds - covered))
    safety_trigger = any(reason in {"sensitive_changed_path", "sensitive_intent", "financially_material"}
                         or reason.startswith("declared_risk:") for reason in full_reasons)
    if safety_trigger and not any(r.kind in {"high_risk_rule", "external_boundary", "critical_user_flow"} for r in risks):
        gaps.append("Sensitive task requires an explicit boundary or high-risk invariant and corresponding checks")
    if (required_kinds or mode == "docs_only") and not checks:
        gaps.append("No project-owned verification command selected; specify a check or review the project instructions")
    if any(c["status"] == "blocked" for c in checks):
        gaps.append("Unsafe command proposal blocked; review the source without executing it")
    if not required_sources:
        gaps.append("No project instruction or verification source found; perform discovery before implementation")
    digest = _input_digest(root, task, hashes, audit)
    observations = _observations(task, checks, digest)
    gaps.extend("Stale verification receipt: " + r["command"] for r in observations if r["freshness"] == "stale")
    selected_mode = "full" if full_reasons else "needs_context" if gaps else "ordinary"
    return {
        "schema_version": 1, "task_id": task["task_id"], "mode": selected_mode,
        "full_reasons": full_reasons, "gaps": list(dict.fromkeys(gaps)),
        "change_mode": mode, "required_sources": required_sources,
        "code_quality_profile": code_quality_profile_as_dict(profile),
        "capability_summary": capability_summary(inventory, scope_paths=tuple(task['changed_paths'])),
        "evidence_validity": {"environment": "caller_reported" if task.get("verification_environment") else "unknown",
                              "reuse": "same digest only; external tool/environment drift requires explicit receipt refresh",
                              "extra_inputs": "use verification_paths for project-specific resolver/config files"},
        "quality_strategy": quality_strategy_as_dict(strategy) if strategy else {"status": "not_applicable", "reason": "docs_only"},
        "checks": checks, "input_digest": digest, "source_hashes": hashes,
        "check_observations": observations, "acceptance": task["acceptance"],
        "invariants": [i for r in risks for i in r.protected_invariants],
        "selectors": ["select_code_quality_profile"] + (["select_test_strategy"] if strategy else []),
        "evidence_ceiling": "routing only; commands not executed; caller receipts do not prove completion",
    }
