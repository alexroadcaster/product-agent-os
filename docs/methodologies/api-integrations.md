# API & Integrations

Source status: `official + verified methodology + local implementation evidence + tool-assisted`

Источники: [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html), [AsyncAPI Specification v3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0), [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html), [RFC 9700: OAuth 2.0 Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html), [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/), [JSON Schema](https://json-schema.org/specification), [CloudEvents](https://cloudevents.io/), [GraphQL Specification](https://spec.graphql.org/), [gRPC Introduction](https://grpc.io/docs/what-is-grpc/introduction/), [Pact](https://docs.pact.io/), [OpenAPI Generator](https://openapi-generator.tech/), [Stoplight Open Source API Toolkit](https://stoplight.io/open-source), [Google API Improvement Proposals](https://google.aip.dev/), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/api-integrations.md).

## Deep research цель

API & Integrations слой защищает public contracts, event contracts, generated clients, consumers, auth, error model, compatibility, rollout, deprecation policy and external-system write boundaries.

Главный принцип: API-изменение нельзя считать локальным изменением кода, пока не понятны contract source of truth, consumers, security model, compatibility impact, observability and release path.

## Поддержанные факты

- OpenAPI Specification v3.2.0 описывает HTTP APIs в language-agnostic формате: operations, parameters, request bodies, responses, examples, security schemes and reusable components.
- AsyncAPI Specification v3.1.0 описывает message-driven APIs в machine-readable and protocol-agnostic формате.
- RFC 9110 задает HTTP semantics; проект не должен изобретать локальные значения для methods, status codes and content negotiation без compatibility reason.
- RFC 9457 Problem Details является сильным default для machine-readable HTTP error payloads, если существующие клиенты не требуют другой формат.
- RFC 9700 OAuth 2.0 Security Best Current Practice должен использоваться как security baseline для OAuth-based APIs.
- OWASP API Security Top 10 2023 дает API-specific risk vocabulary для threat modeling and security review gates.
- JSON Schema current official dialect is 2020-12; payload contracts should state the dialect instead of relying on validator defaults.
- CloudEvents v1.0.2 provides a standardized event metadata envelope option when cross-system event interoperability matters.
- GraphQL projects should pin the specification target and govern schema complexity, deprecations and authorization instead of saying only "GraphQL".
- gRPC uses Protocol Buffers as the default IDL and message interchange format; `.proto` files become source contracts.
- Pact consumer-driven contract tests complement schema contracts because they capture real consumer expectations.
- OpenAPI Generator can generate clients, server stubs and documentation from OpenAPI documents; generated SDKs need manifest, ownership and versioning.
- Stoplight/Spectral is a candidate JSON/YAML lint path for projects with API style guides.
- Google API Improvement Proposals are vendor-specific, but the transferable pattern is a local, versioned API style guide.

## Assumptions

- Product-Agent OS should not choose REST, GraphQL, gRPC or events as a universal default. API style is selected by consumers, latency, ownership, ecosystem, tooling and operational risk.
- Contract-first is required for new public APIs, SDKs and provider/consumer splits; contract-aware development is acceptable when an existing code-first service has a maintained contract.
- Rendered docs, Swagger UI, generated HTML and screenshots are not source of truth. The machine-readable contract or explicit gap is the source of truth.
- Internal APIs can still have consumers. "Internal" only reduces exposure; it does not remove compatibility review.
- External writes are side effects. Agents must use staged drafts, approval records and rollback paths before mutating external systems.

## Инструкции применения на проекте

1. Классифицируйте integration: internal HTTP API, public API, partner API, webhook, async event stream, GraphQL, gRPC, SDK, external provider or automation integration.
2. Назовите contract source of truth: OpenAPI, AsyncAPI, GraphQL schema, `.proto`, JSON Schema, Pact contract or explicit gap.
3. Зафиксируйте provider, consumers, owners, generated clients and runtime environments.
4. Классифицируйте change: additive, behavior-compatible, potentially breaking or breaking.
5. Обновите contract до или вместе с code. Contract drift должен блокировать completion claim.
6. Добавьте examples для success, validation failure, auth failure and important domain failure.
7. Опишите auth scheme, scopes, token claims, object-level authorization, rate limits and sensitive fields.
8. Для HTTP errors используйте documented error model; RFC 9457 Problem Details является default, если нет compatibility constraint.
9. Для events/webhooks опишите payload schema, headers, correlation ID, idempotency, retry, ordering and dead-letter behavior.
10. Для generated SDKs обновите generator config, target languages, versioning and release notes.
11. Добавьте contract tests: schema validation, provider verification and consumer-driven tests where consumer risk is high.
12. Для external writes создайте staged artifact или approval record до фактического external mutation.
13. Добавьте observability expectations: request IDs, correlation IDs, error counters, latency, rate-limit metrics and integration failure alerts.
14. Запишите rollout, deprecation and rollback path in release artifact.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Contract-first development | New public API, SDK, provider/consumer split | Contract пишется или меняется до implementation; code/tests conform to it. |
| Contract-aware development | Existing code-first service | Generated or maintained contract обновляется in the same slice as behavior. |
| Consumer-driven contract testing | Multiple consumers, microservices, frontend/backend split | Consumers express expectations; providers verify before release. |
| API lifecycle governance | Draft, experimental, stable, deprecated, removed APIs | Endpoint/message has lifecycle state, owner, compatibility policy and deprecation path. |
| Backward compatibility by default | Public, partner, mobile, SDK or event contracts | Breaking/non-breaking classification before implementation. |
| Error-contract governance | HTTP APIs consumed by software clients | Stable error types, status codes, examples and extensions. |
| Event-contract governance | Async messaging, queues, streams, webhooks | Schema, metadata, retry, idempotency, ordering, correlation and dead-letter semantics. |
| Integration security by design | Authenticated API, external provider, sensitive data | Auth matrix, scopes, object-level authorization, abuse cases and sensitive field review. |
| Generated-client governance | SDKs or typed clients are generated | Generator, config, target languages, compatibility and release process are documented. |
| API style-guide governance | Large project or many teams | Naming, pagination, filtering, versioning, status codes and examples are versioned/lintable. |
| Two-stage review | Public contract, migration, SDK, auth or event payload | Stage 1 checks contract/security/compatibility; stage 2 checks implementation quality. |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Зачем нужен | Практический формат |
| --- | --- | --- |
| `api-inventory.md` | APIs, owners, lifecycle states, consumers and source-of-truth files. | Markdown/YAML table. |
| OpenAPI document | HTTP API source of truth. | `openapi.yaml`, `openapi.yml`, `openapi.json`, pinned spec version. |
| AsyncAPI document | Message/event API source of truth. | `asyncapi.yaml`, `asyncapi.yml`, `asyncapi.json`, pinned spec version. |
| GraphQL schema | GraphQL contract source. | `schema.graphql`, deprecations, auth notes, complexity constraints. |
| gRPC/protobuf IDL | RPC contract source. | `.proto` files and generator config. |
| JSON Schema library | Shared JSON payload contracts. | JSON Schema 2020-12 or project-pinned dialect. |
| `api-error-catalog.md` | Stable HTTP error types, status codes, extensions and examples. | RFC 9457 Problem Details where compatible. |
| `api-auth-authorization-matrix.md` | Auth schemes, scopes, roles, token claims and object-level rules. | OpenAPI security schemes + OAuth BCP + OWASP API risks. |
| `api-consumer-map.md` | Human/system consumers, SDKs, generated clients, owners and approval path. | Consumer/owner matrix. |
| `api-compatibility-record.md` | Breaking/non-breaking classification and migration impact. | ADR-style record. |
| `api-contract-test-matrix.md` | Provider verification, consumer tests, schema tests and negative cases. | Pact, schema validators, stack-specific API tests. |
| `generated-sdk-manifest.md` | Generator, version, config, target languages, owner and release process. | OpenAPI Generator or stack-specific generator. |
| `webhook-event-contract.md` | Retry, idempotency, ordering, signature verification, replay and dead-letter behavior. | AsyncAPI, CloudEvents where useful. |
| `external-integration-approval.md` | Read/write capability, sandbox credentials, staged draft, approval and rollback path. | Project control-plane artifact. |
| `api-style-guide.md` | Naming, pagination, filtering, versioning, status codes, errors and examples. | Local rules inspired by selected API guidelines. |
| Deprecation plan | Timeline, compatibility mode, communication, release notes and removal criteria. | Release packet / changelog. |

## Product-Agent OS routing

- `api_migration` usage mode routes API/SDK/event changes to migration planning before implementation.
- `workspace-discovery-auditor` detects OpenAPI, AsyncAPI, GraphQL, protobuf, Pact, generated clients and external integrations.
- `implementation-planner` blocks build if contract source, consumers, compatibility classification or owner review is missing.
- `test-eval-designer` asks for contract tests, consumer tests, schema validation and negative auth/error cases.
- `risk-reviewer` performs two-stage review for public contract, auth, event, SDK and external-integration changes.
- `pr-release-operator` includes release notes, migration guidance, SDK impact, deprecation plan and rollback/disable path.

## Candidate readiness gates

- `api_contract_source_present`: OpenAPI, AsyncAPI, GraphQL schema, `.proto`, JSON Schema, Pact contract or explicit gap is named.
- `api_consumer_map_present`: consumers, generated clients and owners are named for public, partner, mobile or multi-team contracts.
- `api_breaking_change_reviewed`: migration plan, deprecation window and owner approval exist for breaking/potentially breaking changes.
- `api_security_reviewed`: auth scheme, authorization rules, scopes, sensitive fields and abuse cases are documented.
- `api_error_contract_present`: success and error examples are present.
- `event_delivery_contract_present`: retry, idempotency, ordering, correlation and dead-letter behavior are documented.
- `generated_client_manifest_present`: SDK generator/config/release impact is documented.
- `external_write_approval_present`: staged draft, approval and rollback path exist before writes to external systems.

## Candidate eval fields

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
| API lint | Spectral / Stoplight | Useful when the project has API style guide rules; adoption requires stack check. |
| Code/doc generation | OpenAPI Generator | Useful for SDKs/stubs/docs; generated output requires ownership and diff review. |
| Consumer contracts | Pact | Useful when real consumer expectations matter more than schema completeness. |
| Event metadata | CloudEvents | Useful for cross-system event interoperability; not mandatory for simple internal events. |
| RPC | gRPC/protobuf | Useful for typed, polyglot service-to-service APIs; `.proto` is the source contract. |
| Query API | GraphQL | Useful for client-shaped reads; requires complexity, authorization and deprecation governance. |
| API style rules | Google AIP-style local guide | Vendor-specific source used as inspiration for local governed style rules. |

## Проверки

- Contract source is updated or gap is explicit.
- Consumers and generated clients are named.
- Breaking change has migration plan and owner review.
- Auth/security changes have security review route.
- Error model is documented and examples exist.
- Event delivery semantics are documented for async integrations.
- Contract check command is run or recorded as missing.
- External write operations are staged and approval-bound.
- Release notes mention SDK, consumer, deprecation and rollback impact when relevant.

## Типовые сбои

- Swagger UI or rendered docs are treated as source of truth instead of OpenAPI/contract files.
- Internal API is assumed to have no consumers.
- Event payload changes are released without consumer compatibility review.
- Security schemes are documented in prose but missing from contract.
- SDKs are regenerated without reproducible config and reviewable diff.
- OAuth scopes or token claims change without authorization matrix.
- Error payloads are improvised per endpoint.
- GraphQL or gRPC is chosen as automatically superior without consumer and operational justification.
- Contract tests duplicate only provider behavior instead of expressing consumer expectations.
- Agent writes to external systems without staged artifact and explicit approval.

## Unsupported claims not adopted

- "Rendered API docs are enough." They are outputs, not source of truth.
- "Internal APIs do not need compatibility review." Internal consumers still break.
- "Schema validation is the same as contract testing." Schema validation does not capture all consumer expectations.
- "GraphQL/gRPC/event-driven is always more modern." Style choice depends on consumers, operations and governance.
- "OAuth exists, so API security is handled." Scopes, token claims, object-level authorization, rate limits and abuse cases still need review.
- "Generated SDKs are mechanical." Generator config, versioning and consumer migration need ownership.

## Open questions for future implementation

- Which API lint tool should become the Product-Agent OS default: Spectral, Redocly CLI, framework-native checks or no default?
- Should Product-Agent OS ship a generic `api-style-guide.md`, or only a selector that asks the project to choose one?
- Which compatibility rules should be encoded separately for JSON Schema, protobuf, GraphQL and AsyncAPI?
- Should API security gates be based on OWASP API Top 10, ASVS, SSDF or a combined project profile?
- How should agentic API migrations handle generated clients across multiple repositories?
- Which API test generators are mature enough for stack-specific default recommendations?
