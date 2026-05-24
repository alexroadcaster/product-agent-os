from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.merge_infrastructure import (  # noqa: E402
    MergeInfrastructureError,
    apply_merge_plan,
    build_merge_plan,
    rollback_merge,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan, apply, or roll back Product-Agent OS staged infrastructure.")
    parser.add_argument("workspace")
    parser.add_argument("stage_dir")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--plan", action="store_true", help="Print a read-only merge plan.")
    mode.add_argument("--apply", action="store_true", help="Apply approved merge decisions.")
    mode.add_argument("--rollback", help="Rollback using this rollback manifest.")
    parser.add_argument("--approval-file", help="Approval record required with --apply.")
    args = parser.parse_args(argv)

    if args.apply and not args.approval_file:
        print("error: --approval-file is required with --apply", file=sys.stderr)
        return 2

    try:
        if args.plan:
            result = build_merge_plan(args.workspace, args.stage_dir)
            exit_code = 0 if result.get("status") != "blocked" else 1
        elif args.apply:
            result = apply_merge_plan(args.workspace, args.stage_dir, args.approval_file)
            exit_code = 0
        else:
            result = rollback_merge(args.workspace, args.rollback)
            exit_code = 0
    except MergeInfrastructureError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 1

    print(json.dumps(result, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
