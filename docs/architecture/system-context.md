# Контекст системы

Source status: repository_source / static_architecture_map; 15.11.2026.

Владелец: архитектура Product-Agent OS; scope/version: DG02 v1. Обновлять при изменении соответствующих исходников, границ данных или решений; связанные проверки указаны ниже. Проверка исходников не доказывает runtime activation или готовность к выпуску.

Пользователь работает в Web SPA через локальный service; launcher управляет локальным запуском и профилем. Реализация и состав пакета описаны в [desktop contract](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/desktop-local/README.md). Исходники и привязка конкретной установки важнее наличия схемы.

| Участник / граница | Ответственность | Источник и ограничение |
| --- | --- | --- |
| Пользователь и браузер | Проекты, задачи, документы и запросы | [React App](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/web/src/ui/App.tsx); UI не предоставляет произвольное право записи |
| Local service | HTTP, сессия, доменные операции и маршрутизация | [application](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/http/application.mts), [startup](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/main.mts); права не наследуются автоматически из UI |
| Профиль и project workspace | SQL-состояние профиля и отдельно исходные файлы | [source adapter](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/adapters/project-sources.ts); authority зависит от режима проекта |
| Codex App и API BYOK | Различные runtime routes с явным выбором | [selector](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/runtime/route-selector.ts); автоматического перехода на другой route нет |
| Python plugin | Отдельный пакет discovery, staged infrastructure и lifecycle | [plugin README](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/plugins/product-agent-os/README.md); не утверждается, что каждый запрос Web вызывает Python |

[Схема в атласе](../diagrams/paos-application-architecture.md) показывает связи. Доступность runtime, прав и модели зависит от среды; локальный package не доказывает hosted delivery или самостоятельную работу при закрытом Codex App.

**Проверки и источник:** [route selector test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project sources test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [историческая архитектура](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md). История содержит superseded решения; см. [реестр](decisions/index.md).
