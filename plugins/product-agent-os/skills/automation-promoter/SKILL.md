---
name: automation-promoter
description: Use when a repeated Product-Agent OS workflow has manual stability evidence and needs candidate-only automation readiness analysis.
---

# Automation Promoter

## Trigger

Use this skill when a recurring or repeated Product-Agent OS workflow may be promoted from manual process to automation candidate.

## Boundaries

Default output is a staged packet. `workspace_apply: forbidden` keeps this skill read-only or proposal-only even when another role has workspace-write.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, schedules, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not modify external systems, perform external writes, install dependencies, use network access, write user-level memory, run destructive commands, or create runtime jobs.
Do not claim automation readiness, manual stability, verification coverage, rollback safety, owner acceptance, or lifecycle advancement without evidence from the current run.
Ask for approval before any write, external action, schedule proposal beyond the staged packet, permission change, or operation outside the allowed scope.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Manual stability evidence from repeated successful manual runs.
- Workflow purpose, trigger or cadence, owner, expected inputs, and expected outputs.
- Verification method, known failure modes, rollback or disable path, and recovery notes.
- Business/Product methodology evidence for internal workflow promotion when automation is justified by product or operating value: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/tracking-plan.md`, engineering time saved, owner acceptance, and residual risk.
- Write policy preference: `read_only`, `draft_only`, or `approved_write`.
- Approval requirements, owner approval status, accepted residual risks, scope boundaries, source status, and unsupported claims.
- Professional Code Authoring automation-candidate scope when future improvements to coding-standard templates, skills, evals, hook-governance or learning-loop candidate generation are proposed.

## Process

1. Confirm manual stability evidence exists and identifies repeated successful manual execution.
2. Identify required inputs and stable outputs with enough detail to detect drift.
3. Define write policy as exactly one of `read_only`, `draft_only`, or `approved_write`.
4. Name verification checks, failure modes, owner, trigger or cadence, and rollback_or_disable path.
5. Mark approval requirements for any future write, schedule, external action, or privileged operation.
6. Return `candidate_only` readiness without activating, scheduling, connecting, or executing anything.
7. For internal workflow promotion, require product or operating value evidence such as engineering time saved, cycle-time reduction, quality improvement, or reduced manual error; map it to `value_proposition_evidence_present`, `outcome_metric_level_separated`, and `metric_scope_classified`.
8. If the automation depends on product analytics, telemetry, usage data, or dashboards, require `analytics_tracking_plan_present` and `.codex/artifact-templates/tracking-plan.md` or block promotion with an accepted gap requirement.
9. Keep `product_hypothesis_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, and `decision_horizon_present` explicit when the automation candidate is promoted as a product or workflow improvement.
10. Block active promotion when manual stability evidence, deterministic command evidence, owner approval, rollback_or_disable, value evidence, or accepted residual risks are missing.
11. Produce a future activation handoff only as a staged approval packet. Current state remains `schedule_status: not_created`; GitHub Actions, Codex App automation, hook activation and external writes stay forbidden until a separate approved activation slice.
12. For Professional Code Authoring automation candidates, keep readiness `candidate_only` even when manual stability exists. Require at least three successful manual pilot uses, deterministic focused tests, owner approval, accepted residual risks, rollback/disable path, false-positive audit, flake replay and cost check before a later activation review can be discussed.
13. Return next lifecycle state `maintenance` only when candidate readiness and blockers are explicit.

## Outputs

Return an automation candidate packet:

```yaml
automation_candidate:
  name: ""
  purpose: ""
  trigger_or_cadence: ""
  required_inputs: []
  stable_outputs: []
  write_policy: "read_only | draft_only | approved_write"
  verification: []
  failure_modes: []
  owner: ""
  rollback_or_disable: ""
  activation_gate:
    manual_stability_present: false
    deterministic_command_evidence_present: false
    owner_approval_present: false
    accepted_residual_risks_present: false
    future_activation_handoff_required: true
    schedule_status: "not_created"
    boundary: "separate approved activation slice; no GitHub Actions, Codex App automation, hook activation or external write"
  business_product_value:
    gates:
      - "product_hypothesis_present"
      - "value_proposition_evidence_present"
      - "analytics_tracking_plan_present"
      - "qualitative_feedback_loop_present"
      - "release_measurement_evidence_present"
      - "decision_horizon_present"
      - "outcome_metric_level_separated"
      - "metric_scope_classified"
    tracking_plan_artifact: ".codex/artifact-templates/tracking-plan.md"
    engineering_time_saved: ""
    residual_risk: ""
  professional_code_authoring_candidate:
    applies_when: "coding-standard templates, skills, evals, hook-governance or learning-loop candidate generation would change"
    candidate_policy: "candidate_only"
    minimum_manual_successful_runs: 3
    deterministic_checks: []
    required_before_activation_review:
      - "owner approval"
      - "accepted residual risks"
      - "rollback or disable path"
      - "false-positive audit"
      - "flake replay"
      - "cost check"
    forbidden_current_slice:
      - "active schedule"
      - "hook activation"
      - "Codex App automation"
      - "GitHub Actions workflow"
      - "provider/model call"
      - "target workspace mutation"
      - "external write"
  approval_required: []
  accepted_residual_risks: []
  readiness: "candidate_only"
  next_lifecycle_state: "maintenance"
```

## Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, deterministic command evidence, owner approval, accepted residual risks, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.

## Verification

Check that manual stability evidence is present, owner is named, required inputs and stable outputs are explicit, write policy is one allowed value, rollback_or_disable is actionable, approval requirements are listed, accepted residual risks are recorded, `future_activation_handoff_required` is true, `schedule_status` remains `not_created`, and readiness remains `candidate_only`. For internal workflow promotion, check engineering time saved or another value signal before using `value_proposition_evidence_present`, and keep `product_hypothesis_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, and `.codex/artifact-templates/tracking-plan.md` explicit when applicable. Do not claim without evidence.

## Failure Modes

- If manual stability evidence is missing, stop and return readiness `candidate_only` with blockers.
- If owner is missing, stop and request owner assignment.
- If stable inputs or stable outputs are missing, stop and request a clearer workflow contract.
- If verification or failure modes are missing, stop and request evidence from manual runs.
- If rollback_or_disable is missing, stop and request an operational disable path.
- If owner approval or accepted residual risks are missing, keep readiness `candidate_only` and block active promotion.
- If a candidate contains `cron`, `RRULE`, `Schedule:`, active Codex App automation, active GitHub Actions workflow, hook activation or external write markers, block promotion.
- If engineering time saved or another value signal is missing for internal workflow promotion, keep readiness `candidate_only` with blockers.
- If product analytics evidence is required but `analytics_tracking_plan_present` or `.codex/artifact-templates/tracking-plan.md` is missing, keep readiness `candidate_only` with blockers.
- If approval is needed, stop before writes, schedules, external actions, or runtime execution.

## Final Response Contract

Return status, lifecycle state, `automation_candidate`, readiness, blockers, evidence used, unsupported claims, approval requirements, residual risks, and the next recommended skill.
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
