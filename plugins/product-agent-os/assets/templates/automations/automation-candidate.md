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
- Owner approval:
- Value evidence:
- Accepted residual risks:
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
Activation also requires accepted residual risks and a separate approval packet for any schedule, hook activation, GitHub Actions workflow, Codex App automation, external write or other privileged operation.

## Professional Code Authoring Candidate Gate

Use this gate when the candidate would update coding-standard templates, skills,
evals, hook-governance candidates or learning-loop candidate generation.

- Candidate policy: candidate_only
- Minimum manual successful runs: 3
- Owner review: required before apply
- Rollback evidence: required before apply
- False-positive audit: required before apply
- Flake replay: required before apply
- Cost check: required before apply
- Forbidden current slice: auto-apply, active schedule, hook activation, provider call, global config mutation, target workspace mutation, raw transcript storage, hidden telemetry, external write.

## Future Activation Handoff

activation_gate:

- activation requirements: at least two successful manual workflow runs, deterministic command evidence, owner approval, rollback or disable plan, accepted residual risks and no active runtime markers.
- future_activation_handoff_required: true
- schedule_status remains not_created until a separate owner-approved activation slice records otherwise.
- no GitHub Actions, Codex App automation, hook activation or external write is performed by this candidate packet.

## Readiness

readiness: candidate_only
candidate-only automation: true
active schedules remain out of scope until explicit approval and rollback/disable evidence exist.
