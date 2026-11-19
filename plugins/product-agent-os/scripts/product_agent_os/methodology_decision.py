"""Assemble task advice using discovery, scoped routing and the v1 wire contract."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from product_agent_os.methodology_check import select_verification_step
from product_agent_os.methodology_contract import SCHEMA_VERSION, read_methodology_decision
from product_agent_os.methodology_policy import select_methodologies
from product_agent_os.methodology_profile import describe_project, scoped_paths
from product_agent_os.methodology_requirements import project_requirements
from product_agent_os.question_protocol import build_question_queue
from product_agent_os.task_routing import fingerprint


def build_methodology_decision(
    workspace: str | Path, audit: dict[str, Any], task: dict[str, Any], route: dict[str, Any],
    revision_sources: dict[str, str], *, host_scope: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Bind advice to the requested project, observable source, and normalized task."""
    if host_scope is not None and host_scope.get("task_id") != task["task_id"]:
        raise ValueError("methodology_decision:host_task_mismatch")
    scope = host_scope if host_scope is not None else {
        "project_id": fingerprint(os.path.normcase(str(Path(workspace).resolve()))),
        "task_id": task["task_id"],
        "source_revision": fingerprint({
            "files": revision_sources, "inventory": sorted(audit["detected_files"]),
        }),
        "task_revision": fingerprint({key: value for key, value in task.items() if key != "check_results"}),
    }
    profile = describe_project(audit, task, route)
    files = {
        scoped_paths([path])[0]: digest
        for path, digest in sorted(revision_sources.items()) if digest != "missing"
    }
    next_step, verification_gap = select_verification_step(task, route, profile, set(files))
    decisions = select_methodologies(profile, route, next_step["kind"])
    requirements = project_requirements(task, route, next_step)
    gaps = list(route["gaps"])
    if verification_gap:
        gaps.insert(0, verification_gap)
    if not verification_gap and any(row["trace"] == "gap" for row in requirements["criteria"]):
        gaps.insert(0, "Which observable check or source supports each acceptance criterion?")
    if any(row["method"] == "fsd" and row["applicability"] == "needs_context" for row in decisions):
        gaps.append("Which import or ownership boundary accounts for the cross-feature change?")
    gaps = list(dict.fromkeys(gaps))
    queue = build_question_queue(
        runtime_gaps=[{
            "category": "verification", "question": gap, "answer_type": "text",
            "source_key": f"methodology_gap_{index}", "priority": "blocking",
        } for index, gap in enumerate(gaps[:1], 1)],
    )
    question = queue["next_blocking_question"]
    refs = {ref for ref in next_step["evidence_refs"] if ref.startswith("file:")}
    refs.update(f"file:{name}" for name in profile["test_paths"] if name in files)
    refs.update(f"file:{name}" for name in scoped_paths(route["required_sources"]) if name in files)
    evidence = [
        {"id": "task", "kind": "task", "path": None, "revision": scope["task_revision"]},
        {"id": "workspace", "kind": "workspace", "path": None, "revision": scope["source_revision"]},
    ]
    for ref in sorted(refs):
        name = ref.removeprefix("file:")
        evidence.append({"id": ref, "kind": "file", "path": name, "revision": files[name]})
    assumptions = (
        ["Project history remains unconfirmed; lifecycle is inferred from detected code and tests"]
        if profile["lifecycle"] != "existing_code_observed" else []
    )
    if profile["environment"] != "not_observed":
        assumptions.append("Tool and environment details came from the caller")
    result = {
        "schema_version": SCHEMA_VERSION,
        "scope": scope,
        "facts": profile,
        "evidence": evidence,
        "decisions": decisions,
        "requirements": requirements,
        "plan": {
            "next_step": next_step, "assumptions": assumptions, "gaps": gaps,
            "blocking_question": question["text"] if question else None,
        },
        "execution": "not_started",
        "acceptance": "not_evaluated",
        "authority": "read_only",
    }
    return read_methodology_decision(result, scope)
