# Agent And Session Control

Source status: `official + experiment`  
Sources: [Agents SDK sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Codex memories](https://developers.openai.com/codex/memories), [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Purpose Of Session Control

Session control is needed so the agent does not turn accumulated dialogue into unverifiable memory. A session should preserve useful continuity, but it must not replace retrieved context, the source registry, or project rules.

## Session Boundary

Every session should have:

```yaml
session_id: ""
goal: ""
allowed_sources: []
memory_policy: "none | session_only | project_memory"
tool_policy: ""
handoff_policy: ""
freshness_required: true
exit_criteria: []
```

A refinement should preserve relevant state and constraints; use an explicit new-session boundary for an incompatible goal. See steering and compaction below.

## When to use Manager pattern

Start with one agent. When independent subtasks justify coordination and evals show value, Manager pattern assigns responsibilities:

- Manager holds the source policy and final answer.
- Specialist agents perform bounded subtasks.
- Verifier agent checks claims.
- Only Manager publishes the result to the user.

Keep Handoff pattern for cases where the next agent must conduct an independent long-running interaction.

## Handoff Contract

Minimal handoff payload:

```yaml
goal: ""
constraints: []
allowed_sources: []
context_summary: ""
verified_claims: []
unsupported_claims: []
open_questions: []
tools_used: []
risks: []
next_agent_task: ""
```

Passing a handoff without `constraints` and `allowed_sources` is forbidden: it is the main path to context drift.

## Session Hygiene

Rules:

- Refresh retrieved context before an important factual answer.
- After a long session, write a summary with decisions, sources, and unresolved questions.
- Do not store raw chain of thought, secrets, or temporary guesses.
- Do not use session memory as a citation source.
- When the topic changes, clear irrelevant context.

## Guardrails For Sessions

| Guardrail | Trigger | Action |
| --- | --- | --- |
| Missing source | Claim without citation | Send to verifier or request retrieval |
| Context drift | Answer relies on an old assumption | Repack context |
| Tool overreach | Agent asks for broad permissions | Request granular approval |
| Handoff loss | Payload without constraints | Reject handoff |
| Session bloat | Too much irrelevant history | Summarize or compact; reset only with an explicit boundary |

## Tracing Questions

For every agent run, record:

- Which sources did the agent see?
- Which tools were actually called?
- Which assumptions were chosen?
- Which claims were verified?
- Where did fallback/refusal occur?
- Which eval proves quality?

## Async tools and steering

Checked 2026-11-03: [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling), [Steering](https://developers.openai.com/api/docs/guides/steering). These are documented API capabilities, not new Product-Agent OS activation.

`async: true` on a supported function/custom tool lets the model continue independent work while the application executes the tool. OpenAI does not execute that tool for the app. Return output with the original `call_id`; async is not Background mode and does not automatically apply to hosted tools or Programmatic Tool Calling.

| State | Application responsibility / proposed contract |
| --- | --- |
| Pending | Keep call_id, owner, deadline and authorized side effects; do not declare dependent output complete |
| Completed | Match output to its call and apply the result once |
| Failed / timeout | Return explicit failure; decide retries by idempotency and budget |
| Duplicate / late | Check identity, current task relevance and prior application; do not repeat side effects |

Responses WebSocket mid-turn steering uses `response.steer`. A queue acknowledgement means accepted, not applied. Track response continuation and the `steered` reason; do not claim an update was handled without evidence. Steering does not undo completed actions or already running tools. Before the next side effect, the application reconciles updated scope and pending calls. Final output requires mandatory dependencies to complete or their absence to be explicitly reflected in the result.

## Reasoning updates and compaction

Sources: [Reasoning](https://developers.openai.com/api/docs/guides/reasoning), [Compaction](https://developers.openai.com/api/docs/guides/compaction). In supported standard single-agent GPT-6 Responses conversations, `configuration_update` can change effort between responses while preserving request-level `reasoning.effort` and the original prefix. The change persists until another update; response-level effort may report the original setting rather than the applied update.

| Mechanism | Compatibility / action |
| --- | --- |
| `configuration_update` | Supported single-agent mode; not universal across runtimes |
| Automatic compaction/truncation | Do not combine with configuration updates |
| Standalone `/responses/compact` | Rejects histories containing configuration updates |
| Explicit `compaction_trigger` | After compaction, restate all changed settings in a new update before the next user message |
| Server-side compaction | `context_management` and `compact_threshold`; opaque encrypted item, not an ordinary summary |

A task refinement does not automatically require reset. Preserve goal, constraints, decisions and pending calls; start a new session for independent scope or fresh settings loading when needed. Compaction, manual summary and cross-session memory have different contracts. Preserve returned state items and required fields when managing history manually; do not request private chain-of-thought.

A Verifier role does not guarantee independent review or eliminate hallucinations. Compare against a single-agent baseline; handoffs add nondeterministic boundaries. [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
