# Сессии, сообщения и восстановление

Source status: repository_source / static_source_review; 15.11.2026.; FUNC-G05 locally_verified_with_explicit_limits, 16.11.2026.

Владелец: runtime/agent owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении селектора, gateway, контрактов, границ исполнения или связанных тестов. Описанные тесты — маршруты проверки, не новый прогон; фактическая активация и human acceptance требуют отдельного evidence.

## Связь объектов

В Web local service session принадлежит проекту. Binding [app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) связывает projectId, sessionId, режим и canonical workspace identity; выбранный binding сохраняется отдельно. Run и сообщения относятся к этой связи и не являются самим Codex App чатом или доказательством его полной истории. [sessions/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/sessions/service.mts) формирует catalog/transcript/search из local store, скрывает отдельные сообщения и применяет safe persisted text.

## Чтение и состояние

Session history использует scoped snapshot pagination: limit 1–100, snapshot живёт 15 минут, cursor привязан к scope; истечение возвращает stale. Coverage обозначена partial с причиной host_history_not_exposed. История Web — доступная локальная проекция, не полный архив действий App host. [API events](../../api/events.md) описывает другие cursors; их нельзя смешивать. [sessions-team.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/sessions-team.test.mts) — связанный тестовый маршрут, не новый прогон.

[draft-registry.ts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/web/src/api/draft-registry.ts) ведёт message draft по project/session и отделяет отправку от подтверждения. Неопределённый ACK не равен успешному ответу или безопасной очистке ввода; [frontend state](../../frontend/state-management.md) объясняет детали. Публичный runtime snapshot и private claim/report относятся к разным authority boundaries.

## После остановки и рестарта

[app-agent-gateway.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) при восстановлении переводит незавершённые App jobs в recovery_required; pending approvals отменяются, неизвестный dispatch остаётся неопределённым. Для recipe [execution-recipes/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/execution-recipes/service.mts) и [backend recovery](../../backend/recovery.md) владеют checkpoint/reconcile. Новая сессия или видимое окно не доказывают attach, активность модели, восстановление внешней операции или owner acceptance. [recipe-recovery.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/recipe-recovery.test.mts) и [app-agent-gateway.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/app-agent-gateway.test.mts) — связанные тесты. В рамках этой документационной задачи runtime не запускался.

## FUNC-G05 — текущие контракты

F16 paos_history_capability_v1 связывает source adapter paos_local_store, projectId и generation frozen snapshot. localHistory=available, hostHistory=not_connected, loadedProfiles=unavailable. Причина относится к выбранному маршруту, а не ко всем возможностям Codex. Cursor из другого профиля/проекта отклоняется, reconnect не превращает локальные сообщения в полную host history. F11 Usage в сессии использует тот же numeric endpoint, фильтр sessionId и явный UTC период, что и проект/задача/агент.
