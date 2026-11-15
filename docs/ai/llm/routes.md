# Выбор LLM/runtime route

Source status: repository_source / current_source_inspection; DG05, 2026-11-15.

Владелец: runtime/LLM owner + docs-maintainer. Область: реализация PAOS на `61f6cd4cd048be478e88e2406c733f98b60bc434`. Обновлять при изменении route, prompt/output, credentials, budget или telemetry контрактов. Ссылки на тесты — маршруты проверки, не новый runtime-прогон.

## Selector и ответственность

[createRuntimeRouteSelector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/route-selector.ts) сериализует connect/disconnect/dispatch. Явное `route` имеет приоритет; без него наличие поля `apiKey` выбирает `local_api_byok`, иначе `codex_app_agent`. App route не принимает `apiKey`/`remember`. Переключение engaged route требует disconnect (`ROUTE_DISCONNECT_REQUIRED`); профиль и чужие unresolved runs проверяются до допуска. Ошибка не переключает на другой gateway.

| Route | Реальный путь | Граница доказательства |
| --- | --- | --- |
| `codex_app_agent` | [App gateway](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/app-agent-gateway.mts) → attached consumer/lease → claim/report и domain operations | Выбор и host lease не предоставляют model authentication; `modelAccess` остаётся `unverified`, инструменты всего App host не ограничиваются этим gateway |
| `local_api_byok` | [Live gateway](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/live-gateway.mts) → qualified RPC → initialize → broker API-key login → coordinator | Успешная auth не доказывает доступ к модели; manifest/profile/policy gates могут отказать до dispatch |

## Credentials и сбои

[Connection broker](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/connections/broker.ts) выполняет `account/login/start` с `type: apiKey`, затем проверяет `account/read`. `remember` требует secure store; [Windows credential store](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/connections/windows-credential-store.ts) использует ограниченный target PAOS/profile/connection и передаёт secret через stdin bridge. Здесь нет примеров ключей и не читаются пользовательские credentials. Broker сохраняет приватный набор прежних secrets для redaction поздних кадров; это не DTO и не telemetry.

При failed connect broker пытается logout и возвращает безопасный код; inherited auth fallback отсутствует. Обычный gateway disconnect вызывает broker.disconnect без `forget`: disconnect не следует документировать как удаление сохранённого credential. Закрытие RPC сбрасывает connected state; неизвестный исход dispatch требует recovery/reconcile, а не автоматического replay. [Recovery](../../backend/recovery.md).

## Model/effort и внешний контракт

[Team pins](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/team/service.mts) различает `requestedModel`/`requestedEffort` и `observedModel`/`observedEffort`, которые здесь равны null. [Coordinator](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/apps/local-service/src/runtime/codex/coordinator.ts) задаёт fixed recipe и `allowProviderModelFallback:false` при thread/start; просмотренный turn/start не передаёт отдельные model/effort overrides. Нельзя выводить effective model из pinned asset.

Официальные [Authentication](https://developers.openai.com/codex/auth) и [App Server](https://developers.openai.com/codex/app-server) проверены 15.11.2026: описывают ChatGPT/API-key authentication и API-key RPC login; protocol содержит model/reasoning capabilities. Это внешний контракт, а не доказательство поддержки всех вариантов PAOS. Установленный adapter и qualification остаются локальными владельцами совместимости.

Проверки: [route selector](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/runtime-route-selector.test.mts), [connections](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/connections.test.mts), [auth route](https://github.com/alexroadcaster/product-agent-os/blob/61f6cd4cd048be478e88e2406c733f98b60bc434/tests/web/auth-route.test.mts). В DG05 выполнена source review, не auth/model вызов.
