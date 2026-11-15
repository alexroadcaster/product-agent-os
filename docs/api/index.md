# HTTP API и контракты

Source status: repository_source / static_contract_inventory; 15.11.2026.

Владелец: maintainers local-service/API; scope/version: DG03, commit `2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765`. Обновлять при изменении handlers, middleware, client, contracts, events или связанных tests. Это локальный API конкретной версии исходников, не публичное облачное API и не гарантия runtime-доступности.

1. [Справочник endpoints](endpoints.md): методы, пути, request/response, побочные эффекты, ограничения и ссылки на service contracts.
2. [Доступ и ошибки](errors.md): loopback, session, CSRF, body limits и безопасная обработка отказов.
3. [События и история](events.md): JSON replay, audit, cursor и граница runtime-событий.
4. [Backend и lifecycle](../backend/index.md), [план функций](../planning/functional-remediation-2026-11-15.md), [реестр источников](../sources/registry.md).

Источники: [HTTP application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [session gate](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/session-gate.mts), [Web client](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/api/client.ts), [service API test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/service-api.test.mts). Связанные tests названы как источники контракта, а не как новый прогон. OpenAPI отсутствует до решения о поддерживаемом генераторе; не запускайте скрипты анализируемого проекта для построения схемы.

Примеры синтетические. Переменная `BASE` ниже обозначает адрес локального тестового экземпляра, а не инструкцию обращаться к пользовательскому профилю.

```http
GET /api/v1/projects/{projectId}/entities?kind=task&limit=20&offset=0 HTTP/1.1
Host: 127.0.0.1:{port}
Cookie: <synthetic-session-cookie>
```

Результат: JSON `{ "items": [], "hasMore": false }` для пустой фикстуры — иллюстрация формы, не receipt. Для успешного запроса необходима предварительно выданная сессия. Не сохраняйте cookie, CSRF, bearer или содержимое приватных проектов в примерах.
