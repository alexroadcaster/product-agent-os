from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any

from product_agent_os.stage_manifest import canonical_json, content_digest


CONTROL_PLANE_FILES = ("REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md")
OPTIONAL_CONTROL_FILES = ("AGENTS.md", "README.md")
SOURCE_POLICY_FILES = ("REQUIREMENTS.md", "README.md", "RUNLOG.md")
SENSITIVE_DIR_NAMES = {".git", ".hg", ".svn", ".venv", "venv", "node_modules", "__pycache__"}
SENSITIVE_FILE_NAMES = {".env", ".env.local", ".envrc", "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
SENSITIVE_SUFFIXES = {".key", ".pem", ".p12", ".pfx", ".log"}
SENSITIVE_NAME_PARTS = ("secret", "token", "credential", "password", "private")
NO_ACTION_BOUNDARY_VALUE = "not_performed"
TARGET_FIXTURE_PACK_SCHEMA_VERSION = "target_fixture_pack_v1"


def build_target_fixture_pack(
    *,
    target_root: Path,
    target_label: str,
    test_id: str = "B39-TEST-M11",
    attempt_id: str = "B39-TEST-M11-A01",
    generated_at: str | None = None,
    development_stage: str = "idea_stage",
    architecture_complexity: str = "complex",
    lifecycle_state: str = "p2b_design_planning",
    usage_mode: str = "read_only_pilot_fixture",
    source_policy_status: str = "present_unverified",
) -> dict[str, Any]:
    """Build a redaction-safe Batch 39 target fixture pack."""

    if not target_root.exists() or not target_root.is_dir():
        raise ValueError("target root is not a directory")

    inventory_entries = _inventory_entries(target_root)
    file_entries = inventory_entries["included"]
    excluded_entries = inventory_entries["excluded"]
    control_plane = _control_plane(target_root)
    source_policy = _source_policy(target_root, source_policy_status)
    archetypes = _archetype_candidates(control_plane, file_entries, architecture_complexity)
    timestamp = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()

    pack = {
        "schema_version": TARGET_FIXTURE_PACK_SCHEMA_VERSION,
        "batch": "B39",
        "test_id": test_id,
        "attempt_id": attempt_id,
        "slice": "B39-S2",
        "generated_at": timestamp,
        "target": {
            "target_label": _safe_label(target_label),
            "target_ref": f"approved_target:{_safe_label(target_label)}",
            "target_kind": "local_workspace",
            "development_stage": development_stage,
            "lifecycle_state": lifecycle_state,
            "usage_mode": usage_mode,
            "architecture_complexity": architecture_complexity,
            "mutation_allowed": False,
        },
        "inventory": {
            "file_count": len(file_entries),
            "top_level_directory_count": _top_level_directory_count(target_root),
            "markdown_file_count": sum(1 for entry in file_entries if entry["path"].endswith(".md")),
            "non_markdown_file_count": sum(1 for entry in file_entries if not entry["path"].endswith(".md")),
            "git_repository_status": "present" if (target_root / ".git").exists() else "not_git_repository",
            "entries": file_entries,
            "excluded_entries": excluded_entries,
            "excluded_count": len(excluded_entries),
            "inventory_digest": content_digest(canonical_json(file_entries)),
        },
        "control_plane": control_plane,
        "source_policy": source_policy,
        "artifact_map": _artifact_map(file_entries),
        "design_signals": _design_signals(target_root, file_entries, control_plane),
        "archetype_candidates": archetypes,
        "safety_profile": {
            "safe_fixture_categories": [
                "relative_path",
                "file_size",
                "content_digest",
                "section_count",
                "citation_density_signal",
                "control_plane_presence",
                "architecture_keywords",
            ],
            "unsafe_content_exclusions": [
                "absolute_user_paths",
                "raw_private_source_bodies",
                "secrets",
                "raw_private_logs",
                "fresh_external_verification_claims",
            ],
            "source_freshness_status": "project_evidence_not_fresh_external_verification",
            "manual_verification_required": True,
        },
        "fixture_usage": {
            "feeds_tests": [
                "B39-TEST-M12",
                "B39-TEST-M13",
                "B39-TEST-M14",
                "B39-TEST-M16",
                "B39-TEST-M21",
            ],
            "safe_fixture_boundary": "relative_paths_digests_counts_only",
            "raw_source_bodies_stored": False,
        },
        "completion_skeptic": {
            "doubt_packet_ref": "none",
            "verdict": "not_run",
            "trigger": "not_applicable_fixture_pack",
            "failure_classes": [],
            "accepted_gap_refs": [],
            "scorecard_ref": "docs/superpowers/specs/scorecard-gates.example.json",
            "promotion_boundary": "manual_only_not_promoted",
        },
        "approval_boundary": _default_approval_boundary(),
        "redaction": {
            "local_absolute_paths_allowed": False,
            "raw_file_bodies_stored": False,
            "raw_private_logs_stored": False,
            "secrets_allowed": False,
        },
        "status": _status(control_plane=control_plane, source_policy=source_policy, excluded_entries=excluded_entries),
    }
    pack["fixture_pack_digest"] = content_digest(canonical_json(pack))
    return pack


def validate_target_fixture_pack(pack: dict[str, Any]) -> list[str]:
    if not isinstance(pack, dict):
        return ["fixture pack must be an object"]
    errors: list[str] = []
    for field in [
        "schema_version",
        "batch",
        "test_id",
        "attempt_id",
        "slice",
        "generated_at",
        "target",
        "inventory",
        "control_plane",
        "source_policy",
        "artifact_map",
        "design_signals",
        "archetype_candidates",
        "safety_profile",
        "fixture_usage",
        "completion_skeptic",
        "approval_boundary",
        "redaction",
        "status",
        "fixture_pack_digest",
    ]:
        if field not in pack:
            errors.append(f"{field} is required")
    if pack.get("schema_version") != TARGET_FIXTURE_PACK_SCHEMA_VERSION:
        errors.append(f"schema_version must be {TARGET_FIXTURE_PACK_SCHEMA_VERSION}")
    if pack.get("batch") != "B39":
        errors.append("batch must be B39")
    if pack.get("test_id") != "B39-TEST-M11":
        errors.append("test_id must be B39-TEST-M11")
    if pack.get("slice") != "B39-S2":
        errors.append("slice must be B39-S2")
    errors.extend(_validate_target(pack.get("target")))
    errors.extend(_validate_inventory(pack.get("inventory")))
    errors.extend(_validate_control_plane(pack.get("control_plane")))
    errors.extend(_validate_source_policy(pack.get("source_policy")))
    errors.extend(_validate_artifact_map(pack.get("artifact_map")))
    errors.extend(_validate_design_signals(pack.get("design_signals")))
    errors.extend(_validate_safety_profile(pack.get("safety_profile")))
    errors.extend(_validate_fixture_usage(pack.get("fixture_usage")))
    errors.extend(_validate_completion_skeptic(pack.get("completion_skeptic")))
    errors.extend(_validate_approval_boundary(pack.get("approval_boundary")))
    errors.extend(_validate_redaction(pack.get("redaction")))
    errors.extend(_validate_status(pack.get("status")))
    if not isinstance(pack.get("fixture_pack_digest"), str) or not pack.get("fixture_pack_digest", "").startswith("sha256:"):
        errors.append("fixture_pack_digest must be a sha256 digest")
    if _contains_local_absolute_path(pack):
        errors.append("local absolute path leaked")
    return errors


def _inventory_entries(target_root: Path) -> dict[str, list[dict[str, Any]]]:
    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for path in sorted(item for item in target_root.rglob("*") if item.is_file()):
        relative = _relative_path(path, target_root)
        exclusion_reason = _sensitive_path_reason(relative)
        if exclusion_reason:
            excluded.append(
                {
                    "path": _safe_excluded_path_ref(relative),
                    "category": "excluded_sensitive",
                    "reason": exclusion_reason,
                }
            )
            continue
        included.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "digest": content_digest(path.read_bytes()),
                "category": _file_category(relative),
            }
        )
    return {"included": included, "excluded": excluded}


def _control_plane(target_root: Path) -> dict[str, Any]:
    required = {name: (target_root / name).is_file() for name in CONTROL_PLANE_FILES}
    optional = {name: (target_root / name).is_file() for name in OPTIONAL_CONTROL_FILES}
    missing_required = sorted(name for name, present in required.items() if not present)
    return {
        "required_files": required,
        "optional_files": optional,
        "required_present_count": sum(1 for present in required.values() if present),
        "required_missing": missing_required,
        "status": "present" if not missing_required else "partial",
    }


def _source_policy(target_root: Path, source_policy_status: str) -> dict[str, Any]:
    candidate_refs = [name for name in SOURCE_POLICY_FILES if (target_root / name).is_file()]
    status = source_policy_status if source_policy_status in {"present", "present_unverified", "blocked", "accepted_gap"} else "present_unverified"
    return {
        "status": status,
        "candidate_refs": candidate_refs,
        "raw_source_bodies_stored": False,
        "source_truth_needs_owner_review": status != "present",
    }


def _archetype_candidates(
    control_plane: dict[str, Any],
    file_entries: list[dict[str, Any]],
    architecture_complexity: str,
) -> list[dict[str, str]]:
    paths = {entry["path"] for entry in file_entries}
    candidates = [
        {
            "archetype": "docs_research",
            "reason": "markdown-heavy target with source and control-plane documents",
            "recommended_test": "B39-TEST-M12",
        },
        {
            "archetype": "expected_block",
            "reason": "target is read-only and source policy remains owner-reviewed before any apply",
            "recommended_test": "B39-TEST-M13",
        },
    ]
    if architecture_complexity == "complex" or any(path.startswith("architecture") for path in paths):
        candidates.append(
            {
                "archetype": "ai_rag",
                "reason": "complex cognitive architecture and research/RAG/MCP signals are present",
                "recommended_test": "B39-TEST-M16",
            }
        )
    if any(path.startswith("docs/superpowers/") for path in paths) or control_plane["status"] == "present":
        candidates.append(
            {
                "archetype": "plugin_skill",
                "reason": "Product-Agent OS control-plane artifacts can exercise skill/plugin governance boundaries",
                "recommended_test": "B39-TEST-M21",
            }
        )
    return candidates


def _artifact_map(file_entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    return {
        "top_level_artifacts": sorted(entry["path"] for entry in file_entries if "/" not in entry["path"]),
        "control_plane_artifacts": sorted(entry["path"] for entry in file_entries if entry["category"] == "control_plane"),
        "architecture_artifacts": sorted(entry["path"] for entry in file_entries if entry["category"] == "architecture"),
        "research_artifacts": sorted(entry["path"] for entry in file_entries if entry["category"] == "research"),
        "legacy_artifacts": sorted(entry["path"] for entry in file_entries if entry["category"] == "legacy"),
    }


def _design_signals(
    target_root: Path,
    file_entries: list[dict[str, Any]],
    control_plane: dict[str, Any],
) -> dict[str, Any]:
    paths = {entry["path"] for entry in file_entries}
    return {
        "architecture_phase_count": _architecture_phase_count(target_root / "architecture-v2.md"),
        "legacy_architecture_phase_count": _architecture_phase_count(target_root / "architecture.md"),
        "citation_density_signal": _pattern_count(target_root / "architecture-v2.md", r"\[C[0-9]+\]"),
        "open_issue_count": _open_issue_count(target_root / "issues.md"),
        "design_complexity_flags": sorted(
            flag
            for flag, present in {
                "large_architecture_docs": any(
                    entry["category"] == "architecture" and entry["size_bytes"] > 30000 for entry in file_entries
                ),
                "research_corpus_present": any(path.startswith("research/") for path in paths),
                "legacy_lineage_present": any(path.startswith("legacy/") for path in paths),
                "control_plane_present": control_plane["status"] == "present",
                "docs_superpowers_history_present": any(path.startswith("docs/superpowers/") for path in paths),
                "implementation_code_absent": not any(
                    path.endswith((".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".cs")) for path in paths
                ),
            }.items()
            if present
        ),
    }


def _status(
    *,
    control_plane: dict[str, Any],
    source_policy: dict[str, Any],
    excluded_entries: list[dict[str, Any]],
) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    if control_plane["status"] != "present":
        blockers.append("target_control_plane_incomplete")
    if source_policy["status"] in {"blocked", "accepted_gap"}:
        blockers.append(f"source_policy_{source_policy['status']}")
    if source_policy["status"] == "present_unverified":
        warnings.append("source_policy_present_unverified_owner_review_required")
    if excluded_entries:
        warnings.append("sensitive_paths_excluded_from_inventory")
    return {
        "overall": "prepared_for_s2_pilots" if not blockers else "needs_attention",
        "open_blockers": blockers,
        "warnings": warnings,
        "next_test": "B39-TEST-M12",
    }


def _validate_target(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["target must be an object"]
    errors: list[str] = []
    for field in (
        "target_label",
        "target_ref",
        "target_kind",
        "development_stage",
        "lifecycle_state",
        "usage_mode",
        "architecture_complexity",
    ):
        if not isinstance(value.get(field), str) or not value.get(field):
            errors.append(f"target.{field} must be a non-empty string")
    if value.get("target_kind") != "local_workspace":
        errors.append("target.target_kind must be local_workspace")
    if value.get("mutation_allowed") is not False:
        errors.append("target.mutation_allowed must be false")
    return errors


def _validate_inventory(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["inventory must be an object"]
    errors: list[str] = []
    for field in ("file_count", "top_level_directory_count", "markdown_file_count", "non_markdown_file_count"):
        if not isinstance(value.get(field), int):
            errors.append(f"inventory.{field} must be integer")
    if value.get("git_repository_status") not in {"present", "not_git_repository"}:
        errors.append("inventory.git_repository_status missing or invalid")
    entries = value.get("entries")
    excluded_entries = value.get("excluded_entries")
    if not isinstance(entries, list):
        errors.append("inventory.entries must be list")
        entries = []
    elif value.get("file_count") != len(entries):
        errors.append("inventory.file_count must match entries length")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"inventory.entries[{index}] must be object")
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path:
            errors.append(f"inventory.entries[{index}].path must be a non-empty string")
        elif _looks_like_absolute_path(path) or ".." in PurePosixPath(path).parts:
            errors.append(f"inventory.entries[{index}].path must be safe relative path")
        if not isinstance(entry.get("digest"), str) or not entry.get("digest", "").startswith("sha256:"):
            errors.append(f"inventory.entries[{index}].digest must be sha256")
        if not isinstance(entry.get("size_bytes"), int):
            errors.append(f"inventory.entries[{index}].size_bytes must be integer")
        if entry.get("category") not in {"control_plane", "architecture", "research", "legacy", "docs", "other"}:
            errors.append(f"inventory.entries[{index}].category missing or invalid")
    if not isinstance(value.get("inventory_digest"), str) or not value.get("inventory_digest", "").startswith("sha256:"):
        errors.append("inventory.inventory_digest must be sha256")
    if not isinstance(value.get("excluded_count"), int):
        errors.append("inventory.excluded_count must be integer")
    if not isinstance(excluded_entries, list):
        errors.append("inventory.excluded_entries must be list")
        excluded_entries = []
    elif isinstance(value.get("excluded_count"), int) and value.get("excluded_count") != len(excluded_entries):
        errors.append("inventory.excluded_count must match excluded_entries length")
    for index, entry in enumerate(excluded_entries):
        if not isinstance(entry, dict):
            errors.append(f"inventory.excluded_entries[{index}] must be object")
            continue
        if entry.get("category") != "excluded_sensitive":
            errors.append(f"inventory.excluded_entries[{index}].category must be excluded_sensitive")
        if not isinstance(entry.get("path"), str) or not entry.get("path"):
            errors.append(f"inventory.excluded_entries[{index}].path must be non-empty string")
        if not isinstance(entry.get("reason"), str) or not entry.get("reason"):
            errors.append(f"inventory.excluded_entries[{index}].reason must be non-empty string")
    return errors


def _validate_control_plane(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["control_plane must be an object"]
    errors: list[str] = []
    if value.get("status") not in {"present", "partial"}:
        errors.append("control_plane.status missing or invalid")
    if not isinstance(value.get("required_files"), dict):
        errors.append("control_plane.required_files must be object")
    if not isinstance(value.get("optional_files"), dict):
        errors.append("control_plane.optional_files must be object")
    if not isinstance(value.get("required_present_count"), int):
        errors.append("control_plane.required_present_count must be integer")
    if not isinstance(value.get("required_missing"), list):
        errors.append("control_plane.required_missing must be list")
    return errors


def _validate_source_policy(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["source_policy must be an object"]
    errors: list[str] = []
    if value.get("status") not in {"present", "present_unverified", "blocked", "accepted_gap"}:
        errors.append("source_policy.status missing or invalid")
    if not isinstance(value.get("candidate_refs"), list):
        errors.append("source_policy.candidate_refs must be list")
    if value.get("raw_source_bodies_stored") is not False:
        errors.append("source_policy.raw_source_bodies_stored must be false")
    if not isinstance(value.get("source_truth_needs_owner_review"), bool):
        errors.append("source_policy.source_truth_needs_owner_review must be boolean")
    return errors


def _validate_artifact_map(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["artifact_map must be an object"]
    errors: list[str] = []
    for field in (
        "top_level_artifacts",
        "control_plane_artifacts",
        "architecture_artifacts",
        "research_artifacts",
        "legacy_artifacts",
    ):
        if not isinstance(value.get(field), list):
            errors.append(f"artifact_map.{field} must be list")
    return errors


def _validate_design_signals(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["design_signals must be an object"]
    errors: list[str] = []
    for field in (
        "architecture_phase_count",
        "legacy_architecture_phase_count",
        "citation_density_signal",
        "open_issue_count",
    ):
        if not isinstance(value.get(field), int):
            errors.append(f"design_signals.{field} must be integer")
    if not isinstance(value.get("design_complexity_flags"), list):
        errors.append("design_signals.design_complexity_flags must be list")
    return errors


def _validate_safety_profile(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["safety_profile must be an object"]
    errors: list[str] = []
    for field in ("safe_fixture_categories", "unsafe_content_exclusions"):
        if not isinstance(value.get(field), list):
            errors.append(f"safety_profile.{field} must be list")
    if value.get("source_freshness_status") != "project_evidence_not_fresh_external_verification":
        errors.append("safety_profile.source_freshness_status missing or invalid")
    if value.get("manual_verification_required") is not True:
        errors.append("safety_profile.manual_verification_required must be true")
    return errors


def _validate_fixture_usage(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["fixture_usage must be an object"]
    errors: list[str] = []
    if not isinstance(value.get("feeds_tests"), list):
        errors.append("fixture_usage.feeds_tests must be list")
    if value.get("safe_fixture_boundary") != "relative_paths_digests_counts_only":
        errors.append("fixture_usage.safe_fixture_boundary missing or invalid")
    if value.get("raw_source_bodies_stored") is not False:
        errors.append("fixture_usage.raw_source_bodies_stored must be false")
    return errors


def _validate_completion_skeptic(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["completion_skeptic must be an object"]
    errors: list[str] = []
    if value.get("verdict") not in {"not_run", "blocked", "accepted_gap", "pass"}:
        errors.append("completion_skeptic.verdict missing or invalid")
    if value.get("promotion_boundary") != "manual_only_not_promoted":
        errors.append("completion_skeptic.promotion_boundary must be manual_only_not_promoted")
    for field in ("failure_classes", "accepted_gap_refs"):
        if not isinstance(value.get(field), list):
            errors.append(f"completion_skeptic.{field} must be list")
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
    for field in ("local_absolute_paths_allowed", "raw_file_bodies_stored", "raw_private_logs_stored", "secrets_allowed"):
        if value.get(field) is not False:
            errors.append(f"redaction.{field} must be false")
    return errors


def _validate_status(value: Any) -> list[str]:
    if not isinstance(value, dict):
        return ["status must be an object"]
    errors: list[str] = []
    if value.get("overall") not in {"prepared_for_s2_pilots", "needs_attention"}:
        errors.append("status.overall missing or invalid")
    if not isinstance(value.get("open_blockers"), list):
        errors.append("status.open_blockers must be list")
    if not isinstance(value.get("warnings"), list):
        errors.append("status.warnings must be list")
    if not isinstance(value.get("next_test"), str):
        errors.append("status.next_test must be string")
    return errors


def _default_approval_boundary() -> dict[str, str]:
    return {
        "target_workspace_mutation": NO_ACTION_BOUNDARY_VALUE,
        "provider_or_api_calls": NO_ACTION_BOUNDARY_VALUE,
        "browser_automation": NO_ACTION_BOUNDARY_VALUE,
        "live_server": NO_ACTION_BOUNDARY_VALUE,
        "cache_mutation": NO_ACTION_BOUNDARY_VALUE,
        "external_actions": NO_ACTION_BOUNDARY_VALUE,
        "git_actions": NO_ACTION_BOUNDARY_VALUE,
        "automation_activation": NO_ACTION_BOUNDARY_VALUE,
        "local_evidence_artifact_write": "allowed_workspace_output_only",
    }


def _file_category(relative_path: str) -> str:
    if relative_path in CONTROL_PLANE_FILES or relative_path in OPTIONAL_CONTROL_FILES:
        return "control_plane"
    if relative_path.startswith("architecture") or "/architecture" in relative_path:
        return "architecture"
    if relative_path.startswith("research/"):
        return "research"
    if relative_path.startswith("legacy/"):
        return "legacy"
    if relative_path.startswith("docs/"):
        return "docs"
    return "other"


def _relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _top_level_directory_count(target_root: Path) -> int:
    return sum(1 for item in target_root.iterdir() if item.is_dir())


def _safe_label(value: str) -> str:
    label = value.strip().replace("\\", "_").replace("/", "_").replace(":", "_")
    return label or "target"


def _sensitive_path_reason(relative_path: str) -> str | None:
    parts = PurePosixPath(relative_path).parts
    lowered_parts = [part.lower() for part in parts]
    name = lowered_parts[-1] if lowered_parts else ""
    stem = Path(name).stem
    suffix = Path(name).suffix
    if any(part in SENSITIVE_DIR_NAMES for part in lowered_parts[:-1]):
        return "sensitive_directory"
    if name in SENSITIVE_FILE_NAMES:
        return "sensitive_filename"
    if suffix in SENSITIVE_SUFFIXES:
        return "sensitive_suffix"
    if any(marker in stem for marker in SENSITIVE_NAME_PARTS):
        return "sensitive_name"
    return None


def _safe_excluded_path_ref(relative_path: str) -> str:
    parts = PurePosixPath(relative_path).parts
    if not parts:
        return "excluded"
    redacted_name = "redacted_sensitive_file"
    if len(parts) == 1:
        return redacted_name
    return str(PurePosixPath(*parts[:-1], redacted_name))


def _architecture_phase_count(path: Path) -> int:
    return _pattern_count(path, r"^## ")


def _open_issue_count(path: Path) -> int:
    if not path.is_file():
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    return len(re.findall(r"(?m)^\s*[-*]\s+(?:\[ \]\s+)?", text))


def _pattern_count(path: Path, pattern: str) -> int:
    if not path.is_file():
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0
    return len(re.findall(pattern, text, flags=re.MULTILINE))


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


__all__ = ["build_target_fixture_pack", "validate_target_fixture_pack"]
