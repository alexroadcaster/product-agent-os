"""Attest one G7 inference request from the local Codex 0.167 trace."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

MODEL = "gpt-6.1-sol"
EFFORT = "medium"
PREFLIGHT_PROMPT = "Synthetic G7 trace preflight. Return G7_TRACE_OK as plain text."
MAX_TRACE_BYTES = 8 * 1024 * 1024
MAX_TRACE_EVENTS = 2048
_LIFECYCLE_EVENTS = {
    "rollout_started", "rollout_ended", "thread_started", "thread_ended",
    "codex_turn_started", "codex_turn_ended", "inference_started",
    "inference_completed", "history_item_accepted", "protocol_event_observed",
    "recording_completed",
}
_TOOL_EVENTS = {
    "tool_call_started", "tool_call_runtime_started", "tool_call_runtime_ended",
    "tool_call_ended", "mcp_tool_call_correlation_assigned", "stdin_target_resolved",
    "code_cell_started", "code_cell_initial_response", "code_cell_ended",
}


class TraceReceiptError(ValueError):
    """The trace cannot support a complete receipt."""


def _sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     allow_nan=False).encode("utf-8")).hexdigest()


def _read(root: Path, relative: str) -> bytes:
    path = root / relative
    try:
        if path.resolve(strict=True) != path or not path.is_file():
            raise TraceReceiptError("unsafe_trace_path")
        with path.open("rb") as source:
            content = source.read(MAX_TRACE_BYTES + 1)
    except (OSError, RuntimeError) as error:
        raise TraceReceiptError("missing_trace_file") from error
    if len(content) > MAX_TRACE_BYTES:
        raise TraceReceiptError("trace_size_limit")
    return content


def _load(content: bytes) -> dict[str, Any]:
    """Reject ambiguous JSON before using any field as evidence."""
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        for key, value in pairs:
            if key in fields:
                raise TraceReceiptError("duplicate_json_field")
            fields[key] = value
        return fields

    def invalid_constant(_: str) -> None:
        raise TraceReceiptError("invalid_trace_json")

    try:
        parsed = json.loads(content, object_pairs_hook=unique, parse_constant=invalid_constant)
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise TraceReceiptError("invalid_trace_json") from error
    if not isinstance(parsed, dict):
        raise TraceReceiptError("invalid_trace_object")
    return parsed


def _bundle(trace_root: Path) -> tuple[Path, dict[str, Any], list[dict[str, Any]]]:
    """Check that a complete, single-thread recording belongs to this probe."""
    try:
        root = trace_root.resolve(strict=True)
        bundles = list(root.iterdir())
    except OSError as error:
        raise TraceReceiptError("missing_trace_bundle") from error
    if (len(bundles) != 1 or not bundles[0].name.startswith("trace-")
            or bundles[0].resolve() != bundles[0] or not bundles[0].is_dir()):
        raise TraceReceiptError("expected_one_trace_bundle")
    bundle = bundles[0]
    manifest = _load(_read(bundle, "manifest.json"))
    if (manifest.get("schema_version") != 2 or manifest.get("raw_event_log") != "trace.jsonl"
            or manifest.get("payloads_dir") != "payloads"
            or not all(isinstance(manifest.get(key), str) and manifest[key]
                       for key in ("trace_id", "rollout_id", "root_thread_id"))
            or bundle.name != f"trace-{manifest['trace_id']}-{manifest['root_thread_id']}"):
        raise TraceReceiptError("unsupported_trace_manifest")
    log = _read(bundle, "trace.jsonl")
    rows = log.splitlines()
    if not log.endswith(b"\n") or not rows or len(rows) > MAX_TRACE_EVENTS:
        raise TraceReceiptError("incomplete_recording")
    events = []
    for seq, row in enumerate(rows, 1):
        event = _load(row)
        payload = event.get("payload")
        if (event.get("schema_version") != 2 or type(event.get("seq")) is not int
                or event["seq"] != seq or event.get("rollout_id") != manifest["rollout_id"]
                or event.get("thread_id") not in (None, manifest["root_thread_id"])
                or not isinstance(payload, dict) or not isinstance(payload.get("type"), str)):
            raise TraceReceiptError("trace_sequence_or_thread")
        events.append(payload)
    if (events[-1]["type"] != "recording_completed"
            or sum(event["type"] == "recording_completed" for event in events) != 1):
        raise TraceReceiptError("incomplete_recording")
    return bundle, manifest, events


def _payload(bundle: Path, reference: Any, expected_kind: str) -> dict[str, Any]:
    if not isinstance(reference, dict):
        raise TraceReceiptError("invalid_payload_reference")
    path = reference.get("path")
    match = re.fullmatch(r"payloads/([1-9][0-9]*)\.json", path) if isinstance(path, str) else None
    if (match is None or reference.get("kind") != {"type": expected_kind}
            or reference.get("raw_payload_id") != f"raw_payload:{match[1]}"):
        raise TraceReceiptError("invalid_payload_reference")
    return _load(_read(bundle, path))


def _inference(
    events: list[dict[str, Any]], manifest: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    def one(kind: str) -> tuple[int, dict[str, Any]]:
        matching = [(index, event) for index, event in enumerate(events) if event["type"] == kind]
        if len(matching) != 1:
            raise TraceReceiptError("expected_one_" + kind)
        return matching[0]

    rollout_index, rollout = one("rollout_started")
    thread_index, thread = one("thread_started")
    turn_index, turn = one("codex_turn_started")
    start_index, start = one("inference_started")
    end_index, end = one("inference_completed")
    turn_end_index, turn_end = one("codex_turn_ended")
    turn_id, call_id = turn.get("codex_turn_id"), start.get("inference_call_id")
    root_thread = manifest["root_thread_id"]
    if (not rollout_index == 0 < thread_index < turn_index < start_index < end_index < turn_end_index
            or rollout.get("trace_id") != manifest["trace_id"]
            or rollout.get("root_thread_id") != root_thread
            or any(event.get("thread_id") != root_thread for event in (thread, turn, start))
            or not isinstance(turn_id, str) or not turn_id
            or start.get("codex_turn_id") != turn_id or turn_end.get("codex_turn_id") != turn_id
            or turn_end.get("status") != "completed"
            or not isinstance(call_id, str) or not call_id or end.get("inference_call_id") != call_id):
        raise TraceReceiptError("inference_binding")
    return start, end


def _request_parts(
    request: dict[str, Any], expected_prompt: str
) -> tuple[list[Any], list[Any], list[dict[str, Any]]]:
    """Bind the intended input and account for both Responses tool encodings."""
    if any(request.get(key) is not None for key in ("previous_response_id", "conversation", "prompt")):
        raise TraceReceiptError("incremental_request")
    if request.get("type") not in (None, "response.create") or request.get("generate") is False:
        raise TraceReceiptError("unsupported_request")
    tools, items = request.get("tools", []), request.get("input")
    if not isinstance(tools, list) or not isinstance(items, list):
        raise TraceReceiptError("missing_request_context")
    additional_tools: list[Any] = []
    common: list[dict[str, Any]] = []
    prompt_count = 0
    for item in items:
        if not isinstance(item, dict):
            raise TraceReceiptError("unsupported_input_item")
        if item.get("type") == "additional_tools":
            if not isinstance(item.get("tools"), list):
                raise TraceReceiptError("missing_additional_tools")
            additional_tools.extend(item["tools"])
            continue
        role, content = item.get("role"), item.get("content")
        if (item.get("type") != "message" or role not in ("system", "developer", "user")
                or not isinstance(content, list) or not content
                or any(not isinstance(part, dict) or part.get("type") != "input_text"
                       or not isinstance(part.get("text"), str) for part in content)):
            raise TraceReceiptError("unsupported_input_item")
        if role == "user" and len(content) == 1 and content[0]["text"] == expected_prompt:
            prompt_count += 1
        else:
            common.append({key: value for key, value in item.items() if key != "id"})
    if prompt_count != 1:
        raise TraceReceiptError("prompt_binding")
    return tools, additional_tools, common


def _matches_marker(value: Any, markers: tuple[str, ...]) -> bool:
    if isinstance(value, str):
        text = value.replace("\\", "/").casefold()
        return any(marker in text for marker in markers)
    if isinstance(value, list):
        return any(_matches_marker(item, markers) for item in value)
    if isinstance(value, dict):
        return any(_matches_marker(item, markers) for pair in value.items() for item in pair)
    return False


def _tool_inventory(tools: list[Any]) -> dict[str, Any]:
    """Keep tool identity metadata only; never tool descriptions, arguments or context."""
    public = {"apply_patch", "exec_command", "write_stdin", "shell", "shell_command",
              "request_user_input", "request_user_input_async", "update_plan", "view_image",
              "sleep", "time", "curr_time", "web", "search_query", "spawn_agent", "send_message",
              "exec", "wait", "js_reset", "js_add_node_module_dir", "parallel", "multi_tool_use", "list_mcp_resources", "list_mcp_resource_templates",
              "read_mcp_resource", "request_permissions", "imagegen", "js", "create_goal", "update_goal"}
    names, unknown, identifiers = set(), [], []
    leaves = 0
    def visit(tool):
        nonlocal leaves
        if not isinstance(tool, dict):
            unknown.append(_sha256(tool))
            leaves += 1
            return
        children = tool.get("tools")
        if isinstance(children, list):
            for child in children:
                visit(child)
            return
        leaves += 1
        name = tool.get("name") or tool.get("function", {}).get("name")
        if isinstance(name, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.:-]{0,119}", name):
            identifiers.append(name)
        if name in public:
            names.add(name)
        else:
            unknown.append(_sha256(tool))
    for tool in tools:
        visit(tool)
    return {"builtin_tool_names": sorted(names), "leaf_tool_count": leaves,
            "unknown_tool_digests": sorted(unknown), "tool_identifiers": sorted(set(identifiers))}


def common_context_receipt(instructions: Any, common: list[dict], thread_id: str) -> dict:
    """Preserve context except bound marker and Codex transport turn/time metadata.

    Matches Codex v0.167 responses_lite.rs comparison: provenance stays intact.
    Raw request/context hashes remain available independently.
    """
    normalized = json.loads(json.dumps(common))
    marker = hashlib.sha256(thread_id.encode()).hexdigest()
    count = 0
    metadata_count = 0
    for item in normalized:
        metadata = item.get("internal_chat_message_metadata_passthrough")
        if isinstance(metadata, dict):
            for key in ("turn_id", "create_time"):
                if key in metadata:
                    value = metadata[key]
                    if (key == "turn_id" and not isinstance(value, str)) or (key == "create_time" and type(value) not in (int, float)):
                        raise TraceReceiptError("invalid_transport_metadata")
                    metadata[key] = "<turn-id>" if key == "turn_id" else 0.0
                    metadata_count += 1
        if item.get("role") != "developer":
            continue
        for part in item.get("content", []):
            text = part.get("text", "")
            if "Product-Agent OS startup context:" not in text:
                continue
            pattern = r"(State marker=\.codex/product-agent-os/lifecycle-state\.)" + marker + r"(\.json;)"
            part["text"], replacements = re.subn(pattern, r"\1<session>\2", text)
            count += replacements
    return {"normalized_common_context_sha256": _sha256({"instructions": instructions, "input": normalized}),
            "context_normalization": "bound_marker_transport_v3", "marker_replacements": count,
            "transport_fields_normalized": metadata_count,
            "common_parts": [{"role": item["role"], "sha256": _sha256(item),
                              "keys": sorted(item), "metadata_shape": {key: type(value).__name__ for key, value in item.get("internal_chat_message_metadata_passthrough", {}).items()} if isinstance(item.get("internal_chat_message_metadata_passthrough"), dict) else type(item.get("internal_chat_message_metadata_passthrough")).__name__, "content_sha256": _sha256(item.get("content")),
                              "parts": [{"keys": sorted(part), "text_sha256": _sha256(part.get("text")),
                                         "text_length": len(part.get("text", ""))} for part in item.get("content", [])]}
                             for item in normalized]}


def build_trace_receipt(
    trace_root: Path,
    *,
    expected_prompt: str,
    expected_model: str = MODEL,
    expected_effort: str = EFFORT,
    forbidden_texts: tuple[str, ...] = (),
    include_output: bool = False,
) -> dict[str, Any]:
    """Inspect one local bundle and return a receipt without raw payloads."""
    bundle, manifest, events = _bundle(trace_root)
    start, end = _inference(events, manifest)
    request = _payload(bundle, start.get("request_payload"), "inference_request")
    response = _payload(bundle, end.get("response_payload"), "inference_response")
    tools, additional_tools, common = _request_parts(request, expected_prompt)
    output_items = response.get("output_items")
    if (not isinstance(end.get("response_id"), str) or not end["response_id"]
            or response.get("response_id") != end["response_id"]
            or not isinstance(output_items, list) or not output_items
            or any(not isinstance(item, dict) or not isinstance(item.get("type"), str)
                   for item in output_items)):
        raise TraceReceiptError("response_binding")
    reasons = []
    types = {event["type"] for event in events}
    if types & _TOOL_EVENTS or any(item["type"] not in ("message", "reasoning") for item in output_items):
        reasons.append("tool_activity")
    if types - _LIFECYCLE_EVENTS - _TOOL_EVENTS:
        reasons.append("unsupported_trace_event")
    if tools or additional_tools:
        reasons.append("tools_present")
    if not any(item["type"] == "message" and item.get("role") == "assistant" for item in output_items):
        reasons.append("missing_assistant_message")
    model_ok = request.get("model") == start.get("model") == expected_model
    reasoning = request.get("reasoning")
    effort_ok = isinstance(reasoning, dict) and reasoning.get("effort") == expected_effort
    if not model_ok:
        reasons.append("model_mismatch")
    if not effort_ok:
        reasons.append("effort_mismatch")
    if start.get("provider_name") not in ("openai", "OpenAI"):
        reasons.append("provider_mismatch")
    markers = tuple(text.replace("\\", "/").casefold() for text in forbidden_texts if text)
    if markers and _matches_marker(request, markers):
        reasons.append("hidden_oracle_marker")
    receipt = {
        "schema_version": "g7_codex_trace_receipt_v1",
        "status": "blocked" if reasons else "passed",
        "reasons": reasons,
        "observed_tool_count": len(tools) + len(additional_tools),
        **_tool_inventory(tools + additional_tools),
        "provider_label": start.get("provider_name") if start.get("provider_name") in ("openai", "OpenAI") else "unrecognized",
        "additional_tool_count": len(additional_tools),
        "observed_model": expected_model if model_ok else None,
        "observed_effort": expected_effort if effort_ok else None,
        "request_sha256": _sha256(request),
        "tool_inventory_sha256": _sha256({"tools": tools, "additional_tools": additional_tools}),
        "prompt_sha256": _sha256(expected_prompt),
        "common_context_sha256": _sha256({"instructions": request.get("instructions"), "input": common}),
        **common_context_receipt(request.get("instructions"), common, manifest["root_thread_id"]),
        "forbidden_marker_check": "configured" if markers else "not_configured",
        "filesystem_isolation": "not_established",
        "strict_AB_eligible": False,
    }

    if include_output and not reasons:
        messages = [item for item in output_items if item.get("type") == "message" and item.get("role") == "assistant"]
        content = messages[-1].get("content", [])
        if not content or any(part.get("type") != "output_text" or not isinstance(part.get("text"), str) for part in content):
            raise TraceReceiptError("unsupported_assistant_output")
        output = "".join(part["text"] for part in content)
        if len(output) > 50000:
            raise TraceReceiptError("candidate_size_limit")
        receipt.update(candidate=output, candidate_sha256=hashlib.sha256(output.encode()).hexdigest())
    return receipt


def _oracle_markers(root: Path) -> tuple[str, ...]:
    relative = "tests/fixtures/product_agent_os/g7-code-quality-evolution"
    corpus = root / relative
    manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
    return (relative, "tests/fixtures/product_agent_os/g7-pressure",
            "def check(candidate):", "def check_batch(candidate):",
            "callback_must_observe_uncommitted_state", "duplicate_must_not_charge_or_notify",
            "failed_notification_must_not_commit", "batch_reuse_contract", *(
        step["oracle"] for chain in manifest["future_generation_chains"] for step in chain["steps"]
    ))


def _blocked(reason: str, call_started: bool = False) -> dict[str, Any]:
    return {"schema_version": "g7_codex_trace_receipt_v1", "status": "blocked",
            "reasons": [reason], "preflight_call_started": call_started,
            "strict_AB_eligible": False}


def _recorded_inference_starts(trace_root: Path) -> int | None:
    """Count started records on failure without treating an incomplete trace as evidence of absence."""
    try:
        bundles = list(trace_root.iterdir())
        if not bundles:
            return 0
        if len(bundles) != 1 or not bundles[0].name.startswith("trace-") or not bundles[0].is_dir():
            return None
        if bundles[0].resolve() != bundles[0]:
            return None
        rows = _read(bundles[0], "trace.jsonl").splitlines()
        if len(rows) > MAX_TRACE_EVENTS:
            return None
        count = 0
        for row in rows:
            payload = _load(row).get("payload")
            if not isinstance(payload, dict):
                return None
            count += payload.get("type") == "inference_started"
        return count
    except (OSError, TraceReceiptError):
        return None


def _process_diagnostics(trace_root: Path, stderr: bytes | None, exit_code: int | None) -> dict[str, Any]:
    """Reduce sensitive child output to bounded flags and a local event count."""
    diagnostic = (stderr or b"")[:MAX_TRACE_BYTES].lower()
    return {
        "exit_code": exit_code,
        "permission_denied": any(token in diagnostic for token in (
            b"access is denied", b"permission denied", b"os error 5",
        )),
        "configuration_error": any(token in diagnostic for token in (
            b"error loading configuration", b"failed to load config",
            b"error parsing configuration", b"invalid config",
        )),
        "inference_starts_observed": _recorded_inference_starts(trace_root),
    }


def configuration_overrides(disabled_mcp: tuple[str, ...], catalog: Path | None) -> list[str]:
    """Build capability reductions without changing durable configuration or protections."""
    overrides = [
        'model_reasoning_effort="medium"', "features.shell_tool=false", "agents.enabled=false",
        "features.apps=false", "features.goals=false",
        'plugins.unified-computer-use@openai-bundled.mcp_servers.cua_repl.enabled=false', 'web_search="disabled"', "allow_browser_and_computer_use=false",
        "features.computer_use=false", "features.browser_use=false", "features.browser_use_external=false",
        "features.code_mode=false", "features.code_mode_only=false", "features.view_image=false",
        "features.image_generation=false", "features.tool_suggest=false", "features.sleep_tool=false",
        "features.request_permissions_tool=false", "tools.experimental_request_user_input.enabled=false",
        "tools.update_plan.enabled=false", "memories.use_memories=false", "memories.generate_memories=false",
        "skills.include_instructions=false",
    ]
    if catalog is not None:
        overrides.append("model_catalog_json=" + json.dumps(str(catalog)))
    # CLI -c splits dotted keys literally; quoting a segment changes its identity.
    plugin_servers = {
        "cloudflare@openai-curated": ("cloudflare-api",),
        "codex-security@openai-curated": ("codex-security",),
        "github@openai-curated": ("github",),
        "openai-developers@openai-curated": ("openai-api-key-local-confirmation", "openai-api-credit-promo"),
        "openai-developers@openai-curated-remote": ("openai-api-key-local-confirmation", "openai-api-credit-promo"),
        "product-agent-os@personal-product-agent-plugins": ("context7",),
        "codex-app-tools@openai-bundled": ("codex_app",),
    }
    overrides.extend(f"plugins.{plugin}.mcp_servers.{server}.enabled=false"
                     for plugin, servers in plugin_servers.items() for server in servers)
    overrides.extend(f"mcp_servers.{name}.enabled=false"
                     for name in sorted({"openaiDeveloperDocs", *disabled_mcp}))
    return overrides


def run_preflight(root: Path, executable: Path, disabled_mcp: tuple[str, ...] = (), catalog: Path | None = None, *, prompt: str = PREFLIGHT_PROMPT,
                  include_output: bool = False) -> dict[str, Any]:
    """Run one explicitly requested synthetic probe using the existing Codex login."""
    root = root.resolve()
    report_dir = root / ".docs-tools/reports"
    if (report_dir.resolve() != report_dir or not report_dir.is_dir()
            or not executable.is_absolute() or not executable.is_file()):
        return _blocked("invalid_preflight_paths")
    if any(not re.fullmatch(r"[A-Za-z0-9_-]+", name) for name in disabled_mcp):
        return _blocked("invalid_mcp_name")
    env = dict(os.environ)
    if any(env.get(name) for name in ("OPENAI_API_KEY", "CODEX_API_KEY", "AZURE_OPENAI_API_KEY")):
        return _blocked("api_key_environment_present")
    env.pop("CODEX_ROLLOUT_TRACE_ROOT", None)
    started = False
    try:
        markers = _oracle_markers(root)
        command = [str(executable)]
        version = subprocess.run(command + ["--version"], cwd=root, env=env,
                                 capture_output=True, timeout=10, check=False)
        if version.returncode or version.stdout.strip() != b"codex-cli 0.167.0":
            return _blocked("unsupported_codex_version")
        login = subprocess.run(command + ["login", "status"], cwd=root, env=env,
                               capture_output=True, timeout=10, check=False)
        if login.returncode or b"Logged in using ChatGPT" not in (login.stdout + login.stderr).splitlines():
            return _blocked("chatgpt_auth_not_confirmed")

        if catalog is not None:
            catalog = catalog.resolve()
            if not catalog.is_relative_to(report_dir) or not catalog.is_file():
                return _blocked("invalid_catalog_path")
        overrides = configuration_overrides(disabled_mcp, catalog)
        command += ["exec", "--ephemeral", "--json", "--sandbox", "read-only", "--model", MODEL]
        command.extend(arg for override in overrides for arg in ("-c", override))
        with tempfile.TemporaryDirectory(prefix="g7-trace-", dir=report_dir) as temporary:
            trace_root = Path(temporary)
            env["CODEX_ROLLOUT_TRACE_ROOT"] = str(trace_root)
            started = True
            try:
                result = subprocess.run(command + ["-"], cwd=root, env=env, timeout=180, check=False,
                                        input=prompt.encode("utf-8"),
                                        stdout=subprocess.PIPE if include_output else subprocess.DEVNULL, stderr=subprocess.PIPE)
            except subprocess.TimeoutExpired as error:
                return dict(_blocked("preflight_timeout", started),
                            **_process_diagnostics(trace_root, error.stderr, None))
            diagnostics = _process_diagnostics(trace_root, result.stderr, result.returncode)
            if result.returncode:
                return dict(_blocked("codex_preflight_exit_nonzero", started), **diagnostics)
            try:
                receipt = build_trace_receipt(trace_root, expected_prompt=prompt, forbidden_texts=markers, include_output=include_output)
            except TraceReceiptError as error:
                return dict(_blocked(str(error), started), **diagnostics)
            if include_output:
                from run_g7_codex_pilot import collect_events
                observed = collect_events((result.stdout or b"").decode("utf-8"))
                receipt["usage"] = observed["usage"]
                receipt["purpose"] = "generation_only"
            return dict(receipt, preflight_call_started=True, codex_version="0.167.0",
                        auth_mode="chatgpt", configuration_sha256=_sha256(overrides), **diagnostics)
    except subprocess.TimeoutExpired:
        return _blocked("preflight_timeout", started)
    except TraceReceiptError as error:
        return _blocked(str(error), started)
    except (OSError, ValueError, KeyError, TypeError, RecursionError):
        return _blocked("preflight_setup_or_cleanup_failed", started)


def main() -> int:
    """Print only a sanitized receipt after an explicitly opted-in probe."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-preflight", action="store_true", required=True)
    parser.add_argument("--codex-executable", required=True, type=Path)
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--disable-mcp", action="append", default=[])
    args = parser.parse_args()
    receipt = run_preflight(Path(__file__).resolve().parents[3], args.codex_executable, tuple(args.disable_mcp), args.catalog)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
