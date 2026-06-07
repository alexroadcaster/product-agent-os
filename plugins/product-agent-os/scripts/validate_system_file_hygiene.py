from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.system_file_hygiene import (  # noqa: E402
    build_system_file_hygiene_audit,
    validate_system_file_hygiene_audit,
)


def main(argv: list[str]) -> int:
    workspace = Path(argv[0]) if argv else Path.cwd()
    packet = build_system_file_hygiene_audit(workspace)
    errors = validate_system_file_hygiene_audit(packet)
    if errors:
        packet = packet | {"validation_errors": errors, "status": "blocked"}
    print(json.dumps(packet, indent=2, sort_keys=True))
    return 1 if packet["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
