---
name: learning-loop-maintainer
description: Use after Product-Agent OS delivery, stopped lifecycle runs, or runlog evidence reviews that need lessons, failure capture, or durable-rule candidates.
---

# Learning Loop Maintainer

## Trigger

Use this skill after Product-Agent OS delivery, after a stopped lifecycle run, or when runlog evidence needs compaction into lessons and next actions.

## Boundaries

Default output is a staged packet. `workspace_apply: explicit_task_authority` permits direct local edits only when the current user request or parent task explicitly authorizes workspace writes, the host agent has `workspace-write`, and the exact owned files are named. It never authorizes external, destructive, global-config, permission, provider, browser, Git, release, deployment, publication, hook, or automation actions.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Change project config only when the current task explicitly owns that file.
Write assigned local RUNLOG or candidate artifacts under explicit task authority; otherwise return staged proposals. Never auto-promote durable rules, skills, hooks, or automation, and do not write user-level memory or external systems.
Do not claim durable-rule readiness, skill readiness, lesson validity, verification coverage, or lifecycle advancement without evidence tied to the checked state. Reuse unchanged evidence with its original run identified; rerun after relevant changes or uncertainty.
Ask for approval for durable-rule promotion, expanded scope, external actions, dependency changes, or operations outside the allowed workspace.

Instruction hierarchy and evidence reuse follow [Source policy](../references/source-policy.md); factual sources do not override instructions. Read other shared references only when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Final result or stop reason from the Product-Agent OS run.
- Runlog evidence, command results, review notes, and handoff packets.
- Failures, decisions, blocked paths, repeated gaps, and open questions.
- Review findings, reusable methods, recurring manual steps, and observed recovery actions.
- Approval constraints, source status, unsupported claims, and evidence gaps.
- Professional Code Authoring evidence when code-writing standards, shortcut-resistance evals, reuse-first guidance, dependency decisions, comment standards, or hook/eval candidates are affected.
- Business/Product methodology evidence after delivery when product, MVP, user value, analytics, release measurement, or workflow promotion claims were made: `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, `.codex/artifact-templates/tracking-plan.md`, accepted gaps, and residual risks.

## Process

1. Extract decisions from evidence and keep each decision tied to the source packet, command result, or review note.
2. Separate confirmed failures from residual risks, open questions, unsupported claims, and missing context.
3. Propose durable-rule candidates only when repeated evidence supports a stable project rule.
4. Propose skill candidates only after repeated manual success, clear reuse, named inputs, named outputs, verification, and failure modes.
5. Propose runlog compaction that summarizes lessons without deleting evidence or hiding failed attempts.
6. Capture Business/Product methodology lessons when product claims were made: record whether `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, and `metric_scope_classified` were satisfied, accepted as gaps, or disproved by evidence.
7. Use `.codex/artifact-templates/tracking-plan.md` and release evidence to compare planned product analytics with observed instrumentation, qualitative feedback, and release measurement evidence.
8. Route stable recurring workflows to `automation-promoter` for candidate-only analysis, but only after value evidence, owner evidence, verification evidence, and residual risk are recorded.
9. For Professional Code Authoring lessons, produce only staged improvement candidates for coding-standard templates, skills, evals or hook-governance artifacts. Require at least three successful manual pilot uses or an owner-accepted gap before review; require rollback evidence, false-positive audit, flake replay, cost check and owner review before any apply discussion.
10. Keep all updates staged and list approval needs before any durable artifact change.
11. Return next lifecycle state `learning_ready` only when decisions, failures, proposed compaction, candidates, and next action are explicit.

## Outputs

Return a learning loop packet:

```yaml
learning_loop_packet:
  decisions: []
  failures: []
  durable_rules_candidate: []
  skill_candidates: []
  runlog_compaction: []
  observations: []
  professional_code_authoring_learning:
    candidate_policy: "candidate_only"
    allowed_update_targets:
      - "coding-standard templates"
      - "skills"
      - "evals"
      - "hook-governance candidates"
    minimum_manual_successful_runs: 3
    forbidden_until_approval:
      - "auto_apply"
      - "hook_activation"
      - "active_schedule_creation"
      - "provider_call"
      - "global_config_mutation"
      - "target_mutation"
      - "raw_transcript_storage"
      - "hidden_telemetry"
      - "external_write"
    required_review_evidence:
      - "owner review"
      - "rollback evidence"
      - "false-positive audit"
      - "flake replay"
      - "cost check"
  business_product_learning:
    gates_reviewed:
      - "product_hypothesis_present"
      - "value_proposition_evidence_present"
      - "analytics_tracking_plan_present"
      - "qualitative_feedback_loop_present"
      - "release_measurement_evidence_present"
      - "decision_horizon_present"
      - "outcome_metric_level_separated"
      - "metric_scope_classified"
    tracking_plan_artifact: ".codex/artifact-templates/tracking-plan.md"
    confirmed_lessons: []
    residual_risks: []
  files_proposed:
    - "RUNLOG.md"
    - "AGENTS.md"
  next_action: ""
  next_lifecycle_state: "learning_ready"
```

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.


## Conditional References

Read the `Skill: learning-loop-maintainer` section of [Complexity routing](../references/complexity-routing.md), only the subsections matching the changed domain or gate below. Mixed work reads all applicable subsections; unknown applicability requires inspection. Do not load unrelated roles.

- **Codex Agentic Workflow** — agent roles, tools, MCP, hooks, skills or automation.
- **LLM / AI / RAG Methodology** — changes or claims in LLM / AI / RAG.
- **Security, Privacy & Compliance Methodology** — changes or claims in Security, Privacy & Compliance.
- **Delivery, Release & Operations** — release, deployment, operations or rollback.

## Verification

Check that every decision, failure, durable-rule candidate, skill candidate, and runlog compaction note is backed by current evidence. For Business/Product methodology, check that `product_hypothesis_present`, `value_proposition_evidence_present`, `analytics_tracking_plan_present`, `qualitative_feedback_loop_present`, `release_measurement_evidence_present`, `decision_horizon_present`, `outcome_metric_level_separated`, `metric_scope_classified`, and `.codex/artifact-templates/tracking-plan.md` status are recorded before promoting a product lesson. Confirm that proposed files remain staged, approval needs are explicit, and unsupported claims are listed instead of promoted.

## Failure Modes

- If final result or stop reason is missing, stop and request the missing lifecycle evidence.
- If runlog evidence is absent, return observations and unsupported claims only.
- If a durable rule lacks repeated evidence, keep it as an observation or open question.
- If a skill candidate lacks repeated manual success or clear reuse, keep it as a possible future method.
- If a recurring workflow appears stable, route to `automation-promoter` without creating automation.
- If approval is needed, stop before edits, promotions, external actions, or lifecycle advancement.

## Final Response Contract

Return status, lifecycle state, `learning_loop_packet`, files proposed, evidence used, unsupported claims, approval requirements, residual risks, and the next recommended skill.
## Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
