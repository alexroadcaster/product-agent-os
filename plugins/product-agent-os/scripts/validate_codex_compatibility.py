from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.codex_compatibility import validate_codex_compatibility  # noqa: E402


def main() -> int:
    plugin_root = Path(__file__).resolve().parents[1]
    report = validate_codex_compatibility(plugin_root)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "compatible" else 1


if __name__ == "__main__":
    raise SystemExit(main())
