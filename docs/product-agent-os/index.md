# Product-Agent OS plugin

Source status: `official + experiment`

## Executive overview

Product-Agent OS plugin - локальный Codex plugin для проектов, где Codex App, CLI, IDE extension, subagents, skills, `AGENTS.md`, hooks, evals и automation candidates должны работать как управляемая delivery-система, а не как набор разовых prompts.

Плагин помогает провести проект через полный lifecycle: read-only workspace audit, требования, план, ownership, staged infrastructure, проверку, review, release packet, learning loop и только затем automation candidate. Он не заменяет owner, не применяет автономные изменения сам по себе и не превращает generated evidence в source of truth.

| Нужно понять | Основная страница |
| --- | --- |
| Как читать generated graph и cockpit | [Project Code Graph](project-code-graph.md) |
| Где проходит live runtime/provider/mutation boundary | [Live Runtime Governance](live-runtime-governance.md) |
| Когда можно переходить к реальному testing | [Approval-Bound Real Testing](approval-bound-real-testing.md) |
| Как проверять и модернизировать agents/skills | [Agent-Skill Modernization Loop](agent-skill-modernization-loop.md) |
| Какие локальные команды есть у plugin | [CLI Reference](cli-reference.md) |
| Какие JSON/HTML/ledger artifacts считаются evidence | [Artifact Contracts](artifact-contracts.md) |
| Как готовить release packet и handoff | [Packaging And Closure](packaging-and-closure.md) |

Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://developers.openai.com/codex/skills), [Subagents](https://developers.openai.com/codex/subagents), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md), [Codex hooks](https://developers.openai.com/codex/hooks), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex workflows](https://developers.openai.com/codex/workflows), [Product-Agent Workflows](../product-agent/overview.md).

## Current operating boundary

| Surface | Разрешено без нового approval | Запрещено без отдельного explicit approval |
| --- | --- | --- |
| Static project graph | Read-only scan, staged graph/cockpit, bounded query packets. | Treat generated graph as source of truth or mutate target files from graph evidence alone. |
| Local runtime | Validate disabled-by-default runtime contract and graph-only fallback. | Start live server, expose public routes or add write endpoints. |
| Provider retrieval | Stage provider gate/eval contracts and threshold fallback. | Perform live external model/API calls or provider calls. |
| Human review and mutation | Stage review ledger, diff preview and dry-run mutation plan. | Mutate canonical graph without accepted owner decision and rollback proof. |
| Audit and real testing | Stage audit/security/observability/readiness packets. | Run browser automation, provider pilots, canonical mutation pilots or git release actions. |

## Core capabilities

- Packaged lifecycle skills: orchestrator, discovery auditor, requirements author, implementation planner, team designer, test/eval designer, risk reviewer, release operator, learning loop maintainer and automation promoter.
- Staged infrastructure renderer for control-plane files, project-scoped `.codex/agents/`, hook templates, workflows, eval templates, PR/release templates and automation candidates.
- Safe merge tooling with approval record, manifest validation, workspace-bound paths and rollback support.
- Project Code Graph, bounded query packets and offline cockpit for navigation without treating generated views as truth.
- Live/runtime/provider governance with approval packets, redaction, budget, fallback, audit and staged-only evidence.
- Scenario workflows for first-run intake, bug rescue, greenfield idea shaping, complex system acceleration, PR review readiness, legacy onboarding, API migration, AI/RAG eval regression, native/mobile work, desktop local-first work, data migration, security-sensitive change, CI stabilization and release packaging.
- Engineering standards layer with product hypothesis, architecture boundary, acceptance scenarios, test/eval-first gates, docs-as-code, metric hardening, evidence-before-completion and release measurement.
- Transcript/session eval runner and fixture eval coverage for expected behavior, forbidden behavior, privacy checks and regression replay without external systems.
- Self-Verification And Modernization Loop for agents and skills through the self-verification metrics loop `agent_skill_metrics_loop`: target registry, trace intake, dataset quality, grader/judge calibration, scorecard ledger, staged modernization candidates, staged evidence only, no live eval/model/API calls, no active schedules and no self-applied updates.

## Какие боли решает

| Боль | Что делает plugin |
| --- | --- |
| Длинная Codex-сессия теряет контекст | Выносит цель, план, проверки и решения в control-plane files |
| Требования живут только в чате | Создает `REQUIREMENTS.md` с scope, non-goals и acceptance criteria |
| Планирование смешивается с implementation | Требует `PLAN.md`, ownership, verification и rollback до build slice |
| Subagents работают без границ | Проектирует роли через ownership, handoff artifacts и stop conditions |
| Проверки называются задним числом | Разделяет deterministic checks в `TEST.md` и quality gates в `EVALS.md` |
| Агент пишет код без инженерной методологии | Добавляет product hypothesis, architecture boundary, test/eval-first path, docs impact и measurement |
| Проектные правила размазаны по memory | Переносит durable rules в `AGENTS.md`, а текущие решения в `RUNLOG.md` |
| Hooks и automations включаются слишком рано | Ставит staged-first и candidate-only boundary до ручного approval |
| Невозможно доказать, что работа verified | Требует evidence: команды, fixture evals, source policy и review findings |

## Кому подходит

| Сценарий | Польза |
| --- | --- |
| Solo developer | Быстро структурировать feature и не потерять acceptance criteria |
| Product engineer | Вести работу от идеи до PR packet через проверяемые artifacts |
| Engineering team | Разделить worktrees, roles и write scopes без конфликтов |
| AI product team | Добавить eval-driven loop и source/context policy |
| Governed workspace | Сохранить approvals, staged writes, rollback и audit trail |

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
    H --> I["PR or release packet"]
    I --> J["RUNLOG.md learning"]
    J --> K["Automation candidate"]
```

Plugin держит lifecycle последовательным. Он не должен перескакивать из `uninitialized` сразу в `build_active`: сначала нужны context, requirements, plan, ownership и quality gates.

## Product workflow gates

| Gate | Когда включается | Что должно появиться |
| --- | --- | --- |
| Workspace discovery | В начале работы или перед сменой scope | Evidence-backed audit, source boundaries, risks and next smallest action |
| Requirements | Перед implementation | Scope, non-goals, acceptance scenarios and evidence owner |
| Planning | Перед build slice | Owned files, forbidden files, commands, expected outputs, rollback and verification |
| Agent/team design | Перед subagents или parallel work | Ownership, handoff artifacts, stop conditions and sequential fallback |
| Review | Для risky/public-contract/migration/security/data/release work | Spec compliance first, then quality/risk review |
| Release | Перед publish/PR/package action | Current checks, artifact manifest, rollback, residual risks and explicit owner approval |
| Learning | После meaningful slice | RUNLOG evidence, failures, accepted gaps and modernization candidates |

## Границы

- Plugin работает внутри Codex. Он не требует отдельного OpenAI API key и не запускает standalone Agents SDK runner.
- Infrastructure generation is staged-first: dry-run or staging directory before any target workspace write.
- Hooks are packaged as templates and examples; they are not silently activated.
- Automation artifacts are candidate-only until manual workflow is stable and explicitly approved.
- Secrets, private customer data, raw private chat logs and local absolute paths must not попадать в docs, fixtures, prompts, memory or templates.

## Куда идти дальше

- [Технические особенности и установка](technical.md) - реальные файлы, команды, capabilities и install boundary.
- [Engineering standards layer](development-standards.md) - как plugin внедряет DDD/FSD/TDD/ADD, docs-as-code и eval-driven quality без превращения их в dogma.
- [Methodology intelligence](methodology-intelligence.md) - read-only audit, Delivery Map, recommendations, owner questions and staged artifact boundary.
- [Scenarios and usage modes](scenarios.md) - first response, minimum artifacts, approval boundary and verification gates for product scenarios.
- [Behavioral evals](behavioral-evals.md) - expected behavior, forbidden behavior, fixture eval and transcript/session replay.
- [Codex compatibility](codex-compatibility.md) - Codex App, CLI, IDE extension, `.codex-plugin`, skills, MCP and staged hooks support boundary.
- [Диаграммы и принципы работы](architecture.md) - state routing, staged-first merge, approval gates and runtime runner flow.
- [Product-Agent Workflows](../product-agent/overview.md) - общий operating model без привязки к plugin package.
