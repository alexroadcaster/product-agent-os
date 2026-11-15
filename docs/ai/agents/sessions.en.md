# Sessions, messages and recovery

Source status: repository_source / static_source_review; 2026-11-15.

Owner: runtime/agent owner + docs-maintainer. Scope: PAOS implementation at `61f6cd4cd048be478e88e2406c733f98b60bc434`. Update when the selector, gateway, contracts, execution boundaries or related tests change. Linked tests are verification routes, not new runs; activation and human acceptance need separate evidence.

## Object relationships

In the Web local service a session belongs to a project. The [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) binding associates projectId, sessionId, mode and canonical workspace identity; the selected binding is saved separately. A run and messages belong to that binding and are neither the Codex App chat itself nor proof of its complete history. [sessions/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/sessions/service.mts) builds catalog/transcript/search from local store, hides some messages and applies safe persisted text.

## Reads and state

Session history uses scoped snapshot pagination: limit 1–100, snapshot lifetime 15 minutes and scope-bound cursor; expiration returns stale. Coverage is partial with host_history_not_exposed. Web history is an available local projection, not a complete archive of App host actions. [API events](../../api/events.md) describes different cursors that must not be interchanged. [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/sessions-team.test.mts) is a related test route, not a new run.

The [draft-registry.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/web/src/api/draft-registry.ts) manages a project/session message draft and separates send from acknowledgement. An uncertain ACK is not a successful answer or safe draft cleanup; [frontend state](../../frontend/state-management.md) owns details. Public runtime snapshot and private claim/report use different authority boundaries.

## After stop and restart

On recovery [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) moves unfinished App jobs to recovery_required; pending approvals are cancelled and unknown dispatch remains uncertain. For recipes [execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/execution-recipes/service.mts) and [backend recovery](../../backend/recovery.md) own checkpoint/reconcile. A new session or visible window does not prove attach, model activity, settlement of an external operation or owner acceptance. [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/recipe-recovery.test.mts) and [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) are related tests. Runtime was not started for this documentation task.
