# REQUIREMENTS.md

<!-- product-agent-os:start requirements -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-27

## Goal

- Развить Product-Agent OS plugin из набора agentic workflow в воспроизводимый engineering operating system для Codex App, CLI и IDE extension.
- Поддерживать разработку проектов разной сложности через staged artifacts, methodology gates, tests/evals, source policy, approvals and human ownership.

## Current Slice

- Last completed slice before this run: Track 10 Task 23 Batch 6 `T10-Q-M23..M25` full verification and explicit-only commit boundary.
- Active planning artifact: `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- Staged next-track artifact: Track 10 `Task 24: Self-Verification And Modernization Loop` with matrix `T10-SV-M-1..M62`, guardrails `T10-SV-G1..G6` and batches 7-12.
- Current slice: Task 24 planning and root system-file sync. Task 24 implementation has not started; commit/push/PR remains explicit-only and was not executed.
- Current route: long-running plugin/skill/docs/evals work.
- Scenario status: Track 9 foundation, all 12 methodology domains through `T9-D12`, Task 20 Cross-Domain Synthesis through `T9-S-M14`, Task 21 runtime runner/finish-options through `T9-R-M25`, Task 22 final documentation sync closure, Track 10 Task 23 full verification and staged Task 24 matrix/batch planning are the current acceptance baseline.

## Scope

- Product-Agent OS implementation package: `plugins/product-agent-os/`.
- User-facing docs: `docs/product-agent-os/`, `docs/product-agent/`, `docs/sources/`.
- Track 9 methodology sources: `docs/methodologies/`.
- Track 9 plan: `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Track 10 plan: `docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md`.
- Project control-plane files: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`.
- Verification: unit tests, fixture eval, Codex compatibility, docs check, strict MkDocs build when docs/nav-sensitive changes are made.

## Non-Goals

- Do not activate hooks, automations, GitHub Actions, external publishing, schedules or package registry mutations without explicit approval.
- Do not treat community claims as durable rules without trust level and verification status.
- Do not force DDD/FSD/docs tooling where the workspace does not justify it.
- Do not mutate target workspaces directly from Track 3 renderer; use dry-run/staged output and approval boundaries.
- Do not treat Track 10 guided questions, answer ledger, status snapshot or HTML dashboard as workspace evidence, approval, automation, or source of truth. Task 23 implementation is verified, but generated artifacts remain staged-first and approval-bound.
- Do not treat Task 24 scorecards, reports, eval packets, modernization candidates or automation candidates as approval to rewrite agents, skills, prompt/policy packs, router/tool policies, harness config, schedules or external workflows. Live eval calls, active schedules, Agents SDK apps and external writes remain out of scope without explicit approval.

## Acceptance Criteria

- Every implemented Track 8 slice has source-backed rationale, concrete plugin artifact, focused tests or evals, fixture coverage where applicable, docs sync and current verification evidence.
- Methodology gates remain conditional: they must name applicability, evidence, accepted gap and residual risk.
- Completion claims must cite commands run in the current run.
- T8-A8 detects and routes FSD-like UI structure without forcing FSD on backend, native, simple CRUD or simple MVP work.
- T8-A9 hardens product metrics with anti-Goodhart, privacy, retention and owner signoff fields.
- T8-A16 generalizes evidence-before-completion so ready/completed/fixed/works/release claims across scenarios require current command, eval, runtime evidence or explicitly marked inspection-only evidence with an explicit test gap.
- T8-C closes T8-A11 by making `docs_as_code_impact` conditional with `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required` statuses, plus stack-aware docs tooling decisions without forced installs or CI/hosted docs/DB introspection activation.
- T8-F generalizes conditional readiness gates with `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` and `approval_required` statuses; every gate must name applicability reason, required evidence, owner and residual risk, and detection alone cannot claim readiness.
- T8-H publishes operator-facing scenario, behavioral eval and Codex compatibility docs with Source status, nav entries, docs check coverage, source registry closure and current verification evidence.
- T8-B adds `standards_trigger_policy` for ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions applicability, with `governance-proposal.md`, no forced external activation and approval-bound governance changes.
- T8-GX adds fixture-level false-positive coverage for backend/native FSD routing, simple CRUD DDD routing, docs-light no-portal routing and hosted docs/DB introspection approval boundaries.
- T8-D adds `methodology_applicability` discovery packets for architecture boundary, test/eval-first evidence, docs-as-code ownership, product measurement, complex-domain DDD, applicable FSD structure, docs tooling decision and standards trigger policy, each with status, applicability reason, evidence, required evidence, owner and residual risk.
- Track 9 work must follow the section implementation protocol: read the relevant task block in `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`, deeply audit the matching `docs/methodologies/` source file, update the task list or backlog if the audit finds missing nuances, and only then implement the focused slice.
- Track 9 domain slices must record methodology concepts, readiness gates, artifact templates, discovery signals, false-positive risks, lifecycle skill impacts, tests/evals and docs sync before being marked complete.
- T9-D1 Business/Product is complete with product hypothesis, value proposition, opportunity tree, experiment plan, tracking plan, metric scope, decision horizon and workflow-promotion value evidence.
- T9-D2 Requirements/Domain is complete with `requirements_domain` catalog data, requirement quality, stable IDs, acceptance scenario quality, business rules, requirements traceability, API/UI/data traceability, domain events, owner review, accepted gaps, change impact and unsupported-claim rejection.
- T9-D3 Solution Architecture is complete with `solution_architecture` catalog data, context/container boundaries, ownership, public contract trace, data ownership, trust boundary review, ADR/tradeoff, runtime topology, observability, diagram render checks, fitness functions, migration rollback, accepted gaps and unsupported-claim rejection.
- T9-D4 Quality/Testing/Evals is complete with `quality_testing_evals` catalog data, quality strategy, risk scope, test/eval/runtime/manual/visual evidence, CI gates, flaky policy, coverage policy, test data privacy, bug reproduction, regression impact and evidence before completion.
- T9-D5 Codex/Agentic Workflow is complete with `codex_agentic_workflow` catalog data, control plane, source of truth, read-only discovery, approval boundaries, model/reasoning policy, memory policy, handoffs, ownership split, subagent safety, MCP review, hook governance, plugin boundary, skill promotion, automation stability and agent eval workflow.
- T9-D6 Frontend is complete with `frontend` catalog data, user-flow acceptance, component state matrix, design-system boundary, conditional Storybook/FSD routing, accessibility, visual/runtime evidence, performance budget and unsupported-claim rejection.
- T9-D7 Backend is complete with `backend` catalog data, service boundary, runtime/failure/observability/security/rollback evidence, dependency/job/data/ops depth, CI/deployment discovery, severity policy and owner-reviewed evidence sufficiency routing.
- T9-D8 API & Integrations is complete with `api_integrations` catalog data, contract source, consumer map, compatibility, security, errors, contract tests, events/webhooks, generated SDK manifest, external-write approval and unsupported-claim rejection.
- T9-D9 Database & Data is complete with `database_data` catalog data, database inventory, dictionary, schema source, migration plan, expand-contract, transaction boundary, rollback/backup evidence, data classification, data quality, data contract, lineage, query performance, retention/deletion, synthetic fixture policy, production access approval and unsupported-claim rejection.
- T9-D10 LLM / AI / RAG is complete with `llm_ai_rag` catalog data, AI behavior promise, baseline/current evals, prompt/model/tool/RAG/grounding evidence, trace evidence, guardrails, cost/latency, eval tooling, model migration, lifecycle/privacy, incident workflow and unsupported-claim rejection.
- T9-D11 Security, Privacy & Compliance is complete with `security_privacy_compliance` catalog data, threat surface, ASVS/SSDF/SAMM mapping, authorization negative tests, secrets, data classification, privacy impact, supply chain, SBOM/provenance, CI permissions, audit logging, compliance overlay, vulnerability response, explicit Codex Security scan status and unsupported-claim rejection.
- T9-D12 Delivery, Release & Operations is complete with `delivery_release_operations` catalog data, release scope, versioning, changelog/release notes, artifact manifest, release evidence, rollout, rollback, CI/CD governance, observability/SLO, runbooks, incidents, post-release learning, release mode, build-release-run, platform distribution, DORA, release integrity handoff, owner-reviewed evidence sufficiency and unsupported-claim rejection.
- Task 20 Cross-Domain Synthesis is complete with normalized shared gates, artifact ownership, evidence-before-completion concepts, semantic evidence sufficiency, cross-domain false positives, conflict rules, grouped report rendering, lifecycle skill routing and final fixture coverage.
- Task 21 through `T9-R-M25` updates runtime runner and finish-option behavior so synthesized methodology packets can be consumed without forcing unrelated gates, scaffolding before approval or claiming verification from detection alone. The completed runtime contract now includes CLI/validator JSON output coverage, generated control-plane/eval/handoff support, schema-v1 backward compatibility, lifecycle-status finish-option mapping, cross-domain runtime bridge checks, compact first-response fields, structured high-risk taxonomy and ownership/parallelism routing guards.
- Task 22 must close Product-Agent OS Track 9 documentation, source registry/backlog, generated docs references and final verification evidence, and absorb the legacy Track 9 `Task 23: Final Verification Baseline` into Task 22 closure.
- Task 22 final documentation sync closure acceptance: Track 1-9 acceptance is documented across Product-Agent OS user-facing docs, root/plugin READMEs, `docs/sources/registry.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` and `RUNLOG.md`; the legacy Track 9 `Task 23: Final Verification Baseline` is absorbed into Task 22 final verification evidence.
- Task 23 guided question protocol and status dashboard is implemented and fully verified through Batch 6 `T10-Q-M23..M25`. Acceptance includes `question_queue_contract_present`, `status_snapshot_present`, `status_dashboard_present`, `dashboard_no_external_assets`, `question_budget_false_positive_guard_present`, `dashboard_not_source_of_truth`, `stale_evidence_no_success_claim`, full unit/fixture/transcript/Codex compatibility/docs/MkDocs/diff hygiene and explicit-only commit boundary.
- Track 10 dashboard acceptance keeps `.codex/product-agent-os/status.html` and `.codex/product-agent-os/status.json` as staged generated views over JSON/Markdown artifacts, not editable source of truth or success evidence.
- Task 24 self-verification and modernization planning is staged with description, implementation surfaces, matrix `T10-SV-M-1..M62`, guardrails `T10-SV-G1..G6`, batches 7-12, verification expectations and explicit-only git boundary in the Track 10 plan.
- Task 24 implementation acceptance is reuse-first: reuse existing redaction, guided question protocol, status snapshot/dashboard, automation policy, runtime contracts/routes, fixture eval runner, transcript eval runner and agentic workflow artifacts; new work is limited to metrics-loop domain logic, report rendering and CLI surfaces.
- Task 24 must prove source-priority, metrics packet bounds, trace data-classification, shared offline artifact safety, no baseline renderer pollution, redacted report output, scorecard ledger, update-candidate rollback and active-automation blocking before any implementation closure claim.
- `docs-maintainer` is now a packaged lifecycle skill for requirement IDs, source registry, glossary/ubiquitous-language and traceability docs after the requirements packet exists.

## Assumptions

- Official OpenAI documentation remains source of truth for Codex App, CLI, IDE extension, subagents, skills, AGENTS.md, memory, sandbox, approvals and MCP.
- Context7 may be used as retrieval layer, but official status depends on the underlying source.
- Root control-plane files describe this repository's active Product-Agent OS implementation work, not generated target-project assets.
- Task 24 planning evidence is not implementation evidence; implementation closure requires current focused tests/evals plus full Product-Agent OS verification proportional to touched files.
<!-- product-agent-os:end requirements -->
