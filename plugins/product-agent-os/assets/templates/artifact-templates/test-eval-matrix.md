# Test/Eval Matrix

Source status: `template`

Owner: tester or test-eval designer

## Scope

Use this artifact for `quality_testing_evals` traceability. Map requirement, scenario, risk and claim to the smallest useful check, eval, runtime/manual evidence or `explicit_gap_accepted`.

## Current Evidence

- Evidence freshness:
- Environment and command:
- Model/effort/settings fingerprint when applicable:

## Matrix

| Requirement or claim | Risk | Scenario | Model | Reasoning effort | Prompt/tools/settings fingerprint | Check/eval/manual evidence | Quality result | Latency | Tokens/cost | Current evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | exact model ID or `not_applicable` | exact value or `not_applicable` | stable comparison reference | smallest valid gate | score/verdict | measured or gap | measured or gap | current command/eval/runtime/manual evidence | TBD | `present_unverified` |

## GPT-6 Migration Comparison

For each migrated role or workflow, keep the task, prompt, tools, skills, sandbox, approvals, fixtures, and output rubric fixed. Run at least:

| Candidate | Required comparison | Promotion rule |
| --- | --- | --- |
| `gpt-6.1-sol` or `gpt-6.1-terra` at preserved effort | compare with recorded prior model at the same effort | no regression in correctness, instruction following, tool completion, safety, or unsupported claims |
| same model at one lower supported effort | cost/latency candidate | promote only if quality is non-inferior and declared latency/cost thresholds pass |

Record fresh-session evidence separately from config parsing. A valid config or green synthetic test proves the contract, not model-quality promotion.

Record control-surface repairs separately: parent permissions and inherited MCP must be held constant in a model-only comparison. Restoring a prior model pin does not authorize restoring unsupported agent-local access settings.

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
- `model_effort_comparison_present`
- `quality_cost_latency_tradeoff_recorded`

Coverage is a signal, not proof.

## Accepted Gap

Record owner, reason, downstream risk, review date and follow-up condition.

## Residual Risk

Unmapped acceptance criteria, contracts, regression impact, model/effort settings, or freshness can leave quality claims unsupported.

## Approval Boundary

`approval_required` before external CI writes, production data use, provider/model calls, remote reruns, or publishing claims outside the workspace.

## Verification

Record command, expected result, actual result, exit code or eval score, environment, model ID, reasoning effort, settings fingerprint, and freshness.

## Rollback

Record rollback path or no-rollback rationale for risky verification gaps.

## Test Data Privacy

test data privacy: use synthetic or sanitized fixtures. No Secrets, credentials, raw private chats, private customer data, or raw provider payloads.
