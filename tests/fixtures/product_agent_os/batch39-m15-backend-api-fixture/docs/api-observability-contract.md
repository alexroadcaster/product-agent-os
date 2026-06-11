# API Observability Contract

Source status: `synthetic_fixture`

Sources: docs/sources/registry.md

API observability expectations:

- Request ID and correlation ID at the API boundary.
- Latency metrics and error counters by endpoint.
- Rate-limit metrics and alert routing before production exposure.

Unsupported claims:

- No telemetry, alert, dashboard or on-call evidence exists.

