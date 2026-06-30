from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.self_learning_initializer import (  # noqa: E402
    SelfLearningInitializerError,
    build_state_initializer_packet,
    stage_state_initializer_packet,
)
from product_agent_os.self_learning_state import DEFAULT_APPROVAL_STATE, DEFAULT_CADENCE_LEVEL  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a staged Product-Agent OS Self-Learning Loop state initializer packet."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace path to inspect.")
    parser.add_argument("--dry-run", action="store_true", help="Build an initializer packet without writing files.")
    parser.add_argument("--stage", help="Stage the proposed state file and initializer packet under this output directory.")
    parser.add_argument("--now", help="Deterministic ISO timestamp for tests.")
    parser.add_argument("--installed-at", help="Initial installed_at timestamp for the proposed state.")
    parser.add_argument("--plugin-version", default="0.1.0", help="Product-Agent OS plugin version to record.")
    parser.add_argument(
        "--cadence-level",
        default=DEFAULT_CADENCE_LEVEL,
        choices=["manual_only", "weekly", "on_change", "disabled"],
        help="Initial self-learning cadence level.",
    )
    parser.add_argument(
        "--approval-state",
        default=DEFAULT_APPROVAL_STATE,
        choices=["manual_only", "disabled", "candidate_only", "approval_required"],
        help="Initial approval state.",
    )
    parser.add_argument("--disable-reason", help="Reason to include when initializing a disabled state.")
    args = parser.parse_args(argv)

    if bool(args.dry_run) == bool(args.stage):
        _print_payload(
            {
                "schema_version": "self_learning_state_initializer_packet_v1",
                "status": "error",
                "error": "choose exactly one of --dry-run or --stage",
                "state_written": False,
            }
        )
        return 2

    now = args.now or datetime.now(UTC).replace(microsecond=0).isoformat()
    if not _valid_iso_datetime(now) or (args.installed_at and not _valid_iso_datetime(args.installed_at)):
        _print_payload(
            {
                "schema_version": "self_learning_state_initializer_packet_v1",
                "status": "blocked",
                "errors": ["now:invalid_datetime" if not _valid_iso_datetime(now) else "installed_at:invalid_datetime"],
                "state_written": False,
            }
        )
        return 2

    mode = "stage" if args.stage else "dry_run"
    try:
        packet = build_state_initializer_packet(
            workspace=Path(args.workspace),
            now=now,
            mode=mode,
            plugin_version=args.plugin_version,
            installed_at=args.installed_at,
            cadence_level=args.cadence_level,
            approval_state=args.approval_state,
            disable_reason=args.disable_reason,
        )
    except (FileNotFoundError, NotADirectoryError) as exc:
        _print_payload(
            {
                "schema_version": "self_learning_state_initializer_packet_v1",
                "status": "blocked",
                "errors": [exc.__class__.__name__],
                "state_written": False,
            }
        )
        return 2

    if args.stage and packet["status"] != "blocked":
        try:
            packet["rendered_artifacts"] = stage_state_initializer_packet(
                workspace=Path(args.workspace),
                stage_root=args.stage,
                packet=packet,
            )
        except SelfLearningInitializerError as exc:
            packet["status"] = "blocked"
            packet.setdefault("blockers", []).append(str(exc))
            _print_payload(packet)
            return 2

    _print_payload(packet)
    return 0 if packet["status"] != "blocked" else 2


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
