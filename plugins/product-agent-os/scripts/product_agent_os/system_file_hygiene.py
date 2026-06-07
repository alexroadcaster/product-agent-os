from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path
from typing import Any

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.validators import is_forbidden_secret_assignment


TRIGGER_POLICY: dict[str, Any] = {
    "schedule_status": "not_created",
    "write_policy": "read_only",
    "periodic_triggers": [
        {
            "id": "weekly_full_system_file_hygiene",
            "cadence": "weekly",
            "scope": "all maintained system file classes",
            "action": "emit report and staged compaction candidates only",
        },
        {
            "id": "monthly_deep_ownership_review",
            "cadence": "monthly",
            "scope": "ownership, source-of-truth routing, duplicate guidance and stale evidence",
            "action": "emit owner review packet only",
        },
    ],
    "event_triggers": [
        "after changes to AGENTS.md, REQUIREMENTS.md, PLAN.md, TEST.md, EVALS.md, RUNLOG.md or README.md",
        "after changes to .codex/agents, .codex/skills, .codex/workflows, .codex/hooks, .codex/evals or .codex/automation-candidates",
        "before release, PR creation, plugin packaging or enabling any automation schedule",
        "after failed verification, repeated manual compaction or stale evidence discovery",
    ],
    "size_triggers": [
        {
            "id": "soft_size_review",
            "action": "review ownership and duplicate content",
        },
        {
            "id": "hard_size_compaction_required",
            "action": "stage compaction proposal before adding more history",
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
MOJIBAKE_MARKERS = ("Рќ", "Рџ", "Р°", "Рё", "Р»", "СЃ", "С‚", "СЊ")
HISTORICAL_LEDGER_PATTERN = re.compile(
    r"\b(Task|Track|Batch)\b|T[0-9]+-[A-Z0-9-]+|B[0-9]+-[A-Z]+-M[0-9]+|done_through"
)
ACTIVE_SCHEDULE_PATTERN = re.compile(
    r"(?im)(recurring schedule is active|codex app automation:\s*active|github actions workflow:\s*active|^cron:|^rrule:)"
)


def build_system_file_hygiene_audit(root: str | Path) -> dict[str, Any]:
    workspace = Path(root)
    inventory: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []

    if not workspace.exists() or not workspace.is_dir():
        return {
            "artifact_kind": "system_file_hygiene_audit",
            "schema_version": 1,
            "workspace": str(workspace),
            "write_policy": "read_only",
            "schedule_status": "not_created",
            "status": "blocked",
            "triggers": TRIGGER_POLICY,
            "system_file_classes": system_file_class_records(),
            "inventory": [],
            "findings": [
                {
                    "severity": "error",
                    "code": "workspace_not_found",
                    "path": str(workspace),
                    "message": "workspace must be an existing directory",
                }
            ],
            "summary": {"files_scanned": 0, "warnings": 0, "errors": 1},
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
            {
                "severity": "warning",
                "code": "missing_control_plane_file",
                "path": name,
                "message": "Product-Agent OS control-plane file is missing",
            }
        )

    errors = [finding for finding in findings if finding["severity"] == "error"]
    warnings = [finding for finding in findings if finding["severity"] == "warning"]
    status = "blocked" if errors else "review_required" if warnings else "ok"
    return {
        "artifact_kind": "system_file_hygiene_audit",
        "schema_version": 1,
        "workspace": str(workspace),
        "write_policy": "read_only",
        "schedule_status": "not_created",
        "status": status,
        "triggers": TRIGGER_POLICY,
        "system_file_classes": system_file_class_records(),
        "inventory": sorted(inventory, key=lambda item: item["path"]),
        "findings": sorted(findings, key=lambda item: (item["severity"], item["path"], item["code"])),
        "summary": {
            "files_scanned": len(inventory),
            "warnings": len(warnings),
            "errors": len(errors),
        },
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
    if packet.get("write_policy") != "read_only":
        errors.append("write_policy:must_be_read_only")
    if packet.get("schedule_status") != "not_created":
        errors.append("schedule_status:must_be_not_created")
    if packet.get("status") not in {"ok", "review_required", "blocked"}:
        errors.append("status:invalid")
    if not isinstance(packet.get("triggers"), dict):
        errors.append("triggers:required")
    if not isinstance(packet.get("system_file_classes"), list) or not packet.get("system_file_classes"):
        errors.append("system_file_classes:required")
    if not isinstance(packet.get("inventory"), list):
        errors.append("inventory:required")
    if not isinstance(packet.get("findings"), list):
        errors.append("findings:required")
    return errors


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
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return (
            {
                "path": relative,
                "class": file_class.key,
                "chars": 0,
                "lines": 0,
                "readable": False,
                "soft_limit_chars": file_class.soft_limit_chars,
                "hard_limit_chars": file_class.hard_limit_chars,
            },
            [
                {
                    "severity": "error",
                    "code": "unreadable_utf8",
                    "path": relative,
                    "message": f"unable to read as utf-8: {exc}",
                }
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
        "soft_limit_chars": file_class.soft_limit_chars,
        "hard_limit_chars": file_class.hard_limit_chars,
    }
    if chars >= file_class.hard_limit_chars:
        findings.append(_finding("error", "hard_size_limit_exceeded", relative, f"{chars} chars >= {file_class.hard_limit_chars}"))
    elif chars >= file_class.soft_limit_chars:
        findings.append(_finding("warning", "soft_size_limit_exceeded", relative, f"{chars} chars >= {file_class.soft_limit_chars}"))
    if text.startswith("\ufeff"):
        findings.append(_finding("warning", "utf8_bom_present", relative, "UTF-8 BOM should be removed from system files"))
    if any(marker in text for marker in MOJIBAKE_MARKERS):
        findings.append(_finding("warning", "mojibake_marker_present", relative, "possible mojibake marker found"))
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        findings.append(_finding("error", "secret_like_literal", relative, "secret-like assignment is forbidden in system files"))
    if path.suffix.lower() == ".md":
        duplicate_headings = _duplicate_headings(text)
        if duplicate_headings:
            findings.append(
                _finding(
                    "warning",
                    "duplicate_markdown_headings",
                    relative,
                    "duplicate headings: " + ", ".join(duplicate_headings[:5]),
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
            )
        )
    if file_class.key == "automation_candidates" and ACTIVE_SCHEDULE_PATTERN.search(text):
        findings.append(
            _finding(
                "error",
                "active_schedule_in_candidate",
                relative,
                "automation candidate must not contain an active schedule",
            )
        )
    return record, findings


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


def _finding(severity: str, code: str, path: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "path": path, "message": message}
