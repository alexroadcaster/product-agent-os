# Архитектура реализации

Source status: repository_source / static_architecture_map; 15.11.2026.

Владелец: архитектура Product-Agent OS; scope/version: DG02 v1. Обновлять при изменении соответствующих исходников, границ данных или решений; связанные проверки указаны ниже. Проверка исходников не доказывает runtime activation или готовность к выпуску.

Эта карта помогает найти исходники и владельца границы для Web/desktop и отдельного Python plugin.

- [Контекст системы](system-context.md) — акторы и внешние границы.
- [Компоненты и процессы](containers.md) — исходники и связанные проверки.
- [Потоки и владение данными](data-flow.md) — authority и переходы.
- [Решения и история](decisions/index.md) — выбор, альтернативы и ограничения.
- [Атлас диаграмм](../diagrams/index.md) и [схема приложения](../diagrams/paos-application-architecture.md).

**Связанные проверки:** [route-selector test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project-source test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts). Ссылки на тесты не доказывают их выполнение в текущем сеансе.

## Backend, API и данные

[Локальный сервис](../backend/index.md), [HTTP-контракты](../api/index.md), [SQLite-схема и жизненный цикл](../db/index.md), [редактируемая SQLite ERD PAOS](../diagrams/paos-sqlite-erd.md). Руководства описывают текущие исходные контракты; карта БД целевого проекта остаётся задачей FUNC-33.

## Реализация frontend

[Frontend и UI/UX](../frontend/index.md) связывает экраны, компоненты, API state, владение дизайном и accessibility evidence с текущими исходниками.

## AI и code intelligence

[Оркестрация агентов](../ai/agents/orchestration.md), [LLM contracts](../ai/llm/index.md), [границы retrieval](../ai/rag/index.md) и [Web/Python graph paths](../code-intelligence/index.md) описывают отдельные текущие surfaces реализации.
