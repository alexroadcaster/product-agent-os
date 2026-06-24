from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path, PureWindowsPath
from typing import Any

from product_agent_os.offline_artifact_safety import (
    GENERATED_VIEW_ONLY_TEXT,
    escape_html,
    prepare_offline_payload,
    validate_offline_artifact,
)
from product_agent_os.self_learning_candidates import summarize_self_learning_candidates
from product_agent_os.self_learning_feedback import summarize_owner_feedback_ledger
from product_agent_os.self_learning_metrics import summarize_self_learning_metrics
from product_agent_os.self_learning_state import workspace_ref
from product_agent_os.stage_manifest import MANIFEST_NAME, content_digest


SELF_LEARNING_RUN_PACKET_SCHEMA_VERSION = "self_learning_run_packet_v1"
SELF_LEARNING_PROGRESS_SCHEMA_VERSION = "self_learning_progress_v1"
SELF_LEARNING_TARGET_ROOT = ".codex/product-agent-os/self-learning"
PROGRESS_JSONL_TARGET = f"{SELF_LEARNING_TARGET_ROOT}/progress.jsonl"
PROGRESS_HTML_TARGET = f"{SELF_LEARNING_TARGET_ROOT}/self-learning-progress.html"
PROGRESS_JSON_TARGET = f"{SELF_LEARNING_TARGET_ROOT}/self-learning-progress.json"
RUN_PACKET_TARGET = "self-learning-run-packet.json"
RUN_PROGRESS_TARGET = "progress.json"
RUN_PROGRESS_HTML_TARGET = "self-learning-progress.html"


PHASES = (
    "scope_check",
    "due_check",
    "evidence_collect",
    "metrics_eval",
    "feedback_eval",
    "candidate_generation",
    "reporting",
    "owner_review",
)


class SelfLearningProgressError(RuntimeError):
    pass


def build_run_id(*, now: str | datetime, workspace: str | Path, scope_packet: dict[str, Any] | None = None) -> str:
    timestamp = _parse_datetime(now).strftime("%Y%m%dT%H%M%SZ")
    scope_ref = scope_packet.get("workspace_ref") if isinstance(scope_packet, dict) else None
    if isinstance(scope_ref, dict) and isinstance(scope_ref.get("path_hash"), str):
        digest = scope_ref["path_hash"].split(":", 1)[1]
    else:
        digest = workspace_ref(workspace)["path_hash"].split(":", 1)[1]
    return f"sll-{timestamp}-{digest}"


def build_progress_events(
    *,
    run_id: str,
    now: str | datetime,
    scope_packet: dict[str, Any],
    due_packet: dict[str, Any],
    status: str,
    blockers: list[str],
) -> list[dict[str, Any]]:
    timestamp = _isoformat(_parse_datetime(now))
    scope_eligible = bool(scope_packet.get("eligible"))
    due_status = str(due_packet.get("status") or "state_invalid")
    events: list[dict[str, Any]] = []

    def add(phase: str, phase_status: str, summary: str, **extra: Any) -> None:
        events.append(
            {
                "schema_version": SELF_LEARNING_PROGRESS_SCHEMA_VERSION,
                "run_id": run_id,
                "phase": phase,
                "status": phase_status,
                "timestamp": timestamp,
                "project_scope_id": workspace_ref_value(scope_packet),
                "owner_approval_state": "manual_only",
                "summary": summary,
                "blocker_reason": "; ".join(blockers) if phase_status == "blocked" and blockers else None,
                "latest_artifact_paths": [
                    PROGRESS_JSONL_TARGET,
                    PROGRESS_HTML_TARGET,
                ],
                **extra,
            }
        )

    add(
        "scope_check",
        "completed" if scope_eligible else "blocked",
        "Product-Agent OS scope is eligible" if scope_eligible else "Product-Agent OS scope is not eligible",
        scope_status=scope_packet.get("status"),
    )
    if not scope_eligible:
        add("blocked", "blocked", "Runner stopped before evidence collection")
        return events

    add(
        "due_check",
        "completed" if due_status in {"due", "not_due", "disabled"} else "blocked",
        f"Due-check status: {due_status}",
        due_status=due_status,
        next_due_at=due_packet.get("next_due_at"),
    )
    if due_status in {"state_invalid", "disabled"}:
        reason = (
            "Runner stopped because self-learning state is disabled"
            if due_status == "disabled"
            else "Runner stopped because self-learning state is invalid"
        )
        add("blocked", "blocked", reason)
        return events

    add("evidence_collect", "completed", "Collected allowed local Product-Agent OS evidence references only")
    add("metrics_eval", "completed", "Read local self-learning metrics ledger without provider or live eval calls")
    add("feedback_eval", "completed", "Read owner feedback ledger summaries without raw session ingestion")
    add("candidate_generation", "completed", "Built review-only candidate summary without auto-apply or external actions")
    add("reporting", "completed", "Prepared staged run packet and progress artifact")
    add("owner_review", "waiting", "Owner review required before any apply, automation, schedule or target write")
    if status == "completed":
        add("completed", "completed", "Manual runner finished staged evidence generation")
    return events


def build_self_learning_run_packet(
    *,
    workspace: str | Path,
    now: str | datetime,
    mode: str,
    scope_packet: dict[str, Any],
    due_packet: dict[str, Any],
) -> dict[str, Any]:
    now_dt = _parse_datetime(now)
    run_id = build_run_id(now=now_dt, workspace=workspace, scope_packet=scope_packet)
    blockers = _blockers(scope_packet, due_packet)
    status = "blocked" if blockers else "ready_for_owner_review"
    events = build_progress_events(
        run_id=run_id,
        now=now_dt,
        scope_packet=scope_packet,
        due_packet=due_packet,
        status=status,
        blockers=blockers,
    )
    progress_status = "blocked" if blockers else "ready_for_owner_review"
    metrics_summary = summarize_self_learning_metrics(workspace)
    feedback_summary = summarize_owner_feedback_ledger(workspace)
    candidate_summary = summarize_self_learning_candidates(
        workspace,
        metrics_summary=metrics_summary,
        feedback_summary=feedback_summary,
    )
    return {
        "schema_version": SELF_LEARNING_RUN_PACKET_SCHEMA_VERSION,
        "run_id": run_id,
        "generated_at": _isoformat(now_dt),
        "mode": mode,
        "status": status,
        "write_policy": "staged_only" if mode == "stage" else "read_only",
        "workspace_ref": scope_packet.get("workspace_ref") if isinstance(scope_packet.get("workspace_ref"), dict) else workspace_ref(workspace),
        "product_agent_os_scope": scope_packet,
        "due_check": due_packet,
        "analysis_executed": False,
        "state_written": False,
        "provider_calls": "not_performed",
        "live_eval_services": "not_performed",
        "target_workspace_writes": "not_performed" if mode == "dry_run" else "not_performed_stage_root_only",
        "auto_apply": {
            "status": "not_enabled",
            "candidate_count": 0,
            "apply_controls_present": False,
            "approval_required_before_apply": True,
        },
        "evidence_sources": [
            {
                "id": "scope_detector",
                "kind": "local_product_agent_os_scope_packet",
                "status": scope_packet.get("status"),
                "raw_private_paths": "excluded",
            },
            {
                "id": "due_check",
                "kind": "self_learning_due_check_packet",
                "status": due_packet.get("status"),
                "raw_private_paths": "excluded",
            },
        ],
        "metrics_summary": metrics_summary,
        "feedback_summary": feedback_summary,
        "candidate_summary": candidate_summary,
        "owner_questions": [
            "Review the staged packet before approving any target write, candidate update or automation.",
        ],
        "unsupported_claims": [
            "generated HTML proves work complete",
            "user satisfaction is known without owner feedback",
            "automation or auto-apply is enabled",
            "provider or live eval calls were performed",
        ],
        "blockers": blockers,
        "progress": {
            "schema_version": SELF_LEARNING_PROGRESS_SCHEMA_VERSION,
            "run_id": run_id,
            "status": progress_status,
            "events": events,
        },
        "rendered_artifacts": {
            "mode": mode,
            "targets": _artifact_targets(run_id),
            "validation": {"ok": True, "errors": []},
        },
    }


def render_self_learning_progress_html(packet: dict[str, Any]) -> dict[str, Any]:
    prepared = prepare_offline_payload(packet)
    safe_packet = prepared["payload"]
    html_text = _render_html(safe_packet, prepared["json_for_html"])
    validation = validate_offline_artifact(
        html_text=html_text,
        embedded_json=prepared["json"],
        payload=safe_packet,
    )
    return {
        "html": html_text,
        "json": prepared["json"],
        "validation": validation,
        "redaction_summary": prepared["redaction_summary"],
    }


def stage_self_learning_run(
    *,
    workspace: str | Path,
    stage_root: str | Path,
    packet: dict[str, Any],
) -> dict[str, Any]:
    workspace_path = Path(workspace).resolve()
    stage_path = Path(stage_root).resolve()
    if stage_path == workspace_path or stage_path.is_relative_to(workspace_path):
        raise SelfLearningProgressError("stage output directory must be outside workspace")
    rendered = render_self_learning_progress_html(packet)
    validation_errors = list(rendered["validation"]["errors"])
    run_id = str(packet.get("run_id") or "unknown-run")
    progress_json = json.dumps(packet["progress"], ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    run_packet_json = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    event_lines = "".join(
        json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
        for event in packet.get("progress", {}).get("events", [])
        if isinstance(event, dict)
    )
    contents = {
        PROGRESS_JSONL_TARGET: event_lines,
        PROGRESS_JSON_TARGET: rendered["json"] + "\n",
        PROGRESS_HTML_TARGET: rendered["html"],
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PROGRESS_TARGET}": progress_json,
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PACKET_TARGET}": run_packet_json,
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PROGRESS_HTML_TARGET}": rendered["html"],
    }
    files: list[dict[str, Any]] = []
    for target, content in contents.items():
        _validate_relative_target(target)
        destination = stage_path / Path(target)
        _write_inside_root(stage_path, destination, content)
        files.append(
            {
                "key": _artifact_key(target),
                "category": "self-learning-loop",
                "target_path": target,
                "action": "create",
                "write_policy": "staged_only",
                "staged_path": str(destination),
                "digest": content_digest(content),
                "managed_section": "",
            }
        )
    result = {
        "mode": "stage",
        "root": str(stage_path),
        "targets": _artifact_targets(run_id),
        "files": files,
        "validation": {
            "ok": not validation_errors,
            "checks": rendered["validation"]["checks"],
            "errors": validation_errors,
        },
    }
    manifest = _redacted_stage_manifest(
        workspace=workspace_path,
        stage_root=stage_path,
        packet=packet,
        files=files,
        validation=result["validation"],
    )
    manifest_path = stage_path / MANIFEST_NAME
    _write_inside_root(stage_path, manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    result["manifest_path"] = str(manifest_path)
    for item in result["files"]:
        if isinstance(item, dict):
            item["staged_path"] = item.get("target_path", "")
    return result


def _redacted_stage_manifest(
    *,
    workspace: Path,
    stage_root: Path,
    packet: dict[str, Any],
    files: list[dict[str, Any]],
    validation: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": "self_learning_stage_manifest_v1",
        "renderer": "product-agent-os",
        "renderer_version": "0.1.0",
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "workspace_ref": packet.get("workspace_ref") if isinstance(packet.get("workspace_ref"), dict) else workspace_ref(workspace),
        "raw_workspace_path_included": False,
        "stage_root_ref": {
            "path_hash": workspace_ref(stage_root).get("path_hash"),
            "raw_path_included": False,
        },
        "run_id": packet.get("run_id"),
        "write_policy": "staged_only",
        "validation": validation,
        "files": [
            {
                key: value
                for key, value in item.items()
                if key in {"key", "category", "target_path", "action", "write_policy", "staged_path", "digest"}
            }
            for item in files
        ],
    }


def dry_run_artifact_plan(packet: dict[str, Any]) -> dict[str, Any]:
    rendered = render_self_learning_progress_html(packet)
    run_id = str(packet.get("run_id") or "unknown-run")
    return {
        "mode": "dry_run",
        "root": ".product-agent-os/self-learning",
        "targets": _artifact_targets(run_id),
        "files": [
            {"target_path": PROGRESS_JSONL_TARGET, "action": "plan_create", "write_policy": "staged_only"},
            {"target_path": PROGRESS_HTML_TARGET, "action": "plan_create", "write_policy": "staged_only"},
            {"target_path": PROGRESS_JSON_TARGET, "action": "plan_create", "write_policy": "staged_only"},
            {
                "target_path": f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PROGRESS_TARGET}",
                "action": "plan_create",
                "write_policy": "staged_only",
            },
        ],
        "validation": rendered["validation"],
    }


def workspace_ref_value(scope_packet: dict[str, Any]) -> str:
    ref = scope_packet.get("workspace_ref")
    if isinstance(ref, dict):
        value = ref.get("path_hash")
        if isinstance(value, str):
            return value
    return "sha256:unknown"


def _blockers(scope_packet: dict[str, Any], due_packet: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if not scope_packet.get("eligible"):
        blockers.append("Product-Agent OS scope is not eligible")
    if due_packet.get("status") == "state_invalid":
        blockers.append("self-learning state is invalid")
    if due_packet.get("status") == "disabled":
        blockers.append("self-learning loop is disabled")
    return blockers


def _artifact_targets(run_id: str) -> list[str]:
    return [
        PROGRESS_JSONL_TARGET,
        PROGRESS_JSON_TARGET,
        PROGRESS_HTML_TARGET,
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PROGRESS_TARGET}",
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PACKET_TARGET}",
        f"{SELF_LEARNING_TARGET_ROOT}/runs/{run_id}/{RUN_PROGRESS_HTML_TARGET}",
    ]


def _render_html(packet: dict[str, Any], embedded_json: str) -> str:
    progress = packet.get("progress") if isinstance(packet.get("progress"), dict) else {}
    events = progress.get("events") if isinstance(progress.get("events"), list) else []
    rows = "\n".join(_event_row(event) for event in events if isinstance(event, dict))
    if not rows:
        rows = "<tr><td colspan=\"4\">No progress events are available.</td></tr>"
    summary_rows = "\n".join(
        f"<tr><th scope=\"row\">{escape_html(label)}</th><td>{_value(value)}</td></tr>"
        for label, value in [
            ("Run ID", packet.get("run_id")),
            ("Status", packet.get("status")),
            ("Mode", packet.get("mode")),
            ("Due status", _nested(packet, "due_check", "status")),
            ("Cadence", _nested(packet, "due_check", "cadence_level")),
            ("Scope status", _nested(packet, "product_agent_os_scope", "status")),
            ("Auto-apply", _nested(packet, "auto_apply", "status")),
            ("Write policy", packet.get("write_policy")),
            ("Generated at", packet.get("generated_at")),
        ]
    )
    blockers = _list_html(packet.get("blockers"))
    unsupported = _list_html(packet.get("unsupported_claims"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Self-Learning Loop Progress</title>
  <style>
    :root {{ color-scheme: light; --ink: #1f2933; --muted: #5f6b7a; --line: #d8dee8; --panel: #f7f9fc; --accent: #136f63; }}
    body {{ margin: 0; font-family: Arial, sans-serif; color: var(--ink); background: #ffffff; line-height: 1.45; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ font-size: 30px; margin: 0 0 8px; letter-spacing: 0; }}
    h2 {{ font-size: 18px; margin: 28px 0 12px; letter-spacing: 0; }}
    .policy {{ border-left: 4px solid var(--accent); background: var(--panel); padding: 12px 14px; color: var(--muted); }}
    table {{ width: 100%; border-collapse: collapse; border: 1px solid var(--line); }}
    th, td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ background: var(--panel); width: 220px; }}
    code {{ white-space: pre-wrap; overflow-wrap: anywhere; }}
    .status {{ display: inline-block; padding: 2px 8px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); }}
    ul {{ margin-top: 0; }}
  </style>
</head>
<body>
  <main>
    <h1>Self-Learning Loop Progress</h1>
    <p class="policy">{escape_html(GENERATED_VIEW_ONLY_TEXT)}</p>
    <h2>Run Summary</h2>
    <table><tbody>{summary_rows}</tbody></table>
    <h2>Phase Progress</h2>
    <table>
      <thead><tr><th scope="col">Phase</th><th scope="col">Status</th><th scope="col">Summary</th><th scope="col">Blocker</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <h2>Blockers</h2>
    {blockers}
    <h2>Unsupported Claims</h2>
    {unsupported}
    <script id="self-learning-progress-payload" type="application/json">{embedded_json}</script>
  </main>
</body>
</html>"""


def _event_row(event: dict[str, Any]) -> str:
    return (
        "<tr>"
        f"<td><code>{escape_html(event.get('phase'))}</code></td>"
        f"<td><span class=\"status\">{escape_html(event.get('status'))}</span></td>"
        f"<td>{escape_html(event.get('summary'))}</td>"
        f"<td>{escape_html(event.get('blocker_reason') or '')}</td>"
        "</tr>"
    )


def _list_html(value: Any) -> str:
    if not isinstance(value, list) or not value:
        return "<p>None.</p>"
    return "<ul>" + "".join(f"<li>{escape_html(item)}</li>" for item in value) + "</ul>"


def _value(value: Any) -> str:
    if value in (None, ""):
        return "<span>not available</span>"
    if isinstance(value, (dict, list)):
        return f"<code>{escape_html(json.dumps(value, ensure_ascii=False, sort_keys=True))}</code>"
    return escape_html(value)


def _nested(packet: dict[str, Any], section: str, key: str) -> Any:
    value = packet.get(section)
    if isinstance(value, dict):
        return value.get(key)
    return None


def _artifact_key(target: str) -> str:
    return target.replace("/", "-").replace(".", "-").strip("-")


def _write_inside_root(root: Path, destination: Path, content: str) -> None:
    resolved_root = root.resolve()
    resolved_destination = destination.resolve()
    if not resolved_destination.is_relative_to(resolved_root):
        raise SelfLearningProgressError(f"staged path escapes output directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def _validate_relative_target(target: str) -> None:
    if not target:
        raise SelfLearningProgressError("empty target path")
    path = Path(target)
    windows_path = PureWindowsPath(target)
    if (
        path.is_absolute()
        or windows_path.is_absolute()
        or bool(path.drive)
        or bool(windows_path.drive)
        or ".." in path.parts
        or ".." in windows_path.parts
    ):
        raise SelfLearningProgressError(f"invalid target path: {target}")


def _parse_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def _isoformat(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
