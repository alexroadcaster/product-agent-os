# Backend

Source status: `official + expert reference + vendor documentation + local implementation evidence + tool-assisted`

Источники: [Twelve-Factor App](https://www.12factor.net/), [OpenTelemetry documentation](https://opentelemetry.io/docs/), [Google SRE SLO chapter](https://sre.google/sre-book/service-level-objectives/), [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md), [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture), [Martin Fowler Microservices Guide](https://martinfowler.com/microservices/), [Azure Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry), [Azure Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker), [Azure Queue-Based Load Leveling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling), [Azure Health Endpoint Monitoring pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring), [Azure Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/backend.md).

## Deep research цель

Backend слой описывает service responsibilities, domain logic, jobs, queues, runtime configuration, observability, reliability, security, health checks, data consistency and operational safety.

Главный принцип: backend-изменение нельзя считать завершенным, если понятен code diff, но не понятны runtime behavior, failure modes, observability, rollback and production impact.

## Поддержанные факты

- Twelve-Factor App задает service-style vocabulary: explicit dependencies, environment config, backing services, build-release-run separation, stateless processes, disposability, dev/prod parity, logs and admin processes.
- OpenTelemetry defines vendor-neutral observability concepts for traces, metrics, logs, context propagation, baggage, semantic conventions, collectors and language instrumentation.
- Google SRE guidance frames SLO work around user-relevant SLIs and recommends a small number of indicators that represent what users care about.
- NIST SSDF recommends secure software development practices that can be integrated into SDLC implementations.
- OWASP ASVS provides a versioned basis for testing web application technical security controls and secure development requirements.
- CNCF Cloud Native Definition characterizes cloud-native systems as loosely coupled, secure, resilient, manageable, sustainable and observable, supported by automation.
- Kubernetes readiness, liveness and startup probes are distinct runtime health mechanisms; readiness prevents traffic from reaching a service that is alive but not ready.
- Hexagonal Architecture / Ports and Adapters separates application logic from UI, database and runtime adapters so application behavior can be tested through ports.
- Martin Fowler's microservices guide defines microservices as independently deployable services built around business capabilities and highlights design-for-failure.
- Azure Architecture Center documents retry, circuit breaker, queue-based load leveling, health endpoint monitoring and saga patterns. These are vendor docs, but the patterns are useful backend resilience references.

## Assumptions

- Product-Agent OS should default to clear backend boundaries before recommending microservices. Microservices are conditional, not a maturity badge.
- Backend docs must describe runtime behavior, not only package/module structure.
- Retry, queue and distributed workflow behavior is unsafe unless idempotency, timeout, max attempts, replay and recovery are explicit.
- SLOs are required for production/user-facing services unless an explicit gap is recorded.
- Security-sensitive backend behavior includes auth, secrets, tokens, PII, money movement, privileged operations, external writes and irreversible side effects.
- Platform-specific health checks should use the deployment platform semantics. Kubernetes probe vocabulary is a useful reference, not a universal runtime requirement.

## Инструкции применения на проекте

1. Классифицируйте backend unit: module, monolith subsystem, service, worker, scheduler, consumer, API backend, integration adapter or migration runner.
2. Назовите service boundary: purpose, owner, inbound contracts, outbound dependencies, data ownership and deployment/runtime shape.
3. Для complex domain свяжите boundary with bounded context and ubiquitous language.
4. Применяйте Hexagonal Architecture / Ports and Adapters, когда domain logic должна быть независима от HTTP, database, queue or vendor SDK concerns.
5. До реализации distributed behavior опишите retries, timeouts, idempotency, deduplication, backpressure, ordering, scheduling and replay.
6. Для каждой remote dependency задайте timeout, retry, circuit breaker, fallback, alert and owner.
7. Для jobs/queues опишите payload contract, retry policy, dead-letter behavior, idempotency key and replay procedure.
8. Для distributed transactions сначала проверьте, достаточно ли local transaction/outbox. Если нет, документируйте saga/compensation and monitoring.
9. Определите observability evidence: traces for request flow, metrics for service health, logs for decisions/errors and correlation IDs across boundaries.
10. Для production services задайте SLI/SLO или explicit gap.
11. Treat health endpoints as contracts: liveness, readiness and startup checks не должны быть синонимами.
12. Документируйте config and secrets boundaries; secrets не должны попадать в docs, prompts, fixtures, logs or examples.
13. Auth, sensitive data, money movement, privileged operations and irreversible side effects route through risk/security review.
14. Для risky backend changes заранее укажите rollback, recovery or replay path.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Modular monolith first | Early/medium product, unclear service boundaries | One deployable backend with explicit module boundaries and ownership. |
| Conditional microservices | Proven independent scaling/team/deploy need | Services map to business capabilities, have independent deployability and explicit failure contracts. |
| Hexagonal Architecture / Ports and Adapters | Domain logic is important and adapters change | Core use cases depend on ports; DB/API/queue/vendor SDK are adapters. |
| DDD boundaries | Complex business domain | Backend modules/services map to bounded contexts and domain language. |
| TDD for domain logic | Deterministic business rules and service logic | Unit tests drive behavior before implementation. |
| Integration-first backend testing | Storage, queues, transactions, external adapters | Tests exercise real or representative boundaries before release. |
| Contract-aware service development | APIs/events/external contracts | OpenAPI, AsyncAPI, Pact, `.proto` or provider contracts updated with code. |
| Twelve-Factor service discipline | SaaS/cloud-style backend | Config/env, dependencies, build-release-run, logs and admin tasks are documented. |
| SRE-inspired reliability | Production service with users or downstream consumers | SLO/gap, user-relevant SLIs, runbooks and alert signals. |
| Observability-driven development | Debugging requires runtime evidence | Traces, metrics, logs, correlation IDs, dashboards and alerts are captured. |
| Resilience pattern design | Remote dependencies, queues, load spikes, transient faults | Timeouts, retry, backoff, circuit breaker, load leveling, backpressure and fallback. |
| Secure SDLC | Auth, secrets, sensitive data, money or privileged operations | Security notes, abuse cases, audit logging and no-secrets evidence are required. |
| Saga / compensating workflow | Distributed transaction cannot use single ACID transaction | Workflow state, idempotency, compensation, monitoring and recovery path. |
| Runbook-driven operations | Production service, worker or scheduled job | Типовые сбои, dashboards, logs, restart/replay steps and escalation path. |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Зачем нужен | Практический формат |
| --- | --- | --- |
| `backend-service-overview.md` | Purpose, owner, boundary, dependencies, data stores, APIs/events and runtime. | Product-Agent OS template. |
| Module/service boundary map | What belongs inside the backend boundary and what is external. | C4, Mermaid, Structurizr, ADR. |
| Ports and adapters map | Inbound ports, outbound ports and concrete adapters. | Hexagonal Architecture note. |
| `backend-runtime-behavior.md` | Jobs, queues, retries, timeouts, idempotency, backpressure and failure modes. | Runtime behavior doc. |
| `backend-dependency-failure-matrix.md` | Per dependency timeout, retry, circuit breaker, fallback, owner and alert. | Resilience matrix. |
| `backend-observability-map.md` | Traces, metrics, logs, correlation IDs, dashboards, alerts and redaction notes. | OpenTelemetry vocabulary. |
| `backend-slo-sheet.md` | User journey, SLI, SLO target, measurement window and alert policy. | Google SRE-inspired sheet. |
| `backend-health-check-contract.md` | Liveness/readiness/startup or equivalent platform health semantics. | Kubernetes/platform docs. |
| `backend-job-queue-contract.md` | Queue name, producer, consumer, payload contract, idempotency, retry, DLQ and replay. | AsyncAPI/runbook. |
| `backend-data-consistency-record.md` | Transaction boundary, consistency model, outbox/saga/compensation and recovery path. | ADR/runbook. |
| Security notes | Authn/authz, secrets, rate limits, audit logging, sensitive data and abuse cases. | NIST SSDF / OWASP ASVS. |
| `backend-config-secrets-manifest.md` | Env/config keys, secret source, rotation notes and local/prod parity. | Twelve-Factor/platform docs. |
| `backend-release-rollback-notes.md` | Migration, feature flag, rollback, replay and data recovery plan. | Release packet. |
| `backend-operational-runbook.md` | Common failures, dashboard links, logs, recovery steps and escalation. | SRE practice. |

## Product-Agent OS routing

- `workspace-discovery-auditor` maps backend stack, commands, CI, APIs, DB, queues, workers, deployment and security signals.
- `requirements-author` records service/user behavior, non-goals and runtime constraints before implementation tasks.
- `implementation-planner` blocks risky backend work if service boundary, runtime behavior, rollback or verification is missing.
- `test-eval-designer` selects unit, integration, contract, migration, runtime and observability checks.
- `risk-reviewer` handles security, data, migration, performance, external dependency and irreversible side-effect risk.
- `pr-release-operator` includes backend release notes, migration guidance, runbook impact and rollback/replay notes.

## Candidate readiness gates

- `backend_service_boundary_present`: purpose, owner, dependencies and data stores are named.
- `backend_runtime_behavior_present`: retry, timeout, idempotency, ordering, replay and failure modes are documented.
- `backend_dependency_failure_matrix_present`: remote dependencies have timeout/retry/fallback/alert/owner policy.
- `backend_observability_contract_present`: logs/metrics/traces/correlation IDs and redaction notes are present.
- `backend_slo_or_gap_present`: user-facing or production service has SLO/SLI or explicit gap.
- `backend_health_probe_contract_present`: liveness/readiness/startup semantics are documented where applicable.
- `backend_security_reviewed`: auth, secrets, sensitive data, money and privileged operations have review route.
- `backend_data_consistency_strategy_present`: transaction boundary, consistency model and recovery path are documented.
- `backend_config_secrets_boundary_present`: config and secrets handling is explicit.
- `backend_rollback_plan_present`: migration, external write or production behavior change has rollback/recovery path.

## Candidate eval fields

- Service/module boundary, owner and purpose are present.
- Dependencies and data stores are named.
- Runtime behavior is documented for jobs, queues and remote calls.
- Retry policy includes timeout, backoff, max attempts and idempotency.
- Observability contract includes no-secrets logging and correlation IDs.
- SLO/SLI exists or gap is explicit.
- Health checks distinguish liveness, readiness and startup where applicable.
- Security-sensitive behavior has a risk review route.
- Data consistency and rollback plan exist for risky changes.
- Verification commands include unit, integration, contract or runtime checks appropriate to the change.

## Tooling candidates

| Tooling area | Candidate | Notes |
| --- | --- | --- |
| Runtime service discipline | Twelve-Factor | Good default vocabulary for config, logs, processes and dev/prod parity. |
| Observability | OpenTelemetry | Cross-stack vocabulary for traces, metrics, logs, context propagation and collectors. |
| Reliability | SLO/SLI sheets | Use user-relevant indicators, not every available metric. |
| Service architecture | C4, ADR, Ports and Adapters map | Useful when service boundaries or adapters change. |
| Runtime health | Kubernetes probes or platform equivalent | Use only when deployment platform supports probe semantics. |
| Resilience patterns | Retry, circuit breaker, load leveling, health endpoint monitoring | Vendor docs are references; implementation should be stack-native. |
| Distributed workflow | Saga/compensation docs | Use only when local transaction/outbox is not enough. |
| Security | SSDF, ASVS, secret scanning, SAST/DAST where applicable | Select by stack and risk profile. |
| Local runtime signals | `Dockerfile`, `Procfile`, `docker-compose.yml`, `serverless.yml`, `k8s/*.yaml` | Discovery signals, not mandatory standards. |

## Проверки

- Service overview updated for new or changed backend responsibility.
- Unit tests cover deterministic domain logic.
- Integration/contract tests cover storage, queues, APIs or external adapters affected by the change.
- Retry logic has timeout, backoff, max attempts and idempotency evidence.
- Observability changes avoid secrets and private data.
- Health checks are tested or explicitly marked as platform-unavailable.
- Rollback/replay path is named for risky backend changes.
- Config and secrets boundary is documented without exposing secrets.
- Runtime verification exists for deployable services where environment is available.

## Типовые сбои

- Backend docs describe packages but omit runtime behavior.
- Retry logic is added without timeout, backoff, max attempts and idempotency.
- Liveness and readiness endpoints are treated as the same check.
- Logs expose secrets, tokens, private data or full payloads.
- Worker can process the same message twice but has no deduplication policy.
- Queue has no dead-letter, replay or poison-message procedure.
- Service boundary changes happen without owner review or ADR.
- Distributed workflow has no compensation or recovery evidence.
- Microservices are introduced before module boundaries, deployment automation and observability are mature.
- Completion is claimed after code inspection without integration/runtime verification.

## Unsupported claims not adopted

- "Backend means only business logic files." Backend includes runtime, data, queues, config, observability, security and operations.
- "Microservices are the professional default." They are useful only with real ownership, deployment and scaling reasons.
- "Retries make systems reliable." Retries without idempotency and backoff can amplify failure.
- "Health endpoint exists, so readiness is solved." Liveness/readiness/startup have different operational meanings.
- "Logs are observability." Logs are one signal; traces, metrics, correlation IDs and dashboards matter for runtime evidence.
- "SLOs are only for large companies." Any production service needs user-relevant reliability expectation or explicit gap.

## Open questions for future implementation

- Should Product-Agent OS default to modular monolith guidance before microservice guidance in generated templates?
- Which stack-specific backend templates should be generated first: Node.js, Python, Java, .NET, Go or framework-agnostic only?
- Should health check templates be platform-neutral or Kubernetes-first with alternatives?
- Which resilience library examples are mature enough for stack-specific snippets?
- How should the plugin detect risky retry/idempotency changes from code alone?
- Should SLO templates live under backend, delivery/operations or both?
