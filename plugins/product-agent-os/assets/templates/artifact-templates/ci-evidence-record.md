# CI Evidence Record

Source status: `template`

Owner: release operator

## Scope

Use this artifact for `quality_testing_evals` CI quality gate evidence. CI configuration is `present_unverified` until a current job, command, artifact and result are recorded.

## Current Evidence

| Job or command | Trigger | Permissions | Artifact/log | Exit code | Freshness | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | least privilege | TBD | TBD | current run required | TBD |

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

Record `explicit_gap_accepted` only with owner, reason, review date and release impact.

## Residual Risk

Old CI status, skipped jobs or broad permissions can make a release claim unsupported.

## Approval Boundary

`approval_required` before changing remote CI, rerunning remote jobs, publishing artifacts or writing to external systems.

## Verification

Record current job URL or local equivalent, command, artifact, logs and result.

## Rollback

Record rollback path for CI changes or no-rollback rationale.

## Test Data Privacy

test data privacy: CI logs and artifacts must redact secrets and private data. No Secrets in examples or fixtures.
