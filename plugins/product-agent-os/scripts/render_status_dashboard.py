from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.redaction import redact_payload  # noqa: E402
from product_agent_os.discovery import analyze_workspace  # noqa: E402
from product_agent_os.infrastructure import (  # noqa: E402
    InfrastructureError,
    render_status_dashboard_plan,
    stage_status_dashboard,
)
from product_agent_os.status_snapshot import build_status_snapshot  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Product-Agent OS status dashboard.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print dashboard plan without writing staged files.")
    parser.add_argument("--stage", help="Write staged dashboard artifacts to this output directory.")
    args = parser.parse_args(argv)

    if args.dry_run == bool(args.stage):
        return _print_error("choose --dry-run or --stage", exit_code=2)

    try:
        snapshot = _snapshot_for_workspace(args.workspace)
        if args.dry_run:
            result = render_status_dashboard_plan(args.workspace, snapshot)
        else:
            result = stage_status_dashboard(args.workspace, args.stage, snapshot)
    except (FileNotFoundError, NotADirectoryError) as exc:
        return _print_error(f"workspace error: {exc}", exit_code=2)
    except (InfrastructureError, OSError, ValueError) as exc:
        return _print_error(str(exc), exit_code=2)

    payload = _redacted_payload(result)
    print(json.dumps(payload, indent=2, sort_keys=True))
    validation = result.get("rendered_artifacts", {}).get("validation", {})
    return 0 if validation.get("ok") else 1


def _snapshot_for_workspace(workspace: str | Path) -> dict[str, Any]:
    workspace_path = Path(workspace)
    if not workspace_path.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace_path}")
    if not workspace_path.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace_path}")
    runtime_result = run_contract(workspace_path)
    discovery_result = analyze_workspace(workspace_path)
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    return build_status_snapshot(
        runtime_result=runtime_result,
        discovery_result=discovery_result,
        generated_at=generated_at,
    )


def _print_error(error: str, *, exit_code: int) -> int:
    print(json.dumps({"status": "error", "error": error}, indent=2, sort_keys=True))
    return exit_code


def _redacted_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


if __name__ == "__main__":
    raise SystemExit(main())
