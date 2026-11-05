# Memory In Codex And Agents SDK

Source status: `official`  
Sources: [Codex memories](https://developers.openai.com/codex/memories), [Agents SDK sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [Agents SDK sandbox agent memory](https://openai.github.io/openai-agents-js/guides/sandbox-agents/memory/), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md).

## Four different context layers

| Layer | What it stores | Where to use it | Do not use as |
| --- | --- | --- | --- |
| `AGENTS.md` | Mandatory project instructions | Team rules, test commands, coding standards | Personal notes or transient state |
| Codex Memories | Useful local context from past threads | Preferences, recurring workflows, pitfalls | The only source of mandatory rules |
| Agents SDK Sessions | Conversation history for app-level agents | Multi-turn apps and agent runners | Long-term knowledge base |
| Sandbox Agent Memory | Lessons from prior sandbox-agent runs in workspace files | Repeated agent workflows and run summaries | Secret storage or unverifiable truth |

## Recommendations

- Keep mandatory instructions in applicable `AGENTS.md`; load ordinary checked-in documentation explicitly through references or task context.
- Use Memories as a supporting recall layer.
- Use session memory for conversation continuity inside the application.
- Isolate sandbox memory with layouts when different agents should not share experience.
- Treat every memory artifact as retained data: do not store secrets, and review it before handoff.

## Memory Architecture For This Project

```mermaid
flowchart LR
    A["AGENTS.md / checked-in docs"] --> M["Main agent prompt"]
    C["Codex memories"] --> M
    S["Agents SDK Session"] --> App["Runnable future app"]
    B["Sandbox agent memory"] --> Worker["Future sandbox agents"]
    M --> KB["Knowledge base edits"]
    Worker --> KB
```

## Update Policy

1. Put a mandatory rule in applicable `AGENTS.md`; supporting docs require explicit loading.
2. If it is a personal user preference, it may go into memory.
3. If it is a conclusion from an experiment, it goes into `docs/insights/` with `experiment` status.
4. If memory conflicts with the current repository or official docs, trust the current state and sources.

## Memory vs Observability

Memory answers the question "what should be preserved for the next step or next session." Observability answers the question "why did the agent do this specific thing." Production agent systems need both layers:

- session memory stores conversation continuity;
- workspace memory stores lessons and run summaries;
- tracing stores tool calls, handoffs, latency, and failures;
- source registry stores the verifiable basis for claims.

Do not replace tracing with memory: when a failure needs investigation, you need an event trail, not only a final note.

## Manage local Codex memory

Checked 2026-11-05: [Memories](https://developers.openai.com/codex/memories). ChatGPT web memory and local Codex memory use different stores and controls. In supported desktop/TUI surfaces use `/memories` to choose whether a chat may read existing memories and contribute to new ones. Chat-level choices do not change global settings.

Desktop **Settings → Personalization → Enable Codex memories** controls the local feature. **Allow memories from tool-assisted chats** controls those chats' eligibility for generation. Configuration separates `memories.use_memories` and `memories.generate_memories`; external-context eligibility is separate. Generation is asynchronous: ending a chat does not imply an immediate write.

Stores under `CODEX_HOME` include `memories/` and `memories_v2/`. Migration behavior depends on client and settings; an existing v1 store is not a failure. Troubleshoot both directories, client/version, use/generate and eligibility. Generated files are not the primary interface for editing mandatory rules.

**Delete Codex memories** resets the selected local store and can also clear Computer History on supported machines. This is a separately authorized action, not an automatic repair. Do not store secrets; review retained data before sharing artifacts.

`AGENTS.md` follows [discovery rules](https://learn.chatgpt.com/docs/agent-configuration/agents-md); an ordinary repository document does not become an instruction merely by existing. Sessions, sandbox memory and traces remain distinct application layers.
