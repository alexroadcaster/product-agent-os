# Worktree Ownership

Project: {project_name}
Profile: {profile_name}

## Inputs

- Workspace root: {workspace_path}
- Branch or worktree assumption:
- Active workers:
- Requested files:
- Fresh-context handoff:
- Complete task context:
- Source constraints:
- Allowed sources:
- Inputs used:
- Expected evidence:
- Handoff output schema:

## Process

- Avoid overlapping edits when multiple workers are active.
- Name owned files and files out of scope before editing.
- Check whether another worker owns the same path.
- Treat parallel writes to the same file, generated output, or shared config as a conflict.
- Require worktrees or explicit ownership for write-heavy subagent tasks, shared generated files, contracts, migrations, public APIs, schemas, release files, or rollback-sensitive work.
- Read-only research can use an agent task packet without a worktree when no writes, external actions, MCP activation, hooks, or automation are requested.
- Require the agent task packet artifact for any subagent or parallel worker before parallel work starts.
- Require a Subagent Context Packet before launch for every subagent or read-only sidecar.
- Require a Subagent Result Packet after completion, timeout, cancellation, or close.
- The Agent Handoff / Context Packet must record role, `fork_turns`, prompt, allowed files, files actually read, and outputs.
- Check that owned files, forbidden files, source constraints, expected evidence, stop conditions, and handoff output schema are explicit per worker.
- Do not advance to parallel work when shared ownership ambiguity, missing handoff schema, missing expected evidence, raw conversation history dependency, or cross-agent file ownership remains.
- Stop on conflict and request coordination.

## Outputs

- File ownership map:
- Worker:
- Files owned:
- Owned files:
- Forbidden files:
- Files out of scope:
- Expected evidence:
- Stop conditions:
- Handoff output schema:
- Sequential fallback:
- Conflict notes:
- Shared ownership ambiguity:
- Missing handoff schema:

## Verification

- Owned paths are explicit and project-scoped.
- Branch or worktree assumption is recorded.
- No worker edits outside its assigned ownership.
- Fresh-context handoff is complete for each subagent or parallel worker.
- Subagent Context Packet exists before launch.
- Subagent Result Packet exists after completion.
- role, `fork_turns`, prompt, allowed files, files actually read, and outputs are recorded.
- Complete task context is enough to avoid raw conversation history.
- Sequential fallback is recorded when ownership cannot be split.

## Stop Conditions

- Ownership conflict exists.
- Shared ownership ambiguity exists.
- Missing handoff schema.
- Expected evidence is missing.
- Source constraints are missing.
- Cross-agent file ownership exists.
- Parallel work without task packet.
- Workspace root is unclear.
- Required file is outside the approved scope.
