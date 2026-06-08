# Product-Agent OS methodology intelligence

Source status: `local product design + experiment`

Источники: [Product-Agent OS architecture](architecture.md), [Product-Agent OS scenarios](scenarios.md), [Behavioral evals](behavioral-evals.md), [Codex workflows](https://developers.openai.com/codex/workflows), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

Methodology intelligence является read-only layer который turns workspace evidence в practical delivery guidance. Это reads files, control-plane artifacts и route signals, затем returns `methodology_packet`, `finish_options`, `owner_questions`, `safe_next_action`, `methodology_synthesis` и `source_artifact_ledger` когда they являются useful.

Эти packets являются recommendation и routing evidence. Они не изменяют target projects, не включают hooks, не активируют automations, не вызывают providers и не approve external writes.

## What Это Solves

Product-agent work часто ломается двумя способами: либо coding начинается до ясного project contract, либо heavy methodology навязывается simple work. Methodology intelligence дает Product-Agent OS средний путь:

- read existing workspace до prescribing process;
- detect который engineering standards apply;
- keep lightweight work lightweight;
- требуют deeper evidence только для real risk;
- return owner questions когда evidence является missing;
- stage recommendations instead из silently changing target workspace.

## Входы

- пользователь intent или route hint;
- read-only workspace inventory;
- `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md`;
- architecture docs, ADRs, API contracts, database docs, Storybook/FSD signals, CI, evals, metrics, release artifacts и security/privacy evidence когда present;
- текущий политика источников, sandbox, approvals и external-system boundaries;
- accepted gaps и previous failure notes.

## Project Scanning Principle

Scan является evidence-first и non-mutating. Product-Agent OS читает workspace пользователя, совмещает repository signals с user intent, определяет maturity/complexity и включает только methodology gates, которые снижают real project risk. Scan не пишет target files, не вызывает providers, не включает hooks, не создает automations, не меняет canonical graph sources и не считает generated dashboards доказательством.

| Слой сканирования | Примеры сигналов | Как Product-Agent OS использует это |
| --- | --- | --- |
| Workspace inventory | Манифесты, source folders, tests, docs, CI, release и config files. | Classifies simple, standard, complex или high-risk work; для маленьких задач не включает лишний process. |
| Stack and surface detection | Frontend, backend, native/mobile, desktop, API, database, AI/RAG, docs, automation, release surfaces. | Routes work в релевантные product, architecture, quality, data, AI, security и operations domains. |
| Contract evidence | OpenAPI, AsyncAPI, GraphQL, gRPC, JSON Schema, Pact, generated SDKs, webhooks. | Activates API contract-first, compatibility, error/auth и contract-test gates. |
| Data evidence | Schemas, migrations, ORM models, DB docs, data contracts, backfills, production-data hints. | Activates migration planning, data dictionary, rollback, backup/restore, classification и access approval gates. |
| AI/RAG evidence | Prompts, evals, model decisions, tools, retrieval config, vector data, datasets, agent traces. | Activates baseline evals, prompt/model/tool contracts, grounding, dataset governance и cost/latency checks. |
| Security and privacy evidence | Auth, secrets, PII, payments, permissions, compliance, SBOM, audit, security review. | Activates threat surface, ASVS/SSDF/SAMM, authz negative tests, privacy и supply-chain review. |
| Codex control-plane evidence | `AGENTS.md`, requirements/plan/test/eval/runlog files, subagents, skills, MCP, hooks, automation candidates. | Activates model/reasoning policy, handoffs, ownership, approvals, memory policy и automation maturity checks. |
| User intent | Feature, bug, release, migration, AI behavior, PR review, production readiness, regulated risk. | Добавляет intent-only risk, если repo evidence неполный, и возвращает owner questions вместо догадки. |

## Выходы

| Output | Purpose |
| --- | --- |
| `methodology_applicability` | Records который domains apply, why, и what evidence является missing. |
| `methodology_packet` | Route-ready evidence bundle для next worker. |
| `finish_options` | Safe options such как answer, stage proposal, request approval, запуск focused verification или stop на gap. |
| `owner_questions` | Smallest blocking questions для decisions который не может быть inferred из source files. |
| `safe_next_action` | Этот next move который respects политика источников, sandbox, approvals и evidence. |
| `source_artifact_ledger` | Mapping из recommendations к source artifacts который support them. |
| `methodology_synthesis` | Grouped recommendations across domains с risk-aware ordering. |

## Methodology Domains

| Domain | Когда применять | Minimum evidence |
| --- | --- | --- |
| Business & Product | Product behavior, MVP, launch, pricing, onboarding, growth или value claims change. | User/problem, non-goals, acceptance scenario, metric, guardrail или explicit gap. |
| Requirements & Domain | Behavior, workflow, rules, public contract, domain language или multi-slice scope is unclear. | Requirement registry, acceptance scenarios, owner questions, business rules, domain model или accepted gap. |
| Solution architecture | Boundaries, services, public contracts, runtime topology или irreversible design change. | Scope, boundary, decision, alternatives, rollback и owner evidence. |
| Quality, Testing & Evals | Ready/done/fixed/works/release claims, behavior changes, regressions, evals или runtime quality matter. | Test/eval matrix, risk-based scope, current evidence, manual QA evidence или explicit test gap. |
| Codex / Agentic Workflow | Codex App, CLI, IDE extension, subagents, skills, MCP, hooks, plugins, memory, automation или long-running agent work applies. | Control plane, source-of-truth boundary, model/reasoning policy, handoff contract, approval boundary и automation maturity evidence. |
| Frontend | User-visible UI, interaction, accessibility, visual QA или performance change. | User flow, component states, browser/runtime evidence, visual/accessibility gap или proof. |
| Backend | Service behavior, jobs, queues, auth, errors, observability или rollback paths. | Runtime behavior, failure mode, health/logging, tests и rollback evidence. |
| API & Integrations | HTTP API, event contract, SDK, webhook, external provider или consumer contract. | Source-of-truth contract, consumer map, compatibility и external-write approval boundary. |
| Database & Data | Schema, migration, lineage, retention, sensitive data или production data. | Inventory, dictionary, migration plan, rollback/backup, data classification и production access boundary. |
| LLM / AI / RAG | Prompt/model/tool/RAG/eval behavior changes. | Baseline/current eval, prompt/model/tool contracts, grounding, traces, cost/latency и incident path. |
| Security, Privacy & Compliance | Authn/authz, secrets, PII, payments, abuse, supply chain, audit или compliance overlay. | Threat surface, risk review, negative tests, secrets/data/privacy evidence, scan status и owner review. |
| Delivery, Release & Operations | Publish, deploy, package, release, automation, incidents или operations readiness. | Release scope, versioning, changelog, artifact manifest, rollout, rollback, SLO/observability и approval evidence. |

Эти 12 methodology domains являются catalog inputs. Cross-domain synthesis является output layer: группирует overlapping recommendations, resolves conflicts, records owner/consumer domains, checks semantic evidence sufficiency и returns risk-aware `safe_next_action`.

Readiness statuses являются explicit: `not_applicable`, `applicable_missing`, `present_unverified`, `present_verified`, `proposal_staged`, `explicit_gap_accepted` и `approval_required`. Detection alone может create только `present_unverified`; readiness требует current evidence, owner review или accepted gap.

## Methodology Examples

| Methodology or practice | Когда включается | Пример применения в Product-Agent OS |
| --- | --- | --- |
| Product discovery and metric design | Product value, launch, growth, onboarding или monetization claims change. | Product hypothesis, value proposition, metric spec, guardrails и owner signoff. |
| Requirements engineering | Behavior, workflow, rules, public contract или multi-slice scope is unclear. | Requirement registry, non-goals, acceptance scenarios, owner questions и traceability. |
| ATDD / BDD acceptance scenarios | User-visible behavior или domain correctness needs shared examples. | Example scenarios linked to tests, evals, manual QA evidence или explicit gaps. |
| DDD | Domain language, bounded contexts, business rules, events, workflows или multi-team ownership matter. | Domain model, ubiquitous language, context map, invariants и domain-to-architecture traceability; simple CRUD не force DDD. |
| Architecture-driven design and ADRs | Quality attributes, runtime topology, contracts, persistence, deployment или trust boundaries change. | Architecture scope, context/container boundaries, tradeoffs, fitness checks, decision records и rollback assumptions. |
| C4 / arc42-style architecture views | Context, container, component, deployment или runtime views are needed. | Architecture overview, trust-boundary map, diagrams и architecture review record. |
| TDD / Red-Green-Refactor | Планируются behavior-changing code, shared logic, bug fixes, migrations, API/schema/UI logic или risky refactors. | Test-first evidence где practical, explicit gap где не подходит, regression evidence привязана к slice. |
| Risk-based testing and QA | Ready/done/fixed/works/release claims требуют evidence. | Unit, integration, contract, runtime, visual, manual QA, CI и flaky-test evidence по blast radius. |
| FSD and frontend boundary discipline | Web UI structure, features, widgets, pages, shared components или frontend ownership boundaries exist. | Feature boundary review, state matrix, visual QA, accessibility, responsive checks и performance budget. |
| API contract-first delivery | OpenAPI, AsyncAPI, GraphQL, gRPC, webhooks, generated clients или external consumers are involved. | API inventory, consumer map, error catalog, auth matrix, compatibility record и contract tests. |
| Eval-driven AI / RAG development | Prompts, models, tools, retrieval, grounding, AI behavior, datasets или safety claims change. | AI behavior spec, baseline eval, prompt contract, model decision, RAG source inventory, rerun evidence и residual risk. |
| Security engineering and release operations | Sensitive data, auth, compliance, deploy, publish, CI/CD, production data или external systems входят в scope. | Threat surface, risk review, privacy impact, release readiness, artifact manifest, rollout, rollback и runbook evidence. |

Packet identifiers и exact contract phrases:

- Security/Privacy/Compliance использует `security_privacy_compliance_contract_present`, `data-classification-register.md` и `vulnerability-response-record.md`.
- Delivery/Release/Operations использует `delivery_release_operations_contract_present`, `release-artifact-manifest.md`, `operations-runbook.md`, `post-release-review.md`, release mode policy и owner-reviewed release evidence sufficiency.
- Cross-Domain Synthesis использует `recommendation_groups`, owner domains, consumer domains, risk-aware safe следующий action и approval-bound behavior.

## Read-Only Process

```mermaid
flowchart TD
    A["Workspace evidence"] --> B["Applicability scan"]
    B --> C["Risk и false-positive check"]
    C --> D["Domain packets"]
    D --> E["Synthesis"]
    E --> F{"Evidence sufficient?"}
    F -->|Yes| G["safe_next_action"]
    F -->|No| H["owner_questions или accepted gap"]
    G --> I{"Создайте required?"}
    I -->|No| J["Только report"]
    I -->|Yes| K["Staged proposal"]
    K --> L["Explicit approval boundary"]
```

## Approval Boundary

Этот staged artifact boundary является strict:

- methodology recommendations может produce report, owner question или staged proposal;
- release, deploy, publish, DB access, security scan, external write, hook activation и automation activation stay blocked пока explicit owner approval и текущий evidence exist;
- generated reports и dashboards являются evidence surfaces, не sources из truth;
- detection alone creates `present_unverified`, не readiness;
- high-risk, production, release, security-sensitive, AI behavior и public-contract work требует owner-reviewed evidence или explicit accepted gap.

## False-Positive Control

Methodology intelligence должен avoid forced ceremony:

- docs-only changes не нужны full product/architecture/release process пока they change public contracts или publishing;
- simple CRUD не force DDD;
- backend/native work не force FSD;
- hosted docs, CI activation и DB introspection остаются approval-required;
- source-like words в file paths являются не enough к infer security, release или data readiness;
- generated artifact является не safety proof пока relevant source или owner evidence является current.

## Проверка

Используйте focused verification когда methodology behavior changes:

```powershell
python -m unittest tests.product_agent_os.test_fixture_eval_runner -v
python plugins\product-agent-os\scripts\run_fixture_eval.py
python tools\check_docs.py
```

Используйте broader verification когда lifecycle skills, templates или routing logic change:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

## Риски

- A read-only audit может still быть wrong если workspace evidence является stale, incomplete или misleading.
- Over-eager methodology routing может force heavy process onto simple work; every recommendation требует applicability и false-positive handling.
- Generated reports может become stale quickly; completion или release claims still нужны fresh command, runtime, eval или owner evidence.
- Domain packet schema может evolve как real projects expose missing fields; additive compatibility следует быть preserved.

Следующий artifact: используйте [Scenarios](scenarios.md) для выбора operating route и [Behavioral evals](behavioral-evals.md) для проверки shortcut resistance.
