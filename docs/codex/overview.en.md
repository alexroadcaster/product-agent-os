# Codex Overview

Codex is an OpenAI coding agent that can read, modify and run code. In official materials, Codex is described as an agent for accelerating development, fixing bugs, understanding unfamiliar code and delegating tasks in local or cloud environments.

Source status: `official`  
Primary sources: [Codex cloud](https://developers.openai.com/codex/cloud), [Codex app](https://developers.openai.com/codex/app), [Codex CLI](https://developers.openai.com/codex/cli), [Codex IDE extension](https://developers.openai.com/codex/ide).

## Mental model

Codex is better treated not as autocomplete, but as a workflow operator:

- receives a task, context and readiness criterion;
- explores code, documents or data;
- makes changes or prepares an artifact;
- runs checks;
- returns a short result with evidence.

For advanced use, the key skill is not to "write a prompt", but to build a managed system: instructions, sources, skills, subagents, sandbox, approvals, memory and eval loops.

## What v1 of this knowledge base includes

| Area | What we study | Where to read |
| --- | --- | --- |
| Surfaces | App, CLI, IDE extension, cloud | [Work surfaces](surfaces.md) |
| Configuration | Approval policies, skill metadata, Codex MCP | [Configuration](configuration.md) |
| Security | Sandbox, approvals, network boundaries | [Security](security.md) |
| Workflows | Prompting, verification, handoff | [Workflows](workflows.md) |
| Agent systems | Subagents, skills, AGENTS.md, memory | [Architecture](../agent-systems/overview.md) |
| SDK layer | Agents SDK, Responses API, guardrails, tracing | [Agents SDK patterns](../agent-systems/sdk-patterns.md) |
| Insights | User tricks, hypotheses, experiments | [Insights](../insights/index.md) |

## Quality standards

Every instruction in the core knowledge base must have one of three statuses:

- a link to an official source;
- a link to a community source and explicit `trust_level`;
- a local hypothesis with a verification scenario.

Without this, a claim remains a note, not an instruction.

## Getting started

Start with the [surface matrix](surfaces.md), then choose the [ordinary/full workflow](../product-agent/lifecycle.md). Plugin support is separate from IDE capabilities; select a model with the [model matrix](models-and-reasoning.md).
