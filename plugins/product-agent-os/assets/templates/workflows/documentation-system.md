# Documentation System Workflow

Project: {project_name}
Profile: {profile_name}
Detected stack: {detected_stack_text}

## Purpose

Use this workflow when a project needs documentation that stays close to code, supports onboarding, and becomes a verification target instead of a stale notes folder.

## Documentation Layers

| Layer | Source of truth | Minimum artifact | Verification |
| --- | --- | --- | --- |
| Product docs | Requirements and release notes | README or docs overview | docs build, link check, owner review |
| Architecture docs | C4, arc42-style sections, ADR log | `docs/architecture/overview.md`, `docs/adr/` | diagram render, ADR review |
| API contracts | OpenAPI for HTTP, AsyncAPI for events | `openapi/`, `asyncapi/` | contract lint, generated docs build |
| UI component docs | Storybook stories and MDX | component stories, state matrix | Storybook build, accessibility or visual check |
| Code reference | language-native comments | TypeDoc, JSDoc, Sphinx, pydoc, Javadoc, XML docs | reference docs build |
| Database docs | migrations, comments, DBML, schema introspection | `db/README.md`, DBML or schema docs | migration validation, DB docs build |
| Release docs | changelog and release packet | changelog, release notes, PR body | version and release review |
| Governance proposals | CODEOWNERS status and GitHub Actions proposals | `governance-proposal.md` | owner approval, least privilege review |

## Docs-As-Code Rules

- Keep code-coupled documentation in the same repository or in a documented aggregator.
- Use Markdown, AsciiDoc, OpenAPI, AsyncAPI, DBML, or other text formats that can be reviewed in diff.
- Prefer machine-readable contracts over prose for public APIs, event payloads, schemas, and generated clients.
- Keep diagrams textual when possible through Mermaid, PlantUML, Structurizr DSL, or an equivalent checked-in format.
- Assign CODEOWNERS or explicit reviewers for `docs/**`, API contracts, database schema docs, and UI component docs.
- Build or lint documentation in CI where project tooling exists; otherwise record the missing check as a test gap.
- Use `docs_tooling_selector` and `docs-tooling-decision.md` before recommending a docs portal or governance tooling.
- Record `docs_as_code_impact` as `not_applicable`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted`, or `approval_required`.
- For docs-light or internal-only projects, prefer a lightweight path and record why heavier tooling was rejected.
- No forced install.
- No CI activation without approval.
- No CODEOWNERS activation without approval.
- No forced external activation.
- Hosted docs approval is required before external publishing, sharing, hosted builds, or Read the Docs style activation.
- DB introspection approval is required before SchemaSpy, live database access, or any credentials-sensitive database documentation command.

## Standards Trigger Policy

Use `standards_trigger_policy` when architecture, API, release, ownership, or CI governance changes are in scope.

| Trigger | Minimum artifact | Status rule |
| --- | --- | --- |
| Architecture boundary, API contract, storage, auth/security, irreversible migration, or automation activation | ADR trigger policy in `adr.md` | ADR/MADR, `not_applicable`, or accepted gap |
| Architecture documentation | C4 System Context, C4 Container, optional component/code only when useful, arc42 goals/constraints/quality attributes/risks | Lightweight for small projects, fuller model for larger systems |
| HTTP API | OpenAPI source of truth in `api-contract-review.md` | Swagger UI is optional tooling, not source of truth |
| Event, webhook, queue, or message contract | AsyncAPI channel, message, payload schema, producer, consumer, ordering, idempotency, compatibility check | Contract source or accepted gap |
| Public package, SDK, plugin, API, app, or docs release | SemVer impact and Keep a Changelog categories in `release-packet.md` | `major`, `minor`, `patch`, or `not_applicable` with reason |
| Ownership governance | CODEOWNERS status in `governance-proposal.md` | `present_verified`, `proposal_staged`, `approval_required`, or `not_applicable` |
| CI governance | GitHub Actions proposal in `governance-proposal.md` | workflow names, commands, permissions, triggers, owners, least privilege, no external activation without approval |

## Change Routing

| Changed area | Required documentation check |
| --- | --- |
| New user-facing feature | README or feature overview, acceptance examples, release note |
| Architecture boundary or dependency | architecture overview, ADR, C4 or equivalent diagram |
| HTTP endpoint | OpenAPI operation, schemas, auth, errors, examples |
| Event or queue payload | AsyncAPI channel, message, payload schema, producer/consumer roles |
| Reusable UI component | Storybook story, states, props, accessibility notes |
| Public function, class, SDK, or module | language-native doc comment and generated reference |
| Database migration | data dictionary, table/column comments, DBML or schema docs |
| AI/RAG behavior | eval cases, grounding notes, prompt/model boundary, source policy |
| CODEOWNERS or GitHub Actions governance | `governance-proposal.md`, least privilege permissions, approval boundary |

## Component Card Minimum

- Purpose:
- Use when:
- Do not use when:
- Props or inputs:
- Events or outputs:
- States: default, loading, empty, error, disabled, success, responsive, keyboard/focus.
- Accessibility:
- Linked API contract:
- Linked code:

## Service Overview Minimum

- Purpose and owner:
- Dependencies:
- Data stores:
- Public APIs or events:
- Background jobs:
- SLO, SLA, and quality attributes:
- Security and privacy notes:
- Operational runbook links:

## Database Dictionary Minimum

- Table or collection purpose:
- Owner:
- Primary key and foreign keys:
- Important fields and business meaning:
- PII or sensitive fields:
- Retention and deletion rule:
- Migration history:

## Outputs

- Documentation impact section in `PLAN.md`.
- Documentation checks in `TEST.md`.
- Documentation quality rubric in `EVALS.md` when quality is subjective.
- Documentation evidence and unresolved gaps in `RUNLOG.md`.
- `docs-tooling-decision.md` with selected tools, rejected tools, evidence owner, maintenance owner, commands, approval needs, accepted gaps, and residual risk.
- `governance-proposal.md` when CODEOWNERS status, GitHub Actions, least privilege, repository ownership, CI workflow permissions, or external activation needs a staged proposal.
- Candidate CODEOWNERS or CI additions staged only when explicitly requested.

## Stop Conditions

- A source-backed claim lacks a trusted source or source status.
- Documentation would expose secrets, private customer data, raw private chat logs, credentials, or unpublished roadmap.
- Public API, database, or user-facing behavior changed without an updated source-of-truth artifact or explicit documented gap.
- Docs publication, sharing, external write, or automation is requested without approval.
- CODEOWNERS, GitHub Actions, repository settings, branch protection, required checks, environments, secrets, publishing, or external activation is requested without approval.
