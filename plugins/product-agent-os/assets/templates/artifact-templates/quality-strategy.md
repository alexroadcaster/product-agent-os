# Quality Strategy

Source status: `template`

Owner: tester or implementation planner

## Risk-Based Code Strategy

- `schema_version`: `quality_strategy_v1`
- `profile_schema_version`: `code_quality_profile_v1`

### Test-First Decision

| status | risk_ids | reason |
| --- | --- | --- |
| TBD | TBD | TBD |

### Risk-To-Test Decisions

| test_kind | status | risk_ids | protected_invariants | rationale |
| --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD |

### Coverage Decision

- status: `not_applicable`
- reason: coverage is telemetry, not a correctness target

### Comment Decision

| status | risk_ids | reasons | rationale |
| --- | --- | --- | --- |
| TBD | TBD | TBD | TBD |

### Performance Decision

| status | risk_ids | rationale |
| --- | --- | --- |
| TBD | TBD | TBD |

### Strategy Gaps

- gaps: TBD

### Selection Evidence Ceiling

- evidence_ceiling: strategy selection only; tests, comments and benchmarks not executed or verified
- tests_executed: false
- benchmarks_executed: false

## Scope

Use this artifact for `quality_testing_evals` strategy, risk based scope and accepted gaps before completion, readiness, release or quality claims.

## Current Evidence

| Evidence type | Command or source | Expected result | Actual result | Freshness | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| local command | TBD | TBD | TBD | current run required | TBD | `present_unverified` |

## Risk Based Scope

Record impact, likelihood, user harm, data/security exposure, failure history, selected checks and deferred checks.

## Professional Code Quality Evidence

- Coding-standard checklist:
- Existing-capability scan:
- Selected leverage path:
- Rejected alternatives:
- Dependency decision:
- Deep module check:
- Legacy seam check:
- Comment policy:
- Cleverness budget:
- Unsupported code-quality claims:
- Code-quality claim evidence:
- Accepted gap:

## Backend Runtime Evidence

For backend work, map `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md` and `backend-release-rollback-notes.md` to unit, integration, contract, runtime and operational checks. Code inspection alone is not backend completion evidence.

## Quality Gate References

- `quality_strategy_present`
- `risk_based_scope_present`
- `test_first_or_gap_present`
- `acceptance_traceability_present`
- `contract_check_present`
- `runtime_evidence_present`
- `manual_qa_evidence_present`
- `visual_a11y_evidence_present`
- `eval_spec_present`
- `eval_rerun_evidence_present`
- `current_evidence_before_completion`
- `ci_quality_gate_present`
- `flaky_test_policy_present`
- `coverage_policy_present`
- `test_data_privacy_present`
- `bug_reproduction_evidence_present`
- `regression_impact_present`
- `professional_code_authoring_evidence_present`

Coverage is a signal, not proof.

## Unsupported Claims

Reject claims that more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate, manual QA is not evidence, AI evals are optional for AI behavior changes, custom code proves seniority, a new dependency is harmless without review, or clean-looking refactor is safe without characterization evidence.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Missing current evidence can make inspection-only work look verified.

## Approval Boundary

`approval_required` before external CI writes, production data use, remote reruns or publication.

## Verification

Record current command/eval/runtime/manual evidence, environment and result before any ready claim.

## Rollback

Record rollback or no-rollback rationale for high-risk quality gaps.

## Test Data Privacy

test data privacy: use synthetic or sanitized data. No Secrets, credentials, raw private chats or private customer data.
