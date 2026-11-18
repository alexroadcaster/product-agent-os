"""Bounded task profile projected from the existing discovery and routing facts."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

from product_agent_os.discovery import _route_source_files


UI_COMPONENTS = frozenset({".jsx", ".tsx", ".vue", ".svelte"})
UI_ASSETS = frozenset({".css", ".scss", ".html"})
NATIVE_CODE = frozenset({".swift", ".kt", ".dart"})
APPLICATION_CODE = UI_COMPONENTS | NATIVE_CODE | {
    ".py", ".rb", ".ts", ".mts", ".js", ".java", ".cs", ".go", ".rs", ".c", ".cpp", ".php",
}
TEST_PATH = re.compile(r"(?:^|/)(?:tests?|specs?|__tests__)/|(?:^|/)test_[^/]+$|\.(?:test|spec)\.[^/]+$")


def _surface(path: PurePosixPath) -> str:
    if path.suffix in UI_COMPONENTS | UI_ASSETS:
        return "frontend"
    if path.suffix in NATIVE_CODE:
        return "native"
    if path.suffix in APPLICATION_CODE:
        return "backend"
    if path.suffix in {".md", ".rst", ".txt"}:
        return "docs"
    return "unknown"


def scoped_paths(paths: list[str]) -> list[str]:
    """Match discovery's slash-separated inventory without case folding identity."""
    return list(dict.fromkeys(PurePosixPath(path.replace("\\", "/")).as_posix() for path in paths))


def describe_project(
    audit: dict[str, Any], task: dict[str, Any], route: dict[str, Any],
) -> dict[str, Any]:
    """Infer a task profile without another walk or treating a declared tool as installed."""
    files = _route_source_files(set(audit["detected_files"]))
    changed = scoped_paths(task["changed_paths"])
    mode = task["change_mode"]
    implementation = [path.lower() for path in changed if not TEST_PATH.search(path.lower())]
    surfaces = {_surface(PurePosixPath(path)) for path in implementation} - {"unknown", "docs"}
    surface = (
        "docs" if mode == "docs_only" else
        "mixed" if len(surfaces) > 1 else
        next(iter(surfaces), "unknown")
    )
    code_paths = {
        path for path in files
        if PurePosixPath(path.lower()).suffix in APPLICATION_CODE and not TEST_PATH.search(path.lower())
    }
    tests = {path for path in files if TEST_PATH.search(path.lower()) and PurePosixPath(path).suffix in APPLICATION_CODE}
    lifecycle = (
        "greenfield_candidate" if not code_paths else
        "existing_code_observed" if tests else
        "legacy_candidate"
    )
    frontend_areas = {
        path.parent.as_posix() for name in implementation
        if (path := PurePosixPath(name)).suffix in UI_COMPONENTS
    }
    return {
        "lifecycle": lifecycle,
        "surface": surface,
        "scale": audit["complexity_profile"]["drivers"]["repo_size"],
        "coupling": (
            "cross_surface" if len(surfaces) > 1 else
            "multiple_frontend_areas" if len(frontend_areas) > 1 else
            "local_scope" if changed else "unknown"
        ),
        "risk": task["risk_level"],
        "change_mode": mode,
        "ui_scope": "frontend" in surfaces,
        "stack": audit["detected_stack"],
        "check_count": sum(check["status"] != "blocked" for check in route["checks"]),
        "test_paths": [path for path in scoped_paths(task.get("verification_paths", [])) if path in tests],
        "environment": "caller_reported" if task.get("verification_environment") else "not_observed",
        "provenance": {
            "lifecycle_scale_stack": "workspace_discovery",
            "surface_coupling": "task_changed_paths",
            "intent_acceptance_risk": "explicit_task_context",
            "checks": "source_review_only",
        },
    }
