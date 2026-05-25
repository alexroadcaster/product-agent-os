# Backend Job Queue Contract

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_job_queue_contract_present`, background jobs, queues, consumers, schedulers, payload contracts, AsyncAPI or provider contract, retry, dead-letter queue, idempotency, replay, deduplication, ordering and backpressure.

## Queue And Job Matrix

| Queue/job | Producer | Consumer | Payload contract | Retry policy | Dead-letter queue | Dead-letter behavior | Idempotency key | Deduplication policy | Ordering guarantee | Backpressure | Replay procedure | Poison-message handling | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

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
- AsyncAPI
- AsyncAPI or provider contract
- contract changes synced with code and tests
- payload contract
- retry policy
- dead-letter queue
- dead-letter behavior
- idempotency key
- deduplication policy
- ordering guarantee
- backpressure
- replay
- replay procedure
- poison-message handling

## Evidence

Record payload examples with synthetic data, retry/dead-letter behavior, deduplication policy, ordering guarantee, backpressure, replay command or accepted gap.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Duplicate processing or poison messages can corrupt data without idempotency and replay evidence.

## Approval Boundary

`approval_required` before production queue replay, external writes, destructive job runs or production payload access.

## Verification

Record unit, integration, contract, runtime and operational checks for queue and job behavior.

## Rollback

Record rollback, disable, drain, replay or no-rollback rationale.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
