# Solution Architecture

Source status: `official + verified methodology + local implementation evidence + tool-assisted + experiment`

Источники: [C4 model](https://c4model.com/), [arc42](https://arc42.org/), [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html), [SEI Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/), [MADR](https://adr.github.io/madr/), [Structurizr DSL](https://docs.structurizr.com/dsl), [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html), [Thoughtworks: Fitness function-driven development](https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development), [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/definitions.html), [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/), [OpenTelemetry Documentation](https://opentelemetry.io/docs/), [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html), [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/v3.1.0), [Product-Agent OS architecture](../product-agent-os/architecture.md), [Context7 research](../sources/context7-research.md), [research dossier](../sources/methodology-research/solution-architecture.md).

## Deep research цель

Solution Architecture слой описывает, как business capabilities, requirements, bounded contexts, services, data stores, APIs, UI surfaces, LLM/AI components, security boundaries и operations собираются в одну проверяемую систему.

Для большого проекта этот слой должен быть достаточно конкретным, чтобы engineer, agent или subagent понимал architecture boundary, ownership, public contracts, data ownership, quality attributes, runtime topology и rollback impact до изменения файлов.

## Главный принцип

Architecture artifact должен отвечать на практический вопрос: какое решение принимается, какая boundary затрагивается, какие качества и риски меняются, чем это проверяется и кто владеет последствиями. Диаграмма без owner, decision, contract или verification быстро становится декоративной.

## Поддержанные факты

- C4 model provides a hierarchy of System Context, Container, Component and Code diagrams, with additional dynamic/deployment views when useful.
- arc42 provides structured architecture communication around goals, constraints, context, solution strategy, building blocks, runtime, deployment, concepts, decisions, quality and risks.
- ISO/IEC/IEEE 42010 frames architecture description around stakeholders, concerns, viewpoints and model kinds.
- SEI ATAM supports tradeoff analysis when quality attributes conflict.
- MADR gives a lightweight Markdown ADR format for significant architecture decisions.
- Structurizr DSL and Mermaid support architecture-as-code paths where diagrams should survive diff, review and build.
- AWS and Azure Well-Architected frameworks provide workload review vocabulary for reliability, security, cost, operations, performance and provider-specific concerns.
- OpenTelemetry, OpenAPI and AsyncAPI provide downstream traceability surfaces for runtime observability and public contract architecture.

## Assumptions

- Architecture docs are useful only when tied to decisions, boundaries, ownership, contracts, quality attributes, verification and rollback.
- C4 context/container views are the normal minimum for complex systems; component/code views are conditional.
- Architecture-as-code is preferred when diagrams must be reviewed, built or kept current, but early prototypes can record accepted gaps.
- ADR is required for significant or irreversible architecture decisions; trivial local choices can stay in `RUNLOG.md`.
- Quality attributes must become scenarios, measurable targets or explicit owner-approved gaps.
- AI-generated architecture is a draft until checked against repository evidence, source-backed standards and owner review.

## Инструкции применения на проекте

1. Классифицируйте architecture impact: new boundary, service split, public API/event, data ownership, runtime topology, security model, integration, dependency rule, migration, platform choice, AI/agent route или quality attribute.
2. Назовите stakeholders and concerns: users, product owner, domain owner, service owner, security/privacy, operations, support, data owner, release owner.
3. Сформулируйте architecture question. Не рисуйте диаграмму "про всё"; укажите decision, risk или onboarding question, на который она отвечает.
4. Для complex system, public contract, data/security-sensitive work, multi-service, multi-team или unclear ownership обновляйте `architecture-overview.md`.
5. Начинайте с C4 System Context: users, external systems, external APIs, trust boundaries, major data flows.
6. Затем фиксируйте C4 Container view: UI, services, workers, queues, storage, integration adapters, AI/LLM components, deployable/runtime units.
7. Component view добавляйте только для containers, где internal structure risky, non-obvious или owned by multiple teams/agents.
8. Code view добавляйте только когда source navigation недостаточен и diagram реально помогает review.
9. Для каждой boundary фиксируйте responsibility, owner, public contract, data ownership, runtime evidence и mapped bounded context, если он есть.
10. Для каждого implementation slice называйте architecture boundary, files in scope, files out of scope, contract impact, data impact, runtime impact и rollback path.
11. ADR/MADR обязателен для significant decisions: architecture boundary, public contract, persistent data, security/privacy model, quality attributes, runtime topology, migration, technology choice или irreversible cost.
12. В ADR записывайте alternatives and consequences. Decision без alternatives обычно является assertion, а не architecture reasoning.
13. Vague quality attributes переводите в scenarios или measurable targets: latency, throughput, availability, recovery, durability, consistency, security, privacy, accessibility, maintainability, observability, cost.
14. Если quality attributes конфликтуют, записывайте tradeoff. Не прячьте cost/reliability/performance/security compromise в implementation details.
15. Используйте architecture-as-code там, где диаграммы должны жить в diff, review и build. Mermaid достаточно для lightweight Markdown docs; Structurizr DSL лучше, когда один model должен генерировать несколько C4 views.
16. Проверяйте diagram render или явно записывайте missing render check. Stale diagram хуже, чем отсутствующая диаграмма.
17. Трассируйте public contracts к architecture: OpenAPI operations, AsyncAPI channels, SDK interfaces, generated clients, event schemas, consumer/versioning impact.
18. Трассируйте data ownership: source of truth, read replicas, derived data, analytics, retention, deletion, migration/backfill, privacy classification.
19. Трассируйте runtime topology к evidence: environments, deployment units, config/secrets, health checks, observability, dashboards, alerts, rollback, runbook links.
20. Для повторяющегося drift добавляйте architecture fitness functions: dependency direction, forbidden imports, public contract drift, missing observability, security gates, cost budgets, docs freshness, eval thresholds.
21. Accepted gaps записывайте явно: owner, reason, residual risk, review date, follow-up condition.
22. AI-generated architecture считайте draft. Проверяйте against repository files, source-backed standards, runtime evidence и owner review.

## Применяемые методологии разработки

| Методология | Когда применять | Как выглядит в проекте |
| --- | --- | --- |
| ISO 42010-style architecture description | Architecture должна обслуживать разных stakeholders and concerns | Stakeholders, concerns, viewpoints, model kinds, conformance evidence |
| C4 model | Нужны shared architecture views на разных уровнях | System context, container, component, optional code; dynamic/deployment as useful |
| arc42 architecture documentation | Нужна structured architecture communication | Goals, constraints, context, solution strategy, building blocks, runtime, deployment, concepts, decisions, quality, risks |
| ADR / MADR | Есть architecturally significant decision | Context, decision drivers, options, decision, consequences, verification, rollback |
| ATAM-style tradeoff analysis | Quality attributes конкурируют или риск высок | Business drivers, quality attributes, scenarios, risks, sensitivity points, tradeoffs |
| Quality attribute scenarios | Non-functional needs влияют на architecture | Stimulus, environment, response, response measure, owner |
| Architecture fitness functions | Boundary drift можно измерять | Automated/repeatable checks for dependency rules, contracts, observability, security, performance, cost, docs freshness |
| Architecture-as-code | Diagrams must survive review/diff/build | Mermaid, Structurizr DSL, PlantUML или equivalent checked-in text |
| Well-Architected review | Cloud/workload production readiness matters | Reliability, security, cost, operations, performance, sustainability/provider-specific concerns as applicable |
| Dependency boundary governance | Monorepo/modules/services/shared packages могут расползаться | Allowed imports/calls, forbidden dependencies, shared package policy, enforcement |
| Public contract architecture | APIs/events/SDK/generated clients существуют | Boundary -> OpenAPI/AsyncAPI/contracts, consumers, versioning, compatibility |
| Data ownership architecture | Persistent data/events/analytics/PII существуют | Stores, owners, schemas, retention, deletion, migration, privacy classification |
| Trust boundary architecture | Sensitive data/auth/external writes/untrusted input | Actors, assets, trust boundaries, entry points, controls, residual risk |
| Runtime/deployment architecture | Несколько deployable units/environments | Environments, deployment units, queues, storage, scaling, probes, observability, rollback |
| Evolutionary architecture | Architecture должна меняться slices | Migration slices, compatibility windows, strangler paths, fitness checks, cleanup triggers |

## Инструменты, артефакты и стандарты документирования

| Артефакт | Зачем нужен | Практический формат |
| --- | --- | --- |
| `architecture-overview.md` | Purpose, boundaries, dependencies, quality attributes, risks, verification | Product-Agent OS template |
| Architecture description index | Links to views, decisions, contracts, risks and owners | ISO 42010-inspired docs index |
| C4 System Context | Users, external systems, trust boundaries, major data flows | Mermaid / Structurizr DSL |
| C4 Container view | UI, services, workers, storage, queues, integrations, deployable units | C4 / Structurizr DSL |
| C4 Component view | Internal structure of risky/non-obvious container | Mermaid / PlantUML |
| Dynamic / sequence view | Important runtime flows and failure paths | Mermaid sequence / C4 dynamic |
| Deployment topology | Environments, nodes, runtime units, network paths, secrets/config, rollback | `runtime-topology.md`, arc42 deployment view |
| Boundary responsibility map | Boundary, responsibility, owner, public contract, data ownership, mapped bounded context | `boundary-responsibility-map.md`, `architecture-overview.md` table |
| Dependency rules | Allowed/forbidden imports/calls and enforcement | `dependency-rules.md`, lint/tests/architecture checks |
| Integration catalog | External systems, auth, data exchanged, retries, idempotency, failure modes | `integration-catalog.md` |
| API/event contract map | Boundary -> OpenAPI/AsyncAPI operation/channel/schema/version/consumer | OpenAPI / AsyncAPI |
| Data ownership map | Boundary -> data store/schema/table/event/PII/retention/migration owner | `database-dictionary.md`, database docs/catalog |
| Trust boundary map | Actors, assets, entry points, data flows, controls, residual risk | `trust-boundary-map.md`, threat model / C4 |
| Quality attribute scenarios | Measurable non-functional expectations | `quality-attribute-scenarios.md`, ATAM / arc42 quality requirements |
| Tradeoff record | Competing qualities, options, consequences, selected compromise | `architecture-tradeoff-record.md`, ADR / review note |
| ADR / decision log | Significant decisions and rationale | MADR / local `adr.md` |
| Architecture fitness checks | Repeatable checks for drift/conformance | tests, CI, lint, contract checks, evals |
| Observability architecture | Traces, metrics, logs, dashboards, alerts, sampling/redaction gaps | `architecture.md`, OpenTelemetry / runbook |
| Migration/evolution plan | Current state, target state, compatibility, rollout, rollback, cleanup trigger | `migration-plan.md`, ADR |
| Architecture review record | Owner review, evidence, unresolved risks, accepted gaps, next action | `architecture-review-record.md`, `RUNLOG.md` / checklist |
| Architecture fitness functions | Repeatable dependency, contract, observability, docs and eval checks | `architecture-fitness-functions.md` |
| Docs tooling decision | Selected/rejected tools, commands, owners, approvals | `docs-tooling-decision.md`, `architecture-docs-tooling-decision.md`, `workspace.dsl` when Structurizr is used |
| Security risk review trace | Trust boundary and security/privacy decision link | `security-risk-review.md`, threat model |
| API contract review trace | Public contract impact and compatibility | `api-contract-review.md` |

## Product-Agent OS routing

- `workspace-discovery-auditor`: detects architecture docs, ADR, OpenAPI, AsyncAPI, DB docs, CI, docs tooling and runtime clues as `present_unverified` until verified.
- `requirements-author`: names product/domain constraints and architecture-significant requirements before planning.
- `implementation-planner`: requires `architecture_boundary` per slice and stops when boundary, accepted gap, docs impact or rollback path is missing.
- `agent-team-designer`: uses architecture boundaries for ownership split across agents/subagents and forbidden files.
- `test-eval-designer`: maps architecture claims to tests, contract checks, diagram render, runtime checks, evals or explicit gaps.
- `risk-reviewer`: reviews public contract, data, security, migration, release and rollback impact.
- `docs-maintainer`: keeps architecture docs, ADRs, diagrams, contracts and source registry aligned with behavior changes.

## Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `solution_architecture_scope_present` | Complex system, multi-service, public contract, data/security or unclear ownership | System purpose, stakeholders, concerns, scope или non-goals отсутствуют |
| `architecture_context_view_present` | External users/systems/trust boundaries exist | Context view или equivalent external boundary map отсутствует |
| `architecture_container_boundary_present` | Multiple deployable/runtime units exist | Container/service/storage/queue/worker boundaries не названы |
| `architecture_boundary_per_slice` | Any non-trivial implementation slice | Slice lacks boundary, in-scope files, out-of-scope files или owner |
| `boundary_responsibility_owner_present` | Boundary added/changed | Responsibility, owner, public contract или data ownership отсутствуют |
| `domain_to_architecture_trace_present` | Domain model or bounded context exists | Bounded context не мапится к architecture boundary или accepted gap |
| `bounded_context_architecture_boundary_trace` | Bounded context or DDD term appears | Нет `context-map.md`, architecture/team/API/data boundary или accepted gap |
| `public_contract_boundary_trace_present` | API/event/SDK/generated client changes | Boundary не linked to OpenAPI/AsyncAPI/contract, consumers или versioning |
| `data_ownership_boundary_present` | Persistent data/analytics/PII/migration changes | Data owner, source of truth, retention, deletion или migration ownership отсутствуют |
| `trust_boundary_security_review_present` | Auth, PII, payments, external writes, untrusted input | Trust boundary, entry point, control или residual risk отсутствуют |
| `quality_attribute_scenarios_present` | Performance/availability/security/privacy/maintainability/cost/operability matter | Quality attributes остаются vague labels без scenario/owner |
| `tradeoff_record_for_high_impact_decision` | Quality attributes conflict or irreversible decision exists | Options, consequences, selected compromise или evidence отсутствуют |
| `adr_for_architecture_decision` | Significant architecture decision | ADR или accepted gap отсутствует |
| `runtime_deployment_topology_present` | Runtime/deployment changes | Environments, deployment units, config/secrets, health checks, rollback или runbook отсутствуют |
| `observability_architecture_present` | Service/runtime behavior matters | Traces, metrics, logs, dashboards, alert owner или explicit observability gap отсутствуют |
| `dependency_rules_present` | Monorepo/modules/services/shared packages exist | Allowed/forbidden dependencies или enforcement path отсутствует |
| `diagram_render_check_present` | Architecture diagram added/changed | Render/build/validate check или explicit gap отсутствует |
| `architecture_fitness_function_present` | Boundary drift/conformance risk repeats | Repeatable check, lint, test, contract check, eval или owner review отсутствует |
| `migration_rollback_path_present` | Architecture migration or service split | Current/target state, compatibility window, rollout, rollback или cleanup trigger отсутствуют |
| `architecture_docs_as_code_present` | Docs-as-code impact exists | Text artifact, selected tool, owner, command или accepted gap отсутствует |
| `architecture_owner_review_present` | High-impact architecture change | Architect/service owner/domain owner review или explicit risk acceptance отсутствует |
| `accepted_gap_recorded` | Architecture gate intentionally skipped | Owner, reason, residual risk, review date, follow-up condition отсутствуют |

## Candidate eval fields

- Architecture scope, stakeholders, concerns, non-goals and decision question are present.
- Context view or equivalent boundary map covers users, external systems and trust boundaries.
- Container/runtime view names UI, services, workers, queues, storage, integrations and deployable units where relevant.
- Boundary responsibility, owner, public contract and data ownership are documented.
- Bounded context maps to architecture/team/API/data boundary or accepted gap.
- Public contract changes trace to OpenAPI/AsyncAPI/contracts, consumers and versioning.
- Data ownership includes source of truth, retention, deletion, migration/backfill and privacy classification.
- Trust boundary review exists for auth, PII, payments, external writes or untrusted input.
- Quality attributes have measurable scenarios, owner and evidence path.
- Tradeoff record exists for conflicting qualities or irreversible decisions.
- Diagram render/build/validate check exists when diagram changes.
- Migration/rollback path exists for service split or architecture migration.
- Owner review or explicit risk acceptance exists for high-impact architecture change.

## Что ещё включить в deep research

- Stakeholder concern map: кто читает architecture docs и какие decisions они принимают.
- Viewpoint catalog: какие views обязательны для web, backend, data, AI, desktop/native, plugin/agent workflows.
- Quality attribute scenario templates and examples.
- Architecture decision trigger policy: когда ADR обязателен, когда достаточно RUNLOG note.
- Tradeoff review checklist for performance/security/cost/reliability/privacy.
- Architecture fitness functions catalog for dependency rules, contract drift, docs freshness, observability, security gates, AI eval thresholds.
- Boundary-to-agent ownership rules for parallel subagents/worktrees.
- Cloud-neutral well-architected review matrix.
- Runtime evidence packet: health checks, traces, metrics, logs, dashboards, alerts, rollback/runbook links.
- Architecture docs lifecycle: owner, render check, review cadence, stale-doc detection.

## Проверки

- Complex system work has `architecture-overview.md` or accepted gap.
- Every non-trivial slice names architecture boundary and files in/out of scope.
- Significant architecture decisions have ADR/MADR or accepted gap.
- Context/container diagrams exist where users, external systems, services, stores or queues matter.
- Diagrams render or missing render check is explicit.
- Public contracts map to OpenAPI/AsyncAPI/SDK/event schemas.
- Data ownership, trust boundaries and runtime topology are visible for sensitive or persistent systems.
- Quality attributes have measurable scenarios or explicit owner-approved gap.
- Architecture claims cite current tests, contract checks, runtime evidence, diagram build, owner review or explicit gaps.

## Failure modes

- Architecture page becomes decorative and not tied to decisions.
- Diagrams are stale because no owner or build/render check exists.
- "Solution architecture" is treated as role title, not reviewable artifact.
- C4 code-level diagrams are overused where context/container would be enough.
- Context view omits external systems, trust boundaries or data flows.
- ADR records chosen option but omits alternatives, consequences, verification and rollback.
- Quality attributes are vague slogans: scalable, secure, reliable.
- Public contracts or data ownership change without architecture trace.
- Runtime topology omits config/secrets, health checks, observability, rollback or runbook.
- AI-generated architecture is accepted without repository evidence and owner review.

## Unsupported claims not adopted

- "Architecture means diagrams." Architecture artifacts must answer decisions, boundaries, quality, verification and ownership questions.
- "C4 code diagrams are always better because they are detailed." Context/container views are often more useful for product and team coordination.
- "ADR is bureaucracy." ADR is required when decision impact is significant or hard to reverse.
- "Well-Architected review proves architecture quality." It is a review lens, not evidence by itself.
- "Architecture-as-code is always required." It is required when diagrams must survive review/build; otherwise accepted gaps are allowed.
- "AI can design architecture from chat alone." Repository evidence, source-backed standards and owner review are required.

## Open questions for future implementation

- Which view catalog should be mandatory by project type: web, backend, data, AI, desktop/native or plugin/agent workflow?
- What exact trigger should require ADR versus `RUNLOG.md` decision note?
- Which architecture fitness functions should ship first: dependency rules, contract drift, docs freshness, observability, security or eval thresholds?
- How should boundary-to-agent ownership rules be encoded for parallel subagents and worktrees?
- Should Mermaid remain default, with Structurizr DSL only when one model must generate many C4 views?
- How should stale architecture docs be detected automatically?
