from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from product_agent_os.batch39_s4_hardening import (  # noqa: E402
    FULL_HARDENING_ATTEMPT_ID,
    FULL_HARDENING_SCHEMA_VERSION,
    build_runtime_browser_harness_status,
    build_target_comparison,
    build_target_dependency_readiness,
    summarize_cli_matrix,
)
from product_agent_os.stage_manifest import canonical_json, content_digest  # noqa: E402


SCRIPT_TIMEOUT_SECONDS = 25
TARGET_COMMAND_TIMEOUT_SECONDS = 120
OUTPUT_NAMES = {
    "sol_0_6": "batch39-s4-full-hardening-sol_0_6-summary.json",
    "neural_flow": "batch39-s4-full-hardening-neural_flow-summary.json",
    "comparison": "batch39-s4-full-hardening-comparison.json",
    "cli_matrix": "batch39-s4-all-script-cli-matrix.json",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build B39-S4 full hardening evidence artifacts.")
    parser.add_argument("--sol", required=True, help="Path to SOL 0.6 target workspace")
    parser.add_argument("--neural-flow", required=True, help="Path to Neural_Flow target workspace")
    parser.add_argument("--output-dir", default=str(REPO_ROOT / "docs" / "superpowers" / "specs"))
    parser.add_argument("--generated-at", default=datetime.now(UTC).replace(microsecond=0).isoformat())
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    targets = {
        "sol_0_6": {
            "path": Path(args.sol),
            "kind": "node_fullstack",
            "runtime_entrypoints": ["frontend:npm run dev", "frontend:npm run start", "backend:npm run dev", "backend:npm run start"],
            "mutation_risks": ["frontend .next cache writes", "backend .sol_data LanceDB writes", "backend dist/build writes"],
            "provider_risks": ["backend @google/genai dependency", "backend provider credential environment keys"],
        },
        "neural_flow": {
            "path": Path(args.neural_flow),
            "kind": "docs_research_only",
            "runtime_entrypoints": [],
            "mutation_risks": [],
            "provider_risks": [],
        },
    }

    cli_matrix = build_cli_matrix()
    target_artifacts: dict[str, dict[str, Any]] = {}
    for target_id, config in targets.items():
        target_artifacts[target_id] = build_target_artifact(
            target_id=target_id,
            target_path=config["path"],
            target_kind=config["kind"],
            generated_at=args.generated_at,
            runtime_entrypoints=config["runtime_entrypoints"],
            mutation_risks=config["mutation_risks"],
            provider_risks=config["provider_risks"],
        )

    comparison = build_comparison_artifact(generated_at=args.generated_at, target_artifacts=target_artifacts)

    artifacts = {
        "cli_matrix": cli_matrix,
        "sol_0_6": target_artifacts["sol_0_6"],
        "neural_flow": target_artifacts["neural_flow"],
        "comparison": comparison,
    }
    for key, payload in artifacts.items():
        output_path = output_dir / OUTPUT_NAMES[key]
        output_path.write_text(canonical_json(payload) + "\n", encoding="utf-8")

    print(canonical_json({"written": {key: OUTPUT_NAMES[key] for key in artifacts}, "status": comparison["status"]}))
    return 0


def build_cli_matrix() -> dict[str, Any]:
    rows = []
    for script_path in sorted(SCRIPTS_DIR.glob("*.py")):
        if script_path.name == Path(__file__).name:
            continue
        result = _run_command([sys.executable, str(script_path), "--help"], timeout=SCRIPT_TIMEOUT_SECONDS)
        rows.append(
            {
                "script": script_path.name,
                "help_status": "passed" if result["exit_code"] == 0 else "failed",
                "exit_code": result["exit_code"],
                "stdout_parse_status": _parse_status(result["stdout"]),
                "stderr_present": bool(result["stderr"]),
                "stdout_preview": _preview(result["stdout"]),
                "stderr_preview": _preview(result["stderr"]),
                "write_scope": "no_write_executed_help_only",
            }
        )
    matrix = summarize_cli_matrix(rows)
    matrix.update(
        {
            "schema_version": "batch39_s4_all_script_cli_matrix_v1",
            "attempt_id": FULL_HARDENING_ATTEMPT_ID,
            "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        }
    )
    matrix["matrix_digest"] = content_digest(canonical_json(matrix))
    return matrix


def build_target_artifact(
    *,
    target_id: str,
    target_path: Path,
    target_kind: str,
    generated_at: str,
    runtime_entrypoints: list[str],
    mutation_risks: list[str],
    provider_risks: list[str],
) -> dict[str, Any]:
    inventory = collect_static_inventory(target_path)
    before_digest = digest_selected_files(target_path)
    dependency = build_target_dependency_readiness(
        target_id=target_id,
        target_kind=target_kind,
        file_refs=inventory["file_refs"],
        runtime_write_risks=mutation_risks if target_kind != "docs_research_only" else ["no runnable runtime entrypoint"],
        provider_risks=provider_risks,
    )
    commands = run_target_command_matrix(target_path)
    after_digest = digest_selected_files(target_path)
    browser_tool_status = browser_preflight_status()
    runtime_browser = build_runtime_browser_harness_status(
        target_id=target_id,
        runtime_entrypoints=runtime_entrypoints,
        browser_tool_status=browser_tool_status,
        mutation_risks=mutation_risks if target_kind != "docs_research_only" else ["no runnable runtime entrypoint"],
        provider_risks=provider_risks,
        executed_runtime=False,
        executed_browser=False,
    )
    artifact = {
        "schema_version": FULL_HARDENING_SCHEMA_VERSION,
        "attempt_id": FULL_HARDENING_ATTEMPT_ID,
        "generated_at": generated_at,
        "target_id": target_id,
        "target_ref": target_id,
        "target_kind": target_kind,
        "target_exists": target_path.exists(),
        "target_is_dir": target_path.is_dir(),
        "inventory": inventory,
        "dependency_readiness": dependency,
        "target_command_matrix": commands,
        "runtime_browser_harness": runtime_browser,
        "mutation_probe": {
            "selected_file_digest_before": before_digest,
            "selected_file_digest_after": after_digest,
            "selected_file_digest_unchanged": before_digest == after_digest,
            "scope": "manifest_and_control_plane_files_only",
        },
        "actions_performed": {
            "target_workspace_mutation": False,
            "dependency_install": False,
            "provider_api_call": False,
            "live_browser_automation": False,
            "git_stage_commit_push_pr": False,
            "deploy_publish_release_automation": False,
        },
        "unsupported_claims": [
            "runtime/browser QA pass is not claimed",
            "full app readiness is not claimed",
            "provider/API behavior is not claimed",
            "source policy clean state is not claimed when validators block",
        ],
    }
    artifact["artifact_digest"] = content_digest(canonical_json(artifact))
    return artifact


def collect_static_inventory(target_path: Path) -> dict[str, Any]:
    refs: list[str] = []
    manifest_refs: list[str] = []
    excluded_refs: list[str] = []
    interesting_names = {
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "pyproject.toml",
        "requirements.txt",
        "mkdocs.yml",
        "AGENTS.md",
        "REQUIREMENTS.md",
        "PLAN.md",
        "TEST.md",
        "EVALS.md",
        "RUNLOG.md",
        "README.md",
    }
    excluded_dirs = {".git", ".next", "dist", "node_modules", "antigravity-awesome-skills-main", "__pycache__"}
    if not target_path.exists():
        return {"file_refs": [], "manifest_refs": [], "excluded_refs": [], "package_scripts": {}, "env_key_names": []}

    for root, dirs, files in os.walk(target_path):
        root_path = Path(root)
        relative_root = _relative_ref(target_path, root_path)
        pruned = []
        for dirname in list(dirs):
            if dirname in excluded_dirs:
                excluded_refs.append(_join_ref(relative_root, dirname))
                pruned.append(dirname)
        for dirname in pruned:
            dirs.remove(dirname)
        for filename in files:
            if filename in interesting_names:
                ref = _join_ref(relative_root, filename)
                refs.append(ref)
                if filename in {"package.json", "package-lock.json", "pyproject.toml", "requirements.txt", "mkdocs.yml"}:
                    manifest_refs.append(ref)

    package_scripts = {}
    for manifest_ref in manifest_refs:
        if not manifest_ref.endswith("package.json"):
            continue
        manifest_path = target_path / Path(manifest_ref)
        try:
            package = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            continue
        scripts = package.get("scripts") if isinstance(package, dict) else {}
        dependencies = package.get("dependencies") if isinstance(package, dict) else {}
        package_scripts[manifest_ref] = {
            "scripts": sorted(scripts) if isinstance(scripts, dict) else [],
            "dependency_names": sorted(dependencies) if isinstance(dependencies, dict) else [],
        }

    return {
        "file_refs": sorted(set(refs + excluded_refs)),
        "manifest_refs": sorted(set(manifest_refs)),
        "excluded_refs": sorted(set(excluded_refs)),
        "package_scripts": package_scripts,
        "env_key_names": env_key_names(target_path),
    }


def env_key_names(target_path: Path) -> list[str]:
    keys: set[str] = set()
    for env_ref in ("backend/.env", "backend/sol.env", ".env", "sol.env"):
        env_path = target_path / Path(env_ref)
        if not env_path.exists() or not env_path.is_file():
            continue
        try:
            for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                clean = line.strip()
                if not clean or clean.startswith("#") or "=" not in clean:
                    continue
                keys.add(clean.split("=", 1)[0].strip())
        except OSError:
            continue
    return sorted(keys)


def digest_selected_files(target_path: Path) -> dict[str, str]:
    refs = [
        "package.json",
        "package-lock.json",
        "frontend/package.json",
        "frontend/package-lock.json",
        "backend/package.json",
        "backend/package-lock.json",
        "AGENTS.md",
        "REQUIREMENTS.md",
        "PLAN.md",
        "TEST.md",
        "EVALS.md",
        "RUNLOG.md",
        "README.md",
        "architecture-v2.md",
        "architecture.md",
        "sol-ide.json",
    ]
    digests: dict[str, str] = {}
    for ref in refs:
        path = target_path / Path(ref)
        if not path.exists() or not path.is_file():
            continue
        try:
            digests[ref] = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            digests[ref] = "unreadable"
    return digests


def run_target_command_matrix(target_path: Path) -> dict[str, Any]:
    commands = {
        "detect_project": [sys.executable, str(SCRIPTS_DIR / "detect_project.py"), str(target_path)],
        "source_policy": [sys.executable, str(SCRIPTS_DIR / "validate_source_policy.py"), str(target_path)],
        "first_run_dry_run": [
            sys.executable,
            str(SCRIPTS_DIR / "run_first_project_analysis.py"),
            str(target_path),
            "--dry-run",
            "--generated-at",
            "2026-06-18T00:00:00Z",
        ],
        "methodology_audit": [sys.executable, str(SCRIPTS_DIR / "run_methodology_audit.py"), str(target_path), "--json"],
        "project_graph_dry_run": [sys.executable, str(SCRIPTS_DIR / "scan_project_code_graph.py"), str(target_path), "--dry-run"],
        "runtime_contract": [
            sys.executable,
            str(SCRIPTS_DIR / "run_codex_runtime_runner.py"),
            str(target_path),
            "--contract",
            "--intent-hint",
            "read only target inspection",
        ],
    }
    rows: dict[str, Any] = {}
    for name, command in commands.items():
        result = _run_command(command, timeout=TARGET_COMMAND_TIMEOUT_SECONDS)
        rows[name] = {
            "command": _command_shape(name),
            "exit_code": result["exit_code"],
            "stdout_parse_status": _parse_status(result["stdout"]),
            "stderr_present": bool(result["stderr"]),
            "stdout_summary": summarize_json_stdout(result["stdout"]),
            "stderr_preview": _preview(result["stderr"]),
        }
    return {
        "status": "executed_read_only_with_expected_blocks",
        "rows": rows,
        "target_workspace_mutation_performed": False,
        "provider_api_calls_performed": False,
    }


def summarize_json_stdout(stdout: str) -> dict[str, Any]:
    if not stdout.strip():
        return {}
    payload = _loads_json_prefix(stdout)
    if payload is None:
        return {"preview": _preview(stdout)}
    summary: dict[str, Any] = {}
    if isinstance(payload, dict):
        for key in ("status", "schema_version", "mode", "usage_mode", "summary", "readiness", "readiness_summary"):
            if key in payload:
                summary[key] = payload[key]
        if "nodes" in payload or "edges" in payload:
            summary["nodes"] = _collection_count(payload.get("nodes"))
            summary["edges"] = _collection_count(payload.get("edges"))
        graph = payload.get("graph") if isinstance(payload.get("graph"), dict) else None
        if graph:
            summary["graph"] = {"nodes": _collection_count(graph.get("nodes")), "edges": _collection_count(graph.get("edges"))}
        if "observations" in payload:
            summary["observations"] = _collection_count(payload.get("observations"))
        if "artifact_targets" in payload:
            summary["artifact_targets"] = payload.get("artifact_targets")
        if not summary:
            for key in sorted(payload)[:8]:
                value = payload[key]
                if isinstance(value, (str, int, float, bool)) or value is None:
                    summary[key] = value
    return _redact_payload(summary)


def build_comparison_artifact(*, generated_at: str, target_artifacts: dict[str, dict[str, Any]]) -> dict[str, Any]:
    previous = load_previous_summaries()
    comparisons: dict[str, Any] = {}
    for target_id, current_artifact in target_artifacts.items():
        graph_summary = _current_graph_summary(current_artifact)
        current = {
            "dependency_readiness": {"status": current_artifact["dependency_readiness"]["status"]},
            "runtime_browser": {"status": current_artifact["runtime_browser_harness"]["status"]},
            "project_graph": graph_summary,
            "source_policy": _command_status(current_artifact, "source_policy"),
            "runtime_contract": _command_status(current_artifact, "runtime_contract"),
        }
        comparisons[target_id] = build_target_comparison(
            target_id=target_id,
            previous=previous.get(target_id, {}),
            current=current,
        )
    artifact = {
        "schema_version": "batch39_s4_full_hardening_comparison_v1",
        "attempt_id": FULL_HARDENING_ATTEMPT_ID,
        "generated_at": generated_at,
        "status": "partial_pass_full_hardening_evidence_runtime_browser_blocked",
        "comparisons": comparisons,
        "previous_sources": previous.get("sources", []),
        "unsupported_claims": [
            "runtime/browser pass is not claimed for either target",
            "target mutation, provider/API, git, release, deploy and automation actions were not performed",
        ],
    }
    artifact["artifact_digest"] = content_digest(canonical_json(artifact))
    return artifact


def load_previous_summaries() -> dict[str, Any]:
    specs = REPO_ROOT / "docs" / "superpowers" / "specs"
    previous: dict[str, Any] = {
        "sources": [],
        "sol_0_6": {"runtime_browser": {"status": "not_performed"}, "project_graph": {"nodes": 0, "edges": 0}},
        "neural_flow": {"runtime_browser": {"status": "not_performed"}, "project_graph": {"nodes": 0, "edges": 0}},
    }
    graph_path = specs / "batch39-s4-graph-depth-03-real-target-retest-summary.json"
    if graph_path.exists():
        previous["sources"].append(graph_path.name)
        try:
            payload = json.loads(graph_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        target_label = str(payload.get("target_label", "")).lower() if isinstance(payload, dict) else ""
        if "sol" in target_label:
            current = payload.get("comparison", {}).get("current", {}) if isinstance(payload.get("comparison"), dict) else {}
            previous["sol_0_6"]["project_graph"] = {
                "nodes": _collection_count(current.get("node_count")),
                "edges": _collection_count(current.get("edge_count")),
            }
    for target_id, filename in {
        "sol_0_6": "batch39-s4-retest-sol_0_6-summary.json",
        "neural_flow": "batch39-s4-retest-neural_flow-summary.json",
    }.items():
        path = specs / filename
        if not path.exists():
            continue
        previous["sources"].append(filename)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {}
        previous[target_id]["source_policy"] = _previous_command(payload, "source_policy")
        previous[target_id]["runtime_contract"] = _previous_command(payload, "runtime_contract")
        previous[target_id]["runtime_browser"] = {"status": "not_performed"}
    return previous


def _extract_graph_numbers(payload: Any, target_id: str) -> dict[str, int]:
    encoded_key = "SOL" if target_id == "sol_0_6" else "Neural"
    candidates: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            text = json.dumps(value, ensure_ascii=False)
            if encoded_key.lower() in text.lower():
                candidates.append(value)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    for candidate in candidates:
        nodes = candidate.get("nodes") or candidate.get("node_count")
        edges = candidate.get("edges") or candidate.get("edge_count")
        if nodes is not None or edges is not None:
            return {"nodes": _collection_count(nodes), "edges": _collection_count(edges)}
    return {"nodes": 0, "edges": 0}


def _previous_command(payload: dict[str, Any], name: str) -> dict[str, Any]:
    commands = payload.get("commands") if isinstance(payload.get("commands"), dict) else {}
    row = commands.get(name) if isinstance(commands.get(name), dict) else {}
    return {"exit_code": row.get("exit_code"), "stdout_parse_status": row.get("stdout_parse_status")}


def _current_graph_summary(artifact: dict[str, Any]) -> dict[str, int]:
    row = artifact["target_command_matrix"]["rows"].get("project_graph_dry_run", {})
    summary = row.get("stdout_summary") if isinstance(row.get("stdout_summary"), dict) else {}
    nodes = summary.get("nodes")
    edges = summary.get("edges")
    graph = summary.get("graph") if isinstance(summary.get("graph"), dict) else {}
    return {"nodes": _int(nodes or graph.get("nodes")), "edges": _int(edges or graph.get("edges"))}


def _command_status(artifact: dict[str, Any], name: str) -> dict[str, Any]:
    row = artifact["target_command_matrix"]["rows"].get(name, {})
    return {"exit_code": row.get("exit_code"), "stdout_parse_status": row.get("stdout_parse_status")}


def browser_preflight_status() -> str:
    try:
        result = subprocess.run(
            ["node", "-e", "require.resolve('playwright')"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "blocked_playwright_unavailable"
    return "available" if result.returncode == 0 else "blocked_playwright_unavailable"


def _run_command(command: list[str], *, timeout: int) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return {
            "exit_code": result.returncode,
            "stdout": _redact_text(result.stdout),
            "stderr": _redact_text(result.stderr),
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "exit_code": "timeout",
            "stdout": _redact_text(exc.stdout or ""),
            "stderr": _redact_text(exc.stderr or ""),
        }
    except OSError as exc:
        return {"exit_code": "os_error", "stdout": "", "stderr": _redact_text(str(exc))}


def _parse_status(stdout: str) -> str:
    if not stdout.strip():
        return "empty"
    return "json" if _loads_json_prefix(stdout) is not None else "text"


def _preview(text: str, *, limit: int = 400) -> str:
    clean = " ".join(_redact_text(text).split())
    return clean[:limit]


def _relative_ref(root: Path, path: Path) -> str:
    try:
        ref = path.relative_to(root).as_posix()
    except ValueError:
        ref = path.name
    return "" if ref == "." else ref


def _join_ref(root_ref: str, name: str) -> str:
    return f"{root_ref}/{name}".strip("/")


def _command_shape(name: str) -> str:
    shapes = {
        "detect_project": "plugins/product-agent-os/scripts/detect_project.py <target>",
        "source_policy": "plugins/product-agent-os/scripts/validate_source_policy.py <target>",
        "first_run_dry_run": "plugins/product-agent-os/scripts/run_first_project_analysis.py <target> --dry-run",
        "methodology_audit": "plugins/product-agent-os/scripts/run_methodology_audit.py <target> --json",
        "project_graph_dry_run": "plugins/product-agent-os/scripts/scan_project_code_graph.py <target> --dry-run",
        "runtime_contract": "plugins/product-agent-os/scripts/run_codex_runtime_runner.py <target> --contract",
    }
    return shapes[name]


def _redact_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _redact_payload(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_redact_payload(item) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def _redact_text(text: str) -> str:
    replacements = {
        str(Path.home()).replace("\\", "/"): "<HOME>",
        str(Path.home()): "<HOME>",
        str(REPO_ROOT).replace("\\", "/"): "<REPO_ROOT>",
        str(REPO_ROOT): "<REPO_ROOT>",
    }
    redacted = text
    for raw, replacement in replacements.items():
        redacted = redacted.replace(raw, replacement)
    return redacted


def _loads_json_prefix(text: str) -> Any | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        payload, _index = json.JSONDecoder().raw_decode(text.lstrip())
    except json.JSONDecodeError:
        return None
    return payload


def _collection_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return len(value)
    return _int(value)


def _int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
