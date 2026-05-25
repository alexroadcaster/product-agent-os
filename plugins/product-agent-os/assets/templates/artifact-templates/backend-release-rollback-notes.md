# Backend Release Rollback Notes

Source status: `template`

Owner: backend and release owners

## Scope

Use this artifact for `backend_rollback_plan_present`, risky backend release, migration, feature flag, rollback, replay and data recovery evidence.

## Rollback Plan

| Change | Risk | Feature flag | Migration impact | Rollback trigger | Rollback/no-rollback rationale | Replay/data recovery | Owner approval | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

## Backend Shared Contract Terms

- `backend_service_boundary_present`
- `backend_runtime_behavior_present`
- `backend_dependency_failure_matrix_present`
- `backend_observability_contract_present`
- `backend_slo_or_gap_present`
- `backend_health_probe_contract_present`
- `backend_job_queue_contract_present`
- `backend_data_consistency_strategy_present`
- `backend_config_secrets_boundary_present`
- `backend_security_reviewed`
- `backend_rollback_plan_present`
- migration
- feature flag
- rollback trigger
- replay
- data recovery

## Evidence

Record release evidence, verification command, rollback command/procedure, owner approval and residual risk.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Risky backend changes can become irreversible without rollback, recovery or replay evidence.

## Approval Boundary

`approval_required` before production release, tag, deploy, migration, external write or destructive rollback action.

## Verification

Record unit, integration, contract, runtime and operational checks before release.

## Rollback

Record rollback, recovery, replay or no-rollback rationale.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
