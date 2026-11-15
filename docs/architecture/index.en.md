# Implementation architecture

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: Product-Agent OS architecture; scope/version: DG02 v1. Update when the cited sources, data boundaries or decisions change; related tests are listed below. Source inspection does not prove runtime activation or release readiness.

This map locates source and boundary ownership for Web/desktop and the separate Python plugin.

- [System context](system-context.md) — actors and external boundaries.
- [Components and processes](containers.md) — source and related tests.
- [Flows and data authority](data-flow.md) — ownership and transitions.
- [Decisions and history](decisions/index.md) — choices, alternatives and limits.
- [Diagram atlas](../diagrams/index.md) and [application diagram](../diagrams/paos-application-architecture.md).

**Related tests:** [route-selector test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project-source test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts). These references do not assert that the tests ran in this session.

## Backend, API and data

[Local service](../backend/index.md), [HTTP contracts](../api/index.md), [SQLite schema and lifecycle](../db/index.md), [editable PAOS SQLite ERD](../diagrams/paos-sqlite-erd.md). These guides describe current source contracts; target database maps remain planned under FUNC-33.
