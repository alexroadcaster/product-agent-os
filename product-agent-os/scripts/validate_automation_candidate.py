from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_automation_candidate.py <candidate-file>", file=sys.stderr)
        return 2
    result = validate_automation_candidate(Path(argv[0]))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] in {"candidate_only", "ready_for_manual_approval"} else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
