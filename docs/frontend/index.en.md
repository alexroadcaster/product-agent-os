# Product-Agent OS frontend and UI/UX

Source status: repository_source / current_source_inspection / documentation_implementation; DG04, 2026-11-15.

Owner: frontend owner + docs-maintainer. Scope: current Web frontend at `ad78d5d15aced23febae90d319f2aba00bd64d0b`; update when a screen, API state, component, design contract or accessibility behavior changes.

## Find the change owner

| Question | Canonical page |
| --- | --- |
| Where is a screen and how is it reached? | [Navigation and states](navigation.md) |
| Who owns data, drafts and late-response guards? | [State management](state-management.md) |
| Which component owns an action or presentation? | [Component map](components.md) |
| How are themes, typography, motion and localization used? | [Design system](design-system.md) |
| What works with a keyboard and what evidence exists? | [Accessibility and verification limits](accessibility.md) |

## Execution boundary

[main.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/main.tsx) mounts React `App` and imports theme/app/workspace/parity CSS. [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx) composes the shell, selected project/section state and feature components. [package.json](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/package.json) declares React, TypeScript, Vite, D3, Mermaid and GSAP; local build runs `tsc --noEmit && vite build`. A dependency does not establish use on every screen.

[HTTP client](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/client.ts) connects UI to the local service. [API](../api/index.md) owns HTTP/auth/error contracts, [backend](../backend/index.md) owns lifecycle and execution, and [DB](../db/index.md) owns durable storage. A UI projection does not replace server authority, runtime ACK or owner decisions. The [product model](../product/domain-model.md) explains entities and responsibilities.

## Design and capability boundaries

[DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/DESIGN.md) and [V3 design assets](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/README.md) remain design owners; this section maps them to code without a second token or screenshot catalog. Historical [V3 receipts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/implementation-evidence.md) belong to their original run and are not current UI acceptance.

The current project Map, bounded Sources and project registration settings do not establish a full file tree, managed background scan, external database map or code-table usages. Future Files/Map/Database/usages belong to F26–F34 in the [functional plan](../planning/functional-remediation-2026-11-15.md); this scope does not implement them.

## Verification and maintenance

Dashboard, TeamManager, and AgentDashboard access Tasks through `features/tasks/read.ts`. The [ADR](../architecture/decisions/adr-dashboard-task-boundary.en.md) covers the boundary and rollback. [Criteria and verification routes](../testing/test-map.en.md#dashboard-a1-criteria) · [METH-11 acceptance](../planning/methodology-improvement-2026-11-15.en.md#a4-results)

The shared `ui/MarkdownBody.tsx` entry renders Tasks comments, Artifacts documents, and Sessions messages with a bounded parser and a common HTTP(S) link policy. Graph, Database and Workflows use `ui/MermaidView.tsx`. Graph and Database also use `ui/NetworkView.tsx`. Each feature owns its data preparation. [METH-10 contract and verification](../planning/methodology-improvement-2026-11-15.en.md#meth-10-results)

`features/usage/RunUsage.tsx` presents project, task, session and agent measurements. Tasks owns navigation and focus restoration. [Usage boundary and verification](../planning/methodology-improvement-2026-11-15.en.md#meth-13-results)

`features/team/AgentDashboard.tsx` owns the team and individual agent views. Shared metric tiles and scales are in `ui/MetricViews.tsx`. [Team boundary and verification](../planning/methodology-improvement-2026-11-15.en.md#meth-14-results)

Find relevant source and tests through the pages above when changing behavior. [UI policy tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-policy.test.mts), [draft tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-registry.test.mts), [theme/locale tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/theme-locale.test.mts) and [browser accessibility checks](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/accessibility/browser-acceptance.mts) are verification routes, not claims of a new run.

DG04 checks source claims, RU/EN, links and documentation build. It does not establish live runtime/provider behavior, current manual screen-reader/WCAG assessment or human product acceptance. Status and evidence: [DOCS-06 / DG04](../planning/documentation-architecture-2026-11-15.md). A contract change updates both languages, the [section map](../product/index.md), navigation and [registry](../sources/registry.md).
