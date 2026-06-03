# Automations and GitHub

Source status: `official + experiment`  
Sources: [Codex automations](https://developers.openai.com/codex/app/automations), [Codex workflows](https://developers.openai.com/codex/workflows), [Codex best practices](https://developers.openai.com/codex/learn/best-practices).

Automation should come after a stable manual workflow or skill. GitHub workflows belong to CI/PR contexts when the repository owner has approved the trigger, permissions and rollback path.

## Inputs

- Stable workflow, owner, cadence, expected evidence and failure handling.
- GitHub or automation permissions, data policy and approval record.

## Outputs

- Automation candidate, GitHub workflow proposal or approved recurring check.
- Audit-ready evidence for what ran, where it wrote and how to disable it.

## Verification

Before activating automation, verify manual success evidence, input stability, output expectations and rollback/disable path.

## Risks

- A scheduled workflow without stable inputs can repeat bad decisions.
- GitHub permissions and external writes need least privilege and explicit approval.
