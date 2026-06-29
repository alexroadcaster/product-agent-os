---
name: learning-loop-maintainer
description: Use after Product-Agent OS delivery, stopped lifecycle runs, or runlog evidence reviews that need lessons, failure capture, or durable-rule candidates.
---

# Learning Loop Maintainer

## Trigger

Use this skill after Product-Agent OS delivery, after a stopped lifecycle run, or when runlog evidence needs compaction into lessons and next actions.

## Boundaries

This is a Track 2 skill. Produce a staged `learning_loop_packet` only.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Self-verification metrics loop (`agent_skill_metrics_loop`): route agent/skill metrics as staged evidence only. Dashboard or report is not proof. Do not apply modernization candidates, do not activate schedules, do not call live eval services, and do not treat a dashboard or report as proof. Rollback evidence required before any modernization candidate can be reviewed.
Project code graph: generated graph is not source of truth; use it as orientation evidence only. Read source files before edits, impact claims, readiness claims, or completion claims. Stale or ambiguous graph blocks readiness claims. Do not treat graph HTML as proof.


Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not edit `AGENTS.md`, `RUNLOG.md`, project files, user-level memory, external systems, or any source-of-truth artifact.
Do not claim durable-rule readiness, skill readiness, lesson validity, verification coverage, or lifecycle advancement without evidence from the current run.
Ask for approval before any write, durable-rule promotion, expanded scope, external action, dependency change, or operation outside the staged packet.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

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

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Track 9 LLM / AI / RAG Methodology

Capture `llm_ai_rag` lessons when AI behavior, prompt/model changes, structured outputs, AI tools, MCP/function calling, RAG retrieval, grounding, datasets, agent traces, safety, latency or cost shaped the run outcome.

Record whether AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, prompt/context inventory, dataset governance, safety evidence, cost evidence, approval boundary and accepted gaps were satisfied, missing or disproved. Preserve references to `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, and `ai-cost-latency-budget.md` without copying raw private prompts, traces or data.

Do not force one eval runner, do not force multi-agent architecture, and do not run live model calls during learning capture. Use `approval_required` before live model/API calls, external writes, risky tools, data exposure or irreversible side effects.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Track 9 Security, Privacy & Compliance Methodology

Use `security_privacy_compliance` when authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data, policy changes, regulated, contractual or compliance overlays appear. Record `security_sensitive_classification_present` and all detected signals as `present_unverified` until owner-reviewed evidence exists.

Stage or request `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md`, and `approval-record.md` when applicable.

Compliance output is methodology planning evidence, not legal advice. Record Codex Security scan status as not requested, requested/run, or blocked; never imply a scan ran. Docs-only security article and keyword-only mentions stay `not_applicable` unless code, data, CI, dependency, policy, external write or owner compliance claim changes apply. Use `approval_required` before payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes or publish actions. Use `explicit_gap_accepted` only with owner, reason, residual risk, review date and follow-up.

## Track 9 Delivery, Release & Operations

Use `delivery_release_operations` for planning-first delivery classification when release, deploy, publish, package, version, changelog, artifact, rollout, rollback, CI/CD governance, operations, incident, post-release, DORA, GitOps, feature flag, deployment, or automation promotion signals appear.

Track `release_scope_present`, `version_impact_present`, `release_evidence_present`, `release_evidence_before_completion`, `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `ci_cd_governance_present`, `operations_runbook_present`, `incident_response_path_present`, `post_release_measurement_present`, and `automation_manual_stability_present`. Stage or request `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `ci-cd-workflow-inventory.md`, `operations-runbook.md`, `incident-record.md`, `post-release-review.md`, and `automation-candidate.md` when applicable.

Require release scope, version impact, current evidence, artifact manifest, rollout, rollback, CI/CD governance, operations, incident path, post-release learning, approval boundary, and automation candidate-only behavior. For automation promotion, require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence, rollback/disable path, candidate-only automation, and keep active schedules remain out of scope.

Do not publish, tag, deploy, upload artifacts, mutate package registries, create releases, or activate automation without explicit approval and rollback/recovery evidence.

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
## Track 9 Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
