# Agents SDK Patterns

Source status: `official + experiment`
Sources: [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python), [Agents SDK JS sessions](https://openai.github.io/openai-agents-js/guides/sessions/), [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses).

## Core Primitives

Agents SDK is useful when you need to move from a manual Codex workflow to a programmable agent system. Context7 highlights a minimal set of primitives:

| Primitive | Role | Documentation meaning |
| --- | --- | --- |
| `Agent` | LLM with instructions and tools | Unit of specialization |
| Tools | External actions or capabilities | Function tools, hosted tools, MCP tools, agents-as-tools |
| Handoffs | Transfer of control to another agent | Decentralized routing |
| Guardrails | Checking inputs/outputs | Policy, safety, schema, quality gates |
| Sessions | Conversation persistence | Application dialogue memory |
| Tracing | Debugging and monitoring | Visibility into decisions, tools, latency, failures |

## Manager Pattern

Manager pattern: a central orchestrator calls specialized agents as tools and keeps control over the workflow.

Use it when:

- the result needs a single owner;
- constraints, source policy, and acceptance criteria matter;
- several agents may produce conflicting conclusions;
- the final text or code must be reconciled.

```mermaid
flowchart TD
    M["Manager Agent"] --> R["Research as tool"]
    M --> V["Verifier as tool"]
    M --> W["Writer as tool"]
    M --> Q["QA as tool"]
    R --> M
    V --> M
    W --> M
    Q --> M
    M --> O["Final answer / docs change"]
```

For this knowledge base, Manager pattern is the default.

## Handoff Pattern

Handoff pattern: an agent transfers control to another specialized agent. This is closer to routing than to a tool call.

Use it when:

- there are different domains with independent policies;
- the next agent must conduct a long interaction;
- the user request explicitly changes mode, for example docs research -> implementation -> review.

Risk: if the handoff is poorly described, global context is lost. Therefore, the handoff payload must include goal, constraints, sources, decisions, and open questions.

## Responses API As A Low-Level Layer

Responses API is suitable when direct API-level control is needed:

- explicitly define tools;
- get structured output by JSON Schema;
- manage streaming;
- use built-in tools;
- build a custom loop around model/tool responses.

Example contract-first output for agent handoff:

```json
{
  "type": "json_schema",
  "name": "agent_handoff",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "goal": { "type": "string" },
      "constraints": { "type": "array", "items": { "type": "string" } },
      "sources": { "type": "array", "items": { "type": "string" } },
      "claims": { "type": "array", "items": { "type": "string" } },
      "risks": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["goal", "constraints", "sources", "claims", "risks"],
    "additionalProperties": false
  }
}
```

## Layer Selection

| Need | Choose |
| --- | --- |
| Quickly complete a local engineering task | Codex App / CLI |
| Repeatable workflow without code | Skill + `AGENTS.md` |
| Parallel research in the current session | Codex subagents |
| Production agent app | Agents SDK |
| Full control over the wire contract | Responses API |
