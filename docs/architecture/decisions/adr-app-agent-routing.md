# ADR — App-agent и API routing

Source status: repository_source / static_architecture_map; 15.11.2026.

Владелец: архитектура Product-Agent OS; scope/version: DG02 v1. Обновлять при изменении соответствующих исходников, границ данных или решений; связанные проверки указаны ниже. Проверка исходников не доказывает runtime activation или готовность к выпуску.

## Статус и происхождение

[Архитектура §21.9](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) фиксирует решение владельца от 11.11.2026: default — Codex App agent; API BYOK остаётся отдельной compatibility-веткой. Ранний App Server-only baseline ниже по истории не следует считать текущим default. [Selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts) задаёт оба route и отсутствие implicit fallback; переданный API key выбирает API route, если route не указан. Исторический receipt не доказывает текущее подключение или readiness.

## Контекст и rationale

Нужен согласованный маршрут для работы через Codex App без требования API key и отдельная явно выбранная совместимость с API. Переключение маршрута требует соблюдения состояния соединения и unresolved runs; ожидание consumer не равно завершённому выполнению.

## Альтернативы и последствия

Исторический автономный App Server-first подход имел иные условия closed-App; отдельный API client требует явного выбора и собственной credential authority. Прозрачный fallback скрывал бы смену runtime и credential boundary; selector в исходниках его не выполняет. Это обоснование — вывод из зафиксированных границ. App route требует активного consumer; route metadata не подтверждает entitlement, native sandbox или успешный model call.

**Связанные проверки и обновление:** [route test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [gateway test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/app-agent-gateway.test.mts); [источник gateway](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-gateway.mts). Пересмотреть при изменении селектора, модели authority или нового решения владельца; проверять реальную активацию только при соответствующем разрешении.
