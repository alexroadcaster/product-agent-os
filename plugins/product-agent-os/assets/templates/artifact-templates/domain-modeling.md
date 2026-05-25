# Domain Modeling Template

Source status: `local methodology artifact`

Project: {project_name}

## Purpose

Use this template for complex backend, enterprise, workflow, or data-heavy changes where generic service boundaries are not enough.

## Applicability

- Gate: `domain_model_when_complex_domain`.
- Traceability gate: `bounded_context_architecture_boundary_trace`.
- Language traceability gate: `ubiquitous_language_traceability`.
- Invariants and failure modes gate: `invariants_and_failure_modes_present`.
- Domain event contract gate: `domain_event_contracts_present`.
- Domain expert review gate: `domain_expert_review_present`.
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
- Domain owner:
- AI-generated claim status:
- Unresolved conflicts:
- Accepted gap:
- Downstream risk:
- Follow-up owner:
- Terms reviewed:
- Terms with accepted gap:
- Follow-up owner:

## Aggregates, Invariants And Failure Modes

| Aggregate | Root | State transition | Invariant | Invalid transition | Enforcement layer | Failure mode | Test/eval evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Domain Events

| Event | Meaning | Producer | Consumers | Schema link | Ordering/idempotency rule | Privacy classification |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

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

## Evidence

- Source:
- Owner review:
- Requirement IDs:
- Linked acceptance scenarios:
- Linked requirements-traceability-matrix.md:

## Accepted Gap

- Owner:
- Reason:
- Scope:
- Review date:
- Downstream risk:
- Follow-up condition:

## Residual Risk

- Risk:
- Mitigation:
