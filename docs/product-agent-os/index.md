# Product-Agent OS plugin

Source status: `official + experiment`

## Executive overview

Product-Agent OS plugin - локальный Codex plugin для проектов, где Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, hooks, evals и automation candidates должны работать как управляемая delivery-система, а не как набор разовых prompts.

Плагин помогает провести проект через полный lifecycle: read-only workspace audit, требования, план, ownership, staged infrastructure, проверки, review, release packet, learning loop и только затем automation candidate. Он не заменяет owner, не применяет автономные изменения сам по себе и не превращает generated evidence в source of truth.

| Нужно понять | Основная страница |
| --- | --- |
| Как читать generated graph и cockpit | [Project Code Graph](project-code-graph.md) |
| Где проходит live runtime/provider/mutation boundary | [Live Runtime Governance](live-runtime-governance.md) |
| Когда можно переходить к реальному testing | [Approval-Bound Real Testing](approval-bound-real-testing.md) |
| Как спланировать первый pilot на real project | [Real-project pilot](real-project-pilot.md) |
| Как проверять и модернизировать agents/skills | [Agent-Skill Modernization Loop](agent-skill-modernization-loop.md) |
| Какие локальные команды есть у plugin | [CLI Reference](cli-reference.md) |
| Какие результаты получает пользователь | [Витрина результатов](artifact-gallery.md) |
| Какие JSON/HTML/ledger artifacts считаются evidence | [Artifact Contracts](artifact-contracts.md) |
| Как готовить release packet и handoff | [Packaging And Closure](packaging-and-closure.md) |

Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows), [Product-Agent Workflows](../product-agent/overview.md).

## Текущая операционная граница

| Surface | Разрешено без нового approval | Запрещено без отдельного explicit approval |
| --- | --- | --- |
| Static project graph | Read-only scan, staged graph/cockpit, bounded query packets. | Treat generated graph как source of truth или mutate target files из graph evidence alone. |
| Local runtime | Проверить disabled-by-default runtime contract и graph-only fallback. | Запустить live server, expose public routes или add писать endpoints. |
| Provider retrieval | Stage provider gate/eval contracts и threshold fallback. | Perform live external model/API calls или provider calls. |
| Human review и mutation | Stage review ledger, diff preview и dry-run mutation plan. | Mutate canonical graph без accepted owner decision и rollback proof. |
| Audit и real testing | Stage audit/security/observability/readiness packets. | Запустите browser automation, provider pilots, canonical mutation pilots или git release actions. |

## Первый запуск: маршрут пользователя

Первый запуск должен дать не scaffolding, а понятный маршрут. Хороший стартовый prompt:

```text
Use Product-Agent OS for this project: start with a read-only workspace audit, identify lifecycle state, usage_mode, methodology gaps, staged artifacts, verification route, approval boundary and safe_next_action.
```

| Шаг | Что делает plugin | Что получает пользователь |
| --- | --- | --- |
| Read-only audit | Читает project rules, docs, tests, runtime hints и текущий diff без изменений. | Карта контекста, рисков, source boundaries и gaps. |
| Lifecycle state | Определяет, проект в intake, requirements, planning, build, review, release или learning. | Понимание, почему следующий шаг именно такой. |
| Methodology selection | Сопоставляет риски проекта с DDD, TDD, ADD, FSD, eval-driven gates и другими practices. | Нужные методологии включаются как checks и artifacts, а не как догма. |
| Staged artifacts | Предлагает `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` или domain packets только когда они нужны. | Можно проверить output до записи в целевой workspace. |
| Маршрут проверки | Называет команды, evals, runtime-проверки, владельцев и путь отката. | Понятно, чем будет доказана готовность. |
| Approval boundary | Отделяет чтение и staged proposals от live server, browser automation, provider/API calls, canonical mutation и git actions. | `safe_next_action` не перескакивает через approvals. |

Сгенерированные graph, cockpit, dashboard и reports помогают review, но не заменяют исходные файлы, результаты команд и решения владельца. Стоп-линия по умолчанию: нет live server launch, browser automation, provider/API calls, canonical graph mutation или git stage/commit/push/PR без отдельного explicit approval.

## Core capabilities

- Packaged lifecycle skills: orchestrator, discovery auditor, requirements author, implementation planner, team designer, test/eval designer, risk reviewer, release operator, learning loop maintainer и automation promoter.
- Staged infrastructure renderer для control-plane files, project-scoped `.codex/agents/`, hook templates, workflows, eval templates, PR/release templates и automation candidates.
- Safe merge tooling с approval record, manifest validation, workspace-bound paths и rollback support.
- Project Code Graph, bounded query packets и offline cockpit для navigation без treating generated views как truth.
- Live/runtime/provider governance с approval packets, redaction, budget, fallback, audit и staged-only evidence.
- Scenario workflows для first-run intake, bug rescue, greenfield idea shaping, complex system acceleration, PR review readiness, legacy onboarding, API migration, AI/RAG eval regression, native/mobile work, desktop local-first work, data migration, security-sensitive change, CI stabilization и release packaging.
- Engineering standards layer с product hypothesis, architecture boundary, acceptance scenarios, test/eval-first gates, docs-as-code, metric hardening, evidence-before-completion и release measurement.
- Transcript/session eval runner и fixture eval coverage для expected behavior, forbidden behavior, privacy checks и regression replay без external systems.
- Self-verification и modernization loop для agents и skills через self-verification metrics loop `agent_skill_metrics_loop`: target registry, trace intake, dataset quality, grader/judge calibration, scorecard ledger, staged modernization candidates, staged evidence only, нет live eval/model/API calls, нет active schedules и нет self-applied updates.

## Какие боли решает

| Боль | Что делает plugin |
| --- | --- |
| Длинная Codex-сессия теряет контекст | Выносит цель, план, проверки и решения в control-plane files |
| Требования живут только в чате | Создает `REQUIREMENTS.md` со scope, non-goals и acceptance criteria |
| Планирование смешивается с implementation | Требует `PLAN.md`, ownership, verification и rollback до build slice |
| Subagents работают без границ | Проектирует роли через ownership, handoff artifacts и stop conditions |
| Проверки называются задним числом | Разделяет deterministic checks в `TEST.md` и quality gates в `EVALS.md` |
| Агент пишет код без инженерной методологии | Добавляет product hypothesis, architecture boundary, test/eval-first path, влияние на docs и measurement |
| Проектные правила размазаны по memory | Переносит durable rules в `AGENTS.md`, а текущие решения в `RUNLOG.md` |
| Hooks и automations включаются слишком рано | Держит staged-first и candidate-only boundary до ручного approval |
| Невозможно доказать, что работа verified | Требует evidence: команды, fixture evals, политика источников и review findings |

## Кому подходит

| Сценарий | Польза |
| --- | --- |
| Solo developer | Быстро структурировать feature и не потерять acceptance criteria |
| Product engineer | Вести работу от идеи до PR packet через проверяемые artifacts |
| Engineering team | Разделить worktrees, roles и писать scopes без конфликтов |
| AI product team | Добавить eval-driven loop и source/context policy |
| Governed workspace | Сохранить approvals, staged writes, rollback и аудиторский след |

## Основной lifecycle

```mermaid
flowchart LR
    A["Idea"] --> B["Workspace audit"]
    B --> C["REQUIREMENTS.md"]
    C --> D["PLAN.md"]
    D --> E["Agent team"]
    E --> F["Build slice"]
    F --> G["TEST.md / EVALS.md"]
    G --> H["Review"]
    H --> I["PR или release packet"]
    I --> J["RUNLOG.md learning"]
    J --> K["Automation candidate"]
```

Plugin держит lifecycle последовательным. Он не должен перескакивать из `uninitialized` сразу в `build_active`: сначала нужны context, requirements, plan, ownership и quality gates.

## Product workflow gates

| Gate | Когда включается | Что должно появиться |
| --- | --- | --- |
| Workspace discovery | В начале работы или перед сменой scope | Evidence-backed audit, source boundaries, risks и next smallest action |
| Requirements | Перед implementation | Scope, non-goals, acceptance scenarios и evidence owner |
| Planning | Перед build slice | Owned files, forbidden files, commands, expected outputs, rollback и verification |
| Agent/team design | Перед subagents или parallel work | Ownership, handoff artifacts, stop conditions и последовательный fallback |
| Review | Для risky/public-contract/migration/security/data/release work | Spec compliance first, затем quality/risk review |
| Release | Перед publish/PR/package action | Current checks, artifact manifest, rollback, residual risks и explicit owner approval |
| Learning | После meaningful slice | RUNLOG evidence, failures, accepted gaps и modernization candidates |

## Границы

- Plugin работает внутри Codex. Он не требует отдельного OpenAI API key и не запускает standalone Agents SDK runner.
- Infrastructure generation является staged-first: dry-run или staging directory до any target workspace write.
- Hooks являются packaged как templates и examples; they являются не silently activated.
- Automation artifacts являются candidate-only пока manual workflow является stable и explicitly approved.
- Secrets, private customer data, raw private chat logs и local absolute paths должен не попадать в docs, fixtures, prompts, memory или templates.

## Граница public/internal документации

Публичные страницы объясняют возможности, маршрут пользователя, результаты, границы и ближайшее действие. `docs/sources/` хранит внутренние source/history materials, acceptance history и verification packets; этот раздел не должен быть первым маршрутом для нового пользователя. Сгенерированный `site/` является HTML-копией исходных Markdown-документов и поверхностью review, а не источником истины.

Если публичная страница ссылается на graph, dashboard, cockpit, scorecard или report, она должна явно говорить, что это обзорная поверхность. Если claim влияет на readiness, release, security или approval, он должен вести к owning source: исходному файлу, source registry, command/eval/runtime evidence, owner decision или accepted gap.

## Doubt / verifier loop

Doubt / verifier loop - ручной и локальный gate завершения для запросов "проверь еще раз". Пользовательский маршрут описан в [doubt-verification-loop.md](../playbooks/doubt-verification-loop.md): `completion-skeptic` читает `doubt_verification_packet`, сверяет claims, requirements, evidence и accepted gaps, затем возвращает `pass`, `revise`, `needs_more_context`, `blocked_by_approval` или `accepted_risk`.

Эта страница только указывает на gate. Документация фиксирует generated `site` view, а ручные pilots, scorecard calibration и любое продвижение за пределы internal/manual use остаются отдельным этапом.

## Куда идти дальше

- [Технические особенности и установка](technical.md) - реальные файлы, команды, capabilities и install boundary.
- [Витрина результатов](artifact-gallery.md) - какие outputs получает пользователь и где проходит trust boundary.
- [Real-project pilot](real-project-pilot.md) - пакет первого запуска, матрица согласия по целям, метрики успеха и evidence ledger для безопасного pilot на реальном проекте.
- [Engineering standards layer](development-standards.md) - как plugin внедряет DDD/FSD/TDD/ADD, docs-as-code и eval-driven quality без превращения их в dogma.
- [Methodology intelligence](methodology-intelligence.md) - read-only audit, Delivery Map, recommendations, owner questions и staged artifact boundary.
- [Scenarios и usage modes](scenarios.md) - first response, minimum artifacts, approval boundary и verification gates для product scenarios.
- [Behavioral evals](behavioral-evals.md) - expected behavior, forbidden behavior, fixture eval и transcript/session replay.
- [Codex compatibility](codex-compatibility.md) - Codex App, CLI, IDE extension, `.codex-plugin`, skills, MCP и staged hooks support boundary.
- [Диаграммы и принципы работы](architecture.md) - state routing, staged-first merge, approval gates и runtime runner flow.
- [Product-Agent Workflows](../product-agent/overview.md) - общий operating model без привязки к plugin package.
