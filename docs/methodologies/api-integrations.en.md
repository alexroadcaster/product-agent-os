# API & Integrations

Source status: `official + verified methodology + tool-assisted`

Research date: `2026-05-24`

Product-Agent OS behavior: detect API and integration work early, require a contract source of truth, route risky changes through consumer, security, compatibility and release gates, and produce reviewable artifacts before code changes reach public or semi-public contracts.

## Scope

This dossier covers HTTP APIs, message/event APIs, webhooks, GraphQL, gRPC, generated SDKs, external integrations, API security, error contracts, versioning, compatibility, documentation artifacts and Product-Agent OS candidates.

It does not choose a universal API style for every project. The project should select an API style based on consumers, latency, ownership, ecosystem, tooling and operational risk.

## Supported facts

- OpenAPI Specification v3.2.0 is the current OpenAPI contract source checked for this research run. It describes HTTP APIs in a programming-language-agnostic format and includes operations, parameters, request bodies, responses, examples, security schemes and reusable components.
- AsyncAPI Specification v3.1.0 is the current AsyncAPI contract source checked for this research run. It describes message-driven APIs in a machine-readable, protocol-agnostic format.
- RFC 9110 defines HTTP semantics. HTTP API design should not invent local meanings for methods, status codes and content negotiation when standard semantics already exist.
- RFC 9457 defines Problem Details for HTTP APIs and obsoletes RFC 7807. It should be considered the default candidate for machine-readable HTTP error payloads unless the project already has a stronger compatibility reason.
- RFC 9700 is the OAuth 2.0 Security Best Current Practice as of January 2025. OAuth-based APIs should treat it as a security baseline source, not as optional prose.
- OWASP API Security Top 10 2023 is the current OWASP API-specific risk catalog checked in this research run. It is useful for API threat modeling and security review gates.
- JSON Schema current version is 2020-12 according to the official JSON Schema specification page. Projects using JSON payload schemas should state the dialect.
- CloudEvents v1.0.2 and the CNCF CloudEvents project provide a standardized event metadata envelope option. It is useful when event interoperability across systems matters.
- GraphQL has a latest release dated September 2025 and a working draft dated April 2026. A project should pin the GraphQL specification target it follows instead of saying only "GraphQL".
- gRPC uses Protocol Buffers as the default Interface Definition Language and message interchange format; `.proto` files become the source contract for service methods and messages.
- Pact documents consumer-driven contract testing as a contract-by-example approach. It complements schema contracts because it captures actual consumer expectations, not every theoretically possible schema state.
- OpenAPI Generator can generate clients, server stubs and documentation from OpenAPI documents. Generated SDKs need a manifest, ownership, versioning and regeneration policy.
- Stoplight Spectral is documented as a JSON/YAML linter with ready-to-use style guides for OpenAPI and AsyncAPI. It is a candidate for API lint gates when the project chooses that toolchain.
- Google API Improvement Proposals are a vendor-specific but mature model for recording API design rules. The useful transferable idea is the local API style guide as a governed artifact.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Contract-first development | New public API, SDK, provider/consumer split | Contract is written or changed before implementation; code and tests conform to it. |
| Contract-aware development | Existing code-first service | Generated or maintained contract is updated in the same slice as behavior changes. |
| Consumer-driven contract testing | Multiple consumers, microservices, frontend/backend split | Consumers express expectations through contract tests; providers verify before release. |
| API lifecycle governance | APIs move from draft to stable to deprecated | Every endpoint/message has lifecycle state, owner, compatibility policy and deprecation path. |
| Backward compatibility by default | Public, partner, mobile, SDK or event contracts | Changes are classified as breaking/non-breaking before implementation. |
| Error-contract governance | HTTP APIs expose machine consumers | Error responses use a documented model, preferably Problem Details when compatible. |
| Event-contract governance | Async messaging, queues, streams, webhooks | Event schema, idempotency, retry, ordering, correlation and dead-letter behavior are documented. |
| Integration security by design | Authenticated API, external provider, sensitive data | Auth scheme, scopes, token claims, rate limits, object-level authorization and abuse cases are reviewed. |
| Generated-client governance | SDKs or typed clients are generated | Generator, config, target languages, compatibility and release process are documented. |
| API style-guide governance | Large project or many teams | Local API rules are versioned and lintable where possible. |
| Two-stage review | Public contract, migration, SDK, auth, event payload | Stage 1 checks contract/security/compatibility; stage 2 checks implementation quality. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| API inventory | List APIs, owners, lifecycle states, consumers and source-of-truth files. | Markdown/YAML table in repo. |
| OpenAPI document | HTTP API source of truth. | OpenAPI v3.2.0 or project-pinned compatible version. |
| AsyncAPI document | Message/event API source of truth. | AsyncAPI v3.1.0 or project-pinned compatible version. |
| GraphQL schema | GraphQL contract source. | `.graphql` schema plus pinned GraphQL spec target. |
| gRPC/protobuf IDL | RPC contract source. | `.proto` files and generator config. |
| JSON Schema library | Shared JSON payload contracts. | JSON Schema 2020-12 unless project pins older dialect. |
| Problem Details catalog | Stable HTTP error types, status codes and extensions. | RFC 9457. |
| Auth and authorization matrix | Schemes, scopes, roles, token claims, object-level rules. | OpenAPI security schemes, OAuth BCP, OWASP API risks. |
| Consumer map | Human/system consumers, SDKs, generated clients, owners and approval path. | `api-consumer-map.md`. |
| Compatibility decision record | Breaking/non-breaking classification and migration impact. | ADR-style record or `api-compatibility-record.md`. |
| Contract test matrix | Provider verification, consumer tests, schema tests and negative cases. | Pact, schema validators, stack-specific API tests. |
| Generated SDK manifest | Generator, version, config, target languages, owner and release process. | OpenAPI Generator or stack-specific generator. |
| Webhook/event delivery contract | Retry, idempotency, ordering, signature verification, replay and dead-letter behavior. | AsyncAPI, CloudEvents where applicable. |
| External integration policy | Read/write capability, sandbox credentials, approval and rollback path. | Project control-plane artifact. |
| API style guide | Naming, pagination, filtering, versioning, status codes, errors and examples. | Local rules inspired by selected API guidelines. |
| Deprecation plan | Timeline, compatibility mode, comms, release notes and removal criteria. | Changelog/release packet. |

## Project application instructions

1. Classify the integration: internal HTTP API, public API, partner API, webhook, async event stream, GraphQL, gRPC, generated SDK, external provider or automation integration.
2. Declare the contract source of truth. If there is no OpenAPI, AsyncAPI, GraphQL schema or `.proto`, record the gap before implementation.
3. Name provider, consumers, owners, generated clients and runtime environments.
4. Classify the change as additive, behavior-compatible, potentially breaking or breaking.
5. Update the contract before or alongside code. Do not let rendered docs or Swagger UI become the source of truth.
6. Add examples for success, validation failure, auth failure and the most important domain failure.
7. Document auth scheme, scopes, object-level authorization rules, rate limits and sensitive fields.
8. Document the error model. For HTTP APIs, prefer RFC 9457 Problem Details when compatible with existing clients.
9. For event/message changes, document schema, headers, correlation ID, idempotency key, retry policy, ordering guarantees and dead-letter behavior.
10. For generated SDKs, update the generation manifest and record whether clients need a major, minor or patch release.
11. Add or update contract tests: schema validation, provider verification and consumer-driven tests where consumer risk is high.
12. For external writes, create a staged draft or approval artifact before the agent touches the external system.
13. Add observability expectations: request IDs, correlation IDs, error counters, latency, rate-limit metrics and integration failure alerts.
14. Record rollout, deprecation and rollback path in the release artifact.

## Product-Agent OS candidate rules

### Discovery signals

- `openapi.yaml`, `openapi.yml`, `openapi.json`, `swagger.yaml`, `swagger.json`
- `asyncapi.yaml`, `asyncapi.yml`, `asyncapi.json`
- `schema.graphql`, `*.graphql`, `*.proto`
- `pact/`, `pacts/`, `contract-tests/`, `consumer-contracts/`
- `api/`, `integrations/`, `webhooks/`, `sdk/`, `clients/`
- terms in requirements: API, endpoint, webhook, SDK, OAuth, scope, token, GraphQL, gRPC, protobuf, Kafka, queue, event, contract, deprecation, migration

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `api_contract_source_present` | Any API or integration change | No named contract source or explicit gap record. |
| `api_consumer_map_present` | Public, partner, SDK, mobile or multi-team API | Consumers, owners or generated clients are unknown. |
| `api_breaking_change_reviewed` | Breaking or potentially breaking contract change | No migration plan, deprecation window or owner approval. |
| `api_security_reviewed` | Auth, scopes, token claims, sensitive data or external provider | No auth matrix, threat notes or security reviewer route. |
| `api_error_contract_present` | HTTP API behavior or validation change | Error response shape and examples are missing. |
| `event_delivery_contract_present` | Event, webhook, queue or stream change | Retry, idempotency, ordering, correlation or dead-letter behavior is missing. |
| `generated_client_manifest_present` | SDK or generated client affected | Generator/config/release impact is not documented. |
| `external_write_approval_present` | External system write or mutation | No staged draft, approval record or rollback path. |

### Candidate templates

- `api-contract-review.md`
- `api-consumer-map.md`
- `api-compatibility-record.md`
- `api-error-catalog.md`
- `api-auth-authorization-matrix.md`
- `api-style-guide.md`
- `api-contract-test-matrix.md`
- `generated-sdk-manifest.md`
- `webhook-event-contract.md`
- `external-integration-approval.md`

### Candidate eval fields

- Contract source is named and linked.
- Consumers and generated clients are named.
- Breaking/non-breaking classification is present.
- Migration/deprecation plan exists for breaking changes.
- Auth scheme and authorization rules are documented.
- Success and error examples are present.
- Event delivery semantics are documented for async integrations.
- Contract verification command or missing-tool gap is recorded.
- External writes are staged and approval-bound.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| HTTP API contract | OpenAPI | Default source for REST-like HTTP APIs. Pin spec version per project. |
| Event API contract | AsyncAPI | Default source for message-driven APIs and webhooks when useful. |
| Shared JSON schemas | JSON Schema | Declare dialect; avoid validator-default ambiguity. |
| Error model | RFC 9457 Problem Details | Good default for machine-readable HTTP errors. |
| API lint | Spectral | Useful when the project has an API style guide. Tool adoption requires stack check. |
| Code/doc generation | OpenAPI Generator | Useful for SDKs/stubs/docs; generated output requires ownership and diff review. |
| Consumer contracts | Pact | Useful when real consumer expectations matter more than schema completeness. |
| Event metadata | CloudEvents | Useful for cross-system event interoperability; not mandatory for simple internal events. |
| RPC | gRPC/protobuf | Useful for low-latency, typed, polyglot service-to-service APIs. |
| Query API | GraphQL | Useful for client-shaped reads and schema-driven product APIs; requires governance for complexity, authorization and deprecation. |

## Failure modes

- Treating rendered API docs as the source of truth instead of the machine-readable contract.
- Shipping event payload changes without consumer compatibility review.
- Assuming an internal API has no consumers.
- Generating SDKs without a reproducible generator config.
- Adding OAuth scopes or token claims without an authorization matrix.
- Returning undocumented error payloads that clients cannot handle.
- Treating GraphQL or gRPC as automatically superior to HTTP APIs without consumer and operational justification.
- Letting contract tests duplicate only provider behavior instead of expressing consumer expectations.
- Allowing an agent to write to external systems without staged artifact and approval.

## Open questions for deeper research

- Which API lint tool should become the Product-Agent OS default: Spectral, Redocly CLI, framework-native checks or no default?
- Should Product-Agent OS ship a generic API style guide template, or only a selector that asks the project to choose one?
- Which schema compatibility rules should be encoded for JSON Schema, protobuf, GraphQL and AsyncAPI separately?
- Should API security gates be based on OWASP API Top 10, ASVS, SSDF, or a combined project profile?
- How should agentic API migrations handle generated clients across multiple repositories?
- Which API test generators are mature enough for default recommendation by stack?

## Sources

- [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- [AsyncAPI Specification v3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0)
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html)
- [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)
- [JSON Schema Specification](https://json-schema.org/specification)
- [CloudEvents](https://cloudevents.io/)
- [GraphQL Specification Versions](https://spec.graphql.org/)
- [gRPC Introduction](https://grpc.io/docs/what-is-grpc/introduction/)
- [Pact Documentation](https://docs.pact.io/)
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Stoplight Open Source API Toolkit](https://stoplight.io/open-source)
- [Google API Improvement Proposals](https://google.aip.dev/)
- [Context7 research](../sources/context7-research.md)

## Async and steering contract

In an OpenAI async integration the application owns pending work, call_id, deadlines and idempotent application. Steering does not cancel a started side effect. Check late/duplicate/failed results against [session control](../agent-systems/session-control.md).
