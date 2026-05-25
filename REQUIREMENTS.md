# REQUIREMENTS.md

<!-- product-agent-os:start requirements -->
Project: Codex Docs / Product-Agent OS
Generated at: 2026-05-25

## Goal

- Развить Product-Agent OS plugin из набора agentic workflow в воспроизводимый engineering operating system для Codex App, CLI и IDE extension.
- Поддерживать разработку проектов разной сложности через staged artifacts, methodology gates, tests/evals, source policy, approvals and human ownership.

## Current Slice

- Last completed slice: `T9-D2` Requirements & Domain methodology integration.
- Active planning artifact: `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Next slice: `T9-D3` Solution Architecture methodology integration.
- Current route: long-running plugin/skill/docs/evals work.
- Scenario status: Track 9 foundation, Business/Product and Requirements/Domain slices are implemented. Track 9 continues domain-by-domain from `T9-D3`.

## Scope

- Product-Agent OS implementation package: `plugins/product-agent-os/`.
- User-facing docs: `docs/product-agent-os/`, `docs/product-agent/`, `docs/sources/`.
- Track 9 methodology sources: `docs/methodologies/`.
- Track 9 plan: `docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md`.
- Project control-plane files: `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`.
- Verification: unit tests, fixture eval, Codex compatibility, docs check, strict MkDocs build when docs/nav-sensitive changes are made.

## Non-Goals

- Do not activate hooks, automations, GitHub Actions, external publishing, schedules or package registry mutations without explicit approval.
- Do not treat community claims as durable rules without trust level and verification status.
- Do not force DDD/FSD/docs tooling where the workspace does not justify it.
- Do not mutate target workspaces directly from Track 3 renderer; use dry-run/staged output and approval boundaries.

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
- `docs-maintainer` is now a packaged lifecycle skill for requirement IDs, source registry, glossary/ubiquitous-language and traceability docs after the requirements packet exists.

## Assumptions

- Official OpenAI documentation remains source of truth for Codex App, CLI, IDE extension, subagents, skills, AGENTS.md, memory, sandbox, approvals and MCP.
- Context7 may be used as retrieval layer, but official status depends on the underlying source.
- Root control-plane files describe this repository's active Product-Agent OS implementation work, not generated target-project assets.
<!-- product-agent-os:end requirements -->
