from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_command_results import (  # noqa: E402
    build_command_result_entry,
    validate_command_result_entry,
    validate_command_results_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append one redacted Batch 39 command result JSONL entry.")
    parser.add_argument("--output", required=True)
    parser.add_argument("--test-id", required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--manifest-ref", required=True)
    parser.add_argument("--command-id", required=True)
    parser.add_argument("--command", required=True)
    parser.add_argument("--exit-code")
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--finished-at", required=True)
    parser.add_argument("--stdout", default="")
    parser.add_argument("--stdout-file")
    parser.add_argument("--stderr", default="")
    parser.add_argument("--stderr-file")
    parser.add_argument("--evidence-class", required=True)
    parser.add_argument("--evidence-source", required=True)
    parser.add_argument("--append", action="store_true")
    args = parser.parse_args(argv)

    entry = build_command_result_entry(
        test_id=args.test_id,
        attempt_id=args.attempt_id,
        manifest_ref=args.manifest_ref,
        command_id=args.command_id,
        command=args.command,
        exit_code=_exit_code(args.exit_code),
        started_at=args.started_at,
        finished_at=args.finished_at,
        stdout=_text_arg_or_file(args.stdout, args.stdout_file),
        stderr=_text_arg_or_file(args.stderr, args.stderr_file),
        evidence_class=args.evidence_class,
        evidence_source=args.evidence_source,
    )
    entry_errors = validate_command_result_entry(entry)
    if entry_errors:
        print(json.dumps({"status": "error", "errors": entry_errors}, indent=2, sort_keys=True))
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    existing = output.read_text(encoding="utf-8") if args.append and output.exists() else ""
    text = existing + json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n"
    jsonl_errors = validate_command_results_jsonl(text)
    if jsonl_errors:
        print(json.dumps({"status": "error", "errors": jsonl_errors}, indent=2, sort_keys=True))
        return 1
    output.write_text(text, encoding="utf-8")
    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(output),
                "command_id": entry["command_id"],
                "entry_digest": entry["entry_digest"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _exit_code(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def _text_arg_or_file(value: str, file_ref: str | None) -> str:
    if not file_ref:
        return value
    path = Path(file_ref)
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
        except OSError:
            return value
    return value


if __name__ == "__main__":
    raise SystemExit(main())
