from __future__ import annotations

import re
import sys
from pathlib import Path


_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _validate_id(label: str, value: str) -> None:
    if not _ID_PATTERN.fullmatch(value):
        raise ValueError(f"invalid {label}: expected slug-like [A-Za-z0-9_-]+")


def _newline_style(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _normalize_newlines(text: str, newline: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", newline)


def _managed_block(owner: str, section_id: str, body: str, newline: str) -> str:
    start = f"<!-- {owner}:start {section_id} -->"
    end = f"<!-- {owner}:end {section_id} -->"
    body = _normalize_newlines(body, newline).rstrip()
    return f"{start}{newline}{body}{newline}{end}{newline}"


def merge_section(text: str, owner: str, section_id: str, body: str) -> str:
    _validate_id("owner", owner)
    _validate_id("section-id", section_id)
    start = f"<!-- {owner}:start {section_id} -->"
    end = f"<!-- {owner}:end {section_id} -->"
    for line in body.splitlines():
        if line == start or line == end:
            raise ValueError("body contains managed boundary marker for the same owner/section")

    newline = _newline_style(text)
    block = _managed_block(owner, section_id, body, newline)
    lines = text.splitlines(keepends=True)
    merged: list[str] = []
    index = 0
    replaced = False

    while index < len(lines):
        if lines[index].rstrip("\r\n") != start:
            merged.append(lines[index])
            index += 1
            continue

        end_index = index + 1
        while end_index < len(lines) and lines[end_index].rstrip("\r\n") != end:
            end_index += 1

        if end_index == len(lines):
            merged.append(lines[index])
            index += 1
            continue

        if replaced:
            raise ValueError("duplicate managed section for owner/section")

        merged.append(block)
        replaced = True
        index = end_index + 1

    if replaced:
        return "".join(merged)

    separator = "" if not text or text.endswith(("\n", "\r")) else newline
    spacer = "" if not text else newline
    return f"{text}{separator}{spacer}{block}"


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: merge_markdown.py <file> <owner> <section-id> <body-file>", file=sys.stderr)
        return 2
    target = Path(argv[0])
    owner = argv[1]
    section_id = argv[2]
    body_path = Path(argv[3])

    try:
        _validate_id("owner", owner)
        _validate_id("section-id", section_id)
        with body_path.open("r", encoding="utf-8", newline="") as handle:
            body = handle.read()
        if target.exists():
            with target.open("r", encoding="utf-8", newline="") as handle:
                original = handle.read()
        else:
            original = ""
        updated = merge_section(original, owner, section_id, body)
        with target.open("w", encoding="utf-8", newline="") as handle:
            handle.write(updated)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError):
        print("error: unable to read or write markdown files", file=sys.stderr)
        return 1
    return 0
