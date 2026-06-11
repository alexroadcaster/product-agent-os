from __future__ import annotations

import argparse
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.windows_codex_permissions import (  # noqa: E402
    apply_permissions,
    check_permissions,
    dumps_json,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check or prepare scoped Windows ACL permissions for Product-Agent OS .codex artifacts."
    )
    parser.add_argument("workspace", help="Target project workspace.")
    parser.add_argument("--apply", action="store_true", help="Create scoped .codex dirs and remove inherited deny ACLs.")
    args = parser.parse_args(argv)

    result = apply_permissions(args.workspace) if args.apply else check_permissions(args.workspace)
    print(dumps_json(result))
    return 0 if result["status"] in {"checked", "applied"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
