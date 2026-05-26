# Threat Surface

Source status: `codex-plugin-template`

Use this before security-sensitive implementation. It is read-only planning evidence until owner review and approval boundary are explicit.

## Scope

- Change:
- Owner:
- Reviewer:
- Systems affected:
- Decision horizon:
- Current evidence:
- Accepted Gap:
- Residual Risk:

## Surface Map

- Actors:
- Assets:
- Entry points:
- Trust boundaries:
- Privileged operations:
- Data exposed:
- External systems:
- External writes:
- Abuse cases:
- Kill switch or mitigation:

## Security Classification

- Authn/authz impact:
- Permissions impact:
- Secrets impact:
- PII/sensitive data impact:
- Payment/billing impact:
- CI/release impact:
- AI/agent/tool impact:
- Compliance overlay:

## Approval Boundary

- `approval_required` before production data, payment/billing, secret rotation, policy change, external security-system mutation or external write:
- Owner approval:
- Rollback:
- Safe next action:

No secrets: do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
