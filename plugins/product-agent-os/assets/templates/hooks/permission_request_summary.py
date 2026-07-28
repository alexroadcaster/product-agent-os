from __future__ import annotations

import json
import sys


MESSAGE = (
    "Approval remains undecided. Before responding, summarize the requested purpose, exact scope and target, "
    "risk, rollback or disable path, and verification evidence. Treat external writes, provider/API calls, "
    "browser automation, git stage/commit/push/PR, hook or automation activation, deployment/publication, and "
    "permission changes as separate approval boundaries."
)


def main() -> int:
    sys.stdin.read()
    print(json.dumps({"systemMessage": MESSAGE}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())