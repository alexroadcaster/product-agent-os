# Test/Eval Matrix

Source status: `template`

Owner: tester or test-eval designer

## Scope

Use this artifact for `quality_testing_evals` traceability. Map requirement, scenario, risk and claim to the smallest useful check, eval, runtime/manual evidence or `explicit_gap_accepted`.

## Matrix

| Requirement or claim | Risk | Scenario | Check/eval/manual evidence | Current Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | current command/eval/runtime/manual evidence | TBD | `present_unverified` |

## Backend Check Mapping

Backend behavior should map service boundary, runtime behavior, dependency failure, queue/job, data consistency, health, observability and rollback claims to unit, integration, contract, runtime and operational checks. Code inspection alone is not backend completion evidence.

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

Record owner, reason, downstream risk, review date and follow-up condition.

## Residual Risk

Unmapped acceptance criteria, contracts or regression impact can leave quality claims unsupported.

## Approval Boundary

`approval_required` before external CI writes, production data use, remote reruns or publishing claims outside the workspace.

## Verification

Record command, expected result, actual result, exit code or eval score, environment and freshness.

## Rollback

Record rollback path or no-rollback rationale for risky verification gaps.

## Test Data Privacy

test data privacy: use synthetic or sanitized fixtures. No Secrets, credentials, raw private chats or private customer data.
