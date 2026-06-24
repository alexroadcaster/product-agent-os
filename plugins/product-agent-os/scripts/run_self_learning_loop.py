from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import detect_product_agent_os_scope  # noqa: E402
from product_agent_os.self_learning_progress import (  # noqa: E402
    SelfLearningProgressError,
    build_self_learning_run_packet,
    dry_run_artifact_plan,
    stage_self_learning_run,
)
from product_agent_os.self_learning_state import (  # noqa: E402
    evaluate_self_learning_due,
    load_self_learning_state,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the Product-Agent OS Self-Learning Loop manually as staged evidence only."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace path to inspect.")
    parser.add_argument("--dry-run", action="store_true", help="Build a run packet without writing files.")
    parser.add_argument("--stage", help="Stage progress JSON/HTML artifacts under this output directory.")
    parser.add_argument("--now", help="Deterministic ISO timestamp for tests.")
    args = parser.parse_args(argv)

    if bool(args.dry_run) == bool(args.stage):
        _print_payload(
            {
                "schema_version": "self_learning_run_packet_v1",
                "status": "error",
                "error": "choose exactly one of --dry-run or --stage",
                "analysis_executed": False,
                "state_written": False,
            }
        )
        return 2

    now = args.now or datetime.now(UTC).replace(microsecond=0).isoformat()
    if not _valid_iso_datetime(now):
        _print_payload(
            {
                "schema_version": "self_learning_run_packet_v1",
                "status": "blocked",
                "errors": ["now:invalid_datetime"],
                "analysis_executed": False,
                "state_written": False,
            }
        )
        return 2

    workspace = Path(args.workspace)
    try:
        scope_packet = detect_product_agent_os_scope(workspace)
    except (FileNotFoundError, NotADirectoryError) as exc:
        _print_payload(
            {
                "schema_version": "self_learning_run_packet_v1",
                "status": "blocked",
                "errors": [exc.__class__.__name__],
                "analysis_executed": False,
                "state_written": False,
            }
        )
        return 2

    state, load_errors = load_self_learning_state(workspace)
    if load_errors:
        due_packet = evaluate_self_learning_due(None, now=now)
        due_packet["errors"] = load_errors
    else:
        due_packet = evaluate_self_learning_due(state, now=now)

    mode = "stage" if args.stage else "dry_run"
    packet = build_self_learning_run_packet(
        workspace=workspace,
        now=now,
        mode=mode,
        scope_packet=scope_packet,
        due_packet=due_packet,
    )

    if args.stage and packet["status"] != "blocked":
        try:
            rendered = stage_self_learning_run(workspace=workspace, stage_root=args.stage, packet=packet)
        except SelfLearningProgressError as exc:
            packet["status"] = "blocked"
            packet.setdefault("blockers", []).append(str(exc))
            _print_payload(packet)
            return 2
        packet["rendered_artifacts"] = _safe_rendered_artifacts(rendered)
    else:
        packet["rendered_artifacts"] = dry_run_artifact_plan(packet)

    _print_payload(packet)
    return 0 if packet["status"] != "blocked" else 2


def _safe_rendered_artifacts(rendered: dict) -> dict:
    safe = dict(rendered)
    safe["root"] = "[STAGE_ROOT]"
    if "manifest_path" in safe:
        safe["manifest_path"] = "[STAGE_ROOT]/product-agent-os-stage-manifest.json"
    return safe


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
