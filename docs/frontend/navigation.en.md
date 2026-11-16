# Frontend navigation and screens

Source status: repository_source / focused_files_service_verified; UI_integration_acceptance_owned_by_FUNC_G03; 2026-11-15.; FUNC-G04: locally_verified_with_measured_limits, 16.11.2026.

Owner: frontend and docs-maintainer. Scope: Web/desktop UI, source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Update when sections, transitions, onboarding or related UI tests change. [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx) and [Sidebar.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Sidebar.tsx) own current behavior; [API](../api/index.md) owns HTTP contracts.

## Entry and project selection

Initialization obtains a session, projects, preferences and connection status. Without a session the pairing form appears; errors are shown and navigation is disabled until `ready`. After entry the selected existing project is retained or the first project selected. Without a project, project-specific sections show an empty state; Settings and portfolio remain separately available. The header contains breadcrumb, search, connection status and reload.

The original DG04 sidebar snapshot had15 sections grouped under Work, Knowledge, Management and Workspace; F26 adds an independent `files` section. Selecting a project or section changes React state; these are not independent URL routes. The sidebar can collapse; the narrow-layout mechanism closes it after selection and Escape returns focus to the menu button. `aria-current` marks the selected page. This mechanism does not extend the desktop design scope; see [accessibility](accessibility.md) for behavior and limits.

## Current screen map

| Identifier | Screen and transitions | Source entry |
| --- | --- | --- |
| `portfolio` | All projects; a card opens project overview, tasks or agents | [Dashboard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/dashboard/Dashboard.tsx) |
| `overview` | Dashboard, sources and usage tabs; links to tasks and agents | App and Dashboard |
| `tasks` | Task list and details; opens a related session | [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) |
| `sessions` | Catalog, history and session view; opens a task or agent | [SessionsCatalog](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/sessions/SessionsCatalog.tsx) |
| `agents`, `skills` | Team catalogs, asset details and related tasks/sessions | [TeamManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/team/TeamManager.tsx) |
| `projectMap` | Current graph, node selection, static relationships and source excerpt when available | [GraphExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphExplorer.tsx) |
| `files` | Independent metadata tree/directory, lazy folder navigation, plain-text reader and file/line reference | `apps/web/src/features/files/ProjectFiles.tsx`; current FUNC-G03 checkout |
| `documents`, `checks`, `search` | Three artifact catalog modes; opens task, session or graph node | [ArtifactExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/artifacts/ArtifactExplorer.tsx) |
| `autonomy`, `decisions` | Autonomy policy and decision queue | [AutonomyManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/autonomy/AutonomyManager.tsx), [DecisionBoard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/decisions/DecisionBoard.tsx) |
| `import`, `backup` | Task import and backup management | [Operations](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Operations.tsx) |
| `settings` | UI preferences, connection, project onboarding and workflow surfaces | App, [ProjectOnboarding](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/projects/ProjectOnboarding.tsx), [WorkflowManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/workflows/WorkflowManager.tsx) |

Internal transitions pass project/task/session/asset/node IDs in App state. The supported message hash anchor contains `project`, `session`, `message`; the project must exist in the list and identifiers have length and character restrictions. This does not promise deep links for every screen. Detail panels, forms and modals belong to their components; closing or losing focus is not confirmation of an operation.

Task details in [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) can expand into an overlay and collapse: [DetailSurface](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Modal.tsx) moves the same DOM to the modal top layer, preserving input. Task deletion and target-transition choice use separate dialogs; deletion requires an explicit checkbox and does not cascade to related records. Escape and close dismiss/collapse the applicable surface without confirming an action.

## Project onboarding and current map boundaries

In Settings the user selects a folder using the native picker or enters a root, supplies a name and confirms addition. Before confirmation the choice is a draft. UI sends `scan:true` and receives a registered project plus a durable `queued` scan. Files opens immediately; stage progress/partial counts are loaded separately from persisted scan status. Picker cancellation, errors and retry have distinct states. Source inspection is bounded; it is not a complete directory browser.

The current `projectMap` is an existing bounded graph, not a promise of complete dependency coverage. F26 implements an independent Files path over shared F28 inventory; managed scanning belongs to F27/F29 and new Map/Database/code-to-table views to F14/F33/F34. Current source-owned statuses are in the [functional matrix](../planning/functional-remediation-2026-11-15.md). A task files tab or source display alone does not establish a complete tree. `partial` or `stale` does not establish that a file or dependency is absent.

## FUNC-26 — Files navigation and reader

`ProjectFiles` consumes `M1Api.projectFiles` and `projectFile`; backend `createProjectFiles(store)` derives root and policy from the registry rather than client input. The directory is available without a ready graph/scan. Opening a folder fetches only its direct children; breadcrumbs and Back to directory retain the path. Empty folders, unsupported extensions, binary and excluded files remain metadata with reasons. The Control-plane filter selects actual paths; search explicitly covers the current directory. Pagination exposes selection boundaries; the500-entry client display cap never declares remaining entries absent.

Text is requested separately by path/metadata revision. `available` contains safe text; `stale`, `unavailable`, `binary`, `too_large`, `unsupported` and `forbidden` return explanations without source bodies while preserving the directory. HTML/scripts render only as React text in `pre/code`. The reader bounds DOM to an80-line window, accepts file/line anchors and offers line navigation. Clipboard failure leaves a selectable manual-copy field. Copying a path grants no read authority; Use in task is enabled only after a successful read and with a supplied callback.

References explicitly separate legacy task `revision`/`revisionKind=sha256` from metadata/policy `fileRevision`, plus rootIdentity, policyVersion and line. A metadata revision must not be stored as the content hash in legacy `fileContexts.revision`. Viewing/reference does not authorize dispatch: F10 rechecks actual execution scope/limits. Hash navigation uses `project`, `file`, `line`; joint App/router wiring and browser acceptance are root FUNC-G03 responsibilities.

A project change creates a new component scope and aborts old list/read requests. Existing `createLatestRequest` rejects superseded responses, and payloads are also checked against project/path. Requests stop on unmount; this component does not poll. Metadata exposes observedAt/revision/policy: explicit refresh/rescan rather than a live-watcher promise. Change observation/common freshness belong to F18. Files does not modify a dirty task editor.

Focused command: `node --test tests/web/project-files.test.mts tests/web/project-files-ui-model.test.mts` — **9/9,0skip** in the current run. Cases cover registered roots without graph state, lazy directory, rawSHA/reference separation, inert HTML, typed stale/missing/binary/size/encoding/forbidden, display redaction/private-key denial, paging/filter/project isolation, actual link/junction/root replacement, in-flight policy revocation and bounded line anchors. Service metadata RED/GREEN was observed. This is service/model evidence; RU/EN×themes, keyboard/focus, layout and the real App journey require root-owned browser acceptance before F26 closure. Context7 [React effects cleanup](https://react.dev/learn/synchronizing-with-effects) was checked against request-scope guards; backend policy/read behavior is in [inventory](../code-intelligence/inventory.md).

## Checks and limits

Related test routes: [ui-v3-dashboard.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-dashboard.test.mts), [ui-v3-diagram.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-diagram.test.mts), [ui-task.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-task.test.mts), [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/sessions-team.test.mts). Links to tests do not claim a new run or human acceptance. Component and API states can change; update this map and its RU/EN pair with the code.

## FUNC-G03 — current integration evidence

Production App/API integration is now verified: persisted asynchronous Add → Files before graph readiness → scan status → inert source preview and line deep link → structured document backlink → task. Browser foundation15/15, RU/EN × light/dark at1440/390px, Back focus, clipboard fallback, cross-project delayed response rejection, no external requests/page errors, unchanged target hashes. Clipboard and delayed delivery are explicitly synthetic boundaries. Source/build hashes and screenshots: `.tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json`. Service/API integration13/13 (`.tmp/func-g03/f26-f27-api-integration.log`), backend typecheck and production frontend build passed. F18 common freshness and final group/native qualification follow; human acceptance remains separate.

## FUNC-G03 — final verification

Current integrated source, not the initial lower-module handoff: browser19/19; full Web594/594,0skip; backend TypeScript and production build passed. Source/build hashes and screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Review policy-race findings are fixed and independently rechecked5/5. Native candidate and production-default receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`. Earlier pending/wiring statements describe their dated intermediate slice; final task reports own closure. Checkout core is available; packaged core remains explicitly unavailable. Human/provider acceptance and F14/F33/F34 are separate.

## FUNC-G04 — Files, Map and Database

Project navigation includes Database with Schema, Changes and Code usages. Settings → Database explicitly selects an offline SQLite metadata candidate; discovery does not open it. Schema has a searchable accessible list/ERD, PK/FK/index/view details, source/revision/coverage/time and bounded pagination. ERD and list share one page and entity selection opens the same details. Binary DB sources have no invented source line. Missing baseline and retained stale metadata remain explicit.

Map provides dependency/symbol modes, incoming/outgoing, bounded paths, graph/Mermaid/list and source evidence navigation to Files. The Files reader links to Map and expandable related tables. Database Code usages and Map DB links navigate to a source line or table. Extra query panels mount only when opened, not in every project background. Project+file+line and project+database+dbtab links support reload/back; foreign late responses are discarded. RU/EN, both themes and narrow layouts reuse V3 components; technical checks remain separate from human acceptance.
