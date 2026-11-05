# Playbook: workspace readiness audit

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations).

Use this playbook to decide whether a workspace is ready for product-agent workflows.

## Inputs

- Workspace files, project rules, setup/build/test commands and source policy.
- Existing skills, automations, evals, sandbox and approval constraints.

## Outputs

- Readiness score, blockers, recommended docs/skill additions and first workflow to stabilize.
- Clear accepted gaps when evidence is missing but the owner accepts residual risk.

## Verification

The audit should remain read-only. It should name commands and evidence gaps without changing project files unless a later implementation slice is approved.

## Risks

- Treating an audit as proof of readiness can hide missing runtime evidence.
- Broad recommendations without a safe next action can expand scope unnecessarily.

## Inventory versus readiness

Skills/plugins/config presence is `present_unverified`. A runtime claim needs effective settings, supported client/authentication, skill exposure and an observed result. Use the [surface matrix](../codex/surfaces.md) and [skill diagnostics](../agent-systems/subagents-skills.md); an audit does not activate discovered assets.
