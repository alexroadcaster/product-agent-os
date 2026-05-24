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

- Preserve durable decisions while removing transient noise.
- Keep hot context needed for the next action.
- Move warm context into concise summaries.
- Propose cold context for archive only when evidence remains discoverable.
- Preserve failures, exit codes, files touched, verification evidence, and open risks.
- Respect privacy boundaries; do not keep private data or unnecessary raw logs.

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
