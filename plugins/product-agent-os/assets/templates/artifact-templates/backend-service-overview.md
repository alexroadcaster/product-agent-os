# Backend Service Overview

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_service_boundary_present`, `backend_runtime_behavior_present`, `backend_rollback_plan_present`, new or changed backend responsibility, module/service boundary mapping, owner review, ADR routing, APIs/events/external providers, provider contracts, Ports and Adapters boundary notes and optional Twelve-Factor vocabulary.

## Boundary

| Backend unit | Type | Purpose | Owner | Inbound contracts | Outbound dependencies | Data ownership | Deployment/runtime shape | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | module/service/worker | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

## Architecture And Contract Links

- Modular monolith is the default unless independent deploy/scale/team/ownership evidence justifies a service split:
- Microservices require explicit owner review, ADR link and migration/rollback notes:
- Owner review and ADR link:
- New or changed backend responsibility:
- Decision authority:
- Boundary rationale:
- ADR link or accepted gap:
- Ports/Adapters boundary:
- Domain logic independent from HTTP/DB/queue/vendor SDK concerns:
- Domain model or bounded context link:
- OpenAPI / AsyncAPI / Pact / protobuf / provider contracts:
- APIs/events/external providers:
- Contract changes synced with code and tests:
- API/event contract sync with code:

## Twelve-Factor Service Discipline

- Twelve-Factor vocabulary is optional service discipline vocabulary, not a mandatory framework:
- Explicit dependencies:
- Config/env keys:
- Build-release-run boundary:
- Process model:
- Stateless process or accepted gap:
- Admin tasks:
- Dev/prod parity:
- Logs-as-event-stream:

## Stack-Specific Snippets Policy

- T9-D7 backend templates are framework-agnostic:
- Stack-specific snippets deferred until separate research proves owner, examples and verification:
- Node.js, Python, Java, .NET and Go snippets:
- Owner, examples and verification:

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
- modular monolith is the default
- independent deploy/scale/team/ownership evidence
- microservices require explicit owner review
- migration/rollback notes
- owner review
- ADR
- ADR link or accepted gap
- decision authority
- boundary rationale
- ports/adapters boundary
- domain logic independent from HTTP/DB/queue/vendor SDK
- new or changed backend responsibility
- Twelve-Factor vocabulary
- explicit dependencies
- config/env keys
- build-release-run
- process model
- stateless process
- admin tasks
- dev/prod parity
- logs-as-event-stream
- OpenAPI
- AsyncAPI
- Pact
- protobuf
- provider contracts
- APIs/events/external providers
- contract changes synced with code and tests
- framework-agnostic
- stack-specific snippets deferred
- Node.js, Python, Java, .NET and Go snippets
- owner, examples and verification
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
