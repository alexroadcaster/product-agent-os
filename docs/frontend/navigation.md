# Frontend: навигация и экраны

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: frontend и docs-maintainer. Область: Web/desktop UI, source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Обновлять при изменении разделов, переходов, onboarding или связанных UI-тестов. [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx) и [Sidebar.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Sidebar.tsx) — источники текущего поведения; [API](../api/index.md) владеет HTTP-контрактами.

## Вход и выбор проекта

После инициализации UI получает сессию, список проектов, настройки и состояние connection. Без сессии показывается форма pairing; ошибка показывается пользователю, а разделы меню отключены до `ready`. После входа сохраняется выбранный существующий проект либо выбирается первый. Если проекта нет, project-specific разделы показывают пустое состояние; Settings и портфель доступны отдельно. Header содержит breadcrumb, поиск, connection status и reload.

В sidebar 15 разделов, сгруппированных под Work, Knowledge, Management и Workspace. Выбор проекта и раздела меняет React state; это не набор самостоятельных URL-маршрутов. Sidebar можно свернуть; механизм узкого layout закрывает меню после выбора, а Escape возвращает фокус к кнопке меню. `aria-current` отмечает активную страницу. Это описание механизма не расширяет desktop scope дизайна; подробности и ограничения — [accessibility](accessibility.md).

## Карта текущих разделов

| Идентификатор | Экран и переходы | Вход в код |
| --- | --- | --- |
| `portfolio` | Все проекты; карточка ведёт к overview, задачам или агентам проекта | [Dashboard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/dashboard/Dashboard.tsx) |
| `overview` | Вкладки dashboard, sources и usage; переходы к задачам и агентам | App и Dashboard |
| `tasks` | Реестр и детали задач; переход к связанной сессии | [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) |
| `sessions` | Каталог, история и просмотр сессии; переход к задаче или агенту | [SessionsCatalog](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/sessions/SessionsCatalog.tsx) |
| `agents`, `skills` | Каталоги команды, карточки assets и связанные задачи/сессии | [TeamManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/team/TeamManager.tsx) |
| `projectMap` | Текущий граф, выбор узла, статические связи и исходный фрагмент при доступности | [GraphExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphExplorer.tsx) |
| `documents`, `checks`, `search` | Каталог артефактов в трёх режимах; переход к задаче, сессии или узлу графа | [ArtifactExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/artifacts/ArtifactExplorer.tsx) |
| `autonomy`, `decisions` | Политика автономности и очередь решений | [AutonomyManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/autonomy/AutonomyManager.tsx), [DecisionBoard](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/decisions/DecisionBoard.tsx) |
| `import`, `backup` | Импорт задач и управление backup | [Operations](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Operations.tsx) |
| `settings` | Настройки интерфейса, connection, добавление проекта и workflow surfaces | App, [ProjectOnboarding](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/projects/ProjectOnboarding.tsx), [WorkflowManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/workflows/WorkflowManager.tsx) |

Внутренние переходы передают project/task/session/asset/node IDs через состояние App. Поддерживаемый hash-anchor для сообщения содержит `project`, `session`, `message`; проект проверяется по списку, длина и допустимые символы идентификаторов ограничены. Это не общая гарантия deep links для любого экрана. Детали, формы и модальные окна принадлежат соответствующим компонентам; закрытие или потеря focus не равносильны подтверждению операции.

Деталь задачи в [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) можно раскрыть в overlay и свернуть обратно: [DetailSurface](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Modal.tsx) переносит тот же DOM в modal top layer, сохраняя ввод. Удаление задачи и выбор целевого перехода открывают отдельные dialog; удаление требует явной отметки и не выполняет каскадное удаление связанных записей. Escape и закрытие закрывают/сворачивают соответствующую поверхность, не подтверждая действие.

## Добавление проекта и границы текущей карты

В Settings пользователь выбирает папку системным picker либо вводит root, задаёт имя и подтверждает добавление. Пока выбор не подтверждён, это draft. UI передаёт `scan:true`, показывает состояние добавления и результат `ready`/`partial`, counts и доступность источников, если они вернулись. Ошибка, отмена picker и повтор отправки имеют отдельные состояния. Source inspection ограничен; это не полный браузер каталога.

Текущая `projectMap` — существующий ограниченный граф, а не обещание полной карты зависимостей. Полное дерево Files, управляемое сканирование, новые Map/Database views, карта целевой БД и code-to-table usages остаются в [FUNC-26–34](../planning/functional-remediation-2026-11-15.md) как planned. Вкладка файлов задачи и показ источников не доказывают существование полноценного дерева проекта. `partial` или `stale` не означают отсутствие файла или зависимости.

## Проверки и ограничения

Связанные маршруты проверок: [ui-v3-dashboard.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-dashboard.test.mts), [ui-v3-diagram.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-v3-diagram.test.mts), [ui-task.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-task.test.mts), [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/sessions-team.test.mts). Ссылки на тесты не означают их новый запуск или человеческую приёмку. Состояния компонентов и API могут измениться; обновлять эту карту вместе с кодом и RU/EN-парой.
