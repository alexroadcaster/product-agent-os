# Доступ, валидация и ошибки

Source status: repository_source / static_contract_inventory; 15.11.2026.

Владелец: local-service/API; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении session gate, bootstrap, body parser или error mapping. [API](index.md) · [маршруты](endpoints.md).

## Границы доступа

[session-gate](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts) принимает origin вида `http://127.0.0.1:{port}` с точным Host; forwarded host и cross-site отклоняются. Mutation требует точный `Origin` и `x-paos-csrf`. Session cookie имеет `HttpOnly`, `SameSite=Strict`, `Path=/`; idle timeout — 30 минут, absolute — 8 часов, не более 64 активных сессий. Restart/re-pair аннулирует их. Эти проверки не являются изоляцией от native HTTP-клиентов ОС.

[Browser launch](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/browser-launch.mts) требует direct navigation с Fetch Metadata, одноразового proof и cookie; `/bootstrap/exchange` — одноразовый pairing code (60 секунд, максимум пять попыток). `/health` не требует session. `/agent/v1` — отдельный внутренний capability channel: Bearer токен из профильного descriptor, exact origin, POST и JSON до 65536 bytes. Browser cookie не даёт эту authority. [Agent channel source](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/app-agent-channel.mts).

## JSON и общие ошибки

[Handler](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts) требует JSON object; default body limit 1 MiB, upload 70 MiB, task-manager commands 16 MiB, team proposal preview/apply 8 MiB, imports preview 3 MiB; desktop picker 8192 bytes, app handoff 4096, launch proof 1024. Конкретные domain validators могут быть строже.

| HTTP status | Условие / код |
| --- | --- |
| 400 | `INVALID_REQUEST` и остальные коды, не попавшие в категории ниже |
| 401 | `SESSION_REQUIRED`, `PAIRING_INVALID` |
| 403 | `ORIGIN_REJECTED`, `CSRF_INVALID`, `LAUNCH_REJECTED` |
| 404 | код содержит `NOT_FOUND` |
| 409 | код содержит `CONFLICT`, `REQUIRED`, `UNAVAILABLE`, `AUTHORITY`, `FORBIDDEN`, `BLOCKED`, `UNVERIFIED`, `UNQUALIFIED`, `DRIFT`, `BUSY`, `STALE` или `PRIVATE` |
| 413 / 415 | `REQUEST_TOO_LARGE` / `JSON_REQUIRED` |

Ответ ошибки: `{ "error": { "code": "REVISION_CONFLICT" } }`. Для безопасного `cyclePath` может добавляться ограниченный `details`. Это синтетическая форма; клиент должен читать код, а не раскрывать содержимое исключения. Private agent channel имеет собственное сопоставление 401/403/404/405/409/413/415. См. [service-api tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts) и [client](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts). Наличие tests не доказывает их текущий прогон.
