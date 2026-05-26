# Security Risk Review

Source status: `codex-plugin-template`

Use this artifact for security-sensitive Product-Agent OS work before implementation, release, production changes, or readiness claims.

Codex Security scan status is explicit: `run with evidence`, `not requested`, or `blocked`. Do not imply that a scan ran from security terminology alone.

## Scope

- Change:
- Owner:
- Security reviewer:
- Approval status:
- Codex Security scan status:
- Files proposed:
- Systems affected:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Threat Surface

- Link to `threat-surface.md`:
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
- Data classification register:
- Redaction lifecycle for prompts, docs, fixtures, eval datasets, logs, traces and screenshots:
- Data minimization:
- Do not include raw secrets, credentials, private keys, payment data, raw PII, or raw customer data here.

## Compliance Boundary

- Compliance overlay:
- Legal/regulatory obligation:
- Customer contractual obligation:
- Internal policy:
- Owner/legal reviewer:
- Evidence:
- Non-goals:
- Review cadence:
- This artifact is not legal advice and does not claim GDPR, CCPA, HIPAA, PCI, SOC 2 or enterprise compliance certification.

## Supply Chain And CI

- Supply-chain review:
- SBOM/provenance decision:
- CI permission review:
- Action pinning:
- Vulnerability response link:
- Release integrity:

## Backend Security Notes

For backend changes, record `backend_security_reviewed` and route authn/authz, secrets, rate limits, audit logging, sensitive data, abuse cases, tokens, PII, money movement, privileged operations, external writes and irreversible side effects to this risk review before implementation or release. Docs, prompts, fixtures and logs must not contain secrets, credentials, tokens, raw PII, production payloads or private customer data. Record no-secrets evidence for every backend security-sensitive artifact.

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
