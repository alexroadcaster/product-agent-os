from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.batch39_inventory import (  # noqa: E402
    build_batch39_inventory,
    validate_batch39_inventory,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Collect Batch 39 source/cache/package/session inventory.")
    parser.add_argument("--workspace", default=".", help="Workspace root to inspect.")
    parser.add_argument("--plugin-root", help="Product-Agent OS source root. Defaults to workspace plugin path.")
    parser.add_argument("--cache-root", action="append", default=[], help="Installed plugin cache root to inspect.")
    parser.add_argument("--output", help="Write inventory JSON to this path. Prints JSON if omitted.")
    parser.add_argument("--generated-at", help="Deterministic timestamp for tests.")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace)
    packet = build_batch39_inventory(
        workspace=workspace,
        plugin_root=Path(args.plugin_root) if args.plugin_root else None,
        cache_roots=[Path(path) for path in args.cache_root],
        generated_at=args.generated_at,
    )
    errors = validate_batch39_inventory(packet)
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, indent=2, sort_keys=True))
        return 1

    payload = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload + "\n", encoding="utf-8")
        print(json.dumps({"status": "ok", "output": _output_ref(workspace, output)}, indent=2, sort_keys=True))
    else:
        print(payload)
    return 0


def _output_ref(workspace: Path, output: Path) -> str:
    try:
        return output.resolve().relative_to(workspace.resolve()).as_posix()
    except ValueError:
        return "external_output"


if __name__ == "__main__":
    raise SystemExit(main())
