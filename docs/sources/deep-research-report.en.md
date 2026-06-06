# Project And Code Documentation For A New Engineering Team

Source status: `mixed source-backed draft`  
Status: incoming deep-research report. Claims are useful for Product-Agent OS design only after primary-source verification and stable source entries in `docs/sources/registry.md`.

## Executive Summary

Good documentation is not a folder of files. It is a working knowledge system for the product: what it does, why it is structured that way, how to use its interfaces, how to change code without breaking the system, and how to keep that knowledge current.

Technical documentation guidance converges on a few principles: documentation should be correct, current, understandable, relevant, maintainable, linkable and version-controlled. The more a team can automate generation and checks, the lower the risk of documentation decay.

For a new team, the practical approach is to split documentation into layers:

- architecture documentation explains system boundaries, component roles and decisions;
- frontend documentation explains UI components, states, accessibility and design-system boundaries;
- backend/API documentation explains runtime behavior, API contracts, errors, auth and operational behavior;
- database documentation explains tables, columns, relationships, migrations and data rules;
- release documentation explains what changed and how to roll back.

Architecture work benefits from ISO/IEC/IEEE 42010 concepts, C4, arc42 and ADR. C4 provides context, container, component and optional code views. arc42 provides a ready structure for architecture communication. ADRs preserve one important decision, its context and consequences.

## Assumptions And Default Approach

The original request did not specify backend language, frontend framework, repository shape, public API status, team size or whether public docs are required. The default recommended setup is therefore:

| Situation | Starting Point | Best Fit |
| --- | --- | --- |
| Small product or internal service | **MkDocs + Markdown + Mermaid + GitHub Pages-like hosting** | Simple setup, fast start and low infrastructure cost |
| JS/TS product with rich UI | **Docusaurus + Storybook + TypeDoc/JSDoc + OpenAPI** | Product docs close to frontend components and MDX |
| Python-heavy backend | **Sphinx + autodoc + Read the Docs or internal CI publishing** | Docstrings, generated API reference and cross-links |
| Multirepo or enterprise documentation | **Antora + AsciiDoc + ADR + C4/Structurizr** | Documentation assembled from multiple repos and versions |
| Database-heavy system | **DBML/dbdocs or SchemaSpy + migration tooling** | Frequently changing schema and a need for readable relation maps |

Repository-local Markdown is a good baseline. If the organization needs a single portal over several repositories, the portal should aggregate source-controlled docs rather than become a parallel source of truth.

## Documentation Taxonomy

| Documentation Type | Purpose | Audience | Update Trigger | Typical Formats And Tools |
| --- | --- | --- | --- | --- |
| Project README | Fast entry: what this is, how to run it, where to find more | New developers, reviewers, DevOps | Startup flow, structure or link changes | Root Markdown |
| Architecture overview | System boundaries, external dependencies, containers and constraints | Whole team, tech leads, architects, QA | Architecture, integration or NFR changes | arc42, C4, Mermaid, PlantUML, Structurizr |
| ADR | One meaningful decision and its consequences | Developers, architects, future maintainers | Architecturally significant decisions | Markdown ADR, MADR |
| UI component docs | Purpose, props, states, accessibility and examples | Frontend, QA, designers | Component or design-system changes | Storybook, MDX, JSDoc, TypeDoc |
| HTTP API contract | Resources, operations, schemas, auth and errors | Backend, frontend, integrators, QA | Every API change | OpenAPI, Swagger UI, Redoc/Redocly |
| Event/message contract | Channels, messages, payload and producer/consumer roles | Backend, integrations, platform team | Every event contract change | AsyncAPI |
| Code reference | Module/class/function interface and constraints | Developers, sometimes SDK consumers | Public interface changes | JSDoc, TypeDoc, Sphinx, pydoc, Javadoc, C# XML docs |
| Database docs | Table, column, relation, migration and constraint meaning | Backend, data/BI, DBA, analysts | Schema changes | DBML, dbdocs, SchemaSpy, SQL comments |
| Changelog | User-visible changes by version | Users, support, team | Every release | Keep a Changelog + SemVer |

## Architecture Documentation

Architecture documentation should answer three questions:

1. Who are the stakeholders?
2. What concerns do they have?
3. Which views of the system answer those concerns?

For a new team, keep the first version small:

- one overview page;
- one C4 System Context diagram;
- one C4 Container diagram;
- a list of integrations;
- an ADR index;
- a short page for quality attributes and risks.

Recommended workflow:

1. Create `docs/architecture/overview.md`.
2. State the business purpose, primary users and external systems.
3. Draw a System Context diagram.
4. Draw a Container diagram for frontend, backend services, queue, database, cache, file storage and communication channels.
5. Add three to five lines per container: responsibility, technology, inputs/outputs and constraints.
6. Create an ADR for hard-to-reverse decisions such as database choice, queue, API standard, auth model, monorepo/multirepo or migration strategy.
7. Add `quality-attributes.md` for performance, availability, security, observability, localization, accessibility and data requirements.
8. Require architecture docs updates when a PR changes boundaries, integrations or critical NFRs.

Minimal architecture page template:

```md
# Architecture Overview

## System Purpose
Short description of the business problem.

## Users And External Systems
- User A
- Operator B
- Payment provider
- Email provider

## Containers
| Container | Responsibility | Technology | Stores Data |
| --- | --- | --- | --- |
| Web app | UI and client logic | React/Vue/... | No |
| API service | Business logic | Node/Python/Java/... | No |
| Database | Persistent data | PostgreSQL/... | Yes |

## Key Constraints
- SLA
- Security or privacy constraints
- Performance constraints
- Deployment constraints

## Related ADRs
- ADR-0001 ...
```

## ADR Example

```md
# ADR-0003 Choose OpenAPI As The REST API Contract

## Context
Frontend, backend and QA need one machine-readable source for operations, schemas, auth and errors.

## Decision
Use OpenAPI as the source contract for HTTP API changes.

## Consequences

### Pros
- Enables generated docs and contract checks.
- Gives frontend and QA a stable reference.
- Makes breaking changes easier to identify.

### Cons
- Requires regular maintenance.
- Can drift from implementation if not checked.
```

## Frontend Documentation

Frontend documentation should explain components and user-visible states, not just list files. Storybook is a strong default when a team has reusable components or design-system work. MDX and Doc Blocks can add narrative where automatic docs are insufficient.

Minimum component card:

```md
# Button

## Purpose
Primary command trigger used in forms and toolbars.

## Use
- Primary action on a page or modal.
- Secondary action inside dense UI.

## Do Not Use
- As a navigation link when a link is semantically correct.

## Props
| Prop | Type | Meaning |
| --- | --- | --- |
| variant | primary/secondary/danger | Visual intent |
| disabled | boolean | Prevents interaction |

## States
- default
- hover/focus
- disabled
- loading

## Accessibility
Keyboard focus visible, accessible name required.

## Related Code
`src/shared/ui/button`
```

For product UI, docs should include route/page, user flow, component variants, empty/loading/error states, accessibility notes, responsive behavior and Storybook links when available.

## Backend And API Documentation

Backend docs should cover runtime behavior, not only code structure:

- service boundary and responsibility;
- dependencies and failure modes;
- API contract and error model;
- auth and permission model;
- configuration and secrets boundary;
- observability: logs, metrics, traces, health checks;
- rollback and recovery;
- operational runbook.

HTTP APIs should use OpenAPI when humans or machines consume them. Event-driven APIs should use or explicitly consider AsyncAPI. Consumer-driven contract tests such as Pact can complement schema contracts when consumer expectations matter.

Minimal API docs should include:

```md
# API Contract

Source contract: `openapi.yaml`

## Auth
...

## Error Model
...

## Compatibility Policy
...

## Verification
- Contract lint command
- Consumer/provider test command
```

## Database Documentation

Database docs should explain meaning, not only schema shape:

- table purpose;
- primary keys and foreign keys;
- important columns;
- business rules;
- indexes and query assumptions;
- migration history;
- data retention and privacy notes;
- backup/restore expectations.

Example:

```md
# orders

## Purpose
Stores customer purchase records.

## Keys And Relations
- `id`: primary key
- `customer_id`: references `customers.id`

## Important Fields
- `status`: draft, paid, cancelled, refunded
- `created_at`: order creation time

## Business Rules
- Paid orders cannot be deleted.
- Refunds require an audit record.

## Change History
- 2026-05-01: added refund status.
```

DBML/dbdocs and SchemaSpy can generate useful views, but generated database docs must not expose secrets, connection strings or private production data.

## Documentation Process

Documentation should move through the same control loop as code:

1. Identify the change type.
2. Determine affected docs.
3. Update source docs, not generated output first.
4. Run docs checks/builds.
5. Record evidence in TEST/RUNLOG.
6. Keep generated HTML as review output, not source of truth.

For Product-Agent OS, every workflow should name:

- inputs;
- outputs;
- owner;
- verification;
- risks;
- next artifact.

## Tooling Recommendations

| Need | Recommended Tooling |
| --- | --- |
| Small internal docs portal | MkDocs |
| Product docs with MDX/React | Docusaurus |
| Python reference docs | Sphinx + autodoc |
| UI component docs | Storybook |
| HTTP API contract | OpenAPI |
| Event/message contract | AsyncAPI |
| Database schema docs | DBML/dbdocs or SchemaSpy |
| Architecture diagrams | Mermaid for simple docs, Structurizr for C4-as-code, PlantUML for UML-heavy teams |
| Release notes | Keep a Changelog + SemVer |
| Prose/style lint | Vale when team style rules exist |
| Markdown structure lint | markdownlint or project-specific docs checks |

## Multi-Agent Documentation Workflow

For a multi-agent system, split ownership by artifact type:

| Role | Ownership | Output |
| --- | --- | --- |
| Product Manager | Requirements, user journey, metrics | REQUIREMENTS.md, metric spec |
| Architect | Boundaries, ADRs, diagrams | architecture overview, ADRs |
| Builder | Code and local docs updates | implementation diff |
| Tester | Tests/evals and evidence | TEST.md, EVALS.md, run output |
| Docs Maintainer | IA, source status, links, localization | docs pages, registry updates |
| Release Operator | Release notes and rollback | release packet, RUNLOG |

Each handoff should return sources used, assumptions, files touched, verification evidence, open risks and the recommended next role.

## Product-Agent OS Implications

Product-Agent OS should:

- prefer behavior-level documentation over tool hype;
- route docs tooling by project stack and maturity;
- keep external hosting, CI activation and DB introspection approval-bound;
- treat generated docs and dashboards as review surfaces, not source of truth;
- keep source-backed claims in `docs/sources/registry.md`;
- require `Source status:` on non-index docs pages;
- preserve official OpenAI terms such as Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, memory, sandbox, approvals, MCP and Agents SDK.

## Checklist For A New Team

1. Create README and architecture overview.
2. Add C4 context/container diagrams.
3. Start ADR index.
4. Define API contracts with OpenAPI/AsyncAPI when applicable.
5. Document core UI components and states.
6. Add database dictionary for persistent data.
7. Define docs build/check command.
8. Add ownership and review rules.
9. Keep generated output separate from source docs.
10. Record verification evidence after each meaningful docs slice.

## Source Families Used

- C4 model and arc42 for architecture views.
- ADR/MADR for decisions.
- OpenAPI and AsyncAPI for contracts.
- Storybook, TypeDoc, JSDoc, Sphinx, Javadoc and C# XML docs for component/code reference docs.
- DBML/dbdocs and SchemaSpy for database docs.
- MkDocs, Docusaurus, Antora and Read the Docs for docs portals.
- GitHub Actions, CODEOWNERS, Vale, markdownlint, Keep a Changelog and SemVer for process and governance.
