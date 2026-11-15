# ADR — App-agent and API routing

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: Product-Agent OS architecture; scope/version: DG02 v1. Update when the cited sources, data boundaries or decisions change; related tests are listed below. Source inspection does not prove runtime activation or release readiness.

## Status and provenance

[Architecture §21.9](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) records the 2026-11-11 owner decision: default is Codex App agent; API BYOK remains a separate compatibility route. The earlier App Server-only baseline in the history is not the current default. The [selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) defines both routes and no implicit fallback; an input containing an API key selects the API route when no route is specified. A historical receipt does not prove current attachment or readiness.

## Context and rationale

A coherent route through Codex App without requiring an API key and a separate explicitly selected API compatibility path are needed. Switching routes must respect connection state and unresolved runs; waiting for a consumer is not completed execution.

## Alternatives and consequences

The historical standalone App Server-first approach had different closed-App conditions; a separate API client requires explicit selection and its own credential authority. Transparent fallback would conceal a change in runtime and credential boundary; the source selector does not perform it. This rationale is an inference from the recorded boundaries. The App route requires an active consumer; route metadata does not prove entitlement, native sandbox or successful model calls.

**Related tests and updates:** [route test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [gateway test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/app-agent-gateway.test.mts); [gateway source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts). Revisit on selector, authority model or owner decision changes; verify actual activation only with applicable authorization.
