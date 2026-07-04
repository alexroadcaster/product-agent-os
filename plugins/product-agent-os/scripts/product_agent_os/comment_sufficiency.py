"""Advisory checks for complex code without intent comments or docstrings."""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


PYTHON_REQUIRED_DOC_SYMBOLS = frozenset(
    {
        "SagaEngine",
        "SagaEngine.run",
        "OutboxRelay",
        "OutboxRelay.run_once",
        "plan_query",
        "Dinic.max_flow",
        "flight_routes",
        "new_roads_queries",
    }
)

JAVASCRIPT_REQUIRED_COMMENT_SYMBOLS = frozenset({"evaluateAccess", "redact", "normalizeEvent"})
JAVASCRIPT_SUFFIXES = frozenset({".js", ".mjs", ".cjs", ".ts", ".tsx"})
DEFAULT_EXCLUDED_PATH_PREFIXES = (
    "tests/",
    "docs/superpowers/specs/",
    ".docs-tools/",
    "site/",
)
DEFAULT_MAX_WARNINGS_PER_FILE = 5
DEFAULT_MAX_WARNINGS = 30


@dataclass(frozen=True)
class CommentSufficiencyWarning:
    path: str
    symbol: str
    line: int
    language: str
    reason: str
    severity: str = "advisory"
    suppressed_count: int = 0

    def as_dict(self) -> dict[str, str | int]:
        return {
            "path": self.path,
            "symbol": self.symbol,
            "line": self.line,
            "language": self.language,
            "reason": self.reason,
            "severity": self.severity,
            "suppressed_count": self.suppressed_count,
        }


def analyze_paths(
    paths: Iterable[Path | str],
    *,
    root: Path | None = None,
    include_tests: bool = False,
    use_default_excludes: bool = True,
    max_warnings_per_file: int | None = DEFAULT_MAX_WARNINGS_PER_FILE,
    max_warnings: int | None = DEFAULT_MAX_WARNINGS,
) -> list[CommentSufficiencyWarning]:
    warnings: list[CommentSufficiencyWarning] = []
    for raw_path in paths:
        path = Path(raw_path)
        if _should_skip_path(path, root, include_tests=include_tests, use_default_excludes=use_default_excludes):
            continue
        if path.suffix == ".py":
            warnings.extend(analyze_python_file(path, root=root))
        elif path.suffix in JAVASCRIPT_SUFFIXES:
            warnings.extend(analyze_javascript_file(path, root=root))
    return _cap_warnings(warnings, max_warnings_per_file=max_warnings_per_file, max_warnings=max_warnings)


def analyze_python_file(
    path: Path,
    *,
    root: Path | None = None,
    required_symbols: frozenset[str] = PYTHON_REQUIRED_DOC_SYMBOLS,
) -> list[CommentSufficiencyWarning]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tree = ast.parse(text, filename=str(path))
    warnings: list[CommentSufficiencyWarning] = []

    def visit_body(body: Sequence[ast.stmt], owner: str | None = None) -> None:
        for node in body:
            if isinstance(node, ast.ClassDef):
                qualname = node.name if owner is None else f"{owner}.{node.name}"
                _maybe_warn_python(path, lines, node, qualname, root, required_symbols, warnings, "class")
                visit_body(node.body, qualname)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualname = node.name if owner is None else f"{owner}.{node.name}"
                _maybe_warn_python(path, lines, node, qualname, root, required_symbols, warnings, "function")

    visit_body(tree.body)
    return warnings


def analyze_javascript_file(
    path: Path,
    *,
    root: Path | None = None,
    required_symbols: frozenset[str] = JAVASCRIPT_REQUIRED_COMMENT_SYMBOLS,
) -> list[CommentSufficiencyWarning]:
    lines = path.read_text(encoding="utf-8").splitlines()
    warnings: list[CommentSufficiencyWarning] = []
    for index, symbol in _javascript_function_symbols(lines):
        end_index = _javascript_function_end(lines, index)
        body = "\n".join(lines[index : end_index + 1])
        needs_comment = symbol in required_symbols or _javascript_looks_complex(body, end_index - index + 1)
        if needs_comment and not _has_preceding_comment(lines, index):
            warnings.append(
                CommentSufficiencyWarning(
                    path=_display_path(path, root),
                    symbol=symbol,
                    line=index + 1,
                    language="javascript",
                    reason="complex function lacks docstring, intent comment, or comment_not_needed_reason",
                )
            )
    return warnings


def _javascript_function_symbols(lines: Sequence[str]) -> Iterable[tuple[int, str]]:
    """Yield conservative JS/TS function-like definitions without a JS parser dependency."""
    declaration_pattern = re.compile(
        r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\("
    )
    arrow_pattern = re.compile(
        r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*"
        r"(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)(?:\s*:\s*[^=]+?)?\s*=>"
    )
    method_pattern = re.compile(
        r"^\s*(?:(?:public|private|protected|static|readonly|async)\s+)*"
        r"([A-Za-z_$][\w$]*)\s*(?:<[^>]+>)?\([^)]*\)(?:\s*:\s*[^{]+)?\s*\{"
    )
    excluded_methods = frozenset({"if", "for", "while", "switch", "catch", "function", "constructor"})
    for index, line in enumerate(lines):
        for pattern in (declaration_pattern, arrow_pattern):
            match = pattern.match(line)
            if match:
                yield index, match.group(1)
                break
        else:
            method_match = method_pattern.match(line)
            if method_match and method_match.group(1) not in excluded_methods:
                yield index, method_match.group(1)


def advisory_payload(warnings: Sequence[CommentSufficiencyWarning]) -> dict[str, object]:
    return {
        "status": "advisory_complete",
        "blocking": False,
        "warning_count": len(warnings),
        "suppressed_warning_count": sum(warning.suppressed_count for warning in warnings),
        "warnings": [warning.as_dict() for warning in warnings],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Python or JavaScript files to inspect.")
    parser.add_argument("--root", default=".", help="Root path used for display-only relative paths.")
    parser.add_argument("--include-tests", action="store_true", help="Include tests/** paths in broad advisory scans.")
    parser.add_argument(
        "--no-default-excludes",
        action="store_true",
        help="Disable default tests/generated/site path exclusions.",
    )
    parser.add_argument(
        "--max-warnings-per-file",
        type=int,
        default=DEFAULT_MAX_WARNINGS_PER_FILE,
        help="Cap advisory warnings per file; use -1 for no per-file cap.",
    )
    parser.add_argument(
        "--max-warnings",
        type=int,
        default=DEFAULT_MAX_WARNINGS,
        help="Cap total advisory warnings; use -1 for no total cap.",
    )
    args = parser.parse_args(argv)
    _reject_zero_cap(parser, "--max-warnings-per-file", args.max_warnings_per_file)
    _reject_zero_cap(parser, "--max-warnings", args.max_warnings)

    root = Path(args.root).resolve()
    warnings = analyze_paths(
        (Path(path) for path in args.paths),
        root=root,
        include_tests=args.include_tests,
        use_default_excludes=not args.no_default_excludes,
        max_warnings_per_file=_none_if_negative(args.max_warnings_per_file),
        max_warnings=_none_if_negative(args.max_warnings),
    )
    print(json.dumps(advisory_payload(warnings), indent=2, sort_keys=True))
    return 0


def _maybe_warn_python(
    path: Path,
    lines: Sequence[str],
    node: ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
    qualname: str,
    root: Path | None,
    required_symbols: frozenset[str],
    warnings: list[CommentSufficiencyWarning],
    node_type: str,
) -> None:
    needs_comment = qualname in required_symbols or _python_looks_complex(node)
    if not needs_comment:
        return
    if ast.get_docstring(node) or _has_preceding_comment(lines, node.lineno - 1):
        return
    warnings.append(
        CommentSufficiencyWarning(
            path=_display_path(path, root),
            symbol=qualname,
            line=node.lineno,
            language="python",
            reason=f"complex {node_type} lacks docstring, intent comment, or comment_not_needed_reason",
        )
    )


def _python_looks_complex(node: ast.AST) -> bool:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("run_"):
        return False
    line_count = getattr(node, "end_lineno", getattr(node, "lineno", 0)) - getattr(node, "lineno", 0) + 1
    branches = sum(
        isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.ExceptHandler, ast.BoolOp, ast.Match))
        for child in ast.walk(node)
    )
    return line_count >= 14 and branches >= 4


def _javascript_looks_complex(body: str, line_count: int) -> bool:
    branch_count = len(re.findall(r"\b(if|for|while|switch|catch)\b|&&|\|\|", body))
    return line_count >= 14 and branch_count >= 4


def _javascript_function_end(lines: Sequence[str], start_index: int) -> int:
    depth = 0
    seen_open = False
    for index in range(start_index, len(lines)):
        for char in lines[index]:
            if char == "{":
                depth += 1
                seen_open = True
            elif char == "}":
                depth -= 1
        if seen_open and depth <= 0:
            return index
    return len(lines) - 1


def _has_preceding_comment(lines: Sequence[str], start_index: int) -> bool:
    for index in range(start_index - 1, max(-1, start_index - 7), -1):
        stripped = lines[index].strip()
        if not stripped:
            continue
        if "comment_not_needed_reason" in stripped:
            return True
        return (
            stripped.startswith("#")
            or stripped.startswith("//")
            or stripped.startswith("/*")
            or stripped.startswith("*")
            or stripped.endswith("*/")
        )
    return False


def _should_skip_path(
    path: Path,
    root: Path | None,
    *,
    include_tests: bool,
    use_default_excludes: bool,
) -> bool:
    if not use_default_excludes:
        return False
    display_path = _display_path(path, root).replace("\\", "/")
    for prefix in DEFAULT_EXCLUDED_PATH_PREFIXES:
        if include_tests and prefix == "tests/":
            continue
        if display_path.startswith(prefix):
            return True
    return False


def _cap_warnings(
    warnings: Sequence[CommentSufficiencyWarning],
    *,
    max_warnings_per_file: int | None,
    max_warnings: int | None,
) -> list[CommentSufficiencyWarning]:
    if max_warnings_per_file is None and max_warnings is None:
        return list(warnings)

    capped: list[CommentSufficiencyWarning] = []
    by_path: dict[str, int] = {}
    suppressed_by_path: dict[int, int] = {}
    for warning in warnings:
        count = by_path.get(warning.path, 0)
        if max_warnings_per_file is not None and count >= max_warnings_per_file:
            if capped:
                suppressed_by_path[id(capped[-1])] = suppressed_by_path.get(id(capped[-1]), 0) + 1
            continue
        by_path[warning.path] = count + 1
        capped.append(warning)

    with_per_file_suppression = [_with_suppressed_count(warning, suppressed_by_path.get(id(warning), 0)) for warning in capped]
    if max_warnings is None or len(with_per_file_suppression) <= max_warnings:
        return with_per_file_suppression

    visible = with_per_file_suppression[:max_warnings]
    hidden_warnings = with_per_file_suppression[max_warnings:]
    hidden_count = len(hidden_warnings) + sum(warning.suppressed_count for warning in hidden_warnings)
    if hidden_count:
        last = visible[-1]
        visible[-1] = _with_suppressed_count(last, last.suppressed_count + hidden_count)
    return visible


def _reject_zero_cap(parser: argparse.ArgumentParser, name: str, value: int) -> None:
    if value == 0:
        parser.error(f"{name} must be positive, or -1 to disable that cap")


def _with_suppressed_count(warning: CommentSufficiencyWarning, suppressed_count: int) -> CommentSufficiencyWarning:
    if suppressed_count == warning.suppressed_count:
        return warning
    return CommentSufficiencyWarning(
        path=warning.path,
        symbol=warning.symbol,
        line=warning.line,
        language=warning.language,
        reason=warning.reason,
        severity=warning.severity,
        suppressed_count=suppressed_count,
    )


def _none_if_negative(value: int) -> int | None:
    return None if value < 0 else value


def _display_path(path: Path, root: Path | None) -> str:
    if root is None:
        return str(path)
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return f"<outside-root>/{path.name}"


if __name__ == "__main__":
    raise SystemExit(main())
