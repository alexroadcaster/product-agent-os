"""Read-only file manifest and freshness model for project code graphs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


_SKIPPED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".mkdocs_task22_site",
    ".mkdocs_task23_site",
    ".understand-anything",
}
_LANGUAGE_BY_SUFFIX = {
    ".py": "python",
    ".md": "markdown",
    ".markdown": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".json": "json",
    ".sql": "sql",
    ".dbml": "dbml",
    ".toml": "toml",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".plantuml": "plantuml",
    ".puml": "plantuml",
}


def collect_project_files(workspace: str | Path, *, max_files: int = 10_000) -> list[dict[str, Any]]:
    """Collect bounded file metadata for graph scanning without reading raw bodies into artifacts."""

    root = Path(workspace).resolve()
    files: list[dict[str, Any]] = []
    omitted_count = 0
    truncated = False
    for path in _iter_project_file_candidates(root):
        if _should_skip(path, root) or path.is_symlink():
            omitted_count += 1
            continue
        if not path.is_file():
            continue
        relative = _relative_path(root, path)
        if not relative:
            omitted_count += 1
            continue
        if len(files) >= max_files:
            omitted_count += 1
            truncated = True
            continue
        try:
            stat = path.stat()
            fingerprint = file_fingerprint(path)
        except OSError:
            omitted_count += 1
            continue
        files.append(
            {
                "relative_path": relative,
                "fingerprint": fingerprint,
                "size_bytes": stat.st_size,
                "language": _language_for_path(relative),
                "generated": _is_generated(relative),
                "low_value": _is_low_value(relative),
            }
        )
    if files and (truncated or omitted_count):
        files[-1]["collection_truncated"] = truncated
        files[-1]["omitted_count"] = omitted_count
    return files


def build_project_graph_manifest(
    workspace: str | Path,
    project_files: list[dict[str, Any]],
    *,
    previous_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a redaction-safe graph manifest with freshness and provenance metadata."""

    root = Path(workspace).resolve()
    normalized_files = sorted(
        [_file_manifest_item(item) for item in project_files],
        key=lambda item: item["relative_path"],
    )
    root_fingerprint = _content_digest(
        json.dumps(
            [(item["relative_path"], item["fingerprint"]) for item in normalized_files],
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    previous_files = {
        item["relative_path"]: item
        for item in (previous_manifest or {}).get("files", [])
        if isinstance(item, dict) and item.get("relative_path")
    }
    changes = _changes(previous_files, {item["relative_path"]: item for item in normalized_files})
    status = (
        "current"
        if previous_manifest is None or not (changes["changed"] or changes["added"] or changes["deleted"])
        else "changed"
    )
    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "workspace": {
            "name": root.name,
            "root_status": "redacted",
        },
        "provenance": _git_provenance(root),
        "build_metadata": {
            "builder": "product-agent-os-project-code-graph",
            "schema_version": 1,
            "mode": "read_only",
        },
        "root_fingerprint": root_fingerprint,
        "files": normalized_files,
        "changes": changes,
        "freshness": {
            "status": status,
            "previous_root_fingerprint": str((previous_manifest or {}).get("root_fingerprint") or ""),
            "current_root_fingerprint": root_fingerprint,
        },
        "summary": {
            "file_count": len(normalized_files),
            "generated_count": sum(1 for item in normalized_files if item["generated"]),
            "low_value_count": sum(1 for item in normalized_files if item["low_value"]),
            "by_language": _counts(normalized_files, "language"),
            "truncated": any(bool(item.get("collection_truncated")) for item in project_files),
            "omitted_count": sum(int(item.get("omitted_count") or 0) for item in project_files),
        },
    }


def file_fingerprint(path: str | Path) -> str:
    """Return a stable sha256 fingerprint for a file."""

    hasher = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return "sha256:" + hasher.hexdigest()


def _file_manifest_item(item: dict[str, Any]) -> dict[str, Any]:
    relative = str(item.get("relative_path") or "")
    return {
        "relative_path": relative,
        "fingerprint": str(item.get("fingerprint") or ""),
        "size_bytes": int(item.get("size_bytes") or 0),
        "language": str(item.get("language") or _language_for_path(relative)),
        "generated": bool(item.get("generated")),
        "low_value": bool(item.get("low_value")),
        "collection_truncated": bool(item.get("collection_truncated")),
        "omitted_count": int(item.get("omitted_count") or 0),
    }


def _changes(previous: dict[str, dict[str, Any]], current: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    previous_paths = set(previous)
    current_paths = set(current)
    unchanged = [
        path
        for path in sorted(previous_paths & current_paths)
        if previous[path].get("fingerprint") == current[path].get("fingerprint")
    ]
    changed = [
        path
        for path in sorted(previous_paths & current_paths)
        if previous[path].get("fingerprint") != current[path].get("fingerprint")
    ]
    return {
        "unchanged": unchanged,
        "changed": changed,
        "added": sorted(current_paths - previous_paths),
        "deleted": sorted(previous_paths - current_paths),
    }


def _should_skip(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in _SKIPPED_DIRS for part in relative_parts)


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return ""


def _iter_project_file_candidates(root: Path):
    for current_root, dir_names, file_names in os.walk(root):
        dir_names[:] = sorted(name for name in dir_names if name not in _SKIPPED_DIRS)
        for file_name in sorted(file_names):
            yield Path(current_root) / file_name


def _language_for_path(value: str) -> str:
    path = Path(value)
    lowered = value.lower()
    if lowered.endswith((".openapi.yaml", ".openapi.yml")) or path.name in {"openapi.yaml", "openapi.yml"}:
        return "yaml"
    return _LANGUAGE_BY_SUFFIX.get(path.suffix.lower(), "unknown")


def _is_generated(value: str) -> bool:
    lowered = value.lower()
    name = Path(value).name.lower()
    return (
        ".generated." in lowered
        or name.endswith(".generated")
        or name.endswith(".lock")
        or "generated/" in lowered
        or lowered.startswith("generated/")
    )


def _is_low_value(value: str) -> bool:
    lowered = value.lower()
    return any(part in lowered for part in ["/coverage/", "/tmp/", "/cache/"]) or lowered.endswith((".log", ".tmp"))


def _git_provenance(root: Path) -> dict[str, str]:
    git_dir, worktree = _git_dir(root)
    branch = "unknown"
    commit = "unknown"
    head = git_dir / "HEAD" if git_dir is not None else Path()
    if head.exists() and head.is_file():
        try:
            head_value = head.read_text(encoding="utf-8").strip()
        except OSError:
            head_value = ""
        if head_value.startswith("ref: "):
            ref = head_value.removeprefix("ref: ").strip()
            branch = ref.split("/")[-1] if ref else "unknown"
            ref_path = git_dir / ref
            if ref_path.exists() and ref_path.is_file():
                try:
                    commit_value = ref_path.read_text(encoding="utf-8").strip()
                except OSError:
                    commit_value = ""
                if _valid_commit(commit_value):
                    commit = commit_value
        elif _valid_commit(head_value):
            commit = head_value
            branch = "detached"
    return {
        "branch": branch,
        "commit": commit,
        "worktree": worktree,
    }


def _git_dir(root: Path) -> tuple[Path | None, str]:
    git_marker = root / ".git"
    if git_marker.is_dir():
        return git_marker, "present"
    if git_marker.is_file():
        try:
            text = git_marker.read_text(encoding="utf-8").strip()
        except OSError:
            return None, "unknown"
        if text.startswith("gitdir:"):
            value = text.removeprefix("gitdir:").strip()
            path = Path(value)
            if not path.is_absolute():
                path = (root / path).resolve()
            return path, "linked"
    return None, "unknown"


def _valid_commit(value: str) -> bool:
    return len(value) == 40 and all(char in "0123456789abcdefABCDEF" for char in value)


def _counts(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _content_digest(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode("utf-8")
    return "sha256:" + hashlib.sha256(content).hexdigest()
