"""Compare observed task inputs without treating a diff as semantic impact proof."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Any

from product_agent_os.methodology_profile import scoped_paths
from product_agent_os.task_routing import TaskContextError, fingerprint

SCHEMA = "paos_methodology_context_v1"
_HASH = re.compile(r"[a-f0-9]{64}")
_OWNER_ROLES = {
    "AGENTS.md": "workspace-owner", "AGENTS.override.md": "workspace-owner",
    "REQUIREMENTS.md": "requirements-author", "TEST.md": "test-eval-designer",
    "EVALS.md": "test-eval-designer", "PLAN.md": "implementation-planner",
    "RUNLOG.md": "lifecycle-orchestrator",
}


def _records(value: Any, key: str, *, file_hashes: bool = False) -> dict[str, str]:
    if not isinstance(value, list) or len(value) > 4096:
        raise TaskContextError("methodology_context:invalid_snapshot")
    records: dict[str, str] = {}
    for row in value:
        if not isinstance(row, dict) or set(row) != {key, "digest"}:
            raise TaskContextError("methodology_context:invalid_snapshot")
        name, digest = row[key], row["digest"]
        if (not isinstance(name, str) or not name or len(name) > 1024 or name in records
                or not isinstance(digest, str) or not (_HASH.fullmatch(digest) or file_hashes and digest == "missing")):
            raise TaskContextError("methodology_context:invalid_snapshot")
        if file_hashes and (name.startswith("/") or ".." in name.split("/") or "\\" in name or ":" in name
                            or any(ord(character) < 32 for character in name)):
            raise TaskContextError("methodology_context:invalid_snapshot")
        records[name] = digest
    return records


def _changes(before: dict[str, str], now: dict[str, str]) -> list[str]:
    return sorted(name for name in before.keys() | now.keys() if before.get(name) != now.get(name))


def compare_context(
    decision: dict[str, Any], routing: dict[str, Any], sources: dict[str, str], previous: Any = None,
) -> dict[str, Any]:
    """Emit a reusable, read-only snapshot and a conservative recheck disposition."""
    files = {scoped_paths([path])[0]: digest for path, digest in sources.items()}
    criteria = {row["id"]: fingerprint(row["criterion"]) for row in decision["requirements"]["criteria"]}
    checks = {fingerprint(check["command"]): fingerprint(check) for check in routing["checks"]}
    snapshot = {
        "schema_version": SCHEMA, "scope": dict(decision["scope"]), "input_digest": routing["input_digest"],
        "files": [{"path": path, "digest": digest} for path, digest in sorted(files.items())],
        "criteria": [{"id": key, "digest": digest} for key, digest in sorted(criteria.items())],
        "checks": [{"id": key, "digest": digest} for key, digest in sorted(checks.items())],
    }
    if previous is None:
        return {"snapshot": snapshot, "impact": None}
    if not isinstance(previous, dict) or set(previous) != set(snapshot) or previous["schema_version"] != SCHEMA:
        raise TaskContextError("methodology_context:invalid_snapshot")
    scope = previous["scope"]
    if (not isinstance(scope, dict) or set(scope) != set(snapshot["scope"])
            or any(scope[key] != snapshot["scope"][key] for key in ("project_id", "task_id"))):
        raise TaskContextError("methodology_context:scope_mismatch")
    if any(not isinstance(item, str) or not _HASH.fullmatch(item)
           for item in (scope["source_revision"], scope["task_revision"], previous["input_digest"])):
        raise TaskContextError("methodology_context:invalid_snapshot")
    previous_files = _records(previous["files"], "path", file_hashes=True)
    changed_files = _changes(previous_files, files)
    changed_criteria = _changes(_records(previous["criteria"], "id"), criteria)
    changed_checks = _changes(_records(previous["checks"], "id"), checks)
    owner_paths = [path for path in changed_files if PurePosixPath(path).name in _OWNER_ROLES]
    changed_check_sources = {scoped_paths([source])[0] for check in routing["checks"] for source in check["sources"]}
    owner_paths = sorted(set(owner_paths) | (set(changed_files) & changed_check_sources))
    dropped = [path for path in changed_files if files.get(path, "missing") == "missing"
               and previous_files.get(path, "missing") != "missing"]
    added = [path for path in changed_files if previous_files.get(path, "missing") == "missing"
             and files.get(path, "missing") != "missing"]
    destinations: dict[str, list[str]] = {}
    for path in added:
        destinations.setdefault(files[path], []).append(path)
    rename_candidates = []
    ambiguous_rename = False
    for old in dropped:
        matches = destinations.get(previous_files[old], [])
        if len(matches) == 1 and len(rename_candidates) < 200:
            rename_candidates.append({"from": old, "to": matches[0]})
        elif matches:
            ambiguous_rename = True
    affected = bool(changed_files or changed_criteria or changed_checks or scope != snapshot["scope"]
                    or previous["input_digest"] != snapshot["input_digest"])
    return {"snapshot": snapshot, "impact": {
        "status": "review_required" if affected else "unchanged",
        "changed_paths": changed_files, "changed_criteria": changed_criteria, "changed_checks": changed_checks,
        "affected_criteria": [{"id": row["id"], "owner": row["owner"]}
                              for row in decision["requirements"]["criteria"]] if affected else [],
        "checks_to_revalidate": sorted(checks) if affected else [],
        "owner_review_paths": owner_paths,
        "missing_owner_paths": sorted(set(dropped) & set(owner_paths)),
        "rename_candidates": rename_candidates, "rename_candidates_incomplete": ambiguous_rename,
        "semantic_coverage": "not_established",
        "previous_evidence": "stale" if affected else "requires_independent_verification",
        "next_action": "Review affected owners and refresh context, permissions and receipts" if affected else None,
    }}
