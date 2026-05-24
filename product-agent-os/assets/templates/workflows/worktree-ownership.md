# Worktree Ownership

Project: {project_name}
Profile: {profile_name}

## Inputs

- Workspace root: {workspace_path}
- Branch or worktree assumption:
- Active workers:
- Requested files:

## Process

- Avoid overlapping edits when multiple workers are active.
- Name owned files and files out of scope before editing.
- Check whether another worker owns the same path.
- Treat parallel writes to the same file, generated output, or shared config as a conflict.
- Stop on conflict and request coordination.

## Outputs

- File ownership map:
- Worker:
- Files owned:
- Files out of scope:
- Conflict notes:

## Verification

- Owned paths are explicit and project-scoped.
- Branch or worktree assumption is recorded.
- No worker edits outside its assigned ownership.

## Stop Conditions

- Ownership conflict exists.
- Workspace root is unclear.
- Required file is outside the approved scope.
