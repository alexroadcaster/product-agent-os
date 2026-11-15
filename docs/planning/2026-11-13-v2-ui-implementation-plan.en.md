# Product-Agent OS desktop UI/UX redesign plan — V2

The plan is stored with the concepts outside the published MkDocs site: it is an owner-selection proposal, not a new page of the current guide.

Source status: project-authored proposal, 13.11.2026; all tasks planned; application implementation has not started.

## Scope

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Owning design: [DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/DESIGN.md)
- This plan is separate from M1–M5; their IDs, statuses and dependencies remain unchanged.
- The current authorized stage covers research, concepts and planning. The cards below describe future implementation after a separate request.
- Functional non-goals: backend/API/schema/permissions/provider/queue semantics and new product capabilities. UI/UX only; no mobile version.
- Estimates are preliminary: 108–182 total engineering hours for sequential execution, not a calendar commitment. Reassess after UI-01. Dependencies determine order and do not authorize automatic execution.
- Rollback: Own UI hunks against each slice baseline; no DB changes, git reset, deployment or deletion of others' edits.
- Verification includes current source state, current-build receipts and mandatory gates in TEST.md; no test count is promised in advance.

## V2 refinement — required coverage

V2 replaces the earlier A/B/C comparison with the paired Porcelain/Obsidian design. The original plan is retained at `../2026-11-13/implementation-plan.md`; UI-01–UI-12 identify the same future tasks, not a new parallel queue. All cards remain planned.

- Canonical design inventory: [coverage.json](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v2/coverage.json). For UI-01, map each source-owned tab/action to the actual app baseline; proposed organization must not be presented as an existing route.
- UI-02/03: both themes, 14 destinations, token parity, desktop 1280/1440/1920; album review controls do not enter the application.
- UI-04: list/board; all eight task tabs; create/move/delete; components/versions/release policy/board/archive.
- UI-05/06: general/project/connection/shutdown; assignments, states, transitions, diagram/recipes, publication, migration, versions/archive; execution steps/recovery and queue.
- UI-07/08: both session levels, all agents/skills tabs and generation, discovery/import, graph/list/node, document proposal/diff.
- UI-09: overview/checks/autonomy/decisions/search/import/backup with all preview/confirmation and receipt surfaces.
- UI-10/11: loading/empty/error/stale/disabled/dirty/confirmation/paused; keyboard/focus, contrast in both themes, no root overflow. Verify real HTTP outcomes; prototype simulation is not carried into production.
- UI-12: human approval of screens and scenarios separately from automated verification.

Introduce motion in each UI slice after verifying its actual states; UI-10 establishes final consistency, not late decoration. This matrix does not authorize installing dependencies, functional expansions or publication. The V1 estimate of 108–182 hours remains a historical preliminary range; UI-01 must reassess the scope after a complete baseline and V2 approval.

## Index

| ID | Task | Dependencies | Estimate | Status |
| --- | --- | --- | --- | --- |
| UI-01 | Select a direction and establish the baseline | none | 4–8 h | planned |
| UI-02 | Semantic tokens and component library | UI-01 | 8–14 h | planned |
| UI-03 | Shell, navigation and content width | UI-01, UI-02 | 8–14 h | planned |
| UI-04 | Tasks and object panel | UI-02, UI-03 | 12–20 h | planned |
| UI-05 | Settings and connection | UI-02, UI-03 | 8–12 h | planned |
| UI-06 | Workflows, transitions, migration and queue | UI-02, UI-03 | 14–22 h | planned |
| UI-07 | Sessions and execution context | UI-02, UI-03 | 10–16 h | planned |
| UI-08 | Resource catalogs and project map | UI-02, UI-03 | 10–18 h | planned |
| UI-09 | Overview, checks, decisions and maintenance operations | UI-02, UI-03 | 10–16 h | planned |
| UI-10 | Motion, states and accessibility | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09 | 8–14 h | planned |
| UI-11 | Contract regression and visual verification | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10 | 12–20 h | planned |
| UI-12 | Design acceptance and implementation documentation | UI-11 | 4–8 h | planned |

## Detailed task cards

### Task `UI-01`

- Task: UI-01 — Select a direction and establish the baseline
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: none
- Blocks: UI-02, UI-03
- Source: DESIGN.md; App.tsx; TaskManager.tsx; WorkflowManager.tsx
- Short description: Agree on paired Porcelain/Obsidian and the complete V2 catalog; capture before screenshots of all 14 sections and states; map parity of existing actions and eight task tabs.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: design/2026-11-13-v2/; apps/web/src/ (read-only baseline)
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Baseline screenshots; parity map in DESIGN.md
- Acceptance criteria: All destinations, fields and confirmations are listed; cover 1280/1440/1920 viewports and a narrow desktop window; record the owner's choice separately from technical verification.
- Verification gates: Compare source and before captures; keyboard smoke on a disposable fixture.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 4–8 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: product-manager + read-only explorer; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Baseline screenshots; parity map in DESIGN.md
- Next step: Present both themes, all screen IDs and the motion lab to the owner.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Present both themes, all screen IDs and the motion lab to the owner.

### Task `UI-02`

- Task: UI-02 — Semantic tokens and component library
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-01
- Blocks: UI-03, UI-04, UI-05, UI-06, UI-07
- Source: apps/web/src/design/theme.css; apps/web/package.json
- Short description: Create the selected palette/type/spacing/radius/motion scales, shared button/input/select/badge/alert/tooltip wrappers and a unified SVG set.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/design/; presentation primitives under apps/web/src/ui/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Tokens, primitives, icon mapping, component specimens
- Acceptance criteria: All colors/fonts use tokens; eight applicable control states; accessible label/focus/error; contrast text 4.5/UI 3; existing handlers preserved.
- Verification gates: Component rendering, contrast checks, typecheck/build; dependencies only after local license review and an owner decision.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 8–14 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; reviewer read-only; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Tokens, primitives, icon mapping, component specimens
- Next step: Record the chosen theme and package decision before installation.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Record the chosen theme and package decision before installation.

### Task `UI-03`

- Task: UI-03 — Shell, navigation and content width
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-01, UI-02
- Blocks: UI-04, UI-05, UI-07, UI-08, UI-09
- Source: App.tsx:77–92,220–267,341–397; design/app.css
- Short description: Group 14 destinations; add icons, a compact header and project switcher; define a responsive desktop grid and inspector route.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/ui/App.tsx; apps/web/src/design/app.css; apps/web/src/locales/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Shell and navigation presentation
- Acceptance criteria: All 14 destinations are available; project context is preserved; no root overflow; current/focus states are visible; narrow viewport behavior does not regress.
- Verification gates: Source parity; bounding boxes/scrollWidth at 1024/1280/1440/1920; keyboard navigation; RU/EN labels; existing App tests.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 8–14 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Shell and navigation presentation
- Next step: Reproduce overflow on the baseline, then implement a minimal corrective UI slice.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Reproduce overflow on the baseline, then implement a minimal corrective UI slice.

### Task `UI-04`

- Task: UI-04 — Tasks and object panel
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/TaskManager.tsx; Editor.tsx; Panels.tsx
- Short description: Compact list/board and inspector; eight tabs with separate content; create/move/delete and task settings panels per coverage.json; preserve current parent links.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/tasks/; task CSS; ui/TaskRelations.tsx; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Task workspace, detail panel, tab overflow
- Acceptance criteria: Preserve eight tabs and filter/group/archive/attachments/links/comments; dirty data and scroll are not lost; move uses the existing preview; long values remain fully accessible.
- Verification gates: Reproduce RED for overflow/selection loss; scoped tests; task lifecycle browser; payload/revision parity; screenshot at all desktop sizes.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: high: complex states and regression risks
- Estimated execution time: 12–20 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; tester with scenario ownership; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Task workspace, detail panel, tab overflow
- Next step: Implement one vertical slice: list → detail → existing edit/preview.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Implement one vertical slice: list → detail → existing edit/preview.

### Task `UI-05`

- Task: UI-05 — Settings and connection
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/Settings.tsx; ui/ConnectionControls.tsx; design/app.css
- Short description: Split settings into compact local panels: general, projects, connection and local service; move large workflow forms out of the shared canvas.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/tasks/Settings.tsx; apps/web/src/ui/ConnectionControls.tsx; settings presentation; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Compact settings navigation, connection states
- Acceptance criteria: Keep native picker/Add/Cancel behavior; do not simulate connection state; technical details remain available; Quit retains its checkbox; preserve active BYOK state.
- Verification gates: Existing settings/connection tests; bounded fixture disconnected/waiting/connected/error; keyboard; Cancel no-mutation; screenshots.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 8–12 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Compact settings navigation, connection states
- Next step: Preserve owning state when switching local settings panels.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Preserve owning state when switching local settings panels.

### Task `UI-06`

- Task: UI-06 — Workflows, transitions, migration and queue
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: WorkflowManager.tsx; recipes/RecipeRunner.tsx; recipes/QueueManager.tsx
- Short description: List states/transitions with a selected editor; separate assignments/recipes/version/migration tabs and an execution/queue subpanel.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/workflows/; workflow CSS; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Transition workbench and compact execution views
- Acceptance criteria: Every original field is available; an error expands its group; draft is preserved; validate/preview/publish/migrate confirmations are identical; pinned IDs and required checks remain unchanged.
- Verification gates: Workflow/recipe/queue tests; keyboard editing; stale revision rejection; migration preview; fixture destructive confirmation; schematic/table parity.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: high: complex states and regression risks
- Estimated execution time: 14–22 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; tester; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Transition workbench and compact execution views
- Next step: First replace only transition map rendering, preserving state and command functions.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: First replace only transition map rendering, preserving state and command functions.

### Task `UI-07`

- Task: UI-07 — Sessions and execution context
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/sessions/SessionsCatalog.tsx; ui/SessionContext.tsx; ui/Operations.tsx
- Short description: Work/Full available history and Chat/Context/Changes; central transcript, run profile/checks/questions/decision; compact events and a stable composer.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/sessions/; apps/web/src/ui/SessionContext.tsx; ui/Operations.tsx; session CSS
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Session workbench and state specimens
- Acceptance criteria: Send/Stop and approvals are visible; terminal ACK is not replaced by animation; no auto-send; selected session and draft persist; stale and disconnected are distinct.
- Verification gates: Session tests; synthetic send/pending/stop/ACK/no-agent scenarios; long transcript/long path; keyboard focus; screenshot evidence.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: high: complex states and regression risks
- Estimated execution time: 10–16 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; tester; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Session workbench and state specimens
- Next step: Check existing polling/scroll behavior without changing transport.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Check existing polling/scroll behavior without changing transport.

### Task `UI-08`

- Task: UI-08 — Resource catalogs and project map
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/team/TeamManager.tsx; features/skills/SkillGenerator.tsx; features/graph/GraphExplorer.tsx; features/artifacts/ArtifactExplorer.tsx
- Short description: Agents and skills: all Profile/Edit/History/Activity; generation and discovery/import; documents reader/proposal/diff; graph/list/node with source/occurrences/related tasks.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/features/team/; skills/; graph/; artifacts/; corresponding CSS
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Resource catalogs, readable graph inspector
- Acceptance criteria: Source/staged/stale/unresolved states are visible; graph preserves actual relationship types and limits; source opens as before; the text alternative is complete.
- Verification gates: Existing catalog/graph/artifact tests; exact fixture node-edge label comparison; keyboard graph/list; long paths; rendered contrast.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 10–18 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: graph-cockpit-engineer or builder; reviewer read-only; one write owner per slice; independent reviewer is read-only.
- Skills: data-visualization, ui-ux-pro-max
- Output artifacts: Resource catalogs, readable graph inspector
- Next step: Use the existing SVG/DOM renderer before selecting new dependencies.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Use the existing SVG/DOM renderer before selecting new dependencies.

### Task `UI-09`

- Task: UI-09 — Overview, checks, decisions and maintenance operations
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: ui/App.tsx; features/decisions/DecisionBoard.tsx; features/autonomy/AutonomyManager.tsx; existing search/import/backup surfaces
- Short description: Unify visual patterns for overview, checks, autonomy, decisions, search, import and backup; move dangerous/review actions out of primary content.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/ui/App.tsx; decisions/; autonomy/; presentation components; locales
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Remaining sections visual parity
- Acceptance criteria: All existing actions remain available; no fake KPI; acceptance is separate from test results; preserve import/restore preview and confirmations; permissions unchanged.
- Verification gates: Existing decisions/autonomy/import/backup tests; expiry/stale/denied fixture states; keyboard; before/after action map; screenshots.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 10–16 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Remaining sections visual parity
- Next step: Use the action list from UI-01 and update one section at a time.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Use the action list from UI-01 and update one section at a time.

### Task `UI-10`

- Task: UI-10 — Motion, states and accessibility
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09
- Blocks: UI-11
- Source: DESIGN.md: motion, states, accessibility; TEST.md existing a11y
- Short description: Reconcile micro-interactions already built into slices: 100–240ms, skeleton/refresh/progress, result/error/stale/empty, focus/keyboard/modal and reduced motion; remove layout shift and false success.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: apps/web/src/design/; affected presentation components; tests/web/accessibility/
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Motion tokens, state coverage, a11y repairs
- Acceptance criteria: No transition all/layout property animation; reduced motion works; content readable without animation; tab order stable; hidden sections do not hide errors; important errors are not auto-dismissed.
- Verification gates: Current-build contrast; RU/EN; light/dark only supported approved themes; keyboard/modal focus; browser zoom; reduced-motion screenshot; current a11y gates.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 8–14 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: builder for CSS; tester for independent checks; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Motion tokens, state coverage, a11y repairs
- Next step: Check the shared component layer before local exceptions.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Check the shared component layer before local exceptions.

### Task `UI-11`

- Task: UI-11 — Contract regression and visual verification
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10
- Blocks: UI-12
- Source: TEST.md; EVALS.md; current Web tests and browser harnesses
- Short description: Compare functional parity with the baseline; measure overflow and layout states on the final build; fix actual defects.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: tests/web/; isolated fixture evidence; own UI repairs
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Regression receipts, visual captures, unresolved gaps
- Acceptance criteria: No previous API contract/permission/preview/draft flow has changed; all necessary tests pass; required gates are not skipped; screen evidence is tied to current source.
- Verification gates: npm run check:web-m1; npm run build:web; node --test tests/web/*.test.mts; applicable synthetic browser/a11y gates from TEST.md; docs gates and diff check.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: high: complex states and regression risks
- Estimated execution time: 12–20 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: tester + reviewer (read-only assurance); builder for scoped fixes; one write owner per slice; independent reviewer is read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Regression receipts, visual captures, unresolved gaps
- Next step: Run focused gates, then the required integrated suite once on the final state.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Run focused gates, then the required integrated suite once on the final state.

### Task `UI-12`

- Task: UI-12 — Design acceptance and implementation documentation
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Multi-slice desktop UI redesign with functional parity and owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-11
- Blocks: none
- Source: DESIGN.md; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md
- Short description: Review the full catalog in both themes and owner scenarios for tasks/workflows/sessions/import/backup; compare quality with the selected concept; record limits, rollback and the next step.
- Technical value: A unified view of existing contracts, controlled UI boundaries and verifiable rollback.
- Product value: Less searching and unnecessary scrolling; clear actions and results without changing capabilities.
- Scope: DESIGN.md; control-plane pointers; owning implementation evidence
- Non-goals: Changes to backend/API/DB/permissions/model providers and business logic; mobile, publication and Git actions.
- Expected result: Acceptance record, current DESIGN, handoff
- Acceptance criteria: Owner feedback is separate from automatic tests; results and gaps are accurate; functional expansions are not hidden in UI scope; no deployment or Git without request.
- Verification gates: Self-review/independent review of the report; python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; python tools/check_docs.py; git diff --check.
- Risks / approval gates: Owner direction selection and a separate implementation request; preserve drafts and confirmations; stop the affected slice if a contract change is needed. A new dependency requires license review and separate installation approval.
- Complexity: medium: bounded presentation scope with required parity
- Estimated execution time: 4–8 h; preliminary estimate, excluding the wait for an owner decision.
- Agents: product-manager + docs-maintainer; one write owner per slice; independent reviewer is read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Acceptance record, current DESIGN, handoff
- Next step: Present final images and working scenarios to the owner.

#### Completion Report

- status: planned
- what was done: Future scope and acceptance have been specified; implementation of this card has not been performed.
- files touched / work locations: Only this planning card; target implementation files have not yet been changed under this plan.
- technical value delivered: Contract for a future slice; no runtime result.
- product value delivered: A verifiable UX outcome is specified; improvement has not yet been measured.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Required future checks are listed under Verification gates; there is no execution result for this card.
- residual risks: Owner selection, baseline details and regression effects remain to be checked.
- follow-up: Present final images and working scenarios to the owner.


