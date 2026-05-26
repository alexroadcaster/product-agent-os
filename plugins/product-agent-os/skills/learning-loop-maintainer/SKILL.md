---
name: learning-loop-maintainer
description: Use after Product-Agent OS delivery, stopped lifecycle runs, or runlog evidence reviews that need lessons, failure capture, or durable-rule candidates.
---

# Learning Loop Maintainer

## Trigger

Use this skill after Product-Agent OS delivery, after a stopped lifecycle run, or when runlog evidence needs compaction into lessons and next actions.

## Boundaries

This is a Track 2 skill. Produce a staged `learning_loop_packet` only.

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
9. Keep all updates staged and list approval needs before any durable artifact change.
10. Return next lifecycle state `learning_ready` only when decisions, failures, proposed compaction, candidates, and next action are explicit.

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
