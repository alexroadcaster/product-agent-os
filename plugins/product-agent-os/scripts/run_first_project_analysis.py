from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.redaction import redact_payload  # noqa: E402
from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact  # noqa: E402
from product_agent_os.first_run_analysis import (  # noqa: E402
    ANALYSIS_DIR,
    ANSWER_LEDGER_TEMPLATE_NAME,
    FIRST_RUN_PACKET_NAME,
    build_first_run_automation_contract,
    run_first_project_analysis,
)
from product_agent_os.question_ledger import render_answer_ledger_json  # noqa: E402


def _print_payload(payload: dict) -> None:
    redacted, _report = redact_payload(payload)
    safe_payload = redacted if isinstance(redacted, dict) else payload
    print(json.dumps(safe_payload, ensure_ascii=False, indent=2, sort_keys=True))


def _actions_performed(*, target_workspace_mutation: bool = False) -> dict[str, bool]:
    return {
        "target_workspace_mutation": target_workspace_mutation,
        "live_server": False,
        "browser_automation": False,
        "provider_api_call": False,
        "mcp_external_call": False,
        "git_stage_commit_push_pr": False,
        "release_deploy_publish": False,
        "active_automation": False,
    }


def _help_payload() -> dict:
    contract = build_first_run_automation_contract()
    return {
        "schema_version": "first_run_orchestrator_help_v1",
        "status": "help",
        "summary": "Run Product-Agent OS first project analysis in a safe mode.",
        "next_safe_command": "python plugins/product-agent-os/scripts/run_first_project_analysis.py <workspace> --full-dry-run",
        "safe_modes": ["--full-dry-run", "--stage <dir>", "--write-analysis"],
        "contract": contract,
        "actions_performed": _actions_performed(),
    }


def main(argv: list[str] | None = None) -> int:
    raw_args = list(sys.argv[1:] if argv is None else argv)
    if not raw_args:
        _print_payload(_help_payload())
        return 0

    parser = argparse.ArgumentParser(description="Run Product-Agent OS first project analysis.")
    parser.add_argument("workspace", nargs="?")
    parser.add_argument("--dry-run", action="store_true", help="Print the analysis packet without writing files.")
    parser.add_argument("--write", action="store_true", help="Write the packet under .codex/product-agent-os/analysis/.")
    parser.add_argument("--full-dry-run", action="store_true", help="Run the safe first-run orchestration without writing target files.")
    parser.add_argument("--stage", help="Write packet and offline HTML artifacts under an explicit external stage directory.")
    parser.add_argument("--write-analysis", action="store_true", help="Write generated analysis packet and HTML under .codex/product-agent-os/analysis/.")
    parser.add_argument("--generated-at", help="Deterministic timestamp for tests.")
    args = parser.parse_args(raw_args)

    mode_count = sum(
        int(bool(value))
        for value in (args.dry_run, args.write, args.full_dry_run, args.stage, args.write_analysis)
    )
    if mode_count != 1:
        _print_payload(
            {
                "status": "error",
                "error": "choose exactly one mode: --dry-run, --write, --full-dry-run, --stage, or --write-analysis",
            }
        )
        return 2
    if not args.workspace:
        _print_payload({"status": "error", "error": "workspace is required for selected mode"})
        return 2

    try:
        generated_at = args.generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
        if args.stage:
            result = _run_stage_mode(args.workspace, args.stage, generated_at=generated_at)
        elif args.write_analysis:
            result = _run_write_analysis_mode(args.workspace, generated_at=generated_at)
        else:
            result = run_first_project_analysis(
                args.workspace,
                generated_at=generated_at,
                write=args.write,
            )
            if args.full_dry_run:
                result["mode"] = "full_dry_run"
                result["orchestration_contract"] = build_first_run_automation_contract()
                result["actions_performed"] = _actions_performed()
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError) as exc:
        _print_payload({"status": "error", "error": str(exc)})
        return 2

    _print_payload(result)
    return 0


def _run_stage_mode(workspace: str, stage_dir: str, *, generated_at: str) -> dict:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_dir).resolve()
    _ensure_stage_outside_target(workspace_path, stage_path)
    result = run_first_project_analysis(workspace_path, generated_at=generated_at, write=False)
    packet = result["packet"]
    stage_path.mkdir(parents=True, exist_ok=True)
    (stage_path / FIRST_RUN_PACKET_NAME).write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (stage_path / ANSWER_LEDGER_TEMPLATE_NAME).write_text(
        render_answer_ledger_json(packet["answer_ledger_routing"]["ledger_template"]) + "\n",
        encoding="utf-8",
    )
    render_result = render_first_run_analysis_artifact(packet, workspace_path, output_dir=stage_path)
    result.update(
        {
            "mode": "stage",
            "orchestration_contract": build_first_run_automation_contract(),
            "actions_performed": _actions_performed(),
            "write_boundary": {
                "stage_root": "explicit_external_stage_root",
                "target_default": "read_only",
                "target_workspace_mutation": False,
            },
            "written_files": [FIRST_RUN_PACKET_NAME, ANSWER_LEDGER_TEMPLATE_NAME] + render_result["written_files"],
            "render_result": render_result,
            "baseline_comparison": render_result["baseline_comparison"],
            "cleanup_guidance": render_result["cleanup_guidance"],
        }
    )
    return result


def _run_write_analysis_mode(workspace: str, *, generated_at: str) -> dict:
    workspace_path = Path(workspace).resolve()
    result = run_first_project_analysis(workspace_path, generated_at=generated_at, write=False)
    packet = result["packet"]
    analysis_dir = workspace_path / ANALYSIS_DIR
    analysis_dir.mkdir(parents=True, exist_ok=True)
    (analysis_dir / FIRST_RUN_PACKET_NAME).write_text(
        json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (analysis_dir / ANSWER_LEDGER_TEMPLATE_NAME).write_text(
        render_answer_ledger_json(packet["answer_ledger_routing"]["ledger_template"]) + "\n",
        encoding="utf-8",
    )
    render_result = render_first_run_analysis_artifact(packet, workspace_path)
    written = [f"{ANALYSIS_DIR}/{FIRST_RUN_PACKET_NAME}", f"{ANALYSIS_DIR}/{ANSWER_LEDGER_TEMPLATE_NAME}"]
    written.extend(f"{ANALYSIS_DIR}/{path}" for path in render_result["written_files"])
    result.update(
        {
            "mode": "write_analysis",
            "orchestration_contract": build_first_run_automation_contract(),
            "actions_performed": _actions_performed(target_workspace_mutation=True),
            "write_boundary": {
                "analysis_dir": ANALYSIS_DIR,
                "allowed_workspace_writes": written,
                "target_workspace_mutation": "generated_analysis_only",
            },
            "written_files": written,
            "render_result": render_result,
            "baseline_comparison": render_result["baseline_comparison"],
            "cleanup_guidance": render_result["cleanup_guidance"],
        }
    )
    return result


def _ensure_stage_outside_target(workspace_path: Path, stage_path: Path) -> None:
    try:
        stage_path.relative_to(workspace_path)
    except ValueError:
        return
    raise ValueError("stage path is inside target; use --write-analysis for in-target generated analysis")


if __name__ == "__main__":
    raise SystemExit(main())
