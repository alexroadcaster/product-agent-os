from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_SUFFIXES = {".py", ".js", ".mjs", ".cjs"}
DISABLE_ENV = "B45_COMMENT_ADVISORY_DISABLED"
ROOT_ENV = "B45_COMMENT_ADVISORY_ROOT"
MAX_CHANGED_FILES = 20


def _workspace_root() -> Path:
    """Resolve the target workspace while keeping the hook reusable in temp test repos."""
    env_root = os.environ.get(ROOT_ENV)
    if env_root:
        return Path(env_root).resolve()
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
        return Path(result.stdout.strip()).resolve()
    current = Path.cwd().resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".codex").exists():
            return candidate
    return current


def _script_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_validator(repo_root: Path) -> tuple[Any | None, Any | None, str]:
    """Load the local validator if available, otherwise fail open with a diagnostic."""
    candidates = [
        repo_root / "plugins" / "product-agent-os" / "scripts",
        _script_repo_root() / "plugins" / "product-agent-os" / "scripts",
    ]
    for scripts_dir in candidates:
        if not (scripts_dir / "product_agent_os" / "comment_sufficiency.py").exists():
            continue
        sys.path.insert(0, str(scripts_dir))
        try:
            from product_agent_os.comment_sufficiency import advisory_payload, analyze_paths

            return analyze_paths, advisory_payload, str(scripts_dir)
        except ImportError:
            continue
    return None, None, "comment_sufficiency validator not found"


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
            result.append(str(path))
    return result


def main() -> int:
    """Run changed-file comment-sufficiency checks as a non-blocking PostToolUse signal."""
    event = sys.stdin.read()
    root = _workspace_root()
    disabled = os.environ.get(DISABLE_ENV, "").lower() in {"1", "true", "yes"}
    base_payload: dict[str, object] = {
        "hook": "comment_sufficiency_advisory",
        "decision": "observe",
        "blocking": False,
        "input_bytes": len(event.encode("utf-8")),
        "mode": "changed_files_tuned_default",
        "workspace_root": str(root),
        "disable_env": DISABLE_ENV,
    }
    if disabled:
        print(json.dumps({**base_payload, "status": "disabled"}, sort_keys=True))
        return 0

    analyze_paths, advisory_payload, validator_source = _load_validator(root)
    if analyze_paths is None or advisory_payload is None:
        print(
            json.dumps(
                {
                    **base_payload,
                    "status": "validator_unavailable",
                    "validator_source": validator_source,
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

    warnings = analyze_paths(changed, root=root)
    payload = advisory_payload(warnings)
    print(
        json.dumps(
            {
                **base_payload,
                "status": "advisory_complete",
                "changed_file_count": len(changed),
                "scanned_paths": _display_paths(changed, root),
                "validator_source": validator_source,
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
