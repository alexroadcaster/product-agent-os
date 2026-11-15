# Frontend: состояние, опрос и черновики

Source status: repository_source / static_contract_review; 15.11.2026.

Владелец: frontend и docs-maintainer. Область: Web UI на source revision `ad78d5d15aced23febae90d319f2aba00bd64d0b` (DG04). Пересматривать при изменении состояния, lifecycle, polling, draft ACK или API-контракта. Исходники: [App](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx), [client](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/client.ts), [session polling](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/session-poll.ts), [draft registry](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/draft-registry.ts).

## Кто владеет состоянием

React state в App содержит `ready`, список проектов, выбранные project/section, настройки, connection и временные ссылки на task/session/asset/graph. Локальные состояния форм, фильтров, активных вкладок, busy и errors принадлежат компонентам. Проектные данные, revisions и authority принадлежат local service; их отображение не превращает кэш UI в источник истины. [API](../api/index.md) и [транзакции](../db/transactions.md) описывают серверную сторону.

`createHttpApi` держит CSRF и project authority epochs в памяти, использует same-origin credentials; при `SESSION_REQUIRED` очищает их. Некоторые команды требуют загруженный epoch, revision и idempotency key. Смена локального экрана сама по себе не отменяет уже принятую сервером операцию. UI не обещает атомарности нескольких независимых вызовов.

## Опрос и устаревшие ответы

| Поток | Реализация и граница |
| --- | --- |
| Connection | Один запрос одновременно; следующий через 750 мс после завершения. Версия connection не позволяет ответу прежнего чтения перезаписать более новое изменение; dispose не публикует поздний ответ. |
| Открытая сессия | Runtime и transcript имеют независимые single-flight lanes и общий `AbortController`; таймер runtime — 750 мс после ответа. Transcript загружает максимум 20 страниц по 50, объединяет по ID/revision, сигнализирует `hasMore` и ошибки. При недоступности runtime прежний snapshot ограничивается `canSend:false` и `recovery_required`. |
| Каталоги и graph | [SessionsCatalog](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/sessions/SessionsCatalog.tsx), [ArtifactExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/artifacts/ArtifactExplorer.tsx) и [GraphExplorer](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/graph/GraphExplorer.tsx) используют счётчики запросов, чтобы не применять устаревшие ответы; cursor и revision принадлежат конкретному запросу. |
| Actions / project change | При добавлении проекта `navigationEpoch` не позволяет позднему ответу принудительно изменить выбранный экран/проект после пользовательской навигации. `createLatestRequest` отменяет заменённый запрос и блокирует позднюю публикацию при dispose. Не каждый запрос во всём приложении использует этот helper. |
| Другие менеджеры | Decisions и scheduler используют отдельный периодический опрос, recipes — свой цикл; интервалы и обработка ошибок нужно читать в соответствующем компоненте, а не предполагать единый глобальный polling. |

HTTP events/history — JSON polling и cursor, не SSE; детали и сроки действия отдельных cursors — [API events](../api/events.md). Отмена fetch ограничивает публикацию в UI, но сама по себе не доказывает отмену серверного side effect. Отображение `partial`, `stale`, loading или error нельзя трактовать как полное отсутствие данных.

## Черновик сообщения и ACK

Компонент session получает lease из registry по `(projectId, sessionId)`. Он читает сохранённый draft и revision; [draft autosave](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/draft-autosave.ts) откладывает запись на 500 мс, сериализует optimistic writes и сохраняет key неудачного intent для явного retry. При несовпадающем восстановленном содержимом возникает `DRAFT_RECOVERY_CONFLICT`, а не молчаливое принятие новой revision. Успешная запись требует подтверждённой увеличенной revision.

Перед send registry создаёт ticket с `clientMessageId`; только распознанный ACK инициирует очистку исходного draft. Неопределённый исход сохраняет черновик; сбой очистки отражается отдельно. ACK очереди App-agent не доказывает завершение работы агента. `busy`, выбранный режим, connection, состояние run и валидная цель ограничивают доступность send/interrupt/approve. Подробности маршрута и ограничений — [backend recovery](../backend/recovery.md).

[UI policy](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/policy.ts) блокирует смену scope при неизвестном исходе; сохранённый ID завершённого run сам по себе не является активной блокировкой. Для ответа на approval сверяются binding/run/generation, pending и срок действия, а для accept — reviewable и содержательные детали. Это клиентская предварительная проверка: сервис остаётся владельцем authority и проверок актуальных evidence.

## Черновик формы задачи

[TaskEditor](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/Editor.tsx) хранит структурированный draft в памяти модуля под ключом project/task (для новой задачи — `new`), показывает unsaved и не перезаписывает dirty draft обновлённой серверной entity. Поэтому такой draft может пережить переходы и закрытие детали в той же загруженной странице, но не является сохранением в БД или гарантией после перезапуска. Отдельные локальные поля ввода, reason и preview не входят в эту запись и не следует обещать их сохранение после размонтирования.

Preview передаёт текущую revision и возвращает digest; последующая правка инвалидирует preview. Save отправляет revision и, если есть, digest; ошибки, включая конфликт revision, показываются в форме, а draft удаляется из памяти только после успешного save либо явного discard. Раскрытие/сворачивание detail overlay сохраняет тот же DOM, но переход на другую вкладку может размонтировать editor: нельзя гарантировать сохранность незафиксированных локальных полей. [TaskManager](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/features/tasks/TaskManager.tsx) и [Modal](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/Modal.tsx) владеют этими границами.

## Проверки и ограничения

Связанные тесты: [ui-session-poll.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-session-poll.test.mts), [ui-draft-autosave.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-autosave.test.mts), [ui-draft-registry.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-registry.test.mts), [ui-api.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-api.test.mts). Это ссылки на покрытие, а не новый прогон. Описаны механизмы исходного кода; реальный runtime, browser concurrency и пользовательская приёмка в рамках документационного анализа не доказаны.
