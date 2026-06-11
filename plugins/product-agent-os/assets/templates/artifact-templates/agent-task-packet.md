# Agent Task Packet

Use this as the fresh-context handoff for any subagent or parallel worker. The packet must be complete enough for the worker to act without raw conversation history.

For Codex subagents, pair this task packet with a Subagent Context Packet before launch and a Subagent Result Packet after completion. The Agent Handoff / Context Packet must name role, `fork_context`, prompt, allowed files, files actually read, and outputs.

## Task

- Goal:
- Lifecycle state:
- Usage mode:
- Task row id:
- Owner:
- Recommended role:
- Dependency status:

## Full Context

- Source/context used:
- Complete task context:
- Source constraints:
- Allowed sources:
- Inputs used:
- Requirements:
- Acceptance criteria:
- Architecture boundary:
- Files already reviewed:
- Assumptions:

## Ownership

- Owned files:
- Files out of scope:
- Forbidden files:
- Owned/forbidden files:
- Shared resources:
- Cross-agent file ownership:
- Conflict notes:
- Shared ownership ambiguity:
- Worktree required for shared generated files, contracts, migrations, public APIs, schemas, release files, or rollback-sensitive work:
- Read-only research exception:

## Execution Contract

- Allowed actions:
- Subagent Context Packet before launch:
- Subagent Result Packet after completion:
- Agent Handoff / Context Packet:
- Role:
- `fork_context`:
- Prompt:
- Allowed files:
- Files actually read:
- Outputs:
- Approval requirements:
- Commands to run:
- Expected evidence:
- Accepted gaps:
- Documentation impact:
- Docs update path assigned:
- Rollback notes:
- Handoff output schema:

## Planning Control Governance

Hard gates live in validator/tests/skills. Hooks are reminder-only unless approved, and closure cannot claim readiness from hook reminders alone.

- Planning control governance:
- File/subsystem boundaries:
- No hook activation:
- No automation activation:
- No MCP activation:
- No Agents SDK runner:
- No external writes:

## Runtime Methodology Packet

Carry only the compact runtime methodology packet. Do not include raw conversation history; no raw conversation history belongs in this handoff.

- Runtime methodology packet:
- `methodology_packet`:
- Owner domain:
- Consumer domains:
- `finish_options`:
- Safe next action:
- Approval requirements:
- Evidence gaps:
- Stop conditions:

## AI/RAG Handoff Compatibility

- Legacy alias: `agent-handoff-contract.md` maps to this agent task packet.
- Handoff owner:
- Inputs:
- Output schema:
- Trace evidence:
- Stop condition:

## Stop Conditions

- Owned files are unclear.
- Required context is missing.
- Source constraints are missing.
- Handoff output schema is missing.
- Missing handoff schema.
- Expected evidence is missing.
- Shared ownership ambiguity exists.
- Cross-agent file ownership exists.
- Approval is required and not present.
- Verification command cannot run and no accepted gap exists.
- Secret-bearing or customer data is needed.
- Parallel work is requested without this agent task packet.
- Auto subagent dispatch is requested.
- Overlapping ownership parallelism is unresolved.
- Raw chat history is needed.
- Do not advance to parallel work until the packet is complete.

## Sequential Fallback

- Sequential fallback:
- Reason parallel work is unsafe:
- Coordination needed before retrying parallel work:

## Scenario Handoff

Keep the handoff concise enough for the next role to act without reading raw conversation history.

- Sources/context used:
- Assumptions:
- Files touched:
- Files proposed:
- Commands run:
- Verification evidence:
- Unsupported claims:
- Open risks:
- Recommended next role:
- Stop reason:
- Next agent task:
