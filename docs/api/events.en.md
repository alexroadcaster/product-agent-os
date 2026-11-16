# Events, replay and history

Source status: repository_source / static_contract_inventory; 2026-11-15.

Owner: local-service/API and storage; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when events, retention, cursors or runtime adapters change. [API](index.md), [backend flow](../backend/commands-events.md).

## HTTP replay and audit

`GET /api/v1/projects/{projectId}/events?cursor=...` and `/history?cursor=...` return JSON `{generation, items, hasMore, nextCursor}`. [StoreEventPage](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts) defines item `{seq, eventId, actorId, occurredAt, payload}`. A cursor encodes projectId/generation/seq and is HMAC-signed with an instance-random secret; a stale, damaged or other-project cursor must be treated as an error. Recreating the instance does not guarantee cursor preservation.

`events` is retention-bounded replay; `history` is separate immutable task audit whose retention is not bounded by replay retention. This is JSON polling; the handler does not declare a `text/event-stream` or SSE endpoint. Earlier project documents proposing SSE are historical architecture, not proof of a current HTTP route.

`/entities` uses `limit` (1–100, default 50) and `offset`; `/search` uses `offset` and limit 50. Session history uses a separate scoped snapshot cursor lasting 15 minutes; graph cursors bind to revision and filters; do not interchange them. [Session history](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/sessions/service.mts), [graph service](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/code-index/service.mts).

## Runtime events and authority

[RuntimeEvent](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/runtime/events.ts) distinguishes `turn_accepted`, `turn_started`, `turn_ended`, `approval_requested`, `request_resolved`, `item_ended`, `non_lifecycle`, `recovery_required`; its type owns exact fields and outcomes. `turn_accepted` acknowledges dispatch, not successful turn completion. Runtime state returns a snapshot; the separate private `/agent/v1` channel uses lease and capability rather than a browser cookie.

The write transaction connects changes, receipts, events and outbox according to the [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts). Runtime events do not all represent owner acceptance; do not promise delivery/streaming outside the verified contract. [Service API tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts), [runtime events test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-events.test.mts); links do not mean a new test run. Assess examples and results of other runs with their provenance.

## FUNC-18 — stamp instead of full snapshot polling

The project freshness endpoint is not SSE, a filesystem watcher or a new event stream. It compares generation/throughSeq with scan/policy versions; the baseline arrives atomically with task-manager rows. A task or scheduler-entry change through another authorized channel invalidates the old UI snapshot. Unknown freshness is separate from fresh; explicit refresh does not replace a dirty draft. See [frontend state](../frontend/state-management.en.md#func-18--snapshot-freshness-and-editor-preservation).
