# Планы и задачи

Source status: repository_source / planning_catalog; 15.11.2026.

Здесь хранятся самостоятельные планы, backlog и task-state Product-Agent OS. Статус берётся из карточек/JSON владельца; перенос не означает завершения задач. Корневой `PLAN.md` — краткий маршрут к владельцам, `research` — исследования и evidence, `superpowers/specs` — design/evidence.

DG01 завершила исправление ссылок и восемь полных EN-переводов; [результаты проверок](documentation-architecture-2026-11-15.md#dg01-results). DG01–DG07 завершены: все DOCS-01–16 implemented / docs_static_verified; этапы A/B DOCS-13/16 закрыты.

## Текущие владельцы

- [A — качество самого Product-Agent OS](methodology-improvement-2026-11-15.md). Выполнены все 17 исполняемых задач в выбранном объёме. Пять прежних исключений сохраняют отдельный `hold`. Прежняя METH-16 — справочная запись. [JSON v2](methodology-improvement-2026-11-15.json)
- [B — методологии в проектах пользователей](user-project-methodologies-2026-11-15.md). B1 выполнена, 7 из 26 задач реализованы. Следующая задача — PAOS-PMETH-19. Полный EN доступен через переключатель языка. [JSON](user-project-methodologies-2026-11-15.json)

Файлы `methodology-improvement-2026-11-15.en.json` и `user-project-methodologies-2026-11-15.en.json` — побайтовые зеркала соответствующих JSON без суффикса; источником статусов остаются исходные файлы. После изменения исходного JSON перед сборкой обновите зеркало командой `Copy-Item -LiteralPath docs/planning/<имя>.json -Destination docs/planning/<имя>.en.json` и сравните SHA-256 обоих файлов через `Get-FileHash`. Зеркало не переводится и не редактируется отдельно.

- [Документация: анализ структуры и 16 задач](documentation-architecture-2026-11-15.md).
- [Функциональные задачи F01–F34 и семь групп](functional-remediation-2026-11-15.md), [task-state JSON](functional-remediation-2026-11-15.json).
- [Web/desktop M1–M5](product-agent-os-web-task-manager-plan-2026-11-09.md), [task-state JSON](product-agent-os-web-task-manager-task-group-2026-11-09.json).
- [V3 UI/UX](2026-11-13-v3-ui-implementation-plan.md).
- [Audit remediation](product-agent-os-audit-remediation-task-plan-2026-11-09.md).
- [Ordinary-route implementation](product-agent-os-ordinary-route-implementation-plan-2026-11-05.md).

## Каталог перенесённых файлов

Сохранены исторические планы, их статусы, критерии и ограничения. Это каталог, а не единая новая очередь. [Машиночитаемая карта переноса](relocation-2026-11-15.json) содержит прежние адреса и контрольные суммы.

| План / состояние | Прежний каталог |
| --- | --- |
| [functional-remediation-2026-11-15.md](functional-remediation-2026-11-15.md) | `research` |
| [functional-remediation-2026-11-15.json](functional-remediation-2026-11-15.json) | `research` |
| [product-agent-os-audit-remediation-task-plan-2026-11-09.md](product-agent-os-audit-remediation-task-plan-2026-11-09.md) | `research` |
| [product-agent-os-ordinary-route-implementation-plan-2026-11-05.md](product-agent-os-ordinary-route-implementation-plan-2026-11-05.md) | `research` |
| [product-agent-os-web-task-manager-plan-2026-11-09.md](product-agent-os-web-task-manager-plan-2026-11-09.md) | `research` |
| [product-agent-os-web-task-manager-task-group-2026-11-09.json](product-agent-os-web-task-manager-task-group-2026-11-09.json) | `research` |
| [2026-05-14-product-agent-os-generated-infrastructure.md](2026-05-14-product-agent-os-generated-infrastructure.md) | `docs/superpowers/plans` |
| [2026-05-14-product-agent-os-lifecycle-skills.md](2026-05-14-product-agent-os-lifecycle-skills.md) | `docs/superpowers/plans` |
| [2026-05-14-product-agent-os-plugin-core.md](2026-05-14-product-agent-os-plugin-core.md) | `docs/superpowers/plans` |
| [2026-05-14-product-agent-os-production-hardening.md](2026-05-14-product-agent-os-production-hardening.md) | `docs/superpowers/plans` |
| [2026-05-15-product-agent-os-codex-runtime-runner.md](2026-05-15-product-agent-os-codex-runtime-runner.md) | `docs/superpowers/plans` |
| [2026-05-25-track-9-methodology-intelligence.md](2026-05-25-track-9-methodology-intelligence.md) | `docs/superpowers/plans` |
| [2026-05-27-track-10-guided-questions-status-dashboard.md](2026-05-27-track-10-guided-questions-status-dashboard.md) | `docs/superpowers/plans` |
| [2026-06-20-track-11-documentation-architecture-refresh.md](2026-06-20-track-11-documentation-architecture-refresh.md) | `docs/superpowers/plans` |
| [2026-08-05-gpt56-r1-r6-remediation.md](2026-08-05-gpt56-r1-r6-remediation.md) | `docs/superpowers/plans` |
| [2026-08-10-batch45-s9-0-team-readiness.md](2026-08-10-batch45-s9-0-team-readiness.md) | `docs/superpowers/plans` |
| [2026-08-10-batch45-s9-a-durable-contract-recovery.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/2026-08-10-batch45-s9-a-durable-contract-recovery.en.md) | `docs/superpowers/plans` |
| [2026-08-10-batch45-s9-a-durable-contract-recovery.md](2026-08-10-batch45-s9-a-durable-contract-recovery.md) | `docs/superpowers/plans` |
| [2026-08-11-batch45-s9-b-compact-authoring-runtime.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/2026-08-11-batch45-s9-b-compact-authoring-runtime.en.md) | `docs/superpowers/plans` |
| [2026-08-11-batch45-s9-b-compact-authoring-runtime.md](2026-08-11-batch45-s9-b-compact-authoring-runtime.md) | `docs/superpowers/plans` |
| [2026-08-14-batch45-s9-c-test-metric-repair.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/2026-08-14-batch45-s9-c-test-metric-repair.en.md) | `docs/superpowers/plans` |
| [2026-08-14-batch45-s9-c-test-metric-repair.md](2026-08-14-batch45-s9-c-test-metric-repair.md) | `docs/superpowers/plans` |
| [2026-08-17-product-agent-os-loop-remediation.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/2026-08-17-product-agent-os-loop-remediation.en.md) | `docs/superpowers/plans` |
| [2026-08-17-product-agent-os-loop-remediation.md](2026-08-17-product-agent-os-loop-remediation.md) | `docs/superpowers/plans` |
| [2026-11-03-gpt6-documentation-refresh.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/2026-11-03-gpt6-documentation-refresh.en.md) | `docs/superpowers/plans` |
| [2026-11-03-gpt6-documentation-refresh.md](2026-11-03-gpt6-documentation-refresh.md) | `docs/superpowers/plans` |
| [product-agent-os-track-10-backlog.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/product-agent-os-track-10-backlog.en.md) | `docs/sources` |
| [product-agent-os-track-10-backlog.md](product-agent-os-track-10-backlog.md) | `docs/sources` |
| [product-agent-os-track-8-detailed-backlog.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/product-agent-os-track-8-detailed-backlog.en.md) | `docs/sources` |
| [product-agent-os-track-8-detailed-backlog.md](product-agent-os-track-8-detailed-backlog.md) | `docs/sources` |
| [product-agent-os-track-9-backlog.en.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/docs/planning/product-agent-os-track-9-backlog.en.md) | `docs/sources` |
| [product-agent-os-track-9-backlog.md](product-agent-os-track-9-backlog.md) | `docs/sources` |
| [batch45-code-quality-runtime-recovery-task-group.json](batch45-code-quality-runtime-recovery-task-group.json) | `docs/superpowers/specs` |
| [batch45-postq4-t16-t22-promotion-grade-eval-task-group.json](batch45-postq4-t16-t22-promotion-grade-eval-task-group.json) | `docs/superpowers/specs` |
| [gpt6-documentation-refresh-task-group.json](gpt6-documentation-refresh-task-group.json) | `docs/superpowers/specs` |
| [batch39-m01-task-plan.txt](batch39-m01-task-plan.txt) | `docs/superpowers/specs` |
| [batch41-post-neural-flow-rerun-task-plan.txt](batch41-post-neural-flow-rerun-task-plan.txt) | `docs/superpowers/specs` |
| [2026-11-13-v2-ui-implementation-plan.md](2026-11-13-v2-ui-implementation-plan.md) | `design/2026-11-13-v2` |
| [2026-11-13-v3-ui-implementation-plan.md](2026-11-13-v3-ui-implementation-plan.md) | `design/2026-11-13-v3` |
| [2026-11-13-ui-implementation-plan.md](2026-11-13-ui-implementation-plan.md) | `design/2026-11-13` |
| [batch45-post-q4-next-tasks.json](batch45-post-q4-next-tasks.json) | `docs/superpowers/specs` |
| [batch45-postq4-architecture-next-actions.json](batch45-postq4-architecture-next-actions.json) | `docs/superpowers/specs` |

[Итоговые результаты DG07](documentation-architecture-2026-11-15.md#dg07-results) и [владельцы документации FUNC](documentation-architecture-2026-11-15.md#feature-doc-owners) сохраняют отдельный feature status. Карта переноса — справочник old→new адресов; redirects опубликованного сайта или deployment не подразумеваются.
