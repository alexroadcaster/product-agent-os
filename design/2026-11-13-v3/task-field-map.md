# Поля задачи и доступность аналитики

Source status: current repository inspection, 13.11.2026. Read-only source audit; no application mutation or live telemetry verification.

## Редактируемые данные

Источник: [Editor.tsx](../../apps/web/src/features/tasks/Editor.tsx), строки 31–85; [M2TaskProfile](../../packages/contracts/issues/task-profile.ts), строки 19–29. Имена полей ниже канонические; UI может иметь русские подписи.

| Группа | Поля | Правило макета |
| --- | --- | --- |
| Основное | title, type, parentId, priority, summary | Типы epic/task/bug/user_story/sub_task; 5 приоритетов; родитель ограничен типом |
| Процесс | workflow.id, workflow.version | Выбор при создании; существующая версия закреплена. Смена только через migration preview |
| Ценность | technicalValue, productValue | Два отдельных текстовых поля |
| Приёмка | acceptanceCriteria[] | Список, не одна декоративная строка |
| Планирование | estimateSeconds, rank, startDate, dueDate, timezone | Отдельно оценка и фактическое время; даты не наследуются автоматически |
| Классификация | components[], affectsVersions[], fixVersions[] | Несколько значений; архивность доступного варианта обозначена |
| Риски | risks[], noRisks | noRisks — UI-представление массива `['none']`, не новое backend поле |
| Файлы | files[].relativePath, plannedOperation, actualOperation, previousRelativePath | Предыдущий путь для rename; запланированная и фактическая операции не смешиваются |
| Контекст файла | fileContexts[].relativePath, revision, context | Привязан к пути, revision может быть неизвестна |
| Назначения | agentAssignments[]; assignments[].agentId, profileVersion, runId, sessionId, startedAt, endedAt | Краткие ID и подробные записи — разные существующие формы |
| Артефакты | artifactReferences[]; artifacts[].type, reference, revision, provenance, availability | available/unverified/unavailable/stale не равнозначны |
| Блокировка | blocker.reason, owner; since | Reason/owner редактируются; since сохраняет дату появления |
| Изменение | reason, revision, previewDigest | Причина изменения; optimistic revision и preview не скрываются за «автосохранением» |

## Восемь вкладок и связанные действия

Источник: [TaskManager.tsx](../../apps/web/src/features/tasks/TaskManager.tsx), строки 67–93; [Panels.tsx](../../apps/web/src/features/tasks/Panels.tsx).

| Вкладка | Полнота |
| --- | --- |
| Описание | Поля Editor; preview, save/apply preview, discard. Черновик в памяти, не реальная запись из альбома |
| Файлы | Путь, операция, revision/context; назначения и артефакты со всеми подробными полями (Panels 101–105) |
| Критерии | Evidence/outcome по критериям; зависимости, blocker, дети и исключения scope; причина и target перехода |
| Комментарии | Add/reply/edit/delete, attachmentIds, mentions, Markdown rendering (84–96); отдельный preview не приписываем исходнику |
| История | Ревизии, coverage и redaction (117–118) |
| Вложения | Attach/download/delete, причина удаления, подтверждение ссылок, лимиты/hash (73–78) |
| Связи | blocks/relates_to/duplicates/clones, actor/date/reason/waiver, pending stop-and-reconcile/activate (41–52) |
| Сессии | Привязанные сессии и переход к существующему контексту (TaskManager 87) |

Дополнительная вкладка «Расход» в V3 — новая визуальная концепция, не существующий API.

Read-only сведения (Panels 22–35): actual start/end/duration, creator.kind/actorId/displayName, initiatedBy, createdAt, timezone, hierarchy done/descendants/cancelled, summed estimate/actual/unknown, own estimate, children, exclusions/reason. Task ID/public key/project/revision/legacy alias/provenance нельзя превращать в редактируемые поля без отдельного контракта.

Переходы сохраняют target/reason, evidence/outcome, resolution (cancelled/duplicate/wont_do), hotfix reason и soft-WIP override. Ready требует заполнения title/summary/technicalValue/productValue/criteria/estimate/files-or-artifacts/risks; done проверяет зависимости, детей и blocker ([task-profile.ts](../../packages/contracts/issues/task-profile.ts):105–137). Макет показывает preview и подтверждение, а не мгновенное обходное изменение статуса.

## Токеномика: что уже существует

| Метрика | Текущее доказательство | Как показывать |
| --- | --- | --- |
| Запуски/исходы агента | [team/service.mts](../../apps/local-service/src/team/service.mts):52–55: startedRuns, outcomes, taskIds/runIds/sessionIds за период | Есть источник локальных наблюдаемых событий; coverage partial |
| durationSeconds/tokenCount/cost агента | Тот же service устанавливает null, reason `duration_token_cost_telemetry_unavailable` | Недоступно. Не 0 и не предполагаемая цена |
| task/project tokens/cost/tool_use | M2TaskProfile не содержит полей; готовый агрегат не подтверждён | Только демонстрационная концепция |
| Runtime tokenUsage fixture | Упоминание события в test fixture | Не доказывает доступность метрик в UI или полноценное покрытие |
| Карта | [GraphExplorer.tsx](../../apps/web/src/features/graph/GraphExplorer.tsx):7–34; [code-graph.ts](../../packages/contracts/graph/code-graph.ts):1–12 | Частичный lexical graph, revision-pinned, stale/coverage видимы; не runtime proof |

Карточка агента уже показывает unknown при null; AutonomyManager и DecisionBoard сообщают, что токены/стоимость не измеряются. V3 не изменяет это поведение приложения. Mermaid whole/module — новая организация синтетической схемы. «Весь проект» означает все узлы текущего снимка, а не доказанную полноту репозитория.

## Контракт демонстрационных чисел

Один leaf record расхода относится к task/project/agent/run; итог считается по уникальному record ID. Input включает cachedInput, total=input+output; cachedInput второй раз не добавляется. tool_use — количество вызовов инструментов, не токены и не деньги. Cost — условная сумма synthetic receipt в USD, не актуальный прайс провайдера. Период явно указан. Неизвестные поля остаются null и исключают вывод «нулевой расход». Предполагаемая будущая агрегация с несколькими агентами требует явного правила attribution; текущий прототип демонстрирует однозначное владение записью.
