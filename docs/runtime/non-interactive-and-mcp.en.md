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
