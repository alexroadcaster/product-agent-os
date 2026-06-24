# Self-Learning Loop automation candidate

Status: `candidate_only`

This file is a proposal packet, not an active schedule, hook, Codex App automation,
GitHub Action, external workflow or recurring job.

## Promotion Gate

- `minimum_manual_successful_runs: 3`
- `owner_approval_record: required_before_activation`
- `active_schedule_status: not_created`
- `rollback_disable_path: required_before_activation`
- `false_positive_audit: required_before_activation`
- `flake_replay: required_before_activation`
- `cost_check: required_before_activation`

## Forbidden Until Approval

- no real Codex App session export import
- no hidden telemetry
- no raw transcript storage
- no provider/model/live eval call
- no target workspace mutation
- no skill, prompt, route, memory, config, hook or automation auto-apply
- no git, release, deploy, publish or external write action

## Required Activation Approval Shape

Any future activation approval must name the schedule or trigger, exact command,
workspace scope, owner, evidence window, rollback/disable path, privacy boundary,
verification commands and stop condition.
