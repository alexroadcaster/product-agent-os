# Product-Agent OS desktop UI/UX redesign plan — V3

The plan is stored with the concepts outside the published MkDocs site. The owner approved the design; this document governs local UI/UX implementation, not publication.

Source status: approved V3 + Sidebar collapse, 13.11.2026; UI-01–UI-12 reopened: V3 repair locally verified; UI-12 needs_user_acceptance; overall status is in_progress until acceptance. The owner authorized UI/UX implementation; functional contracts must be preserved.


## Reopened after visual audit

Current checkpoint: full visual review of 85 screens × 2 themes completed; final build, web500 and V3 browser378 passed. All 170 states were reviewed again. [Side-by-side gallery](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-gallery.html), [ledger](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-visual-review.json), [current checks and differences](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md). UI-01–UI-11 have local evidence; cards remain in_progress until acceptance resolves the differences, and UI-12 is not closed. Historical Completion Reports below do not replace the current comparison.

Previous Completion Reports below are historical results from the first implementation, not proof of visual parity. The owner rejected the implementation. All UI-01–UI-12 were reopened on 13.11.2026.

1. Shell: sidebar groups, header, local navigation and consistent rhythm.
2. Tasks: compact list, 420px inspector, full two-column form, full-screen window and actions.
3. Settings/workflows: vertical navigation, forms and nested states with draft preservation.
4. Dashboard/team/sessions/graph/artifacts/operations: transfer the composition without substituting synthetic behavior.
5. Motion: source springs sidebar, tabs/panels/modal/reduced motion.
6. Compare 87 coverage.json entries: product screens separately from two review labs; light and dark themes for every available state, screenshot plus composition assessment.
7. Regression-check existing contracts and update evidence. Owner acceptance is separate.

Visual audit RED: task title in a four-column row, planning in five, create-agent button 63px; filters/settings/archive are not in their V3 positions. Earlier tests checked overflow/contrast, not composition.

## Scope

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Owning design: [DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/DESIGN.md)
- This plan is separate from M1–M5; their IDs, statuses and dependencies remain unchanged.
- The owner approved the design and authorized UI-01–UI-12. Local frontend implementation and synthetic verification are in progress. Acceptance of the implementation is separate from design approval.
- Functional non-goals: backend/API/schema/permissions/provider/queue semantics and new product capabilities. UI/UX only; no mobile version.
- V1 estimates of 108–182 hours are historical and do not apply to V3. New scope includes portfolio/agent dashboards, task overlay and two graph renderers; individual card times were not measured and no calendar commitment is made.
- Rollback: Own UI hunks against each slice baseline; no DB changes, git reset, deployment or deletion of others' edits.
- Verification includes current source state, current-build receipts and mandatory gates in TEST.md; no test count is promised in advance.

## V2 refinement — required coverage

V2 replaced the earlier A/B/C comparison with the paired Porcelain/Obsidian design. The original plan is retained at `../2026-11-13/implementation-plan.md`; UI-01–UI-12 identify the same implementation tasks, not a new parallel queue. Current implementation statuses are owned by the index and cards below.

- Canonical design inventory: [coverage.json](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/coverage.json). For UI-01, map each source-owned tab/action to the actual app baseline; proposed organization must not be presented as an existing route.
- UI-02/03: both themes, 15 destinations, token parity, desktop 1280/1440/1920; album review controls do not enter the application.
- UI-04: list/board; all eight task tabs; create/move/delete; components/versions/release policy/board/archive.
- UI-05/06: general/project/connection/shutdown; assignments, states, transitions, diagram/recipes, publication, migration, versions/archive; execution steps/recovery and queue.
- UI-07/08: both session levels, all agents/skills tabs and generation, discovery/import, graph/list/node, document proposal/diff.
- UI-09: overview/checks/autonomy/decisions/search/import/backup with all preview/confirmation and receipt surfaces.
- UI-10/11: loading/empty/error/stale/disabled/dirty/confirmation/paused; keyboard/focus, contrast in both themes, no root overflow. Verify real HTTP outcomes; prototype simulation is not carried into production.
- UI-12: human approval of screens and scenarios separately from automated verification.

Introduce motion in each UI slice after verifying actual states; UI-10 establishes final consistency, not late decoration. Necessary local frontend dependencies are within authorized implementation; versions and licenses are checked and global installation is unnecessary. Functional expansions and publication are excluded. The V1 estimate of 108–182 hours remains a historical preliminary range; UI-01 must reassess scope after a complete baseline of approved V3.

## V3 refinement — required criteria for six improvements

V3 replaces V2 as the approved direction; the V2 archive is unchanged. UI-01–UI-12 are authorized for implementation. A completed prototype alone does not satisfy application verification. [Complete field map](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/task-field-map.md), [research](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/research.md) and [coverage](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/coverage.json) refine the following criteria:

| Card | Required V3 improvement | Implementation verification |
| --- | --- | --- |
| UI-01 | Separate available source data from proposed analytics; approve all screens/both modes | in_progress |
| UI-02 | Duoicons from icons0/Iconify, consistent two-tone geometry and semantic colors | in_progress |
| UI-03 | Shared environment for all projects and explicit entry to a specific project | in_progress |
| UI-04 | Full task dialog via double click plus button/Enter, all Editor fields and eight tabs | in_progress |
| UI-07 | Session/task usage with source and unknown values | in_progress |
| UI-08 | Dashboard for all agents and each agent; D3 graph + Mermaid whole/module + list | in_progress |
| UI-09 | Portfolio/project dashboards: progress, remaining work, queue, load and usage | in_progress |
| UI-10 | GSAP lifecycle, reduced motion, local loading/feedback transitions | in_progress |
| UI-11 | Numeric invariants, actual renderer activation, all routes in both themes | in_progress |
| UI-12 | Approval of the new gallery and future analytics contract | in_progress |

Token usage collection requires a separate functional decision. Portfolio aggregates existing complete task snapshots in the presentation layer. An honest unavailable state is permitted initially in the UI slice. Actual usage collection/storage and provider prices are outside this plan. Historical V1/V2 estimates do not cover the new scope and must be reassessed in UI-01.

## Index

| ID | Task | Dependencies | Historical V1 estimate | Status |
| --- | --- | --- | --- | --- |
| UI-01 | Select a direction and establish the baseline | none | baseline V3 | in_progress |
| UI-02 | Semantic tokens and component library | UI-01 | 8–14 h | in_progress |
| UI-03 | Shell, navigation and content width | UI-01, UI-02 | 8–14 h | in_progress |
| UI-04 | Tasks and object panel | UI-02, UI-03 | 12–20 h | in_progress |
| UI-05 | Settings and connection | UI-02, UI-03 | 8–12 h | in_progress |
| UI-06 | Workflows, transitions, migration and queue | UI-02, UI-03 | 14–22 h | in_progress |
| UI-07 | Sessions and execution context | UI-02, UI-03 | 10–16 h | in_progress |
| UI-08 | Resource catalogs and project map | UI-02, UI-03 | 10–18 h | in_progress |
| UI-09 | Overview, checks, decisions and maintenance operations | UI-02, UI-03 | 10–16 h | in_progress |
| UI-10 | Motion, states and accessibility | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09 | 8–14 h | in_progress |
| UI-11 | Contract regression and visual verification | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10 | 12–20 h | in_progress |
| UI-12 | Design acceptance and implementation documentation | UI-11 | 4–8 h | in_progress |

## Detailed task cards

### Task `UI-01`

- Task: UI-01 — Select a direction and establish the baseline
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: none
- Blocks: UI-02, UI-03
- Source: DESIGN.md; App.tsx; TaskManager.tsx; WorkflowManager.tsx
- Short description: Record V3/Sidebar approval; capture actual app baseline, actions/fields/data sources map and baseline checks. All 87 prototype routes are layout examples, not a promise of new backend routes.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: design/2026-11-13-v3/; apps/web/src/ (read-only baseline)
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Baseline screenshots; parity map in DESIGN.md
- Acceptance criteria: All destinations, fields and confirmations are listed; cover 1280/1440/1920 viewports and a narrow desktop window; record the owner's choice separately from technical verification.
- Verification gates: Compare source and before captures; keyboard smoke on a disposable fixture.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: product-manager + read-only explorer; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Baseline screenshots; parity map in DESIGN.md
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: V3/Sidebar approval recorded; actual app baseline and data sources compared.
- files touched / work locations: DESIGN.md; implementation-evidence.md; baseline browser/build/test logs
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Baseline build0; integration112; original sandbox errors retained; final full suite outside the symlink restriction passed 500. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-02`

- Task: UI-02 — Semantic tokens and component library
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-01
- Blocks: UI-03, UI-04, UI-05, UI-06, UI-07
- Source: apps/web/src/design/theme.css; apps/web/package.json
- Short description: Transfer Porcelain/Obsidian tokens, compact controls, semantic statuses, Duoicons SVG, focus/error/loading primitives and local motion foundation without changing handlers.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/design/; presentation primitives under apps/web/src/ui/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Tokens, primitives, icon mapping, component specimens
- Acceptance criteria: All colors/fonts use tokens; eight applicable control states; accessible label/focus/error; contrast text 4.5/UI 3; existing handlers preserved.
- Verification gates: Component rendering, contrast checks, typecheck/build; dependencies only after local license review and an owner decision.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; reviewer read-only; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Tokens, primitives, icon mapping, component specimens
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Porcelain/Obsidian tokens, compact controls, colored local Duoicons, semantic states and SVG notices.
- files touched / work locations: apps/web/src/design/theme.css; workspace.css; ui/Icon.tsx; package.json; THIRD_PARTY_NOTICES.md
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Typecheck/build0; contrast desktop matrix; dependencies pinned, npm audit reported zero vulnerabilities at installation. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-03`

- Task: UI-03 — Shell, navigation and content width
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-01, UI-02
- Blocks: UI-04, UI-05, UI-07, UI-08, UI-09
- Source: App.tsx:77–92,220–267,341–397; design/app.css
- Short description: Implement Sidebar collapse 216↔64 with original springs 260/24,300/22,380/28,300/26, tooltip/keyboard/reduced motion, compact header, project switcher and entry to all projects. Preserve navigationEpoch and existing deep links.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/ui/App.tsx; apps/web/src/design/app.css; apps/web/src/locales/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Shell and navigation presentation
- Acceptance criteria: All 14 destinations are available; project context is preserved; no root overflow; current/focus states are visible; narrow viewport behavior does not regress.
- Verification gates: Source parity; bounding boxes/scrollWidth at 1024/1280/1440/1920; keyboard navigation; RU/EN labels; existing App tests.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Shell and navigation presentation
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: React Sidebar collapse 216↔64, original springs260/24,300/22,380/28,300/26; tooltip, reduced motion and all 15 destinations; navigationEpoch preserved.
- files touched / work locations: apps/web/src/ui/Sidebar.tsx; App.tsx; design/workspace.css
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Browser collapse/expand, keyboard tooltip/Escape, route persistence, reduced motion, desktop widths1280/1440/1920. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-04`

- Task: UI-04 — Tasks and object panel
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/TaskManager.tsx; Editor.tsx; Panels.tsx
- Short description: Preserve all TaskEditor fields and eight existing tabs; add a task usage unavailable surface and dblclick/Enter/explicit full-card overlay with focus return. Do not duplicate editors/commands; preserve draft, filters, drag/drop and create/save/preview/move/delete guards.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/tasks/; task CSS; ui/TaskRelations.tsx; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Task workspace, detail panel, tab overflow
- Acceptance criteria: Preserve eight tabs and filter/group/archive/attachments/links/comments; dirty data and scroll are not lost; move uses the existing preview; long values remain fully accessible.
- Verification gates: Reproduce RED for overflow/selection loss; scoped tests; task lifecycle browser; payload/revision parity; screenshot at all desktop sizes.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: high: complex states and regression risks
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; tester with scenario ownership; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Task workspace, detail panel, tab overflow
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: The single task editor switches to a native modal on dblclick/Enter/button; all eight tabs/fields/guards and drafts are preserved.
- files touched / work locations: features/tasks/TaskManager.tsx; task-detail.css; ui/Modal.tsx
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: RED→GREEN task-overlay19; existing integration112; raw multiline/invalid estimate/unsaved title and the same DOM confirmed. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-05`

- Task: UI-05 — Settings and connection
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/Settings.tsx; ui/ConnectionControls.tsx; design/app.css
- Short description: Split Settings into general/projects/connection/local service while preserving forms, native folder flow, connection statuses and shutdown confirmation; open workflows in a separate local panel.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/tasks/Settings.tsx; apps/web/src/ui/ConnectionControls.tsx; settings presentation; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Compact settings navigation, connection states
- Acceptance criteria: Keep native picker/Add/Cancel behavior; do not simulate connection state; technical details remain available; Quit retains its checkbox; preserve active BYOK state.
- Verification gates: Existing settings/connection tests; bounded fixture disconnected/waiting/connected/error; keyboard; Cancel no-mutation; screenshots.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Compact settings navigation, connection states
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Settings are split into General/Projects/Connection/Service/Workflows/All (English equivalents of the Russian UI labels); forms remain mounted.
- files touched / work locations: ui/App.tsx; ui/settings-workspace.css
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: settings-layout14; keyboard local tabs, preserved preference/project drafts and existing callbacks. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-06`

- Task: UI-06 — Workflows, transitions, migration and queue
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: WorkflowManager.tsx; recipes/RecipeRunner.tsx; recipes/QueueManager.tsx
- Short description: Compact states/transitions workbench and assignments/recipes/publication/migration/version/archive/execution/queue panels; preserve current preview digests, pinned versions, refresh-preserve-form and stop confirmations.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/workflows/; workflow CSS; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Transition workbench and compact execution views
- Acceptance criteria: Every original field is available; an error expands its group; draft is preserved; validate/preview/publish/migrate confirmations are identical; pinned IDs and required checks remain unchanged.
- Verification gates: Workflow/recipe/queue tests; keyboard editing; stale revision rejection; migration preview; fixture destructive confirmation; schematic/table parity.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: high: complex states and regression risks
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; tester; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Transition workbench and compact execution views
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Workflow workbench: definition/publication/migration/versions/execution/queue, compact state/transition rows, expansion for an invalid field; guards/preview/CAS unchanged.
- files touched / work locations: features/workflows/WorkflowManager.tsx; workflow-workbench.css
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: settings-layout14 after fixing row opening; M2b51 publication/migration scenario passed. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-07`

- Task: UI-07 — Sessions and execution context
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/sessions/SessionsCatalog.tsx; ui/SessionContext.tsx; ui/Operations.tsx
- Short description: Preserve work/history catalogs, transcript/context/changes/run/checks/questions/decision and composer/drafts; add session usage context without fabricated values or new backend calls.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/sessions/; apps/web/src/ui/SessionContext.tsx; ui/Operations.tsx; session CSS
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Session workbench and state specimens
- Acceptance criteria: Send/Stop and approvals are visible; terminal ACK is not replaced by animation; no auto-send; selected session and draft persist; stale and disconnected are distinct.
- Verification gates: Session tests; synthetic send/pending/stop/ACK/no-agent scenarios; long transcript/long path; keyboard focus; screenshot evidence.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: high: complex states and regression risks
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; tester; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Session workbench and state specimens
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Compact session catalog/transcript/composer/context grids and explicit unavailable usage; history, polling and draft lifecycle preserved.
- files touched / work locations: features/sessions/SessionsCatalog.tsx; design/workspace.css
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Existing M2b51; all destinations RU/EN light/dark; session screenshots; overall web regression500. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-08`

- Task: UI-08 — Resource catalogs and project map
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/team/TeamManager.tsx; features/skills/SkillGenerator.tsx; features/graph/GraphExplorer.tsx; features/artifacts/ArtifactExplorer.tsx
- Short description: Rework agents/skills profiles/edit/history/activity, collective and per-agent dashboards using existing metrics; documents reader/proposal/diff; D3 graph and Mermaid whole-available-page/module plus list with shared revision/coverage and node IDs.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/team/; skills/; graph/; artifacts/; corresponding CSS
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Resource catalogs, readable graph inspector
- Acceptance criteria: Source/staged/stale/unresolved states are visible; graph preserves actual relationship types and limits; source opens as before; the text alternative is complete.
- Verification gates: Existing catalog/graph/artifact tests; exact fixture node-edge label comparison; keyboard graph/list; long paths; rendered contrast.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: graph-cockpit-engineer or builder; reviewer read-only; one write owner per slice; independent reviewer is read-only.
- Skills: data-visualization, ui-ux-pro-max
- Output artifacts: Resource catalogs, readable graph inspector
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Team/per-agent dashboards, existing catalog/profile actions, D3/strict Mermaid and list from the same revision-pinned page; module filter, zoom/pan/reset.
- files touched / work locations: features/team/TeamManager.tsx; features/graph/GraphExplorer.tsx; GraphViews.tsx; diagram-source.ts; features/dashboard/
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: M2b51; M2c37; real renderer activation/node parity; unit escaping special labels; two fresh review findings fixed. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-09`

- Task: UI-09 — Overview, checks, decisions and maintenance operations
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: ui/App.tsx; features/decisions/DecisionBoard.tsx; features/autonomy/AutonomyManager.tsx; existing search/import/backup surfaces
- Short description: Portfolio and project dashboard from existing taskManager/teamMetrics/queue sources: progress, remaining work, states, queue and load. Usage is unavailable where not measured. Preserve Sources, checks, autonomy, decisions, search, import, backup and confirmations.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/ui/App.tsx; decisions/; autonomy/; presentation components; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Remaining sections visual parity
- Acceptance criteria: All existing actions remain available; no fake KPI; acceptance is separate from test results; preserve import/restore preview and confirmations; permissions unchanged.
- Verification gates: Existing decisions/autonomy/import/backup tests; expiry/stale/denied fixture states; keyboard; before/after action map; screenshots.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Remaining sections visual parity
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: Portfolio/project dashboards from taskManager/scheduler/teamMetrics; progress denominator, queue, current assignments and observed runs. Other operational surfaces received shared tokens/layout without handler changes.
- files touched / work locations: features/dashboard/Dashboard.tsx; model.ts; ui/App.tsx; design/workspace.css
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Dashboard invariants RED→GREEN5 focused tests together with diagram; no fabricated cost/tool_use; existing functional journeys. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-10`

- Task: UI-10 — Motion, states and accessibility
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09
- Blocks: UI-11
- Source: DESIGN.md: motion, states, accessibility; TEST.md existing a11y
- Short description: Reconcile motion and loading/empty/error/stale/disabled/dirty/confirmation/paused states, keyboard/focus/modal and reduced motion. Sidebar width spring is an explicitly approved exception; other motion uses transform/opacity; clean up tween/rAF on unmount.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/design/; affected presentation components; tests/web/accessibility/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Motion tokens, state coverage, a11y repairs
- Acceptance criteria: No transition all; Sidebar width spring is an approved exception; reduced motion works; content readable without animation; tab order stable; hidden sections do not hide errors; important errors are not auto-dismissed.
- Verification gates: Current-build contrast; RU/EN; light/dark only supported approved themes; keyboard/modal focus; browser zoom; reduced-motion screenshot; current a11y gates.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: builder for CSS; tester for independent checks; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Motion tokens, state coverage, a11y repairs
- Next step: Accept the current implementation against the side-by-side gallery and account for noted differences; see implementation-evidence.md for local checks.

#### Completion Report

- status: in_progress
- what was done: GSAP route heading transition with cleanup, native dialog motion, CSS state feedback/skeleton and reduced motion; exact sidebar springs remain separately owned.
- files touched / work locations: ui/App.tsx; ui/Sidebar.tsx; design/workspace.css; task/settings/workflow CSS
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Browser reduced motion/collapse/focus; accessibility core136 checks20views; contrast issue 4.428 fixed with accent-text. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Owner acceptance of the implementation under UI-12.

### Task `UI-11`

- Task: UI-11 — Contract regression and visual verification
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:47
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10
- Blocks: UI-12
- Source: TEST.md; EVALS.md; current Web tests and browser harnesses
- Short description: Verify the actual built application: baseline contract parity, RU/EN, two themes, desktop1280/1440/1920, root overflow, full task fields, sidebar, numeric source/coverage and actual D3/Mermaid render. Synthetic isolated service without provider calls.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: tests/web/; isolated fixture evidence; own UI repairs
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Regression receipts, visual captures, unresolved gaps
- Acceptance criteria: No previous API contract/permission/preview/draft flow has changed; all necessary tests pass; required gates are not skipped; screen evidence is tied to current source.
- Verification gates: npm run check:web-m1; npm run build:web; node --test tests/web/*.test.mts; applicable synthetic browser/a11y gates from TEST.md; docs gates and diff check.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: high: complex states and regression risks
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: tester + reviewer (read-only assurance); builder for scoped fixes; one write owner per slice; independent reviewer is read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Regression receipts, visual captures, unresolved gaps
- Next step: Owner acceptance of the implementation in UI-12.

#### Completion Report

- status: in_progress
- what was done: Integrated verification completed: 500 web tests, 356 V3 browser checks, focused suites and docs gates passed. Failed intermediate receipts are retained.
- files touched / work locations: tests/web/; implementation-evidence.md
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: 13-11-2026 17:47
- verification evidence: Full web500 passed; build/typecheck exit0; V3 356 checks/120 views, accessibility136, docs105/check_docs passed. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: UI-12: owner acceptance of the implementation.

### Task `UI-12`

- Task: UI-12 — Design acceptance and implementation documentation
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-11
- Blocks: none
- Source: DESIGN.md; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md
- Short description: Present implemented screens and scenarios, update DESIGN/plan/evidence/control-plane; record owner acceptance or awaiting acceptance separately; do not claim user acceptance based on automatic tests.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: DESIGN.md; control-plane pointers; owning implementation evidence
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Acceptance record, current DESIGN, handoff
- Acceptance criteria: Owner feedback is separate from automatic tests; results and gaps are accurate; functional expansions are not hidden in UI scope; no deployment or Git without request.
- Verification gates: Self-review/independent review of the report; python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; python tools/check_docs.py; git diff --check.
- Risks / approval gates: Design and implementation are owner-authorized; preserve drafts and confirmations; stop the affected slice if a contract change is needed. Necessary UI dependencies are locally installed with pinned versions and license review; backend dependencies are excluded.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: Historical V1 estimate does not apply; individual card wall time is unavailable because slices ran sequentially in one session.
- Agents: product-manager + docs-maintainer; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Acceptance record, current DESIGN, handoff
- Next step: Complete current gates and hand off the result to the owner.

#### Completion Report

- status: in_progress
- what was done: Implementation handoff prepared; the design is already approved, and user acceptance of the implementation is not substituted with automatic checks.
- files touched / work locations: DESIGN.md; implementation-plan.md; implementation-evidence.md; control-plane pointers
- technical value delivered: Presentation layer preserves existing commands, versions, authorization and data; individual frontend projections are verifiable.
- product value delivered: Compact navigation and a clear project workspace; measuring user efficiency is separate from implementation.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Human implementation acceptance pending; UI-12 remains in_progress until the owner's decision. Full receipts: [implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry is not implemented in the UI; performance on large real projects has not been measured.
- follow-up: Close only after the relevant gates and owner decision.
