# Worktrees, hooks and rules

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://developers.openai.com/codex/config/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

Worktrees isolate larger changes. Hooks and rules can guide or block unsafe actions, but they should remain explicit, reviewable and aligned with sandbox and approvals.

## Inputs

- Change scope, branch/worktree policy, file ownership and approval boundary.
- Hook or rule proposal with trigger, allowed action and failure handling.

## Outputs

- Isolated workspace plan, hook proposal or durable rule update.
- Clear guidance on what requires explicit owner approval.

## Verification

Check that worktrees do not hide conflicting edits and hooks do not activate without approval.

## Risks

- Creating branches or worktrees without owner approval can conflict with project rules.
- Hooks can block valid work or mutate state unexpectedly if they are too broad.
