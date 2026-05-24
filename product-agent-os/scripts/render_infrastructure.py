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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Product-Agent OS infrastructure plan.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without writing staged files.")
    parser.add_argument("--stage", help="Write staged artifacts to this output directory.")
    args = parser.parse_args(argv)

    if args.dry_run == bool(args.stage):
        print("error: choose --dry-run or --stage", file=sys.stderr)
        return 2

    try:
        if args.dry_run:
            result = render_infrastructure_plan(args.workspace)
        else:
            result = stage_infrastructure(args.workspace, args.stage)
    except InfrastructureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    validation = result.get("rendered_artifacts", {}).get("validation", {})
    return 0 if validation.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
