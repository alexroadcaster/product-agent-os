# Diagram atlas

Source status: `official + experiment`

Этот раздел превращает базу знаний из набора статей в рабочую карту реализации проектов через Codex, agents, skills, runtime и eval loops.

Используйте диаграммы не как иллюстрации, а как порядок действий:

1. Начните с [Product-Agent Delivery Lifecycle](product-delivery-lifecycle.md), чтобы понять весь путь от идеи до release.
2. Зафиксируйте [архитектуру планов и задач](../product-agent-os/architecture.md#архитектура-планов-и-задач), если проект требует матрицу задач, поэтапную поставку или отчет после реализации.
3. Перейдите к [Команде агентов и skills](agent-team-and-skills.md), чтобы разложить проект на роли, зоны владения и reusable methods.
4. Используйте [Runtime decision map](runtime-decision-map.md), чтобы выбрать Codex App, CLI, Cloud, `codex exec`, MCP, GitHub Action или automation.
5. Проверьте [границу source и generated evidence](source-generated-trust-boundary.md), если работа опирается на generated graph, cockpit HTML, reports или `site/`.
6. Используйте [архитектуру first-run cockpit](first-run-cockpit-architecture.md), [цикл evidence и risk](evidence-risk-lifecycle.md) и [Architecture Intelligence diagram atlas](architecture-intelligence-diagram-atlas.md), когда first-run выводы превращаются в документацию или handoff.
7. Проверьте [границу skill exposure и invocation](skill-exposure-and-invocation.md), если claim касается source bundle, installed cache или active session behavior.
8. Проверьте [Skill lifecycle](skill-lifecycle.md), прежде чем превращать playbook в skill.
9. Завершите проект через [Context, memory, verification](context-memory-verification.md), чтобы снизить hallucinations и сохранить полезные знания.

## Как читать atlas

Каждая страница отвечает на один практический вопрос:

| Диаграмма | Рабочий вопрос | Главный результат |
| --- | --- | --- |
| Product-Agent Delivery Lifecycle | Как реализовать проект end-to-end? | Понятный путь от идеи до PR/release |
| Архитектура планов и задач | Как создавать, обновлять и очищать файлы-планы? | Плановый контракт для задач, отчетов, evidence и handoffs |
| Команда агентов и skills | Как собрать агентную команду под проект? | Роли, handoffs, candidate skills |
| Runtime decision map | Где запускать задачу Codex? | Выбор runtime-поверхности |
| Source/generated trust boundary | Что является source truth, а что только orientation evidence? | Явная граница generated-view-only, command evidence, owner approval и accepted gap |
| First-run cockpit architecture | Как first-run packet становится cockpit surface? | Artifact flow, evidence gates и browser-proof boundary |
| Evidence and risk lifecycle | Когда claim supported, blocked или unsupported? | Evidence-before-completion route и next safe action |
| Skill exposure and invocation | Почему source skill, installed cache и active session не одно и то же? | Route для source/cache/session proof |
| Architecture Intelligence diagram atlas | Как читать expanded architecture intelligence maps? | First-run flow, graph depth, methodology routing, site sync и Structurizr trigger boundary |
| Skill lifecycle | Когда workflow достоин стать skill? | Проверенный reusable method |
| Context, memory, verification | Как уменьшить hallucinations? | Grounded workflow с проверкой |

## Минимальный рабочий маршрут

Для нового проекта проходите страницы в таком порядке:

```mermaid
flowchart LR
    A["Идея проекта"] --> B["Delivery lifecycle"]
    B --> B1["Архитектура планов"]
    B1 --> C["Команда агентов и skills"]
    C --> D["Runtime decision"]
    D --> E["Source/generated boundary"]
    E --> F["Architecture Intelligence maps"]
    F --> G["Implementation loop"]
    G --> H["Skill exposure boundary"]
    H --> I["Skill lifecycle"]
    G --> J["Context и verification"]
    I --> K["Reusable project methods"]
    J --> L["Product-ready output"]
```

Если после прохождения маршрута у проекта нет `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md` и `RUNLOG.md`, значит workflow еще не готов к автономной или полуавтономной агентной работе.

## Обновление моделей и runtimes

Используйте [матрицу моделей](../codex/models-and-reasoning.md) и [playbook миграции](../playbooks/model-migration.md) вместе с диаграммами команды/runtime. API-возможности и кандидатные модели описаны отдельно от текущей активации Product-Agent OS.
