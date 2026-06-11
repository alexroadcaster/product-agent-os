# Database Production Access Approval

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

## Request

- Production access: `not_requested`.
- Production DB introspection: `not_requested`.
- Migration execution: `not_requested`.
- Least privilege: required before any future request.

## Boundary

Approval is required before production DB access, production data access, migration execution, backup restore, dumps, schema introspection or external database writes.

