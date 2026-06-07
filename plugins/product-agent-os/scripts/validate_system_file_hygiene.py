from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.system_file_hygiene import (  # noqa: E402
    build_system_file_hygiene_audit,
    validate_system_file_hygiene_audit,
)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a read-only Product-Agent OS system file hygiene audit.")
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace directory to inspect.")
    parser.add_argument(
        "--trigger",
        default="manual_owner_requested",
        help="Audit trigger id or owner-provided reason to record in the JSON packet.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = _parse_args(argv)
    workspace = Path(args.workspace)
    packet = build_system_file_hygiene_audit(workspace, audit_trigger=args.trigger)
    errors = validate_system_file_hygiene_audit(packet)
    if errors:
        packet = packet | {
            "validation_errors": errors,
            "status": "blocked",
            "summary": packet["summary"] | {"status": "blocked"},
        }
    print(json.dumps(packet, indent=2, sort_keys=True))
    return 1 if packet["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
