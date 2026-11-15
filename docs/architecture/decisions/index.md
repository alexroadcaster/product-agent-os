# Реестр архитектурных решений

Source status: repository_source / static_architecture_map; 15.11.2026.

Владелец: архитектура Product-Agent OS; scope/version: DG02 v1. Обновлять при изменении соответствующих исходников, границ данных или решений; связанные проверки указаны ниже. Проверка исходников не доказывает runtime activation или готовность к выпуску.

Исторический [архитектурный документ](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) сохраняется без переноса и содержит исходные ADR-W01–W09 и последующие уточнения. Его ранние схемы и статусы относятся к соответствующим датам и могут быть superseded. Ниже извлечены решения с установленным provenance; каталог не заявляет, что все исторические предложения приняты.

| Запись | Статус | Основание и последствия |
| --- | --- | --- |
| [ADR-W03: storage и authority](adr-w03-storage-authority.md) | Выбор local SQLite и будущего team PostgreSQL принят в историческом source; team реализация отдельно planned | Cutover проверяется для конкретного проекта; файлы и SQL не объявляются одновременно writable masters |
| [App-agent и API routing](adr-app-agent-routing.md) | Owner-selected default 11.11.2026; кодовая реализация selector; runtime verification ограничена отдельными receipts | Нет implicit fallback, наличие route не равно доступности потребителя или модели |
| [ADR-W05: первоначальный выбор runtime](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md) | Исторически принято, §13/§19; предположения о default route и закрытом App superseded последующим выбором App-agent владельцем | Сохранены происхождение App Server маршрута и прежний непроверенный closed-App gate; [актуальное решение](adr-app-agent-routing.md) требует App и подключённого consumer |
| ADR-W01/W02/W04/W06–W09 | Исторические предложения либо уточняемые решения, см. source | Не повышены в accepted без отдельного доказательства |

**Проверки:** [route test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/runtime-route-selector.test.mts), [project-source test](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts). Пересматривать реестр при новом принятом решении или изменении реализации; связанные требования и задачи принадлежат [плану](../../planning/product-agent-os-web-task-manager-plan-2026-11-09.md).
