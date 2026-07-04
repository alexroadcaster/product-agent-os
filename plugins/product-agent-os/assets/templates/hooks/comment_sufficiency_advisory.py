from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx"}
DISABLE_ENV = "B45_COMMENT_ADVISORY_DISABLED"
ROOT_ENV = "B45_COMMENT_ADVISORY_ROOT"
MAX_CHANGED_FILES = 20


def _workspace_root() -> tuple[Path | None, str | None]:
    """Resolve the target workspace while keeping the hook reusable in temp test repos."""
    env_root = os.environ.get(ROOT_ENV)
    if env_root:
        candidate = Path(env_root).resolve()
        if not candidate.exists() or not candidate.is_dir():
            return None, "env_root_missing_or_not_directory"
        return candidate, None
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        result = None
    if result and result.returncode == 0 and result.stdout.strip():
        candidate = Path(result.stdout.strip()).resolve()
        if candidate.exists() and candidate.is_dir():
            return candidate, None
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex").exists():
            return candidate, None
    return current, None


def _script_repo_root() -> Path:
    script_path = Path(__file__).resolve()
    for candidate in script_path.parents:
        if (candidate / "plugins" / "product-agent-os" / "scripts").exists():
            return candidate
    return script_path.parents[2]


def _load_validator(repo_root: Path) -> tuple[Any | None, Any | None, str]:
    """Load the local validator if available, otherwise fail open with a diagnostic."""
    candidates = [
        ("workspace_plugin", repo_root / "plugins" / "product-agent-os" / "scripts"),
        ("packaged_plugin", _script_repo_root() / "plugins" / "product-agent-os" / "scripts"),
    ]
    for source_ref, scripts_dir in candidates:
        scripts_dir = scripts_dir.resolve()
        if not (scripts_dir / "product_agent_os" / "comment_sufficiency.py").exists():
            continue
        sys.path.insert(0, str(scripts_dir))
        try:
            from product_agent_os.comment_sufficiency import advisory_payload, analyze_paths

            return analyze_paths, advisory_payload, source_ref
        except Exception:
            continue
        finally:
            try:
                sys.path.remove(str(scripts_dir))
            except ValueError:
                pass
    return None, None, "comment_sufficiency_validator_not_found"


def _git_lines(root: Path, args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _changed_paths(root: Path) -> list[Path]:
    seen: set[Path] = set()
    relative_paths: list[str] = []
    relative_paths.extend(_git_lines(root, ["diff", "--name-only", "--diff-filter=ACMR"]))
    relative_paths.extend(_git_lines(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"]))
    relative_paths.extend(_git_lines(root, ["ls-files", "--others", "--exclude-standard"]))
    for relative in relative_paths:
        path = (root / relative).resolve()
        if path in seen or not path.exists() or path.suffix not in SUPPORTED_SUFFIXES:
            continue
        seen.add(path)
    return sorted(seen, key=lambda item: item.as_posix())


def _display_paths(paths: Iterable[Path], root: Path) -> list[str]:
    result: list[str] = []
    for path in paths:
        try:
            result.append(path.relative_to(root).as_posix())
        except ValueError:
            result.append(f"<outside-workspace>/{path.name}")
    return result


def _workspace_ref(root: Path | None) -> str:
    if root is None:
        return "unresolved"
    digest = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:12]
    return f"{root.name}:{digest}"


def _redact_message(message: str, root: Path) -> str:
    redacted = message.replace(str(root), "<workspace>")
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        redacted = redacted.replace(user_profile, "<userprofile>")
    return redacted


def main() -> int:
    """Run changed-file comment-sufficiency checks as a non-blocking PostToolUse signal."""
    event = sys.stdin.read()
    root, root_error = _workspace_root()
    disabled = os.environ.get(DISABLE_ENV, "").lower() in {"1", "true", "yes"}
    base_payload: dict[str, object] = {
        "hook": "comment_sufficiency_advisory",
        "decision": "observe",
        "blocking": False,
        "input_bytes": len(event.encode("utf-8")),
        "mode": "changed_files_tuned_default",
        "workspace_ref": _workspace_ref(root),
        "raw_workspace_path_included": False,
        "disable_env": DISABLE_ENV,
    }
    if disabled:
        print(json.dumps({**base_payload, "status": "disabled"}, sort_keys=True))
        return 0
    if root is None:
        print(
            json.dumps(
                {
                    **base_payload,
                    "status": "invalid_workspace_root_fail_open",
                    "root_error": root_error,
                    "notes": ["Advisory hook failed open; comment sufficiency is not enforced."],
                },
                sort_keys=True,
            )
        )
        return 0

    analyze_paths, advisory_payload, validator_source_ref = _load_validator(root)
    if analyze_paths is None or advisory_payload is None:
        print(
            json.dumps(
                {
                    **base_payload,
                    "status": "validator_unavailable",
                    "validator_source_ref": validator_source_ref,
                    "notes": ["Advisory hook failed open; comment sufficiency is not enforced."],
                },
                sort_keys=True,
            )
        )
        return 0

    changed = _changed_paths(root)
    if len(changed) > MAX_CHANGED_FILES:
        print(
            json.dumps(
                {
                    **base_payload,
                    "status": "skipped_too_many_changed_files",
                    "changed_file_count": len(changed),
                    "max_changed_files": MAX_CHANGED_FILES,
                    "notes": ["Run the comment_sufficiency.py CLI manually for broad audits."],
                },
                sort_keys=True,
            )
        )
        return 0

    try:
        warnings = analyze_paths(changed, root=root)
        payload = advisory_payload(warnings)
    except Exception as exc:
        print(
            json.dumps(
                {
                    **base_payload,
                    "status": "validator_error_fail_open",
                    "changed_file_count": len(changed),
                    "scanned_paths": _display_paths(changed, root),
                    "validator_source_ref": validator_source_ref,
                    "error_type": type(exc).__name__,
                    "error_message": _redact_message(str(exc), root),
                    "notes": ["Advisory hook failed open; comment sufficiency is not enforced."],
                },
                sort_keys=True,
            )
        )
        return 0
    print(
        json.dumps(
            {
                **base_payload,
                "status": "advisory_complete",
                "changed_file_count": len(changed),
                "scanned_paths": _display_paths(changed, root),
                "validator_source_ref": validator_source_ref,
                "validator": payload,
                "notes": [
                    "Warnings are reviewer signals only.",
                    "The hook exits 0 and must not be used as blocker proof.",
                    "Use raw CLI replay for broad false-positive audits.",
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
