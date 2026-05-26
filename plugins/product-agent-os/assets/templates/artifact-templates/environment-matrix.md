# Environment Matrix

Source status: `codex-plugin-template`

Use this to record release targets, approval boundaries, secret boundaries and GitOps desired-state operations.

## Scope

- Release:
- Owner:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Targets

| Target | Owner | Approval path | Branch/tag rules | Secret boundaries | External write |
| --- | --- | --- | --- | --- | --- |
| Dev |  |  |  |  |  |
| Stage |  |  |  |  |  |
| Prod |  |  |  |  |  |
| Local |  |  |  |  |  |
| Mobile |  |  |  |  |  |
| Store |  |  |  |  |  |
| Registry |  |  |  |  |  |

## GitOps Desired State

- Desired-state source:
- Reconciliation controller:
- Drift behavior:
- Approval path:
- Rollback/revert:
- GitOps status: `present_unverified | owner_evidence_present | accepted_gap`

Detection of GitOps files is `present_unverified` until owner evidence records source, controller, drift, approval and rollback/revert behavior.

Do not include raw secrets, credentials, access tokens, private keys, raw PII, raw private chats or private customer data.
