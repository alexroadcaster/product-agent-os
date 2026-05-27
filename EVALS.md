# EVALS.md

<!-- product-agent-os:start evals -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-27

## Rubrics

- Source grounding: official sources and checked-in docs drive durable rules; community claims stay in insight/research layer.
- Methodology applicability: gates are conditional and can be marked not applicable or accepted gap.
- Evidence-before-completion: implemented in `T8-A16`; no ready/completed/fixed/works/release claim without current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap.
- Architecture boundary: implementation stays inside named files and ownership boundaries.
- Domain traceability: complex domain work links domain model, bounded contexts, architecture boundary and ubiquitous language terms.
- Documentation quality: user-facing docs are Russian, behavior-level, and name inputs, outputs, verification, risks and next artifact.

## Thresholds

- Blocking failure: unit test failure, fixture eval failure, docs check failure, strict MkDocs failure after nav/MkDocs-sensitive docs changes, or Codex compatibility regression.
- Accepted gap: allowed only when reason, owner, evidence owner and follow-up are explicit.
- Residual risk: must be carried into `RUNLOG.md` and final response.

## Behavioral Route Evals

- Scenario workflows through `T8-S16`: implemented.
- No-placeholder planning, two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain model and bounded-context traceability: implemented.
- Ubiquitous language traceability: implemented in `T8-A7`.
- FSD structure routing: implemented in `T8-A8`.
- Metric hardening: implemented in `T8-A9`.
- Evidence-before-completion: implemented in `T8-A16`.
- Docs tooling selector and `docs_as_code_impact` applicability statuses: implemented in `T8-C`.
- Conditional readiness gates: implemented in `T8-F`.
- Scenario, behavioral eval and Codex compatibility docs: implemented in `T8-H`.
- Transcript/session eval replay: implemented in `T8-GY`.
- Standards trigger policy: implemented in `T8-B`.
- False-positive scenario fixture coverage: implemented in `T8-GX`.
- Detailed discovery status depth: implemented in `T8-D`.
- Track 9 methodology intelligence plan: authored in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Track 9 foundation, `T9-D1` Business/Product, `T9-D2` Requirements/Domain, `T9-D3` Solution Architecture, `T9-D4` Quality/Testing/Evals, `T9-D5` Codex/Agentic Workflow, `T9-D6` Frontend, `T9-D7` Backend, `T9-D8` API & Integrations, `T9-D9` Database & Data, `T9-D10` LLM / AI / RAG, `T9-D11` Security, Privacy & Compliance, `T9-D12` Delivery, Release & Operations, `T9-S` Task 20 Cross-Domain Synthesis and `T9-R` Task 21 Runtime Runner And Finish Options through `M14`: implemented.

## Track 9 Methodology Intelligence Evals

- Section protocol: every Track 9 section must start by reading its plan task and deeply auditing the matching `docs/methodologies/` source file.
- Plan freshness: if the source-file audit finds missing gates, artifacts, tooling candidates, false-positive risks, unsupported claims or open questions, the plan or Track 9 backlog must be updated before implementation.
- Domain coverage: every domain section must map source methodology concepts to catalog entries, discovery signals, readiness gates, artifact templates, lifecycle skill guidance, tests/evals and docs sync.
- Proportionality: DDD, FSD, docs portals, security/compliance, AI/RAG evals, database production gates and release governance must be conditional, with `not_applicable` or accepted gaps allowed when justified.
- Evidence: section completion requires focused tests/evals plus full verification proportional to touched files.
- Residual risk: semantic methodology quality still requires owner/domain/security/product review and cannot be proven by template presence alone.

## Runtime Runner Finish Option Evals

- `runtime_methodology_packet_present`: implemented through `T9-R-M14`.
- Required evidence: compact `methodology_packet`, bounded list/type validation, runtime route propagation, ordered `finish_options`, owner questions, source artifact ledger, semantic evidence sufficiency, safe next action and read-only methodology write policy.
- Approval boundary: recommendation-only packets cannot stage artifacts; high-risk methodology actions and external writes remain approval-required; automation promotion requires manual stability plus value/maturity evidence.
- Completion boundary: `present_unverified` methodology detections, recommendation text and source artifact presence do not satisfy completed/readiness claims without current verification evidence.
- Runtime safety checks: methodology route payloads are redacted, malformed packets return stable errors without traceback, and synthetic codex-runner fixtures cover approval, detection-only, external-write, automation maturity, redaction and malformed-packet paths.
- Residual risk: current runtime checks cover synthetic methodology packets and free-text high-risk matching; remaining Task 21 rows must add CLI/validator depth, generated control-plane/eval/handoff contracts, schema-v1 compatibility, status-to-finish-options mapping, cross-domain runtime bridge checks, compact first-response fields, structured high-risk taxonomy and ownership/parallelism routing.

## Business Product Evals

- `business_product_contract_present`: implemented in `T9-D1`.
- Required evidence: product hypothesis, target segment, value proposition, opportunity framing, decision horizon, metric scope, analytics tracking plan, qualitative feedback loop, privacy classification, AI product eval where applicable, release measurement evidence and workflow-promotion value evidence.
- False-positive protection: typo-only docs edits, formatting-only edits and dependency pins without behavior impact do not force product methodology.
- Residual risk: product artifacts prove the evidence shape, not that the selected market, value proposition or metric is strategically correct.

## Requirements Domain Evals

- `requirements_domain_contract_present`: implemented in `T9-D2`.
- Required evidence: requirements scope, requirements owner, requirement quality, stable IDs, acceptance scenarios, declarative scenario quality, requirements traceability, business rules, non-goals/constraints, constraints traceability, open questions, stakeholder owner map, story slice map, Example Mapping, domain discovery, domain model when complex, bounded context trace, ubiquitous language trace, invariants/failure modes, domain event contracts, API/UI/data traceability, domain expert review, requirement change impact, accepted gap and requirements evidence before implementation.
- False-positive protection: typo-only docs edits, formatting-only edits and dependency metadata without behavior impact do not force Requirements & Domain methodology on README-only work.
- Unsupported claims rejected: BDD replaces testing, Gherkin is mandatory, user story template is complete requirements, glossary is ubiquitous language and OpenAPI is requirements source of truth.
- Residual risk: requirements/domain artifacts prove traceability structure, not that domain experts have semantically validated every business rule.

## Solution Architecture Evals

- `solution_architecture_contract_present`: implemented in `T9-D3`.
- Required evidence: architecture scope, C4 context/container or equivalent boundary map, slice boundary, boundary responsibility owner, bounded-context-to-architecture trace, dependency rules, public contract trace, data ownership boundary, runtime topology, observability architecture, quality attribute scenarios, ADR/tradeoff record, trust boundary review, diagram render check, architecture fitness functions, migration rollback path, architecture docs lifecycle, owner review and accepted gaps.
- False-positive protection: typo-only docs edits, formatting-only edits, docs-light prototypes without reviewed/diffable diagrams and non-cloud work without Well-Architected review do not force Solution Architecture methodology.
- Unsupported claims rejected: architecture means diagrams, rendered diagram proves correctness, C4 code diagrams are always required, ADR is bureaucracy, Well-Architected review proves architecture quality, architecture-as-code is always required and AI can design architecture from chat alone.
- Residual risk: architecture artifacts prove boundary and evidence shape, not that the selected architecture is semantically optimal or owner-approved for a real production system.

## Quality Testing Evals

- `quality_testing_evals_contract_present`: implemented in `T9-D4`.
- Required evidence: quality strategy, risk based scope, test-first evidence or explicit gap, acceptance traceability, contract checks, runtime evidence, manual QA evidence, visual/a11y evidence, eval spec, eval rerun evidence, current evidence before completion, CI quality gate, flaky-test policy, coverage policy, test data privacy, bug reproduction evidence and regression impact.
- False-positive protection: typo-only docs edits, formatting-only edits, docs-only source cleanup and dependency metadata changes without behavior impact do not force Quality, Testing & Evals methodology.
- Unsupported claims rejected: more tests always means better quality, 100 percent line coverage proves correctness, E2E tests should dominate because they are most realistic, manual QA is not evidence and AI evals are optional for AI behavior changes.
- Residual risk: quality artifacts prove current evidence shape and gate routing, not that a human owner has judged every check sufficient for the real project risk.

## Codex Agentic Workflow Evals

- `codex_agentic_workflow_contract_present`: implemented in `T9-D5`.
- Required evidence: agentic scope, project source of truth, control plane, read-only discovery, approval boundary, fresh-context handoff, ownership split, subagent parallelism safety, skill promotion evidence, plugin boundary, MCP permission review, hook activation approval, automation manual stability, model/reasoning policy, memory policy, agent eval workflow and evidence before completion.
- False-positive protection: simple docs/local work does not force subagents, worktrees, MCP review, hook governance, plugin packaging, automation, Agents SDK orchestration or agent eval workflow unless signals, intent or side-effect risk make them applicable.
- Unsupported claims rejected: memory is project source of truth, subagents are automatically faster, MCP tools are safe because they are tools, hooks are harmless convenience scripts, repeated workflows should become automation immediately, Agents SDK and Codex runtime are the same layer, and inspection proves completion.
- Residual risk: Codex workflow artifacts prove governance shape and approval routing, not that a human owner has approved every model, subagent, MCP, hook, skill, plugin or automation decision for a real project.

## Frontend Evals

- `frontend_contract_present`: implemented in `T9-D6`.
- Required evidence: user-flow acceptance, component docs, component state matrix, design-system boundary, conditional FSD boundary review, API/data state alignment, accessibility review, keyboard/focus contract, responsive viewport matrix, visual evidence, browser/runtime evidence, console status, Playwright trace or accepted gap, performance budget, browser support, content/i18n boundary and interaction test evidence.
- False-positive protection: backend-only, data-only, CLI-only, docs-only, native-only, dependency-only and simple CRUD work does not force Frontend methodology.
- Unsupported claims rejected: FSD is mandatory for every frontend project, Storybook proves UI quality, automated accessibility addon output is enough, a desktop screenshot proves responsive UI, lab Web Vitals always represent production UX and code inspection proves UI completion.
- Residual risk: frontend artifacts prove UI evidence shape and route/gate coverage, not that a human owner has semantically accepted every screenshot, interaction test, accessibility review or performance budget as sufficient for a real product.

## Backend Evals

- `backend_contract_present`: implemented through `T9-D7-M45`.
- Required evidence: service/module boundary, owner, inbound contracts, outbound dependencies, data ownership, deployment/runtime shape, runtime behavior, dependency failure matrix, observability, SLI/SLO or explicit gap, health endpoint semantics, job/queue contract, data consistency strategy, config/secrets boundary, security review, rollback/recovery and owner-reviewed evidence sufficiency or accepted gap.
- Resilience depth: remote dependencies record per dependency timeout, retry/backoff/max attempts, circuit breaker non-applicability, fallback, alert owner and verification evidence.
- Jobs and data depth: queues/jobs record payload contract, retry policy, dead-letter behavior, dead-letter queue, idempotency key, replay procedure, poison-message handling, deduplication, ordering and backpressure; risky distributed data behavior records local transaction, outbox, saga, compensation, monitoring, reconciliation, migration impact and recovery path.
- Operations depth: observability rejects logs-only evidence and requires traces, metrics, logs, dashboards, alerts, correlation IDs, alert ownership, redaction and no-private-payload logging; health checks distinguish liveness, readiness, startup and platform equivalents.
- Rollback and boundary depth: risky backend changes record rollback command or manual procedure, data recovery/replay, irreversible side effects, owner approval and residual risk; new or changed backend responsibility records owner review, decision authority, boundary rationale and ADR link or accepted gap.
- Twelve-Factor depth: backend templates use Twelve-Factor vocabulary for explicit dependencies, config/env keys, build-release-run, process model, stateless process or accepted gap, admin tasks, dev/prod parity and logs-as-event-stream without making Twelve-Factor a mandatory framework.
- Intake/security/ops/contract depth: backend requirements intake records service/user behavior, affected backend unit, dependencies, data stores, runtime constraints, operational assumptions and explicit gaps before implementation planning; security notes cover authn/authz, secrets, rate limits, audit logging, sensitive data, abuse cases, privileged operations and no-secrets evidence.
- Discovery depth: backend dependency categories are exposed as `present_unverified` signals for database, message broker, cache, payment, email, storage, search and third-party HTTP/provider clients; backend delivery discovery records backend stack, backend commands, CI, APIs, DB, queues, workers, deployment manifests and security signals without executing deployments or external writes.
- Severity and snippet policy: risky production backend without service boundary/runtime/failure evidence/security route/rollback is blocker/high-risk; complete accepted-gap fields downgrade eligible observability/SLO/health recommendations; simple local/backend-light work stays warning-level. T9-D7 templates stay framework-agnostic and defer Node.js, Python, Java, .NET and Go snippets until stack-specific owner/examples/verification exist.
- Retry/idempotency detection: T9-D7 uses lightweight read-only signals for retry/idempotency terms plus dependency/job context; deeper static analysis of correctness is deferred to avoid false positives.
- Evidence sufficiency routing: backend records owner reviewed test/eval/runtime evidence sufficiency for real project risk or accepted gap owner, reason, review date, downstream risk and follow-up; shared semantic sufficiency normalization remains T9-S/cross-domain.
- False-positive protection: frontend-only, docs-only, CLI-only, native-only, dependency metadata without backend runtime behavior and package-name-only service folders do not force Backend methodology.
- Unsupported claims rejected: backend means only business logic files, microservices are the professional default, retries make systems reliable, health endpoint exists so readiness is solved, logs are observability and SLOs are only for large companies.
- Residual risk: backend artifacts prove evidence shape and route/gate coverage, not that a human owner has judged runtime tests, SLOs, health checks, rollback plans, operational runbooks or provider contracts sufficient for a real production system.

## API Integrations Evals

- `api_integrations_contract_present`: implemented in `T9-D8`.
- Required evidence: source-of-truth contract, consumer map, compatibility/breaking-change review, security schemes/scopes/token claims/object-level authorization/rate limits, error contract, contract-test matrix, event/webhook delivery contract, generated SDK manifest, external-write approval, request ID, correlation ID, API observability, style choice and unsupported API claim rejection.
- False-positive protection: Swagger UI/rendered docs alone does not make an API contract source, API-only contract fixtures do not force Backend blockers, internal APIs can still have consumers, and GraphQL/gRPC/events are not universal defaults.
- Unsupported claims rejected: Swagger UI is source of truth, schema validation is contract testing, OAuth proves API security, GraphQL/gRPC/events are mandatory defaults and internal APIs have no consumers.
- Residual risk: API artifacts prove contract evidence shape and route/gate coverage, not that a human owner has judged every consumer, compatibility rule, authz rule, error semantic, event delivery policy, generated SDK release or external-write approval sufficient for a real production system.

## Database Data Evals

- `database_data_contract_present`: implemented in `T9-D9`.
- Required evidence: database inventory, database dictionary, schema source, migration plan, expand-contract rollout, transaction boundary, rollback feasibility, backup/restore evidence, data classification, data quality checks, producer/consumer data contract, lineage, query/index performance, retention/deletion policy, synthetic fixture policy, production access approval, constraints/integrity and unsupported database claim rejection.
- False-positive protection: schema-only files and local/demo database fixtures stay `present_unverified`; runtime pipeline and RAG ingestion signals stay `present_unverified` until owner-reviewed runtime, lineage or ingestion evidence exists.
- Approval boundary: DB introspection, production DB access, production data access, migration execution, destructive cleanup, backup restore and retention mutation remain `approval_required`.
- Unsupported claims rejected: ORM schema is database source of truth, migration applied means safe, down migration means rollback-safe, backups exist means restore-safe, manual SQL is enough, anonymized production data is safe by default and lineage can be reconstructed later.
- Residual risk: database artifacts prove evidence shape and route/gate coverage, not that a human owner has accepted migration safety, data quality, rollback, restore, lineage, privacy or production-access sufficiency for a real production system.

## LLM AI RAG Evals

- `llm_ai_rag_contract_present`: implemented through `T9-D10-M36`.
- Required evidence: AI behavior promise, baseline eval, eval rerun evidence, app-backed eval path, dataset governance, prompt contract, model decision record, structured output schema, tool/function/MCP contract, human approval boundary, RAG source inventory, retrieval config, grounding rubric, agent task packet, agent workflow trace, guardrail matrix, trace evidence packet, cost/latency budget and current-run evidence before AI/RAG quality claims.
- Tooling and migration depth: eval tooling selector records Promptfoo, OpenAI Evals, pytest/Jest app-backed evals, Ragas and LangSmith as conditional choices with selected/rejected/deferred runner rationale; model migration records snapshot or approved alias, prompt migration impact, compatibility checks, rollback, minimum threshold and sampling parameter rationale.
- RAG lifecycle and incident depth: RAG source/retrieval/dataset artifacts record deletion path, retention, source exclusion, stale-source pruning, privacy owner, vector store lifecycle, deletion propagation, deduplication and privacy review; failed eval, hallucination report, unsafe output, tool misuse or data exposure routes to an AI incident workflow with severity, mitigation, follow-up eval and Security/Privacy handoff.
- Discovery/report depth: AI behavior diff signals are limited to workspace and intent signals with no external branches or network dependency; methodology reports render evidence_required, approval_boundary, accepted_gap_option, residual_risk and safe_next_action with redaction.
- False-positive protection: docs-only AI mentions, generic context maps, generic tools, generic schemas, frontend `model/` folders, vector math and non-behavior prompt documentation do not force AI/RAG methodology blockers.
- Approval boundary: live model calls, external eval services, vector DB access, raw prompt/trace/customer-data review, tool writes, shell/money/data exposure and irreversible side effects remain approval-bound.
- Unsupported claims rejected: prompt inspection is enough, citations alone prove grounding, model upgrade automatically improves quality, schema presence proves tool safety and AI quality can be claimed without current eval evidence.
- Residual risk: AI/RAG artifacts prove evidence shape and route/gate coverage, not that a human owner has judged eval thresholds, prompts, model choice, grounding quality, tool permissions, guardrails or cost/latency budgets sufficient for a real production system.

## Security Privacy Compliance Evals

- `security_privacy_compliance_contract_present`: implemented in `T9-D11`.
- Required evidence: security-sensitive classification, threat surface, security risk review, ASVS/SSDF/SAMM mapping, ASVS level selection, API security scheme, authorization negative tests, secrets policy, data classification, redaction lifecycle, privacy impact record, external-write approval, abuse/rate-limit review, audit logging review, supply-chain review, SBOM/provenance decision, CI permissions, AI security review, compliance overlay taxonomy, vulnerability response workflow, explicit Codex Security scan status and security evidence before completion.
- False-positive protection: docs-only security articles, keyword-only compliance claims, package metadata, SBOM files and CI permission files stay `present_unverified` until owner-reviewed evidence exists; docs-only repositories do not become regulated automatically.
- Approval boundary: payment/billing, production data, secret rotation, policy changes, external security-system mutation, external writes, publish actions and Codex Security scans remain approval-bound or explicitly not requested.
- Unsupported claims rejected: security review after coding, no-secrets-in-code means safe, ASVS/OWASP proves compliance, SBOM once is enough, Codex Security scan is implied, OAuth proves API security and privacy compliance is universal.
- Residual risk: security/privacy/compliance artifacts prove evidence shape and route/gate coverage, not legal compliance, certification, or that a human security/privacy/compliance owner has accepted every residual risk for a real production system.

## Delivery Release Operations Evals

- `delivery_release_operations_contract_present`: implemented in `T9-D12`.
- Required evidence: release scope, version impact, changelog/release notes, artifact manifest, release evidence before completion, rollout strategy, rollback/recovery, environment approval boundary, external release approval, CI/CD governance, observability/SLO, operations runbook, incident response, post-release review, automation manual stability, release mode policy, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident/postmortem learning, observability/on-call tooling, release integrity security handoff and owner-reviewed release evidence sufficiency.
- False-positive protection: docs-only release notes, CI-only workflows, deployment manifests without execution, feature flags without owners, GitOps files without approval paths, mobile signing alone, DORA individual quota and release/observability tooling files without owner evidence stay insufficient for release-ready claims.
- Approval boundary: publish, tag, GitHub Release creation, artifact upload, deploy, PR creation, branch push, package registry mutation, marketplace/store submission, CI/CD environment mutation and active automation remain `approval_required`.
- Unsupported claims rejected: CI green means release ready, tests passed so release is ready, rollback is just revert, feature flags remove release risk, GitOps is automatically safe, generated changelog is enough for users, DORA metrics prove individual performance and repeatable automation is automatically safe.
- Residual risk: delivery/release/operations artifacts prove evidence shape and route/gate coverage, not that a human release, operations, security or product owner has accepted every release risk for a real production system.

## Cross Domain Synthesis Evals

- `cross_domain_synthesis_contract_present`: implemented through `T9-S-M14`.
- Required evidence: grouped recommendations, owner domains, consumer domains, source domains, merged gates, source artifact ledger, alias/deferred artifact decisions, semantic evidence sufficiency, owner-question dedupe, risk-aware safe next action and lifecycle skill consumption.
- Fixture evidence: `run_fixture_eval.py` exposes `cross_domain_synthesis_contract_present`, `semantic_evidence_sufficiency_contract_present`, `safe_next_action_risk_ordered`, `source_artifact_mapping_contract_present` and `cross_domain_false_positive_guards_present`.
- False-positive protection: small PII, complex non-production monorepo, internal CLI, docs-only release notes, CI-only workflows, tooling-only release files and backend FSD-like directories do not force unrelated heavy methodology gates without owner-reviewed evidence.
- Approval boundary: synthesized recommendations stay read-only/staged; detection alone remains `present_unverified` and does not authorize scaffolding, external writes, release actions, production access, security scans, automations or finish claims.
- Residual risk: synthesis artifacts prove packet shape, grouping and routing, not that a human owner has accepted every real-project overlap or evidence sufficiency decision.

## Completion Evidence Evals

- `evidence_before_completion`: implemented in `T8-A16`.
- Required evidence: ready claim, completed claim, fixed claim, works claim and release claim need current command evidence, current eval evidence, current runtime evidence or explicit test gap.
- Inspection-only: answers based only on code inspection must stay labeled `inspection-only` and list unsupported completion claim.
- Residual risk: the gate proves evidence is recorded, not that manually interpreted evidence is semantically sufficient.

## Domain Model Evals

- `domain_model_when_complex_domain`: implemented in `T8-A5`.
- `bounded_context_architecture_boundary_trace`: implemented in `T8-A6`.
- `ubiquitous_language_traceability`: implemented in `T8-A7`.
- Human domain/architecture review remains required for conceptual correctness.

## UI Architecture Evals

- `fsd_structure`: implemented in `T8-A8`.
- False-positive protection: backend, native, simple CRUD and simple MVP work must not be forced into Feature-Sliced Design.
- Residual risk: directory detection does not prove architecture quality; owner review is still required for public API and import rule correctness.

## Metric Hardening Evals

- `metric_hardening_when_product_behavior_changes`: implemented in `T8-A9`.
- Required evidence: North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence.
- Residual risk: metric artifacts reduce proxy-metric and telemetry risk, but a product owner still needs to validate whether the selected metric actually reflects user value.

## Docs Tooling Evals

- `docs_tooling_selector`: implemented in `T8-C`.
- `docs_as_code_impact`: supports `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: selected tools, rejected tools, evidence owner, maintenance owner, commands, accepted gap or approval boundary.
- False-positive protection: docs-light and internal-only projects are not forced into MkDocs, Docusaurus, Sphinx, Antora, hosted docs, CI activation or DB introspection.
- Residual risk: selector evidence is route and artifact evidence; owners still need to validate whether a chosen docs tool is operationally worth maintaining.

## Conditional Readiness Evals

- `conditional_readiness_gates_contract_present`: implemented in `T8-F`.
- `readiness_statuses`: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required`.
- Required evidence: every gate has `applies_when`, pass condition, accepted gap, required evidence, owner and residual risk.
- False-positive protection: detection alone can only support `present_unverified`; applicable gates without evidence are `applicable_missing`, not ready.
- Residual risk: the contract proves readiness evidence is structured; owners still need to judge whether the evidence is sufficient for the actual project risk.

## Scenario Documentation Evals

- `test_product_agent_os_docs`: implemented in `T8-H`.
- Required evidence: dedicated scenario, behavioral eval and Codex compatibility pages have Source status, Inputs, Outputs, Verification and Risks.
- Navigation evidence: MkDocs nav and `tools/check_docs.py` required paths include the new pages.
- Residual risk: docs describe route and eval contracts; transcript/session replay catches deterministic term/shortcut/privacy failures but does not replace semantic reviewer judgment.

## Transcript Session Evals

- `evaluate_transcript_sessions`: implemented in `T8-GY`.
- Required evidence: each synthetic or redacted session maps to `behavioral_case`, has `expected_terms`, optional `forbidden_terms`, and produces `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`.
- Runner evidence: `run_transcript_eval.py` exits `0` only when every session passes and exits `1` when expected evidence is missing, forbidden behavior appears or unsafe transcript content is retained.
- Residual risk: deterministic replay is stable and local, but it is not a calibrated LLM-as-judge for nuanced conversation quality.

## Standards Trigger Evals

- `standards_trigger_policy`: implemented in `T8-B`.
- Required evidence: ADR trigger policy, C4/arc42 applicability, OpenAPI source of truth, AsyncAPI event contract, SemVer impact, Keep a Changelog categories, CODEOWNERS status, GitHub Actions least privilege, `governance-proposal.md` and no forced external activation.
- Fixture evidence: `standards_trigger_contract_present` in `run_fixture_eval.py`.
- Residual risk: the contract proves standards applicability is recorded; owners still need to decide whether an ADR, diagram, governance proposal or release category is proportionate for the real project.

## False-Positive Fixture Evals

- `T8-GX`: implemented.
- Required evidence: `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal` and `hosted-docs-approval` are synthetic, secret-free fixtures with named expected checks in `run_fixture_eval.py`.
- Fixture evidence: `fsd_structure_not_detected_for_backend`, `fsd_structure_not_detected_for_native`, `domain_model_not_forced_for_simple_crud`, `docs_light_does_not_select_heavy_portal` and `hosted_docs_and_db_introspection_require_approval`.
- Residual risk: false-positive fixtures prove routing boundaries for selected synthetic workspaces; they do not prove every real project-specific methodology decision.

## Detailed Discovery Status Evals

- `T8-D`: implemented.
- Required evidence: `methodology_applicability` is present in discovery output with packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision and standards trigger policy.
- Fixture evidence: `methodology_applicability_contract_present` in `run_fixture_eval.py`.
- Residual risk: discovery packets structure methodology/tooling applicability; owners still need to validate semantic quality and sufficiency of the evidence for the real project.

## Unsupported Claims

- Claim:
- Missing source:
- Verification needed:
<!-- product-agent-os:end evals -->
