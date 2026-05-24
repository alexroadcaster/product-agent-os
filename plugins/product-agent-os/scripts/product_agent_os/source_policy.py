from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from product_agent_os.validators import is_forbidden_secret_assignment


OPENAI_BEHAVIOR_PATTERN = re.compile(
    r"\b(OpenAI|Codex|Agents SDK|MCP|hooks?|approvals?|models?|automation|sandbox)\b",
    re.IGNORECASE,
)
OFFICIAL_SOURCE_HINT_PATTERN = re.compile(
    r"(Sources?:|source registry|docs/sources/registry\.md|developers\.openai\.com|github\.com/openai|official docs)",
    re.IGNORECASE,
)
COMMUNITY_PATTERN = re.compile(r"\b(community|user report|reddit|forum|сообщество|отчет пользователя)\b", re.IGNORECASE)
FRESHNESS_PATTERN = re.compile(
    r"\b(current|latest|today|сейчас|актуальн|models?|pricing|security|approvals?|hooks?|Agents SDK|MCP|automation)\b",
    re.IGNORECASE,
)


def validate_source_policy(workspace: str | Path) -> dict[str, Any]:
    """Validate deterministic source-policy markers for a workspace."""
    workspace_path = Path(workspace)
    files: list[dict[str, Any]] = []
    errors: list[str] = []
    secret_findings: list[str] = []
    registry_updates_required: list[str] = []

    if not workspace_path.exists():
        errors.append(f"workspace does not exist: {workspace_path}")
    elif not workspace_path.is_dir():
        errors.append(f"workspace is not a directory: {workspace_path}")
    else:
        for path in _candidate_docs(workspace_path):
            file_report = _validate_file(workspace_path, path)
            files.append(file_report)
            if "Source status is required" in file_report["missing_context"]:
                errors.append("missing Source status")
            secret_findings.extend(file_report["secret_findings"])
            if file_report["registry_update_required"]:
                registry_updates_required.append(file_report["path"])

    status = _status(files, errors, secret_findings)
    report = {
        "status": status,
        "workspace": str(workspace_path),
        "files": files,
        "registry_updates_required": registry_updates_required,
        "secret_findings": secret_findings,
        "errors": sorted(set(errors)),
    }
    return report | {"source_policy_report": dict(report)}


def _candidate_docs(workspace: Path) -> list[Path]:
    docs_root = workspace / "docs"
    if docs_root.exists() and docs_root.is_dir():
        return sorted(docs_root.rglob("*.md"))
    return []


def _validate_file(workspace: Path, path: Path) -> dict[str, Any]:
    relative = path.relative_to(workspace).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return _file_report(
            relative,
            source_status="missing",
            missing_context=["unable to read file as utf-8 text"],
        )

    source_status = _source_status(text)
    exempt = relative in {"docs/index.md", "docs/sources/registry.md"}
    supported_facts: list[str] = []
    assumptions: list[str] = []
    unsupported_claims: list[str] = []
    missing_context: list[str] = []
    freshness_risks: list[str] = []
    secret_findings: list[str] = []

    if source_status == "missing" and not exempt:
        missing_context.append("Source status is required")
    if _has_openai_behavior_claim(text) and not _has_official_source_hint(text):
        missing_context.append("official source hint is required for OpenAI behavior claim")
    if _has_openai_behavior_claim(text):
        supported_facts.append("OpenAI-related claim requires source-policy review")
    if FRESHNESS_PATTERN.search(text):
        freshness_risks.append("current OpenAI/runtime behavior may drift")
    if _has_community_claim(text) and not _has_community_metadata(text):
        unsupported_claims.append("community claim lacks trust_level or verification_status")
    for line_number, line in _non_fenced_lines(text):
        if is_forbidden_secret_assignment(line):
            secret_findings.append(f"{relative}:{line_number}: secret-like literal is forbidden")

    return {
        "path": relative,
        "source_status": source_status,
        "supported_facts": supported_facts,
        "assumptions": assumptions,
        "unsupported_claims": unsupported_claims,
        "missing_context": missing_context,
        "freshness_risks": freshness_risks,
        "registry_update_required": bool(missing_context or unsupported_claims),
        "secret_findings": secret_findings,
    }


def _file_report(
    path: str,
    *,
    source_status: str,
    missing_context: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "path": path,
        "source_status": source_status,
        "supported_facts": [],
        "assumptions": [],
        "unsupported_claims": [],
        "missing_context": missing_context or [],
        "freshness_risks": [],
        "registry_update_required": bool(missing_context),
        "secret_findings": [],
    }


def _source_status(text: str) -> str:
    match = re.search(r"Source status:\s*`([^`]+)`", text)
    return match.group(1).strip() if match else "missing"


def _has_openai_behavior_claim(text: str) -> bool:
    return bool(OPENAI_BEHAVIOR_PATTERN.search(text))


def _has_official_source_hint(text: str) -> bool:
    return bool(OFFICIAL_SOURCE_HINT_PATTERN.search(text))


def _has_community_claim(text: str) -> bool:
    return bool(COMMUNITY_PATTERN.search(text))


def _has_community_metadata(text: str) -> bool:
    return "trust_level:" in text and "verification_status:" in text


def _non_fenced_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    fence_length = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        fence = re.match(r"^\s*(`{3,})", line)
        if fence and fence_length == 0:
            fence_length = len(fence.group(1))
            continue
        if fence and fence_length and len(fence.group(1)) >= fence_length:
            fence_length = 0
            continue
        if fence_length == 0:
            lines.append((line_number, line))
    return lines


def _status(files: list[dict[str, Any]], errors: list[str], secret_findings: list[str]) -> str:
    if errors or secret_findings:
        return "blocked"
    if any(item["missing_context"] or item["unsupported_claims"] for item in files):
        return "needs_review"
    return "ok"
