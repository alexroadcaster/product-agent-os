# ADR — Dashboard and Tasks boundary

Source status: repository_source / bounded_internal_architecture_decision; 2026-11-18.

## Decision

Owner: Product-Agent OS frontend. For the [Dashboard pilot](../../planning/methodology-improvement-2026-11-15.en.md#a1-results), enforce boundaries in the existing structure. Dashboard acts as a page, App owns navigation and composition, and Tasks owns status and blocking semantics. The local service retains write authority and snapshot ownership. App's existing entry points are `Dashboard.tsx` and `TaskManager.tsx`.

Dashboard, `TeamManager.tsx`, and `AgentDashboard.tsx` use `features/tasks/read.ts`. The entry explicitly exports `assignedWork`, `semanticStatus`, `isBlocked`, `statusText`, `errorText`, `durationText`, `label`, and the `Locale` type. The single implementations live in Tasks' `model.ts` and `labels.ts`. The boundary separates reads from editing, commands, and screen composition. [A2 verification](../../planning/methodology-improvement-2026-11-15.en.md#a2-results) · [METH-11 verification](../../planning/methodology-improvement-2026-11-15.en.md#a4-results)

Tasks, Artifacts, and Sessions use `ui/MarkdownBody.tsx`. The parser and URL validator live in the same layer. The boundary preserves the supported Markdown subset, HTTP(S) links without embedded credentials, and literal output for unsupported markup. [METH-10 verification](../../planning/methodology-improvement-2026-11-15.en.md#meth-10-results)

Graph, Workflows, and Database pass prepared source to `ui/MermaidView.tsx`. Graph and Database pass nodes and links to `ui/NetworkView.tsx`. Graph's Mermaid mapping stays in `features/graph/diagram-source.ts`. Workflows and Database retain their own mappings.

`features/usage/RunUsage.tsx` owns measurement reads, the UTC period, and coverage presentation. Tasks passes `taskId`, Sessions passes `sessionId`, project overview passes `projectId`, and the agent view passes `agentId` within its project. The panel owns state and reads from `M1Api.teamMetrics`, so it has a dedicated feature entry. App and screens retain navigation. The service retains the contract and storage. [METH-13 verification](../../planning/methodology-improvement-2026-11-15.en.md#meth-13-results)

Team owns `features/team/AgentDashboard.tsx` and agent selection. Dashboard and Team consume the Tasks projection `assignedWork`, the Usage period and summary, and the shared `Metric` and `Bars` from `ui/MetricViews.tsx`. The existing `RunMetrics` contract supplies the measurement type for both screens. [METH-14 verification](../../planning/methodology-improvement-2026-11-15.en.md#meth-14-results)

## Alternatives

Keeping only the current folders and tests costs less but leaves new imports of sibling internals undetected. A pages-first FSD migration would provide physical separation, but one testable boundary does not justify moving full screens and updating all consumers. Checking the boundary in place gives a reversible pilot. Decisions about `pages`, `widgets`, `entities` and `shared` depend on A2 results and demonstrated need.

## Enforced rules

- Modules may import other modules in the same area. App uses the existing screen entry points. Other consumers use explicitly approved public entry points.
- Dashboard and Tasks may use their API client, localization, shared contracts, and allowlisted UI primitives. The rule permits `tasks/read.ts` for Dashboard and two explicit Team consumers, `TeamManager.tsx` and `AgentDashboard.tsx`. The boundary check covers other consumers, direct imports of Tasks internals, and imports of App or peer screens.
- A cycle involving Dashboard or Tasks fails the check, including a path through intermediate frontend modules. The existing contracts → apps and local service → frontend prohibitions still apply.
- The test rejects direct imports of feature modules or App by shared Markdown, its parser, its URL validator, or the Mermaid and D3 views. Tasks may import the named `MarkdownBody` and `safeExternalUrl` entries.
- The test allows `RunUsage.tsx` for Tasks and Dashboard, and also allows `UsageSummary.tsx` and `observed-period.ts` for Dashboard. These Usage entries and `MetricViews.tsx` may not import App or feature modules.
- The original exceptions were pinned at revision `bd7d9135f994201170277171eb54e4040cef4fa8`. A2 removed three Dashboard → Tasks edges, METH-11 two TeamManager → Tasks edges, METH-10 two Artifacts/Sessions → Tasks edges, METH-13 two Tasks/Sessions → Dashboard edges, and METH-14 one Team → Dashboard edge. The nine remaining exceptions in `tests/web/fixtures/dashboard-import-baseline.json` are on the existing METH-11 hold. The test requires removing entries when their edges are removed.
- `node --test tests/web/contracts-boundaries.test.mts` parses TS, TSX and MTS. Literal imports resolve against source files and supported `baseUrl`/`paths` in the Web tsconfig. Unknown aliases and computed targets have distinct diagnostics. The rule covers the specified frontend boundary. Shared contracts and the backend have their own rules.

## Rollback and stopping criterion

To roll back METH-14, restore `AgentDashboard`, metric rendering, and the assignment projection in Dashboard. Restore the Team import, the former Tasks entry, the exception, and the boundary rule. Rerun Dashboard, team summary, and selected agent scenarios.

To roll back METH-13, restore the panel and the former `UsageDashboard` entry in Dashboard, the original imports, the Tasks focus handlers, and the former error formatting. Restore both exceptions and the former boundary rule. Rerun Tasks, Sessions, and project overview scenarios.

To roll back METH-10, restore the Markdown renderer, parser and URL validator in Tasks, the three consumers' imports, and the two exceptions. Restore Mermaid and D3 in `GraphViews.tsx`, the original imports, and Graph's node inputs. Restore the former test rule and rerun the build and focused browser scenarios.

To roll back METH-11, restore the two direct Team imports, the four original runtime exports of `tasks/read.ts`, the former Dashboard-only check rule, and both Team exceptions. A separate A2 rollback must account for Team's dependency on the shared entry. After rolling back METH-11, restore the three Dashboard imports, remove `tasks/read.ts`, and restore the corresponding exceptions and A1 rule. Synchronize the affected statuses, tests and report, then rerun the boundary check, build and browser scenario. There is no data migration.

## Expansion decision {#a2-rollout}

`METH-18` confirms the Dashboard pilot. The comparison shows two Tasks internal paths reduced to one public entry, three direct violations removed, and all 50 common browser checks preserved. Expansion considers the same kind of coupling in a specific consumer.

| Task | Decision and rationale |
| --- | --- |
| METH-10 | `bounded_go` for Markdown, Mermaid, and D3. Frontend shared UI owns the change. Tasks, Artifacts, and Sessions use Markdown. Graph, Workflows, and Database use Mermaid. Graph and Database use the D3 network view. Remove two imports of Tasks internals and three Graph view imports from Workflows/Database, preserve rendering, and separate presentation from data preparation. |
| METH-11 | `bounded_go` for one consumer, `TeamManager.tsx`. Owners are Tasks and Team frontend. The Tasks entry can explicitly expose the already used `durationText`, `label`, `errorText`, and `Locale` type. Measurable outcome: remove two Team → Tasks deep imports, introduce zero violations, and pass relevant Team and Dashboard scenarios. Rollback restores the two imports, Team exceptions, and former export list. |
| METH-13 | `bounded_go` for Tasks. Frontend Usage owns the measurements panel. Tasks owns opening analytics from a task and returning to it. The baseline confirmed task filtering and preservation of the selected task, tab, and drafts, and exposed lost focus in both transitions. Restore focus and remove two Tasks/Sessions imports of Dashboard. Workflows stays on `hold` until its own change is selected with draft, CAS, focus, and queue checks. |
| METH-14 | `bounded_go` for Team. Team owns its sole-consumer `AgentDashboard`. Tasks owns the open-assignment projection, Usage owns coverage presentation and the observation period, and `ui` owns the metric tile and scale. Baseline browser evidence covers team totals, agent detail and the `agentId` filter. Remove Team → Dashboard while preserving those checks. Skills stays on `hold` until its entry presents a demonstrated problem. |
| METH-15 | `hold`. METH-13 moves Sessions to the shared Usage entry and preserves `sessionId`. Further migration of Sessions, Artifacts, Graph, or App requires a separate scenario with a measurable benefit and checks for route and state ownership. |

The selected METH-10, METH-11, METH-13 and METH-14 scopes are implemented. Product direction B has its own plan. [A4 results](../../planning/methodology-improvement-2026-11-15.en.md#a4-results)

Reviewed import and public API rules with Context7. [FSD layers](https://feature-sliced.design/docs/reference/layers) · [FSD public API](https://feature-sliced.design/docs/reference/public-api)

Mermaid retains its local asset, lazy loading, strict mode, and theme. Configuration was checked through Context7. [Mermaid securityLevel](https://mermaid.js.org/config/schema-docs/config-properties-securitylevel.html)
