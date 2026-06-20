# Worktrees, hooks and rules

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://developers.openai.com/codex/config/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

Worktrees isolate larger changes. Hooks and rules can guide or block unsafe actions, but they should remain explicit, reviewable and aligned with sandbox and approvals.

## Product-Agent OS lifecycle hooks

Product-Agent OS ships staged hooks through `plugins/product-agent-os/assets/templates/hooks/` and `render_infrastructure.py --stage`. For an end project they land under `.codex/hooks/` as proposed/staged assets, not as silently activated automation.

The lifecycle guard works as follows:

- `SessionStart` reports control-plane and lifecycle file presence;
- `PreToolUse` allows read-only discovery but blocks mutating or non-read-only commands without `.codex/product-agent-os/lifecycle-state.json`;
- the marker must be written only after a user-visible start brief and must contain `task_start_brief_shown`, `task_id`, `scope`, `updated_at`, and `approval_boundary`;
- `PostToolUse` and `Stop` remind the agent to record evidence, update `RUNLOG.md`, run control-plane sync, and show a user-visible completion brief.

The marker is not a transcript store: do not put raw chat, secrets, private source bodies, private customer data, or credentials in it. Hook activation remains a separate approval boundary.

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
