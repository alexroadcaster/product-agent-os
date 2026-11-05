---
title: "Архив — Track 9 Methodology Intelligence Design"
---

# Архив — Track 9 Methodology Intelligence Design {#track-9-methodology-intelligence-design}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `local product design + methodology research synthesis`

Sources: [Methodologies for Large Projects](../../methodologies/index.md), [Business & Product](../../methodologies/business-product.md), [Requirements & Domain](../../methodologies/requirements-domain.md), [Solution Architecture](../../methodologies/solution-architecture.md), [Frontend](../../methodologies/frontend.md), [Backend](../../methodologies/backend.md), [API & Integrations](../../methodologies/api-integrations.md), [Database & Data](../../methodologies/database-data.md), [LLM / AI / RAG](../../methodologies/llm-ai-rag.md), [Quality, Testing & Evals](../../methodologies/quality-testing-evals.md), [Security, Privacy & Compliance](../../methodologies/security-privacy-compliance.md), [Delivery, Release & Operations](../../methodologies/delivery-release-operations.md), [Codex / Agentic Workflow](../../methodologies/codex-agentic-workflow.md), [Product-Agent OS plugin docs](../../product-agent-os/index.md).

## Goal

Track 9 turns Product-Agent OS from a scenario workflow plugin into a methodology-aware product engineering system. When connected to a user project, it should first understand the workspace, classify project complexity and delivery maturity, build a project delivery map, then recommend the right methodologies, documentation artifacts, readiness gates, owners, evidence, approvals and next actions.

The product goal is to replace chaotic vibe-coding on real projects with a guided path toward product-ready software: clear intent, scoped architecture, useful artifacts, current evidence, reviewable risks and staged changes that are safe to show to users, teams or stakeholders.

## Core Product Principle

Track 9 must cover all aspects of development without forcing all methodology on every project.

The operating rule is:

```text
cover every methodology domain
force only what is clearly applicable
record gaps and assumptions honestly
stage artifacts only after approval
```

## Existing Foundation

Track 8 already provides scenario routing, conditional readiness statuses, evidence-before-completion, acceptance scenarios, conditional DDD, bounded-context traceability, ubiquitous language traceability, conditional FSD routing, metric hardening, docs tooling selection, standards trigger policy, transcript/session evals and detailed `methodology_applicability` packets.

Track 9 builds on that foundation instead of replacing it. Scenario routing still answers "what situation is this project or request in?" Methodology intelligence answers "which engineering disciplines, artifacts and evidence are proportionate for this project's complexity, risk and maturity?"

## High-Level Flow

Track 9 uses a two-step onboarding flow.

```text
User connects Product-Agent OS to workspace
    ↓
Read-only audit
    ↓
Complexity and maturity classification
    ↓
Delivery Map
    ↓
Methodology applicability analysis
    ↓
Human-readable audit report + machine-readable JSON
    ↓
User approval
    ↓
Staged artifacts and control-plane proposals
```

The first step is read-only. It produces recommendations and questions. The second step stages artifacts only after explicit approval.

## Classification Model

Track 9 uses two independent axes.

`maturity_level` describes the delivery and governance level:

| Level | Meaning |
| --- | --- |
| `baseline` | MVP, solo owner or low-risk internal work; minimum requirements, plan, checks and runlog. |
| `team` | Multiple engineers, subagents or workstreams; ownership, handoffs, architecture boundary and docs impact matter. |
| `production` | Real users, deployments, data, release process or operations; security, rollback, release readiness and runtime evidence matter. |
| `regulated` | PII, payments, healthcare, finance, minors, enterprise governance, legal/compliance or audit requirements. |

`complexity_profile` describes the system and change complexity:

| Profile | Meaning |
| --- | --- |
| `simple` | Small project or narrow change with few dependencies and low blast radius. |
| `standard` | Normal product or service with tests, docs, API/UI/data surfaces or repeatable delivery. |
| `complex` | Multiple subsystems, integrations, teams, domains, workflows, data stores or runtime environments. |
| `high_risk` | Security, privacy, money, production data, irreversible migration, public contract, AI behavior, release or operational risk. |

The classifier records:

- `observed_signals`: facts discovered in files and workspace structure;
- `intent_signals`: user request or prompt intent, never treated as proof by itself;
- `unknowns`: facts that cannot be proven from workspace state;
- `questions_for_owner`: questions that should be answered by the user or project owner;
- `provisional_assumptions`: conservative assumptions used to choose a safe next step;
- `confidence`: confidence for each classification and domain recommendation;
- `blocked_until_answered`: whether missing answers block staging or implementation;
- `safe_next_action`: what Product-Agent OS can do without overclaiming.

## Delivery Map

The read-only audit produces a Delivery Map rather than a passive repository summary.

The Delivery Map includes:

- surface map: stack, package managers, entrypoints, test commands, docs, CI, runtime manifests and generated folders;
- system map: domains, subsystems, UI/API/data/AI surfaces, data stores, external integrations, deploy/runtime surfaces and ownership gaps;
- lifecycle map: current Product-Agent OS lifecycle state, control-plane status, existing evidence and missing files;
- methodology map: applicable domains, missing gates, unverified artifacts, accepted gaps and approval-required actions;
- next-action map: prioritized actions that connect a reason, methodology, artifact, owner, evidence and approval boundary.

## Audit Outputs

The read-only audit produces two outputs:

1. `methodology-audit-report.md`
   Human-readable report for the user. It explains project classification, Delivery Map, methodology recommendations, questions, assumptions, risks and next actions.

2. `methodology-applicability.json`
   Machine-readable contract for plugin scripts, lifecycle skills, fixture evals and later staged artifact generation.

The JSON output must be stable enough for tests and fixture evals. Markdown is for humans and must not become the source parser for plugin behavior.

## Recommendation Model

Recommendations are prioritized actions, not a list of documents to generate.

Each recommendation records:

- priority: `P0_blocker`, `P1_high_risk`, `P2_recommended`, `P3_optional_maturity` or `not_applicable`;
- reason: why this matters for this project;
- methodology domain;
- readiness gate;
- recommended artifact;
- evidence required;
- evidence owner;
- approval boundary;
- accepted gap option;
- residual risk;
- safe next action.

This prevents document spam. An artifact is recommended only when it closes a gate, reduces a risk, supports ownership, records evidence or enables a concrete next action.

## Methodology Domains

Track 9 includes every methodology file under `docs/methodologies`.

| Slice | Source file | Product-Agent OS purpose |
| --- | --- | --- |
| `T9-D1` | `business-product.md` | Product hypothesis, value, opportunities, metrics, guardrails and measurement. |
| `T9-D2` | `requirements-domain.md` | Requirements quality, acceptance scenarios, business rules, domain model, traceability and change impact. |
| `T9-D3` | `solution-architecture.md` | Architecture boundaries, views, ADRs, quality attributes, tradeoffs, ownership and fitness checks. |
| `T9-D4` | `quality-testing-evals.md` | Risk-based tests, evals, current evidence, runtime/manual/visual evidence and CI quality gates. |
| `T9-D5` | `codex-agentic-workflow.md` | Control-plane maturity, model/reasoning policy, handoffs, subagents, MCP, hooks, skills, plugins and automation promotion. |
| `T9-D6` | `frontend.md` | UI behavior, component states, Storybook applicability, visual/a11y evidence, responsive checks, performance and FSD boundaries. |
| `T9-D7` | `backend.md` | Service boundaries, modular monolith vs microservices, runtime behavior, queues, observability, SLOs and rollback. |
| `T9-D8` | `api-integrations.md` | OpenAPI/AsyncAPI/GraphQL/gRPC contracts, consumers, compatibility, errors, generated clients and external writes. |
| `T9-D9` | `database-data.md` | Database inventory, schema source, migrations, transactions, data quality, classification and production access. |
| `T9-D10` | `llm-ai-rag.md` | AI behavior spec, eval baseline, prompts, models, tools, RAG sources, grounding, datasets, approvals and cost/latency. |
| `T9-D11` | `security-privacy-compliance.md` | Threat surface, ASVS/SSDF, authorization tests, secrets, privacy impact, supply chain, audit logging and compliance overlays. |
| `T9-D12` | `delivery-release-operations.md` | Release readiness, versioning, changelog, artifact manifest, rollout, rollback, CI/CD governance, runbooks and operations. |

The order is intentional: product intent, requirements, architecture, quality and Codex workflow come before technical domains. Security/privacy and delivery/operations remain cross-cutting overlays but still receive dedicated domain slices.

## Domain Slice Contract

Each domain slice follows the same implementation contract.

### Catalog Entries

Each domain adds machine-readable catalog entries:

- domain id;
- purpose;
- applicability triggers;
- non-applicability triggers;
- maturity impact;
- complexity impact;
- related Track 8 scenarios;
- related artifacts;
- readiness gates;
- eval fields;
- conflict and overlap notes.

### Discovery Signals

Each domain defines:

- file, folder, manifest and config signals;
- prompt intent hints;
- signals that only support `present_unverified`;
- unknowns that should become questionnaire entries;
- false-positive risks.

### Readiness Gates

All gates reuse the existing status vocabulary:

- `not_applicable`;
- `applicable_missing`;
- `present_unverified`;
- `present_verified`;
- `proposal_staged`;
- `explicit_gap_accepted`;
- `approval_required`.

Detection alone can only produce `present_unverified`. `present_verified` requires current command evidence, owner evidence, artifact evidence or a clearly recorded accepted gap.

### Artifact Templates

Each domain adds or extends artifact templates only when they are tied to a gate or recommendation. Templates must be synthetic, source-safe and secret-free.

Examples include product briefs, requirement traceability matrices, architecture review records, frontend state matrices, backend runtime behavior docs, API consumer maps, database migration plans, AI eval specs, security risk reviews and release readiness packets.

### Lifecycle Skill Updates

Each domain updates relevant lifecycle skills:

- `workspace-discovery-auditor` observes signals and unknowns;
- `requirements-author` captures product, requirement and domain evidence;
- `implementation-planner` blocks build work when applicable gates are missing;
- `agent-team-designer` maps ownership and handoff boundaries;
- `test-eval-designer` selects checks and evals;
- `risk-reviewer` reviews missing evidence, accepted gaps, conflicts and risky changes;
- `pr-release-operator` includes release, contract, security and operations impact;
- `learning-loop-maintainer` records lessons and domain decisions;
- `automation-promoter` refuses promotion without maturity evidence and rollback.

### Tests And Evals

Each domain slice must add:

- focused unit tests for catalog/discovery/gate behavior;
- fixture eval coverage;
- false-positive tests when the domain can be over-applied;
- docs sync;
- Product-Agent OS docs updates when user behavior changes;
- source registry updates when source-backed claims change.

## Adaptive Deep-Dive Loop

The Track 9 queue is a living backlog. Each methodology file is inspected before implementation and can expand into multiple sub-slices.

```text
T9-Dn-0: domain deep audit
    ↓
T9-Dn-1..N: implementation sub-slices
    ↓
T9-Dn-final: domain verification and docs sync
```

Each domain deep audit records:

- concepts already covered by Track 8;
- new concepts;
- duplicate or overlapping gates;
- new artifacts;
- existing artifacts that need extension;
- likely false positives;
- required tests and evals;
- open questions;
- items deferred to cross-domain synthesis.

The backlog may change when a deep audit finds hidden sub-tasks, cross-domain overlap, false positives, duplicate artifacts, insufficient tests or a changed product direction. Every change must be recorded in `RUNLOG.md` or a Track 9 status/backlog document with rationale.

## Cross-Domain Synthesis

After all 12 domains are integrated, Track 9 runs a synthesis slice.

The synthesis pass must:

- deduplicate gates;
- merge overlapping artifacts;
- identify conflicting recommendations;
- define priority rules;
- normalize naming and vocabulary;
- map mutually exclusive frameworks;
- add cross-domain false-positive fixtures;
- verify that recommendations stay proportionate;
- update docs and final Track 9 baseline.

Known overlap areas:

- metric hardening appears in product, quality and delivery;
- security review appears in backend, API, data, AI, delivery and compliance;
- architecture boundary appears in requirements, architecture, frontend, backend, API and data;
- evidence-before-completion appears everywhere;
- release readiness appears in delivery, security, docs, package/plugin and operations contexts;
- accepted gaps and residual risk appear in every methodology.

## Safety Rules

Track 9 follows these safety rules:

1. Read-only first.
   Workspace onboarding produces audit output only.

2. Recommendation before generation.
   Product-Agent OS explains why an artifact or methodology is applicable before staging it.

3. Explicit approval before staged artifacts.
   No target workspace writes happen without approval. Staged artifacts remain reviewable proposals.

4. Conditional methodology.
   DDD, FSD, security/compliance, release governance and other frameworks are conditional.

5. No false readiness.
   Observed files, directories or prompt intent do not prove readiness.

6. No document spam.
   Documents exist to close gates, reduce risk, record ownership or enable next action.

7. No secrets or private data.
   Reports, fixtures, templates, prompts, memory notes and examples must not contain secrets, private keys, tokens, customer data, raw private chats or absolute user-specific paths.

8. Evidence before completion.
   Ready, completed, fixed, works and release claims require current evidence or an explicit inspection-only/test-gap label.

## Verification Strategy

Every Track 9 implementation slice must run verification proportional to touched files.

For docs-only or design docs:

```powershell
python tools\check_docs.py
```

For plugin scripts, templates, fixtures or tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python plugins\product-agent-os\scripts\run_transcript_eval.py plugins\product-agent-os\assets\eval-fixtures\transcripts\product-agent-os-synthetic-sessions.json
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
```

For navigation, Mermaid, Markdown extensions or MkDocs-sensitive changes:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; $env:NO_MKDOCS_2_WARNING='1'; python -m mkdocs build --strict
```

## Definition Of Done For A Domain Slice

A domain slice is done when:

- its methodology file has been deeply audited;
- applicable concepts are represented in catalog, discovery, gates, templates, skills or evals;
- duplicates and overlaps are recorded for synthesis;
- false-positive risks are covered by tests or explicitly deferred;
- user-facing docs explain behavior where needed;
- current verification evidence is recorded;
- residual risks are explicit.

## Definition Of Done For Track 9

Track 9 is done when:

- all 12 methodology files complete the domain integration loop;
- the plugin has a unified methodology catalog;
- read-only audit produces `methodology-audit-report.md` and `methodology-applicability.json`;
- recommendations are prioritized and linked to artifacts, gates, owners, evidence and approvals;
- staged artifacts are generated only after approval;
- cross-domain synthesis resolves duplicates, conflicts and naming drift;
- regression fixtures cover high-risk false positives;
- Product-Agent OS docs explain Track 9 onboarding and methodology selection;
- full test, fixture eval, transcript eval, compatibility, docs and MkDocs baseline passes.

## Non-Goals

Track 9 does not:

- activate hooks, automations, GitHub Actions, external writes, package publishing or release actions without explicit approval;
- make every methodology mandatory for every project;
- replace human product, domain, security, legal or architecture ownership;
- claim semantic correctness from artifact presence alone;
- infer production, compliance, privacy or business risk from files without recording uncertainty;
- use Markdown reports as the parser for plugin behavior;
- store private customer data, raw private chat logs or secrets in generated artifacts.

## Initial Risks

- Scope risk: 12 domains create a large implementation surface. Mitigation: domain-by-domain slices and adaptive deep audits.
- False-positive risk: methodology signals can over-apply gates to simple projects. Mitigation: non-applicability triggers, false-positive fixtures and accepted gaps.
- Duplication risk: many domains share gates and artifacts. Mitigation: synthesis backlog and final cross-domain synthesis pass.
- User-experience risk: recommendations can become overwhelming. Mitigation: priority levels, safe next action and staged generation only after approval.
- Verification risk: deterministic tests can prove contract shape but not methodology quality. Mitigation: owner review fields, residual risks and future semantic evals.
- Stale-doc risk: methodology docs and plugin catalog can drift. Mitigation: docs sync checks and Track 9 status/backlog evidence.

## Open Design Decisions For Implementation Planning

These decisions are scoped for implementation planning, not unresolved design gaps:

- Whether `methodology_catalog` lives as JSON only or as Python data with generated JSON.
- Exact file paths for read-only audit outputs and staged artifact output.
- Whether each domain deep audit gets a dedicated status document or one combined Track 9 backlog.
- How much of the catalog is generated from `docs/methodologies` versus hand-authored in plugin assets.
- Which domain slice receives the first executable implementation after foundation.
