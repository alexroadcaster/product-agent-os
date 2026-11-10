# Runlog Compaction

Project: {project_name}
Profile: {profile_name}

## Inputs

- Current RUNLOG.md:
- Hot context:
- Warm context:
- Cold context:
- Privacy boundaries:

## Process

- Measure UTF-8 bytes: warning 32 000, hard 40 000; retain stricter project limits.
- Preserve detailed task matrices under `docs/planning/` intact: default size alone is not a compaction trigger. Index/README/control-plane files retain budgets. Explicit per-file limits, content/link checks and exact apply authority remain applicable.
- Preserve durable decisions and original evidence bytes; do not delete history.
- Keep hot context needed for the next action.
- Keep summaries as navigation only; move exact original blocks to named owning artifacts.
- Propose cold context for archive only when evidence remains discoverable.
- Preserve failures, exit codes, files touched, verification evidence, and open risks.
- Respect privacy boundaries; do not keep private data or unnecessary raw logs.
- Propose source/destination hashes, byte ranges, retention owner/reason, diff, forecast and recovery map. Snapshot dirty/untracked input locally within the source privacy boundary.
- Apply only the exact reviewed manifest under explicit authority and one writer. Reject stale inputs, aliases and unresolved links; verify budgets and exact-byte recovery before completion.
- Keep the journal. After interruption, confirm the writer has stopped before explicit recovery; never clear a lock by age or overwrite later edits.
- Recheck after every changed-document update; no automatic cleanup, hook activation or schedule.

## Outputs

- Hot context summary:
- Warm context summary:
- Cold archive proposal:
- Evidence preservation notes:
- Privacy redactions:

## Verification

- Decisions and rationale remain recoverable.
- Evidence paths or command summaries are preserved.
- Archive proposal does not remove active blockers.

## Stop Conditions

- Evidence would be lost.
- Privacy boundary is unclear.
- Next owner cannot continue from the compacted summary.
