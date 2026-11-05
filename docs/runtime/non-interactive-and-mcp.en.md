# Non-interactive Codex and MCP

Source status: `official + experiment`  
Sources: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python).

Non-interactive Codex runs are useful when the prompt contract is stable and verification is deterministic. MCP and Agents SDK orchestration are useful when the integration contract, permissions and audit evidence are explicit.

## Inputs

- A stable prompt, workspace path, sandbox policy and verification command.
- MCP server or Agents SDK contract when orchestration is needed.

## Outputs

- Deterministic command output, staged artifacts or an orchestration packet.
- Evidence that the run stayed inside approved filesystem, network and tool boundaries.

## Verification

Run non-interactive jobs with explicit commands and inspect output before making a completion claim.

## Risks

- Non-interactive mode is a poor fit for ambiguous first-run work.
- MCP and Agents SDK tools can cross trust boundaries unless permissions and approvals are explicit.

## MCP and API: separate boundaries

[Custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) inherit parent MCP. An agent-local declaration neither overrides parent MCP nor proves tool availability. Inspect effective configuration and observed tool results in an authorized runtime; documentation changes activate no server.

Command network policy is not a policy for web search, connectors, MCP or browser tools. Each needs its own controls and authorized scope; see [security](../codex/security.md). Do not transfer API parameters into the CLI runner: [API compatibility](../agent-systems/sdk-patterns.md) applies to the corresponding endpoint. The current runner is not replaced with Responses or Agents API.

## Distinguish two MCP routes

Codex as an MCP server executes work for an external orchestrator; an MCP server connected to Codex supplies tools to it. These are different roles and policy boundaries. `codex exec --json` emits JSONL events; `--output-schema` defines the final result contract. Turn completion is not successful task verification. Preconfigure allowed policy for a noninteractive route and handle unavailable approval as an explicit failure. [Non-interactive mode](https://developers.openai.com/codex/noninteractive).
