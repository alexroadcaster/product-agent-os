# Frontend navigation and screens

Source status: repository_source / static_contract_review; 2026-11-15.

Owner: frontend and docs-maintainer. Scope: Web/desktop UI, source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Update when sections, transitions, onboarding or related UI tests change. [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx) and [Sidebar.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Sidebar.tsx) own current behavior; [API](../api/index.md) owns HTTP contracts.

## Entry and project selection

Initialization obtains a session, projects, preferences and connection status. Without a session the pairing form appears; errors are shown and navigation is disabled until `ready`. After entry the selected existing project is retained or the first project selected. Without a project, project-specific sections show an empty state; Settings and portfolio remain separately available. The header contains breadcrumb, search, connection status and reload.

The sidebar has 15 sections grouped under Work, Knowledge, Management and Workspace. Selecting a project or section changes React state; these are not independent URL routes. The sidebar can collapse; the narrow-layout mechanism closes it after selection and Escape returns focus to the menu button. `aria-current` marks the selected page. This mechanism does not extend the desktop design scope; see [accessibility](accessibility.md) for behavior and limits.

## Current screen map

| Identifier | Screen and transitions | Source entry |
| --- | --- | --- |
| `portfolio` | All projects; a card opens project overview, tasks or agents | [Dashboard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/dashboard/Dashboard.tsx) |
| `overview` | Dashboard, sources and usage tabs; links to tasks and agents | App and Dashboard |
| `tasks` | Task list and details; opens a related session | [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) |
| `sessions` | Catalog, history and session view; opens a task or agent | [SessionsCatalog](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/sessions/SessionsCatalog.tsx) |
| `agents`, `skills` | Team catalogs, asset details and related tasks/sessions | [TeamManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/team/TeamManager.tsx) |
| `projectMap` | Current graph, node selection, static relationships and source excerpt when available | [GraphExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphExplorer.tsx) |
| `documents`, `checks`, `search` | Three artifact catalog modes; opens task, session or graph node | [ArtifactExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/artifacts/ArtifactExplorer.tsx) |
| `autonomy`, `decisions` | Autonomy policy and decision queue | [AutonomyManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/autonomy/AutonomyManager.tsx), [DecisionBoard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/decisions/DecisionBoard.tsx) |
| `import`, `backup` | Task import and backup management | [Operations](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Operations.tsx) |
| `settings` | UI preferences, connection, project onboarding and workflow surfaces | App, [ProjectOnboarding](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/projects/ProjectOnboarding.tsx), [WorkflowManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/workflows/WorkflowManager.tsx) |

Internal transitions pass project/task/session/asset/node IDs in App state. The supported message hash anchor contains `project`, `session`, `message`; the project must exist in the list and identifiers have length and character restrictions. This does not promise deep links for every screen. Detail panels, forms and modals belong to their components; closing or losing focus is not confirmation of an operation.

Task details in [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) can expand into an overlay and collapse: [DetailSurface](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Modal.tsx) moves the same DOM to the modal top layer, preserving input. Task deletion and target-transition choice use separate dialogs; deletion requires an explicit checkbox and does not cascade to related records. Escape and close dismiss/collapse the applicable surface without confirming an action.

## Project onboarding and current map boundaries

In Settings the user selects a folder using the native picker or enters a root, supplies a name and confirms addition. Before confirmation the choice is a draft. UI sends `scan:true` and displays progress plus `ready`/`partial`, counts and source availability when returned. Picker cancellation, errors and retry have distinct states. Source inspection is bounded; it is not a complete directory browser.

The current `projectMap` is an existing bounded graph, not a promise of complete dependency coverage. The complete Files tree, managed scan, new Map/Database views, target DB map and code-to-table usages remain planned in [FUNC-26–34](../planning/functional-remediation-2026-11-15.md). A task files tab or source display does not establish a full project tree. `partial` or `stale` does not establish that a file or dependency is absent.

## Checks and limits

Related test routes: [ui-v3-dashboard.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-dashboard.test.mts), [ui-v3-diagram.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-diagram.test.mts), [ui-task.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-task.test.mts), [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/sessions-team.test.mts). Links to tests do not claim a new run or human acceptance. Component and API states can change; update this map and its RU/EN pair with the code.
