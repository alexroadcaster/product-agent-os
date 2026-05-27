# Automation Candidate

Project: {project_name}
name:
purpose:
trigger_or_cadence:
required_inputs:
candidate_only: true

## manual stability evidence

- Manual workflow runs:
- Successful manual workflow runs:
- Manual success evidence:
- Failures observed:
- Required approvals:
- Approval requirements:
- Value evidence:
- Minimum threshold: at least two successful manual workflow runs or `explicit_gap_accepted` with owner, reason, residual risk, follow-up condition, and why active automation is still not enabled.

## Stable Inputs And Outputs

- Inputs:
- Outputs:
- Invariants:

## Owner

- Accountable owner:
- Backup owner:
- Review cycle:

## Cadence

- Trigger:
- Frequency:
- Quiet hours or blackout windows:

## Verification

- Deterministic checks:
- Runtime checks:
- Evidence artifact:
- Alert condition:

## Failure Modes

- Known failure:
- Detection:
- Response:

## Rollback Or Disable Path

- Disable path:
- Rollback steps:
- State cleanup:

## Explicit Write Policy

- Allowed write targets:
- Forbidden write targets:
- External side effects:

## Explicit Approval

Automation must not be enabled until the owner records explicit approval, stable inputs, expected outputs, rollback or disable path, monitoring, and write policy.

## Readiness

readiness: candidate_only
candidate-only automation: true
active schedules remain out of scope until explicit approval and rollback/disable evidence exist.
