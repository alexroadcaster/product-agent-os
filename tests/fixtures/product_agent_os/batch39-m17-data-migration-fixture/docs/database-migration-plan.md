# Database Migration Plan

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Scope

- Schema source: `schema/orders.sql`.
- Migration tool: generic SQL fixture, no live runner.
- Schema-diff tooling: deferred because this is a static contract test.

## Change Classification

- Expand-contract: add `invoices` table after `orders`.
- Transaction boundary: single logical migration unit.
- Destructive change: none in executable fixture.
- Backfill: not executed.
- Production data impact: `not_applicable_synthetic_fixture`.

## Plan

| Step | Direction | Preconditions | Schema History | Versioned | Rollback or Compensation | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| `001` | forward | source-policy clean | `001_init_orders.sql` | yes | remove synthetic fixture tables in disposable DB only | fixture owner |

## Approval Boundary

- Do not run migration without approval.
- Do not access production data without approval.
- Backup/restore evidence is required before safety claims.

