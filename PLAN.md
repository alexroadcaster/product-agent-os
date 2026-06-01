# PLAN.md

<!-- product-agent-os:start plan -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-06-01

## Current State

- `T9-D8` API & Integrations methodology integration is implemented; final verification evidence is recorded in `TEST.md` and `RUNLOG.md`.
- `T9-D9` Database & Data methodology integration is implemented; final verification evidence is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- `T9-D10` LLM / AI / RAG methodology integration is implemented through rows `M30..M36`; final batch verification is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- `T9-D11` Security, Privacy & Compliance methodology integration is implemented; focused security checks and fixture eval evidence are recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- `T9-D12` Delivery, Release & Operations methodology integration is implemented; final verification evidence is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- `T9-S` Task 20 Cross-Domain Synthesis is implemented through `M10..M14`; final fixture/report/lifecycle/docs handoff evidence is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- `T9-R` Task 21 Update Runtime Runner And Finish Options is implemented through `M25`; runtime methodology packet, finish options, safety guards, CLI/validator output, generated control-plane/eval/handoff contracts, schema compatibility, status mapping, cross-domain bridge, compact first response, high-risk taxonomy, ownership/parallelism routing and evidence sync are recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- Verification baseline after the latest completed Track 9 batch: T9-R M16..M25 runtime/template/fixture/full checks pass; final evidence is recorded in `TEST.md`, `RUNLOG.md` and the Track 9 backlog.
- Track 9 design is recorded in `docs/superpowers/specs/2026-05-25-track-9-methodology-intelligence-design.md`.
- Track 9 implementation plan is recorded in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Track 10 implementation plan is staged in `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- Task 22 final Track 9 documentation sync is closed in docs, source registry, READMEs and root control-plane scope; final verification evidence is recorded in `TEST.md` and `RUNLOG.md`.
- Track 10 `Task 23: Guided Question Protocol And Project Status Dashboard` is implemented and fully verified through Batch 6 `T10-Q-M23..M25`: `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, and `stale_evidence_no_success_claim` are now the eval/docs/skills contract.
- Track 10 `Task 24: Self-Verification And Modernization Loop` is staged in the Track 10 plan with description, reuse-first guardrails, matrix `T10-SV-M-1..M62` and batches 7-12. Batch 7 foundation/registry, Batch 8 trace/redaction/dataset/judge, Batch 9 metrics/scorecards/confidence/cadence, Batch 10 ledger/reports/candidates/CLI, Batch 11 runtime/discovery/lifecycle/eval contracts and Batch 12 docs/control-plane/final verification closure are implemented with read-only metrics-loop contracts, staged-only report rendering, review-only runtime routing and focused RED/GREEN tests.
- Track 10 `Task 25: Project Code Graph And HTML Cockpit Visualization` is staged in the Track 10 plan with read-only scanner scope, V2 matrix `T10-CG-V2-M01..M32` and batches 13-18. Batch 13 `T10-CG-V2-M01..M07` is implemented and verified for file-level graph foundation, Batch 14 `T10-CG-V2-M08..M13` is implemented and verified for Python AST package/module/class/function/method overlays plus structured overlays, Batch 15 `T10-CG-V2-M14..M18` is implemented and verified for graph query packets, query CLI mode, runtime/status/lifecycle graph summaries and graph analysis reports, and Task 25 Batch 16 `T10-CG-V2-M19..M26` is implemented for generated cockpit visualization with Code Flow inside `Code Intelligence`, Graphology-compatible static projection, local Graphology/Sigma vendor boundary, selected-node evidence and fallback static views. Search-quality evals, fixture structural fields, optional indexed-query backend, semantic/rationale extraction and final Task 25 closure verification evidence does not exist yet.
- Commit/push/PR remains explicit-only after Track 10 verification batches; no `git add`, `git commit`, `git push` or PR creation was executed.

## Architecture Boundary

- Primary implementation boundary: `plugins/product-agent-os/`.
- Track 9 methodology source boundary: `docs/methodologies/`.
- Documentation boundary: `docs/product-agent-os/`, `docs/product-agent/`, `docs/sources/`, root control-plane files.
- Track 10 planning boundary: `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
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
| 6 | `T9-D5` Codex / Agentic Workflow | `done` | Control-plane, skills, subagents, handoff, MCP and automation gates |
| 7 | `T9-D6` Frontend | `done` | UI behavior, component state, FSD, Storybook, a11y and visual evidence gates |
| 8 | `T9-D7` Backend | `done` | Service boundary, runtime, observability, SLO and rollback gates |
| 9 | `T9-D8` API & Integrations | `done` | OpenAPI/AsyncAPI/GraphQL/gRPC contract and compatibility gates |
| 10 | `T9-D9` Database & Data | `done` | Schema, migration, data quality, lineage, privacy and production access gates |
| 11 | `T9-D10` LLM / AI / RAG | `done` | AI behavior, prompt/model/tool/RAG eval and safety gates |
| 12 | `T9-D11` Security, Privacy & Compliance | `done` | Threat, privacy, ASVS/SSDF, secrets, supply-chain and compliance gates |
| 13 | `T9-D12` Delivery, Release & Operations | `done` | Release readiness, artifact manifest, rollout, rollback and operations gates |
| 14 | `T9-S` cross-domain synthesis | `done` | Deduplicated gates, merged artifacts, conflict rules and final baseline |
| 15 | `Task 21` runtime runner and finish options through `T9-R-M14` | `done` | Runtime consumption of synthesis packets, finish-option behavior and evidence sync |
| 16 | `Task 21` runtime runner expansion `T9-R-M16..M25` | `done` | CLI/validator, generated control-plane/eval/handoff, compatibility, status mapping, bridge, taxonomy and ownership guards |
| 17 | `Task 22` final Track 9 documentation sync | `done` | Product-Agent OS docs, source registry/backlog closure and final Track 9 verification |
| 18 | Track 10 `Task 23` guided questions and status dashboard | `verified-no-commit` | Typed question protocol, answer ledger, status snapshot, staged offline HTML dashboard, behavioral/transcript evals, lifecycle skill wording, docs/source registry sync and full Batch 6 verification |
| 19 | Track 10 `Task 24` self-verification and modernization loop | `verified-no-commit` | Reuse-first metrics loop foundation, trace/redaction/dataset/judge contracts, metric aggregation, scorecards, confidence gates, cadence recommendations, redacted run records, scorecard ledger, offline report/CLI, daily/weekly packets, staged modernization candidates, runtime/discovery/lifecycle/eval integration, false-positive coverage and docs/control-plane closure are implemented; final verification uses `timeout_ms: 1200000` and commit/push/PR remains explicit-only |
| 20 | Track 10 `Task 25` project code graph and HTML cockpit visualization | `batch-16-focused-no-commit` | Batch 13 implements file-level graph foundation, Batch 14 implements Python scanner/dependency/structured overlays, Batch 15 implements graph query packets/runtime/status/analysis, and Batch 16 implements generated cockpit visualization with focused verification. Batches 17-18 remain for fixture/search evals, future gates and final closure. |

## Track 10 Handoff

- Start Track 10 only after Track 9 `Task 22` closes docs, source registry and backlog references for Track 1 through Track 9.
- Track 10 `Task 23` starts only after Task 22 closure and uses the Track 10 plan at `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- During Task 22 closure, absorb the legacy Track 9 `Task 23: Final Verification Baseline` into Task 22 final verification evidence.
- Track 10 `Task 23` must keep JSON/Markdown as source of truth; `status.html` is a generated review artifact, not an editable database or runtime authority.
- Track 10 must preserve staged-first behavior: generated question ledgers, status snapshots and dashboard files are proposed under `.codex/product-agent-os/` and protected by existing approval/merge safety.
- Track 10 non-goals remain: no standalone server, no database, no live model/API calls, no external writes, no hook/automation activation and no browser-based file editing.
- Batch 6 closure verifies Task 23 guided question protocol and status dashboard guarantees: compact first response, one blocking question maximum, no broad methodology interview, dashboard generated view only, `dashboard_not_source_of_truth`, `stale_evidence_no_success_claim`, full unit/fixture/transcript/Codex compatibility/docs/MkDocs/diff hygiene and explicit-only commit boundary.
- Track 10 `Task 24` starts after Task 23 closure and uses the same Track 10 plan. Its batches are Batch 7 foundation/registry, Batch 8 trace/redaction/dataset/judge contracts, Batch 9 metrics/scorecards/confidence/cadence, Batch 10 ledger/reports/candidates/CLI, Batch 11 runtime/discovery/lifecycle/evals and Batch 12 docs/control-plane/full verification.
- Task 24 must modernize existing Product-Agent OS surfaces before adding new subsystems: reuse redaction, guided question protocol, status snapshot/dashboard, automation policy, runtime contracts/routes, fixture eval runner, transcript eval runner and agentic workflow artifacts.
- Task 24 Batch 7 implements only foundation/registry surfaces: source-priority policy, target registry collection, explicit evidence intake, stale/failed/accepted-gap markers, generated-view exclusions and deterministic packet bounds. It does not add report rendering, CLI staging, runtime route fields, automation candidates or active schedules.
- Task 24 Batch 8 implements only trace/redaction/dataset/grader/judge contract surfaces: portable trace normalization, metrics redaction blocking, stratified evidence datasets, dataset quality blockers, local grader summaries and judge calibration blocking. It does not add metric aggregation, scorecards, report rendering, CLI staging, runtime route fields, automation candidates or active schedules.
- Task 24 Batch 9 implements only metrics/scorecard/confidence/cadence contract surfaces: sectioned metric aggregation, repeatability calculations, guarded scorecards, confidence and decision gates, cadence recommendation and deterministic redacted run records. It does not add scorecard ledger templates, report rendering, CLI staging, runtime route fields, lifecycle wording, fixture eval fields, active automations or external writes.
- Task 24 Batch 10 implements only ledger/report/candidate/CLI surfaces: trace data-classification gate, shared offline artifact safety, scorecard ledger, daily/weekly report packets, component prioritization, modernization candidates, redacted offline metrics report renderer, CLI dry-run/stage and metrics automation candidate-only blocking. It keeps reports and daily/weekly automation candidates opt-in staged artifacts and does not add runtime route fields, lifecycle wording, active automations, live eval/model/API calls or external writes.
- Task 24 Batch 11 implements only runtime/discovery/lifecycle/eval integration: bounded status snapshot summaries, `agent_skill_metrics_loop` discovery/applicability packets, methodology audit recommendations, additive runtime packet validation, review-only finish options, one-blocking-question guided question routing, lifecycle skill wording, fixture false-positive coverage, behavioral eval cases and transcript sessions. It does not apply modernization candidates, activate schedules, call live eval services or claim semantic metric sufficiency.
- Task 24 Batch 12 implements docs/control-plane/final verification closure for `T10-SV-M58..M62`: Product-Agent OS docs, READMEs, source registry, Track 10 backlog and root control-plane artifacts explain `agent_skill_metrics_loop`, target registry, trace intake, dataset quality, grader/judge calibration, cadence recommendation, scorecard ledger, report safety, modernization candidates, source-of-truth policy and approval boundary. The full unittest command must use `timeout_ms: 1200000`; git add/commit/push/PR stays explicit-only.
- Task 24 non-goals remain: no autonomous mutation, no active schedules, no live eval/model/API calls, no external writes, no dashboard/report-as-source claims and no update candidate without rollback target, owner review and explicit approval state.
- Task 24 closure requires current focused tests/evals for the metrics loop plus full Product-Agent OS verification; planning rows and matrix presence alone are not implementation evidence.
- Track 10 `Task 25` starts after Task 24 closure and uses the same Track 10 plan. Its V2 batches are Batch 13 graph foundation/schema/staging with baseline audit, schema/ontology/validator, manifest/freshness/provenance, read-only staging, privacy/source boundary, observation ledger and scale fixtures; Batch 14 Python AST scanner, dependency edges and overlays with package/symbol extraction, imports/calls, conservative resolution, tests/fixtures, unsupported-language behavior, docs/contracts/schemas/diagrams overlays, readiness partitions and aliases; Batch 15 agent query packets, runtime integration and analysis with query CLI, budget/filter safety, read-order/trace/delta/impact packets, status/runtime/lifecycle integration and analysis report; Batch 16 HTML cockpit, code graph visualization and project map with eight-page cockpit shell, page contracts, offline no-external-assets renderer, visual projection, local Graphology/Sigma boundary, filters, focused subgraphs, selected-node evidence, large-graph clustering/fallback/mobile behavior, Code Flow section and visual QA; Batch 17 evals/docs/control-plane/future gates with fixture fields, search-quality evals, docs/source registry sync and explicit future backend/semantic gates; Batch 18 focused/full verification and closure.
- Task 25 must keep project scanning read-only and staged-first. Graph HTML is a generated cockpit view; source code, checked-in docs and graph JSON/JSONL artifacts are the evidence layer. No standalone server, database, live model/API call, external write, hook/automation activation or browser file editing is in scope.
- Task 25 implementation acceptance requires stable graph node IDs, confidence-labelled edges, manifest freshness/provenance, observation lineage, temporal edge invalidation/supersession, schema/size validation, controlled ontology registry, shrink guard, stage-local path/symlink safety, conservative symbol resolution, generated-file downranking, redaction/no-raw-source policy, unsupported-language statuses, structured docs/contract chunking, partition-aware scopes, canonical alias ledger, trace/affected-test/as-of/delta/status/search query packets, query filter safety, operation budget/tracing packets, search-quality evals, bounded 1k/5k/10k graph behavior, token-budgeted adaptive agent query packets, eight-page HTML cockpit structure, Graphology-compatible visual projection, local Graphology/Sigma asset manifest, Sigma renderer bootstrap, large-graph render modes, selected-node evidence panel, graph navigation commands, fallback static view, mobile graph behavior, visual QA, analysis report, Code Flow section inside `Code Intelligence`, optional indexed-query backend decision without live database activation, semantic/rationale extraction approval-gated outside baseline and no external visualization assets.

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
- Codex/agentic workflow gate: `codex_agentic_workflow` records agentic scope, source of truth, control plane, read-only discovery, approval boundary, fresh-context handoff, ownership split, safe subagent parallelism, skill promotion evidence, plugin boundary, MCP permission review, hook activation approval, automation manual stability, model/reasoning policy, memory policy, agent eval workflow and evidence before completion.
- Codex/agentic workflow artifacts: `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, `agent-eval-workflow.md`, plus existing `AGENTS.md`, `.codex/config.toml`, `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, `automation-candidate.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`.
- Frontend gate: `frontend` records user-flow acceptance, component docs, component state matrix, design-system boundary, conditional FSD boundary review, API/data state alignment, accessibility review, keyboard/focus evidence, responsive viewport matrix, visual evidence, runtime console evidence, performance budget, browser support, content/i18n boundary, interaction test evidence and unsupported-claim rejection.
- Frontend artifacts: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, `frontend-performance-budget.md`, plus existing `component-card.md`, `acceptance-scenarios.md`, `api-contract-review.md`, `quality-strategy.md`, `test-eval-matrix.md` and `manual-qa-evidence.md`.
- Backend gate: `backend` records service boundary, runtime behavior, dependency failure policy, observability, SLI/SLO or explicit gap, health endpoint semantics, job/queue contract, data consistency strategy, config/secrets boundary, security review, rollback/recovery, CI/deployment discovery, severity policy, framework-agnostic snippet policy, retry/idempotency detection limits, owner-reviewed evidence sufficiency and unsupported-claim rejection.
- Backend artifacts: `backend-service-overview.md`, `backend-runtime-behavior.md`, `backend-dependency-failure-matrix.md`, `backend-observability-map.md`, `backend-slo-sheet.md`, `backend-health-check-contract.md`, `backend-job-queue-contract.md`, `backend-data-consistency-record.md`, `backend-config-secrets-manifest.md`, `backend-release-rollback-notes.md`, `backend-operational-runbook.md`, plus overlap with `adr.md`, `migration-plan.md`, `security-risk-review.md`, `release-packet.md`, `api-contract-review.md`, `quality-strategy.md`, `test-eval-matrix.md` and `manual-qa-evidence.md`.
- API & Integrations gate: `api_integrations` records contract source, consumer map, breaking-change review, security review, error contract, contract-test matrix, event delivery, generated SDK manifest, external-write approval, API observability, style choice and unsupported-claim rejection.
- API & Integrations artifacts: `api-inventory.md`, `api-contract-review.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md`, `api-style-guide.md`, plus overlap with `integration-catalog.md`, `migration-plan.md`, `security-risk-review.md`, `release-packet.md`, `quality-strategy.md` and `test-eval-matrix.md`.
- Database & Data gate: `database_data` records datastore inventory, dictionary, schema source, migration plan, expand-contract rollout, transaction boundary, rollback feasibility, backup/restore evidence, data classification, data quality, producer/consumer data contract, lineage, query/index performance, retention/deletion, synthetic fixture policy, production access approval, constraints/integrity and unsupported-claim rejection.
- Database & Data artifacts: `database-inventory.md`, `database-dictionary.md`, `database-migration-plan.md`, `database-expand-contract-record.md`, `database-backfill-runbook.md`, `database-rollback-feasibility.md`, `database-backup-restore-evidence.md`, `database-data-classification-matrix.md`, `database-data-quality-checks.md`, `database-data-contract.md`, `database-lineage-map.md`, `database-query-performance-review.md`, `database-retention-deletion-policy.md`, `database-synthetic-fixtures-policy.md`, `database-production-access-approval.md`, plus overlap with `migration-plan.md`, `security-risk-review.md`, `quality-strategy.md`, `test-eval-matrix.md` and `release-packet.md`.
- LLM / AI / RAG gate: `llm_ai_rag` records user-visible AI behavior promise, baseline eval, eval rerun evidence, dataset governance, prompt contract, model decision, structured output schema, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding rubric, agent workflow trace, safety/guardrail review, cost/latency budget, current-run evidence, handoff compatibility, eval tooling selection, model migration thresholds, RAG lifecycle/privacy, diff-signal limits, AI incident workflow and unsupported-claim rejection.
- LLM / AI / RAG artifacts: `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-task-packet.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md`, `ai-cost-latency-budget.md`, plus existing `ai-eval-spec.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`.
- Security, Privacy & Compliance gate: `security_privacy_compliance` records security-sensitive classification, threat surface, security risk review, ASVS/SSDF/SAMM mapping, ASVS level selection, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact, external-write approval, abuse/rate-limit review, audit logging, supply chain, SBOM/provenance, CI permissions, AI security, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status, evidence before completion and unsupported-claim rejection.
- Security, Privacy & Compliance artifacts: `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md` and `approval-record.md`.
- Delivery, Release & Operations gate: `delivery_release_operations` records release scope, version impact, changelog/release notes, artifact manifest, release evidence before completion, rollout strategy, rollback/recovery, environment approval boundary, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review, automation manual stability, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff, owner-reviewed release evidence sufficiency and unsupported-claim rejection.
- Delivery, Release & Operations artifacts: `versioning-policy.md`, `release-readiness.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `post-release-review.md`, `approval-record.md`, `automation-candidate.md`, plus cross-domain handoff to `supply-chain-review.md`, `sbom-manifest.md` and `vulnerability-response-record.md`.
- Cross-domain synthesis gate: `methodology_synthesis` groups recommendations by owner artifact, records owner and consumer domains, merged gates, source artifact ledger, alias/deferred artifact decisions, semantic evidence sufficiency, owner-question dedupe, risk-aware safe next action and false-positive guards for mixed methodology surfaces.
- Cross-domain synthesis artifacts: additive audit/discovery/report packets, grouped `recommendation_groups`, source artifact ledger, semantic evidence sufficiency fields in generated control-plane/eval templates, synthetic overlap fixtures and lifecycle skill routing guidance.
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

## T9-D6 Completed Slice

- Added `frontend` methodology catalog coverage for user flows, component docs/state, design-system governance, conditional FSD, API/data state alignment, accessibility, keyboard/focus, responsive/visual/runtime evidence, interaction tests, performance, browser support, content/i18n and unsupported-claim rejection.
- Added artifact templates: `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md` and `frontend-performance-budget.md`.
- Strengthened `component-card.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, `behavioral-workflows.json` and lifecycle skills with Frontend gates.
- Added synthetic `frontend-ui-app` fixture and fixture eval coverage through `frontend_contract_present`.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, renderer registration, lifecycle skill routing and fixture eval coverage through `solution_architecture_contract_present`.

## T9-D7 Backend Completed Slice

- Rows `T9-D7-M0..M19` established backend catalog coverage, discovery, read-only audit recommendations, staged backend artifacts, generated control-plane/eval coverage, lifecycle routing, unsupported-claim rejection and synthetic `backend-service-app` fixture coverage.
- Rows `T9-D7-M20..M29` deepen dependency failure policy, job/queue/DLQ/replay policy, data consistency and saga policy, observability/no-private-payload logging, SLI/SLO or explicit gap, health endpoint semantics, operational runbook handoff, rollback/recovery policy, Twelve-Factor vocabulary and service-boundary owner review/ADR routing.
- Rows `T9-D7-M30..M39` deepen requirements-author backend intake, security notes, observability semantics, SLO/health/runbook/config/rollback depth, contract-aware backend evidence and backend dependency categories.
- Rows `T9-D7-M40..M45` add backend delivery discovery signals, severity policy, framework-agnostic snippet policy, lightweight retry/idempotency detection, Product-Agent OS docs/source sync and semantic evidence sufficiency routing to T9-S.
- Backend methodology is complete for Track 9 scope; human owner review of concrete test/eval/runtime sufficiency for a real project remains a shared T9-S/cross-domain concern.

## T9-D8 API & Integrations Completed Slice

- Added `api_integrations` catalog coverage for contract sources, consumers, compatibility, security, errors, contract tests, events/webhooks, generated SDKs, external writes, observability, style choice and unsupported-claim rejection.
- Added read-only discovery/audit coverage for OpenAPI, Swagger source files, AsyncAPI, GraphQL, protobuf, JSON Schema, Pact, webhooks/events, generated clients and external providers.
- Added API artifact templates and renderer registration for inventory, consumer map, compatibility, contract-test matrix, error catalog, auth/authorization matrix, generated SDK manifest, webhook/event contract, external integration approval and style guide.
- Strengthened generated control-plane/eval templates, lifecycle skills, Product-Agent OS README/docs, source registry and Track 9 backlog with API gates.
- Added synthetic API fixtures for full contract coverage, external-write approval, Swagger-UI-only false positive and GraphQL/gRPC style choice.

## T9-D9 Database & Data Completed Slice

- Added `database_data` catalog coverage for database inventory, dictionary, schema source, migration plan, expand-contract rollout, transaction boundary, rollback feasibility, backup/restore evidence, data classification, data quality, data contract, lineage, query performance, retention/deletion, synthetic fixtures, production access approval, constraints/integrity and unsupported-claim rejection.
- Added read-only discovery/audit coverage for schema files, migrations, migration tooling, ORM models, dictionaries, data quality, lineage, query performance, production access, destructive changes, pipelines, RAG ingestion, backup/restore and privacy/retention signals.
- Added Database & Data artifact templates and renderer registration for inventory, migration plan, expand-contract, backfill, rollback feasibility, backup/restore, classification, quality checks, data contract, lineage, query performance, retention/deletion, synthetic fixtures and production access approval.
- Strengthened generated control-plane/eval templates, lifecycle skills, Product-Agent OS README/docs, source registry and Track 9 backlog with Database & Data gates.
- Added synthetic database fixtures for schema-only false positive, destructive migration, production access approval and lineage/RAG overlap.

## T9-D10 LLM / AI / RAG Completed Slice

- Rows `T9-D10-M0..M9` added the `llm_ai_rag` catalog contract, read-only discovery packet, readiness gate, baseline/rerun recommendations, unsupported-claim handling and false-positive guards.
- Rows `T9-D10-M10..M19` strengthened audit recommendations for dataset governance, prompts, models, structured output, tool/function/MCP contracts, human approvals, RAG, agent traces, guardrails and cost/latency, and added the AI/RAG artifact template set.
- Rows `T9-D10-M20..M29` resolved source-aligned template aliases, registered 15 AI/RAG templates in the renderer, strengthened `ai-eval-regression.md`, `ai-eval-spec.md` and generated `PLAN/TEST/EVALS/RUNLOG`, added behavioral/transcript coverage, synthetic AI/RAG fixtures, `llm_ai_rag_contract_present` fixture eval coverage and lifecycle skill routing.
- Rows `T9-D10-M30..M36` closed agent handoff compatibility, eval tooling selector policy, model migration thresholds, RAG deletion/privacy lifecycle, diff-signal policy, AI incident boundary and methodology report rendering.

## T9-D11 Security, Privacy & Compliance Completed Slice

- Rows `T9-D11-M0..M7` added the `security_privacy_compliance` catalog contract, read-only discovery depth, domain routing, granular gate recommendations and unsupported-claim rejection.
- Rows `T9-D11-M8..M13` strengthened the security artifact set, renderer registration, source/no-secrets policy, readiness and behavioral eval contracts, synthetic false-positive fixtures and lifecycle skill routing.
- Rows `T9-D11-M16..M23` mapped the full source artifact set, ASVS/SSDF/SAMM policy, authorization negative-test depth, redaction lifecycle, SBOM/provenance policy, vulnerability response workflow, compliance overlay taxonomy and methodology report redaction.
- The staged renderer now includes 16 new Security, Privacy & Compliance templates and the `python-app` renderer file count increased from 157 to 173.

## T9-D12 Delivery, Release & Operations Completed Slice

- Rows `T9-D12-M0..M9` added the `delivery_release_operations` catalog contract, template aliases, read-only discovery depth, methodology applicability packet and initial release scope/version/changelog/release evidence recommendations.
- Rows `T9-D12-M10..M19` added artifact manifest, rollout, rollback/recovery, environment approval, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response and post-release measurement gates.
- Rows `T9-D12-M20..M29` added automation manual stability, renderer registration for 13 delivery templates, methodology report external-action status, generated control-plane/eval coverage, lifecycle skill routing and false-positive/approval fixtures.
- Rows `T9-D12-M30..M40` added final release depth for release mode policy, build-release-run boundary, platform distribution, release communication, versioning tooling, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency.
- The staged renderer keeps file count 186; fixture eval covers 66 fixtures and exposes `delivery_release_operations_contract_present`.

## T9-S Task 20 Cross-Domain Synthesis Completed Slice

- Rows `T9-S-M0..M4` added synthesis contract tests, additive top-level `synthesis` catalog metadata, source artifact aliases/decisions and pure grouping/classification/dedupe helpers.
- Rows `T9-S-M5..M9` integrated `methodology_synthesis` into audit output, added grouped recommendations, risk-aware safe next action, discovery applicability packets, semantic evidence sufficiency contracts and focused false-positive hardening.
- Rows `T9-S-M10..M14` added packaged mixed-risk overlap fixtures, named fixture eval checks, Cross-Domain Synthesis report rendering, lifecycle skill consumption, behavioral eval/docs sync and final handoff evidence.
- The staged renderer keeps file count 186; fixture eval covers 73 fixtures and exposes `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present`.
- Task 21 consumes synthesized packets in runtime routing and finish-option behavior without forcing unrelated methodology gates.

## T9-R Task 21 Runtime Runner And Finish Options Completed Slice

- Rows `T9-R-M0..M6` added a compact route-level `methodology_packet`, bounded list/type validation, runtime propagation from workspace discovery, ordered finish options, recommendation-only no-write behavior and detection-only completion blocking.
- Rows `T9-R-M7..M13` added approval-bound high-risk methodology action handling, automation maturity blocking, methodology route payload redaction, malformed packet fallback behavior, synthetic runtime methodology fixtures and named fixture eval checks.
- Row `T9-R-M14` synchronized Track 9 evidence, residual risks and next action across the backlog, RUNLOG and root control-plane/system files.
- Rows `T9-R-M16..M25` added CLI/validator JSON output coverage, generated control-plane/eval/handoff contracts, schema-v1 backward compatibility, lifecycle-status finish options, cross-domain runtime bridge checks, compact first-response fields, structured high-risk taxonomy and ownership/parallelism routing.
- Fixture eval covers 80 fixtures and 16 codex-runner fixtures, with runtime checks for methodology packet presence, approval-bound finish options, detection-not-completion, external-write blocking, automation maturity, redaction, malformed packet blocking, cross-domain bridge and compact first response.

## T9-D4 Completed Slice

- Added `quality_testing_evals` methodology catalog coverage for quality strategy, risk based scope, current command/eval/runtime/manual evidence, acceptance traceability, contract checks, eval reruns, CI gates, flaky-test ownership, coverage policy, test data privacy, bug reproduction, regression impact and evidence before completion.
- Added artifact templates: `test-eval-matrix.md`, `quality-strategy.md`, `ci-evidence-record.md`, `flaky-test-policy.md`, and `manual-qa-evidence.md`.
- Strengthened generated `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json` and `behavioral-workflows.json` with quality statuses, evidence gates and the `quality-current-evidence-before-completion` behavioral case.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, discovery signals, renderer registration, lifecycle skill routing and fixture eval coverage through `quality_testing_evals_contract_present`.

## T9-D5 Completed Slice

- Added `codex_agentic_workflow` methodology catalog coverage for control-plane maturity, source-of-truth boundaries, read-only discovery, approval boundaries, model/reasoning policy, memory policy, handoffs, ownership split, subagent safety, MCP review, hook governance, plugin boundary, skill promotion, automation stability, agent eval workflow and evidence before completion.
- Added artifact templates: `model-reasoning-policy.md`, `mcp-permission-review.md`, `hook-governance.md`, `skill-promotion-record.md`, and `agent-eval-workflow.md`.
- Strengthened generated `AGENTS.md`, `.codex/config.toml`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`, `project-readiness.json`, `behavioral-workflows.json`, `agent-task-packet.md`, `worktree-ownership.md` and `automation-candidate.md` with Codex workflow gates, runtime routing, approval boundaries and no silent activation.
- Added read-only audit recommendations, false-positive and unsupported-claim coverage, discovery signals, renderer registration, lifecycle skill routing and fixture eval coverage through `codex_agentic_workflow_contract_present`.

## Rollback

- Revert only files touched by the current slice.
- Preserve verification evidence and failure notes in `RUNLOG.md`.
- Do not use destructive git operations without explicit approval.
<!-- product-agent-os:end plan -->
