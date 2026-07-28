from __future__ import annotations

import json
import sys


MESSAGE = (
    "Before stopping, re-read the task and record a compact completion ledger: source contract, scope items, "
    "files changed, current-run checks, activation/fallback proof when relevant, gaps, source conflicts, reviewer "
    "status, and next action. Run the configured control-plane sync when owned state changed, then show a "
    "user-visible Completion Brief. This reminder does not prove completion and does not force continuation."
)


def main() -> int:
    sys.stdin.read()
    print(json.dumps({"systemMessage": MESSAGE}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())