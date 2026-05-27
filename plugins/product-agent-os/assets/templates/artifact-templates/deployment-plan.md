# Deployment Plan

Source status: `codex-plugin-template`

Use this before deployment, environment promotion, GitOps reconciliation or production configuration mutation.

## Scope

- Release:
- Owner:
- Target environment:
- Release candidate:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Deployment

- Deploy command:
- Approval:
- Rollout window:
- Stop criteria:
- Rollback/revert:
- Verification:

## Build-Release-Run Boundary

- Gate: `build_release_run_boundary_present`
- Immutable artifact:
- Release identifier:
- Runtime configuration boundary:
- Environment-specific config injection:
- Accepted platform exception:
- Rebuild-per-environment risk:

## GitOps / Desired State

- Desired-state source:
- Reconciliation controller:
- Drift behavior:
- Approval path:
- Rollback/revert:

Do not run deploy, reconcile or external mutation commands from this template alone. Keep external actions approval-bound.

Do not include raw secrets, credentials, access tokens, private keys, raw PII, raw private chats or private customer data.
