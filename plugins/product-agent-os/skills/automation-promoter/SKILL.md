---
name: automation-promoter
description: Use when a repeated Product-Agent OS workflow has manual stability evidence and needs candidate-only automation readiness analysis.
---

# Automation Promoter

## Trigger

Use this skill when a recurring or repeated Product-Agent OS workflow may be promoted from manual process to automation candidate.

## Boundaries

This is a Track 2 skill. Produce a staged `automation_candidate` packet only. Readiness is `candidate_only`.

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
- Approval requirements, scope boundaries, source status, and unsupported claims.

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
10. Block promotion when manual stability evidence, owner, stable inputs, stable outputs, verification, rollback_or_disable, value evidence, or residual risk is missing.
11. Return next lifecycle state `maintenance` only when candidate readiness and blockers are explicit.

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
  approval_required: []
  readiness: "candidate_only"
  next_lifecycle_state: "maintenance"
```

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Verification

Check that manual stability evidence is present, owner is named, required inputs and stable outputs are explicit, write policy is one allowed value, rollback_or_disable is actionable, approval requirements are listed, and readiness remains `candidate_only`. For internal workflow promotion, check engineering time saved or another value signal before using `value_proposition_evidence_present`, and keep `product_hypothesis_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, and `.codex/artifact-templates/tracking-plan.md` explicit when applicable. Do not claim without evidence.

## Failure Modes

- If manual stability evidence is missing, stop and return readiness `candidate_only` with blockers.
- If owner is missing, stop and request owner assignment.
- If stable inputs or stable outputs are missing, stop and request a clearer workflow contract.
- If verification or failure modes are missing, stop and request evidence from manual runs.
- If rollback_or_disable is missing, stop and request an operational disable path.
- If engineering time saved or another value signal is missing for internal workflow promotion, keep readiness `candidate_only` with blockers.
- If product analytics evidence is required but `analytics_tracking_plan_present` or `.codex/artifact-templates/tracking-plan.md` is missing, keep readiness `candidate_only` with blockers.
- If approval is needed, stop before writes, schedules, external actions, or runtime execution.

## Final Response Contract

Return status, lifecycle state, `automation_candidate`, readiness, blockers, evidence used, unsupported claims, approval requirements, residual risks, and the next recommended skill.
