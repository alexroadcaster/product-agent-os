"""Read-only agent and skill metrics-loop foundation for Product-Agent OS."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import redact_payload


METRICS_PACKET_LIMITS = {
    "targets": 20,
    "evidence_records": 80,
    "questions": 8,
    "update_candidates": 12,
    "embedded_json_bytes": 12_000,
}

_SOURCE_OF_TRUTH = [
    "control_plane",
    "run_record",
    "trace_packet",
    "eval_packet",
    "accepted_gap",
]
_GENERATED_REVIEW_ONLY = [
    "status_dashboard_html",
    "metrics_report_html",
    "generated_report_html",
]
_REJECTED_SOURCES = [
    "memory",
    "raw_chat_log",
    "unsupported_community_claim",
]
_CONTROL_PLANE_FILES = {"AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"}
_EVAL_HINTS = ("fixture eval", "transcript eval", "eval summary", "eval-run-report")
_DATE_PATTERN = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")
_KEY_VALUE_PATTERN = re.compile(r"^\s*([A-Za-z0-9_-]+)\s*[:=]\s*\"?([^\"\r\n]+)\"?\s*$")


def source_priority_policy() -> dict[str, Any]:
    """Return the source-priority contract for metrics-loop evidence."""

    return {
        "schema_version": 1,
        "write_policy": "read_only",
        "source_of_truth": list(_SOURCE_OF_TRUTH),
        "generated_review_only": list(_GENERATED_REVIEW_ONLY),
        "rejected": list(_REJECTED_SOURCES),
        "generated_view_success_claim_policy": "never",
        "notes": [
            "HTML dashboards and reports are generated review views only.",
            "Memory and raw chat logs are recall material, not evidence.",
            "Community claims require verification before evidence use.",
        ],
    }


def collect_target_registry(workspace: str | Path) -> dict[str, Any]:
    """Collect local agentic targets without external calls or workspace writes."""

    root = Path(workspace)
    targets: list[dict[str, Any]] = []
    targets.extend(_agent_targets(root))
    targets.extend(_skill_targets(root))
    targets.extend(_artifact_policy_targets(root))
    targets.extend(_automation_candidate_targets(root))
    targets.extend(_config_targets(root))
    targets.extend(_harness_targets(root))
    targets = _dedupe_targets(targets)
    targets = _bounded_list(targets, "target_id", METRICS_PACKET_LIMITS["targets"])
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "policy": source_priority_policy(),
        "targets": targets,
        "summary": {
            "total": len(targets),
            "by_type": _counts(targets, "target_type"),
            "no_data": sum(1 for target in targets if target.get("no_data_status") != "metrics_data_present"),
        },
        "warnings": [],
    }
    return _redacted_dict(packet)


def build_evidence_packet(
    workspace: str | Path,
    *,
    as_of_date: str = "",
    max_records: int | None = None,
    evidence_max_age_days: int = 14,
) -> dict[str, Any]:
    """Build a bounded evidence packet from explicit project artifacts only."""

    root = Path(workspace)
    records: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []

    for path in _evidence_candidate_paths(root):
        relative = _relative_path(root, path)
        excluded_type = _excluded_source_type(relative)
        if excluded_type:
            excluded.append(_excluded_record(relative, excluded_type))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        records.extend(_records_from_text(relative, text, as_of_date, evidence_max_age_days))

    limit = max_records or METRICS_PACKET_LIMITS["evidence_records"]
    bounded, warnings = _trim_records(records, limit, "evidence_records")
    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "as_of_date": as_of_date,
        "policy": source_priority_policy(),
        "evidence_records": bounded,
        "excluded_records": sorted(excluded, key=lambda item: (item["source_type"], item["source_path"])),
        "summary": {
            "total": len(bounded),
            "by_source_type": _counts(bounded, "source_type"),
            "excluded": len(excluded),
        },
        "warnings": warnings,
    }
    return _redacted_dict(packet)


def build_metrics_packet(
    *,
    targets: list[dict[str, Any]] | None = None,
    evidence_records: list[dict[str, Any]] | None = None,
    questions: list[dict[str, Any]] | None = None,
    update_candidates: list[dict[str, Any]] | None = None,
    embedded_json: Any | None = None,
) -> dict[str, Any]:
    """Build a bounded metrics-loop packet safe for later routing or rendering."""

    warnings: list[str] = []
    bounded_targets, target_warnings = _trim_items(
        targets or [],
        METRICS_PACKET_LIMITS["targets"],
        "targets",
    )
    bounded_evidence, evidence_warnings = _trim_items(
        evidence_records or [],
        METRICS_PACKET_LIMITS["evidence_records"],
        "evidence_records",
    )
    bounded_questions, question_warnings = _trim_items(
        questions or [],
        METRICS_PACKET_LIMITS["questions"],
        "questions",
    )
    bounded_candidates, candidate_warnings = _trim_items(
        update_candidates or [],
        METRICS_PACKET_LIMITS["update_candidates"],
        "update_candidates",
    )
    warnings.extend(target_warnings)
    warnings.extend(evidence_warnings)
    warnings.extend(question_warnings)
    warnings.extend(candidate_warnings)
    embedded, embedded_warnings = _bounded_embedded_json(embedded_json)
    warnings.extend(embedded_warnings)

    packet = {
        "schema_version": 1,
        "write_policy": "read_only",
        "limits": dict(METRICS_PACKET_LIMITS),
        "policy": source_priority_policy(),
        "targets": bounded_targets,
        "evidence_records": bounded_evidence,
        "questions": bounded_questions,
        "update_candidates": bounded_candidates,
        "embedded_json": embedded,
        "warnings": sorted(set(warnings)),
    }
    return _redacted_dict(packet)


def _agent_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    agent_paths = sorted((root / ".codex" / "agents").glob("*.toml"))
    for path in agent_paths:
        text = _safe_read(path)
        name = _metadata_value(text, "name") or path.stem
        targets.append(
            _target(
                target_id=f"agent:{_slug(name)}",
                target_type="agent",
                name=name,
                source_path=_relative_path(root, path),
                owner=_metadata_value(text, "owner"),
                version=_metadata_value(text, "version"),
                risk_level=_metadata_value(text, "risk_level") or "medium",
                expected_artifacts=["agent-task-packet.md", "handoff-contract.md", "eval-run-report.md"],
                eval_suite=["agent_skill_metrics"],
                maturity_level="configured",
                tool_permission_level="workspace_tools",
            )
        )
    if len(agent_paths) > 1:
        targets.append(
            _target(
                target_id="subagent_team:codex-agents",
                target_type="subagent_team",
                name="codex-agents",
                source_path=".codex/agents",
                expected_artifacts=["worktree-ownership.md", "handoff-contract.md"],
                eval_suite=["handoff-completeness", "agent_skill_metrics"],
                maturity_level="configured",
                tool_permission_level="workspace_tools",
            )
        )
    return targets


def _skill_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    search_roots = [
        root / ".codex" / "skills",
        root / "skills",
        root / "plugins" / "product-agent-os" / "skills",
    ]
    for skill_root in search_roots:
        if not skill_root.exists():
            continue
        for path in sorted(skill_root.glob("*/SKILL.md")):
            text = _safe_read(path)
            name = _frontmatter_value(text, "name") or path.parent.name
            targets.append(
                _target(
                    target_id=f"skill:{_slug(name)}",
                    target_type="skill",
                    name=name,
                    source_path=_relative_path(root, path),
                    owner=_frontmatter_value(text, "owner"),
                    version=_frontmatter_value(text, "version"),
                    risk_level=_frontmatter_value(text, "risk_level") or "medium",
                    expected_artifacts=["skill-promotion-record.md", "agent-eval-workflow.md"],
                    eval_suite=["agent_skill_metrics", "transcript_session_eval"],
                    maturity_level="managed",
                    tool_permission_level="workspace_tools",
                )
            )
    return targets


def _artifact_policy_targets(root: Path) -> list[dict[str, Any]]:
    definitions = [
        ("prompt-contract.md", "prompt_pack", "prompt-contract", "prompt_contract"),
        ("model-reasoning-policy.md", "policy_pack", "model-reasoning-policy", "model_reasoning_policy"),
        ("mcp-permission-review.md", "policy_pack", "mcp-permission-review", "tool_permission_policy"),
        ("hook-governance.md", "policy_pack", "hook-governance", "hook_policy"),
        ("agent-workflow-map.md", "policy_pack", "agent-workflow-map", "agent_workflow_policy"),
    ]
    targets = []
    for filename, target_type, name, maturity in definitions:
        for path in _find_named_artifacts(root, filename):
            targets.append(
                _target(
                    target_id=f"{target_type}:{_slug(name)}",
                    target_type=target_type,
                    name=name,
                    source_path=_relative_path(root, path),
                    expected_artifacts=["eval-run-report.md", "trace-evidence-packet.md"],
                    eval_suite=["agent_skill_metrics"],
                    maturity_level=maturity,
                    tool_permission_level="policy_documented",
                )
            )
    return targets


def _automation_candidate_targets(root: Path) -> list[dict[str, Any]]:
    targets = []
    candidate_root = root / ".codex" / "automation-candidates"
    if not candidate_root.exists():
        return targets
    for path in sorted(candidate_root.glob("*.md")):
        name = path.stem
        targets.append(
            _target(
                target_id=f"automation_candidate:{_slug(name)}",
                target_type="automation_candidate",
                name=name,
                source_path=_relative_path(root, path),
                risk_level="high",
                expected_artifacts=["automation-candidate.md", "approval-record.md", "eval-run-report.md"],
                eval_suite=["automation_policy", "agent_skill_metrics"],
                maturity_level="candidate_only",
                tool_permission_level="approval_bound",
                production_impact=True,
            )
        )
    return targets


def _config_targets(root: Path) -> list[dict[str, Any]]:
    path = root / ".codex" / "config.toml"
    if not path.exists():
        return []
    return [
        _target(
            target_id="policy_pack:codex-config",
            target_type="policy_pack",
            name="codex-config",
            source_path=_relative_path(root, path),
            expected_artifacts=["model-reasoning-policy.md", "mcp-permission-review.md", "approval-record.md"],
            eval_suite=["agent_skill_metrics"],
            maturity_level="configured",
            tool_permission_level="codex_policy",
        )
    ]


def _harness_targets(root: Path) -> list[dict[str, Any]]:
    paths = [
        root / ".codex" / "product-agent-os" / "harness-version.json",
        root / ".codex" / "product-agent-os" / "status.json",
    ]
    targets = []
    for path in paths:
        if not path.exists():
            continue
        name = path.stem
        targets.append(
            _target(
                target_id=f"harness:{_slug(name)}",
                target_type="harness",
                name=name,
                source_path=_relative_path(root, path),
                expected_artifacts=["eval-run-report.md", "trace-evidence-packet.md"],
                eval_suite=["agent_skill_metrics"],
                maturity_level="detected",
                tool_permission_level="read_only",
            )
        )
    return targets


def _target(
    *,
    target_id: str,
    target_type: str,
    name: str,
    source_path: str,
    owner: str = "",
    version: str = "",
    risk_level: str = "unknown",
    expected_artifacts: list[str] | None = None,
    eval_suite: list[str] | None = None,
    maturity_level: str = "detected",
    usage_volume: str = "unknown",
    tool_permission_level: str = "unknown",
    production_impact: bool = False,
) -> dict[str, Any]:
    return {
        "target_id": target_id,
        "target_type": target_type,
        "name": name,
        "owner": owner or "unassigned",
        "version": version or "unversioned",
        "risk_level": risk_level if risk_level in {"low", "medium", "high", "unknown"} else "unknown",
        "expected_artifacts": expected_artifacts or [],
        "eval_suite": eval_suite or [],
        "source_artifacts": [source_path],
        "maturity_level": maturity_level,
        "usage_volume": usage_volume,
        "tool_permission_level": tool_permission_level,
        "production_impact": bool(production_impact),
        "no_data_status": "target_registered_no_metrics_yet",
    }


def _evidence_candidate_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for filename in _CONTROL_PLANE_FILES:
        path = root / filename
        if path.exists() and path.is_file():
            paths.append(path)
    for pattern in [
        ".codex/artifact-templates/trace-evidence-packet.md",
        ".codex/artifact-templates/eval-run-report.md",
        ".codex/evals/*.json",
        ".codex/eval-reports/*.json",
        ".codex/product-agent-os/status.html",
        ".codex/eval-reports/*.html",
        "memory.md",
        "raw-chat.log",
    ]:
        paths.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(paths), key=lambda item: item.as_posix())


def _records_from_text(relative: str, text: str, as_of_date: str, evidence_max_age_days: int) -> list[dict[str, Any]]:
    source_type = _source_type(relative, text)
    recorded_at = _first_date(text)
    records = [
        _evidence_record(
            source_path=relative,
            source_type=source_type,
            status=_status_from_text(text),
            recorded_at=recorded_at,
        )
    ]
    if Path(relative).name in _CONTROL_PLANE_FILES and source_type != "control_plane":
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="control_plane",
                status=_status_from_text(text),
                recorded_at=recorded_at,
            )
        )
    lowered = text.lower()
    if "accepted gap" in lowered:
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="accepted_gap",
                status="accepted_gap",
                recorded_at=recorded_at,
            )
        )
    if "failed verification" in lowered or "verification failed" in lowered or "fixture eval failed" in lowered:
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="failed_verification",
                status="failed",
                recorded_at=recorded_at,
            )
        )
    if _is_stale(recorded_at, as_of_date, evidence_max_age_days):
        records.append(
            _evidence_record(
                source_path=relative,
                source_type="stale_evidence",
                status="stale",
                recorded_at=recorded_at,
            )
        )
    return records


def _source_type(relative: str, text: str) -> str:
    name = Path(relative).name
    lowered = f"{relative}\n{text}".lower()
    if name == "trace-evidence-packet.md":
        return "trace_packet"
    if name == "eval-run-report.md" or any(hint in lowered for hint in _EVAL_HINTS):
        return "eval_packet"
    if name in _CONTROL_PLANE_FILES:
        return "control_plane"
    if relative.endswith(".json"):
        return "run_record"
    return "control_plane"


def _excluded_source_type(relative: str) -> str:
    lowered = relative.lower()
    name = Path(relative).name.lower()
    if name == "status.html" or lowered.endswith("/status.html"):
        return "status_dashboard_html"
    if name == "agent-skill-evaluation-report.html":
        return "metrics_report_html"
    if name.endswith(".html"):
        return "generated_report_html"
    if name.startswith("memory"):
        return "memory"
    if "raw-chat" in name or "raw_chat" in name:
        return "raw_chat_log"
    return ""


def _evidence_record(*, source_path: str, source_type: str, status: str, recorded_at: str = "") -> dict[str, Any]:
    record_id = _stable_id(source_type, source_path, status, recorded_at)
    return {
        "record_id": record_id,
        "source_type": source_type,
        "source_path": source_path,
        "status": status,
        "recorded_at": recorded_at,
    }


def _excluded_record(source_path: str, source_type: str) -> dict[str, Any]:
    return {
        "record_id": _stable_id("excluded", source_type, source_path),
        "source_type": source_type,
        "source_path": source_path,
        "reason": "not_source_of_truth",
    }


def _status_from_text(text: str) -> str:
    lowered = text.lower()
    if "accepted gap" in lowered:
        return "accepted_gap_present"
    if "failed verification" in lowered or "verification failed" in lowered or "fixture eval failed" in lowered:
        return "failed"
    if "exited 0" in lowered or "0 failures" in lowered or " ok" in lowered:
        return "recorded"
    return "present_unverified"


def _first_date(text: str) -> str:
    match = _DATE_PATTERN.search(text)
    return match.group(1) if match else ""


def _is_stale(recorded_at: str, as_of_date: str, max_age_days: int) -> bool:
    try:
        recorded = date.fromisoformat(recorded_at)
        current = date.fromisoformat(as_of_date)
    except ValueError:
        return False
    return (current - recorded).days > max_age_days


def _trim_items(items: list[dict[str, Any]], limit: int, name: str) -> tuple[list[dict[str, Any]], list[str]]:
    sorted_items = sorted((_json_ready(item) for item in items), key=_item_sort_key)
    if len(sorted_items) <= limit:
        return sorted_items, []
    return sorted_items[:limit], [f"{name}_trimmed"]


def _trim_records(items: list[dict[str, Any]], limit: int, name: str) -> tuple[list[dict[str, Any]], list[str]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        unique[str(item.get("record_id"))] = item
    return _trim_items(list(unique.values()), limit, name)


def _bounded_list(items: list[dict[str, Any]], key: str, limit: int) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for item in items:
        unique[str(item.get(key))] = item
    return sorted(unique.values(), key=lambda item: str(item.get(key)))[:limit]


def _bounded_embedded_json(value: Any) -> tuple[dict[str, Any], list[str]]:
    if value is None:
        return {"status": "empty", "byte_size": 0, "data": None}, []
    rendered = json.dumps(value, sort_keys=True, separators=(",", ":"))
    byte_size = len(rendered.encode("utf-8"))
    limit = METRICS_PACKET_LIMITS["embedded_json_bytes"]
    if byte_size <= limit:
        return {"status": "included", "byte_size": byte_size, "data": value}, []
    return {
        "status": "trimmed",
        "byte_size": limit,
        "original_byte_size": byte_size,
        "data": None,
    }, ["embedded_json_trimmed"]


def _dedupe_targets(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unique: dict[str, dict[str, Any]] = {}
    for target in targets:
        unique[str(target.get("target_id"))] = target
    return sorted(unique.values(), key=lambda item: str(item.get("target_id")))


def _find_named_artifacts(root: Path, filename: str) -> list[Path]:
    candidates = [
        root / filename,
        root / ".codex" / "artifact-templates" / filename,
        root / "plugins" / "product-agent-os" / "assets" / "templates" / "artifact-templates" / filename,
    ]
    return [path for path in candidates if path.exists() and path.is_file()]


def _metadata_value(text: str, key: str) -> str:
    for line in text.splitlines():
        match = _KEY_VALUE_PATTERN.match(line)
        if match and match.group(1).strip().lower() == key.lower():
            return match.group(2).strip()
    return ""


def _frontmatter_value(text: str, key: str) -> str:
    if not text.startswith("---"):
        return ""
    for line in text.splitlines()[1:]:
        if line.strip() == "---":
            break
        match = _KEY_VALUE_PATTERN.match(line)
        if match and match.group(1).strip().lower() == key.lower():
            return match.group(2).strip()
    return ""


def _safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def _item_sort_key(item: dict[str, Any]) -> tuple[str, str]:
    for key in ("target_id", "record_id", "id", "candidate_id", "source_path"):
        value = item.get(key)
        if value:
            return key, str(value)
    return "json", json.dumps(item, sort_keys=True)


def _json_ready(item: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(item, sort_keys=True, default=str))


def _stable_id(*parts: str) -> str:
    return "_".join(_slug(part) for part in parts if part)[:120] or "record"


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower()).strip("-")
    return slug or "unknown"


def _counts(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _redacted_dict(packet: dict[str, Any]) -> dict[str, Any]:
    redacted, report = redact_payload(packet)
    if not isinstance(redacted, dict):
        return {"schema_version": 1, "write_policy": "read_only", "redaction_summary": report}
    redacted["redaction_summary"] = report
    return redacted
