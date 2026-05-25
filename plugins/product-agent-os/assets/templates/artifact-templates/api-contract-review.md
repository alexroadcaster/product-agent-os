# API Contract Review Template

Source status: `template`

Project: {project_name}

## Scope

- HTTP API covered by OpenAPI:
- Message-driven API covered by AsyncAPI:
- Pact or provider contract:
- External provider contract:
- Provider contract:
- protobuf / gRPC contract:
- JSON Schema dialect:
- GraphQL specification target:
- Generated clients or SDKs:
- Consumers:
- Lifecycle state: `draft | experimental | stable | deprecated | removed`
- Contract drift between source, code and generated docs:
- Linked backend-service-overview.md:

## Standards Trigger Policy

- Gate: `standards_trigger_policy`.
- OpenAPI source of truth: HTTP API contracts should point to the checked-in OpenAPI document or record an explicit gap.
- Swagger UI: optional renderer/editor/tooling around OpenAPI, not the source of truth.
- Swagger UI is not source of truth; rendered docs are outputs.
- AsyncAPI source of truth: event, queue, webhook, or message-driven contracts should point to AsyncAPI or an accepted alternative/gap.
- Provider contracts: Pact, protobuf, checked-in provider schemas or an accepted gap are required where external providers apply.

## Contract Checks

- OpenAPI version and lint command:
- AsyncAPI version and lint command:
- Backward compatibility:
- JSON Schema dialect and compatibility rule:
- GraphQL complexity, authorization and deprecation:
- gRPC/protobuf compatibility:
- Request and response schemas:
- Examples:
- Contract drift check:

## AsyncAPI Event Contract

- Channel:
- Message:
- Payload schema:
- Producer:
- Consumer:
- Ordering:
- Idempotency:
- Headers:
- Signature verification:
- Correlation ID:
- Idempotency key:
- Replay:
- CloudEvents applicability:
- Compatibility check:
- Retry or dead-letter behavior:

## Security

- Auth scheme:
- OpenAPI security schemes:
- GraphQL auth:
- Authorization model:
- Scopes:
- Token claims:
- Object-level authorization:
- Sensitive fields:
- Rate limits and abuse controls:
- OWASP API risks:
- OAuth / RFC 9700 baseline:
- Prose-only security notes are unsupported:
- Error disclosure:

## Behavior

- Success responses:
- Validation errors:
- Auth errors:
- Domain failure errors:
- RFC 9457 Problem Details:
- Error type/status code/extensions:
- Idempotency:
- Pagination or streaming:
- Retry expectations:

## Observability

- Request ID:
- Correlation ID:
- Error counters:
- Latency:
- Rate-limit metrics:
- Integration failure alerts:

## External Writes

- External write:
- Staged approval artifact:
- Approval status:
- Rollback/disable path:

## Verification

- Contract tests:
- Schema validation:
- Provider verification:
- Consumer-driven tests:
- Integration tests:
- Backend code sync:
- API/event contract sync with code:
- Contract changes synced with code and tests:
- Generated docs build:
- Consumer review:
- Contract check command:
- Missing-tool gap:
- Release/rollback impact:
- Accepted gap owner/reason/review date/downstream risk/follow-up:
