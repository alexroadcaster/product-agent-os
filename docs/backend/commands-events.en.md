# Backend: commands, events and outbox

Source status: repository_source / static_source_review; 2026-11-15.

Owner: backend and storage; scope/version: DG03, `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Update when a command, revision, event, outbox or cursor contract changes.

## From request to durable receipt

[application.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) authorizes a local request and passes normalized input to a domain service. A domain command uses [storage contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/packages/contracts/storage/local-store.ts): `projectId`, `actorId`, `idempotencyKey`, `expectedAuthorityEpoch` and changes with `expectedRevision`. This is the storage contract, not a universal HTTP request body: current request/response shapes are in [API](../api/endpoints.md).

[local-store.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts) correlates each RPC with a Worker response. [sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) writes within `BEGIN IMMEDIATE`: it checks a repeated key and payload hash, project authority epoch and revisions, then applies changes and records the command receipt, project sequence event and any outbox jobs in one transaction. An exception rolls back the transaction. Repeating the same project/key and payload returns the saved receipt; a different payload with the same key yields `IDEMPOTENCY_CONFLICT`. This is command-write idempotency, not proof of exactly-once execution of arbitrary external actions.

## Order and reads

A receipt contains `commandId`, `projectId`, `seq` and revisions. Events are read by project sequence; the client cursor also carries generation, so reset/restore and expired history require explicit handling rather than blindly resuming the old cursor. An outbox job is created as `pending` and may be marked `acknowledged`; persisting an outbox row does not prove delivery or completion of an external operation. Search index jobs run after the command transaction with separate revision checks. See [API events](../api/events.md) and [data transactions](../db/transactions.md).

## Queues and errors

The Worker caps pending requests at 100 and returns `STORAGE_BUSY`; closure yields `STORAGE_CLOSED`. Scheduler and recipe service have separate serial queues, but unrelated requests and runtime gateways are not one global queue. Scheduler checks frozen preview, revision, authority and workspace ownership; reuse of an idempotency key with different input conflicts. Errors such as `REVISION_CONFLICT`, `AUTHORITY_CONFLICT` and `QUEUE_PREVIEW_STALE` require refreshing state rather than automatically retrying a potentially mutating operation. For HTTP mapping see [errors](../api/errors.md).

## Checks and limits

Related tests: [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts), [runtime-events.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-events.test.mts); links do not mean they ran for this change. External outbox consumers, delivery and current runtime outcomes are not established here.
