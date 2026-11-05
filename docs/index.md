# Product-Agent OS

Source status: `official + experiment`

Документация помогает выполнить задачу с Codex, подключить существующий проект или спроектировать agent application. Проверка пользовательских маршрутов по официальной документации: **05.11.2026**. Доступность функций зависит от client, account, auth и managed policy.

## Начните со своей задачи

| Нужно | Первый маршрут | Результат |
| --- | --- | --- |
| Выполнить или исправить одну задачу | [Поверхности](codex/surfaces.md) → [Workflows](codex/workflows.md) | Ограниченный scope, изменение, проверка и итог |
| Подключить свой проект | [Product-Agent OS](product-agent-os/index.md) → [workspace audit](playbooks/workspace-readiness-audit.md) | Read-only discovery и проверяемый staged proposal |
| Построить agent application | [Runtime choice](agent-systems/sdk-patterns.md) → [evals](agent-systems/evals-observability.md) | Явное владение state/tools и критерии качества |

Для обычной правки не требуется новый набор документов или команда. Для сложной работы используйте [Diagram atlas](diagrams/index.md), [lifecycle](product-agent/lifecycle.md) и [model migration](playbooks/model-migration.md). Выбор модели и reasoning: [актуальная матрица](codex/models-and-reasoning.md).

## Что реализовано и что это доказывает

Product-Agent OS — локальный plugin package: lifecycle skills, staged infrastructure, validators, project graph/cockpit и eval fixtures. Он помогает готовить reviewable artifacts; наличие пакета не доказывает hosted delivery, успешную работу на любом проекте или production readiness.

Исходные Markdown, current source/configuration, command/runtime evidence и owner decisions определяют факты. Generated `site/`, dashboards, graphs, cockpit и reports помогают навигации, но не заменяют эти доказательства.

## Источники и история

Официальные материалы OpenAI служат источником platform claims; проектные решения помечены отдельно. Community/experiment не становятся официальной инструкцией без проверки. [Registry](sources/registry.md) · [insights](insights/index.md) · [current state and dated history](product-agent-os/control-plane-current-state.md).

Исторические plans и source receipts сохраняются с датами и не заменяют текущие руководства. Public guides объясняют цель, входы, действия, ожидаемый результат и ограничения.

Внешние записи, Git publication, deployment, provider calls и активация hooks/schedules требуют применимого разрешения. Документация не активирует эти возможности.

## Граница public/internal документации

Внутренние evidence pages сохраняют реестр источников, packets, backlogs и verification records. Источником истины остаются Markdown, текущие code/configuration, наблюдаемые checks и owner decisions. Исторические записи не заменяют актуальные руководства.
