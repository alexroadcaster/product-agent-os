# Architecture Overview Template

Source status: `local methodology artifact`

Project: {project_name}

Use this artifact for `solution_architecture_scope_present`, `architecture_context_view_present`, `architecture_container_boundary_present`, `architecture_boundary_per_slice`, `runtime_deployment_topology_present`, `observability_architecture_present`, `domain_to_architecture_trace_present`, and `accepted_gap_recorded`.

## Purpose

- Business or user problem:
- Primary users:
- Architecture question:
- System owner:
- Architecture owner:
- Evidence owner:
- In scope:
- Out of scope:
- Non-goals:

## Standards Trigger Policy

- Gate: `standards_trigger_policy`.
- C4 applicability: small systems can use lightweight Mermaid context/container notes; larger or multi-service systems need C4 System Context and C4 Container views or an accepted gap.
- Component/code only when useful: add C4 Component or code view only when internals are risky, shared, or non-obvious.
- arc42 review: cover architecture goals, constraints, context, solution strategy, decisions, quality attributes, and risks when architecture changes are material.
- C4/arc42 only when applicable: do not force detailed diagrams for docs-light prototypes or simple single-surface work.

## Stakeholders And Concerns

| Stakeholder | Concern | Decision they need | Evidence owner |
| --- | --- | --- | --- |
|  |  |  |  |

## C4 Views

- C4 System Context: users, external systems, trust boundaries.
- C4 Container: UI, services, workers, storage, queues, integrations.
- C4 Component: only for containers whose internal structure is not obvious.
- Code view: only when it adds value beyond source navigation.
- Render check: record command, output, owner and `present_unverified | present_verified | explicit_gap_accepted` status.

## Responsibilities

| Boundary | Responsibility | Owner | Public contract | Data ownership | Trust boundary | Mapped bounded context |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

## Backend Boundary Overlay

Use this section with `backend-service-overview.md` when backend runtime or service ownership changes.

- Backend unit classification:
- Purpose:
- Owner:
- Inbound contracts:
- Outbound dependencies:
- Data ownership:
- Deployment/runtime shape:
- Modular monolith or microservice rationale:
- ADR or owner-review link:

## Domain Model Boundary Traceability

Use this section when a domain model exists. It keeps `context-to-boundary traceability` visible from architecture review, so every mapped bounded context has a matching architecture boundary and clear ownership.

| Architecture boundary id | Domain model context | Responsibility | Contract or module | Evidence owner |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Dependency Rules

- Allowed dependencies:
- Forbidden dependencies:
- Boundary responsibility:
- Dependency rule owner:
- Fitness function or check:

## Runtime Topology

| Runtime unit | Deployment target | Dependencies | Health signal | Rollback path |
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
- Cost:
- Reliability:

## Observability

- Logs:
- Metrics:
- Traces:
- Dashboards:
- Alerts:
- Owner:

## Risks

- Architecture risk:
- Migration risk:
- External dependency risk:
- Technical debt:
- Residual risk:

## Accepted Gap

- Gap:
- Owner:
- Reason:
- Scope:
- Review date:
- Downstream risk:
- Follow-up condition:

## Verification

- Diagram render:
- Contract checks:
- Runtime checks:
- Observability checks:
- ADR links:
- Architecture owner review:
- Rollback or no-rollback rationale:
- No secrets, credentials, private customer data, raw private chat logs, connection strings or unpublished roadmap details stored in this artifact:
