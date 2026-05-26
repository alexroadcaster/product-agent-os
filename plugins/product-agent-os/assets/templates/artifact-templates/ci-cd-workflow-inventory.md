# CI/CD Workflow Inventory

Source status: `codex-plugin-template`

Use this before CI/CD workflow changes, release jobs, deploy jobs, package publishing or environment mutation.

## Scope

- Change:
- Owner:
- Reviewer:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Workflows

| Workflow names | Triggers | Permissions | Secrets | Environments | Artifacts | Cache | Concurrency |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Release Controls

- Required reviewers:
- Wait timers:
- Branch/tag restrictions:
- External action pinning:
- Remote CI mutation approval:
- External write capability:
- Package publish capability:
- Deploy capability:
- Rollback/disable path:

Use least privilege. `approval_required` before workflow changes that can publish, deploy, mutate environments or access production secrets.

Do not include raw secrets, credentials, access tokens, private keys, raw PII, raw private chats or private customer data.
