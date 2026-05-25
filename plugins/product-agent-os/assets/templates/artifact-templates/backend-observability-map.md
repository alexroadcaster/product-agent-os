# Backend Observability Map

Source status: `template`

Owner: backend owner

## Scope

Use this artifact for `backend_observability_contract_present`, traces, metrics, logs, dashboards, alerts, alert ownership, correlation IDs, context propagation, semantic conventions or accepted gaps, collector/instrumentation notes, redaction policy, no-private-payload logging and OpenTelemetry-style vocabulary.

## Observability Signals

| Runtime path | Trace/span | Metric | Log event | Correlation ID | Dashboard | Alert ownership | Redaction/no-secrets/no-private-payload logging note | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | `present_unverified` |

## Instrumentation Notes

- Semantic conventions or accepted gaps:
- Collector/exporter or platform path:
- Collector/instrumentation notes:
- Context propagation:
- Baggage/privacy boundary:

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
- logs are observability is an unsupported claim
- traces
- metrics
- logs
- dashboards
- alerts
- alert ownership
- correlation IDs
- context propagation
- semantic conventions or accepted gaps
- collector/instrumentation notes
- redaction
- redaction policy
- no-private-payload logging
- collector/exporter
- logs alone are not accepted as observability

## Evidence

Record current observability evidence, dashboard/log query links or placeholders, alert ownership, no-secrets logging evidence and no-private-payload logging evidence.

## Accepted Gap

Use `explicit_gap_accepted` only with owner, reason, scope, downstream risk, review date and follow-up condition.

## Residual Risk

Logs alone are not accepted as observability and may expose secrets if redaction and no-private-payload logging are not explicit.

## Approval Boundary

`approval_required` before connecting to production telemetry, exporting logs externally or using production payloads.

## Verification

Record unit, integration, contract, runtime and operational checks for emitted signals.

## Rollback

Record rollback or disable path for noisy, sensitive or broken instrumentation.

## No Secrets

No Secrets, credentials, tokens, raw private chats, production payloads or private customer data in examples, fixtures, logs or prompts.
