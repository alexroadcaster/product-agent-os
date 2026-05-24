# Integration Catalog

## Integration Entry

- External system:
- System owner:
- Business purpose:
- Environment:
- Auth:
- Secret handling:
- Data exchanged:
- PII or sensitive fields:
- Rate limits:
- Retry policy:
- Idempotency key:
- Timeout:
- Error handling:

## Contract Surface

- HTTP contract:
- OpenAPI location:
- Webhook:
- Event contract:
- AsyncAPI location:
- Producer:
- Consumer:
- Ordering:
- Compatibility notes:

## Operations

- Observability:
- Logs:
- Metrics:
- Alerts:
- Runbook:
- Rollback:
- Approval needs:
- Test or eval command:
- Residual risks:

## Stop Notes

- Do not call external systems without explicit approval.
- Do not store secrets or customer data in this catalog.
- Do not parallelize integration work when ownership or idempotency is unclear.
