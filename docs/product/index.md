# Разработка Product-Agent OS

Source status: repository_source / current_source_inspection / documentation_implementation; DG02/DG03, 15.11.2026.

Владелец: docs-maintainer; владельцы доменов указаны ниже. Область: маршрутизация документации Web/desktop, local service и Python plugin на `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Пересматривать карту при изменении раздела, контракта, владельца задачи или capability.

## Три входа

- Разработка PAOS: эта карта → [продукт](overview.md) → [архитектура](../architecture/system-context.md) → владеющий исходник/тест/задача.
- Использование PAOS: [plugin/operator guides](../product-agent-os/index.md), [Web pilot](../web/pilot.md), [доступность](../web/accessibility.md).
- Знания о Codex и методах: [Codex](../codex/overview.md), [методологии](../methodologies/index.md), [агентные системы](../agent-systems/overview.md). Общие методы не доказывают runtime-возможности PAOS.

## Найти подсистему

Сейчас доступны существующие входы с опорой на исходники. Backend, API и DB описаны в DG03; frontend и AI guides закреплены за следующими группами. Все ID ниже ведут к [плану документации](../planning/documentation-architecture-2026-11-15.md) или [функциональному плану](../planning/functional-remediation-2026-11-15.md).
| Область | Текущее руководство | Вход в исходники | Владелец подробного руководства / очередь |
| --- | --- | --- | --- |
| Backend / API | [Локальный сервис](../backend/index.md), [справочник API](../api/index.md) | [HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) | DOCS-04/05, DG03 |
| Frontend / UI | [Сценарии](user-journeys.md), [возможности](capabilities.md) | [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/ui/App.tsx) | DOCS-06, DG04 |
| DB / SQLite | [Схема SQLite](../db/schema.md), [жизненный цикл данных](../db/index.md) | [Schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts) | DOCS-07, DG03 |
| AI / agents / LLM | [Границы системы](../architecture/system-context.md), [runtime routes](../architecture/decisions/adr-app-agent-routing.md) | [Route selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) | DOCS-08/09, DG05 |
| RAG / retrieval / code intelligence | [Capabilities](capabilities.md), [plugin graph](../product-agent-os/project-code-graph.md) | [FTS search](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/search-queries.mts) | DOCS-10/11, DG05; FUNC-14/26–34 отдельно |

## Владение документацией и обновления

| Разделы | Назначение | Ответственная роль | Авторитетный источник / вход | Событие обновления |
| --- | --- | --- | --- | --- |
| `product/` | Текущая модель, возможности и сценарии PAOS | product-manager | Contracts и код; [capabilities](capabilities.md), [задачи](../planning/index.md) | Изменение поведения или статуса capability |
| `architecture/`, `architecture/decisions/` | Границы компонентов и обоснование решений | architect | Исходники, принятые решения и их evidence; [архитектура](../architecture/system-context.md) | Изменение процесса, authority, хранения или маршрута |
| `backend/`, `api/`, `db/` | Жизненный цикл сервиса, HTTP-контракты, SQLite и восстановление | backend/storage owner + docs-maintainer | [Backend](../backend/index.md), [API](../api/index.md), [DB](../db/index.md); связанные исходники и тесты | Изменение модуля, endpoint, схемы, транзакции или recovery-контракта |
| `diagrams/` | Единый атлас исполняемых путей и границ | architect + owner подсистемы | Связанный source-backed guide; [атлас](../diagrams/index.md) | Изменение потока; схема и RU/EN проверяются вместе |
| `product-agent-os/`, `web/` | Использование plugin, доступность Web и local pilot | docs-maintainer + owner реализации | [Plugin guides](../product-agent-os/index.md), [pilot](../web/pilot.md), текущий код и датированные receipts | Изменение команды, UI, установки или ограничения |
| `product-agent/`, `playbooks/` | Метод работы и повторяемые пользовательские маршруты | lifecycle-orchestrator | Workflow/skill source; [lifecycle](../product-agent/lifecycle.md) | Изменение маршрута или границ ответственности |
| `codex/`, `runtime/`, `agent-systems/`, `prompting/` | База знаний о Codex и проектировании агентов | research-source-analyst + docs-maintainer | Официальные источники в [registry](../sources/registry.md); проектные выводы помечаются отдельно | Изменение внешнего контракта; проверка источника и даты |
| `methodologies/`, `artifact-templates/`, `templates/` | Методологии и повторно используемые образцы | owner методологии + docs-maintainer | [Методологии](../methodologies/index.md), canonical template source | Изменение применимости или контракта; пример не считается реализацией |
| `planning/` | Очереди, карточки, зависимости и статусы | product-manager + owner задачи | Owning MD/JSON в [каталоге](../planning/index.md); root PLAN только маршрутизирует | Изменение scope, зависимости, статуса или evidence |
| `sources/`, `evidence/`, `release/`, `superpowers/` | Источники, датированные проверки и проектные решения | owner проверки/решения + release-operator | Первичный receipt/manifest/spec; [registry](../sources/registry.md) | Новый результат добавляет provenance; прежний результат не переписывается как свежий |
| `insights/` | Неподтверждённые community/experiment наблюдения | research-source-analyst | [Insights](../insights/index.md) с trust_level/verification_status | Новая проверка или изменение источника |
| `assets/` | Оформление и локальные ресурсы сайта | docs-maintainer | mkdocs.yml, исходные assets и лицензии | Изменение отображения; сборка и соответствующие render checks |

Роли назначают ответственность в репозитории, но не доказывают запуск агента. Каждая содержательная страница указывает source status, scope/date, ссылки на исходники/тесты и ограничения. Runtime-поведение определяется кодом и применимыми наблюдаемыми проверками; статус задачи — владеющим plan/JSON; приёмка — решением владельца.

## Как обновлять документацию

1. Проверить изменённый контракт, текущий код, callers и связанные тесты. Найти каноническую страницу по таблице.
2. Обновить её и полноценную RU/EN-пару; добавить ссылку с квалифицированным статусом вместо второго независимого требования.
3. Обновить навигацию и registry при изменении маршрута или утверждений с источниками. Сохранить датированные research, решения и receipts; извлекать актуальное руководство с provenance, не удалять историю.
4. Выполнить затронутые source/link/matrix checks. Изменения навигации или render требуют isolated strict build, language-link postprocess и site checks. Изменения диаграмм дополнительно требуют соответствующей parser/render проверки.
5. Записать evidence в owning task; закрывать только выполненный scope. Дальнейший порядок — [очередь документации](../planning/documentation-architecture-2026-11-15.md).

## Доказательства и ограничения

DG02 описывает существующую реализацию и создаёт документацию; live providers, все пользовательские journeys, commercial release и реализация FUNC/M5 этим не подтверждаются. Каталог нового домена появляется вместе с содержательными страницами, без пустых placeholders. Исторические research/PRD доступны через provenance обзора и ADR. [Registry источников](../sources/registry.md) и [атлас диаграмм](../diagrams/index.md) сохраняют своё назначение.

Связанные проверки: `tools/check_docs.py`, `tests/product_agent_os/test_product_agent_os_docs.py`, `tests/product_agent_os/site_checks.py`; матрицы и HTML links проверяются в результатах DG02 владеющего плана.
