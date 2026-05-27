# Product-Agent OS Track 9 Backlog

Source status: `local implementation planning`

This backlog tracks methodology intelligence work for the local Product-Agent OS plugin. It is planning evidence, not an official OpenAI source.

## Track 9 Goal

Track 9 turns the methodology atlas in `docs/methodologies/` into read-only Product-Agent OS guidance: a catalog, workspace audit, prioritized recommendations, owner questions, staged artifact suggestions and behavioral eval coverage. The plugin must inspect a workspace and explain which methodology gates apply before it proposes any write.

## Foundation Slices

| Status | Slice | Output |
| --- | --- | --- |
| `done` | Task 0 baseline and cleanup | Clean branch baseline before Track 9 implementation. |
| `done` | Task 1 catalog tests | Contract tests for methodology domain metadata. |
| `done` | Task 2 catalog foundation | `methodology_catalog.py` and initial catalog contract. |
| `done` | Task 3 audit tests | Contract tests for read-only methodology audit packets. |
| `done` | Task 4 read-only audit | `methodology_audit.py` with workspace signals, `maturity_level`, `complexity_profile`, recommendations and owner questions. |
| `done` | Task 5 report and CLI | `methodology-audit-report.md`, `methodology_report.py` and `run_methodology_audit.py`. |
| `done` | Task 6 fixture eval integration | Fixture eval fields for methodology catalog, read-only audit and prioritized recommendations. |
| `done` | Task 7 docs foundation | Operator docs, MkDocs navigation, required docs check and Track 9 source registry entry. |

## Domain Integration Queue

| Status | ID | Source file | Scope |
| --- | --- | --- | --- |
| `done` | `T9-D1` | `business-product.md` | Product hypothesis, value, opportunities, metrics, guardrails and measurement. |
| `done` | `T9-D2` | `requirements-domain.md` | Requirements quality, acceptance scenarios, business rules, domain model, traceability and change impact. |
| `done` | `T9-D3` | `solution-architecture.md` | Architecture boundaries, views, ADRs, quality attributes, tradeoffs, ownership and fitness checks. |
| `done` | `T9-D4` | `quality-testing-evals.md` | Risk-based tests, evals, current evidence, runtime/manual/visual evidence and CI quality gates. |
| `done` | `T9-D5` | `codex-agentic-workflow.md` | Control-plane maturity, model/reasoning policy, handoffs, subagents, MCP, hooks, skills, plugins and automation promotion. |
| `done` | `T9-D6` | `frontend.md` | UI behavior, component states, Storybook applicability, visual/a11y evidence, responsive checks, performance and FSD boundaries. |
| `done` | `T9-D7` | `backend.md` | Service boundaries, modular monolith vs microservices, runtime behavior, queues, observability, SLOs and rollback. |
| `done` | `T9-D8` | `api-integrations.md` | OpenAPI/AsyncAPI/GraphQL/gRPC contracts, consumers, compatibility, errors, generated clients and external writes. |
| `done` | `T9-D9` | `database-data.md` | Database inventory, schema source, migrations, transactions, data quality, classification and production access. |
| `done` | `T9-D10` | `llm-ai-rag.md` | AI behavior spec, eval baseline, prompts, models, tools, RAG sources, grounding, datasets, approvals, cost/latency, handoff, tooling, migration, lifecycle, diff policy and incidents. |
| `done` | `T9-D11` | `security-privacy-compliance.md` | Threat surface, ASVS/SSDF, authorization tests, secrets, privacy impact, supply chain, audit logging and compliance overlays. |
| `done` | `T9-D12` | `delivery-release-operations.md` | Release readiness, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, runbooks and operations. |

## Domain Deep-Audit Log

### `T9-D1` Business and Product Domain Integration

Status: `done`

Source audited: `docs/methodologies/business-product.md`

Implemented scope:

- Added `business_product` catalog coverage for product hypothesis, target segment, value proposition, opportunity-not-solution framing, metrics, analytics tracking, qualitative feedback, privacy classification, AI product eval, release measurement evidence, workflow promotion value evidence, decision horizon, outcome metric levels and metric scope.
- Added `decision_horizons`: `discovery`, `MVP`, `beta`, `production`, `scale`.
- Added staged artifact templates: `product-brief.md`, `value-proposition.md`, `opportunity-tree.md`, `experiment-plan.md`, and `tracking-plan.md`.
- Strengthened `REQUIREMENTS.md`, `PLAN.md`, `EVALS.md`, `RUNLOG.md`, `metric-spec.md`, and `release-notes.md` with product hypothesis, value evidence, analytics, feedback, release measurement, no-production-telemetry fallback and outcome-level fields.
- Added read-only audit recommendations and false-positive coverage for product/MVP/value/metric intent, product analytics, AI product claims, release measurement claims, internal workflow promotion and typo/format/dependency-only work.
- Routed Business/Product methodology into `requirements-author`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `learning-loop-maintainer`, and `automation-promoter`.
- Added fixture eval check `business_product_contract_present`.

Severity and false-positive resolution:

- Missing `product_hypothesis_present` is `P2_recommended` for discovery-only or empty-workspace MVP intent, but becomes `P1_high_risk` for implementation or release intent without product hypothesis evidence.
- Product analytics or usage data claims trigger `analytics_tracking_plan_present` and `tracking-plan.md`; plain metric hardening remains in `metric-spec.md`.
- Release success claims require `release_measurement_evidence_present`; no production telemetry must be recorded as an explicit fallback rather than treated as success evidence.
- Internal workflow promotion requires value evidence such as `engineering time saved`, and stays candidate-only until manual stability, owner, verification and rollback evidence exist.
- Typo-only docs edits, formatting-only edits and dependency pin changes without behavior impact keep `business_product` not applicable.

### `T9-D2` Requirements and Domain Integration

Status: `done`

Source audited: `docs/methodologies/requirements-domain.md`

Deep-audit deltas to implement:

- Extend Track 8 acceptance scenarios, conditional DDD, bounded-context traceability, ubiquitous-language traceability and false-positive protection instead of duplicating them.
- Represent requirement taxonomy when relevant: functional, non-functional, compliance, operational, AI behavior, data/privacy and release/rollback.
- Add requirement quality criteria as a first-class gate: atomicity, clarity, testability, feasibility, traceability, source and owner.
- Require stable requirement IDs for multi-slice, regulatory, risky, long-lived or public-contract work.
- Add a requirement registry with status, owner, source and linked artifacts.
- Treat stakeholder/owner mapping as a first-class artifact for source-backed domain meaning and business rules.
- Preserve story slicing evidence: value slice, risk slice, MVP boundary, deferred slices, non-goals and acceptance scenario links.
- Record business rules with source, owner, enforcement layer, exceptions, failure mode and tests/evals.
- Use Example Mapping for unclear, large or disputed stories: story -> rules -> examples -> questions.
- Require domain discovery workshop evidence for complex workflow, cross-silo process or overloaded domain language.
- Track constraints across compliance, privacy, security, operational, performance, platform, accessibility, data retention, localization, cost, rollout and rollback.
- Require declarative acceptance scenarios with no UI selectors, database internals, function names or test harness details.
- Record invariants and failure modes when domain state transitions matter.
- Require domain event contract evidence when events cross boundaries: meaning, producer, consumers, schema link, ordering/idempotency and privacy classification.
- Add API/UI/data traceability distinct from DDD traceability: requirement/domain term -> API/event/schema/UI/data/code/test/eval.
- Require domain expert or owner review for business-critical, compliance, finance/legal and AI-generated domain claims.
- Require requirement change impact review after planning changes: tests/evals, API, DB, UI, docs, rollout and rollback.
- Allow accepted gaps only with owner, reason, scope, review date, downstream risk and follow-up condition.
- Route `docs-maintainer` to maintain requirement IDs, source registry, glossary/ubiquitous-language docs and traceability docs after the requirements packet exists.
- Reject unsupported claims as evidence: BDD replaces testing, Gherkin is mandatory, a user-story template is complete requirements, a glossary is ubiquitous language, and OpenAPI is requirements source of truth.

Implemented scope:

- Added `requirements_domain` catalog coverage for requirements scope/owner, requirement quality, stable IDs, acceptance scenarios, declarative scenario quality, requirements traceability, business rules, non-goals/constraints, open questions, Example Mapping, domain discovery, conditional DDD, invariants/failure modes, domain events, API/UI/data traceability, domain expert review, change impact, accepted gaps and evidence-before-implementation.
- Added staged artifact templates: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`.
- Strengthened `acceptance-scenarios.md`, `domain-modeling.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, Product-Agent OS README and lifecycle skills with Requirements & Domain gates.
- Added a `docs-maintainer` lifecycle skill for requirement IDs, source registry, glossary/ubiquitous-language and traceability docs after the requirements packet exists.
- Added read-only audit recommendations and false-positive coverage for behavior changes, risky/public-contract work, unclear stories, business rules, domain events, owner review, change impact, accepted gaps, declarative scenarios, unsupported methodology claims and typo/format/dependency-only work.
- Added fixture eval check `requirements_domain_contract_present`; renderer file count is now 88 after adding eight Requirements & Domain artifact templates.

Severity and false-positive resolution:

- Behavior-changing work without acceptance scenarios is a `P0_blocker`.
- Requirement quality, stable requirement IDs for risky/public-contract work, constraints traceability, API/UI/data traceability, business rules, domain event contracts, domain expert review, change impact, accepted gaps and declarative scenario quality are `P1_high_risk` when applicable.
- Stakeholder/owner map, story-slice map, Example Mapping and domain discovery workshop evidence are `P2_recommended` unless other risk gates raise severity.
- Typo-only docs edits, formatting-only edits and dependency metadata without behavior impact keep `requirements_domain` not applicable for README-only work.
- Unsupported claims are rejected as evidence: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language, and OpenAPI is requirements source of truth.

### `T9-D3` Solution Architecture Integration

Status: `done`

Source audited: `docs/methodologies/solution-architecture.md`

Deep-audit deltas implemented:

- Used the full Solution Architecture gate set, including `bounded_context_architecture_boundary_trace`, `adr_for_architecture_decision`, `observability_architecture_present` and `migration_rollback_path_present`.
- Kept C4 detail level, architecture-as-code, Well-Architected review and docs tooling conditional rather than universal requirements.
- Rejected unsupported claims as evidence: architecture means diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves architecture quality, architecture-as-code is always required and AI can design architecture from chat alone.
- Mapped candidate artifacts into this slice or existing artifacts; deferred standalone `boundary-responsibility-map.md`, `quality-attribute-scenarios.md`, `architecture-tradeoff-record.md`, `dependency-rules.md` and `runtime-topology.md` because their fields are covered by `architecture-overview.md`, `adr.md`, `architecture-review-record.md`, `architecture-fitness-functions.md`, `integration-catalog.md` and `migration-plan.md` until a later domain proves a separate artifact is needed.

Implemented scope:

- Added `solution_architecture` catalog coverage for architecture scope, context/container views, slice boundaries, boundary owner, bounded-context trace, dependency rules, public contracts, data ownership, runtime topology, observability, quality attributes, ADR/tradeoffs, trust boundary review, diagram render checks, fitness functions, migration rollback, docs lifecycle, owner review and accepted gaps.
- Added staged artifact templates: `architecture-review-record.md`, `architecture-fitness-functions.md`, `trust-boundary-map.md`, and `architecture-docs-tooling-decision.md`.
- Strengthened `architecture-overview.md` and `adr.md` with owner, evidence, accepted gap, residual risk, rollback/no-rollback rationale and no-secrets guidance.
- Added read-only audit recommendations and false-positive coverage for multi-surface work, public contracts, data ownership, trust boundaries, ADR, observability, rollback, diagram render checks, architecture fitness functions and typo/format/docs-light/non-cloud work.
- Routed Solution Architecture methodology into `workspace-discovery-auditor`, `requirements-author`, `implementation-planner`, `agent-team-designer`, `test-eval-designer`, `risk-reviewer` and `docs-maintainer`.
- Added fixture eval check `solution_architecture_contract_present`; renderer file count is now 92 after adding four Solution Architecture artifact templates.

Severity and false-positive resolution:

- Missing architecture scope, context/container boundaries, boundary owner, public contract trace, data ownership, trust boundary review, ADR, observability and migration rollback are `P1_high_risk` when applicable.
- Diagram render checks and architecture fitness functions are `P2_recommended` unless a later risk gate raises severity.
- Typo-only docs edits, formatting-only edits, docs-light prototypes without reviewed/diffable diagrams and non-cloud work without Well-Architected review keep `solution_architecture` not applicable.
- Unsupported architecture claims are rejected as evidence and routed to `architecture-review-record.md`.

### `T9-D4` Quality, Testing and Evals Integration

Status: `done`

Source audited: `docs/methodologies/quality-testing-evals.md`

Deep-audit deltas implemented:

- Treat quality as current evidence: command, eval, runtime, manual or explicit inspection-only gap evidence with owner, freshness, environment, expected result, actual result and residual risk.
- Do not treat generic "tests exist", old CI status, line coverage, screenshots without criteria or inspection-only review as quality proof.
- Add discovery signals for quality directories, test/eval config files, CI workflows, coverage reports, Playwright/Cypress/Storybook/Pact/Promptfoo/Ragas/Stryker/Hypothesis/Codecov/GitHub Actions signals and flaky-test evidence; detection remains `present_unverified`.
- Add stable eval fields for every quality gate: `quality_strategy_contract_present`, `risk_based_scope_contract_present`, `test_first_or_gap_contract_present`, `acceptance_traceability_contract_present`, `contract_check_contract_present`, `runtime_evidence_contract_present`, `manual_qa_evidence_contract_present`, `visual_a11y_evidence_contract_present`, `eval_spec_contract_present`, `eval_rerun_evidence_contract_present`, `current_evidence_before_completion_contract_present`, `ci_quality_gate_contract_present`, `flaky_test_policy_contract_present`, `coverage_policy_contract_present`, `test_data_privacy_contract_present`, `bug_reproduction_evidence_contract_present`, `regression_impact_contract_present` and `unsupported_quality_claims_rejected_contract_present`.
- Map recommendations with exact gate, priority and artifact: missing local test command/evidence -> `quality_strategy_present` `P0_blocker` -> `quality-strategy.md`; risky/broad/constrained scope -> `risk_based_scope_present` `P1_high_risk` -> `quality-strategy.md`; acceptance traceability -> `acceptance_traceability_present` `P1_high_risk` -> `test-eval-matrix.md`; deterministic bugfix/business rule without test-first or gap -> `test_first_or_gap_present` `P1_high_risk` -> `test-eval-matrix.md`; API/event/schema contract gap -> `contract_check_present` `P1_high_risk` -> `api-contract-review.md`; runtime claim without evidence -> `runtime_evidence_present` `P1_high_risk` -> `manual-qa-evidence.md`; visual/a11y gap -> `visual_a11y_evidence_present` `P1_high_risk` for public UI and `P2_recommended` for internal UI -> `manual-qa-evidence.md`; AI/subjective eval spec or rerun gap -> `eval_spec_present` or `eval_rerun_evidence_present` `P1_high_risk` -> `ai-eval-spec.md` or `EVALS.md`; CI quality gate gap -> `ci_quality_gate_present` `P1_high_risk` for release/shared branch and `P2_recommended` otherwise -> `ci-evidence-record.md`; flaky/retry without owner/expiry -> `flaky_test_policy_present` `P2_recommended` -> `flaky-test-policy.md`; coverage-as-proof claim -> `unsupported_quality_claims_rejected` `P1_high_risk` and coverage policy gap -> `coverage_policy_present` `P2_recommended` -> `quality-strategy.md`; test data privacy gap -> `test_data_privacy_present` `P1_high_risk` -> `quality-strategy.md`; bugfix without reproduction -> `bug_reproduction_evidence_present` `P0_blocker` or accepted gap -> `bug-rescue-report.md`/`RUNLOG.md`; regression impact missing -> `regression_impact_present` `P1_high_risk` -> `test-eval-matrix.md`; completion claim without current evidence -> `current_evidence_before_completion` `P0_blocker` -> `RUNLOG.md`; unsupported quality claims -> `unsupported_quality_claims_rejected` `P1_high_risk` -> `quality-strategy.md`.
- Create five staged artifact templates in this slice: `test-eval-matrix.md`, `quality-strategy.md`, `ci-evidence-record.md`, `flaky-test-policy.md` and `manual-qa-evidence.md`.
- Strengthen generated `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with quality strategy, risk scope, acceptance traceability, contract/runtime/manual/visual evidence, eval baseline/rerun, CI evidence, flaky policy, coverage policy, test data privacy and current evidence before completion.
- Map source candidate artifacts into the five templates or existing artifacts: `red-green-refactor-log.md`, `bug-reproduction.md`, `risk-based-test-plan.md`, `regression-impact-map.md`, `contract-test-map.md`, `runtime-evidence.md`, `visual-a11y-evidence.md`, `coverage-policy.md`, `manual-qa-charter.md` and `evidence-packet.md` are covered by the five templates plus `TEST.md`, `EVALS.md`, `RUNLOG.md`, `ai-eval-spec.md`, `api-contract-review.md`, `bug-rescue-report.md` and `ci-stabilization-report.md`. Standalone `mutation-test-report.md`, `property-test-spec.md`, `flaky-test-ledger.md`, `ci-quality-gates.md` and `eval-run-report.md` are deferred until a later domain or stack-specific slice proves separate ownership.
- Route Quality, Testing and Evals through `workspace-discovery-auditor`, `requirements-author`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `docs-maintainer` and `pr-release-operator`.
- Reject unsupported claims as evidence: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate because they are most realistic, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Preserve lightweight false-positive behavior for typo-only docs edits, formatting-only changes, docs-only source cleanup and dependency metadata changes without behavior impact.

Implemented scope:

- Added `quality_testing_evals` catalog coverage for quality strategy, risk based scope, test-first evidence or accepted gap, acceptance traceability, contract checks, runtime evidence, manual QA evidence, visual/a11y evidence, eval spec, eval rerun evidence, current evidence before completion, CI quality gate, flaky-test policy, coverage policy, test data privacy, bug reproduction, regression impact and unsupported-claim rejection.
- Added read-only audit recommendations with deterministic gate, priority and artifact mapping for missing local evidence, risky scope, traceability, deterministic changes, API/event/schema contracts, runtime claims, public/internal UI visual evidence, AI evals, CI gates, flaky retries, coverage-as-proof claims, test data privacy, bug reproduction, regression impact and completion claims.
- Added staged artifact templates: `test-eval-matrix.md`, `quality-strategy.md`, `ci-evidence-record.md`, `flaky-test-policy.md` and `manual-qa-evidence.md`.
- Strengthened generated `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with quality evidence gates, statuses and behavioral eval coverage for completion claims without current evidence.
- Added quality discovery signals and kept detection as `present_unverified`, not readiness evidence.
- Routed Quality, Testing and Evals into `workspace-discovery-auditor`, `requirements-author`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `docs-maintainer` and `pr-release-operator`.
- Added fixture eval check `quality_testing_evals_contract_present`; renderer file count is now 97 after adding five Quality, Testing and Evals artifact templates.

Severity and false-positive resolution:

- Missing local command/evidence and completion claims without current evidence are `P0_blocker`.
- Risky scope, missing acceptance traceability, deterministic change without test-first evidence or accepted gap, public API/event/schema contract gaps, runtime evidence gaps, public UI visual/a11y gaps, AI eval baseline/rerun gaps, test data privacy gaps and regression impact gaps are `P1_high_risk` when applicable.
- Internal UI visual/a11y gaps, flaky-test ownership and coverage policy gaps are `P2_recommended` unless another risk gate raises severity.
- Typo-only docs edits, formatting-only edits, docs-only source cleanup and dependency metadata changes without behavior impact keep `quality_testing_evals` not applicable.
- Unsupported quality claims are rejected as evidence and routed to `quality-strategy.md`.

### `T9-D5` Codex / Agentic Workflow Integration

Status: `done`

Source audited: `docs/methodologies/codex-agentic-workflow.md`

Deep-audit deltas implemented:

- Represented Codex / Agentic Workflow as durable control-plane and capability governance, not chat memory or broad agent orchestration.
- Used the full gate set: `agentic_scope_classified`, `source_of_truth_present`, `control_plane_present`, `read_only_discovery_complete`, `approval_boundary_present`, `fresh_context_handoff_present`, `ownership_split_present`, `subagent_parallelism_safe`, `skill_promotion_evidence_present`, `plugin_boundary_present`, `mcp_permission_review_present`, `hook_activation_approval_present`, `automation_manual_stability_present`, `model_reasoning_policy_present`, `memory_policy_present`, `agent_eval_workflow_present` and `agentic_evidence_before_completion`.
- Added severity policy so control-plane/source-of-truth gaps, side-effecting MCP, hook activation, external writes, production data, overlapping subagent edits, active automation and completion claims without evidence are blocker or high-risk when applicable, while lightweight docs/local work remains warning or not applicable.
- Added runtime routing shape for Codex App, IDE extension, CLI, `codex exec`, GitHub Action, MCP, Agents SDK and automation, with no default escalation to MCP, Agents SDK or automation.
- Added lifecycle test policy for skills: trigger tests, negative trigger tests, missing-input behavior, verification-failure behavior and failure-log evidence.
- Set automation promotion threshold to at least two successful manual runs or an explicit owner-approved accepted gap.
- Distinguished staged hook templates, read-only validation hooks and blocking/side-effecting hooks; hook activation requires trust review, event/matcher/command, failure behavior, disable path and explicit approval.
- Required MCP review for new MCP config, changed trust boundary, auth/secrets, remote servers, side-effecting tools, production/customer data or external writes; read-only local docs MCP can be lower severity but still records capability/data boundary.
- Required worktrees or explicit ownership for parallel subagents when edits can overlap, generated files are shared, migrations/contracts/public APIs/schemas are touched, or merge/rollback risk is high; read-only research can use packets without worktrees.
- Clarified Codex-native subagents vs Agents SDK: Codex-native subagents are default for Codex App/CLI/IDE engineering delegation; Agents SDK is for code-owned agent apps with application-owned orchestration, tools, guardrails, sessions, tracing and evals.
- Expanded agent eval workflow with baseline, trace-derived dataset, tool-call correctness, handoff correctness, expected/forbidden behavior, grader or deterministic assertion, threshold, rerun command, regression label, latency/cost and privacy/no-secrets handling.

Implemented scope:

- Added `codex_agentic_workflow` catalog coverage for control plane, source of truth, read-only discovery, approval boundaries, model/reasoning policy, memory policy, handoffs, ownership split, subagent safety, MCP review, hook governance, plugin boundary, skill promotion, automation stability, agent eval workflow, evidence before completion and unsupported-claim rejection.
- Added read-only audit recommendations with deterministic gate, priority and artifact mapping for missing control plane, missing source of truth, missing read-only discovery, missing approval boundary, subagent/parallel work without ownership, MCP side effects, hook activation, plugin packaging, repeated workflow promotion, automation schedules, model/reasoning policy gaps, memory-as-source-of-truth claims, agent behavior without eval workflow and completion claims without evidence.
- Added staged artifact templates: `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md` and `agent-eval-workflow.md`.
- Strengthened generated `AGENTS.md`, `.codex/config.toml`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json`, `behavioral-workflows.json`, `agent-task-packet.md`, `worktree-ownership.md`, `automation-candidate.md` and `handoff-contract.md` with Codex workflow gates, runtime routing, approval boundaries and no silent activation.
- Added Codex workflow discovery signals for `.codex/`, agents, workflows, artifact templates, skills, plugins, subagents, MCP, hooks, automation, task packets, handoff/worktree artifacts, source-of-truth terms, approval-boundary terms and side-effect risks. Detection remains `present_unverified`.
- Routed Codex / Agentic Workflow into all 11 lifecycle skills while keeping hooks, MCP, automation, external writes and Agents SDK orchestration approval-bound.
- Added fixture eval check `codex_agentic_workflow_contract_present`; renderer file count is now 102 after adding five Codex workflow artifact templates.

Candidate artifact mapping:

- `context-memory-policy.md` is covered by `AGENTS.md`, `.codex/config.toml`, `model-reasoning-policy.md` and generated `PLAN/EVALS/RUNLOG` memory-policy fields until a later slice proves separate ownership.
- `agentic-workflow-readiness.md` is covered by `project-readiness.json`, generated `PLAN/TEST/EVALS/RUNLOG` and the `codex_agentic_workflow_contract_present` fixture check.
- `agent-eval-case.md` is covered by `agent-eval-workflow.md` plus `behavioral-workflows.json`; standalone cases can be added when a real agent app needs separate ownership.
- `skill-candidate.md` and `skill-failure-log.md` are covered by `skill-promotion-record.md`.
- `hook-activation-record.md` is covered by `hook-governance.md`.
- `docs/sources/registry.md` was checked for T9-D5 source impact; no new registry entry was added because this slice operationalizes already checked-in methodology/research files and existing official Codex references rather than introducing new external source-backed platform claims. The existing Track 9 internal source entry was refreshed to mention T9-D5 coverage.

Severity and false-positive resolution:

- Missing control plane, source of truth, approval boundary, side-effecting MCP review, hook activation approval, overlapping subagent ownership, active automation stability and evidence-before-completion are blocker or high-risk when applicable.
- Skill promotion evidence, plugin boundary, model/reasoning policy, memory policy and agent eval workflow are high-risk or recommended depending on scope and side-effect risk.
- Simple docs/local work does not force subagents, worktrees, MCP review, hooks, plugin packaging, automation, Agents SDK orchestration or agent eval workflow unless explicit signals, user intent or side-effect boundaries make them applicable.
- Unsupported agentic workflow claims are rejected as evidence: memory is project source of truth, subagents are automatically faster, MCP tools are safe because they are tools, hooks are harmless convenience scripts, repeated workflows should become automation immediately, Agents SDK and Codex runtime are the same layer, and inspection proves completion.

### `T9-D6` Frontend Integration

Status: `done`

Source audited: `docs/methodologies/frontend.md`

Deep-audit deltas implemented:

- Represented frontend as user-observable UI behavior and browser/runtime evidence, not component hierarchy or code inspection.
- Used the full gate set: `frontend_user_flow_acceptance_present`, `frontend_component_docs_present`, `frontend_component_state_matrix_present`, `frontend_design_system_boundary_present`, `frontend_fsd_boundary_reviewed`, `frontend_api_contract_alignment_present`, `frontend_accessibility_review_present`, `frontend_keyboard_focus_contract_present`, `frontend_responsive_viewport_matrix_present`, `frontend_visual_evidence_present`, `frontend_runtime_console_evidence_present`, `frontend_performance_budget_present`, `frontend_browser_support_present`, `frontend_content_i18n_boundary_present` and `frontend_interaction_test_evidence_present`.
- Kept Storybook and Feature-Sliced Design conditional: Storybook is documentation and verification surface, not proof by itself; FSD applies only when UI scale/coupling or owner decision justifies layer/slice/segment/public API/import-rule review.
- Set public UI default accessibility target to WCAG 2.2 AA unless an owner records an accepted exception.
- Required browser/runtime evidence, console status, Playwright trace or accepted gap before UI completion claims.
- Added visual baseline stability, responsive/input/theme coverage, API/data state alignment, route/page inventory and performance budget policies.
- Rejected unsupported frontend claims as evidence: FSD is mandatory for every frontend project, Storybook proves UI quality, automated accessibility addon output is enough, a desktop screenshot proves responsive UI, lab Web Vitals always represent production UX and code inspection proves UI completion.

Implemented scope:

- Added `frontend` catalog coverage for user flows, component docs, state matrices, design-system governance, FSD boundaries, API/data alignment, accessibility, keyboard/focus, responsive/visual/runtime evidence, interaction tests, performance, browser support, content/i18n and unsupported-claim rejection.
- Added frontend discovery signals for UI framework/package/filesystem evidence, routes/pages/components, Storybook, Playwright, Testing Library, axe, Chromatic, tokens/themes/components metadata and UI terms. Detection remains `present_unverified`.
- Added read-only audit recommendations with deterministic priority, gate, artifact, evidence, approval, accepted-gap and residual-risk fields for frontend gaps.
- Added staged artifact templates: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md` and `frontend-performance-budget.md`.
- Strengthened `component-card.md` with the full Track 9 template contract plus user flow, component state, Storybook, FSD, API, accessibility and design-system ownership fields.
- Strengthened generated `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with frontend readiness, evidence and shortcut-resistance fields.
- Routed Frontend methodology into `workspace-discovery-auditor`, `requirements-author`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `docs-maintainer` and `pr-release-operator`.
- Added synthetic `frontend-ui-app` fixture with React/Vite, Storybook, Playwright, Testing Library/a11y, design token/component metadata and no secrets/private data.
- Added fixture eval check `frontend_contract_present`; renderer file count is now 107 after adding five Frontend artifact templates.

Candidate artifact mapping:

- `ui-flow-spec.md` is covered by `frontend-flow-spec.md`.
- `component-state-matrix.md` is covered by `frontend-state-matrix.md`.
- `accessibility-review.md` is covered by `frontend-accessibility-review.md`.
- `route-page-inventory.md`, `frontend-api-dependency-map.md` and `frontend-content-i18n-record.md` are covered by `frontend-flow-spec.md` until a later slice proves separate ownership.
- `storybook-story-map.md`, `design-system-inventory.md`, `design-tokens-reference.md`, `frontend-boundary-map.md` and `fsd-boundary-record.md` are covered by `component-card.md` and `frontend-state-matrix.md`.
- `responsive-viewport-matrix.md`, `keyboard-focus-map.md`, `visual-evidence-packet.md` and `frontend-browser-support-matrix.md` are covered by `frontend-visual-qa.md` and `frontend-accessibility-review.md`.
- `frontend-interaction-test-matrix.md` is covered by `test-eval-matrix.md`, `manual-qa-evidence.md` and the frontend interaction evidence gate.
- TypeScript alias/import/public API violation analysis for FSD is deferred to a later architecture/static-analysis hardening slice; T9-D6 implements lightweight structure detection plus owner/gap routing to avoid false positives.
- `docs/sources/registry.md` was checked for T9-D6 source impact; no new registry entry was added because the relevant frontend source entries already exist for Codex frontend designs, Storybook, Playwright, Testing Library, WCAG, web.dev and Feature-Sliced Design.

Severity and false-positive resolution:

- Missing user-flow acceptance, API/data state alignment, accessibility, runtime console evidence, interaction evidence and unsupported completion claims are blocker or high-risk when applicable.
- Component docs, design-system governance, FSD boundary review, responsive/visual coverage, performance budgets, browser support and content/i18n are high-risk or recommended depending on public surface and release risk.
- Backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD work does not force frontend gates.
- External visual services, hosted browser services, production-data screenshots and publication remain `approval_required`.

### `T9-D7` Backend Integration

Status: `done`

Source audited: `docs/methodologies/backend.md`

Batch 1 implemented scope (`T9-D7-M0` through `T9-D7-M9`):

- Represented backend as runtime behavior, production failure modes, operational evidence and owner-reviewed boundaries, not as package structure or service count.
- Added `backend` catalog coverage for service boundaries, runtime behavior, dependency failure policy, observability, SLO/gap, health probes, jobs/queues, data consistency, config/secrets, security review, rollback and unsupported-claim rejection.
- Added backend discovery signals for backend/server/service/worker/job/queue/scheduler/consumer/adapter/repository/migration paths, Docker/Procfile/docker-compose/Kubernetes/serverless files, OpenAPI/AsyncAPI/protobuf contracts and backend runtime terms. Detection remains `present_unverified`.
- Added read-only audit recommendations with deterministic priority, gate, artifact, evidence, approval, accepted-gap and residual-risk fields for backend gaps.
- Added staged artifact templates: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md` and `backend-operational-runbook.md`.
- Strengthened `architecture-overview.md`, `api-contract-review.md`, `quality-strategy.md`, `test-eval-matrix.md` and `manual-qa-evidence.md` with backend boundary, API/event contract and runtime verification overlap terms.

Candidate artifact mapping:

- Module/service boundary map is covered by `backend-service-overview.md` and `architecture-overview.md`.
- Ports and Adapters map is covered by `backend-service-overview.md` until a later architecture slice proves separate ownership.
- Security notes are covered by `security-risk-review.md` and `backend-config-secrets-manifest.md`.
- SLO ownership remains split: backend owns service SLI/SLO shape via `backend-slo-sheet.md`; Delivery/Operations will own release and operational gate depth in `T9-D12`.
- Distributed workflow recovery evidence is covered by `backend-data-consistency-record.md`, `backend-runtime-behavior.md` and `backend-operational-runbook.md`.
- Contract-aware backend development is covered by `api-contract-review.md`, `backend-service-overview.md` and `backend-job-queue-contract.md` until `T9-D8` owns API/Integration detail.

Batch 1 false-positive and unsupported-claim resolution:

- Frontend-only, docs-only, CLI-only, native-only, dependency-metadata-only and package-name-only service folder work does not force backend gates.
- Unsupported backend claims are rejected as evidence: backend means only business logic files, microservices are the professional default, retries make systems reliable, health endpoint solves readiness, logs are observability and SLOs only matter for large companies.
- Fixture eval renderer/count sync is added as a batch-1 guard: `backend_contract_present` now covers the catalog/templates/discovery/audit backend contract and renderer output is `118` files. Full lifecycle skill routing, generated control-plane/eval template sync, source registry/docs sync and final `T9-D7-M13` depth remain pending later T9-D7 batches.

Batch 1 verification:

- `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_fixture_eval_runner -v` ran 150 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 393 tests with `OK`.

Batch 2 implemented scope (`T9-D7-M10` through `T9-D7-M19`):

- Strengthened backend security/secrets overlap: `security-risk-review.md` and `backend-config-secrets-manifest.md` now cover authn/authz, tokens, PII, money movement, privileged operations, external writes, irreversible side effects, no-secrets handling for docs/prompts/fixtures/logs and `approval_required` boundaries.
- Added generated control-plane/eval backend coverage in `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json`; backend shortcuts now explicitly reject package-docs-only runtime proof, logs-only observability, health-endpoint-only readiness, retry-only reliability and default microservices.
- Routed Backend through lifecycle skills for workspace discovery, requirements, implementation planning, test/eval design, risk review, docs maintenance and PR/release operation. Shared wording keeps microservices conditional and requires runtime/failure/observability/security/rollback evidence or accepted gaps.
- Completed the first full `backend_contract_present` fixture eval depth by adding lifecycle/control-plane/eval coverage and a positive synthetic `backend-service-app` fixture.
- Strengthened false-positive and approval-bound behavior: backend detection remains `present_unverified`, production data/external writes/secrets/deploy actions remain approval-bound, and backend completion needs owner-reviewed evidence sufficiency or an accepted gap.
- Deepened unsupported-claim handling, modular-monolith/microservice policy, Ports and Adapters / DDD boundary policy, and runtime/retry/idempotency/backpressure policy in templates and audit recommendations.

Batch 2 verification:

- `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixtures tests.product_agent_os.test_discovery tests.product_agent_os.test_fixture_eval_runner -v` ran 204 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer output still at 118 files.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 401 tests with `OK`.

Batch 3 implemented scope (`T9-D7-M20` through `T9-D7-M29`):

- Clarified the active Track 9 plan so `T9-D7-M26/M27` record incremental backend batch evidence and final verification scope, without claiming full `T9-D7` closure before the remaining backend rows are complete.
- Deepened dependency failure policy: `backend-dependency-failure-matrix.md` and audit recommendations now require per dependency timeout, retry/backoff/max attempts, circuit breaker non-applicability, fallback, alert owner and verification evidence.
- Deepened job/queue policy: `backend-job-queue-contract.md` now records dead-letter queue, dead-letter behavior, idempotency key, replay procedure, poison-message handling, deduplication policy, ordering guarantee and backpressure.
- Deepened data consistency policy: `backend-data-consistency-record.md` and `migration-plan.md` now cover local transaction, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path.
- Deepened observability and logging policy: `backend-observability-map.md` now rejects logs-only observability and requires traces, metrics, logs, dashboards, alerts, correlation IDs, alert ownership, redaction and no-private-payload logging.
- Deepened SLI/SLO, health and operations evidence: `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-operational-runbook.md` and readiness gates now record SLI/SLO or explicit gap, no-telemetry/not-yet-production gap, health endpoint semantics, liveness/readiness/startup/platform equivalent, operational owner, escalation path, evidence freshness and handoff to Delivery/Operations.
- Deepened rollback/recovery evidence: `backend-release-rollback-notes.md` and `release-packet.md` now require rollback command or manual procedure, data recovery/replay, irreversible side effects, owner approval and residual risk.
- Added optional Twelve-Factor service discipline vocabulary across backend service/config/runtime templates: explicit dependencies, config/env keys, build-release-run, process model, stateless process or accepted gap, admin tasks, dev/prod parity and logs-as-event-stream, without making Twelve-Factor mandatory.
- Added service-boundary owner review and ADR routing depth: `backend-service-overview.md`, `adr.md` and audit recommendations now require changed backend responsibility, owner review, decision authority, boundary rationale and ADR link or accepted gap.
- Expanded `backend_contract_present` fixture eval terms and payload sources to include the new resilience, operations, Twelve-Factor and owner-review evidence.
- Synced root `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` with batch-level backend evidence and residual risk; Product-Agent OS public docs/source registry refresh remains planned in `T9-D7-M44`.

Batch 3 verification:

- RED run: focused new tests failed as expected before implementation on missing resilience/operations/Twelve-Factor/owner-review terms in backend templates, audit recommendations and fixture eval contract.
- `python -m unittest tests.product_agent_os.test_infrastructure_templates.InfrastructureTemplateTest.test_backend_resilience_operations_twelve_factor_and_owner_review_depth tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_backend_resilience_ops_twelve_factor_and_owner_review_recommendations tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_backend_contract_terms_include_resilience_ops_depth -v` ran 3 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_fixture_eval_runner -v` ran 105 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v` ran 84 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v` ran 134 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; renderer file count stayed 118.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 404 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.

Batch 4 implemented scope (`T9-D7-M30` through `T9-D7-M39`):

- Strengthened backend requirements intake in `requirements-author` and generated `REQUIREMENTS.md`: service/user behavior, non-goals, runtime constraints, affected backend unit, dependencies, data stores, operational assumptions and explicit gaps are recorded before implementation planning.
- Deepened backend security notes: `security-risk-review.md`, `backend-config-secrets-manifest.md` and audit recommendations now distinguish authn/authz, secrets, rate limits, audit logging, sensitive data, abuse cases, privileged operations and no-secrets evidence.
- Deepened observability, SLO, health and runbook evidence: backend artifacts now include semantic conventions or accepted gaps, collector/instrumentation notes, redaction policy, health checks tested where platform/runtime is available, platform-unavailable gap owner/reason/follow-up, log/query links or placeholders and severity assumptions.
- Deepened config/secrets and rollback evidence: config manifests now require required/optional status and no-secrets/no-private-data constraints for docs, prompts, fixtures, logs and examples; rollback artifacts and release packet now include feature flag, verification command and rollback/no-rollback rationale.
- Deepened contract-aware backend evidence: `backend-service-overview.md`, `api-contract-review.md` and `backend-job-queue-contract.md` now record APIs/events/external providers, OpenAPI, AsyncAPI, Pact, protobuf/provider contracts and contract changes synced with code and tests.
- Added `backend_dependency_signals` discovery packet with `present_unverified` categories for database, message broker, cache, payment, email, storage, search and third-party HTTP/provider clients, plus synthetic fixture files covering each category.
- Corrected the active Track 9 plan rows for release packet work to reference `assets/templates/workflows/release-packet.md`, not a non-existent artifact-template file.

Batch 4 verification:

- RED run: focused new tests failed as expected before implementation on missing backend intake, security/observability/health/runbook/config/rollback/contract depth and missing `backend_dependency_signals`.
- `python -m unittest tests.product_agent_os.test_infrastructure_templates.InfrastructureTemplateTest.test_backend_intake_security_ops_and_contract_depth tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_backend_intake_security_ops_contract_and_health_recommendations tests.product_agent_os.test_discovery.DiscoveryTest.test_backend_dependency_signals_distinguish_categories_as_present_unverified tests.product_agent_os.test_discovery.DiscoveryTest.test_backend_service_fixture_routes_backend_methodology tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_backend_contract_terms_include_resilience_ops_depth -v` ran 5 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v` ran 208 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; renderer file count stayed 118.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 407 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.

Batch 5 implemented scope (`T9-D7-M40..M45`):

- Added backend delivery discovery signals for backend stack, backend commands, CI, APIs, DB, queues, workers, deployment manifests and security signals. Discovery stays read-only and records `present_unverified` without executing deployments, commands, CI or external writes.
- Added lightweight retry/idempotency discovery signals for retry/idempotency terms, dependency context and job context. Deeper static analysis of retry correctness is deferred with owner/reason to avoid false positives.
- Defined backend severity policy: risky production backend without service boundary, runtime/failure evidence, security route or rollback is blocker/high-risk; missing observability, SLO, health verification or owner review remains high-risk unless accepted gap fields are complete; simple local/backend-light work stays warning/not-applicable depth.
- Kept T9-D7 backend templates framework-agnostic: stack-specific backend snippets deferred until Node.js, Python, Java, .NET and Go research proves owner, examples and verification.
- Refreshed Product-Agent OS source registry and user-facing docs for `backend_contract_present`, Backend eval coverage and backend methodology routing.
- Routed semantic evidence sufficiency to the cross-domain semantic sufficiency backlog/T9-S: backend completion evidence records whether the human owner reviewed test/eval/runtime evidence sufficiency for real project risk or accepted gap owner, reason, review date, downstream risk and follow-up.

Batch 5 verification:

- RED run: focused new tests failed as expected before implementation on missing backend delivery/resilience discovery packets, severity policy, framework-agnostic snippet policy, docs/source sync, fixture terms and owner-reviewed evidence sufficiency routing.
- GREEN run: `python -m unittest tests.product_agent_os.test_discovery.DiscoveryTest.test_backend_delivery_signals_record_commands_ci_deploy_without_execution tests.product_agent_os.test_discovery.DiscoveryTest.test_backend_resilience_signals_are_lightweight_present_unverified tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_backend_severity_policy_and_lightweight_retry_recommendations tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_backend_routes_semantic_evidence_sufficiency_to_owner_review_backlog tests.product_agent_os.test_lifecycle_skills.LifecycleSkillsTest.test_workspace_discovery_records_backend_delivery_signals_without_execution tests.product_agent_os.test_infrastructure_templates.InfrastructureTemplateTest.test_backend_framework_agnostic_and_evidence_sufficiency_policy tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track9_backend_docs_and_source_registry_are_synced tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_backend_contract_terms_include_resilience_ops_depth -v` ran 8 tests with `OK`.
- Focused backend/domain suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v` ran 232 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 414 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 42 fixtures, 0 failures, renderer file count 118 and `backend_contract_present: true`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

### `T9-D8` API and Integrations Integration

Status: `done`

Source audited: `docs/methodologies/api-integrations.md`

Deep-audit deltas implemented:

- Treat API methodology as a contract-source discipline, not a rendered-docs discipline: OpenAPI/AsyncAPI/GraphQL/protobuf/JSON Schema/Pact sources count as evidence, while Swagger UI is not source of truth.
- Split schema validation from contract testing: contract-test evidence records provider verification, consumer-driven checks, negative cases, compatibility rules and missing-tool gaps.
- Add explicit consumer and compatibility gates for public and internal APIs; internal APIs can still have consumers and breaking-change risk.
- Add security and error depth: contract-linked security schemes, scopes, token claims, object-level authorization, rate limits, abuse cases, sensitive fields, RFC 9457 Problem Details or an explicit error-model compatibility gap.
- Add event/webhook delivery evidence: schema, headers, signature verification, correlation ID, idempotency key, retry policy, ordering guarantee, replay, dead-letter behavior and CloudEvents applicability or non-applicability.
- Add generated SDK reproducibility: generator, version, config, target languages, regeneration command, reviewable diff, SemVer impact and release process.
- Keep API style choices conditional: GraphQL, gRPC, event-driven APIs, Spectral, Redocly and framework-native linting are not universal defaults.
- Preserve API-only/backend false-positive protection: API-only contract fixtures do not force Backend blockers unless runtime/server/service/worker evidence exists.
- Keep external writes approval-bound: provider mutation, generated client publication, webhook registration and other external actions require `approval_required`.

Implemented scope:

- Added `api_integrations` catalog coverage with applies/not-applicable rules, maturity/complexity impact, decision horizons, artifacts, gates, eval fields and overlaps.
- Added read-only API discovery signals for OpenAPI, Swagger source files, AsyncAPI, GraphQL schema, protobuf, JSON Schema, Pact, webhooks/events, generated clients and external providers.
- Added audit recommendations for `api_contract_source_present`, `api_consumer_map_present`, `api_breaking_change_reviewed`, `api_security_reviewed`, `api_error_contract_present`, `api_contract_test_matrix_present`, `event_delivery_contract_present`, `generated_client_manifest_present`, `external_write_approval_present`, `api_observability_contract_present`, `api_style_choice_recorded` and unsupported API claims.
- Added staged artifact templates: `api-inventory.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md` and `api-style-guide.md`.
- Strengthened `api-contract-review.md`, `migration-plan.md`, `integration-catalog.md`, generated control-plane templates, `project-readiness.json`, `behavioral-workflows.json`, lifecycle skills, Product-Agent OS README and operator docs.
- Added synthetic fixtures for full API contract coverage, external-write approval, Swagger-UI-only false positive and GraphQL/gRPC style choice.
- Added fixture eval check `api_integrations_contract_present`; renderer file count increased from 118 to 128 after the ten new API templates.

Severity and false-positive resolution:

- Public, breaking, security-sensitive, event/webhook, generated SDK and external-write gaps are high-risk or blocker depth as appropriate.
- Simple local/internal prototype work can use `not_applicable`, `P2_recommended` or `explicit_gap_accepted` only with owner, reason, review date, downstream consumer risk and follow-up.
- API-only contract fixtures do not force Backend blockers.
- Unsupported claims rejected: Swagger UI is source of truth, schema validation is contract testing, OAuth proves API security, GraphQL/gRPC/events are mandatory defaults and internal APIs have no consumers.
- API lint tooling deferred with owner/reason: Spectral, Redocly, framework-native linting, JSON Schema/protobuf/GraphQL/AsyncAPI compatibility rules, API security profile and stack-specific contract test generators remain candidate choices, not universal Product-Agent OS defaults.
- multi-repository generated clients deferred until a later slice proves owner, repo boundaries, release process and safe write/approval flow.

Verification:

- RED runs: focused API catalog/audit/discovery/template/lifecycle/fixture/docs tests failed before implementation on missing API catalog gates, recommendations, discovery signals, readiness/control-plane terms, docs sync and fixture eval checks.
- Focused T9-D8 GREEN runs passed for catalog, audit, discovery, template, lifecycle, fixture and docs contracts before the final verification batch.
- Focused T9-D8 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures -v` ran 242 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 45 fixtures, 0 failures, renderer file count 128 and `api_integrations_contract_present: true`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 424 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

### `T9-D9` Database and Data Integration

Status: `done`

Source audited: `docs/methodologies/database-data.md`

Deep-audit deltas to implement:

- Treat Database & Data as a full methodology domain, not only the existing `data_migration` usage-mode workflow.
- Separate database gates for inventory, dictionary, schema source, migration plan, expand/contract rollout, transaction boundary, rollback feasibility, backup/restore evidence, data classification, data quality, data contract, lineage, query/index performance, retention/deletion, synthetic fixtures, production access approval and unsupported-claim rejection.
- Keep database tooling conditional. PostgreSQL, Liquibase, Flyway, Alembic, Prisma, Rails/Django migrations, dbt, Great Expectations, OpenLineage, DBML, dbdocs, SchemaSpy and schema-diff tooling are candidate evidence sources, not universal Product-Agent OS defaults.
- Keep DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation `approval_required`.
- Use conservative destructive-change detection for `DROP`, rename, truncate, destructive cleanup, retention purge, unsafe `EXPLAIN ANALYZE` on writes, ORM/schema drift and manual SQL-only changes. These are questions/recommendations, not execution or full SQL parser claims.
- Preserve Track 8 `data_migration` compatibility: existing route mode and generic `migration-plan.md` remain valid, while database-specific work also stages or recommends `database-migration-plan.md` and related database artifacts.
- Add a stable `database_data_signals` packet while keeping backward-compatible `data_migration_signals`.
- Cover runtime/data pipeline signals: database clients, ORM models, data warehouse jobs, scheduled pipelines, reporting tables, analytics models and RAG ingestion sources stay `present_unverified`.
- Explicit eval wording: runtime/pipeline/RAG signals stay `present_unverified` until owner-reviewed runtime, lineage or ingestion evidence exists.
- Deepen privacy and restore evidence: legal basis, minimization, retention, deletion/export path, access boundary, restore target, RPO/RTO, restore drill date/result and verification result.

Planned implementation scope:

- Fill `database_data` catalog coverage with applies/not-applicable rules, maturity/complexity impact, decision horizons, artifacts, gates, eval fields and cross-domain overlaps.
- Add read-only database discovery, audit recommendations, fixture eval contract, generated control-plane/eval coverage, lifecycle skill routing and synthetic fixtures.
- Add staged database artifact templates for inventory, migration plan, expand/contract, backfill runbook, rollback feasibility, backup/restore, data classification, data quality, data contract, lineage, query performance, retention/deletion, synthetic fixtures and production access approval.
- Strengthen `database-dictionary.md`, `data-migration.md`, operator docs, README, source registry and root control-plane files after behavior is implemented.

Severity and false-positive resolution:

- Production data access, destructive migration, irreversible data loss, missing rollback, missing restore evidence, sensitive data leakage and broad production credentials are blocker/high-risk depth as appropriate.
- Schema-only files and local/demo database fixtures are `present_unverified` signals, not readiness proof and not automatic production blockers.
- Unsupported claims rejected: ORM schema is database source of truth, migration applied means safe, down migration means rollback-safe, backups exist means restore-safe, manual SQL is enough, anonymized production data is safe by default and lineage can be reconstructed later.
- Stack-specific migration tool defaults and schema-diff tooling deferred until a later stack/tooling decision proves owner, safety policy and verification evidence.

Verification:

- RED checks failed as expected before implementation on missing `database_data` catalog gates, audit recommendations, discovery packets, readiness/control-plane terms, docs/source sync and fixture eval checks.
- Focused T9-D9 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 234 tests with `OK`.
- Fixture runner tests: `python -m unittest tests.product_agent_os.test_fixture_eval_runner -v` ran 15 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 49 fixtures, 0 failures, renderer file count 142 and `database_data_contract_present: true`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 433 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Strict MkDocs: `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict` exited `0`.
- Diff hygiene: `git diff --check` exited `0`.

### `T9-D10` LLM / AI / RAG Integration

Status: `done`

Source audited: `docs/methodologies/llm-ai-rag.md`

Execution policy:

- Implement T9-D10 in batches of up to 10 matrix rows and report after each batch: `M0..M9`, `M10..M19`, `M20..M29`, then `M30..M36`.
- Commit, push and PR actions remain deferred until explicitly requested.

Deep-audit deltas to implement:

- Treat LLM / AI / RAG as a full methodology domain, not only the existing `ai_eval_regression` usage-mode workflow.
- Separate gates for user-visible AI behavior, baseline eval, eval rerun report, dataset governance, prompt contract, model decision, structured output, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding eval, agent workflow trace, safety review, cost/latency budget, no private data in fixtures and unsupported-claim rejection.
- Preserve existing Track 8 `ai_eval_regression` route and `ai_eval_signals`, while adding a stable read-only `llm_ai_rag_signals` packet.
- Detection remains `present_unverified`; no model calls, eval runs, vector DB access, external writes or owner approvals are performed during discovery.
- Keep eval tooling conditional. Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas and LangSmith are candidate tools, not universal defaults.
- Record template naming compatibility: source names such as `prompt-contract.md`, `model-decision-record.md` and `rag-eval-report.md` are canonical unless aliases are explicitly mapped.
- RAG quality must split retrieval quality and answer quality; citations alone are not proof.
- Tool/function calling is product capability: schema, permissions, side effects, idempotency, retries, errors and approvals are part of the contract.
- Agent workflows start with the smallest useful single-agent or manager pattern; multi-agent handoffs need owner and trace evidence.
- Datasets, prompts, fixtures, traces and screenshots must exclude secrets, credentials, raw private chats and private customer data.

Batch `M0..M9` implementation scope:

- Add RED tests for `llm_ai_rag` catalog, audit recommendations, discovery packet, false positives, readiness gate and `ai-eval-spec.md` rerun evidence.
- Fill `llm_ai_rag` catalog metadata and cross-domain overlaps.
- Add read-only `llm_ai_rag_signals` and `llm_ai_rag_readiness_when_ai_behavior_changes`.
- Add baseline eval and eval rerun/report recommendations with stable priority/artifact mapping.
- Strengthen `ai-eval-spec.md` for user-visible behavior promise, current result, baseline/current comparison, failed cases, current-run evidence, inspection-only gap and dataset privacy terms.

Batch `M0..M9` completed scope:

- Implemented the `llm_ai_rag` catalog contract, read-only discovery packet, readiness packet, baseline/rerun audit recommendations, unsupported-claim handling and false-positive guard for generic eval docs, docs-only AI mentions, generic context maps, `AGENTS.md`, generic tools, generic schemas and latency/cost-only evidence.
- Synced the existing fixture eval oracle with the new `llm_ai_rag_readiness` packet and conditional readiness gate id without adding the full AI/RAG fixture contract yet.
- Verification: focused T9-D10 tests ran 172 tests with `OK`; full unittest ran 438 tests with `OK`; fixture eval exited `0` after 49 fixtures with 0 failures; `python tools\check_docs.py` passed; `git diff --check` exited `0`.

Deferred from `M0..M9` to later T9-D10 batches:

- Full AI/RAG artifact template set, renderer registration and dedicated AI/RAG fixture eval contract are handled in `M20..M29`.
- Agent handoff compatibility, eval tooling selector, model migration threshold policy, RAG lifecycle/deletion/privacy, diff-signal policy, incident workflow and methodology report coverage are handled in `M30..M36`.

Batch `M10..M19` completed scope:

- Strengthened `llm_ai_rag` audit recommendation evidence for dataset governance, prompt contracts, model decisions, structured output, tool/function/MCP contracts, human approval boundaries, RAG source/retrieval/grounding, agent workflow traces, safety/guardrails and cost/latency budgets.
- Added a false-positive guard for non-behavior prompt documentation cleanup so prompt-writing docs do not force AI/RAG methodology blockers.
- Added source-aligned AI/RAG artifact templates: `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md` and `ai-cost-latency-budget.md`.
- Synced template inventory tests with the new files. Renderer registration, generated target mapping and renderer file count updates remain deferred to `T9-D10-M22`.
- Verification: focused audit/template suite ran 108 tests with `OK`; full unittest ran 439 tests with `OK`; fixture eval exited `0`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.

Deferred from `M10..M19` to later T9-D10 batches:

- Agent handoff compatibility, eval tooling selector, model migration threshold policy, RAG lifecycle/deletion/privacy, diff-signal policy, incident workflow and methodology report coverage remain in `M30..M36`.

Batch `M20..M29` completed scope:

- Resolved AI/RAG template naming compatibility with source-aligned canonical names: `prompt-contract.md`, `model-decision-record.md` and `rag-eval-report.md`. Plan-era names `ai-prompt-contract.md`, `ai-model-decision-record.md` and `rag-grounding-eval.md` are mapped through aliases rather than registered as duplicate renderer targets.
- Strengthened the existing Track 8 `ai-eval-regression.md` workflow and `ai-eval-spec.md` with app-backed eval path, baseline/current comparison, prompt/context inventory, retrieval metrics, grounding evidence, dataset governance, thresholds, failed cases, cost/latency and current-run evidence.
- Registered 15 AI/RAG artifact templates in the staged renderer under `.codex/artifact-templates/`; the `python-app` renderer file count increased from 142 to 157.
- Strengthened generated `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md` templates with `llm_ai_rag_readiness_when_ai_behavior_changes`, AI behavior promise, baseline/rerun evidence, dataset governance, prompt/model/schema/tool/RAG/agent/safety/cost evidence, accepted-gap handling and forbidden shortcut language.
- Added behavioral case `llm-ai-rag-evidence-before-completion` and a fifth synthetic transcript session so prompt-inspection-only and current-evidence-free AI/RAG quality claims are rejected.
- Added synthetic AI/RAG fixtures for prompt/model changes, tool approval, structured output, agent trace, latency/cost budget and RAG quality regression; fixture privacy checks reject secrets, tokens, raw private chats, customer data and live API keys.
- Added `llm_ai_rag_contract_present` to fixture eval coverage and routed `llm_ai_rag` through lifecycle skills without forcing one eval runner, multi-agent architecture or live model/API calls.
- Verification: focused AI/RAG fast suite ran 190 tests with `OK`; focused fixture runner suite ran 15 tests with `OK`; full unittest ran 445 tests with `OK`; fixture eval exited `0` with 54 fixtures, 0 failures, renderer file count 157 and `llm_ai_rag_contract_present: true`; transcript eval exited `0` with 5 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.

Deferred from `M20..M29` to later T9-D10 batches:

- Agent handoff compatibility, eval tooling selector and deferred runner policy, model migration threshold policy, RAG lifecycle/deletion/privacy, AI behavior diff-signal policy, AI incident workflow boundary and methodology report/render coverage remain in `M30..M36`.

Batch `M30..M36` completed scope:

- Mapped source/legacy `agent-handoff-contract.md` to existing `agent-task-packet.md` without registering a duplicate generated contract, while strengthening handoff owner, inputs, output schema, stop condition and trace evidence fields.
- Added final `llm_ai_rag` catalog gates/eval fields for handoff compatibility, eval tooling selector, model migration policy, RAG corpus lifecycle/privacy, AI behavior diff-signal policy and AI incident workflow.
- Strengthened `ai-eval-spec.md` with Promptfoo, OpenAI Evals, pytest/Jest, Ragas and LangSmith as conditional candidates, including selected runner, rejected runner, deferred decision, stack/privacy/CI fit and no forced eval runner.
- Strengthened model/eval/RAG/dataset/guardrail/RUNLOG templates with snapshot or approved alias, prompt migration impact, compatibility checks, minimum threshold, sampling parameter rationale, deletion path, retention, stale-source pruning, privacy owner, vector store lifecycle, deletion propagation, deduplication, privacy review, AI incident boundary, severity, mitigation, follow-up eval and Security/Privacy handoff.
- Added read-only `diff_signal_policy` to `llm_ai_rag_signals`; it is limited to workspace and intent signals, records no external branches, no network and no filename-only certainty.
- Added audit recommendations for final-batch gates and methodology report rendering for `evidence_required`, `evidence_owner`, `approval_boundary`, `accepted_gap_option`, `residual_risk` and `safe_next_action` with redaction of local paths and private data markers.
- Verification: focused M30..M36 RED checks failed as expected before implementation; focused GREEN check ran 6 tests with `OK`; full unittest ran 449 tests with `OK`; fixture eval exited `0` with 54 fixtures, renderer file count 157 and `llm_ai_rag_contract_present: true`; transcript eval exited `0` with 5 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py` passed; `git diff --check` exited `0`.

### `T9-D11` Security, Privacy & Compliance Integration

Status: `done`

Source audited: `docs/methodologies/security-privacy-compliance.md`

Deep-audit deltas to implement:

- Treat Security, Privacy & Compliance as a planning-first methodology domain for authn, authz, permissions, secrets, PII, sensitive data, payments, billing, abuse/rate limits, audit logging, supply chain, CI permissions, AI/agent security, external writes and compliance overlays.
- Use the full gate set from the methodology source: security-sensitive classification, threat surface, security risk review, ASVS mapping, API security scheme, authz negative tests, secrets policy, data classification, privacy impact, external-write approval, abuse/rate-limit review, audit logging, supply chain, CI permissions, AI security, compliance overlay and evidence before completion.
- Record source references as methodology evidence and platform/security guidance, not legal advice. Compliance output must record applicability, owner, evidence, non-goals, gaps and review cadence without claiming GDPR, CCPA, HIPAA, PCI, SOC 2 or enterprise compliance certification.
- Resolve artifact-name compatibility before renderer registration: source-era names such as `threat-model.md`, `asvs-mapping.md`, `secrets-inventory.md`, `authz-matrix.md`, `audit-log-policy.md` and `compliance-applicability-matrix.md` must map to canonical Product-Agent OS templates or aliases without duplicate conflicting contracts.
- Map or explicitly defer the full source artifact set: `data-classification-register.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `ai-security-review.md`, `vulnerability-response-record.md` and `approval-record.md` must not be silently dropped.
- Represent Secure SDLC/SSDF and OWASP SAMM as lifecycle/maturity vocabulary. ASVS Level 1/2/3 selection must record applicability, project risk, owner, evidence and gaps without claiming compliance.
- API authorization negative tests must cover allowed and forbidden behavior, BOLA, BFLA, object property authorization, role/scope/resource ownership, rate limits and unsafe consumption. OAuth or API docs alone are not accepted as security evidence.
- Data classification and redaction lifecycle must cover prompts, docs, fixtures, eval datasets, logs, traces and screenshots. Raw secrets, credentials, payment data, raw PII, raw private chats and private customer data are blocked.
- SBOM/provenance policy must distinguish internal apps, packages, plugins, containers and release artifacts, and must connect SBOM to vulnerability status, update path, license status, provenance, action pinning, release signing or an explicit accepted gap.
- Vulnerability/security incident workflow must cover security bugs, advisories, leaked secrets, abuse incidents, dependency alerts and data exposure with triage, severity, containment, fix evidence, verification, disclosure, release/patch plan and post-incident lessons.
- Compliance overlays must separate legal/regulatory obligations, customer contractual obligations and internal policy, with conditional overlays for finance, healthcare, minors, enterprise, public sector, marketplace and AI agent tooling.
- Codex Security scan remains explicit opt-in. Security-sensitive routing can recommend a scan or record `not requested`, but must not imply that a scan ran from security terminology alone.
- False-positive policy: security docs mention without code path remains `present_unverified`; docs-only repositories with security articles do not become regulated automatically; keyword-only compliance claims do not prove compliance; no-secrets-in-code does not prove artifact safety.
- Unsupported claims must be rejected as high-risk evidence gaps: security review after coding, no-secrets-in-code means safe, ASVS/OWASP proves compliance, SBOM once is enough, Codex Security scan is implied, OAuth proves API security and privacy compliance is universal.

Implemented scope:

- Added `security_privacy_compliance` catalog coverage for security-sensitive classification, threat surface, security risk review, ASVS/SSDF/SAMM mapping, ASVS level selection, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact, external-write approval, abuse/rate-limit review, audit logging, supply chain, SBOM/provenance, CI permissions, AI security, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status, security evidence before completion and unsupported-claim rejection.
- Added read-only discovery/audit coverage for authn/authz, permissions, secrets, PII/sensitive data, payment/billing, abuse/rate limits, audit logging, supply chain, SBOM/provenance, CI permissions, compliance terms, AI/agent security and Codex approval-bound signals. Detection remains `present_unverified`; no scan, security mutation, external write or compliance certification is implied.
- Resolved source-era artifact naming through canonical templates and aliases for threat surface/model, ASVS/SSDF mapping, secrets policy/inventory, authz negative tests, audit logging and compliance overlay/applicability.
- Added or strengthened Security, Privacy & Compliance artifact templates: `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md` and `approval-record.md`.
- Registered the 16 new security templates in the staged renderer; renderer file count increased from 157 to 173 and `security_privacy_compliance_contract_present` is true for `python-app`.
- Strengthened source policy to block raw PII/private data/payment data markers in docs/templates/fixtures in addition to secret-like literals.
- Added readiness and behavioral eval coverage for `security_privacy_compliance_when_sensitive_surface`, false-positive handling, approval boundaries and unsupported security/compliance claims.
- Added synthetic fixtures for payment/billing high risk, docs-only security article false positive, unsupported compliance claim rejection, CI permissions and SBOM/provenance `present_unverified` behavior, all without raw secrets or private data.
- Routed the methodology through lifecycle skills with planning-first classification, threat surface, data classification, owner review, tests/evidence, rollback, approval boundary, compliance owner and explicit Codex Security scan status.
- Added methodology report coverage for security/privacy recommendations, approval boundaries, accepted gaps, residual risks and redaction of secrets, payment data, raw PII and private customer data.

Verification policy:

- RED catalog check: `python -m unittest tests.product_agent_os.test_methodology_catalog -v` should fail before catalog implementation on missing `security_privacy_compliance` gates.
- Focused security slice check: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v`.
- Final implementation check: `python plugins\product-agent-os\scripts\run_fixture_eval.py`; `python -m unittest discover -s tests -p "test_*.py" -v`; `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`; `python tools\check_docs.py`; `git diff --check`.
- Commit, push and PR actions remain deferred until explicitly requested.

Verification:

- RED catalog check failed as expected before implementation on missing `security_privacy_compliance` gates.
- Focused security suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_source_policy tests.product_agent_os.test_fixture_eval_runner -v` ran 81 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 57 fixtures, 0 failures, renderer file count 173 and `security_privacy_compliance_contract_present: true`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 460 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

### `T9-D12` Delivery, Release & Operations Integration

Status: `in_progress`

Source audited: `docs/methodologies/delivery-release-operations.md`

Deep-audit deltas to implement:

- Treat Delivery, Release & Operations as a planning-first methodology domain for release readiness, versioning, changelog/release notes, artifact manifests, rollout, rollback/recovery, CI/CD governance, environments, operations runbooks, incident/postmortem learning, DORA and automation promotion.
- Use the full gate set from the methodology source and second-pass plan audit: release scope, version impact, changelog/release notes, artifact manifest, current release evidence, rollout, rollback, environment and external approval boundaries, CI/CD governance, observability/SLO, operations runbook, incident response, post-release measurement, automation manual stability, release mode, build-release-run, platform distribution, release communication, versioning tooling, GitHub environment controls, DORA five-metric design, blameless postmortem, observability/on-call tooling, security handoff and owner-reviewed evidence sufficiency.
- Resolve artifact-name compatibility before broad renderer registration. Plan-era names such as `release-scope.md`, `version-impact-record.md`, `artifact-manifest.md`, `rollout-strategy.md`, `ci-cd-governance.md`, `incident-response-path.md` and `post-release-measurement.md` map to canonical names rather than becoming duplicate templates.
- Detection alone can only justify `present_unverified`. Release-ready, deployed, published, operational-ready and automated claims require current evidence, owner evidence or an explicit accepted gap with owner, reason, review date, residual risk and follow-up condition.
- External release actions remain approval-bound: publish, tag, GitHub Release creation, artifact upload, deploy, package registry mutation, marketplace/store submission, PR creation, branch push, CI/CD environment mutation and active automation.
- False-positive policy: `CHANGELOG.md`, docs-only release notes, CI config, Dockerfile, health check, generated changelog, feature flag or GitOps file alone cannot prove readiness.
- Unsupported claims must be rejected as evidence gaps: CI green means release ready, tests passed so release is ready, rollback is just revert, feature flags remove risk, GitOps is automatically safe, generated changelog is enough for users, DORA proves individual performance and repeatable automation is automatically safe.

Implemented scope in batch `M0..M9`:

- Refreshed Track 9 plan/backlog state for T9-D12 batch execution and preserved the user-requested 10-row checkpoint policy.
- Added `delivery_release_operations` catalog coverage for the full planned gate/artifact/eval/overlap set so later batches can attach behavior to stable gate ids without renaming.
- Added `DELIVERY_TEMPLATE_ALIASES` for plan-era artifact names mapped to canonical release/operations artifact names.
- Added read-only discovery signal depth for release intent, version, changelog/release notes, artifact, deployment, GitHub Actions, GitHub environments, GitOps, feature flags, rollout, rollback, SLO, observability, incident, postmortem, DORA and automation promotion. Discovery records these as `present_unverified` and does not claim release readiness.
- Added methodology applicability packet `delivery_release_operations_readiness` with required evidence and residual-risk language.
- Added audit routing and initial recommendations for release scope, version impact, changelog/release notes, release evidence, release evidence before completion and unsupported delivery claims.
- Added `versioning-policy.md` and strengthened `release-readiness.md` and `release-packet.md` for M7..M9 fields.

Implemented scope in batch `M10..M19`:

- Added audit recommendations for `artifact_manifest_present`, `rollout_strategy_present`, `rollback_recovery_present`, `environment_approval_boundary_present`, `external_release_approval_present`, `ci_cd_governance_present`, `observability_release_evidence_present`, `slo_or_operational_gap_present`, `operations_runbook_present`, `incident_response_path_present` and `post_release_measurement_present`.
- Added delivery/operations artifact templates for release artifact manifests, rollout plans, rollback/recovery, environment matrices, deployment plans, CI/CD workflow inventory, observability maps, SLO specs, operations runbooks, incident records, postmortems and post-release reviews.
- Strengthened shared `approval-record.md`, `ci-permissions-review.md` and `metric-spec.md` for external release approvals, CI/CD governance and DORA/anti-Goodhart process measurement.
- Kept renderer registration deferred to `T9-D12-M21`; the new delivery templates are source templates now, but not yet staged into generated `.codex/artifact-templates/` outputs.

Implemented scope in batch `M20..M29`:

- Added the Delivery/Release/Operations automation promotion gate `automation_manual_stability_present` so automation candidates require manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence and rollback/disable path before any promotion.
- Registered and rendered 13 delivery templates under generated `.codex/artifact-templates/`: `versioning-policy.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md` and `post-release-review.md`; renderer file count increased from 173 to 186.
- Extended `methodology-audit-report.md` rendering with an External Action Status section so reports say that no external action is implied and recommendations remain staged/read-only until approval evidence exists.
- Strengthened generated `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with `delivery_release_operations_readiness_when_release_or_operations_changes`, release evidence, artifact manifest, rollout, rollback, CI/CD, SLO/observability, operations, incident, post-release review and automation candidate-only gates.
- Added fixture eval contract `delivery_release_operations_contract_present` and package-release checks for delivery detection, approval requirements, artifact manifest, release evidence before completion, rollout/rollback and operations terms.
- Added synthetic false-positive/approval fixtures: `release-docs-only-note`, `release-ci-only-workflow`, `release-deployment-manifest-only`, `release-feature-flag-no-owner`, `release-gitops-no-approval` and `package-release-approval`.
- Updated lifecycle skills so release/deploy/publish/package/operations work routes to delivery planning first, keeps publish/tag/release/upload/deploy/package registry/marketplace/store/automation activation approval-bound, and states that candidate-only automation and active schedules remain out of scope until explicitly approved.

Implemented scope in batch `M30..M40`:

- Added final delivery gates for release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency.
- Extended discovery with versioning tooling and observability/on-call tooling signals for `.releaserc`, release-please, semantic-release, Conventional Commits, OpenTelemetry, Prometheus, Grafana, Sentry, Datadog, PagerDuty and Opsgenie. These signals remain `present_unverified`.
- Strengthened release, deployment, versioning, environment, post-release, metric, incident, postmortem, observability, SLO, operations, release-notes and release-packet templates with final evidence fields and accepted-gap language.
- Expanded readiness and behavioral eval contracts so release completion cannot rely on rebuild-per-environment, generated changelog, single observability tool, DORA individual quota, mobile signing alone or release-ready claims without owner-reviewed evidence sufficiency.
- Added fixture eval checks and synthetic false-positive fixtures: `release-mobile-signing-only`, `release-dora-individual-quota` and `release-tooling-only`.
- Kept external release actions approval-bound and did not create schedules, publish artifacts, mutate CI/CD environments or perform external writes.

Verification so far:

- RED focused run failed as expected before implementation on missing `delivery_release_operations` catalog data, delivery aliases, discovery packet, audit recommendations and `versioning-policy.md`.
- Focused batch suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates -v` ran 191 tests with `OK`.
- Batch `M10..M19` RED run failed as expected before implementation on missing operational delivery gates, missing new templates and missing strengthened release approval/CI/DORA terms.
- Batch `M10..M19` focused suite: `python -m unittest tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates -v` ran 123 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; renderer file count remained 173 because renderer registration is deferred to `T9-D12-M21`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 469 tests with `OK`.
- Batch `M20..M29` RED run failed as expected before implementation on missing automation manual stability gate, report external-action status, renderer registration, readiness/behavioral eval contracts, package-release fixture checks, synthetic fixtures and lifecycle skill routing.
- Focused infrastructure rerun after GREEN: `python -m unittest tests.product_agent_os.test_infrastructure_templates -v` ran 77 tests with `OK`.
- Focused docs sync: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 10 tests with `OK`.
- Focused delivery suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_report tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 296 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 63 fixtures, 0 failures, renderer file count 186 and `delivery_release_operations_contract_present: true`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 476 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.
- Batch `M30..M40` RED run failed as expected before implementation on missing final delivery eval fields, discovery statuses, audit recommendations, template/eval terms and fixture checks.
- Batch `M30..M40` focused suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v` ran 216 tests with `OK`.
- Focused fixture false-positive suite: `python -m unittest tests.product_agent_os.test_fixtures tests.product_agent_os.test_fixture_eval_runner -v` ran 36 tests with `OK`.
- Final focused delivery suite after `M30..M40`: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_methodology_report tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 298 tests with `OK`.
- Final fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 66 fixtures, 0 failures, renderer file count 186 and `delivery_release_operations_contract_present: true`.
- Final full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 478 tests with `OK`.
- Final transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Final Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Final docs check: `python tools\check_docs.py` passed.
- Final diff hygiene: `git diff --check` exited `0`.
- `docs/sources/registry.md` was checked for T9-D12 source impact; no new registry entry was added because this batch operationalizes the checked-in delivery methodology artifact and existing Product-Agent OS behavior rather than introducing new external source-backed platform claims.
- Commit, push and PR actions remain deferred until explicitly requested.

## Task 20 Cross-Domain Synthesis Baseline

Status: `in_progress`

Source audited: all files under `docs/methodologies/`

Baseline duplicate gates before synthesis:

- `accepted_gap_recorded`: `requirements_domain`, `solution_architecture`.
- `automation_manual_stability_present`: `codex_agentic_workflow`, `delivery_release_operations`.
- `bounded_context_architecture_boundary_trace`: `requirements_domain`, `solution_architecture`.
- `external_write_approval_present`: `api_integrations`, `security_privacy_compliance`.

Baseline duplicate artifacts before synthesis:

- `approval-record.md`: `codex_agentic_workflow`, `security_privacy_compliance`, `delivery_release_operations`.
- `security-risk-review.md`: `solution_architecture`, `backend`, `api_integrations`, `database_data`, `llm_ai_rag`, `security_privacy_compliance`.
- `api-contract-review.md`: `solution_architecture`, `quality_testing_evals`, `frontend`, `backend`, `api_integrations`, `database_data`.
- `test-eval-matrix.md`: `quality_testing_evals`, `frontend`, `backend`, `llm_ai_rag`.
- `release-readiness.md`: `database_data`, `delivery_release_operations`.
- `architecture-overview.md`: `solution_architecture`, `backend`.

Baseline duplicate eval fields before synthesis:

- `accepted_gap_contract_present`: `requirements_domain`, `solution_architecture`.
- `api_security_review_contract_present`: `api_integrations`, `security_privacy_compliance`.
- `automation_manual_stability_contract_present`: `codex_agentic_workflow`, `delivery_release_operations`.
- `external_write_approval_contract_present`: `api_integrations`, `security_privacy_compliance`.
- `post_release_measurement_contract_present`: `business_product`, `delivery_release_operations`.

Current fixture symptoms to resolve during Task 20:

- backend FSD-like directories can trigger frontend recommendations unless UI/runtime evidence is checked before frontend blockers.
- security/payment can be ordered behind generic quality strategy when `safe_next_action` only follows first sorted recommendation.
- RAG ingestion can miss AI/RAG routing when no explicit `rag/` directory exists and the evidence is expressed through database ingestion or lineage terms.

Symptoms resolved by batch `T9-S-M5..M9`:

- backend FSD-like directories no longer trigger frontend recommendations without UI/runtime evidence.
- security/payment and release risks can outrank generic quality strategy in `safe_next_action`.
- CI-only workflows, docs-only release notes and tooling-only release files no longer prove security or release readiness without owner-reviewed evidence.

Batch `T9-S-M0..M4` implemented:

- Added RED synthesis tests and kept the expected RED failure evidence.
- Added additive top-level `synthesis` catalog metadata without changing domain `gates`, `artifacts` or `eval_fields` list shapes.
- Added shared gate owners, artifact owners, artifact aliases, source artifact decisions, priority tie-breakers, conflict rules, false-positive rule metadata, semantic evidence sufficiency and owner-question dedupe metadata.
- Added source artifact compatibility coverage for methodology-source artifact names such as `context-map.md`, `agent-eval-case.md`, `skill-candidate.md`, `ui-flow-spec.md`, `visual-evidence-packet.md`, `threat-model.md`, `asvs-mapping.md`, `runbook.md`, `slo.md` and `CHANGELOG.md`.
- Added pure `methodology_synthesis.py` helpers for grouped recommendations, source artifact classification, source artifact ledger and owner-question dedupe. Audit output integration is intentionally deferred to `T9-S-M5`.

Batch `T9-S-M5..M9` implemented:

- Integrated `methodology_synthesis` into `build_methodology_audit()` as additive top-level `recommendation_groups` and `methodology_synthesis` output while keeping existing recommendation keys compatible.
- Made `safe_next_action` risk-aware so high-risk security, release, payment and public-contract blockers can outrank generic quality recommendations.
- Added a discovery `methodology_synthesis` applicability packet with `present_unverified` status and evidence for recommendation groups, source artifact ledger and semantic evidence sufficiency.
- Added shared `semantic_evidence_sufficiency` generated control-plane, readiness and behavioral eval contracts, including owner-reviewed accepted-gap fields.
- Hardened false-positive routing for backend FSD-like TypeScript directories, CI-only workflows, docs-only release notes and tooling-only release artifacts.

Batch `T9-S-M10..M14` implemented:

- Added mixed-risk cross-domain fixtures for small PII app, complex monorepo without production users, internal CLI without UI/API/release hard blockers, AI/RAG plus data/security overlap, package release with security handoff, source artifact alias/deferred mapping and owner-question dedupe.
- Fixture eval exposes `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present`.
- Methodology reports render a Cross-Domain Synthesis section with grouped recommendations, owner domains, consumer domains, merged gates, source artifact alias/deferred decisions, accepted-gap option, approval boundary, residual risk and safe next action.
- Lifecycle skills consume synthesized packets without dumping every methodology gate, scaffolding before approval or treating detection as verification.
- Product docs explain semantic evidence sufficiency review ownership, grouped recommendations, false-positive guards, source artifact alias/deferred decisions and approval-bound behavior.

## Cross-Domain Synthesis Backlog

| Status | Item | Reason |
| --- | --- | --- |
| `done` | Normalize repeated methodology gates across domains. | `methodology_synthesis` now groups recommendations by owner artifact, preserves owner/consumer domains, dedupes owner questions and carries semantic evidence sufficiency into the shared packet. |
| `done` | Add cross-domain false-positive fixtures. | Batch `T9-S-M10..M14` added packaged mixed-risk fixtures for small PII, complex non-production monorepo, internal CLI, AI/RAG plus data/security, package release plus security handoff, source artifact alias/deferred mapping and owner-question dedupe. |
| `planned` | Reuse decision horizon across requirements, architecture, release and operations domains. | Product formalism should scale by `discovery`, `MVP`, `beta`, `production` and `scale` rather than forcing production ceremony on early discovery. |
| `planned` | Normalize outcome metric levels across product, quality, release and workflow automation domains. | Separate `business_outcome`, `product_outcome` and `feature_traction_metric` to reduce proxy metric risk. |
| `planned` | Standardize no-production-telemetry fallback language. | Product, release and operations domains need the same rule: lack of telemetry is a gap, not success evidence. |
| `planned` | Carry workflow-promotion value evidence into agentic workflow and operations domains. | Automation promotion should require manual stability plus value evidence such as engineering time saved before any schedule or external action. |
| `planned` | Synthesize requirement/API/UI/data traceability across Requirements, Architecture, API, UI and Data domains. | T9-D2 introduces the trace chain before later domains own contract, UI and schema-specific enforcement. |
| `planned` | Split architecture candidate artifacts only when later slices prove separate ownership. | T9-D3 maps boundary responsibility, quality scenarios, tradeoff records, dependency rules and runtime topology into existing architecture artifacts to avoid template sprawl. |
| `planned` | Reuse stakeholder/owner mapping across Product, Requirements, Security, Release and Operations domains. | Owner review appears repeatedly and should have one durable shape for source, decision authority and escalation. |
| `planned` | Carry story-slice and MVP boundary evidence into Product, Frontend and Delivery domains. | Requirements slicing should inform UI scope, rollout scope and release notes without forcing heavy ceremonies. |
| `planned` | Normalize domain event requirements across Requirements, API/Integrations and Data domains. | Event meaning, schema, ordering, idempotency and privacy classification will be shared by multiple later slices. |
| `planned` | Normalize accepted-gap records across all methodology gates. | Accepted gaps need owner, reason, scope, review date, downstream risk and follow-up condition everywhere, not only in T9-D2. |
| `planned` | Normalize owner/domain expert review across business-critical, compliance, finance/legal and AI-generated claims. | Later Security, AI and Release domains need the same human-review evidence packet. |
| `planned` | Normalize change-impact review across requirements, API, data, UI, docs, release and rollback. | Requirement changes after planning should produce a shared impact review rather than domain-specific fragments. |
| `planned` | Reuse runtime evidence packets across Quality, Frontend, Backend, Desktop and Native domains. | T9-D4 establishes current runtime/manual evidence shape before platform-specific domains add their own build/run/screenshot/log details. |
| `planned` | Share visual and accessibility evidence with the Frontend domain. | T9-D4 defines when visual/a11y evidence is required, while T9-D6 will own UI state, responsive and component-specific depth. |
| `planned` | Share contract-check evidence with API/Integrations. | T9-D4 blocks unsupported API/event/schema quality claims, while T9-D8 will own contract-source and compatibility detail. |
| `planned` | Share test data privacy evidence with Database, Security and AI domains. | Fixtures, traces, screenshots, eval datasets and logs need one no-secrets/private-data policy across later data, security and AI slices. |
| `planned` | Share eval baseline/rerun evidence with LLM/AI/RAG. | T9-D4 defines eval evidence as a quality gate; T9-D10 will own AI behavior, retrieval, grounding, model and grader detail. |
| `planned` | Share CI quality gate evidence with Delivery and Operations. | T9-D4 defines local/CI evidence and permission boundaries; T9-D12 will own release, rollout and operational gate depth. |
| `planned` | Normalize current evidence before completion across all domains. | Completion/readiness claims must stay evidence-bound regardless of which methodology domain owns the slice. |
| `done` | Normalize semantic evidence sufficiency review across high-risk domains. | High-risk, production, release, security-sensitive, AI behavior and public-contract slices now share generated control-plane, readiness and behavioral eval contracts for owner-reviewed evidence sufficiency or an accepted gap with owner, reason, review date, downstream risk and follow-up condition. |
| `planned` | Revisit deferred quality artifacts after stack-specific slices. | Mutation, property-based, flaky ledger, CI quality gates and eval run report may deserve standalone templates only after later domains prove separate ownership. |
| `planned` | Reuse Codex runtime routing across AI, security and delivery domains. | T9-D5 defines Codex App/CLI/IDE/codex exec/GitHub Action/MCP/Agents SDK/automation boundaries before later domains add model, security and release-specific depth. |
| `planned` | Normalize capability activation approvals across MCP, hooks, plugins, automations, CI and external systems. | T9-D5 keeps capability activation staged-first and approval-bound; Security and Delivery slices will own least-privilege and release-risk details. |
| `planned` | Revisit deferred Codex workflow artifacts after AI and Operations slices. | Standalone memory, agent readiness, agent eval case, skill failure log and hook activation records may deserve separate templates only after later slices prove separate ownership. |
| `done` | Synthesize final `methodology-applicability.json` contract. | Task 20 finalizes the additive discovery `methodology_synthesis` applicability packet and report/lifecycle consumption contract; Task 21 owns runtime runner consumption and finish-option routing. |
| `done` | Update operator docs after all domain slices. | Product-Agent OS methodology, behavioral eval and development standards docs now describe grouped recommendations, false-positive protection, source artifact compatibility, semantic evidence sufficiency and approval-bound behavior. |

Known accepted overlaps after `T9-S-M10..M14`:

- `security-risk-review.md` is owned by Security/Privacy/Compliance and consumed by architecture, backend, API, database, AI/RAG and delivery handoffs.
- `approval-record.md` is owned by Security/Privacy/Compliance and consumed by Codex workflow and Delivery/Release/Operations.
- `api-contract-review.md` is owned by API & Integrations and consumed by architecture, quality, frontend, backend and database work.
- `test-eval-matrix.md` is owned by Quality/Testing/Evals and consumed by frontend, backend and AI/RAG evidence.
- `release-readiness.md` is owned by Delivery/Release/Operations and consumed by database, security and product release decisions.
- `semantic_evidence_sufficiency` is owned by Quality/Testing/Evals and consumed by high-risk, production, release, security-sensitive, AI behavior and public-contract slices.

## Verification Evidence

Current foundation evidence is recorded in the branch commits for Tasks 1 through 7. The required checks for this docs slice are:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict`

Domain slices must also run the focused catalog/audit tests, fixture evals and any domain-specific docs checks added by that slice.

`T9-S` Task 20 batch `M0..M4` evidence:

- RED run: `python -m unittest tests.product_agent_os.test_methodology_synthesis -v` failed as expected before implementation on missing backlog baseline, `synthesis` catalog block, `SOURCE_ARTIFACT_TEMPLATE_ALIASES` and `methodology_synthesis.py`.
- Focused suite: `python -m unittest tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_infrastructure_templates -v` ran 102 tests with `OK`.
- Fixture runner CLI check: `python -m unittest tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_cli_prints_json_and_exits_zero_when_all_fixtures_are_ok -v` ran 1 test with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` exited `0`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` exited `0`.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

`T9-S` Task 20 batch `M5..M9` evidence:

- RED checks failed as expected before implementation on risk-aware recommendation ordering, missing audit/discovery synthesis packets, missing semantic evidence sufficiency contract, backend FSD-like false-positive routing and CI-only release/security escalation.
- Focused GREEN check: `python -m unittest tests.product_agent_os.test_methodology_synthesis.MethodologySynthesisContractTest.test_risk_aware_synthesis_prioritizes_security_and_release_over_generic_quality tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_audit_exposes_grouped_synthesis_without_losing_existing_keys tests.product_agent_os.test_methodology_audit.MethodologyAuditContractTest.test_security_release_and_quality_safe_next_action_resolution tests.product_agent_os.test_discovery.DiscoveryTest.test_methodology_applicability_reports_status_packets tests.product_agent_os.test_discovery.DiscoveryTest.test_backend_fsd_like_typescript_dirs_do_not_trigger_frontend_without_ui_runtime_evidence tests.product_agent_os.test_discovery.DiscoveryTest.test_ci_only_workflow_does_not_escalate_to_security_or_release_p0 tests.product_agent_os.test_infrastructure_templates.InfrastructureTemplateTest.test_cross_domain_semantic_evidence_sufficiency_contract_is_shared tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_template_validates_expected_contract tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_cases_encode_forbidden_shortcuts tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_expected_renderer_behavior_by_fixture -v` ran 10 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 492 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with all fixtures `ok: true`, renderer file count 186 and `semantic_evidence_sufficiency_contract_present: true`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

`T9-S` Task 20 batch `M10..M14` evidence:

- RED checks failed as expected before implementation on missing cross-domain fixture checks, methodology report synthesis rendering, lifecycle skill packet wording, behavioral eval case coverage and docs/backlog sync.
- Focused GREEN check: `python -m unittest tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_cross_domain_synthesis_fixtures tests.product_agent_os.test_fixture_eval_runner.FixtureEvalRunnerTest.test_fixture_eval_checks_expected_renderer_behavior_by_fixture tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_required_fixture_projects_exist tests.product_agent_os.test_fixtures.FixtureCompletenessTest.test_false_positive_scenario_fixtures_are_synthetic_and_secret_free tests.product_agent_os.test_methodology_report.MethodologyReportTest.test_report_renders_cross_domain_synthesis_groups_and_source_ledger tests.product_agent_os.test_lifecycle_skills.LifecycleSkillsTest.test_lifecycle_skills_consume_cross_domain_synthesis_packets tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_template_validates_expected_contract tests.product_agent_os.test_behavioral_workflow_evals.BehavioralWorkflowEvalTest.test_behavioral_eval_cases_encode_forbidden_shortcuts tests.product_agent_os.test_product_agent_os_docs.ProductAgentOsDocsTest.test_track9_cross_domain_synthesis_docs_and_backlog_are_synced -v` ran 9 tests with `OK`.
- Focused synthesis suite: `python -m unittest tests.product_agent_os.test_methodology_synthesis tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_methodology_report tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner tests.product_agent_os.test_fixtures tests.product_agent_os.test_product_agent_os_docs -v` ran 316 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 73 fixtures, 0 failures, renderer file count 186 and `cross_domain_synthesis_contract_present: true`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 496 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Product docs check: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 11 tests with `OK`.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.
- Commit, push and PR actions remain deferred until explicitly requested.

`T9-R` Task 21 batch `M0..M6` evidence:

- RED runtime tests failed as expected before implementation on missing compact methodology packet schema, route propagation, validation, finish options, recommendation-only no-write behavior and detection-only completion blocking.
- Focused runtime suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v` ran 28 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 502 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

`T9-R` Task 21 batch `M7..M13` evidence:

- RED/focused run first failed as expected on missing high-risk methodology approval, automation maturity and fixture checks, then ran 36 tests with `OK`.
- Guard suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_guards -v` ran 6 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 508 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; compact summary reported 80 fixtures, 0 failures, 13 codex-runner fixtures and new runtime checks `runtime_methodology_packet_present`, `runtime_finish_options_approval_bound`, `runtime_detection_not_completion`, `runtime_external_write_blocked`, `runtime_automation_maturity_required`, `runtime_methodology_redaction_enforced`, `runtime_malformed_methodology_packet_blocked` all `true`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

`T9-R` Task 21 row `M14` evidence sync:

- Backlog, RUNLOG, root control-plane/system files and the Track 9 plan next-action row now record current Task 21 evidence through `T9-R-M14`.
- The plan/backlog next action was corrected from stale `Task 22` wording to the remaining Task 21 expansion `T9-R-M16..M25`; `T9-R-M15` commit/push remains explicit-only.
- Source registry was not changed because this row records internal implementation evidence and checked-in methodology/runtime behavior, not new external source-backed claims.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

`T9-R` Task 21 batch `M16..M25` evidence:

- RED/focused checks failed as expected before implementation on missing structured high-risk taxonomy, status-to-finish-options mapping, runtime packet template/eval/handoff fields and behavioral fixture coverage.
- Focused runtime/template suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_contracts tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_behavioral_workflow_evals -v` ran 109 tests with `OK`.
- CLI suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_cli -v` ran 10 tests with `OK`.
- Runtime fixture suite: `python -m unittest tests.product_agent_os.test_codex_runtime_runner_fixture_eval -v` ran 6 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 518 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 80 fixtures, 0 failures, renderer file count 186, 16 codex-runner fixtures and runtime bridge/compact first-response checks present.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 5 sessions and 0 failures.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- Docs check: `python tools\check_docs.py` passed.
- Diff hygiene: `git diff --check` exited `0`.

## Runtime Runner And Finish Options Backlog

| Status | Item | Reason |
| --- | --- | --- |
| `done` | Compact runtime methodology packet and finish options. | Runtime routes carry bounded methodology recommendations, groups, owner questions, source artifact ledger, semantic sufficiency and safe next action with ordered finish options. |
| `done` | Recommendation-only no-write and detection-only no-completion guards. | Methodology detections and recommendations remain read-only evidence until approval, staging target and current verification evidence exist. |
| `done` | High-risk action, external-write and automation maturity safety. | Synthetic runtime fixtures prove approval-bound external actions, automation manual stability/value requirements, redaction and malformed packet fallback. |
| `done` | Evidence/backlog sync through `T9-R-M14`. | Current verification evidence, residual risks and next action are recorded in backlog, RUNLOG and root control-plane/system files. |
| `done` | Complete Task 21 expansion rows `T9-R-M16..M25`. | Added CLI/validator JSON output tests, generated control-plane/eval/handoff support, schema-v1 compatibility, status-to-finish-options mapping, cross-domain runtime bridge checks, compact first-response fields, structured high-risk taxonomy and ownership/parallelism routing guards. |
| `done` | Complete `Task 22` final Track 9 documentation sync. | Product-Agent OS docs, source registry/backlog state, READMEs and root control-plane files now close Track 1-9 documentation. Legacy Track 9 `Task 23: Final Verification Baseline` is absorbed into Task 22 final verification evidence before Track 10 `Task 23` starts. |

`Task 22` evidence:

- RED docs run: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` failed on missing Task 22 closure assertions before docs edits.
- Docs synchronized: `docs/product-agent-os/index.md`, `technical.md`, `architecture.md`, `scenarios.md`, `behavioral-evals.md`, `codex-compatibility.md`, `development-standards.md`, `methodology-intelligence.md`, root `README.md`, plugin `README.md`, `docs/sources/registry.md`, root control-plane files and docs tests.
- Final verification: focused docs tests ran 13 tests with `OK`; full unittest ran 520 tests with `OK`; fixture eval exited `0` with 80 fixtures, 0 failures and renderer file count 186; transcript eval exited `0` with 5 sessions and 0 failures; Codex compatibility returned `status: compatible`; `python tools\check_docs.py`, strict MkDocs with disposable `--site-dir .mkdocs_task22_site`, and `git diff --check` exited `0`.

`T9-D1` evidence:

- `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` ran 105 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 80 after adding five Business/Product artifact templates.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 347 tests with `OK`.
- `python tools\check_docs.py` passed.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.

`T9-D2` evidence:

- RED run: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` failed as expected before implementation on missing `requirements_domain` gates, artifact templates, audit recommendations, `docs-maintainer` skill and fixture check; the run reached fixture eval and timed out after 120 seconds after showing the expected failures.
- Focused catalog/audit run: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit -v` ran 18 tests with `OK`.
- Focused renderer/lifecycle/fixture run: `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` ran 97 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 88 and `requirements_domain_contract_present` is true for `python-app`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 357 tests with `OK`.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.

`T9-D3` evidence:

- RED runs failed as expected before implementation on missing `solution_architecture` catalog gates, audit recommendations, architecture templates, lifecycle skill routing and fixture eval check.
- `python -m unittest tests.product_agent_os.test_methodology_catalog -v` ran 7 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_methodology_audit -v` ran 15 tests with `OK`.
- `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_fixture_eval_runner -v` ran 120 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 92 and `solution_architecture_contract_present` is true for `python-app`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 362 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.

`T9-D4` evidence:

- RED run: focused catalog/audit/discovery/template/lifecycle/behavioral/fixture tests failed as expected before implementation on missing `quality_testing_evals` gates, audit recommendations, quality discovery signals, five artifact templates, lifecycle skill routing, behavioral eval coverage and fixture eval check.
- Focused T9-D4 suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_fixture_eval_runner -v` ran 168 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 97 and `quality_testing_evals_contract_present` is true for `python-app`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 370 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.

`T9-D5` evidence:

- RED runs failed as expected before implementation on missing `codex_agentic_workflow` gates, audit recommendations, discovery signals, five artifact templates, lifecycle skill routing, behavioral eval coverage and fixture eval check.
- Focused catalog/audit/discovery suite: `python -m unittest tests.product_agent_os.test_methodology_catalog tests.product_agent_os.test_methodology_audit tests.product_agent_os.test_discovery -v` ran 70 tests with `OK`.
- Focused template/lifecycle/behavioral/automation/runtime suite: `python -m unittest tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_lifecycle_skills tests.product_agent_os.test_behavioral_workflow_evals tests.product_agent_os.test_automation_policy tests.product_agent_os.test_codex_runtime_runner_contracts -v` ran 105 tests with `OK`.
- Targeted fixture runner checks passed for expected renderer behavior and CLI JSON exit.
- `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0`; fixture renderer file count is now 102 and `codex_agentic_workflow_contract_present` is true for `python-app`.
- `python -m unittest discover -s tests -p "test_*.py" -v` ran 378 tests with `OK`.
- `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible` with 11 bundled skills.
- `python tools\check_docs.py` passed.
- `git diff --check` exited `0`.

## Residual Risks

- The catalog currently represents foundation behavior and selected generic gates; domain slices can still reveal missing artifacts or conflicts.
- Read-only audit can classify workspace signals, but owner intent, product risk and regulatory constraints still require human confirmation.
- Recommendation priority order is deterministic, but real-world severity can change when a project has production traffic, sensitive data or external consumers.
- Codex workflow gates prove governance shape and approval routing, not that a human owner has approved every model, subagent, MCP, hook, skill, plugin or automation decision for a real project.
