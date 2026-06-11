from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    contract = json.loads((ROOT / "openapi" / "openapi.json").read_text(encoding="utf-8"))
    required_paths = {"/health", "/tasks/{task_id}"}
    paths = set(contract.get("paths", {}))
    missing = sorted(required_paths - paths)
    if missing:
        print(json.dumps({"status": "error", "missing_paths": missing}, sort_keys=True))
        return 1
    schemas = contract.get("components", {}).get("schemas", {})
    missing_schemas = sorted({"Task", "Error"} - set(schemas))
    if missing_schemas:
        print(json.dumps({"status": "error", "missing_schemas": missing_schemas}, sort_keys=True))
        return 1
    print(json.dumps({"status": "ok", "paths": sorted(paths), "schemas": sorted(schemas)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())

