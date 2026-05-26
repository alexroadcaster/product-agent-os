# CI Permissions Review

Source status: `codex-plugin-template`

Use this for GitHub Actions, CI workflows, automation workflows, package release jobs and external action changes.

## Scope

- Change:
- Owner:
- Security/release reviewer:
- Workflow:
- Current Evidence:
- Accepted Gap:
- Residual Risk:

## Review

- Workflow triggers:
- Token permissions:
- Secrets:
- External actions:
- Action pinning:
- External action pinning:
- Artifacts:
- Cache:
- Environment approvals:
- Required reviewers:
- Wait timers:
- Branch/tag restrictions:
- Approval boundary:
- External writes:
- Release/publish capability:
- Remote CI mutation approval:
- Rollback/disable path:
- Verification:

Use least privilege. `approval_required` before broad token permissions, production deploy, package publish, external release or security-system mutation.

Do not include raw secrets, credentials, access tokens, private keys, payment data, raw PII, raw private chats or private customer data.
