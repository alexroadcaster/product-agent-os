# API Security Review

Source status: `codex-plugin-template`

Use this for API, webhook, integration, generated client and contract security changes.

## Scope

- Change:
- Owner:
- Security reviewer:
- Contract source:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Review

- Security scheme:
- OAuth/JWT/session policy:
- Scopes:
- Token claims:
- Error behavior:
- Negative examples:
- Object-level authorization:
- Function-level authorization:
- Object property authorization:
- Rate limits:
- Input/output validation:
- Unsafe consumption:
- Abuse cases:
- OpenAPI or equivalent contract:

OAuth or API documentation alone is not security evidence. Link to `authz-negative-test-matrix.md`, `abuse-rate-limit-plan.md` and the security risk review.

Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
