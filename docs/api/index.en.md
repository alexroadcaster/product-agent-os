# HTTP API and contracts

Source status: repository_source / static_contract_inventory; 2026-11-15.

Owner: local-service/API maintainers; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when handlers, middleware, client, contracts, events or related tests change. This is the local API for this source revision, not a hosted public API or a claim of runtime availability.

1. [Endpoint inventory](endpoints.md): methods, paths, request/response, side effects, limitations and service-contract links.
2. [Access and errors](errors.md): loopback, session, CSRF, body limits and failure handling.
3. [Events and history](events.md): JSON replay, audit, cursor and runtime-event boundary.
4. [Backend and lifecycle](../backend/index.md), [feature plan](../planning/functional-remediation-2026-11-15.md), [source registry](../sources/registry.md).

Sources: [HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [session gate](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts), [Web client](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts), [service API test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts). Related tests identify contract evidence; they are not claimed as newly run here. OpenAPI is unavailable until a supported generator is selected; do not run scripts from a target project to generate a schema.

Examples are synthetic. `BASE` below denotes a local test instance, not permission to access a user profile.

```http
GET /api/v1/projects/{projectId}/entities?kind=task&limit=20&offset=0 HTTP/1.1
Host: 127.0.0.1:{port}
Cookie: <synthetic-session-cookie>
```

Result: JSON `{ "items": [], "hasMore": false }` for an empty fixture illustrates shape, not a receipt. A previously issued session is required. Do not persist cookies, CSRF, bearer tokens or private project content in examples.
