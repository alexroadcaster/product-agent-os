from __future__ import annotations

import json
import sys


ADDITIONAL_CONTEXT = (
    "Treat the completed tool result as current-run evidence only. Record the command, exit code, and relevant "
    "output in the owning source artifact or a compact RUNLOG.md pointer when useful. Do not infer completion, "
    "runtime activation, or product acceptance from hook output alone; record every missing gate as an explicit gap."
)


def main() -> int:
    sys.stdin.read()
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": ADDITIONAL_CONTEXT,
                }
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())