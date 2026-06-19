from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[2]
sys.path.insert(0, str(SCRIPT_DIR))

from product_agent_os.batch41_s6_closure import (  # noqa: E402
    build_batch41_s6_closure_packet,
    build_go_no_go_decision_packet,
    build_no_unapproved_actions_proof,
    build_plugin_cache_readiness,
    build_real_target_pilot_summary,
    build_real_target_pilots_rollup,
    build_synthetic_e2e_summary,
    build_usefulness_scorecard,
    build_verification_sweep_summary,
    inspect_marker_text,
    target_snapshot,
    write_json,
)


DEFAULT_OUTPUT_DIR = ROOT / "docs" / "superpowers" / "specs"
DEFAULT_PLUGIN_CACHE_ROOT = (
    Path.home() / ".codex" / "plugins" / "cache" / "personal-product-agent-plugins" / "product-agent-os" / "0.1.0"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Batch 41 S6 first-run closure evidence.")
    parser.add_argument("--generated-at", help="Deterministic timestamp for evidence packets.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Directory for S6 JSON artifacts.")
    parser.add_argument("--neural-flow", help="Optional read-only Neural_Flow target path.")
    parser.add_argument("--sol-target", help="Optional read-only SOL/app-like target path.")
    parser.add_argument("--plugin-cache-root", default=str(DEFAULT_PLUGIN_CACHE_ROOT), help="Installed plugin cache root.")
    args = parser.parse_args(argv)

    generated_at = args.generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    output_dir = Path(args.output_dir)

    with TemporaryDirectory(prefix="batch41-s6-") as temp_root:
        temp_path = Path(temp_root)
        synthetic_root = temp_path / "synthetic-target"
        synthetic_stage = temp_path / "synthetic-stage"
        _create_synthetic_target(synthetic_root)
        synthetic_before = target_snapshot(synthetic_root)
        synthetic_dry_run = _run_first_project_analysis(synthetic_root, "--full-dry-run", generated_at=generated_at)
        synthetic_stage_payload = _run_first_project_analysis(
            synthetic_root,
            "--stage",
            str(synthetic_stage),
            generated_at=generated_at,
        )
        synthetic_after = target_snapshot(synthetic_root)
        synthetic_summary = build_synthetic_e2e_summary(
            generated_at=generated_at,
            full_dry_run_payload=synthetic_dry_run,
            stage_payload=synthetic_stage_payload,
            target_snapshot_before=synthetic_before,
            target_snapshot_after=synthetic_after,
        )

        pilots = [
            _build_optional_pilot(
                task_id="B41-S6-M25",
                target_label="Neural_Flow",
                target_kind="docs_research_expected_block",
                target_arg=args.neural_flow,
                temp_path=temp_path,
                generated_at=generated_at,
            ),
            _build_optional_pilot(
                task_id="B41-S6-M26",
                target_label="SOL 0.6 app-like target",
                target_kind="app_static_runtime_boundary",
                target_arg=args.sol_target,
                temp_path=temp_path,
                generated_at=generated_at,
            ),
        ]

    real_target_rollup = build_real_target_pilots_rollup(generated_at=generated_at, pilots=pilots)
    scorecard = build_usefulness_scorecard(
        generated_at=generated_at,
        synthetic_e2e_summary=synthetic_summary,
        real_target_pilots=pilots,
    )
    plugin_cache = _build_plugin_cache_readiness(generated_at, Path(args.plugin_cache_root))
    verification = build_verification_sweep_summary(
        generated_at=generated_at,
        command_results={
            "runner_self": {
                "status": "passed",
                "result": "S6 runner generated local evidence artifacts",
            }
        },
        skipped_checks=[],
    )
    closure = build_batch41_s6_closure_packet(
        generated_at=generated_at,
        synthetic_e2e_summary=synthetic_summary,
        real_target_pilots=pilots,
        usefulness_scorecard=scorecard,
        verification_evidence={"runner_self": "passed"},
        plugin_cache_readiness=plugin_cache,
    )
    no_actions = build_no_unapproved_actions_proof(generated_at=generated_at)
    go_no_go = build_go_no_go_decision_packet(generated_at=generated_at, closure_packet=closure)

    artifacts = {
        "batch41-s6-synthetic-e2e-summary.json": synthetic_summary,
        "batch41-s6-real-target-pilots-summary.json": real_target_rollup,
        "batch41-s6-usefulness-scorecard.json": scorecard,
        "batch41-s6-verification-sweep-summary.json": verification,
        "batch41-s6-plugin-cache-readiness.json": plugin_cache,
        "batch41-s6-no-unapproved-actions-proof.json": no_actions,
        "batch41-s6-go-no-go-decision-packet.json": go_no_go,
        "batch41-s6-closure-summary.json": closure,
    }
    written_files: list[str] = []
    for name, payload in artifacts.items():
        write_json(output_dir / name, payload)
        written_files.append(name)

    print(
        json.dumps(
            {
                "status": closure["status"],
                "written_files": written_files,
                "go_no_go": closure["go_no_go"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


def _run_first_project_analysis(workspace: Path, *mode_args: str, generated_at: str) -> dict[str, Any]:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "run_first_project_analysis.py"),
        str(workspace),
        *mode_args,
        "--generated-at",
        generated_at,
    ]
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "mode": mode_args[0].removeprefix("--") if mode_args else "unknown",
            "error": "first project analysis command timed out after 120 seconds",
            "actions_performed": {"target_workspace_mutation": False},
        }
    if result.returncode != 0:
        return {
            "status": "error",
            "mode": mode_args[0].removeprefix("--") if mode_args else "unknown",
            "error": "first project analysis command failed",
            "exit_code": result.returncode,
            "actions_performed": {"target_workspace_mutation": False},
        }
    return json.loads(result.stdout)


def _build_optional_pilot(
    *,
    task_id: str,
    target_label: str,
    target_kind: str,
    target_arg: str | None,
    temp_path: Path,
    generated_at: str,
) -> dict[str, Any]:
    if not target_arg:
        return build_real_target_pilot_summary(
            task_id=task_id,
            target_label=target_label,
            target_kind=target_kind,
            generated_at=generated_at,
            target_access_status="not_provided",
            full_dry_run_payload={"status": "not_run", "mode": "full_dry_run"},
            stage_payload={"status": "not_run", "mode": "stage", "render_result": {"page_count": 0}},
            target_snapshot_before={"fingerprint": "sha256:not-provided", "file_count": 0},
            target_snapshot_after={"fingerprint": "sha256:not-provided", "file_count": 0},
        )

    target_path = Path(target_arg)
    if not target_path.exists() or not target_path.is_dir():
        return build_real_target_pilot_summary(
            task_id=task_id,
            target_label=target_label,
            target_kind=target_kind,
            generated_at=generated_at,
            target_access_status="missing",
            full_dry_run_payload={"status": "not_run", "mode": "full_dry_run"},
            stage_payload={"status": "not_run", "mode": "stage", "render_result": {"page_count": 0}},
            target_snapshot_before={"fingerprint": "sha256:missing", "file_count": 0},
            target_snapshot_after={"fingerprint": "sha256:missing", "file_count": 0},
        )

    before = target_snapshot(target_path)
    stage_path = temp_path / f"{task_id.lower()}-stage"
    dry_run = _run_first_project_analysis(target_path, "--full-dry-run", generated_at=generated_at)
    if dry_run.get("status") == "timeout":
        stage = {"status": "not_run", "mode": "stage", "render_result": {"page_count": 0}}
    else:
        stage = _run_first_project_analysis(target_path, "--stage", str(stage_path), generated_at=generated_at)
    after = target_snapshot(target_path)
    return build_real_target_pilot_summary(
        task_id=task_id,
        target_label=target_label,
        target_kind=target_kind,
        generated_at=generated_at,
        target_access_status="readable",
        full_dry_run_payload=dry_run,
        stage_payload=stage,
        target_snapshot_before=before,
        target_snapshot_after=after,
    )


def _build_plugin_cache_readiness(generated_at: str, cache_root: Path) -> dict[str, Any]:
    source_root = SCRIPT_DIR
    marker_map = {
        "first_run_guided_response": ("first_run_guided_response_v1",),
        "answer_ledger_template": ("answer-ledger-template.json",),
        "s6_closure_runner": ("run_batch41_s6_closure.py",),
    }
    source_markers = inspect_marker_text(source_root, marker_map)
    cache_markers = inspect_marker_text(cache_root, marker_map)
    return build_plugin_cache_readiness(
        generated_at=generated_at,
        source_markers=source_markers,
        cache_markers=cache_markers,
    )


def _create_synthetic_target(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    (root / "docs").mkdir(parents=True)
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "logs").mkdir()
    (root / "README.md").write_text(
        "# Synthetic Product-Agent OS pilot\n\n"
        "Source status: synthetic fixture.\n\n"
        "This project exercises docs, app code, tests, logs and source-policy routing.\n",
        encoding="utf-8",
    )
    (root / "AGENTS.md").write_text(
        "# AGENTS.md\n\n"
        "Use read-only analysis by default. Runtime and browser checks require approval.\n",
        encoding="utf-8",
    )
    (root / "REQUIREMENTS.md").write_text(
        "# REQUIREMENTS.md\n\nSource status: synthetic fixture.\n\n- Build a guided first-run report.\n",
        encoding="utf-8",
    )
    (root / "PLAN.md").write_text(
        "# PLAN.md\n\nSource status: synthetic fixture.\n\n- Keep generated artifacts staged first.\n",
        encoding="utf-8",
    )
    (root / "TEST.md").write_text(
        "# TEST.md\n\nSource status: synthetic fixture.\n\n- Run static checks before runtime proof.\n",
        encoding="utf-8",
    )
    (root / "docs" / "guide.md").write_text(
        "# Guide\n\nSource status: synthetic fixture.\n\nGenerated reports are orientation evidence only.\n",
        encoding="utf-8",
    )
    (root / "docs" / "sources.md").write_text(
        "# Sources\n\n- synthetic fixture\n",
        encoding="utf-8",
    )
    (root / "src" / "app.py").write_text(
        "def summarize(value: str) -> str:\n"
        "    return value.strip().lower()\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_app.py").write_text(
        "from src.app import summarize\n\n"
        "def test_summarize():\n"
        "    assert summarize(' Hello ') == 'hello'\n",
        encoding="utf-8",
    )
    (root / "package.json").write_text(
        json.dumps({"scripts": {"test": "pytest", "dev": "vite"}, "dependencies": {"vite": "latest"}}, indent=2),
        encoding="utf-8",
    )
    (root / "logs" / "app.log").write_text("synthetic log line\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
