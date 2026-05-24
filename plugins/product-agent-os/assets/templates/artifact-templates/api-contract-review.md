# API Contract Review Template

Project: {project_name}

## Scope

- HTTP API covered by OpenAPI:
- Message-driven API covered by AsyncAPI:
- Generated clients or SDKs:
- Consumers:

## Standards Trigger Policy

- Gate: `standards_trigger_policy`.
- OpenAPI source of truth: HTTP API contracts should point to the checked-in OpenAPI document or record an explicit gap.
- Swagger UI: optional renderer/editor/tooling around OpenAPI, not the source of truth.
- AsyncAPI source of truth: event, queue, webhook, or message-driven contracts should point to AsyncAPI or an accepted alternative/gap.

## Contract Checks

- OpenAPI version and lint command:
- AsyncAPI version and lint command:
- Backward compatibility:
- Request and response schemas:
- Examples:

## AsyncAPI Event Contract

- Channel:
- Message:
- Payload schema:
- Producer:
- Consumer:
- Ordering:
- Idempotency:
- Compatibility check:
- Retry or dead-letter behavior:

## Security

- Auth scheme:
- Authorization model:
- Sensitive fields:
- Rate limits and abuse controls:
- Error disclosure:

## Behavior

- Success responses:
- Validation errors:
- Auth errors:
- Idempotency:
- Pagination or streaming:
- Retry expectations:

## Verification

- Contract tests:
- Integration tests:
- Generated docs build:
- Consumer review:
