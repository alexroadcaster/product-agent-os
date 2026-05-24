from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from codex_runtime_runner.redaction import validate_redaction
from product_agent_os.behavioral_evals import validate_behavioral_eval_template


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BEHAVIORAL_TEMPLATE = PLUGIN_ROOT / "assets" / "templates" / "evals" / "behavioral-workflows.json"
DEFAULT_TRANSCRIPT_FIXTURE = (
    PLUGIN_ROOT
    / "assets"
    / "eval-fixtures"
    / "transcripts"
    / "product-agent-os-synthetic-sessions.json"
)
EXTRA_SECRET_MARKERS = ("sk-", "BEGIN PRIVATE KEY")


def evaluate_transcript_sessions(
    transcript_path: str | Path,
    behavioral_template_path: str | Path = DEFAULT_BEHAVIORAL_TEMPLATE,
) -> dict[str, Any]:
    transcript = Path(transcript_path)
    template = Path(behavioral_template_path)
    errors: list[str] = []

    data = _read_json(transcript, "transcript", errors)
    template_data = _read_json(template, "behavioral_template", errors)
    cases = _case_index(template_data) if isinstance(template_data, dict) else {}

    if isinstance(template_data, dict):
        template_report = validate_behavioral_eval_template(template)
        if template_report.get("status") != "ok":
            errors.append("behavioral_template:needs_review")

    sessions = data.get("sessions") if isinstance(data, dict) else None
    if not isinstance(data, dict):
        errors.append("transcript:object_required")
        sessions = []
    elif data.get("synthetic") is not True:
        errors.append("transcript:synthetic_required")

    if not isinstance(sessions, list) or not sessions:
        errors.append("sessions:non_empty_list_required")
        sessions = []

    results = [_evaluate_session(index, session, cases) for index, session in enumerate(sessions)]
    failed = [result for result in results if result["status"] != "ok"]
    status = "ok" if not errors and not failed else "failed"
    return {
        "ok": status == "ok",
        "status": status,
        "transcript": transcript.name,
        "behavioral_template": template.name,
        "session_count": len(results),
        "summary": {
            "passed": len(results) - len(failed),
            "failed": len(failed),
        },
        "errors": sorted(set(errors)),
        "results": results,
    }


def _read_json(path: Path, label: str, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{label}:file_not_found")
    except json.JSONDecodeError:
        errors.append(f"{label}:invalid_json")
    except OSError:
        errors.append(f"{label}:read_failed")
    return {}


def _case_index(template_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cases = template_data.get("cases", [])
    if not isinstance(cases, list):
        return {}
    return {
        str(case.get("name")): case
        for case in cases
        if isinstance(case, dict) and isinstance(case.get("name"), str)
    }


def _evaluate_session(index: int, session: Any, cases: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(session, dict):
        return _session_result(f"session-{index}", "", ["session:object_required"])

    session_id = str(session.get("id") or f"session-{index}")
    case_name = str(session.get("behavioral_case") or session.get("behavioral_case_id") or "")
    schema_errors: list[str] = []
    if session.get("source") != "synthetic":
        schema_errors.append("session:synthetic_source_required")
    if not case_name:
        schema_errors.append("behavioral_case:required")
    elif case_name not in cases:
        schema_errors.append("behavioral_case:unknown")

    messages = session.get("messages", [])
    if not isinstance(messages, list) or not messages:
        schema_errors.append("messages:non_empty_list_required")
        messages = []

    assistant_text = "\n".join(
        str(message.get("content", ""))
        for message in messages
        if isinstance(message, dict) and message.get("role") == "assistant"
    )
    message_text = "\n".join(
        str(message.get("content", ""))
        for message in messages
        if isinstance(message, dict)
    )
    full_session_text = json.dumps(session, sort_keys=True)
    expected_terms = _string_list(session.get("expected_terms"))
    if not expected_terms:
        schema_errors.append("expected_terms:non_empty_list_required")

    case = cases.get(case_name, {})
    case_forbidden = _string_list(case.get("forbidden")) if isinstance(case, dict) else []
    forbidden_terms = _dedupe([*case_forbidden, *_string_list(session.get("forbidden_terms"))])

    assistant_text_lower = assistant_text.lower()
    missing_expected_terms = [
        term for term in expected_terms if term.lower() not in assistant_text_lower
    ]
    forbidden_terms_present = [
        term for term in forbidden_terms if term.lower() in assistant_text_lower
    ]
    privacy_errors = _privacy_errors(f"{message_text}\n{full_session_text}")
    status = (
        "ok"
        if not schema_errors and not missing_expected_terms and not forbidden_terms_present and not privacy_errors
        else "failed"
    )

    return _session_result(
        session_id,
        case_name,
        schema_errors,
        status=status,
        message_count=len(messages),
        missing_expected_terms=missing_expected_terms,
        forbidden_terms_present=forbidden_terms_present,
        privacy_errors=privacy_errors,
    )


def _session_result(
    session_id: str,
    case_name: str,
    schema_errors: list[str],
    *,
    status: str = "failed",
    message_count: int = 0,
    missing_expected_terms: list[str] | None = None,
    forbidden_terms_present: list[str] | None = None,
    privacy_errors: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": session_id,
        "behavioral_case": case_name,
        "status": status,
        "message_count": message_count,
        "schema_errors": sorted(set(schema_errors)),
        "missing_expected_terms": missing_expected_terms or [],
        "forbidden_terms_present": forbidden_terms_present or [],
        "privacy_errors": privacy_errors or [],
    }


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str) and item.strip()]


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _privacy_errors(text: str) -> list[str]:
    errors = validate_redaction(text)
    if any(marker in text for marker in EXTRA_SECRET_MARKERS):
        errors.append("redaction:secret_marker_retained")
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay Product-Agent OS transcript/session eval fixtures.")
    parser.add_argument("transcript", nargs="?", default=str(DEFAULT_TRANSCRIPT_FIXTURE))
    parser.add_argument("--behavioral-template", default=str(DEFAULT_BEHAVIORAL_TEMPLATE))
    args = parser.parse_args(argv)

    report = evaluate_transcript_sessions(args.transcript, args.behavioral_template)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
