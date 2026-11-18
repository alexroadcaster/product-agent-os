"""Choose an inert next verification from the existing source-backed checks."""

from __future__ import annotations

import shlex
from pathlib import PurePosixPath
from typing import Any

from product_agent_os.methodology_profile import scoped_paths
from product_agent_os.test_strategy_selector import TEST_FIRST_MODES


BEHAVIOR_CHECKS = {"unit", "property", "characterization", "contract_integration", "end_to_end"}


def step(kind: str, action: str, target: str | None = None, *refs: str) -> dict[str, Any]:
    return {"kind": kind, "action": action, "target": target, "evidence_refs": list(refs) or ["task"]}


def _test_named_in_command(command: str, test_paths: list[str]) -> str | None:
    """Match explicit unittest or pytest targets to files, without loading target code."""
    try:
        args = shlex.split(command)
    except ValueError:
        return None
    if not args:
        return None
    runner, *tail = args
    if runner in {"python", "python3", "python.exe"}:
        if tail and tail[0] == "-B":
            tail = tail[1:]
        if len(tail) != 3 or tail[0] != "-m" or tail[1] not in {"unittest", "pytest"}:
            return None
        suite, target = tail[1:]
    elif runner == "pytest" and len(tail) == 1:
        suite, target = "pytest", tail[0]
    else:
        return None
    if target.startswith("-"):
        return None
    target = target.removeprefix("./").split("::", maxsplit=1)[0]
    for name in test_paths:
        if target == name:
            return name
        if suite == "unittest" and name.endswith(".py"):
            module = ".".join(PurePosixPath(name).with_suffix("").parts)
            if target == module or target.startswith(module + "."):
                return name
    return None


def select_verification_step(
    task: dict[str, Any], route: dict[str, Any], profile: dict[str, Any], file_refs: set[str],
) -> tuple[dict[str, Any], str | None]:
    """Return a check or one explicit gap. No check is run by this layer."""
    mode = profile["change_mode"]
    sources = [path for path in scoped_paths(task.get("verification_paths", [])) if path in file_refs]
    if task.get("evals_required"):
        eval_source = next((path for path in sources if PurePosixPath(path).name == "EVALS.md"), None)
        if eval_source:
            return step("review_evaluation", "Review the versioned rubric and eval evidence", eval_source, f"file:{eval_source}"), None
        return step("clarify", "Identify the evaluation source"), "Which current source defines the evaluation and its rubric?"
    if mode == "docs_only":
        if sources:
            source = sources[0]
            return step("check_source", "Compare the documentation claim with this source", source, f"file:{source}"), None
        return step("clarify", "Identify the source for the documentation change"), "Which source supports the documentation criterion?"
    if mode == "configuration":
        source = next((path for path in scoped_paths(task["changed_paths"]) if path in file_refs), None)
        if source:
            return step("check_configuration", "Review the current configuration and applicable static constraints", source, f"file:{source}"), None
        return step("clarify", "Identify the configuration schema or source"), "Which file defines the configuration or its schema?"
    if mode in TEST_FIRST_MODES | {"refactor"}:
        strategy = route["quality_strategy"]
        if mode == "refactor" or strategy.get("test_first_decision", {}).get("status") == "required":
            for check in route["checks"]:
                if check["status"] != "present_unverified" or not BEHAVIOR_CHECKS.intersection(check["test_kinds"]):
                    continue
                named_test = _test_named_in_command(check["command"], profile["test_paths"])
                declared_in = next((path for path in scoped_paths(check["sources"]) if path in file_refs), None)
                if named_test in file_refs and declared_in:
                    kind = "run_characterization" if mode == "refactor" else "run_regression"
                    action = (
                        "Characterize current behavior before refactoring" if mode == "refactor" else
                        "Run the named test and require the intended behavioral failure before a fix"
                    )
                    refs = tuple(dict.fromkeys([f"file:{declared_in}", f"file:{named_test}"]))
                    return step(kind, action, check["command"], *refs), None
        return step("clarify", "Identify a relevant executable test and its project check"), (
            "Which source-backed check names the test for the declared behavior?"
        )
    return step("review_scope", "Review the proposed scope and choose the relevant verification"), None
