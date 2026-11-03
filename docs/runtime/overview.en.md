# Runtime overview

Source status: `official + experiment`  
Sources: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex automations](https://developers.openai.com/codex/app/automations), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk).

Product-Agent OS chooses runtime by uncertainty, risk and approval boundary. Codex App and IDE extension fit steering and review; CLI and `codex exec` fit deterministic local checks; GitHub Action, MCP, Agents SDK and automation require clearer contracts.

## Inputs

- Work item, risk level, allowed commands and current approval policy.
- Available surfaces: Codex App, CLI, IDE extension, GitHub, MCP, Agents SDK and automation.

## Outputs

- A runtime decision with expected evidence and forbidden actions.
- A staged packet when live or external systems are proposed.

## Verification

Record the chosen runtime, command evidence and stop condition. Do not claim runtime behavior from code inspection alone.

## Risks

- Live server launch, browser automation, provider calls and git release actions need explicit approval.
- Automating before a workflow is stable can repeat unresolved failures.

## API runtime map and implementation level

[Agents API](https://developers.openai.com/api/docs/guides/agents) runs an OpenAI-managed Codex harness; Agents SDK runs the agent loop in the application; Responses API provides a direct API contract with optional hosted orchestration. [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) is a separate beta capability, not a synonym for Codex subagents.

Use the [SDK patterns table](../agent-systems/sdk-patterns.md) and [runtime diagram](../diagrams/runtime-decision-map.md) to choose state/tool/approval ownership. Product-Agent OS documents these routes; this refresh does not implement Agents API, async/steering or a new hosted runner. Documented, designed, implemented and runtime-verified are different evidence levels and do not automatically imply one another.
