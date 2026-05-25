---
name: docs-maintainer
description: Use when requirements, source registry, glossary or traceability documentation must stay aligned after a requirements packet exists.
---

# Docs Maintainer

## Trigger

Use this skill when a requirements packet, methodology packet, implementation plan, review result or release note changes documentation, source registry, glossary, ubiquitous language, or traceability docs.

## Boundaries

This is a Track 2 skill. Produce a staged documentation packet only.

Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
Do not create active automation, recurring automation, hooks, workflow files, project templates, MCP servers, or an Agents SDK runner.
Do not mutate global config. Do not modify config. Do not edit project config.
Do not write docs directly, edit code, run destructive commands, install external dependencies, use network access, write user-level memory, or connect to external systems.
Do not claim documentation readiness, source support, traceability, or verification results without evidence from the current run.
Ask for approval before any write, external action, navigation change, expanded scope, or irreversible publication decision.

Read shared references when needed: [Lifecycle states](../references/lifecycle-states.md), [Handoff contract](../references/handoff-contract.md), [Source policy](../references/source-policy.md), and [Complexity routing](../references/complexity-routing.md).

## Inputs

- Requirements packet with requirement IDs, source notes, owner map, open questions, accepted gaps, and traceability docs.
- Requirements & Domain artifacts: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, `domain-review-record.md`, and `acceptance-scenarios.md`.
- Methodology gates: `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation`.
- Source registry updates, glossary or ubiquitous language terms, architecture/API/UI/data docs, release notes and user-facing docs affected by the slice.
- Evidence-before-completion (`evidence_before_completion`) fields: ready claim, completed claim, fixed claim, works claim, release claim, current command evidence, current eval evidence, current runtime evidence, inspection-only, explicit test gap, unsupported completion claim, and completion claim without current evidence.

## Process

1. Verify that a requirements packet or review packet exists before staging docs changes.
2. Keep requirement IDs aligned across source registry, glossary, ubiquitous language, traceability docs, architecture, API, UI, database and release docs.
3. Check `requirement-registry.md` for `requirement_quality_present`: atomicity, clarity, testability, feasibility, traceability, source and owner.
4. Check `stakeholder-owner-map.md` before making source-backed domain meaning or business rule claims.
5. Check `story-slice-map.md` before documenting MVP boundary, deferred slices, non-goals or release scope.
6. Check `requirements-traceability-matrix.md` before claiming `requirements_traceability_present`, `constraints_traceability_present`, `domain_event_contracts_present`, or `api_ui_data_traceability_present`.
7. Check `business-rules.md` before documenting business rules; confirm source, owner, enforcement layer, exceptions, failure mode and tests/evals.
8. Check `example-map.md` when open questions or unclear stories affect docs.
9. Check `requirement-change-impact.md` when requirement or domain rule changes after planning affect tests/evals, API, DB, UI, docs, rollout, rollback or approval boundary.
10. Check `domain-review-record.md` before documenting business-critical, compliance, finance/legal or AI-generated domain claims, accepted gaps, unsupported claims or owner review.
11. Preserve `declarative_acceptance_scenarios_present`: docs should not turn business-facing scenarios into UI selectors, database internals, function names, or test harness details.
12. Keep glossary and ubiquitous language separate: a glossary is not enough; terms must trace to requirement IDs, source, API/event/contract, UI label, code/test or owner review.
13. Reject unsupported claims as docs evidence: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language, and OpenAPI is requirements source of truth.
14. Stage source registry and docs updates only; do not publish, change navigation broadly, or mutate external systems without explicit approval.
15. Use evidence-before-completion before any ready claim, completed claim, fixed claim, works claim, or release claim.

## Outputs

Return a documentation packet:

```yaml
docs_packet:
  requirement_ids: []
  source_registry_updates: []
  glossary_updates: []
  ubiquitous_language_updates: []
  traceability_docs: []
  requirements_domain:
    artifacts:
      - "requirement-registry.md"
      - "stakeholder-owner-map.md"
      - "story-slice-map.md"
      - "requirements-traceability-matrix.md"
      - "business-rules.md"
      - "example-map.md"
      - "requirement-change-impact.md"
      - "domain-review-record.md"
    gates:
      - "requirements_traceability_present"
      - "requirement_quality_present"
      - "constraints_traceability_present"
      - "declarative_acceptance_scenarios_present"
      - "business_rules_present"
      - "domain_expert_review_present"
      - "requirement_change_impact_review_present"
      - "accepted_gap_recorded"
      - "requirements_evidence_before_implementation"
  files_proposed: []
  accepted_gaps: []
  evidence_before_completion:
    current_command_evidence: []
    current_eval_evidence: []
    current_runtime_evidence: []
    inspection_only: false
    explicit_test_gap: ""
    unsupported_completion_claim: []
    completion_claim_without_current_evidence: []
  next_lifecycle_state: "maintenance"
```

## Solution Architecture Methodology

Use Solution Architecture routing when a slice touches architecture boundary, public contract, data ownership, trust boundary, runtime topology, observability, rollback, or parallel agent ownership. Track `solution_architecture_scope_present`, `architecture_boundary_per_slice`, `boundary_responsibility_owner_present`, `adr_for_architecture_decision`, `diagram_render_check_present`, `runtime_deployment_topology_present`, `observability_architecture_present`, `migration_rollback_path_present`, and `architecture_fitness_function_present`.

Stage or request `.codex/artifact-templates/architecture-overview.md`, `.codex/artifact-templates/adr.md`, `.codex/artifact-templates/architecture-review-record.md`, `.codex/artifact-templates/architecture-fitness-functions.md`, `.codex/artifact-templates/trust-boundary-map.md`, and `.codex/artifact-templates/architecture-docs-tooling-decision.md` when the corresponding gate applies. C4/arc42 only when applicable; architecture-as-code is conditional; Well-Architected review is conditional. Use `not_applicable` or `explicit_gap_accepted` with owner, reason, residual risk and follow-up condition rather than forcing diagrams, cloud review or docs tooling.

## Evidence Before Completion

Evidence-before-completion (`evidence_before_completion`): do not make a ready claim, completed claim, fixed claim, works claim, or release claim without current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap. If only inspection happened, label the result `inspection-only` and list every unsupported completion claim. Treat completion claim without current evidence as blocked.

## Quality Testing & Evals Methodology

Use `quality_testing_evals` when quality, test, eval, runtime, manual QA, visual/a11y, CI, flaky, coverage, test data privacy, bugfix, regression, release, readiness, or completion evidence applies. Stage or request `quality-strategy.md`, `test-eval-matrix.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md` when the corresponding gate applies.

Track `quality_strategy_present`, `risk_based_scope_present`, `test_first_or_gap_present`, `acceptance_traceability_present`, `contract_check_present`, `runtime_evidence_present`, `manual_qa_evidence_present`, `visual_a11y_evidence_present`, `eval_spec_present`, `eval_rerun_evidence_present`, `current_evidence_before_completion`, `ci_quality_gate_present`, `flaky_test_policy_present`, `coverage_policy_present`, `test_data_privacy_present`, `bug_reproduction_evidence_present`, and `regression_impact_present`. Coverage is a signal, not proof. Do not force TDD, do not force E2E, do not force coverage, and do not force AI evals when not applicable; use `not_applicable`, `present_unverified`, `explicit_gap_accepted`, or `approval_required` with owner, reason, residual risk and follow-up condition.

## Verification

Check that staged docs reference current requirement IDs, source registry entries, glossary/ubiquitous language terms, traceability docs, accepted gaps and owner review. Verify that `requirements_traceability_present`, `requirement_quality_present`, `constraints_traceability_present`, `declarative_acceptance_scenarios_present`, `business_rules_present`, `domain_expert_review_present`, `requirement_change_impact_review_present`, `accepted_gap_recorded`, and `requirements_evidence_before_implementation` are satisfied, explicitly not applicable, or recorded as accepted gaps before claiming docs readiness.

## Failure Modes

- If requirement IDs are missing, stop and route to `requirements-author`.
- If source registry evidence is missing, keep the claim unsupported.
- If glossary terms are not traced to ubiquitous language usage, mark the gap.
- If traceability docs are stale after a requirement change, route to `implementation-planner` or `risk-reviewer`.
- If accepted gaps lack owner, reason, scope, review date, downstream risk or follow-up condition, do not claim the gap is accepted.
- If docs use UI selectors, database internals, function names or test harness details as business scenarios, route back to requirements repair.
- If approval is needed, stop before writes or external actions.

## Final Response Contract

Return status, lifecycle state, `docs_packet`, files proposed, sources used, verification evidence, unsupported claims, accepted gaps, approval requirements, risks, and the next recommended skill.
