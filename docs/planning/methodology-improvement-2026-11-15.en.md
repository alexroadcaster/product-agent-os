# Product-Agent OS — methodology improvement plan

Source status: repository_source / owner_requested_planning / proposed_methodology_improvements; implementation_not_started.
Date: 2026-11-15. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Goal, authority and ownership

This plan defines 18 concrete tasks for Spec-Driven Development (Spec-DD), Design-Driven Development (Design-DD), Test-Driven Development (TDD), Agentic-Driven Development (ADD) and incremental Feature-Sliced Design (FSD). Every task is planned with pending_execution_timestamp. Only this plan, JSON, its full English counterpart and planning/control-plane/source pointers are authorized. This request does not authorize implementation, new active instructions, runtime/browser/provider calls, installation, Git or publication.

[JSON state](methodology-improvement-2026-11-15.json) owns status/priority/dependencies; synchronized RU/EN cards own descriptions and AC. Update them together; tables are indexes, not another queue. [Russian](methodology-improvement-2026-11-15.md). METH improves the development process; FUNC/Web/V3 retain functional scope and status. Authoring this plan completes no METH task.

## Baseline and evidence

Source snapshot: git HEAD `35458110145d928b9b14d9312b60d852f11f6e88`; hashes of seven inspected implementation/test owners are in JSON. This is not release qualification. Planning inspected source/owners; historical test/browser/native receipts were not rerun.

- [FUNC-G01](functional-remediation-2026-11-15.md#func-g01-results) has seven implemented tasks on this baseline: F01/F03–F08; the other 27 FUNC tasks are planned. This is owner state, not a new test result. Do not replan the repaired draft/dashboard/contract behaviors.
- Spec-DD already appears in [requirements and capabilities](../product/capabilities.md) and concrete matrices; [TEST](../../TEST.md) and [EVALS](../../EVALS.md) own verification selection and claim ceilings.
- Design-DD has [DESIGN](../../DESIGN.md), V3 coverage and the [implementation plan](2026-11-13-v3-ui-implementation-plan.md). Historical V3 review identified a composition-coverage gap; this does not assert a new defect in the current build.
- TDD has rules and individual historical RED/GREEN receipts; completed tests cannot prove test-first ordering for every task.
- ADD has build/review/handoff contracts and ownership separation. Better agentic quality/cost requires a comparable baseline rather than role counts.
- The frontend has feature folders, but dashboard/tasks/team/workflows import sibling internals. Strict FSD is not established; the [contract-boundary test](../../tests/web/contracts-boundaries.test.mts) protects application boundaries, not every FSD import. METH-09 must explicitly cover TSX and aliases to avoid hidden coverage gaps.

Sources: `apps/web/src/features/dashboard/model.ts`, `tasks/TaskManager.tsx`, `workflows/WorkflowManager.tsx`, `team/TeamManager.tsx`, `apps/web/src/ui/App.tsx`; Python owner `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`. Read their current state again before future edits.

Methodology primary sources checked in the preceding analysis on 2026-11-15: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html), [FSD layers](https://feature-sliced.design/docs/reference/layers), [FSD public API](https://feature-sliced.design/docs/reference/public-api), [Spec Kit process](https://github.github.io/spec-kit/quickstart.html), [IBM human-centered design](https://www.ibm.com/training/enterprise-design-thinking/framework), [AWS AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/). ADD/Design-DD are explicitly scoped working approaches here, not assertions of a single industry standard. Proposals and judgments below are project-authored, not external research results.

## Priorities, stages and dependencies

P1 protects contracts and acceptance evidence; P2 is the main bounded pilot/process improvement; P3 is optional evidence-gated scaling. P1 does not mean a production incident. Task numbers are not execution order.

| Stage | Tasks | Exit condition |
| --- | --- | --- |
| A. Baseline and contracts | METH-01–06 | Ownership/AC/states/TDD gaps and a bounded agent contract; active rules change only in later separate slices |
| B. FSD foundation | METH-08–11 | Accepted architecture decision, import ratchet and minimal shared/entity APIs without mass moves |
| C. Sequential pilots | METH-12, METH-13; then METH-07 | Dashboard → tasks → workflows; reversible checkpoints and an honest outcome-comparison ceiling |
| D. Acceptance and decision | METH-17 → METH-18 | Bounded pilot verdict and separate go/bounded_go/hold/stop |
| E. Optional expansion | METH-14–16 | Selected areas after go; not required for pilot acceptance |

Start with METH-01, then independent METH-02 and METH-08 branches. Structural critical chain: 01 → 08/05 → 09 → 10 → 11 → 12 → 13 → 17 → 18. The design branch 02 → 03 → 04 enters 12. The agentic branch 06 + 12 → 07 enters 17. JSON depends_on defines the full DAG; Blocks is its reverse. Only task dependencies gate a start; finishing an entire stage is not another prerequisite.

## Relationship to the existing backlog

| Existing owner | Reuse | No duplicate ownership |
| --- | --- | --- |
| F01/F03–F08, FUNC-G01 | Baseline and regression protection | Fixes, native qualification and completion state |
| F02/F28 | References for future artifact traceability/canonical paths | Task↔artifact links and inventory; METH-02 does not wait for F28 |
| F11/F12/F16 | Metric/team/skill limitations | Telemetry, external search and actually loaded-profile proof |
| F18/F20/F30 | Refresh/performance/engine boundaries | Refresh changes, benchmarking or mandatory dependency-cruiser installation |
| F19/F21/F22/F23/F24, UI-12 | Reusable scenarios/evidence and separate full/human acceptance | Full E2E, recovery, backup/restore, feature availability and human acceptance |
| F25, DOCS-01–16 | Canonical documentation/status ownership | Recreating guides or changing feature task-state |
| F14/F26–34, M5 | Migration-scope exclusions | New Files/Map/Database/usages or hosting/auth/team capabilities |

external_refs are references and ownership constraints, not new edges in another DAG. The current FSD pilot prerequisite F08 is implemented; recheck it before edits and recheck F01 when pinned runtime sources are affected. Shared-file conflicts require sequential writes, not invented functional dependencies.

## Proposed incremental FSD boundaries

This is a proposal for METH-08, not an accepted ADR:

- `app` owns composition/global providers/session/project scope; `pages` own screen composition; add `widgets` only for useful standalone reusable blocks.
- `features` own actual user interactions; `entities/task` owns task projections/selectors/presentation; `shared` owns non-domain primitives/infrastructure.
- Do not create empty layers. Define public APIs/import rules before moving confirmed scope. Keep shared business contracts in `packages/contracts`; do not apply frontend FSD to Python/backend.
- Allow legacy→new compatibility bridges with a single implementation/state and a removal owner; migrated code cannot import legacy internals. No blanket exceptions or wildcard exports.
- Start by preventing new violations against a revision-pinned legacy baseline; migrated scope has zero unresolved violations. Tighten the ratchet after every accepted checkpoint.
- Stopping after dashboard or tasks/workflows retains a working pilot and an explicit legacy remainder. Other screens are not prerequisites for delivering functional fixes.

## Future task verification

These profiles propose task acceptance. TEST.md retains the current verification route and is unchanged by this plan.

| Profile | Minimum evidence |
| --- | --- |
| V-PLAN | Semantic/source/link review and `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <changed-plan>`; changed-path docs checks from TEST; DAG/MD–JSON/RU–EN parity; no runtime claims |
| V-TDD | Existing risk/check inventory and focused regression for new tests; observable expected RED only for behavior changes, GREEN and scoped refactor evidence; no artificial RED for docs/moves |
| V-BOUNDARY | `node --test tests/web/contracts-boundaries.test.mts` with meaningful parser/import positives and negatives; alias resolution, TSX and remaining exceptions; additional checks by affected contract |
| V-WEB | Focused current-consumer Node tests, `npm run check:web-m1`, `npm run build:web`; synthetic current-build browser/visual/keyboard checks for the changed journey in both themes; native/recovery only when relevant |
| V-ADD | Baseline/candidate on named representative/negative cases; explicit self-review or separately authorized independent review; deterministic correctness separate from actual model quality and activation |
| V-PLUGIN | Focused `tests.product_agent_os.test_methodology_audit` and `test_methodology_catalog`, affected fixture/eval scenarios selected by TEST; routing baseline comparison; no target/provider mutation |
| V-INTEGRATED | Combined pilot state: affected integrations, source/build/harness provenance, visual/state coverage and findings disposition; full suites only for TEST triggers; separate human acceptance |

New dependencies/installation, active durable prompts/rules, hooks/trust, actual models/providers, target workspaces, Git/publication and production require applicable separate authority. A future local implementation request does not automatically authorize these actions. Use existing temporary synthetic profiles; do not persist pairing/session material, secrets or private raw chats.

## Metrics, stopping and rollback

Baseline/pilot metrics: unauthorized import edges, meaningful regression findings, reopened tasks, repair cycles, owner interventions and elapsed time with provenance. Tokens/cost require reliable observations; missing data is not zero. Do not claim better agent time/quality/cost without comparable actual-agent evidence.

Mandatory minimum: zero new unauthorized edges, zero unresolved critical pilot regressions and evidence for every mandatory pilot AC. Define other thresholds/measurement windows before the candidate run in METH-01/07. Judge FSD by change localization, review effort and maintainability, not folder, test or agent counts.

Stop for draft/data loss, scope/approval violations, unverifiable aliases, missing material baselines, unclear source ownership, concurrent-write conflicts or a need to expand authority. Roll back only owned hunks/checkpoints while preserving public compatibility/user data; no destructive Git or DB operations. Changed pinned runtime sources require qualification through current TEST rather than mechanically replaced hashes.

## Plan-preparation verification — 2026-11-15

This checks the planning artifact, not execution of METH tasks. Review mode: self_review; no independent review or runtime acceptance is claimed.

- `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/methodology-improvement-2026-11-15.md` — ok, errors=[]; the English counterpart returned the same result.
- `python -B tools/check_docs.py --paths` for nine changed Markdown owners (both new plans, both planning indexes, both registries, REQUIREMENTS/PLAN/RUNLOG) — OK: 9 changed Markdown source(s); site/archive were not checked.
- Local read-only assertions through `python -B -`: 18 unique planned tasks, 54 bilingual AC and 27 reciprocal dependency edges; acyclic DAG; matching RU/EN/JSON titles/status/priority/dependencies/AC/profiles; P3 does not block METH-17/18; METH-14 requires the METH-18 rollout decision.
- Preservation: hashes of 19 existing source/contract owners are unchanged; removing only the inserted planning sections recovers the original bytes of seven updated existing documents. Other session markers and concurrent workstreams were not touched.
- `git diff --check` — exit 0. No application tests/build/browser/native/provider or generated-site run. All 18 implementation timestamps remain pending_execution_timestamp.
- Control-plane sync: updated REQUIREMENTS/PLAN/RUNLOG and planning/source pointers; TEST/EVALS/prod_test no_change_needed because active verification policy and historical execution evidence were unchanged.

## Task index

| ID | Priority | Approach | Task | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-METH-01 | P1 | Spec-DD, ADD | Record the baseline and improvement ownership | — |
| PAOS-METH-02 | P1 | Spec-DD | Trace requirements to source and checks in two pilot scenarios | PAOS-METH-01 |
| PAOS-METH-03 | P1 | Design-DD, Spec-DD | Specify the pilot design-state contract | PAOS-METH-02 |
| PAOS-METH-04 | P1 | Design-DD, TDD | Check UI composition and behavior against the design contract | PAOS-METH-03 |
| PAOS-METH-05 | P1 | TDD, Spec-DD | Close TDD and regression-evidence gaps for critical contracts | PAOS-METH-01, PAOS-METH-02 |
| PAOS-METH-06 | P2 | ADD, Spec-DD | Simplify agent-slice and handoff contracts using baseline evals | PAOS-METH-01, PAOS-METH-02, PAOS-METH-05 |
| PAOS-METH-07 | P2 | ADD | Measure agentic-pilot outcomes on comparable tasks | PAOS-METH-06, PAOS-METH-12 |
| PAOS-METH-08 | P1 | FSD, Design-DD | Design incremental FSD boundaries and a transition ADR | PAOS-METH-01 |
| PAOS-METH-09 | P1 | FSD, TDD | Add incremental frontend-import checks | PAOS-METH-05, PAOS-METH-08 |
| PAOS-METH-10 | P2 | FSD | Extract necessary shared UI and infrastructure modules | PAOS-METH-09 |
| PAOS-METH-11 | P2 | FSD, Spec-DD | Extract frontend entities/task and domain public interfaces | PAOS-METH-10 |
| PAOS-METH-12 | P2 | FSD, Design-DD, Spec-DD | Migrate the dashboard as an FSD pilot | PAOS-METH-02, PAOS-METH-04, PAOS-METH-11 |
| PAOS-METH-13 | P2 | FSD, Design-DD, TDD | Migrate tasks and workflows in separate compatible slices | PAOS-METH-12 |
| PAOS-METH-14 | P3 | FSD, ADD | Extend FSD to team and skills after a go decision | PAOS-METH-13, PAOS-METH-18 |
| PAOS-METH-15 | P3 | FSD, Design-DD | Migrate selected remaining screens and finish the composition boundary | PAOS-METH-14 |
| PAOS-METH-16 | P3 | Spec-DD, FSD, TDD, ADD | Refine conditional methodology support in the Python plugin | PAOS-METH-05, PAOS-METH-18 |
| PAOS-METH-17 | P1 | Spec-DD, Design-DD, TDD, ADD, FSD | Accept the integrated pilot and verify contract preservation | PAOS-METH-07, PAOS-METH-13 |
| PAOS-METH-18 | P2 | ADD, FSD, Spec-DD | Decide on further rollout and update documentation owners | PAOS-METH-17 |

## Detailed task cards

### Task `PAOS-METH-01`

- Task: PAOS-METH-01
- Task name: Record the baseline and improvement ownership
- Status: planned
- Priority: P1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: None.
- Blocks: PAOS-METH-02, PAOS-METH-05, PAOS-METH-06, PAOS-METH-08
- External references: PAOS-FUNC-01, PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-08, PAOS-FUNC-25
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Capture a current source/contract/test baseline and avoid duplicating FUNC, Web and V3 work.
- Technical value: Capture a current source/contract/test baseline and avoid duplicating FUNC, Web and V3 work.
- Product value: Preserve repaired behavior and give each new change one owner.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/planning/methodology-improvement-2026-11-15.json`; `docs/frontend/index.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Baseline and ownership map in this card; no new global registry.
- Acceptance criteria: PAOS-METH-01-AC01: Record the revision, local changes, imports and current web/plugin checks; date historical receipts explicitly. PAOS-METH-01-AC02: Classify every METH card as own/reuse/reference against FUNC/Web/V3; do not create another owner for existing AC or status. PAOS-METH-01-AC03: Assign file/subsystem owners and sequential work points; inspect the current owner of F01/F03–F08 without automatically reopening them.
- Verification gates: V-PLAN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Concurrent planning edits; recheck revisions before writing. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect + product-manager; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Baseline and ownership map in this card; no new global registry.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Concurrent planning edits; recheck revisions before writing.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-02`

- Task: PAOS-METH-02
- Task name: Trace requirements to source and checks in two pilot scenarios
- Status: planned
- Priority: P1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-03, PAOS-METH-05, PAOS-METH-06, PAOS-METH-12
- External references: PAOS-FUNC-02, PAOS-FUNC-25
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Use existing requirement owners for dashboard coverage and task/workflow draft preservation.
- Technical value: Use existing requirement owners for dashboard coverage and task/workflow draft preservation.
- Product value: Assess the user contract and locate missing checks quickly.
- Scope: `docs/product/capabilities.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Two traceability tables in existing product/testing owners and plan AC references.
- Acceptance criteria: PAOS-METH-02-AC01: For each of the two chains, map criterion → canonical owner → source → test/browser scenario → receipt or explicit gap; cover every applicable pilot criterion. PAOS-METH-02-AC02: Specify partial portfolio, preserved drafts and new-object reset behavior; name empty/error/stale scenarios explicitly. PAOS-METH-02-AC03: Reflect changed API/data assumptions in their canonical owner and align mirrors; this traceability work neither implements F02 nor waits for F28.
- Verification gates: V-PLAN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not change FUNC scope/status; gaps are not passed checks. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + tester; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Two traceability tables in existing product/testing owners and plan AC references.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Do not change FUNC scope/status; gaps are not passed checks.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-03`

- Task: PAOS-METH-03
- Task name: Specify the pilot design-state contract
- Status: planned
- Priority: P1
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-04
- External references: PAOS-FUNC-24, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Map dashboard and task/workflow editing to approved V3 and actual API capabilities.
- Technical value: Map dashboard and task/workflow editing to approved V3 and actual API capabilities.
- Product value: Close the gap between approved design, available data and the user journey.
- Scope: `DESIGN.md`; `design/2026-11-13-v3/coverage.json`; `design/2026-11-13-v3/task-field-map.md`; `docs/frontend/state-management.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Updates to existing state/coverage owners; new mockups only for necessary missing states.
- Acceptance criteria: PAOS-METH-03-AC01: Specify default/loading/empty/error/partial/stale/dirty/validation/confirmation states with both themes and keyboard/focus, or justified not_applicable. PAOS-METH-03-AC02: Make metric sources, units and unavailable states explicit; synthetic usage does not become application data and this task does not implement F11. PAOS-METH-03-AC03: Give design differences a disposition: repair/propose to owner/accepted gap; design agreement does not close UI-12 or human acceptance.
- Verification gates: V-PLAN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: A new user journey needs an owner decision; do not silently replace approved V3. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + frontend owner; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Updates to existing state/coverage owners; new mockups only for necessary missing states.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: A new user journey needs an owner decision; do not silently replace approved V3.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-04`

- Task: PAOS-METH-04
- Task name: Check UI composition and behavior against the design contract
- Status: planned
- Priority: P1
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-03
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Extend the existing UI harness for the pilot without a second screenshot/evidence system.
- Technical value: Extend the existing UI harness for the pilot without a second screenshot/evidence system.
- Product value: Catch composition and interaction regressions beyond overflow/contrast checks.
- Scope: `tests/web/single-window/ui-v3-scenario.mts`; `tests/web/ui-v3-dashboard.test.mts`; `design/2026-11-13-v3/implementation-evidence.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Pilot checks in the existing harness and evidence in the existing owner.
- Acceptance criteria: PAOS-METH-04-AC01: Check current-build pilot screenshots in both themes, editor open/close, focus return, draft preservation during navigation and partial/error feedback. PAOS-METH-04-AC02: Checks detect deliberately changed fixture geometry/state; justify thresholds and stable regions, and make baseline updates explicitly reviewable. PAOS-METH-04-AC03: Compare differences with the design owner; separate automated technical passes from human acceptance and bind receipts to build/harness hashes.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Synthetic profiles only; no providers/credentials or screenshots of actual user data. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + frontend owner; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Pilot checks in the existing harness and evidence in the existing owner.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Synthetic profiles only; no providers/credentials or screenshots of actual user data.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-05`

- Task: PAOS-METH-05
- Task name: Close TDD and regression-evidence gaps for critical contracts
- Status: planned
- Priority: P1
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01, PAOS-METH-02
- Blocks: PAOS-METH-06, PAOS-METH-09, PAOS-METH-16
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Separate existing protections, missing regression cases and RED requirements for the next behavior change.
- Technical value: Separate existing protections, missing regression cases and RED requirements for the next behavior change.
- Product value: Preserve draft/retry/recovery/approval invariants during refactors and tooling changes.
- Scope: `TEST.md`; `tests/web/ui-draft-autosave.test.mts`; `tests/web/contracts-boundaries.test.mts`; `tests/product_agent_os/test_methodology_audit.py`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Compact risk/test mapping in TEST and existing task evidence; only meaningful missing tests.
- Acceptance criteria: PAOS-METH-05-AC01: Map risk → invariant → lowest reliable check for draft conflict/lost ACK, import boundaries, Stop/recovery, backup/restore and approval routing; reuse existing tests. PAOS-METH-05-AC02: Define expected RED causes and minimal GREEN for new TS boundary behavior in METH-09 and Python routing behavior in METH-16; record evidence when implementing them. PAOS-METH-05-AC03: Setup/import failures are not RED; behavior-preserving moves use characterization/regression without artificially broken production code; F21/F22 retain full recovery ownership.
- Verification gates: V-TDD; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not duplicate full recovery suites or require RED for docs or pure moves. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Compact risk/test mapping in TEST and existing task evidence; only meaningful missing tests.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Do not duplicate full recovery suites or require RED for docs or pure moves.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-06`

- Task: PAOS-METH-06
- Task name: Simplify agent-slice and handoff contracts using baseline evals
- Status: planned
- Priority: P2
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01, PAOS-METH-02, PAOS-METH-05
- Blocks: PAOS-METH-07
- External references: None; this plan owns the work.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Check whether the existing concise contract is sufficient and remove measured duplication without a new mandatory packet.
- Technical value: Check whether the existing concise contract is sufficient and remove measured duplication without a new mandatory packet.
- Product value: Reduce overhead and context loss while preserving ownership and authority boundaries.
- Scope: `.codex/workflows/build-slice.md`; `.codex/workflows/review-slice.md`; `.codex/evals/agent-context-contract.json`; `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Change only demonstrably redundant sections and record baseline/candidate evidence in the existing eval owner.
- Acceptance criteria: PAOS-METH-06-AC01: Compare the baseline and one candidate on a bounded fix, docs-only work, missing context, overlapping ownership, premature success and unapproved external action. PAOS-METH-06-AC02: Preserve goal/AC, source revision, owned/forbidden files, checks, stop conditions and handoff; do not force the ordinary concise route into a full packet. PAOS-METH-06-AC03: Promote the candidate only with no new boundary/claim failures; static contract passes do not establish fresh-session activation or improved LLM quality.
- Verification gates: V-ADD; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: These are future durable instruction changes: a separately authorized slice, baseline evals and before-images; do not change hooks/trust. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: lifecycle-orchestrator + reviewer; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Change only demonstrably redundant sections and record baseline/candidate evidence in the existing eval owner.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: These are future durable instruction changes: a separately authorized slice, baseline evals and before-images; do not change hooks/trust.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-07`

- Task: PAOS-METH-07
- Task name: Measure agentic-pilot outcomes on comparable tasks
- Status: planned
- Priority: P2
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-06, PAOS-METH-12
- Blocks: PAOS-METH-17
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Compare baseline and candidate on the same task set, separating orchestration correctness from solution quality.
- Technical value: Compare baseline and candidate on the same task set, separating orchestration correctness from solution quality.
- Product value: Decide on the process using outcome quality and effort rather than agent or test counts.
- Scope: `EVALS.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Baseline/candidate evidence in this card; separate correctness/quality/cost verdicts.
- Acceptance criteria: PAOS-METH-07-AC01: Use identical task inputs/AC/revision and an available runtime; record accepted/reopened outcomes, repair cycles, owner interventions and elapsed time with provenance. PAOS-METH-07-AC02: Report tokens/cost only with reliable provenance; unavailable is not zero and F11 telemetry is not implemented for this pilot. PAOS-METH-07-AC03: If actual-agent comparison requires unavailable authorization, limit results to deterministic routing; model-quality benefit remains insufficient_evidence and does not justify promotion.
- Verification gates: V-ADD; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: No automatic provider calls, private raw chats or unsupported productivity claims; human acceptance remains separate. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + product-manager; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Baseline/candidate evidence in this card; separate correctness/quality/cost verdicts.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: No automatic provider calls, private raw chats or unsupported productivity claims; human acceptance remains separate.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-08`

- Task: PAOS-METH-08
- Task name: Design incremental FSD boundaries and a transition ADR
- Status: planned
- Priority: P1
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-09
- External references: PAOS-FUNC-08, PAOS-FUNC-30
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Choose minimal layers and ownership from actual imports and product journeys.
- Technical value: Choose minimal layers and ownership from actual imports and product journeys.
- Product value: Make the next migration reviewable without a full rewrite or unnecessary folders.
- Scope: `docs/architecture/decisions/`; `docs/frontend/index.md`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One proposed ADR in the existing decisions directory and a migration map; choose its number after current inventory.
- Acceptance criteria: PAOS-METH-08-AC01: Compare retaining feature folders, boundaries-only improvements and partial FSD; base the ADR on coupling, testability and migration cost. PAOS-METH-08-AC02: Map App composition → pages/widgets when useful → interaction features → entities → shared; do not automatically classify whole-screen TaskManager/Dashboard as features. PAOS-METH-08-AC03: Specify public APIs, an owned legacy exception list with removal tasks, legacy→new bridges, fallback/rollback and sufficiency criteria; do not apply frontend FSD to backend/Python.
- Verification gates: V-PLAN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: The ADR is a future deliverable, not an accepted decision; F30 is not a mandatory dependency. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: One proposed ADR in the existing decisions directory and a migration map; choose its number after current inventory.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: The ADR is a future deliverable, not an accepted decision; F30 is not a mandatory dependency.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-09`

- Task: PAOS-METH-09
- Task name: Add incremental frontend-import checks
- Status: planned
- Priority: P1
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05, PAOS-METH-08
- Blocks: PAOS-METH-10
- External references: PAOS-FUNC-08, PAOS-FUNC-30
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Extend the existing AST boundary check for migrated scopes and prevention of new violations.
- Technical value: Extend the existing AST boundary check for migrated scopes and prevention of new violations.
- Product value: Stop coupling growth before moves without blocking all legacy code.
- Scope: `tests/web/contracts-boundaries.test.mts`; `apps/web/package.json`; `apps/web/src/`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Extend the existing parser/check and synthetic cases; add a dependency only when demonstrated necessary.
- Acceptance criteria: PAOS-METH-09-AC01: RED/GREEN fixtures cover .ts/.tsx/.mts, type imports/reexports/literal dynamic imports and configured aliases; an unmapped alias is an explicit gap/failure, not silently skipped. PAOS-METH-09-AC02: Reject upward/same-layer/deep imports and cycles in migrated scopes under the accepted ADR; permit entity cross-imports only through an agreed API, not a blanket exception. PAOS-METH-09-AC03: Pin current legacy edges and prevent growth; remove migrated modules from exceptions; preserve contracts→apps and backend→frontend prohibitions.
- Verification gates: V-BOUNDARY; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not hide actual imports with exclusions; make baseline updates reviewable. Do not install dependency-cruiser automatically. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + builder; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Extend the existing parser/check and synthetic cases; add a dependency only when demonstrated necessary.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Do not hide actual imports with exclusions; make baseline updates reviewable. Do not install dependency-cruiser automatically.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-10`

- Task: PAOS-METH-10
- Task name: Extract necessary shared UI and infrastructure modules
- Status: planned
- Priority: P2
- Methodologies: FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-09
- Blocks: PAOS-METH-11
- External references: None; this plan owns the work.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Extract reusable non-domain primitives and infrastructure required by the pilot.
- Technical value: Extract reusable non-domain primitives and infrastructure required by the pilot.
- Product value: Remove shared presentation dependencies on internal task/graph screens.
- Scope: `apps/web/src/ui/Icon.tsx`; `apps/web/src/ui/Modal.tsx`; `apps/web/src/features/tasks/CommentMarkdown.tsx`; `apps/web/src/locales/`; `apps/web/src/features/graph/GraphViews.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Minimal shared public APIs, compatibility bridges and an updated migration map.
- Acceptance criteria: PAOS-METH-10-AC01: Place only used primitives, safe Markdown/rendering and i18n infrastructure in shared; retain task status rules and task-specific labels with their domain. PAOS-METH-10-AC02: Separate generic rendering from graph-domain mapping only with proven reuse; avoid wildcard public exports and new frontend→backend dependencies. PAOS-METH-10-AC03: Keep compatibility reexports one-way with single implementations/state; preserve theme/focus/Markdown-safety/reduced-motion regressions.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: This is a behavior-preserving move; do not change visual design, sanitization policy, APIs or data. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — shared frontend ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Minimal shared public APIs, compatibility bridges and an updated migration map.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: This is a behavior-preserving move; do not change visual design, sanitization policy, APIs or data.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-11`

- Task: PAOS-METH-11
- Task name: Extract frontend entities/task and domain public interfaces
- Status: planned
- Priority: P2
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-10
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-08
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Separate task presentation/model selectors, interaction state and server-owned contracts.
- Technical value: Separate task presentation/model selectors, interaction state and server-owned contracts.
- Product value: Let dashboard and team use a stable task API instead of deep imports into a task screen.
- Scope: `apps/web/src/features/tasks/model.ts`; `apps/web/src/features/tasks/labels.ts`; `apps/web/src/features/dashboard/model.ts`; `packages/contracts/issues/task-profile.ts`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: ADR-aligned entities/task public API, transition adapters and domain regression evidence.
- Acceptance criteria: PAOS-METH-11-AC01: Give reusable selectors/status presentation/task labels one frontend domain owner; keep editor drafts and commands interaction-owned without duplicating backend authority. PAOS-METH-11-AC02: Keep packages/contracts application-independent and free of React/UI imports; preserve F08 types and decode/persistence semantics. PAOS-METH-11-AC03: Pilot consumers use an explicit public API; semanticStatus/isBlocked/aggregation and contract-boundary tests pass, and legacy bridges have removal owners.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not duplicate business rules between service and UI or change progress/blocked semantics for structure. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect + builder — task domain; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: ADR-aligned entities/task public API, transition adapters and domain regression evidence.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Do not duplicate business rules between service and UI or change progress/blocked semantics for structure.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-12`

- Task: PAOS-METH-12
- Task name: Migrate the dashboard as an FSD pilot
- Status: planned
- Priority: P2
- Methodologies: FSD, Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02, PAOS-METH-04, PAOS-METH-11
- Blocks: PAOS-METH-07, PAOS-METH-13
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-18
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Move dashboard composition to minimal ADR-aligned pages/widgets while retaining existing data flow.
- Technical value: Move dashboard composition to minimal ADR-aligned pages/widgets while retaining existing data flow.
- Product value: Evaluate FSD on a real bounded screen with measurable contracts.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `apps/web/src/ui/App.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One migrated dashboard, evidence in this card and frontend owner docs.
- Acceptance criteria: PAOS-METH-12-AC01: The migrated dashboard has no imports into legacy feature internals; selectors use domain public APIs and services/F18 refresh behavior remain unchanged. PAOS-METH-12-AC02: Preserve F05 partial coverage, F06 queue numbering and F07 recent-task ordering on current sources; pass both themes and the METH-03 state matrix. PAOS-METH-12-AC03: Record before/after boundary edges, touched files, regression/visual results and rollback; a negative outcome can stop rollout without rewriting other screens.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: No new metrics/synthetic numbers, API requests or unmeasured performance claims; qualify native runtime only if pinned sources changed. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — dashboard ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: One migrated dashboard, evidence in this card and frontend owner docs.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: No new metrics/synthetic numbers, API requests or unmeasured performance claims; qualify native runtime only if pinned sources changed.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-13`

- Task: PAOS-METH-13
- Task name: Migrate tasks and workflows in separate compatible slices
- Status: planned
- Priority: P2
- Methodologies: FSD, Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-12
- Blocks: PAOS-METH-14, PAOS-METH-17
- External references: PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-21
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Separate screen composition from editing/queue interactions without changing task/workflow semantics.
- Technical value: Separate screen composition from editing/queue interactions without changing task/workflow semantics.
- Product value: Isolate two coupled user journeys while preserving unfinished work.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/tasks/Editor.tsx`; `apps/web/src/features/workflows/WorkflowManager.tsx`; `apps/web/src/features/workflows/recipes/`; `apps/web/src/ui/App.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Two sequential migrated checkpoints and updated domain/state docs.
- Acceptance criteria: PAOS-METH-13-AC01: Complete a tasks checkpoint before a workflows checkpoint, each with source hashes, affected tests, visual evidence and reversible hunks. PAOS-METH-13-AC02: Preserve F03 new-task reset, F04 workflow drafts/CAS, dialog focus/eight tabs, preview/confirmation and queue controls; do not claim full F21 recovery closure. PAOS-METH-13-AC03: Migrated consumers do not depend on sibling-screen internals; remove migrated edges from baseline exceptions and add interaction features only for real responsibilities.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Serialize shared App/navigation/labels edits; no new workflow rules, DB migrations or scope expansion. The current request authorizes planning only.
- Complexity: L
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — tasks, затем builder — workflows; sequential; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Two sequential migrated checkpoints and updated domain/state docs.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Serialize shared App/navigation/labels edits; no new workflow rules, DB migrations or scope expansion.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-14`

- Task: PAOS-METH-14
- Task name: Extend FSD to team and skills after a go decision
- Status: planned
- Priority: P3
- Methodologies: FSD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-13, PAOS-METH-18
- Blocks: PAOS-METH-15
- External references: PAOS-FUNC-11, PAOS-FUNC-12, PAOS-FUNC-16
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Apply validated boundaries to team/skills without implementing new capabilities.
- Technical value: Apply validated boundaries to team/skills without implementing new capabilities.
- Product value: Simplify reuse of task/dashboard primitives and safe future catalog changes.
- Scope: `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/features/skills/SkillGenerator.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Migrated team/skills one checkpoint at a time; no commitment to migrate the entire frontend.
- Acceptance criteria: PAOS-METH-14-AC01: Start only after a METH-18 go decision for this area; team and skills have separate checkpoints and owners. PAOS-METH-14-AC02: Preserve catalog/profile/edit/history/generation preview and unavailable usage; F11/F12/F16 retain ownership and no provider search is invoked. PAOS-METH-14-AC03: Pass public API/boundary tests and scoped UI checks; report removed legacy edges and remaining exceptions.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: P3 is optional for pilot acceptance; do not add provider calls or asset promotion. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — team/skills ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Migrated team/skills one checkpoint at a time; no commitment to migrate the entire frontend.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: P3 is optional for pilot acceptance; do not add provider calls or asset promotion.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-15`

- Task: PAOS-METH-15
- Task name: Migrate selected remaining screens and finish the composition boundary
- Status: planned
- Priority: P3
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-14
- Blocks: None.
- External references: PAOS-FUNC-02, PAOS-FUNC-14, PAOS-FUNC-26, PAOS-FUNC-33, PAOS-FUNC-34
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Continue only approved screen moves and retain App ownership of composition/session scope.
- Technical value: Continue only approved screen moves and retain App ownership of composition/session scope.
- Product value: Reduce overall import coupling without losing history, document or graph context.
- Scope: `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Operations.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Selected-screen checkpoints, App composition map and dispositions for remaining legacy exceptions.
- Acceptance criteria: PAOS-METH-15-AC01: Migrate sessions → artifacts → graph one at a time; exclude new Files/Database/usages features and resolve FUNC ownership conflicts before edits. PAOS-METH-15-AC02: Keep composition/global providers/session selection in App; move feature-local state only when justified and preserve behavior/route IDs. PAOS-METH-15-AC03: Allow no unauthorized legacy/deep/upward imports in the selected migrated scope; remove compatibility adapters only after consumer inventory and regression checks.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not claim full FSD from folders alone; unselected scope remains explicitly bounded legacy. The current request authorizes planning only.
- Complexity: L
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — один screen owner за раз; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Selected-screen checkpoints, App composition map and dispositions for remaining legacy exceptions.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: Do not claim full FSD from folders alone; unselected scope remains explicitly bounded legacy.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-16`

- Task: PAOS-METH-16
- Task name: Refine conditional methodology support in the Python plugin
- Status: planned
- Priority: P3
- Methodologies: Spec-DD, FSD, TDD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05, PAOS-METH-18
- Blocks: None.
- External references: None; this plan owns the work.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Transfer only demonstrated pilot lessons into plugin recommendations and verification evidence.
- Technical value: Transfer only demonstrated pilot lessons into plugin recommendations and verification evidence.
- Product value: Give target projects proportionate recommendations rather than FSD mandates based on folder names.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/assets/methodology/methodology-catalog.json`; `tests/product_agent_os/test_methodology_audit.py`; `docs/methodologies/frontend.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One focused plugin slice with representative eval comparison; no blanket methodology requirement.
- Acceptance criteria: PAOS-METH-16-AC01: Compare baseline/candidate cases for small frontends, growing coupled frontends, backend-only, native-only, misleading features folders, missing source and already-bounded frontends. PAOS-METH-16-AC02: Use RED/GREEN for new detection/routing behavior; distinguish not_applicable/applicable_missing/present_unverified and never treat missing evidence as proof of a violation. PAOS-METH-16-AC03: The proposal does not mutate targets or activate hooks/agents, and folder detection is not import/runtime proof; align RU/EN docs and catalog/evals.
- Verification gates: V-PLUGIN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: This repo pilot does not prove broad usefulness; prompt/routing changes require separate baseline comparison, not installation. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: plugin-runtime-builder + tester; proposed ownership; delegation=0 now.
- Skills: python-design-patterns + python-code-style; advisory, for the future Python slice only.
- Output artifacts: One focused plugin slice with representative eval comparison; no blanket methodology requirement.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: This repo pilot does not prove broad usefulness; prompt/routing changes require separate baseline comparison, not installation.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-17`

- Task: PAOS-METH-17
- Task name: Accept the integrated pilot and verify contract preservation
- Status: planned
- Priority: P1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-07, PAOS-METH-13
- Blocks: PAOS-METH-18
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22, PAOS-FUNC-23, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Reconcile dashboard/tasks/workflows and methodology-process evidence on one source state.
- Technical value: Reconcile dashboard/tasks/workflows and methodology-process evidence on one source state.
- Product value: Accept a useful bounded result with explicit gaps before scaling.
- Scope: `tests/web/`; `docs/testing/index.md`; `docs/frontend/`; `docs/planning/methodology-improvement-2026-11-15.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: AC/evidence reconciliation and a reasoned pilot_accepted/partial/blocked verdict.
- Acceptance criteria: PAOS-METH-17-AC01: Every pilot AC has a current check/receipt or explicit unresolved gap; pass all required affected-contract checks and give findings a disposition. PAOS-METH-17-AC02: Check scope/session selection, drafts, partial data, navigation/focus and contract independence; reuse recovery/backup evidence only while relevant state is unchanged. PAOS-METH-17-AC03: Limit review and technical acceptance to the pilot; UI-12/F23 human acceptance and F19 full-product E2E retain owners, and P3 tasks do not block bounded pilot closure.
- Verification gates: V-INTEGRATED; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: No release-readiness or full-product acceptance claims; an unresolved critical pilot gap forbids acceptance. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + reviewer; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: AC/evidence reconciliation and a reasoned pilot_accepted/partial/blocked verdict.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: No release-readiness or full-product acceptance claims; an unresolved critical pilot gap forbids acceptance.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

### Task `PAOS-METH-18`

- Task: PAOS-METH-18
- Task name: Decide on further rollout and update documentation owners
- Status: planned
- Priority: P2
- Methodologies: ADD, FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-17
- Blocks: PAOS-METH-14, PAOS-METH-16
- External references: PAOS-FUNC-25
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.json); current paths below; external refs are references only.
- Short description: Choose go/bounded_go/hold/stop for each next area using evidence.
- Technical value: Choose go/bounded_go/hold/stop for each next area using evidence.
- Product value: Scale useful changes and stop unsupported complexity.
- Scope: `docs/architecture/decisions/`; `docs/frontend/`; `docs/testing/`; `docs/sources/registry.md`; `PLAN.md`; `RUNLOG.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Reviewable rollout decision in the existing ADR/evidence owner and a compact handoff.
- Acceptance criteria: PAOS-METH-18-AC01: Compare baseline/pilot unauthorized edges, regression findings, change/review effort and available outcome metrics; test counts are not benefit metrics. PAOS-METH-18-AC02: Record separate decisions, scope, owners and rollback for METH-14/15/16; hold/stop retains the working pilot without an indefinite migration mandate. PAOS-METH-18-AC03: Update only affected docs/registry/control-plane owners; change active rules only in a separately authorized slice and preserve existing FUNC/Web status and release gates.
- Verification gates: V-PLAN; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: A go decision does not automatically authorize implementation/provider/install/Git or deployment. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + architect; owner decision; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Reviewable rollout decision in the existing ADR/evidence owner and a compact handoff.
- Next step: Check dependencies and current source owners; obtain a separately authorized implementation scope for the selected task.

#### Completion Report

- status: planned
- what was done: Implementation not started; task card authored.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: A go decision does not automatically authorize implementation/provider/install/Git or deployment.
- follow-up: Select the next authorized slice from the DAG; no automatic start.

