# System File Hygiene Audit Automation Candidate

Automation type: system-file-hygiene
Readiness: candidate_only

## Owner

- Accountable owner: Project operator
- Backup owner:
- Review cycle: weekly report, monthly deep review

## Cadence

- Trigger: manual only until explicit approval
- Frequency: weekly full audit plus monthly deep ownership review
- Event triggers: on system-file change, size threshold crossing, release preparation, automation approval review

## Stable Inputs

- Inputs: root control-plane files, `README.md`, nested `AGENTS.md`, `.codex/agents`, `.codex/skills`, `.codex/workflows`, `.codex/artifact-templates`, `.codex/evals`, `.codex/hooks`, `.codex/automation-candidates`, docs source files, repository governance files and plugin package control files

## Stable Outputs

- Outputs: JSON hygiene audit, staged `system-file-hygiene-report.md`, optional compaction candidates and owner review notes

## Verification

- Deterministic checks: python plugins\product-agent-os\scripts\validate_system_file_hygiene.py <workspace>
- Successful manual workflow runs: 0
- Owner approval:
- Accepted residual risks:

## Failure Modes

- Known failure: a file crosses hard size limit, contains secret-like literals, contains active schedule markers inside an automation candidate, or has unclear evidence ownership

## Rollback Or Disable Path

- Disable path: remove the automation candidate packet and stop running the audit command
- Rollback steps: discard staged report and compaction proposals
- State cleanup: delete generated hygiene report artifacts

## Explicit Write Policy

- Allowed write targets: staged report artifacts only after explicit approval
- Forbidden write targets: target system files, hooks, GitHub Actions, Codex App automations, MCP config, global config and external systems
- External side effects: none

## Explicit Approval

- Approval status: not requested
- Active schedules remain out of scope until explicit approval, stable inputs, expected outputs, monitoring, rollback or disable path and write policy are recorded.
- Activation also requires at least two successful manual runs, deterministic command evidence, owner approval, accepted residual risks and a separate approval packet.

## Future Activation Handoff

activation_gate:

- activation requirements: two successful manual runs, deterministic command evidence, owner approval, rollback or disable plan, accepted residual risks and no active runtime markers.
- future_activation_handoff_required: true
- schedule_status remains not_created until a separate owner-approved activation slice records otherwise.
- no GitHub Actions, Codex App automation, hook activation or external write is performed by this candidate packet.

## Readiness

readiness: candidate_only
candidate-only automation: true
active schedules remain out of scope until explicit approval and rollback/disable evidence exist.
