# Solution Architecture Methodology Research

Source status: `official + verified methodology + local implementation evidence + tool-assisted`

Research date: `2026-05-24`

Target methodology page: [../../methodologies/solution-architecture.md](../../methodologies/solution-architecture.md)

Target Product-Agent OS behavior: make architecture a reviewable, source-backed and verifiable artifact that maps requirements, domain boundaries, quality attributes, public contracts, data ownership, security boundaries, runtime topology, decisions, risks and rollback before implementation changes system structure.

## Scope

This dossier covers solution architecture for large software projects: system context, containers/services, components, code-level detail when useful, quality attributes, tradeoffs, architecture decisions, contracts, data ownership, trust boundaries, runtime/deployment topology, observability, migration and architecture governance.

It does not mandate enterprise architecture frameworks, a specific cloud provider, UML, C4, Structurizr, Mermaid, arc42, microservices, DDD or ADRs for every change. These practices are conditional and should scale with system complexity, public contract risk, data/security impact, team count, deployment risk and long-lived maintainability needs.

## Supported facts

- The C4 model defines hierarchical abstractions for software architecture: software systems, containers, components and code. It also defines hierarchical diagrams: system context, container, component and code, plus supporting system landscape, dynamic and deployment diagrams.
- The C4 model is notation independent and tooling independent. This supports Mermaid, Structurizr DSL, PlantUML or other project-appropriate tools as long as the architecture view is understandable and maintained.
- C4 can be combined with arc42: system context aligns with Context and Scope, container with Building Block View level 1, component with level 2 and code with level 3.
- arc42 provides an open-source, pragmatic template for documenting and communicating software and system architectures. It is process-agnostic, technology-agnostic and suited to lean/agile approaches.
- ISO/IEC/IEEE 42010:2022 specifies requirements for the structure and expression of architecture descriptions. It distinguishes architecture from the architecture description that expresses it, covers frameworks/languages/viewpoints/model kinds, and does not prescribe a specific creation process, notation, tool or recording format.
- SEI's Architecture Tradeoff Analysis Method (ATAM) is a structured technique for understanding tradeoffs in software-intensive system architectures. It evaluates architecture fitness against competing quality attributes such as modifiability, security, performance and availability.
- SEI ATAM guidance explicitly notes that quality attributes interact and improving one can worsen another, so architecture decisions need tradeoff analysis rather than one-dimensional optimization.
- MADR defines an Architectural Decision as a justified software design choice that addresses an architecturally significant functional or non-functional requirement, and an ADR as the record that documents the decision and rationale.
- Structurizr DSL is a text-based domain-specific language for defining software architecture models based on the C4 model. The Structurizr documentation includes Markdown/AsciiDoc documentation and ADR support.
- Mermaid provides text-based diagram syntax for many diagram types and can live inside Markdown documentation. Its own documentation warns that syntax issues can break diagrams, so render/build checks are part of evidence.
- Thoughtworks describes architecture fitness functions as objective tests or metrics that measure whether architecture is aligned with architectural goals and can provide continuous feedback against architectural drift.
- AWS Well-Architected Framework defines six pillars: operational excellence, security, reliability, performance efficiency, cost optimization and sustainability. It also states that architecture tradeoffs are made based on business context.
- Azure Well-Architected Framework is a set of quality-driven tenets, architectural decision points and review tools for workloads, with pillars including reliability, security, cost optimization, operational excellence and performance efficiency.
- OpenTelemetry is a vendor-neutral observability framework for generating, collecting and exporting telemetry data such as traces, metrics and logs; this is useful as runtime evidence for architecture claims.
- The local Product-Agent OS implementation already has `architecture-overview.md`, `adr.md`, `architecture_boundary`, `bounded_context_architecture_boundary_trace`, docs-as-code routing and readiness statuses for architecture-related gates.

## Assumptions

- Solution architecture should be a decision and verification surface, not a decorative diagram pack.
- For large projects, the minimum useful architecture artifact is an `architecture-overview.md` that names system purpose, users, external systems, trust boundaries, containers/services, data stores, quality attributes, risks, owners and verification route.
- Context and container views are usually the default minimum for complex systems. Component and code views should be added only where they reduce delivery or review risk.
- Every implementation slice should name the architecture boundary it touches and what remains out of scope.
- Architecture decisions should be captured only when they are significant: public contract, boundary, data ownership, security model, runtime topology, migration, technology choice, quality attribute or rollback impact.
- Quality attributes should be expressed as scenarios or measurable expectations, not vague "scalable/secure/fast" labels.
- Architecture-as-code should be preferred when diagrams must survive review, diff, build and CI, but teams can record an accepted gap for docs-light or early prototype work.
- Cloud well-architected frameworks are useful quality checklists, not vendor-neutral architecture law. Use them conditionally when the target workload is cloud-hosted or when the pillars help structure review.
- AI-generated architecture should remain `present_unverified` until checked against repository evidence, primary sources and owner review.

## Unsupported claims not adopted

- "Solution architecture is a role title." Product-Agent OS treats it as a reviewable artifact and decision workflow.
- "One diagram is enough for a large system." Large systems need views selected by stakeholder concerns and risk.
- "C4 code-level diagrams are always required." Code views are optional and only useful when they add value beyond source navigation.
- "arc42 is a process." arc42 is documentation and communication structure, not a required delivery process.
- "ADR for every small decision." ADRs should capture architecturally significant decisions, not noise.
- "A rendered diagram proves architecture correctness." Render proves syntax/display only; correctness needs source evidence, owner review, tests, contracts or runtime evidence.
- "Well-Architected pillars mean a cloud vendor must be adopted." Pillars are review heuristics and should not imply provider lock-in.
- "Architecture can be inferred from directory names." Directory structure is a clue, not verified architecture compliance.
- "Architecture fitness functions replace review." Fitness functions provide continuous signals; tradeoff review and owner judgment still matter.

## Methodologies

| Methodology | When to apply | Project-level behavior |
| --- | --- | --- |
| ISO 42010-style architecture description | Architecture must serve multiple stakeholders and concerns | Identify stakeholders, concerns, viewpoints, model kinds and conformance evidence. |
| C4 model | Teams need shared architecture views at different levels | System context, container, component and optional code views; supporting dynamic/deployment views when useful. |
| arc42 architecture documentation | Architecture needs structured communication | Goals, constraints, context, solution strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality and risks. |
| ADR / MADR | Architecturally significant decision appears | Record context, decision drivers, considered options, selected decision, consequences, verification and rollback. |
| ATAM-style tradeoff analysis | Quality attributes compete or risk is high | Analyze business drivers, quality attributes, scenarios, risks, sensitivity points and tradeoffs. |
| Quality attribute scenarios | Non-functional needs affect architecture | Convert performance, availability, security, privacy, maintainability, cost and operability into measurable scenarios. |
| Architecture fitness functions | Architecture drift can be measured | Add automated or repeatable checks for dependency rules, contracts, observability, security, performance, cost or docs freshness. |
| Architecture-as-code | Diagrams must be reviewed and maintained | Use Mermaid, Structurizr DSL, PlantUML or equivalent checked-in text formats with render/validate checks. |
| Well-Architected review | Cloud/workload production readiness matters | Review reliability, security, cost, operations, performance and sustainability/provider-specific concerns as applicable. |
| Dependency boundary governance | Monorepo, modular app, services or parallel agents can erode boundaries | Define allowed imports/calls, shared packages, ownership and forbidden dependencies. |
| Public contract architecture | APIs, events, SDKs or generated clients exist | Map boundaries to OpenAPI/AsyncAPI/contracts, consumers, versioning and compatibility. |
| Data ownership architecture | Persistent data, events, analytics or PII exists | Map data stores, owners, schemas, retention, deletion, migration and privacy classifications. |
| Trust boundary architecture | Sensitive data, auth, external writes or untrusted input exists | Map actors, assets, trust boundaries, entry points, controls and residual security risk. |
| Runtime/deployment architecture | System has multiple deployable units or environments | Map environments, deployment units, queues, storage, scaling, probes, observability and rollback. |
| Evolutionary architecture | Architecture must change incrementally | Plan migration slices, compatibility windows, strangler paths, fitness checks and rollback/cleanup triggers. |

## Documentation artifacts and standards

| Artifact | Purpose | Candidate source/tool |
| --- | --- | --- |
| `architecture-overview.md` | System purpose, boundaries, dependencies, quality attributes, risks and verification. | C4, arc42, Product-Agent OS template |
| Architecture description index | Entry point that links views, decisions, contracts, risks and owner map. | ISO 42010-inspired docs index |
| C4 System Context | Users, external systems, external dependencies and trust boundaries. | C4, Mermaid, Structurizr DSL |
| C4 Container view | UI, services, workers, storage, queues, integrations and deployable units. | C4, Structurizr DSL |
| C4 Component view | Internal structure of a risky or non-obvious container. | C4, Mermaid/PlantUML |
| Dynamic / sequence view | Important runtime flows, failure paths and integration sequences. | C4 dynamic view, Mermaid sequence |
| Deployment topology | Environments, nodes, runtime units, network paths, secrets/config and rollback. | arc42 deployment view, platform docs |
| Boundary responsibility map | Boundary, responsibility, owner, public contract, data ownership and mapped bounded context. | `architecture-overview.md` |
| Dependency rules | Allowed imports/calls, forbidden dependencies, shared package policy and enforcement. | lint rules, architecture tests |
| Integration catalog | External systems, owners, auth, data exchanged, retries, idempotency, observability and failure modes. | API docs, backend methodology |
| API/event contract map | Boundary -> OpenAPI/AsyncAPI operation/channel/schema/version/consumer. | OpenAPI, AsyncAPI |
| Data ownership map | Boundary -> data store/schema/table/event/PII/retention/migration owner. | Database docs/catalog |
| Trust boundary map | Actors, assets, entry points, data flows, controls and residual risk. | Threat model, C4, security review |
| Quality attribute scenarios | Stimulus, environment, response, response measure and owner. | ATAM, arc42 quality requirements |
| Tradeoff record | Competing qualities, options, consequences, chosen compromise and evidence. | ATAM-style review, ADR |
| ADR / decision log | Significant architecture decisions and consequences. | MADR, local `adr.md` |
| Architecture fitness checks | Automated/repeatable checks for drift and conformance. | tests, CI, lint, contract checks, evals |
| Observability architecture | Traces, metrics, logs, dashboards, alert owners and sampling/redaction gaps. | OpenTelemetry, runbook |
| Migration/evolution plan | Current state, target state, compatibility, rollout, rollback and cleanup trigger. | ADR, migration plan |
| Architecture review record | Review owner, evidence, unresolved risks, accepted gaps and next action. | RUNLOG, review checklist |
| Docs tooling decision | Selected/rejected diagram and docs tools, commands, owners and approval needs. | `docs-tooling-decision.md` |

## Project application instructions

1. Classify architecture impact before implementation: new boundary, service split, public API/event, data ownership, runtime topology, security model, integration, dependency rule, migration, platform choice, AI/agent route or quality attribute.
2. Start with stakeholders and concerns: users, product owner, domain owner, service owner, security/privacy, operations, support, data owner and release owner.
3. Define the architecture question. Avoid generic diagrams; name the decision or risk the view must answer.
4. Write or update `architecture-overview.md` for complex systems, public contracts, data/security sensitive work, multi-service work, multi-team work or unclear ownership.
5. Start with C4 System Context: users, external systems, external APIs, trust boundaries and major data flows.
6. Add C4 Container view for deployable/runtime boundaries: UI, services, workers, queues, storage, integration adapters and AI/LLM components.
7. Add Component view only for containers whose internals are risky, non-obvious or owned by multiple agents/teams.
8. Add Code view only when source navigation is insufficient and the diagram helps review a hard design decision.
9. For every boundary, record responsibility, owner, public contract, data ownership, runtime evidence and mapped bounded context where applicable.
10. For every slice, name architecture boundary, files in scope, files out of scope, contract impact, data impact, runtime impact and rollback path.
11. Use ADR/MADR when a decision affects architecture boundary, public contract, persistent data, security/privacy, quality attributes, runtime topology, migration or irreversible cost.
12. For each ADR, record considered options and consequences. A decision without alternatives is usually an assertion, not architecture reasoning.
13. Convert vague quality attributes into scenarios or measurable targets: latency, throughput, availability, recovery, durability, consistency, security, privacy, accessibility, maintainability, observability and cost.
14. When quality attributes conflict, record the tradeoff. Do not hide cost/reliability/performance/security compromises in implementation details.
15. Use architecture-as-code where the diagram must be reviewed, diffed or built. Mermaid is enough for lightweight Markdown docs; Structurizr DSL is better when a single model must produce multiple C4 views.
16. Validate diagram syntax or explicitly record the missing render check. A stale diagram is worse than an absent one.
17. Map public contracts to architecture: OpenAPI operations, AsyncAPI channels, SDK interfaces, generated clients, event schemas and consumer/versioning impact.
18. Map data ownership to architecture: source of truth, read replicas, derived data, analytics, retention, deletion, migration/backfill and privacy classification.
19. Map runtime topology to evidence: environments, deployment units, config/secrets, health checks, observability, dashboards, alerts, rollback and runbook links.
20. Use architecture fitness functions for repeated conformance risks: dependency direction, forbidden imports, public contract drift, missing observability, security gates, cost budgets, docs freshness or eval thresholds.
21. Record accepted gaps explicitly with owner, reason, residual risk, review date and follow-up condition.
22. Treat AI-generated architecture as draft. Verify against repository files, source-backed standards, runtime evidence and owner review before using it for implementation.

## Product-Agent OS candidate rules

### Discovery signals

- Directories: `docs/architecture/`, `architecture/`, `docs/adr/`, `adr/`, `docs/diagrams/`, `openapi/`, `asyncapi/`, `contracts/`, `infra/`, `deploy/`, `ops/`, `runbooks/`
- Files: `architecture-overview.md`, `architecture.md`, `context-map.md`, `*.dsl`, `workspace.dsl`, `*.puml`, `*.mmd`, `ADR*.md`, `adr.md`, `docs-tooling-decision.md`, `integration-catalog.md`, `api-contract-review.md`, `database-dictionary.md`, `migration-plan.md`, `security-risk-review.md`
- Terms: solution architecture, architecture boundary, C4, context diagram, container diagram, component diagram, deployment view, runtime view, ADR, MADR, arc42, Structurizr, Mermaid, PlantUML, quality attribute, tradeoff, fitness function, dependency rule, public contract, data ownership, trust boundary, rollback, migration, observability
- Risk signals: public API, generated client, event contract, persistent data, PII, auth, payments, external write, migration, multi-service, multi-team, subagent parallelism, cloud architecture, queue, worker, storage, LLM/agent orchestration, security boundary, performance/SLO, release rollback

### Readiness gates

| Gate | Trigger | Block condition |
| --- | --- | --- |
| `solution_architecture_scope_present` | Complex system, multi-service, public contract, data/security or unclear ownership | System purpose, stakeholders, concerns, scope or non-goals are missing. |
| `architecture_context_view_present` | External users/systems/trust boundaries exist | Context view or equivalent external boundary map is missing. |
| `architecture_container_boundary_present` | Multiple deployable/runtime units exist | Container/service/storage/queue/worker boundaries are not named. |
| `architecture_boundary_per_slice` | Any non-trivial implementation slice | Slice lacks boundary, in-scope files, out-of-scope files or owner. |
| `boundary_responsibility_owner_present` | Boundary is added or changed | Responsibility, owner, public contract or data ownership is missing. |
| `domain_to_architecture_trace_present` | Domain model or bounded context exists | Bounded context does not map to architecture boundary or accepted gap. |
| `public_contract_boundary_trace_present` | API/event/SDK/generated client changes | Boundary is not linked to OpenAPI/AsyncAPI/contract, consumers or versioning. |
| `data_ownership_boundary_present` | Persistent data, analytics, PII or migration changes | Data owner, source of truth, retention, deletion or migration ownership is missing. |
| `trust_boundary_security_review_present` | Auth, PII, payments, external writes or untrusted input | Trust boundary, entry point, control or residual risk is missing. |
| `quality_attribute_scenarios_present` | Performance, availability, security, privacy, maintainability, cost or operability matter | Quality attributes are vague labels without measurable scenario or owner. |
| `tradeoff_record_for_high_impact_decision` | Quality attributes conflict or irreversible decision exists | Options, consequences, selected compromise or evidence are missing. |
| `adr_for_architecture_decision` | Significant architecture decision | ADR or accepted gap is missing. |
| `runtime_deployment_topology_present` | Runtime/deployment changes | Environments, deployment units, config/secrets, health checks, rollback or runbook are missing. |
| `observability_architecture_present` | Service/runtime behavior matters | Traces, metrics, logs, dashboards, alert owner or explicit observability gap is missing. |
| `dependency_rules_present` | Monorepo/modules/services/shared packages exist | Allowed/forbidden dependencies or enforcement path is missing. |
| `diagram_render_check_present` | Architecture diagram is added or changed | Render/build/validate check or explicit gap is missing. |
| `architecture_fitness_function_present` | Boundary drift or conformance risk repeats | No repeatable check, lint, test, contract check, eval or owner review exists. |
| `migration_rollback_path_present` | Architecture migration or service split | Current/target state, compatibility window, rollout, rollback or cleanup trigger is missing. |
| `architecture_docs_as_code_present` | Docs-as-code impact exists | Text-based artifact, selected tool, owner, command or accepted gap is missing. |
| `architecture_owner_review_present` | High-impact architecture change | Architect/service owner/domain owner review or explicit risk acceptance is missing. |
| `accepted_gap_recorded` | Architecture gate intentionally skipped | Owner, reason, residual risk, review date and follow-up condition are missing. |

### Candidate templates

- `architecture-overview.md`
- `adr.md`
- `architecture-review-record.md`
- `boundary-responsibility-map.md`
- `quality-attribute-scenarios.md`
- `architecture-tradeoff-record.md`
- `architecture-fitness-functions.md`
- `dependency-rules.md`
- `integration-catalog.md`
- `runtime-topology.md`
- `trust-boundary-map.md`
- `architecture-docs-tooling-decision.md`

### Candidate eval fields

- `solution_architecture_scope_present`
- `architecture_context_view_present`
- `architecture_container_boundary_present`
- `architecture_boundary_per_slice`
- `boundary_responsibility_owner_present`
- `quality_attribute_scenarios_present`
- `tradeoff_record_for_high_impact_decision`
- `adr_for_architecture_decision`
- `public_contract_boundary_trace_present`
- `data_ownership_boundary_present`
- `trust_boundary_security_review_present`
- `runtime_deployment_topology_present`
- `observability_architecture_present`
- `dependency_rules_present`
- `diagram_render_check_present`
- `architecture_fitness_function_present`
- `migration_rollback_path_present`
- `architecture_owner_review_present`

## Failure modes

- Architecture documentation describes the system after the fact and does not influence decisions.
- Diagrams are decorative and not tied to requirements, decisions, owners, contracts or verification.
- Context view omits external systems, trust boundaries or data flows.
- Container view hides queues, workers, storage, batch jobs or AI/LLM components.
- Component/code diagrams are overused and become stale faster than source navigation.
- ADRs record the chosen option but omit alternatives, consequences, verification and rollback.
- Quality attributes remain slogans: scalable, secure, reliable, maintainable.
- Architecture decisions optimize one quality attribute while silently damaging another.
- Public contracts, generated clients or event schemas change without architecture trace.
- Data ownership and privacy classification stay implicit until migration/release time.
- Runtime topology omits config/secrets, health checks, observability, rollback or runbook links.
- Architecture-as-code exists but render/validate checks are never run.
- AI-generated architecture is accepted without checking repository evidence and owner review.

## Open questions for future research

- Should Product-Agent OS add a standalone `quality-attribute-scenarios.md` template, or keep quality attributes inside `architecture-overview.md` and ADRs?
- Should architecture fitness functions become part of `TEST.md`, `EVALS.md`, or a separate `architecture-fitness-functions.md` artifact?
- Should solution architecture gates be hard for all public-contract/data/security changes, or conditional warnings until Track 8 readiness hardening is finished?
- How should agent-team ownership use architecture boundaries when boundaries overlap with domain contexts and frontend feature slices?

## Sources

- [C4 model](https://c4model.com/)
- [arc42](https://arc42.org/)
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html)
- [SEI: Architecture Tradeoff Analysis Method](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/)
- [MADR](https://adr.github.io/madr/)
- [Structurizr DSL](https://docs.structurizr.com/dsl)
- [Mermaid syntax reference](https://mermaid.js.org/intro/syntax-reference.html)
- [Thoughtworks: Fitness function-driven development](https://www.thoughtworks.com/en-us/insights/articles/fitness-function-driven-development)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/definitions.html)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html)
- [AsyncAPI Specification](https://www.asyncapi.com/docs/reference/specification/v3.1.0)
- [Context7 research](../context7-research.md)
