from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.self_learning_state import (  # noqa: E402
    evaluate_self_learning_due,
    load_self_learning_state,
    load_self_learning_state_file,
    workspace_ref,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check whether the Product-Agent OS Self-Learning Loop is due without running it."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace path to inspect.")
    parser.add_argument("--dry-run", action="store_true", help="Read state and print due status without writes.")
    parser.add_argument("--now", help="Deterministic ISO timestamp for tests.")
    parser.add_argument("--state-file", help="Read Self-Learning Loop state from an explicit staged JSON file.")
    args = parser.parse_args(argv)

    if not args.dry_run:
        _print_payload(
            {
                "schema_version": "self_learning_due_check_v1",
                "status": "error",
                "error": "only --dry-run is supported in B44-S1",
                "analysis_executed": False,
                "state_written": False,
            }
        )
        return 2

    now = args.now or datetime.now(UTC).replace(microsecond=0).isoformat()
    if args.now and not _valid_iso_datetime(args.now):
        _print_payload(
            {
                "schema_version": "self_learning_due_check_v1",
                "status": "state_invalid",
                "errors": ["now:invalid_datetime"],
                "analysis_executed": False,
                "state_written": False,
                "mode": "dry_run",
            }
        )
        return 2

    workspace = Path(args.workspace)
    if args.state_file:
        state, load_errors = load_self_learning_state_file(args.state_file)
        state_source = "explicit_state_file"
    else:
        state, load_errors = load_self_learning_state(workspace)
        state_source = "workspace_state_file"
    if load_errors:
        payload = evaluate_self_learning_due(None, now=now)
        payload["errors"] = load_errors
    else:
        payload = evaluate_self_learning_due(state, now=now)
    payload.update(
        {
            "mode": "dry_run",
            "workspace_ref": workspace_ref(workspace),
            "state_source": state_source,
            "state_workspace_write_required": False,
            "manual_run_command": "python plugins/product-agent-os/scripts/run_self_learning_loop.py <workspace> --dry-run",
            "manual_run_command_status": "available_manual_only",
            "manual_runner_boundary": {
                "write_policy": "read_only_or_staged_only",
                "auto_apply_status": "not_enabled",
                "schedule_status": "not_created",
            },
        }
    )
    _print_payload(payload)
    if "now:invalid_datetime" in payload.get("errors", []):
        return 2
    return 0 if payload["status"] in {"due", "not_due", "disabled", "state_invalid"} else 2


def _print_payload(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def _valid_iso_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    raise SystemExit(main())
