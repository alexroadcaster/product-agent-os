# Manual QA Evidence

Source status: `template`

Owner: tester or reviewer

## Scope

Use this artifact for `quality_testing_evals` runtime, manual, visual and accessibility evidence that cannot be fully automated yet.
Keep the evidence `present_unverified` until environment, criteria, reviewer and artifacts are recorded.

## Current Evidence

| Charter | Environment | Criteria | Reviewer | Notes | Result | Artifacts |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | current manual evidence required | screenshot/log/trace |

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

Record `explicit_gap_accepted` with owner, reason, scope, downstream risk, review date and follow-up.

## Residual Risk

Manual evidence without criteria, environment or reviewer cannot support a quality claim.

## Approval Boundary

`approval_required` before collecting production data, changing external systems or publishing evidence.

## Verification

Record viewport, keyboard/focus, accessibility result, runtime logs, screenshots, traces or API output.

## Rollback

Record rollback/no-rollback rationale for runtime or UI evidence gaps.

## Test Data Privacy

test data privacy: screenshots, logs and traces must be sanitized. No Secrets, credentials, raw private chats or private customer data.
