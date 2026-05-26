# Secrets Policy

Source status: `codex-plugin-template`

Use this to record secret storage, rotation, access scope, scanning and incident path without storing secret values.

## Scope

- Change:
- Owner:
- Security reviewer:
- Secret classes:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Policy

- Secret storage location:
- Access scope:
- Rotation policy:
- Revocation path:
- Scan coverage:
- CI secret boundary:
- Local developer boundary:
- Prompt/log/trace/screenshot redaction:
- Incident path:
- Verification:

## Approval Boundary

- `approval_required` before secret rotation, credential changes, key management changes or external secret-manager mutation:
- Rollback:
- Owner approval:

No secrets: never write raw secrets, credentials, access tokens, private keys, webhook signing secrets, payment data, raw PII, raw private chats or private customer data into docs, prompts, memory, fixtures, examples, logs, traces, screenshots or templates.
