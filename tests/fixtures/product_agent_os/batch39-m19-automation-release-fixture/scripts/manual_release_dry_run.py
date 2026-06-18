from __future__ import annotations

import json


def main() -> int:
    result = {
        "status": "dry_run_only",
        "release_publication": False,
        "deployment": False,
        "tag_created": False,
        "automation_activation": False,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
