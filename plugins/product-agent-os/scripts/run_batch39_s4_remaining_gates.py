from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from product_agent_os.batch39_s4_remaining_gates import build_remaining_gates_summary  # noqa: E402
from product_agent_os.stage_manifest import canonical_json, content_digest  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build B39-S4 remaining gates evidence artifacts.")
    parser.add_argument("--output-dir", default=str(REPO_ROOT / "docs" / "superpowers" / "specs"))
    parser.add_argument("--generated-at", default=datetime.now(UTC).replace(microsecond=0).isoformat())
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    cli_matrix = _read_json(output_dir / "batch39-s4-all-script-cli-matrix.json")
    summary = build_remaining_gates_summary(
        generated_at=args.generated_at,
        cli_help_pass_count=int(cli_matrix.get("help_pass_count", 0)),
        cli_help_gap_count=int(cli_matrix.get("help_gap_count", 0)),
        mkdocs_available=_mkdocs_available(),
    )
    closure_matrix = _build_closure_matrix(summary)
    paths = {
        "remaining_gates": output_dir / "batch39-s4-remaining-gates-summary.json",
        "closure_matrix": output_dir / "batch39-s4-closure-readiness-matrix.json",
    }
    paths["remaining_gates"].write_text(canonical_json(summary) + "\n", encoding="utf-8")
    paths["closure_matrix"].write_text(canonical_json(closure_matrix) + "\n", encoding="utf-8")
    print(
        canonical_json(
            {
                "status": summary["slice_status"],
                "written": {key: path.name for key, path in paths.items()},
                "digest": content_digest(canonical_json({"summary": summary, "closure_matrix": closure_matrix})),
            }
        )
    )
    return 0


def _build_closure_matrix(summary: dict[str, Any]) -> dict[str, Any]:
    tasks = summary["tasks"]
    blocked = [task_id for task_id, task in tasks.items() if str(task.get("status", "")).startswith("blocked")]
    approval_required = [
        task_id for task_id, task in tasks.items() if str(task.get("status", "")) == "approval_required_live_or_external_surface"
    ]
    partial = [task_id for task_id, task in tasks.items() if str(task.get("status", "")).startswith("partial")]
    return {
        "schema_version": "batch39_s4_closure_readiness_matrix_v1",
        "attempt_id": summary["attempt_id"],
        "generated_at": summary["generated_at"],
        "slice": "B39-S4",
        "closure_status": "not_release_ready_expected_blocks_recorded",
        "task_counts": {
            "total": len(tasks),
            "partial": len(partial),
            "blocked_expected": len(blocked),
            "approval_required": len(approval_required),
        },
        "blocked_expected_tasks": blocked,
        "approval_required_tasks": approval_required,
        "partial_tasks": partial,
        "go_no_go_input_for_b39_s5": {
            "go": False,
            "reason": "B39-S4 remaining gates executed, but public docs/site, runtime/browser, MCP/live, release governance and owner feedback remain gated.",
            "next_slice": "B39-S5",
        },
        "actions_performed": summary["actions_performed"],
        "unsupported_claims": summary["unsupported_claims"],
    }


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _mkdocs_available() -> bool:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "mkdocs", "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


if __name__ == "__main__":
    raise SystemExit(main())
