# Requirements & Domain Methodology Research

Source status: `official + verified methodology + local implementation evidence + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/requirements-domain.md](../../methodologies/requirements-domain.md)

Target Product-Agent OS behavior: convert business intent into testable behavior contracts, domain language, domain boundaries and traceable implementation evidence before agents or engineers start building behavior-changing slices.

## Scope

This dossier covers requirements engineering, business analysis, user stories, ATDD, BDD, Gherkin, Example Mapping, Domain-Driven Design, EventStorming, Domain Storytelling, bounded contexts, ubiquitous language, domain invariants, domain events, context maps and traceability into architecture, API, UI, database, tests, evals and release evidence.

It does not force formal DDD, Gherkin, EventStorming, BABOK or ISO processes onto every project. These practices are conditional: they become required when domain complexity, stakeholder risk, compliance, team count, service count, user-facing behavior or AI/agent ambiguity makes informal requirements unsafe.

## Supported facts

- Agile Alliance describes ATDD as a collaboration between customer, development and testing perspectives to write acceptance tests before implementing the corresponding functionality.
- Agile Alliance describes BDD as a refinement of TDD and ATDD that connects proposed user stories to business outcomes, works outside-in and describes behavior in a notation accessible to domain experts, testers and developers.
- Agile Alliance also warns that BDD is a conceptual approach and should not be reduced to a specific tool or programming language.
- Agile Alliance user-story guidance treats user stories as user-goal-oriented work items whose acceptance criteria should be expressible in terms usable for automated acceptance tests.
- Cucumber Gherkin reference defines executable specification structure with `Feature`, `Rule`, `Scenario`/`Example`, `Given`, `When`, `Then`, `And`, `But`, `Background`, `Scenario Outline` and `Examples`.
- Cucumber guidance says `Given` describes initial context, `When` describes an event or action and `Then` describes an expected observable outcome.
- Cucumber guidance says implementation details should be hidden in step definitions and expected outcomes should be observable to the user or external system instead of deeply buried implementation state.
- Cucumber Example Mapping uses story, rules, examples and questions to clarify acceptance criteria before a story is pulled into development.
- ISO/IEC/IEEE 29148:2018 is a requirements engineering standard for systems and software life-cycle processes and can be used regardless of project scope, product, methodology, size or complexity.
- IEEE's public description of ISO/IEC/IEEE 29148 says it covers requirements engineering processes and products, defines the construct of a good requirement, gives attributes and characteristics of requirements and discusses iterative requirements processes.
- IIBA describes BABOK as a globally recognized standard for business analysis practice, covering skills, deliverables and techniques across six knowledge areas.
- Martin Fowler describes Domain-Driven Design as software development centered on a domain model with rich understanding of domain processes and rules, especially suited to complex domains.
- Fowler describes Bounded Context as a central DDD strategic design pattern that divides large models and teams into explicit model boundaries with explicit relationships.
- Fowler describes Ubiquitous Language as a rigorous shared language between developers and users, based on the domain model and evolved as understanding grows.
- Domain Language is Eric Evans' DDD site and primary background source for DDD resources and terminology.
- EventStorming describes itself as a collaborative workshop format for exploring complex business domains, cross-discipline conversations, service dynamics and event-driven software behavior.
- Domain Storytelling positions domain stories as a way to learn domain language, reach shared understanding and derive requirements or backlog items from domain stories.
- The C4 model defines architecture diagrams through hierarchical abstractions: software systems, containers, components and code, with system context, container, component and code diagrams plus supporting views.
- OpenAPI 3.2.0 defines API operation and reusable component structures that can become downstream traceability artifacts for requirements, acceptance scenarios, domain terms and public contracts.
- The local Product-Agent OS implementation already includes `acceptance-scenarios.md`, `domain-modeling.md`, `domain_model_when_complex_domain`, `bounded_context_architecture_boundary_trace` and `ubiquitous_language_traceability` gates.

## Assumptions

- For Product-Agent OS, a behavior-changing slice should not start from folder structure or implementation tasks. It should start from requirement, owner, acceptance scenario, non-goals and observable evidence.
- User stories are useful planning artifacts, but a story title alone is not a sufficient requirement. It needs acceptance criteria, business rules, examples, edge cases and open questions.
- Gherkin is one acceptable scenario format, but not the only acceptable format. Product-Agent OS should accept equivalent behavior formats when they preserve actor, context, trigger, observable outcome and evidence mapping.
- DDD should be conditional. It is required for complex domains, workflow-heavy systems, multi-service boundaries, enterprise vocabulary conflicts, data-heavy workflows and AI/agent systems that make domain decisions. It should not be forced onto trivial CRUD unless a human owner asks for it.
- Ubiquitous language should be more than a glossary. A project term should trace to requirement, API/event/schema, UI label, code module or domain owner.
- A bounded context should map to an architecture boundary or carry an accepted gap. Otherwise it remains a workshop artifact rather than an implementation control.
- Domain expert review is required when requirements contain business rules, policy, financial/legal/compliance meaning or AI-generated domain claims.
- Accepted gaps are valid only when explicit: owner, reason, scope, expiry/review date and downstream risk must be recorded.

## Unsupported claims not adopted

- "BDD replaces testing." BDD clarifies behavior and can generate executable scenarios, but it does not replace unit, integration, contract, exploratory, performance, security or eval checks.
- "Gherkin is mandatory for BDD." BDD is a conceptual practice; Gherkin is one useful executable notation.
- "A user story template is a complete requirement." A template without acceptance criteria, examples, business rules, constraints and evidence owner is incomplete.
- "A glossary is ubiquitous language." Ubiquitous language must be used in conversations, models, code/API/UI and owner review.
- "DDD is the right default for every project." DDD has coordination and modeling cost and is most useful for complex domains.
- "Bounded Context equals folder or microservice." A bounded context is a model boundary; implementation boundaries should be traced, not assumed.
- "OpenAPI is the requirements source of truth." OpenAPI is a contract artifact. It can trace requirements, but it does not replace business intent and acceptance scenarios.
- "AI can infer domain rules from chat memory." Domain rules need source, owner confirmation or explicit accepted-gap status.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| Requirements engineering | Any non-trivial product/system work | Capture need, stakeholder, scope, constraints, quality attributes, acceptance criteria, traceability and change impact. |
| BABOK-style business analysis | Business process, stakeholder, policy or enterprise value ambiguity | Elicit needs, analyze options, define solution value, manage stakeholder collaboration and document deliverables. |
| User stories and story slicing | Agile/product backlog work | Keep user-goal language, split by value/risk, add acceptance criteria, examples, non-goals and owner. |
| ATDD | Behavior must be agreed before implementation | Customer/product, development and testing perspectives define acceptance tests/scenarios first. |
| BDD / Specification by Example | Domain behavior and examples must be shared | Outside-in behavior language, rules and examples become executable or reviewable specifications. |
| Gherkin | Scenarios benefit from executable plain-text structure | Use `Given/When/Then` or equivalent behavior format, hide implementation details and assert observable outcomes. |
| Example Mapping | User story acceptance criteria are unclear | Map story -> rules -> examples -> questions before pulling work into development. |
| EventStorming | Complex process, event flow or cross-silo understanding is missing | Explore domain events, commands, policies, actors, external systems, hotspots and candidate boundaries. |
| Domain Storytelling | Actors/process language is unclear | Use visual domain stories to learn language, shared understanding and candidate requirements/backlog items. |
| Conditional DDD | Complex domain, workflow, enterprise, data-heavy, multi-service or multi-context work | Model entities/value objects/aggregates/services/events/invariants and evolve model with domain experts. |
| Bounded Context / context mapping | Terms or rules differ across teams/services | Define model boundaries, relationships, integration language and architecture trace. |
| Ubiquitous language traceability | Domain terms drive implementation/API/UI/tests | Map term -> source requirement -> code/API/event/schema/UI label -> owner/review. |
| Invariant and business-rule modeling | Incorrect state transitions are costly | Record invariant, allowed transition, enforcement layer, test/eval evidence and exception behavior. |
| Domain event modeling | Workflow/event-driven behavior exists | Record event name, meaning, producer, consumer, schema, ordering/idempotency assumptions and privacy rules. |
| C4 boundary mapping | Requirements/domain concepts need architecture translation | Map actors, systems, containers, components and code-level ownership only as far as useful. |
| Requirements traceability matrix | Regulated, risky, multi-team or long-lived work | Trace requirement -> scenario -> implementation -> test/eval -> evidence owner -> release note. |
| Change impact analysis | Requirement/domain rule changes after implementation starts | Identify affected tests, API, database, UI, docs, evals, rollout and migration/rollback needs. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| `REQUIREMENTS.md` | Users, goals, non-goals, constraints, business rules, acceptance criteria and source constraints. | Product-Agent OS control plane, ISO 29148/BABOK-inspired structure |
| Requirement registry | Stable requirement IDs, status, owner, source and linked artifacts. | Markdown table, issue tracker, requirements tool |
| Stakeholder/owner map | Business/domain owner, reviewer, decision authority and escalation path. | BABOK-style stakeholder collaboration |
| User-story map/backlog | Value slices, journey order, MVP boundary and deferred stories. | User Story Mapping, issue tracker |
| `acceptance-scenarios.md` | Requirement -> scenario -> check -> evidence owner before behavior changes. | ATDD/BDD/Gherkin or equivalent behavior format |
| Example map | Story, rules, concrete examples, open questions and out-of-scope slices. | Cucumber Example Mapping |
| Business rules catalog | Rule, rationale/source, owner, enforcement layer, exceptions and tests. | Decision table, requirements docs |
| Non-goals and constraints | Explicit boundaries that prevent silent scope growth. | `REQUIREMENTS.md`, ADR |
| `domain-modeling.md` | Bounded contexts, ubiquitous terms, invariants, aggregates/events and domain review. | Product-Agent OS template, DDD |
| Ubiquitous language map | Term -> definition -> source -> artifact links -> owner -> review status. | DDD glossary plus traceability |
| Context map | Bounded contexts, model relationships, upstream/downstream dependencies and integration language. | DDD strategic design, Mermaid/C4 |
| Event catalog | Domain events, producers, consumers, schema links, ordering/idempotency and privacy flags. | AsyncAPI, event docs |
| Invariant catalog | State rules, validation/enforcement location, failure behavior and test evidence. | Domain model/test docs |
| C4 system/context/container diagrams | Translate domain boundaries into architecture ownership and dependencies. | C4 model, Structurizr/Mermaid |
| API contract trace | Requirement/domain term -> OpenAPI operation/schema/error/security/deprecation. | OpenAPI 3.2.0 |
| UI language trace | Domain term -> screen/label/copy/error message/accessibility name. | UI flow spec, Storybook |
| Data dictionary/schema trace | Domain term -> table/field/event/schema/index/privacy classification. | Database docs/catalog |
| Decision log / ADR | Boundary, term, rule or requirement decisions with consequences. | MADR/ADR |
| Domain review record | Human owner review, unresolved conflicts, accepted gaps and expiry. | Review checklist/RUNLOG |
| Change impact record | Requirement change impact across code, tests, API, DB, UI, docs, evals and release. | RUNLOG/PLAN |

## Project application instructions

1. Classify the work before implementation: new requirement, behavior change, bug, refactor with behavior risk, domain model change, API contract change, data model change, UI copy/flow change or AI/agent behavior change.
2. Start with business intent: user/stakeholder, problem, expected outcome, value signal, scope and non-goals.
3. Assign a requirement ID and owner for any behavior-changing work. Owner can be product, domain expert, technical owner or explicitly marked `accepted gap`.
4. Capture constraints early: compliance, privacy, security, operational, performance, platform, accessibility, data retention, localization, cost and rollout.
5. Write acceptance scenarios before implementation. Minimum trace is `requirement -> scenario -> check -> evidence owner`.
6. Prefer concrete examples over abstract prose. Each rule should have at least one happy path and at least one edge/negative path when risk justifies it.
7. Use Gherkin only when it improves collaboration or executable specification. Equivalent behavior tables are acceptable when easier for the team.
8. Keep scenarios declarative. Hide UI selectors, database internals, implementation function names and test harness setup outside the behavior statement.
9. For each user story, record acceptance criteria, business rules, open questions, deferred slices and non-goals. A story title alone is not ready.
10. Use Example Mapping when a story is large, unclear or disputed. Stop when rules, examples and questions are explicit enough for development or when open questions block the slice.
11. Use EventStorming or Domain Storytelling when the team lacks shared process/language understanding, especially before event-driven, workflow-heavy or cross-silo changes.
12. Apply DDD only when domain complexity justifies it. For simple CRUD/MVP, record `domain_model_not_required` with owner and reason instead of creating ceremonial models.
13. When DDD applies, define bounded contexts, key aggregates/entities/value objects, domain services, invariants, domain events and integration relationships.
14. Every bounded context must map to an architecture boundary, team/agent ownership boundary or explicit accepted gap.
15. Build ubiquitous language as traceability, not a static glossary. Map important terms to requirement, API/event/schema, UI label, code module/test and owner.
16. Record unresolved term conflicts as decisions or open questions. Do not let one term silently mean different things across API, UI, code and data.
17. Trace domain events to contracts. If an event crosses a boundary, document meaning, producer, consumers, schema, idempotency/ordering assumptions and privacy classification.
18. Trace requirements downstream before completion: tests/evals, API contract, database changes, UI states/copy, documentation and release/rollback notes.
19. When a requirement changes after planning, run change impact review and update affected scenarios, contracts, data model, UI states, tests/evals, docs and rollout plan.
20. Require domain expert or owner review for business rules, compliance-sensitive claims, financial/legal meaning, AI-generated domain interpretations and accepted gaps.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `docs/requirements/`, `docs/domain/`, `docs/architecture/`, `features/`, `specs/`, `use-cases/`, `domain/`, `contexts/`, `events/`, `contracts/`
- Files: `REQUIREMENTS.md`, `acceptance-scenarios.md`, `domain-modeling.md`, `architecture-overview.md`, `business-rules.md`, `context-map.md`, `glossary.md`, `ubiquitous-language.md`, `event-catalog.md`, `openapi.yaml`, `asyncapi.yaml`, `*.feature`, `ADR*.md`
- Terms: requirement, acceptance criteria, acceptance scenario, Given/When/Then, Gherkin, BDD, ATDD, Example Mapping, user story, domain model, DDD, bounded context, ubiquitous language, aggregate, entity, value object, invariant, domain event, context map, business rule, stakeholder, non-goal, open question, accepted gap
- Risk signals: complex domain, multi-service, workflow, policy, compliance, financial, legal, privacy, AI-generated business logic, event-driven architecture, shared vocabulary conflict, data model change, public API change, multi-team ownership, release migration

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `requirements_scope_present` | Any non-trivial product/system work | Goal, user/stakeholder, scope or non-goals are missing. |
| `requirements_owner_present` | Behavior-changing work | No product/domain/technical owner or accepted-gap owner is named. |
| `requirement_ids_present` | Multi-slice, regulated or long-lived work | Requirements cannot be referenced from tests, contracts, docs or release evidence. |
| `acceptance_scenarios_when_behavior_changes` | Any behavior change | Scenario, observable outcome, check or evidence owner is missing. |
| `requirements_traceability_present` | Behavior crosses code/API/UI/data/tests | No `requirement -> scenario -> implementation -> check -> evidence owner` chain. |
| `business_rules_present` | Domain policy or process rule exists | Rule, source, owner, exception behavior or enforcement layer is missing. |
| `non_goals_constraints_present` | Ambiguous feature or stakeholder scope | Non-goals, constraints or excluded behavior are not explicit. |
| `open_questions_recorded` | Requirement uncertainty exists | Questions are hidden in chat or inferred instead of captured with owner/next action. |
| `example_mapping_when_unclear_story` | Story is unclear, large or disputed | Rules, examples, questions and deferred slices are not explicit. |
| `domain_discovery_workshop_when_complex_process` | Complex workflow/cross-silo process | Event/process/story discovery evidence or accepted gap is missing. |
| `domain_model_when_complex_domain` | Complex backend/workflow/enterprise/data-heavy/multi-service/multi-context work | Domain model, context map or accepted gap is missing. |
| `bounded_context_architecture_boundary_trace` | Bounded context or DDD term appears | Context has no architecture/team/API/data boundary or accepted gap. |
| `ubiquitous_language_traceability` | Domain terms drive behavior/API/UI/data | Important terms lack source, artifact links, owner or review status. |
| `invariants_and_failure_modes_present` | Domain state transitions matter | Invariants, invalid transitions, enforcement layer or tests are missing. |
| `domain_event_contracts_present` | Domain events cross boundaries | Meaning, schema, producer/consumer, idempotency/ordering or privacy notes are missing. |
| `api_ui_data_traceability_present` | Requirement touches API, UI or database | Contract/schema/screen/state mapping is missing. |
| `domain_expert_review_present` | Business-critical, compliance, finance/legal or AI-generated domain claim | Human owner review or explicit risk acceptance is missing. |
| `requirement_change_impact_review_present` | Requirement/domain rule changes after planning | Affected tests, API, DB, UI, docs, evals, rollout or rollback are not reviewed. |
| `accepted_gap_recorded` | Methodology gate is intentionally skipped | Owner, reason, scope, review date and risk are missing. |
| `requirements_evidence_before_implementation` | Agent/engineer starts implementation | Requirements/scenarios/domain gates are absent and no accepted gap exists. |

### Candidate templates

- `REQUIREMENTS.md`
- `acceptance-scenarios.md`
- `domain-modeling.md`
- `business-rules.md`
- `context-map.md`
- `ubiquitous-language.md`
- `event-catalog.md`
- `domain-review-record.md`
- `requirements-traceability-matrix.md`
- `requirement-change-impact.md`

### Candidate eval fields

- `requirements_scope_present`
- `requirements_owner_present`
- `acceptance_scenarios_when_behavior_changes`
- `requirements_traceability_present`
- `business_rules_present`
- `non_goals_constraints_present`
- `domain_model_when_complex_domain`
- `bounded_context_architecture_boundary_trace`
- `ubiquitous_language_traceability`
- `domain_expert_review_present`
- `accepted_gap_recorded`
- `requirement_change_impact_review_present`

## Типовые сбои

- Implementation starts from file/folder structure without confirmed business behavior.
- A user story title is treated as complete requirements.
- Критерии приемки describe implementation tasks instead of observable outcomes.
- Gherkin files duplicate test code and become unreadable to domain experts.
- Example Mapping creates questions but no owner or next action.
- DDD is forced on simple CRUD and slows delivery without reducing risk.
- DDD is skipped for complex workflows because no one wants to own the model.
- Bounded contexts are named but do not map to architecture, teams, APIs or data ownership.
- Glossary terms are written once but code, API, UI and documentation drift into different vocabulary.
- Domain events are named as technical messages with no business meaning, producer/consumer contract or privacy classification.
- AI-generated domain assumptions are accepted without source or domain owner review.
- Requirement changes do not update tests, contracts, data model, UI, docs, evals or release notes.

## Open questions for future research

- Should Product-Agent OS ship a generic `requirements-traceability-matrix.md` template or derive traceability from `REQUIREMENTS.md`, `TEST.md`, `EVALS.md` and contract docs?
- Should `domain_expert_review_present` be a hard gate only for complex/risky domains, or a warning for all behavior-changing work?
- Should EventStorming and Domain Storytelling become separate optional artifact templates or remain discovery guidance inside `domain-modeling.md`?
- How should requirements-domain gates integrate with AI/RAG eval datasets where acceptance criteria are probabilistic or judge-based?

## Sources

- [Agile Alliance: Acceptance Test Driven Development](https://agilealliance.org/glossary/atdd/)
- [Agile Alliance: Behavior Driven Development](https://agilealliance.org/glossary/bdd/)
- [Agile Alliance: User Stories](https://agilealliance.org/glossary/user-stories/)
- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/)
- [Cucumber Example Mapping](https://cucumber.io/docs/bdd/example-mapping/)
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html)
- [IEEE/ISO/IEC 29148-2018](https://standards.ieee.org/ieee/29148/6937/)
- [IIBA BABOK](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/)
- [Martin Fowler: Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Martin Fowler: Bounded Context](https://martinfowler.com/bliki/BoundedContext.html)
- [Martin Fowler: Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html)
- [Domain Language](https://www.domainlanguage.com/)
- [EventStorming](https://www.eventstorming.com/)
- [Domain Storytelling: Requirements](https://domainstorytelling.org/requirements)
- [C4 model](https://c4model.com/)
- [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- [Context7 research](../context7-research.md)
