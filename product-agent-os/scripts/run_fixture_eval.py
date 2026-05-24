from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


sys.path.insert(0, str(Path(__file__).resolve().parent))

from product_agent_os.discovery import analyze_workspace  # noqa: E402
from product_agent_os.automation_policy import validate_automation_candidate  # noqa: E402
from product_agent_os.infrastructure import InfrastructureError, render_infrastructure_plan, stage_infrastructure  # noqa: E402
from product_agent_os.merge_infrastructure import (  # noqa: E402
    ROLLBACK_MANIFEST_NAME,
    MergeInfrastructureError,
    apply_merge_plan,
    build_merge_plan,
)
from product_agent_os.source_policy import validate_source_policy  # noqa: E402
from product_agent_os.stage_manifest import MANIFEST_NAME, content_digest, workspace_audit_digest  # noqa: E402
from codex_runtime_runner.cli import run_contract  # noqa: E402
from codex_runtime_runner.guards import validate_automation_boundary, validate_codex_handoff  # noqa: E402
from codex_runtime_runner.redaction import redact_text, validate_redaction  # noqa: E402


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = PLUGIN_ROOT / "assets" / "fixtures"


def _failed_result(fixture: str, reason: str) -> dict[str, Any]:
    return {
        "fixture": fixture,
        "ok": False,
        "profile": "",
        "risks": [reason],
        "renderer_status": "",
        "merge_status": "",
        "source_policy_status": "",
        "automation_status": "",
        "rollback_status": "",
        "failure_log_regression_status": "",
        "codex_runtime_runner_status": "",
        "codex_runtime_runner_checks": {},
        "renderer_file_count": 0,
        "renderer_actions": {},
        "expected_checks": {},
        "evidence": {},
    }


def evaluate_fixture(path: Path) -> dict[str, Any]:
    try:
        audit = analyze_workspace(path)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        return _failed_result(path.name, str(exc))
    except Exception as exc:
        return _failed_result(path.name, f"discovery failed: {type(exc).__name__}: {exc}")

    profile = audit.get("complexity_profile", {})
    profile_name = profile.get("name", "") if isinstance(profile, dict) else ""
    risks = audit.get("risks", [])
    try:
        rendered = render_infrastructure_plan(path)
        renderer_status = str(rendered["infrastructure_plan"]["status"])
        merge_status = renderer_status
        renderer_files = rendered["rendered_artifacts"]["files"]
        renderer_validation = rendered["rendered_artifacts"]["validation"]
        renderer_actions = _renderer_actions(renderer_files)
        expected_checks = _expected_checks(path.name, rendered, renderer_actions)
        source_policy_status = _source_policy_status(path)
        automation_status = _automation_status(path)
        behavior = _track_four_behavior(path)
        rollback_status = behavior["rollback_status"] or _rollback_status(path)
        failure_log_status, failure_log_checks = _failure_log_status(path)
        codex_runtime_runner_status, codex_runtime_runner_checks = _codex_runtime_runner_eval(path)
        expected_checks.update(failure_log_checks)
        expected_checks.update(codex_runtime_runner_checks)
        expected_checks.update(
            _track_four_expected_checks(
                path.name,
                source_policy_status,
                automation_status,
                rollback_status,
                failure_log_status,
            )
        )
        expected_checks.update(behavior["expected_checks"])
        merge_status = behavior["merge_status"] or renderer_status
        evidence = _evidence(path, source_policy_status, automation_status, behavior)
        renderer_ok = (
            bool(renderer_validation.get("ok"))
            and renderer_status in {"needs_approval", "blocked"}
            and all(expected_checks.values())
        )
    except InfrastructureError as exc:
        renderer_status = ""
        merge_status = ""
        source_policy_status = ""
        automation_status = ""
        rollback_status = ""
        failure_log_status = ""
        codex_runtime_runner_status = ""
        codex_runtime_runner_checks = {}
        renderer_files = []
        renderer_actions = {}
        expected_checks = {}
        evidence = {}
        renderer_ok = False
        risks = risks if isinstance(risks, list) else ["invalid discovery risks"]
        risks = [*risks, f"renderer failed: {exc}"]
    except Exception as exc:
        renderer_status = ""
        merge_status = ""
        source_policy_status = ""
        automation_status = ""
        rollback_status = ""
        failure_log_status = ""
        renderer_files = []
        renderer_actions = {}
        expected_checks = {}
        evidence = {}
        renderer_ok = False
        risks = risks if isinstance(risks, list) else ["invalid discovery risks"]
        risks = [*risks, f"renderer failed: {type(exc).__name__}: {exc}"]

    ok = bool(audit.get("workspace")) and bool(profile_name) and isinstance(risks, list) and renderer_ok
    return {
        "fixture": path.name,
        "ok": ok,
        "profile": profile_name,
        "risks": risks if isinstance(risks, list) else ["invalid discovery risks"],
        "renderer_status": renderer_status,
        "merge_status": merge_status,
        "source_policy_status": source_policy_status,
        "automation_status": automation_status,
        "rollback_status": rollback_status,
        "failure_log_regression_status": failure_log_status,
        "codex_runtime_runner_status": codex_runtime_runner_status,
        "codex_runtime_runner_checks": codex_runtime_runner_checks,
        "renderer_file_count": len(renderer_files),
        "renderer_actions": renderer_actions,
        "expected_checks": expected_checks,
        "evidence": evidence,
    }


def _renderer_actions(files: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(item.get("target_path")): str(item.get("action"))
        for item in files
        if isinstance(item, dict) and item.get("target_path")
    }


def _expected_checks(
    fixture: str,
    rendered: dict[str, Any],
    actions: dict[str, str],
) -> dict[str, bool]:
    plan = rendered.get("infrastructure_plan", {})
    warnings = " ".join(plan.get("warnings", [])) if isinstance(plan, dict) else ""
    blocked = " ".join(plan.get("blocked", [])) if isinstance(plan, dict) else ""
    payload = json.dumps(rendered, sort_keys=True).lower()
    checks: dict[str, bool] = {}
    if fixture in {"empty-repo", "node-app", "python-app"}:
        checks["agents_md_create"] = actions.get("AGENTS.md") == "create"
        checks["config_create"] = actions.get(".codex/config.toml") == "create"
    if fixture in {"existing-codex-config", "unsafe-write-request"}:
        checks["config_leave_unchanged"] = actions.get(".codex/config.toml") == "leave_unchanged"
        checks["agents_md_leave_unchanged"] = actions.get("AGENTS.md") == "leave_unchanged"
    if fixture == "duplicate-managed-section":
        checks["duplicate_markers_blocked"] = (
            actions.get("AGENTS.md") == "blocked" and "duplicate managed section" in blocked
        )
    if fixture == "monorepo":
        checks["worktree_ownership_warning"] = "worktree ownership" in warnings
    if fixture == "docs-source-conflict":
        checks["source_registry_warning"] = "source registry" in warnings
    if fixture == "failed-verification":
        checks["failed_verification_warning"] = (
            "failed verification evidence" in warnings and "checks passed" not in payload
        )
    return checks


def _track_four_expected_checks(
    fixture: str,
    source_policy_status: str,
    automation_status: str,
    rollback_status: str,
    failure_log_status: str,
) -> dict[str, bool]:
    checks: dict[str, bool] = {}
    if fixture == "source-policy-conflict":
        checks["source_policy_status_needs_review"] = source_policy_status == "needs_review"
    if fixture == "automation-candidate-valid":
        checks["automation_status_ready_for_manual_approval"] = (
            automation_status == "ready_for_manual_approval"
        )
    if fixture == "automation-candidate-invalid":
        checks["automation_status_blocked"] = automation_status == "blocked"
    if fixture == "failure-log-regression":
        checks["failure_log_regression_status_ready"] = failure_log_status == "ready"
    if fixture == "rollback-required":
        checks["rollback_status_required"] = rollback_status == "required"
    return checks


def _source_policy_status(path: Path) -> str:
    report = validate_source_policy(path)
    return str(report["status"])


def _automation_status(path: Path) -> str:
    candidates = sorted(path.rglob("automation-candidate.md"))
    if not candidates:
        return "not_applicable"
    report = validate_automation_candidate(candidates[0])
    return str(report["status"])


def _rollback_status(path: Path) -> str:
    runlog = path / "RUNLOG.md"
    if not runlog.exists():
        return "not_exercised"
    text = runlog.read_text(encoding="utf-8")
    if "rollback_manifest_visible" in text or "rollback-required" in text:
        return "required"
    return "not_exercised"


def _track_four_behavior(path: Path) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    commands: list[str] = []
    reports: list[dict[str, str]] = []
    merge_status = ""
    rollback_status = ""

    if path.name == "stale-merge-plan":
        merge_status, check = _exercise_stale_merge_plan(path)
        checks["stale_digest_blocked"] = check
        commands.extend(["stage_infrastructure", "build_merge_plan"])
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "path-traversal-stage":
        merge_status, check = _exercise_path_traversal_stage()
        checks["path_traversal_blocked"] = check
        commands.append("build_merge_plan")
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "symlink-escape":
        merge_status, check = _exercise_symlink_escape()
        checks["symlink_escape_blocked"] = check
        commands.append("build_merge_plan")
        reports.append({"name": "merge_policy", "status": merge_status})
    elif path.name == "hook-activation-unapproved":
        merge_status, check = _exercise_unapproved_hook_activation()
        checks["hooks_unapproved_companion_only"] = check
        commands.extend(["build_merge_plan", "apply_merge_plan"])
        reports.append({"name": "hook_activation", "status": merge_status})
    elif path.name == "hook-activation-approved":
        merge_status, rollback_status, hook_check, rollback_check = _exercise_approved_hook_activation()
        checks["hooks_approved_apply"] = hook_check
        checks["rollback_manifest_visible"] = rollback_check
        commands.extend(["build_merge_plan", "apply_merge_plan"])
        reports.append({"name": "hook_activation", "status": merge_status})

    return {
        "expected_checks": checks,
        "merge_status": merge_status,
        "rollback_status": rollback_status,
        "commands": commands,
        "reports": reports,
    }


def _exercise_stale_merge_plan(path: Path) -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        shutil.copytree(path, workspace)
        stage_infrastructure(workspace, stage_root)
        (workspace / "AGENTS.md").write_text("# Added after staging\n", encoding="utf-8")
        plan = build_merge_plan(workspace, stage_root)
    blocked = " ".join(plan.get("blocked", []))
    return str(plan.get("status", "")), plan.get("status") == "blocked" and "workspace audit digest" in blocked


def _exercise_path_traversal_stage() -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, "AGENTS.md", "content\n")
        _write_stage_manifest(workspace, stage_root, [{"target_path": "../AGENTS.md", "staged_path": "AGENTS.md"}])
        try:
            build_merge_plan(workspace, stage_root)
        except MergeInfrastructureError as exc:
            return "blocked", "escapes" in str(exc)
    return "needs_approval", False


def _exercise_symlink_escape() -> tuple[str, bool]:
    if not hasattr(os, "symlink"):
        return "skipped_unsupported", True
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        outside = Path(tmp) / "outside.md"
        workspace.mkdir()
        stage_root.mkdir()
        outside.write_text("outside\n", encoding="utf-8")
        try:
            os.symlink(outside, workspace / "AGENTS.md")
        except (OSError, NotImplementedError):
            return "skipped_unsupported", True
        _write_stage_file(stage_root, "AGENTS.md", _managed_doc("project-rules", "Generated rules."))
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": "AGENTS.md", "staged_path": "AGENTS.md", "managed_section": "project-rules"}],
        )
        plan = build_merge_plan(workspace, stage_root)
    blocked = " ".join(plan.get("blocked", []))
    return str(plan.get("status", "")), plan.get("status") == "blocked" and "symlink" in blocked


def _exercise_unapproved_hook_activation() -> tuple[str, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": ".codex/hooks/hooks.json", "staged_path": ".codex/hooks/hooks.json"}],
        )
        plan = build_merge_plan(workspace, stage_root)
        approval = _write_approval(stage_root, plan["id"], [], [])
        result = apply_merge_plan(workspace, stage_root, approval)
        hooks_path = workspace / ".codex" / "hooks" / "hooks.json"
    decision = plan["decisions"][0]
    return (
        str(result.get("status", "")),
        decision.get("action") == "companion_only" and not hooks_path.exists(),
    )


def _exercise_approved_hook_activation() -> tuple[str, str, bool, bool]:
    with tempfile.TemporaryDirectory(prefix="product-agent-os-fixture-") as tmp:
        workspace = Path(tmp) / "workspace"
        stage_root = Path(tmp) / "stage"
        workspace.mkdir()
        stage_root.mkdir()
        _write_stage_file(stage_root, ".codex/hooks/hooks.json", "{}\n")
        _write_stage_manifest(
            workspace,
            stage_root,
            [{"target_path": ".codex/hooks/hooks.json", "staged_path": ".codex/hooks/hooks.json"}],
        )
        plan = build_merge_plan(workspace, stage_root)
        approval = _write_approval(
            stage_root,
            plan["id"],
            [".codex/hooks/hooks.json"],
            ["create_file"],
            enable_hooks=True,
        )
        result = apply_merge_plan(workspace, stage_root, approval)
        hooks_path = workspace / ".codex" / "hooks" / "hooks.json"
        rollback_path = stage_root / ROLLBACK_MANIFEST_NAME
        hook_check = result.get("status") == "applied" and hooks_path.exists()
        rollback_check = rollback_path.exists() and rollback_path.is_file()
    return str(result.get("status", "")), "available" if rollback_check else "missing", hook_check, rollback_check


def _write_stage_file(stage_root: Path, relative_path: str, content: str) -> None:
    path = stage_root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_stage_manifest(workspace: Path, stage_root: Path, files: list[dict[str, str]]) -> None:
    manifest_files: list[dict[str, str]] = []
    target_paths: list[str] = []
    for item in files:
        target_path = item["target_path"]
        staged_path = item["staged_path"]
        target_paths.append(target_path)
        staged = stage_root / staged_path
        manifest_files.append(
            {
                "target_path": target_path,
                "staged_path": staged_path,
                "action": item.get("action", "create"),
                "write_policy": item.get("write_policy", "staged_only"),
                "digest": content_digest(staged.read_bytes()),
                "managed_section": item.get("managed_section", ""),
            }
        )
    manifest = {
        "schema_version": 1,
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "workspace": str(workspace.resolve()),
        "generated_at": "2026-05-14T00:00:00+00:00",
        "workspace_audit_digest": workspace_audit_digest(workspace, target_paths),
        "infrastructure_plan_digest": content_digest("fixture\n"),
        "validation": {"ok": True, "checks": [], "errors": {}},
        "files": manifest_files,
    }
    (stage_root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")


def _write_approval(
    stage_root: Path,
    plan_id: str,
    approved_targets: list[str],
    approved_actions: list[str],
    *,
    enable_hooks: bool = False,
) -> Path:
    path = stage_root / "approval.json"
    payload = {
        "approval": {
            "schema_version": 1,
            "merge_plan_id": plan_id,
            "approved_by": "fixture-eval",
            "approved_at": "2026-05-14T00:00:00+00:00",
            "approved_targets": approved_targets,
            "approved_actions": approved_actions,
            "accepted_risks": ["synthetic fixture workspace write"],
            "denied_targets": [],
            "notes": "fixture eval approval",
            "enable_hooks": enable_hooks,
            "approved_hook_events": ["SessionStart"] if enable_hooks else [],
            "blocking_hooks": ["PreToolUse"] if enable_hooks else [],
            "hook_rollback": "remove hooks.json when rollback digest matches" if enable_hooks else "",
        }
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _managed_doc(section_id: str, body: str) -> str:
    return (
        "# Generated\n\n"
        f"<!-- product-agent-os:start {section_id} -->\n"
        f"{body}\n"
        f"<!-- product-agent-os:end {section_id} -->\n"
    )


def _failure_log_status(path: Path) -> tuple[str, dict[str, bool]]:
    runlog = path / "RUNLOG.md"
    if not runlog.exists():
        return "not_applicable", {}
    text = runlog.read_text(encoding="utf-8")
    if "expected_regression_fixture:" not in text and "expected_check:" not in text:
        return "not_applicable", {}
    checks = {
        "failure_log_regression_visible": (
            "expected_regression_fixture:" in text and "expected_check:" in text
        )
    }
    return "ready" if all(checks.values()) else "needs_review", checks


def _codex_runtime_runner_eval(path: Path) -> tuple[str, dict[str, bool]]:
    if not path.name.startswith("codex-runner-"):
        return "not_applicable", {}

    checks: dict[str, bool] = {"contract_mode_offline": True}
    if path.name == "codex-runner-ready":
        result = run_contract(path)
        checks["route_matches_lifecycle_state"] = (
            result["lifecycle_state"] == "quality_gate"
            and result["route_packet"]["recommended_skill"] == "risk-reviewer"
        )
        return str(result["status"]), checks

    if path.name == "codex-runner-missing-context":
        result = run_contract(path)
        checks["missing_context_detected"] = result["status"] == "needs_context"
        return str(result["status"]), checks

    if path.name == "codex-runner-approval-required":
        result = run_contract(path, allow_subagents=True)
        checks["approval_required_for_writes"] = result["status"] == "needs_approval"
        return str(result["status"]), checks

    if path.name == "codex-runner-handoff-incomplete":
        errors = validate_codex_handoff(
            {
                "lifecycle_state": "quality_gate",
                "constraints": [],
                "verification_evidence": [],
            }
        )
        checks["handoff_incomplete_blocked"] = (
            "constraints:empty" in errors and "verification_evidence:empty" in errors
        )
        return "blocked", checks

    if path.name == "codex-runner-automation-blocked":
        errors = validate_automation_boundary((path / "RUNLOG.md").read_text(encoding="utf-8"))
        checks["active_automation_blocked"] = "automation:active_request_blocked" in errors
        return "blocked", checks

    if path.name == "codex-runner-secret-redaction":
        redacted, _report = redact_text("TOKEN=fixture-secret\nC:\\Users\\person\\workspace")
        checks["secret_redaction_enforced"] = validate_redaction(redacted) == []
        return "blocked", checks

    return "not_applicable", {}


def _evidence(
    path: Path,
    source_policy_status: str,
    automation_status: str,
    behavior: dict[str, Any],
) -> dict[str, Any]:
    return {
        "files_inspected": sorted(str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()),
        "commands": [
            "render_infrastructure_plan",
            "validate_source_policy",
            "validate_automation_candidate",
            *behavior["commands"],
        ],
        "reports": [
            {"name": "source_policy", "status": source_policy_status},
            {"name": "automation_policy", "status": automation_status},
            *behavior["reports"],
        ],
    }


def evaluate_all(fixtures_root: Path = FIXTURES) -> list[dict[str, Any]]:
    if not fixtures_root.exists():
        return [_failed_result(fixtures_root.name, f"fixture directory does not exist: {fixtures_root}")]
    if not fixtures_root.is_dir():
        return [_failed_result(fixtures_root.name, f"fixture path is not a directory: {fixtures_root}")]

    return [
        evaluate_fixture(path)
        for path in sorted(fixtures_root.iterdir(), key=lambda item: item.name)
        if path.is_dir()
    ]


def main() -> int:
    results = evaluate_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if results and all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
