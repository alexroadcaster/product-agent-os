# Backend Dependency Failure Matrix

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_dependency_failure_matrix_present`, remote service, database, cache, queue, payment, email, storage, search or third-party provider failure policy.

## Matrix

| Dependency | Owner | Timeout | Retry | Circuit breaker/non-applicability | Fallback | Alert | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | unit/integration/contract/runtime | `present_unverified` |

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
- backend-dependency-failure-matrix.md
- timeout
- retry
- circuit breaker
- fallback
- alert
- owner

## Evidence

Record dependency owner, failure policy, linked runtime behavior, current verification command and accepted gap.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Unbounded dependency failure can cascade across backend services and users.

## Approval Boundary

`approval_required` before external provider writes, production credentials, production data access or live failover tests.

## Verification

Record unit, integration, contract, runtime and operational checks for dependency failure behavior.

## Rollback

Record rollback, fallback disable path or no-rollback rationale.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
