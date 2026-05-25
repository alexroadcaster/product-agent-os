# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-25

## Current State

- `T9-D4` Quality, Testing & Evals methodology integration is complete.
- Verification baseline after `T9-D4`: focused T9-D4 checks passed; fixture eval exited `0` with renderer file count 97 and `quality_testing_evals_contract_present: true`; full verification is recorded in `RUNLOG.md`.
- Track 9 design is recorded in `docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`.
- Track 9 implementation plan is recorded in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Next implementation slice: `T9-D5` Codex / Agentic Workflow methodology integration.

## Architecture Boundary

- Primary implementation boundary: `plugins/product-agent-os/`.
- Track 9 methodology source boundary: `docs/methodologies/`.
- Documentation boundary: `docs/product-agent-os/`, `docs/product-agent/`, `docs/sources/`, root control-plane files.
- Tests boundary: `tests/product_agent_os/`.
- Out of scope unless explicitly requested: separate `product-agent-os/` packaged copy or release artifact, external automation activation, marketplace publishing, live target-workspace writes.

## Next Implementation Queue

| Order | Task | Status | Expected artifact |
| --- | --- | --- | --- |
| 0 | Repository hygiene before Track 9 | `done` | Clean intentional base before Track 9 implementation |
| 1 | `T9-F0` methodology intelligence foundation | `done` | Catalog, audit model, report/JSON output, discovery integration |
| 2 | `T9-D1` Business & Product | `done` | Product hypothesis, metrics, experiment and measurement gates |
| 3 | `T9-D2` Requirements & Domain | `done` | Requirements traceability, business rules, domain model and language gates |
| 4 | `T9-D3` Solution Architecture | `done` | Architecture boundary, C4/arc42/ADR and quality attribute gates |
| 5 | `T9-D4` Quality, Testing & Evals | `done` | Risk-based test/eval strategy and current evidence gates |
| 6 | `T9-D5` Codex / Agentic Workflow | `planned` | Control-plane, skills, subagents, handoff, MCP and automation gates |
| 7 | `T9-D6` Frontend | `planned` | UI behavior, component state, FSD, Storybook, a11y and visual evidence gates |
| 8 | `T9-D7` Backend | `planned` | Service boundary, runtime, observability, SLO and rollback gates |
| 9 | `T9-D8` API & Integrations | `planned` | OpenAPI/AsyncAPI/GraphQL/gRPC contract and compatibility gates |
| 10 | `T9-D9` Database & Data | `planned` | Schema, migration, data quality, lineage, privacy and production access gates |
| 11 | `T9-D10` LLM / AI / RAG | `planned` | AI behavior, prompt/model/tool/RAG eval and safety gates |
| 12 | `T9-D11` Security, Privacy & Compliance | `planned` | Threat, privacy, ASVS/SSDF, secrets, supply-chain and compliance gates |
| 13 | `T9-D12` Delivery, Release & Operations | `planned` | Release readiness, artifact manifest, rollout, rollback and operations gates |
| 14 | `T9-S` cross-domain synthesis | `planned` | Deduplicated gates, merged artifacts, conflict rules and final baseline |

## Track 9 Section Implementation Protocol

For each Track 9 section:

1. Read the relevant task block in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
2. Run a deep audit of the matching source file under `docs/methodologies/`.
3. Compare the plan task with the source file's methodology concepts, gates, artifacts, tooling candidates, false-positive risks, unsupported claims and open questions.
4. If the plan misses nuances, update the plan or Track 9 backlog before writing implementation code or templates.
5. Implement only the focused section slice after the plan/backlog is current.
6. Add or update tests/evals/docs for that section.
7. Record verification evidence and residual risk in `RUNLOG.md`.

## Methodology Gates

- Product/data gate: hypothesis, metric and measurement plan are clear or marked not applicable.
- Architecture gate: slice boundary, dependency rule, public contract and ownership are clear.
- Domain model gate: `domain_model_when_complex_domain` is satisfied or explicitly not applicable.
- Bounded context trace gate: `bounded_context_architecture_boundary_trace` maps every bounded context to an architecture boundary or accepted gap.
- Ubiquitous language gate: `ubiquitous_language_traceability` maps domain terms to requirements, API/events/contracts, UI labels, code modules or owners, or an accepted gap with domain expert review.
- FSD structure gate: `fsd_structure` applies only to web UI/component architecture with FSD-like layer directories or explicit owner decision; backend, native, simple CRUD and simple MVP work record not applicable or accepted gap.
- Metric hardening gate: `metric_hardening_when_product_behavior_changes` requires North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence before product success claims.
- Evidence-before-completion gate: `evidence_before_completion` blocks ready/completed/fixed/works/release claims unless current command evidence, current eval evidence, current runtime evidence, owner evidence or explicit test gap is present; inspection-only answers must stay labeled as inspection-only and list unsupported completion claims.
- Docs tooling gate: `docs_tooling_selector` records `docs_as_code_impact`, `docs-tooling-decision.md`, selected tools, rejected tools, evidence owner, maintenance owner, applicable docs commands, accepted gaps and approval boundaries; docs-light/internal-only work can be `not_applicable`, while hosted docs, CI activation and DB introspection stay approval-bound.
- Standards trigger gate: `standards_trigger_policy` records ADR trigger policy, C4/arc42 applicability, OpenAPI source of truth, AsyncAPI event contract, SemVer impact, Keep a Changelog categories, CODEOWNERS status, GitHub Actions least privilege and `governance-proposal.md`; external activation remains approval-bound.
- Requirements/domain gate: `requirements_domain` records requirements scope/owner, requirement quality, stable IDs, declarative acceptance scenarios, requirements traceability, business rules, non-goals/constraints, open questions, domain events, API/UI/data traceability, domain expert review, accepted gaps and change impact.
- Requirements/domain artifacts: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, `domain-review-record.md`.
- Solution architecture gate: `solution_architecture` records architecture scope, context/container boundaries, boundary owner, domain-to-architecture trace, public contract trace, data ownership, trust boundary review, quality attributes, ADR/tradeoff, runtime topology, observability, diagram render check, fitness functions, docs lifecycle, accepted gaps and unsupported-claim rejection.
- Solution architecture artifacts: `architecture-overview.md`, `adr.md`, `architecture-review-record.md`, `architecture-fitness-functions.md`, `trust-boundary-map.md`, `architecture-docs-tooling-decision.md`, `api-contract-review.md`, `database-dictionary.md`, `security-risk-review.md`, `migration-plan.md`, `integration-catalog.md`.
- Quality/testing/evals gate: `quality_testing_evals` records quality strategy, risk based scope, test-first evidence or accepted gap, acceptance traceability, contract checks, runtime/manual/visual evidence, eval spec/rerun evidence, current evidence before completion, CI quality gate, flaky-test policy, coverage policy, test data privacy, bug reproduction, regression impact and unsupported-claim rejection.
- Quality/testing/evals artifacts: `test-eval-matrix.md`, `quality-strategy.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, `manual-qa-evidence.md`, plus existing `TEST.md`, `EVALS.md`, `RUNLOG.md`, `ai-eval-spec.md`, `api-contract-review.md`, `bug-rescue-report.md` and `ci-stabilization-report.md` when applicable.
- Conditional readiness gate: `project-readiness.json` defines `readiness_statuses` and per-gate `applies_when`, pass condition, accepted gap, required evidence, owner and residual risk. Detection alone can only support `present_unverified`; `present_verified` requires current command, owner or artifact evidence.
- Test gate: deterministic tests, contract checks, evals or accepted gaps are named before implementation.
- Documentation gate: docs-as-code artifacts and source-of-truth updates are named.
- Review gate: security, privacy, performance, migration and rollback risks are reviewable.

## T8-A7 Completed Slice

- Added failing-first tests for ubiquitous language traceability fields in `domain-modeling.md`, lifecycle skill wording and fixture eval contract.
- Updated `domain-modeling.md` with term-to-requirement, API/event/contract, UI label, code module or owner, accepted-gap and domain expert review fields.
- Updated `implementation-planner` to stop before build when required domain terms are untraceable.
- Added readiness and fixture eval checks for `ubiquitous_language_traceability`.
- Synced Product-Agent OS docs, backlog, gap matrix and root control-plane files.

## T8-A8 Completed Slice

- Added `fsd_structure` discovery signal with frontend layer directory detection.
- Added false-positive tests for backend, native, simple CRUD and simple MVP work.
- Updated `component-card.md`, `development-standards.md`, `project-readiness.json`, `workspace-discovery-auditor` and `implementation-planner` with conditional FSD guidance.
- Synced Product-Agent OS docs, backlog, gap matrix and root control-plane files.

## T8-A9 Completed Slice

- Hardened `metric-spec.md` with `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence.
- Connected metric evidence to `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills and fixture eval.
- Added focused template/readiness/lifecycle/fixture tests so proxy metric success claims require counter-metric, guardrail, qualitative review and post-release review evidence.

## T8-A16 Completed Slice

- Added failing-first tests for generalized evidence-before-completion across behavioral evals, generated control-plane templates, lifecycle skills and fixture eval.
- Added `evidence-before-completion` behavioral eval coverage for ready/completed/fixed/works/release claims without current evidence.
- Added `evidence_before_completion` to `project-readiness.json`, control-plane templates, `release-packet.md`, `development-standards.md`, all lifecycle skills and fixture eval contract checks.
- Confirmed focused T8-A16 suite, full unittest, fixture eval and Codex compatibility checks pass before docs sync.

## T8-C Completed Slice

- Added `docs-tooling-decision.md` with selected tools, rejected tools, `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `approval_required`, evidence owner, commands, approval needs and maintenance owner.
- Added stack-aware `docs_tooling_decision` discovery for MkDocs, Docusaurus, Sphinx, Antora, Read the Docs, Storybook, OpenAPI/AsyncAPI, DBML/dbdocs, SchemaSpy, TypeDoc/JSDoc/Javadoc/XML docs, Vale, markdownlint, Mermaid, PlantUML and Structurizr DSL.
- Updated `documentation-system.md`, `project-readiness.json`, generated `PLAN/TEST/EVALS/RUNLOG`, lifecycle skills and fixture eval so docs impact and docs tooling choices are testable.
- Added false-positive and approval-bound coverage: docs-light/internal-only projects do not get a heavy docs portal, and hosted docs plus DB introspection are `approval_required`.
- Added focused tests/evals and docs sync for docs tooling decisions and `T8-A11` closure.

## T8-F Completed Slice

- Added failing-first tests for conditional readiness status vocabulary and per-gate readiness contract in `project-readiness.json`.
- Added `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Added structured conditional gates for scenario, methodology, tooling, review, release, compatibility and finish-option readiness with applicability reason, required evidence, owner and residual risk.
- Updated generated `AGENTS/PLAN/TEST/EVALS/RUNLOG` templates and lifecycle skills so readiness cannot be claimed from detection alone.
- Added fixture eval coverage via `conditional_readiness_gates_contract_present`.

## T8-H Completed Slice

- Added failing-first docs contract tests for dedicated Product-Agent OS scenario, behavioral eval and Codex compatibility pages.
- Added `docs/product-agent-os/scenarios.md`, `behavioral-evals.md` and `codex-compatibility.md` with Inputs, Outputs, Verification and Risks sections.
- Added the pages to MkDocs navigation and `tools/check_docs.py` required paths.
- Added source registry closure note and synced Product-Agent OS README, docs, plugin spec, backlog and gap matrix.
- Verified focused docs contract, full unittest, fixture eval, Codex compatibility, docs check and strict MkDocs.

## T8-GY Completed Slice

- Added failing-first transcript/session tests for `evaluate_transcript_sessions`, CLI exit codes, missing expected evidence, forbidden behavior and privacy/no-secrets rejection.
- Added `plugins/product-agent-os/scripts/product_agent_os/transcript_evals.py` and `run_transcript_eval.py`.
- Added `plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json` with 4 synthetic sessions mapped to `behavioral_case` entries.
- Added fixture eval coverage via `transcript_session_eval_runner_contract_present`.
- Synced Product-Agent OS behavioral eval docs, README/spec/status docs, source registry and root control-plane files.

## T8-B Completed Slice

- Added `governance-proposal.md` and registered it in the staged renderer.
- Strengthened `adr.md`, `architecture-overview.md`, `api-contract-review.md`, `documentation-system.md` and `release-packet.md` with standards trigger policy fields.
- Added `standards_trigger_policy_when_architecture_api_release_or_governance_changes` to `project-readiness.json`.
- Added fixture eval coverage through `standards_trigger_contract_present`.
- Updated lifecycle skills for discovery, planning, review and release with ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions routing and no forced external activation.

## T8-GX Completed Slice

- Added synthetic fixtures `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal` and `hosted-docs-approval`.
- Added fixture eval assertions for `fsd_structure_not_detected_for_backend`, `fsd_structure_not_detected_for_native`, `domain_model_not_forced_for_simple_crud`, `docs_light_does_not_select_heavy_portal` and `hosted_docs_and_db_introspection_require_approval`.
- Added fixture completeness and no-secrets tests for the new false-positive scenario fixtures.
- Synced Product-Agent OS behavioral eval docs, README, backlog and root control-plane files.

## T8-D Completed Slice

- Added `methodology_applicability` to workspace discovery output.
- Added structured status packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision and standards trigger policy.
- Reused readiness statuses: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Added focused discovery tests for packet shape and status transitions, plus fixture eval coverage via `methodology_applicability_contract_present`.
- Synced Product-Agent OS README/docs/backlog and root control-plane files.

## T9-D1 Completed Slice

- Added `business_product` methodology catalog coverage for product hypothesis, target segment, value proposition, opportunity framing, metrics, analytics tracking, qualitative feedback, privacy classification, AI product eval, release measurement, workflow-promotion value evidence, decision horizon and metric scope.
- Added artifact templates: `product-brief.md`, `value-proposition.md`, `opportunity-tree.md`, `experiment-plan.md`, and `tracking-plan.md`.
- Added read-only audit recommendations, false-positive coverage, lifecycle skill routing and fixture eval coverage through `business_product_contract_present`.

## T9-D2 Completed Slice

- Added `requirements_domain` methodology catalog coverage for requirement quality, stable IDs, acceptance scenarios, declarative scenario quality, traceability, business rules, non-goals/constraints, open questions, domain events, API/UI/data traceability, owner review, accepted gaps and change impact.
- Added artifact templates: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md`.
- Added `docs-maintainer` lifecycle skill and strengthened requirements/planning/testing/review skills with Requirements & Domain gates.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, renderer registration and fixture eval coverage through `requirements_domain_contract_present`.

## T9-D3 Completed Slice

- Added `solution_architecture` methodology catalog coverage for architecture scope, context/container views, slice boundaries, owner responsibility, bounded-context trace, dependency rules, public contracts, data ownership, runtime topology, observability, quality attributes, ADR/tradeoffs, trust boundaries, diagram render checks, fitness functions, migration rollback, docs lifecycle, owner review and accepted gaps.
- Added artifact templates: `architecture-review-record.md`, `architecture-fitness-functions.md`, `trust-boundary-map.md`, and `architecture-docs-tooling-decision.md`.
- Strengthened `architecture-overview.md` and `adr.md` with `Source status:`, owner, evidence, accepted gaps, residual risk, rollback/no-rollback rationale and no-secrets guidance.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, renderer registration, lifecycle skill routing and fixture eval coverage through `solution_architecture_contract_present`.

## T9-D4 Completed Slice

- Added `quality_testing_evals` methodology catalog coverage for quality strategy, risk based scope, current command/eval/runtime/manual evidence, acceptance traceability, contract checks, eval reruns, CI gates, flaky-test ownership, coverage policy, test data privacy, bug reproduction, regression impact and evidence before completion.
- Added artifact templates: `test-eval-matrix.md`, `quality-strategy.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md`.
- Strengthened generated `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with quality statuses, evidence gates and the `quality-current-evidence-before-completion` behavioral case.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, discovery signals, renderer registration, lifecycle skill routing and fixture eval coverage through `quality_testing_evals_contract_present`.

## Rollback

- Revert only files touched by the current slice.
- Preserve verification evidence and failure notes in `RUNLOG.md`.
- Do not use destructive git operations without explicit approval.
<!-- product-agent-os:end plan -->
