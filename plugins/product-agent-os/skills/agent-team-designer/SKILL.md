---
name: agent-team-designer
description: Use when an implementation plan exists and agent roles, file ownership, handoffs, reasoning guidance, and stop conditions are needed.
---

# Agent Team Designer

## Trigger

Use this skill when an implementation plan exists and the project needs agent roles, file ownership, handoff packets, reasoning/model guidance, and stop conditions.

## Boundaries

This is a Track 2 skill. Produce a staged team design packet only.

Guided question protocol: ask the smallest blocking question only; enforce one blocking question maximum; optional questions stay in the packet; route answers into artifacts or accepted gaps; guided questions are not workspace evidence. Do not use guided questions as a substitute for workspace evidence.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not create `.codex/agents/*.toml`, write `AGENTS.md` or `RUNLOG.md` directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim team readiness, ownership safety, verification completion, or model suitability without evidence from the current run.
Ask for approval before any write, external action, expanded scope, permission change, or irreversible team/runtime decision.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- `implementation_plan_packet` with slices, dependencies, verification gates, rollback notes, and risks.
- `workspace_audit` packet with project structure, existing Codex assets, and constraints.
- Complexity profile, team constraints, approval limits, and available verification gates.
- Known file or subsystem ownership requirements from the user or project docs.
- Scenario handoff packet when a scenario workflow produced context, proposed files, or stop reasons.
- Fresh-context handoff inputs when any subagent or parallel worker is proposed: `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, complete task context, source constraints, allowed sources, inputs used, owned files, forbidden files, expected evidence, stop conditions, handoff output schema, shared ownership ambiguity, and missing handoff schema.

## Process

1. Validate that an implementation plan exists and the lifecycle state is `plan_ready`.
2. Route back to `implementation-planner` if slices, gates, or ownership signals are incomplete.
3. Choose only needed roles around ownership: Product Manager, Architect, Builder, Tester, Reviewer, Docs Maintainer, and Release Operator.
4. Assign disjoint file or subsystem ownership for each role and mark unresolved overlaps.
5. Assign methodology ownership: Product Manager owns hypothesis/metrics, Architect owns architecture boundary, Tester owns test/eval gates, Docs Maintainer owns docs-as-code artifacts, Reviewer owns risk closure.
6. Require fresh-context handoff for any subagent or parallel worker, not only complex acceleration.
7. Build each fresh-context handoff from `agent-task-packet.md`, `handoff-contract.md`, and `worktree-ownership.md`; include complete task context, source constraints, allowed sources, inputs used, owned files, forbidden files, expected evidence, handoff output schema, stop conditions, and accepted gaps.
8. Define scenario handoff packet fields: sources/context used, assumptions, files touched, files proposed, verification evidence, open risks, stop reason, and recommended next role.
9. Define model/reasoning policy with escalation and downgrade rules tied to risk, ambiguity, cost, and latency.
10. Define stop conditions for missing evidence, overlapping ownership, approvals, secrets exposure, failed verification gates, shared ownership ambiguity, missing handoff schema, or raw conversation history as context.
11. Use sequential fallback when ownership cannot be split, when source constraints are missing, or when expected evidence cannot be assigned per worker.
12. Keep handoffs concise enough for the next role to act without reading raw conversation history.
13. Return `team_ready` only when ownership, fresh-context handoffs, model guidance, escalation rules, methodology ownership, and stop conditions are staged.

## Outputs

Return an agent team design packet:

```yaml
agent_team_design_packet:
  roles: []
  ownership_map: []
  methodology_ownership: []
  handoff_packets: []
  fresh_context_handoff:
    complete_task_context: []
    source_constraints: []
    allowed_sources: []
    inputs_used: []
    owned_files: []
    forbidden_files: []
    expected_evidence: []
    handoff_output_schema: []
    stop_conditions: []
    sequential_fallback: ""
  scenario_handoff:
    sources_context_used: []
    assumptions: []
    files_touched: []
    files_proposed: []
    verification_evidence: []
    open_risks: []
    recommended_next_role: ""
    stop_reason: ""
  model_reasoning_policy: []
  escalation_rules: []
  stop_conditions: []
  unresolved_overlaps: []
  files_proposed:
    - "AGENTS.md"
    - "RUNLOG.md"
  next_lifecycle_state: "team_ready"
```

## Requirements Domain Methodology

Use Requirements & Domain evidence to assign ownership. `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md` identify owners, bounded contexts, business rules, domain expert review, accepted gaps, and handoff boundaries. Treat `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` as ownership inputs before splitting work.

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Track 9 Codex Agentic Workflow

Use `codex_agentic_workflow` when Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, automation, worktrees, external writes, approval boundaries, memory policy, or Agents SDK orchestration applies. Stage or request `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md` when the corresponding gate applies.

Track `agentic_scope_classified`, `control_plane_present`, `source_of_truth_present`, `read_only_discovery_complete`, `model_reasoning_policy_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `approval_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `plugin_boundary_present`, `skill_promotion_evidence_present`, `automation_manual_stability_present`, `agent_eval_workflow_present`, `memory_policy_present`, and `agentic_evidence_before_completion`. Use memory as recall only. Use `present_unverified` for detected assets until evidence exists. No silent activation: MCP, hooks, automation, external writes, plugin packaging, GitHub Actions, and Agents SDK app orchestration require `approval_required` or explicit owner-approved gap.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Verification

Check that each role has a concrete ownership boundary, no planned agents share write scope without a handoff rule, every handoff includes verification evidence fields, every scenario handoff separates files touched from files proposed, and every proposed artifact remains staged. Do not claim without evidence.
For fresh-context handoff, check that any subagent or parallel worker has complete task context, source constraints, allowed sources, inputs used, owned files, forbidden files, expected evidence, handoff output schema, stop conditions, and sequential fallback before work starts. Do not advance to parallel work when shared ownership ambiguity, missing handoff schema, missing expected evidence, raw conversation history dependency, or cross-agent file ownership remains.

## Failure Modes

- If no implementation plan exists, stop and route to `implementation-planner`.
- If ownership cannot be separated, route back to planning with overlap details.
- If fresh-context handoff is missing for any subagent or parallel worker, do not advance to parallel work.
- If scenario handoff context is missing for complex acceleration, do not advance to parallel work.
- If ownership cannot be split safely, use sequential fallback rather than parallel work.
- If the task packet depends on raw conversation history instead of complete task context, stop and request a proper handoff packet.
- If required verification gates are absent, stop and request planning updates.
- If model or reasoning guidance would override project rules, keep it as a proposal and flag the conflict.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `agent_team_design_packet`, files proposed, ownership overlaps, verification evidence, unsupported claims, approval requirements, risks, and the next recommended skill.
## Track 9 Cross-Domain Synthesis

Consume `methodology_synthesis` and `recommendation_groups` as grouped recommendations; do not dump every methodology gate. Preserve owner domains, consumer domains, semantic evidence sufficiency, source artifact ledger, alias/deferred artifact ledger and risk-aware safe next action. Do not scaffold before approval, and remember that detection is not verification.
