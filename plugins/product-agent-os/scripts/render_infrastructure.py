from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_infrastructure_plan,
    stage_infrastructure,
)
from product_agent_os.task_routing import TaskContextError, add_task_intake_arguments, task_context_from_args  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Product-Agent OS infrastructure plan.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without writing staged files.")
    parser.add_argument("--stage", help="Write staged artifacts to this output directory.")
    add_task_intake_arguments(parser)
    args = parser.parse_args(argv)

    if args.dry_run == bool(args.stage):
        print("error: choose --dry-run or --stage", file=sys.stderr)
        return 2

    try:
        task_context = task_context_from_args(args.workspace, args)
        task_options = {"task_context": task_context} if task_context is not None else {}
        if args.dry_run:
            result = render_infrastructure_plan(args.workspace, **task_options)
        else:
            result = stage_infrastructure(args.workspace, args.stage, **task_options)
    except (InfrastructureError, TaskContextError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    validation = result.get("rendered_artifacts", {}).get("validation", {})
    return 0 if validation.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
