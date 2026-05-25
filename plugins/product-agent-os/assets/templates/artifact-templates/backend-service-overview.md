# Backend Service Overview

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_rollback_plan_present`, module/service boundary mapping and Ports and Adapters boundary notes.

## Boundary

| Backend unit | Type | Purpose | Owner | Inbound contracts | Outbound dependencies | Data ownership | Deployment/runtime shape | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | module/service/worker | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

## Architecture And Contract Links

- Modular monolith default or microservice rationale:
- Owner review and ADR link:
- Ports and Adapters boundary:
- Domain model or bounded context link:
- OpenAPI / AsyncAPI / Pact / protobuf / provider contract:
- API/event contract sync with code:

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
- `backend-service-overview.md`
- `backend-runtime-behavior.md`
- purpose
- owner
- inbound contracts
- outbound dependencies
- data ownership
- deployment/runtime shape
- OpenAPI
- AsyncAPI
- Pact
- protobuf
- unit
- integration
- contract
- runtime
- operational checks
- code inspection alone is not backend completion evidence

## Evidence

Record linked requirements, contracts, owner review, ADR, runtime evidence, dependency evidence, test/eval evidence and accepted gaps.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Missing backend boundary evidence can hide unclear ownership, data responsibility and runtime failure paths.

## Approval Boundary

`approval_required` before production data access, external writes, secret handling, deploy actions or irreversible side effects.

## Verification

Record unit, integration, contract, runtime and operational checks with command, environment, result and freshness.

## Rollback

Record rollback, recovery, replay or no-rollback rationale for the backend responsibility change.

## No Secrets

No Secrets, credentials, tokens, connection strings, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
