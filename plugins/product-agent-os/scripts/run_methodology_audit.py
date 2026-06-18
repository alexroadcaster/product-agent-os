from __future__ import annotations

import json
import sys
from pathlib import Path

from product_agent_os.methodology_audit import build_methodology_audit
from product_agent_os.methodology_report import render_methodology_audit_report


def main(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: run_methodology_audit.py <workspace> (--json | --report)")
        return 0
    if len(argv) != 2 or argv[1] not in {"--json", "--report"}:
        print("usage: run_methodology_audit.py <workspace> (--json | --report)", file=sys.stderr)
        return 2

    workspace = Path(argv[0])
    mode = argv[1]
    if not workspace.exists() or not workspace.is_dir():
        error = {"status": "error", "error": f"invalid workspace: {workspace}"}
        if mode == "--json":
            print(json.dumps(error, indent=2, sort_keys=True))
        else:
            print(error["error"], file=sys.stderr)
        return 1

    audit = build_methodology_audit(workspace, intent_hint="")
    if mode == "--json":
        print(json.dumps(audit, indent=2, sort_keys=True))
    else:
        print(render_methodology_audit_report(audit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
