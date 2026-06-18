from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.redaction import redact_payload  # noqa: E402
from product_agent_os.first_run_analysis import run_first_project_analysis  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Product-Agent OS first project analysis.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print the analysis packet without writing files.")
    parser.add_argument("--write", action="store_true", help="Write the packet under .codex/product-agent-os/analysis/.")
    parser.add_argument("--generated-at", help="Deterministic timestamp for tests.")
    args = parser.parse_args(argv)

    if int(bool(args.dry_run)) + int(bool(args.write)) != 1:
        print(json.dumps({"status": "error", "error": "choose exactly one mode: --dry-run or --write"}, indent=2, sort_keys=True))
        return 2

    try:
        result = run_first_project_analysis(
            args.workspace,
            generated_at=args.generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
            write=args.write,
        )
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2

    redacted, _report = redact_payload(result)
    payload = redacted if isinstance(redacted, dict) else result
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
