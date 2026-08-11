"""Select conservative test-strategy evidence from a code-quality profile."""

from __future__ import annotations

from dataclasses import dataclass

from product_agent_os.code_quality_selector import CodeQualityProfile


EVIDENCE_CEILING = (
    "strategy selection only; tests, comments and benchmarks not executed or verified"
)
TEST_KINDS = (
    "unit",
    "property",
    "characterization",
    "contract_integration",
    "end_to_end",
    "mutation",
    "benchmark",
)
RISK_TO_TEST = {
    "pure_logic": "unit",
    "property_invariant": "property",
    "legacy_behavior": "characterization",
    "external_boundary": "contract_integration",
    "critical_user_flow": "end_to_end",
    "high_risk_rule": "mutation",
    "hot_path": "benchmark",
    "performance_claim": "benchmark",
}
TEST_FIRST_MODES = frozenset(
    {"new_behavior", "defect_fix", "refactor", "legacy_change", "generated_code"}
)
CHANGE_MODES = TEST_FIRST_MODES | {"configuration"}
COMMENT_REASONS = (
    "non_obvious_intent",
    "invariant",
    "trade_off",
    "compatibility",
    "concurrency",
    "security",
    "operational_boundary",
)
ALLOWED_PROFILE_STATUSES = frozenset(
    {"present_unverified", "applicable_missing", "not_applicable"}
)
SUPPORTED_LANGUAGES = frozenset(
    {"python", "javascript", "typescript", "go", "rust", "java", "csharp"}
)


@dataclass(frozen=True)
class ChangeRisk:
    """A change risk and the invariants it must protect."""

    risk_id: str
    kind: str
    description: str
    protected_invariants: tuple[str, ...]
    languages: tuple[str, ...]


@dataclass(frozen=True)
class CommentSignal:
    """A signal that may require an intent comment or docstring."""

    risk_id: str
    reason: str
    detail: str


@dataclass(frozen=True)
class TestStrategyRequest:
    """Pure input for deterministic test-strategy selection."""

    profile: CodeQualityProfile
    change_mode: str
    executable_test_seam: bool
    test_seam_reason: str
    risks: tuple[ChangeRisk, ...]
    comment_signals: tuple[CommentSignal, ...]


@dataclass(frozen=True)
class TestFirstDecision:
    """Whether the selected change needs test-first evidence."""

    status: str
    risk_ids: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class TestDecision:
    """One selected or deferred test-evidence category."""

    test_kind: str
    status: str
    risk_ids: tuple[str, ...]
    protected_invariants: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class CoverageDecision:
    """The status of coverage telemetry for the selected strategy."""

    status: str
    reason: str


@dataclass(frozen=True)
class CommentDecision:
    """The status of comment evidence for the selected strategy."""

    status: str
    risk_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class PerformanceDecision:
    """The status of performance evidence for the selected strategy."""

    status: str
    risk_ids: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class QualityStrategy:
    """A conservative, unexecuted strategy for quality evidence."""

    schema_version: str
    profile_schema_version: str
    test_first_decision: TestFirstDecision
    test_decisions: tuple[TestDecision, ...]
    coverage_decision: CoverageDecision
    comment_decision: CommentDecision
    performance_decision: PerformanceDecision
    gaps: tuple[str, ...]
    evidence_ceiling: str


def select_test_strategy(request: TestStrategyRequest) -> QualityStrategy:
    """Select deterministic, unexecuted evidence from declared change risks."""
    _validate_request(request)
    risks = tuple(sorted(request.risks, key=lambda risk: risk.risk_id))
    grouped_risks = {
        test_kind: tuple(risk for risk in risks if RISK_TO_TEST[risk.kind] == test_kind)
        for test_kind in TEST_KINDS
    }
    test_decisions = tuple(
        _test_decision(test_kind, grouped_risks[test_kind]) for test_kind in TEST_KINDS
    )
    all_risk_ids = tuple(risk.risk_id for risk in risks)
    test_first_required = bool(risks) and request.executable_test_seam and request.change_mode in TEST_FIRST_MODES
    test_first = TestFirstDecision(
        status="required" if test_first_required else "not_applicable",
        risk_ids=all_risk_ids if test_first_required else (),
        reason="executable test seam is available" if test_first_required else _test_first_reason(request),
    )
    comment_decision = _comment_decision(request.comment_signals)
    benchmark = next(decision for decision in test_decisions if decision.test_kind == "benchmark")
    performance_decision = PerformanceDecision(
        status="required" if benchmark.risk_ids else "not_applicable",
        risk_ids=benchmark.risk_ids,
        rationale=(
            "benchmark evidence is required for hot-path or performance claims"
            if benchmark.risk_ids
            else "no_changed_risk_requires_benchmark"
        ),
    )
    gaps = _strategy_gaps(request.profile, risks)
    return QualityStrategy(
        schema_version="quality_strategy_v1",
        profile_schema_version=request.profile.schema_version,
        test_first_decision=test_first,
        test_decisions=test_decisions,
        coverage_decision=CoverageDecision(
            status="not_applicable",
            reason="coverage is telemetry, not a correctness target",
        ),
        comment_decision=comment_decision,
        performance_decision=performance_decision,
        gaps=gaps,
        evidence_ceiling=EVIDENCE_CEILING,
    )


def _test_decision(test_kind: str, risks: tuple[ChangeRisk, ...]) -> TestDecision:
    """Coalesce one risk category into its fixed test-decision slot."""
    if not risks:
        return TestDecision(
            test_kind=test_kind,
            status="not_applicable",
            risk_ids=(),
            protected_invariants=(),
            rationale=f"no_changed_risk_requires_{test_kind}",
        )
    return TestDecision(
        test_kind=test_kind,
        status="required",
        risk_ids=tuple(risk.risk_id for risk in risks),
        protected_invariants=tuple(
            sorted({invariant for risk in risks for invariant in risk.protected_invariants})
        ),
        rationale=f"changed risk requires {test_kind} evidence",
    )


def _test_first_reason(request: TestStrategyRequest) -> str:
    """Explain why test-first evidence is not applicable without adding evidence."""
    if not request.risks:
        return "no changed risks supplied"
    if not request.executable_test_seam:
        return request.test_seam_reason
    return "change mode does not require test-first evidence"


def _comment_decision(signals: tuple[CommentSignal, ...]) -> CommentDecision:
    """Coalesce approved comment signals into a deterministic decision."""
    if not signals:
        return CommentDecision(
            status="not_applicable",
            risk_ids=(),
            reasons=(),
            rationale="no non-obvious comment trigger was supplied",
        )
    reasons = tuple(reason for reason in COMMENT_REASONS if any(signal.reason == reason for signal in signals))
    return CommentDecision(
        status="required",
        risk_ids=tuple(sorted({signal.risk_id for signal in signals})),
        reasons=reasons,
        rationale="comment documents non-obvious intent, invariant, trade-off or boundary",
    )


def _strategy_gaps(
    profile: CodeQualityProfile, risks: tuple[ChangeRisk, ...]
) -> tuple[str, ...]:
    """List missing profile-language evidence without creating a test command."""
    if not risks:
        return ("no_changed_risks",)
    present_languages = {
        language
        for stack in profile.stack_profiles
        if stack.status == "present_unverified"
        for language in stack.languages
    }
    return tuple(
        f"profile_language_missing:{risk.risk_id}:{language}"
        for risk in risks
        for language in sorted(risk.languages)
        if language not in present_languages
    )


def _validate_request(request: TestStrategyRequest) -> None:
    """Validate the public input and conservative profile state before selection."""
    if not isinstance(request, TestStrategyRequest):
        raise TypeError("request must be a TestStrategyRequest")
    if not isinstance(request.profile, CodeQualityProfile):
        raise TypeError("request profile must be a CodeQualityProfile")
    if not isinstance(request.risks, tuple) or not isinstance(request.comment_signals, tuple):
        raise TypeError("risks and comment signals must be tuples")
    if not isinstance(request.executable_test_seam, bool):
        raise TypeError("executable test seam must be a bool")
    if not all(isinstance(risk, ChangeRisk) for risk in request.risks):
        raise TypeError("risks must contain ChangeRisk values")
    if not all(isinstance(signal, CommentSignal) for signal in request.comment_signals):
        raise TypeError("comment signals must contain CommentSignal values")
    _validate_profile(request.profile)
    if request.change_mode not in CHANGE_MODES:
        raise ValueError("unsupported change mode")
    if request.executable_test_seam != (not bool(request.test_seam_reason)):
        raise ValueError("test seam reason must match executable test seam state")
    _validate_risks(request.risks)
    _validate_comment_signals(request.comment_signals, request.risks)


def _validate_profile(profile: CodeQualityProfile) -> None:
    """Reject forged profile versions or evidence states before strategy selection."""
    if profile.schema_version != "code_quality_profile_v1":
        raise ValueError("unsupported profile schema version")
    states = [profile.inventory_status]
    for stack in profile.stack_profiles:
        states.append(stack.status)
        for category in stack.categories:
            states.append(category.status)
            states.extend(tool.status for tool in category.tools)
    states.extend(utility.status for utility in profile.project_utilities)
    if not all(state in ALLOWED_PROFILE_STATUSES for state in states):
        raise ValueError("profile contains an unsupported evidence state")


def _validate_risks(risks: tuple[ChangeRisk, ...]) -> None:
    """Validate risk identifiers, mappings, invariant text, and language scope."""
    identifiers: set[str] = set()
    for risk in risks:
        if risk.kind not in RISK_TO_TEST:
            raise ValueError("unsupported risk kind")
        _require_text(risk.risk_id, "risk id")
        if "/" in risk.risk_id or "\\" in risk.risk_id or ".." in risk.risk_id:
            raise ValueError("risk id must not be path-like")
        _require_text(risk.description, "risk description")
        if not risk.protected_invariants or not risk.languages:
            raise ValueError("risks require invariants and languages")
        for invariant in risk.protected_invariants:
            _require_text(invariant, "protected invariant")
        for language in risk.languages:
            if language not in SUPPORTED_LANGUAGES:
                raise ValueError("unsupported risk language")
        if risk.risk_id in identifiers:
            raise ValueError("duplicate risk id")
        identifiers.add(risk.risk_id)


def _validate_comment_signals(
    signals: tuple[CommentSignal, ...], risks: tuple[ChangeRisk, ...]
) -> None:
    """Validate approved comment reasons and reject conflicting duplicate signals."""
    risk_ids = {risk.risk_id for risk in risks}
    details: dict[tuple[str, str], str] = {}
    for signal in signals:
        if signal.risk_id not in risk_ids:
            raise ValueError("comment signal references an unknown risk")
        if signal.reason not in COMMENT_REASONS:
            raise ValueError("unsupported comment reason")
        _require_text(signal.detail, "comment detail")
        key = (signal.risk_id, signal.reason)
        previous = details.setdefault(key, signal.detail)
        if previous != signal.detail:
            raise ValueError("conflicting duplicate comment details")


def _require_text(value: str, label: str) -> None:
    """Require non-empty, NUL-free text in a pure input contract."""
    if not value.strip() or "\0" in value:
        raise ValueError(f"{label} must be non-empty and NUL-free")


def quality_strategy_as_dict(strategy: QualityStrategy) -> dict[str, object]:
    """Serialize a quality strategy in its fixed public schema order."""
    return {
        "schema_version": strategy.schema_version,
        "profile_schema_version": strategy.profile_schema_version,
        "test_first_decision": {
            "status": strategy.test_first_decision.status,
            "risk_ids": list(strategy.test_first_decision.risk_ids),
            "reason": strategy.test_first_decision.reason,
        },
        "test_decisions": [
            {
                "test_kind": decision.test_kind,
                "status": decision.status,
                "risk_ids": list(decision.risk_ids),
                "protected_invariants": list(decision.protected_invariants),
                "rationale": decision.rationale,
            }
            for decision in strategy.test_decisions
        ],
        "coverage_decision": {
            "status": strategy.coverage_decision.status,
            "reason": strategy.coverage_decision.reason,
        },
        "comment_decision": {
            "status": strategy.comment_decision.status,
            "risk_ids": list(strategy.comment_decision.risk_ids),
            "reasons": list(strategy.comment_decision.reasons),
            "rationale": strategy.comment_decision.rationale,
        },
        "performance_decision": {
            "status": strategy.performance_decision.status,
            "risk_ids": list(strategy.performance_decision.risk_ids),
            "rationale": strategy.performance_decision.rationale,
        },
        "gaps": list(strategy.gaps),
        "evidence_ceiling": strategy.evidence_ceiling,
    }
