# Backend Health Check Contract

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_health_probe_contract_present`, health endpoint semantics, liveness, readiness, startup or platform-equivalent health semantics and verification. Health checks are tested where the platform/runtime is available. Documentation alone is not sufficient for deployable service health readiness.

## Health Semantics

| Check | Meaning | Dependencies checked | Failure behavior | Platform mapping | Test evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| liveness | process alive | TBD | restart/alert | platform equivalent | TBD | `present_unverified` |
| readiness | can receive traffic/work | TBD | remove from traffic/work | platform equivalent | TBD | `present_unverified` |
| startup | initialization complete | TBD | startup gate | platform equivalent | TBD | `present_unverified` |

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
- health endpoint exists, so readiness is solved is an unsupported claim
- health endpoint semantics
- liveness
- readiness
- startup
- platform equivalent
- platform-unavailable gap
- platform-unavailable gap owner
- platform-unavailable gap reason
- platform-unavailable follow-up
- documentation alone is not sufficient

## Evidence

Record current health-check test, runtime command, health endpoint semantics, platform behavior or accepted platform-unavailable gap. A platform-unavailable gap must name owner, reason and follow-up.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Conflating liveness and readiness can send traffic to a service that is alive but not ready.

## Approval Boundary

`approval_required` before changing production probes, deployment health gates or traffic routing.

## Verification

Record unit, integration, contract, runtime and operational checks for health semantics.

## Rollback

Record rollback/no-rollback rationale for health check changes.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
