# Security Risk Review

Source status: `codex-plugin-template`

Use this artifact for security-sensitive Product-Agent OS work before implementation, release, production changes, or readiness claims.

## Scope

- Change:
- Owner:
- Security reviewer:
- Approval status:
- Files proposed:
- Systems affected:

## Threat Surface

- Entry points:
- Actors:
- Trust boundaries:
- Privileged operations:
- External systems:
- External writes:
- Irreversible side effects:
- Data exposed:
- Abuse cases:

## Authn/Authz And Permissions

- Authn impact:
- Authz impact:
- Permissions impact:
- Role or scope changes:
- Access-control tests:
- Residual risk:

## Payment And Billing

- Payment impact:
- Billing impact:
- Provider or checkout path:
- Refund, dispute, or charge risk:
- Required approval:
- Residual risk:

## Secrets And Sensitive Data

- Secrets touched:
- Tokens touched:
- Secret storage policy:
- PII touched:
- Sensitive data touched:
- Customer data boundary:
- Data minimization:
- Do not include raw secrets, credentials, private keys, payment data, raw PII, or raw customer data here.

## Backend Security Notes

For backend changes, record `backend_security_reviewed` and route authn/authz, tokens, PII, money movement, privileged operations, external writes and irreversible side effects to this risk review before implementation or release. Docs, prompts, fixtures and logs must not contain secrets, credentials, tokens, raw PII, production payloads or private customer data.

Use `approval_required` before touching auth, secrets, PII, money movement, privileged operations, production data, external writes or irreversible side effects. If the security surface is intentionally out of scope, record `explicit_gap_accepted` with owner, reason, review date, downstream risk and follow-up condition.

## Abuse Controls And Audit Logging

- Abuse controls:
- Rate limit impact:
- Fraud or misuse risk:
- Audit logging:
- Alerting or monitoring:
- Residual risk:

## Tests And Evidence

- Unit tests:
- Integration tests:
- Authorization tests:
- Payment tests:
- Abuse-control tests:
- Audit logging checks:
- Manual checks:
- Missing checks:

## Rollback And Approval

- Rollback:
- Feature flag or kill switch:
- Permission rollback:
- Payment disable path:
- Secret rollback:
- Owner review:
- Approval:
- Deployment boundary:

## Verdict

- Spec compliance verdict:
- Quality/risk verdict:
- Blocking findings:
- Residual risk:
- Next action:
