# Approval Record

Source status: `codex-plugin-template`

Use this before production data, external writes, payment/billing, customer data, secret rotation, policy changes or external security-system mutations.

## Scope

- Change:
- Owner:
- Approver:
- Approval status:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Approval Boundary

- Production data:
- External write:
- Payment/billing:
- Customer data:
- Secret rotation:
- Policy change:
- External security system:
- Rollback:
- Expiry/review date:
- Audit-ready evidence:

No action is approved by this template alone. Record explicit approval before side effects. Use `approval_required` until the approver and evidence are recorded.

Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
