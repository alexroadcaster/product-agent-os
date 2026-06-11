# Backend Observability Map

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

Synthetic observability expectations:

- Trace identifier at request boundary.
- Counter for task reads.
- Error count by response family.
- Redacted structured log fields for route and status only.

Unsupported claims:

- The fixture does not emit traces, metrics, alerts or logs.
- The fixture does not prove incident diagnosis or operational maturity.

