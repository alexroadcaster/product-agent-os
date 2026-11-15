# Продукт Product-Agent OS

Source status: `repository_source / product_contract / static_review`, 15.11.2026.

**Владелец:** product и владельцы Web/desktop и plugin. **Scope/version:** локальный продукт и его границы, DG02/2026-11-15. Обновлять при изменении задачи пользователя, поддерживаемого маршрута, authority или статуса поставки; исходные требования и карточки не копировать как отдельную очередь.

Product-Agent OS помогает вести разработку с Codex: определить состояние проекта, сформулировать работу, подготовить ограниченный маршрут, сохранить решения и сопоставить результат с проверками. В Web/desktop пользователь работает с проектами, задачами, сессиями, решениями и результатами; Python plugin предоставляет отдельные локальные discovery, lifecycle, staging и verification инструменты. Наличие обоих пакетов не доказывает, что любой проект автоматически проходит delivery или готов к production.

## Для кого и какая задача решается

Основной сценарий исторического [PRD](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/research/product-agent-os-web-prd-2026-11-05.md): технически самостоятельный пользователь или ведущий инженер возвращается в проект, уточняет работу для AI и хочет понять, что известно, какое решение требуется и чему можно доверять. Командный сценарий в PRD — гипотеза о будущем использовании, а не доказанный shared access. Предполагаемое уменьшение времени ориентации не измерено этим документом.

| Поверхность | Назначение | Источник текущего статуса |
| --- | --- | --- |
| Web/desktop + local service | Управление локальным проектом, task manager, сессии, решения и результаты | [Web-план и карточки](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md); [functional backlog](../planning/functional-remediation-2026-11-15.md) |
| Python plugin | Discovery, workflow, staged инфраструктура и evidence для инженерной работы | [Plugin и границы](../product-agent-os/index.md), [архитектура plugin](../product-agent-os/architecture.md) |
| Planned расширения | Устранение известных пробелов, Files/scan, PoC графа и DB; отдельный M5 | [F01–F34](../planning/functional-remediation-2026-11-15.md), [M5](../planning/product-agent-os-web-task-manager-plan-2026-11-09.md#paos-m5) |

План Web фиксирует исторические локальные implementation и acceptance receipts. Для нового изменения проверяют текущий source и конкретный receipt, а не переносят старую приёмку на новые версии или условия. Функциональный backlog фиксирует F01–F34 как `planned` на 15.11.2026; PAOS-0047/0052/0053 принадлежат отдельному M5-плану. Планы — владельцы статусов и зависимостей, эта страница не поддерживает их независимую копию.

## Модель и маршруты

- [Доменная модель](domain-model.md): project, task, workflow, run, approval и evidence, включая границы достоверности.
- [Карта возможностей и трассировка](capabilities.md): requirement → source contract → test/evidence → owning task.
- [Пользовательские сценарии](user-journeys.md): подключение проекта, подготовка работы, выполнение и приёмка.
- [Архитектура системы](../architecture/system-context.md) и [атлас диаграмм](../diagrams/index.md): границы компонентов и источников.

## Проверки и ограничения

Related tests: [project-sources.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/project-sources.test.mts), [task-profile.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/task-profile.test.mts), [workflows.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/2f8a0cb8b428ba4499d9d7bd35f1f4b42b2be765/tests/web/workflows.test.mts). Они являются маршрутами проверки соответствующих контрактов, а не утверждением об их запуске при написании этой страницы. Host/provider activation, качество AI, коммерческая готовность и human acceptance требуют отдельных актуальных evidence.
