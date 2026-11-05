# Worktrees, hooks and rules

Source status: `official + experiment`  
Sources: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions).

Worktrees isolate larger changes. Hooks and rules can guide or block unsafe actions, but they should remain explicit, reviewable and aligned with sandbox and approvals.

## GAP-05: exact report authority — 2026-11-05

Optional pinned report authority permits one new Markdown file through a grant pinned by SHA-256 in the trusted hook command: `--report-authority` and `--report-authority-sha256`. Research/review/planning markers grant no writes by default; tool payload cannot supply authority.

The grant binds workspace digest, new/previous task IDs, exact marker bytes, output path and expiry of at most 24 hours. It requires a fresh/nonterminal marker with an explicit task transition. One literal `apply_patch` Add File is accepted, direct or a single literal call within `functions.exec`. Existing/neighbor paths, control-plane/config/hooks, traversal/symlinks, dynamic/multiple calls and shell writes are denied. Pinned-mode shell reads are limited to literal `Get-Content`/`Get-ChildItem -LiteralPath 'path'` with `login: false`; other commands require review.

This is a preflight guard, not an atomic filesystem transaction. Sandbox, secret/path/command restrictions and host approvals remain intact. Active/package sources are synchronized; `hooks.json`, trust and cache are unchanged. A fresh-host positive/negative probe remains a separate gate. Next artifact: an exact-hash approval packet and authorized probe receipt. Active/package `task-plan-lifecycle.md` defines the grant; rollback restores only this slice's source changes without modifying trust.

## Product-Agent OS lifecycle hooks

Product-Agent OS ships staged hooks through `plugins/product-agent-os/assets/templates/hooks/` and `render_infrastructure.py --stage`. For an end project they land under `.codex/hooks/` as proposed/staged assets, not as silently activated automation.

The lifecycle guard works as follows:

- `SessionStart` reports control-plane and lifecycle file presence;
- `PreToolUse` allows read-only discovery through a fast path that does not read the marker, but blocks mutating or non-read-only commands without `.codex/product-agent-os/lifecycle-state.json`;
- Before mutation show the applicable scope: large/high-risk/material/release work uses `task_start_brief_v2`, `brief_format: bold_fields` and nine fields; ordinary work uses `task_scope_note_v1`, `brief_format: concise`, and Scope/Evidence/Limits. Then record task_id, scope, updated_at, approval_boundary, brief_digest and brief_fields_present in the marker; `task_start_brief_shown` applies only to the full route. `task_start_brief_v1` / `field_list` remains compatible with already-started legacy sessions.
- the per-write `PostToolUse` comment-sufficiency advisory checks only paths from the current patch instead of rescanning the entire dirty worktree;
- after all writes, checks, and control-plane sync, the marker moves to `ready_for_completion_ledger` (full) or `ready_for_completion_brief` (concise/legacy) and further mutations are denied;
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

Activation evidence needs client/runtime, loaded source, hash/trust, the actual event/tool, authorized scenario and observed outcome. JSON parsing, unit tests and direct script execution are local evidence, not fresh-session proof. The 2026-11-03 receipt records `verified_local_runtime` for the tested Desktop routes: large, ordinary and terminal-marker denial. ACT-F1..F6 are resolved in source-owned `lifecycle_parity.repair`; this is a dated run, not a new test of this page. Silent Stop execution and completeness across all mutation channels are not proven. [Current evidence boundary](../product-agent-os/control-plane-current-state.md). The project Stop lifecycle above remains project policy, not universal OpenAI semantics.

## Trust and execution boundaries

Checked 2026-11-05 against [Hooks](https://learn.chatgpt.com/docs/hooks). Applicable hook sources are merged; a nearer file does not replace all earlier hooks. Matching command hooks can start concurrently. Definition or bundled plugin script changes require another review; installed/enabled does not mean trusted/executed.

An MCP hook uses an already available server: it does not start or reconnect MCP. A missing server/tool or MCP-hook error does not guarantee denial; verify fail-closed behavior separately. Cloud-orchestrated Work does not support local command/plugin hooks; supported admin-managed MCP hooks are configured separately.

A worktree separates Git working files, not permissions. A small change usually fits the current workspace. Choose Git-only worktrees, setup and Handoff through the [official route](https://learn.chatgpt.com/docs/environments/git-worktrees) and project authority. Verify loaded definition and trust, an allowed case, a denied case, and evidence for the specific tool/runtime.
