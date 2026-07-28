from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx"}
DISABLE_ENV = "CODEX_COMMENT_ADVISORY_DISABLED"
ROOT_ENV = "CODEX_COMMENT_ADVISORY_ROOT"
LEGACY_DISABLE_ENV = "B45_COMMENT_ADVISORY_DISABLED"
LEGACY_ROOT_ENV = "B45_COMMENT_ADVISORY_ROOT"
MAX_CHANGED_FILES = 20


def _env_value(primary: str, legacy: str) -> str | None:
    return os.environ.get(primary) or os.environ.get(legacy)


def _workspace_root() -> tuple[Path | None, str | None]:
    """Resolve the target workspace while keeping the hook reusable in temp test repos."""
    env_root = _env_value(ROOT_ENV, LEGACY_ROOT_ENV)
    if env_root:
        candidate = Path(env_root).resolve()
        if not candidate.exists() or not candidate.is_dir():
            return None, "configured root is missing or is not a directory"
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


def _load_validator(repo_root: Path) -> tuple[Any | None, str]:
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
            from product_agent_os.comment_sufficiency import analyze_paths

            return analyze_paths, source_ref
        except Exception:
            continue
        finally:
            try:
                sys.path.remove(str(scripts_dir))
            except ValueError:
                pass
    return None, "comment_sufficiency_validator_not_found"


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


def _emit_additional_context(message: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": message,
                }
            },
            sort_keys=True,
        )
    )


def _emit_system_message(message: str) -> None:
    print(json.dumps({"systemMessage": message}, sort_keys=True))


def main() -> int:
    """Run changed-file comment-sufficiency checks as a non-blocking PostToolUse signal."""
    sys.stdin.read()
    disabled = (_env_value(DISABLE_ENV, LEGACY_DISABLE_ENV) or "").lower() in {"1", "true", "yes"}
    if disabled:
        return 0

    root, root_error = _workspace_root()
    if root is None:
        _emit_system_message(
            "Comment sufficiency advisory failed open because the configured workspace root is invalid ("
            + str(root_error)
            + "). It did not block the tool result."
        )
        return 0

    analyze_paths, validator_source_ref = _load_validator(root)
    if analyze_paths is None:
        _emit_system_message(
            "Comment sufficiency advisory failed open because its validator is unavailable ("
            + validator_source_ref
            + "). It did not block the tool result."
        )
        return 0

    changed = _changed_paths(root)
    if len(changed) > MAX_CHANGED_FILES:
        _emit_system_message(
            f"Comment sufficiency advisory skipped {len(changed)} changed source files because the automatic cap "
            f"is {MAX_CHANGED_FILES}. Run the comment_sufficiency.py CLI manually for this broad audit."
        )
        return 0

    try:
        warnings = analyze_paths(changed, root=root)
    except Exception as exc:
        _emit_system_message(
            "Comment sufficiency advisory failed open with "
            + type(exc).__name__
            + ". It did not block the tool result and did not expose workspace paths."
        )
        return 0

    if not warnings:
        return 0

    warning_refs = [f"{warning.path}:{warning.line} ({warning.symbol})" for warning in warnings]
    message = (
        f"Comment sufficiency advisory found {len(warnings)} reviewer-only warning(s) in "
        + ", ".join(_display_paths(changed, root))
        + ": "
        + "; ".join(warning_refs)
        + ". Review intent comments/docstrings where the warning is valid. This advisory is non-blocking and is not "
        + "completion proof. Validator source="
        + validator_source_ref
        + "."
    )
    _emit_additional_context(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())