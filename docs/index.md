# Product-Agent OS

[Планы и задачи проекта](planning/index.md): текущие очереди, исторические планы и backlog документации подсистем.

Source status: repository_source (DG02 routing, 2026-11-15) + official/experiment (dated knowledge guides).

## Входы в документацию

| Цель | Маршрут | Результат |
| --- | --- | --- |
| Разрабатывать PAOS | [Карта разработки и владельцы разделов](product/index.md) → [модель продукта](product/overview.md) → [архитектура](architecture/system-context.md) | Текущие контракты, ссылки на код/тесты и владеющие задачи |
| Использовать PAOS | [Plugin guides](product-agent-os/index.md) и [локальный Web/desktop pilot](web/pilot.md) | Поддерживаемые действия и явные ограничения |
| Изучать Codex и методы | [Codex](codex/overview.md), [методологии](methodologies/index.md), [агентные системы](agent-systems/overview.md) | Общие руководства со своими источниками |

Backend/frontend/DB/AI доступны через [карту подсистем](product/index.md), текущая очередь — через [планы](planning/index.md), без чтения исторического RUNLOG. Владелец: docs-maintainer; маршрутизация проверена 15.11.2026 для DG02. При изменении раздела или реализованной capability обновляются оба языка и навигация. Связанные проверки: source documentation, strict MkDocs, site language/search и HTML links.

Приведённые ниже учебные маршруты сохраняют датированную проверку источников; DG02 не перепроверяет каждое внешнее platform claim.


Документация помогает выполнить задачу с Codex, подключить существующий проект или спроектировать agent application. Проверка пользовательских маршрутов по официальной документации: **05.11.2026**. Доступность функций зависит от client, account, auth и managed policy.

## Начните со своей задачи

| Нужно | Первый маршрут | Результат |
| --- | --- | --- |
| Выполнить или исправить одну задачу | [Поверхности](codex/surfaces.md) → [Workflows](codex/workflows.md) | Ограниченный scope, изменение, проверка и итог |
| Подключить свой проект | [Product-Agent OS](product-agent-os/index.md) → [workspace audit](playbooks/workspace-readiness-audit.md) | Read-only discovery и проверяемый staged proposal |
| Построить agent application | [Runtime choice](agent-systems/sdk-patterns.md) → [evals](agent-systems/evals-observability.md) | Явное владение state/tools и критерии качества |

Для обычной правки не требуется новый набор документов или команда. Для сложной работы используйте [Diagram atlas](diagrams/index.md), [lifecycle](product-agent/lifecycle.md) и [model migration](playbooks/model-migration.md). Выбор модели и reasoning: [актуальная матрица](codex/models-and-reasoning.md).

## Что реализовано и что это доказывает

В репозитории реализованы Web/desktop, local service с SQLite и явными runtime routes, а также отдельный Python plugin с lifecycle skills, staged infrastructure, validators, graph/cockpit и eval fixtures. [Возможности и границы evidence](product/capabilities.md) разделяют наличие исходников, датированные проверки и планируемую работу. Наличие этих поверхностей не доказывает hosted delivery, успешную работу на любом проекте или production readiness.

Исходные Markdown, current source/configuration, command/runtime evidence и owner decisions определяют факты. Generated `site/`, dashboards, graphs, cockpit и reports помогают навигации, но не заменяют эти доказательства.

## Источники и история

Официальные материалы OpenAI служат источником platform claims; проектные решения помечены отдельно. Community/experiment не становятся официальной инструкцией без проверки. [Registry](sources/registry.md) · [insights](insights/index.md) · [current state and dated history](product-agent-os/control-plane-current-state.md).

Исторические plans и source receipts сохраняются с датами и не заменяют текущие руководства. Public guides объясняют цель, входы, действия, ожидаемый результат и ограничения.

Внешние записи, Git publication, deployment, provider calls и активация hooks/schedules требуют применимого разрешения. Документация не активирует эти возможности.

## Граница public/internal документации

Внутренние evidence pages сохраняют реестр источников, packets, backlogs и verification records. Источником истины остаются Markdown, текущие code/configuration, наблюдаемые checks и owner decisions. Исторические записи не заменяют актуальные руководства.

## Сопровождение реализации

Используйте [эксплуатацию](operations/index.md), [Python plugin](product-agent-os/index.md) и [матрицу владельцев feature documentation](planning/documentation-architecture-2026-11-15.md#feature-doc-owners). [DG07](planning/documentation-architecture-2026-11-15.md#dg07-results) фиксирует финальную интеграцию документации; датированные platform sources и runtime acceptance сохраняют отдельный scope.
