---
title: "Archive - Backend Methodology Research"
---

# Archive - Backend Methodology Research {#backend-methodology-research}

> Historical source record. Dates and verdicts below describe that run; use current guides for present behavior.

Source status: `official + expert reference + vendor documentation + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/backend.md](../../methodologies/backend.md)

Target Product-Agent OS behavior: detect backend work, force service boundary and runtime behavior clarity, route risky service changes through reliability/security/data/operations gates, and require evidence for tests, observability, rollback and production readiness before completion.

## Scope

This dossier covers backend services, modular monolith modules, workers, schedulers, queues, service boundaries, domain logic, background jobs, runtime configuration, resiliency, observability, SLOs, security, health checks, distributed consistency and operational documentation.

It does not mandate microservices, Kubernetes, a cloud provider or a specific framework. Those are conditional implementation choices, not default architecture rules.

## Supported facts

- The Twelve-Factor App defines a methodology for service-style applications, including explicit dependencies, environment-based config, backing services as attached resources, build-release-run separation, stateless processes, disposability, dev/prod parity, logs as event streams and one-off admin processes.
- OpenTelemetry is a vendor-neutral observability framework for traces, metrics and logs, with concepts for context propagation, baggage, semantic conventions, collectors and language instrumentation.
- Google SRE guidance frames SLO work around user-relevant SLIs and recommends choosing a small number of indicators that represent what users care about.
- NIST SSDF recommends secure software development practices that can be integrated into SDLC implementations.
- OWASP ASVS provides a versioned basis for testing web application technical security controls and secure development requirements.
- CNCF Cloud Native Definition characterizes cloud-native systems as loosely coupled, secure, resilient, manageable, sustainable and observable, supported by automation.
- Kubernetes readiness, liveness and startup probes are distinct runtime health mechanisms. Readiness prevents traffic from reaching a service that is alive but not ready.
- Hexagonal Architecture, also known as Ports and Adapters, separates application logic from UI, database and runtime adapters so the application can be tested and driven through multiple ports.
- Martin Fowler's microservices guide defines microservices as independently deployable services built around business capabilities and highlights design-for-failure as a characteristic.
- Microsoft Azure Architecture Center documents retry, circuit breaker, queue-based load leveling, health endpoint monitoring and saga patterns. These are vendor-specific docs, but the patterns are broadly useful as backend resilience and distributed workflow references.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Modular monolith first | Early or medium-size product, unclear service boundaries | Keep deployable complexity low while enforcing module ownership and domain boundaries. |
| Conditional microservices | Independent scaling, team ownership or deployment autonomy is proven | Services map to business capabilities, have independent deployability and explicit failure contracts. |
| Hexagonal Architecture / Ports and Adapters | Domain logic is important and adapters change | Core use cases depend on ports/interfaces; database, HTTP, queue and vendor SDKs are adapters. |
| Domain-Driven Design boundaries | Complex business domain or ambiguous vocabulary | Backend modules/services map to bounded contexts and ubiquitous language. |
| TDD for domain logic | Deterministic business rules and service logic | Unit tests drive behavior before implementation. |
| Integration-first backend testing | Storage, queues, transactions, external adapters | Tests exercise real or representative boundaries before release. |
| Contract-aware service development | Service exposes APIs/events or consumes external contracts | OpenAPI, AsyncAPI, Pact, `.proto` or provider contract changes are updated with code. |
| Twelve-Factor service discipline | SaaS/cloud-style backend | Config, dependencies, runtime process model, logs and admin tasks are documented. |
| SRE-inspired reliability | Production service with users or downstream consumers | SLO or explicit gap, user-relevant SLIs, runbooks and alert signals. |
| Observability-driven development | Debugging requires runtime evidence | Traces, metrics, logs, correlation IDs and dashboard/alert expectations are captured. |
| Resilience pattern design | Remote dependencies, queues, load spikes or transient faults | Timeouts, retry, backoff, circuit breaker, load leveling, backpressure and fallback are designed together. |
| Secure SDLC | Backend touches auth, sensitive data, money, secrets or privileged operations | Security requirements, threat notes, abuse cases, audit logging and no-secrets evidence are required. |
| Saga / compensating workflow | Distributed business transaction cannot use a single ACID transaction | Workflow state, idempotency, compensation, monitoring and failure recovery are documented. |
| Runbook-driven operations | Production service or scheduled job | Operators get failure modes, dashboards, logs, restart/replay steps and escalation path. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| Service overview | Purpose, owner, boundary, dependencies, data stores, APIs/events and runtime. | `backend-service-overview.md` |
| Module/service boundary map | Shows what belongs inside the backend boundary and what is external. | C4, Mermaid, Structurizr, ADR |
| Ports and adapters map | Lists inbound ports, outbound ports and concrete adapters. | Hexagonal Architecture |
| Runtime behavior doc | Background jobs, queues, retries, timeouts, idempotency, backpressure and failure modes. | `backend-runtime-behavior.md` |
| Dependency failure matrix | Per dependency: timeout, retry, circuit breaker, fallback, owner and alert. | Resilience pattern docs |
| Observability map | Traces, metrics, logs, correlation IDs, dashboards, alerts and redaction notes. | OpenTelemetry |
| SLO sheet | User journey, SLI, SLO target, measurement window and alert policy. | Google SRE |
| Health check contract | Liveness/readiness/startup or equivalent health semantics. | Kubernetes docs, platform docs |
| Queue/job contract | Queue name, producer, consumer, payload contract, idempotency, retry, DLQ and replay. | AsyncAPI, runbook |
| Data consistency record | Transaction boundary, consistency model, outbox/saga/compensation and recovery path. | ADR/runbook |
| Security notes | Authn/authz, secrets, rate limits, audit logging, sensitive data and abuse cases. | NIST SSDF, OWASP ASVS |
| Config and secrets manifest | Env/config keys, secret source, rotation notes and local/prod parity. | Twelve-Factor, platform docs |
| Release and rollback notes | Migration, feature flag, rollback, replay and data recovery plan. | Release packet |
| Operational runbook | Common failures, dashboard links, logs, recovery steps and escalation. | SRE practice |

## Project application instructions

1. Classify the backend unit: module, monolith subsystem, service, worker, scheduler, consumer, API backend, integration adapter or migration runner.
2. Name the service boundary: purpose, owner, inbound contracts, outbound dependencies, data ownership and deployment/runtime shape.
3. If the domain is complex, map the boundary to bounded contexts and domain language.
4. Decide whether Ports and Adapters is useful. Apply it when domain logic must stay independent from HTTP, database, queue or vendor SDK concerns.
5. Document runtime behavior before implementing distributed behavior: retries, timeouts, idempotency, deduplication, backpressure, ordering, scheduling and replay.
6. For every remote dependency, write a failure policy: timeout, retry, circuit breaker, fallback, alert and owner.
7. For background jobs and queues, document payload contract, retry policy, dead-letter behavior, idempotency key and replay procedure.
8. For distributed transactions, prefer a simple local transaction when possible. If not possible, document saga/compensation and monitoring explicitly.
9. Define observability evidence: traces for request flow, metrics for service health, logs for decisions/errors and correlation IDs across boundaries.
10. For production services, define SLO or record why it is not yet applicable.
11. Treat health endpoints as contracts. Liveness, readiness and startup checks should not be vague aliases.
12. Document config and secrets. Secrets must not appear in docs, prompts, fixtures, logs or examples.
13. Route auth, sensitive data, money movement, privileged operations and irreversible side effects through security/risk review.
14. Record rollback and recovery before claiming completion for risky backend changes.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `backend/`, `server/`, `services/`, `workers/`, `jobs/`, `queues/`, `cron/`, `schedulers/`, `consumers/`, `adapters/`, `repositories/`, `migrations/`
- Files: `Dockerfile`, `Procfile`, `docker-compose.yml`, `k8s/*.yaml`, `helm/`, `serverless.yml`, `openapi.yaml`, `asyncapi.yaml`, `.proto`
- Terms: service, worker, queue, retry, timeout, idempotency, circuit breaker, background job, scheduler, migration, auth, token, secret, SLO, runbook, health check, readiness, liveness
- Dependency signals: database clients, message broker clients, HTTP clients, payment/email/storage/search providers, cache clients

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `backend_service_boundary_present` | New service/module/worker or changed ownership | Purpose, owner, dependencies or data stores are missing. |
| `backend_runtime_behavior_present` | Worker, queue, scheduler, remote dependency or background behavior | Retry, timeout, idempotency, ordering, replay or failure mode is unspecified. |
| `backend_dependency_failure_matrix_present` | Remote service, DB, cache, queue or third-party dependency | No timeout/retry/fallback/alert/owner policy. |
| `backend_observability_contract_present` | Production runtime behavior changes | Logs/metrics/traces/correlation IDs or redaction notes are missing. |
| `backend_slo_or_gap_present` | User-facing or production service | No SLO/SLI or explicit gap. |
| `backend_health_probe_contract_present` | Deployable service or worker with health checks | Liveness/readiness/startup semantics are not documented. |
| `backend_security_reviewed` | Auth, secrets, sensitive data, money, privileged operations | No security notes, threat/abuse cases or reviewer route. |
| `backend_data_consistency_strategy_present` | Multi-step data change, queue, outbox, saga or migration | Transaction boundary, consistency model and recovery path are missing. |
| `backend_config_secrets_boundary_present` | Config/env/secrets change | No config manifest or secret handling note. |
| `backend_rollback_plan_present` | Migration, irreversible side effect, external write or production behavior change | No rollback, recovery or replay path. |

### Candidate templates

- `backend-service-overview.md`
- `backend-runtime-behavior.md`
- `backend-dependency-failure-matrix.md`
- `backend-observability-map.md`
- `backend-slo-sheet.md`
- `backend-health-check-contract.md`
- `backend-job-queue-contract.md`
- `backend-data-consistency-record.md`
- `backend-config-secrets-manifest.md`
- `backend-operational-runbook.md`
- `backend-release-rollback-notes.md`

### Candidate eval fields

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
| Observability | OpenTelemetry | Default cross-stack vocabulary for traces, metrics, logs, context propagation and collectors. |
| Reliability | SLO/SLI sheets | Use user-relevant indicators, not every available metric. |
| Service architecture | C4, ADR, Ports and Adapters map | Useful when service boundaries or adapters change. |
| Runtime health | Kubernetes probes or platform equivalent | Use only when the deployment platform supports probe semantics. |
| Resilience patterns | Retry, circuit breaker, load leveling, health endpoint monitoring | Vendor-specific docs are references; project implementation should be stack-native. |
| Distributed workflow | Saga/compensation docs | Use only when local transaction/outbox is not enough. |
| Security | SSDF, ASVS, secret scanning, SAST/DAST where applicable | Select by stack and risk profile. |

## Failure modes

- Backend docs describe package structure but omit runtime behavior.
- A retry is added without timeout, backoff, max attempts and idempotency.
- Liveness and readiness endpoints are treated as the same thing.
- Logs expose secrets, tokens, private data or full payloads.
- A worker can process the same message twice but has no deduplication policy.
- A queue has no dead-letter, replay or poison-message procedure.
- A service boundary changes without owner review or ADR.
- A distributed transaction is implemented without compensation or recovery evidence.
- Microservices are chosen before module boundaries, deployment automation and observability are mature.
- Completion is claimed after code inspection without integration/runtime verification.

## Open questions for deeper research

- Should Product-Agent OS default to modular monolith guidance before microservice guidance?
- Which stack-specific backend templates should be generated first: Node.js, Python, Java, .NET, Go or framework-agnostic only?
- Should health check templates be platform-neutral or Kubernetes-first with alternatives?
- Which resilience library examples are mature enough for stack-specific snippets?
- How should the plugin detect risky retry/idempotency changes from code alone?
- Should SLO templates live under backend, delivery/operations or both?

## Sources

- [The Twelve-Factor App](https://www.12factor.net/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [CNCF Cloud Native Definition](https://github.com/cncf/toc/blob/main/DEFINITION.md)
- [Kubernetes liveness, readiness and startup probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Alistair Cockburn: Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
- [Martin Fowler: Microservices Guide](https://martinfowler.com/microservices/)
- [Microsoft Azure Architecture Center: Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Microsoft Azure Architecture Center: Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
- [Microsoft Azure Architecture Center: Queue-Based Load Leveling pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling)
- [Microsoft Azure Architecture Center: Health Endpoint Monitoring pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring)
- [Microsoft Azure Architecture Center: Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga)
- [Context7 research](../context7-research.md)
