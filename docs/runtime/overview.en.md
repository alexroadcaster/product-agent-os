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
