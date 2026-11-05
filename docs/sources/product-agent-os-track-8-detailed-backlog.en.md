---
title: "Archive - Product-Agent OS Track 8: detailed implementation backlog"
---

# Archive - Product-Agent OS Track 8: detailed implementation backlog {#product-agent-os-track-8-detailed-implementation-backlog}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + verified methodology + implementation planning`

Date: **2026-05-23**.
Based on the [development methodology research log](development-methodology-research-log.md), the [gap matrix](development-methodology-gap-matrix.md) and the current Product-Agent OS state after Track 7.
Expanded with comparative analysis of [`obra/superpowers`](https://github.com/obra/superpowers) as a community/opensource intake source for behavioral workflow design; this source is not a source of truth for Codex and is used only for ideas that pass through Product-Agent OS safety, source and eval gates.

## Track 8 goal

Make Product-Agent OS capable not only of generating control-plane artifacts, but also of selecting and verifying engineering methodologies, standards and documentation tooling based on project context:

- methodologies: Agentic / AI-native development, TDD, ATDD, BDD, DDD, FSD, data-informed development, eval-driven AI development, docs-as-code;
- standards and specs: ADR/MADR, C4, arc42, OpenAPI, AsyncAPI, SemVer, Keep a Changelog, CODEOWNERS, GitHub Actions;
- tools: Swagger/OpenAPI tooling, Storybook, Mermaid, PlantUML, Structurizr DSL, DBML/dbdocs/SchemaSpy, MkDocs, Docusaurus, Sphinx, Antora, Read the Docs, TypeDoc, JSDoc, Javadoc, C# XML docs, Vale, markdownlint.

## Implementation progress

Status updated: **2026-05-24**.

| Status | Backlog area | What was implemented | Evidence |
| --- | --- | --- | --- |
| `done` | `T8-0` behavioral routing tests | Added focused tests for the behavioral eval template, Codex-only compatibility, `usage_mode`, first-response route contract and fixture usage-mode checks. | `python -m unittest discover -s tests -p "test_*.py" -v` -> 239 tests `OK`. |
| `done` | `T8-GY` behavioral workflow eval scaffold | Added `behavioral-workflows.json` with route, shortcut, bug rescue, plan quality, two-stage review, fresh-context handoff, finish options, Codex-only compatibility and cost/model cases. | `test_behavioral_workflow_evals.py`, `test_infrastructure_templates.py`. |
| `done` | `T8-GY` transcript/session evals | Implemented deterministic transcript/session runner, CLI wrapper, synthetic session fixture, privacy/no-secrets guard and fixture eval contract. | `test_transcript_session_evals.py`, `run_transcript_eval.py`, `transcript_session_eval_runner_contract_present`. |
| `done` | `T8-CY` Codex-only compatibility contract | Added the Codex-only validator and report template; checks cover `.codex-plugin`, bundled skills, Context7 MCP, staged hooks and absence of non-Codex adapter requirements. | `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` -> `status: compatible`. |
| `done` | `T8-S4` base usage-mode classifier | `discovery.py` returns `usage_mode` with primary, secondary, confidence, reasons, fallback, first response contract, minimum artifacts and behavioral eval cases for base modes. | Focused discovery tests and fixture eval usage-mode checks pass. |
| `done` | `T8-S1` bug rescue with `T8-A12` systematic debugging | Added `bug-rescue.md`, `bug-rescue-report.md`, `bug_reproduction_signals`, behavioral cases for no broad rewrite and no fix claim without reproduction, plus lifecycle wording for evidence-first routing. | `python -m unittest discover -s tests -p "test_*.py" -v` -> 243 tests `OK`; fixture eval exits `0`; Codex compatibility `status: compatible`. |
| `done` | `T8-S2` greenfield idea workflow | Added `greenfield-idea-to-plan.md`, `greenfield-idea-brief.md`, approval-before-scaffold minimum artifact, lightweight mode, and behavioral cases for no scaffold before approval. | Focused T8-S2 tests -> 48 tests `OK`; full verification is run after this status update. |
| `done` | `T8-S3` complex system acceleration | Added `complex-system-acceleration.md`, `integration-catalog.md`, release gates minimum artifact, ownership-first lifecycle overlay, and behavioral cases for ownership split and no over-parallelization. | Focused T8-S3 tests -> 50 tests `OK`; full verification is run after this status update. |
| `done` | `T8-S4` full usage-mode matrix | Classifier covers `greenfield_idea`, `bug_rescue`, `complex_system_acceleration`, `pr_review`, `legacy_onboarding`, `api_migration`, `ai_eval_regression`, `native_mobile_feature`, `desktop_local_first`, `data_migration`, `security_sensitive_change`, `ci_stabilization`, `release_packaging`, `docs_only`, `standard_feature`, and `maintenance`; `route_inputs` separates prompt intent, workspace signals and control-plane state. | Focused T8-S4 tests cover synthetic workspaces, fixture eval expectations and runner `--intent-hint` guard behavior; full unittest now runs 250 tests with `OK`. |
| `done` | `T8-S5` scenario handoff packet | Added standard Scenario Handoff fields to bug rescue, greenfield idea, complex acceleration and agent task packets; lifecycle skills block role transition or parallel work when handoff evidence is missing. | Focused T8-S5 tests ran 38 tests with `OK`; full unittest now runs 252 tests with `OK`; fixture eval exits `0`; Codex compatibility returns `status: compatible`; docs check passes. |
| `done` | `T8-S6` PR review workflow | Added `pr-review-readiness.md`, `pr-risk-review.md`, PR diff surface detection, PR review behavioral eval, and lifecycle wording for read-only two-stage PR review before merge. | Focused T8-S6 tests ran 57 tests with `OK`; full unittest now runs 255 tests with `OK`; fixture eval exits `0`; Codex compatibility returns `status: compatible`; docs check passes. |
| `done` | `T8-S7` legacy onboarding workflow | Added `legacy-onboarding.md`, `onboarding-map.md`, legacy run-script/docs-debt detection, `legacy_onboarding_signals`, behavioral eval coverage, and lifecycle wording that blocks refactor before orientation. | Focused T8-S7 tests ran 60 tests with `OK`; full unittest now runs 258 tests with `OK`; fixture eval exits `0`; Codex compatibility returns `status: compatible`; docs check passes. |
| `done` | `T8-S8` API migration workflow | Added `api-migration.md`, `migration-plan.md`, `api_migration_signals`, behavioral eval coverage, and lifecycle wording for contract changes before implementation or release. | Focused T8-S8 tests ran 63 tests with `OK`; full unittest ran 261 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. |
| `done` | `T8-S9` AI eval regression workflow | Added `ai-eval-regression.md`, `ai-eval-spec.md`, `ai_eval_signals`, behavioral eval coverage, and lifecycle wording for baseline, no-secrets dataset policy, rubric, threshold, rerun evidence, latency, cost and grounding before quality claims. | Focused T8-S9 tests ran 66 tests with `OK`; full unittest ran 264 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 63 artifacts. |
| `done` | `T8-S10` native mobile feature workflow | Added `native-mobile-feature.md`, `native_mobile_signals`, behavioral eval coverage, and lifecycle wording for platform assumptions, permissions, offline state, simulator/emulator, device, logs, screenshots, build command, runtime evidence, manual device gap and approval before runtime claims. | Focused T8-S10 tests ran 69 tests with `OK`; full unittest ran 267 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 64 artifacts. |
| `done` | `T8-S11` desktop local-first workflow | Added `desktop-local-first.md`, `desktop_local_signals`, behavioral eval coverage, and lifecycle wording for desktop platform assumptions, filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, runtime log check, build command, recovery path, rollback, runtime evidence, manual OS gap and approval before desktop runtime claims. | Focused T8-S11 tests ran 72 tests with `OK`; full unittest ran 270 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 65 artifacts. |
| `done` | `T8-S12` data migration workflow | Added `data-migration.md`, `data_migration_signals`, behavioral eval coverage, and lifecycle wording for schema changes, backfill, data quality, PII, sensitive fields, retention, rollback, validation, dry run, backup, database dictionary, owner review, production DB boundary and approval before production data access or migration execution. | Focused T8-S12 tests ran 75 tests with `OK`; full unittest ran 273 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 66 artifacts. |
| `done` | `T8-S13` security-sensitive change workflow | Added `security-sensitive-change.md`, `security-risk-review.md`, `security_sensitive_signals`, behavioral eval coverage, and lifecycle wording for threat surface, authn/authz, permissions, payment, billing, secrets, PII, sensitive data, abuse controls, rate limit, audit logging, tests, rollback, owner review, approval, and explicit Codex Security boundaries. | Focused T8-S13 tests ran 78 tests with `OK`; full unittest ran 276 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 68 artifacts. |
| `done` | `T8-S14` CI stabilization workflow | Added `ci-stabilization.md`, `ci-stabilization-report.md`, `ci_stabilization_signals`, behavioral eval coverage, and lifecycle wording for failing job, command, logs, environment, deterministic/flaky classification, failure evidence, isolation plan, local reproduction, rerun evidence, remote CI/GitHub Actions boundaries, approval, and no remote mutation before evidence. | Focused T8-S14 tests ran 81 tests with `OK`; full unittest ran 279 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer now stages 70 artifacts. |
| `done` | `T8-S15` release packaging workflow | Added `release-packaging.md`, `release-readiness.md`, `release_packaging_signals`, behavioral eval coverage, and lifecycle wording for release scope, package metadata, version/SemVer, changelog, build/test/docs evidence, security/license notes, artifacts, package registry, owner review, publish approval, tag boundary, rollback, and no publish/tag/release/upload before approval. | Focused T8-S15 tests ran 84 tests with `OK`; full unittest ran 282 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-S16` first-run route and intake | Hardened `first-run-intake.md`, expanded `first_response_contract`, added first-run behavioral cases for empty, broken, existing control-plane and complex system starts, and synced lifecycle skill wording. | Focused T8-S16 tests ran 98 tests with `OK`; full unittest ran 283 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A13` no-placeholder planning hardening | `implementation-planner` now enforces `plan_quality_check`; `PLAN.md`, `build-slice.md`, `plan-quality-check.md`, and `no-placeholder-plan` behavioral eval require exact files, owned/forbidden files, exact commands, expected outputs, rollback, evidence owner, placeholder scan, plan repair, and `mechanical_change` exception. | Focused T8-A13 tests ran 71 tests with `OK`; full unittest ran 285 tests with `OK`; fixture eval exited `0` and includes `plan_quality_contract_present`; Codex compatibility returned `status: compatible`; docs check and strict MkDocs passed. |
| `done` | `T8-A14` generalized two-stage review | `risk-reviewer`, `review-slice.md`, `RUNLOG.md`, `pr-risk-review.md`, and `two-stage-review` behavioral eval now require spec compliance before quality/risk for risky public-contract, migration, security-sensitive, data migration, release packaging and parallel slices. | Focused T8-A14 tests ran 63 tests with `OK`; full unittest ran 287 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A15` fresh-context handoff hardening | `agent-team-designer`, `handoff-contract.md`, `agent-task-packet.md`, `worktree-ownership.md`, and `fresh-context-handoff` behavioral eval now require complete task context, source constraints, allowed sources, inputs used, owned files, forbidden files, expected evidence, handoff output schema, stop conditions, and sequential fallback for any subagent or parallel worker. | Focused T8-A15 tests ran 65 tests with `OK`; full unittest ran 289 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A3/T8-A4` acceptance scenario hardening | `acceptance-scenarios.md`, generated `REQUIREMENTS/TEST/EVALS`, `development-standards.md`, `project-readiness.json`, `behavioral-workflows.json`, and lifecycle skills now require ATDD/BDD traceability before behavior changes. | Focused T8-A3/T8-A4 tests ran 77 tests with `OK`; full unittest ran 291 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A5` conditional domain model gate | `discovery.py`, `domain-modeling.md`, `project-readiness.json`, `implementation-planner`, and fixture eval now require `domain_model_when_complex_domain` only for complex backend/workflow/enterprise/data-heavy/multi-service or multi-context work, with accepted gap support and no DDD forcing for simple CRUD/MVP. | Focused T8-A5 tests ran 104 tests with `OK`; full unittest ran 294 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A6` bounded context architecture traceability | `domain-modeling.md`, `architecture-overview.md`, `project-readiness.json`, `implementation-planner`, `discovery.py`, generated `PLAN/TEST/EVALS/RUNLOG`, and fixture eval now require `bounded_context_architecture_boundary_trace`: every bounded context maps to architecture boundary or records an accepted gap. | Focused T8-A6 tests ran 106 tests with `OK`; full unittest ran 296 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A7` ubiquitous language traceability | `domain-modeling.md`, `project-readiness.json`, `implementation-planner`, generated `PLAN/TEST/EVALS/RUNLOG`, and fixture eval now require `ubiquitous_language_traceability`: every domain term maps to requirement/source plus API/event/contract, UI label, code module or owner, or records accepted gap with domain expert review. | Focused T8-A7 tests ran 79 tests with `OK`; full unittest ran 298 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A8` FSD structure routing | `discovery.py`, `component-card.md`, `development-standards.md`, `project-readiness.json`, `workspace-discovery-auditor`, and `implementation-planner` now support optional `fsd_structure` for applicable web UI work without forcing FSD on backend, native, simple CRUD or simple MVP work. | Focused T8-A8 tests ran 102 tests with `OK`; full unittest ran 302 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A9` metric hardening | `metric-spec.md`, `release-packet.md`, generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, and fixture eval now require `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff, and post-release review evidence. | Focused T8-A9 tests ran 83 tests with `OK`; full unittest ran 304 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-A16` evidence-before-completion | `release-packet.md`, `development-standards.md`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, behavioral eval, and fixture eval now require current evidence or explicit inspection-only gap before ready/completed/fixed/works/release claims. | Focused T8-A16 tests ran 87 tests with `OK`; full unittest ran 306 tests with `OK`; fixture eval exited `0` with renderer file count 73; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-C` docs tooling selector + `T8-A11` closure | `docs-tooling-decision.md`, `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, `docs_tooling_decision` discovery and fixture eval now require stack-aware docs tooling decisions and `docs_as_code_impact` applicability statuses. | Focused T8-C tests ran 122 tests with `OK`; full unittest ran 312 tests with `OK`; fixture eval exited `0` with renderer file count 74; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-F` conditional readiness gates | `project-readiness.json`, generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, lifecycle skills and fixture eval now require `readiness_statuses`, per-gate applicability, required evidence, owner and residual risk; detection alone can only support `present_unverified`. | Focused T8-F tests ran 88 tests with `OK`; full unittest ran 313 tests with `OK`; fixture eval exited `0` with 35 fixtures, 0 failures and renderer file count 74; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done` | `T8-B` standards trigger hardening | `governance-proposal.md`, strengthened `adr.md`, `architecture-overview.md`, `api-contract-review.md`, `documentation-system.md`, `release-packet.md`, `project-readiness.json`, lifecycle skills and fixture eval now require ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions trigger policy without forced external activation. | Focused T8-B tests ran 90 tests with `OK`; full unittest ran 322 tests with `OK`; fixture eval exited `0` with 35 fixtures, 0 failures and renderer file count 75; transcript eval exited `0` with 4 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs exited `0`. |
| `done` | `T8-GX` scenario fixture coverage hardening | Added false-positive and approval-bound fixtures for backend/native FSD routing, simple CRUD DDD routing, docs-light no-portal routing, and hosted docs/DB introspection approval boundaries. | Focused T8-GX fixture tests ran 27 tests with `OK`; full unittest ran 324 tests with `OK`; fixture eval exited `0` with 40 fixtures, 0 failures and renderer file count 75; transcript eval exited `0` with 4 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs exited `0`. |
| `done` | `T8-D` detailed discovery status depth | `discovery.py` now returns `methodology_applicability` status packets and fixture eval asserts `methodology_applicability_contract_present`. | Focused T8-D discovery/fixture tests ran 48 tests with `OK`; full unittest ran 326 tests with `OK`; fixture eval exited `0` with 40 fixtures, 0 failures, renderer file count 75 and `methodology_applicability_contract_present: true`; transcript eval exited `0` with 4 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs exited `0`. |
| `done` | `T8-E` first behavioral artifact set | Added `agent-task-packet.md`, `behavioral-eval-case.md`, `plan-quality-check.md`, `codex-compatibility-report.md`. | Template registry and renderer tests pass. |
| `done` | `T8-H` system docs and control-plane sync | Synced Product-Agent OS README, product-agent docs, architecture/technical/development standards pages, plugin spec, generated `AGENTS/REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG` templates and Track 8 backlog with T8-H semantics; added dedicated scenario, behavioral eval and Codex compatibility docs. | Focused T8-H docs tests ran 3 tests with `OK`; full unittest ran 316 tests with `OK`; fixture eval exited `0` with 35 fixtures, 0 failures and renderer file count 74; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. |
| `done-for-current-slices` | `T8-I` current verification loop | Current plugin and docs checks were refreshed for implemented slices through T8-D. | Focused T8-D discovery/fixture tests ran 48 tests with `OK`; full unittest ran 326 tests with `OK`; fixture eval exited `0` with 40 fixtures, 0 failures, renderer file count 75 and `methodology_applicability_contract_present: true`; transcript eval exited `0` with 4 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs exited `0`. |

## Deep plan audit: completed vs remaining

Audit date: **2026-05-23**. A task is marked `done` only when the packaged plugin has the staged artifact or route, tests/evals cover the behavior, and current verification evidence exists. `partial` means reusable behavior exists but the full planned contract still has evidence, docs, methodology, or tooling gaps.

| Plan area | Status | Evidence in plugin | Remaining work |
| --- | --- | --- | --- |
| `T8-S1` bug rescue | `done` | `bug-rescue.md`, `bug-rescue-report.md`, `bug_reproduction_signals`, root-cause behavioral cases, lifecycle stop conditions. | Broader repeated-failure UX can be refined later, but the planned slice is complete. |
| `T8-S2` greenfield idea | `done` | `greenfield-idea-to-plan.md`, `greenfield-idea-brief.md`, no-scaffold-before-approval cases, lightweight mode. | User-facing scenario docs are covered by `T8-H`; further UX tuning belongs to transcript/session evals. |
| `T8-S3` complex system acceleration | `done` | `complex-system-acceleration.md`, `integration-catalog.md`, ownership split, release gates, no-overparallelization evals. | Dedicated API/data/security/mobile workflows remain separate follow-up slices. |
| `T8-S4` usage mode classifier | `done` | `usage_mode`, `route_inputs`, `--intent-hint`, extended synthetic fixtures, fixture eval route assertions. | Classification quality can improve with more false-positive fixtures after each new workflow. |
| `T8-S5` scenario handoff packet | `done` | Scenario Handoff fields in workflow/task packet templates and lifecycle checks before role transitions. | Keep handoff concise for trivial or mechanical changes. |
| `T8-S6` PR review | `done` | `pr-review-readiness.md`, `pr-risk-review.md`, PR/diff signals, two-stage review wording and evals. | Real PR connector behavior is outside this slice and remains approval-bound. |
| `T8-S7` legacy onboarding | `done` | `legacy-onboarding.md`, `onboarding-map.md`, `legacy_onboarding_signals`, `present_unverified` rules, no-refactor-before-orientation eval. | Runtime claims stay unverified until commands or owners confirm them. |
| `T8-S8` API migration | `done` | `api-migration.md`, `migration-plan.md`, `api_migration_signals`, `api-migration-plan` behavioral case, lifecycle overlay, fixture `api-migration-repo`, minimum artifacts `migration plan` and `api contract review`. | Broader false-positive routing and real contract lint integrations can be refined later; the planned slice is complete. |
| `T8-S9` AI eval regression | `done` | `ai-eval-regression.md`, `ai-eval-spec.md`, `ai_eval_signals`, `ai-eval-regression-plan` behavioral case, lifecycle overlay, fixture `rag-quality-regression`, minimum artifacts `ai eval spec` and `baseline result`. | Judge calibration, false-positive routing and real eval runner integration can be refined later; the planned slice is complete. |
| `T8-S10` native mobile feature | `done` | `native-mobile-feature.md`, `native_mobile_signals`, `native-mobile-runtime-plan` behavioral case, lifecycle overlay, fixture `native-mobile-permissions`, minimum artifacts `platform runtime check` and `acceptance scenarios`. | Tooling varies heavily; real platform build/run evidence remains project-specific, but the planned slice is complete. |
| `T8-S11` desktop local-first | `done` | `desktop-local-first.md`, `desktop_local_signals`, `desktop-local-runtime-plan` behavioral case, lifecycle overlay, fixture `desktop-local-indexer`, minimum artifacts `local data risk note` and `runtime log check`. | Runtime verification is OS-specific; real desktop build/run evidence remains project-specific, but the planned slice is complete. |
| `T8-S12` data migration | `done` | `data-migration.md`, `data_migration_signals`, `data-migration-plan` behavioral case, lifecycle overlay, fixture `data-migration-pii`, minimum artifacts `migration plan` and `database dictionary`. | Real production data/DB access and migration execution remain project-specific and approval-bound, but the planned slice is complete. |
| `T8-S13` security-sensitive change | `done` | `security-sensitive-change.md`, `security-risk-review.md`, `security_sensitive_signals`, `security-sensitive-change-plan` behavioral case, lifecycle overlay, fixture `security-auth-payment`, minimum artifacts `security risk review` and `approval boundary`. | Dedicated security scans and external security-system changes remain explicit-request and approval-bound, but the planned slice is complete. |
| `T8-S14` CI stabilization | `done` | `ci-stabilization.md`, `ci-stabilization-report.md`, `ci_stabilization_signals`, `ci-stabilization-plan` behavioral case, lifecycle overlay, fixture `ci-flaky-tests`, minimum artifacts `ci stabilization report` and `failure evidence`. | Remote CI logs, reruns, settings, branch protection, hosted runner changes and GitHub Actions mutations remain approval-bound, but the planned slice is complete. |
| `T8-S15` release packaging | `done` | `release-packaging.md`, `release-readiness.md`, `release_packaging_signals`, `release-packaging-readiness` behavioral case, lifecycle overlay, fixture `package-release`, minimum artifacts `release readiness` and `finish options`. | Publishing, tagging, release creation, artifact upload, package registry mutation, marketplace/store submission, PR creation and branch pushes remain approval-bound, but the planned slice is complete. |
| `T8-S16` first-run route and intake | `done` | `first-run-intake.md`, runtime route packet with `usage_mode`, expanded `first_response_contract`, first-run behavioral cases for empty, broken, existing control-plane and complex system starts, and lifecycle skill wording. | The planned slice is complete; further UX tuning can happen through transcript/session evals. |
| `T8-A12` systematic debugging | `done` | Implemented through bug rescue workflow, report template and no-fix-without-repro behavioral cases. | None for the current slice. |
| `T8-A13` no-placeholder planning | `done` | `implementation-planner`, `PLAN.md`, `build-slice.md`, `plan-quality-check.md`, `no-placeholder-plan`, and fixture eval all enforce no-placeholder plan quality for non-trivial slices. | Runtime quality still depends on the agent actually filling fields truthfully; future transcript evals can test real session behavior. |
| `T8-A14` two-stage review | `done` | `review-slice.md`, PR review workflow, `risk-reviewer`, `RUNLOG.md`, `pr-risk-review.md`, and `two-stage-review` behavioral case require `stage 1: spec compliance` before `stage 2: quality/risk` for PR, public contract, migration, security-sensitive, data migration, release packaging and parallel slices. | Runtime quality still depends on truthful current evidence; future transcript/session evals can test real review conversations. |
| `T8-A15` fresh-context subagent handoff | `done` | `agent-team-designer`, `agent-task-packet.md`, `handoff-contract.md`, `worktree-ownership.md`, and `fresh-context-handoff` behavioral case enforce complete task context, source constraints, allowed sources, inputs used, owned/forbidden files, expected evidence, handoff output schema, stop conditions, and sequential fallback for any subagent or parallel worker. | Runtime quality still depends on truthful task packet content; future transcript/session evals can test real multi-agent conversations. |
| `T8-A3` / `T8-A4` acceptance and BDD scenarios | `done` | `acceptance-scenarios.md`, generated `REQUIREMENTS/TEST/EVALS`, `development-standards.md`, `project-readiness.json`, `behavioral-workflows.json`, `requirements-author`, `implementation-planner`, and `test-eval-designer` enforce ATDD/BDD traceability before behavior changes. | Real scenario quality still needs product, development and testing review; BDD does not replace unit, integration, contract tests or evals. |
| `T8-A5` conditional DDD domain model gate | `done` | `domain_model` discovery signal, complex-domain gap detection, `domain_model_when_complex_domain` readiness gate, strengthened `domain-modeling.md`, implementation-planner stop condition and fixture eval coverage are implemented. | Domain modeling quality still needs domain expert review; `T8-A6` closed bounded context traceability and `T8-A7` deepens ubiquitous language traceability. |
| `T8-A6` bounded context architecture traceability | `done` | `domain-modeling.md`, `architecture-overview.md`, readiness eval, implementation-planner and fixture eval enforce `bounded_context_architecture_boundary_trace` from bounded context to architecture boundary. Discovery also detects architecture context-map files as domain model evidence. | Human architecture review is still needed to validate whether the mapping is conceptually correct. |
| `T8-A7` ubiquitous language traceability | `done` | `domain-modeling.md`, generated control-plane templates, readiness eval, implementation-planner and fixture eval enforce `ubiquitous_language_traceability` from domain terms to requirements/API/events/contracts/UI labels/code modules or owners. | Human domain expert review is still needed to validate whether the terms are conceptually correct. |
| `T8-A8` FSD modeling | `done` | `fsd_structure` discovery signal, planner boundary prompt, `component-card.md`, development standards, readiness eval signal and false-positive tests are implemented. | UI architecture quality still needs owner review; directory detection is only a routing clue. |
| `T8-A9` metrics | `done` | `metric-spec.md`, `release-packet.md`, generated control-plane templates, readiness eval, lifecycle skills and fixture eval enforce anti-Goodhart, privacy classification, retention period, data minimization, owner signoff and post-release review evidence. | Metric quality still needs product owner review; artifact presence does not prove the chosen metric is conceptually correct. |
| `T8-A10` eval-driven AI development | `done` | `ai-eval-spec.md`, `ai-eval-regression.md`, `ai_eval_signals`, baseline/dataset/no-secrets/rubric/threshold/rerun gates and behavioral eval coverage exist. | Eval quality still depends on dataset representativeness and judge calibration. |
| `T8-A16` evidence-before-completion | `done` | `release-packet.md`, `development-standards.md`, generated control-plane templates, readiness eval, lifecycle skills, behavioral eval and fixture eval enforce current command/eval/runtime evidence or explicit inspection-only gap before ready/completed/fixed/works/release claims. | Evidence sufficiency still needs human review; the gate proves evidence is recorded, not that interpretation is perfect. |
| `T8-B1` to `T8-B5` ADR/C4/arc42/OpenAPI/AsyncAPI | `done` | `adr.md`, `architecture-overview.md`, `api-contract-review.md`, `documentation-system.md`, `project-readiness.json`, lifecycle skills and fixture eval now enforce trigger policy, C4/arc42 applicability, OpenAPI source-of-truth vs Swagger UI, and AsyncAPI producer/consumer compatibility fields. | Real project diagram rendering and contract lint commands remain stack-specific and approval/tooling-bound. |
| `T8-B6` / `T8-B7` SemVer and Keep a Changelog | `done` | `release-packet.md`, lifecycle skills and fixture eval now require SemVer impact as major/minor/patch/not_applicable with rationale and Keep a Changelog categories when release-bound public changes apply. | Tool-specific changelog linting remains optional and project-specific. |
| `T8-B8` / `T8-B9` CODEOWNERS and GitHub Actions | `done` | `governance-proposal.md`, `documentation-system.md`, lifecycle skills and fixture eval now require CODEOWNERS status, GitHub Actions least privilege fields, workflow names, commands, permissions, triggers, owners and no forced external activation. | Repository settings, branch protection, CODEOWNERS activation and GitHub Actions activation remain explicit-approval external actions. |
| `T8-C` documentation tooling selector + `T8-A11` docs-as-code applicability | `done` | `docs-tooling-decision.md`, `documentation-system.md`, generated `PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills, `docs_tooling_decision` discovery, focused tests and fixture eval contract now cover stack/tool-specific docs decisions and applicability statuses. | Planned slice complete; future refinement can add more project-specific docs build command discovery. |
| `T8-D` discovery model | `done` | `usage_mode`, `behavioral_route_inputs`, many surface detectors, `domain_model`, optional `fsd_structure`, `docs_tooling_decision`, `methodology_applicability`, `bug_reproduction_signals`, `legacy_onboarding_signals`, `api_migration_signals`, `ai_eval_signals`, `native_mobile_signals`, `desktop_local_signals`, `data_migration_signals`, `security_sensitive_signals`, `ci_stabilization_signals`, `release_packaging_signals`, and fixture route checks exist. | Planned discovery status depth is covered for the current Track 8 scope; future additions should be regression-driven by new project layouts. |
| `T8-E` artifact templates | `done-for-current-scope` | Current packaged set covers ADR, architecture, domain, docs tooling decision, governance proposal, metrics, API, migration plan, AI eval spec, UI component, DB, task packet, eval case, plan quality, acceptance scenarios, compatibility, bug, greenfield, integration, PR, onboarding, security review, CI stabilization report and release readiness. | Future scenario fixtures may add more examples, but the planned governance proposal artifact is present. |
| `T8-F` readiness eval | `done` | `project-readiness.json` defines `readiness_statuses` and structured `conditional_readiness_gates`; generated control-plane templates, lifecycle skills and fixture eval enforce applicability, evidence, owner and residual risk. | Planned slice complete; transcript/session evals now add deterministic replay coverage for selected conversations. |
| `T8-G` lifecycle skill updates | `done-for-current-scope` | Discovery auditor, lifecycle orchestrator, requirements author, implementation planner, test/eval designer, agent team, risk/review, API migration, AI eval regression, native/mobile, desktop local-first, data migration, security-sensitive, CI stabilization, release packaging, docs tooling selector, standards trigger policy, conditional readiness and compatibility paths have current-slice wording/tests. | Planned skill wording is current; future refinements can add deeper discovery statuses without changing the current skill contract. |
| `T8-GX` fixture and eval coverage | `done` | Extended fixtures exist and fixture eval checks expected `usage_mode`; T8-GX adds `backend-no-fsd`, `native-no-fsd`, `simple-crud-no-ddd`, `docs-light-no-portal` and `hosted-docs-approval` with named false-positive and approval-bound expected checks. | Planned fixture-hardening slice complete; future real-project layouts can add more fixtures as regressions are found. |
| `T8-GY` behavioral workflow evals | `done` | Behavioral template, validator, deterministic transcript/session runner and synthetic transcript fixtures exist with route, shortcut, review, handoff, finish, compatibility and privacy cases. | Semantic transcript quality still needs reviewer or future calibrated judge coverage. |
| `T8-H` documentation updates | `done` | Product-Agent OS README, product-agent docs, architecture/technical/development standards pages, plugin spec, generated control-plane templates, Track 8 backlog, dedicated scenarios page, behavioral eval docs, Codex compatibility docs and source registry closure note reflect current done behavior through T8-D. | Planned docs slice complete; future updates should track new refinement slices when selected. |
| `T8-I` verification loop | `done-for-current-slices` | Focused T8-D discovery/fixture tests ran 48 tests with `OK`; full unittest ran 326 tests with `OK`; fixture eval exited `0` with 40 fixtures, 0 failures, renderer file count 75 and `methodology_applicability_contract_present: true`; transcript eval exited `0` with 4 sessions and 0 failures; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs exited `0`. | Re-run full verification after every subsequent plugin/docs slice. |

## Next implementation tasks after T8-D

Reviewed on **2026-05-24** after the T8-D detailed discovery model status depth focused verification. The current Track 8 implementation queue is complete; future work should be scheduled only as a regression-driven refinement or a new explicitly scoped track.

| Order | Status | Task | Scope | Main artifacts | Required checks |
| --- | --- | --- | --- | --- | --- |
| 1 | `done` | `T8-H` dedicated scenario and eval docs | Publish scenario, behavioral eval and Codex compatibility pages for plugin operators. | `docs/product-agent-os/scenarios.md`, `behavioral-evals.md`, `codex-compatibility.md`, source registry closure notes. | Focused docs contract, docs check, strict MkDocs build, source registry check. |
| 2 | `done` | `T8-GY` transcript/session eval runner | Add transcript-oriented eval path beyond synthetic behavioral JSON. | `behavioral-workflows.json`, `transcript_evals.py`, `run_transcript_eval.py`, synthetic transcript fixture, eval docs. | Runner tests, synthetic transcript fixtures, privacy/no-secrets checks. |
| 3 | `done` | `T8-B` standards trigger hardening | Add stronger ADR/C4/OpenAPI/AsyncAPI/SemVer/CODEOWNERS/GitHub Actions trigger rules where project context makes them applicable. | `documentation-system.md`, `api-contract-review.md`, `release-packet.md`, `governance-proposal.md`. | Focused template/readiness/lifecycle tests and no forced external activation checks. |
| 4 | `done` | `T8-GX` scenario fixture coverage hardening | Add false-positive and approval-bound scenario fixtures for methodology/tooling gates that were mostly unit/template-level. | fixtures, `run_fixture_eval.py`, behavioral eval docs. | Focused fixture tests, fixture eval and no-secrets checks. |
| 5 | `done` | `T8-D` detailed discovery status depth | Add richer methodology/tooling status objects for remaining readiness gates. | `discovery.py`, `run_fixture_eval.py`, focused discovery tests. | Focused discovery/fixture tests, fixture eval and docs sync. |

## Completed implementation slice: `T8-S1` bug rescue

Scope: implement the bug-rescue workflow with `T8-A12` systematic debugging behavior.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `bug-rescue.md`, `bug-rescue-report.md`, reproduction evidence, rollback notes and failed-log discovery signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/bug-rescue.md` | Add staged workflow that starts from symptom, expected/actual behavior, reproduction command or manual repro, failing evidence and suspect boundary. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/bug-rescue-report.md` | Add diagnosis report with hypotheses, eliminated causes, root-cause evidence, regression test path, fix scope, rollback and unresolved risks. |
| 4 | `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Register the workflow and report in the staged renderer without direct project mutation. |
| 5 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Extend `bug_reproduction_signals` while treating logs as possible evidence, not verified truth. |
| 6 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Add behavioral cases proving bug-rescue routing, no broad rewrite, no fix claim without reproduction and stop-at-diagnosis behavior when repro is missing. |
| 7 | `plugins/product-agent-os/skills/*/SKILL.md` where needed | Update lifecycle wording only where it changes runtime behavior: systematic debugging first, smallest fix, regression evidence before completion. |

Verification for the slice:

- Focused template and discovery tests.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py`.
- Codex-only compatibility check: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py`.
- Docs check: `python tools\check_docs.py`.

Result: completed on **2026-05-23**. Next slice was `T8-S2` greenfield idea workflow.

## Completed implementation slice: `T8-S2` greenfield idea

Scope: implement the empty-folder and idea-stage workflow before any scaffold or project mutation.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `greenfield-idea-to-plan.md`, `greenfield-idea-brief.md`, no scaffold before approval, and lightweight first-slice fields. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/greenfield-idea-to-plan.md` | Add staged workflow for problem, users, options, non-goals, selected direction, first vertical slice and approval boundary. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/greenfield-idea-brief.md` | Add idea brief template with product hypothesis, constraints, first acceptance scenarios, metrics and docs/tooling decision input. |
| 4 | `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Register the workflow and brief in the staged renderer. |
| 5 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Add behavioral cases proving no scaffold before approval and lightweight mode for very small ideas. |
| 6 | Lifecycle skills where needed | Make first response ask at most one blocking question and propose the next smallest artifact instead of dumping all methodology gates. |

Result: completed on **2026-05-23**. Next slice was `T8-S3` complex system acceleration.

## Completed implementation slice: `T8-S3` complex system acceleration

Scope: implement a workflow for experienced developers accelerating web/API/integration-heavy systems without unsafe over-parallelization.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `complex-system-acceleration.md`, `integration-catalog.md`, ownership boundaries, OpenAPI/AsyncAPI, DB/docs and release gates. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/complex-system-acceleration.md` | Add staged workflow for web, API, integration, DB, docs, eval and release slices. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/integration-catalog.md` | Add integration catalog with system owner, auth, data exchanged, rate limits, retry/idempotency, event/webhook contracts, observability and rollback. |
| 4 | `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Register workflow and catalog in the staged renderer. |
| 5 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Add behavioral cases for ownership split and no over-parallelization when files or systems overlap. |
| 6 | Lifecycle skills where needed | Route complex acceleration to ownership-first planning and fresh-context task packets before parallel work. |

Result: completed on **2026-05-23**. Next slice is `T8-S4` full usage-mode matrix.

## Completed implementation slice: `T8-S4` full usage-mode matrix

Scope: finish route classification before methodology gates and expose behavioral route inputs.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_discovery.py` | Add failing tests for legacy onboarding, API migration, AI/RAG eval regression, native mobile, desktop local-first, data migration, security-sensitive, CI stabilization and release packaging surfaces. |
| 2 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Add explicit surface detectors and return `route_inputs` with prompt intent, workspace signals and control-plane state separated. |
| 3 | `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`, `routes.py` | Add `--intent-hint` support and carry behavioral route inputs in the route packet without weakening source, approval or write guards. |
| 4 | `plugins/product-agent-os/assets/fixtures/*` and `run_fixture_eval.py` | Add synthetic scenario fixtures and fixture eval checks for the extended classifier matrix. |
| 5 | `plugins/product-agent-os/README.md` | Document the expanded classifier and intent-routing guard boundary. |

Result: completed on **2026-05-23**. Next slice was `T8-S5` scenario handoff packet.

## Completed implementation slice: `T8-S5` scenario handoff packet

Scope: standardize the handoff packet produced by each scenario workflow.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Add failing tests that each scenario workflow names sources/context, assumptions, files touched/proposed, verification evidence, open risks and recommended next role. |
| 2 | `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md` | Extend scenario handoff fields only where current packet is insufficient. |
| 3 | Scenario workflow templates | Ensure bug rescue, greenfield idea and complex acceleration workflows each emit a concise handoff output. |
| 4 | Lifecycle skills where needed | Enforce handoff contract before role transitions or parallel work. |
| 5 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Add or extend behavioral cases for scenario handoff completeness without turning small tasks into bureaucracy. |

Result: completed on **2026-05-23**. Full verification ran 252 tests with `OK`, fixture eval exited `0`, Codex compatibility returned `status: compatible`, and docs check passed. Next slice is `T8-S6` PR review workflow.

## Completed implementation slice: `T8-S6` PR review workflow

Scope: add a workflow for reviewing changed files before merge.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `pr-review-readiness.md`, `pr-risk-review.md`, diff/PR route inputs and risk fields. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/pr-review-readiness.md` | Add staged workflow for changed files, behavior/API/DB/UI/security/docs/release impact, missing checks and review evidence. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/pr-risk-review.md` | Add review artifact with spec-compliance verdict, quality/risk verdict, commands, findings, questions and residual risk. |
| 4 | `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Register workflow and artifact in the staged renderer. |
| 5 | Lifecycle skills and behavioral evals | Route PR review to two-stage review without external writes, PR creation or publish actions. |

Result: completed on **2026-05-23**. Full verification ran 255 tests with `OK`, fixture eval exited `0`, Codex compatibility returned `status: compatible`, and docs check passed. Next slice is `T8-S7` legacy onboarding.

## Completed implementation slice: `T8-S7` legacy onboarding

Scope: add a workflow for safe orientation in old or undocumented repositories.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `legacy-onboarding.md`, `onboarding-map.md`, legacy/docs-debt route signals, and `present_unverified` wording. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/legacy-onboarding.md` | Add staged workflow for source map, entry points, run commands, docs debt, verification status and first safe documentation slice. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/onboarding-map.md` | Add artifact for entry points, runbook, architecture/doc gaps, verification status and first safe slice without refactor. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route legacy/undocumented repositories to read-only onboarding before refactor or broad cleanup. |

Result: completed on **2026-05-23**. Full verification ran 258 tests with `OK`, fixture eval exited `0`, Codex compatibility returned `status: compatible`, and docs check passed. Next slice was `T8-S8` API migration.

## Completed implementation slice: `T8-S8` API migration

Scope: add a workflow for changing HTTP/event contracts and consumer-facing API behavior.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `api-migration.md`, `migration-plan.md`, contract/versioning/deprecation fields, and API migration route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/api-migration.md` | Add staged workflow for OpenAPI/AsyncAPI, consumers, backwards compatibility, generated clients, examples, rollout and release impact. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/migration-plan.md` | Add artifact for current state, target state, compatibility, rollout, validation, deprecation, rollback and consumer impact. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route contract-changing work to migration planning before implementation or release. |

Result: implemented on **2026-05-23**. Focused T8-S8 verification ran 63 tests with `OK`; full unittest ran 261 tests with `OK`; fixture eval exited `0`; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`; renderer staged 61 artifacts after `T8-S8`. The next slice was `T8-S9` AI eval regression.

## Completed implementation slice: `T8-S9` AI eval regression

Scope: add a workflow for AI/RAG quality regressions where deterministic tests are not enough.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `ai-eval-regression.md`, `ai-eval-spec.md`, baseline/dataset/rubric/threshold fields, and AI eval route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/ai-eval-regression.md` | Add staged workflow for baseline, dataset policy, prompt/context changes, retrieval metrics, judge rubric, threshold, latency/cost and no-secrets handling. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/ai-eval-spec.md` | Add artifact for eval goal, dataset, metrics, judge rubric, baseline result, target threshold, failure examples, rerun command and residual risk. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route AI/RAG regression work to eval planning before model/prompt/retrieval changes or quality claims. |

Result: implemented on **2026-05-23**. Focused T8-S9 verification ran 66 tests with `OK`; full unittest ran 264 tests with `OK`; fixture eval exited `0` with renderer file count 63; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S10` native mobile feature.

## Completed implementation slice: `T8-S10` native mobile feature

Scope: add a workflow for iOS/Android/native mobile changes where platform build, simulator/emulator checks, permissions and screenshots matter.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `native-mobile-feature.md`, platform permission/offline/runtime fields, and native route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/native-mobile-feature.md` | Add staged workflow for platform assumptions, permissions, offline state, simulator/emulator, logs, screenshots, build commands and manual device gaps. |
| 3 | Discovery, lifecycle skills and behavioral evals | Route native/mobile work to platform runtime planning before implementation or quality claims. |

Result: implemented on **2026-05-23**. Focused T8-S10 verification ran 69 tests with `OK`; full unittest ran 267 tests with `OK`; fixture eval exited `0` with renderer file count 64; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S11` desktop local-first.

## Completed implementation slice: `T8-S11` desktop local-first

Scope: add a workflow for desktop apps with filesystem, local DB, background jobs, privacy, logs and recovery path.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `desktop-local-first.md`, filesystem/local data/background runtime fields, and desktop route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/desktop-local-first.md` | Add staged workflow for filesystem permissions, local DB, indexing/background jobs, privacy, app logs, runtime check and recovery path. |
| 3 | Discovery, lifecycle skills and behavioral evals | Route desktop/local-first work to local runtime planning before implementation or behavior claims. |

Result: implemented on **2026-05-23**. Focused T8-S11 verification ran 72 tests with `OK`; full unittest ran 270 tests with `OK`; fixture eval exited `0` with renderer file count 65; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S12` data migration.

## Completed implementation slice: `T8-S12` data migration

Scope: add a workflow for schema, backfill, retention and sensitive-data migration work.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `data-migration.md`, migration/rollback/privacy fields, and data migration route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/data-migration.md` | Add staged workflow for schema changes, backfill, data quality, PII/sensitive fields, retention, rollback and validation. |
| 3 | Discovery, lifecycle skills and behavioral evals | Route data migration work to migration planning before implementation, production DB access or completion claims. |

Result: implemented on **2026-05-23**. Focused T8-S12 verification ran 75 tests with `OK`; full unittest ran 273 tests with `OK`; fixture eval exited `0` with renderer file count 66; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S13` security-sensitive change.

## Completed implementation slice: `T8-S13` security-sensitive change

Scope: add a workflow for auth, permissions, payments, secrets or personal data changes.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `security-sensitive-change.md`, `security-risk-review.md`, approval/no-secrets wording, and security-sensitive route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/security-sensitive-change.md` | Add staged workflow for threat surface, authn/authz, permissions, payment surface, secrets, PII, abuse controls, rollback and approval gates. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/security-risk-review.md` | Add review artifact for threat surface, sensitive fields, tests, approvals, rollback and residual risk. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route security-sensitive work to risk review before implementation; integrate with Codex Security only when explicitly requested. |

Result: implemented on **2026-05-23**. Focused T8-S13 verification ran 78 tests with `OK`; full unittest ran 276 tests with `OK`; fixture eval exited `0` with renderer file count 68; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S14` CI stabilization.

## Completed implementation slice: `T8-S14` CI stabilization

Scope: add a workflow for failing or flaky CI without mutating remote CI settings.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `ci-stabilization.md`, `ci-stabilization-report.md`, deterministic-vs-flaky wording, and CI route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/ci-stabilization.md` | Add staged workflow for failing job, command, logs, environment, deterministic/flaky classification, isolation plan, rerun evidence, and no remote mutation. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/ci-stabilization-report.md` | Add report artifact for CI failure evidence, flake history, isolation, local reproduction, rerun command, residual risk, and approval needs. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route CI work to stabilization planning before claiming CI health or changing remote CI settings. |

Result: implemented on **2026-05-23**. Focused T8-S14 verification ran 81 tests with `OK`; full unittest ran 279 tests with `OK`; fixture eval exited `0` with renderer file count 70; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0`. The next slice was `T8-S15` release packaging.

## Completed implementation slice: `T8-S15` release packaging

Scope: add a workflow for package, SDK, plugin, app or open-source release readiness without publishing, tagging or mutating external release systems.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Add failing tests for `release-packaging.md`, `release-readiness.md`, SemVer/changelog/build/docs/security/publish approval wording, and release route signals. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/release-packaging.md` | Add staged workflow for release scope, package metadata, SemVer, changelog, build/test/docs evidence, security/license notes, rollback and publish approval. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/release-readiness.md` | Add readiness artifact for version impact, changelog, artifacts, commands, checks, docs, owners, publish boundary and residual risk. |
| 4 | Discovery, lifecycle skills and behavioral evals | Route release work to readiness planning before tagging, publishing, creating releases or claiming release readiness. |

Result: implemented on **2026-05-23**. Focused T8-S15 verification ran 84 tests with `OK`; full unittest ran 282 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. The next slice was `T8-S16` first-run route and intake hardening.

## Completed implementation slice: `T8-S16` first-run route and intake

Scope: harden the initial plugin response so Product-Agent OS chooses the right first action without dumping every methodology gate.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_codex_runtime_runner_*.py`, `tests/product_agent_os/test_lifecycle_skills.py` | Add failing tests for empty, broken, existing control-plane and complex system first-run behavior, route packet fields and lifecycle wording. |
| 2 | `plugins/product-agent-os/assets/templates/workflows/first-run-intake.md` | Add first response contract, entry scenario table, evidence gaps and safety boundaries for scaffold, fix, regenerate and parallelization shortcuts. |
| 3 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` and `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py` | Expand `first_response_contract` with minimum artifacts and evidence gaps and attach first-run behavioral cases to `usage_mode`. |
| 4 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` and `behavioral_evals.py` | Add behavioral cases for `first-run-empty-greenfield`, `first-run-broken-bug-rescue`, `first-run-existing-control-plane` and `first-run-complex-system`. |
| 5 | Lifecycle skills and system docs | Route first launch through small, approval-bound responses before scaffold, fix, regeneration or parallel work. |

Result: implemented on **2026-05-23**. Focused T8-S16 verification ran 98 tests with `OK`; full unittest ran 283 tests with `OK`; fixture eval exited `0` with renderer file count 72; Codex compatibility returned `status: compatible`; docs check passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`. The next slice was `T8-A13` no-placeholder planning hardening.

## Completed implementation slice: `T8-A13` no-placeholder planning hardening

Scope: make implementation plans executable enough for non-trivial work, while allowing a documented `mechanical_change` exception for small docs, formatting or config edits.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Failing-first checks require no-placeholder plan quality in planner skill, control-plane templates, behavioral eval and fixture eval. |
| 2 | `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | Planner stops before build unless non-trivial slices have exact files, owned files, forbidden files, exact commands, expected outputs, rollback, evidence owner and placeholder scan. |
| 3 | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md` | `PLAN.md` includes a no-placeholder plan quality gate, plan repair fields and `mechanical_change` reason. |
| 4 | `plugins/product-agent-os/assets/templates/workflows/build-slice.md` | Build slice workflow blocks implementation when plan quality is missing or blocked. |
| 5 | `plugins/product-agent-os/assets/templates/artifact-templates/plan-quality-check.md` | Plan quality template captures exact files, commands, expected outputs, evidence owner, placeholder scan, plan repair and stop-before-build verdict. |
| 6 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | `no-placeholder-plan` requires owned/forbidden files, exact commands, expected outputs, rollback, evidence owner, placeholder scan and `mechanical_change`; forbids vague validation and implementation before plan repair. |
| 7 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval emits `plan_quality_contract_present` for the Python fixture and fails if packaged planning artifacts lose the no-placeholder contract. |

Verification for the slice:

- Focused T8-A13 tests: 71 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 285 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-23**. The next slice was `T8-A14` generalized two-stage review.

## Completed implementation slice: `T8-A14` generalized two-stage review

Scope: generalize review from PR-only behavior into a reusable risky-slice gate where spec compliance is checked before quality and risk.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py` | Failing-first checks require a generalized two-stage review contract in the skill, templates and behavioral eval. |
| 2 | `plugins/product-agent-os/skills/risk-reviewer/SKILL.md` | Risk reviewer requires `stage 1: spec compliance` before `stage 2: quality/risk` for PR, public contract, migration, security-sensitive, data migration, release packaging, parallel and external-system slices. |
| 3 | `plugins/product-agent-os/assets/templates/workflows/review-slice.md` | Review workflow captures acceptance criteria, source constraints, public contract, missing evidence and both verdicts before readiness. |
| 4 | `plugins/product-agent-os/assets/templates/control-plane/RUNLOG.md` | RUNLOG records the two-stage review trace, missing evidence and blockers for generic one-stage reviews. |
| 5 | `plugins/product-agent-os/assets/templates/artifact-templates/pr-risk-review.md` | PR risk review packet is reusable as a risky-slice review packet while keeping PR/external-write boundaries explicit. |
| 6 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | `two-stage-review` now requires generalized review artifact, stage order, acceptance/source/public-contract fields and forbids generic review only, reversed stage order and ready verdicts with missing evidence. |

Verification for the slice:

- Focused T8-A14 tests: 63 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 287 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-23**. The next slice was `T8-A15` fresh-context handoff hardening.

## Completed implementation slice: `T8-A15` fresh-context handoff hardening

Scope: make subagent and parallel-worker handoffs complete enough to work from fresh context, not from raw chat history or implicit ownership.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py` | Failing-first checks require fresh-context handoff in the skill, templates, reference contract and behavioral eval. |
| 2 | `plugins/product-agent-os/skills/agent-team-designer/SKILL.md` | Agent team design requires fresh-context handoff for any subagent or parallel worker, not only complex acceleration. |
| 3 | `plugins/product-agent-os/skills/references/handoff-contract.md` | Handoff contract names complete task context, source constraints, allowed sources, inputs used, ownership, expected evidence, output schema, stop conditions and sequential fallback. |
| 4 | `plugins/product-agent-os/assets/templates/artifact-templates/agent-task-packet.md` | Agent task packet can carry complete context, source constraints, ownership, expected evidence, handoff output schema, accepted gaps and stop conditions. |
| 5 | `plugins/product-agent-os/assets/templates/workflows/worktree-ownership.md` | Ownership workflow blocks parallel work when ownership, source constraints, expected evidence, output schema or fallback are missing. |
| 6 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | `fresh-context-handoff` now requires fresh-context handoff, agent task packet, worktree ownership, required context fields, and forbids shared ownership ambiguity, missing handoff schema, raw conversation history, parallel work without task packet, cross-agent file ownership and missing expected evidence. |

Verification for the slice:

- Focused T8-A15 tests: 65 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 289 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 72.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A3/T8-A4` acceptance scenarios.

## Completed implementation slice: `T8-A3/T8-A4` acceptance scenario hardening

Scope: make ATDD/BDD behavior scenarios an explicit traceability artifact before behavior changes, without treating BDD as a replacement for tests and evals.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_behavioral_workflow_evals.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Failing-first checks require acceptance scenario registry, traceability fields, readiness gate, behavioral case, lifecycle skill wording and fixture eval coverage. |
| 2 | `plugins/product-agent-os/assets/templates/artifact-templates/acceptance-scenarios.md` | Template maps `requirement -> scenario -> check -> evidence owner`, supports Given/When/Then or equivalent behavior format, and records business rule, edge case, non-goal, explicit gap and evidence owner. |
| 3 | `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Renderer stages `.codex/artifact-templates/acceptance-scenarios.md` with the rest of Product-Agent OS infrastructure. |
| 4 | `plugins/product-agent-os/assets/templates/control-plane/REQUIREMENTS.md`, `TEST.md`, `EVALS.md`, and `workflows/development-standards.md` | Generated control-plane files require acceptance scenarios or explicit gap before behavior changes. |
| 5 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` and `behavioral-workflows.json` | Readiness eval includes `acceptance_scenarios_when_behavior_changes`; behavioral eval includes `acceptance-scenarios-traceability`. |
| 6 | `plugins/product-agent-os/skills/requirements-author/SKILL.md`, `implementation-planner/SKILL.md`, and `test-eval-designer/SKILL.md` | Lifecycle skills route behavior changes through acceptance scenarios before implementation and block scenarios without requirement, check or evidence owner. |
| 7 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval includes `acceptance_scenarios_contract_present` and renderer stages 73 artifacts. |

Verification for the slice:

- Focused T8-A3/T8-A4 tests: 77 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 291 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A5` conditional domain model gate.

## Completed implementation slice: `T8-A5` conditional domain model gate

Scope: make DDD domain modeling conditional, observable and enforceable for complex domains without forcing it on simple CRUD or simple MVP work.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Failing-first checks require a `domain_model` signal, false-positive protection for plain `domain/` folders, readiness gate terms, implementation-planner wording and fixture eval coverage. |
| 2 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Workspace audit detects explicit domain modeling evidence such as domain docs, glossary, context map or packaged domain-modeling template, and reports `missing domain model for complex domain` only when complex backend/workflow/enterprise/data-heavy/multi-service or multi-context signals make DDD applicable. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/domain-modeling.md` | Domain modeling template records `domain_model_when_complex_domain`, applicability, accepted gap, bounded context, ubiquitous language and invariant expectations. |
| 4 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Readiness eval includes `domain_model_when_complex_domain` as a conditional methodology gate. |
| 5 | `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | Planner stops before build when complex domain work lacks a domain-modeling artifact or accepted gap, and explicitly does not force DDD for simple CRUD/simple MVP work. |
| 6 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval includes `domain_model_gate_contract_present` for the packaged contract. |

Verification for the slice:

- Focused T8-A5 tests: 104 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 294 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A6` bounded context architecture traceability.

## Completed implementation slice: `T8-A6` bounded context architecture traceability

Scope: make bounded contexts actionable by requiring a trace from each domain context to an architecture boundary, not just a standalone DDD document.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_discovery.py`, `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Failing-first checks require architecture context-map discovery, `bounded_context_architecture_boundary_trace`, template fields, planner stop condition and fixture eval coverage. |
| 2 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Workspace audit treats `docs/architecture/context-map.md` and similar architecture/domain context docs as `domain_model` evidence without treating plain code folders as proof. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/domain-modeling.md` | Domain model template includes boundary id, architecture boundary and context-to-boundary traceability fields. |
| 4 | `plugins/product-agent-os/assets/templates/artifact-templates/architecture-overview.md` | Architecture overview template includes mapped bounded context and domain model boundary traceability. |
| 5 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Readiness eval includes `bounded_context_architecture_boundary_trace` as a methodology gate. |
| 6 | `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | Planner stops before build when a required domain model lacks context-to-boundary traceability or accepted gap. |
| 7 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval includes `bounded_context_trace_contract_present` for the packaged contract. |

Verification for the slice:

- Focused T8-A6 tests: 106 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 296 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A7` ubiquitous language traceability.

## Completed implementation slice: `T8-A7` ubiquitous language traceability

Scope: make ubiquitous language actionable by requiring domain terms to trace beyond a glossary into requirements, contracts, UI labels, code modules or owners.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_fixture_eval_runner.py` | Failing-first checks require `ubiquitous_language_traceability`, term-to-requirement, API/event/contract, UI label, code module or owner, domain expert review and fixture eval coverage. |
| 2 | `plugins/product-agent-os/assets/templates/artifact-templates/domain-modeling.md` | Domain modeling template includes a Ubiquitous Language Traceability table with accepted-gap and evidence-owner fields. |
| 3 | `plugins/product-agent-os/assets/templates/control-plane/PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` | Generated control-plane templates expose the language traceability gate for planning, checks, evals and run evidence. |
| 4 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Readiness eval includes `ubiquitous_language_traceability` as a methodology gate. |
| 5 | `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | Planner stops before build when required domain terms are untraceable, while simple CRUD/MVP work can still mark DDD not applicable. |
| 6 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval includes `ubiquitous_language_traceability_contract_present` for the packaged contract. |

Verification for the slice:

- Focused T8-A7 tests: 79 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 298 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A8` FSD structure routing.

## Completed implementation slice: `T8-A8` FSD structure routing

Scope: detect Feature-Sliced Design-like web UI structure as an optional routing signal without forcing FSD on backend, native, simple CRUD or simple MVP work.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_discovery.py` | Failing-first checks require positive `fsd_structure` detection and backend/native/simple CRUD false-positive protection. |
| 2 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Discovery reports optional `fsd_structure` only when enough FSD layer directories and UI component files are present. |
| 3 | `plugins/product-agent-os/assets/templates/artifact-templates/component-card.md` | Component card records FSD applicability, layer, slice, segment, public API, import rule and not-applicable reason. |
| 4 | `plugins/product-agent-os/assets/templates/workflows/development-standards.md` | Development standards explain conditional FSD routing and non-applicability for backend, native, simple CRUD and simple MVP work. |
| 5 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Readiness eval includes `fsd_structure_when_ui_architecture_applies` and `fsd_structure`. |
| 6 | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | Lifecycle skills treat FSD directory evidence as a clue, require component boundary evidence only when applicable, and stop before build on missing FSD boundary. |

Verification for the slice:

- Focused T8-A8 tests: 102 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 302 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A9` metric hardening.

## Completed implementation slice: `T8-A9` metric hardening

Scope: harden product behavior metrics so agents cannot treat a single proxy metric as product success without anti-Goodhart, privacy, retention and owner evidence.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_infrastructure_templates.py` | Failing-first checks require metric hardening terms in `metric-spec.md`, `release-packet.md`, generated control-plane templates and `project-readiness.json`. |
| 2 | `tests/product_agent_os/test_lifecycle_skills.py` | Lifecycle skills require metric hardening wording in `requirements-author`, `risk-reviewer` and `pr-release-operator`. |
| 3 | `tests/product_agent_os/test_fixture_eval_runner.py`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval exposes `metric_hardening_contract_present` for the `python-app` fixture. |
| 4 | `plugins/product-agent-os/assets/templates/artifact-templates/metric-spec.md` | Metric spec records `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input metric, counter-metric, proxy metric risk, guardrail, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence. |
| 5 | `plugins/product-agent-os/assets/templates/workflows/release-packet.md` | Release packet blocks product success claims from proxy metrics without counter-metric, guardrail, qualitative review and post-release review evidence. |
| 6 | Generated `REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG`, `project-readiness.json`, lifecycle skills and docs | Control-plane and skill contracts carry metric hardening into requirements, planning, review, release and runlog evidence. |

Verification for the slice:

- Focused T8-A9 tests: 83 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 304 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-A16` evidence-before-completion generalization.

## Completed implementation slice: `T8-A16` evidence-before-completion generalization

Scope: generalize evidence-before-completion beyond release packaging so ready/completed/fixed/works/release claims need current command/eval/runtime evidence, owner evidence, or an explicit inspection-only gap.

| Step | Artifact or code | Expected result |
| --- | --- | --- |
| 1 | `tests/product_agent_os/test_behavioral_workflow_evals.py` | Failing-first behavioral eval checks require `evidence-before-completion` route coverage and forbidden unsupported completion claims. |
| 2 | `tests/product_agent_os/test_infrastructure_templates.py` | Generated `release-packet.md`, `development-standards.md`, control-plane templates, readiness eval and behavioral eval carry the shared completion evidence contract. |
| 3 | `tests/product_agent_os/test_lifecycle_skills.py` | All Product-Agent OS lifecycle skills require `evidence_before_completion` wording for ready/completed/fixed/works/release claims. |
| 4 | `tests/product_agent_os/test_fixture_eval_runner.py`, `plugins/product-agent-os/scripts/run_fixture_eval.py` | Fixture eval exposes `completion_evidence_contract_present` for the `python-app` fixture. |
| 5 | `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json`, `project-readiness.json` | Behavioral and readiness evals include completion evidence fields, unsupported completion claim checks and inspection-only gap handling. |
| 6 | Generated `AGENTS/PLAN/TEST/EVALS/RUNLOG`, lifecycle skills and docs | Control-plane and skill contracts carry evidence-before-completion into planning, testing, evals, review, release and runlog evidence. |

Verification for the slice:

- Focused T8-A16 tests: 87 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 306 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 73.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-C` docs tooling selector.

## Completed implementation slice: `T8-C` docs tooling selector + `T8-A11`

Scope: implement stack-aware docs tooling selection and close the docs-as-code applicability gate.

Files touched:

| Area | Files | Purpose |
| --- | --- | --- |
| 1 | `plugins/product-agent-os/assets/templates/artifact-templates/docs-tooling-decision.md`, `plugins/product-agent-os/scripts/product_agent_os/templates.py` | Adds generated `.codex/artifact-templates/docs-tooling-decision.md`. |
| 2 | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Adds `docs_tooling_decision` with `docs_as_code_impact` status, selected/rejected tools, commands and approval-required items. |
| 3 | `plugins/product-agent-os/assets/templates/workflows/documentation-system.md`, `plugins/product-agent-os/assets/templates/evals/project-readiness.json`, generated control-plane templates | Makes docs tooling choices and T8-A11 statuses reviewable. |
| 4 | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`, `implementation-planner`, `test-eval-designer`, `risk-reviewer` | Routes lifecycle packets through `docs_tooling_selector`. |
| 5 | `tests/product_agent_os/test_infrastructure_templates.py`, `test_discovery.py`, `test_lifecycle_skills.py`, `test_fixture_eval_runner.py` | Adds focused RED/GREEN coverage for selector contracts, stack routing, docs-light false positives, approval-required docs actions and fixture eval. |

Verification for the slice:

- Focused T8-C tests: 122 tests with `OK`.
- Full plugin unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 312 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with renderer file count 74.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs checks: `python tools\check_docs.py` passed; strict MkDocs build exited `0` with `NO_MKDOCS_2_WARNING=1`.

Result: implemented on **2026-05-24**. The next slice was `T8-F` conditional readiness gates.

## Completed implementation slice: `T8-F` conditional readiness gates

Scope: make scenario, methodology and tooling readiness gates evaluable through explicit statuses instead of gate names alone.

Files touched:

| Area | Files | Purpose |
| --- | --- | --- |
| 1 | `plugins/product-agent-os/assets/templates/evals/project-readiness.json` | Adds `readiness_statuses`, transition rules and structured `conditional_readiness_gates` with applicability, pass condition, accepted gap, evidence, owner and residual risk. |
| 2 | `plugins/product-agent-os/scripts/run_fixture_eval.py` | Adds `conditional_readiness_gates_contract_present` fixture eval coverage. |
| 3 | Generated `AGENTS/PLAN/TEST/EVALS/RUNLOG` templates | Carries readiness status vocabulary into target project control-plane artifacts. |
| 4 | `workspace-discovery-auditor`, `implementation-planner`, `test-eval-designer`, `risk-reviewer`, `project-lifecycle-orchestrator` | Enforces that detection alone only supports `present_unverified` and that readiness needs evidence, owner, applicability reason and residual risk. |
| 5 | `tests/product_agent_os/test_infrastructure_templates.py`, `test_fixture_eval_runner.py` | Adds RED/GREEN coverage for the conditional readiness schema and fixture eval flag. |

Verification for the slice:

- RED check: conditional readiness tests failed on missing `readiness_statuses` and missing `conditional_readiness_gates_contract_present`.
- Focused T8-F tests: 88 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 313 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs check: `python tools\check_docs.py` passed.
- Strict MkDocs: `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict` exited `0`.

Result: implemented on **2026-05-24**. The next slice was `T8-H` scenario and eval docs.

## Completed implementation slice: `T8-H` scenario and eval docs

Scope: publish operator-facing docs for Track 8 scenario routing, behavioral evals and Codex-only compatibility.

Files touched:

| Area | Files | Purpose |
| --- | --- | --- |
| 1 | `docs/product-agent-os/scenarios.md` | Documents `usage_mode`, first response, minimum artifacts, approval boundary and verification gates for scenario routes. |
| 2 | `docs/product-agent-os/behavioral-evals.md` | Documents expected behavior, forbidden behavior, fixture eval, transcript/session eval strategy and residual risks. |
| 3 | `docs/product-agent-os/codex-compatibility.md` | Documents Codex App, CLI, IDE extension, `.codex-plugin`, skills, MCP, staged hooks and non-goals. |
| 4 | `mkdocs.yml`, `tools/check_docs.py`, Product-Agent OS docs, README, source registry and gap matrix | Adds pages to navigation, docs structure checks and source/status closure. |
| 5 | `tests/product_agent_os/test_product_agent_os_docs.py` | Adds RED/GREEN coverage for dedicated docs, navigation, required docs check and backlog closure. |

Verification for the slice:

- RED check: T8-H docs contract failed on missing pages, nav entries and registry/backlog closure.
- Focused T8-H docs tests: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 3 tests with `OK`.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 316 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs check: `python tools\check_docs.py` passed.
- Strict MkDocs: `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict` exited `0`.

Result: implemented on **2026-05-24**. The next slice was `T8-GY` transcript/session eval runner.

## Completed implementation slice: `T8-GY` transcript/session eval runner

Scope: add deterministic transcript/session replay beyond static behavioral JSON template validation.

Files touched:

| Area | Files | Purpose |
| --- | --- | --- |
| 1 | `plugins/product-agent-os/scripts/product_agent_os/transcript_evals.py` | Evaluates synthetic or redacted session transcripts against `behavioral-workflows.json`, expected terms, forbidden terms and privacy/no-secrets checks. |
| 2 | `plugins/product-agent-os/scripts/run_transcript_eval.py` | CLI wrapper with exit `0` for all-pass replay and exit `1` for missing evidence, forbidden behavior or privacy errors. |
| 3 | `plugins/product-agent-os/assets/eval-fixtures/transcripts/product-agent-os-synthetic-sessions.json` | Packaged synthetic sessions for greenfield approval, bug rescue no-repro stop, two-stage review and evidence-before-completion. |
| 4 | `tests/product_agent_os/test_transcript_session_evals.py`, `test_fixture_eval_runner.py`, `test_product_agent_os_docs.py` | RED/GREEN coverage for runner behavior, CLI exit codes, fixture eval contract and source/backlog closure. |
| 5 | Product-Agent OS docs, README, source registry and root control-plane files | Documents transcript/session replay and its deterministic, non-semantic residual risk. |

Verification for the slice:

- RED check: T8-GY focused suite failed on missing `product_agent_os.transcript_evals` and missing fixture eval contract key.
- Focused T8-GY transcript/fixture tests: `python -m unittest tests.product_agent_os.test_transcript_session_evals tests.product_agent_os.test_fixture_eval_runner -v` ran 14 tests with `OK`.
- Focused docs closure tests: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` ran 3 tests with `OK`.
- Transcript eval: `python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json` exited `0` with 4 sessions and 0 failures.
- Full unittest: `python -m unittest discover -s tests -p "test_*.py" -v` ran 320 tests with `OK`.
- Fixture eval: `python plugins\product-agent-os\scripts\run_fixture_eval.py` exited `0` with 35 fixtures, 0 failures and renderer file count 74.
- Codex compatibility: `python plugins\product-agent-os\scripts\validate_codex_compatibility.py` returned `status: compatible`.
- Docs check: `python tools\check_docs.py` passed.
- Strict MkDocs: `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict` exited `0`.

Result: implemented on **2026-05-24**. The next slice is `T8-B` standards trigger hardening.

## Non-goals

- Do not install external tools automatically.
- Do not turn Product-Agent OS into a multi-harness adapter. Track 8 checks only Codex App, CLI, IDE extension, `.codex-plugin`, bundled `skills`, Context7 MCP config and staged hook templates.
- Do not enable CI, hooks, CODEOWNERS, hosted docs, GitHub Actions or automations without explicit approval.
- Do not enable aggressive always-on skill triggers or session-start hooks without a staged proposal and explicit approval.
- Do not make Docusaurus, PlantUML, DBML, Storybook or any other tool mandatory for every project.
- Do not replace the runtime verification checklist with mere document presence.
- Do not move community claims into core guidance without source status and verification status.
- Do not start broad bug fixing without reproduction evidence, ownership boundary and rollback notes.
- Do not scaffold an empty project before explicit approval of the chosen product/architecture direction.
- Do not access external integrations, production DB, hosted docs, CI settings or secret-bearing configs without explicit approval.
- Do not publish packages, releases, tags, docs sites, GitHub changes or external tickets without explicit approval.
- Do not treat discovered logs, folders, package scripts or docs evidence as verified without a command, exit code and owner/reviewer evidence.

## Applicability model

Every methodology, standard or tool should receive one of these statuses instead of a boolean `present/missing`:

| Status | Meaning |
| --- | --- |
| `not_applicable` | Not needed for the current stack, scale or change. |
| `applicable_missing` | Needed but not found; requires a staged proposal or explicit gap. |
| `present_unverified` | Found, but the verification command is unknown or has not run. |
| `present_verified` | Found and backed by current verification/artifact evidence. |
| `proposal_staged` | A proposal is prepared but not applied to the project. |
| `approval_required` | Requires approval: external write, CI activation, hosted docs, DB access, secrets-sensitive operation. |
| `explicit_gap_accepted` | The gap is recorded and accepted by the owner as a temporary decision. |

## Usage mode model

`usage_mode` should be composite because real tasks often intersect multiple scenarios: for example, bug rescue inside a complex system or a security-sensitive API migration.

| Field | Meaning |
| --- | --- |
| `primary` | Main mode that determines the first response and minimum artifacts. |
| `secondary` | Additional modes that add gates without changing the primary workflow. |
| `confidence` | `low`, `medium`, `high`; at low confidence the plugin should ask a short clarifying question or choose a safe fallback. |
| `reasons` | 2-5 facts from the workspace/user prompt explaining why the mode was selected. |
| `fallback` | Safe mode when classification is disputed, usually `standard_feature` or `maintenance`. |
| `first_response_contract` | What the plugin says or asks on the first turn: selected mode, evidence gap, approval boundary and next smallest action. |
| `minimum_artifacts` | Minimum staged artifact set for the mode; advanced proposals appear only when needed or approved. |
| `behavioral_eval_cases` | Prompt/session fixtures proving correct route, stop condition and absence of forbidden behavior. |

Minimum initial modes:

```text
bug_rescue
greenfield_idea
complex_system_acceleration
pr_review
legacy_onboarding
api_migration
ai_eval_regression
native_mobile_feature
desktop_local_first
data_migration
security_sensitive_change
ci_stabilization
release_packaging
standard_feature
docs_only
maintenance
```

## T8-0. Test-first implementation scaffold

| Task | Files | Acceptance | Verification |
| --- | --- | --- | --- |
| Write failing tests for new artifact templates. | `tests/product_agent_os/test_infrastructure_templates.py` | Tests expect `acceptance-scenarios.md`, `ai-eval-spec.md`, `docs-tooling-decision.md` or the selected final set. | Focused unittest fails before implementation. |
| Write failing tests for new discovery signals. | `tests/product_agent_os/test_discovery.py` | Tests cover positive/negative cases for `domain_model`, `fsd_structure`, `docs_tooling`, `code_reference_docs`. | Focused unittest fails before implementation. |
| Write failing tests for readiness gates. | `tests/product_agent_os/test_infrastructure_templates.py` | `project-readiness.json` expects conditional gates for acceptance scenarios, domain model, FSD boundary, docs tooling decision and AI eval spec. | Focused unittest fails before implementation. |
| Write failing tests for scenario workflows. | `tests/product_agent_os/test_infrastructure_templates.py`, `tests/product_agent_os/test_discovery.py` | Tests expect usage mode classification and workflow templates for bug rescue, greenfield idea and complex integration acceleration. | Focused unittest fails before implementation. |
| Write failing tests for behavioral routing. | `tests/product_agent_os/test_behavioral_workflow_evals.py` or extension of `test_codex_runtime_runner_state_routes.py` | Prompt-like fixtures expect `usage_mode`, next skill, first response contract, stop condition and forbidden actions. | Focused unittest fails before implementation and captures false routes. |
| Write failing tests for transcript/session evals. | `tests/product_agent_os/test_behavioral_workflow_evals.py`, `plugins/product-agent-os/assets/templates/evals/behavioral-workflows.json` | Synthetic session cases check route -> staged artifacts -> evidence gaps -> no forbidden external activation. | Fixture eval shows expected pass/fail without contacting external systems. |
| Write failing tests for no-placeholder plan quality. | `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Plan/template checks reject placeholder tokens, vague steps, commands without expected result and slices without exact files. | Focused unittest fails on the current weak wording first. |
| Write failing tests for two-stage review. | `tests/product_agent_os/test_lifecycle_skills.py`, `tests/product_agent_os/test_infrastructure_templates.py` | Review workflow requires spec/acceptance compliance verdict first, then code quality/risk verdict. | Skill/template tests see both review stages and the stop condition when evidence is missing. |
| Write failing tests for Codex-only compatibility. | `tests/product_agent_os/test_plugin_structure.py`, `tests/product_agent_os/test_codex_compatibility.py` | Plugin checks cover `.codex-plugin`, Codex skills, Context7 MCP, Codex hook template staging and absence of required non-Codex manifests. | Focused unittest confirms Track 8 does not require Claude/Cursor/OpenCode/Gemini adapters. |
| Update fixture eval expectations. | `plugins/product-agent-os/scripts/run_fixture_eval.py` or existing fixture tests if count/assertions are pinned there. | Renderer includes new staged artifacts without direct project mutation. | Fixture eval after implementation returns all fixtures `ok: true`. |

## T8-A. Methodology gates

| ID | Methodology | Task | Plugin artifact | Acceptance | Eval/check | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| T8-A1 | Agentic / AI-native development | Clarify the task packet: ownership, forbidden files, approvals, run evidence, stop conditions, promotion path. | `development-standards.md`, lifecycle skills. | Every agent task packet contains evidence expectations and the promotion rule `manual -> skill -> plugin -> automation`. | Template tests or skill text checks. | Do not turn it into bureaucracy for mechanical edits. |
| T8-A2 | TDD | Add evidence contract for Red-Green-Refactor. | `RUNLOG.md`, `TEST.md`, `build-slice.md`. | Fields exist: failing test evidence, green evidence, refactor evidence or explicit accepted gap. | Template tests for required fields. | Not always applicable to docs-only or config-only changes. |
| T8-A3 | ATDD | Add `acceptance-scenarios.md`. | `.codex/artifact-templates/acceptance-scenarios.md`. | Trace `requirement -> scenario -> check -> evidence owner`. | Registry/template tests, fixture eval. | Do not duplicate `REQUIREMENTS.md`; the template should be a traceability artifact. |
| T8-A4 | BDD | Add behavior scenario format without dogmatic forcing. | `acceptance-scenarios.md`, `development-standards.md`. | Given/When/Then or equivalent, business rule, edge case, non-goal and evidence exist. | Template tests. | BDD does not replace unit, integration and contract tests. |
| T8-A5 | DDD | Introduce a conditional domain modeling gate. | `domain-modeling.md`, `project-readiness.json`, `implementation-planner` skill. | Complex backend/workflow/data-heavy projects require bounded context, ubiquitous language, invariant or accepted gap. | Eval gate + discovery test. | Do not force DDD on simple CRUD/MVP work. |
| T8-A6 | Bounded Context | Add `domain_model` signal and traceability to architecture boundary. | `discovery.py`, `domain-modeling.md`, `architecture-overview.md`, `project-readiness.json`, `implementation-planner`, fixture eval. | Discovery sees domain docs/glossary/context map; planner links context to boundary or accepted gap. | Discovery/template/lifecycle/fixture tests. | A `domain/` folder by itself does not prove DDD maturity; mapping still needs human architecture/domain review. |
| T8-A7 | Ubiquitous Language | Strengthen domain template traceability. | `domain-modeling.md`, `project-readiness.json`, `implementation-planner`, fixture eval. | Term maps to requirement/source, API/event/contract, UI label, code module or owner, or accepted gap. | Template/lifecycle/fixture tests. | Requires human domain expert review. |
| T8-A8 | FSD | Add optional `fsd_structure` signal and FSD boundary prompt. | `discovery.py`, `component-card.md`, `development-standards.md`, `project-readiness.json`, lifecycle skills. | Detection understands `app/pages/widgets/features/entities/shared`; planner requires public API/import boundary for growing UI only when applicable. | Focused T8-A8 discovery/template/lifecycle tests. | Do not apply to backend/native/simple CRUD/simple MVP work without UI architecture need. |
| T8-A9 | Data-informed development | Strengthen metric spec. | `metric-spec.md`, `release-packet.md`, generated control-plane templates, lifecycle skills, fixture eval. | `metric_hardening_when_product_behavior_changes`, North Star or primary value metric, input/counter metrics, guardrails, qualitative review, privacy classification, retention period, data minimization, owner signoff and post-release review evidence exist. | Focused T8-A9 template/lifecycle/fixture tests. | Metrics can still be wrong; product owner and post-release review are needed. |
| T8-A10 | Eval-driven AI development | Add AI/RAG eval spec. | `.codex/artifact-templates/ai-eval-spec.md`, `EVALS.md`, `TEST.md`. | Baseline, fixtures policy, no-secrets rule, task rubric, thresholds, rerun command and regression handling exist. | Template tests, fixture eval. | Eval quality depends on dataset and judge calibration. |
| T8-A11 | Docs-as-code | Close inside `T8-C`: introduce docs impact gate with applicability status. | `documentation-system.md`, `docs-tooling-decision.md`, `project-readiness.json`, generated `PLAN/TEST/EVALS/RUNLOG`, lifecycle skills. | Docs impact can be `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`; status must name evidence owner, commands, accepted gap or approval boundary. | Template/readiness/fixture tests inside `T8-C`. | Do not activate CI/CODEOWNERS, hosted docs, external sharing, DB introspection or docs publication without approval. |
| T8-A12 | Systematic debugging | Strengthen bug rescue through root-cause workflow. | `bug-rescue.md`, `bug-rescue-report.md`, `risk-reviewer` skill. | Before fixing there is symptom, expected/actual, reproduction evidence, boundary trace, hypotheses, eliminated causes and a stop condition for no-repro. | Behavioral eval + template tests for root cause phases. | Small bugs can be overloaded; the lightweight path should accept a one-command repro. |
| T8-A13 | No-placeholder implementation planning | Ban vague implementation steps in plan packets. | `implementation-planner` skill, `PLAN.md`, `build-slice.md`. | Every slice has exact files, explicit commands, expected result, rollback and evidence owner; no placeholder tokens, repeated-by-reference steps or vague validation. | Skill text tests + plan-quality behavioral fixture. | An overly detailed plan can slow trivial docs edits; it needs a `mechanical_change` exception with reason. |
| T8-A14 | Two-stage review | Split review into spec compliance and quality/risk. | `review-slice.md`, `risk-reviewer` skill, `RUNLOG.md`. | Review packet first checks acceptance criteria/source constraints, then checks code quality, tests, security, docs and release impact. | Template tests check two verdicts. | Doubles review overhead; apply to risky/parallel/public changes. |
| T8-A15 | Fresh-context subagent handoff | Clarify task packet for subagents. | `agent-team-designer` skill, `handoff-contract.md`, `worktree-ownership.md`. | Every subagent receives complete task context, owned files, forbidden files, expected verification evidence and handoff output schema. | Skill text tests + scenario fixture for complex acceleration. | Parallel work without ownership remains risky; default should be sequential when conflict exists. |
| T8-A16 | Evidence-before-completion | Record the final verification gate. | `release-packet.md`, `development-standards.md`, generated control-plane templates, lifecycle skills, readiness eval, behavioral eval, fixture eval. | Release/ready/completed/fixed/works claims are allowed only with current command evidence, current eval evidence, current runtime evidence or explicit inspection-only gap. | Focused T8-A16 tests, fixture eval `completion_evidence_contract_present`. | Quick opinions must be marked as inspection-only; evidence sufficiency still needs human review. |

## T8-B. Standards and specifications

| ID | Standard/spec | Task | Plugin artifact | Acceptance | Eval/check | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| T8-B1 | ADR/MADR | Add ADR trigger policy. | `adr.md`, `documentation-system.md`, `risk-reviewer` skill. | ADR required/proposed for architecture boundary, storage, API contract, auth/security, irreversible migration, automation activation. | Template/skill text tests. | Not every decision needs an ADR; `not_applicable` is needed. |
| T8-B2 | C4 | Clarify minimum diagrams by complexity. | `architecture-overview.md`, docs tooling decision. | Small: context/container optional Mermaid; larger: context/container expected; component/code only when useful. | Template tests. | Diagram rendering in the target repo depends on tooling. |
| T8-B3 | arc42 | Add architecture quality rubric. | `EVALS.md`, `architecture-overview.md`. | Architecture review includes goals, constraints, context, decisions, quality attributes and risks. | Eval/template tests. | Rubric is subjective; reviewer evidence is needed. |
| T8-B4 | OpenAPI | Clarify OpenAPI vs Swagger. | `api-contract-review.md`, docs tooling selector. | OpenAPI is source of truth; Swagger UI/tooling is optional renderer/editor/lint ecosystem. | Template tests. | Tool versions differ; no forced install. |
| T8-B5 | AsyncAPI | Add producer/consumer compatibility fields. | `api-contract-review.md`. | Event contract includes channel, message, payload schema, producer, consumer, ordering/idempotency and compatibility check. | Template tests. | Event semantics are often not fully expressible by schema. |
| T8-B6 | SemVer | Add version impact gate. | `release-packet.md`, `pr-release-operator` skill. | For plugin/package/API: major/minor/patch/not applicable with rationale. | Template tests. | SemVer applies only when public API/version contract exists. |
| T8-B7 | Keep a Changelog | Add human-readable release categories. | `release-packet.md`. | Added, Changed, Deprecated, Removed, Fixed, Security are used when relevant. | Template tests. | Do not turn it into a raw git log. |
| T8-B8 | CODEOWNERS | Add governance proposal status. | `documentation-system.md`, staged infrastructure notes. | CODEOWNERS status can be `present_verified`, `proposal_staged`, `approval_required`, `not_applicable`. | Discovery and template tests. | Requiring owners can slow small teams. |
| T8-B9 | GitHub Actions | Add least-privilege CI proposal fields. | CI/governance workflow section, docs tooling selector. | Proposed workflow names commands, permissions, triggers, owners, no external activation without approval. | Template tests. | External system side effects require approval. |

## T8-C. Documentation tooling selector

`T8-C` includes closure of `T8-A11`. The slice is not only a tool recommendation matrix; it must make docs-as-code impact evaluable through explicit applicability statuses and evidence. A workspace can select a lightweight/no-portal path when docs tooling is not justified, but the reason, owner and residual gap must be recorded.

Required status vocabulary for `docs_as_code_impact`: `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, `approval_required`.

| ID | Tool group | Task | Plugin artifact | Selection rule | Check proposal |
| --- | --- | --- | --- | --- | --- |
| T8-C1 | Docs portal | Add `docs-tooling-decision.md`. | `.codex/artifact-templates/docs-tooling-decision.md`. | Choose MkDocs, Docusaurus, Sphinx, Antora, Read the Docs, or none based on stack, repo topology, public docs, versioning need. | `mkdocs build`, `docusaurus build`, `sphinx-build`, `antora`, hosted approval note where applicable. |
| T8-C2 | MkDocs | Keep as simple Markdown default. | Docs tooling selector. | Small/medium repo, Markdown docs, simple static site, Python-friendly tooling. | Strict build if installed. |
| T8-C3 | Docusaurus | Recommend for React/MDX/product docs. | Docs tooling selector. | React/MDX-heavy docs, interactive pages, public docs, i18n/versioning needs. | Build command only if package script/tool exists. |
| T8-C4 | Sphinx | Recommend for Python reference docs. | Docs tooling selector, code reference docs routing. | Python package/library, public Python API, docstrings, API reference. | `sphinx-build` proposal, import-safety warning. |
| T8-C5 | Antora | Recommend for enterprise/multirepo AsciiDoc. | Docs tooling selector. | Multirepo/multiversion docs, AsciiDoc governance, larger org. | Antora build proposal only if tooling exists or approved. |
| T8-C6 | Read the Docs | Keep hosted docs as approval-bound option. | Docs tooling selector. | Public/open docs needing hosted builds/versioning. | `approval_required` for external hosting/sharing. |
| T8-C7 | OpenAPI/Swagger | Route HTTP API docs. | `api-contract-review.md`, selector. | HTTP API or SDK consumers. Swagger is UI/tooling around OpenAPI, not source of truth. | OpenAPI lint/build command slot. |
| T8-C8 | AsyncAPI | Route event/message docs. | `api-contract-review.md`, selector. | Queues, event bus, message-driven APIs. | AsyncAPI lint/docs build slot. |
| T8-C9 | Storybook | Route UI component docs. | `component-card.md`, selector, discovery. | Reusable UI components, design system, component states. | Storybook build, a11y/visual check if present. |
| T8-C10 | Mermaid | Default text diagrams. | `architecture-overview.md`, selector. | Markdown docs, simple diagrams, no heavy architecture-as-code need. | Docs build/render check. |
| T8-C11 | PlantUML | Optional UML/sequence diagrams. | Selector. | Team already uses PlantUML/UML or needs complex sequence/component diagrams. | PlantUML render proposal only if tool exists/approved. |
| T8-C12 | Structurizr DSL | Optional C4 architecture-as-code. | Selector. | Larger/multiservice systems needing C4 model, views, ADR/docs as code. | Structurizr validate/export proposal. |
| T8-C13 | DBML/dbdocs | Database docs lightweight path. | `database-dictionary.md`, selector. | Relational DB schema docs, readable schema dictionary. | DBML validation/docs proposal; no connection strings. |
| T8-C14 | SchemaSpy | Existing DB introspection path. | Selector/database docs workflow. | Existing relational DB where introspection is approved. | `approval_required` if DB access needed; no secrets in artifacts. |
| T8-C15 | TypeDoc/JSDoc | JS/TS reference docs. | Selector/code reference docs section. | Public TS/JS packages, SDKs, libraries. | TypeDoc/JSDoc build proposal if scripts exist. |
| T8-C16 | Sphinx/Javadoc/C# XML docs | Language-native reference docs. | Selector/code reference docs section. | Public Python/Java/.NET APIs. | Stack-specific docs build proposal. |
| T8-C17 | Vale/markdownlint | Optional docs quality lint. | Selector/docs governance section. | Public docs, regulated terminology, existing docs lint culture. | Proposal staged; no CI enablement without approval. |

## T8-CY. Codex-only compatibility contract

Track 8 borrows the idea of explicit runtime compatibility checks, but scopes it only to Codex. Product-Agent OS must not add or require Claude, Cursor, OpenCode, Gemini, Droid or generic multi-harness adapters.

| ID | Surface | Task | Plugin artifact | Acceptance | Eval/check | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| T8-CY1 | Codex plugin manifest | Harden `.codex-plugin/plugin.json` checks. | `.codex-plugin/plugin.json`, `test_plugin_structure.py`. | Manifest includes valid name/version/description, `skills`, optional MCP config, interface metadata and Codex-safe links. | Plugin structure tests. | Marketplace requirements may evolve; official Codex docs stay source of truth. |
| T8-CY2 | Codex App / CLI / IDE extension | Document supported Codex surfaces only. | `plugins/product-agent-os/README.md`, docs update. | README states Product-Agent OS supports Codex App, CLI and IDE extension workflows; no non-Codex install promises. | Docs check + keyword tests. | Different Codex surfaces may expose skills/tools differently; behavior must be framed by available capabilities. |
| T8-CY3 | Skills routing | Validate bundled Product-Agent OS skills. | `skills/*/SKILL.md`, `test_lifecycle_skills.py`. | Skill descriptions, triggers, boundaries, inputs, outputs, verification and failure modes are present. | Skill structure tests. | Trigger quality still needs behavioral prompt evals, not only text checks. |
| T8-CY4 | Context7 MCP | Keep Context7 as optional Codex MCP config. | `.mcp.json`, `README.md`. | MCP config remains secret-free and uses project/user configuration for any API key. | Plugin structure tests and source-policy validation. | Network and package availability vary; plugin cannot assume Context7 startup. |
| T8-CY5 | Staged hooks | Keep hook templates inactive by default. | `assets/templates/hooks/*`, `merge_infrastructure.py`. | Hooks can be staged and approved, but plugin does not silently activate session-start behavior. | Hook activation gate tests. | Users may manually activate hooks incorrectly; docs must state approval and rollback path. |
| T8-CY6 | Non-Codex adapter exclusion | Make absence of non-Codex manifests intentional. | `test_codex_compatibility.py`, README. | Tests fail if Track 8 requires `.claude-plugin`, `.cursor-plugin`, `.opencode`, Gemini extension or non-Codex install path. | Focused compatibility test. | Repo may contain unrelated docs about other ecosystems; test should target Product-Agent OS package only. |

## T8-CX. Usage scenario workflows

| ID | Scenario | Task | Plugin artifact | Acceptance | Eval/check | Residual risk |
| --- | --- | --- | --- | --- | --- | --- |
| T8-S1 | Bug rescue | Add workflow for users who are stuck in bugs after exploratory or vibe-coded work. | `.codex/workflows/bug-rescue.md`, optional `.codex/artifact-templates/bug-rescue-report.md`. | Workflow requires symptom, expected/actual behavior, reproduction command or manual repro, failing evidence, suspect boundary, files in/out of scope, regression test path, rollback notes. | Template tests check reproduction/evidence/rollback fields; discovery test can classify `bug_rescue` from failed tests/logs/user prompt context. | If no reproduction exists, plugin must stop at diagnosis packet, not pretend to fix. |
| T8-S2 | Greenfield idea | Add workflow for empty folder or idea-stage work before scaffold. | `.codex/workflows/greenfield-idea-to-plan.md`, optional `.codex/artifact-templates/greenfield-idea-brief.md`. | Workflow creates staged requirements, options, non-goals, first vertical slice, acceptance scenarios, metric spec, docs/tooling decision and approval gate before any scaffold. | Template tests check no-scaffold-before-approval language and first-slice fields. | Over-planning can slow small ideas; workflow must support lightweight mode. |
| T8-S3 | Complex system acceleration | Add workflow for experienced developers scaling web/API/integration-heavy systems. | `.codex/workflows/complex-system-acceleration.md`, `.codex/artifact-templates/integration-catalog.md`. | Workflow maps web/API/integration/DB/docs/eval slices, ownership boundaries, parallelization rules, external system contracts, integration risks and release gates. | Template tests check integration catalog, ownership, OpenAPI/AsyncAPI, DB/docs, release gates. | Risk of over-parallelization and conflicting file ownership. |
| T8-S4 | Usage mode classifier | Add explicit route before methodology gates. | `discovery.py`, runner route packet, `workspace-discovery-auditor` skill. | Audit returns `usage_mode` for base and extended modes, plus `route_inputs` separating intent hints, workspace signals and control-plane state. | Unit tests with synthetic workspaces, prompt-like inputs and fixture eval expectations. | Mode can be ambiguous; output must include confidence and fallback path. |
| T8-S5 | Scenario handoff packet | Standardize what each scenario hands to the next role. | lifecycle skills and workflow templates. | Handoff includes sources/context, assumptions, files touched/proposed, verification evidence, open risks, recommended next role. | Skill text tests or fixture eval checks for handoff contract. | Handoff packets can become verbose; keep scenario-specific minimums. |
| T8-S6 | PR review | Add workflow for reviewing changed files before merge. | `.codex/workflows/pr-review-readiness.md`, optional `.codex/artifact-templates/pr-risk-review.md`. | Workflow maps diff to behavior/API/DB/UI/security/docs/release risks, missing checks and review evidence. | Template tests for diff risk map, contract docs, release impact and commands. | Requires git/diff context; if absent, route to maintenance or standard feature. |
| T8-S7 | Legacy onboarding | Add workflow for old or undocumented repos. | `.codex/workflows/legacy-onboarding.md`, `.codex/artifact-templates/onboarding-map.md`. | Workflow creates source map, run commands, architecture/doc gaps and safe first documentation slice without refactor. | Template tests check runbook, docs debt map and `present_unverified` wording. | Discovery may infer too much from stale docs; mark unverified until commands run. |
| T8-S8 | API migration | Add workflow for changing HTTP/event contracts. | `.codex/workflows/api-migration.md`, `.codex/artifact-templates/migration-plan.md`. | Workflow covers OpenAPI/AsyncAPI, consumers, generated clients, backwards compatibility, deprecation, examples, release impact. | Template tests for contract/versioning/deprecation fields. | Internal APIs may still have external consumers; require owner review. |
| T8-S9 | AI eval regression | Add workflow for AI/RAG quality regression. | `.codex/workflows/ai-eval-regression.md`, `ai-eval-spec.md`. | Workflow requires baseline, dataset, rubric, thresholds, one-factor-at-a-time change and no-secrets fixtures. | Template/eval tests for baseline and dataset policy. | Eval judgments can be noisy; record confidence and residual risk. |
| T8-S10 | Native mobile feature | Add workflow for iOS/Android/native mobile changes. | `.codex/workflows/native-mobile-feature.md`. | Workflow covers permissions, offline states, simulator/emulator assumptions, screenshots/logs and platform build commands. | Template tests for runtime verification fields. | Tooling varies heavily; plugin should propose commands from detected project only. |
| T8-S11 | Desktop local-first | Add workflow for desktop apps with filesystem/local DB/background work. | `.codex/workflows/desktop-local-first.md`. | Workflow covers local data, filesystem permissions, indexing/background jobs, privacy, app logs and recovery path. | Template tests for local data/rollback/log fields. | Runtime verification is OS-specific; avoid claiming behavior from inspection only. |
| T8-S12 | Data migration | Add workflow for schema, backfill and retention changes. | `.codex/workflows/data-migration.md`, `migration-plan.md`, `database-dictionary.md`. | Workflow covers migration, rollback, data quality, PII/sensitive fields, retention and DB docs. | Template tests for migration/rollback/privacy fields. | Production DB access requires approval and secret-safe handling. |
| T8-S13 | Security-sensitive change | Add workflow for auth, permissions, payments, secrets or personal data. | `.codex/workflows/security-sensitive-change.md`, `.codex/artifact-templates/security-risk-review.md`. | Workflow covers threat surface, authn/authz, sensitive fields, abuse controls, approval needs and rollback. | Template tests for approval and no-secrets wording. | May require dedicated security scan outside Track 8 scope. |
| T8-S14 | CI stabilization | Add workflow for failing or flaky CI. | `.codex/workflows/ci-stabilization.md`, `.codex/artifact-templates/ci-stabilization-report.md`. | Workflow separates deterministic failure from flake, captures job/command/log/environment evidence and proposes smallest isolation. | Template tests for flake evidence and no external CI mutation. | Remote CI logs may need approval or connector access. |
| T8-S15 | Release packaging | Add workflow for package, SDK, plugin, app or open-source release readiness. | `.codex/workflows/release-packaging.md`, `.codex/artifact-templates/release-readiness.md`. | Workflow covers public API, SemVer, changelog, docs, examples, package metadata, license/security notes, publish approval and rollback. | Template tests for release gates and no-publish-without-approval wording. | Publishing/tagging is external/irreversible and must remain approval-bound. |
| T8-S16 | First-run route and intake | Add first response contract for initial plugin use. | `project-lifecycle-orchestrator` skill, `.codex/workflows/first-run-intake.md`. | First response states detected/assumed `usage_mode`, confidence, missing context, next smallest artifact and approval boundary instead of dumping all gates. | Behavioral prompt evals for empty, broken, existing and complex repos. | Too many questions can stall; plugin should ask only when confidence is low or write approval is needed. |

## T8-D. Discovery model

| Task | Files | Acceptance | Verification |
| --- | --- | --- | --- |
| Add `usage_mode` classification. | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Returns primary mode, secondary modes, confidence, reasons and fallback for all minimum modes. | Unit tests for empty workspace, failing-test workspace, monorepo/integration-heavy workspace, docs-only workspace, PR/diff-like workspace, native/mobile, desktop, data migration, CI and release packaging fixtures. |
| Add `methodology_applicability` map. | `plugins/product-agent-os/scripts/product_agent_os/discovery.py` | Done for T8-D: returns status packets per methodology/tooling gate, not only boolean signals. | Focused discovery tests for packet shape/status transitions and fixture eval check `methodology_applicability_contract_present`. |
| Add `domain_model` signal. | `discovery.py` | Done for T8-A5: detects domain modeling docs/templates/glossary/context map without treating any `domain/` folder as proof. | Positive/negative tests pass in focused T8-A5 suite. |
| Add `fsd_structure` signal. | `discovery.py` | Detects FSD-like UI folders and avoids false positive in backend-only repos. | Positive/negative tests. |
| Add `docs_tooling` detail object. | `discovery.py` | Reports `mkdocs`, `docusaurus`, `sphinx`, `antora`, `storybook`, `openapi`, `asyncapi`, `dbml`, `typedoc`, `javadoc`, `dotnet_xml_docs` where detectable. | Unit tests with synthetic files. |
| Add `code_reference_docs` signal. | `discovery.py` | Detects typedoc/jsdoc/sphinx/javadoc/dotnet doc config where practical. | Unit tests. |
| Add `release_policy` signal. | `discovery.py` | Detects changelog, version files, package metadata when available. | Unit tests. |
| Add `integration_surface` signal. | `discovery.py` | Detects API clients, webhook handlers, queue/event configs, env examples, integration docs and generated clients without reading secrets. | Unit tests with synthetic integration files and secret-safe fixtures. |
| Add `data_migration_signals`. | `discovery.py` | Detects schema, backfill, PII, sensitive fields, retention, rollback, validation, dry run and database dictionary clues as `present_unverified` until run evidence or owner evidence exists. | Unit tests with synthetic migration files, DBML/docs and no production data access. |
| Add `bug_reproduction_signals`. | `discovery.py` | Detects failing test artifacts/log files only when present in workspace and reports them as possible evidence, not truth. | Unit tests with test logs and no false positive on normal files. |
| Add `security_sensitive_surface`. | `discovery.py` | Detects auth, permission, payment, secrets, PII and external-write indicators without reading secret values. | Unit tests with synthetic auth/payment/env files. |
| Add `platform_runtime_surface`. | `discovery.py` | Detects mobile/native and desktop/local-first project signals separately from generic web/backend. | Unit tests for iOS/Android/Electron/Tauri/Swift/.NET desktop style files where practical. |
| Add `ci_failure_surface`. | `discovery.py` | Detects CI workflows and local CI/failure logs as possible evidence. | Unit tests for workflow files and synthetic failure logs. |
| Add `distribution_surface`. | `discovery.py` | Detects package/plugin/app release metadata, changelog, version files and publishing scripts without running them. | Unit tests for package metadata and release files. |
| Add `legacy_docs_debt_surface`. | `discovery.py` | Detects missing/stale docs signals through absence of README/control-plane/docs portal and mismatch between code stack and docs. | Unit tests for legacy fixture. |
| Add `codex_plugin_surface`. | `discovery.py`, `test_plugin_structure.py` | Detects `.codex-plugin`, bundled skills, `.mcp.json`, Codex hook templates and plugin README without expecting non-Codex manifests. | Unit tests for Product-Agent OS and negative fixtures with unrelated adapter files. |
| Add `behavioral_route_inputs`. | `discovery.py`, runner routes | Accepts prompt-like intent hints, workspace signals and current control-plane state as separate inputs for route classification. | Unit tests prove prompt intent cannot override safety/approval/source guards. |

## T8-E. Artifact templates

| Template | Purpose | Required fields | Tests |
| --- | --- | --- | --- |
| `acceptance-scenarios.md` | ATDD/BDD traceability before implementation. | Requirement id, scenario, business rule, actors, preconditions, behavior steps, edge cases, mapped check, evidence owner. | Template registry + keyword tests. |
| `ai-eval-spec.md` | Eval-driven AI/RAG baseline and thresholds. | App path, dataset source, no-secrets policy, baseline, rubric, assertions, judge policy, thresholds, rerun command, regression handling. | Template registry + no-secrets wording tests. |
| `docs-tooling-decision.md` | Stack-aware docs tooling choice. | Project profile, selected tools, rejected tools, applicability statuses, commands, approval needs, maintenance owner. | Template registry + selector coverage tests. |
| `governance-proposal.md` | Staged CI/CODEOWNERS/docs lint proposal. | Proposed artifact, reason, owner, permissions, trigger, commands, approval status, rollback. | Template tests for `proposal_staged` and `approval_required`. |
| `release-version-impact.md` or release packet extension | Changelog/SemVer impact. | User-visible changes, breaking changes, migration notes, version impact, release notes, rollback. | Template tests. |
| `bug-rescue-report.md` | Bug diagnosis and rescue evidence. | Symptom, expected/actual, reproduction, failing command, data-flow trace, hypotheses, eliminated causes, suspected boundary, regression test, fix scope, rollback, unresolved risks. | Template tests for reproduction, root-cause phases and rollback fields. |
| `greenfield-idea-brief.md` | Idea-stage product/architecture intake before scaffold. | Problem, users, options, selected direction, non-goals, first vertical slice, acceptance scenarios, metrics, approval gate. | Template tests for approval-before-scaffold language. |
| `integration-catalog.md` | Complex system integration map. | External system, owner, auth, data exchanged, rate limits, retry/idempotency, webhook/event contracts, observability, rollback, approval needs. | Template tests for auth/secrets/idempotency/observability fields. |
| `pr-risk-review.md` | Pre-merge risk map. | Changed files, behavior/API/DB/UI/security/docs/release impact, missing checks, reviewer questions, commands. | Template tests for impact areas and evidence fields. |
| `onboarding-map.md` | Legacy repo orientation. | Entry points, run commands, architecture map, docs debt, verification status, first safe slice. | Template tests for `present_unverified` and runbook fields. |
| `migration-plan.md` | API/data migration planning. | Current state, target state, compatibility, rollout, backfill, rollback, consumers, validation. | Template tests for compatibility and rollback fields. |
| `security-risk-review.md` | Sensitive change review. | Threat surface, authn/authz, secrets/PII, abuse controls, approvals, tests, rollback. | Template tests for no-secrets and approval fields. |
| `ci-stabilization-report.md` | CI/flaky test diagnosis. | Failing job, command, logs, frequency, deterministic/flaky classification, isolation plan, verification. | Template tests for failure evidence fields. |
| `release-readiness.md` | Release readiness evidence. | Public API, SemVer, changelog, docs, examples, package metadata, license/security notes, finish options, publish approval, rollback. | Template tests for SemVer/changelog/approval/finish-menu fields. |
| `agent-task-packet.md` | Fresh-context task handoff for subagents or parallel workers. | Goal, full context, owned files, forbidden files, assumptions, commands, expected evidence, stop conditions, handoff output. | Template tests for ownership, evidence and no-secrets wording. |
| `behavioral-eval-case.md` | Prompt/session eval specification for plugin behavior. | Prompt, workspace fixture, expected `usage_mode`, expected skill route, expected staged artifacts, forbidden actions, residual risk. | Template tests and fixture eval coverage. |
| `plan-quality-check.md` | No-placeholder plan review. | Exact files, concrete steps, commands, expected output, rollback, evidence owner, placeholder scan result. | Template tests reject vague placeholders. |
| `codex-compatibility-report.md` | Codex-only plugin compatibility evidence. | Codex surface, manifest status, skill status, MCP status, hook staging status, non-Codex adapter exclusion, checks run. | Plugin structure and compatibility tests. |

## T8-F. Readiness eval

| Gate | Applies when | Pass condition | Accepted gap |
| --- | --- | --- | --- |
| `acceptance_scenarios_when_behavior_changes` | User-facing behavior or business rule changes. | Scenario maps to test/eval/manual check. | Explicit gap in RUNLOG with owner. |
| `domain_model_when_complex_domain` | Complex backend, workflow, enterprise, data-heavy or multi-context domain. | Domain model exists or proposal staged. | Complexity judged low or gap accepted. |
| `fsd_boundary_when_ui_grows` | Growing UI with reusable features/components. | Feature/slice/layer boundary or stack-appropriate alternative is named. | Small MVP or non-UI project. |
| `ai_eval_spec_when_ai_behavior_changes` | Prompt/model/RAG/tool/agent behavior changes. | Baseline, dataset, threshold and rerun command exist. | Explicit accepted eval gap. |
| `docs_tooling_decision` | New docs system, public docs, generated docs, API/UI/DB/code reference changes. | Tooling decision exists with applicability statuses. | Not applicable documented. |
| `contract_docs_when_api_or_event_changes` | HTTP/event contract changes. | OpenAPI/AsyncAPI updated or proposal/gap recorded. | Internal-only prototype with accepted risk. |
| `db_docs_when_schema_changes` | Schema/migration/data model changes. | Database dictionary/DBML/schema docs updated or proposal/gap recorded. | No persistent schema touched. |
| `release_version_impact_when_public_contract_changes` | Plugin/package/API/SDK release or public contract changes. | SemVer/changelog impact named. | No public contract. |
| `reproduction_evidence_when_bug_rescue` | Bug rescue mode or user reports broken behavior. | Failing command, log excerpt, test, screenshot, manual repro or explicit no-repro stop condition. | No reproduction available; stop at diagnosis packet. |
| `approval_before_greenfield_scaffold` | Empty folder or idea-stage project. | Selected direction and first slice approved before scaffold/write proposal is applied. | User explicitly requests no scaffold and only wants research/spec. |
| `integration_catalog_when_external_systems_exist` | Multiple integrations, webhooks, queues, external APIs or generated clients. | Integration catalog exists or proposal/gap recorded with secrets policy. | Simple local-only project or no integration touched. |
| `ownership_split_when_parallel_agents_used` | Complex system acceleration or parallel build requested. | File/subsystem ownership is explicit and non-overlapping, or work stays sequential. | Parallelism not used. |
| `pr_risk_review_when_review_mode` | PR review mode or diff-focused request. | Changed areas, risks, missing checks and release/docs impact are named. | No diff/change context available. |
| `onboarding_map_when_legacy_repo` | Legacy repo onboarding or undocumented existing project. | Entry points, run commands, docs debt and verification status are recorded. | User only requested a narrow code change. |
| `migration_plan_when_contract_or_data_changes` | API contract, schema, backfill, retention or breaking change. | Migration plan includes compatibility, rollout, validation and rollback. | Prototype with no persisted data/public consumers. |
| `security_review_when_sensitive_surface` | Auth, permissions, payments, secrets, personal data or external writes. | Security risk review exists and approval needs are explicit. | No sensitive surface touched. |
| `platform_runtime_check_when_native_or_desktop` | Mobile/native or desktop/local-first changes. | Platform build/run/log/screenshot or simulator/manual check is named. | Docs-only or non-runtime change. |
| `ci_failure_evidence_when_ci_stabilization` | CI stabilization mode. | Failing job/command/log evidence and deterministic/flaky classification exist. | CI context unavailable; stop at local reproduction plan. |
| `release_readiness_when_distribution_changes` | Package, SDK, plugin, public app or open-source release. | Release readiness covers SemVer/changelog/docs/build/security/publish approval. | Internal-only unreleased work. |
| `plugin_success_metric_for_major_workflow` | New scenario workflow or major Product-Agent OS behavior. | Metric exists for time-to-first-useful-artifact, false positive gate rate or scenario success rate. | Experimental workflow explicitly marked. |
| `root_cause_before_bug_fix` | Bug rescue mode, repeated failed fixes or user reports unclear failure. | Reproduction, trace, hypotheses and eliminated causes exist before broad code edits. | One-line typo with obvious failing test can use lightweight path. |
| `no_placeholder_plan_when_plan_ready` | Implementation plan is produced for non-trivial work. | Plan has exact files, concrete steps, commands, expected outputs and no placeholder language. | Mechanical docs/config edits can record a reduced plan. |
| `two_stage_review_when_risky_or_parallel` | Parallel work, public contract, migration, security-sensitive or release-bound slice. | Review includes spec compliance verdict and quality/risk verdict. | Narrow low-risk slice can use single reviewer note with reason. |
| `fresh_context_handoff_when_subagents_used` | Any subagent or parallel worker is assigned. | Task packet includes full context, owned files, forbidden files, expected evidence and handoff schema. | Sequential inline execution can skip subagent packet. |
| `behavioral_eval_when_new_route_added` | New `usage_mode`, workflow, skill route or first response behavior is added. | Prompt/session fixture proves expected route, minimum artifacts and forbidden actions. | Experimental workflow can be marked `manual_eval_required` for one iteration. |
| `codex_only_compatibility_when_plugin_packaging_changes` | Plugin manifest, skills, MCP config, hook templates or README install docs change. | Compatibility report covers Codex App, CLI, IDE extension and `.codex-plugin`; non-Codex adapters remain out of scope. | Official Codex platform changes may require follow-up research. |
| `finish_options_when_release_ready` | PR/release packet is produced. | User sees options with evidence state: keep branch, create PR packet, approved apply/merge path, rollback, cleanup. | External publish/tag/PR still requires explicit approval. |

## T8-G. Lifecycle skill updates

| Skill | Update | Acceptance |
| --- | --- | --- |
| `workspace-discovery-auditor` | Output applicability statuses, richer docs tooling signals, Codex plugin surface and route inputs. | Handoff includes signals, statuses, missing gates, approval-required items, prompt intent hints and Codex-only compatibility notes. |
| `requirements-author` | Ask for acceptance scenarios and product metrics when behavior changes. | Requirements packet maps goals to scenarios and metrics or records gaps. |
| `implementation-planner` | Route slices through methodology gates conditionally and enforce no-placeholder quality for non-trivial plans. | Plan names methodology/tool applicability, exact files, concrete steps, commands, expected outputs, rollback and verification per slice. |
| `test-eval-designer` | Map scenario -> deterministic/manual/eval check and add behavioral prompt/session eval cases for new routes. | Every scenario has a check or accepted gap; every new route has expected mode, artifacts and forbidden behavior. |
| `risk-reviewer` | Review standards/tooling applicability, secrets risk, root-cause evidence, two-stage review requirements and approval requirements. | Finds over-forcing, missing docs contracts, unsafe DB/docs generation, weak evidence and skipped spec-compliance review. |
| `docs-maintainer` | Use docs tooling selector and source status policy. | Docs changes include build/lint/proposal status. |
| `pr-release-operator` | Add changelog, SemVer impact and finish options. | Release packet names user-visible changes, version impact, rollback and evidence-backed options; it cannot publish or tag without explicit approval. |
| `project-lifecycle-orchestrator` | Route by `usage_mode` and first response contract before assigning roles. | Bug rescue, greenfield, complex acceleration, docs-only and maintenance paths select different minimum artifacts and avoid dumping all gates on first contact. |
| `agent-team-designer` | Enforce ownership split and fresh-context task packets for complex acceleration. | Parallel agents receive non-overlapping files/subsystems, forbidden files, expected evidence and explicit merge/review handoff. |
| `reviewer` or equivalent review path | Support PR review, security-sensitive modes and two-stage review. | Review packets lead with findings, include spec-compliance verdict, quality/risk verdict, missing checks, release/security/docs impact and residual risk. |
| `release operator` path | Support release packaging mode and finish menu. | Release readiness offers evidence-backed keep/PR/merge/apply/rollback/cleanup options; external actions remain approval-bound. |
| Codex compatibility path | Validate Product-Agent OS only against Codex surfaces. | Plugin checks cover `.codex-plugin`, Codex App/CLI/IDE extension docs, bundled skills, Context7 MCP and staged hooks, without requiring non-Codex adapters. |

## T8-GX. Fixture and eval coverage

| Fixture | Purpose | Must prove |
| --- | --- | --- |
| `empty-idea-workspace` | Greenfield idea mode. | No scaffold before approval; staged idea brief and first slice. |
| `buggy-small-app` | Bug rescue mode. | Reproduction gate and bug rescue report are generated. |
| `complex-web-api-integrations` | Complex system acceleration. | Integration catalog, ownership split and contract docs gates. |
| `pr-review-api-db-change` | PR review mode. | PR risk review sees API, DB, docs and release impact. |
| `legacy-undocumented-repo` | Legacy onboarding. | Onboarding map and docs debt statuses are generated. |
| `api-migration-repo` | API migration. | Migration plan, OpenAPI/consumer/version gates. |
| `rag-quality-regression` | AI eval regression. | AI eval spec with baseline, no-secrets dataset policy and threshold. |
| `native-mobile-permissions` | Native/mobile feature. | Platform runtime check and permission/offline acceptance scenarios. |
| `desktop-local-indexer` | Desktop/local-first. | Local data, filesystem, indexing and rollback gates. |
| `data-migration-pii` | Data migration. | DB docs, PII, retention, validation and rollback gates. |
| `security-auth-payment` | Security-sensitive change. | Security risk review and approval-required status. |
| `ci-flaky-tests` | CI stabilization. | CI evidence, deterministic/flaky classification and no external mutation. |
| `package-release` | Release packaging. | SemVer, changelog, docs, build and no-publish-without-approval gates. |
| `first-run-intake` | Initial plugin launch. | First response chooses/asks for `usage_mode`, names confidence, missing context, next smallest action and approval boundary. |
| `behavioral-routing-prompts` | Prompt-only route tests. | User prompts map to expected route without needing a full workspace fixture. |
| `adversarial-skip-planning` | Prompt pressure to skip planning/tests/approval. | Plugin preserves required gates, marks unsupported shortcuts and does not mutate external systems. |
| `bug-three-failed-fixes` | Repeated failed bug attempts. | Plugin escalates from patching to root-cause/architecture re-check. |
| `no-placeholder-plan` | Plan quality. | Generated plan packet contains exact paths, commands, expected outputs and no placeholder language. |
| `two-stage-review-slice` | Review loop quality. | Review records spec-compliance verdict before quality/risk verdict. |
| `codex-plugin-compatibility` | Codex-only packaging. | `.codex-plugin`, skills, MCP and staged hooks validate; non-Codex adapters are not required. |
| `finish-branch-release-menu` | Release finish behavior. | Release packet offers evidence-backed finish options without publishing, tagging or opening PRs automatically. |

## T8-GY. Behavioral workflow eval coverage

Structural template tests prove files exist. Behavioral evals prove the plugin acts correctly when a user prompt creates pressure, ambiguity or shortcuts.

| Eval | Purpose | Inputs | Expected behavior | Forbidden behavior |
| --- | --- | --- | --- | --- |
| Route selection prompt eval | Check first route before work starts. | Prompt, optional workspace fixture, control-plane state. | Returns `usage_mode`, confidence, reasons, fallback and next skill. | Start editing before route/safety decision. |
| First-run response eval | Check first launch UX. | Empty, broken, mature and complex repo prompts. | Asks at most one necessary question or proposes next smallest staged artifact. | Dump full methodology matrix or scaffold without approval. |
| Explicit invocation eval | Check direct user requests. | Prompt naming a skill/workflow/mode. | Honors explicit route when safe and records why. | Let prompt override sandbox/source/approval guards. |
| Adversarial shortcut eval | Check pressure to skip gates. | Prompts like "just fix it", "no tests", "skip docs", "apply now". | Keeps minimal required evidence or records accepted gap. | Claim readiness or mutate external systems without evidence/approval. |
| Bug rescue behavior eval | Check root-cause discipline. | Failing tests/logs or user bug narrative. | Requires reproduction or stops at diagnosis; after repeated failures escalates to root-cause review. | Keep patching without reproduction or hypotheses. |
| Data migration behavior eval | Check database migration safety. | Schema/backfill/PII/retention prompt or workspace fixture. | Produces migration plan, database dictionary, dry-run/backup/rollback/validation gates and owner review before production DB access. | Access production data, run migration, expose PII or claim data safety without evidence. |
| Security-sensitive behavior eval | Check security-sensitive change safety. | Auth/payment/permission/PII prompt or workspace fixture. | Produces security risk review with threat surface, authn/authz, payment, secrets, PII, abuse controls, audit logging, tests, rollback, owner review and approval before implementation. | Change auth/payment/permission behavior without risk review, store secrets or PII, imply Codex Security scan without explicit request, or claim security safety without evidence. |
| Plan quality eval | Check no-placeholder planning. | Requirements and workspace audit packet. | Plan includes exact files, concrete steps, commands, expected outputs, rollback and evidence owner. | Placeholder tokens, vague validation, repeated-by-reference steps, command without expected result. |
| Two-stage review eval | Check review order. | Slice summary, diff summary, evidence packet. | Produces spec-compliance verdict first, then quality/risk verdict. | Treat generic code review as enough for risky work. |
| Fresh-context handoff eval | Check subagent task packets. | Complex/parallel plan. | Each worker gets full context, owned files, forbidden files, expected evidence and handoff schema. | Shared ownership ambiguity or missing stop conditions. |
| Finish options eval | Check release end state. | Ready release packet with evidence. | Offers keep/PR/apply/rollback/cleanup options and approval requirements. | Publish, tag, open PR or activate automation automatically. |
| Codex-only compatibility eval | Check packaging scope. | Product-Agent OS package. | Validates Codex App/CLI/IDE extension docs, `.codex-plugin`, skills, MCP and staged hooks. | Require or generate Claude/Cursor/OpenCode/Gemini adapters. |
| Cost/model budget eval | Check agent workflow cost discipline. | Agent team packet and risk profile. | Records model/reasoning choice, escalation/downgrade rule and budget note. | Default every role to maximum reasoning without rationale. |

## T8-H. Documentation updates

| Docs | Update |
| --- | --- |
| `docs/product-agent-os/development-standards.md` | Explain conditional methodology gates and applicability statuses. |
| `docs/product-agent-os/technical.md` | Add new templates, discovery signals, readiness gates and renderer outputs. |
| `docs/product-agent-os/architecture.md` | Update flow diagram if discovery/eval model changes materially. |
| `docs/product-agent/product-agent-os-plugin-spec.md` | Record Track 8 contract: tool selector, methodology gates, no silent installs. |
| `plugins/product-agent-os/README.md` | Summarize new Track 8 behavior for plugin users. |
| `docs/sources/development-methodology-gap-matrix.md` | Mark closed gaps after implementation with evidence. |
| `docs/product-agent-os/index.md` | Add user-facing explanation of bug rescue, greenfield idea and complex acceleration scenarios. |
| `docs/product-agent-os/scenarios.md` | Document all usage modes, first response, minimum artifacts, approval boundaries and verification gates. |
| `docs/product-agent-os/behavioral-evals.md` | Document prompt/session eval strategy, behavioral fixtures, forbidden behaviors and residual risks. |
| `docs/product-agent-os/codex-compatibility.md` | Document Codex-only support scope: Codex App, CLI, IDE extension, `.codex-plugin`, skills, MCP and staged hooks. |
| `docs/sources/product-agent-os-final-predevelopment-review.md` | Keep as final design review input and update only if pre-development assumptions change. |

## T8-I. Verification plan

| Check | When | Expected result |
| --- | --- | --- |
| Focused discovery tests | After `discovery.py` changes. | New signals/statuses pass positive and negative tests. |
| Focused infrastructure template tests | After template/eval registry changes. | New artifacts are registered and expected fields exist. |
| Full unittest | After any plugin code/template/test change. | `python -m unittest discover -s tests -p "test_*.py" -v` returns `OK`. |
| Fixture eval | After renderer/template changes. | `python plugins\product-agent-os\scripts\run_fixture_eval.py` exits `0`, all fixtures `ok: true`. |
| Docs check | After docs changes. | `python tools\check_docs.py` returns `OK`. |
| Strict MkDocs build | After nav/diagram/MkDocs-sensitive docs changes. | `$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict` exits `0`. |
| Scenario fixture eval | After scenario workflow or usage mode changes. | Each synthetic scenario fixture returns expected usage mode, staged artifacts and no forbidden external activation. |
| Behavioral route eval | After route, first-response, lifecycle skill or scenario behavior changes. | Prompt/session fixtures return expected route, confidence, next skill, minimum artifacts and stop condition. |
| Plan quality eval | After implementation-planner, `PLAN.md`, `build-slice.md` or task packet changes. | No-placeholder checks pass and every non-trivial slice has exact files, commands and expected outputs. |
| Two-stage review eval | After review workflow or `risk-reviewer` changes. | Review evidence includes spec-compliance verdict before quality/risk verdict. |
| Codex-only compatibility check | After plugin manifest, README, skills, MCP or hook templates change. | `.codex-plugin`, Codex skills, MCP and staged hooks validate; no non-Codex adapter is required. |
| Source registry check | After adding community or comparative sources. | `docs/sources/registry.md` includes trust level and verification status. |

## Recommended execution order

1. `[done]` `T8-0` failing tests for behavioral routing, Codex compatibility, base usage-mode routing and fixture expectations.
2. `[done]` `T8-GY behavioral workflow eval coverage` scaffold, including route, shortcut, review and Codex-only compatibility fixtures.
3. `[done]` `T8-S4 usage_mode` classifier matrix and route inputs.
4. `[done]` `T8-CY Codex-only compatibility contract`.
5. `[done]` `T8-S1` bug rescue with `T8-A12` systematic debugging.
6. `[done]` `T8-S2` greenfield idea workflow.
7. `[done]` `T8-S3` complex system acceleration.
8. `[done]` `T8-S4` extended usage-mode classifier fixtures and route inputs.
9. `[done]` `T8-S5` scenario handoff packet.
10. `[done]` `T8-S6` PR review workflow.
11. `[done]` `T8-S7` legacy onboarding workflow.
12. `[done]` `T8-S8` API migration workflow with `api-migration.md`, `migration-plan.md`, `api_migration_signals`, behavioral eval and lifecycle overlay.
13. `[done]` `T8-S9` AI eval regression workflow with `ai-eval-regression.md`, `ai-eval-spec.md`, `ai_eval_signals`, behavioral eval and lifecycle overlay.
14. `[done]` `T8-S10` native mobile feature workflow with `native-mobile-feature.md`, `native_mobile_signals`, behavioral eval and lifecycle overlay.
15. `[done]` `T8-S11` desktop local-first workflow with `desktop-local-first.md`, `desktop_local_signals`, behavioral eval and lifecycle overlay.
16. `[done]` `T8-S12` data migration workflow with `data-migration.md`, `data_migration_signals`, behavioral eval and lifecycle overlay.
17. `[done]` `T8-S13` security-sensitive change workflow with `security-sensitive-change.md`, `security-risk-review.md`, `security_sensitive_signals`, behavioral eval and lifecycle overlay.
18. `[done]` `T8-S14` CI stabilization workflow with `ci-stabilization.md`, `ci-stabilization-report.md`, `ci_stabilization_signals`, behavioral eval and lifecycle overlay.
19. `[done]` `T8-S15` release packaging workflow with `release-packaging.md`, `release-readiness.md`, `release_packaging_signals`, behavioral eval and lifecycle overlay.
20. `[done]` `T8-S16` first-run route and intake hardening.
21. `[done]` `T8-A13` no-placeholder planning hardening.
22. `[done]` `T8-A14` generalized two-stage review.
23. `[done]` `T8-A15` fresh-context handoff.
24. `[done]` `T8-A3`, `T8-A4`, `T8-E acceptance-scenarios`.
25. `[done]` `T8-A5` conditional DDD/domain model gate.
26. `[done]` `T8-A6` bounded context architecture traceability.
27. `[done]` `T8-A7` ubiquitous language traceability.
28. `[done]` `T8-A8` FSD structure routing.
29. `[done]` `T8-A9` metric hardening.
30. `[done]` `T8-A10 ai-eval-spec`; AI eval route, workflow, artifact, signals and behavioral case are implemented.
31. `[done]` `T8-A16` evidence-before-completion generalization.
32. `[done]` `T8-C docs tooling selector` with `T8-A11` docs-as-code applicability gate closure.
33. `[done]` `T8-GY transcript/session eval runner` with deterministic replay, CLI wrapper, synthetic transcript fixture, no-secrets/privacy guard and fixture eval contract.
34. `[done]` `T8-D docs_tooling/integration/security/platform/ci/distribution/codex_plugin` discovery model. Base usage-mode route inputs, `domain_model`, `fsd_structure`, `docs_tooling_decision`, `methodology_applicability`, API migration signals, AI eval signals, native mobile signals, desktop local signals, data migration signals, security-sensitive signals, CI stabilization signals and release packaging signals are implemented.
35. `[done]` `T8-F readiness eval` conditional gates, including scenario, methodology and tooling readiness statuses.
36. `[done]` `T8-B standards trigger hardening`, including ADR/C4/arc42/OpenAPI/AsyncAPI/SemVer/Keep a Changelog/CODEOWNERS/GitHub Actions trigger rules, `governance-proposal.md`, readiness gate and fixture eval contract.
37. `[done-for-current-scope]` `T8-G` lifecycle skills, including orchestrator, reviewer, release, agent-team, docs tooling, standards trigger policy, conditional readiness and Codex compatibility routing.
38. `[done]` `T8-GX` scenario fixture eval coverage, including backend/native FSD false-positive fixtures, simple CRUD DDD false-positive fixture, docs-light no-portal fixture, hosted docs/DB introspection approval fixture and no-secrets checks.
39. `[done]` `T8-H` system docs and generated control-plane templates are synced through T8-D; dedicated scenarios/behavioral-evals/Codex-compatibility docs, source registry closure notes and source/gap matrix updates are present.
40. `[done-for-current-slices]` `T8-I` full plugin verification; focused T8-D, full unittest, fixture eval, transcript eval, compatibility, docs check and strict MkDocs are clean.

## Rollback

- Template rollback: remove template file, template registry entry, generated fixture expectation and related tests.
- Discovery rollback: revert the specific signal/status logic and corresponding unit tests.
- Eval rollback: remove only new gates from `project-readiness.json` and tests that assert them.
- Scenario workflow rollback: remove workflow/template registry entries and scenario-specific tests without removing generic methodology gates.
- Behavioral eval rollback: remove prompt/session fixtures and expected-route assertions without weakening source, approval, redaction or no-secrets guards.
- Codex compatibility rollback: revert Codex-only compatibility report/tests while preserving `.codex-plugin` manifest and existing plugin packaging.
- Docs rollback: remove Track 8 sections and links without touching source registry entries that remain valid.
- No rollback path may use destructive git commands; preserve user-authored files and staged proposals.
