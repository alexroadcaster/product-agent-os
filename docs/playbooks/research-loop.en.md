# Playbook: multi-agent research loop

Source status: `official + experiment`  
Sources: [Codex subagents](https://developers.openai.com/codex/concepts/subagents), [Codex workflows](https://developers.openai.com/codex/workflows), [Agent Skills](https://developers.openai.com/codex/skills).

## Goal

Create a managed research loop for updating the knowledge base: source discovery, separation of official facts from community signals, claim verification and release of a documentation change.

## When to use

- A new Codex changelog entry appeared.
- A section needs to be added for a new capability.
- There is a community trick that may be useful but needs verification.

## Single-agent mode

```text
Research the topic "{topic}" for the Codex knowledge base.

Do:
1. Find official OpenAI sources.
2. Create source cards.
3. Separate community claims from official claims.
4. Propose documentation changes.
5. Name verification commands.
Do not mix unverified tricks with official instructions.
```

## Parallel mode

Use only when you explicitly want subagents:

```text
Use parallel subagents for this research task.

Agent 1: official Codex docs.
Agent 2: Agents SDK docs for memory/orchestration.
Agent 3: community insight backlog.

Each agent returns verified claims, uncertain claims, and source cards.
Wait for all agents. Then synthesize one update plan and do not include raw logs.
```

## Acceptance criteria

- New official claims have source cards.
- Community claims live only in `docs/insights/`.
- Every proposed edit has verification status.
- MkDocs build passes.

## Context7 enrichment

When the topic is related to OpenAI SDK, Responses API, Codex or Agents SDK, add a separate pass through [Context7 deep research](context7-deep-research.md). Its goal is to find SDK-level details: primitives, method contracts, tool types, structured output examples and observability patterns. After retrieval, still update the source registry instead of inserting unsigned claims directly.

