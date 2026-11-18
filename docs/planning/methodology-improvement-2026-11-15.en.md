# Product-Agent OS — direction A: internal quality and architecture

Source status: repository_source / owner_requested_internal_quality_plan / a1_local_verification.
Created 2026-11-15, revised 2026-11-18. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Two directions — revision 3, 2026-11-18

A improves Product-Agent OS and its maintenance process. A contains **17 executable tasks**, 8 P1 / 7 P2 / 2 P3. B develops methodology application in user projects: [26 product tasks](user-project-methodologies-2026-11-15.en.md), [JSON](user-project-methodologies-2026-11-15.en.json). There are no cross-direction hard dependencies.

Retain METH-16 with its ID, title and three legacy AC as a **reference-only** record outside JSON v2's tasks array; it is not scheduled and owns no product implementation status. Canonical owners: PMETH-03/07/10/11/16/17/22/23/26; JSON preserves exact AC mappings and former edges. V-REFERENCE checks B links/coverage without executing code from A. METH-18 considers internal expansion options METH-10/11/13–15. Direction B follows its own delivery plan.

Revision 2 used HEAD `5a9c87bea374accc953a8401fa1ac32678ff6e6e` and FUNC owner state of 10 implemented / 24 planned. Revision 3 uses the FUNC owner's 2026-11-18 status. All 18 IDs are retained, including reference-only METH-16.

## Goal, authority and ownership

Direction A covers Spec-DD, Design-DD, TDD, ADD, and frontend boundaries. A1 defines the testable Dashboard contract and import constraints. A2 tests an actual change at the Dashboard and Tasks boundary.

[JSON state v2](methodology-improvement-2026-11-15.en.json) owns status, priority, and dependencies for 17 A tasks. `cross_track_references` retains METH-16 separately. The RU/EN cards match JSON. B has its own [detailed plan](user-project-methodologies-2026-11-15.en.md) and owner.

## Baseline and evidence

Source snapshot: git HEAD `35458110145d928b9b14d9312b60d852f11f6e88`; hashes of seven inspected implementation/test owners are in JSON. This snapshot belongs to the initial planning pass. Planning inspected source/owners; historical test/browser/native receipts were not rerun.

- The FUNC state owner `functional-remediation-2026-11-15.json` and [G07 results](functional-remediation-2026-11-15.en.md#func-g07-results) record 33 implemented and one awaiting_user_decision (F23) as of 2026-11-18. Reuse the verified contracts and scenarios of F05–F08, F14, F19 and F24 within their evidence limits. The F23 human pilot remains open. The [G01](functional-remediation-2026-11-15.en.md#func-g01-results) 7/27 count belongs to the first revision.
- Spec-DD already appears in [requirements and capabilities](../product/capabilities.md) and concrete matrices; workspace files `TEST.md` and `EVALS.md` own verification selection and claim ceilings.
- Design-DD has workspace file `DESIGN.md`, V3 coverage and the [implementation plan](2026-11-13-v3-ui-implementation-plan.md). Historical V3 review identified a composition-coverage gap; this does not assert a new defect in the current build.
- TDD has rules and individual historical RED/GREEN receipts; completed tests cannot prove test-first ordering for every task.
- ADD has build/review/handoff contracts and ownership separation. Better agentic quality/cost requires a comparable baseline rather than role counts.
- Before A1, the frontend used feature folders and internal imports between Dashboard, Tasks, and peer modules. The original `tests/web/contracts-boundaries.test.mts` covered application boundaries. A1 adds TSX and pilot resolution rules under the [ADR](../architecture/decisions/adr-dashboard-task-boundary.en.md).

Sources: `apps/web/src/features/dashboard/model.ts`, `tasks/TaskManager.tsx`, `workflows/WorkflowManager.tsx`, `team/TeamManager.tsx`, `apps/web/src/ui/App.tsx`; Python owner `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`. Read their current state again before future edits.

Methodology primary sources checked in the preceding analysis on 2026-11-15: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html), [FSD layers](https://feature-sliced.design/docs/reference/layers), [FSD public API](https://feature-sliced.design/docs/reference/public-api), [Spec Kit process](https://github.github.io/spec-kit/quickstart.html), [IBM human-centered design](https://www.ibm.com/training/enterprise-design-thinking/framework), [AWS AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/). ADD/Design-DD are explicitly scoped working approaches here, not assertions of a single industry standard. Proposals and judgments below are project-authored, not external research results.

## Priorities, stages and dependencies

P1 protects contracts and acceptance evidence; P2 is the main bounded pilot/process improvement; P3 is optional evidence-gated scaling. P1 does not mean a production incident. Task numbers are not execution order.

### Delivery groups

Groups organize tasks by outcome. Each task can start when its own `depends_on` and applicable selection conditions are satisfied.

| Group | Tasks | Start and outcome |
| --- | --- | --- |
| **A1. Dashboard criteria and boundaries** | 01, 02, 03, 04, 08, 09 | After 01, the 02 → 03 → 04 branch defines Dashboard behavior and states. The 08 → 09 branch defines the import boundaries and their checks. |
| **A2. Dashboard pilot and expansion decision** | 12, 17, 18 | After 04 and 09, task 12 tests the boundary between Dashboard and Tasks. Task 17 evaluates technical acceptance, and 18 decides whether to expand. The pilot may end at Dashboard. |
| **A3. Testing quality and agent workflows** | 05, 06, 07 | After 02, work through 05 → 06 → 07 alongside the pilot. The outputs are a map of test gaps, a verified handoff procedure and a separate evaluation of agent work. Actual-agent runs in 07 require authorization and comparable conditions. |
| **A4. Selective expansion of architectural boundaries** | 10, 11, 13, 14, 15 | After 18, select justified changes to shared UI components, the Tasks API or individual screens. Record the expected benefit, verification and rollback for each selected area. |

Two branches follow METH-01. METH-02 → 03 → 04 defines Dashboard criteria and states. METH-08 → 09 defines the ADR and import check. They converge on METH-12 → 17 → 18. METH-05/06/07 run separately from technical acceptance. Each METH-10/11/13–15 expansion requires a METH-18 decision for its specific scope. JSON `depends_on` lists mandatory edges and `blocks` stores their reverse. `activation_condition` records the selection conditions.

## Relationship to the existing backlog

| Existing owner | Reuse | No duplicate ownership |
| --- | --- | --- |
| F01/F03–F08, FUNC-G01 | Baseline and regression protection | Fixes, native qualification and completion state |
| F02/F28 | References for future artifact traceability/canonical paths | Task↔artifact links and inventory; METH-02 does not wait for F28 |
| F11/F12/F16 | Metric/team/skill limitations | Telemetry, external search and actually loaded-profile proof |
| F18/F20 | Refresh semantics and performance budgets | Refresh changes and duplicate benchmarks |
| F14/F30 | F14 uses the Rolldown AST and a bounded resolver. Reuse import semantics and fixtures where applicable | A second runtime graph or installation of the dependency-cruiser PoC |
| F19/F21/F22/F23/F24, UI-12 | Reusable scenarios/evidence and separate full/human acceptance | Full E2E, recovery, backup/restore, feature availability and human acceptance |
| F25, DOCS-01–16 | Canonical documentation/status ownership | Recreating guides or changing feature task-state |
| F26–29/F31–34, M5 | Migration-scope exclusions | New Files/Map/Database/usages or hosting/auth/team capabilities |

`external_refs` points to owners and evidence. F08 protects application-independent contracts, and F18 owns refresh semantics. Recheck F01 when touching pinned runtime sources. Sequence writes to shared files.

## Dashboard and Tasks boundary

METH-08 compared retaining the current modules, strengthening their boundaries, and adopting bounded FSD. The A2 pilot strengthens the boundary in the existing modules. [Decision and rollback criteria](../architecture/decisions/adr-dashboard-task-boundary.en.md)

- `App.tsx` owns composition, session, and active project. Dashboard uses the explicit `features/tasks/read.ts` API for Tasks selectors (`semanticStatus`, `isBlocked`) with a single implementation.

- Extract widgets, entities/task and shared only for demonstrated needs. Verify API use and regressions before moving more screens. Shared business contracts remain in `packages/contracts`.

- Accepted compatibility bridges have a single implementation and a removal owner. Check for new violations against a revision-pinned baseline and resolve open violations at the selected Dashboard boundary.

- The pilot may end with Dashboard. Give every later selected screen its own protections and rollback. Recheck draft/CAS behavior, project/session isolation, focus and current state semantics when the corresponding shared paths change.

## Future task verification

These profiles describe expected verification for each task. `TEST.md` lists the current commands and routes.

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

## Initial plan-preparation verification — 2026-11-15

This checks the planning artifact, not execution of METH tasks. Review mode: self_review; no independent review or runtime acceptance is claimed.

- `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/methodology-improvement-2026-11-15.md` — ok, errors=[]; the English counterpart returned the same result.
- `python -B tools/check_docs.py --paths` for nine changed Markdown owners (both new plans, both planning indexes, both registries, REQUIREMENTS/PLAN/RUNLOG) — OK: 9 changed Markdown source(s); site/archive were not checked.
- Local read-only assertions through `python -B -`: 18 unique planned tasks, 54 bilingual AC and 27 reciprocal dependency edges; acyclic DAG; matching RU/EN/JSON titles/status/priority/dependencies/AC/profiles; P3 does not block METH-17/18; METH-14 requires the METH-18 rollout decision.
- Preservation: hashes of 19 existing source/contract owners are unchanged; removing only the inserted planning sections recovers the original bytes of seven updated existing documents. Other session markers and concurrent workstreams were not touched.
- `git diff --check` — exit 0. No application tests/build/browser/native/provider or generated-site run. All 18 implementation timestamps remain pending_execution_timestamp.
- Control-plane sync: updated REQUIREMENTS/PLAN/RUNLOG and planning/source pointers; TEST/EVALS/prod_test no_change_needed because active verification policy and historical execution evidence were unchanged.

## Direction-split verification — revision 2

Revision 2 static split/parity/preservation evidence remains in direction B. Revision 3 retains the former wording of revised acceptance criteria and removed edges in JSON `pilot_revision`. The initial verification dates and results above belong to the original revision.

## A1 results {#a1-results}

The METH-01 baseline was a clean worktree at `bd7d9135f994201170277171eb54e4040cef4fa8`. Composition and navigation resided in `apps/web/src/ui/App.tsx`. The Dashboard model imported `semanticStatus` and `isBlocked` from Tasks, and its views used labels and UI primitives. The 19 original edges are preserved in `tests/web/fixtures/dashboard-import-baseline.json` at revision `4d853089a0ffa8be4c47ba7ee3909a754f09a169`. Current Web checks are in `TEST.md` and Python methodology checks in `tests.product_agent_os.test_methodology_audit`. FUNC G01 and F18 results from November 15 retain their original receipts.

| Cards | Owner of the A result | Reuse and references |
| --- | --- | --- |
| 01 | Direction A matrix and pinned imports | FUNC G07 and F23, Web, and V3 retain their source ownership. |
| 02 | [Criterion-to-check mapping](../testing/test-map.en.md#dashboard-a1-criteria) | FUNC owns F05–F07/F18 criteria and implementation. |
| 03 | [Dashboard states](../frontend/state-management.en.md#dashboard-a1-states) | V3 supplies the composition and FUNC the data semantics. |
| 04 | Dashboard browser scenario and V3 evidence | Extends the F05–F07 scenario with existing local-service fixtures. |
| 08, 09 | [ADR](../architecture/decisions/adr-dashboard-task-boundary.en.md), boundary test, and exceptions | Reuse installed Rolldown and the F14 resolver. F08 owns contract independence. |
| 05, 06, 07 | TDD coverage of critical contracts, handoff, and ADD measurement | Reuse existing FUNC/Web tests and eval owners. F19 and F23 retain their acceptance scope. |
| 12, 17, 18 | Boundary pilot, technical acceptance, and expansion decision | Reuse A1 and applicable FUNC/V3 checks. F19 and UI-12/F23 retain their decisions. |
| 10, 11, 13, 14, 15 | Possible work on shared UI, the Tasks API, and screens | Reuse current FUNC/Web/V3 contracts. Start a selected slice after 18. |
| 16 | Reference entry | Direction B owns product criteria and implementation. |

The current build's browser receipt is `.tmp/func-g01-dashboard/evidence-hrwQrx/result.json`, with 50 checks. It covers RU/light and EN/dark desktop at 1440×1000, plus EN/dark mobile at 390×844. The composition assertion rejects a fixture that stacks the principal columns. `light-stale.png` and `dark-error.png` were inspected against the state contract. Dynamic text such as timestamps is checked semantically. Geometry tolerates 1 px of rounding. The checks cover local Dashboard behavior. UI-12 owns full V3 user acceptance.

In RED, the old parser rejected TSX, scanning source exposed 19 unrecorded edges, and the Tasks check exposed unguarded imports of App and a peer screen. GREEN covers an allowed App entry, forbidden upward, cross-feature, and deep imports, an unresolved alias, a computed import, and a cycle through another module. The final focused run passed 26 checks, including 8 boundary tests.

Final verification on 2026-11-18: `node --test --test-concurrency=1 tests/web/*.test.mts` passed **702/702** on Windows with zero skips. `npm run check:web-m1` and `npm run build:web` passed. The Python methodology audit passed 57/57. Documentation checks, RU/EN matrix validators, task-state consistency, and an isolated MkDocs build passed. Verified 7 browser receipt hashes, 12 preserved cards outside A1 per language, and byte-exact JSON mirrors.

The initial sandboxed browser run exited 1 with Windows access denied. A retry reached the scenario and exposed an invalid synthetic record field. The corrected fixture passed all 50 checks. The initial full Web run stopped after Windows native fixture failures. The final run with authorized native fixtures exited 0. Separate logs are in `.tmp/func-g01-dashboard/`. The final log is `a1-web-suite-final.log`.

## A2 results {#a2-results}

METH-12 started from clean revision `4d853089a0ffa8be4c47ba7ee3909a754f09a169`. Before and after the change, the Web build ran the same `func-g01-dashboard-acceptance.mts` scenario against the local service and SQLite with synthetic projects. The final scenario adds two checks for navigation to a task and back.

| Comparison | Before | After |
| --- | --- | --- |
| Direct Dashboard → Tasks internals | `Dashboard.tsx → labels.ts`, `RunUsage.tsx → labels.ts`, `model.ts → model.ts` | The same three consumers use one public entry, `tasks/read.ts`. Zero direct edges to internal files. |
| Violations and exceptions around Dashboard/Tasks | 19 existing exceptions, including three from Dashboard | 16 exceptions from the same source revision, zero from Dashboard, and zero new violations. |
| Browser verification | 50/50, `evidence-2HAMGM/result.json` | 50/50 matched by name plus 2/2 navigation checks, `evidence-1LoV2F/result.json`. Both receipts are in `.tmp/func-g01-dashboard/`. |
| Change and review scope | External consumers depend on two Tasks internal paths. | Added one three-line API file and changed imports in three Dashboard files. A future implementation move that preserves the API has one external path to inspect. Reviewer time and ADD effects were outside this measurement. |

| Acceptance criterion | Evidence |
| --- | --- |
| METH-12-AC01 and METH-17-AC01 | RED showed the missing public module and the A1 rule rejecting the proposed path. GREEN verifies the Dashboard-only path, rejects a bypass and unrelated consumer, checks the exact public functions, and proves they use the original Tasks `model.ts` and `labels.ts` implementations. |
| METH-12-AC02 and METH-17-AC02 | F05 partial/empty/error, F06 queue positions and reorder, F07 `updatedAt` after creation and edit, F18 stale/refresh, light and dark themes, Tab/Enter and correct task detail. The boundary check verifies contract independence. Production changes are imports and exports. Shared App, service, draft, and session paths were outside the pilot change. |
| METH-12-AC03 and METH-17-AC03 | The build receipt pins 16 harness, source, and asset hashes. Reviewed `light-stale.png` and `dark-error.png` before and after. Timestamps and the order of two synthetic projects in the error state varied. Error meaning, control availability, and layout were preserved. No critical regressions were evident in the pilot. `pilot_accepted` applies to the local pilot. UI-12/F23 and F19 retain their acceptance owners. [Rollback](../architecture/decisions/adr-dashboard-task-boundary.en.md) |
| METH-18-AC01–AC03 | The comparison supports `bounded_go` for METH-11 in `TeamManager.tsx` only. Other A4 work is on `hold` until its own boundary has supporting evidence. The ADR records measurable METH-11 criteria and rollback. [A4 decisions](../architecture/decisions/adr-dashboard-task-boundary.en.md#a2-rollout) |

The final `node --test --test-concurrency=1 tests/web/*.test.mts` passed **704/704** with zero skips, `.tmp/func-g01-dashboard/a2-web-final.log`. Boundary, Dashboard model, and F18 focused checks passed 22/22. `npm run check:web-m1` and both `npm run build:web` runs passed. The RED log is `a2-boundary-red.log` in the same directory. The baseline revision and verified candidate hashes support repeatable comparison. The single-window fixture produced six expected 503 responses, with zero requests outside loopback.

A3 starts with `PAOS-METH-05`. A4 has one selected METH-11 scope. A2 delivers the decision and its documentation.

## Task index

| ID | Priority | Group / methods | Task | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-METH-01 | P1 | A1; Spec-DD, ADD | Record the baseline and improvement ownership | — |
| PAOS-METH-02 | P1 | A1; Spec-DD | Trace Dashboard criteria to source and checks | PAOS-METH-01 |
| PAOS-METH-03 | P1 | A1; Design-DD, Spec-DD | Specify the pilot design-state contract | PAOS-METH-02 |
| PAOS-METH-04 | P1 | A1; Design-DD, TDD | Check UI composition and behavior against the design contract | PAOS-METH-03 |
| PAOS-METH-05 | P1 | A3; TDD, Spec-DD | Close TDD and regression-evidence gaps for critical contracts | PAOS-METH-02 |
| PAOS-METH-06 | P2 | A3; ADD, Spec-DD | Simplify agent-slice and handoff contracts using baseline evals | PAOS-METH-05 |
| PAOS-METH-07 | P2 | A3; ADD | Measure agentic-pilot outcomes on comparable tasks | PAOS-METH-06 |
| PAOS-METH-08 | P1 | A1; FSD, Design-DD | Design incremental FSD boundaries and a transition ADR | PAOS-METH-01 |
| PAOS-METH-09 | P1 | A1; FSD, TDD | Add incremental frontend-import checks | PAOS-METH-08 |
| PAOS-METH-10 | P2 | A4; FSD | Extract necessary shared UI and infrastructure modules | PAOS-METH-18 |
| PAOS-METH-11 | P2 | A4; FSD, Spec-DD | Stabilize the public interfaces of the Tasks domain | PAOS-METH-18 |
| PAOS-METH-12 | P2 | A2; FSD, Design-DD, Spec-DD | Pilot the architecture boundaries on Dashboard | PAOS-METH-04, PAOS-METH-09 |
| PAOS-METH-13 | P2 | A4; FSD, Design-DD, TDD | Improve Tasks and Workflows boundaries where value is demonstrated | PAOS-METH-18 |
| PAOS-METH-14 | P3 | A4; FSD, ADD | Extend FSD to team and skills after a go decision | PAOS-METH-18 |
| PAOS-METH-15 | P3 | A4; FSD, Design-DD | Migrate selected remaining screens and finish the composition boundary | PAOS-METH-18 |
| PAOS-METH-16 | P3 (legacy) | reference-only B | Refine conditional methodology support in the Python plugin | —; do not execute from A |
| PAOS-METH-17 | P1 | A2; Spec-DD, Design-DD, TDD, ADD, FSD | Accept the technical Dashboard pilot and verify its contracts | PAOS-METH-12 |
| PAOS-METH-18 | P2 | A2; ADD, FSD, Spec-DD | Decide on further rollout and update documentation owners | PAOS-METH-17 |

## Detailed task cards

### Task `PAOS-METH-01`

- Task: PAOS-METH-01
- Task name: Record the baseline and improvement ownership
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: None.
- Blocks: PAOS-METH-02, PAOS-METH-08
- External references: PAOS-FUNC-01, PAOS-FUNC-02, PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-19, PAOS-FUNC-23, PAOS-FUNC-24, PAOS-FUNC-25, PAOS-FUNC-30
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Capture a current source/contract/test baseline and avoid duplicating FUNC, Web and V3 work.
- Technical value: Capture a current source/contract/test baseline and avoid duplicating FUNC, Web and V3 work.
- Product value: Preserve repaired behavior and give each new change one owner.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/planning/methodology-improvement-2026-11-15.json`; `docs/frontend/index.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Baseline and ownership map in this card; no new global registry.
- Acceptance criteria: PAOS-METH-01-AC01: Record the revision, local changes, imports and current web/plugin checks; date historical receipts explicitly. PAOS-METH-01-AC02: Classify every METH card as own/reuse/reference against FUNC/Web/V3; do not create another owner for existing AC or status. PAOS-METH-01-AC03: Assign file owners and sequence shared edits. The current FUNC JSON and G07 results give the 2026-11-18 baseline of 33 implemented and one awaiting_user_decision (F23). Reuse F01/F03–F08 and F14/F19/F24/F25 within their verified limits.
- Verification gates: V-PLAN. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: Recheck HEAD and local changes before recording a new baseline. The ownership map identifies the FUNC, Web, and V3 sources.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect + product-manager; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Baseline and ownership map in this card; no new global registry.
- Next step: Use this baseline in METH-02 and METH-08.

#### Completion Report

- status: implemented
- what was done: Recorded the revision, starting state, ownership map, and original imports.
- files touched / work locations: docs/planning/methodology-improvement-2026-11-15.*; tests/web/fixtures/dashboard-import-baseline.json
- technical value delivered: Each A task has an owner and references to FUNC/Web/V3.
- product value delivered: Existing fixes and coverage inform the Dashboard work.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: HEAD/worktree check, 19 edges in the boundary test, 57 methodology audit checks, and RU/EN/JSON consistency.
- residual risks: Edges outside the pilot have assigned removal tasks.
- follow-up: Use this baseline in METH-02 and METH-08.

### Task `PAOS-METH-02`

- Task: PAOS-METH-02
- Task name: Trace Dashboard criteria to source and checks
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-03, PAOS-METH-05
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-19, PAOS-FUNC-25
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Map Dashboard states to the existing F05–F07 criteria and checks. Track affected editor contracts as regression protections.
- Technical value: Map Dashboard states to the existing F05–F07 criteria and checks. Track affected editor contracts as regression protections.
- Product value: Assess the user contract and locate missing checks quickly.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/testing/index.md`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One Dashboard criterion map with pointers to existing checks and gaps.
- Acceptance criteria: PAOS-METH-02-AC01: For applicable Dashboard criteria, record criterion → canonical owner → source → existing test/browser scenario → receipt or explicit gap. Reuse F05–F07 and current TEST checks. PAOS-METH-02-AC02: Show partial portfolio explicitly and cover applicable empty/error/stale states. If shared navigation or editor state changes, an existing check verifies that drafts remain intact and isolated. PAOS-METH-02-AC03: Reflect changed API/data assumptions in their canonical owner and align mirrors; this traceability work neither implements F02 nor waits for F28.
- Verification gates: V-PLAN. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: FUNC retains its sources, criteria, and task statuses. Record any verification gap explicitly.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + tester; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: One Dashboard criterion map with pointers to existing checks and gaps.
- Next step: Reuse the mapping in METH-12 and METH-17.

#### Completion Report

- status: implemented
- what was done: Mapped F05–F07/F18 and V3 criteria to implementation and checks.
- files touched / work locations: docs/testing/test-map.md; docs/testing/test-map.en.md
- technical value delivered: Each applicable criterion has a current route and an observable result.
- product value delivered: Dashboard behavior can be checked consistently.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: Test map, model and freshness tests, and browser receipt evidence-hrwQrx.
- residual risks: If shared navigation changes, rerun the applicable FUNC draft scenarios.
- follow-up: Reuse the mapping in METH-12 and METH-17.

### Task `PAOS-METH-03`

- Task: PAOS-METH-03
- Task name: Specify the pilot design-state contract
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-04
- External references: PAOS-FUNC-05, PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Clarify the applicable Dashboard states against V3, F05 and available API data.
- Technical value: Clarify the applicable Dashboard states against V3, F05 and available API data.
- Product value: Close the gap between approved design, available data and the user journey.
- Scope: `DESIGN.md`; `design/2026-11-13-v3/coverage.json`; `docs/frontend/state-management.md`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Updates to existing state/coverage owners; new mockups only for necessary missing states.
- Acceptance criteria: PAOS-METH-03-AC01: Identify applicable Dashboard default/loading/empty/error/partial/stale and keyboard/focus states in both themes. Check dirty/validation/confirmation when the affected contract warrants it and record reasons for remaining not_applicable states. PAOS-METH-03-AC02: Make metric sources, units and unavailable states explicit; synthetic usage does not become application data and this task does not implement F11. PAOS-METH-03-AC03: Give design differences a disposition: repair/propose to owner/accepted gap; design agreement does not close UI-12 or human acceptance.
- Verification gates: V-PLAN. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: A new user journey or a change to approved V3 requires the owner's decision.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + frontend owner; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Updates to existing state/coverage owners; new mockups only for necessary missing states.
- Next step: Reuse the contract in the pilot browser scenario.

#### Completion Report

- status: implemented
- what was done: Aligned applicable Dashboard states and metric provenance with V3 and FUNC contracts.
- files touched / work locations: DESIGN.md; docs/frontend/state-management.md; docs/frontend/state-management.en.md
- technical value delivered: States and actions are defined for both themes.
- product value delivered: Loading, empty, errors, and partial coverage are distinguishable. Unavailable usage is explicit.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: State map, 50 browser checks, and review of light-stale.png and dark-error.png.
- residual risks: V3 user acceptance belongs to UI-12.
- follow-up: Reuse the contract in the pilot browser scenario.

### Task `PAOS-METH-04`

- Task: PAOS-METH-04
- Task name: Check UI composition and behavior against the design contract
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: PAOS-METH-03
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-05, PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Extend the existing UI harness for the pilot without a second screenshot/evidence system.
- Technical value: Extend the existing UI harness for the pilot without a second screenshot/evidence system.
- Product value: Catch composition and interaction regressions beyond overflow/contrast checks.
- Scope: `tests/web/single-window/func-g01-dashboard-acceptance.mts`; `tests/web/single-window/ui-v3-scenario.mts`; `tests/web/ui-v3-dashboard.test.mts`; `design/2026-11-13-v3/implementation-evidence.md`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Pilot checks in the existing harness and evidence in the existing owner.
- Acceptance criteria: PAOS-METH-04-AC01: Check both themes, partial/error and applicable Dashboard keyboard/focus states on the current build. If the pilot changes shared overlay/navigation, reuse the existing scenario for focus return and draft preservation. PAOS-METH-04-AC02: Checks detect deliberately changed fixture geometry/state; justify thresholds and stable regions, and make baseline updates explicitly reviewable. PAOS-METH-04-AC03: Compare differences with the design owner; separate automated technical passes from human acceptance and bind receipts to build/harness hashes.
- Verification gates: V-WEB. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: The browser uses disposable profiles and synthetic projects. Screenshots come from the local build.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + frontend owner; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Pilot checks in the existing harness and evidence in the existing owner.
- Next step: Rerun this scenario after METH-12.

#### Completion Report

- status: implemented
- what was done: Extended the browser scenario to check geometry, Tab/Enter, and states in both themes.
- files touched / work locations: tests/web/single-window/func-g01-dashboard-acceptance.mts; design/2026-11-13-v3/implementation-evidence.md
- technical value delivered: The assertion catches a deliberately broken grid and distinguishes a stale snapshot from a refreshed one.
- product value delivered: Dashboard rendering and local keyboard interaction regressions are observable on the local build.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: 50/50 in Chromium with local Web/HTTP/SQLite. evidence-hrwQrx/result.json records hashes and screenshots.
- residual risks: The run used synthetic projects. UI-12 owns V3 visual acceptance.
- follow-up: Rerun this scenario after METH-12.

### Task `PAOS-METH-05`

- Task: PAOS-METH-05
- Task name: Close TDD and regression-evidence gaps for critical contracts
- Status: planned
- Priority: P1
- Delivery group: A3
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-06
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Separate existing protections, missing regression cases and RED requirements for the next behavior change.
- Technical value: Separate existing protections, missing regression cases and RED requirements for the next behavior change.
- Product value: Preserve draft/retry/recovery/approval invariants during refactors and tooling changes.
- Scope: `TEST.md`; `tests/web/ui-draft-autosave.test.mts`; `tests/web/contracts-boundaries.test.mts`; `tests/product_agent_os/test_methodology_audit.py`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Compact risk/test mapping in TEST and existing task evidence; only meaningful missing tests.
- Acceptance criteria: PAOS-METH-05-AC01: Map risk → invariant → lowest reliable check for draft conflict/lost ACK, import boundaries, Stop/recovery, backup/restore and approval routing; reuse existing tests. PAOS-METH-05-AC02: Define the expected RED reason and minimal GREEN before each new testable change. METH-09 owns its import fixtures and can start from the ADR independently of this map. Product Python routing belongs to B. PAOS-METH-05-AC03: Setup/import failures are not RED; behavior-preserving moves use characterization/regression without artificially broken production code; F21/F22 retain full recovery ownership.
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
- Delivery group: A3
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05
- Blocks: PAOS-METH-07
- External references: None; this plan owns the work.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
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
- Delivery group: A3
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-06
- Blocks: None.
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Compare baseline and candidate on the same task set, separating orchestration correctness from solution quality.
- Technical value: Compare baseline and candidate on the same task set, separating orchestration correctness from solution quality.
- Product value: Decide on the process using outcome quality and effort rather than agent or test counts.
- Scope: `EVALS.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Baseline/candidate evidence in this card; separate correctness/quality/cost verdicts.
- Acceptance criteria: PAOS-METH-07-AC01: Record identical task inputs/AC/revision, permissions and tools, plus comparable model and reasoning effort for an actual-agent comparison. Record provenance for accepted/reopened, repair cycles, owner interventions and elapsed time. PAOS-METH-07-AC02: Report tokens/cost only with reliable provenance; unavailable is not zero and F11 telemetry is not implemented for this pilot. PAOS-METH-07-AC03: If actual-agent comparison requires unavailable authorization, limit results to deterministic routing; model-quality benefit remains insufficient_evidence and does not justify promotion.
- Verification gates: V-ADD; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: No automatic provider calls, private raw chats or unsupported productivity claims; human acceptance remains separate. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + product-manager; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Baseline/candidate evidence in this card; separate correctness/quality/cost verdicts.
- Next step: With separate authorization and recorded comparable experiment conditions. A separate deterministic-only result is valid. Confirm the selected scope and obtain separate implementation authority.

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
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-09
- External references: PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-30
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Compare retaining the current structure, strengthening current feature boundaries and bounded FSD. Choose the smallest response to demonstrated coupling.
- Technical value: Compare retaining the current structure, strengthening current feature boundaries and bounded FSD. Choose the smallest response to demonstrated coupling.
- Product value: Make the next migration reviewable without a full rewrite or unnecessary folders.
- Scope: `docs/architecture/decisions/`; `docs/frontend/index.md`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One ADR selecting the check scope and Dashboard boundary and recording costs and rollback conditions.
- Acceptance criteria: PAOS-METH-08-AC01: Compare retaining feature folders, boundaries-only improvements and partial FSD; base the ADR on coupling, testability and migration cost. PAOS-METH-08-AC02: Identify the current Dashboard composition owner and minimum public API. A pages-first design is valid if FSD is selected. Extract widgets, entities and shared only for demonstrated needs. Whole-screen TaskManager/Dashboard do not become interaction features by name. PAOS-METH-08-AC03: Specify public APIs, an owned legacy exception list with removal tasks, legacy→new bridges, fallback/rollback and sufficiency criteria; do not apply frontend FSD to backend/Python.
- Verification gates: V-PLAN. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: The ADR records rollback and scope selection. F30 remains a reference.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: One ADR selecting the check scope and Dashboard boundary and recording costs and rollback conditions.
- Next step: Test the narrow read API in METH-12.

#### Completion Report

- status: implemented
- what was done: Compared three alternatives and selected a testable boundary in the existing structure.
- files touched / work locations: docs/architecture/decisions/adr-dashboard-task-boundary.md; docs/architecture/decisions/adr-dashboard-task-boundary.en.md; docs/frontend/index*.md
- technical value delivered: Recorded public entry points, dependency owners, exceptions, and rollback conditions.
- product value delivered: METH-12 can test a single reversible interface between Dashboard and Tasks.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: Checked the ADR against FSD via Context7 and the local import graph. METH-09 exercises the rules.
- residual risks: METH-18 decides later migrations.
- follow-up: Test the narrow read API in METH-12.

### Task `PAOS-METH-09`

- Task: PAOS-METH-09
- Task name: Add incremental frontend-import checks
- Status: implemented
- Priority: P1
- Delivery group: A1
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A1 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:35
- Depends on: PAOS-METH-08
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-30
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Extend the existing boundary test using the installed AST parser and ADR rules. The check runs without starting F14 or installing dependency-cruiser.
- Technical value: Extend the existing boundary test using the installed AST parser and ADR rules. The check runs without starting F14 or installing dependency-cruiser.
- Product value: Stop coupling growth before moves without blocking all legacy code.
- Scope: `tests/web/contracts-boundaries.test.mts`; `tests/web/graph-imports.test.mts`; `tsconfig.web-m1.json`; `apps/web/src/`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: The existing command checks the frontend scope and prior backend/contracts boundaries. Resolution examples reuse current fixtures where semantics match.
- Acceptance criteria: PAOS-METH-09-AC01: The extended tests/web/contracts-boundaries.test.mts checks .ts/.tsx/.mts, type imports/re-exports/literal dynamic imports and supported aliases. RED/GREEN distinguishes a denied edge from resolution failure. Report unsupported aliases or dynamic targets explicitly. PAOS-METH-09-AC02: Enforce public APIs and ADR-defined rules for upward/same-layer/deep imports and cycles in the pilot scope. Permit entity cross-imports through a specific API only if that structure is selected. PAOS-METH-09-AC03: Pin current legacy edges and prevent growth; remove migrated modules from exceptions; preserve contracts→apps and backend→frontend prohibitions.
- Verification gates: V-BOUNDARY. Current commands are listed in TEST.md. Results are in the Completion Report.
- Risks / approval gates: Each existing exception has a source revision and removal task. The check uses the installed parser and existing resolver.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + builder; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: The existing command checks the frontend scope and prior backend/contracts boundaries. Resolution examples reuse current fixtures where semantics match.
- Next step: Remove an exception in the same change as its edge.

#### Completion Report

- status: implemented
- what was done: Extended the AST scan with import resolution, pilot rules, and exact exceptions.
- files touched / work locations: tests/web/contracts-boundaries.test.mts; tests/web/fixtures/dashboard-import-baseline.json
- technical value delivered: The check distinguishes boundary violations, cycles, computed targets, and resolution failures.
- product value delivered: New Dashboard and Tasks edges are checked before migration, and existing application boundaries are preserved.
- actual implementation date and time: 18-11-2026 17:35
- verification evidence: RED: TSX, existing edges, and Tasks imports of App and a peer screen. GREEN: 8 boundary tests and 26 affected-contract checks.
- residual risks: The 19 existing edges have owners and removal tasks. A1 introduced no new source-code edges.
- follow-up: Remove an exception in the same change as its edge.

### Task `PAOS-METH-10`

- Task: PAOS-METH-10
- Task name: Extract necessary shared UI and infrastructure modules
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: None.
- External references: None; this plan owns the work.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Extract a proven non-domain component after the METH-18 decision and inspection of its existing owner.
- Technical value: Extract a proven non-domain component after the METH-18 decision and inspection of its existing owner.
- Product value: Remove shared presentation dependencies on internal task/graph screens.
- Scope: `apps/web/src/ui/Icon.tsx`; `apps/web/src/ui/Modal.tsx`; `apps/web/src/features/tasks/CommentMarkdown.tsx`; `apps/web/src/locales/`; `apps/web/src/features/graph/GraphViews.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Minimal shared public APIs, compatibility bridges and an updated migration map.
- Acceptance criteria: PAOS-METH-10-AC01: Tie each extraction to the problem selected in METH-18 and current consumers. Shared may contain only needed primitives, safe Markdown/rendering or i18n infrastructure. Keep task status rules and task labels with their domain. PAOS-METH-10-AC02: Separate generic rendering from graph-domain mapping only with proven reuse; avoid wildcard public exports and new frontend→backend dependencies. PAOS-METH-10-AC03: Keep compatibility reexports one-way with single implementations/state; preserve theme/focus/Markdown-safety/reduced-motion regressions.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: This is a behavior-preserving move; do not change visual design, sanitization policy, APIs or data. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — shared frontend ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Minimal shared public APIs, compatibility bridges and an updated migration map.
- Next step: METH-18 selected this work and identified a specific reusable non-domain component or maintenance problem. Confirm the selected scope and obtain separate implementation authority.

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
- Task name: Stabilize the public interfaces of the Tasks domain
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: None.
- External references: PAOS-FUNC-08
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Extend the existing Tasks boundary where there is a demonstrated need. Extracting entities/task requires a clear benefit for consumers.
- Technical value: Extend the existing Tasks boundary where there is a demonstrated need. Extracting entities/task requires a clear benefit for consumers.
- Product value: Let dashboard and team use a stable task API instead of deep imports into a task screen.
- Scope: `apps/web/src/features/tasks/model.ts`; `apps/web/src/features/tasks/labels.ts`; `apps/web/src/features/dashboard/model.ts`; `packages/contracts/issues/task-profile.ts`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: An ADR-backed public API, transition adapters where needed and regression evidence.
- Acceptance criteria: PAOS-METH-11-AC01: Reusable selectors/status presentation/task labels have one owner and confirmed consumers. Extract entities/task only with demonstrated value. Drafts and commands remain interaction-owned and backend authority is preserved. PAOS-METH-11-AC02: Keep packages/contracts application-independent and free of React/UI imports; preserve F08 types and decode/persistence semantics. PAOS-METH-11-AC03: Pilot consumers use an explicit public API; semanticStatus/isBlocked/aggregation and contract-boundary tests pass, and legacy bridges have removal owners.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not duplicate business rules between service and UI or change progress/blocked semantics for structure. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: architect + builder — task domain; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: An ADR-backed public API, transition adapters where needed and regression evidence.
- Next step: METH-18 selected this work after confirming reuse or a maintenance problem with the existing Tasks API. Confirm the selected scope and obtain separate implementation authority.

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
- Task name: Pilot the architecture boundaries on Dashboard
- Status: implemented
- Priority: P2
- Delivery group: A2
- Methodologies: FSD, Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A2 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:52
- Depends on: PAOS-METH-04, PAOS-METH-09
- Blocks: PAOS-METH-17
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-18
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Improve the Dashboard boundary in one reversible ADR-aligned change. Keep data flow and screen composition if a public Tasks API is sufficient.
- Technical value: Improve the Dashboard boundary in one reversible ADR-aligned change. Keep data flow and screen composition if a public Tasks API is sufficient.
- Product value: Evaluate FSD on a real bounded screen with measurable contracts.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `apps/web/src/features/tasks/model.ts`; `apps/web/src/ui/App.tsx`; `tests/web/ui-v3-dashboard.test.mts`; `tests/web/single-window/func-g01-dashboard-acceptance.mts`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: A Dashboard checkpoint with import-ratchet results, measured boundary changes and evidence in the existing owner.
- Acceptance criteria: PAOS-METH-12-AC01: Use a minimal explicit Tasks API for required selectors, including semanticStatus/isBlocked, with a single implementation. Add pages/widgets or entities/task only where justified by the ADR and actual need. Preserve services and F18 refresh semantics. PAOS-METH-12-AC02: Preserve F05 partial coverage, F06 queue numbering and F07 recent-task ordering on current sources; pass both themes and the METH-03 state matrix. PAOS-METH-12-AC03: Record before/after boundary edges, touched files, regression/visual results and rollback; a negative outcome can stop rollout without rewriting other screens.
- Verification gates: V-WEB. Current routes are in TEST.md. Results are in the Completion Report.
- Risks / approval gates: Dashboard has zero open violations in scope. The remaining 16 exceptions retain owners.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — dashboard ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: A Dashboard checkpoint with import-ratchet results, measured boundary changes and evidence in the existing owner.
- Next step: Use the build and receipts for METH-17 technical acceptance.

#### Completion Report

- status: implemented
- what was done: Moved Dashboard to the explicit Tasks read API and removed three corresponding exceptions.
- files touched / work locations: apps/web/src/features/tasks/read.ts; apps/web/src/features/dashboard/{Dashboard.tsx,RunUsage.tsx,model.ts}; tests/web/contracts-boundaries.test.mts; tests/web/fixtures/dashboard-import-baseline.json
- technical value delivered: Four functions and the Locale type share one public entry and retain the original implementations.
- product value delivered: F05–F07 and F18 behavior is preserved on the current build.
- actual implementation date and time: 18-11-2026 17:52
- verification evidence: Two new boundary tests RED, 22/22 focused GREEN, Web 704/704, browser 50/50 before and 52/52 after. Receipts and rollback are in A2 results.
- residual risks: Dashboard has zero open violations in scope. The remaining 16 exceptions retain owners.
- follow-up: Use the build and receipts for METH-17 technical acceptance.

### Task `PAOS-METH-13`

- Task: PAOS-METH-13
- Task name: Improve Tasks and Workflows boundaries where value is demonstrated
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD, Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: None.
- External references: PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-21
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Deliver METH-18-selected changes as separate checkpoints and preserve editor and queue semantics.
- Technical value: Deliver METH-18-selected changes as separate checkpoints and preserve editor and queue semantics.
- Product value: Isolate two coupled user journeys while preserving unfinished work.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/tasks/Editor.tsx`; `apps/web/src/features/workflows/WorkflowManager.tsx`; `apps/web/src/features/workflows/recipes/`; `apps/web/src/ui/App.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Selected Tasks and/or Workflows checkpoints with their guards and owner doc updates where needed.
- Acceptance criteria: PAOS-METH-13-AC01: METH-18 explicitly selected Tasks and/or Workflows. Each selected screen has separate source hashes, checks, visual evidence and reversible changes. If both are selected and a dependency exists, do Tasks first. PAOS-METH-13-AC02: Preserve F03 new-task reset, F04 workflow drafts/CAS, dialog focus/eight tabs, preview/confirmation and queue controls; do not claim full F21 recovery closure. PAOS-METH-13-AC03: Migrated consumers do not depend on sibling-screen internals; remove migrated edges from baseline exceptions and add interaction features only for real responsibilities.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Serialize shared App/navigation/labels edits; no new workflow rules, DB migrations or scope expansion. The current request authorizes planning only.
- Complexity: L
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — tasks, then builder — workflows; sequential; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Selected Tasks and/or Workflows checkpoints with their guards and owner doc updates where needed.
- Next step: METH-18 selected Tasks and/or Workflows after evaluating Dashboard. Each selected screen has a separate checkpoint protecting drafts, CAS, navigation and focus. Confirm the selected scope and obtain separate implementation authority.

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
- Delivery group: A4
- Methodologies: FSD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: None.
- External references: PAOS-FUNC-11, PAOS-FUNC-12, PAOS-FUNC-16
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Apply validated boundaries to team/skills without implementing new capabilities.
- Technical value: Apply validated boundaries to team/skills without implementing new capabilities.
- Product value: Simplify reuse of task/dashboard primitives and safe future catalog changes.
- Scope: `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/features/skills/SkillGenerator.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Migrated team/skills one checkpoint at a time; no commitment to migrate the entire frontend.
- Acceptance criteria: PAOS-METH-14-AC01: Start after a METH-18 go/bounded_go decision for the demonstrated scope. Each selected Team or Skills area has its own checkpoint and owner. PAOS-METH-14-AC02: Preserve catalog/profile/edit/history/generation preview and unavailable usage; F11/F12/F16 retain ownership and no provider search is invoked. PAOS-METH-14-AC03: Pass public API/boundary tests and scoped UI checks; report removed legacy edges and remaining exceptions.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: P3 is optional for pilot acceptance; do not add provider calls or asset promotion. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — team/skills ownership; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Migrated team/skills one checkpoint at a time; no commitment to migrate the entire frontend.
- Next step: METH-18 selected Team and/or Skills for a demonstrated local problem. METH-13 matters only if the ADR identifies an actual dependency. Confirm the selected scope and obtain separate implementation authority.

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
- Delivery group: A4
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: None.
- External references: PAOS-FUNC-02, PAOS-FUNC-14, PAOS-FUNC-26, PAOS-FUNC-33, PAOS-FUNC-34
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Continue only approved screen moves and retain App ownership of composition/session scope.
- Technical value: Continue only approved screen moves and retain App ownership of composition/session scope.
- Product value: Reduce overall import coupling without losing history, document or graph context.
- Scope: `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Operations.tsx`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Selected-screen checkpoints, App composition map and dispositions for remaining legacy exceptions.
- Acceptance criteria: PAOS-METH-15-AC01: Deliver METH-18-selected Sessions, Artifacts, Graph or composition changes one at a time in demonstrated dependency order. Keep new Files/Database/usages features outside scope and resolve FUNC ownership conflicts before edits. PAOS-METH-15-AC02: Keep composition/global providers/session selection in App; move feature-local state only when justified and preserve behavior/route IDs. PAOS-METH-15-AC03: Allow no unauthorized legacy/deep/upward imports in the selected migrated scope; remove compatibility adapters only after consumer inventory and regression checks.
- Verification gates: V-WEB; profile above; current TEST routing takes precedence; execute during future implementation.
- Risks / approval gates: Do not claim full FSD from folders alone; unselected scope remains explicitly bounded legacy. The current request authorizes planning only.
- Complexity: L
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: builder — one screen owner at a time; proposed ownership; delegation=0 now.
- Skills: build-web-apps:frontend-testing-debugging; for future UI verification only; architecture follows the ADR.
- Output artifacts: Selected-screen checkpoints, App composition map and dispositions for remaining legacy exceptions.
- Next step: METH-18 selected specific screens or a composition change. Order follows each screen's demonstrated dependencies. Confirm the selected scope and obtain separate implementation authority.

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
- Record kind: cross_track_reference
- Canonical implementation owner: [direction B](user-project-methodologies-2026-11-15.en.md); PAOS-PMETH-03, PAOS-PMETH-07, PAOS-PMETH-10, PAOS-PMETH-11, PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-22, PAOS-PMETH-23, PAOS-PMETH-26
- Acceptance semantics: Retain the three AC below as legacy coverage; execute them through canonical B owners. This record has no independent implementation status.
- Methodologies: Spec-DD, FSD, TDD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: None; reference-only.
- Blocks: None.
- External references: PAOS-PMETH-03, PAOS-PMETH-07, PAOS-PMETH-10, PAOS-PMETH-11, PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-22, PAOS-PMETH-23, PAOS-PMETH-26; reference-only, no hard dependency.
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Retain the previous ID and AC while transferring implementation ownership to B.
- Technical value: Transfer only demonstrated pilot lessons into plugin recommendations and verification evidence.
- Product value: Give target projects proportionate recommendations rather than FSD mandates based on folder names.
- Scope: Cross-track references and AC mapping only; retain former work locations in the JSON reference. Execute no code from this record.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: One canonical product owner in B without a duplicate A task.
- Acceptance criteria: PAOS-METH-16-AC01: Compare baseline/candidate cases for small frontends, growing coupled frontends, backend-only, native-only, misleading features folders, missing source and already-bounded frontends. PAOS-METH-16-AC02: Use RED/GREEN for new detection/routing behavior; distinguish not_applicable/applicable_missing/present_unverified and never treat missing evidence as proof of a violation. PAOS-METH-16-AC03: The proposal does not mutate targets or activate hooks/agents, and folder detection is not import/runtime proof; align RU/EN docs and catalog/evals.
- Verification gates: V-REFERENCE; links/AC mappings/status ownership and removal of former active edges.
- Risks / approval gates: This repo pilot does not prove broad usefulness; prompt/routing changes require separate baseline comparison, not installation. The current request authorizes planning only.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: No execution/delegation from this reference; owners are assigned in B.
- Skills: python-design-patterns + python-code-style; advisory, for the future Python slice only.
- Output artifacts: Retained references/links to B; B owns implementation artifacts.
- Next step: Select a separately authorized B PMETH task without waiting for internal METH-18 go.

#### Completion Report

- status: planned
- what was done: Planning record reclassified as reference-only; implementation not started.
- files touched / work locations: No implementation files changed now; future locations are listed in Scope.
- technical value delivered: Not claimed before implementation.
- product value delivered: Not claimed before implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Only plan preparation is checked; this task's AC are not claimed as executed.
- residual risks: This repo pilot does not prove broad usefulness; prompt/routing changes require separate baseline comparison, not installation.
- follow-up: Track B coverage without a second implementation or status authority.

### Task `PAOS-METH-17`

- Task: PAOS-METH-17
- Task name: Accept the technical Dashboard pilot and verify its contracts
- Status: implemented
- Priority: P1
- Delivery group: A2
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A2 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:58
- Depends on: PAOS-METH-12
- Blocks: PAOS-METH-18
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22, PAOS-FUNC-23, UI-12
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Reconcile Dashboard and import-ratchet evidence for one verified build and its sources. Include changed shared contracts and the owners of their checks.
- Technical value: Reconcile Dashboard and import-ratchet evidence for one verified build and its sources. Include changed shared contracts and the owners of their checks.
- Product value: Accept a useful bounded result with explicit gaps before scaling.
- Scope: `tests/web/contracts-boundaries.test.mts`; `tests/web/ui-v3-dashboard.test.mts`; `tests/web/single-window/func-g01-dashboard-acceptance.mts`; `docs/planning/methodology-improvement-2026-11-15.md`. Future work locations, with exact files confirmed for the selected scope.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: AC/evidence reconciliation and a reasoned pilot_accepted/partial/blocked verdict.
- Acceptance criteria: PAOS-METH-17-AC01: Each mandatory Dashboard criterion and import rule has a current check/receipt or explicit gap. Required checks for affected contracts pass and findings have dispositions. PAOS-METH-17-AC02: Verify partial/error Dashboard, navigation/focus and contract independence in the affected scope. Verify scope/session and drafts if shared paths change. Reuse recovery/backup receipts only if relevant state is unchanged. PAOS-METH-17-AC03: Review and verdict cover the technical Dashboard pilot. METH-07 and METH-10/11/13–15 do not gate acceptance. UI-12/F23 human acceptance and F19 full product E2E retain their owners.
- Verification gates: V-INTEGRATED. Current routes are in TEST.md. Results are in the Completion Report.
- Risks / approval gates: The verdict covers the local technical pilot. UI-12/F23 and F19 retain their acceptance owners.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: tester + reviewer; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: AC/evidence reconciliation and a reasoned pilot_accepted/partial/blocked verdict.
- Next step: Use the comparison in METH-18.

#### Completion Report

- status: implemented
- what was done: Reconciled criteria against build, browser, visual, and boundary evidence. Verdict pilot_accepted.
- files touched / work locations: tests/web/single-window/func-g01-dashboard-acceptance.mts; docs/planning/methodology-improvement-2026-11-15.md; docs/planning/methodology-improvement-2026-11-15.en.md; design/2026-11-13-v3/implementation-evidence.md
- technical value delivered: Sixteen hashes pin source, tests, and build. Verified both themes, errors, and keyboard navigation to task detail.
- product value delivered: The Dashboard user journey was verified locally.
- actual implementation date and time: 18-11-2026 17:58
- verification evidence: Compared 50 matching checks plus two navigation checks. Web 704/704, zero skips. Screenshots and service behavior were reviewed.
- residual risks: The verdict covers the local technical pilot. UI-12/F23 and F19 retain their acceptance owners.
- follow-up: Use the comparison in METH-18.

### Task `PAOS-METH-18`

- Task: PAOS-METH-18
- Task name: Decide on further rollout and update documentation owners
- Status: implemented
- Priority: P2
- Delivery group: A2
- Methodologies: ADD, FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner requested A2 implementation.
- Validator target: detailed task blocks
- Date and time of task implementation: 18-11-2026 17:58
- Depends on: PAOS-METH-17
- Blocks: PAOS-METH-10, PAOS-METH-11, PAOS-METH-13, PAOS-METH-14, PAOS-METH-15
- External references: PAOS-FUNC-25
- Source: [baseline and source hashes](methodology-improvement-2026-11-15.en.json); current paths below; external refs are references only.
- Short description: Choose go/bounded_go/hold/stop for each next area using evidence.
- Technical value: Choose go/bounded_go/hold/stop for each next area using evidence.
- Product value: Scale useful changes and stop unsupported complexity.
- Scope: `docs/architecture/decisions/`; `docs/frontend/`; `docs/testing/`; `docs/sources/registry.md`; `PLAN.md`; `RUNLOG.md`. Future work locations, not files changed now.
- Non-goals: New product features, provider/credentials, target/Git/publication/production; other FUNC/Web statuses; anything outside this slice.
- Expected result: Reviewable rollout decision in the existing ADR/evidence owner and a compact handoff.
- Acceptance criteria: PAOS-METH-18-AC01: Compare baseline and Dashboard pilot using unauthorized edges, regression findings and change/review effort. Consider ADD outcome metrics separately when comparable METH-07 evidence exists. PAOS-METH-18-AC02: Record separate scope, owner, measurable benefit, go/bounded_go/hold/stop and rollback decisions for METH-10/11/13–15. If the case for expansion is unproven, stop after Dashboard. B makes its own decision. PAOS-METH-18-AC03: Update only affected docs/registry/control-plane owners; change active rules only in a separately authorized slice and preserve existing FUNC/Web status and release gates.
- Verification gates: V-PLAN. Current routes are in TEST.md. Results are in the Completion Report.
- Risks / approval gates: Wider migration requires its own evidence. METH-07 owns ADD metrics.
- Complexity: M
- Estimated execution time: Estimate after current discovery and bounded-slice selection; no calendar commitment.
- Agents: product-manager + architect; owner decision; proposed ownership; delegation=0 now.
- Skills: documentation-and-adrs; select other skills for the actual change.
- Output artifacts: Reviewable rollout decision in the existing ADR/evidence owner and a compact handoff.
- Next step: A3 starts at METH-05. METH-11 uses the selected ADR scope.

#### Completion Report

- status: implemented
- what was done: Kept the Dashboard pilot and selected a narrow METH-11 scope for TeamManager. METH-10/13/14/15 are on hold.
- files touched / work locations: docs/architecture/decisions/adr-dashboard-task-boundary.md; docs/architecture/decisions/adr-dashboard-task-boundary.en.md; PLAN.md; RUNLOG.md; docs/frontend/index*.md; docs/planning/methodology-improvement-2026-11-15.*
- technical value delivered: Recorded the boundary comparison, change size, measurable two-exception target, and rollback.
- product value delivered: A3 can start at METH-05. A4 expansion first tests one analogous consumer.
- actual implementation date and time: 18-11-2026 17:58
- verification evidence: Verified counts of 19 → 16 and 3 → 0, tests and screenshots, the ADR, and synchronized RU/EN/JSON statuses.
- residual risks: Wider migration requires its own evidence. METH-07 owns ADD metrics.
- follow-up: A3 starts at METH-05. METH-11 uses the selected ADR scope.

