# ADR-W03 — storage и authority

Source status: repository_source / static_architecture_map; 15.11.2026.

Владелец: архитектура Product-Agent OS; scope/version: DG02 v1. Обновлять при изменении соответствующих исходников, границ данных или решений; связанные проверки указаны ниже. Проверка исходников не доказывает runtime activation или готовность к выпуску.

## Статус и происхождение

Исторический выбор движков и направления authority принят в [§20 архитектуры](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-architecture-2026-11-05.md); [исследование storage](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-storage-research-2026-11-09.md) сохраняет альтернативы. Этот ADR — извлечение, не новое решение владельца. SQLite + FTS5 local реализованы в исходниках; PostgreSQL + pgvector относится к будущему team-направлению, а не к подтверждённой действующей интеграции.

## Контекст и rationale

Нужны устойчивые локальные operational entities, поиск и обратимый путь от legacy-состояния. После проверенного cutover SQL может владеть соответствующими сущностями, а исходный код и документы остаются файлами. До подтверждённого cutover legacy source может оставаться владельцем. Нельзя считать обе стороны независимо изменяемыми masters.

## Альтернативы

File-only хранение упрощает взаимодействие с репозиторием, но оставляет задачу согласованности и индексации operational состояния. Team PostgreSQL выбран для будущего отдельного режима, но требует проектирования развёртывания, tenancy и подтверждения миграции. Это сравнение зафиксированного направления, а не доказательство готовности команды или выбора конкретного хостинга.

## Последствия и пересмотр

[Local store](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/local-store.mts), [worker](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/sqlite-worker.mts) и [schema](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/apps/local-service/src/storage/migrations/schema.mts) — текущие source anchors. Проверять authority конкретного проекта, migration/restore и собственные receipts; SQL-транзакция не гарантирует атомарность filesystem. [Project-source tests](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts) и текущие проверки storage дополняют, но не заменяют evidence реального cutover. Пересмотреть запись при изменении storage/authority или утверждении team-дизайна.
