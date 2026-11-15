# Backend: local service

Source status: repository_source / static_source_review; 2026-11-15.

Owner: backend/local-service with storage and runtime owners. Scope/version: DG03, snapshot `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when the entrypoint, route, queue, write or recovery changes; source and test links below refer to this snapshot.

## Scope and reading route

The local service is the PAOS Web/desktop Node process: it connects loopback HTTP, task services, the storage Worker, scheduler, recipes and the selected runtime. [main.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts) constructs these dependencies; [application.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) routes requests. SQLite runs in a separate Worker thread, not a separate network server. The [Python plugin](../product-agent-os/index.md) is a separate package, not a mandatory part of every Web request. [Application context](../architecture/system-context.md) owns system boundaries.

- [Modules and ownership](modules.md): handler, domain service, Worker and runtime boundaries, including existing UI/backend coupling.
- [Lifecycle](lifecycle.md): startup, session gate, draining and shutdown.
- [Commands and events](commands-events.md): revision, idempotency, event/outbox and write order.
- [Recovery](recovery.md): cancellation, unknown outcome, restart and safe continuation.

## Related contracts

[HTTP API](../api/index.md), [SQLite and data](../db/index.md), [product journeys](../product/user-journeys.md) and the [F08 plan](../planning/functional-remediation-2026-11-15.md) describe their owning concerns. Requirements and current improvement status remain in their task cards; this documentation does not imply completion.

## Checks and limits

Related contract tests: [runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts), [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts), [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-recovery.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts). Links identify relevant tests, not new runs. Source inspection does not prove an active App consumer, provider access, behavior of a particular profile, human acceptance or release readiness.
