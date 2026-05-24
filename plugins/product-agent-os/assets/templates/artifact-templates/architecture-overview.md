# Architecture Overview Template

Project: {project_name}

## Purpose

- Business or user problem:
- Primary users:
- System owner:

## Standards Trigger Policy

- Gate: `standards_trigger_policy`.
- C4 applicability: small systems can use lightweight Mermaid context/container notes; larger or multi-service systems need C4 System Context and C4 Container views or an accepted gap.
- Component/code only when useful: add C4 Component or code view only when internals are risky, shared, or non-obvious.
- arc42 review: cover architecture goals, constraints, context, solution strategy, decisions, quality attributes, and risks when architecture changes are material.

## C4 Views

- C4 System Context: users, external systems, trust boundaries.
- C4 Container: UI, services, workers, storage, queues, integrations.
- C4 Component: only for containers whose internal structure is not obvious.
- Code view: only when it adds value beyond source navigation.

## Responsibilities

| Boundary | Responsibility | Owner | Public contract | Data ownership | Mapped bounded context |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

## Domain Model Boundary Traceability

Use this section when a domain model exists. It keeps `context-to-boundary traceability` visible from architecture review, so every mapped bounded context has a matching architecture boundary and clear ownership.

| Architecture boundary id | Domain model context | Responsibility | Contract or module | Evidence owner |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Quality Attributes

- Performance:
- Availability:
- Security:
- Privacy:
- Accessibility:
- Observability:
- Maintainability:

## Risks

- Architecture risk:
- Migration risk:
- External dependency risk:
- Technical debt:

## Verification

- Diagram render:
- Contract checks:
- Runtime checks:
- ADR links:
