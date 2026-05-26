# Authorization Negative Test Matrix

Source status: `codex-plugin-template`

Use this for authn/authz, role, scope, tenant, resource ownership and API authorization changes.

## Scope

- Change:
- Owner:
- Security reviewer:
- API or UI surface:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Matrix

| Actor/role | Resource | Allowed behavior | Forbidden behavior | Negative test | Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Required Negative Cases

- BOLA / broken object-level authorization:
- BFLA / broken function-level authorization:
- Object property authorization:
- Role checks:
- Scope checks:
- Tenant/resource ownership:
- Rate limits:
- Unsafe consumption:
- Error behavior:
- Abuse case:

OAuth, JWT, session middleware or API docs alone are not security evidence. Link tests to `api-security-review.md` and the security risk review.

Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
