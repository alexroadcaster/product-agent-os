# Development Standards Workflow

Project: {project_name}
Profile: {profile_name}
Detected stack: {detected_stack_text}

## Purpose

Use this workflow when a feature is larger than a mechanical edit and needs a source-grounded product, architecture, test, implementation, review, and measurement loop.

## Standard Loop

1. Product hypothesis: define user value, success metric, non-goals, privacy constraints, and rollback expectation.
2. Architecture boundary: choose the smallest coherent slice and the stack-appropriate structure before implementation.
3. Test-first specification: write or update acceptance tests, contract tests, fixture tests, or eval cases before behavior changes; for deterministic code, prefer a visible Red-Green-Refactor loop.
4. Professional code authoring: for non-mechanical code work, apply `.codex/workflows/coding-standards.md` and fill `.codex/artifact-templates/coding-standard-checklist.md` or record `not_applicable` with reason.
5. Agentic implementation: give the builder a bounded task packet with owned files, forbidden files, commands, coding-standard checklist status, and stop conditions.
6. Human review and quality gate: review architecture, security, data handling, docs, command evidence, leverage decision, dependency decision, and unsupported code-quality claims before release.
7. Evidence-before-completion: apply `evidence_before_completion` before any ready claim, completed claim, fixed claim, works claim, or release claim.
8. Post-release measurement: compare real metrics, support signals, defects, latency, cost, and user feedback against the hypothesis.
9. Learning loop: record decisions, failures, reusable methods, and candidate rules in `RUNLOG.md` before promoting them.

## Architecture Boundary

- Web UI: prefer feature slices, route or page boundaries, component states, and a clear dependency rule.
- Web UI with `fsd_structure`: use Feature-Sliced Design only when the workspace already shows `app`, `pages`, `widgets`, `features`, `entities`, and `shared` layer directories or the owner explicitly chooses it; record layer, slice, segment, public API, and import rule in `component-card.md`.
- FSD is not applicable by default for backend, native, simple CRUD, or simple MVP work; record `not applicable` or an accepted gap instead of forcing Feature-Sliced Design.
- Mobile UI: prefer feature or flow modules, explicit permission and offline states, and simulator/device verification.
- Desktop UI: isolate filesystem, local database, indexing, privacy, and long-running background work.
- Backend/API: define service responsibility, public contracts, data ownership, idempotency, error paths, and migration boundaries.
- AI/RAG: define retrieval path, prompt/model boundary, eval dataset, grounding rules, latency, cost, and regression threshold.

## Test-First Options

- Unit tests for deterministic logic, parsers, validators, formatters, permissions, and time handling.
- Red-Green-Refactor proof for new behavior and defect fixes: failing test first, minimal implementation, cleanup while tests stay green.
- ATDD or BDD-style acceptance scenarios when behavior spans user, tester, and product perspectives.
- For behavior changes, fill `.codex/artifact-templates/acceptance-scenarios.md` or record an explicit gap before implementation.
- Acceptance scenarios use `requirement -> scenario -> check -> evidence owner`.
- Given, When, Then or an equivalent behavior format captures the business rule, edge case, non-goal, and evidence owner without turning BDD into dogma.
- Integration tests for service boundaries, storage, queues, importer-indexer-searcher paths, and external adapters.
- Contract tests for OpenAPI, AsyncAPI, database schemas, SDK interfaces, and generated clients.
- Evals for AI answer quality, retrieval quality, grounding, hallucination risk, UX judgment, and documentation quality.
- Runtime or visual checks for UI, native app behavior, browser flows, screenshots, logs, traces, and accessibility.

## Agent Task Packet

- Goal:
- Product hypothesis:
- Success metric:
- Architecture boundary:
- Files in scope:
- Files out of scope:
- Tests or evals to create first:
- Commands to run:
- Documentation to update:
- Security and data constraints:
- Coding-standard checklist status:
- Existing-capability scan:
- Selected leverage path:
- Dependency decision:
- Unsupported code-quality claims:
- Approval needs:
- Stop conditions:

## Professional Code Authoring

- Use `.codex/workflows/coding-standards.md` for non-mechanical code authoring, refactoring, defect fixes, generated-code edits, dependency changes, and high-risk domain changes.
- Record `.codex/artifact-templates/coding-standard-checklist.md` or `not_applicable` for docs-only, read-only, formatting-only, or tiny mechanical edits.
- Prefer delete/configure/standard library/framework/platform/current dependency/project helper before custom code.
- Require `one_line_candidate` for small behavior where an existing API, helper, selector, schema option, CLI flag, config key, or framework primitive may solve it.
- Require `negative_dependency_rule` before proposing a new dependency.
- Require `deep_module_check` before touching shared modules, public contracts, generated code, data models, runtime behavior, cache/concurrency, or cross-boundary code.
- Require `legacy_seam_check` and characterization evidence before legacy refactoring or rewrite proposals.
- Keep comments focused on non-obvious intent, invariants, tradeoffs, security/data/migration/concurrency risk, and compatibility constraints.

## Review Gate

- The slice matches the product hypothesis and stated non-goals.
- Architecture changes stay inside the named boundary or have an ADR proposal.
- Behavior changes have deterministic tests, evals, or an explicit documented gap.
- Non-mechanical code work has a coding-standard checklist or a clear `not_applicable` reason.
- New custom code has an existing-capability scan, selected leverage path, rejected alternatives, and tests/evals or an accepted gap.
- New dependencies have a dependency decision, owner, risk note, rollback/removal path, and approval status.
- API, event, database, UI, and user-facing changes update their source-of-truth docs.
- Command evidence includes exit code, relevant output, artifacts inspected, and residual risk.
- Ready claim, completed claim, fixed claim, works claim, and release claim cite current command evidence, current eval evidence, current runtime evidence, owner evidence, or an explicit test gap.
- Inspection-only work stays labeled `inspection-only` and lists every unsupported completion claim.
- Completion claim without current evidence is blocked.
- Security, privacy, performance, migration, and rollback risks are named.

## Evidence Before Completion

- Gate: `evidence_before_completion`
- Ready claim:
- Completed claim:
- Fixed claim:
- Works claim:
- Release claim:
- Current command evidence:
- Current eval evidence:
- Current runtime evidence:
- Inspection-only:
- Explicit test gap:
- Unsupported completion claim:
- Completion claim without current evidence:

## Outputs

- Updated `REQUIREMENTS.md` hypothesis and acceptance criteria.
- Updated `.codex/artifact-templates/acceptance-scenarios.md` mapping, or an explicit gap, when behavior changes.
- Updated `PLAN.md` slice, ownership, rollback, and verification gates.
- Updated `TEST.md` deterministic checks and manual/runtime checks.
- Updated `EVALS.md` subjective or AI quality rubrics and thresholds.
- Updated `RUNLOG.md` evidence, failures, decisions, and post-release measurement plan.

## Stop Conditions

- User value or success metric is unclear.
- Architecture boundary is not named.
- No test-first or eval-first path exists and the gap is not explicitly accepted.
- Non-mechanical code work lacks coding-standard checklist status or `not_applicable` reason.
- New custom code or dependency is proposed without existing-capability scan and rejected alternatives.
- The requested work touches security, auth, payments, personal data, production migrations, or external writes without approval.
- The task asks for active automation before manual stability evidence exists.
- A ready claim, completed claim, fixed claim, works claim, or release claim would be made from inspection-only evidence without an explicit test gap.
