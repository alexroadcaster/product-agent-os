# Database Data Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Contract

- `orders.id` is stable and unique.
- `orders.customer_ref` contains only synthetic redacted references.
- `orders.status` is one of `created`, `paid`, `cancelled`.
- `invoices.order_id` must reference `orders.id`.

## Unsupported Claims

- Static schema presence does not prove runtime database safety.
- Static constraints do not prove production integrity.
- No migration has been executed.

