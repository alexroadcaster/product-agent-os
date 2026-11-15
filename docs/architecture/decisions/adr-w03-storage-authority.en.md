# ADR-W03 — storage and authority

Source status: repository_source / static_architecture_map; 2026-11-15.

Owner: Product-Agent OS architecture; scope/version: DG02 v1. Update when the cited sources, data boundaries or decisions change; related tests are listed below. Source inspection does not prove runtime activation or release readiness.

## Status and provenance

The historical engine and authority direction was accepted in [architecture §20](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md); the [storage research](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-storage-research-2026-11-09.md) retains alternatives. This ADR is an extraction, not a new owner decision. SQLite + FTS5 local exists in source; PostgreSQL + pgvector belongs to the future team direction, not a confirmed live integration.

## Context and rationale

Durable local operational entities, search and a recoverable path from legacy state are required. Following verified cutover SQL may own the relevant entities while code and documents remain files. Before confirmed cutover a legacy source may remain authoritative. The two sides must not be treated as independently writable masters.

## Alternatives

File-only storage simplifies repository interaction but leaves operational consistency and indexing to solve. Team PostgreSQL was selected for a future separate mode but needs deployment design, tenancy and migration evidence. This comparison records an existing direction; it does not prove team readiness or select a hosting provider.

## Consequences and review

[Local store](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) and [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts) are current source anchors. Verify authority of the specific project, migration/restore and its receipts; an SQL transaction does not make filesystem operations atomic. [Project-source tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts) and current storage checks complement but do not replace evidence of an actual cutover. Revisit on storage/authority changes or approval of team design.
