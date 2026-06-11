# Database Dictionary

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

| Table | Field | Meaning | Classification | Constraint |
| --- | --- | --- | --- | --- |
| `orders` | `id` | Synthetic order identifier | synthetic | primary key |
| `orders` | `customer_ref` | Redacted customer reference, not PII | synthetic | not null |
| `orders` | `status` | Order lifecycle status | synthetic | enum-like check |
| `orders` | `created_at` | Creation timestamp | synthetic | not null |
| `invoices` | `order_id` | Linked order identifier | synthetic | foreign key |

