# Methodologies for Large Projects

Source status: `official + verified methodology + tool-assisted`

Этот раздел задает deep research plan для ведения большого проекта через Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, control-plane artifacts, docs-as-code и eval loops.

Цель раздела - не собрать энциклопедию методологий, а дать рабочую карту: когда методология применима, какие артефакты нужны, какие инструменты документирования выбрать, как проверить результат и где остановиться.

## Почему не хватает frontend/backend/API

Технические разделы отвечают на вопрос "где реализовать". Большой проект еще должен отвечать на вопросы:

- зачем это строится и какая метрика докажет пользу;
- какие требования, business rules и domain terms нельзя потерять;
- какая solution architecture удерживает границы системы;
- какие contracts, data rules, security/privacy constraints и release gates обязательны;
- как агентам безопасно работать через staged artifacts, approvals и current evidence.

## Карта разделов

| Раздел | Главный вопрос | Основной output |
| --- | --- | --- |
| [Business & Product](business-product.md) | Зачем строим и как измеряем ценность? | Product hypothesis, metric spec, guardrails |
| [Requirements & Domain](requirements-domain.md) | Что система должна делать и какие domain rules важны? | Requirements, acceptance scenarios, domain model |
| [Solution Architecture](solution-architecture.md) | Как части системы связаны и где boundaries? | Architecture overview, C4/arc42, ADR |
| [Frontend](frontend.md) | Как строить и документировать UI behavior? | Component docs, Storybook states, visual/a11y checks |
| [Backend](backend.md) | Как управлять business logic, services и reliability? | Service overview, jobs, observability, rollback |
| [API & Integrations](api-integrations.md) | Как сохранить public contracts и compatibility? | OpenAPI/AsyncAPI, contract review, consumer map |
| [Database & Data](database-data.md) | Как менять данные безопасно? | Database dictionary, migration plan, data quality gates |
| [LLM / AI / RAG](llm-ai-rag.md) | Как проверять AI behavior и снижать hallucination risk? | AI eval spec, baseline, grounding evidence |
| [Quality, Testing & Evals](quality-testing-evals.md) | Как доказывать качество до completion claims? | Test/eval matrix, evidence format, gaps |
| [Security, Privacy & Compliance](security-privacy-compliance.md) | Какие security/privacy gates блокируют delivery? | Security risk review, ASVS/SSDF mapping |
| [Delivery, Release & Operations](delivery-release-operations.md) | Как выпускать и поддерживать систему? | Release readiness, SLOs, runbooks, DORA metrics |
| [Codex / Agentic Workflow](codex-agentic-workflow.md) | Как Codex работает в большом проекте без потери context? | Control-plane files, handoffs, automation candidates |

## Единый шаблон deep research

Каждый раздел должен отвечать на одинаковый набор вопросов:

1. `Purpose`: какую проблему большого проекта закрывает раздел.
2. `Applicability`: когда раздел обязателен, optional или not applicable.
3. `Concepts`: какие идеи должен понимать инженер или агент.
4. `Development methodologies`: какие методологии применять и где они вредны.
5. `Documentation artifacts`: какие документы, diagrams, contracts или templates нужны.
6. `Tooling`: какие tools выбрать по stack, scale и ownership.
7. `Verification`: какие tests, evals, builds, checks или reviews дают evidence.
8. `Ownership`: кто owner артефакта, кто reviewer, кто evidence owner.
9. `Risks`: security, privacy, cost, performance, migration, compliance, operational risk.
10. `Codex routing`: какой skill, subagent или workflow запускается и где approval boundary.
11. `Failure modes`: как раздел превращается в бюрократию, stale docs или false confidence.
12. `Promotion path`: когда manual workflow становится playbook, skill, plugin или automation.

## Принцип применения

Для больших проектов используйте lightweight maturity levels:

| Level | Когда подходит | Требование |
| --- | --- | --- |
| `baseline` | MVP, один владелец, низкий риск | Минимальные requirements, plan, tests, runlog |
| `team` | Несколько инженеров или subagents | Ownership, handoffs, architecture boundary, docs impact |
| `production` | Пользователи, данные, release process | Security/privacy review, release readiness, rollback |
| `regulated` | PII, payments, healthcare, finance, enterprise governance | Explicit approvals, audit evidence, source-backed policies |

## Как использовать с Product-Agent OS

- `REQUIREMENTS.md` держит business, product, acceptance и source-of-truth constraints.
- `PLAN.md` держит architecture boundary, slices, exact files, rollback and docs impact.
- `TEST.md` держит deterministic checks, contract checks, runtime checks and accepted gaps.
- `EVALS.md` держит subjective/AI/domain quality gates.
- `RUNLOG.md` держит current evidence, decisions, failures and residual risks.
- `AGENTS.md` держит durable project rules.

## Источники и Context7

Primary sources должны храниться в [source registry](../sources/registry.md). Context7 используется как retrieval layer для developer documentation, но official status сохраняется только если underlying source официальный. Для этого раздела были перепроверены FSD, Storybook и OpenAPI через Context7, а security/operations источники проверены прямым web research 2026-05-24.

