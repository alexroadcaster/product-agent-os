# Discovery и графы проекта

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Выберите путь

| Вопрос | Текущий владелец и результат |
| --- | --- |
| Что найдено при первом обследовании? | [Discovery](discovery.md): Python first-run анализ и evidence |
| Какие файлы включены и почему неполно? | [Inventory](inventory.md): отдельные правила Web и Python |
| Какие узлы и связи доступны? | [Модель графа](graph-model.md): Web lexical и Python overlays |
| Где искать путь и возможный impact? | [Queries и impact](queries-impact.md): cursor/revision и bounded packets |
| Какие адаптеры и будущие PoC? | [Adapters](adapters.md): реальные реализации и очередь F26–F34 |

## Два разных пути

Web local service вызывает собственный JS/TS code-index; его HTTP и UI описаны в [API](../api/endpoints.md) и [frontend](../frontend/navigation.md). Python plugin формирует отдельный file graph и overlays через CLI, stage и query packets. Текущий source не устанавливает автоматическую передачу Web snapshot в Python graph или обратное объединение.

[Project Code Graph](../product-agent-os/project-code-graph.md) и [Graph intelligence contract](../product-agent-os/graph-intelligence-contract.md) сохраняют владение Python graph и его evidence boundary. [Retrieval](../ai/rag/index.md) отдельно описывает поиск и semantic cache. Graph `partial`, `stale`, `unresolved` или `unsupported` не доказывает отсутствие зависимости.

## Следующий шаг

Используйте graph как указатель на файлы, затем откройте действительный source и связанные tests; перечень affected tests является кандидатом, а не доказательством достаточности. Реальное дерево файлов, управляемый scan, карта БД и связи кода с таблицами, а также PoC engines остаются в [функциональном плане](../planning/functional-remediation-2026-11-15.md), F26–F34.

Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.
