# Agent And Session Control

Source status: `official + experiment`  
Sources: [Agents SDK sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Codex memories](https://developers.openai.com/codex/memories), [Codex subagents](https://developers.openai.com/codex/subagents).

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

If the goal changed, it is better to create a new session or explicitly reset context.

## Manager Pattern As Default

To reduce hallucinations, use Manager pattern:

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
| Session bloat | Too much irrelevant history | Summarize and reset |

## Tracing Questions

For every agent run, record:

- Which sources did the agent see?
- Which tools were actually called?
- Which assumptions were chosen?
- Which claims were verified?
- Where did fallback/refusal occur?
- Which eval proves quality?
