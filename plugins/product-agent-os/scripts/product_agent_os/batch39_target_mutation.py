from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


NO_ACTION_BOUNDARY_VALUE = "not_performed"
TARGET_MUTATION_PROOF_SCHEMA_VERSION = "target_mutation_proof_v1"


def build_target_mutation_proof(
    *,
    test_id: str,
    attempt_id: str,
    before_root: Path,
    after_root: Path,
    target_ref: str,
    generated_at: str | None = None,
    mutation_allowed: bool = False,
    approval_ref: str = "none",
) -> dict[str, Any]:
    """Build a redaction-safe pre/post target mutation proof."""

    before_snapshot = snapshot_target(before_root, root_ref="before")
    after_snapshot = snapshot_target(after_root, root_ref="after")
    diff = compare_snapshots(before_snapshot, after_snapshot)
    proof = {
        "schema_version": TARGET_MUTATION_PROOF_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "generated_at": generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        "target": {
            "target_ref": _safe_ref(target_ref),
            "target_kind": "fixture_or_project_snapshot",
            "mutation_allowed": mutation_allowed,
            "approval_ref": approval_ref,
        },
        "before_snapshot": before_snapshot,
        "after_snapshot": after_snapshot,
        "diff": diff,
        "approval_boundary": _default_approval_boundary(),
        "redaction": {
            "absolute_paths_stored": False,
            "raw_file_bodies_stored": False,
            "secrets_allowed": False,
        },
        "verdict": _verdict(diff=diff, mutation_allowed=mutation_allowed, approval_ref=approval_ref),
    }
    proof["proof_digest"] = content_digest(canonical_json(proof))
    return proof


def snapshot_target(root: Path, *, root_ref: str) -> dict[str, Any]:
    if not root.exists() or not root.is_dir():
        raise ValueError(f"target root is not a directory: {root_ref}")
    entries = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative_path = _relative_posix_path(path, root)
        entries.append(
            {
                "path": relative_path,
                "digest": content_digest(path.read_bytes()),
                "size_bytes": path.stat().st_size,
            }
        )
    snapshot = {
        "root_ref": root_ref,
        "file_count": len(entries),
        "entries": entries,
    }
    snapshot["snapshot_digest"] = content_digest(canonical_json(snapshot))
    return snapshot


def compare_snapshots(before_snapshot: dict[str, Any], after_snapshot: dict[str, Any]) -> dict[str, Any]:
    before = {entry["path"]: entry for entry in before_snapshot.get("entries", [])}
    after = {entry["path"]: entry for entry in after_snapshot.get("entries", [])}
    before_paths = set(before)
    after_paths = set(after)
    added = sorted(after_paths - before_paths)
    deleted = sorted(before_paths - after_paths)
    modified = sorted(
        path
        for path in before_paths & after_paths
        if before[path].get("digest") != after[path].get("digest")
        or before[path].get("size_bytes") != after[path].get("size_bytes")
    )
    return {
        "status": "changed" if added or deleted or modified else "unchanged",
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "counts": {
            "added": len(added),
            "modified": len(modified),
            "deleted": len(deleted),
        },
    }


def validate_target_mutation_proof(proof: dict[str, Any]) -> list[str]:
    if not isinstance(proof, dict):
        return ["proof must be an object"]
    errors: list[str] = []
    for field in [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "generated_at",
        "target",
        "before_snapshot",
        "after_snapshot",
        "diff",
        "approval_boundary",
        "redaction",
        "verdict",
        "proof_digest",
    ]:
        if field not in proof:
            errors.append(f"{field} is required")
    if proof.get("schema_version") != TARGET_MUTATION_PROOF_SCHEMA_VERSION:
        errors.append(f"schema_version must be {TARGET_MUTATION_PROOF_SCHEMA_VERSION}")
    if proof.get("batch") != "B39":
        errors.append("batch must be B39")
    for field in ("test_id", "attempt_id", "generated_at"):
        if not isinstance(proof.get(field), str) or not proof.get(field):
            errors.append(f"{field} must be a non-empty string")
    errors.extend(_validate_target(proof.get("target")))
    errors.extend(_validate_snapshot(proof.get("before_snapshot"), "before_snapshot"))
    errors.extend(_validate_snapshot(proof.get("after_snapshot"), "after_snapshot"))
    errors.extend(_validate_diff(proof.get("diff")))
    errors.extend(_validate_approval_boundary(proof.get("approval_boundary")))
    errors.extend(_validate_redaction(proof.get("redaction")))
    if proof.get("verdict") not in {"no_mutation_detected", "approved_mutation_detected", "unapproved_mutation_detected"}:
        errors.append("verdict missing or invalid")
    if not isinstance(proof.get("proof_digest"), str) or not proof.get("proof_digest", "").startswith("sha256:"):
        errors.append("proof_digest must be a sha256 digest")
    if _contains_local_absolute_path(proof):
        errors.append("local absolute path leaked")
    target = proof.get("target") if isinstance(proof.get("target"), dict) else {}
    diff = proof.get("diff") if isinstance(proof.get("diff"), dict) else {}
    if diff.get("status") == "changed" and target.get("mutation_allowed") is not True:
        errors.append("unapproved target mutation detected")
    if target.get("mutation_allowed") is True and target.get("approval_ref") == "none":
        errors.append("mutation_allowed requires approval_ref")
    return errors


def _validate_target(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["target must be an object"]
    errors: list[str] = []
    if not isinstance(value.get("target_ref"), str) or not value.get("target_ref"):
        errors.append("target.target_ref must be a non-empty string")
    if value.get("target_kind") != "fixture_or_project_snapshot":
        errors.append("target.target_kind must be fixture_or_project_snapshot")
    if not isinstance(value.get("mutation_allowed"), bool):
        errors.append("target.mutation_allowed must be boolean")
    if not isinstance(value.get("approval_ref"), str) or not value.get("approval_ref"):
        errors.append("target.approval_ref must be a non-empty string")
    return errors


def _validate_snapshot(value: Any, name: str) -> list[str]:
    if not isinstance(value, dict):
        return [f"{name} must be an object"]
    errors: list[str] = []
    if not isinstance(value.get("root_ref"), str) or not value.get("root_ref"):
        errors.append(f"{name}.root_ref must be a non-empty string")
    if not isinstance(value.get("file_count"), int):
        errors.append(f"{name}.file_count must be integer")
    entries = value.get("entries")
    if not isinstance(entries, list):
        errors.append(f"{name}.entries must be list")
        entries = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{name}.entries[{index}] must be object")
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"{name}.entries[{index}].path must be a non-empty string")
        elif _looks_like_absolute_path(path) or ".." in PurePosixPath(path).parts:
            errors.append(f"{name}.entries[{index}].path must be safe relative path")
        if not isinstance(entry.get("digest"), str) or not entry.get("digest", "").startswith("sha256:"):
            errors.append(f"{name}.entries[{index}].digest must be a sha256 digest")
        if not isinstance(entry.get("size_bytes"), int):
            errors.append(f"{name}.entries[{index}].size_bytes must be integer")
    if value.get("file_count") != len(entries):
        errors.append(f"{name}.file_count must match entries length")
    if not isinstance(value.get("snapshot_digest"), str) or not value.get("snapshot_digest", "").startswith("sha256:"):
        errors.append(f"{name}.snapshot_digest must be a sha256 digest")
    return errors


def _validate_diff(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["diff must be an object"]
    errors: list[str] = []
    if value.get("status") not in {"unchanged", "changed"}:
        errors.append("diff.status missing or invalid")
    for field in ("added", "modified", "deleted"):
        if not isinstance(value.get(field), list):
            errors.append(f"diff.{field} must be list")
    counts = value.get("counts")
    if not isinstance(counts, dict):
        errors.append("diff.counts must be object")
        return errors
    for field in ("added", "modified", "deleted"):
        if not isinstance(counts.get(field), int):
            errors.append(f"diff.counts.{field} must be integer")
        elif isinstance(value.get(field), list) and counts.get(field) != len(value.get(field)):
            errors.append(f"diff.counts.{field} must match diff.{field} length")
    return errors


def _validate_approval_boundary(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["approval_boundary must be an object"]
    errors: list[str] = []
    expected = _default_approval_boundary()
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            errors.append(f"approval_boundary.{field} must be {expected_value}")
    return errors


def _validate_redaction(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["redaction must be an object"]
    errors: list[str] = []
    for field in ("absolute_paths_stored", "raw_file_bodies_stored", "secrets_allowed"):
        if value.get(field) is not False:
            errors.append(f"redaction.{field} must be false")
    return errors


def _default_approval_boundary() -> dict[str, str]:
    return {
        "target_workspace_mutation": NO_ACTION_BOUNDARY_VALUE,
        "mcp_server_activation": NO_ACTION_BOUNDARY_VALUE,
        "agents_sdk_runner_activation": NO_ACTION_BOUNDARY_VALUE,
        "canonical_graph_mutation": NO_ACTION_BOUNDARY_VALUE,
        "provider_or_api_calls": NO_ACTION_BOUNDARY_VALUE,
        "browser_automation": NO_ACTION_BOUNDARY_VALUE,
        "live_server": NO_ACTION_BOUNDARY_VALUE,
        "cache_mutation": NO_ACTION_BOUNDARY_VALUE,
        "external_actions": NO_ACTION_BOUNDARY_VALUE,
        "git_actions": NO_ACTION_BOUNDARY_VALUE,
        "automation_activation": NO_ACTION_BOUNDARY_VALUE,
        "local_evidence_artifact_write": "allowed_workspace_output_only",
    }


def _verdict(*, diff: dict[str, Any], mutation_allowed: bool, approval_ref: str) -> str:
    if diff.get("status") != "changed":
        return "no_mutation_detected"
    if mutation_allowed and approval_ref != "none":
        return "approved_mutation_detected"
    return "unapproved_mutation_detected"


def _relative_posix_path(path: Path, root: Path) -> str:
    return str(PurePosixPath(path.relative_to(root).as_posix()))


def _safe_ref(value: str) -> str:
    normalized = str(PurePosixPath(value.replace("\\", "/")))
    if _looks_like_absolute_path(normalized):
        return "redacted_absolute_path"
    return normalized


def _contains_local_absolute_path(payload: Any) -> bool:
    if isinstance(payload, str):
        return _looks_like_absolute_path(payload)
    if isinstance(payload, dict):
        return any(_contains_local_absolute_path(key) or _contains_local_absolute_path(value) for key, value in payload.items())
    if isinstance(payload, list):
        return any(_contains_local_absolute_path(item) for item in payload)
    return False


def _looks_like_absolute_path(value: str) -> bool:
    normalized = value.strip()
    if len(normalized) >= 3 and normalized[1] == ":" and normalized[2] in {"\\", "/"} and normalized[0].isalpha():
        return True
    if normalized.startswith("\\\\") or normalized.startswith("//"):
        return True
    if normalized.startswith("/"):
        return True
    return False


__all__ = [
    "TARGET_MUTATION_PROOF_SCHEMA_VERSION",
    "build_target_mutation_proof",
    "compare_snapshots",
    "snapshot_target",
    "validate_target_mutation_proof",
]
