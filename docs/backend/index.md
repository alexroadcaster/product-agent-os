# Backend: local service

Source status: repository_source / static_source_review; 15.11.2026.

Владелец: backend/local-service с владельцами storage и runtime. Scope/version: DG03, snapshot `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении entrypoint, маршрута, очереди, записи или восстановления; source и test links ниже относятся к этому snapshot.

## Область и маршрут чтения

Local service — Node-процесс PAOS Web/desktop: он связывает loopback HTTP, сервисы задач, storage Worker, scheduler, recipes и выбранный runtime. [main.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts) создаёт эти зависимости; [application.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) маршрутизирует запросы. SQLite находится в отдельном Worker thread, а не в отдельном сетевом сервере. [Python plugin](../product-agent-os/index.md) — отдельный пакет, а не обязательная часть каждого Web-запроса. [Контекст приложения](../architecture/system-context.md) определяет общие границы.

- [Модули и владение](modules.md): границы между handler, domain service, Worker и runtime, включая текущую связанность UI/backend.
- [Жизненный цикл](lifecycle.md): запуск, session gate, отвод запросов, завершение.
- [Команды и события](commands-events.md): revision, idempotency, event/outbox и порядок записи.
- [Восстановление](recovery.md): cancellation, неизвестный результат, restart и безопасное продолжение.

## Смежные контракты

[HTTP API](../api/index.md), [SQLite и данные](../db/index.md), [product journeys](../product/user-journeys.md) и [план F08](../planning/functional-remediation-2026-11-15.md) дают подробности владельцев. Требования и текущий статус каждой доработки остаются в её карточке, а не выводятся из существования этой документации.

## Проверки и ограничения

Связанные contract tests: [runtime-route-selector.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [scheduler-runtime.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/scheduler-runtime.test.mts), [runtime-sqlite.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-sqlite.test.mts), [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/recipe-recovery.test.mts), [runtime-adapter-shutdown.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-adapter-shutdown.test.mts). Это ссылки на релевантные тесты, не утверждение о новом запуске. Source inspection не доказывает активность App consumer, provider access, текущую работоспособность конкретного профиля, human acceptance или release readiness.
