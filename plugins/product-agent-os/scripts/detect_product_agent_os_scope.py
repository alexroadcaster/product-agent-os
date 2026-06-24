from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import detect_product_agent_os_scope


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detect whether a workspace is eligible for Product-Agent OS scoped learning."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace path to inspect.")
    args = parser.parse_args(argv)

    try:
        packet = detect_product_agent_os_scope(Path(args.workspace))
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(packet, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
