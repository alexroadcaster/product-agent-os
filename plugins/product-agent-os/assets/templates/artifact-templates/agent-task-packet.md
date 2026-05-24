# Agent Task Packet

Use this as the fresh-context handoff for any subagent or parallel worker. The packet must be complete enough for the worker to act without raw conversation history.

## Task

- Goal:
- Lifecycle state:
- Usage mode:
- Owner:
- Recommended role:

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
- Shared resources:
- Cross-agent file ownership:
- Conflict notes:
- Shared ownership ambiguity:

## Execution Contract

- Allowed actions:
- Approval requirements:
- Commands to run:
- Expected evidence:
- Accepted gaps:
- Documentation impact:
- Rollback notes:
- Handoff output schema:

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
