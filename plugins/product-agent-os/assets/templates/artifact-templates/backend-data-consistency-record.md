# Backend Data Consistency Record

Source status: `template`

Owner: backend and data owners

## Scope

Use this artifact for `backend_data_consistency_strategy_present`, local transaction, transaction boundary, consistency model, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path.

## Consistency Strategy

| Workflow/change | Transaction boundary | Consistency model | Outbox/saga/compensation | Monitoring | Reconciliation | Migration impact | Recovery path | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | local transaction/outbox/saga/compensation | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

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
- local transaction
- outbox
- saga
- compensation
- reconciliation
- migration impact
- recovery path

## Evidence

Record migration impact, consistency decision, reconciliation path, verification command and linked rollback/replay notes.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Distributed workflows can partially commit without compensation, monitoring or recovery evidence.

## Approval Boundary

`approval_required` before production data writes, migrations, external writes or destructive recovery actions.

## Verification

Record unit, integration, contract, runtime and operational checks for consistency behavior.

## Rollback

Record rollback, compensation, replay, data recovery or no-rollback rationale.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
