# Domain Modeling Template

Project: {project_name}

## Purpose

Use this template for complex backend, enterprise, workflow, or data-heavy changes where generic service boundaries are not enough.

## Applicability

- Gate: `domain_model_when_complex_domain`.
- Traceability gate: `bounded_context_architecture_boundary_trace`.
- Language traceability gate: `ubiquitous_language_traceability`.
- Required when the project or slice is complex backend, enterprise, workflow, data-heavy, multi-service, or multi-context.
- Not required for simple CRUD or simple MVP work unless the owner explicitly wants DDD.
- Every bounded context must map to an architecture boundary in `.codex/artifact-templates/architecture-overview.md`, or record an accepted gap.
- Every ubiquitous language term must trace to a requirement or source and at least one API/event/contract, UI label, code module, or owner; otherwise record an accepted gap.
- Accepted gap:
- Reason DDD is not applicable:
- Evidence owner:

## Bounded Contexts

| Bounded context | Boundary id | Architecture boundary | Business capability | Owner | Upstream dependencies | Downstream consumers |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Context-To-Boundary Traceability

Each row proves that domain terminology and rules have a concrete architecture boundary. Use this as the `context-to-boundary traceability` record before implementation planning.

| Bounded context | Architecture boundary id | Boundary responsibility | Source in architecture-overview.md | Accepted gap | Evidence owner |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Ubiquitous Language Traceability

Use this as the `ubiquitous_language_traceability` record. It prevents domain language from staying glossary-only: every term must have term-to-requirement traceability and a concrete downstream artifact, owner, or accepted gap.

| Bounded context | Term | Meaning inside this context | Requirement or source | API/event/contract | UI label | Code module or owner | Do not confuse with | Accepted gap | Evidence owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

## Domain Expert Review

- Domain expert reviewer:
- Terms reviewed:
- Terms with accepted gap:
- Follow-up owner:

## Aggregates And Invariants

| Aggregate | Root | Invariant | Transaction boundary | Failure mode |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Domain Events

| Event | Producer | Consumers | Payload source | Ordering or idempotency rule |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Context Map

- Partnership:
- Customer/supplier:
- Conformist:
- Anti-corruption layer:
- Shared kernel:

## Verification

- Domain examples:
- Acceptance tests:
- Contract tests:
- Migration or backfill checks:
