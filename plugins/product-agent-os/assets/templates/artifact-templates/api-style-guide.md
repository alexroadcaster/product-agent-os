# API Style Guide Decision

Source status: `template`

Project: {project_name}

## Style Choice

- No universal default:
- REST/OpenAPI applicability:
- GraphQL applicability:
- gRPC/protobuf applicability:
- Event-driven applicability:
- Consumer and operational rationale:

## Professional Coding Decisions

- Framework-native option:
- Existing project helper or adapter:
- Existing generated client or SDK:
- Custom protocol/client/serializer requested:
- Rejected native/current-tooling alternatives:
- Idempotency rule:
- Error model:
- Retry behavior:
- Timeout behavior:
- Compatibility evidence:
- Dependency decision:

## Tooling Deferrals

- Spectral status:
- Redocly status:
- Framework-native status:
- Spectral/Redocly/framework-native deferred:
- API lint tooling deferred with owner/reason:
- JSON Schema compatibility rule deferred with owner/reason:
- Protobuf compatibility rule deferred with owner/reason:
- GraphQL compatibility rule deferred with owner/reason:
- AsyncAPI compatibility rule deferred with owner/reason:
- API security profile deferred with owner/reason:
- Contract test generator deferred with owner/reason:

## False Positive Policy

- API-only contract fixtures do not force backend blockers.
- Custom API helper, protocol, serializer, or dependency choice needs source-backed rationale and rejected native/current-tooling alternatives.

## Verification

- Style rule owner:
- Lint/check command or missing-tool gap:
- Contract/idempotency/error/retry/timeout evidence:
- Accepted gap owner/reason/review date/downstream risk/follow-up:
