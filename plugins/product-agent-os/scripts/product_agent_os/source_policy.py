from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from product_agent_os.validators import is_forbidden_secret_assignment


OPENAI_BEHAVIOR_PATTERN = re.compile(
    r"\b(OpenAI|Codex|Agents SDK|MCP|hooks?|approvals?|models?|automation|sandbox)\b",
    re.IGNORECASE,
)
OFFICIAL_HOSTS = {"developers.openai.com", "platform.openai.com", "learn.chatgpt.com", "help.openai.com", "openai.com"}
URL_PATTERN = re.compile(r'https?://[^\s<>"`]+', re.IGNORECASE)
CHECKED_DATE_PATTERN = re.compile(r"(?im)^[ \t]*(?:Checked(?: on)?|checked_on|Last verified|Проверено|Дата проверки)(?:[ \t]*:[ \t]*|[ \t]+)`?([^\s`]+)")
FRESHNESS_REVIEW_DAYS = 90  # Local review heuristic, never a source freshness guarantee.
COMMUNITY_PATTERN = re.compile(r"\b(community|user report|reddit|forum|сообщество|отчет пользователя)\b", re.IGNORECASE)
FRESHNESS_PATTERN = re.compile(
    r"\b(current|latest|today|сейчас|актуальн|models?|pricing|security|approvals?|hooks?|Agents SDK|MCP|automation)\b",
    re.IGNORECASE,
)
SENSITIVE_DATA_LITERAL_PATTERN = re.compile(
    r"(?i)^\s*(?:raw_?pii|pii_value|payment_?data|private_?customer_?data|raw_?private_?chat|customer_?data_value)\s*[=:]\s*[^\r\n]+"
)


def validate_source_policy(workspace: str | Path, *, as_of: date | None = None) -> dict[str, Any]:
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
            file_report = _validate_file(workspace_path, path, as_of or date.today())
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


def _validate_file(workspace: Path, path: Path, as_of: date) -> dict[str, Any]:
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
    exempt = relative in {"docs/index.md", "docs/index.en.md", "docs/sources/registry.md", "docs/sources/registry.en.md"}
    source_evidence = _source_evidence(text, as_of)
    references, registry_hosts = _registry_evidence(workspace, path, text)
    source_evidence["registry_references"] = references
    source_evidence["official_hosts"] = sorted(set(source_evidence["official_hosts"]) | registry_hosts)
    source_evidence["source_present"] = bool(source_evidence["official_hosts"])
    supported_facts: list[str] = []
    assumptions: list[str] = []
    unsupported_claims: list[str] = []
    missing_context: list[str] = []
    freshness_risks: list[str] = []
    secret_findings: list[str] = []

    if source_status == "missing" and not exempt:
        missing_context.append("Source status is required")
    if source_evidence["claim_class"] == "official_behavior" and not source_evidence["source_present"]:
        missing_context.append("official source hint is required for OpenAI behavior claim")
    if any(ref["status"] != "resolved" for ref in references):
        missing_context.append("registry reference is missing or unsafe")
    if source_evidence["source_present"]:
        supported_facts.append("Official-source URL is present; content and claim support were not verified")
    if source_evidence["freshness"]["status"] in {"stale", "invalid", "future", "conflict"}:
        missing_context.append("source check date requires review")
    if source_evidence["claim_class"] == "official_behavior" and FRESHNESS_PATTERN.search(text):
        freshness_risks.append("current OpenAI/runtime behavior may drift")
    if _has_community_claim(text) and not _has_community_metadata(text):
        unsupported_claims.append("community claim lacks trust_level or verification_status")
    for line_number, line in _non_fenced_lines(text):
        if is_forbidden_secret_assignment(line):
            secret_findings.append(f"{relative}:{line_number}: secret-like literal is forbidden")
        if SENSITIVE_DATA_LITERAL_PATTERN.search(line):
            secret_findings.append(f"{relative}:{line_number}: raw PII/private data/payment data marker is forbidden")

    return {
        "path": relative,
        "source_status": source_status,
        "source_evidence": source_evidence,
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
    match = re.search(r"(?m)^Source status:[ \t]*([^\r\n]+)", text)
    return match.group(1).strip().strip("`") or "missing" if match else "missing"


def _has_openai_behavior_claim(text: str) -> bool:
    return _claim_class(text) == "official_behavior"


def _claim_class(text: str) -> str:
    """Conservative lexical routing, not a semantic verification verdict.

    Explicit external behavior overrides a project-local label. A historical
    receipt or project contract alone does not become an official claim merely
    because it names Codex. Mixed pages still need human semantic review.
    """
    prose = "\n".join(line for _, line in _non_fenced_lines(text))
    status = _source_status(prose).lower()
    explicit_behavior = any(
        OPENAI_BEHAVIOR_PATTERN.search(line)
        and re.search(r"\b(supports?|allows?|requires?|always|never|automatically|доступ\w*|поддержива\w*|всегда|автоматически|позволя\w*)\b", line, re.I)
        for line in prose.splitlines() if not line.startswith(("#", "Source status:"))
    )
    if explicit_behavior:
        return "official_behavior"
    if re.search(r"historical|receipt|историческ", status):
        return "historical_receipt"
    if re.search(r"project.(?:local|authored|plan|contract|evidence)|проектн", status):
        return "project_contract"
    if "official" in status and re.search(r"\b(approvals?|sandbox|MCP|hooks?|models?)\b", prose, re.I):
        return "official_behavior"
    return "mention_only" if OPENAI_BEHAVIOR_PATTERN.search(prose) else "unknown"


def _has_official_source_hint(text: str) -> bool:
    return bool(_official_hosts(text))


def _official_hosts(text: str) -> list[str]:
    """Classify exact URL hosts; headings, userinfo and suffixes are not evidence."""
    hosts = set()
    prose = "\n".join(line for _, line in _non_fenced_lines(text))
    for candidate in URL_PATTERN.findall(prose):
        try:
            parsed = urlsplit(candidate.rstrip(".,);]}"))
            host = (parsed.hostname or "").lower().rstrip(".")
            if parsed.scheme.lower() != "https" or parsed.username is not None or parsed.password is not None or parsed.port not in (None, 443):
                continue
            if host in OFFICIAL_HOSTS or (host == "github.com" and parsed.path.lower().split("/")[1:2] == ["openai"]):
                hosts.add(host)
        except ValueError:
            continue
    return sorted(hosts)


def _source_evidence(text: str, as_of: date) -> dict[str, Any]:
    """Separate link presence, date markers and semantic evidence; no web requests."""
    hosts = _official_hosts(text)
    prose = "\n".join(line for _, line in _non_fenced_lines(text))
    markers = [match.group(1).rstrip(".,:;") for match in CHECKED_DATE_PATTERN.finditer(prose)
               if match.group(1).lower() not in {"against", "по"}]
    freshness = {"status": "missing", "checked_on": None, "review_after_days": FRESHNESS_REVIEW_DAYS}
    if markers:
        try:
            dates = []
            for value in markers:
                if re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", value):
                    day, month, year = value.split(".")
                    value = f"{year}-{month}-{day}"
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                    raise ValueError("invalid_calendar_marker")
                dates.append(date.fromisoformat(value))
            # Different sections may have different check dates. Use the oldest
            # marker conservatively; never promote the whole page from its latest.
            freshness["checked_on"] = min(dates).isoformat()
            freshness["checked_dates"] = sorted({value.isoformat() for value in dates})
            age = (as_of - min(dates)).days
            freshness["status"] = "future" if max(dates) > as_of else "stale" if age > FRESHNESS_REVIEW_DAYS else "date_present_not_verified"
        except ValueError:
            freshness["status"] = "invalid"
    return {"source_present": bool(hosts), "official_hosts": hosts, "claim_class": _claim_class(text),
            "claim_supported": "not_verified", "freshness": freshness}


def _registry_evidence(workspace: Path, page: Path, text: str) -> tuple[list[dict[str, str]], set[str]]:
    """Resolve one local registry hop; no crawler, external read or date inheritance."""
    root = workspace.resolve()
    allowed = {"docs/sources/registry.md", "docs/sources/registry.en.md"}
    references: list[dict[str, str]] = []
    hosts: set[str] = set()
    prose = "\n".join(line for _, line in _non_fenced_lines(text))
    for target in re.findall(r"\[[^\]\n]*\]\(([^)\s]+)\)", prose)[:256]:
        decoded = unquote(target)
        if not decoded.split("#", 1)[0].replace("\\", "/").endswith(("registry.md", "registry.en.md")):
            continue
        ref = {"status": "unsafe", "path": ""}
        references.append(ref)
        try:
            parsed = urlsplit(decoded)
            if parsed.scheme or parsed.netloc or parsed.query or "\\" in decoded or parsed.path.startswith("/"):
                continue
            resolved = (page.parent / parsed.path).resolve()
            if not resolved.is_relative_to(root):
                continue
            relative = resolved.relative_to(root).as_posix()
            if relative not in allowed or not resolved.is_file():
                ref["status"] = "missing"
                continue
            ref["path"] = relative
            if resolved.stat().st_size > 1024 * 1024:
                ref["status"] = "needs_review"
                continue
            registry = resolved.read_text(encoding="utf-8")
            if parsed.fragment:
                registry = _registry_section(registry, parsed.fragment)
                if registry is None:
                    ref["status"] = "missing"
                    continue
            ref["status"] = "resolved"
            hosts.update(_official_hosts(registry))
        except (OSError, ValueError):
            ref["status"] = "missing"
    return references, hosts


def _registry_section(text: str, anchor: str) -> str | None:
    """Select a heading section or explicit table source ID, never an unrelated row."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            slug = re.sub(r"[^\w\s-]", "", heading.group(2).lower()).replace(" ", "-")
            if slug != anchor.lower():
                continue
            end = index + 1
            while end < len(lines):
                next_heading = re.match(r"^(#{1,6})\s", lines[end])
                if next_heading and len(next_heading.group(1)) <= len(heading.group(1)):
                    break
                end += 1
            return "\n".join(lines[index:end])
        if line.startswith("|") and line.split("|")[1].strip().strip("`").lower() == anchor.lower():
            return line
    return None


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
