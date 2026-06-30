from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path, PureWindowsPath


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.self_learning_evals import (  # noqa: E402
    build_halo_recommendation_packet,
    build_promptfoo_export_packet,
    build_self_learning_eval_cases,
    build_self_learning_failure_taxonomy,
    validate_self_learning_eval_cases,
    validate_self_learning_failure_taxonomy,
)
from product_agent_os.self_learning_state import workspace_ref  # noqa: E402
from product_agent_os.stage_manifest import MANIFEST_NAME, content_digest  # noqa: E402


PROMPTFOO_CONFIG_TARGET = ".codex/product-agent-os/self-learning/evals/promptfooconfig.yaml"
PROMPTFOO_EXPORT_TARGET = ".codex/product-agent-os/self-learning/evals/promptfoo-export.json"
HALO_PACKET_TARGET = ".codex/product-agent-os/self-learning/evals/halo-recommendation-packet.json"
EVAL_CASES_TARGET = ".codex/product-agent-os/self-learning/evals/eval-cases.json"
FAILURE_TAXONOMY_TARGET = ".codex/product-agent-os/self-learning/evals/failure-taxonomy.json"


class PromptfooExportError(RuntimeError):
    pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export Self-Learning Loop eval cases to Promptfoo-compatible staged artifacts."
    )
    parser.add_argument("workspace", nargs="?", default=".", help="Workspace path used only for hash-only manifest refs.")
    parser.add_argument("--dry-run", action="store_true", help="Print export packets without writing files.")
    parser.add_argument("--stage", help="Stage Promptfoo/HALO/eval artifacts under this output directory.")
    parser.add_argument("--now", help="Deterministic generated_at timestamp for tests.")
    args = parser.parse_args(argv)

    if bool(args.dry_run) == bool(args.stage):
        _print_payload(
            {
                "schema_version": "self_learning_promptfoo_export_v1",
                "status": "error",
                "error": "choose exactly one of --dry-run or --stage",
                "provider_calls": "not_performed",
            }
        )
        return 2

    eval_cases = build_self_learning_eval_cases()
    taxonomy = build_self_learning_failure_taxonomy()
    errors = validate_self_learning_eval_cases(eval_cases) + validate_self_learning_failure_taxonomy(taxonomy)
    packet = build_promptfoo_export_packet(eval_cases=eval_cases, generated_at=args.now)
    halo_packet = build_halo_recommendation_packet(eval_cases=eval_cases, taxonomy=taxonomy, generated_at=args.now)
    result = {
        "schema_version": "self_learning_promptfoo_halo_export_v1",
        "status": "blocked" if errors else "ready_for_owner_review",
        "mode": "stage" if args.stage else "dry_run",
        "provider_calls": "not_performed",
        "promptfoo_export": packet,
        "halo_recommendation_packet": halo_packet,
        "eval_cases": eval_cases,
        "failure_taxonomy": taxonomy,
        "validation_errors": errors,
        "approval_required_before_promptfoo_run": True,
        "auto_apply": "disabled",
    }
    if args.stage and not errors:
        try:
            result["rendered_artifacts"] = _stage_export(
                workspace=Path(args.workspace),
                stage_root=Path(args.stage),
                promptfoo_packet=packet,
                halo_packet=halo_packet,
                eval_cases=eval_cases,
                taxonomy=taxonomy,
            )
        except PromptfooExportError as exc:
            result["status"] = "blocked"
            result.setdefault("validation_errors", []).append(str(exc))
            _print_payload(result)
            return 2

    _print_payload(result)
    return 0 if result["status"] != "blocked" else 2


def _stage_export(
    *,
    workspace: Path,
    stage_root: Path,
    promptfoo_packet: dict,
    halo_packet: dict,
    eval_cases: dict,
    taxonomy: dict,
) -> dict:
    workspace_path = workspace.resolve()
    stage_path = stage_root.resolve()
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise PromptfooExportError("stage output directory must be outside workspace")
    contents = {
        PROMPTFOO_CONFIG_TARGET: promptfoo_packet["promptfoo_config_yaml"] + "\n",
        PROMPTFOO_EXPORT_TARGET: json.dumps(promptfoo_packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        HALO_PACKET_TARGET: json.dumps(halo_packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        EVAL_CASES_TARGET: json.dumps(eval_cases, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        FAILURE_TAXONOMY_TARGET: json.dumps(taxonomy, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    }
    files: list[dict] = []
    for target, content in contents.items():
        _validate_relative_target(target)
        destination = stage_path / Path(target)
        _write_inside_root(stage_path, destination, content)
        files.append(
            {
                "key": target.replace("/", "-").replace(".", "-").strip("-"),
                "category": "self-learning-loop",
                "target_path": target,
                "action": "create",
                "write_policy": "staged_only",
                "staged_path": target,
                "digest": content_digest(content),
                "managed_section": "",
            }
        )
    validation = {"ok": True, "errors": []}
    manifest = {
        "schema_version": "self_learning_promptfoo_halo_stage_manifest_v1",
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "workspace_ref": workspace_ref(workspace_path),
        "raw_workspace_path_included": False,
        "stage_root_ref": {"path_hash": workspace_ref(stage_path).get("path_hash"), "raw_path_included": False},
        "write_policy": "staged_only",
        "provider_calls": "not_performed",
        "approval_required_before_promptfoo_run": True,
        "validation": validation,
        "files": files,
    }
    _write_inside_root(stage_path, stage_path / MANIFEST_NAME, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return {
        "mode": "stage",
        "root": "[STAGE_ROOT]",
        "targets": list(contents),
        "files": files,
        "manifest_path": f"[STAGE_ROOT]/{MANIFEST_NAME}",
        "validation": validation,
    }


def _write_inside_root(root: Path, destination: Path, content: str) -> None:
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise PromptfooExportError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_relative_target(target: str) -> None:
    path = Path(target)
    windows_path = PureWindowsPath(target)
    if (
        not target
        or path.is_absolute()
        or windows_path.is_absolute()
        or bool(path.drive)
        or bool(windows_path.drive)
        or ".." in path.parts
        or ".." in windows_path.parts
    ):
        raise PromptfooExportError(f"invalid target path: {target}")


def _print_payload(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    raise SystemExit(main())
