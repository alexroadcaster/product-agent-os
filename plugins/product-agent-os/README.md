# Product-Agent OS

## Task 22 final documentation sync closure

Task 22 final documentation sync closure defines this package as the Product-Agent OS full stack for Track 1-9: plugin manifest, lifecycle skills, staged renderer, approved merge tooling, Codex-only runtime runner, engineering standards, scenario workflows, behavioral evals and methodology intelligence. It preserves schema v1 additive compatibility for runtime packets and keeps every staged artifact boundary explicit.

The package does not activate external systems by itself. Generated files, hooks, MCP usage, automations, release actions, DB access and hosted docs remain staged or approval_required until a project owner approves them and current evidence exists.

Product-Agent OS is a local Codex plugin for turning a real project workspace into a governed product delivery loop. It packages lifecycle skills, project infrastructure templates, safe merge tooling, fixture evals, and a Codex-only runtime contract runner.

The plugin is designed for Codex App, CLI, and IDE extension workflows. It does not require a separate OpenAI API key and does not run as a standalone Agents SDK app.

Task 25 Batch 19 `T10-CG-V2-M33..M38` implements the approved offline static search index at `.codex/product-agent-os/project-code-graph-search-index.json`. The index is generated, cache-bound and not source of truth; it builds from graph artifact only, supports optional indexed search, blocks stale indexes, records cache hit/miss/invalidation and has a rollback/disable path. Batch 19 uses no live database/server, LLM, embedding or cross-encoder.

Task 25 Batch 20 `T10-CG-V2-M39..M44` implements the approved local query backend gate in `project_graph_backend.py`. The gate creates a generated local file-store at `.codex/product-agent-os/project-code-graph-backend.json` only from graph and static-index artifacts, records `project_graph_local_backend_gate_present`, requires an approval decision packet with storage path, port policy, process lifecycle, auth boundary, cleanup, logging, performance threshold and rollback path, and keeps server mode disabled by default. The backend store is not source of truth, no production server is started, read-only API handling is contract-only, graph-only fallback remains available, and Batch 21-23 remain future-gated.

Track 6 adds an engineering standards layer: product hypothesis, architecture boundary, test-first or eval-first verification, docs-as-code impact, human review, release measurement, and learning loop. Track 7 hardens that layer with discovery signals, readiness methodology gates, and concrete artifact templates for architecture, domain modeling, metrics, API contracts, UI components, and database documentation. Track 8 adds first-run intake plus scenario workflows for bug rescue, greenfield idea shaping, complex system acceleration, scenario handoffs, PR review readiness, legacy onboarding, API migration, AI/RAG eval regression, native/mobile feature work, desktop local-first work, data migration, security-sensitive change, CI stabilization, and release packaging. It also hardens methodology gates for no-placeholder planning, two-stage review, fresh-context handoff, acceptance scenarios, conditional DDD domain modeling, bounded-context-to-architecture traceability, ubiquitous language traceability, conditional FSD structure routing, metric hardening for product behavior changes, evidence-before-completion for ready/completed/fixed/works/release claims, docs tooling selection for docs-as-code impact, conditional readiness statuses, standards trigger policy for ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions, and detailed discovery status packets through `methodology_applicability`. Track 9 starts a methodology intelligence layer with a machine-readable catalog for 12 methodology domains before audit, report, and staged artifact behavior are added; Business/Product, Requirements/Domain, Solution Architecture, Quality/Testing/Evals, Codex/Agentic Workflow, Frontend, Backend, API & Integrations, Database & Data, LLM / AI / RAG, Security, Privacy & Compliance, and Delivery, Release & Operations through `T9-D12` are now covered with fixture eval contracts including `backend_contract_present`, `api_integrations_contract_present`, `database_data_contract_present`, `llm_ai_rag_contract_present`, `security_privacy_compliance_contract_present`, `delivery_release_operations_contract_present`, `api_contract_source_present`, `external_write_approval_present`, runtime/failure/observability/security/rollback evidence, API contract/consumer/compatibility/security/error/event/SDK evidence, database inventory/migration/data-contract/production-approval evidence, AI behavior/prompt/model/tool/RAG eval evidence, security/privacy/compliance threat/data/supply-chain evidence, delivery release/artifact/rollout/rollback/operations/automation evidence and owner reviewed test/eval/runtime evidence sufficiency. This is packaged as templates and workflow packets, not as silent external automation.

API & Integrations methodology adds conditional `api_integrations` routing for OpenAPI, AsyncAPI, GraphQL, gRPC/protobuf, JSON Schema, Pact, webhooks/events, generated SDKs, external providers and public/internal consumers. It stages `api-inventory.md`, `api-consumer-map.md`, `api-compatibility-record.md`, `api-contract-test-matrix.md`, `api-error-catalog.md`, `api-auth-authorization-matrix.md`, `generated-sdk-manifest.md`, `webhook-event-contract.md`, `external-integration-approval.md` and `api-style-guide.md`; Swagger UI is not source of truth and external writes remain approval-bound.

Database & Data methodology adds conditional `database_data` routing and `database_data_signals` for schema, migration, ORM, warehouse, data quality, lineage, retention, backup/restore and production-data surfaces. The fixture eval contract `database_data_contract_present` covers `database_migration_plan_present`, `database_production_access_approval_present`, inventory, dictionary, data contract, rollback/backup evidence, classification, quality checks, lineage, query performance, retention/deletion and synthetic fixture policy. Schema-only artifacts are not safety proof, schema-diff tooling remains deferred, and production DB/data access or migration execution remains approval-bound.

LLM / AI / RAG methodology adds conditional `llm_ai_rag` routing for user-visible AI behavior, prompts, models, structured outputs, tool/function/MCP calls, RAG sources, retrieval, grounding, datasets, agent traces, guardrails and cost/latency budgets. The fixture eval contract `llm_ai_rag_contract_present` covers `ai-behavior-spec.md`, `prompt-contract.md`, `model-decision-record.md`, `eval-run-report.md`, `ai-dataset-manifest.md`, `structured-output-schema.md`, `ai-tool-contract.md`, `rag-source-inventory.md`, `rag-retrieval-config.md`, `rag-eval-report.md`, `grounding-rubric.md`, `agent-task-packet.md`, `agent-workflow-map.md`, `guardrail-matrix.md`, `trace-evidence-packet.md` and `ai-cost-latency-budget.md`. It also covers eval tooling selector/deferred runner policy, model migration thresholds, RAG lifecycle/privacy, workspace/intent-only diff-signal policy, AI incident workflow and methodology report rendering of evidence, approvals, accepted gaps and residual risks. Prompt inspection is not enough, citations alone do not prove grounding, model upgrades do not imply quality, and live model calls, external eval systems, vector DB access and tool writes remain approval-bound.

Security, Privacy & Compliance methodology adds conditional `security_privacy_compliance` routing for authn/authz, permissions, secrets, PII, sensitive data, payment/billing, abuse controls, rate limits, audit logging, supply chain, SBOM/provenance, CI permissions, AI/tool security, external writes, production data and compliance overlays. The fixture eval contract `security_privacy_compliance_contract_present` covers `security-risk-review.md`, `threat-surface.md`, `asvs-ssdf-mapping.md`, `authz-negative-test-matrix.md`, `secrets-policy.md`, `data-classification-register.md`, `privacy-impact-record.md`, `api-security-review.md`, `abuse-rate-limit-plan.md`, `supply-chain-review.md`, `sbom-manifest.md`, `ci-permissions-review.md`, `audit-logging-review.md`, `ai-security-review.md`, `compliance-overlay.md`, `vulnerability-response-record.md` and `approval-record.md`. It records Codex Security scan status as explicit `requested`, `not requested` or accepted gap evidence, not as an implied scan. Compliance overlays record applicability, owner, evidence, non-goals, gaps and review cadence without claiming legal compliance or certification; payment/billing, production data, secret rotation, policy changes, external security-system mutations and external writes remain `approval_required`.

Delivery, Release & Operations methodology adds conditional `delivery_release_operations` routing for release/deploy/publish/package/operations work. The fixture eval contract `delivery_release_operations_contract_present` covers `versioning-policy.md`, `release-readiness.md`, `release-artifact-manifest.md`, `rollout-plan.md`, `rollback-recovery-plan.md`, `environment-matrix.md`, `deployment-plan.md`, `ci-cd-workflow-inventory.md`, `observability-map.md`, `slo-spec.md`, `operations-runbook.md`, `incident-record.md`, `postmortem.md`, `post-release-review.md`, `approval-record.md` and `automation-candidate.md`. Final delivery gates include `release_mode_policy_present`, build-release-run boundary, platform distribution evidence, release communication, versioning tooling decision, GitHub environment controls, DORA measurement design, incident postmortem learning, observability/on-call tooling, release integrity security handoff and `release_evidence_sufficiency_owner_reviewed`. Release evidence stays planning-first: publish, tag, release creation, upload, deploy, package registry mutation, marketplace/store submission, CI/CD environment mutation and active automation remain `approval_required`. Automation promotion requires `automation_manual_stability_present`: manual success evidence, stable inputs/outputs, owner, verification, approval requirements, value evidence and rollback/disable path.

Backend methodology remains covered by `backend_contract_present`, `backend_service_boundary_present`, runtime/failure/observability/security/rollback evidence and owner reviewed test/eval/runtime evidence sufficiency.

Track 8 operator docs are split into scenario routing, behavioral evals, and Codex compatibility pages in `docs/product-agent-os/`. They document first response, minimum artifacts, approval boundaries, expected and forbidden behavior, fixture eval coverage, transcript/session replay, and Codex App/CLI/IDE extension package scope.

Track 10 `Task 23` adds Guided question protocol and a status snapshot/dashboard view. Guided question protocol asks one blocking question maximum, keeps optional questions in the packet, and routes answers into artifacts or accepted gaps without treating questions as workspace evidence. The status snapshot feeds `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json`; the dashboard is generated view only over underlying artifacts, has no external assets, and cannot support success claims from stale evidence.

Task 24 Self-Verification And Modernization Loop adds a self-verification metrics loop for Product-Agent OS agents, skills, prompt/policy packs, router/tool policies and harness versions. The `agent_skill_metrics_loop` route emits staged evidence only: target registry, trace/dataset/grader summaries, scorecard ledger, report packet and modernization candidates. It performs no live eval/model/API calls, creates no active schedules, applies no candidates by itself and allows no self-applied updates.

Task 25 Project Code Graph And HTML Cockpit Visualization now includes Task 25 Batch 13, Batch 14, Batch 15 and Batch 16 as the prior graph/cockpit baseline, plus Task 25 Batch 17 as a read-only eval/future-gate layer. Task 25 Batch 18 `T10-CG-V2-M31..M32` closes the baseline with focused/full verification: full unittest ran 664 tests with `OK`, fixture eval exited `0` for 91 fixture directories, transcript eval exited `0` with 17 sessions and 0 failures, Codex compatibility returned `status: compatible`, strict MkDocs and diff hygiene passed, and the explicit-only git boundary was preserved. The scanner emits redacted graph JSON/JSONL with stable file nodes, Python AST package/module/class/function/method overlays, conservative import/call/test edges, structured Markdown/OpenAPI/AsyncAPI/DBML/SQL/JSON/YAML/Mermaid/PlantUML overlays, partition scopes, canonical aliases, manifest freshness/provenance and observation lineage. Query mode reads existing graph artifacts and emits bounded `neighbors`, `path`, `trace`, `impact`, `affected_tests`, `changed_since`, `why_changed`, `read_order`, `hotspots`, `node`, `status` and `search` packets without source reads. Runtime/status summaries and graph analysis reports are orientation evidence only. The generated cockpit renderer stages offline `.codex/product-agent-os/project-cockpit.html` and `.codex/product-agent-os/project-cockpit.json` review surfaces with exactly eight top-level pages, Code Flow inside `Code Intelligence`, Graphology-compatible static projection, local Graphology/Sigma vendor boundary, filters, selected-node evidence, fallback table, mobile CSS and no external assets. Batch 17 adds fixture structural fields, a local search-quality eval loop for symbol recall, top-k/MRR, trace labels, affected-test precision, edge density and explicit thresholds, plus future backend and semantic gates. Batch 19 adds the generated offline static search index as a cache, not as source of truth. Batch 20 adds a generated local file-store backend gate as an approved, disabled-by-default orientation cache with read-only contract API and graph-only fallback. Generated cockpit HTML/JSON and backend/index caches are not source of truth. Live production server, LLM, embedding, cross-encoder, semantic extraction and rationale/comment extraction remain future-gated outside the approved Batch 19-20 surfaces without explicit approval that defines redaction, cache, token budget, eval threshold and rollback path.

Official references:

- [Codex plugins](https://developers.openai.com/codex/plugins)
- [Build plugins](https://developers.openai.com/codex/plugins/build)
- [Agent Skills](https://developers.openai.com/codex/skills)
- [Subagents](https://developers.openai.com/codex/subagents)
- [Codex MCP](https://developers.openai.com/codex/mcp)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [Context7 MCP clients](https://context7.com/docs/resources/all-clients)

## What Problem It Solves

Codex can implement large tasks, but real product work fails when the operating context lives only in chat. Product-Agent OS moves durable state into explicit artifacts:

| Problem | Product-Agent OS behavior |
| --- | --- |
| Requirements are implicit or lost between sessions | Create or update `REQUIREMENTS.md` with scope, non-goals, constraints, and acceptance criteria |
| Implementation starts before planning | Route to `PLAN.md` before build work |
| Subagents edit overlapping files | Create role and ownership boundaries before parallel work |
| Tests are guessed after the fact | Define deterministic checks in `TEST.md` and subjective gates in `EVALS.md` |
| Reviews lack evidence | Require commands, reports, risks, and handoff data in `RUNLOG.md` |
| Hooks and automations are activated too early | Keep hooks staged and automations candidate-only until explicitly approved |
| Existing project files might be overwritten | Stage proposals first and preserve user-authored content outside managed sections |

## Current Capabilities

### Lifecycle Skills

The plugin bundles these skills under `skills/`:

| Skill | Role |
| --- | --- |
| `project-lifecycle-orchestrator` | Determine lifecycle state and next action |
| `workspace-discovery-auditor` | Inspect a workspace without writing |
| `requirements-author` | Draft or refine requirements |
| `implementation-planner` | Produce an executable implementation plan |
| `agent-team-designer` | Define project-scoped agent roles and handoff boundaries |
| `test-eval-designer` | Define tests, evals, and quality gates |
| `risk-reviewer` | Review risk, unsupported claims, and missing verification |
| `docs-maintainer` | Align requirement IDs, source registry, glossary, and traceability docs |
| `pr-release-operator` | Prepare PR or release packets |
| `learning-loop-maintainer` | Capture lessons, failures, and durable rules |
| `automation-promoter` | Produce candidate-only automation readiness packets |

Codex loads skills through progressive disclosure: it sees each skill's name and description first, then loads the full `SKILL.md` only when the task matches or the user invokes it.

### Usage Mode and Behavioral Evals

Workspace discovery returns a `usage_mode` packet with `primary`, `secondary`, `confidence`, routing reasons, fallback, first-response contract, minimum artifacts, and behavioral eval cases. Supported classifier modes include greenfield idea, bug rescue, complex system acceleration, PR review, legacy onboarding, API migration, AI/RAG eval regression, native mobile feature, desktop local-first, data migration, security-sensitive change, CI stabilization, release packaging, docs-only, standard feature work, and maintenance. First-run intake distinguishes empty workspace, failed verification, existing control-plane, and complex system starts before any broad methodology dump. Discovery also returns `route_inputs` so prompt-like intent hints, workspace signals, and current control-plane state stay separate. The Codex runtime runner can accept `--intent-hint`, but source policy, approval and write guards still win over routing intent. Greenfield idea mode requires selected direction, first vertical slice, lightweight-mode option, and approval before scaffold. Complex system acceleration requires an integration catalog, ownership split, release gates, and no parallel work with overlapping files or unclear external-system ownership. PR review mode requires PR review readiness, a changed files map, two-stage review, missing checks, and no external writes, PR creation, push, or publish action without explicit approval. Legacy onboarding requires a source map, entry points, run commands, docs debt, verification status, and `present_unverified` labels before refactor. API migration mode requires a migration plan, API contract review, OpenAPI/AsyncAPI sources, consumers, generated clients, backwards compatibility, deprecation, rollout, release impact, owner review, and contract check evidence before implementation or release. AI/RAG eval regression mode requires an AI eval spec, baseline result, no-secrets dataset policy, prompt/context and retrieval metrics, judge rubric, thresholds, latency/cost/grounding evidence, failure examples, and rerun command before model, prompt, retrieval, dataset, rubric, or threshold changes and before quality claims. Native/mobile mode requires platform assumptions, iOS/Android scope, permissions, offline state, simulator/emulator or device plan, build command, logs, screenshots, runtime evidence, manual device gap, and approval before permission, signing, or store changes. Desktop local-first mode requires desktop platform assumptions, filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, runtime log check, build command, recovery path, rollback, runtime evidence, manual OS gap, and approval before filesystem access, local data, packaging, signing, or distribution changes. Data migration mode requires a migration plan, database dictionary, schema change, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, owner review, production DB boundary, and approval before production data access, production DB access, or migration execution. Security-sensitive mode requires a security risk review, threat surface, authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval boundary, and explicit Codex Security usage only when requested. CI stabilization mode requires a CI stabilization report, failure evidence, failing job, command, logs, environment, deterministic/flaky classification, isolation plan, local reproduction, rerun evidence, remote CI/GitHub Actions boundary, and approval before remote CI reruns, CI settings changes, or CI health claims. Release packaging mode requires release readiness, package metadata, version/SemVer impact, changelog, build/test/docs evidence, security and license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback, and residual risk before publishing, tagging, release creation, artifact upload, or package registry mutation. Bug rescue also returns `bug_reproduction_signals` so candidate logs are treated as possible evidence, not verified truth.

The Codex runtime runner carries that packet in its route result so the first response can stay small: mode, confidence, next smallest action, minimum artifacts, approval boundary, evidence gaps, `next_blocking_question`, `question_counts`, and `question_summary`. The bundled `behavioral-workflows.json` eval template captures route selection, first-run empty/broken/existing/complex entry cases, shortcut resistance, no scaffold before approval, lightweight greenfield mode, ownership-first complex acceleration, no over-parallelization, scenario handoff completeness, PR review readiness, legacy onboarding map, AI eval regression planning, native/mobile runtime planning, desktop local runtime planning, data migration planning, security-sensitive planning, CI stabilization planning, release packaging readiness, root-cause bug rescue, no broad rewrite before root cause, no fix claim without reproduction, guided-question-smallest-blocking-question, guided-question-no-broad-methodology-interview, status-dashboard-generated-view-only, status-dashboard-stale-evidence-no-success-claim, runtime-first-response-no-question-dump, acceptance scenario traceability, no-placeholder planning, two-stage review, fresh-context handoff, evidence-before-completion, finish options, and Codex-only compatibility.

`run_transcript_eval.py` adds deterministic transcript/session replay for synthetic or redacted session fixtures. The packaged `product-agent-os-synthetic-sessions.json` fixture maps each session to a `behavioral_case`, checks `expected_terms`, blocks `forbidden_terms`, reports `missing_expected_terms`, `forbidden_terms_present` and `privacy_errors`, and runs without external systems or model calls.

No-placeholder planning is now a hard planning gate: `implementation-planner`, `PLAN.md`, `build-slice.md`, `plan-quality-check.md`, behavioral evals, and fixture evals require exact files, owned/forbidden files, exact commands, expected outputs, rollback, evidence owner and placeholder scan before non-trivial build work. Small docs, formatting, or config edits can use a `mechanical_change` exception only when the reason and reduced evidence path are explicit.

Generalized two-stage review is now a hard review gate for risky slices: PR review, public contract changes, migration, security-sensitive work, data migration, release packaging, parallel work, and external-system changes must record `stage 1: spec compliance` before `stage 2: quality/risk`. `risk-reviewer`, `review-slice.md`, `RUNLOG.md`, `pr-risk-review.md`, and `behavioral-workflows.json` block generic review only, reversed stage order, and ready verdicts with missing evidence.

Fresh-context handoff is now a hard team gate for subagents and parallel workers: `agent-team-designer`, `handoff-contract.md`, `agent-task-packet.md`, `worktree-ownership.md`, and `behavioral-workflows.json` require complete task context, source constraints, allowed sources, inputs used, owned files, forbidden files, expected evidence, handoff output schema, stop conditions, and sequential fallback before parallel work. Raw conversation history is not a valid worker context.

Acceptance scenarios are now a hard ATDD/BDD gate for behavior changes: `requirements-author`, `implementation-planner`, `test-eval-designer`, `REQUIREMENTS.md`, `TEST.md`, `EVALS.md`, `development-standards.md`, `project-readiness.json`, `behavioral-workflows.json`, and `acceptance-scenarios.md` require `requirement -> scenario -> check -> evidence owner`, Given/When/Then or an equivalent behavior format, business rule, edge case, non-goal, explicit gap handling, and proof that BDD does not replace unit, integration, contract tests, or evals.

Requirements & Domain methodology now extends acceptance and conditional DDD gates with `requirements_domain`: `requirement-registry.md`, `stakeholder-owner-map.md`, `story-slice-map.md`, `requirements-traceability-matrix.md`, `business-rules.md`, `example-map.md`, `requirement-change-impact.md`, and `domain-review-record.md` cover requirement quality, stable IDs, owner review, story slicing, business rules, constraints, domain events, API/UI/data traceability, change impact, accepted gaps, and unsupported-claim rejection. `docs-maintainer` keeps requirement IDs, source registry, glossary/ubiquitous language and traceability docs aligned after the requirements packet exists.

Conditional DDD domain modeling is now a hard gate only when it applies: `discovery.py`, `domain-modeling.md`, `architecture-overview.md`, `project-readiness.json`, `implementation-planner`, and fixture eval require `domain_model_when_complex_domain` for complex backend, workflow, enterprise, data-heavy, multi-service, or multi-context work, `bounded_context_architecture_boundary_trace` from every bounded context to an architecture boundary or accepted gap, and `ubiquitous_language_traceability` from each domain term to a requirement/source plus API/event/contract, UI label, code module or owner. Simple CRUD and simple MVP work can record DDD as not applicable or an accepted gap instead of being forced into domain ceremony.

Conditional FSD structure routing is now available only when it applies: `discovery.py` detects optional `fsd_structure` for web UI work with Feature-Sliced Design layer directories, `component-card.md` records layer, slice, segment, public API and import rule, and `implementation-planner` stops before build when applicable UI boundaries are missing. Backend, native, simple CRUD and simple MVP work record FSD as not applicable or accepted gap instead of being forced into UI architecture ceremony.

Metric hardening is now a product/data gate for behavior changes: `metric-spec.md`, `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, and fixture eval require `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence before product success claims. A single proxy metric is not enough evidence for success.

Evidence-before-completion is now a general verification gate, not only a release-packaging concern: `release-packet.md`, `development-standards.md`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, behavioral evals, and fixture eval require `evidence_before_completion` before ready claim, completed claim, fixed claim, works claim, or release claim. Completion language needs current command evidence, current eval evidence, current runtime evidence, owner evidence, or explicit test gap; inspection-only answers must stay labeled and list unsupported completion claims.

Codex / Agentic Workflow methodology is now a governance gate for Product-Agent OS itself: `codex_agentic_workflow`, generated `AGENTS.md`, `.codex/config.toml`, `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, `behavioral-workflows.json`, lifecycle skills, `agent-task-packet.md`, `worktree-ownership.md`, `automation-candidate.md`, and `handoff-contract.md` require source-of-truth boundaries, read-only discovery, approval boundaries, model/reasoning policy, memory as recall only, fresh-context handoff, ownership split, subagent parallelism safety, MCP permission review, hook activation approval, skill promotion evidence, plugin boundary, automation manual stability, agent eval workflow and evidence before completion. It also records the runtime routing distinction between Codex App, IDE extension, CLI, `codex exec`, GitHub Action, MCP, Agents SDK and automation without silently activating external capabilities.

Frontend methodology is now a UI evidence gate: `frontend`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, `behavioral-workflows.json`, lifecycle skills, `component-card.md`, `frontend-flow-spec.md`, `frontend-state-matrix.md`, `frontend-visual-qa.md`, `frontend-accessibility-review.md`, and `frontend-performance-budget.md` require user-flow acceptance, component state coverage, design-system ownership, conditional Storybook/FSD routing, API/data state alignment, WCAG 2.2 AA target or accepted exception, keyboard/focus evidence, responsive and visual evidence, browser/runtime evidence, console status, Playwright trace or accepted gap, interaction evidence, performance budgets and privacy-safe screenshots/stories/mocks before UI completion claims.

Docs tooling selection is now a conditional docs-as-code gate: `docs-tooling-decision.md`, `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, discovery, and fixture eval require `docs_tooling_selector` and `docs_as_code_impact` statuses. It routes MkDocs, Docusaurus, Sphinx, Antora, Read the Docs, Storybook, OpenAPI/AsyncAPI, DBML/dbdocs, SchemaSpy, TypeDoc/JSDoc/Javadoc/XML docs, Vale, markdownlint, Mermaid, PlantUML, and Structurizr DSL where detected, while docs-light/internal-only work can be `not_applicable` and hosted docs or DB introspection stay `approval_required`.

Conditional readiness gates are now explicit in `project-readiness.json`, generated control-plane templates, lifecycle skills, and fixture eval. `readiness_statuses` are `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, and `approval_required`. Every gate records applicability, required evidence, owner, accepted gap, and residual risk; detection alone can only produce `present_unverified`.

Discovery now exposes top-level `methodology_applicability` status packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision, and standards trigger policy. Each packet carries status, applicability reason, observed evidence, required evidence, owner, and residual risk so routing can distinguish missing evidence, unverified evidence, proposal-staged work, accepted gaps, approval boundaries, and not-applicable gates.

T8-GX fixture hardening adds false-positive and approval-bound scenario fixtures: backend folders do not imply Feature-Sliced Design, native/mobile folders do not imply Feature-Sliced Design, simple CRUD `src/domain/*` folders do not imply DDD, docs-light work does not force a heavy docs portal, and hosted docs plus DB introspection remain approval-required.

Current Track 8 coverage status:

| Coverage | Modes |
| --- | --- |
| `done` workflow + artifact + eval coverage | `bug_rescue`, `greenfield_idea`, `complex_system_acceleration`, `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging` |
| `done` routing core | `usage_mode` classifier, `route_inputs`, first-response contract, first-run intake hardening, Codex-only compatibility |
| `done` methodology gate | no-placeholder planning with `plan_quality_check`, exact files, owned/forbidden files, exact commands, expected outputs, rollback, evidence owner, placeholder scan, plan repair and `mechanical_change` exception; generalized two-stage review with spec compliance before quality/risk for risky/public-contract/migration/security/data/release/parallel slices; fresh-context handoff for subagents and parallel workers; acceptance scenarios with ATDD/BDD traceability before behavior changes; conditional DDD domain modeling with `domain_model_when_complex_domain` for complex backend/workflow/enterprise/data-heavy/multi-service/multi-context work; bounded-context-to-architecture traceability with `bounded_context_architecture_boundary_trace`; ubiquitous language traceability with `ubiquitous_language_traceability`; conditional Feature-Sliced Design routing with optional `fsd_structure` for applicable web UI work; metric hardening with `metric_hardening_when_product_behavior_changes` for product behavior changes; evidence-before-completion with `evidence_before_completion` for ready/completed/fixed/works/release claims; docs tooling selection with `docs_tooling_selector` and `docs_as_code_impact` statuses; conditional readiness gates with `readiness_statuses`, applicability, evidence, owner and residual risk; detailed discovery status packets with `methodology_applicability`; standards trigger policy with `standards_trigger_policy`, `governance-proposal.md`, ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions applicability and no forced external activation |
| `done` fixture hardening | false-positive and approval-bound fixtures for backend/native FSD routing, simple CRUD DDD routing, docs-light no-portal routing, and hosted docs/DB introspection approval boundaries |

### Staged Infrastructure Renderer

The renderer can propose a project control plane:

```text
AGENTS.md
REQUIREMENTS.md
PLAN.md
TEST.md
EVALS.md
RUNLOG.md
.codex/config.toml
.codex/agents/*.toml
.codex/hooks/*
.codex/workflows/*.md
.codex/evals/*.json
.codex/pr/*
.codex/automation-candidates/automation-candidate.md
```

The workflow inventory includes:

- `development-standards.md` for hypothesis -> architecture -> tests/evals -> implementation -> review -> measurement.
- `documentation-system.md` for architecture docs, API contracts, UI component docs, code reference, database docs, and release docs.
- `first-run-intake.md` for mode, confidence, next smallest action, minimum artifacts, approval boundary, and evidence gaps on first launch across empty, broken, existing control-plane, and complex system starts.
- `bug-rescue.md` for evidence-first debugging when a project is stuck in broken behavior.
- `greenfield-idea-to-plan.md` for empty-folder or idea-stage projects before scaffold.
- `complex-system-acceleration.md` for web/API/integration-heavy systems before parallel work.
- `pr-review-readiness.md` for changed-file review before merge, with spec compliance before quality/risk review and no external action without approval.
- `legacy-onboarding.md` for old or undocumented repositories before refactor, with source map, run commands, docs debt, and `present_unverified` status.
- `api-migration.md` for HTTP API and event contract migrations before implementation or release.
- `ai-eval-regression.md` for AI/RAG quality regressions before model, prompt, retrieval, dataset, rubric, or threshold changes.
- `native-mobile-feature.md` for iOS/Android/native mobile changes before permission, signing, store, or runtime behavior claims.
- `desktop-local-first.md` for desktop/local-first changes before filesystem access, local data, packaging, signing, distribution, or runtime behavior claims.
- `data-migration.md` for schema, backfill, retention, and sensitive-data migrations before production DB access or migration execution.
- `security-sensitive-change.md` for authn, authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, rollback, approval, and explicit Codex Security boundaries.
- `ci-stabilization.md` for failing or flaky CI before remote CI reruns, CI settings changes, broad fixes, or CI health claims.
- `release-packaging.md` for package, SDK, plugin, app, mobile, desktop, or open-source release readiness before publishing, tagging, release creation, artifact upload, or package registry mutation.
- `.codex/artifact-templates/*.md` for ADR, architecture overview, domain modeling, docs tooling decisions, metric specs, API contract review, API inventory, API consumer maps, API compatibility records, API contract test matrices, generated SDK manifests, webhook/event contracts, external integration approvals, migration plans, AI eval specs, component cards, database inventories, database dictionaries, database migration plans, database data contracts, database production access approvals, integration catalogs, onboarding maps, PR risk reviews, security risk reviews, threat surfaces, ASVS/SSDF mappings, authorization negative tests, secrets policies, data classification registers, privacy impact records, supply-chain reviews, SBOM manifests, CI permissions reviews, audit logging reviews, AI security reviews, compliance overlays, vulnerability response records, approval records, CI stabilization reports, release readiness, acceptance scenarios, behavioral eval cases, task packets with scenario handoffs, plan quality checks, greenfield idea briefs, bug rescue reports, model/reasoning policies, MCP permission reviews, hook governance records, skill promotion records, agent eval workflows, and Codex compatibility reports.
- `.codex/artifact-templates/governance-proposal.md` for CODEOWNERS status, GitHub Actions least privilege proposals, workflow names, commands, permissions, triggers, owners and no forced external activation.

It is staged-first by design:

1. Inspect target workspace.
2. Render proposed artifacts to a separate stage directory.
3. Write `product-agent-os-stage-manifest.json`.
4. Build a read-only merge plan.
5. Require an explicit approval record before target workspace writes.
6. Write a rollback manifest after approved apply.

Existing files are preserved unless they contain Product-Agent OS managed sections:

```markdown
<!-- product-agent-os:start section-id -->
...
<!-- product-agent-os:end section-id -->
```

### Safe Merge and Rollback

`merge_infrastructure.py` protects the target workspace by validating:

- stage manifest shape and digests;
- workspace binding;
- stale workspace state;
- path traversal;
- symlink escapes;
- parent/child target conflicts;
- approved targets and actions;
- hook activation metadata when hooks are explicitly enabled.

An approved apply writes `product-agent-os-rollback-manifest.json` into the stage directory. Rollback refuses to proceed if target files changed after apply.

### Codex Runtime Runner

Track 5 adds a Codex-only runner:

```powershell
python scripts\run_codex_runtime_runner.py <workspace> --contract
```

The runner does not call a model. It reads workspace artifacts, infers lifecycle state, plans the next route, validates source and approval boundaries, redacts sensitive output, and returns a deterministic result contract.

Possible statuses:

| Status | Meaning |
| --- | --- |
| `route_ready` | A next skill/subagent route is available |
| `needs_context` | Required control-plane context is missing |
| `needs_approval` | Route requires explicit approval before writes |
| `blocked` | Source, automation, approval, or handoff guard failed |
| `completed` | Reserved for future verified completion packets |
| `failed` | Reserved for runtime failures |

### Source, Automation, and Redaction Guards

The plugin includes local validators for:

- OpenAI/Codex/source-backed claims;
- community claim metadata;
- secret-like literal detection;
- automation candidate readiness;
- active automation boundary;
- handoff completeness;
- local path and private data redaction in runner output.

### Bundled Context7 MCP

The plugin manifest points to `.mcp.json`, which registers a `context7` MCP server with:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "startup_timeout_sec": 20
  }
}
```

This follows the Codex MCP example for Context7 and keeps secrets out of the plugin package. A project or user can still configure an API key separately in their Codex MCP configuration when higher Context7 limits or private sources are required.

## Repository Layout

```text
product-agent-os/
  .codex-plugin/
    plugin.json
  .mcp.json
  README.md
  assets/
    fixtures/
    templates/
  hooks/
  scripts/
    product_agent_os/
    codex_runtime_runner/
    render_infrastructure.py
    merge_infrastructure.py
    run_codex_runtime_runner.py
    run_fixture_eval.py
    validate_*.py
  skills/
    project-lifecycle-orchestrator/
    workspace-discovery-auditor/
    requirements-author/
    implementation-planner/
    agent-team-designer/
    test-eval-designer/
    risk-reviewer/
    docs-maintainer/
    pr-release-operator/
    learning-loop-maintainer/
    automation-promoter/
```

`plugin.json` is the required Codex plugin manifest. The current manifest points to bundled skills and `.mcp.json`; `.mcp.json` registers Context7 for up-to-date developer documentation. Hook scripts are present as templates and examples, but plugin-bundled hooks are opt-in in Codex and this plugin does not silently activate them.

## Install in Codex

Codex installs plugins through marketplaces. For local development, use either a repo marketplace or a personal marketplace.

### Option A: Repo-Scoped Marketplace

Use this when the plugin should be discoverable from a specific repository.

1. Put the plugin under the repository's `plugins/` directory:

```text
<repo>/
  .agents/
    plugins/
      marketplace.json
  plugins/
    product-agent-os/
      .codex-plugin/
        plugin.json
```

2. Add or update `<repo>/.agents/plugins/marketplace.json`:

```json
{
  "name": "local-product-agent-plugins",
  "interface": {
    "displayName": "Local Product-Agent Plugins"
  },
  "plugins": [
    {
      "name": "product-agent-os",
      "source": {
        "source": "local",
        "path": "./plugins/product-agent-os"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

3. Restart Codex.
4. Open the plugin directory.
5. Select `Local Product-Agent Plugins`.
6. Install or enable `Product-Agent OS`.

Codex resolves `source.path` relative to the marketplace root, not relative to `.agents/plugins/`.

### Option B: Personal Marketplace

Use this when you want the plugin available across projects on your machine.

1. Copy the plugin to a personal plugin directory, for example:

```powershell
New-Item -ItemType Directory -Force -Path $HOME\.codex\plugins | Out-Null
Copy-Item -Recurse -Force plugins\product-agent-os $HOME\.codex\plugins\product-agent-os
```

2. Add or update `$HOME\.agents\plugins\marketplace.json`:

```json
{
  "name": "personal-product-agent-plugins",
  "interface": {
    "displayName": "Personal Product-Agent Plugins"
  },
  "plugins": [
    {
      "name": "product-agent-os",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/product-agent-os"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

3. Restart Codex and enable the plugin from the plugin directory.

### Option C: Add a Marketplace From CLI

When you maintain a local marketplace root, Codex can track it:

```powershell
codex plugin marketplace add <local-marketplace-root>
```

Then restart Codex and install the plugin from that marketplace.

## Apply to a Project

There are two supported ways to apply the plugin to a project.

### Guided Codex Flow

After installing the plugin, open the target project in Codex and start with one of the manifest prompts:

```text
Use Product-Agent OS to audit this workspace and propose a safe infrastructure plan.
```

or:

```text
Use Product-Agent OS to guide this feature from requirements to PR packet.
```

Expected first behavior:

1. Codex uses `workspace-discovery-auditor` or the local discovery helper.
2. It reports detected stack, existing control-plane files, missing artifacts, risks, and blockers.
3. It proposes staged infrastructure instead of writing directly.
4. It asks for approval before target workspace writes.

### Scripted Local Flow

Use scripts when you want deterministic local artifacts and machine-checkable output.

From this plugin directory:

```powershell
cd plugins\product-agent-os
```

Inspect a target workspace without writing:

```powershell
python scripts\render_infrastructure.py <workspace> --dry-run
```

Stage proposed infrastructure outside the target workspace:

```powershell
python scripts\render_infrastructure.py <workspace> --stage <stage-dir>
```

Build a read-only merge plan:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --plan
```

The merge plan writes `product-agent-os-approval-template.json` into the stage directory. Fill it in as `product-agent-os-approval.json` or another approval file. The approval record must name the current merge plan id, approved targets, approved actions, approver, timestamp, accepted risks, denied targets, notes, and hook activation decision.

Apply approved changes:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --apply --approval-file <approval.json>
```

Rollback an applied merge:

```powershell
python scripts\merge_infrastructure.py <workspace> <stage-dir> --rollback <rollback-manifest.json>
```

Run the Codex-only route contract:

```powershell
python scripts\run_codex_runtime_runner.py <workspace> --contract
```

Validate a runner result:

```powershell
python scripts\validate_codex_runtime_runner.py <result.json>
```

## Recommended First Run

For a real project, start with this sequence:

1. Run dry-run:

```powershell
python scripts\render_infrastructure.py <workspace> --dry-run
```

2. Review the `infrastructure_plan.status`, `create`, `update`, `leave_unchanged`, `warnings`, and `blocked` fields.
3. If the plan is acceptable, stage to a directory outside the workspace:

```powershell
python scripts\render_infrastructure.py <workspace> --stage C:\tmp\product-agent-os-stage
```

4. Build a merge plan:

```powershell
python scripts\merge_infrastructure.py <workspace> C:\tmp\product-agent-os-stage --plan
```

5. Inspect staged files and the approval template.
6. Fill approval only for the exact targets and actions you intend to apply.
7. Apply with approval.
8. Run the project's normal tests and update `RUNLOG.md` with evidence.

## Lifecycle State Routing

The Codex runtime runner maps project state to next work:

| Lifecycle state | Next worker | Write policy |
| --- | --- | --- |
| `uninitialized` | `workspace-discovery-auditor` | `read_only` |
| `infrastructure_planned` | `requirements-author` | `staged_only` |
| `requirements_ready` | `implementation-planner` | `staged_only` |
| `plan_ready` | `agent-team-designer` | `staged_only` |
| `team_ready` | `test-eval-designer` | `staged_only` |
| `build_active` | `builder` subagent when allowed | `approved_write` |
| `quality_gate` | `risk-reviewer` | `read_only` |
| `review_ready` | `pr-release-operator` | `staged_only` |
| `release_ready` | `learning-loop-maintainer` | `staged_only` |
| `learning_ready` | `automation-promoter` | `staged_only` |
| `maintenance` | `project-lifecycle-orchestrator` | `read_only` |

`approved_write` always requires explicit approval. Automation promotion remains candidate-only.

## Safety Rules

- Do not stage artifacts inside the target workspace.
- Do not apply a merge plan without reviewing staged files.
- Do not enable hook activation unless the approval record includes hook-specific metadata.
- Do not create active recurring automations from this plugin.
- Do not store secrets, tokens, private keys, customer data, or raw private chat logs in generated artifacts.
- Do not treat memory or chat history as source of truth for OpenAI product behavior.
- Do not claim checks passed unless they were run in the current lifecycle step.

## Validate This Plugin

From the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

The fixture eval suite covers greenfield setup, existing files, source-policy conflicts, failed verification logs, unsafe writes, safe merge behavior, rollback, automation candidate readiness, Codex runtime runner guardrails, scenario usage modes, and false-positive methodology/tooling gates.

## Development Notes

- Keep plugin scripts dependency-free unless a future track explicitly justifies a dependency.
- Keep bundled MCP config free of secrets; users should provide Context7 credentials through their own Codex MCP configuration when needed.
- Keep all templates synthetic and free of private data.
- Keep Product-Agent OS documentation user-facing; implementation plans and specs should remain internal history unless intentionally exposed.
- Prefer behavior-level tests and fixture evals over snapshot-only tests.
- Update source-backed docs when official OpenAI Codex plugin, skills, hooks, approvals, or automation behavior changes.
