from __future__ import annotations

import json
import sys


MESSAGE = (
    "Host approval remains undecided. Reuse the current request or applicable bounded standing authorization; "
    "do not request the same user permission again. Explain only an unresolved scope or host boundary. "
    "Existing authorization never overrides a sandbox, managed policy or host rejection."
)


def main() -> int:
    sys.stdin.read()
    print(json.dumps({"systemMessage": MESSAGE}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
