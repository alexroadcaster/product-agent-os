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
5. Preserve unrelated dirty changes.

## Outputs

- Ownership map:
- Conflicts:
- Sequential fallback:
- Evidence owner:
- Next agent:

## Stop Conditions

- Ownership conflict exists.
- Expected evidence is missing.
- A required file is outside the approved scope.
- Parallel work depends on raw conversation history instead of a fresh context handoff.

## Handoff

Return owned files, forbidden files, source constraints, expected evidence, stop conditions, and next role.
