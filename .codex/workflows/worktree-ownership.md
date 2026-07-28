# Worktree Ownership

Source status: project-local system workflow.

## Purpose

Keep autonomous agents from editing overlapping files or treating generated surfaces as source truth.

## Inputs

- Workspace root:
- Active agent:
- Task:
- Owned files:
- Forbidden files:
- Shared files:
- Expected evidence:
- Handoff output schema:

## Process

1. Name owned and forbidden paths before edits.
2. Treat root control-plane files, `.codex` system files, generated status outputs, public contracts, release files, and source registries as shared-risk surfaces.
3. Use sequential fallback when two agents need the same path or public contract.
4. Require a fresh context handoff before any parallel write.
5. Require a Subagent Context Packet before launch for every subagent or read-only sidecar.
6. Require a Subagent Result Packet after completion, timeout, cancellation, or close.
7. The Agent Handoff / Context Packet must record role, `fork_turns`, prompt, allowed files, files actually read, and outputs.
8. Preserve unrelated dirty changes.

## Outputs

- Ownership map:
- Conflicts:
- Sequential fallback:
- Evidence owner:
- Next agent:
- Subagent Context Packet before launch:
- Subagent Result Packet after completion:
- Agent Handoff / Context Packet:
- Role:
- `fork_turns`:
- Prompt:
- Allowed files:
- Files actually read:
- Outputs:

## Stop Conditions

- Ownership conflict exists.
- Expected evidence is missing.
- A required file is outside the approved scope.
- Parallel work depends on raw conversation history instead of a fresh context handoff.
- Subagent launch is missing a Subagent Context Packet.
- Subagent completion is missing a Subagent Result Packet.
- role, `fork_turns`, prompt, allowed files, files actually read, or outputs are missing.

## Handoff

Return owned files, forbidden files, source constraints, expected evidence, stop conditions, and next role.

For subagents, also return the linked Subagent Context Packet and Subagent Result Packet.
