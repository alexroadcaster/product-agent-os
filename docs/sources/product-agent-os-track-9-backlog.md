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
| `planned` | `T9-D6` | `frontend.md` | UI behavior, component states, Storybook applicability, visual/a11y evidence, responsive checks, performance and FSD boundaries. |
| `planned` | `T9-D7` | `backend.md` | Service boundaries, modular monolith vs microservices, runtime behavior, queues, observability, SLOs and rollback. |
| `planned` | `T9-D8` | `api-integrations.md` | OpenAPI/AsyncAPI/GraphQL/gRPC contracts, consumers, compatibility, errors, generated clients and external writes. |
| `planned` | `T9-D9` | `database-data.md` | Database inventory, schema source, migrations, transactions, data quality, classification and production access. |
| `planned` | `T9-D10` | `llm-ai-rag.md` | AI behavior spec, eval baseline, prompts, models, tools, RAG sources, grounding, datasets, approvals and cost/latency. |
| `planned` | `T9-D11` | `security-privacy-compliance.md` | Threat surface, ASVS/SSDF, authorization tests, secrets, privacy impact, supply chain, audit logging and compliance overlays. |
| `planned` | `T9-D12` | `delivery-release-operations.md` | Release readiness, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, runbooks and operations. |

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

## Cross-Domain Synthesis Backlog

| Status | Item | Reason |
| --- | --- | --- |
| `planned` | Normalize repeated methodology gates across domains. | Avoid duplicate recommendations for owner questions, evidence, metrics, source status and approval boundaries. |
| `planned` | Add cross-domain false-positive fixtures. | Ensure one methodology signal does not force unrelated heavy process on simple work. |
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
| `planned` | Normalize semantic evidence sufficiency review across high-risk domains. | High-risk, production, release, security-sensitive, AI behavior and public-contract slices need explicit owner review that the recorded tests/evals/manual evidence are sufficient for the real project risk, or an accepted gap with owner, reason, review date, downstream risk and follow-up condition. |
| `planned` | Revisit deferred quality artifacts after stack-specific slices. | Mutation, property-based, flaky ledger, CI quality gates and eval run report may deserve standalone templates only after later domains prove separate ownership. |
| `planned` | Reuse Codex runtime routing across AI, security and delivery domains. | T9-D5 defines Codex App/CLI/IDE/codex exec/GitHub Action/MCP/Agents SDK/automation boundaries before later domains add model, security and release-specific depth. |
| `planned` | Normalize capability activation approvals across MCP, hooks, plugins, automations, CI and external systems. | T9-D5 keeps capability activation staged-first and approval-bound; Security and Delivery slices will own least-privilege and release-risk details. |
| `planned` | Revisit deferred Codex workflow artifacts after AI and Operations slices. | Standalone memory, agent readiness, agent eval case, skill failure log and hook activation records may deserve separate templates only after later slices prove separate ownership. |
| `planned` | Synthesize final `methodology-applicability.json` contract. | Give lifecycle skills a stable packet for route decisions and staged artifact suggestions. |
| `planned` | Update operator docs after all domain slices. | Keep the public docs aligned with the implemented domain catalog. |

## Verification Evidence

Current foundation evidence is recorded in the branch commits for Tasks 1 through 7. The required checks for this docs slice are:

- `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`
- `python tools\check_docs.py`
- `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict`

Domain slices must also run the focused catalog/audit tests, fixture evals and any domain-specific docs checks added by that slice.

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
