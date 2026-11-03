# Worktrees, hooks and rules

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions).

Worktrees isolate larger changes. Hooks and rules can guide or block unsafe actions, but they should remain explicit, reviewable and aligned with sandbox and approvals.

## Product-Agent OS lifecycle hooks

Product-Agent OS ships staged hooks through `plugins/product-agent-os/assets/templates/hooks/` and `render_infrastructure.py --stage`. For an end project they land under `.codex/hooks/` as proposed/staged assets, not as silently activated automation.

The lifecycle guard works as follows:

- `SessionStart` reports control-plane and lifecycle file presence;
- `PreToolUse` allows read-only discovery through a fast path that does not read the marker, but blocks mutating or non-read-only commands without `.codex/product-agent-os/lifecycle-state.json`;
- the marker must be written only after a user-visible full field-list start brief and must contain `task_start_brief_shown`, `task_id`, `scope`, `updated_at`, `approval_boundary`, `brief_schema_version: task_start_brief_v1`, `brief_format: field_list`, `brief_digest`, and `brief_fields_present` with every required start brief field;
- the per-write `PostToolUse` comment-sufficiency advisory checks only paths from the current patch instead of rescanning the entire dirty worktree;
- after all writes, checks, and control-plane sync, the marker moves to `ready_for_completion_brief` and further mutations are denied;
- Project `Stop` is advisory: it does not validate chat format or request corrective continuation. Full scopes use start brief (9 fields) and Completion Ledger (13 items); ordinary work uses concise results, evidence and limits. Finish tools and control-plane sync before the terminal response. Explicit local packet validation does not prove activation.

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

## Current hook contract and activation diagnostics

Checked 2026-11-03: [Hooks reference](https://learn.chatgpt.com/docs/hooks). Non-managed hooks require review/trust for their current hash; new or changed definitions are skipped until trusted. A trusted project layer and valid JSON alone do not prove execution. `command` and `mcp_tool` handlers are supported; `prompt`/`agent` handlers are parsed but skipped. Multiple matching command hooks for one event may run concurrently: do not assume an ordering for shared-state writes.

| Event | Boundary |
| --- | --- |
| `SessionStart` | Startup context, not implementation acceptance |
| `PreToolUse` | A supported deny can prevent an action; callback failure is not guaranteed denial |
| `PostToolUse` | Post-action checking; cannot undo a completed side effect |
| `Stop` | Can request continuation; respect `stop_hook_active` to avoid loops |
| `SessionEnd`, `Interrupt` | Short best-effort lifecycle, not a long gate |

`timeout` is in seconds: usually default 600; `SessionEnd`/`Interrupt` default 1 and maximum 3. MCP uses the shorter hook/server timeout; elicitation waiting has separate semantics. Coverage depends on tool/event and runtime. Cloud-orchestrated enterprise remote MCP hooks have separate limits; a local command hook is not a universal cloud guardrail. Check the exact reference coverage row before relying on it.

Activation evidence needs client/runtime, loaded source, hash/trust, the actual event/tool, authorized scenario and observed outcome. JSON parsing, unit tests and direct script execution are local evidence, not fresh-session proof. The lifecycle parity implementation changes hook source; trust is unchanged and fresh-session activation remains unverified. The project Stop lifecycle above remains project policy, not universal OpenAI semantics.
