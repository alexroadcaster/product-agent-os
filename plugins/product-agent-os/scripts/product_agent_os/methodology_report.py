"""Markdown report rendering for Product-Agent OS methodology audits."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PRIORITY_ORDER = {
    "P0_blocker": 0,
    "P1_high_risk": 1,
    "P2_recommended": 2,
    "P3_optional_maturity": 3,
    "not_applicable": 4,
}


def render_methodology_audit_report(audit: dict[str, Any]) -> str:
    """Render a deterministic Markdown report from a methodology audit packet."""

    lines = [
        "# Product-Agent OS Methodology Audit",
        "",
        "Source status: `local audit output`",
        "",
        "## Maturity Level",
        "",
        _classification_line(audit.get("maturity_level", {})),
        "",
        "## Complexity Profile",
        "",
        _classification_line(audit.get("complexity_profile", {})),
        "",
        "## Delivery Map",
        "",
        _json_block(audit.get("delivery_map", {})),
        "",
        "## Methodology Domains",
        "",
        *_domain_lines(audit.get("methodology_domains", [])),
        "",
        "## Recommendations",
        "",
        *_recommendation_lines(audit.get("recommendations", [])),
        "",
        "## Questions For Owner",
        "",
        *_list_lines(audit.get("questions_for_owner", [])),
        "",
        "## Provisional Assumptions",
        "",
        *_list_lines(audit.get("provisional_assumptions", [])),
        "",
        "## Approval Boundaries",
        "",
        *_list_lines(_approval_boundaries(audit.get("recommendations", []))),
        "",
        "## Safe Next Action",
        "",
        str(audit.get("safe_next_action", "none")),
        "",
        "## Residual Risks",
        "",
        *_list_lines(_residual_risks(audit.get("recommendations", []))),
        "",
    ]
    return _redact("\n".join(lines))


def _classification_line(packet: Any) -> str:
    if not isinstance(packet, dict):
        return "- selected: unknown\n- confidence: unknown\n- reasons: none"
    selected = packet.get("selected", "unknown")
    confidence = packet.get("confidence", "unknown")
    reasons = packet.get("reasons", [])
    reason_text = ", ".join(str(item) for item in reasons) if reasons else "none"
    return f"- selected: {selected}\n- confidence: {confidence}\n- reasons: {reason_text}"


def _domain_lines(domains: Any) -> list[str]:
    if not isinstance(domains, list) or not domains:
        return ["- none"]
    return [
        f"- `{domain.get('id', 'unknown')}`: {domain.get('status', 'unknown')}"
        for domain in domains
        if isinstance(domain, dict)
    ] or ["- none"]


def _recommendation_lines(recommendations: Any) -> list[str]:
    if not isinstance(recommendations, list) or not recommendations:
        return ["- none"]
    lines: list[str] = []
    for item in sorted(
        (recommendation for recommendation in recommendations if isinstance(recommendation, dict)),
        key=lambda recommendation: (
            PRIORITY_ORDER.get(str(recommendation.get("priority", "not_applicable")), 99),
            str(recommendation.get("domain", "")),
            str(recommendation.get("gate", "")),
        ),
    ):
        lines.append(f"- `{item.get('priority', 'not_applicable')}` `{item.get('domain', 'unknown')}`")
        lines.append(f"  - gate: {item.get('gate', 'unknown')}")
        lines.append(f"  - artifact: {item.get('artifact', 'unknown')}")
        lines.append(f"  - reason: {item.get('reason', 'unknown')}")
        lines.append(f"  - evidence_required: {_format_value(item.get('evidence_required', []))}")
        lines.append(f"  - evidence_owner: {item.get('evidence_owner', 'unknown')}")
        lines.append(f"  - approval_boundary: {item.get('approval_boundary', 'unknown')}")
        lines.append(f"  - accepted_gap_option: {item.get('accepted_gap_option', 'unknown')}")
        lines.append(f"  - residual_risk: {item.get('residual_risk', 'unknown')}")
        lines.append(f"  - safe_next_action: {item.get('safe_next_action', 'unknown')}")
    return lines or ["- none"]


def _format_value(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value) if value else "none"
    return str(value)


def _list_lines(items: Any) -> list[str]:
    if not isinstance(items, list) or not items:
        return ["- none"]
    return [f"- {item}" for item in items]


def _approval_boundaries(recommendations: Any) -> list[str]:
    if not isinstance(recommendations, list):
        return []
    return [
        str(recommendation["approval_boundary"])
        for recommendation in recommendations
        if isinstance(recommendation, dict) and recommendation.get("approval_boundary")
    ]


def _residual_risks(recommendations: Any) -> list[str]:
    if not isinstance(recommendations, list):
        return []
    return [
        str(recommendation["residual_risk"])
        for recommendation in recommendations
        if isinstance(recommendation, dict) and recommendation.get("residual_risk")
    ]


def _json_block(value: Any) -> str:
    return "```json\n" + json.dumps(value, indent=2, sort_keys=True) + "\n```"


def _redact(text: str) -> str:
    try:
        from codex_runtime_runner.redaction import redact_text
    except ImportError:
        home = str(Path.home())
        return text.replace(home, "[redacted-local-path]")
    redacted, _report = redact_text(text)
    return redacted
