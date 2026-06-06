# Methodologies for Large Projects

Source status: `official + verified methodology + tool-assisted`

This section is the operating map for running large projects through Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, control-plane artifacts, docs-as-code and eval loops.

The goal is not to collect an encyclopedia of methods. The goal is to show when a method is applicable, which artifacts are needed, which documentation tools to choose, how to verify the result and where to stop.

## Why frontend/backend/API are not enough

Technical areas answer where implementation happens. A large project must also answer:

- why the work is being built and which metric proves value;
- which requirements, business rules and domain terms must not be lost;
- which solution architecture keeps system boundaries coherent;
- which contracts, data rules, security/privacy constraints and release gates are mandatory;
- how agents work safely through staged artifacts, approvals and current evidence.

## Section map

| Section | Main question | Primary output |
| --- | --- | --- |
| [Business & Product](business-product.md) | Why are we building this and how do we measure value? | Product hypothesis, metric spec, guardrails |
| [Requirements & Domain](requirements-domain.md) | What must the system do and which domain rules matter? | Requirements, acceptance scenarios, domain model |
| [Solution Architecture](solution-architecture.md) | How are system parts connected and where are the boundaries? | Architecture overview, C4/arc42, ADR |
| [Frontend](frontend.md) | How should UI behavior be built and documented? | Component docs, Storybook states, visual/a11y checks |
| [Backend](backend.md) | How should business logic, services and reliability be managed? | Service overview, jobs, observability, rollback |
| [API & Integrations](api-integrations.md) | How do we preserve public contracts and compatibility? | OpenAPI/AsyncAPI, contract review, consumer map |
| [Database & Data](database-data.md) | How do we change data safely? | Database dictionary, migration plan, data quality gates |
| [LLM / AI / RAG](llm-ai-rag.md) | How do we verify AI behavior and reduce hallucination risk? | AI eval spec, baseline, grounding evidence |
| [Quality, Testing & Evals](quality-testing-evals.md) | How do we prove quality before completion claims? | Test/eval matrix, evidence format, gaps |
| [Security, Privacy & Compliance](security-privacy-compliance.md) | Which security/privacy gates block delivery? | Security risk review, ASVS/SSDF mapping |
| [Delivery, Release & Operations](delivery-release-operations.md) | How do we release and operate the system? | Release readiness, SLOs, runbooks, DORA metrics |
| [Codex / Agentic Workflow](codex-agentic-workflow.md) | How does Codex work in a large project without losing context? | Control-plane files, handoffs, automation candidates |

## Shared deep research template

Each section should answer the same questions:

1. `Purpose`: which large-project problem the section solves.
2. `Applicability`: when the section is required, optional or not applicable.
3. `Concepts`: which ideas an engineer or agent must understand.
4. `Development methodologies`: which methods to apply and where they become harmful.
5. `Documentation artifacts`: which documents, diagrams, contracts or templates are needed.
6. `Tooling`: which tools fit the stack, scale and ownership model.
7. `Verification`: which tests, evals, builds, checks or reviews provide evidence.
8. `Ownership`: who owns the artifact, who reviews it and who owns evidence.
9. `Risks`: security, privacy, cost, performance, migration, compliance and operational risk.
10. `Codex routing`: which skill, subagent or workflow starts and where the approval boundary is.
11. `Failure modes`: how the section can become bureaucracy, stale docs or false confidence.
12. `Promotion path`: when a manual workflow becomes a playbook, skill, plugin or automation.

## Application principle

For large projects, use lightweight maturity levels:

| Level | When it fits | Requirement |
| --- | --- | --- |
| `baseline` | MVP, one owner, low risk | Minimal requirements, plan, tests and runlog |
| `team` | Several engineers or subagents | Ownership, handoffs, architecture boundary and docs impact |
| `production` | Users, data and release process | Security/privacy review, release readiness and rollback |
| `regulated` | PII, payments, healthcare, finance or enterprise governance | Explicit approvals, audit evidence and source-backed policies |

## How to use this with Product-Agent OS

- `REQUIREMENTS.md` holds business, product, acceptance and source-of-truth constraints.
- `PLAN.md` holds architecture boundary, slices, exact files, rollback and docs impact.
- `TEST.md` holds deterministic checks, contract checks, runtime checks and accepted gaps.
- `EVALS.md` holds subjective, AI and domain quality gates.
- `RUNLOG.md` holds current evidence, decisions, failures and residual risks.
- `AGENTS.md` holds durable project rules.

## Sources and Context7

Primary sources belong in the [source registry](../sources/registry.md). Context7 is a retrieval layer for developer documentation, but official status is kept only when the underlying source is official. This section was cross-checked against the methodology research dossiers under [sources/methodology-research](../sources/methodology-research/api-integrations.md) and the local Product-Agent OS implementation.
