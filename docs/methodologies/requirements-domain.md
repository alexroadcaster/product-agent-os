# Requirements & Domain

Source status: `official + verified methodology + local implementation evidence + tool-assisted + experiment`

Источники: [Agile Alliance ATDD](https://agilealliance.org/glossary/atdd/), [Agile Alliance BDD](https://agilealliance.org/glossary/bdd/), [Agile Alliance User Stories](https://agilealliance.org/glossary/user-stories/), [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/reference/), [Cucumber Example Mapping](https://cucumber.io/docs/bdd/example-mapping/), [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html), [IEEE 29148 overview](https://standards.ieee.org/ieee/29148/6937/), [IIBA BABOK](https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/), [Martin Fowler: Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html), [Martin Fowler: Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), [Martin Fowler: Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), [Domain Language](https://www.domainlanguage.com/), [EventStorming](https://www.eventstorming.com/), [Domain Storytelling](https://domainstorytelling.org/requirements), [C4 model](https://c4model.com/), [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/requirements-domain.md).

## Deep research цель

Requirements & Domain слой переводит business intent в проверяемые behavior contracts, domain language, domain boundaries и downstream evidence до того, как engineer, agent или subagent начинает менять поведение системы.

Для большого проекта это защита от silent scope drift: разные teams, services, agents, API, UI, database и tests должны одинаково понимать пользователей, термины, business rules, boundaries, acceptance criteria и owner review.

## Главный принцип

Не начинайте с folder structure, фреймворка или реализации. Начинайте с `requirement -> scenario -> check -> evidence owner`, а затем уже трассируйте это в architecture, API, UI, database, tests, evals, docs и release notes.

## Поддержанные факты

- ATDD and BDD support writing acceptance behavior before implementation and using shared language between product, development and testing.
- User stories are useful work items, but story title alone is not a complete requirement without acceptance criteria, examples, business rules and non-goals.
- Gherkin gives executable specification syntax, but BDD is a conceptual practice and can use equivalent behavior tables.
- ISO/IEC/IEEE 29148 and IEEE descriptions support requirements engineering attributes, traceability and iterative requirements processes.
- BABOK is a recognized business analysis reference for stakeholder collaboration, elicitation and solution value.
- Domain-Driven Design, Bounded Context and Ubiquitous Language are useful when domain complexity, workflow risk or vocabulary conflicts make informal requirements unsafe.
- EventStorming and Domain Storytelling support domain discovery through events, actors, policies, hotspots and shared process language.
- C4 and OpenAPI provide downstream traceability surfaces from domain boundaries and requirements to architecture and API contracts.

## Assumptions

- Behavior-changing work should not start from folder structure or implementation tasks.
- Gherkin is optional; equivalent behavior formats are valid when they preserve actor, context, trigger, observable outcome and evidence mapping.
- DDD is conditional: required for complex domains and risky workflow-heavy systems, but not forced onto trivial CRUD.
- Ubiquitous language must trace into requirements, API/event/schema, UI labels, code/tests and owner review.
- Accepted gaps are valid only with owner, reason, scope, review date and downstream risk.
- AI-generated domain claims require source, owner confirmation or explicit accepted-gap status.

## Инструкции применения на проекте

1. Классифицируйте работу: new requirement, behavior change, bug with behavior risk, domain model change, API contract change, data model change, UI flow/copy change или AI/agent behavior change.
2. Зафиксируйте business intent: пользователь/стейкхолдер, проблема, ожидаемый outcome, value signal, scope и non-goals.
3. Дайте requirement stable ID и owner. Owner может быть product, domain expert, technical owner или explicit accepted gap.
4. Запишите constraints: compliance, privacy, security, operational, performance, platform, accessibility, data retention, localization, cost, rollout.
5. До implementation напишите acceptance scenarios. Минимальный trace: `requirement -> scenario -> check -> evidence owner`.
6. Используйте конкретные examples, а не абстрактное описание. Для важного business rule нужен happy path и хотя бы один edge/negative path.
7. Gherkin полезен, когда сценарии должны быть executable или понятны domain experts. Equivalent behavior table допустим, если сохраняет actor, context, trigger, observable outcome и evidence.
8. Сценарии должны быть declarative: без UI selectors, database internals, function names и test harness деталей.
9. User story title не считается requirements. Story готова только с acceptance criteria, business rules, examples, open questions, deferred slices и non-goals.
10. Если story спорная, крупная или размытая, используйте Example Mapping: story -> rules -> examples -> questions.
11. Для сложных процессов используйте EventStorming или Domain Storytelling, чтобы достать domain events, actors, commands, policies, hotspots и candidate boundaries.
12. DDD включайте условно: complex domain, workflow-heavy, enterprise, data-heavy, multi-service, multi-context или AI/agent domain decision work.
13. Для simple CRUD/MVP допустим accepted gap: `domain_model_not_required`, owner, reason, scope и review date.
14. Если DDD включен, фиксируйте bounded contexts, key aggregates/entities/value objects, domain services, invariants, domain events и integration relationships.
15. Каждый bounded context должен мапиться в architecture/team/API/data boundary или иметь explicit accepted gap.
16. Ubiquitous language не равен glossary. Термин должен трассироваться к requirement, API/event/schema, UI label, code/test и owner.
17. Unresolved domain conflicts храните как open decisions/questions, а не как скрытые assumptions.
18. Domain event, который пересекает boundary, должен иметь meaning, producer, consumers, schema link, ordering/idempotency assumptions и privacy classification.
19. При изменении requirement после planning запускайте change impact review: tests/evals, API, DB, UI, docs, rollout, rollback.
20. Для business-critical, compliance, finance/legal или AI-generated domain claims нужен domain expert / owner review.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| Requirements engineering | Любая нетривиальная product/system работа | Need, stakeholder, scope, constraints, quality attributes, acceptance criteria, traceability, change impact |
| BABOK-style business analysis | Есть stakeholder/process/value ambiguity | Elicitation, stakeholder collaboration, solution value, deliverables, open questions |
| User stories and story slicing | Agile/product backlog | User-goal language, value/risk slicing, acceptance criteria, examples, non-goals |
| ATDD | Behavior должен быть согласован до реализации | Product/customer + development + testing perspectives пишут acceptance scenarios/tests first |
| BDD / Specification by Example | Нужен общий behavior language | Outside-in examples, business rules, observable outcomes, executable/reviewable specification |
| Gherkin | Сценарии нужно сделать executable/plain-text | `Given/When/Then` или equivalent format без implementation details |
| Example Mapping | Story unclear/large/disputed | Story -> rules -> examples -> questions before development |
| EventStorming | Сложный process/event flow/cross-silo domain | Domain events, commands, policies, actors, external systems, hotspots, candidate boundaries |
| Domain Storytelling | Непонятны actors/process language | Visual domain stories, shared language, candidate requirements/backlog items |
| Conditional DDD | Complex domain/workflow/enterprise/data/multi-service | Domain model, contexts, aggregates, invariants, events, expert review |
| Bounded Context / context mapping | Термины/rules отличаются между teams/services | Context map, integration language, architecture boundary trace |
| Ubiquitous language traceability | Domain terms влияют на implementation/API/UI/data | Term -> requirement -> API/event/schema/UI/code/test -> owner |
| Invariant modeling | Ошибочные state transitions дорого стоят | Invariant, enforcement layer, failure behavior, test/eval evidence |
| Domain event modeling | Есть event-driven behavior | Event meaning, producer/consumer, schema, idempotency/ordering, privacy |
| C4 boundary mapping | Domain надо перевести в architecture | System/context/container/component boundaries only as far as useful |
| Requirements traceability matrix | Regulated/risky/multi-team/long-lived work | Requirement -> scenario -> implementation -> test/eval -> evidence owner |
| Change impact analysis | Requirement/domain rule меняется после planning | Affected API, DB, UI, tests, docs, evals, rollout, rollback |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Зачем нужен | Практический формат |
| --- | --- | --- |
| `REQUIREMENTS.md` | Users, goals, non-goals, constraints, acceptance criteria, source constraints | Product-Agent OS control plane |
| Requirement registry | Stable IDs, status, owner, source, linked artifacts | Markdown table / tracker |
| Stakeholder/owner map | Кто подтверждает domain meaning и business rules | BABOK-style stakeholder map |
| User-story map/backlog | Value slices, MVP boundary, deferred work | Story map / issue tracker |
| `acceptance-scenarios.md` | Behavior contract before implementation | ATDD/BDD/Gherkin или equivalent table |
| Example map | Story, rules, examples, questions | Workshop note / markdown |
| `business-rules.md` | Rule, source, owner, enforcement layer, exceptions | Decision table |
| Non-goals and constraints | Защита от scope creep | `REQUIREMENTS.md`, ADR |
| `domain-modeling.md` | Contexts, terms, invariants, aggregates/events, domain review | Product-Agent OS template |
| Ubiquitous language map | Term traceability and owner review | `ubiquitous-language.md`, `glossary.md`, artifact links |
| Context map | Bounded contexts and integration relationships | `context-map.md`, Mermaid/C4/Structurizr |
| Event catalog | Domain events and contract assumptions | `event-catalog.md`, AsyncAPI/event docs |
| Invariant catalog | State rules and enforcement evidence | Domain model + tests |
| C4 diagrams | Domain boundary -> architecture boundary | `architecture-overview.md`, System Context / Container / Component as useful |
| API contract trace | Requirement/domain term -> OpenAPI operation/schema/error/security | `openapi.yaml`, OpenAPI 3.2.0 |
| UI language trace | Domain term -> screen/label/copy/error/accessibility name | UI flow spec / Storybook |
| Data dictionary/schema trace | Domain term -> table/field/event/schema/privacy | Database docs/catalog, `asyncapi.yaml` for events |
| ADR / decision log | Boundary, term, rule, requirement decisions | MADR/ADR |
| Domain review record | Human review, unresolved conflicts, accepted gaps | `domain-review-record.md`, `RUNLOG.md`, checklist |
| Traceability matrix | Requirement -> scenario -> implementation -> test/eval -> evidence owner | `requirements-traceability-matrix.md` |
| Change impact record | Downstream effects after requirement changes | `requirement-change-impact.md`, `PLAN.md`, `RUNLOG.md` |

## Product-Agent OS routing

- `requirements-author`: пишет requirements, non-goals, constraints, acceptance criteria и scenario packets.
- `implementation-planner`: блокирует implementation, если behavior scenarios, traceability или complex-domain gates отсутствуют.
- `agent-team-designer`: использует bounded contexts и ownership boundaries для team/subagent split.
- `test-eval-designer`: превращает acceptance scenarios в test/eval plan и evidence requirements.
- `risk-reviewer`: проверяет source-backed domain claims, accepted gaps, owner review и impact на API/UI/data/security/release.
- `docs-maintainer`: поддерживает requirement IDs, source registry, methodology pages, glossary/ubiquitous language и traceability docs.

## Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `requirements_scope_present` | Any non-trivial product/system work | Goal, user/stakeholder, scope или non-goals отсутствуют |
| `requirements_owner_present` | Behavior-changing work | Нет product/domain/technical owner или accepted-gap owner |
| `requirement_ids_present` | Multi-slice/regulatory/long-lived work | Requirements нельзя сослать из tests/contracts/docs/release evidence |
| `acceptance_scenarios_when_behavior_changes` | Any behavior change | Нет scenario, observable outcome, check или evidence owner |
| `requirements_traceability_present` | Behavior crosses code/API/UI/data/tests | Нет chain `requirement -> scenario -> implementation -> check -> evidence owner` |
| `business_rules_present` | Domain policy/process rule exists | Rule, source, owner, exceptions или enforcement layer отсутствуют |
| `non_goals_constraints_present` | Ambiguous feature/stakeholder scope | Non-goals, constraints, excluded behavior не явные |
| `open_questions_recorded` | Requirement uncertainty exists | Вопросы остались в chat или assumptions |
| `example_mapping_when_unclear_story` | Story unclear/large/disputed | Rules, examples, questions, deferred slices не записаны |
| `domain_discovery_workshop_when_complex_process` | Complex workflow/cross-silo process | Event/process/story discovery evidence или accepted gap отсутствует |
| `domain_model_when_complex_domain` | Complex domain/backend/workflow/data/multi-service work | Domain model/context map или accepted gap отсутствует |
| `bounded_context_architecture_boundary_trace` | Bounded context or DDD term appears | Нет architecture/team/API/data boundary или accepted gap |
| `ubiquitous_language_traceability` | Domain terms drive behavior/API/UI/data | Terms не связаны с source/artifacts/owner/review |
| `invariants_and_failure_modes_present` | Domain state transitions matter | Invariants, invalid transitions, enforcement layer или tests отсутствуют |
| `domain_event_contracts_present` | Domain events cross boundaries | Meaning, schema, producer/consumer, idempotency/ordering/privacy отсутствуют |
| `api_ui_data_traceability_present` | Requirement touches API/UI/database | Contract/schema/screen/state mapping отсутствует |
| `domain_expert_review_present` | Business-critical/compliance/finance/legal/AI-generated domain claim | Human owner review или risk acceptance отсутствует |
| `requirement_change_impact_review_present` | Requirement/domain rule changes after planning | Tests, API, DB, UI, docs, evals, rollout, rollback не reviewed |
| `accepted_gap_recorded` | Methodology gate intentionally skipped | Owner, reason, scope, review date, risk отсутствуют |
| `requirements_evidence_before_implementation` | Agent/engineer starts implementation | Requirements/scenarios/domain gates отсутствуют и нет accepted gap |

## Candidate eval fields

- Requirements scope, user/stakeholder, non-goals and owner are present.
- Stable requirement IDs exist for multi-slice, regulatory or long-lived work.
- Acceptance scenarios include observable outcomes, checks and evidence owner.
- Business rules include source, owner, exceptions and enforcement layer.
- Open questions are recorded with owner and next action.
- Example Mapping or equivalent clarification exists for unclear/large/disputed stories.
- Complex domain work has domain model, context map or explicit accepted gap.
- Bounded contexts trace to architecture/team/API/data boundary or accepted gap.
- Ubiquitous language terms trace to source, artifacts, implementation and owner.
- Domain events crossing boundaries have meaning, schema, producer/consumer, ordering/idempotency and privacy notes.
- Requirement changes include downstream impact review for tests, API, DB, UI, docs, evals, rollout and rollback.
- `accepted_gap_recorded` exists when methodology gate is intentionally skipped.

## Что ещё включить в deep research

- Requirement taxonomy: functional, non-functional, compliance, operational, AI behavior, data/privacy, release/rollback.
- Requirement quality criteria: atomicity, clarity, testability, feasibility, traceability, source and owner.
- Product discovery connection: opportunity, outcome, metric, user segment, value/risk.
- Domain discovery playbooks: Example Mapping, EventStorming, Domain Storytelling, domain expert interview.
- Domain-to-architecture mapping: bounded context -> C4 boundary -> team/subagent ownership -> API/data contract.
- Domain-to-AI mapping: AI-generated domain claims, eval datasets, reviewer rubric, hallucination/grounding risk.
- Conflict resolution process for overloaded terms.
- Accepted gap policy for simple CRUD/MVP.
- Domain review checklist for human owner.
- Change impact matrix from requirement to tests, API, database, UI, docs, evals and release.

## Unsupported claims not adopted

- "BDD replaces testing." BDD clarifies behavior, but does not replace unit, integration, contract, exploratory, performance, security or eval checks.
- "Gherkin is mandatory for BDD." Gherkin is one useful notation, not the concept itself.
- "A user story template is a complete requirement." A template without criteria, examples, business rules and evidence owner is incomplete.
- "A glossary is ubiquitous language." Ubiquitous language must be used in conversations, models, code/API/UI and owner review.
- "DDD is the right default for every project." It has coordination cost and is most useful for complex domains.
- "OpenAPI is the requirements source of truth." OpenAPI is a contract artifact and does not replace business intent.

## Open questions for future implementation

- Which requirement quality fields should become mandatory for all behavior-changing work?
- When should accepted `domain_model_not_required` be allowed for simple CRUD/MVP work?
- Should `requirements-traceability-matrix.md` be generated for every project or only risky/multi-team work?
- How should Product-Agent OS detect overloaded domain terms automatically?
- Which event discovery method should be recommended first: EventStorming, Domain Storytelling, interviews or Example Mapping?

## Проверки

- Every behavior change maps `requirement -> scenario -> check -> evidence owner`.
- Complex domain work has `domain_model_when_complex_domain` or explicit accepted gap.
- Every bounded context maps to architecture/team/API/data boundary or accepted gap.
- Ubiquitous language terms trace to project artifacts, not only definitions.
- Domain events that cross boundaries have schema, producer/consumer, ordering/idempotency and privacy notes.
- Requirement changes trigger impact review across tests/evals, API, DB, UI, docs and rollout.
- Business-critical, compliance, finance/legal and AI-generated domain claims have owner review.

## Failure modes

- Implementation starts from folders or framework choices, not behavior.
- User story title is treated as complete requirements.
- Acceptance criteria describe implementation details instead of observable outcomes.
- BDD/Gherkin becomes test automation boilerplate unreadable to domain experts.
- Example Mapping creates questions without owner or next action.
- DDD is forced onto simple CRUD and slows delivery.
- DDD is skipped for complex domain because no one owns the model.
- Bounded contexts exist only in workshop notes and do not map to architecture/API/data/team boundaries.
- Glossary exists, but code/API/UI use different terms.
- Domain events are technical messages without business meaning or contract.
- AI infers domain rules from memory/chat without source or owner confirmation.
