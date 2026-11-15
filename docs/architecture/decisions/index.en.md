# Architecture decision index

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: Product-Agent OS architecture; scope/version: DG02 v1. Update when the cited sources, data boundaries or decisions change; related tests are listed below. Source inspection does not prove runtime activation or release readiness.

The [historical architecture document](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) remains in place and retains original ADR-W01–W09 and subsequent amendments. Its early diagrams and statuses apply to their dates and may be superseded. The records below extract decisions with established provenance; this index does not claim all historical proposals were accepted.

| Record | Status | Basis and consequences |
| --- | --- | --- |
| [ADR-W03: storage and authority](adr-w03-storage-authority.md) | Historical source records local SQLite and future team PostgreSQL engine choices as accepted; team implementation remains planned | Verify cutover per project; files and SQL are not declared simultaneously writable masters |
| [App-agent and API routing](adr-app-agent-routing.md) | Owner-selected default 2026-11-11; selector implemented in source; runtime verification limited to separate receipts | No implicit fallback; a route does not establish consumer or model availability |
| [ADR-W05: original runtime selection](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) | Historical accepted choice, §13/§19; default-route and closed-App assumptions superseded by the later owner-selected App-agent route | Preserve App Server lineage and the original unverified closed-App gate; [current route decision](adr-app-agent-routing.md) requires App and an attached consumer |
| ADR-W01/W02/W04/W06–W09 | Historical proposals or decisions requiring further reconciliation; see source | Not promoted to accepted without separate evidence |

**Tests:** [route test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project-source test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts). Revisit the index after an accepted decision or implementation change; related requirements and tasks belong to the [plan](../../planning/product-agent-os-web-task-manager-plan-2026-11-09.md).
