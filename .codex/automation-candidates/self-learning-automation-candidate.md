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

## Professional Code Authoring Candidate Gate

- `candidate_policy: candidate_only`
- `minimum_manual_successful_runs: 3`
- `allowed_update_targets: coding-standard templates, skills, evals and hook-governance candidates`
- `owner_review: required_before_apply`
- `rollback_evidence: required_before_apply`
- `false_positive_audit: required_before_apply`
- `flake_replay: required_before_apply`
- `cost_check: required_before_apply`
- `future_activation_handoff_required: true`

## Forbidden Until Approval

- no real Codex App session export import
- no hidden telemetry
- no raw transcript storage
- no provider/model/live eval call
- no target workspace mutation
- no skill, prompt, route, memory, config, hook or automation auto-apply
- no coding-standard template, skill, eval or hook-governance auto-apply
- no git, release, deploy, publish or external write action

## Required Activation Approval Shape

Any future activation approval must name the schedule or trigger, exact command,
workspace scope, owner, evidence window, rollback/disable path, privacy boundary,
verification commands and stop condition.
