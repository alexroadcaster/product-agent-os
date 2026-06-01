from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))

from codex_runtime_runner.redaction import redact_payload  # noqa: E402
from product_agent_os.project_code_graph import PROJECT_GRAPH_TARGET, build_project_code_graph, graph_to_jsonl  # noqa: E402


SHRINK_GUARD_RATIO = 0.5


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a workspace into a Product-Agent OS project code graph.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print graph JSON without writing files.")
    parser.add_argument("--stage", help="Write graph artifacts to this explicit stage directory.")
    args = parser.parse_args(argv)

    if args.dry_run == bool(args.stage):
        return _print_error("choose --dry-run or --stage", exit_code=2)

    try:
        if args.dry_run:
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            graph = build_project_code_graph(workspace)
            print(json.dumps(_redacted_payload(graph), indent=2, sort_keys=True))
            return 0 if graph.get("validation", {}).get("ok") else 1
        workspace = Path(args.workspace).resolve()
        if not workspace.exists():
            raise ProjectGraphCliError("workspace does not exist")
        if not workspace.is_dir():
            raise ProjectGraphCliError("workspace is not a directory")
        result = stage_project_code_graph(workspace, Path(args.stage))
        print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
        return 0 if result.get("rendered_artifacts", {}).get("validation", {}).get("ok") else 1
    except ProjectGraphCliError as exc:
        return _print_error(str(exc), exit_code=2)
    except (OSError, ValueError):
        return _print_error("project graph scan failed", exit_code=2)


class ProjectGraphCliError(RuntimeError):
    pass


def stage_project_code_graph(workspace: Path, stage_root: Path) -> dict[str, Any]:
    """Stage graph JSON/JSONL under stage_root without mutating the workspace."""

    stage_root = stage_root.resolve()
    workspace = workspace.resolve()
    if stage_root == workspace or stage_root.is_relative_to(workspace):
        raise ProjectGraphCliError("stage output directory must be outside workspace")
    if stage_root.exists() and not stage_root.is_dir():
        raise ProjectGraphCliError("stage output path is not a directory")

    target = stage_root / PROJECT_GRAPH_TARGET
    previous_graph = _load_previous_graph(target)
    graph = build_project_code_graph(workspace, previous_graph=previous_graph)
    previous_target = target.with_name("project-code-graph.previous.json")
    validation = dict(graph.get("validation", {}))
    errors = list(validation.get("errors", []))
    previous_node_count = _previous_node_count(target)
    current_node_count = len(graph.get("nodes", []))
    if previous_node_count and current_node_count < previous_node_count * SHRINK_GUARD_RATIO:
        _backup_existing(target, previous_target)
        errors.append("shrink_guard")
        validation = {
            "ok": False,
            "checks": validation.get("checks", []),
            "errors": sorted(set(errors)),
        }
        return {
            "rendered_artifacts": {
                "status": "blocked",
                "mode": "stage",
                "root_status": "redacted",
                "files": [
                    {
                        "target_path": PROJECT_GRAPH_TARGET,
                        "action": "blocked",
                        "write_policy": "blocked",
                        "staged_path": PROJECT_GRAPH_TARGET,
                    }
                ],
                "validation": validation,
            }
        }

    _backup_existing(target, previous_target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(graph, indent=2, sort_keys=True), encoding="utf-8")
    jsonl_target = target.with_suffix(".jsonl")
    jsonl_target.write_text(graph_to_jsonl(graph), encoding="utf-8")
    return {
        "rendered_artifacts": {
            "status": "ready" if validation.get("ok") else "blocked",
            "mode": "stage",
            "root_status": "redacted",
            "files": [
                {
                    "target_path": PROJECT_GRAPH_TARGET,
                    "action": "create",
                    "write_policy": "staged_only",
                    "staged_path": PROJECT_GRAPH_TARGET,
                },
                {
                    "target_path": ".codex/product-agent-os/project-code-graph.jsonl",
                    "action": "create",
                    "write_policy": "staged_only",
                    "staged_path": ".codex/product-agent-os/project-code-graph.jsonl",
                },
            ],
            "validation": validation,
        }
    }


def _load_previous_graph(target: Path) -> dict[str, Any] | None:
    if not target.exists() or not target.is_file():
        return None
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _previous_node_count(target: Path) -> int:
    if not target.exists() or not target.is_file():
        return 0
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    nodes = payload.get("nodes")
    return len(nodes) if isinstance(nodes, list) else 0


def _backup_existing(target: Path, backup_target: Path) -> None:
    if not target.exists() or not target.is_file():
        return
    backup_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, backup_target)


def _print_error(error: str, *, exit_code: int) -> int:
    print(json.dumps({"status": "error", "error": error}, indent=2, sort_keys=True))
    return exit_code


def _redacted_payload(payload: dict[str, Any]) -> dict[str, Any]:
    redacted, _report = redact_payload(payload)
    return redacted if isinstance(redacted, dict) else payload


if __name__ == "__main__":
    raise SystemExit(main())
