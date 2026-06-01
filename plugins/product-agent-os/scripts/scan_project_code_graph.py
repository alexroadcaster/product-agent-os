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
from product_agent_os.project_graph_backend import (  # noqa: E402
    disable_local_query_backend,
    handle_backend_api_request,
    load_local_query_backend_store,
    stage_local_query_backend,
)
from product_agent_os.project_graph_index import load_static_search_index, stage_project_graph_search_index  # noqa: E402
from product_agent_os.project_graph_queries import load_graph_artifact, query_project_graph  # noqa: E402
from product_agent_os.project_graph_semantic import (  # noqa: E402
    disable_semantic_retrieval_index,
    load_semantic_retrieval_index,
    stage_semantic_retrieval_index,
)


SHRINK_GUARD_RATIO = 0.5


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a workspace into a Product-Agent OS project code graph.")
    parser.add_argument("workspace")
    parser.add_argument("--dry-run", action="store_true", help="Print graph JSON without writing files.")
    parser.add_argument("--stage", help="Write graph artifacts to this explicit stage directory.")
    parser.add_argument("--query", help="Run a bounded query against an existing graph artifact.")
    parser.add_argument("--build-index", action="store_true", help="Build or reuse an offline static search index from --graph.")
    parser.add_argument("--build-backend", action="store_true", help="Stage a disabled-by-default local query backend store from --graph.")
    parser.add_argument("--disable-backend", action="store_true", help="Delete the generated local query backend store from --stage.")
    parser.add_argument("--build-semantic-index", action="store_true", help="Stage an approved semantic retrieval index from --graph.")
    parser.add_argument("--disable-semantic-index", action="store_true", help="Delete the generated semantic retrieval index from --stage.")
    parser.add_argument("--graph", help="Path to project-code-graph.json or project-code-graph.jsonl for query mode.")
    parser.add_argument("--index", help="Optional project-code-graph-search-index.json for indexed search query mode.")
    parser.add_argument("--backend", help="Optional project-code-graph-backend.json for backend query mode.")
    parser.add_argument("--backend-approval", help="JSON approval packet for --build-backend.")
    parser.add_argument("--semantic-index", help="Optional project-code-graph-semantic-index.json for semantic search query mode.")
    parser.add_argument("--semantic-approval", help="JSON approval packet for --build-semantic-index.")
    parser.add_argument("--node-id", help="Source node id for graph query mode.")
    parser.add_argument("--target-id", help="Target node id for graph path/trace query mode.")
    parser.add_argument("--text", help="Search text for graph query mode.")
    parser.add_argument("--max-results", type=int, default=25, help="Maximum query items to return.")
    parser.add_argument("--max-depth", type=int, default=6, help="Maximum path/trace depth.")
    parser.add_argument("--max-tokens", type=int, default=4000, help="Approximate query packet token budget.")
    parser.add_argument("--hub-threshold", type=int, help="Suppress neighbor expansion above this degree.")
    parser.add_argument("--node-type", action="append", default=[], help="Node type filter for query mode.")
    parser.add_argument("--edge-type", action="append", default=[], help="Edge type filter for query mode.")
    parser.add_argument("--confidence", action="append", default=[], help="Edge confidence filter for query mode.")
    parser.add_argument("--path-prefix", action="append", default=[], help="Relative path prefix filter for query mode.")
    args = parser.parse_args(argv)

    mode_count = (
        int(bool(args.dry_run))
        + int(
            bool(args.stage)
            and not args.build_index
            and not args.build_backend
            and not args.disable_backend
            and not args.build_semantic_index
            and not args.disable_semantic_index
        )
        + int(bool(args.query))
        + int(bool(args.build_index))
        + int(bool(args.build_backend))
        + int(bool(args.disable_backend))
        + int(bool(args.build_semantic_index))
        + int(bool(args.disable_semantic_index))
    )
    if mode_count != 1:
        return _print_error(
            "choose exactly one mode: --dry-run, --stage, --query, --build-index, --build-backend, "
            "--disable-backend, --build-semantic-index, or --disable-semantic-index",
            exit_code=2,
        )

    try:
        if args.query:
            if args.backend:
                store = load_local_query_backend_store(args.backend)
                request = _query_request(args)
                packet = handle_backend_api_request(
                    store,
                    {"method": "POST", "path": "/query", "body": request},
                )
                print(json.dumps(_redacted_payload(packet), indent=2, sort_keys=True))
                return 0 if packet.get("status") != "blocked" else 1
            if not args.graph:
                raise ProjectGraphCliError("query mode requires --graph")
            graph = load_graph_artifact(Path(args.graph))
            static_index = load_static_search_index(args.index) if args.index else None
            semantic_index = load_semantic_retrieval_index(args.semantic_index) if args.semantic_index else None
            request = _query_request(args)
            packet = query_project_graph(
                graph,
                {key: value for key, value in request.items() if value not in (None, [], "")},
                static_index=static_index,
                semantic_index=semantic_index,
            )
            print(json.dumps(_redacted_payload(packet), indent=2, sort_keys=True))
            return 0 if packet.get("status") != "blocked" else 1
        if args.build_index:
            if not args.graph:
                raise ProjectGraphCliError("build-index mode requires --graph")
            if not args.stage:
                raise ProjectGraphCliError("build-index mode requires --stage")
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            try:
                result = stage_project_graph_search_index(Path(args.graph), Path(args.stage), workspace=workspace)
            except ValueError as exc:
                raise ProjectGraphCliError(str(exc)) from exc
            print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
            return 0 if result.get("rendered_artifacts", {}).get("status") == "ready" else 1
        if args.build_backend:
            if not args.graph:
                raise ProjectGraphCliError("build-backend mode requires --graph")
            if not args.stage:
                raise ProjectGraphCliError("build-backend mode requires --stage")
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            approval = _load_json_file(args.backend_approval) if args.backend_approval else None
            try:
                result = stage_local_query_backend(
                    Path(args.graph),
                    Path(args.stage),
                    workspace=workspace,
                    approval=approval,
                    static_index_artifact=Path(args.index) if args.index else None,
                )
            except ValueError as exc:
                raise ProjectGraphCliError(str(exc)) from exc
            print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
            return 0 if result.get("rendered_artifacts", {}).get("status") == "ready" else 1
        if args.disable_backend:
            if not args.stage:
                raise ProjectGraphCliError("disable-backend mode requires --stage")
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            try:
                result = disable_local_query_backend(Path(args.stage), workspace=workspace)
            except ValueError as exc:
                raise ProjectGraphCliError(str(exc)) from exc
            print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
            return 0
        if args.build_semantic_index:
            if not args.graph:
                raise ProjectGraphCliError("build-semantic-index mode requires --graph")
            if not args.stage:
                raise ProjectGraphCliError("build-semantic-index mode requires --stage")
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            approval = _load_json_file(args.semantic_approval) if args.semantic_approval else None
            try:
                result = stage_semantic_retrieval_index(
                    Path(args.graph),
                    Path(args.stage),
                    workspace=workspace,
                    approval=approval,
                    static_index_artifact=Path(args.index) if args.index else None,
                )
            except ValueError as exc:
                raise ProjectGraphCliError(str(exc)) from exc
            print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
            return 0 if result.get("rendered_artifacts", {}).get("status") == "ready" else 1
        if args.disable_semantic_index:
            if not args.stage:
                raise ProjectGraphCliError("disable-semantic-index mode requires --stage")
            workspace = Path(args.workspace).resolve()
            if not workspace.exists():
                raise ProjectGraphCliError("workspace does not exist")
            if not workspace.is_dir():
                raise ProjectGraphCliError("workspace is not a directory")
            try:
                result = disable_semantic_retrieval_index(Path(args.stage), workspace=workspace)
            except ValueError as exc:
                raise ProjectGraphCliError(str(exc)) from exc
            print(json.dumps(_redacted_payload(result), indent=2, sort_keys=True))
            return 0
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


def _query_request(args: argparse.Namespace) -> dict[str, Any]:
    request = {
        "query": args.query,
        "node_id": args.node_id,
        "target_id": args.target_id,
        "text": args.text,
        "max_results": args.max_results,
        "max_depth": args.max_depth,
        "max_tokens": args.max_tokens,
    }
    if args.hub_threshold is not None:
        request["hub_threshold"] = args.hub_threshold
    if args.node_type:
        request["node_types"] = args.node_type
    if args.edge_type:
        request["edge_types"] = args.edge_type
    if args.confidence:
        request["confidence"] = args.confidence
    if args.path_prefix:
        request["path_prefixes"] = args.path_prefix
    return {key: value for key, value in request.items() if value not in (None, [], "")}


def _load_json_file(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ProjectGraphCliError("approval packet must be a JSON object")
    return payload


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
