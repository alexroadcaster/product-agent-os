# Адаптеры и будущие интеграции

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: graph-cockpit-engineer + docs-maintainer. Область: DG05 / DOCS-11, snapshot `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении scanner, API, adapters, query contracts, тестов или статуса PoC. Результаты графа — производное evidence для навигации, не замена чтению исходников и проверкам.

## Реализованные локальные адаптеры

[project_graph_adapters.py](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/plugins/product-agent-os/scripts/product_agent_os/project_graph_adapters.py) содержит `python_ast`, `typescript_javascript_stdlib` и `unsupported_file`. Python AST строит package/symbol/import/call/test overlays, ограниченный JS/TS adapter распознаёт выбранные экспортные и импортные source patterns; для файлов больше 1 000 000 байт и generated-файлов языковой overlay не строится. `unresolved` — сохранённая неопределённость, а не подтверждённая зависимость.

Web использует отдельный [parser worker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/parser-worker.mts) и [lexical builder](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/code-index/lexical.mts); это не запуск Python adapter. Python scanner имеет staged generated artifacts, optional local indexes и отдельные approval-bound extension gates. Это разные контракты, хранилища и пределы доказательств.

## Запланированные решения

| Инициатива | Статус и ожидаемая работа |
| --- | --- |
| F26–F29: Files / scan / inventory / discovery | planned: отдельная директория, управляемый scan и UI/UX |
| F30 dependency-cruiser | planned PoC для анализа JS/TS зависимостей |
| F31 codebase-memory-mcp | planned PoC graph/agent navigation |
| F32 tbls | planned PoC документации схемы целевой БД |
| F33/F34 | planned: карта целевой БД и связи кода с таблицами, с отображением и evidence |

Точные acceptance, licensing и integration gates принадлежат [функциональному плану](../planning/functional-remediation-2026-11-15.md). Упоминание проекта здесь не означает установку, выполнение PoC, интеграцию с Web или разрешение на подключение к реальной БД. После выполнения конкретной FUNC задачи её владелец обновляет эти страницы и source registry.

Существующие AI adapters и query-quality границы описаны в [retrieval](../ai/rag/index.md). Связанные тесты: [Web code index](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/code-index.test.mts), [Python graph queries](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_queries.py), [Python overlays](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/product_agent_os/test_project_graph_overlays.py). Это маршруты проверки, а не утверждение о новом прогоне.
