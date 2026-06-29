from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


REQUIRED_BEHAVIORAL_CASES = {
    "route-selection",
    "runtime-methodology-packet-safety",
    "agent-skill-metrics-loop-safety",
    "agent-skill-metrics-regression-finding",
    "agent-skill-metrics-no-data-target",
    "agent-skill-metrics-trace-missing-span",
    "agent-skill-metrics-judge-not-calibrated",
    "agent-skill-metrics-approval-required-modernization",
    "agent-skill-metrics-automation-candidate-only",
    "guided-question-smallest-blocking-question",
    "guided-question-no-broad-methodology-interview",
    "status-dashboard-generated-view-only",
    "status-dashboard-stale-evidence-no-success-claim",
    "runtime-first-response-no-question-dump",
    "first-run-response",
    "first-run-empty-greenfield",
    "first-run-broken-bug-rescue",
    "first-run-existing-control-plane",
    "first-run-complex-system",
    "greenfield-no-scaffold-before-approval",
    "greenfield-lightweight-mode",
    "complex-ownership-split",
    "complex-no-overparallelization",
    "scenario-handoff-completeness",
    "pr-review-readiness",
    "legacy-onboarding-map",
    "api-migration-plan",
    "ai-eval-regression-plan",
    "native-mobile-runtime-plan",
    "desktop-local-runtime-plan",
    "data-migration-plan",
    "security-sensitive-change-plan",
    "ci-stabilization-plan",
    "release-packaging-readiness",
    "explicit-invocation",
    "adversarial-shortcut",
    "bug-rescue-root-cause",
    "bug-rescue-no-broad-rewrite",
    "bug-rescue-no-repro-stop",
    "acceptance-scenarios-traceability",
    "quality-current-evidence-before-completion",
    "frontend-evidence-before-completion",
    "backend-evidence-before-completion",
    "llm-ai-rag-evidence-before-completion",
    "cross-domain-semantic-evidence-sufficiency",
    "cross-domain-synthesis-mixed-surface-routing",
    "no-placeholder-plan",
    "two-stage-review",
    "fresh-context-handoff",
    "evidence-before-completion",
    "completion-skeptic-check-again-trigger",
    "completion-skeptic-false-pass-blocked",
    "completion-skeptic-false-rewrite-blocked",
    "completion-skeptic-source-sensitive-docs",
    "completion-skeptic-code-tool-evidence",
    "completion-skeptic-fake-evidence-adversarial",
    "completion-skeptic-scorecard-thresholds",
    "task-matrix-validator-and-completion-report",
    "task-matrix-agent-handoff-and-planning-control",
    "professional-code-authoring-custom-code-bloat",
    "professional-code-authoring-unnecessary-dependency",
    "professional-code-authoring-missing-existing-capability-scan",
    "professional-code-authoring-comment-noise",
    "professional-code-authoring-shallow-wrapper",
    "professional-code-authoring-unsupported-legacy-rewrite",
    "finish-options",
    "codex-only-compatibility",
    "cost-model-budget",
}

SECRET_MARKERS = (
    "BEGIN PRIVATE KEY",
    "PASSWORD=",
    "API_KEY=",
    "TOKEN=",
)
SECRET_VALUE_PATTERN = re.compile(
    r"(?i)\b(?:sk|rk|sess|ghp|github_pat|xox[baprs]?)-[A-Za-z0-9][A-Za-z0-9._-]{5,}"
)


def validate_behavioral_eval_template(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    case_names = {
        str(case.get("name", ""))
        for case in cases
        if isinstance(case, dict) and case.get("name")
    }
    unsafe_cases = [
        str(case.get("name", "<unnamed>"))
        for case in cases
        if not _case_is_safe(case)
    ]
    missing_required_cases = sorted(REQUIRED_BEHAVIORAL_CASES - case_names)
    codex_only = data.get("codex_only") is True
    status = (
        "ok"
        if codex_only and not missing_required_cases and not unsafe_cases
        else "needs_review"
    )

    return {
        "status": status,
        "codex_only": codex_only,
        "case_count": len(cases) if isinstance(cases, list) else 0,
        "required_cases": sorted(REQUIRED_BEHAVIORAL_CASES),
        "missing_required_cases": missing_required_cases,
        "unsafe_cases": unsafe_cases,
    }


def _case_is_safe(case: object) -> bool:
    if not isinstance(case, dict):
        return False
    for key in ["name", "input", "expected", "forbidden", "residual_risk"]:
        if key not in case:
            return False
    forbidden = case.get("forbidden")
    if not isinstance(forbidden, list) or not forbidden:
        return False
    payload = json.dumps(case, sort_keys=True)
    return not any(marker in payload for marker in SECRET_MARKERS) and not SECRET_VALUE_PATTERN.search(payload)
