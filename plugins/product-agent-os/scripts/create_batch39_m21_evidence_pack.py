from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from product_agent_os.analysis_artifact_renderer import render_first_run_analysis_artifact
from product_agent_os.batch39_m21_plugin_skill_pilot import (
    build_m21_attempt_summary,
    build_m21_three_target_rollup,
    write_m21_evidence_pack,
)
from product_agent_os.first_run_analysis import ANALYSIS_DIR, FIRST_RUN_PACKET_NAME, run_first_project_analysis


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create Batch 39 M21 three-target evidence pack.")
    parser.add_argument("--output-dir", required=True, help="Workspace-local directory for generated evidence JSON files.")
    parser.add_argument("--synthetic-target", required=True, help="Synthetic plugin/skill fixture workspace.")
    parser.add_argument("--neural-flow-target", required=True, help="Read-only Neural Flow target workspace.")
    parser.add_argument("--sol-target", required=True, help="Read-only SOL target workspace.")
    parser.add_argument("--generated-at", required=True, help="Stable ISO timestamp for deterministic evidence.")
    args = parser.parse_args(argv)

    generated_at = str(args.generated_at)
    synthetic_result, synthetic_artifact = _run_synthetic(Path(args.synthetic_target), generated_at)
    neural_flow_result = run_first_project_analysis(Path(args.neural_flow_target), generated_at=generated_at, write=False)
    sol_result = run_first_project_analysis(Path(args.sol_target), generated_at=generated_at, write=False)

    attempts = [
        build_m21_attempt_summary(
            attempt_id="B39-TEST-M21-A01",
            target_label="synthetic_plugin_skill_fixture",
            target_kind="synthetic_fixture",
            mode="synthetic_local",
            source_policy_status="verified_synthetic",
            first_run_packet=synthetic_result,
            rendered_artifact=synthetic_artifact,
            generated_at=generated_at,
        ),
        build_m21_attempt_summary(
            attempt_id="B39-TEST-M21-A02",
            target_label="Neural Flow",
            target_kind="approved_read_only_target",
            mode="read_only_comparative",
            source_policy_status="present_unverified",
            first_run_packet=neural_flow_result,
            generated_at=generated_at,
        ),
        build_m21_attempt_summary(
            attempt_id="B39-TEST-M21-A03",
            target_label="SOL",
            target_kind="approved_read_only_target",
            mode="read_only_real_target",
            source_policy_status="present_unverified",
            first_run_packet=sol_result,
            generated_at=generated_at,
        ),
    ]
    rollup = build_m21_three_target_rollup(attempts, generated_at=generated_at)
    written = write_m21_evidence_pack(Path(args.output_dir), attempts, rollup)
    print(json.dumps({"status": "ok", "written_files": sorted(written)}, ensure_ascii=False, sort_keys=True))
    return 0


def _run_synthetic(target: Path, generated_at: str) -> tuple[dict[str, Any], dict[str, Any]]:
    dry_run_result = run_first_project_analysis(target, generated_at=generated_at, write=False)
    with tempfile.TemporaryDirectory(prefix="batch39-m21-synthetic-") as tmp:
        temp_workspace = Path(tmp) / "workspace"
        shutil.copytree(target, temp_workspace)
        render_result = render_first_run_analysis_artifact(dry_run_result["packet"], temp_workspace)
        artifact = {
            "status": "rendered_in_temp_copy",
            "page_count": int(render_result.get("page_count", 0) or 0),
            "manifest_ref": f"{ANALYSIS_DIR}/analysis-manifest.json",
            "packet_ref": f"{ANALYSIS_DIR}/{FIRST_RUN_PACKET_NAME}",
        }
    return dry_run_result, artifact


if __name__ == "__main__":
    raise SystemExit(main())

