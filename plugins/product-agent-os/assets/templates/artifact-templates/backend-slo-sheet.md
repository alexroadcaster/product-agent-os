# Backend SLO Sheet

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_slo_or_gap_present`, user-facing or production backend reliability expectations and explicit no-telemetry or not-yet-production gaps.

## SLO Table

| User journey | User-relevant SLI | SLO target | Measurement window | Alert policy | Owner | Telemetry status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | present_unverified/explicit_gap_accepted | `present_unverified` |

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
- SLOs are only for large companies is an unsupported claim
- user journey
- SLI
- SLO target
- measurement window
- alert policy

## Evidence

Record telemetry source, current dashboard or gap, alert owner and linked runbook.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Production reliability expectations can remain implicit without SLI/SLO or explicit gap.

## Approval Boundary

`approval_required` before accessing production telemetry or changing production alerting.

## Verification

Record unit, integration, contract, runtime and operational checks for the SLI source where available.

## Rollback

Record rollback/no-rollback rationale for SLO, alert or measurement changes.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
