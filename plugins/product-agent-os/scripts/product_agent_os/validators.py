from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Any

import tomllib

from product_agent_os.contracts import CONTROL_PLANE_FILES
from product_agent_os.doubt_verification import (
    DOUBT_VERIFICATION_PACKET_SCHEMA_VERSION,
    main_doubt_verification,
    validate_doubt_verification_packet,
    validate_doubt_verification_packet_file,
)


def read_skill_contract(path: Path) -> str:
    """Read entrypoint plus its exact conditional role section for static checks.

    This is a verification reader, not runtime loading or activation. No recursive
    links, unrelated role sections or external references enter the contract.
    Non-skill artifact callers retain their existing plain-text read behavior.
    """
    text = path.read_text(encoding="utf-8")
    if path.name != "SKILL.md" or "## Conditional References" not in text:
        return text
    name = path.parent.name
    if not re.fullmatch(r"[a-z0-9-]+", name) or f"`Skill: {name}`" not in text or "../references/complexity-routing.md" not in text:
        raise ValueError("invalid_conditional_skill_reference")
    root = path.parent.parent.resolve()
    reference = (root / "references/complexity-routing.md").resolve()
    if not reference.is_relative_to(root):
        raise ValueError("conditional_reference_outside_skills")
    with reference.open("rb") as stream:
        raw = stream.read(512 * 1024 + 1)
    if len(raw) > 512 * 1024:
        raise ValueError("conditional_reference_too_large")
    sections = re.findall(r"(?ms)^## Skill: " + re.escape(name) + r"\n(.*?)(?=^## |\Z)", raw.decode("utf-8").replace("\r\n", "\n"))
    if len(sections) != 1:
        raise ValueError("conditional_skill_section_missing_or_ambiguous")
    return text + "\n" + sections[0]


def validate_skill_agent_metadata(path: Path, *, expected_implicit: bool = False) -> list[str]:
    """Validate the repository's flat YAML subset without enabling any skill.

    Complex YAML, aliases and unknown fields require review rather than being
    guessed by a permissive regex parser. No third-party YAML runtime is needed.
    """
    try:
        if path.stat().st_size > 65536:
            return ["metadata_too_large"]
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return ["metadata_missing_or_unreadable"]
    sections: dict[str, dict[str, str]] = {}
    current = None
    errors = []
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        root = re.fullmatch(r"(interface|policy):\s*", line)
        if root:
            current = root[1]
            if current in sections:
                errors.append("duplicate_metadata_section")
            sections.setdefault(current, {})
            continue
        field = re.fullmatch(r"  ([a-z_]+):[ \t]*(.+)", line)
        if current is None or field is None:
            errors.append("unsupported_metadata_yaml")
            continue
        key, value = field.groups()
        if key in sections[current]:
            errors.append("duplicate_metadata_field")
        sections[current][key] = value.strip()
    interface = sections.get("interface", {})
    allowed = {"display_name", "short_description", "default_prompt", "icon_small", "icon_large", "brand_color"}
    if set(interface) - allowed:
        errors.append("unknown_interface_field")
    for key, value in interface.items():
        try:
            scalar = json.loads(value) if value.startswith('"') else value
            if not isinstance(scalar, str) or not scalar.strip() or scalar.startswith(("[", "{", "&", "*", "|", ">")) or (not value.startswith(('"', "'")) and (scalar.lower() in {"null", "true", "false", "yes", "no", "~"} or re.fullmatch(r"[-+]?\d+(?:\.\d+)?", scalar))):
                errors.append("invalid_interface_scalar:" + key)
        except ValueError:
            errors.append("invalid_interface_scalar:" + key)
    if not {"display_name", "short_description", "default_prompt"}.issubset(interface):
        errors.append("required_interface_field_missing")
    policy = sections.get("policy", {})
    if set(policy) != {"allow_implicit_invocation"}:
        errors.append("explicit_invocation_policy_required")
    if policy.get("allow_implicit_invocation") != ("true" if expected_implicit else "false"):
        errors.append("implicit_invocation_policy_mismatch")
    return sorted(set(errors))


def _skill_tree_digest(root: Path) -> dict[str, Any]:
    """Hash bounded skill text with canonical newlines; never return its contents."""
    if root.is_symlink() or root.parent.is_symlink():
        return {"present": True, "normalized_sha256": None, "raw_sha256": None, "errors": ["symlink_skill_root_requires_review"]}
    if not root.is_dir():
        return {"present": False, "normalized_sha256": None, "raw_sha256": None, "errors": []}
    normalized, raw_hashes, errors = {}, {}, []
    paths = sorted(p for p in root.rglob("*") if p.is_file())
    if len(paths) > 200:
        return {"present": True, "normalized_sha256": None, "raw_sha256": None, "errors": ["skill_inventory_limit"]}
    for path in paths:
        try:
            if not path.resolve().is_relative_to(root.resolve()) or path.stat().st_size > 1024 * 1024:
                raise ValueError("bounded_file_required")
            raw = path.read_bytes(); name = path.relative_to(root).as_posix()
            raw_hashes[name] = hashlib.sha256(raw).hexdigest()
            normalized[name] = hashlib.sha256(raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").encode()).hexdigest()
        except (OSError, ValueError):
            errors.append("skill_file_unreadable_or_unsupported")
    digest = lambda values: hashlib.sha256(json.dumps(values, sort_keys=True).encode()).hexdigest()
    return {"present": True, "normalized_sha256": digest(normalized) if not errors else None,
            "raw_sha256": digest(raw_hashes) if not errors else None, "errors": sorted(set(errors))}


def build_skill_provenance(source_root: Path, cache_root: Path | None = None, *, selected_root: Path | None = None) -> dict[str, Any]:
    """Separate source/cache presence from caller-selected path and host evidence."""
    source_root = source_root.resolve()
    cache_root = cache_root.resolve() if cache_root else None
    selected_root = selected_root.resolve() if selected_root else None
    source_names = {p.parent.name for p in (source_root / "skills").glob("*/SKILL.md")}
    cache_names = {p.parent.name for p in (cache_root / "skills").glob("*/SKILL.md")} if cache_root else set()
    records = []
    for name in sorted(source_names | cache_names):
        source = _skill_tree_digest(source_root / "skills" / name)
        cache = _skill_tree_digest(cache_root / "skills" / name) if cache_root else {"present": False, "normalized_sha256": None, "raw_sha256": None, "errors": []}
        metadata = source_root / "skills" / name / "agents/openai.yaml"
        policy_errors = validate_skill_agent_metadata(metadata) if metadata.resolve().is_relative_to(source_root) else ["metadata_outside_source"]
        selected = "repository" if selected_root == source_root else "installed_cache" if cache_root and selected_root == cache_root else "unknown"
        records.append({"name": name, "source_path": "source/skills/" + name, "cache_path": "cache/skills/" + name if cache_root else None,
                        "source": source, "cache": cache, "installed": cache["present"],
                        "normalized_match": bool(source["normalized_sha256"] and source["normalized_sha256"] == cache["normalized_sha256"]),
                        "policy_class": "read_only_implicit_candidate_not_enabled" if name == "workspace-discovery-auditor" else "explicit_only",
                        "implicit_enabled": False if not policy_errors else None, "metadata_errors": policy_errors,
                        "selected_source": selected, "selection_evidence": "caller_declared_path_not_host_loading",
                        "exposed": "not_verified", "invoked": "not_verified"})
    return {"schema_version": 1, "status": "needs_review" if any(r["metadata_errors"] or r["source"]["errors"] or r["cache"]["errors"] for r in records) else "present_unverified",
            "policy": "preserve_explicit_only_no_metadata_rewrite", "skills": records, "host_status": "not_verified"}


AGENT_REQUIRED_FIELDS = [
    "name",
    "description",
    "developer_instructions",
]
AGENT_FORBIDDEN_TOP_LEVEL_FIELDS = {
    "ownership",
    "inputs",
    "outputs",
    "stop_conditions",
    "model_policy",
    "handoff_requirements",
}
# Repository policy, not a claim that other official models are unsupported.
AGENT_ALLOWED_MODELS = {"gpt-6.1-sol", "gpt-6.1-terra"}
AGENT_ALLOWED_REASONING_EFFORTS = {"low", "medium", "high", "xhigh", "max"}
AGENT_PARENT_ONLY_FIELDS = {
    "sandbox_mode", "sandbox_workspace_write", "default_permissions", "permissions",
    "approval_policy", "approvals_reviewer", "model_provider", "mcp_servers",
    "service_tier",
}
AGENT_DISABLE_FEATURES = {"shell_tool", "apps", "plugins", "memories", "request_permissions_tool"}
AGENT_MAX_INSTRUCTION_CHARS = 7000
AGENT_PHASE_IDENTIFIER_PATTERN = re.compile(
    r"(?i)\b(?:Batch\s+\d+|B\d+-S\d+|Track\s+\d+)\b"
)
AGENT_PROMPT_PATH_PATTERN = re.compile(
    r"`(?P<path>(?:\.codex|docs|plugins|tests)/[A-Za-z0-9_./*-]+|"
    r"(?:AGENTS|REQUIREMENTS|PLAN|TEST|EVALS|RUNLOG|prod_test)\.md)`"
)
OPENAI_DOCS_SKILL_SUFFIX = "/openai-docs/skill.md"
PROJECT_SKILL_PATH_FRAGMENT = "/plugins/product-agent-os/skills/"
WORKSPACE_APPLY_AUTHORITY = "workspace_apply: explicit_task_authority"
TASK_MATRIX_SCHEMA_VERSION = "task_matrix_plan_v1"
TASK_MATRIX_ALLOWED_STATUSES = {"planned", "in_progress", "implemented", "blocked", "accepted_gap"}
TASK_MATRIX_REQUIRED_FIELDS = [
    "Task",
    "Status",
    "Schema version",
    "Timezone",
    "Plan trigger",
    "Validator target",
    "Date and time of task implementation",
    "Depends on",
    "Blocks",
    "Source",
    "Short description",
    "Technical value",
    "Product value",
    "Scope",
    "Non-goals",
    "Expected result",
    "Acceptance criteria",
    "Verification gates",
    "Risks / approval gates",
    "Complexity",
    "Estimated execution time",
    "Agents",
    "Skills",
    "Output artifacts",
    "Next step",
]
TASK_MATRIX_COMPLETION_FIELDS = [
    "status",
    "what was done",
    "files touched / work locations",
    "technical value delivered",
    "product value delivered",
    "actual implementation date and time",
    "verification evidence",
    "residual risks",
    "follow-up",
]
READ_TEXT_ERROR = "unable to read file as utf-8 text"
SECRET_NAME_PATTERN = re.compile(r"(?i)(SECRET|TOKEN|PASSWORD|PRIVATE[_-]?KEY|API[_-]?KEY)")
SECRET_ASSIGNMENT_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    (?:export\s+)?
    ["']?
    (?P<name>[A-Z_][A-Z0-9_.-]*)
    ["']?
    \s*(?:=|:)\s*
    (?P<value>[^#\r\n]+?)
    \s*$
    """
)
SECRET_ENVIRON_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    os\.environ\[
    (?P<quote>["'])
    (?P<name>[A-Z_][A-Z0-9_.-]*)
    (?P=quote)
    \]
    \s*=\s*
    (?P<value>[^#\r\n]+?)
    \s*$
    """
)
SAFE_ENV_LOOKUP_PATTERN = re.compile(
    r"""(?ix)
    ^\s*
    os\.
    (?:
        getenv
        |
        environ\.get
    )
    \(
    \s*
    (?P<quote>["'])
    [A-Z_][A-Z0-9_.-]*
    (?P=quote)
    \s*
    \)
    \s*$
    """
)
TASK_HEADING_PATTERN = re.compile(r"^###\s+Task\s+`?(?P<id>[^`\r\n]+?)`?\s*$")
TASK_FIELD_PATTERN = re.compile(r"^\s*-\s+(?P<name>[^:]+):\s*(?P<value>.*)$")
TASK_TIMESTAMP_PATTERN = re.compile(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$")
TASK_PLACEHOLDER_PATTERN = re.compile(r"(<[^>]+>|\{\{[^}]+\}\}|\{generated_at\}|\bTODO\b|\bTBD\b|\?\?\?|\.\.\.)")
HOOK_JSON_REQUIRED_EVENTS = [
    "SessionStart",
    "PreToolUse",
    "PermissionRequest",
    "PostToolUse",
    "Stop",
]
TASK_START_PACKET_FIELDS = [
    "Request", "Goal", "Context", "Scope", "Value", "Execution", "Acceptance",
    "Risks / approvals", "Next step",
]
COMPLETION_LEDGER_FIELDS = [
    "Result", "Scope", "Evidence", "Review", "Limits", "Tech debt",
    "Activation / fallback", "Docs impact", "Context integrity", "Runtime metrics",
    "Closure", "Next step", "Execution time",
]


def validate_report_authoring_request(output_path: str, previous_content: bytes | None,
                                     content: str) -> list[str]:
    """Validate authoring input shape; filesystem/session/grant checks belong to the hook."""
    if not isinstance(output_path, str) or not output_path:
        return ["report_path_required"]
    parts = output_path.split("/")
    protected = {"agents.md", "agents.override.md", "requirements.md", "plan.md", "test.md", "evals.md", "runlog.md", "skill.md"}
    if (any(p in {"", ".", ".."} or p.startswith(".") or p.endswith((".", " ")) for p in parts)
            or any(c in output_path for c in "\\:~") or any(ord(c) < 32 for c in output_path)
            or not output_path.endswith(".md") or parts[-1].lower() in protected
            or any(re.fullmatch(r"(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", p) for p in parts)):
        return ["report_path_must_be_canonical_unprotected_markdown"]
    if not isinstance(content, str) or not content.endswith("\n") or "\r" in content or len(content.encode("utf-8")) > 1_000_000:
        return ["report_content_requires_bounded_utf8_lf_text"]
    if previous_content is not None:
        if not isinstance(previous_content, bytes) or len(previous_content) > 1_000_000:
            return ["previous_report_must_be_bounded_bytes"]
        try:
            previous_content.decode("utf-8")
        except UnicodeError:
            return ["previous_report_must_be_utf8"]
    return []


def validate_lifecycle_packet_text(text: str, kind: str) -> list[str]:
    """Check reporting shape and explicit closure contradictions, not evidence truth.

    This is an opt-in local validator. Stop hooks do not automatically inspect chat.
    Fenced examples and quoted source text cannot satisfy visible packet fields.
    """
    if kind not in {"start", "completion"}:
        return ["packet kind must be start or completion"]
    visible = []
    fence = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence is None and not stripped.startswith(">"):
            visible.append(line)
    body = "\n".join(visible)
    required = TASK_START_PACKET_FIELDS if kind == "start" else COMPLETION_LEDGER_FIELDS
    pattern = (r"^\*\*([^*\n]+)\*\*[ \t]*$" if kind == "start" else
               r"^- (?:\*\*(?P<bold>[^*:\n]+):\*\*|(?P<plain>[^*:\n]+):)[ \t]*")
    matches = list(re.finditer(pattern, body, re.M))
    errors: list[str] = []
    fields: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1) if kind == "start" else (match.group("bold") or match.group("plain"))
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        value = body[match.end():end].strip()
        if name in fields:
            errors.append("duplicate packet field: " + name)
        fields[name] = value
        if name not in required:
            errors.append("unexpected packet field: " + name)
        if not value or value.casefold() in {"n/a", "not_available", "pending", "tbd"}:
            errors.append("packet field needs content or a reason: " + name)
    errors.extend("missing packet field: " + name for name in required if name not in fields)
    if kind == "completion":
        if not body.startswith("closure_contract: product-agent-os-completion-ledger-v2\n"):
            errors.append("missing Product-Agent OS completion ledger contract marker")
        review = fields.get("Review", "")
        closure = fields.get("Closure", "")
        if not re.search(r"\bcontext_mode\s*=\s*(self_review|separate_reused_context|separate_fresh_context|fresh_blind_review|not_available)\b", review):
            errors.append("Review must identify observed context_mode")
        verdict = re.search(r"\btester_verdict\s*=\s*(closed_allowed|partial_only|blocked|not_reviewed)\b", review)
        if verdict is None:
            errors.append("Review must identify tester_verdict")
        level = re.search(r"\bclosure_level\s*=\s*([a-z_]+)\b", closure)
        if level is None:
            errors.append("Closure must identify closure_level")
        elif level.group(1) in {"completed", "ready", "locally_verified", "docs_static_verified", "implemented_locally_verified"}:
            if verdict is None or verdict.group(1) != "closed_allowed":
                errors.append("unreviewed or partial work cannot claim parent closure")
            if "accepted_gap" in fields.get("Docs impact", ""):
                errors.append("accepted docs gap cannot close the parent")
    return errors


def validate_control_plane(
    root: Path, *, mode: str = "structural", receipts: dict[str, Any] | None = None,
    required_documents: list[str] | None = None,
) -> dict[str, Any]:
    """Structural compatibility is explicit; semantic mode never infers acceptance."""
    from product_agent_os.control_plane_documents import document_readiness

    if mode not in {"structural", "semantic"}:
        raise ValueError("unsupported control-plane validation mode")
    required = list(CONTROL_PLANE_FILES) if required_documents is None else required_documents
    if not required or any(name not in CONTROL_PLANE_FILES for name in required):
        raise ValueError("explicit known document scope required")
    missing = [name for name in required if not (root / name).is_file()]
    result: dict[str, Any] = {"ok": not missing, "missing": missing, "mode": mode}
    if mode == "semantic":
        documents = {}
        for name in required:
            if name in missing:
                documents[name] = {"state": "missing", "errors": ["regular file required"]}
                continue
            try:
                text = (root / name).read_bytes().decode("utf-8")
                documents[name] = document_readiness(name, text, (receipts or {}).get(name))
            except (OSError, UnicodeError) as exc:
                documents[name] = {"state": "unreadable", "errors": [type(exc).__name__]}
        result["documents"] = documents
        result["ok"] = all(doc["state"] in {"draft", "reviewed", "accepted"} for doc in documents.values())
        result["claim_ceiling"] = "content_complete_not_owner_acceptance"
    return result


def validate_agent_file(
    path: Path,
    *,
    available_prompt_paths: set[str] | None = None,
) -> list[str]:
    """Check PAOS role policy and the supported custom-agent configuration surface."""
    text, error = read_utf8_text(path)
    if error:
        return [error]
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid toml: {exc}"]
    errors: list[str] = []
    for field in AGENT_REQUIRED_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing required field: {field}")
    for field in sorted(AGENT_FORBIDDEN_TOP_LEVEL_FIELDS):
        if field in data:
            errors.append(f"unsupported top-level agent metadata field: {field}")
    errors.extend(_parent_only_agent_errors(data))
    instructions = data.get("developer_instructions")
    if isinstance(instructions, str) and instructions.strip():
        lowered = instructions.lower()
        for expected in ["ownership", "inputs", "outputs", "stop conditions", "handoff"]:
            if expected not in lowered:
                errors.append(f"developer_instructions missing agent contract term: {expected}")
        if len(instructions) > AGENT_MAX_INSTRUCTION_CHARS:
            errors.append(
                "developer_instructions exceed prompt budget: "
                f"{len(instructions)} > {AGENT_MAX_INSTRUCTION_CHARS} characters"
            )
        if AGENT_PHASE_IDENTIFIER_PATTERN.search(instructions):
            errors.append("developer_instructions contain volatile phase identifier")
        errors.extend(
            _validate_agent_prompt_paths(
                path,
                instructions,
                available_prompt_paths=available_prompt_paths,
            )
        )
    model = data.get("model")
    if model is not None and model not in AGENT_ALLOWED_MODELS:
        errors.append(f"unsupported agent model: {model}")
    effort = data.get("model_reasoning_effort")
    if effort is not None and effort not in AGENT_ALLOWED_REASONING_EFFORTS:
        errors.append(f"unsupported model_reasoning_effort: {effort}")
        if model in AGENT_ALLOWED_MODELS:
            errors.append(f"unsupported model_reasoning_effort for {model}: {effort}")
    errors.extend(_validate_agent_capabilities(data))
    return errors


def _parent_only_agent_errors(data: dict[str, Any]) -> list[str]:
    return [f"parent-only agent setting: {key}" for key in sorted(AGENT_PARENT_ONLY_FIELDS & data.keys())]


def _validate_agent_capabilities(data: dict[str, Any]) -> list[str]:
    """Custom agents may reduce inherited capabilities, never configure access."""
    errors: list[str] = []
    features = data.get("features", {})
    if not isinstance(features, dict):
        errors.append("custom agent features must be a table")
    else:
        for key, value in features.items():
            if key not in AGENT_DISABLE_FEATURES or value is not False:
                errors.append(f"custom agent feature must disable a supported capability: {key}")
    skills = data.get("skills", {})
    if not isinstance(skills, dict):
        return errors + ["custom agent skills must be a table"]
    configs = skills.get("config", [])
    if not isinstance(configs, list):
        return errors + ["custom agent skills.config must be an array"]
    for config in configs:
        if not isinstance(config, dict):
            errors.append("custom agent skill config must be a table")
            continue
        if config.get("enabled") is not False:
            errors.append("custom agent skills.config may only disable inherited skills")
        if not any(isinstance(config.get(key), str) and config[key].strip() for key in ("path", "name")):
            errors.append("custom agent skill config requires a non-empty path or name")
    for key in skills.keys() - {"config", "bundled", "include_instructions"}:
        errors.append(f"unsupported custom agent skills setting: {key}")
    if "include_instructions" in skills and skills["include_instructions"] is not False:
        errors.append("custom agent skills.include_instructions may only be false")
    if "bundled" in skills and skills["bundled"] != {"enabled": False}:
        errors.append("custom agent skills.bundled may only disable bundled skills")
    return errors


def _project_root_for_agent(path: Path) -> Path | None:
    if path.parent.name == "agents" and path.parent.parent.name == ".codex":
        project_root = path.parent.parent.parent
        has_project_contract = (project_root / "AGENTS.md").exists() or (
            project_root / ".codex" / "config.toml"
        ).exists()
        if has_project_contract:
            return project_root
    return None


def _validate_agent_prompt_paths(
    path: Path,
    instructions: str,
    *,
    available_prompt_paths: set[str] | None = None,
) -> list[str]:
    project_root = _project_root_for_agent(path)
    if project_root is None:
        return []
    errors: list[str] = []
    for match in AGENT_PROMPT_PATH_PATTERN.finditer(instructions):
        relative = match.group("path")
        if "*" in relative:
            continue
        if available_prompt_paths is not None and relative in available_prompt_paths:
            continue
        if not (project_root / relative).exists():
            errors.append(f"referenced prompt path does not exist: {relative}")
    return sorted(set(errors))


def _agent_skill_configs(data: dict[str, Any]) -> list[dict[str, Any]]:
    skills = data.get("skills")
    if not isinstance(skills, dict):
        return []
    configs = skills.get("config")
    if not isinstance(configs, list):
        return []
    return [item for item in configs if isinstance(item, dict) and item.get("enabled", True)]


def _validate_parent_skills_and_mcp(data: dict[str, Any]) -> list[str]:
    """Validate declared parent routes; this does not prove effective tool access."""
    errors: list[str] = []
    project_skill_texts: list[str] = []
    has_openai_docs = False
    for config in _agent_skill_configs(data):
        raw_path = config.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            errors.append("skill config path must be a non-empty string")
            continue
        normalized = raw_path.replace("\\", "/").lower()
        has_openai_docs = has_openai_docs or normalized.endswith(OPENAI_DOCS_SKILL_SUFFIX)
        skill_path = Path(raw_path)
        if not skill_path.is_file():
            errors.append(f"skill path does not exist: {raw_path}")
            continue
        if PROJECT_SKILL_PATH_FRAGMENT in normalized:
            text, error = read_utf8_text(skill_path)
            if error:
                errors.append(f"unable to inspect project skill: {raw_path}")
            else:
                project_skill_texts.append(text.lower())
    mcp_servers = data.get("mcp_servers")
    if has_openai_docs:
        if not isinstance(mcp_servers, dict) or not isinstance(
            mcp_servers.get("openaiDeveloperDocs"),
            dict,
        ):
            errors.append("parent openai-docs skill requires openaiDeveloperDocs MCP server")
        elif mcp_servers["openaiDeveloperDocs"].get("enabled") is False or mcp_servers["openaiDeveloperDocs"].get("url") != "https://developers.openai.com/mcp":
            errors.append("parent openaiDeveloperDocs must enable the official documentation endpoint")
    if data.get("default_permissions") == ":workspace" and project_skill_texts:
        if not any(WORKSPACE_APPLY_AUTHORITY in text for text in project_skill_texts):
            errors.append(
                "parent workspace skills lack explicit task write authority"
            )
    return errors


def validate_agent_project_config(config_path: Path, agent_files: list[Path] | None = None) -> list[str]:
    """Enforce the PAOS parent policy without claiming to resolve all config layers."""
    text, error = read_utf8_text(config_path)
    if error:
        return [error]
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid toml: {exc}"]
    errors: list[str] = []
    agent_files = agent_files or []
    for agent_path in agent_files:
        agent_text, agent_error = read_utf8_text(agent_path)
        if agent_error:
            errors.append(f"{agent_path.name}: {agent_error}")
            continue
        try:
            agent_data = tomllib.loads(agent_text)
        except tomllib.TOMLDecodeError:
            errors.append(f"{agent_path.name}: invalid toml")
            continue
        errors.extend(f"{agent_path.name}: {e}" for e in _parent_only_agent_errors(agent_data))
    has_profiles = "default_permissions" in data or "permissions" in data
    has_legacy = "sandbox_mode" in data or "sandbox_workspace_write" in data
    if has_profiles and has_legacy:
        errors.append("permission profiles and legacy sandbox_mode must not be composed")
    if has_legacy:
        errors.append("PAOS parent config must not contain legacy sandbox settings")
    if data.get("default_permissions") != ":workspace":
        errors.append("PAOS parent config must set default_permissions = :workspace")
    agents = data.get("agents")
    if not isinstance(agents, dict):
        errors.append("project config missing [agents] table")
        return errors
    if agents.get("default_subagent_model") != "gpt-6.1-sol":
        errors.append("generic subagents must default to gpt-6.1-sol")
    if agents.get("default_subagent_reasoning_effort") != "medium":
        errors.append("generic subagents must default to medium reasoning")
    errors.extend(_validate_parent_skills_and_mcp(data))
    return errors


def read_utf8_text(path: Path) -> tuple[str, str | None]:
    try:
        if not path.exists():
            return "", "file does not exist"
        return path.read_text(encoding="utf-8"), None
    except (OSError, UnicodeDecodeError):
        return "", READ_TEXT_ERROR


def is_forbidden_secret_assignment(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped or stripped.startswith(("#", "//", ";")):
        return False
    match = SECRET_ENVIRON_PATTERN.match(line) or SECRET_ASSIGNMENT_PATTERN.match(line)
    if not match:
        return False
    if not SECRET_NAME_PATTERN.search(match.group("name")):
        return False
    value = match.group("value").strip()
    if not value or value.startswith(("$", "{{", "<")):
        return False
    if SAFE_ENV_LOOKUP_PATTERN.match(value):
        return False
    return True


def validate_hook_file(path: Path) -> list[str]:
    text, error = read_utf8_text(path)
    if error:
        return [error]
    errors: list[str] = []
    if any(is_forbidden_secret_assignment(line) for line in text.splitlines()):
        errors.append("contains forbidden secret-like literal")
    if path.name == "hooks.json":
        errors.extend(validate_hook_json_text(text))
    return errors


def validate_hook_json_text(text: str) -> list[str]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [f"invalid json: {exc}"]
    if not isinstance(data, dict):
        return ["hook json must be an object"]
    hook_events = data.get("hooks", data)
    if not isinstance(hook_events, dict):
        return ["hook json hooks must be an object"]
    errors: list[str] = []
    for event in HOOK_JSON_REQUIRED_EVENTS:
        value = hook_events.get(event)
        if value is None:
            errors.append(f"missing hook event: {event}")
            continue
        if not isinstance(value, list):
            errors.append(f"hook event must be a list: {event}")
            continue
        for index, group in enumerate(value):
            if not isinstance(group, dict):
                errors.append(f"hook event group must be an object: {event}[{index}]")
                continue
            commands = group.get("hooks")
            if not isinstance(commands, list) or not commands:
                errors.append(f"hook event group hooks must be a non-empty list: {event}[{index}]")
                continue
            for hook_index, hook in enumerate(commands):
                if not isinstance(hook, dict):
                    errors.append(f"hook command must be an object: {event}[{index}].hooks[{hook_index}]")
                    continue
                if hook.get("type") != "command":
                    errors.append(f"hook command type must be command: {event}[{index}].hooks[{hook_index}]")
                command = hook.get("command")
                if not isinstance(command, str) or not command.strip():
                    errors.append(f"hook command must be a non-empty string: {event}[{index}].hooks[{hook_index}]")
    return errors


def validate_task_matrix_file(path: Path) -> list[str]:
    text, error = read_utf8_text(path)
    if error:
        return [error]
    return validate_task_matrix_text(text)


def validate_task_matrix_text(text: str) -> list[str]:
    tasks = _parse_task_matrix_tasks(text)
    if not tasks:
        return ["no detailed task blocks found"]

    errors: list[str] = []
    for task in tasks:
        errors.extend(_validate_task_matrix_task(task))
    return errors


def _parse_task_matrix_tasks(text: str) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    section = "fields"
    for line in text.splitlines():
        heading = TASK_HEADING_PATTERN.match(line)
        if heading:
            current = {
                "id": heading.group("id").strip(),
                "fields": {},
                "completion": {},
                "raw": [line],
            }
            tasks.append(current)
            section = "fields"
            continue
        if current is None:
            continue
        current["raw"].append(line)
        if line.strip().lower() == "#### completion report":
            section = "completion"
            continue
        field = TASK_FIELD_PATTERN.match(line)
        if not field:
            continue
        name = field.group("name").strip()
        value = field.group("value").strip()
        target = current["completion"] if section == "completion" else current["fields"]
        target[name.lower()] = value
    return tasks


def _validate_task_matrix_task(task: dict[str, Any]) -> list[str]:
    task_id = _task_matrix_task_id(task)
    errors: list[str] = []
    fields = task["fields"]
    completion = task["completion"]

    if _contains_task_matrix_placeholder("\n".join(task["raw"])):
        errors.append(f"{task_id}: unresolved placeholder in task block")

    for field in TASK_MATRIX_REQUIRED_FIELDS:
        if field.lower() not in fields:
            errors.append(f"{task_id}: missing required field: {field}")

    for field in TASK_MATRIX_COMPLETION_FIELDS:
        if field.lower() not in completion:
            errors.append(f"{task_id}: missing completion report field: {field}")

    status = _normalize_task_matrix_status(fields.get("status", ""))
    completion_status = _normalize_task_matrix_status(completion.get("status", ""))
    if status and status not in TASK_MATRIX_ALLOWED_STATUSES:
        errors.append(f"{task_id}: invalid status: {fields.get('status', '')}")
    if completion_status and completion_status != status:
        errors.append(f"{task_id}: completion report status must match task status")
    if fields.get("schema version") and fields["schema version"] != TASK_MATRIX_SCHEMA_VERSION:
        errors.append(f"{task_id}: schema version must be {TASK_MATRIX_SCHEMA_VERSION}")
    if fields.get("timezone") and fields["timezone"] != "Europe/Moscow":
        errors.append(f"{task_id}: timezone must be Europe/Moscow")
    if fields.get("validator target") and "detailed task blocks" not in fields["validator target"].lower():
        errors.append(f"{task_id}: validator target must be detailed task blocks")

    task_timestamp = fields.get("date and time of task implementation", "")
    completion_timestamp = completion.get("actual implementation date and time", "")
    if status == "planned":
        if task_timestamp != "pending_execution_timestamp":
            errors.append(f"{task_id}: planned requires pending_execution_timestamp")
        if TASK_TIMESTAMP_PATTERN.match(completion_timestamp):
            errors.append(f"{task_id}: planned rows must not contain actual implementation date/time")
    if status == "implemented":
        if not TASK_TIMESTAMP_PATTERN.match(task_timestamp):
            errors.append(f"{task_id}: implemented requires actual DD-MM-YYYY HH:mm timestamp")
        if not TASK_TIMESTAMP_PATTERN.match(completion_timestamp):
            errors.append(f"{task_id}: implemented completion report requires actual DD-MM-YYYY HH:mm timestamp")
        for field in [
            "what was done",
            "files touched / work locations",
            "technical value delivered",
            "product value delivered",
            "verification evidence",
            "residual risks",
            "follow-up",
        ]:
            value = completion.get(field, "")
            if not value or value.lower() in {"pending", "n/a", "none"}:
                errors.append(f"{task_id}: implemented requires {field}")
        evidence = completion.get("verification evidence", "").lower()
        if "inspection-only" in evidence or "inspection only" in evidence:
            errors.append(f"{task_id}: implemented cannot use inspection-only verification evidence")
    return errors


def _task_matrix_task_id(task: dict[str, Any]) -> str:
    if _contains_task_matrix_placeholder(task["id"]):
        return task["id"]
    return task["fields"].get("task") or task["id"]


def _normalize_task_matrix_status(value: str) -> str:
    return value.strip().strip("`").lower()


def _contains_task_matrix_placeholder(value: str) -> bool:
    return bool(TASK_PLACEHOLDER_PATTERN.search(value))


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("ok") else 1


def main_control_plane(argv: list[str]) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Validate explicit document scope; structural mode is legacy compatibility.")
    parser.add_argument('workspace', nargs='?', default='.')
    parser.add_argument('--semantic', action='store_true')
    parser.add_argument('--document', action='append', choices=CONTROL_PLANE_FILES,
                        help='Applicable canonical document; repeat to match the staged selection.')
    args = parser.parse_args(argv)
    root = Path(args.workspace)
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "missing": CONTROL_PLANE_FILES,
                "errors": ["workspace does not exist"],
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "missing": CONTROL_PLANE_FILES,
                "errors": ["workspace is not a directory"],
            }
        )
    result = validate_control_plane(root, mode="semantic" if args.semantic else "structural",
                                    required_documents=args.document)
    result["root"] = str(root)
    result["errors"] = []
    return print_json(result)


def main_agents(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_agents.py [agents-dir]")
        return 0
    root = Path(argv[0]) if argv else Path(".codex/agents")
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["agent directory does not exist"],
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["agent path is not a directory"],
            }
        )
    files = sorted(root.glob("*.toml"))
    file_errors = {str(path): validate_agent_file(path) for path in files}
    errors = ["no agent TOML files found"] if not files else []
    config_path = root.parent / "config.toml"
    config_errors = validate_agent_project_config(config_path, files) if config_path.exists() else []
    ok = (
        bool(files)
        and not errors
        and not config_errors
        and all(not item for item in file_errors.values())
    )
    return print_json(
        {
            "ok": ok,
            "root": str(root),
            "files": [str(path) for path in files],
            "errors": errors,
            "config_errors": config_errors,
            "file_errors": file_errors,
        }
    )


def main_hooks(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_hooks.py [hooks-dir]")
        return 0
    root = Path(argv[0]) if argv else Path(".codex/hooks")
    if not root.exists():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["hook directory does not exist"],
            }
        )
    if root.is_file():
        file_errors = {str(root): validate_hook_file(root)}
        ok = not file_errors[str(root)]
        return print_json(
            {
                "ok": ok,
                "root": str(root),
                "files": [str(root)],
                "errors": [],
                "file_errors": file_errors,
            }
        )
    if not root.is_dir():
        return print_json(
            {
                "ok": False,
                "root": str(root),
                "files": [],
                "errors": ["hook path is not a directory"],
            }
        )
    files = sorted(path for path in root.iterdir() if path.is_file())
    file_errors = {str(path): validate_hook_file(path) for path in files}
    errors = ["no hook files found"] if not files else []
    ok = bool(files) and all(not item for item in file_errors.values())
    return print_json(
        {
            "ok": ok,
            "root": str(root),
            "files": [str(path) for path in files],
            "errors": errors,
            "file_errors": file_errors,
        }
    )


def main_task_matrix(argv: list[str]) -> int:
    if any(arg in {"-h", "--help"} for arg in argv):
        print("usage: validate_task_matrix.py <task-matrix-file>")
        return 0
    if not argv:
        return print_json(
            {
                "ok": False,
                "path": "",
                "schema_version": TASK_MATRIX_SCHEMA_VERSION,
                "errors": ["task matrix path is required"],
            }
        )
    path = Path(argv[0])
    errors = validate_task_matrix_file(path)
    return print_json(
        {
            "ok": not errors,
            "path": str(path),
            "schema_version": TASK_MATRIX_SCHEMA_VERSION,
            "errors": errors,
        }
    )
