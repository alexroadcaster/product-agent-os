# Flaky Test Policy

Source status: `template`

Owner: tester

## Scope

Use this artifact for `quality_testing_evals` retries, quarantine and intermittent failure ownership.
Keep the policy `present_unverified` until current rerun evidence, owner and expiry are recorded.

## Current Evidence

| Test or job | Symptom | Rerun evidence | Root-cause class | Owner | Expiry | Follow-up |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | current command evidence | TBD | TBD | TBD | TBD |

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

Coverage is a signal, not proof.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, downstream risk, review date and expiry.

## Residual Risk

Retries can hide real failures when owner, expiry and follow-up are missing.

## Approval Boundary

`approval_required` before changing remote CI settings, quarantine rules or external dashboards.

## Verification

Record current rerun command, observed failure class and follow-up check.

## Rollback

Record how to remove retry/quarantine changes or why no rollback applies.

## Test Data Privacy

test data privacy: logs and traces must be sanitized. No Secrets, credentials or private customer data.
