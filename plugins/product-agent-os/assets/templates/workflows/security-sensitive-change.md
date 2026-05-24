# Security-Sensitive Change Workflow

Source status: `codex-plugin-template`

Use this workflow when a change touches authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit behavior, audit logging, or other security-sensitive boundaries.

## Inputs

- User goal and accepted scope.
- Current requirements, plan, changed files map, and relevant `AGENTS.md` rules.
- Authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, and approval evidence.
- Known production, external-system, database, billing, or customer-data boundaries.
- Explicit user request for Codex Security scan if security scan integration is wanted.

## Process

1. Keep the workflow read-only until the security risk review, threat surface, owner review, approval boundary, rollback, and verification plan are explicit.
2. Inventory authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, test, rollback, and approval clues as `present_unverified`.
3. Identify the threat surface: actors, trust boundaries, entry points, data exposed, privileged operations, external systems, billing/payment paths, and abuse cases.
4. Stage the security risk review artifact before implementation.
5. Require spec compliance before quality/risk verdict: what behavior is allowed, what is forbidden, and which user or system role owns approval.
6. Require security tests or an explicit test gap for authn, authz, permission, payment, billing, PII, sensitive data, abuse control, rate limit, and audit logging behavior touched by the change.
7. Record rollback and mitigation: feature flag, kill switch, revert plan, permission rollback, payment disable path, or data access rollback.
8. Do not store secrets, credentials, private keys, raw PII, raw customer data, payment data, access tokens, or secret-bearing config values in artifacts, prompts, fixtures, logs, or examples.
9. Do not change auth, permissions, billing, payment, secrets handling, PII handling, sensitive data access, abuse controls, rate limit behavior, audit logging, or production policy until owner review and approval are explicit.
10. Do not process payments, run billing operations, rotate production secrets, access customer data, or mutate external security systems without explicit approval.
11. Use Codex Security only when explicitly requested; do not imply a Codex Security scan was run from this workflow alone.
12. Keep the Scenario Handoff concise.

## Outputs

- Staged security risk review with:
  - threat surface;
  - authn/authz and permissions impact;
  - payment and billing impact;
  - secrets and PII/sensitive data handling;
  - abuse controls and rate limit impact;
  - audit logging impact;
  - tests and missing checks;
  - owner review and approval boundary;
  - rollback and mitigation;
  - residual risk.
- Scenario Handoff:
  - sources/context used;
  - assumptions;
  - files touched;
  - files proposed;
  - verification evidence;
  - open risks;
  - recommended next role;
  - stop reason.

## Verification

- Threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval, and residual risk are explicit.
- Security-sensitive claims cite current tests, review evidence, owner evidence, or an explicit gap.
- No secrets, credentials, private keys, raw PII, raw customer data, payment data, or access tokens are stored in artifacts.
- Codex Security scan status is either explicitly requested and evidenced, or marked not run.
- External writes, production changes, payment operations, customer-data access, secret rotation, policy changes, and deployment remain approval-bound.

## Stop Conditions

- Threat surface is unclear.
- Authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, or audit logging impact is unknown.
- Owner review, approval boundary, tests, rollback, or residual risk is missing.
- A secret, raw PII, raw customer data, payment data, or access token would be stored in an artifact.
- The task requires Codex Security but the user has not explicitly requested it.
- The task requires external security-system mutation, production policy change, payment processing, or customer-data access without approval.
