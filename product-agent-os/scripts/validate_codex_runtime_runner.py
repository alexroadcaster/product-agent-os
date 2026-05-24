from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.contracts import validate_runner_result  # noqa: E402


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_codex_runtime_runner.py <result-json>", file=sys.stderr)
        return 2
    path = Path(argv[0])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    errors = validate_runner_result(payload)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
