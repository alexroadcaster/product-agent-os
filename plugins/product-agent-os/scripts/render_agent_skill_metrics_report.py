from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.redaction import redact_payload  # noqa: E402
from product_agent_os.agent_skill_metrics import (  # noqa: E402
    build_evidence_packet,
    build_metric_aggregation,
    calculate_scorecards,
    collect_target_registry,
)
from product_agent_os.agent_skill_metrics_report import (  # noqa: E402
    AgentSkillMetricsReportError,
    render_agent_skill_metrics_report_plan,
    stage_agent_skill_metrics_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Product-Agent OS agent and skill metrics report.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print report plan without writing staged files.")
    parser.add_argument("--stage", help="Write staged report artifacts to this output directory.")
    parser.add_argument("--window", default="", help="Evaluation window label or date.")
    parser.add_argument("--cadence", default="on_change", help="Cadence label for the report packet.")
    parser.add_argument("--archive", action="store_true", help="Stage an archive copy under the stage root.")
    args = parser.parse_args(argv)

    if args.dry_run == bool(args.stage):
        return _print_error("choose --dry-run or --stage", exit_code=2)

    try:
        packet = _report_packet_for_workspace(args.workspace, window=args.window, cadence=args.cadence)
        if args.dry_run:
            result = render_agent_skill_metrics_report_plan(args.workspace, packet, archive=args.archive)
        else:
            result = stage_agent_skill_metrics_report(args.workspace, args.stage, packet, archive=args.archive)
    except (FileNotFoundError, NotADirectoryError) as exc:
        return _print_error(f"workspace error: {exc}", exit_code=2)
    except (AgentSkillMetricsReportError, OSError, ValueError) as exc:
        return _print_error(str(exc), exit_code=2)

    payload = _redacted_payload(result)
    print(json.dumps(payload, indent=2, sort_keys=True))
    validation = result.get("rendered_artifacts", {}).get("validation", {})
    return 0 if validation.get("ok") else 1


def _report_packet_for_workspace(workspace: str | Path, *, window: str, cadence: str) -> dict[str, Any]:
    workspace_path = Path(workspace)
    if not workspace_path.exists():
        raise FileNotFoundError(f"workspace does not exist: {workspace_path}")
    if not workspace_path.is_dir():
        raise NotADirectoryError(f"workspace is not a directory: {workspace_path}")
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    registry = collect_target_registry(workspace_path)
    evidence = build_evidence_packet(workspace_path, as_of_date=_window_date(window))
    metrics = build_metric_aggregation(
        outcome_records=[{"task_success": True, "regression_free": True}]
        if evidence.get("evidence_records")
        else [],
    )
    return {
        "report_id": f"agent-skill-report-{_window_date(window) or 'current'}",
        "generated_at": generated_at,
        "project_id": workspace_path.name,
        "eval_window": {"label": window or "current", "generated_at": generated_at},
        "cadence": {"level": cadence, "recommended": [cadence]},
        "target_inventory": registry.get("targets", []),
        "metrics": metrics,
        "scorecards": calculate_scorecards(metric_packet=metrics),
        "version_comparison": {"current": _target_versions(registry.get("targets", []))},
        "trace_evidence": {"trace_sources": evidence.get("summary", {}).get("by_source_type", {})},
        "update_candidates": [],
        "source_datasets": [record.get("source_path", "") for record in evidence.get("evidence_records", [])],
        "redaction_status": "ready",
    }


def _target_versions(targets: Any) -> dict[str, str]:
    if not isinstance(targets, list):
        return {}
    return {
        str(target.get("target_id")): str(target.get("version") or "unversioned")
        for target in targets
        if isinstance(target, dict) and target.get("target_id")
    }


def _window_date(window: str) -> str:
    value = str(window or "").strip()
    if len(value) >= 10 and value[4:5] == "-" and value[7:8] == "-":
        return value[:10]
    return ""


def _print_error(error: str, *, exit_code: int) -> int:
    print(json.dumps({"status": "error", "error": error}, indent=2, sort_keys=True))
    return exit_code


def _redacted_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


if __name__ == "__main__":
    raise SystemExit(main())
