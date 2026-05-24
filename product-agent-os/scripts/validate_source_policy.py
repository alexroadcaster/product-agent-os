from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.source_policy import validate_source_policy  # noqa: E402


def main(argv: list[str]) -> int:
    workspace = Path(argv[0]) if argv else Path.cwd()
    result = validate_source_policy(workspace)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
