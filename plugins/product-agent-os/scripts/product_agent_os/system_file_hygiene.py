from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import re
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.stage_manifest import content_digest
from product_agent_os.validators import is_forbidden_secret_assignment


TRIGGER_POLICY: dict[str, Any] = {
    "schedule_status": "not_created",
    "write_policy": "read_only",
    "periodic_triggers": [
        {
            "id": "weekly_full_system_file_hygiene",
            "cadence": "weekly",
            "scope": "all maintained system file classes",
            "write_policy": "read_only",
            "action": "emit report and staged compaction candidates only",
            "stop_conditions": [
                "secrets or unreadable system files are detected",
                "hard-size violations lack an owner routing destination",
                "active schedule markers appear in automation candidates",
            ],
        },
        {
            "id": "monthly_deep_ownership_review",
            "cadence": "monthly",
            "scope": "ownership, source-of-truth routing, duplicate guidance and stale evidence",
            "write_policy": "read_only",
            "action": "emit owner review packet only",
            "stop_conditions": [
                "ownership or source-of-truth routing is ambiguous",
                "historical ledger content has no destination artifact",
            ],
        },
    ],
    "event_triggers": [
        {
            "id": "root_control_plane_change",
            "when": "after changes to AGENTS.md, REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md or README.md",
            "scope": "changed root control-plane file plus adjacent source owner",
            "write_policy": "read_only",
            "action": "emit report and owner routing recommendation only",
            "stop_conditions": [
                "duplicate durable rules, secrets, stale success claims or hard-size violations are introduced",
            ],
        },
        {
            "id": "agent_skill_or_workflow_change",
            "when": "after changes to .codex/agents, .codex/skills, .codex/workflows, .codex/hooks, .codex/evals or .codex/automation-candidates",
            "scope": "changed Codex agent, skill, workflow, hook, eval or automation candidate file",
            "write_policy": "read_only",
            "action": "emit focused agent/skill/workflow hygiene finding only",
            "stop_conditions": [
                "role ownership, trigger, verification, failure mode or disable path is missing",
                "active schedule markers appear before explicit approval",
            ],
        },
        {
            "id": "release_or_automation_approval_review",
            "when": "before release, PR creation, plugin packaging or enabling any automation schedule",
            "scope": "system files, automation candidates, approval records and rollback evidence",
            "write_policy": "read_only",
            "action": "emit approval readiness findings only",
            "stop_conditions": [
                "manual stability evidence, explicit approval or rollback/disable evidence is missing",
                "GitHub Actions, Codex App automation, hook activation or external write is implied without approval",
            ],
        },
        {
            "id": "failed_verification_or_repeated_compaction",
            "when": "after failed verification, repeated manual compaction or stale evidence discovery",
            "scope": "files implicated by the failed check plus their owning source packets",
            "write_policy": "read_only",
            "action": "emit stale-evidence and routing findings only",
            "stop_conditions": [
                "evidence cannot be traced to a current source owner",
                "a generated view is treated as source of truth",
            ],
        },
    ],
    "size_triggers": [
        {
            "id": "soft_size_review",
            "scope": "file that crossed its soft limit plus likely destination artifacts",
            "write_policy": "read_only",
            "action": "review ownership and duplicate content",
            "stop_conditions": [
                "continued edits would add implementation history to the wrong owner file",
            ],
        },
        {
            "id": "hard_size_compaction_required",
            "scope": "file that crossed its hard limit plus required owner routing",
            "write_policy": "read_only",
            "action": "stage compaction proposal before adding more history",
            "stop_conditions": [
                "hard-size violation has no owner routing plan",
                "compaction would delete unique source-backed information",
            ],
        },
    ],
}


@dataclass(frozen=True)
class SystemFileClass:
    key: str
    label: str
    patterns: tuple[str, ...]
    owner: str
    soft_limit_chars: int
    hard_limit_chars: int
    maintenance_focus: str


SYSTEM_FILE_CLASSES: tuple[SystemFileClass, ...] = (
    SystemFileClass(
        key="root_control_plane",
        label="Root Product-Agent OS control plane",
        patterns=("AGENTS.md", "REQUIREMENTS.md", "PLAN.md", "TEST.md", "EVALS.md", "RUNLOG.md"),
        owner="project root",
        soft_limit_chars=40000,
        hard_limit_chars=50000,
        maintenance_focus="current state, ownership routing, evidence-before-completion and compact handoff",
    ),
    SystemFileClass(
        key="project_entrypoint",
        label="Project entrypoint and operator overview",
        patterns=("README.md",),
        owner="project root",
        soft_limit_chars=40000,
        hard_limit_chars=50000,
        maintenance_focus="product/operator entrypoint without historical implementation ledger",
    ),
    SystemFileClass(
        key="nested_agents_md",
        label="Nested AGENTS.md instruction layers",
        patterns=("**/AGENTS.md",),
        owner="nearest workspace or package",
        soft_limit_chars=30000,
        hard_limit_chars=45000,
        maintenance_focus="durable local rules without duplicated root policy or task logs",
    ),
    SystemFileClass(
        key="codex_config",
        label="Codex project configuration",
        patterns=(".codex/config.toml", ".codex/settings.json", ".mcp.json", ".codex/*.mcp.json"),
        owner="project operator",
        soft_limit_chars=12000,
        hard_limit_chars=20000,
        maintenance_focus="permissions, model policy, MCP boundaries and no secrets",
    ),
    SystemFileClass(
        key="codex_agents",
        label="Codex subagent profiles",
        patterns=(".codex/agents/*.toml",),
        owner="agent-team designer",
        soft_limit_chars=12000,
        hard_limit_chars=18000,
        maintenance_focus="role ownership, inputs, outputs, stop conditions and model policy",
    ),
    SystemFileClass(
        key="codex_skills",
        label="Project skills",
        patterns=(".codex/skills/**/SKILL.md", "skills/**/SKILL.md"),
        owner="skill owner",
        soft_limit_chars=24000,
        hard_limit_chars=36000,
        maintenance_focus="single repeatable method, trigger, inputs, outputs, verification and failure modes",
    ),
    SystemFileClass(
        key="codex_workflows",
        label="Project workflow playbooks",
        patterns=(".codex/workflows/*.md",),
        owner="workflow owner",
        soft_limit_chars=20000,
        hard_limit_chars=30000,
        maintenance_focus="stable steps, evidence, stop conditions and rollback",
    ),
    SystemFileClass(
        key="artifact_templates",
        label="Reusable artifact templates",
        patterns=(".codex/artifact-templates/*.md",),
        owner="docs maintainer",
        soft_limit_chars=18000,
        hard_limit_chars=28000,
        maintenance_focus="fillable contract fields without implementation history or private data",
    ),
    SystemFileClass(
        key="automation_candidates",
        label="Automation candidate packets",
        patterns=(".codex/automation-candidates/*.md",),
        owner="automation owner",
        soft_limit_chars=16000,
        hard_limit_chars=24000,
        maintenance_focus="candidate-only readiness, owner, cadence, stable IO, verification and disable path",
    ),
    SystemFileClass(
        key="hooks",
        label="Project hook policy files",
        patterns=(".codex/hooks/*",),
        owner="project operator",
        soft_limit_chars=16000,
        hard_limit_chars=24000,
        maintenance_focus="least privilege, no secrets, explicit activation and rollback",
    ),
    SystemFileClass(
        key="evals",
        label="Local eval definitions",
        patterns=(".codex/evals/*.json", "evals/*.json"),
        owner="test/eval owner",
        soft_limit_chars=50000,
        hard_limit_chars=75000,
        maintenance_focus="bounded cases, thresholds, privacy-safe fixtures and current evidence windows",
    ),
    SystemFileClass(
        key="pr_release_packets",
        label="PR and release packet templates",
        patterns=(".codex/pr/*.md", ".github/PULL_REQUEST_TEMPLATE*.md"),
        owner="release operator",
        soft_limit_chars=18000,
        hard_limit_chars=28000,
        maintenance_focus="release evidence, risks, rollback and explicit git/external-action boundaries",
    ),
    SystemFileClass(
        key="docs_source_control",
        label="Documentation source and evidence control files",
        patterns=(
            "docs/sources/registry*.md",
            "docs/sources/*backlog*.md",
            "docs/sources/*approval*.md",
            "docs/sources/*evidence*.md",
            "docs/insights/*.md",
            "docs/superpowers/plans/*task-matrix*.md",
            "docs/playbooks/*.md",
            "docs/product-agent/**/*.md",
            "docs/product-agent-os/**/*.md",
            "docs/runtime/**/*.md",
            "docs/artifact-templates/**/*.md",
            "mkdocs.yml",
            "tools/check_docs.py",
        ),
        owner="docs maintainer",
        soft_limit_chars=120000,
        hard_limit_chars=180000,
        maintenance_focus="source status, registry routing, public/internal boundaries and stale evidence",
    ),
    SystemFileClass(
        key="external_automation_policy",
        label="External automation and repository governance files",
        patterns=(".github/workflows/*", "CODEOWNERS", "SECURITY.md", ".github/dependabot.yml"),
        owner="release or security operator",
        soft_limit_chars=30000,
        hard_limit_chars=50000,
        maintenance_focus="least privilege, external writes, schedules, branch scope and rollback",
    ),
    SystemFileClass(
        key="plugin_package_control",
        label="Checked-in plugin package control files",
        patterns=(
            "plugins/*/.codex-plugin/plugin.json",
            "plugins/*/README.md",
            "plugins/*/.mcp.json",
            "plugins/*/skills/**/SKILL.md",
            "plugins/*/assets/templates/**/*.md",
            "plugins/*/assets/templates/**/*.json",
        ),
        owner="plugin maintainer",
        soft_limit_chars=60000,
        hard_limit_chars=90000,
        maintenance_focus="plugin manifest, skill contracts, template registry and package evidence",
    ),
)


EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "site",
    "tmp",
    "output",
    ".tmp-external",
    ".product-agent-os-status-current",
    "fixtures",
}
MOJIBAKE_MARKERS = (
    "\u0420\u045c",
    "\u0420\u045f",
    "\u0420\u00b0",
    "\u0420\u0451",
    "\u0420\u00bb",
    "\u0421\u0403",
    "\u0421\u201a",
    "\u0421\u040a",
    "\u0420\u00a0\u0421\u045a",
    "\u0420\u00a0\u0421\u045f",
)
HISTORICAL_LEDGER_PATTERN = re.compile(
    r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+|done_through"
)
ACTIVE_SCHEDULE_PATTERN = re.compile(
    r"(?im)(recurring schedule is active|codex app automation:\s*active|github actions workflow:\s*active|^\s*-?\s*(cron|rrule|schedule):|^\s*-?\s*hook activation:\s*active\b|^\s*-?\s*external writes?:\s*active\b)"
)
SYSTEM_FILE_CLASS_BY_KEY = {item.key: item for item in SYSTEM_FILE_CLASSES}
MAX_FILE_STATUSES = 200
SYSTEM_FILE_STALE_AFTER_DAYS = 30
SYSTEM_FILE_STATUS_STATES = {
    "ok",
    "review_required",
    "blocked",
    "missing",
    "unreadable",
    "stale",
    "owner_unknown",
}
SHA256_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


def build_system_file_hygiene_audit(
    root: str | Path,
    audit_trigger: str = "manual_owner_requested",
    audit_started_at: str | None = None,
) -> dict[str, Any]:
    workspace = Path(root)
    inventory: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    trigger = audit_trigger.strip() if isinstance(audit_trigger, str) and audit_trigger.strip() else "manual_owner_requested"
    audit_dt = _audit_datetime(audit_started_at)
    last_audit_at = audit_dt.isoformat()

    if not workspace.exists() or not workspace.is_dir():
        workspace_findings = [
            _finding(
                "error",
                "workspace_not_found",
                _workspace_ref(workspace),
                "workspace must be an existing directory",
                None,
            )
        ]
        return {
            "artifact_kind": "system_file_hygiene_audit",
            "schema_version": 1,
            "audit_trigger": trigger,
            "last_audit_at": last_audit_at,
            "workspace": _workspace_ref(workspace),
            "write_policy": "read_only",
            "schedule_status": "not_created",
            "status": "blocked",
            "triggers": TRIGGER_POLICY,
            "system_file_classes": system_file_class_records(),
            "inventory": [],
            "findings": workspace_findings,
            "file_statuses": [],
            "summary": _summary("blocked", [], workspace_findings, trigger),
        }

    seen: set[Path] = set()
    for file_class in SYSTEM_FILE_CLASSES:
        for path in _iter_matching_files(workspace, file_class):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            record, file_findings = _inspect_system_file(workspace, path, file_class)
            inventory.append(record)
            findings.extend(file_findings)

    missing_control_plane = [
        name for name in CONTROL_PLANE_FILES if not (workspace / name).exists()
    ]
    for name in missing_control_plane:
        findings.append(
            _finding(
                "warning",
                "missing_control_plane_file",
                name,
                "Product-Agent OS control-plane file is missing",
                SYSTEM_FILE_CLASS_BY_KEY["root_control_plane"],
            )
        )

    errors = [finding for finding in findings if finding["severity"] == "error"]
    warnings = [finding for finding in findings if finding["severity"] == "warning"]
    status = "blocked" if errors else "review_required" if warnings else "ok"
    return {
        "artifact_kind": "system_file_hygiene_audit",
        "schema_version": 1,
        "audit_trigger": trigger,
        "last_audit_at": last_audit_at,
        "workspace": _workspace_ref(workspace),
        "write_policy": "read_only",
        "schedule_status": "not_created",
        "status": status,
        "triggers": TRIGGER_POLICY,
        "system_file_classes": system_file_class_records(),
        "inventory": sorted(inventory, key=lambda item: item["path"]),
        "findings": sorted(findings, key=lambda item: (item["severity"], item["path"], item["code"])),
        "file_statuses": _file_statuses(inventory, findings, audit_dt, last_audit_at),
        "summary": _summary(status, warnings, errors, trigger, files_scanned=len(inventory)),
    }


def system_file_class_records() -> list[dict[str, Any]]:
    return [
        {
            "key": item.key,
            "label": item.label,
            "patterns": list(item.patterns),
            "owner": item.owner,
            "soft_limit_chars": item.soft_limit_chars,
            "hard_limit_chars": item.hard_limit_chars,
            "maintenance_focus": item.maintenance_focus,
        }
        for item in SYSTEM_FILE_CLASSES
    ]


def validate_system_file_hygiene_audit(packet: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("artifact_kind") != "system_file_hygiene_audit":
        errors.append("artifact_kind:invalid")
    if packet.get("schema_version") != 1:
        errors.append("schema_version:unsupported")
    if not isinstance(packet.get("audit_trigger"), str) or not packet["audit_trigger"].strip():
        errors.append("audit_trigger:required")
    if packet.get("write_policy") != "read_only":
        errors.append("write_policy:must_be_read_only")
    if packet.get("schedule_status") != "not_created":
        errors.append("schedule_status:must_be_not_created")
    if packet.get("status") not in {"ok", "review_required", "blocked"}:
        errors.append("status:invalid")
    triggers = packet.get("triggers")
    if not isinstance(triggers, dict):
        errors.append("triggers:required")
    elif not _valid_trigger_policy(triggers):
        errors.append("triggers:invalid")
    system_file_classes = packet.get("system_file_classes")
    if not isinstance(system_file_classes, list) or not system_file_classes:
        errors.append("system_file_classes:required")
    elif not all(_valid_system_file_class_record(item) for item in system_file_classes):
        errors.append("system_file_classes:invalid")
    inventory = packet.get("inventory")
    if not isinstance(inventory, list):
        errors.append("inventory:required")
    elif not all(_valid_inventory_record(item) for item in inventory):
        errors.append("inventory:invalid")
    findings = packet.get("findings")
    if not isinstance(findings, list):
        errors.append("findings:required")
    elif not all(_valid_finding_record(item) for item in findings):
        errors.append("findings:invalid")
    file_statuses = packet.get("file_statuses")
    if not isinstance(file_statuses, list):
        errors.append("file_statuses:required")
    elif len(file_statuses) > MAX_FILE_STATUSES or not all(_valid_file_status_record(item) for item in file_statuses):
        errors.append("file_statuses:invalid")
    summary = packet.get("summary")
    if not isinstance(summary, dict):
        errors.append("summary:required")
    elif summary.get("status") not in {"ok", "review_required", "blocked"}:
        errors.append("summary:status_required")
    elif summary["status"] != packet.get("status"):
        errors.append("summary:status_mismatch")
    elif not all(isinstance(summary.get(key), int) and summary[key] >= 0 for key in ("files_scanned", "warnings", "errors")):
        errors.append("summary:invalid")
    elif summary.get("audit_trigger") != packet.get("audit_trigger"):
        errors.append("summary:audit_trigger_mismatch")
    elif summary.get("no_secrets_status") not in {"passed", "blocked"}:
        errors.append("summary:no_secrets_status_required")
    elif not isinstance(summary.get("active_schedule_markers"), int) or summary["active_schedule_markers"] < 0:
        errors.append("summary:invalid")
    elif summary.get("approval_boundary") != "owner_approval_required_for_writes":
        errors.append("summary:invalid")
    return errors


def _valid_trigger_policy(triggers: dict[str, Any]) -> bool:
    if triggers.get("write_policy") != "read_only" or triggers.get("schedule_status") != "not_created":
        return False
    for group in ("periodic_triggers", "event_triggers", "size_triggers"):
        records = triggers.get(group)
        if not isinstance(records, list) or not records:
            return False
        if not all(_valid_trigger_record(item) for item in records):
            return False
    return True


def _valid_trigger_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    required_strings = ("id", "scope", "action")
    if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required_strings):
        return False
    if record.get("write_policy") != "read_only":
        return False
    stop_conditions = record.get("stop_conditions")
    return isinstance(stop_conditions, list) and bool(stop_conditions) and all(
        isinstance(item, str) and item.strip() for item in stop_conditions
    )


def _valid_system_file_class_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    required_strings = ("key", "label", "owner", "maintenance_focus")
    if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required_strings):
        return False
    patterns = record.get("patterns")
    if not isinstance(patterns, list) or not patterns or not all(isinstance(item, str) and item.strip() for item in patterns):
        return False
    soft_limit = record.get("soft_limit_chars")
    hard_limit = record.get("hard_limit_chars")
    return isinstance(soft_limit, int) and isinstance(hard_limit, int) and 0 < soft_limit <= hard_limit


def _valid_inventory_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    required_strings = ("path", "class", "owner")
    if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required_strings):
        return False
    if not isinstance(record.get("readable"), bool):
        return False
    return all(
        isinstance(record.get(key), int) and record[key] >= 0
        for key in ("chars", "lines", "soft_limit_chars", "hard_limit_chars")
    )


def _valid_finding_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    if record.get("severity") not in {"warning", "error"}:
        return False
    if record.get("approval_boundary") != "owner_approval_required_for_writes":
        return False
    return all(
        isinstance(record.get(key), str) and record[key].strip()
        for key in (
            "code",
            "path",
            "message",
            "class",
            "owner",
            "finding_type",
            "compaction_decision",
        )
    )


def _valid_file_status_record(record: Any) -> bool:
    if not isinstance(record, dict):
        return False
    if any(key in record for key in ("raw_body", "raw_content", "content", "text", "excerpt")):
        return False
    if not _safe_relative_path(str(record.get("path", ""))):
        return False
    if record.get("state") not in SYSTEM_FILE_STATUS_STATES:
        return False
    if record.get("severity") not in {"none", "warning", "error"}:
        return False
    if "top_finding" in record and not isinstance(record["top_finding"], str):
        return False
    required_strings = ("class", "owner", "mtime_utc", "content_digest", "last_audit_at")
    if any(not isinstance(record.get(key), str) or not record[key].strip() for key in required_strings):
        return False
    if _parse_datetime(record["mtime_utc"]) is None or _parse_datetime(record["last_audit_at"]) is None:
        return False
    if not SHA256_DIGEST_PATTERN.match(record["content_digest"]):
        return False
    return all(
        isinstance(record.get(key), int) and record[key] >= 0
        for key in ("finding_count", "size", "line_count", "age_days")
    )


def _iter_matching_files(root: Path, file_class: SystemFileClass) -> list[Path]:
    matches: list[Path] = []
    for pattern in file_class.patterns:
        for path in root.glob(pattern):
            if path.is_file() and not _is_excluded(path.relative_to(root)):
                matches.append(path)
    return sorted(matches)


def _is_excluded(relative_path: Path) -> bool:
    return any(part in EXCLUDED_PARTS for part in relative_path.parts)


def _inspect_system_file(root: Path, path: Path, file_class: SystemFileClass) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    relative = path.relative_to(root).as_posix()
    findings: list[dict[str, Any]] = []
    raw = b""
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        metadata = _file_metadata(path, raw)
        return (
            {
                "path": relative,
                "class": file_class.key,
                "chars": 0,
                "lines": 0,
                "readable": False,
                "owner": file_class.owner,
                "soft_limit_chars": file_class.soft_limit_chars,
                "hard_limit_chars": file_class.hard_limit_chars,
                **metadata,
            },
            [
                _finding(
                    "error",
                    "unreadable_utf8",
                    relative,
                    f"unable to read as utf-8: {exc}",
                    file_class,
                )
            ],
        )

    chars = len(text)
    lines = text.count("\n") + (1 if text else 0)
    record = {
        "path": relative,
        "class": file_class.key,
        "chars": chars,
        "lines": lines,
        "readable": True,
        "owner": file_class.owner,
        "soft_limit_chars": file_class.soft_limit_chars,
        "hard_limit_chars": file_class.hard_limit_chars,
        **_file_metadata(path, raw),
    }
    if chars >= file_class.hard_limit_chars:
        findings.append(_finding("error", "hard_size_limit_exceeded", relative, f"{chars} chars >= {file_class.hard_limit_chars}", file_class))
    elif chars >= file_class.soft_limit_chars:
        findings.append(_finding("warning", "soft_size_limit_exceeded", relative, f"{chars} chars >= {file_class.soft_limit_chars}", file_class))
    if text.startswith("\ufeff"):
        findings.append(_finding("warning", "utf8_bom_present", relative, "UTF-8 BOM should be removed from system files", file_class))
    if any(marker in text for marker in MOJIBAKE_MARKERS):
        findings.append(_finding("warning", "mojibake_marker_present", relative, "possible mojibake marker found", file_class))
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        findings.append(_finding("error", "secret_like_literal", relative, "secret-like assignment is forbidden in system files", file_class))
    if path.suffix.lower() == ".md":
        duplicate_headings = _duplicate_headings(text)
        if duplicate_headings:
            findings.append(
                _finding(
                    "warning",
                    "duplicate_markdown_headings",
                    relative,
                    "duplicate headings: " + ", ".join(duplicate_headings[:5]),
                    file_class,
                )
            )
    ledger_count = len(HISTORICAL_LEDGER_PATTERN.findall(text))
    if _needs_ledger_density_warning(relative, file_class.key, ledger_count):
        findings.append(
            _finding(
                "warning",
                "historical_ledger_density",
                relative,
                f"{ledger_count} historical ledger markers require ownership review",
                file_class,
            )
        )
    if ACTIVE_SCHEDULE_PATTERN.search(text):
        findings.append(
            _finding(
                "error",
                "active_schedule_in_candidate",
                relative,
                "system file must not contain an active schedule before explicit approval",
                file_class,
            )
        )
    return record, findings


def _file_metadata(path: Path, raw: bytes) -> dict[str, Any]:
    try:
        stat = path.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime, UTC).replace(microsecond=0).isoformat()
    except OSError:
        mtime = datetime.fromtimestamp(0, UTC).isoformat()
    return {
        "mtime_utc": mtime,
        "content_digest": content_digest(raw),
    }


def _file_statuses(
    inventory: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    audit_dt: datetime,
    last_audit_at: str,
) -> list[dict[str, Any]]:
    findings_by_path: dict[str, list[dict[str, Any]]] = {}
    for finding in findings:
        path = str(finding.get("path", ""))
        findings_by_path.setdefault(path, []).append(finding)
    records: list[dict[str, Any]] = []
    inventory_paths: set[str] = set()
    for item in sorted(inventory, key=lambda record: record["path"]):
        path = str(item.get("path", ""))
        if not _safe_relative_path(path):
            continue
        inventory_paths.add(path)
        file_findings = findings_by_path.get(path, [])
        severity = _status_severity(file_findings)
        age_days = _age_days(str(item.get("mtime_utc", "")), audit_dt)
        state = _status_state(file_findings, severity, str(item.get("owner", "")), age_days)
        records.append(
            {
                "path": path,
                "class": str(item.get("class", "")),
                "owner": str(item.get("owner", "")),
                "state": state,
                "severity": severity,
                "finding_count": len(file_findings),
                "size": int(item.get("chars", 0)),
                "line_count": int(item.get("lines", 0)),
                "mtime_utc": str(item.get("mtime_utc", "")),
                "age_days": age_days,
                "content_digest": str(item.get("content_digest", "")),
                "last_audit_at": last_audit_at,
                "top_finding": _top_finding(file_findings, state),
            }
        )
    for path, file_findings in sorted(findings_by_path.items()):
        if path in inventory_paths or not _safe_relative_path(path):
            continue
        severity = _status_severity(file_findings)
        owner = _finding_owner(file_findings)
        state = _status_state(file_findings, severity, owner, 0)
        records.append(
            {
                "path": path,
                "class": _finding_class(file_findings),
                "owner": owner,
                "state": state,
                "severity": severity,
                "finding_count": len(file_findings),
                "size": 0,
                "line_count": 0,
                "mtime_utc": datetime.fromtimestamp(0, UTC).isoformat(),
                "age_days": 0,
                "content_digest": content_digest(b""),
                "last_audit_at": last_audit_at,
                "top_finding": _top_finding(file_findings, state),
            }
        )
    return sorted(records, key=_file_status_sort_key)[:MAX_FILE_STATUSES]


def _status_severity(findings: list[dict[str, Any]]) -> str:
    if any(finding.get("severity") == "error" for finding in findings):
        return "error"
    if any(finding.get("severity") == "warning" for finding in findings):
        return "warning"
    return "none"


def _status_state(findings: list[dict[str, Any]], severity: str, owner: str, age_days: int) -> str:
    codes = {str(finding.get("code", "")) for finding in findings}
    finding_types = {str(finding.get("finding_type", "")) for finding in findings}
    if "missing_control_plane_file" in codes or "missing_required_file" in finding_types:
        return "missing"
    if "unreadable_utf8" in codes or "readability" in finding_types:
        return "unreadable"
    normalized_owner = owner.strip().lower()
    if not normalized_owner or normalized_owner in {"unknown", "owner_unknown", "not_available"}:
        return "owner_unknown"
    if severity == "error":
        return "blocked"
    if severity == "warning":
        return "review_required"
    if age_days >= SYSTEM_FILE_STALE_AFTER_DAYS:
        return "stale"
    return "ok"


def _top_finding(findings: list[dict[str, Any]], state: str) -> str:
    if findings:
        ordered = sorted(
            findings,
            key=lambda finding: (
                0 if finding.get("severity") == "error" else 1,
                str(finding.get("code", "")),
            ),
        )
        return str(ordered[0].get("code") or "system_file_hygiene")
    if state == "stale":
        return f"mtime_older_than_{SYSTEM_FILE_STALE_AFTER_DAYS}_days"
    if state == "owner_unknown":
        return "owner_unknown"
    return "none"


def _finding_class(findings: list[dict[str, Any]]) -> str:
    for finding in findings:
        value = str(finding.get("class", "")).strip()
        if value:
            return value
    return "workspace"


def _finding_owner(findings: list[dict[str, Any]]) -> str:
    for finding in findings:
        value = str(finding.get("owner", "")).strip()
        if value:
            return value
    return "project operator"


def _file_status_sort_key(record: dict[str, Any]) -> tuple[int, str, str]:
    state_rank = {
        "blocked": 0,
        "unreadable": 1,
        "missing": 2,
        "review_required": 3,
        "owner_unknown": 4,
        "stale": 5,
        "ok": 6,
    }
    return (
        state_rank.get(str(record.get("state", "")), 9),
        str(record.get("class", "")),
        str(record.get("path", "")),
    )


def _age_days(mtime_utc: str, audit_dt: datetime) -> int:
    parsed = _parse_datetime(mtime_utc)
    if parsed is None:
        return 0
    return max(0, (audit_dt - parsed).days)


def _audit_datetime(value: str | None) -> datetime:
    parsed = _parse_datetime(value or "")
    if parsed is not None:
        return parsed.replace(microsecond=0)
    return datetime.now(UTC).replace(microsecond=0)


def _parse_datetime(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC).replace(microsecond=0)


def _safe_relative_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if not normalized or normalized.startswith(("/", "../", "~")):
        return False
    if ":/" in normalized or re.match(r"^[A-Za-z]:", normalized):
        return False
    return ".." not in normalized.split("/")


def _workspace_ref(workspace: Path) -> str:
    name = workspace.name.strip()
    return name or "."


def _duplicate_headings(text: str) -> list[str]:
    counts: dict[str, int] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        heading = re.sub(r"\s+", " ", stripped.lstrip("#").strip().lower())
        if not heading:
            continue
        counts[heading] = counts.get(heading, 0) + 1
    return sorted(heading for heading, count in counts.items() if count > 1)


def _needs_ledger_density_warning(relative: str, class_key: str, marker_count: int) -> bool:
    if marker_count == 0:
        return False
    if relative == "README.md":
        return True
    if class_key == "root_control_plane" and relative not in {"RUNLOG.md", "TEST.md", "EVALS.md"}:
        return marker_count > 20
    if class_key in {"codex_agents", "codex_skills", "codex_workflows", "artifact_templates"}:
        return marker_count > 10
    return False


def _summary(
    status: str,
    warnings: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    audit_trigger: str,
    files_scanned: int = 0,
) -> dict[str, Any]:
    findings = [*warnings, *errors]
    secret_like_findings = sum(1 for finding in findings if finding["code"] == "secret_like_literal")
    secret_scan_unverifiable_findings = sum(
        1 for finding in findings if finding["code"] in {"unreadable_utf8", "workspace_not_found"}
    )
    active_schedule_markers = sum(1 for finding in findings if finding["finding_type"] == "active_schedule")
    return {
        "status": status,
        "files_scanned": files_scanned,
        "warnings": len(warnings),
        "errors": len(errors),
        "audit_trigger": audit_trigger,
        "no_secrets_status": "blocked" if secret_like_findings or secret_scan_unverifiable_findings else "passed",
        "secret_like_findings": secret_like_findings,
        "secret_scan_unverifiable_findings": secret_scan_unverifiable_findings,
        "active_schedule_markers": active_schedule_markers,
        "approval_boundary": "owner_approval_required_for_writes",
    }


def _finding(
    severity: str,
    code: str,
    path: str,
    message: str,
    file_class: SystemFileClass | None,
) -> dict[str, str]:
    class_key = file_class.key if file_class else "workspace"
    owner = file_class.owner if file_class else "project operator"
    return {
        "severity": severity,
        "code": code,
        "path": path,
        "message": message,
        "class": class_key,
        "owner": owner,
        "finding_type": _finding_type(code),
        "compaction_decision": _compaction_decision(code),
        "approval_boundary": "owner_approval_required_for_writes",
    }


def _finding_type(code: str) -> str:
    if code == "missing_control_plane_file":
        return "missing_required_file"
    if code in {"workspace_not_found", "unreadable_utf8"}:
        return "readability"
    if code in {"utf8_bom_present", "mojibake_marker_present"}:
        return "encoding"
    if code == "secret_like_literal":
        return "secret"
    if code == "duplicate_markdown_headings":
        return "structure"
    if code in {"soft_size_limit_exceeded", "hard_size_limit_exceeded"}:
        return "size"
    if code == "historical_ledger_density":
        return "historical_ledger"
    if code == "active_schedule_in_candidate":
        return "active_schedule"
    return "system_file_hygiene"


def _compaction_decision(code: str) -> str:
    if code in {"workspace_not_found", "unreadable_utf8", "secret_like_literal", "active_schedule_in_candidate"}:
        return "blocked_until_owner_review"
    if code == "missing_control_plane_file":
        return "restore_or_record_accepted_gap"
    if code in {"utf8_bom_present", "mojibake_marker_present"}:
        return "repair_encoding_before_compaction"
    if code == "soft_size_limit_exceeded":
        return "review_before_more_edits"
    if code in {"hard_size_limit_exceeded", "historical_ledger_density", "duplicate_markdown_headings"}:
        return "route_to_owner_before_compaction"
    return "owner_review"
