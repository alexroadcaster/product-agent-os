# Frontend и UI/UX Product-Agent OS

Source status: repository_source / current_source_inspection / documentation_implementation; DG04, 15.11.2026.

Владелец: frontend owner + docs-maintainer. Область: текущий Web frontend на `ad78d5d15aced23febae90d319f2aba00bd64d0b`; обновлять при изменении экрана, API state, компонента, дизайн-контракта или accessibility поведения.

## Как найти место изменения

| Вопрос | Каноническая страница |
| --- | --- |
| Где расположен экран и как в него попасть? | [Навигация и состояния](navigation.md) |
| Кто хранит данные, drafts и защищает от поздних ответов? | [Управление состоянием](state-management.md) |
| Какой компонент отвечает за действие или представление? | [Карта компонентов](components.md) |
| Как использовать темы, типографику, движение и локализацию? | [Дизайн-система](design-system.md) |
| Что поддерживается с клавиатуры и какие доказательства доступны? | [Доступность и границы проверки](accessibility.md) |

## Исполняемая граница

[main.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/main.tsx) монтирует React `App` и подключает theme/app/workspace/parity CSS. [App.tsx](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/ui/App.tsx) собирает оболочку, состояние выбранного проекта/раздела и feature-компоненты. [package.json](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/package.json) задаёт React, TypeScript, Vite, D3, Mermaid и GSAP; локальный build включает `tsc --noEmit && vite build`. Наличие зависимости не доказывает использование на каждом экране.

[HTTP client](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/apps/web/src/api/client.ts) связывает UI с локальным сервисом. [API](../api/index.md) владеет HTTP/auth/error контрактами, [backend](../backend/index.md) — lifecycle и исполнением, [DB](../db/index.md) — durable storage. UI-проекция не заменяет серверную authority, runtime ACK или решение владельца. [Продуктовая модель](../product/domain-model.md) объясняет сущности и ответственность.

## Границы дизайна и возможностей

[DESIGN.md](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/DESIGN.md) и [V3 design assets](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/README.md) остаются владельцами дизайна; этот раздел связывает их с кодом и не создаёт вторую копию tokens или screenshots. Исторические [V3 receipts](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/design/2026-11-13-v3/implementation-evidence.md) относятся к своему запуску и не являются текущей UI-приёмкой.

Текущая Карта проекта, bounded Sources и настройки добавления проекта не означают полное файловое дерево, управляемый фоновый scan, карту внешней БД или code-table usages. Будущие Files/Map/Database/usages закреплены за F26–F34 в [функциональном плане](../planning/functional-remediation-2026-11-15.md); текущий scope не реализует их.

## Проверка и обновление

Dashboard, TeamManager и AgentDashboard обращаются к Tasks через `features/tasks/read.ts`. Границу и откат описывает [ADR](../architecture/decisions/adr-dashboard-task-boundary.md). [Критерии и маршруты проверки](../testing/test-map.md#dashboard-a1-criteria) · [Приёмка METH-11](../planning/methodology-improvement-2026-11-15.md#a4-results)

Общий вход `ui/MarkdownBody.tsx` отображает комментарии Tasks, документы Artifacts и сообщения Sessions. Он использует ограниченный парсер и общее правило HTTP(S)-ссылок. Graph, Database и Workflows используют `ui/MermaidView.tsx`, Graph и Database также используют `ui/NetworkView.tsx`. Подготовка данных принадлежит feature-модулям. [Контракт и проверка METH-10](../planning/methodology-improvement-2026-11-15.md#meth-10-results)

`features/usage/RunUsage.tsx` отображает измерения в областях проекта, задачи, сессии и агента. Tasks владеет навигацией и восстановлением фокуса. [Граница и проверка Usage](../planning/methodology-improvement-2026-11-15.md#meth-13-results)

`features/team/AgentDashboard.tsx` владеет командным и персональным представлениями. Общие числовая карточка и шкала находятся в `ui/MetricViews.tsx`. [Граница и проверка Team](../planning/methodology-improvement-2026-11-15.md#meth-14-results)

Для изменения поведения найдите соответствующий source и тест по страницам раздела. [UI policy tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-policy.test.mts), [draft tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/ui-draft-registry.test.mts), [theme/locale tests](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/theme-locale.test.mts) и [browser accessibility checks](https://github.com/alexroadcaster/product-agent-os/blob/ad78d5d15aced23febae90d319f2aba00bd64d0b/tests/web/accessibility/browser-acceptance.mts) — маршруты проверки, не утверждение о новом прогоне.

DG04 проверяет исходные утверждения, RU/EN, ссылки и сборку документации. Live runtime/provider, текущая ручная screen-reader/WCAG оценка и human product acceptance этим не подтверждаются. Статус и evidence: [DOCS-06 / DG04](../planning/documentation-architecture-2026-11-15.md). При изменении контракта обновляются обе локализации, [карта разделов](../product/index.md), навигация и [registry](../sources/registry.md).
