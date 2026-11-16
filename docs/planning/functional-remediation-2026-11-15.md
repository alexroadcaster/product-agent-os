# Product-Agent OS — функциональные доработки после V3

Source status: repository_source / current_local_synthetic_implementation; remaining_tasks_planned.
Дата планирования: 15.11.2026. Timezone: Europe/Moscow. Schema version: task_matrix_plan_v1.

<!-- func-g01-g05-status -->
FUNC-G01: 7/7 locally_verified; FUNC-G02: 3/3 poc_research_locally_verified; FUNC-G03: 7/7 locally_verified; FUNC-G04: 5/5 implemented, locally_verified_with_measured_limits; FUNC-G05: 5/5 locally_verified_with_explicit_limits; всего27 implemented /7 planned. Три M5 references сохранены.

## Объём и статус

План содержит **34 задачи PAOS-FUNC-01–PAOS-FUNC-34** и ссылки на **3 ранее запланированные задачи M5**. Текущий итог: **27 implemented / 7 planned**, FUNC-G01 закрыта по локальным техническим AC. Итого в этой обзорной матрице 37 позиций; это не общее число задач проекта. Существующие 56 карточек M1–M5, их 53 implemented / 3 planned и оценки сохранены. Новые дефекты не переписывают исторические receipts: они требуют текущего воспроизведения и новой проверки.

Машинное состояние новой группы: [functional-remediation-2026-11-15.json](functional-remediation-2026-11-15.json). Этот MD владеет техническим и продуктовым обоснованием, acceptance и completion evidence. Ссылки M5 не создают второй владеющий статус: их владелец — [docs/planning/product-agent-os-web-task-manager-task-group-2026-11-09.json](product-agent-os-web-task-manager-task-group-2026-11-09.json) и [docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md](product-agent-os-web-task-manager-plan-2026-11-09.md).

Первоначальный запрос разрешал планирование. Последующий запрос 15.11.2026 разрешил полное выполнение FUNC-G01, необходимые локальные synthetic проверки, статусы и документацию; семь задач группы выполнены. Следующий запрос разрешил FUNC-G02: три исследовательских PoC закрыты измеренными решениями и изолированной UI-приёмкой. Следующие запросы разрешили G03 (7 implemented) и G04 (5 implemented с измеренными ограничениями); последующий запрос разрешил G05 (5 implemented); текущий остаток —7 planned задач и отдельные M5 references. P1 — блокировка исполнения или проверка целостности/recovery; P2 — функциональная ценность, корректность информации и поддерживаемость; P3 — ограниченный дефект отображения. Приоритет проверочной задачи не означает, что отказ уже наблюдался.

## Исходные основания и границы доказательств

- Статический аудит исходников 15.11.2026 выявил семь кандидатов в дефекты F01–F07. F01 подтверждён сравнением fingerprint: текущий `apps/web/package-lock.json` SHA-256 `f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac`, квалифицированный `d279009aa1dca2bd2d6ba0e18a77d085a67e872d0dce78dd360fb23d43975f38`; отказ native broker выводится из проверки контракта и должен быть воспроизведён. Runtime в этом планировании не запускался.
- F08–F10/F18/F24 относятся к устройству реализации и полноте пользовательского пути. Производительность не признана плохой без измерений: F20 предшествует F09.
- F11–F17 — отсутствующие расширения либо намеренно ограниченные возможности текущего local scope. Это не семь доказанных регрессий redesign. Перед build нужны доступные capabilities и решения о данных, записи, privacy или канале поставки.
- F19–F23 — недостающее текущее доказательство. Исторические Web/browser receipts из [design/2026-11-13-v3/implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md) не выдаются за заново выполненные проверки.
- Предыдущий audit MD не был создан из-за запрета записи; первичные ссылки и наблюдения перенесены в Source каждой карточки. Чат и этот план не заменяют код и актуальные runtime результаты.
- Внешние API и OpenAI capabilities этим планом не утверждаются. Если задача опирается на новый host/provider contract, при её discovery нужно проверить текущую официальную документацию и фактически доступный интерфейс.

## Рекомендуемая последовательность

1. F01/core fixes и F28 сохраняют свои ветки. F30/F31/F32 — независимые PoC на synthetic fixtures: сначала общий протокол, версии и UI wireframes, затем измерения. Они не ждут внедрения F28/F27/F20; используют согласованные draft contracts и единый baseline protocol. Нынешний запрос не запускает PoC.
2. F28 → F26/F27 → F29. Файловый браузер доступен до графа/БД и не зависит от F30–F34. Общие HTTP/API/storage/UI файлы изменяются последовательными slices с явным владельцем. F18 задаёт freshness contract, новые consumers реализуют его в своих задачах.
3. F20 сохраняет baseline и проверяет уже внедрённые файлы/scan/discovery. F20 → F09; F14 использует F09/F27/F28 и решения обоих F30/F31. Обоснованный reject завершает PoC, но downstream build требует выбора альтернативы или явного blocker.
4. F32 + F26/F27/F28 → F33 (DB schema и полноценный раздел UI); F14 + F33 → F34 (code-to-table связи и usage/impact UI). Новые adapters повторяют benchmark protocol F20 в своих AC; F20 не зависит от F14/F33/F34 и цикла нет.
5. F24 финализирует capabilities всех новых экранов после F14/F33/F34; ранние состояния Files/scan внедряются без ожидания. F19 принимает полный путь Files → Map → Database → code usages → source; ранние Files receipts сохраняются отдельно. F23 затем проверяет человеческое понимание и полезность. F25 синхронизирует claims по мере внедрения.
6. M5 остаётся отдельной дорожкой: PAOS-0047 опционален, PAOS-0052 → PAOS-0053 не зависит от sign-in. F33 не реализует team storage и не открывает внешние БД автоматически.

Hard dependencies записаны в Depends on/JSON; Blocks — точные обратные связи, execution_order — допустимая топологическая последовательность, а не разрешение параллельных записей. F30/F31 не обязуют подключать оба движка: F14 фиксирует один backend или явную композицию. Полная приёмка и human pilot ждут интеграции новых UI; ранняя функциональность Files не ждёт её.

Оценки предварительные: F30–F32 включают PoC и изолированные UI-прототипы, не production integration. F33/F34 оценивают design; build — после выбранного adapter и UI review. Общая дата завершения не выводится; F23 сохраняет 14 дней наблюдения.

## Группы реализации — 7 согласованных подгрупп

Source status: repository_owned_plan_dependency_analysis; planning_only. Группировка 15.11.2026 охватывает **все 34 PAOS-FUNC задачи ровно по одному разу**. Это слои поставки поверх исходных карточек: ID, acceptance, Depends on/Blocks, execution_order, оценки и статусы сохранены. Три M5 ссылки остаются во внешнем source-owned плане и не включены в эти семь групп. Состав и cross-group edges продублированы в JSON (`delivery_groups`, `delivery_group_id`); статус принадлежит задаче, не отдельной копии группового статуса.

### Как выполнять группы без лишнего ожидания

Группы не являются семью последовательными большими релизами. `depends_on_groups` означает наличие рёбер между отдельными задачами; начать можно готовую задачу, не дожидаясь всех участников предыдущей группы. Внутренние ветки ниже — удобные slices, дополнительные prerequisites всегда читать в исходной карточке. Пересечение work locations — ограничение одновременной записи, а не новая функциональная зависимость.

| Группа | Результат | Задачи | Внешние task-зависимости из групп |
| --- | --- | --- | --- |
| FUNC-G01 — Стабильность текущего UI и базовых контрактов | Исправлены подтверждённые UX-дефекты, native runtime квалифицирован, UI/backend contracts имеют независимого владельца. | F01, F03, F04, F05, F06, F07, F08 | Нет |
| FUNC-G02 — Выбор готовых движков и UX-прототипы | Измеренные решения adopt/bounded_adopt/reject и adapters для кода/БД; проверенные изолированные UX-прототипы. | F30, F31, F32 | Нет |
| FUNC-G03 — Файлы, сканирование и подключение проекта | Папка проекта доступна сразу; scan управляемый, discovery и file references согласованы, изменения и ограничения видимы. | F28, F26, F27, F02, F29, F10, F18 | FUNC-G01 |
| FUNC-G04 — Производительность, карта кода и база данных | Измеренная производительность, граф кода, ERD/schema diff и объяснимые связи кода с таблицами доступны UI и агенту. | F20, F09, F14, F33, F34 | FUNC-G01, FUNC-G02, FUNC-G03 |
| FUNC-G05 — Возможности агентов, документы и управление | Достоверные метрики и история, поиск skills, безопасное применение предложений и enforceable autonomy. | F11, F12, F13, F15, F16 | FUNC-G01, FUNC-G03 |
| FUNC-G06 — Восстановление данных и поставка приложения | Проверены Stop/crash/import/backup/restore и подготовлен безопасный install/update/rollback в выбранном канале. | F21, F22, F17 | FUNC-G01 |
| FUNC-G07 — Сквозная приёмка, понятность UI и документация | Функции согласованы в интерфейсе, полный пользовательский путь проверен, human pilot и документация имеют честный статус. | F24, F19, F23, F25 | FUNC-G01, FUNC-G03, FUNC-G04, FUNC-G06 |

### FUNC-G01 — Стабильность текущего UI и базовых контрактов

- **F01** — Восстановить квалификацию native runtime после redesign.
- **F03** — Полностью сбрасывать черновик новой задачи.
- **F04** — Сохранять черновик назначений workflow при навигации.
- **F05** — Обозначить неполное покрытие portfolio рядом с итогами.
- **F06** — Исправить нумерацию очереди на dashboard.
- **F07** — Сортировать последние задачи по времени.
- **F08** — Разделить общие контракты и зависимости UI/backend.

- Результат: Исправлены подтверждённые UX-дефекты, native runtime квалифицирован, UI/backend contracts имеют независимого владельца.
- Условия старта: F01/F03–F07 без task dependencies; F08 только после F01 и architecture review.
- Внутренние ветки: F01 → F08; F03; F04; F05 → F06 → F07. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: Editor и WorkflowManager можно проверять отдельно от runtime; F05/F06/F07 объединить в один ownership Dashboard/model и общий regression набор.
- Ownership: Runtime/manifest; task Editor; WorkflowManager; Dashboard/model; contracts. Один writer на каждую область; F08 application.mts согласовать с G03.
- UI/UX: Существующие формы и dashboard: сохранение/сброс состояния, сортировка/нумерация и честные coverage labels.
- Условие закрытия: Все семь карточек проходят собственные AC; runtime tuple подтверждён на проверенной версии, reset/navigation/dashboard regressions проверены. UI fixes не ждут PoC.

### FUNC-G02 — Выбор готовых движков и UX-прототипы

- **F30** — Проверить dependency-cruiser для графа зависимостей JS/TS.
- **F31** — Проверить codebase-memory-mcp как движок индексации для агентов.
- **F32** — Проверить tbls для извлечения схемы БД и Mermaid ERD.

- Результат: Измеренные решения adopt/bounded_adopt/reject и adapters для кода/БД; проверенные изолированные UX-прототипы.
- Условия старта: Нет hard dependencies. Сначала общий protocol/ground truth, pinned versions/licenses и draft F28/F20 contracts; готовая реализация F28/F20 не нужна.
- Внутренние ветки: F30; F31; F32. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: Три независимых PoC на согласованных fixtures; F30/F31 сравнивать на одинаковых задачах. Выводы в shared architecture/design/matrix интегрирует один владелец.
- Ownership: Раздельные disposable PoC roots/processes и evidence; общий prototype navigation/data contract, один интегратор design/architecture.
- UI/UX: Прототипы «Карты» и «Базы данных», graph/list/Mermaid, evidence, coverage и отказные состояния; не production UI.
- Условие закрытия: Каждый PoC завершён решением с evidence и ограничениями; F14/F33 выбирают пригодный backend. Reject не означает реализованную функцию и не разрешает silent fallback.

### FUNC-G03 — Файлы, сканирование и подключение проекта

- **F28** — Унифицировать инвентаризацию, покрытие и исключения.
- **F26** — Добавить файловый браузер проекта.
- **F27** — Сделать сканирование управляемым фоновым заданием.
- **F02** — Восстановить связи структурированных артефактов с задачами.
- **F29** — Подключить core discovery к добавлению проекта.
- **F10** — Показывать ограничения файлового scope до запуска.
- **F18** — Согласовать обновление снимков задач и dashboard.

- Результат: Папка проекта доступна сразу; scan управляемый, discovery и file references согласованы, изменения и ограничения видимы.
- Условия старта: F28 независим; F26/F27/F02 после F28. F10 дополнительно требует F01, F18 — F05/F07. Не ждать всей G01 или G02.
- Внутренние ветки: F28; F26 → F10; F27 → F29; F02; F18. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: После inventory contract раздельно готовить directory и scan adapters, но wiring application.mts/api/client.ts выполнять последовательно. F29 после F27; reader/scope/freshness привязать к одним paths/revisions.
- Ownership: Один владелец inventory/root policy; последовательные shared HTTP/API/storage patches; Files/Onboarding/freshness UI с общей навигацией.
- UI/UX: Раздел «Файлы», reader, project overview/scan progress, scope preflight, stale/error/unsupported и возврат после restart.
- Условие закрытия: Все семь карточек закрыты по своим AC; Add→Files→scan→discovery→file reference проходит, cancel/restart/retry и root boundaries проверены. Files работает без G04.

### FUNC-G04 — Производительность, карта кода и база данных

- **F20** — Измерить масштабирование и длительную работу.
- **F09** — Оптимизировать чтение и жизненный цикл снимков.
- **F14** — Расширить полезность и устойчивость карты проекта.
- **F33** — Добавить карту БД и раздел «База данных» проекта.
- **F34** — Связать код с таблицами и показать влияние изменений.

- Результат: Измеренная производительность, граф кода, ERD/schema diff и объяснимые связи кода с таблицами доступны UI и агенту.
- Условия старта: F20 после F01/F26/F27/F29; F09 после F08/F20; F14 после F02/F09/F27/F28/F30/F31. F33 после F26/F27/F28/F32 и может начаться до F20/F09/F14. F34 ждёт F14 и F33.
- Внутренние ветки: F20 → F09 → F14; F33; F34. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: После входных contracts вести code и DB ветки независимо; общий SQLite/schema/scans/API/UI wiring имеет одного writer. F34 объединяет готовые outputs. Measurement before optimization сохраняется.
- Ownership: Code-index/impact; database-map; storage/scans; GraphExplorer/DatabaseExplorer. Shared App/Sidebar/client/locales и schema migrations интегрировать последовательными slices.
- UI/UX: «Карта»: dependencies/symbols/impact; «База данных»: «Схема», «Изменения», «Использование в коде»; двусторонние source-line переходы и доступный list/table.
- Условие закрытия: Пять карточек проходят AC и budgets; compatible revisions/coverage/provenance сохранены, read-only DB доказан, graph/table/Mermaid согласованы. Новый workload повторяется в F14/F33/F34 без обратной зависимости F20.

### FUNC-G05 — Возможности агентов, документы и управление

- **F11** — Ввести измеряемую статистику runs и расхода.
- **F12** — Спроектировать и подключить внешний поиск skills.
- **F13** — Добавить безопасное применение document proposals.
- **F15** — Уточнить и расширить границы автономности.
- **F16** — Подтверждать доступную историю и реально загруженные профили.

- Результат: Достоверные метрики и история, поиск skills, безопасное применение предложений и enforceable autonomy.
- Условия старта: F12 design независим; F16 после F01; F11 после F05/F08; F13 после F02/F08; F15 после F01/F10/F11. Реальные source/provider/write/enforcement gates каждой карточки сохраняются.
- Внутренние ветки: F11 → F15; F12; F13; F16. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: После контрактов можно отдельно готовить proposals и autonomy. F11/F12/F16 делят team/service.mts и TeamManager — один owner и последовательная интеграция.
- Ownership: Team/telemetry/history; ArtifactExplorer/writer; autonomy/runtime. Общие team/service, Dashboard, artifacts/service и HTTP patches согласовать с G01/G03/G04.
- UI/UX: Dashboard/Team/History/Artifacts/Autonomy: source/version, confirmed loaded state, proposal preview/conflict, лимиты и причины недоступности.
- Условие закрытия: Каждая из пяти карточек подтверждена поддерживаемыми источниками и своими AC; unsupported остаётся unknown/unavailable, provider/target authority не расширяется. Design-only решение не закрывает implementation задачу.

### FUNC-G06 — Восстановление данных и поставка приложения

- **F21** — Перепроверить очередь, Stop и crash recovery.
- **F22** — Перепроверить импорт, backup и restore.
- **F17** — Подготовить удобную установку, обновление и rollback.

- Результат: Проверены Stop/crash/import/backup/restore и подготовлен безопасный install/update/rollback в выбранном канале.
- Условия старта: F21/F22 после F01; F17 после F01/F22 и отдельного distribution/signing/licensing design gate. Не ждать G04/G05 для ранних synthetic checks.
- Внутренние ветки: F21; F22 → F17. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: Crash и data recovery допускают разные disposable profiles. Packaging после recovery evidence; shared runtime/launcher/profile resources нельзя менять одновременно.
- Ownership: Recovery fixtures; import/export/backup; desktop-local/launcher. Только disposable profiles, без записи в пользовательский профиль или публикации.
- UI/UX: Понятные recovery/compatibility/update/rollback состояния и сохранность профиля; отдельные необратимые/внешние действия по исходным gates.
- Условие закрытия: Три карточки проходят собственные AC; квалификация относится к конкретному tuple/schema/build. После значимых последующих runtime/storage/packaging изменений повторить именно затронутые checks; ранний pass не доказывает финальную сборку.

### FUNC-G07 — Сквозная приёмка, понятность UI и документация

- **F24** — Объяснять доступность функций в момент действия.
- **F19** — Проверить сквозной функционал на текущей сборке.
- **F23** — Провести продуктовую приёмку ключевых сценариев.
- **F25** — Согласовать текущие продуктовые статусы и критерии.

- Результат: Функции согласованы в интерфейсе, полный пользовательский путь проверен, human pilot и документация имеют честный статус.
- Условия старта: F25 ведётся с первой группы, F24 — по мере доступности consumers; их полное закрытие по исходным AC. F19 после своих dependencies, F23 после F19/F21/F22/F24; ранний ограниченный pilot не закрывает весь backlog.
- Внутренние ветки: F24 → F19 → F23; F25. Независимые ветки не разрешают overlapping writes.
- Что объединяем для ускорения: Docs и capability copy идут вместе с feature slices; F19 может сохранять ранние Files receipts. Финальный F24→F19→F23 последовательный, отдельная human acceptance не подменяется тестами.
- Ownership: Один интегратор App/Sidebar/locales/capabilities; tester владеет combined-build evidence; product owner — human pilot, docs owner — F25. Без повторной копии статусов в группах.
- UI/UX: Единая навигация Files/Map/Database и остальных модулей, RU/EN/темы/a11y, consistent status labels, понятные next actions и весь сквозной путь.
- Условие закрытия: Все четыре карточки проходят AC; для закрытия всего grouped backlog дополнительно закрыты G01–G06, проверены применимые cross-group сценарии G05/G06 и provenance итоговой сборки. Незакрытый gate не скрывается снятием задачи из группы; M5/release readiness не заявляются.

### Порядок поставки и точки ускорения

1. **Первый запуск работ:** независимые F01/F03/F04/F05–F07 (G01), F30–F32 (G02), F28 (G03), design F12 (G05) и текущие docs F25 (G07). Это план готовности, не запуск агентов/PoC сейчас. На Dashboard/model F05–F07 один владелец.
2. **Ранний полезный результат:** после F28 выпускать F26 дерево/reader и F27 scan lifecycle; затем F02/F29/F10/F18 по их prerequisites. F08 после F01 стабилизирует общие contracts; его HTTP edits и G03 wiring идут последовательно. Файлы не ждут выбора code engine/DB. После F01 отдельно доступны F21/F22/F16.
3. **Две ветки карты:** F20 → F09 → F14 с решениями F30/F31; параллельно F33 после F32/F26/F27/F28. F33 не ждёт F20/F09/F14. Затем F14 + F33 → F34. Это экономит ожидание code-ветки при работе над схемой БД.
4. **Остальные возможности:** F11/F12/F13/F16 по своим gates, затем F15 после F10/F11/F01. F17 после F22 и решения о поставке; реальная публикация/установка не разрешается группировкой. Shared team/API/storage wiring последовательно.
5. **Сквозное закрытие:** F24 → F19 → F23 после исходных зависимостей; F25 сопровождает все группы. Полное закрытие G07/backlog требует G01–G06 и актуальных применимых receipts, включая возможности G05 и поставку/recovery G06. Их отсутствие не маскируется более узким F19 pass. M5 и широкая release readiness отдельно.

Зависимая цепочка для планирования: F28 → F27 → F29 → F20 → F09 → F14 → F34 → F24 → F19 → F23; у узлов есть дополнительные prerequisites, например F26 для F20, F08 для F09 и F33 для F34. Это не вычисленный critical path по времени: design/build оценки неоднородны, точных длительностей нет. Процент или срок ускорения не заявляется.

### Общие файлы: обязательная последовательная интеграция

| Область | Пересекающиеся группы/задачи | Правило |
| --- | --- | --- |
| `http/application.mts`, contracts | G01/F08, G03/F26/F27/F29, G05/F13 | Согласованный API contract; один writer на shared file, последовательно интегрировать handlers |
| SQLite/schema/code-index/scans | G03, G04; evidence G06 | Один migration/storage owner; отдельные adapters допустимы после interface freeze, потом scoped integration/recovery |
| `App.tsx`, `Sidebar.tsx`, `api/client.ts`, locales | G03, G04, G07 | Один navigation/API интегратор; feature components отдельно, router и labels не править конкурентно |
| Dashboard/model и Team service/UI | G01/F05–F07, G03/F18, G05/F11/F12/F16, G07/F24 | Объединять изменения одной области в согласованный slice; не смешивать totals/coverage/freshness |
| Artifacts/impact | G03/F02/F28, G04/F09/F14/F34, G05/F13 | Сначала единые paths/revisions, затем readers/graph и отдельно approved writer contract |
| Architecture/design/matrix/docs | G02, G04, G05, G07/F25 | Один владелец итогового документа; независимые результаты не означают одновременную запись |
| Disposable runtime/profile | G01/F01, G06/F21/F22/F17, final G07 | Разные synthetic roots и process ownership; не уничтожать/обновлять чужой профиль |

### Анализ рисков группировки и критерии её проверки

- F20 нельзя переносить только в финальную проверку: он даёт основание F09. F09 не оптимизируется без воспроизведённого bottleneck.
- F30/F31/F32 не требуют завершённого product integration для старта; решение PoC не равно выполнению F14/F33.
- F21/F22 можно выполнять рано, но после существенных storage/runtime изменений нужен scoped retest на новой версии; одинаковые проверки без изменившихся входов не повторяются.
- F24/F25 начинаются по мере поставки; их размещение в G07 не откладывает UX/status/docs до конца. Human F23 сохраняет отдельный protocol и 14-дневное наблюдение, технический pass его не заменяет.
- G05/F12/F13/F15/F16 и G06/F17 сохраняют source/authority/enforcement/distribution gates. Группа может быть частично готова; неразрешённый gate остаётся видимым и не считается выполнением.
- Перед закрытием grouped backlog сопоставить все AC задач, UI/API/agent transitions и итоговый build. Ни один участник или M5 reference не теряется, duplicates и task/group cycles запрещены; shared writes должны иметь единственного владельца.

## Полная обзорная матрица новых задач

F01 в сокращённых зависимостях означает PAOS-FUNC-01. Статусы карточек и JSON ниже актуальны; исходные оценки сохранены.

| ID | Приоритет / тип | Задача | Техническое значение | Продуктовое значение | Критерии приёмки | Зависимости |
| --- | --- | --- | --- | --- | --- | --- |
| PAOS-FUNC-01 | P1 · Дефект | Восстановить квалификацию native runtime после redesign | Согласовать lockfile, manifest и native broker без ослабления проверки fingerprint. | Запуск задачи из обновлённого интерфейса действительно приводит к выполнению. | 1) На текущем lockfile воспроизведён отказ package_lock_mismatch; исправление не подменяет квалификацию простой перезаписью хеша.<br>2) На заново квалифицированном tuple новый broker исполняет synthetic command внутри разрешённого root и отклоняет запись снаружи.<br>3) Отрицательные сценарии для изменённых binary, lockfile и adapter остаются fail-closed; повторный старт проходит. | — |
| PAOS-FUNC-02 | P2 · Дефект | Восстановить связи структурированных артефактов с задачами | Унифицировать нормализацию files, artifactReferences, artifacts и fileContexts. | Документ находится из задачи, а задача — из документа и поиска. | 1) Задача со ссылкой только в artifacts.reference находится фильтром каталога по taskId и отображается в связанных задачах документа.<br>2) Legacy artifactReferences/files сохраняют поведение; дубли и разделители путей нормализуются.<br>3) Внешний URL не принимается за локальный путь; stale revision и недоступный файл отображаются явно.<br>4) File references используют нормализацию и root identity F28; каталог, дерево и задачи ссылаются на один разрешённый relativePath/revision. Deleted/moved/excluded не превращаются в доступный документ или право чтения. | F28 |
| PAOS-FUNC-03 | P2 · Дефект | Полностью сбрасывать черновик новой задачи | Синхронизировать модель, rawInputs, estimate, preview и dirty-state при Discard. | После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче. | 1) В новой задаче заполнить criteria/risks/references/estimate, нажать Discard: все поля и модель возвращаются к одному пустому состоянию.<br>2) Следующее сохранение не возвращает отменённые данные; dirty/preview/error не вводят в заблуждение.<br>3) Для существующей задачи Discard возвращает серверную revision и не уничтожает чужие изменения. | — |
| PAOS-FUNC-04 | P2 · Дефект | Сохранять черновик назначений workflow при навигации | Включить typeMapping и исходную CAS revision в общий жизненный цикл draft. | Пользователь не теряет несохранённые назначения процессов при переходе между разделами. | 1) Изменить mapping типа задачи, уйти из Settings и вернуться: черновик восстановлен либо уход заранее остановлен понятным выбором.<br>2) Save/Discard корректно снимают dirty-state; default workflow и mapping не перетирают друг друга.<br>3) Смена проекта не переносит черновик в другой проект; stale save возвращает conflict без потери введённого. | — |
| PAOS-FUNC-05 | P2 · Дефект | Обозначить неполное покрытие portfolio рядом с итогами | Провести partial/loaded/expected из агрегатора в отображение KPI и progress. | Частично загруженные проекты не выглядят как полный итог портфеля. | 1) При успехе1 проекта и ошибке1 проекта рядом с totals показано «1 из2; данные неполные».<br>2) Неизвестные значения не заменяются нулём; progress явно относится к доступной выборке.<br>3) Loading, retry, all-failed и восстановление полного покрытия проверены в RU/EN. | — |
| PAOS-FUNC-06 | P3 · Дефект | Исправить нумерацию очереди на dashboard | Единый 1-based контракт позиции между scheduler и frontend. | Одинаковый порядок задач на dashboard и в управлении очередью. | 1) Для backend positions1/2 dashboard показывает №1/№2.<br>2) Для null номер отсутствует; reorder отражается одинаково на обеих поверхностях. | — |
| PAOS-FUNC-07 | P3 · Дефект | Сортировать последние задачи по времени | Задать явную сортировку по updatedAt с устойчивым tie-breaker и unknown policy. | Блок последних задач ведёт к действительно недавней работе. | 1) UUID-порядок специально противоположен времени: отображаются3 последних по updatedAt.<br>2) Равные и отсутствующие timestamps обрабатываются детерминированно; подпись поясняет выбранную семантику.<br>3) Создание и изменение задачи обновляют состав блока после refresh. | — |
| PAOS-FUNC-08 | P2 · Архитектура | Разделить общие контракты и зависимости UI/backend | Убрать импорты backend→frontend и contracts→backend, сохранив публичное поведение. | Изменение оформления реже ломает серверные функции и выпуск. | 1) Preferences и task decoder имеют одного независимого владельца; contracts не импортируют apps.<br>2) Существующие payload/schema и отказные сценарии сохранены; frontend и service проходят typecheck и текущие тесты.<br>3) Проверка направления импортов предотвращает регрессию; runtime tuple повторно квалифицирован, если затронуты pinned sources. | F01 |
| PAOS-FUNC-09 | P2 · Архитектура | Оптимизировать чтение и жизненный цикл снимков | По измерениям устранить лишние полные сканы и добавить ограниченное освобождение cache. | Длительная работа и большие проекты не упираются в задержки и накопленные snapshots. | 1) Выбраны и реализованы только bottlenecks, воспроизведённые F20; before/after на одном workload.<br>2) Девятый проект не требует restart лишь из-за8 graph snapshots: eviction/rebuild сохраняет revision/cursor safety.<br>3) Нагрузка на task/artifact/history чтение ограничена; превышение бюджета даёт объяснимый partial/error и безопасное восстановление.<br>4) После F20 сравнить metadata listing, graph status и scanner на том же workload: повторный запрос статуса не должен безусловно перечитывать все содержимое файлов; bytes/read и scan count измерены.<br>5) Cache key/eviction учитывают root identity, policy version и scan revision F27/F28; eviction не скрывает файлы из дерева F26 и не смешивает разные проекты. | F08, F20 |
| PAOS-FUNC-10 | P2 · Доработка | Показывать ограничения файлового scope до запуска | Общий preflight для числа файлов, размеров, excluded paths и границ actual diff. | Пользователь заранее понимает, почему задача не стартует и как её разделить. | 1) 32/33 файла,64KiB/64KiB+1 и суммарные512KiB проверяются до dispatch с конкретным объяснением.<br>2) Sensitive/link/binary exclusions не раскрывают содержимое; blocked execution не выдаётся за стартовавший run.<br>3) Если расширение лимитов необходимо, оно проходит отдельный bounded performance/security gate; лимиты не снимаются безусловно.<br>4) Выбор file reference из дерева F26 проходит execution preflight повторно: видимость/читаемость/индексация файла не означают разрешение на dispatch. Policy F28 и реальные execution limits отображаются раздельно; stale path/root требует обновления. | F01, F26, F28 |
| PAOS-FUNC-11 | P2 · Расширение | Ввести измеряемую статистику runs и расхода | Versioned telemetry с provenance, дедупликацией и агрегацией session→run→task→agent. | Длительность и расход помогают сравнивать результат работы без выдуманных чисел. | 1) Сначала утверждены доступные источники duration/tokens/tool calls/cost, privacy и retention; unsupported поля остаются unknown.<br>2) Повтор события не увеличивает totals; partial streams, restart и связь нескольких агентов не приводят к double count.<br>3) Dashboard, задача и агент показывают согласованные значения, период и source; стоимость появляется только при известной модели расчёта. | F05, F08 |
| PAOS-FUNC-12 | P2 · Расширение | Спроектировать и подключить внешний поиск skills | Отдельный read-only discovery adapter с provenance, лицензией, pin и preview. | Нужный skill можно найти вне локального каталога и осознанно добавить. | 1) До build выбран разрешённый источник, network/privacy policy и формат результата.<br>2) Поиск показывает origin/license/revision; timeout/offline не ломают локальный каталог.<br>3) Поиск ничего не устанавливает; добавление проходит существующий preview/apply и проверяет drift и зависимости. | — |
| PAOS-FUNC-13 | P2 · Расширение | Добавить безопасное применение document proposals | Preview-bound compare-and-swap writer с сохранением пользовательских правок и recovery. | Согласованное предложение можно довести до изменения документа внутри приложения. | 1) До build утверждены writer authority, source-vs-SQL ownership и eligible documents.<br>2) Apply меняет только проверенный файл при совпавшей revision; внешний edit вызывает conflict без overwrite.<br>3) Повтор apply идемпотентен; crash/rollback и sensitive paths проверены; staged/applied/accepted показываются отдельно. | F02, F08 |
| PAOS-FUNC-14 | P2 · Расширение | Расширить полезность и устойчивость карты проекта | Выбрать поддержку языков/связей; durable revision index, imports resolution и честный coverage. | Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа. | 1) До build утверждена матрица поддерживаемых языков и типов связей; unsupported semantics остаются явно отмеченными.<br>2) Для выбранного scope cross-file imports/aliases проверяются на эталонных fixtures; unresolved не становится ложным ребром.<br>3) Restart/rebuild сохраняет либо явно инвалидирует revision; D3/Mermaid/list и impact показывают один набор данных.<br>4) Graph consumer использует inventory F28 и этап code в F27; discovered/readable/indexed/unsupported/excluded/error различаются. Нулевой или успешный JS/TS индекс не означает полного анализа проекта.<br>5) Ready/stale/unavailable графа не блокирует дерево F26; restart/cancel/retry не публикуют устаревший результат, недоступный parser оставляет другие результаты сканирования доступными.<br>6) По F30/F31 зафиксирован выбор backend/композиции и rollback; обоснованный отказ PoC не становится скрытым fallback. Неподдерживаемые языки и семантика показываются явно; raw SQLite стороннего движка не становится API PAOS.<br>7) В существующей «Карте» реализованы режимы зависимостей/символов в пределах выбранных capabilities, поиск, incoming/outgoing, путь/impact и evidence drawer с file/line переходами. Graph/list/Mermaid, фильтры и counters используют один snapshot; loading/empty/partial/error/unavailable/stale и version/coverage видимы.<br>8) Общий UI/UX-контракт F30–F34 применён к production экрану, не только PoC; переходы Files↔Map и выбор проекта проверены. Раздел «Архитектура» включается только для source-backed модели: импорт не равен вызову, C4 grouping не считается извлечённым бизнес-фактом. | F02, F09, F27, F28, F30, F31 |
| PAOS-FUNC-15 | P2 · Расширение | Уточнить и расширить границы автономности | Capability-based file/operation/cost policy без обещаний ограничения всего App host. | Пользователь понимает и контролирует допустимую самостоятельность агента. | 1) До build документированы enforceable границы и невозможные обещания; narrow-path execution без enforcement отклоняется.<br>2) В разрешённом маршруте выход за scope/лимит останавливает новые dispatch; unknown outcome остаётся fenced.<br>3) Денежный лимит допускается только при достаточном metering/reservation изF11; иначе UI явно сообщает недоступность. | F01, F10, F11 |
| PAOS-FUNC-16 | P2 · Расширение | Подтверждать доступную историю и реально загруженные профили | Развести configured/pinned/observed model, effort и asset version; capability-based history adapter. | Пользователь знает, какой агент фактически работал и какая часть истории доступна. | 1) До build проверен поддерживаемый host contract; недоступная история не извлекается обходом приватных хранилищ.<br>2) UI различает configured/pinned/observed; loadedVersion появляется только из подтверждённого события.<br>3) Reconnect/profile switch не смешивают историю и identity; partial coverage и отсутствие attestation объясняются. | F01 |
| PAOS-FUNC-17 | P2 · Расширение | Подготовить удобную установку, обновление и rollback | Поверх переносимого package задать version/digest/signing, compatibility и recovery UX. | Обновление не требует ручного подбора каталогов и не ставит данные под угрозу. | 1) До build выбраны канал доставки, формат installer, signing и AUTH/licensing gates; публикация отдельно.<br>2) Synthetic install/update/rollback сохраняют профиль; incompatible schema/tuple блокируют запуск с понятным восстановлением.<br>3) Не удаляются пользовательские профили и старые версии без отдельного решения; новый чистый Windows-профиль проходит согласованный сценарий. | F01, F22 |
| PAOS-FUNC-18 | P2 · Доработка | Согласовать обновление снимков задач и dashboard | Определить refresh/invalidation contract при фоне, мутациях и смене проекта. | После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить. | 1) Изменение задачи/очереди в другом разрешённом канале либо обновляет экран, либо явно делает snapshot устаревшим.<br>2) Поздний ответ предыдущего проекта не заменяет текущие данные; dirty editor не перезаписывается refresh.<br>3) Polling/subscription останавливаются при unmount и не создают неограниченную нагрузку.<br>4) Create/modify/rename/delete и изменение policy/root инвалидируют затронутые directory/document/graph/analysis snapshots; выбран watcher либо bounded rescan/refresh с явной свежестью, без обещания невыбранного live watcher.<br>5) Scan events имеют scanId/revision; позднее событие отменённого задания или другого проекта не меняет UI. После возврата/restart отображается сохранённый scan status без перезаписи черновиков.<br>6) Общий freshness contract распространяется на code/schema snapshots и code-table links: совместимые revisions, late-response rejection, явный stale и остановка polling при уходе. Реализацию и проверку новых consumers выполняют F14/F33/F34; F18 не ждёт их и не блокирует ранний Files путь. | F05, F07, F26, F27 |
| PAOS-FUNC-19 | P1 · Проверка | Проверить сквозной функционал на текущей сборке | Связать real UI/API/storage/native receipts с одним revision без подмены execution mock-данными. | Пользователь проходит весь рабочий путь и получает проверяемый результат. | 1) Synthetic путь task→assignment→run→approval→command→diff/checks→owner acceptance проходит на текущем build.<br>2) Формы, custom workflow, RU/EN, обе темы, keyboard, links и partial/error состояния проверены послеF02–F07/F10/F18.<br>3) Actual App/model roundtrip и генерация agent/skill проверяются только при отдельном разрешении; без него фиксируется live gap, synthetic pass его не закрывает.<br>4) На synthetic fixture пройден путь Add → немедленно доступное дерево → этапы сканирования → preview допустимого файла → file reference задачи; карта и discovery не подменяют полноту файлового дерева.<br>5) Проверены empty/no-Control-plane/Python-only/mixed проекты, Unicode/пробелы, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift во время scan, cancel/restart/retry и два проекта. Ошибка отдельного файла сохраняет разрешённую часть, root violation блокируется; до/после target hashes совпадают.<br>6) RU/EN, две темы, keyboard/focus, pagination, явная неполнота поиска и отсутствие false-ready проверены; fixtures не используют реальные профили/credentials и не запускают target scripts.<br>7) После F14/F33/F34 пройден расширенный путь Files → Map → DB schema → code usages → source line → task reference; сохранены selection/back/filter/project isolation. Проверены confirmed/inferred/unresolved и различие runtime schema/ORM/migrations, экспорт Mermaid и bounded больших графов.<br>8) Новые вкладки/разделы имеют RU/EN, обе темы, keyboard/focus, доступный list/table fallback и все UI states; backend failure/cancel/restart не маскируются mock UI. Отдельные ранние receipts Files/scan допускаются до graph/DB, но окончательное закрытие F19 требует расширенного сценария. | F01, F02, F03, F04, F05, F06, F07, F10, F18, F24, F26, F27, F29, F14, F33, F34 |
| PAOS-FUNC-20 | P2 · Проверка | Измерить масштабирование и длительную работу | Воспроизводимый workload с hardware/cache profile, latency/RSS/queue-depth и error budgets. | Большой проект и длительная сессия остаются управляемыми. | 1) Зафиксированы hardware/cache и объёмы:10k задач,100k сообщений,1k файлов; границы1001 файлов и9 проектов проверены отдельно.<br>2) Измерены cold startup, search/list/event-visible latency, RSS и снимки в повторяемом длительном прогоне; нет скрытой потери данных.<br>3) Результаты сравнены с WEB-NFR и согласованными порогами; deviations заведены вF09, неподдерживаемые объёмы явно ограничены.<br>4) До замеров фиксируются budgets и dataset: большой monorepo, широкая/глубокая директория, пустые папки, generated/vendor/ignored, binary/large, mixed languages. Измеряются registration-to-tree, раскрытие/поиск, scan phases, cancellation latency, restart recovery, RSS, количество обходов и прочитанных bytes.<br>5) Границы старых лимитов 1000/1001 файлов, 10000/10001 записей, depth32/33, 512KiB и 8MiB проверяются как корректный partial/bounded outcome, а не требование снять guards. Metadata listing не обязано читать содержимое всего проекта.<br>6) Baseline допускается до F26–F29; окончательное закрытие F20 требует их версии и сравнения с baseline. F09 использует этот протокол для before/after; benchmark не меняет user workspace.<br>7) Один воспроизводимый benchmark protocol задаёт ground truth и budgets для F30/F31/F32: cold/incremental scan, RSS/disk, latency и precision/recall. Для F14/F33/F34 добавлены UI responsiveness, schema size, edge limits и стоимость bounded agent context; они повторяют протокол в собственных AC. F20 не зависит от завершения PoC/DB/графа, чтобы не создать цикл F20→F09→F14. | F01, F26, F27, F29 |
| PAOS-FUNC-21 | P1 · Проверка | Перепроверить очередь, Stop и crash recovery | Проверить identity/CAS/lease/ownership fences и отсутствие replay в отказах. | Потеря соединения не запускает задачу дважды и не теряет результат. | 1) Crash до dispatch, после dispatch до receipt и после terminal receipt покрыты отдельными сценариями.<br>2) Stop без ACK не освобождает ownership; lost consumer/timeout требуют корректной сверки.<br>3) В разных roots разрешённая параллельность сохраняется, overlapping roots блокируются; selective Stop не отменяет чужой run. | F01 |
| PAOS-FUNC-22 | P1 · Проверка | Перепроверить импорт, backup и restore | Проверить source authority, freeze/CAS, counts/hashes/FK, blobs и идемпотентность. | Задачи, история и вложения сохраняются при переносе и восстановлении. | 1) Source drift и неизвестный writer останавливают cutover; две writable authority не появляются.<br>2) Corrupt/missing blob, прерванный import и повтор запроса дают безопасный результат без дублей.<br>3) Restore в новый synthetic profile сохраняет данные и ссылки; старый профиль неизменён; credentials/pending operations не воспроизводятся. | F01 |
| PAOS-FUNC-23 | P2 · Проверка | Провести продуктовую приёмку ключевых сценариев | Связать acceptance с наблюдаемой корректностью решений, а не числом кликов. | Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг. | 1) До пилота согласованы участники, сценарии, opt-in/retention и baseline MD/chat; production data не обязательны.<br>2) Пройдены первое открытие, возвращение, конфликт, partial evidence и приёмка; ошибки понимания фиксируются вместе с успехами.<br>3) Цели4/5 за3мин и3/5 повторное использование за14дней изPRD проверяются как гипотезы; ноль ложных трактовок verified и потерь данных; owner принимает результат отдельно.<br>4) В пилот добавлены выбор папки, поиск обычного файла вне Control-plane, объяснение excluded/unsupported/partial, отмена/повтор и возвращение после restart. Наблюдатель проверяет, что участник не путает видимость файла, успешную индексацию и разрешение на исполнение.<br>5) В human pilot включены поиск места изменения через Map и DB usages, чтение ERD/table, переход к source, понимание stale/partial/inferred и обнаружение неподдерживаемой семантики. Сравниваются успешность и время с согласованным baseline, UI convenience не выводится из технических тестов. | F19, F21, F22, F24 |
| PAOS-FUNC-24 | P2 · Доработка | Объяснять доступность функций в момент действия | Единый capability vocabulary для staged/unsupported/partial/connected/qualified/accepted. | Пользователь отличает доступную функцию от экрана с будущей возможностью. | 1) Для usage, graph, proposals, skills discovery, history, autonomy и runtime рядом с действием показаны реальный scope и причина недоступности.<br>2) Есть конкретный следующий шаг; unsupported не выглядит как loading, connected не называется execution-qualified.<br>3) RU/EN и accessibility состояния проверены; нет повторного запроса уже действующей bounded authority.<br>4) В onboarding и проекте показаны независимые registration/tree/inventory/documents/code/analysis состояния F26–F29, время и scope наблюдения; counts.files не называется indexed без соответствующего покрытия.<br>5) Empty/no-supported-code не получает ложный «проект полностью проанализирован»; excluded/error/unsupported объясняют причину и действие. Недоступный parser/core adapter не скрывает доступное дерево, контрольный список Control-plane явно назван отдельным фильтром.<br>6) В project navigation и onboarding явно различаются Files, Map, DB schema и code usages; Settings владеет регистрацией/источником, не дублирует самостоятельные explorers. F14/F33/F34 несут production UI; до их завершения доступны ранние capability states, полное закрытие F24 требует всех consumers.<br>7) UI показывает только внедрённые capabilities/языки/DB sources и объясняет отсутствие: not_configured, unsupported, unavailable, indexing, partial, stale, failed. PoC/experimental не называется production-ready; engine выбран продуктом по evidence, внутренние настройки backend не навязываются пользователю. | F05, F10, F26, F27, F29, F14, F33, F34 |
| PAOS-FUNC-25 | P2 · Документация | Согласовать текущие продуктовые статусы и критерии | Один актуальный указатель PRD/architecture/plan/registry с сохранённой историей. | План и документация ясно показывают, что работает, ограничено и ждёт проверки. | 1) Текущие scope/status/acceptance не противоречат историческим implementation_not_started/API-only блокам: история явно помечена и маршрутизирована.<br>2) Для F01–F34 и M5 есть единый owner/status/source; implemented не подменяет human/live acceptance.<br>3) Синхронизированы только изменённые claims и RU/EN registry; validators/docs tests проходят, старые56cards сохранены.<br>4) Текущая проверка docs-site больше не сообщает missing web/accessibility.html и web/pilot.html в RU/EN; search/sitemap/switcher parity подтверждён на явно выбранном build. Публикация и promotion сайта отдельно.<br>5) Документы различают «Источники», файловое дерево F26, сканирование F27, inventory policy F28 и discovery F29; версии API/coverage, recovery и ограничения описаны в existing PRD/architecture, без заявления об автоматическом ремонте или полной семантике.<br>6) F30–F34 содержат upstream URLs, дату research, выбранные version/commit/license и реальные PoC receipts при выполнении; README claims не выдаются за локальные измерения. PRD/architecture/UI help описывают вкладки Map/Database/usages, read-only источники, экспорт, coverage и fallback; links и RU/EN согласованы. | — |
| PAOS-FUNC-26 | P2 · Расширение | Добавить файловый браузер проекта | Независимый от графа API директорий и безопасного чтения с ленивой загрузкой, стабильными ссылками и ограниченными ответами. | Пользователь видит структуру выбранной папки и открывает доступные файлы, даже когда индекс не готов или язык не поддерживается. | 1) После регистрации раздел «Файлы» доступен без графа и завершённого сканирования; видны вложенные и пустые каталоги, исходники, конфигурации и бинарные файлы как метаданные, в пределах разрешённой политики F28.<br>2) Раскрытие каталога загружает только нужную ветку; pagination и фильтры показывают границы выборки; поиск по имени/пути явно сообщает scope. Метаданные содержат relativePath, тип, размер, modifiedAt и состояние доступа.<br>3) Текст читается по отдельному запросу с проверкой root identity, revision, размера и кодировки; binary/oversized/unreadable получают объяснение. Неподдерживаемое индексатором расширение не скрывает файл. HTML/скрипты не исполняются при просмотре.<br>4) Нет чтения за пределами корня через traversal, symlink/junction/hardlink и подмену каталога; sensitive content не раскрывается. Выбор файла не передаёт весь проект модели и не выдаёт разрешение на выполнение.<br>5) Выбранный путь можно скопировать и использовать как file reference; Control-plane — фильтр над реальными путями. Смена проекта и поздний ответ не смешивают дерево; RU/EN, keyboard, focus, empty/error/loading проверены.<br>6) Контракт file/line navigation поддерживает будущие переходы из Map/Database/code usages и возврат к выбранному файлу; недоступный/удалённый source объяснён. F26 не ждёт F30–F34, backend action отсутствующей capability не показывает ложный результат. | F28 |
| PAOS-FUNC-27 | P2 · Расширение | Сделать сканирование управляемым фоновым заданием | Сохраняемые scan ID и этапы, bounded worker, идемпотентность, отмена, повтор и восстановление отдельно от регистрации проекта. | Проект доступен сразу после регистрации; пользователь видит ход сканирования, частичный результат и способ продолжить после сбоя. | 1) Регистрация сохраняется один раз и возвращает доступный проект без ожидания полного обхода; scan status содержит scanId, root identity, policy version, этап inventory/documents/code/analysis, начало/обновление, счётчики и причины partial/error.<br>2) Повтор Add/retry в том числе после restart не создаёт новый проект или дублирующую работу; конкурентные запросы одной revision объединяются либо получают объяснимый conflict. Изменившийся root не продолжает старое задание.<br>3) Cancel останавливает дальнейшую работу и позднюю публикацию; повтор запускается с явно определённой revision. Restart восстанавливает либо переводит задание в recovery_required/interrupted; незавершённое не становится completed.<br>4) Заданы budgets времени/памяти/записей и concurrency; failure одного анализатора сохраняет допустимые результаты других этапов. Ready одного индекса не означает полный анализ проекта; неподключённый analysis adapter отображается как unavailable.<br>5) Состояние и последнее успешное покрытие доступны после открытия Settings/проекта и restart; events или bounded polling не перезаписывают более новую revision. Scan bookkeeping остаётся в профиле PAOS, target workspace не изменяется.<br>6) Версионированный analyzer contract допускает code/schema/code_database этапы с отдельными capabilities/status/progress, cancellation и atomic publication. F30–F32 проверяют внешние исполнители изолированно, F14/F33/F34 подключают только выбранные; F27 не зависит от их реализации и не запускает установщики автоматически. | F28 |
| PAOS-FUNC-28 | P2 · Архитектура | Унифицировать инвентаризацию, покрытие и исключения | Общий контракт путей, revision и coverage для directory/document/code consumers при раздельных правах listing, reading и indexing. | Файлы не исчезают из обзора из-за отсутствия языкового анализатора; пользователь понимает, что найдено, пропущено или недоступно. | 1) Контракт различает discovered, readable, indexed, unsupported, excluded и error; счётчики определяют разные стадии и не суммируют пересекающиеся множества как общее число файлов. Empty и unknown отличаются; отсутствие подходящего кода не означает полный анализ.<br>2) Файловое дерево независимо от набора расширений индексатора. .gitignore и project include/exclude имеют явную precedence и разные правила видимости/индексации; ignore не выдаёт права доступа. Sensitive paths/content защищены даже при include override.<br>3) Отчёт показывает применённую policy version, причины пропуска, лимиты и partial coverage. Тяжёлые generated/vendor каталоги не читаются без необходимости; разрешённое раскрытие метаданных не снимает ограничений чтения содержимого.<br>4) Ошибка, превышение размера или unsupported encoding отдельного файла сохраняет другие разрешённые записи; directory-level denial помечает неполноту. При root identity drift, попытке выхода за корень или недостоверной revision публикация небезопасного результата блокируется.<br>5) Bounded/paged inventory поддерживает normalised relative paths, Unicode/пробелы и Windows case semantics; ссылки и race conditions не расширяют root. Одинаковые policy/root/revision дают согласованные ссылки и причины во всех consumers.<br>6) Изменение политики инвалидирует затронутые snapshots; file metadata не требует полного чтения всех исходников. Позитивные/отрицательные сценарии и нагрузочные границы проверены; исходники проекта не меняются.<br>7) PoC и будущие adapters применяют те же правила root/policy/read/index и показывают несовпадение coverage; сторонний индексатор не обходит исключения и не создаёт кеш в target. Обнаруженные DB/ORM/migration candidates — метаданные, не разрешение подключаться или выполнять миграции; scan limits и sensitive paths сохраняются. | — |
| PAOS-FUNC-29 | P2 · Расширение | Подключить core discovery к добавлению проекта | Версионированный read-only adapter к существующему discovery/first-run analysis с provenance, ограничениями и invalidation. | После добавления проекта видны стек, структура, Control-plane gaps и обоснованные следующие шаги, а не только количество узлов графа. | 1) До build выбран способ reuse существующих core discovery/first-run модулей и deployment/runtime contract. Недоступный Python/adapter/version даёт явный unavailable; установка зависимостей и альтернативный полный scanner автоматически не запускаются.<br>2) Analysis запускается как отдельный этап F27, использует согласованную inventory policy F28 и возвращает schema version, source revision, stack/components, control-plane coverage, findings с источниками/confidence/limitations.<br>3) Обнаруженные scripts/configs только анализируются как данные: не исполняются команды проекта, tests, hooks, модели или провайдеры; target files не создаются и не исправляются. Предложения Control-plane остаются предложениями.<br>4) Пустой проект, проект без Control-plane, Python-only, mixed stack и unsupported language получают объяснимые результаты без выдуманной полноты; timeout/error сохраняют доступное дерево и уже полученное покрытие.<br>5) Изменения файлов, root или inventory policy делают прежние выводы stale; повтор и restart не смешивают revisions. Выводы доступны из выбранного проекта в RU/EN, связаны с разрешёнными file references и не раскрывают secrets.<br>6) Discovery показывает кандидаты языков/ORM/DB/schema files со source и confidence для F14/F33/F34, не открывает соединения и не исполняет migrations. В project overview есть маршруты к Files/Map/Database по capabilities; отсутствие адаптера не подменяется сторонним auto-install. | F27, F28 |
| PAOS-FUNC-30 | P2 · PoC | Проверить dependency-cruiser для графа зависимостей JS/TS | Проверить reuse анализатора импортов вместо расширения собственного lexical parser; согласовать adapter JSON и семантику ребра. | Пользователь и агент видят проверяемые зависимости файла, циклы и путь к месту изменения. | 1) До запуска зафиксированы версия/commit, MIT и лицензии поставки, Windows/Node compatibility, fixture corpus, baseline текущего lexical graph и бюджеты времени/RSS/размера ответа; результаты не выводятся из README.<br>2) На synthetic JS/TS fixtures проверены ESM/CommonJS, tsconfig aliases, re-exports, cycles, missing imports, dynamic import и monorepo boundaries; импорт не называется вызовом функции. Известные ожидаемые рёбра сопоставлены с output: false positives/negatives и unresolved перечислены.<br>3) JSON adapter сохраняет normalized path/root identity, source revision, тип/направление ребра и evidence; соблюдает согласованный контракт F28 без зависимости от завершения его реализации. Конфигурация передаётся PAOS как данные: target JS-config/scripts/hooks не исполняются; target hashes не меняются.<br>4) В изолированном UI-прототипе существующей «Карты» есть режим «Зависимости»: поиск файла, incoming/outgoing, фильтр типа, выделение пути/цикла, переход к строке/файлу и синхронные graph/list/Mermaid. Ошибки и unsupported показаны; peer review сценария не считается human acceptance.<br>5) На одинаковых заданиях поиска места изменения сравнены время, файлы/объём контекста и правильность результата с baseline; parser failure/timeout не скрывает дерево. Provider calls не нужны для deterministic benchmark; оценка с моделью — только при отдельной точной авторизации.<br>6) Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.<br>7) Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance. | — |
| PAOS-FUNC-31 | P2 · PoC | Проверить codebase-memory-mcp как движок индексации для агентов | Оценить SQLite-backed индекс, многоязычные связи, запросы и управляемость отдельного native процесса через версионированный adapter. | Агент получает небольшой релевантный контекст и объяснимый путь к изменению, а пользователь видит основания поиска. | 1) Закреплены version/commit/license и зависимости поставки, Windows packaging, поддерживаемые языки/виды связей, workload и бюджеты. Сравнение с текущим поиском использует те же ground-truth fixtures и задания, что F30; F30 не обязан завершиться раньше.<br>2) Проверены search/definition/references/call path/impact и related tests только для заявленных capabilities; measured precision/recall, unresolved и unsupported опубликованы. Bounded ответы дают file/line evidence, revision, truncation/pagination; stale индекс не выдаётся за текущий.<br>3) Измерены cold/incremental indexing, rename/delete/branch-like change, cancel/retry/restart, два проекта, memory/disk и latency; SQLite/cache/locks принадлежат движку и не открываются PAOS как неофициальный writable API.<br>4) На disposable профиле доказаны lifecycle/cleanup daemon, timeout и child-process ownership; account-wide coordination и конфликт другого build/cache исследованы. Нельзя завершать пользовательский daemon или менять global MCP/skills/hooks/PATH, скачивать модели или отправлять код наружу. Если изоляция несовместима с PAOS, результат bounded_adopt/reject, не обход защиты.<br>5) Прототип «Карты» содержит поиск символа, callers/callees/path/impact, панель объяснения и переход к исходнику; состояния недоступного движка, partial coverage, stale и превышенного бюджета видны. Контракт UI не зависит от внутренних таблиц движка; изучается использование уже существующего graph UI PAOS.<br>6) Сравнительный отчёт определяет роли F30/F31: один выбранный backend либо явная композиция по языкам без дублей/конфликтующих revisions. До подключения engine учитывает inventory policy F28; при невозможности ограничить индексирование чувствительных файлов вариант отклонён.<br>7) Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.<br>8) Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance. | — |
| PAOS-FUNC-32 | P2 · PoC | Проверить tbls для извлечения схемы БД и Mermaid ERD | Оценить внешний schema adapter JSON/Mermaid против встроенной SQLite introspection и закрепить контракт schema snapshot. | Получить достоверную карту таблиц без ручного рисования и без чтения пользовательских строк. | 1) Закреплены version/commit/MIT/dependency licenses, Windows distribution, минимальный SQLite-first scope и бюджеты; tbls JSON/Mermaid сравниваются с metadata introspection существующего SQLite driver. PostgreSQL и другие СУБД — отдельные capability targets, не автоматический scope.<br>2) Synthetic SQLite покрывает PK/FK, composite FK, UNIQUE/index, views, nullable/generated columns, self-reference и отсутствие FK. Список объектов и рёбер сравнен с ground truth; ограничение формата/драйвера и inferred relation не скрыты.<br>3) Используется явно выбранный read-only fixture/consistent snapshot; данные строк, credentials и DSN не попадают в logs/output. Проверены locked/WAL/change-during-read, недоступный и повреждённый файл; соединение не создаёт отсутствующую БД, не мигрирует её и не исполняет project config/extensions/hooks.<br>4) Результат содержит source kind, schema fingerprint/revision, tables/columns/keys/indexes/views, coverage и warnings; canonical JSON и Mermaid согласованы. Проверены экранирование имён и limits на размер ERD, неисполнение HTML/скриптов.<br>5) Изолированный прототип будущего раздела «База данных» показывает источник, ERD и таблицу объектов, выбор таблицы/колонки, поиск/фильтр и явный no-database/unsupported/stale/error. Экспорт Mermaid не требует внешнего сервиса; tiny Mermaid проверяется на нужной ERD-семантике.<br>6) Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.<br>7) Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance. | — |
| PAOS-FUNC-33 | P2 · Расширение | Добавить карту БД и раздел «База данных» проекта | Версионированные schema snapshots, schema diff и read-only адаптер выбранного источника с provenance и freshness. | Пользователь просматривает таблицы и связи, понимает источник и актуальность схемы и переходит к её определению. | 1) Перед build по F32 выбраны adapter, поддерживаемые источники и budgets; отсутствие выбранного backend остаётся blocker. БД самого PAOS и БД анализируемого проекта различаются. Обнаружение кандидата в дереве не открывает БД автоматически: пользователь выбирает разрешённый источник; external/live/credentials требуют точной авторизации.<br>2) Контракт различает фактическую DB schema, статические ORM/миграции и предложенные связи. Неприменённая миграция не объявляется текущей БД; execute migrations/project code/extensions запрещён. SQLite-first read-only schema extraction не читает строки и не создаёт/меняет БД; PostgreSQL scope не предполагается из поддержки tbls.<br>3) В project navigation добавлен раздел «База данных» с вкладками «Схема» и «Изменения»; в «Схеме» доступны ERD/табличный режим, поиск, фильтры, details таблицы/колонки, PK/FK/index/views и переход к разрешённому schema/migration source. Settings сохраняет регистрацию и выбор источника, не становится вторым независимым browser.<br>4) ERD и таблица показывают одну revision; composite FK и direction корректны, inferred связи отличаются от declared. Выбор узла синхронизируется с details/list, большие схемы дают bounded subgraph и предупреждение, Mermaid export экранирует имена, не раскрывает secrets и сообщает фильтры/coverage.<br>5) Вкладка «Изменения» сравнивает два совместимых snapshots: added/removed/changed objects; rename без доказательства показан как add/remove или гипотеза. При отсутствии baseline явное empty; дрейф источника/политики маркирует stale, schema fingerprint и время наблюдения видимы.<br>6) Этап database_schema в F27 имеет независимые progress/cancel/retry/recovery/partial/error; ошибка сохраняет прежний успешный snapshot с stale и не блокирует Files/code. Невыбранная/отсутствующая БД — not_configured/none_found, а не бесконечная загрузка. Late responses другого проекта/revision отклоняются.<br>7) Пройдены API/adapter и browser сценарии F32 на disposable fixtures: RU/EN, обе темы, keyboard/focus, table alternative, deep link/back, restart и switching projects. До/после target и контрольных файлов не меняются; отсутствуют sensitive DSN/rows в UI/export/logs; runtime evidence привязан к build.<br>8) На workload F20 измерены schema extraction, cold/warm view, large ERD, memory и response size; budget deviations имеют bounded outcome. Docs/capabilities F24/F25 обновляются по реально внедрённому scope; UI mock не закрывает acceptance.<br>9) Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance. | F26, F27, F28, F32 |
| PAOS-FUNC-34 | P2 · Расширение | Связать код с таблицами и показать влияние изменений | Добавить provenance-aware рёбра code→query/ORM→table с разрешением в совместимых code/schema revisions и bounded impact queries. | Пользователь и агент видят, какой код читает или меняет таблицу и какие участки нужно проверить при изменении схемы. | 1) До build выбрана ограниченная language/SQL/ORM матрица на основе F30/F31/F32; code call paths включаются лишь при подтверждённой семантике, import edges не подменяют CALLS. Ground-truth cases и пороги precision/recall фиксируются до измерений.<br>2) Связь хранит file/symbol/line span, query or model evidence, table identity/source, operation read/write/schema/unknown, extraction method/confidence и code+schema revisions. Dynamic SQL, naming heuristics, aliases и непрослеживаемый вызов остаются inferred/unresolved; unknown не считается отсутствием зависимости.<br>3) Проверены raw SQL, выбранный ORM, join/aliases, одинаковые имена таблиц в разных источниках, rename/drop, generated/dynamic query и unsupported language. Код/запросы не исполняются; secrets/строки БД не извлекаются; precision/recall и ограничения представлены для каждого поддерживаемого типа.<br>4) В «Базе данных» добавлена вкладка «Использование в коде»: таблица → места чтения/записи → файл/строка; в существующей «Карте» — фильтр связей с БД и панель пути/влияния. В reader файла доступен переход к связанным таблицам. Selection/deep link/back/filter сохраняются в пределах проекта; произвольные связи не рисуются как подтверждённые.<br>5) Пользователь переключает confirmed/inferred и read/write/unknown, открывает evidence ребра и видит incomplete impact. Доступная таблица/список дублирует смысл графа; RU/EN, обе темы, keyboard/focus, empty/unsupported/partial/error/stale и большие результаты проверены в browser.<br>6) Agent queries возвращают ограниченные source-backed paths и кандидаты тестов, truncation/cursors и обе revisions; rename/delete/change источника инвалидирует только совместимый snapshot. Смешение code/schema разных проектов или устаревших ревизий запрещено; rebuild/restart/cancel/retry проверены.<br>7) На согласованных задачах сравнен поиск места изменения без связей и с ними: correctness, пропущенные affected files/tests, контекст и время; никаких обещаний полного runtime call graph. Budgets F20 и guardrails F27/F28 соблюдены; failures одного analyzer не блокируют дерево и schema map.<br>8) Документация объясняет разницу schema ERD и code-to-table impact; release claims и capability states синхронизированы с F24/F25. Закрытие требует рабочей интеграции UI/API/agent contract, а не только схемы или прототипа.<br>9) Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance. | F14, F33 |

## Существующие M5: ссылки без дублирования состояния

Состояние на момент чтения владельца: `planned`. Текущий статус всегда читать в исходной группе M1–M5.

| ID | Задача | Техническое значение | Продуктовое значение | Критерии приёмки исходной карточки | Зависимости |
| --- | --- | --- | --- | --- | --- |
| PAOS-0047 | Опциональный Sign in with ChatGPT | После допуска реализовать отдельный SIWC route, consent, PKCE/scopes, refresh/restart/resume и preview capability matrix | Eligible пользователь может использовать разрешённый ChatGPT plan без второго рабочего приложения. | Только после подтверждённого admission exact paid/local route: identity и plan scope проверены, refresh/resume не дублирует работу, unsupported tools скрыты с причиной; API route не зависит от этой задачи. | PAOS-0039, PAOS-0044, PAOS-0046 |
| PAOS-0052 | Командный профиль PostgreSQL и pgvector | После отдельного M5 team design/start решения реализовать server repository, dialect migrations, tenancy/RLS, lexical и versioned vector index; hosting/auth/runtime design gate до кода | Команда работает с общим актуальным состоянием и поиском в пределах своих прав. | ST-10: domain parity, negative tenant/pool tests, filtered search; embedding model/privacy approved; lexical fallback; hosting/auth/runtime placement согласованы; local M4 не зависит от M5 | PAOS-0048, PAOS-0049, PAOS-0051, PAOS-0030 |
| PAOS-0053 | Перенос local проекта в team workspace | Versioned logical export/import, actor/tenant mapping, blob checks, final delta и one-authority handover | Пользователь переносит проект команде с прежними задачами и историей без конфликтующих writable копий. | ST-11/ST-AC-08: UUID/key collisions, identity mapping, counts/hashes/FK, final delta, rollback; credentials/pending approvals/commands исключены; local read-only после switch; без bidirectional sync | PAOS-0056, PAOS-0052 |

## Общий контракт исполнения и приёмки

- Ошибка сначала воспроизводится на текущем revision; RED из broken setup не принимается. Ограничение признаётся дефектом только относительно принятого контракта.
- Проверки должны указывать исходники/dependencies, среду, synthetic dataset, наблюдаемый результат и границы доказательства. Mock UI, подключённый App и full execution — разные состояния.
- Никаких tokens, secrets, raw private chat или настоящих customer данных в отчётах. Pairing material остаётся в памяти; provider calls и реальные профили за пределами synthetic проверки требуют точного разрешения.
- Design-approved, implemented, technically verified и human accepted — разные факты. Задачи расширения F11–F17 нельзя завершить только дизайном; для implemented нужны все поведенческие AC и checks.
- Технические и продуктовые поля обязательны для каждой новой карточки; completion получает фактическую дату только после выполнения. Все будущие commands ниже — план, а не журнал выполненных проверок.
- Rollback каждой задачи сохраняет пользовательские файлы и чужую работу. Планирование не создаёт branch/commit/PR и не меняет приложение, hook/trust или permissions.

## Готовность к запуску задач

Статус пакета: `proposal_staged`; это полный backlog, а не утверждение `plan_ready` для всей реализации. Проверка структуры плана не закрывает следующие gates.

| Gate / задачи | Статус | Владелец и требуемое доказательство | Риск до закрытия |
| --- | --- | --- | --- |
| Воспроизведение F01–F07 | present_unverified | tester: RED и конкретный исходный revision; AC и Source в карточках | статическое предположение может отличаться от runtime |
| Архитектура F08/F09 | proposal_staged | architect: boundary/contract review в существующей architecture и измерения F20; existing-capability scan до нового кода | излишний рефакторинг, изменение публичного поведения |
| Telemetry F11 | applicable_missing | architect/product-manager: tracking sources, ownership, privacy/retention, unknown policy | выдуманные метрики и double count |
| Расширения F12–F17 | approval_required | владелец + architect: индивидуальный design gate из карточки, поддерживаемые capabilities, оценка build | недоступный API, нарушение write/enforcement/distribution границ |
| Сценарии F19–F22 | proposal_staged | tester: protocol → checks → receipts в Completion Report; ожидается exit0 и прохождение всех scoped AC без подмены native исполнения | synthetic и live доказательства могут быть ошибочно смешаны |
| Human pilot F23 | applicable_missing | product-manager + владелец: согласованный protocol, участники/consent, baseline, наблюдаемые результаты за 14 дней | продуктовая ценность пока гипотеза |
| Docs tooling текущей планировки | not_applicable | existing Python docs checks и Markdown достаточны; сайт, CI и новые зависимости не меняются | rendered-site freshness не заявляется |
| Coding standard текущей планировки | not_applicable | код не меняется; при старте implementation использовать действующий coding-standards workflow | план не заменяет source review конкретного slice |
| GitHub PoC F30–F32 | proposal_staged | architect/tester: pinned version/license, synthetic ground truth, budgets, UI prototype, adopt/bounded_adopt/reject; запуск ещё не разрешён текущим планированием | upstream promises и несовместимость изоляции/упаковки |
| DB map / code links F33–F34 | applicable_missing | architect/UI owner: решения PoC, source/read-only contract, wireframes и scoped API/browser evidence до closure | схема не равна runtime usage; prototype не равен production UI |
| M5 | approval_required | исходные карточки владеют admission/team design и migration gates | нельзя начать team/provider работу из ссылки в этой матрице |

Business/product hypothesis: корректное сохранение состояния и понятный scope должны уменьшить ошибки работы; подтверждение F23, а не факт из числа тестов. Outcome scope — local App-active продукт; наблюдение repeat use — 14 дней; delivery metrics и пользовательская ценность разделены. Для расширений с новыми domain/API/storage boundaries необходимы актуализация existing architecture/ADR и согласование invariants до build; принудительная новая методология, портал или набор шаблонов сейчас не создаются.

## Дополнение: файлы и сканирование — 15.11.2026

Владелец разрешил только обновление плана. Добавлены F26–F29; уточнены AC десяти существующих задач F02/F09/F10/F14/F18/F19/F20/F23/F24/F25 и hard dependencies семи из них. Все 29 задач группы остаются planned; три M5 — ссылки на прежний источник состояния.

Выбранная граница: регистрация проекта → доступное файловое дерево и read-on-demand → управляемое сканирование → отдельные inventory/documents/code/analysis результаты. «Файл видим», «файл разрешено читать», «файл проиндексирован» и «можно выполнить команду» — разные факты. Unsupported язык не скрывает директорию. Контекст модели формируется отдельно, без автоматической отправки всего проекта.

Source-backed основание: [Sources](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts) перечисляет шесть Control-plane файлов; [регистрация](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts) сохраняет проект, затем ждёт source/code scan; [inventory](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/sources.mts) использует фиксированные исключения и лимиты; [core discovery](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py) и [first-run](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py) существуют отдельно от проверенного Web onboarding. Это статический вывод, не новый runtime receipt.

| Design gate | Статус / владелец | Что требуется перед build |
| --- | --- | --- |
| F28 inventory policy | proposal_staged; architect + security reviewer | Общие root/path/revision/coverage semantics; listing/read/index separation; precedence ignores; budgets; fail-closed boundary |
| F26 directory API/UI | proposal_staged; builder + product-manager | Read-only дерево и preview, pagination, empty/error/keyboard/RU/EN; файл не зависит от языка индексатора |
| F27 scan lifecycle | proposal_staged; architect + tester | Durable state machine, recovery/idempotency/cancel, profile storage и migration/rollback contract; bounded workload |
| F29 core adapter | proposal_staged; architect + plugin-runtime-builder | Reuse вместо независимого scanner; versioned structured result, runtime availability, read-only invocation и stale policy |
| F19/F20/F23 coverage | proposal_staged; tester/product-manager | Расширенные fixtures, измеряемые budgets до benchmark и отдельная human acceptance |

Shared ownership: F28 владеет inventory contract; F26 — directory API/reader; F27 — orchestration/profile state; F29 — core adapter/result. Изменения общих application.mts, client.ts, storage и onboarding сериализовать. F18/F24 интегрируют завершённые contracts, F19/F20 проверяют их вместе. Новые имена work locations — план, файлы реализации сейчас не создаются.

Обязательная проверочная матрица: empty/no-Control-plane, Python-only/mixed stack, большой monorepo, Unicode/пробелы, wide/deep directories, ignored/generated/vendor, binary/large/invalid-encoding/unreadable, symlink/junction/hardlink/traversal, root replacement, file rename/delete во время scan, два проекта, cancel/restart/retry. Для F20 сначала фиксируются budgets и hardware/cache; лимит не снимается ради прохождения теста. Существующие guarded source helpers переиспользуются после проверки контракта.

## FUNC-G01 — результаты выполнения {#func-g01-results}

Статус: **closed / implemented_locally_verified**, 7/7 задач F01/F03/F04/F05/F06/F07/F08. Machine status выводится из семи member tasks; на момент закрытия G01 root JSON оставался in_progress, поскольку27 задач других групп были planned; текущий итог после G02 указан выше. Все исходные AC, ID, приоритеты, estimates, Depends on/Blocks/execution_order, delivery-group definitions и M5 references сохранены. Реализация разрешена владельцем 15.11.2026; Git/publication/provider/real credentials не использовались.

| Проверка | Наблюдаемый результат / receipt |
| --- | --- |
| F01 исходный RED | Manifest mismatch на текущем lockfile; `.tmp/func-g01-runtime/manifest-red.log`, `native-red.log`. Простая перезапись pin не использовалась как квалификация. |
| F01/F08 final native | Candidate и production default прошли Discussion/Planning/Execution, inside write/outside+private-temp EPERM, binary/lock/adapter drift до spawn, повторный broker start/Stop и cleanup. `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, `native-default-final-escalated.log`; runtime focused12/12. |
| Native tuple | Codex0.167.0, Node26.5.0, Windows10.0.26200 x64, SQLite3.53.3. Adapter `fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5`; lock `f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac`. Candidate receipt SHA `a2cad642d6f3bc416a04a954f4bbbfa009aae75d5aeacc77bac3f940313dcf4a`. |
| F03/F04 browser | `node tests/web/single-window/func-g01-drafts-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>`:54/54, `.tmp/func-g01-drafts/evidence-C6lIVM/result.json`. Production UI/HTTP/SQLite, concurrent writers и exact ACK revision; source hashes и fixture cleanup. |
| F05/F06/F07 browser | `node tests/web/single-window/func-g01-dashboard-acceptance.mts --synthetic-browser --playwright-core <installed-path> --chromium <installed-path>`:30/30, `.tmp/func-g01-dashboard/evidence-MIaKso/result.json`. RU/EN partial/loading/retry/all-failed/complete, queue parity/reorder/null, updatedAt/create/edit refresh, desktop/mobile readability и screenshots. |
| Shared contracts | AST guard сначала выявил два обратных import edges; после переноса проходят direct/compatibility identity, M1/M2 decoder и theme/locale tests. `node --test tests/web/contracts-boundaries.test.mts tests/web/task-profile.test.mts tests/web/m2-profile.test.mts tests/web/theme-locale.test.mts`; все15 представлены также в полном Web receipt. |
| Typecheck/build | `npm run check:web-m1` и `npm run build:web` exit0. После CSS visual repair build повторён. Предупреждение bundle >500kB сохранено; оптимизация F09/F20 не входила в группу. |
| Full Web + environment repair | `npm run test:web-m1`:507 tests,492 pass/11 fail/4 skip из-за sandbox EPERM при создании link/symlink fixtures; исходный `.tmp/func-g01/web-final.log` сохранён. Ровно15 затронутых случаев повторены с разрешённым executor:15 pass/0 fail/0 skip, `.tmp/func-g01/web-boundary-retest.log`. Итого507 уникальных тестов прошли в двух контекстах; исходный полный запуск не объявляется green. |
| Review | Независимый implementation review `/root/func_g01_review`: closed_allowed; architecture review выполнен до F08. Cycle2 CSS/readability delta: closed_allowed. Проверяющий подтвердил current source/asset hashes и устранил замечание к исторической machine-state ссылке EN. |
| Финальные source/state gates | `tools/check_docs.py --paths`20 changed Markdown sources passed; docs unittest3/3; `validate_task_matrix.py` RU/EN exit0; `validate_task_state_consistency.py .` exit0; `git diff --check` exit0. Проверены34 статуса RU/EN/JSON, unchanged27 task objects/cards, все исходные AC/dependencies/estimates/order/groups/M5 refs и browser source hashes. Групповой отчёт перенесён перед карточками после первого validator rejection, который относил angle-bracket command arguments к последней F34; исходная F34 не менялась. |

Причины повторов и отклонённые попытки сохранены: Chromium startup без нужных executor permissions (0 checks), native MXC unavailable, исходные RED F03/F04 и ACK/refresh race, преждевременные browser assertions до завершения async save, mobile readability RED. Тестовые waits исправлены по наблюдаемому clean/enabled состоянию; product guards, sandbox policy и Chromium sandbox не ослаблялись. Первый build выявил отсутствие toSorted в frontend TypeScript lib; использована копия массива со стандартным sort. AST regression использует уже установленный public parser: установленный TypeScript7 package не предоставляет прежний JS AST API.

Кодовый контракт: existing_capability — прежние handlers, memory Maps, StoreReceipt, strict decoder/preferences и installed parser; smallest_safe_patch — reset/CAS/projection corrections и два compatibility seams; invariants — original CAS, project isolation, unknown≠0, exact runtime pins; dependency_decision — no_new_dependency; risk_selected_tests — browser/state/decoder/import/native + demonstrated link-fixture retest; comment_decision — concurrency/order/boundary intent documented; performance_applicability — не benchmark, budgets не менялись; evidence_and_gaps — current source hashes/tuple и явно раздельные receipts.

Documentation impact: updated — frontend state-management/components, backend lifecycle/modules, architecture containers, testing map, RU/EN source registry, эти карточки и owning JSON; control-plane REQUIREMENTS/PLAN/TEST/RUNLOG синхронизированы. EVALS/prod_test no_change_needed: eval policy и исторический Batch39 не менялись. API docs no_change_needed: endpoints/payload/schema/errors сохранены. Atlas review no_change_needed: container/runtime boundaries в диаграммах прежние; ownership/import detail отражён в architecture/modules. Site build/publication не выполнялись, dependencies не устанавливались. Human acceptance, provider/model behavior и широкая production readiness не заявлены.

## FUNC-G02 — протокол и engine результаты {#func-g02-results}

Текущий статус: **implemented / poc_research_locally_verified; 3/3 closed**. Запрос владельца15.11.2026 разрешил полный execution F30/F31/F32; прежние фразы planning_only в исходных AC описывают авторизацию первоначального планирования, не текущий запрос. Иные FUNC/M5 не запускаются. Protocol/ground truth закреплены до измерений в `tests/fixtures/func_g02/protocol.json` и `corpus.json`; SHA protocol `4d8c4760f20f65c3dde015067ff6e5e59eb6835bca2f89afc99138b43f0639be`, corpus `d727efe0e2fe11a9303262addadbbfb73ab97ec5af844ed585acdbbfe537f11a`.

| Задача | Engine decision и подтверждённая граница |
| --- | --- |
| F30 | bounded_adopt: dependency-cruiser18.6.0 + отдельный TypeScript5.9.2 только для imports.10/10expectededges, precision1/recall1; lexical baseline7/10. Change tasks3/3vs2/3. Cold median817.39ms vs218.27ms;200additionalfiles961.49ms/146.33MiB.4model tests и17engine scenarios. |
| F31 | reject для текущего Windows workspace profile: codebase-memory-mcp0.12.1 отказал admission доindex.12integrity/admission/preservation checks и3unit tests; version/help прошли. Индексация/query/lifecycle/RSS после отказа не выполнялись, метрики null. ACL/source причина — inference, не внутренний trace. |
| F32 | reject tbls1.96.1 как authoritative SQLite metadata: generated omission, valid identifier failure и missingDBcreated при testedread-onlyDSN.26observations=23positive+3candidatefailures. Явно выбрана node:sqlite metadata alternative; tbls200table367.996ms; текущий исправленный Node baseline5.945ms измерен отдельно in-process. Прежний baseline16.892ms сохранён с его provenance. Nullability regression6/6 passed; native receipts не менялись. |

До измерений: pinned version/commit/license, общий synthetic JS/TS/Python corpus, independent expected import/call/change-task oracle, SQLite DDL ground truth,30s small/60s large index timeout,1MiB stdout,1024MiB RSS/cache,200-file/table workload,3cold runs. Query budget5s; prototype interaction budget1500ms. Контракты F28/F20 — draft-only, их production implementation не prerequisite. External tools получают allowlisted read-only projection; config/secret exclusions не становятся graph data. Целевые JS-config/scripts/hooks не исполняются, model/provider/network во время measurement не используются.

Версионированный proposal `paos_engine_poc_snapshot_v1`: meta engine/version/sourceRevision/rootIdentity/policyVersion/coverage/capabilities/warnings, stable node IDs/path/line и typed directed edges/evidence. Import≠call, unknown≠false/zero, unresolved/inferred не становятся observed. Сторонний SQLite/cache не является writable PAOS state. F14 получает import-only F30 + текущий bounded lexical baseline; multilingual semantic/call path остаётся gap. F33 получает явно выбранный Node read-only metadata adapter proposal, не tbls silent fallback. Production integration F14/F33/F34 остаётся planned.

UI design до build: existing V3, read-only explorer — компактная project/mode/source/coverage bar, outline → graph/list/Mermaid → evidence inspector; mobile list-first и collapsible details. URL-only state, project switch очищает incompatible selection, source-line→Back. Graph/import и declared-FK schema — разные семантики; видимая направленность, keyboard/table alternative, zoom/reset, RU/EN, light/dark, loading/empty/partial/error/unavailable/stale. F31 unavailable не показывает fabricated measured graph; proposed symbol/call fixture выделен отдельно. Peer review protocol/wireframe `/root/func_g02_cbm`: approve; renderer compatibility проверяется фактически.

Доказательства: `.tmp/func-g02/f30/result.json`, `tool-audit.json`, `snapshot.json`; F31 `result.json`, native preflight/ACL/source/checksum receipts; F32 `result.json`, `dsn-mode-probes.json`, raw JSON/Mermaid и selected snapshot. Три candidate failures F32 и admission reject F31 сохраняются, не объявляются green. Native findings и benchmark provenance не переписываются из-за последующего metadata/UI repair. Итоговый prototype/typecheck/build прошёл; browser22/22 и общий model/preview набор22/22. Build-bound evidence: `.tmp/func-g02/prototype-build.json`, `prototype-browser/result.json`. Установленный tiny Mermaid отрисовал canonical erDiagram; команды просмотра — в README прототипа.


Независимый review `/root/func_g02_review`, separate_reused_context, два цикла: P2 effective-nullability исправлен и принят; последние два UI P2 исправлены (project-bound direct URLs/export и filtered ER parity). Root проверил delta, новые model/browser regressions, текущие source/build/harness hashes и desktop/mobile screenshots: closed_allowed. Независимый verdict до этих последних исправлений — partial_only; третий review cycle не заявляется. F31 downstream capabilities не выполнялись после admission rejection; три F32 candidate failures сохранены как отрицательное evidence. Закрыты исследовательские решения, не функции продукта.

Команды закрытия: общий22-unit command записан в machine state, `node tests/web/poc/func-g02/prototype-build.mts`, `node tests/web/poc/func-g02/prototype-browser.mts --synthetic-browser --playwright-core ABSOLUTE_INSTALLED_PATH --chromium ABSOLUTE_INSTALLED_PATH`, matrix validators RU/EN, scoped source-docs и preservation checks. Просмотр: `node tests/web/poc/func-g02/prototype-preview.mts`. Control-plane sync обновляет REQUIREMENTS/PLAN/TEST/RUNLOG; EVALS/prod_test no_change_needed: AI behavior и production-test evidence не менялись. Human acceptance и production integration не входят в PoC closure.

Финальное статическое закрытие: оба task-matrix validator прошли; source-docs19 прошли; сохранены31 прочий task object и31 карточка каждого языка, все исходные AC/приоритеты/оценки/зависимости/группы и M5; production sources не менялись. Receipt сохранности и source/build/harness binding: `.tmp/func-g02/closure-consistency.json`; diff check прошёл. Исторический M5 hash до переноса не являлся текущим baseline: исправленная проверка сравнила неизменённый Git source на старте задачи. M5 файл не менялся.

## FUNC-G03 — execution и решения {#func-g03-results}

Статус: implemented / locally_verified,7/7; group exit passed. Пользователь разрешил полное выполнение F28/F26/F27/F02/F29/F10/F18; прежние planning_only фразы относятся к первоначальному планированию. Root отвечает за HTTP/API/storage integration и task/docs sync; lower inventory module выделен отдельному owner. Прочие27 task records, закрытые G01/G02 и M5 сохраняются.

Решение F28: нижний read-only inventory без зависимости от project-sources; отдельные listing/read/index права, stage counts и explicit partial coverage, metadata tree независимо от языкового parser. Hard root/link/sensitive denial выше exclude/include/gitignore; изменения policy/root/revision инвалидируют snapshots. Direct directory listing ленивый; recursive scan bounded.

Решение F27: project registration не ждёт scan; persisted versioned JSON+CAS в profile-owned store_meta, без изменения immutable schema migrations и без task/document pseudo-entities. Cancellation проверяется в analyzer перед atomic publication; timeout Promise без публикационного fence недостаточен. Restart переводит незавершённые jobs в interrupted/recovery, late responses не публикуются.

Решение F29: existing Python core получает только allowlisted F28 projection в owned временном профиле, а не заново сканирует реальный root. Вывод привязан к target root/policy/revision и явно partial; missing Python/version/timeout — unavailable/error, без auto-install или второго scanner.

Проверяемые seams: inventory metadata/checked read и исключения; authenticated directory/read/scan/analysis API; durable scan CAS/cancel/restart; task artifact path normalization; execution file preflight; UI navigation/late responses/freshness/dirty drafts. Сценарии каждой задачи и evidence owner заданы исходными AC и назначенными tests; root собирает итоговое API/browser/native activation evidence.

Кодовый контракт: existing_capability — checked-handle readers, codeIndex worker, core discovery, LocalStore store_meta, createLatestRequest и V3 UI; smallest_safe_patch — lower inventory + bounded directory/job/analysis adapters, sequential shared wiring; invariants — root/policy/revision isolation, no target mutation/secret disclosure, cancellation before publication, dirty drafts preserved; dependency_decision — no_new_dependency; risk_selected_tests — public seams/negative security/recovery/browser; comment_decision — policy ordering, CAS and publication fences; performance_applicability — bounded metadata/worker/projection/polling; evidence_and_gaps — current synthetic checks passed, no provider/human/release claims.

### Итоговые проверки и границы

Все семь участников F28/F26/F27/F02/F29/F10/F18 реализованы и проверены по исходным AC. Остальные27 task objects/cards, прежние priorities/estimates/dependencies/order/groups и3 M5 references сохранены. Общий итог17 implemented /17 planned. Закрытие группы выводится из участников и exit evidence; следующая группа автоматически не запускается.

| Контракт | Текущее evidence |
| --- | --- |
| F28 inventory / F26 Files | lower16 и Files9, policy/CAS/consumer regressions; Add→немедленное дерево→plain reader→line/hash/copy/back; реальные link/root/policy denial |
| F27 lifecycle | durable queued/CAS/cancel/retry/restart; registration replay, запрет late graph publication; настоящие inventory/documents/code/analysis stages |
| F02 references | structured artifacts и legacy paths/backlinks/task filters, stale raw pins, excluded/deleted source denial; production UI backlink→task |
| F29 core | настоящий isolated Python/core9 focused cases и HTTP restart/stale; allowlisted projection, source/confidence/candidates, без target scripts/DB open |
| F10 preflight |32/33 пути,65536/65537 и524288/524289 raw bytes; operations/rename/pins; blocked UI Send сохраняет draft; server/native policy fences |
| F18 freshness | atomic snapshot/stamp, second-channel stale, refresh внутри overlay, dirty draft/original CAS409, disposed polling; modified/renamed source и stale analysis |

Итоговый обязательный `npm run test:web-m1`: **594/594,0skip**, `.tmp/func-g03/full-web-native.log`. Native environment выбран для полного прогона после отказов sandbox на exact synthetic link/junction setup. Первоначальные setup failures сохранены; это не behavior RED. `npm run check:web-m1` и `npm run build:web` прошли; прежний warning chunk >500kB сохранён (performance owners F09/F20). Production UI browser **19/19**, RU/EN × light/dark Files при1440/390px, source/build hashes и screenshots: `.tmp/func-g03/browser-final/evidence-IfLiEa/result.json`. Clipboard, задержанная доставка и UI no-Send runtime boundary явно названы fixtures; core/HTTP/SQLite/FS — настоящая локальная реализация. Внешних запросов/page errors нет; target hashes сохранены.

Native candidate и production-default inspector прошли для adapterRevision `64cd3b58c5688e0673cb3bea5ea250817e10eb281d07c9a4e293ade759f0d33e`; SHA256 candidate receipt `94643d3bee58f959281c18f9f099896959ab92a64ea6e4fc4d5c2ab05c52b450`. Receipts: `.tmp/func-g03/native-candidate-reviewed.log`, `native-default-reviewed.log`; production default не использует candidate exception. Discussion/planning запрещают запись, execution разрешает owned workspace и запрещает outside/temp; drift отказан до child spawn, interrupt, повторное создание broker и isolated-home cleanup прошли. Python `.py` bridge включён в executable source pin (наблюдённый RED/GREEN). Исходный sandbox rpc_rejected receipt сохранён. Provider/model/auth credential operations не использовались.

Independent review `/root/func_g03_review`: cycle1 separate_fresh_context воспроизвёл P2 captured-policy race; root исправил общую причину final registry fences и atomic task/registry observation. Deterministic RED2/2 и consumer RED3/3 сохранены; cycle2 separate_reused_context независимо подтвердил5/5, tester_verdict=closed_allowed. Root repair regression30/30 и affected consumer/API20/20 прошли; affected58 имели57pass/1sandbox link setup failure, exact native retest1/1, затем full native594/594. Failed setup/probe directories и временный executable удалены внутри owned containment; receipts сохранены. Защитные проверки не ослаблялись.

Документация: обновлены canonical API/events/backend/recovery/data-flow/inventory/discovery/queries/security/transactions/frontend/navigation/state/components и RU/EN registry; source-docs30 и оба matrix validators прошли. Root REQUIREMENTS/PLAN/TEST/RUNLOG синхронизированы. EVALS/prod_test no_change_needed: rubric, model/prompt и Batch39 evidence не менялись. Atlas/MkDocs no_change_needed: существующий architecture data-flow владеет этой runtime boundary; новых lifecycle routes/navigation pages нет. Итоговая preservation/source/build/native binding — `.tmp/func-g03/closure-consistency.json`.

Принятые ограничения: существующий desktop distribution не включает checkout core/catalog и явно возвращает unavailable; packaging принадлежит F17. Projection/output/time ограничены; portable OS RSS hard cap и общая performance qualification принадлежат F09/F20. Будущие Map/schema/code-table consumers — F14/F33/F34. Synthetic local closure не доказывает provider execution, human acceptance, массовую или коммерческую release readiness. Dependencies не устанавливались; реальные profiles/credentials/targets, global config и Git/publication не менялись. Rollback только own hunks; после executable changes заново квалифицировать manifest, сохранить user files и прежнее G01/G02/M5 evidence.

## FUNC-G04 — execution и решения {#func-g04-results}

Статус: implemented / locally_verified_with_measured_limits. Владелец разрешил F20/F09/F14/F33/F34. Сохранён dirty baseline G03193files, HEAD5a9c87b; прочие29task records и M5 остаются у прежних владельцев/evidence. Root владеет shared storage/HTTP/API/App, статусами и control-plane sync; независимые участки имеют явные file boundaries.

Порядок: F20 protocol/baseline до source fixes F09; F14 после measured fixes; F33 после explicit source/adapter design; F34 после совместимых code/schema consumers. Не более root+двух специалистов, затем independent review. Git/publication/providers/live DB/global installation/configuration не входят.

Решение F33: Node26 SQLite readOnly schema-only extraction явно выбранного project-local offline SQLite, отдельно от profile DB PAOS. Нет автоматического открытия кандидатов, копирования DB bytes, чтения rows, project SQL/scripts/extensions или PostgreSQL scope из tbls. Hard-link/reparse/root/policy/private guards и отдельный admission предшествуют доступу. Windows native read lease держит target и ancestors от root до target против write/delete, пока SQLite владеет вторым handle; фиксированный trusted PowerShell/C# helper, без policy bypass/установки. Node проверяет root/identity/policy после readiness; extraction закрывается до release lease. Sidecars, WAL header, busy lease и unsupported host дают fail closed. Одни pre/post path checks не выдаются за защиту от ABA. Metadata извлекаются bounded trusted SQL/authorizer с time/output/SQLite limits; JS heap limit не является native-memory guarantee. Source hashes/policy проверяются перед публикацией; Windows lease conformance обязательна перед closure.

Language/backend и UI gates F14/F34 будут записаны здесь до build, с сохранением measured adopt/reject F30/F31/F32 и V3 design. Test seams: existing public API, source/scan snapshots, source selection, graph/schema/links queries и rendered navigation; synthetic native/browser fixtures разрешены, provider/human acceptance отдельно.

Code-change contract: existing_capability=F28checkedinventory/F27CAS/NodeSQLite/rolldown+TypeScript/V3D3Mermaid/LocalStore; smallest_safe_patch=measured read/cache fixes и bounded adapters/consumers; invariants=project/root/policy/revision/late-publication isolation и preservation; dependency_decision=no_new_dependency, installed/native capabilities first; risk_selected_tests=protocol/groundtruth, auth/path/read-only/recovery/cancel, API/browser/native; comment_decision=authority/lease/cache/semantic limits; performance_applicability=required F20 before/after; evidence_and_gaps=current measurements pending, no readiness claim.

### Production navigation и wireframes — выбор до build

Technical design использует существующие V3 tokens/components, D3, escaped Mermaid и полноценную table/list альтернативу. Он выбран для реализации; human acceptance этим не заявлена. Files, Map и Database — независимые project navigation entries; Settings владеет только регистрацией/выбором источника.

| Поверхность | Desktop wireframe | Mobile и состояния |
| --- | --- | --- |
| Map | Dependencies/Symbols → search/direction/edge filters + revision/coverage → object list / graph-list-Mermaid / evidence drawer; incoming/outgoing, bounded path/impact, source line и Files links | Сначала список; collapsible evidence, keyboard node selection/focus return; zoom/reset; loading/empty/partial/error/unavailable/stale |
| Database/Schema | Source/revision/coverage + scan/cancel/retry → bounded ERD/table одной страницы → columns/PK/FK/index/views выбранной таблицы; safe export и source definition при наличии evidence | Table alternative, search/type filters, selection в рамках проекта; кандидаты не открываются автоматически |
| Database/Changes | Совместимые baseline/current revisions → added/removed/changed; rename остаётся add/remove без доказательства | Явные no-baseline/incompatible/stale; source switch не сравнивает разные БД |
| Database/Code usages | Table→read/write/unknown и confirmed/inferred/unresolved→file/span/evidence; обе совместимые revisions, truncation/cursor, bounded agent context | Доступный список и source line; Files reader возвращается к related tables, Map имеет DB-filter и incomplete impact |
| Settings/Project | Явный relative source + observed metadata pin + settings CAS → Select/Clear, затем отдельный scan | not_configured/none_found/unavailable/forbidden объяснены; нет DSN/credentials/target scripts |

F20 protocol закреплён до замеров в tests/fixtures/func_g04/protocol.json: неизменные WEB-NFR thresholds, три повтора/bounded soak, actual hardware/cache отдельно от reference4-core, полные10k задач/100k сообщений/~200MiB/1k файлов и точные boundaries. API-visible latency отдельно от rendered UI/cold GUI. Budget failures сохраняются и становятся measured inputs F09.

### F14/F34 — выбранная production-композиция до build

- F14: установленный public rolldown/utils.parseSync1.2.18 (OXC AST), JS/TS/JSX/TSX/MJS/CJS/MTS/CTS; lexical define/read/write/reference/call внутри файла. Cross-file связи — только imports/reexports, literal dynamic import и unshadowed literal require; это не runtime calls. Pure allowlist resolver работает только по разрешённым F28 путям и безопасно прочитанным root tsconfig baseUrl/paths. JSON comments/extends/references/package exports и неизвестные aliases дают явный partial/unresolved; target config/code не исполняется. Цель ground truth G02: precision1, recall≥0.9 на10 import edges; Python и другие языки показываются unsupported.
- G02 dependency-cruiser18.6.0 остаётся bounded_adopt PoC import-only; его изолированная .tmp установка и TypeScript5.9.2 не становятся production dependency. Installed TypeScript7.0.2 не экспортирует прежние createSourceFile/resolveModuleName APIs. CBM reject сохранён. Проверенный public ResolverFactory из rolldown/experimental в Windows отклонил допустимые paths с restriction; без restriction обнаружил parent package.json вне проекции. Он не выбран. Явная production альтернатива — уже установленный AST плюс небольшой deterministic allowlist resolver; отсутствие resolver capability не переключает backend молча.
- F14 restart/eviction явно инвалидирует memory graph; cursor содержит cache generation и filters. Новый rebuild обязателен. Files независим. Rollback — вернуть только G04 parser/resolver/UI hunks, оставить F28 guards и G03 scan contracts.
- F34: JS/TS+SQL; literal SELECT FROM/JOIN, INSERT INTO, UPDATE, DELETE FROM, CREATE/ALTER/DROP TABLE; один ORM — Prisma static subset (schema.prisma model/@@map + literal file: datasource, статически связанный PrismaClient/delegate). Tokenizer/AST отделяет comments/strings/aliases. Confirmed требует совпадающий registered DB source: literal new URL(...,import.meta.url) для node:sqlite либо literal Prisma datasource. Cwd/env/dynamic SQL/untraced binding/table-name-only совпадения — inferred/unresolved, не confirmed.
- F34 evidence связывает file/span/symbol/query/model/table/source/operation/method/confidence/reason и code+schema revisions. Одинаковые таблицы разных БД не сливаются. Никакого выполнения SQL/Prisma/project code, чтения строк, DSN или runtime call graph. Перед продвижением — ground truth по типам, source scope/revision/cancel guards, bounded context≤32KiB и сравнение static manual-search задач с query links по correctness/missed files/tests/context/time.

Примечание целостности: выбранный до build текст восстановлен из исходного temporary design packet после исправления inter-character Markdown escaping; исходные карточки и AC не менялись.

### FUNC-G04 — итоговые проверки

Пять карточек F20/F09/F14/F33/F34 реализованы; общий итог матрицы — 22 implemented / 12 planned. Исходные AC, оценки, dependencies, группы и M5 references сохранены. Закрытие означает bounded local synthetic verification с измеренными ограничениями. Review: separate_reused_context, /root/func_g04_review, tester_verdict=closed_allowed.

Web: 658/658, 0 fail/skip (.tmp/func-g04/web-closure-native-final.log); typecheck и build текущего UI прошли. Browser: 18/18, 204 source hashes, dist binding, 30 screenshots, 200 объектов на четырёх страницах, настоящий API/native lease и service/profile restart; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json. Native candidate и production-default прошли для adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b, provider/model/credential operations — 0. Три текущих F20 receipts: .tmp/func-g04/scale-closure/result-diagnostic-1794778219987.json; .tmp/func-g04/scale-closure/result-reference-1794778236139.json; .tmp/func-g04/scale-closure/result-filesystem-1794778628384.json. Все 133 входных source hashes совпадают с текущим кодом; protocol 37c20aadc0d3474ef78cf86928e9ee1727be7bf415152fc393e92c8b079af625 не менялся.

| Metric | Current closure run | Comparison |
| --- | --- | --- |
| Indexed search p95 / 36 | 159.06 ms | 500 ms |
| Command ACK p95 / 36 | 403.71 ms | 500 ms |
| Task page 50 p95 / 36 | 3.33 ms | 1000 ms |
| Commit → freshness API p95 | 404.80 ms | 1000 ms |
| Task Manager p95 / 3 | 504.80 ms | 1000 ms |
| HTTP creation after full seed | 1063.57 ms | 10 000 ms |
| Graph rebuild / 1000 files | 11475.70 ms | 60 000 ms |
| Graph status / 3 | 313.49 / 294.86 / 277.69 ms | 1000 ms |
| Soak | 120.15 s / 119 iterations | 120 s |
| Browser per-process backend/harness | 253.07 MiB | 1024 MiB |
| Browser aggregate sampled current | 1101.32 MiB | diagnostic only |

Холодные history/catalog generations сохраняют измеренные превышения comparison 1000 ms. Полный обход 10k/10001 directories завершается явным bounded timeout 30 s; lazy listing имеет bounded/partial outcome. JS heap не ограничивает native RSS на уровне ОС. Browser aggregate current/lifetime peaks остаются диагностикой, общего memory pass нет. Фактический host: i7-12700H/20 logical CPUs/15.73 GiB/Node26.5/SQLite3.53.3. Reference 4-core hardware, cold GUI, отсутствие долгосрочных утечек, human/provider/production/commercial acceptance не квалифицированы.

Сохранены неуспешные попытки: baseline oversized startup/repeated graph reads; первый Web656/657 с authority error contract; native stack exits; ERD100objects/1969ms; anchor/filter и mobile-heading bugs; ошибочный aggregate RSS assertion; последний P2 __proto__ dictionary RED. Для продуктовых ошибок выполнены focused fixes и текущие regressions. Поздний обычный sandbox run получил lease/symlink denials: 631 pass/16 fail/3 skip, один зависший owned test child остановлен; receipt сохранён, разрешённый native repeat прошёл все658. Browser attempt10 прошёл на manifest до promotion; current binding — attempt11. Failed receipts не переписывались.

Docs: 26 domain Markdown sources, RU/EN матрица и четыре root control-plane файла — всего32. Registry RU/EN ссылается на Context7 primary sources. Повреждённые временным helper G04 design block и registry heading исправлены до финальных source checks; исходные cards/AC сохранены. EVALS/prod_test и diagram/MkDocs routes: no_change_needed, поскольку AI rubric, Batch39 и atlas/navigation contract не менялись. Site freshness не заявлена. Cleanup удаляет owned fixtures и копию test executable, сохраняя существующие cache/runtime и user files. Rollback — только own hunks; executable drift требует повторной native qualification.

## FUNC-G05 — execution и решения {#func-g05-results}

Статус: implemented / locally_verified_with_explicit_limits,5/5. Scope F11/F12/F13/F15/F16. На старте сохранены HEAD8c2fbd4 и1120 source snapshots; dirty был только own lifecycle marker. Остальные29 task records, исходные AC/groups/M5 и receipts G01–G04 сохранены. Root интегрировал shared files; независимая autonomy implementation и read-only source/design/review выполнялись по уточнённому ownership. Текущие проверки и пределы claims приведены ниже.

F11/F16 source gate: выбранный App-agent bridge предоставляет local PAOS history, server-observed intervals и mediated operations, но не host-history/model/effort/loaded-asset/token attestation. Официальный App Server поддерживает history/usage methods; это другая capability с отдельным pinned-version admission. Private host stores не читаются, новый API-key route не выбирается, наблюдения не выдумываются. Open/unresolved intervals остаются unknown; task elapsed/agent effort и mediated commands/all host tools различаются; tokens/cost остаются unknown без поддержанного источника. F12 external source и F15 extension contracts закрепляются до соответствующего build.

Code-change contract: existing_capability=F28 checked sources, LocalStore CAS, G04 fixed native lease, existing Team/Sessions/Artifact/Autonomy and V3 UI; smallest_safe_patch=route-aware projections and bounded adapters/writer, preserve unrelated routes; invariants=project/profile/root/policy isolation, raw source pins, idempotency, no invented attestation or metrics, no lost user edits; dependency_decision=no_new_dependency, installed/native capabilities first; risk_selected_tests=existing public HTTP/service/worker seams plus real synthetic native/browser conflict/recovery/isolation tests; comment_decision=comment_needed for authority, retention, journal and metric semantics; performance_applicability=required for bounded query/output/journal/fetch paths, no unrelated full F20 rerun; evidence_and_gaps=proceed with local source/synthetic evidence, host/provider/real-target acceptance separate.

F13 design gate: source-vs-SQL ownership определяется server-derived origin. SQL document apply выполняется одним Store CAS transaction вместе с proposal/outcome. Workspace apply допускает только существующие readable regular .md/.txt до512KiB после F28 admission; AGENTS.md, SKILL.md, .codex/config/hooks/rules/plugin/skill instruction paths, ignored/generated/private/link/hardlink/reparse и redacted before/after запрещены. Apply-preview закрепляет project/profile/root/policy/epoch, proposal revision, raw before identity/hash и persisted after hash; final apply не принимает путь или новый body от клиента. Новые staged proposals сохраняют server-derived source pins; legacy без pins требует refresh/restage. Windows fixed trusted helper держит root→parent handles и exclusive existing-target handle, проверяет raw hash, ждёт durable private prepared journal и final scope/policy fence, затем пишет/flushes/rehashes через тот же handle. Это защищённая in-place запись с recovery, не atomic replace. До записи устанавливается SQLite fence против смены policy/authority/cutover; unresolved outcome блокирует новые записи и не получает автоматический replay. Current=after → applied, current=before → явный retry, иное → recovery_required без overwrite. Rollback требует отдельного preview и CAS текущего hash. Journal хранится в protected profile metadata вне public document/settings snapshots: ≤4 records/project, ≤2MiB/record и ≤8MiB/project; evict только terminal, unresolved не удаляется, quota fail closed. Public events/API содержат metadata/hashes, без raw journal bytes. Существующие readers/writers дают busy; пользовательские процессы не закрываются. Root control-plane docs кроме AGENTS допустимы только через exact-file preview; source и SQL не синхронизируются автоматически.

### F12 source gate до build

Deprecated default openai/skills отклонён. Выбран актуальный public package superpowers в openai/plugins, pin d420d13051bffe4543ed39e30fa46b87148e47dd: manifest6.3.0 и фактический MIT LICENSE проверены. Поиск ограничен этим явным package, не всем marketplace. Только fixed anonymous api.github.com GET commit/root/plugins/package trees; query/project context, credentials, redirects, чужие repositories, scripts/hooks/installation и provider calls исключены. Limits:10s deadline,2MiB JSON/body,1000 entries package tree,256KiB SKILL,32 skill-local Markdown/text resources,1MiB bundle,15min catalog cache/четыре bundle cache entries. Git blob SHA проверяет bytes отдельно от raw SHA256. Preview сохраняет license/provenance и весь поддержанный resource set; links/submodules/outside-skill references/unknown licenses/executable или unsupported resources fail closed. Поиск не устанавливает; managed copy проходит existing preview/apply/CAS с dependency checks и cached immutable source proof. Timeout/offline/rate limit сохраняют local sources. Native plugin bindings не подключаются; нужна проверка совместимости владельцем.


Live index inspection выявила agents/openai.yaml в каждом текущем skill: исходный text-only subset не давал пригодного импорта. До расширения поддержки закреплено точное исключение: skill-local agents/openai.yaml сохраняется как opaque UTF-8 text, не разбирается как исполнимая host configuration и не активируется. Остальные unsupported resource guards сохранены; исходный failed anonymous receipt не переписывается.

### FUNC-F15 — граница реализации

Optional `maxCommandsTotal` ограничивает суммарные durable reservations команд за окно policy; отсутствие поля сохраняет прежний v1 контракт. Повторы operationId не расходуют лимит повторно; неопределённые исходы не возвращают резерв. Последняя разрешённая команда может завершиться, новые команды/runs после исчерпания не допускаются. Счётчик reservations отличается от наблюдаемых команд F11; tokens/cost и host tools остаются unavailable и не объявляются ограниченными. Узкие allowedPaths сохраняют существующий запрет. На интервал реализации F15 единственный code writer — агент document_apply, только autonomy contracts/service/UI/tests; root выполняет документацию и read-only подготовку.

Промежуточный checkpoint перед final qualification: F11 lifecycle/scope/recovery3/3; F12 source/negative cases3/3 и anonymous upstream8GET; F13 native13 cases (последняя rollback regression1/1), pairedAPI1/1; F15 policy/runtime20/20; F16 identity/cursor2/2; cross-capability pairedAPI1/1. Независимый review обнаружил и проверил исправление F13 rollback-operation. Native candidate и production-default qualification прошли на adapter aa9c663dd1df54c6f47258234b5b9e9b5df6e0980e5ff58677e4403e30584bcc без provider/model/credential operations; на том checkpoint итоговые fullsuite/browser/status checks ещё выполнялись; итог ниже.

<!-- FUNC-G05 ownership refinement: После read-only сверки границ ownership уточнён: агент владеет только autonomy contract/service/UI/tests, root — team/history/metrics/dashboard. Пересекающихся файлов нет; full build/suite выполняются после общего freeze. -->

### Итоговые evidence

Пять задач implemented; группа закрыта по локальным техническим AC. Fullweb686/686,0fail/skip; typecheck/build passed; browser16/16 (.tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json); native candidate→qualified default passed, adapter aa9c663dd1df54c6f47258234b5b9e9b5df6e0980e5ff58677e4403e30584bcc. Исходные actual RED/setup/selector receipts сохранены; failed attempts не переименованы в passed.

Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.

Control-plane sync: REQUIREMENTS/PLAN/TEST/RUNLOG updated; EVALS=no_change_needed (no model/prompt/route/rubric changes); prod_test=no_change_needed (Batch39 ledger unchanged); atlas/navigation=no_change_needed (existing lifecycle boundaries, no new docs page/workflow). Root size advisories predate this slice; docs-maintainer owns a separate preservation-safe compactness follow-up. Git/publication/install/provider/real-profile operations absent. Final independent evidence review and preservation gates are recorded in latest verification.

Status audit: исправлена унаследованная неточность RU overview M5 (там ошибочно повторялись FUNC counts). Текущий owning M5 JSON подтверждает56 карточек,53 implemented/3planned; его содержимое и статусы не изменены.

Независимый final review: context_mode=separate_reused_context; reviewer=/root/func_g05_completion_review; tester_verdict=closed_allowed; closure_level=locally_verified_with_explicit_limits. Evidence .tmp/func-g05/final-review.json, closure-consistency.json, docs-final.log (28sources), matrix-ru.log, matrix-en.log. Независимо пересчитанные source/build/native hashes совпали; открытых implementation/evidence blockers нет. Два ожидаемых bootstrap401 SESSION_REQUIRED сохранены, unexpected HTTP/page errors и external browser requests отсутствуют. Parent Node peak237100KiB не является aggregate OS memory measurement.

## Подробные карточки

### Task `PAOS-FUNC-01`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-01 — Восстановить квалификацию native runtime после redesign
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:17
- Priority: P1
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-08`, `PAOS-FUNC-10`, `PAOS-FUNC-15`, `PAOS-FUNC-16`, `PAOS-FUNC-17`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-21`, `PAOS-FUNC-22`
- Source: Lock SHA-256 d279009a… в manifest и f126e4dc… текущего файла не совпали; adapter99 совпал в аудите15.11. [packages/contracts/runtime/manifest.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/runtime/manifest.mts), [apps/local-service/src/runtime/sandbox-broker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/sandbox-broker.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Восстановить квалификацию native runtime после redesign.
- Technical value: Согласовать lockfile, manifest и native broker без ослабления проверки fingerprint.
- Product value: Запуск задачи из обновлённого интерфейса действительно приводит к выполнению.
- Scope: `packages/contracts/runtime/manifest.mts`; `packages/contracts/runtime/qualified-manifest.json`; `apps/local-service/src/runtime/sandbox-broker.mts`; `tests/web/runtime-manifest.test.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Запуск задачи из обновлённого интерфейса действительно приводит к выполнению. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: На текущем lockfile воспроизведён отказ package_lock_mismatch; исправление не подменяет квалификацию простой перезаписью хеша. AC2: На заново квалифицированном tuple новый broker исполняет synthetic command внутри разрешённого root и отклоняет запись снаружи. AC3: Отрицательные сценарии для изменённых binary, lockfile и adapter остаются fail-closed; повторный старт проходит.
- Verification gates: `node --test tests/web/runtime-manifest.test.mts` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: native_synthetic_acceptance_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: plugin-runtime-builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Воспроизведён package_lock_mismatch; candidate-only квалификация допускает изменённые lock/adapter pins только для нового native acceptance. Manifest продвинут после passed native receipt; production loader не ослаблен.
- files touched / work locations: `packages/contracts/runtime/qualified-manifest.json`, `tests/web/runtime-manifest.test.mts`, `tests/web/single-window/sandbox-broker-acceptance.mts`
- technical value delivered: Текущий lockfile квалифицирован вместе с binary/Node/OS/SQLite и adapter; fail-closed drift checks сохранены.
- product value delivered: Новый native broker выполняет synthetic command в разрешённом root и отклоняет внешнюю запись.
- actual implementation date and time: 15-11-2026 18:17
- verification evidence: RED `.tmp/func-g01-runtime/manifest-red.log`, `native-red.log`; GREEN runtime-manifest + sandbox-broker 12/12; native candidate/default `.tmp/func-g01-runtime/native-candidate-initial-escalated.log`, `native-default-initial-escalated.log` exit0, three modes, inside write/outside+temp EPERM, binary/lock/adapter drift rejected before spawn, repeat start/Stop/auth cleanup. Initial sandbox MXC failure retained in native-candidate-initial.log. Final F08 requalification: `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, `native-default-final-escalated.log` exit0; adapter fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5, lock f126e4dceeb06cb9644fe1167cbb5b2b2689fb8022325d54292445398ad30aac; runtime12/12. Binary cleanup verified.
- residual risks: Bounded native offline acceptance; provider/model/production/human acceptance не заявлены. Финальный tuple после F08 проверен.
- follow-up: Нет в пределах AC; новая правка pinned sources требует новой квалификации.
- Documentation impact: updated; `docs/backend/lifecycle.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Описаны exact tuple, candidate promotion, текущие receipts и граница claims.

### Task `PAOS-FUNC-02`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-02 — Восстановить связи структурированных артефактов с задачами
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-13`, `PAOS-FUNC-14`, `PAOS-FUNC-19`
- Source: taskPaths читает files/artifactReferences; Editor отдельно сохраняет artifacts. [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/web/src/features/tasks/Editor.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/Editor.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Восстановить связи структурированных артефактов с задачами.
- Technical value: Унифицировать нормализацию files, artifactReferences, artifacts и fileContexts.
- Product value: Документ находится из задачи, а задача — из документа и поиска.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/impact/service.mts`; `tests/web/skill-generation-artifacts.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Документ находится из задачи, а задача — из документа и поиска. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Задача со ссылкой только в artifacts.reference находится фильтром каталога по taskId и отображается в связанных задачах документа. AC2: Legacy artifactReferences/files сохраняют поведение; дубли и разделители путей нормализуются. AC3: Внешний URL не принимается за локальный путь; stale revision и недоступный файл отображаются явно. AC4: File references используют нормализацию и root identity F28; каталог, дерево и задачи ссылаются на один разрешённый relativePath/revision. Deleted/moved/excluded не превращаются в доступный документ или право чтения.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Сначала воспроизведение RED на текущей версии, затем исправление и GREEN. Общие docs gates применяются при изменении документации.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Завершить F29/F10/F18 и финальные gates FUNC-G03.

#### Completion Report

- status: implemented
- what was done: Единая нормализация explicit task references связала structured artifacts и legacy paths с каталогом и backlinks; stale pin отделён от доступности текущего документа и read authority.
- files touched / work locations: apps/local-service/src/artifacts/references.mts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/task-manager/service.mts; apps/web/src/features/artifacts/ArtifactExplorer.tsx; tests/web/skill-generation-artifacts.test.mts
- technical value delivered: Registry/root/policy/revision contracts проверены через реальные HTTP/SQLite/FS и production React.
- product value delivered: Данные проекта доступны с явными причинами недоступности и сохранённой навигацией.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0; .tmp/func-g03/f02-focused-final.log:21/21
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Завершить F29/F10/F18 и финальные gates FUNC-G03.
- Documentation impact: updated; docs/code-intelligence/queries-impact.md; docs/code-intelligence/queries-impact.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-03`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-03 — Полностью сбрасывать черновик новой задачи
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:26
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Reset не сбрасывает rawInputs; эффект очистки требует entity. [apps/web/src/features/tasks/Editor.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/Editor.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Полностью сбрасывать черновик новой задачи.
- Technical value: Синхронизировать модель, rawInputs, estimate, preview и dirty-state при Discard.
- Product value: После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче.
- Scope: `apps/web/src/features/tasks/Editor.tsx`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: После отмены пользователь не видит данные, которые уже отсутствуют в сохраняемой задаче. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: В новой задаче заполнить criteria/risks/references/estimate, нажать Discard: все поля и модель возвращаются к одному пустому состоянию. AC2: Следующее сохранение не возвращает отменённые данные; dirty/preview/error не вводят в заблуждение. AC3: Для существующей задачи Discard возвращает серверную revision и не уничтожает чужие изменения.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: browser_reproduction_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 3–6 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Discard очищает rawInputs, reason/error, модель, estimate, preview и dirty-state. Сохранение после отмены не возвращает отменённые данные; conflict сохраняет dirty draft, discard принимает текущую серверную revision.
- files touched / work locations: `apps/web/src/features/tasks/Editor.tsx`, `tests/web/single-window/func-g01-drafts-acceptance.mts`
- technical value delivered: Discard очищает rawInputs, reason/error, модель, estimate, preview и dirty-state. Сохранение после отмены не возвращает отменённые данные; conflict сохраняет dirty draft, discard принимает текущую серверную revision.
- product value delivered: Отмена предсказуемо очищает форму; concurrent изменения не теряются неявно.
- actual implementation date and time: 15-11-2026 18:26
- verification evidence: Baseline RED `.tmp/func-g01-drafts/evidence-DGhYbl/result.json`; ACK-race RED evidence-pS0YXr/result.json; final `.tmp/func-g01-drafts/evidence-C6lIVM/result.json` 54/54 on final F08 build, actual UI/HTTP/SQLite concurrent writes, source/build hashes, fixture cleanup; typecheck exit0. Retained sandbox startup and premature-oracle receipts3Hhk34/8nW2Uj/W7ljj0; bounded observable waits repaired test timing.
- residual risks: Browser desktop/mobile geometry проверены; human acceptance и полная UX/a11y qualification отдельно. Drafts остаются только в памяти страницы.
- follow-up: Нет в пределах AC; сквозная F19 и human F23 остаются planned.
- Documentation impact: updated; `docs/frontend/state-management.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Отдельные разделы F03/F04 описывают reset/navigation/CAS, текущее source ownership и evidence54.

### Task `PAOS-FUNC-04`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-04 — Сохранять черновик назначений workflow при навигации
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:26
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Draft cache не включает typeMapping/mappingDirty. [apps/web/src/features/workflows/WorkflowManager.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/workflows/WorkflowManager.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Сохранять черновик назначений workflow при навигации.
- Technical value: Включить typeMapping и исходную CAS revision в общий жизненный цикл draft.
- Product value: Пользователь не теряет несохранённые назначения процессов при переходе между разделами.
- Scope: `apps/web/src/features/workflows/WorkflowManager.tsx`; `tests/web/single-window/m2b-browser-acceptance.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь не теряет несохранённые назначения процессов при переходе между разделами. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Изменить mapping типа задачи, уйти из Settings и вернуться: черновик восстановлен либо уход заранее остановлен понятным выбором. AC2: Save/Discard корректно снимают dirty-state; default workflow и mapping не перетирают друг друга. AC3: Смена проекта не переносит черновик в другой проект; stale save возвращает conflict без потери введённого.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: browser_reproduction_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Memory-only draft хранит typeMapping/mappingDirty/original CAS revision отдельно от definition. Navigation/project changes изолированы; Save/Discard assignments корректны; default-only ACK принимает только собственную committed revision, не чужой последующий refresh.
- files touched / work locations: `apps/web/src/features/workflows/WorkflowManager.tsx`, `tests/web/single-window/func-g01-drafts-acceptance.mts`
- technical value delivered: Memory-only draft хранит typeMapping/mappingDirty/original CAS revision отдельно от definition. Navigation/project changes изолированы; Save/Discard assignments корректны; default-only ACK принимает только собственную committed revision, не чужой последующий refresh.
- product value delivered: Несохранённые назначения переживают навигацию и не перетирают чужую запись.
- actual implementation date and time: 15-11-2026 18:26
- verification evidence: Baseline RED `.tmp/func-g01-drafts/evidence-DGhYbl/result.json`; ACK-race RED evidence-pS0YXr/result.json; final `.tmp/func-g01-drafts/evidence-C6lIVM/result.json` 54/54 on final F08 build, actual UI/HTTP/SQLite concurrent writes, source/build hashes, fixture cleanup; typecheck exit0. Retained sandbox startup and premature-oracle receipts3Hhk34/8nW2Uj/W7ljj0; bounded observable waits repaired test timing.
- residual risks: Browser desktop/mobile geometry проверены; human acceptance и полная UX/a11y qualification отдельно. Drafts остаются только в памяти страницы.
- follow-up: Нет в пределах AC; сквозная F19 и human F23 остаются planned.
- Documentation impact: updated; `docs/frontend/state-management.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Отдельные разделы F03/F04 описывают reset/navigation/CAS, текущее source ownership и evidence54.

### Task `PAOS-FUNC-05`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-05 — Обозначить неполное покрытие portfolio рядом с итогами
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-11`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: aggregateSnapshots возвращает partial; dashboard totals его не показывает. [apps/web/src/features/dashboard/model.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/model.ts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Обозначить неполное покрытие portfolio рядом с итогами.
- Technical value: Провести partial/loaded/expected из агрегатора в отображение KPI и progress.
- Product value: Частично загруженные проекты не выглядят как полный итог портфеля.
- Scope: `apps/web/src/features/dashboard/model.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Частично загруженные проекты не выглядят как полный итог портфеля. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: При успехе1 проекта и ошибке1 проекта рядом с totals показано «1 из2; данные неполные». AC2: Неизвестные значения не заменяются нулём; progress явно относится к доступной выборке. AC3: Loading, retry, all-failed и восстановление полного покрытия проверены в RU/EN.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 3–6 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Показаны loaded/expected и partial рядом с totals/progress, ожидаемое количество берётся из projects до первого ответа.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`, `apps/web/src/design/parity.css`
- technical value delivered: Показаны loaded/expected и partial рядом с totals/progress, ожидаемое количество берётся из projects до первого ответа.
- product value delivered: Частичный portfolio больше не выглядит полным; unknown не превращается в ноль.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures для отказов/timestamps/очереди; provider/human acceptance и полная accessibility qualification не заявлены.
- follow-up: Нет в пределах AC; сквозная приёмка F19/F24 остаётся отдельной.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Описаны актуальные правила отображения, source owners и browser evidence.

### Task `PAOS-FUNC-06`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-06 — Исправить нумерацию очереди на dashboard
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P3
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-19`
- Source: Backend indexOf+1, dashboard position+1. [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Исправить нумерацию очереди на dashboard.
- Technical value: Единый 1-based контракт позиции между scheduler и frontend.
- Product value: Одинаковый порядок задач на dashboard и в управлении очередью.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Одинаковый порядок задач на dashboard и в управлении очередью. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Для backend positions1/2 dashboard показывает №1/№2. AC2: Для null номер отсутствует; reorder отражается одинаково на обеих поверхностях.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 1–3 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Убрано повторное +1 для scheduler position; null остаётся без номера.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`
- technical value delivered: Убрано повторное +1 для scheduler position; null остаётся без номера.
- product value delivered: Dashboard и QueueManager показывают одинаковые позиции и reorder.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures для отказов/timestamps/очереди; provider/human acceptance и полная accessibility qualification не заявлены.
- follow-up: Нет в пределах AC; сквозная приёмка F19/F24 остаётся отдельной.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Описаны актуальные правила отображения, source owners и browser evidence.

### Task `PAOS-FUNC-07`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-07 — Сортировать последние задачи по времени
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Дефект; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:23
- Priority: P3
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-18`, `PAOS-FUNC-19`
- Source: Dashboard slice(-3), storage ORDER BY id. [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Сортировать последние задачи по времени.
- Technical value: Задать явную сортировку по updatedAt с устойчивым tie-breaker и unknown policy.
- Product value: Блок последних задач ведёт к действительно недавней работе.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `tests/web/ui-v3-dashboard.test.mts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Блок последних задач ведёт к действительно недавней работе. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: UUID-порядок специально противоположен времени: отображаются3 последних по updatedAt. AC2: Равные и отсутствующие timestamps обрабатываются детерминированно; подпись поясняет выбранную семантику. AC3: Создание и изменение задачи обновляют состав блока после refresh.
- Verification gates: `node --test tests/web/ui-v3-dashboard.test.mts` Выполненные команды, RED/GREEN и provenance записаны в Completion Report.
- Risks / approval gates: reproduce_then_fix; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 2–4 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Добавлена чистая сортировка по updatedAt с ID tie-breaker и unknown-last; семантика указана в UI.
- files touched / work locations: `apps/web/src/features/dashboard/Dashboard.tsx`, `model.ts`, `tests/web/ui-v3-dashboard.test.mts`, `tests/web/single-window/func-g01-dashboard-acceptance.mts`
- technical value delivered: Добавлена чистая сортировка по updatedAt с ID tie-breaker и unknown-last; семантика указана в UI.
- product value delivered: Три последние задачи отражают создание и изменение после refresh.
- actual implementation date and time: 15-11-2026 18:23
- verification evidence: Browser RED `.tmp/func-g01-dashboard/evidence-IGkHii/result.json`; final GREEN `.tmp/func-g01-dashboard/evidence-MIaKso/result.json` 30/30, source/build hashes, RU/EN loading/partial/all-failed/retry/complete, 1-based/null/reorder/QueueManager parity, updatedAt ordering/create/edit refresh, desktop1440/mobile390 no overflow; model7/7. Visual QA added mobile readability oracles: RED evidence-6EV9zr (two layout failures), scoped summary wrapping/dashboard grid fixed in parity.css, final30/30 and desktop/mobile screenshots visually checked.
- residual risks: Synthetic HTTP fixtures для отказов/timestamps/очереди; provider/human acceptance и полная accessibility qualification не заявлены.
- follow-up: Нет в пределах AC; сквозная приёмка F19/F24 остаётся отдельной.
- Documentation impact: updated; `docs/frontend/components.md` + `.en.md`; `docs/sources/registry.md` + `.en.md`; Описаны актуальные правила отображения, source owners и browser evidence.

### Task `PAOS-FUNC-08`

- Delivery group: `FUNC-G01`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-08 — Разделить общие контракты и зависимости UI/backend
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Архитектура; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 18:27
- Priority: P2
- Evidence level: implemented_locally_verified
- Execution authority: owner_authorized_local_synthetic; FUNC-G01, 15.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-09`, `PAOS-FUNC-11`, `PAOS-FUNC-13`
- Source: HTTP imports web/preferences; contracts imports local-service/task-profile. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [packages/contracts/issues/task-profile.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/packages/contracts/issues/task-profile.ts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Разделить общие контракты и зависимости UI/backend.
- Technical value: Убрать импорты backend→frontend и contracts→backend, сохранив публичное поведение.
- Product value: Изменение оформления реже ломает серверные функции и выпуск.
- Scope: `apps/local-service/src/http/application.mts`; `apps/web/src/design/preferences.ts`; `packages/contracts/issues/task-profile.ts`; `apps/local-service/src/tasks/task-profile.ts`. Ownership выполненного slice: root + назначенные агенты; shared edits сериализованы.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Изменение оформления реже ломает серверные функции и выпуск. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Preferences и task decoder имеют одного независимого владельца; contracts не импортируют apps. AC2: Существующие payload/schema и отказные сценарии сохранены; frontend и service проходят typecheck и текущие тесты. AC3: Проверка направления импортов предотвращает регрессию; runtime tuple повторно квалифицирован, если затронуты pinned sources.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сохранение текущих контрактов, регрессии и сравнение before/after. Общие docs gates применяются при изменении документации.
- Risks / approval gates: architecture_review_before_refactor; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Закрыта по локальным AC; новые изменения pinned sources требуют повторной квалификации.

#### Completion Report

- status: implemented
- what was done: Две чистые реализации перенесены в независимый contracts owner. M1 decoder сохранён побайтно кроме import; прежние пути re-export ту же функцию. DOM apply остаётся Web. AST guard проверяет import/export/type/literal dynamic edges; HTTP payload/schema не менялись.
- files touched / work locations: `packages/contracts/tasks/decode-task-profile.ts`, `packages/contracts/ui/preferences.ts`, legacy decoder/frontend preferences re-exports, `issues/task-profile.ts`, HTTP `application.mts`, `locales/messages.ts`, `tests/web/contracts-boundaries.test.mts`, final runtime manifest
- technical value delivered: Обратные импорты contracts→apps и service→Web source удалены без новых dependencies и без переписывания validation.
- product value delivered: Изменение оформления больше не требует импортировать frontend implementation в backend preferences.
- actual implementation date and time: 15-11-2026 18:27
- verification evidence: Independent pre-edit architecture review /root/func_g01_runtime; AST RED found exact contracts-to-service + service-to-Web edges; GREEN shared/decoder/M2/preferences focused15, npm run check:web-m1/build:web exit0. Final native candidate/default exit0 `.tmp/func-g01-runtime/native-candidate-final-escalated.log`, native-default-final-escalated.log; manifest adapter fc34f72a89cd1a217cc22bd0a160284f9ee8671c453d06531e86e24b69a4c8d5; runtime12/12. Full Web `.tmp/func-g01/web-final.log` 507 tests492pass/11fixture EPERM/4skip + exact15 boundary retests `.tmp/func-g01/web-boundary-retest.log`15pass0fail0skip:507 unique passed across two executor contexts. Independent final review /root/func_g01_review closed_allowed.
- residual risks: Оставлена существующая packaging/parser dependency на Web package. AST guard проверяет статические/literal edges, не произвольные вычисляемые imports; provider/human/production claims не повышены.
- follow-up: Нет в пределах AC; новая правка pinned source требует native requalification.
- Documentation impact: updated; `docs/backend/modules.md` + `.en.md`, `docs/architecture/containers.md` + `.en.md`, `docs/sources/registry.md` + `.en.md`; Описаны новые owners, compatibility seams, выбранный вариант/альтернатива и проверенная финальная квалификация. API docs no_change_needed: endpoints/payload/schema/errors сохранены.

### Task `PAOS-FUNC-09`

- Delivery group: `FUNC-G04`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-09 — Оптимизировать чтение и жизненный цикл снимков
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Архитектура; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-08`, `PAOS-FUNC-20`
- Blocks: `PAOS-FUNC-14`
- Source: Полные projectEntities; graph memory cap8; catalog snapshot limits. [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/local-service/src/task-manager/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/task-manager/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Оптимизировать чтение и жизненный цикл снимков.
- Technical value: По измерениям устранить лишние полные сканы и добавить ограниченное освобождение cache.
- Product value: Длительная работа и большие проекты не упираются в задержки и накопленные snapshots.
- Scope: `apps/local-service/src/task-manager/service.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/sessions/service.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Длительная работа и большие проекты не упираются в задержки и накопленные snapshots. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Выбраны и реализованы только bottlenecks, воспроизведённые F20; before/after на одном workload. AC2: Девятый проект не требует restart лишь из-за8 graph snapshots: eviction/rebuild сохраняет revision/cursor safety. AC3: Нагрузка на task/artifact/history чтение ограничена; превышение бюджета даёт объяснимый partial/error и безопасное восстановление. AC4: После F20 сравнить metadata listing, graph status и scanner на том же workload: повторный запрос статуса не должен безусловно перечитывать все содержимое файлов; bytes/read и scan count измерены. AC5: Cache key/eviction учитывают root identity, policy version и scan revision F27/F28; eviction не скрывает файлы из дерева F26 и не смешивает разные проекты.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Сохранение текущих контрактов, регрессии и сравнение before/after. Общие docs gates применяются при изменении документации.
- Risks / approval gates: measured_bottleneck_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 12–24 ч после benchmark; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.

#### Completion Report

- status: implemented
- what was done: По воспроизведённым F20 bottlenecks внедрены metadata-only graph status,8-entry LRU/generation-bound cursors,8 checked parallel source handles с прежним8MiB cap, SQL kind filtering до64MiB cap, frozen TEMP history и SQL preview artifacts с bounded raw reads.
- files touched / work locations: apps/local-service/src/code-index/service.mts; apps/local-service/src/storage/; apps/local-service/src/sessions/service.mts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/task-manager/service.mts; apps/local-service/src/main.mts; tests/web/snapshot-lifecycle.test.mts; tests/web/snapshot-history-scale.test.mts
- technical value delivered: Устранены startup SNAPSHOT_TOO_LARGE, повторные code body reads при status и ninth-project refusal; raw SHA256/authority guards и immutable history сохранены.
- product value delivered: Крупная история и документы не мешают чтению задач; eviction не требует restart и не скрывает Files.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; observable RED3/3→GREEN3/3 plus real100k-message frozen/1000-large-document regressions; full658 includes current guards; Baseline graph 60.865 s/status 17.6–21.3 s/ninth LIMIT; current closure graph 11475.70 ms/status 313.49/294.86/277.69 ms, 0 content reads/bytes and one metadata walk; ninth project succeeds; final cold-generation deviations and fast existing cursors retained in F20 receipts; no threshold raised
- residual risks: Новый большой cold snapshot не имеет warm-SLO1s; partial/recovery и caps230MiB payload/256MiB TEMP сохранены. History cursor expiry15min/eviction/restart требует refresh. Статус проверяет metadata; отдельный excerpt сверяет raw hash. Native RSS не ограничен JS heap.
- follow-up: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.
- Documentation impact: updated; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/backend/lifecycle.md; docs/backend/lifecycle.en.md; docs/db/transactions.md; docs/db/transactions.en.md; docs/testing/test-map.md; docs/testing/test-map.en.md; scoped source checks passed.

### Task `PAOS-FUNC-10`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-10 — Показывать ограничения файлового scope до запуска
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-15`, `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: Capture ограничен32 файлами,64KiB/файл,512KiB суммарно. [apps/local-service/src/runtime/app-agent-files.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/runtime/app-agent-files.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Показывать ограничения файлового scope до запуска.
- Technical value: Общий preflight для числа файлов, размеров, excluded paths и границ actual diff.
- Product value: Пользователь заранее понимает, почему задача не стартует и как её разделить.
- Scope: `apps/local-service/src/runtime/app-agent-files.mts`; `apps/local-service/src/runtime/app-agent-gateway.mts`; `apps/web/src/ui/SessionContext.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл). Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь заранее понимает, почему задача не стартует и как её разделить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: 32/33 файла,64KiB/64KiB+1 и суммарные512KiB проверяются до dispatch с конкретным объяснением. AC2: Sensitive/link/binary exclusions не раскрывают содержимое; blocked execution не выдаётся за стартовавший run. AC3: Если расширение лимитов необходимо, оно проходит отдельный bounded performance/security gate; лимиты не снимаются безусловно. AC4: Выбор file reference из дерева F26 проходит execution preflight повторно: видимость/читаемость/индексация файла не означают разрешение на dispatch. Policy F28 и реальные execution limits отображаются раздельно; stale path/root требует обновления.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: shared_preflight_contract_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Next step: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.

#### Completion Report

- status: implemented
- what was done: Единый metadata-only preflight проверяет saved scope и исходные32/64KiB/512KiB limits, operations/rename/pins/policy/root до Send; server повторяет authority checks, native boundary rechecks policy после waits. Blocked UI сохраняет draft и не dispatch-ит run.
- files touched / work locations: apps/local-service/src/runtime/app-agent-files.mts; apps/local-service/src/runtime/task-file-preflight.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/runtime/live-gateway.mts; apps/web/src/ui/SessionContext.tsx; apps/web/src/ui/App.tsx; tests/web/file-preflight.test.mts
- technical value delivered: Shared root/policy/revision contracts и final authority fences подтверждены на текущих API/SQLite/FS/build/native fixtures.
- product value delivered: Неполнота и устаревшие данные видимы; файловые ограничения объясняются до dispatch, данные и черновики сохраняются.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.
- Documentation impact: updated; docs/security/filesystem.md; docs/security/filesystem.en.md; docs/db/transactions.md; docs/db/transactions.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-11`

- Delivery group: `FUNC-G05`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-11 — Ввести измеряемую статистику runs и расхода
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-08`
- Blocks: `PAOS-FUNC-15`
- Source: Metrics durationSeconds/tokenCount/cost=null; tool_use не измеряется. [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Ввести измеряемую статистику runs и расхода.
- Technical value: Versioned telemetry с provenance, дедупликацией и агрегацией session→run→task→agent.
- Product value: Длительность и расход помогают сравнивать результат работы без выдуманных чисел.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/events/task-time.ts`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Длительность и расход помогают сравнивать результат работы без выдуманных чисел. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Сначала утверждены доступные источники duration/tokens/tool calls/cost, privacy и retention; unsupported поля остаются unknown. AC2: Повтор события не увеличивает totals; partial streams, restart и связь нескольких агентов не приводят к double count. AC3: Dashboard, задача и агент показывают согласованные значения, период и source; стоимость появляется только при известной модели расчёта.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/task-time.test.mts tests/web/ui-v3-dashboard.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: telemetry_source_privacy_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч discovery/design; build после выбора источников; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: telemetry_source_privacy_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

#### Completion report

- status: implemented
- what was done: Versioned numeric telemetry измеряет run intervals и mediated commands, исключает approval wait, дедуплицирует retries и сохраняет unknown при recovery. Один scoped endpoint и RunUsage показывают согласованные значения в Dashboard/проекте/задаче/сессии/агенте; tokens/cost/host tools остаются unknown.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/llm/budgets-and-observability.md; docs/api/endpoints.md; docs/frontend/components.md; docs/security/data-retention.md; registry and scoped source checks.

### Task `PAOS-FUNC-12`

- Delivery group: `FUNC-G05`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-12 — Спроектировать и подключить внешний поиск skills
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: нет
- Blocks: нет
- Source: remote_discovery_adapter_not_configured. [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Спроектировать и подключить внешний поиск skills.
- Technical value: Отдельный read-only discovery adapter с provenance, лицензией, pin и preview.
- Product value: Нужный skill можно найти вне локального каталога и осознанно добавить.
- Scope: `apps/local-service/src/team/service.mts`; `apps/local-service/src/team/sources.mts`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Нужный skill можно найти вне локального каталога и осознанно добавить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build выбран разрешённый источник, network/privacy policy и формат результата. AC2: Поиск показывает origin/license/revision; timeout/offline не ломают локальный каталог. AC3: Поиск ничего не устанавливает; добавление проходит существующий preview/apply и проверяет drift и зависимости.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-review-repair.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: external_source_design_and_authority_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 4–8 ч design; build после выбора адаптера; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: external_source_design_and_authority_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

#### Completion report

- status: implemented
- what was done: Явный anonymous fixed-source reader openai/plugins superpowers по pinned commit проверяет Git/raw hashes, фактическую MIT license, path/mode/dependency/byte/deadline limits. Query остаётся локально; preview→Apply создаёт managed copy с resources/provenance/license, без native activation. Локальный каталог сохраняется при внешнем отказе.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/security/supply-chain.md; docs/api/endpoints.md; docs/frontend/components.md; docs/product/capabilities.md; registry and scoped source checks.

### Task `PAOS-FUNC-13`

- Delivery group: `FUNC-G05`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-13 — Добавить безопасное применение document proposals
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-08`
- Blocks: нет
- Source: Текущая политика staged_only, applied:false. [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Добавить безопасное применение document proposals.
- Technical value: Preview-bound compare-and-swap writer с сохранением пользовательских правок и recovery.
- Product value: Согласованное предложение можно довести до изменения документа внутри приложения.
- Scope: `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/http/application.mts`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Согласованное предложение можно довести до изменения документа внутри приложения. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build утверждены writer authority, source-vs-SQL ownership и eligible documents. AC2: Apply меняет только проверенный файл при совпавшей revision; внешний edit вызывает conflict без overwrite. AC3: Повтор apply идемпотентен; crash/rollback и sensitive paths проверены; staged/applied/accepted показываются отдельно.
- Verification gates: `node --test tests/web/skill-generation-artifacts.test.mts`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: document_write_authority_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после утверждения write contract; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: document_write_authority_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

#### Completion report

- status: implemented
- what was done: Preview/ack/CAS Apply, exact-current-preview rollback и явное recovery реализованы для SQL и существующих разрешённых Windows files. Protected durable journal, immutable outcome receipts, exclusive native handle/root pins, raw hash/file revision и bounded retention сохраняют bytes и unknown outcomes. Исправлен текущий rollback operation ID; запись не создаёт acceptance.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/db/transactions.md; docs/backend/recovery.md; docs/security/filesystem.md; docs/security/data-retention.md; docs/ai/llm/prompts-and-outputs.md; docs/frontend/components.md; docs/api/endpoints.md; registry and scoped source checks.

### Task `PAOS-FUNC-14`

- Delivery group: `FUNC-G04`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-14 — Расширить полезность и устойчивость карты проекта
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-02`, `PAOS-FUNC-09`, `PAOS-FUNC-27`, `PAOS-FUNC-28`, `PAOS-FUNC-30`, `PAOS-FUNC-31`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`, `PAOS-FUNC-34`
- Source: lexical_subset_only, imports unresolved, memory-only index. [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Расширить полезность и устойчивость карты проекта.
- Technical value: Выбрать поддержку языков/связей; durable revision index, imports resolution и честный coverage.
- Product value: Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа.
- Scope: `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/code-index/lexical.mts`; `apps/local-service/src/impact/service.mts`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Карта помогает оценить влияние изменения, а не создаёт видимость полного анализа. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build утверждена матрица поддерживаемых языков и типов связей; unsupported semantics остаются явно отмеченными. AC2: Для выбранного scope cross-file imports/aliases проверяются на эталонных fixtures; unresolved не становится ложным ребром. AC3: Restart/rebuild сохраняет либо явно инвалидирует revision; D3/Mermaid/list и impact показывают один набор данных. AC4: Graph consumer использует inventory F28 и этап code в F27; discovered/readable/indexed/unsupported/excluded/error различаются. Нулевой или успешный JS/TS индекс не означает полного анализа проекта. AC5: Ready/stale/unavailable графа не блокирует дерево F26; restart/cancel/retry не публикуют устаревший результат, недоступный parser оставляет другие результаты сканирования доступными. AC6: По F30/F31 зафиксирован выбор backend/композиции и rollback; обоснованный отказ PoC не становится скрытым fallback. Неподдерживаемые языки и семантика показываются явно; raw SQLite стороннего движка не становится API PAOS. AC7: В существующей «Карте» реализованы режимы зависимостей/символов в пределах выбранных capabilities, поиск, incoming/outgoing, путь/impact и evidence drawer с file/line переходами. Graph/list/Mermaid, фильтры и counters используют один snapshot; loading/empty/partial/error/unavailable/stale и version/coverage видимы. AC8: Общий UI/UX-контракт F30–F34 применён к production экрану, не только PoC; переходы Files↔Map и выбор проекта проверены. Раздел «Архитектура» включается только для source-backed модели: импорт не равен вызову, C4 grouping не считается извлечённым бизнес-фактом.
- Verification gates: `npm run test:web-m1`; `node --test tests/web/ui-v3-diagram.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: language_semantics_storage_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после выбора языков; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + graph-cockpit-engineer + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.

#### Completion Report

- status: implemented
- what was done: Выбрана явная installed parser+pure allowlist resolver композиция; добавлены aliases/baseUrl, literal dynamic import/unshadowed require, dependencies/symbols, direction/bounded path, source evidence→Files, общий revision дляgraph/list/Mermaid. Native parser изолирован owned child с watchdog.
- files touched / work locations: apps/local-service/src/code-index/; apps/local-service/src/process/child-watchdog.mts; packages/contracts/graph/code-graph.ts; apps/web/src/features/graph/; apps/web/src/ui/App.tsx; tests/web/graph-imports.test.mts; tests/web/graph-query-modes.test.mts; tests/web/graph-parser-isolation.test.mts
- technical value delivered: Ground truth imports10/10 без fake cross-file calls; unsupported/dynamic/unresolved и parser failure сохраняются явно, Files независим.
- product value delivered: Карта помогает найти зависимости и исходный файл/строку с проверяемым evidence и доступным списком.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; G02 corpus7/10→10/10 imports,fixture precision1/recall1; aliases/config drift/shadowing/cycles/Unicode/no config execution; native deep input failure contained; graph owner remains usable; actual child timeout/cancel cleanup; actual browser dependencies/direction/path/keyboard/source/Files and fresh nonempty Map in4locale/theme×2viewport states
- residual risks: Только JS/TS lexical/import subset; без package exports/config inheritance/full TS linker/runtime calls/C4 business facts. Restart/eviction явно требует rebuild.1k files/8MiB/512KiB и bounded path8hops/1000visited сохранены.
- follow-up: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.
- Documentation impact: updated; docs/code-intelligence/graph-model.md; docs/code-intelligence/graph-model.en.md; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/backend/modules.md; docs/backend/modules.en.md; scoped source checks passed.

### Task `PAOS-FUNC-15`

- Delivery group: `FUNC-G05`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-15 — Уточнить и расширить границы автономности
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-10`, `PAOS-FUNC-11`
- Blocks: нет
- Source: Scope executable только '.', hostToolsConstrained=false, tokenCostMetering unavailable. [apps/local-service/src/autonomy-policy/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/autonomy-policy/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Уточнить и расширить границы автономности.
- Technical value: Capability-based file/operation/cost policy без обещаний ограничения всего App host.
- Product value: Пользователь понимает и контролирует допустимую самостоятельность агента.
- Scope: `apps/local-service/src/autonomy-policy/service.mts`; `packages/contracts/autonomy/policy.ts`; `apps/local-service/src/runtime/sandbox-broker.mts`; `apps/web/src/features/autonomy/AutonomyManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Пользователь понимает и контролирует допустимую самостоятельность агента. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build документированы enforceable границы и невозможные обещания; narrow-path execution без enforcement отклоняется. AC2: В разрешённом маршруте выход за scope/лимит останавливает новые dispatch; unknown outcome остаётся fenced. AC3: Денежный лимит допускается только при достаточном metering/reservation изF11; иначе UI явно сообщает недоступность.
- Verification gates: `node --test tests/web/autonomy-policy.test.mts tests/web/autonomy-runtime.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: enforcement_capability_and_owner_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после подтверждения enforcement; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + security-privacy-supply-chain-reviewer + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: enforcement_capability_and_owner_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

#### Completion report

- status: implemented
- what was done: Optional maxCommandsTotal расширяет совместимый v1 policy-wide command reservation budget. Durable counting не удваивает retry, не возвращает unknown reservations, останавливает новые dispatch/runs/resume после cap и допускает завершение последней команды. UI различает reservation/observed count; narrow paths и денежные/host-tool обещания отклоняются.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/llm/budgets-and-observability.md; docs/api/endpoints.md; docs/frontend/components.md; registry and scoped source checks.

### Task `PAOS-FUNC-16`

- Delivery group: `FUNC-G05`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-16 — Подтверждать доступную историю и реально загруженные профили
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 07:29
- Priority: P2
- Evidence level: locally_verified_with_explicit_limits
- Execution authority: owner_authorized_func_g05_local_synthetic; 16.11.2026.
- Depends on: `PAOS-FUNC-01`
- Blocks: нет
- Source: host_history_not_exposed; loadedVersion/observedModel/observedEffort unknown. [apps/local-service/src/sessions/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/sessions/service.mts), [apps/local-service/src/team/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/team/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Подтверждать доступную историю и реально загруженные профили.
- Technical value: Развести configured/pinned/observed model, effort и asset version; capability-based history adapter.
- Product value: Пользователь знает, какой агент фактически работал и какая часть истории доступна.
- Scope: `apps/local-service/src/sessions/service.mts`; `apps/local-service/src/team/service.mts`; `packages/contracts/team/assets.ts`; `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/team/TeamManager.tsx`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Пользователь знает, какой агент фактически работал и какая часть истории доступна. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build проверен поддерживаемый host contract; недоступная история не извлекается обходом приватных хранилищ. AC2: UI различает configured/pinned/observed; loadedVersion появляется только из подтверждённого события. AC3: Reconnect/profile switch не смешивают историю и identity; partial coverage и отсутствие attestation объясняются.
- Verification gates: `node --test tests/web/sessions-team.test.mts tests/web/team-run-navigation.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: supported_host_capability_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 6–12 ч capability review; build после подтверждения API; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: architect + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: supported_host_capability_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

#### Completion report

- status: implemented
- what was done: Официальный host contract проверен; paos_history_capability_v1 связывает adapter/project/generation, разделяет local available и host not_connected. Profile executionEvidence показывает текущий configured и immutable run-pinned model/effort/version/hash; observed/loaded остаются unavailable без attestation. Foreign profile cursors, project switch/late responses/restart проверены без private host scraping.
- verification evidence: .tmp/func-g05/web-native-final.log:686/686,0fail/skip; .tmp/func-g05/browser-acceptance/evidence-OPJn2D/result.json:16/16; .tmp/func-g05/typecheck-final.log:passed; .tmp/func-g05/build-responsive-final.log:passed; .tmp/func-g05/native-candidate.json:passed; .tmp/func-g05/native-default.json:passed
- actual implementation date and time: 16-11-2026 07:29
- residual risks: Bounded local synthetic acceptance; Windows document writer; external ignore revocation is final-checked, not atomic; unknown partial writes require explicit/manual recovery; active journal limits do not purge historical backups. Complete host history/usage, loaded-profile attestation, monetary/host-tool enforcement, provider/human/release acceptance are unavailable or separate.
- Documentation impact: updated; docs/ai/agents/context.md; docs/ai/agents/sessions.md; docs/api/endpoints.md; docs/frontend/components.md; registry and scoped source checks.

### Task `PAOS-FUNC-17`

- Delivery group: `FUNC-G06`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-17 — Подготовить удобную установку, обновление и rollback
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Расширение; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: bounded_capability_or_missing_extension
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-22`
- Blocks: нет
- Source: Portable CLI есть; signed installer/auto-update не заявлены. [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Подготовить удобную установку, обновление и rollback.
- Technical value: Поверх переносимого package задать version/digest/signing, compatibility и recovery UX.
- Product value: Обновление не требует ручного подбора каталогов и не ставит данные под угрозу.
- Scope: `apps/desktop-local/distribution.mts`; `apps/desktop-local/main.mts`; `apps/desktop-local/README.md`; `apps/launcher/launcher.ts`; `tests/web/desktop-local.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Выбор дизайна без реализации и проверок не закрывает эту задачу.
- Expected result: Обновление не требует ручного подбора каталогов и не ставит данные под угрозу. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До build выбраны канал доставки, формат installer, signing и AUTH/licensing gates; публикация отдельно. AC2: Synthetic install/update/rollback сохраняют профиль; incompatible schema/tuple блокируют запуск с понятным восстановлением. AC3: Не удаляются пользовательские профили и старые версии без отдельного решения; новый чистый Windows-профиль проходит согласованный сценарий.
- Verification gates: `node --test tests/web/desktop-local.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: distribution_signing_commercial_design_required; сначала bounded discovery/design, затем конкретный build scope и оценка; неизвестная host capability не считается обещанной. Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: high — несколько контрактов и design gate
- Estimated execution time: 8–16 ч design; build после выбора канала; rough_range_not_commitment. Это оценка discovery/design, общая build-оценка пока неизвестна.
- Agents: release-operator + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить и согласовать design gate; до этого build не начинать.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: distribution_signing_commercial_design_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-18`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-18 — Согласовать обновление снимков задач и dashboard
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-07`, `PAOS-FUNC-26`, `PAOS-FUNC-27`
- Blocks: `PAOS-FUNC-19`
- Source: Task/dashboard преимущественно initial/manual snapshots, queue polling отдельно. [apps/web/src/features/tasks/TaskManager.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/tasks/TaskManager.tsx), [apps/web/src/features/dashboard/Dashboard.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/dashboard/Dashboard.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Согласовать обновление снимков задач и dashboard.
- Technical value: Определить refresh/invalidation contract при фоне, мутациях и смене проекта.
- Product value: После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/api/latest-request.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/local-service/src/project-scans/service.mts` (новый планируемый файл). Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: После выполнения пользователь видит актуальный статус без угадывания, какой экран обновить. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Изменение задачи/очереди в другом разрешённом канале либо обновляет экран, либо явно делает snapshot устаревшим. AC2: Поздний ответ предыдущего проекта не заменяет текущие данные; dirty editor не перезаписывается refresh. AC3: Polling/subscription останавливаются при unmount и не создают неограниченную нагрузку. AC4: Create/modify/rename/delete и изменение policy/root инвалидируют затронутые directory/document/graph/analysis snapshots; выбран watcher либо bounded rescan/refresh с явной свежестью, без обещания невыбранного live watcher. AC5: Scan events имеют scanId/revision; позднее событие отменённого задания или другого проекта не меняет UI. После возврата/restart отображается сохранённый scan status без перезаписи черновиков. AC6: Общий freshness contract распространяется на code/schema snapshots и code-table links: совместимые revisions, late-response rejection, явный stale и остановка polling при уходе. Реализацию и проверку новых consumers выполняют F14/F33/F34; F18 не ждёт их и не блокирует ранний Files путь.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: freshness_contract_before_build; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.

#### Completion Report

- status: implemented
- what was done: Atomic task snapshot/profile stamp, bounded single-flight polling, явный stale/refresh в Dashboard/Task Manager/overlay и dirty CAS conflict внедрены; explicit file refresh и общий provenance invalidation не обещают live watcher. Scan attempt/request scopes отвергают late events.
- files touched / work locations: packages/contracts/project-freshness.ts; apps/local-service/src/storage/sqlite-worker.mts; apps/web/src/api/project-freshness.ts; apps/web/src/ui/ProjectFreshness.tsx; apps/web/src/features/tasks/Editor.tsx; apps/web/src/features/dashboard/Dashboard.tsx; tests/web/project-freshness.test.mts; tests/web/project-freshness-poll.test.mts
- technical value delivered: Shared root/policy/revision contracts и final authority fences подтверждены на текущих API/SQLite/FS/build/native fixtures.
- product value delivered: Неполнота и устаревшие данные видимы; файловые ограничения объясняются до dispatch, данные и черновики сохраняются.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.
- Documentation impact: updated; docs/frontend/state-management.md; docs/frontend/state-management.en.md; docs/api/events.md; docs/api/events.en.md; docs/backend/recovery.md; docs/backend/recovery.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-19`

- Delivery group: `FUNC-G07`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-19 — Проверить сквозной функционал на текущей сборке
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-02`, `PAOS-FUNC-03`, `PAOS-FUNC-04`, `PAOS-FUNC-05`, `PAOS-FUNC-06`, `PAOS-FUNC-07`, `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-24`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-14`, `PAOS-FUNC-33`, `PAOS-FUNC-34`
- Blocks: `PAOS-FUNC-23`
- Source: Redesign receipts visual/synthetic не доказывают новый native full path. [design/2026-11-13-v3/implementation-evidence.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/design/2026-11-13-v3/implementation-evidence.md), [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/TEST.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Проверить сквозной функционал на текущей сборке.
- Technical value: Связать real UI/API/storage/native receipts с одним revision без подмены execution mock-данными.
- Product value: Пользователь проходит весь рабочий путь и получает проверяемый результат.
- Scope: `tests/web/single-window/m4-integration-acceptance.mts`; `tests/web/single-window/m2-task-manager-browser-acceptance.mts`; `tests/web/single-window/m2b-browser-acceptance.mts`; `tests/web/single-window/m2c-browser-acceptance.mts`; `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл); `tests/web/project-files.test.mts` (новый планируемый файл); `tests/web/project-scans.test.mts` (новый планируемый файл); `tests/web/project-analysis.test.mts` (новый планируемый файл). Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь проходит весь рабочий путь и получает проверяемый результат. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Synthetic путь task→assignment→run→approval→command→diff/checks→owner acceptance проходит на текущем build. AC2: Формы, custom workflow, RU/EN, обе темы, keyboard, links и partial/error состояния проверены послеF02–F07/F10/F18. AC3: Actual App/model roundtrip и генерация agent/skill проверяются только при отдельном разрешении; без него фиксируется live gap, synthetic pass его не закрывает. AC4: На synthetic fixture пройден путь Add → немедленно доступное дерево → этапы сканирования → preview допустимого файла → file reference задачи; карта и discovery не подменяют полноту файлового дерева. AC5: Проверены empty/no-Control-plane/Python-only/mixed проекты, Unicode/пробелы, unreadable/oversized/binary/invalid-encoding, ignore/sensitive/link/traversal, rename/delete/root drift во время scan, cancel/restart/retry и два проекта. Ошибка отдельного файла сохраняет разрешённую часть, root violation блокируется; до/после target hashes совпадают. AC6: RU/EN, две темы, keyboard/focus, pagination, явная неполнота поиска и отсутствие false-ready проверены; fixtures не используют реальные профили/credentials и не запускают target scripts. AC7: После F14/F33/F34 пройден расширенный путь Files → Map → DB schema → code usages → source line → task reference; сохранены selection/back/filter/project isolation. Проверены confirmed/inferred/unresolved и различие runtime schema/ORM/migrations, экспорт Mermaid и bounded больших графов. AC8: Новые вкладки/разделы имеют RU/EN, обе темы, keyboard/focus, доступный list/table fallback и все UI states; backend failure/cancel/restart не маскируются mock UI. Отдельные ранние receipts Files/scan допускаются до graph/DB, но окончательное закрытие F19 требует расширенного сценария.
- Verification gates: `npm run test:web-m1`; `npm run check:web-m1`; `npm run build:web` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: separate_synthetic_and_actual_runtime_receipts; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч без ожидания live approval; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: separate_synthetic_and_actual_runtime_receipts; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-20`

- Delivery group: `FUNC-G04`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-20 — Измерить масштабирование и длительную работу
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-01`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`
- Blocks: `PAOS-FUNC-09`
- Source: Большие проекты/long-running после redesign не измерены; runtime index/cache caps. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Измерить масштабирование и длительную работу.
- Technical value: Воспроизводимый workload с hardware/cache profile, latency/RSS/queue-depth и error budgets.
- Product value: Большой проект и длительная сессия остаются управляемыми.
- Scope: `tests/web/storage.test.mts`; `tests/web/code-index.test.mts`; `tests/web/ui-stream-search.test.mts`; `tests/web/single-window/functional-scale-acceptance.mts` (новый планируемый файл); `research/product-agent-os-web-prd-2026-11-05.md`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/project-inventory/service.mts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/project-analysis/service.mts` (новый планируемый файл). Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Большой проект и длительная сессия остаются управляемыми. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Зафиксированы hardware/cache и объёмы:10k задач,100k сообщений,1k файлов; границы1001 файлов и9 проектов проверены отдельно. AC2: Измерены cold startup, search/list/event-visible latency, RSS и снимки в повторяемом длительном прогоне; нет скрытой потери данных. AC3: Результаты сравнены с WEB-NFR и согласованными порогами; deviations заведены вF09, неподдерживаемые объёмы явно ограничены. AC4: До замеров фиксируются budgets и dataset: большой monorepo, широкая/глубокая директория, пустые папки, generated/vendor/ignored, binary/large, mixed languages. Измеряются registration-to-tree, раскрытие/поиск, scan phases, cancellation latency, restart recovery, RSS, количество обходов и прочитанных bytes. AC5: Границы старых лимитов 1000/1001 файлов, 10000/10001 записей, depth32/33, 512KiB и 8MiB проверяются как корректный partial/bounded outcome, а не требование снять guards. Metadata listing не обязано читать содержимое всего проекта. AC6: Baseline допускается до F26–F29; окончательное закрытие F20 требует их версии и сравнения с baseline. F09 использует этот протокол для before/after; benchmark не меняет user workspace. AC7: Один воспроизводимый benchmark protocol задаёт ground truth и budgets для F30/F31/F32: cold/incremental scan, RSS/disk, latency и precision/recall. Для F14/F33/F34 добавлены UI responsiveness, schema size, edge limits и стоимость bounded agent context; они повторяют протокол в собственных AC. F20 не зависит от завершения PoC/DB/графа, чтобы не создать цикл F20→F09→F14.
- Verification gates: `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: benchmark_protocol_and_thresholds_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + architect; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.

#### Completion Report

- status: implemented
- what was done: Зафиксирован до замеров protocol/hardware/cache/ground truth; baseline failure сохранён; after/final повторены на10k задач/100k сообщений/1000 документов и1000 code files с120ssoak и точными boundaries. Итог measured_with_deviations/bounded_outcomes, не all-NFR pass.
- files touched / work locations: tests/fixtures/func_g04/protocol.json; tests/web/single-window/functional-scale-acceptance.mts; tests/web/single-window/graph-database-browser-acceptance.mts
- technical value delivered: Воспроизводимые source-bound measurements, SQL integrity, bytes/walks/RSS и actual application scan/recovery вместо предположений.
- product value delivered: Понятны реальные поддержанные сценарии, время ожидания и ограничения масштаба без скрытой потери данных.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; Current closure diagnostic/reference/filesystem: .tmp/func-g04/scale-closure/result-diagnostic-1794778219987.json; .tmp/func-g04/scale-closure/result-reference-1794778236139.json; .tmp/func-g04/scale-closure/result-filesystem-1794778628384.json; 133 current source hashes; SQL 10k/100k/1k integrity/FK0; soak 120.15 s / 119 iterations; preserved targets + cleanup; unchanged protocol 37c20aadc0d3474ef78cf86928e9ee1727be7bf415152fc393e92c8b079af625
- residual risks: Холодные history/catalog generations превышают comparison 1000 ms в сохранённых runs; подробные значения и все отклонения — в F20 receipts. 10k/10001 directories дают bounded 30 s INVENTORY_TIMEOUT. Reference 4-core/GUI cold launch/whole-system RSS не квалифицированы. Browser sampled aggregate 1101.32 MiB — diagnostic, не per-process peak. Human/provider/release отдельно.
- follow-up: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.
- Documentation impact: updated; docs/testing/test-map.md; docs/testing/test-map.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-21`

- Delivery group: `FUNC-G06`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-21 — Перепроверить очередь, Stop и crash recovery
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-23`
- Source: Recovery/ownership implemented; необходим current-run regression. [apps/local-service/src/recovery/recipe-checkpoint.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/recovery/recipe-checkpoint.mts), [apps/local-service/src/scheduler/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/scheduler/service.mts). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Перепроверить очередь, Stop и crash recovery.
- Technical value: Проверить identity/CAS/lease/ownership fences и отсутствие replay в отказах.
- Product value: Потеря соединения не запускает задачу дважды и не теряет результат.
- Scope: `tests/web/recipe-recovery.test.mts`; `tests/web/recipe-crash.test.mts`; `tests/web/scheduler-runtime.test.mts`; `tests/web/parallel-workspaces.test.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Потеря соединения не запускает задачу дважды и не теряет результат. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Crash до dispatch, после dispatch до receipt и после terminal receipt покрыты отдельными сценариями. AC2: Stop без ACK не освобождает ownership; lost consumer/timeout требуют корректной сверки. AC3: В разных roots разрешённая параллельность сохраняется, overlapping roots блокируются; selective Stop не отменяет чужой run.
- Verification gates: `node --test tests/web/recipe-recovery.test.mts tests/web/recipe-crash.test.mts tests/web/scheduler-runtime.test.mts tests/web/parallel-workspaces.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: disposable_profiles_only; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: disposable_profiles_only; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-22`

- Delivery group: `FUNC-G06`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-22 — Перепроверить импорт, backup и restore
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P1
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-01`
- Blocks: `PAOS-FUNC-17`, `PAOS-FUNC-23`
- Source: Import/backup контракты есть; current combined verification отсутствует. [apps/local-service/src/import-export/migration.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/import-export/migration.mts), [apps/desktop-local/README.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/desktop-local/README.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Перепроверить импорт, backup и restore.
- Technical value: Проверить source authority, freeze/CAS, counts/hashes/FK, blobs и идемпотентность.
- Product value: Задачи, история и вложения сохраняются при переносе и восстановлении.
- Scope: `tests/web/domain-migration.test.mts`; `tests/web/storage-backup.test.mts`; `apps/local-service/src/import-export/migration.mts`. Ownership назначается при старте; перечисленные роли — предложение, agents сейчас не запущены.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Задачи, история и вложения сохраняются при переносе и восстановлении. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Source drift и неизвестный writer останавливают cutover; две writable authority не появляются. AC2: Corrupt/missing blob, прерванный import и повтор запроса дают безопасный результат без дублей. AC3: Restore в новый synthetic profile сохраняет данные и ссылки; старый профиль неизменён; credentials/pending operations не воспроизводятся.
- Verification gates: `node --test tests/web/domain-migration.test.mts tests/web/storage-backup.test.mts` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: synthetic_data_no_real_profile_mutation; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: tester + reviewer; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: synthetic_data_no_real_profile_mutation; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-23`

- Delivery group: `FUNC-G07`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-23 — Провести продуктовую приёмку ключевых сценариев
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Проверка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: verification_gap
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-19`, `PAOS-FUNC-21`, `PAOS-FUNC-22`, `PAOS-FUNC-24`
- Blocks: нет
- Source: PRD pilot metrics и UI-12 acceptance остаются отдельными gates. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [docs/planning/2026-11-13-v3-ui-implementation-plan.md](2026-11-13-v3-ui-implementation-plan.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Провести продуктовую приёмку ключевых сценариев.
- Technical value: Связать acceptance с наблюдаемой корректностью решений, а не числом кликов.
- Product value: Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь без подсказки понимает статус, blocker, evidence и следующий шаг. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: До пилота согласованы участники, сценарии, opt-in/retention и baseline MD/chat; production data не обязательны. AC2: Пройдены первое открытие, возвращение, конфликт, partial evidence и приёмка; ошибки понимания фиксируются вместе с успехами. AC3: Цели4/5 за3мин и3/5 повторное использование за14дней изPRD проверяются как гипотезы; ноль ложных трактовок verified и потерь данных; owner принимает результат отдельно. AC4: В пилот добавлены выбор папки, поиск обычного файла вне Control-plane, объяснение excluded/unsupported/partial, отмена/повтор и возвращение после restart. Наблюдатель проверяет, что участник не путает видимость файла, успешную индексацию и разрешение на исполнение. AC5: В human pilot включены поиск места изменения через Map и DB usages, чтение ERD/table, переход к source, понимание stale/partial/inferred и обнаружение неподдерживаемой семантики. Сравниваются успешность и время с согласованным baseline, UI convenience не выводится из технических тестов.
- Verification gates: Наблюдаемый пилот по согласованному протоколу; автоматического эквивалента human acceptance нет. Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: human_pilot_protocol_and_consent_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 6–12 ч подготовки/анализа плюс14дней наблюдения, не срок разработки; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: product-manager + tester; human acceptance — владелец; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Проверить зависимости и актуальность находки. Подготовить воспроизводимый сценарий и записать исходное состояние.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: human_pilot_protocol_and_consent_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-24`

- Delivery group: `FUNC-G07`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-24 — Объяснять доступность функций в момент действия
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Доработка; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: `PAOS-FUNC-05`, `PAOS-FUNC-10`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-14`, `PAOS-FUNC-33`, `PAOS-FUNC-34`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-23`
- Source: Ряд экранов уже отображает unknown/staged; нужна единая journey-проверка. [apps/web/src/ui/ConnectionControls.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/ConnectionControls.tsx), [apps/web/src/features/artifacts/ArtifactExplorer.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/artifacts/ArtifactExplorer.tsx). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Объяснять доступность функций в момент действия.
- Technical value: Единый capability vocabulary для staged/unsupported/partial/connected/qualified/accepted.
- Product value: Пользователь отличает доступную функцию от экрана с будущей возможностью.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/ui/ConnectionControls.tsx`; `apps/web/src/locales/app.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (новый планируемый файл); `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: Пользователь отличает доступную функцию от экрана с будущей возможностью. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Для usage, graph, proposals, skills discovery, history, autonomy и runtime рядом с действием показаны реальный scope и причина недоступности. AC2: Есть конкретный следующий шаг; unsupported не выглядит как loading, connected не называется execution-qualified. AC3: RU/EN и accessibility состояния проверены; нет повторного запроса уже действующей bounded authority. AC4: В onboarding и проекте показаны независимые registration/tree/inventory/documents/code/analysis состояния F26–F29, время и scope наблюдения; counts.files не называется indexed без соответствующего покрытия. AC5: Empty/no-supported-code не получает ложный «проект полностью проанализирован»; excluded/error/unsupported объясняют причину и действие. Недоступный parser/core adapter не скрывает доступное дерево, контрольный список Control-plane явно назван отдельным фильтром. AC6: В project navigation и onboarding явно различаются Files, Map, DB schema и code usages; Settings владеет регистрацией/источником, не дублирует самостоятельные explorers. F14/F33/F34 несут production UI; до их завершения доступны ранние capability states, полное закрытие F24 требует всех consumers. AC7: UI показывает только внедрённые capabilities/языки/DB sources и объясняет отсутствие: not_configured, unsupported, unavailable, indexing, partial, stale, failed. PoC/experimental не называется production-ready; engine выбран продуктом по evidence, внутренние настройки backend не навязываются пользователю.
- Verification gates: `npm run check:web-m1`; `npm run test:web-m1` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: capability_wording_review_required; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 8–16 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: product-manager + builder + tester; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Проверить зависимости и актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: capability_wording_review_required; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.

### Task `PAOS-FUNC-25`

- Delivery group: `FUNC-G07`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-25 — Согласовать текущие продуктовые статусы и критерии
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Документация; функциональный аудит после V3 redesign и запрос владельца на матрицу задач.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Priority: P2
- Evidence level: static_observation
- Execution authority: planning_only; внесение в план не запускает реализацию.
- Depends on: нет
- Blocks: нет
- Source: Датированные addenda сосуществуют с ранними status blocks; нужен current-state entry. Текущий docs unittest: 4 failures из-за отсутствующих rendered accessibility/pilot RU/EN и search/sitemap parity. [research/product-agent-os-web-prd-2026-11-05.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/research/product-agent-os-web-prd-2026-11-05.md), [PLAN.md](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/PLAN.md). Provenance: статический аудит 15.11.2026; новые runtime результаты не заявлены.
- Short description: Согласовать текущие продуктовые статусы и критерии.
- Technical value: Один актуальный указатель PRD/architecture/plan/registry с сохранённой историей.
- Product value: План и документация ясно показывают, что работает, ограничено и ждёт проверки.
- Scope: `research/product-agent-os-web-prd-2026-11-05.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/product-agent-os-web-task-manager-plan-2026-11-09.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/web/accessibility.md`; `docs/web/accessibility.en.md`; `docs/web/pilot.md`; `docs/web/pilot.en.md`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Non-goals: изменения вне указанного поведения; публикация, реальные credentials, provider calls и изменение hook/trust. Чужие dirty изменения не входят в исправление.
- Expected result: План и документация ясно показывают, что работает, ограничено и ждёт проверки. Подтверждение — перечисленные ниже наблюдаемые сценарии, отдельно от human acceptance.
- Acceptance criteria: AC1: Текущие scope/status/acceptance не противоречат историческим implementation_not_started/API-only блокам: история явно помечена и маршрутизирована. AC2: Для F01–F34 и M5 есть единый owner/status/source; implemented не подменяет human/live acceptance. AC3: Синхронизированы только изменённые claims и RU/EN registry; validators/docs tests проходят, старые56cards сохранены. AC4: Текущая проверка docs-site больше не сообщает missing web/accessibility.html и web/pilot.html в RU/EN; search/sitemap/switcher parity подтверждён на явно выбранном build. Публикация и promotion сайта отдельно. AC5: Документы различают «Источники», файловое дерево F26, сканирование F27, inventory policy F28 и discovery F29; версии API/coverage, recovery и ограничения описаны в existing PRD/architecture, без заявления об автоматическом ремонте или полной семантике. AC6: F30–F34 содержат upstream URLs, дату research, выбранные version/commit/license и реальные PoC receipts при выполнении; README claims не выдаются за локальные измерения. PRD/architecture/UI help описывают вкладки Map/Database/usages, read-only источники, экспорт, coverage и fallback; links и RU/EN согласованы.
- Verification gates: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v`; `python tools/check_docs.py`; `git diff --check` Это будущие проверки задачи, не выполненные проверки этой планировки. Проверить позитивные, отказные и recovery-сценарии в указанном scope. Общие docs gates применяются при изменении документации.
- Risks / approval gates: source_reconciliation_not_history_deletion; Реальные профили, внешний сервис, публикация и provider/model calls требуют отдельной точной авторизации. Synthetic acceptance — только disposable roots.
- Complexity: medium — ограниченный сценарий с отрицательными проверками
- Estimated execution time: 4–8 ч; rough_range_not_commitment. Перед стартом уточнить на актуальной сборке.
- Agents: docs-maintainer + product-manager; независимые участки назначить перед исполнением; одновременные записи в один файл исключить.
- Skills: implementation-planner для плана; task-matching implementation/verification skills выбираются при старте, без установки новых skills этой задачей.
- Output artifacts: scoped diff в перечисленных work locations; результаты проверок и Documentation impact в этом Completion Report; статус в JSON этой группы; короткий handoff в RUNLOG.md.
- Rollback: отменить только собственные hunks после проверки drift; для данных — сохранённый synthetic backup и согласованный recovery contract; destructive Git не допускается.
- Planning update 15.11.2026: расширены acceptance и связи с F26–F29; исполнение не начато.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Проверить актуальность находки. Назначить владельца и уточнить минимальный проверяемый slice.

#### Completion Report

- status: planned
- what was done: задача сформулирована в плане; реализация и выполнение её приёмочных сценариев не начаты.
- files touched / work locations: implementation none; планируемые work locations указаны в Scope.
- technical value delivered: результат реализации ещё не получен.
- product value delivered: результат для пользователя ещё не подтверждён.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: только исходные ссылки и статические наблюдения в Source; future Verification gates не выполнены этой задачей.
- residual risks: source_reconciliation_not_history_deletion; актуальность исходного состояния повторно проверяется при старте.
- follow-up: Next step выше; после выполнения синхронизировать статус JSON, эту карточку и только затронутые control-plane claims.
- Documentation impact: planning_only; пока код и функциональные claims не меняются. При завершении сопоставить changed fact, source revision, canonical owner, updated/no_change_needed/handoff_required и evidence в этом отчёте.


### Task `PAOS-FUNC-26`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-26 — Добавить файловый браузер проекта
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-10`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`, `PAOS-FUNC-33`
- Source: Sources показывает шесть фиксированных Control-plane файлов; catalog читает .md/.txt, graph — отобранные исходники. Общего дерева и независимого directory API в проверенном onboarding нет. [apps/local-service/src/adapters/project-sources.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts), [apps/web/src/ui/Operations.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/ui/Operations.tsx), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/web/src/features/graph/GraphExplorer.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/graph/GraphExplorer.tsx). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Добавить файловый браузер проекта.
- Technical value: Независимый от графа API директорий и безопасного чтения с ленивой загрузкой, стабильными ссылками и ограниченными ответами.
- Product value: Пользователь видит структуру выбранной папки и открывает доступные файлы, даже когда индекс не готов или язык не поддерживается.
- Scope: `packages/contracts/project-files.ts` (новый планируемый файл); `apps/local-service/src/project-files/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/files/ProjectFiles.tsx` (новый планируемый файл); `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/locales/app.ts`; `tests/web/project-files.test.mts` (новый планируемый файл); `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл). Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Architecture boundary: project-files API → checked filesystem metadata/read → ProjectFiles UI; graph readiness не является precondition.
- Non-goals: Редактирование, удаление и перемещение файлов; terminal; выполнение preview-кода; автоматическая передача содержимого модели.
- Expected result: Проверяемое дерево и read-only reader, typed API, focused/browser receipts в этой карточке.
- Acceptance criteria: AC1: После регистрации раздел «Файлы» доступен без графа и завершённого сканирования; видны вложенные и пустые каталоги, исходники, конфигурации и бинарные файлы как метаданные, в пределах разрешённой политики F28. AC2: Раскрытие каталога загружает только нужную ветку; pagination и фильтры показывают границы выборки; поиск по имени/пути явно сообщает scope. Метаданные содержат relativePath, тип, размер, modifiedAt и состояние доступа. AC3: Текст читается по отдельному запросу с проверкой root identity, revision, размера и кодировки; binary/oversized/unreadable получают объяснение. Неподдерживаемое индексатором расширение не скрывает файл. HTML/скрипты не исполняются при просмотре. AC4: Нет чтения за пределами корня через traversal, symlink/junction/hardlink и подмену каталога; sensitive content не раскрывается. Выбор файла не передаёт весь проект модели и не выдаёт разрешение на выполнение. AC5: Выбранный путь можно скопировать и использовать как file reference; Control-plane — фильтр над реальными путями. Смена проекта и поздний ответ не смешивают дерево; RU/EN, keyboard, focus, empty/error/loading проверены. AC6: Контракт file/line navigation поддерживает будущие переходы из Map/Database/code usages и возврат к выбранному файлу; недоступный/удалённый source объяснён. F26 не ждёт F30–F34, backend action отсутствующей capability не показывает ложный результат.
- Verification gates: `node --test tests/web/project-files.test.mts tests/web/project-inventory.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`; `npm run build:web`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: directory_api_ui_contract_review_required; status=proposal_staged, владелец design gate — builder + tester; product-manager принимает сценарий просмотра. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 24–40 ч, rough planning range; уточнить после API/UI контракта; не обязательство по сроку.
- Agents: builder + tester; product-manager принимает сценарий просмотра; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Проверяемое дерево и read-only reader, typed API, focused/browser receipts в этой карточке. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Завершить F29/F10/F18 и финальные gates FUNC-G03.

#### Completion Report

- status: implemented
- what was done: Реализованы lazy project Files, bounded directory search/pagination, безопасный reader, source/metadata pins, copy и deep links с RU/EN и двумя темами.
- files touched / work locations: apps/local-service/src/project-files/service.mts; apps/web/src/features/files/ProjectFiles.tsx; apps/local-service/src/http/application.mts; apps/web/src/ui/App.tsx; tests/web/project-files-api.test.mts
- technical value delivered: Registry/root/policy/revision contracts проверены через реальные HTTP/SQLite/FS и production React.
- product value delivered: Данные проекта доступны с явными причинами недоступности и сохранённой навигацией.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Завершить F29/F10/F18 и финальные gates FUNC-G03.
- Documentation impact: updated; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-27`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-27 — Сделать сканирование управляемым фоновым заданием
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:00
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-14`, `PAOS-FUNC-18`, `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`, `PAOS-FUNC-29`, `PAOS-FUNC-33`
- Source: POST /projects коммитит регистрацию, затем ожидает inspectProjectSources/codeIndex.rebuild. Scan summary не является durable job; once receipts находятся в памяти и истекают через 10 минут. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [apps/local-service/src/storage/sqlite-worker.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/storage/sqlite-worker.mts), [apps/web/src/features/projects/ProjectOnboarding.tsx](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/web/src/features/projects/ProjectOnboarding.tsx), [tests/web/settings-desktop.test.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/tests/web/settings-desktop.test.mts). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Сделать сканирование управляемым фоновым заданием.
- Technical value: Сохраняемые scan ID и этапы, bounded worker, идемпотентность, отмена, повтор и восстановление отдельно от регистрации проекта.
- Product value: Проект доступен сразу после регистрации; пользователь видит ход сканирования, частичный результат и способ продолжить после сбоя.
- Scope: `packages/contracts/project-scan.ts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `apps/local-service/src/storage/local-store.mts`; `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/storage/migrations/schema.mts`; `apps/local-service/src/code-index/service.mts`; `apps/web/src/api/client.ts`; `apps/web/src/features/projects/ProjectOnboarding.tsx`; `tests/web/project-scans.test.mts` (новый планируемый файл); `tests/web/settings-desktop.test.mts`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Architecture boundary: project registration → profile-owned scan job → bounded analyzers; независимые lifecycle и source authority.
- Non-goals: Запуск задач/агентов, provider calls, автоматическое выполнение команд проекта и изменение target-файлов; бесконечный watchdog.
- Expected result: Durable scan lifecycle и UI прогресса; schema compatibility/rollback и crash/cancel/retry receipts.
- Acceptance criteria: AC1: Регистрация сохраняется один раз и возвращает доступный проект без ожидания полного обхода; scan status содержит scanId, root identity, policy version, этап inventory/documents/code/analysis, начало/обновление, счётчики и причины partial/error. AC2: Повтор Add/retry в том числе после restart не создаёт новый проект или дублирующую работу; конкурентные запросы одной revision объединяются либо получают объяснимый conflict. Изменившийся root не продолжает старое задание. AC3: Cancel останавливает дальнейшую работу и позднюю публикацию; повтор запускается с явно определённой revision. Restart восстанавливает либо переводит задание в recovery_required/interrupted; незавершённое не становится completed. AC4: Заданы budgets времени/памяти/записей и concurrency; failure одного анализатора сохраняет допустимые результаты других этапов. Ready одного индекса не означает полный анализ проекта; неподключённый analysis adapter отображается как unavailable. AC5: Состояние и последнее успешное покрытие доступны после открытия Settings/проекта и restart; events или bounded polling не перезаписывают более новую revision. Scan bookkeeping остаётся в профиле PAOS, target workspace не изменяется. AC6: Версионированный analyzer contract допускает code/schema/code_database этапы с отдельными capabilities/status/progress, cancellation и atomic publication. F30–F32 проверяют внешние исполнители изолированно, F14/F33/F34 подключают только выбранные; F27 не зависит от их реализации и не запускает установщики автоматически.
- Verification gates: `node --test tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts tests/web/code-index.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: persisted_scan_state_recovery_schema_design_required; status=proposal_staged, владелец design gate — architect + builder + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 24–40 ч, rough planning range; storage/recovery design до build; не обязательство по сроку.
- Agents: architect + builder + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Durable scan lifecycle и UI прогресса; schema compatibility/rollback и crash/cancel/retry receipts. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Завершить F29/F10/F18 и финальные gates FUNC-G03.

#### Completion Report

- status: implemented
- what was done: Регистрация идемпотентна и возвращает queued до scan; profile-owned CAS хранит стадии/progress/restart/retry/cancel, publication guards сохраняют предыдущий graph. Persisted status UI подключён.
- files touched / work locations: apps/local-service/src/project-scans/service.mts; apps/local-service/src/storage/sqlite-worker.mts; apps/local-service/src/http/application.mts; apps/web/src/features/projects/ProjectScanStatus.tsx; tests/web/project-scans-api.test.mts
- technical value delivered: Registry/root/policy/revision contracts проверены через реальные HTTP/SQLite/FS и production React.
- product value delivered: Данные проекта доступны с явными причинами недоступности и сохранённой навигацией.
- actual implementation date and time: 15-11-2026 21:00
- verification evidence: .tmp/func-g03/browser-foundation/evidence-q8ECT0/result.json:15/15; .tmp/func-g03/f26-f27-api-integration.log:13/13; .tmp/func-g03/check-foundation.log:exit0; .tmp/func-g03/build-foundation.log:exit0
- residual risks: Bounded synthetic local verification; no provider calls, native clipboard or human/release acceptance. Final shared regression/native qualification follows.
- follow-up: Завершить F29/F10/F18 и финальные gates FUNC-G03.
- Documentation impact: updated; docs/backend/lifecycle.md; docs/backend/lifecycle.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-28`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-28 — Унифицировать инвентаризацию, покрытие и исключения
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 20:10
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-02`, `PAOS-FUNC-10`, `PAOS-FUNC-14`, `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-29`, `PAOS-FUNC-33`
- Source: scanCheckedSources использует жёсткий denylist и extension filter, не возвращает все пропуски и не читает .gitignore; лимит подходящих файлов может оборвать обход. Metadata, read и indexing coverage требуют раздельного контракта. [apps/local-service/src/code-index/sources.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/sources.mts), [apps/local-service/src/code-index/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/code-index/service.mts), [apps/local-service/src/artifacts/service.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/artifacts/service.mts), [apps/local-service/src/adapters/project-sources.ts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/adapters/project-sources.ts). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Унифицировать инвентаризацию, покрытие и исключения.
- Technical value: Общий контракт путей, revision и coverage для directory/document/code consumers при раздельных правах listing, reading и indexing.
- Product value: Файлы не исчезают из обзора из-за отсутствия языкового анализатора; пользователь понимает, что найдено, пропущено или недоступно.
- Scope: `packages/contracts/project-inventory.ts` (новый планируемый файл); `apps/local-service/src/project-inventory/service.mts` (новый планируемый файл); `apps/local-service/src/code-index/sources.mts`; `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/artifacts/service.mts`; `apps/local-service/src/adapters/project-sources.ts`; `tests/web/project-inventory.test.mts` (новый планируемый файл); `tests/web/code-index.test.mts`; `tests/web/skill-generation-artifacts.test.mts`. Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Architecture boundary: checked filesystem inventory → per-consumer visibility/read/index policy; source root остаётся владельцем файлов.
- Non-goals: Безусловное снятие существующих лимитов или denylist; полный обход excluded directories; секреты в индексах; новый независимый scanner без оценки reuse.
- Expected result: Общий inventory/coverage contract и миграция потребителей без ослабления guards; fixture evidence.
- Acceptance criteria: AC1: Контракт различает discovered, readable, indexed, unsupported, excluded и error; счётчики определяют разные стадии и не суммируют пересекающиеся множества как общее число файлов. Empty и unknown отличаются; отсутствие подходящего кода не означает полный анализ. AC2: Файловое дерево независимо от набора расширений индексатора. .gitignore и project include/exclude имеют явную precedence и разные правила видимости/индексации; ignore не выдаёт права доступа. Sensitive paths/content защищены даже при include override. AC3: Отчёт показывает применённую policy version, причины пропуска, лимиты и partial coverage. Тяжёлые generated/vendor каталоги не читаются без необходимости; разрешённое раскрытие метаданных не снимает ограничений чтения содержимого. AC4: Ошибка, превышение размера или unsupported encoding отдельного файла сохраняет другие разрешённые записи; directory-level denial помечает неполноту. При root identity drift, попытке выхода за корень или недостоверной revision публикация небезопасного результата блокируется. AC5: Bounded/paged inventory поддерживает normalised relative paths, Unicode/пробелы и Windows case semantics; ссылки и race conditions не расширяют root. Одинаковые policy/root/revision дают согласованные ссылки и причины во всех consumers. AC6: Изменение политики инвалидирует затронутые snapshots; file metadata не требует полного чтения всех исходников. Позитивные/отрицательные сценарии и нагрузочные границы проверены; исходники проекта не меняются. AC7: PoC и будущие adapters применяют те же правила root/policy/read/index и показывают несовпадение coverage; сторонний индексатор не обходит исключения и не создаёт кеш в target. Обнаруженные DB/ORM/migration candidates — метаданные, не разрешение подключаться или выполнять миграции; scan limits и sensitive paths сохраняются.
- Verification gates: `node --test tests/web/project-inventory.test.mts tests/web/code-index.test.mts tests/web/skill-generation-artifacts.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: inventory_policy_security_boundary_design_required; status=proposal_staged, владелец design gate — architect + builder + security-privacy-supply-chain-reviewer + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 12–20 ч, rough planning range; выбрать reuse/adapter до build; не обязательство по сроку.
- Agents: architect + builder + security-privacy-supply-chain-reviewer + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Общий inventory/coverage contract и миграция потребителей без ослабления guards; fixture evidence. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: F26/F27/F02 используют этот контракт; final combined browser/native qualification остаётся gate FUNC-G03.

#### Completion Report

- status: implemented
- what was done: Общий нижний inventory boundary внедрён в graph, artifact catalog и fixed control-plane consumers. Реализованы metadata tree, отдельные listing/read/index права, gitignore/project policy precedence, versioned pins/cursors, profile-owned policy CAS, partial per-file failures и redacted display-only read. Default analyzer read и hard sensitive/link/root/private-key guards сохраняют отказ. Проверена совместимость finite G02 projection с F28 authority.
- files touched / work locations: packages/contracts/project-inventory.ts; apps/local-service/src/project-inventory/service.mts; apps/local-service/src/code-index/sources.mts; apps/local-service/src/code-index/service.mts; apps/local-service/src/adapters/project-sources.ts; apps/local-service/src/artifacts/service.mts; apps/local-service/src/storage/local-store.mts; apps/local-service/src/storage/sqlite-worker.mts; tests/web/project-inventory*.test.mts
- technical value delivered: Единый root/policy/revision контракт и безопасное чтение без дублирования scanner policy; metadata не выдаются за успешную индексацию.
- product value delivered: Разрешённые файлы сохраняются при ошибке отдельного source; причины исключений и неполнота видимы. UI-приёмка всей группы выполняется далее.
- actual implementation date and time: 15-11-2026 20:10
- verification evidence: .tmp/func-g03/f28-verified-final.log:57/57,0skip; .tmp/func-g03/f28-final-typecheck.log:exit0; .tmp/func-g03/f28-lower-evidence.json:current lower15/15/source hashes; .tmp/func-g03/f28-consumer-red.log -> f28-consumer-green.log; .tmp/func-g03/f28-state-red.log -> f28-state-green.log; .tmp/func-g03/f28-cursor-red.log -> f28-consumers-final.log
- residual risks: Known credential filtering is bounded; git global/info excludes and tracked state are not git-status parity. Production browser/native tuple qualification and human acceptance are separate group/follow-up gates.
- follow-up: F26/F27/F02 используют этот контракт; final combined browser/native qualification остаётся gate FUNC-G03.
- Documentation impact: updated; docs/code-intelligence/inventory.md; docs/code-intelligence/inventory.en.md; docs/security/filesystem.md; docs/security/filesystem.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-29`

- Delivery group: `FUNC-G03`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-29 — Подключить core discovery к добавлению проекта
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца на файловую директорию и управляемое сканирование; многоэтапный функциональный scope.
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 21:41
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g03_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-27`, `PAOS-FUNC-28`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-20`, `PAOS-FUNC-24`
- Source: Core analyze_workspace и run_first_project_analysis умеют discovery/first-run composition. Проверенный POST /projects не вызывает их: сейчас это только source inventory и code graph. [apps/local-service/src/http/application.mts](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/apps/local-service/src/http/application.mts), [plugins/product-agent-os/scripts/product_agent_os/discovery.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/discovery.py), [plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py](https://github.com/alexroadcaster/product-agent-os/blob/33ed0350738e549f932a9fffdeeff9d4908ca94c/plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py). Источники прочитаны в анализе 15.11.2026; runtime не запускался.
- Short description: Подключить core discovery к добавлению проекта.
- Technical value: Версионированный read-only adapter к существующему discovery/first-run analysis с provenance, ограничениями и invalidation.
- Product value: После добавления проекта видны стек, структура, Control-plane gaps и обоснованные следующие шаги, а не только количество узлов графа.
- Scope: `apps/local-service/src/project-analysis/service.mts` (новый планируемый файл); `packages/contracts/project-analysis.ts` (новый планируемый файл); `apps/local-service/src/project-scans/service.mts` (новый планируемый файл); `apps/local-service/src/http/application.mts`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `apps/web/src/features/projects/ProjectAnalysis.tsx` (новый планируемый файл); `apps/web/src/features/projects/ProjectOnboarding.tsx`; `apps/web/src/api/client.ts`; `tests/web/project-analysis.test.mts` (новый планируемый файл); `tests/web/single-window/project-files-browser-acceptance.mts` (новый планируемый файл). Новые пути помечены planned; файл, вводимый другой задачей, используется только после неё.
- Architecture boundary: profile scan stage → bounded structured core adapter → project analysis view; analysis не расширяет execution authority.
- Non-goals: Автоматический ремонт проекта, создание Control-plane, LLM-аудит, сборка/тесты target и публикация; неподтверждённые обещания полноты.
- Expected result: Read-only discovery integration и source-backed summary, capability/timeout/stale fixtures; reuse contract в существующей architecture.
- Acceptance criteria: AC1: До build выбран способ reuse существующих core discovery/first-run модулей и deployment/runtime contract. Недоступный Python/adapter/version даёт явный unavailable; установка зависимостей и альтернативный полный scanner автоматически не запускаются. AC2: Analysis запускается как отдельный этап F27, использует согласованную inventory policy F28 и возвращает schema version, source revision, stack/components, control-plane coverage, findings с источниками/confidence/limitations. AC3: Обнаруженные scripts/configs только анализируются как данные: не исполняются команды проекта, tests, hooks, модели или провайдеры; target files не создаются и не исправляются. Предложения Control-plane остаются предложениями. AC4: Пустой проект, проект без Control-plane, Python-only, mixed stack и unsupported language получают объяснимые результаты без выдуманной полноты; timeout/error сохраняют доступное дерево и уже полученное покрытие. AC5: Изменения файлов, root или inventory policy делают прежние выводы stale; повтор и restart не смешивают revisions. Выводы доступны из выбранного проекта в RU/EN, связаны с разрешёнными file references и не раскрывают secrets. AC6: Discovery показывает кандидаты языков/ORM/DB/schema files со source и confidence для F14/F33/F34, не открывает соединения и не исполняет migrations. В project overview есть маршруты к Files/Map/Database по capabilities; отсутствие адаптера не подменяется сторонним auto-install.
- Verification gates: `node --test tests/web/project-analysis.test.mts tests/web/project-scans.test.mts tests/web/settings-desktop.test.mts`; `npm run check:web-m1`; `npm run test:web-m1`. Ожидается exit0 и прохождение всех scoped AC на synthetic fixtures. Это будущие команды: новые tests/harness сейчас отсутствуют. Browser acceptance использует согласованный runner protocol и disposable roots; точные flags фиксируются до build. Если меняются core Python модули, дополнительно применяются focused tests и полный маршрут TEST.md для plugin/runtime. Runtime tuple проверяется заново перед native acceptance после изменения pinned sources.
- Risks / approval gates: core_adapter_capability_contract_and_readonly_review_required; status=proposal_staged, владелец design gate — architect + plugin-runtime-builder + builder + tester. До build утвердить API/policy/state contract, source ownership и recovery. Нет provider/live calls, установки зависимостей или изменений существующих профилей без отдельной точной авторизации.
- Complexity: high — API, filesystem boundary и обработка неполных результатов.
- Estimated execution time: 16–32 ч, rough planning range; integration/packaging выбор до build; не обязательство по сроку.
- Agents: architect + plugin-runtime-builder + builder + tester; роли предложены, subagents не запущены. Shared API/storage/UI файлы изменять последовательно с владельцами зависимых задач.
- Skills: implementation-planner для этой планировки; task-matching runtime/frontend/test skills выбрать при старте. Для Python implementation соблюдать существующие python-design-patterns/python-code-style guidance.
- Output artifacts: Read-only discovery integration и source-backed summary, capability/timeout/stale fixtures; reuse contract в существующей architecture. Статус — JSON этой группы; evidence и Documentation impact — этот Completion Report; компактный handoff — RUNLOG.md.
- Rollback: только собственные изменения после проверки drift; schema/recovery изменения проверять на disposable profile. Target files не менять; старый успешный snapshot сохранять до атомарной публикации нового.
- Planning update GitHub/UI 15.11.2026: обновлены AC и зависимости F30–F34; общий UI/UX-контракт дополнения применяется в затронутом scope, реализация не начата.
- Next step: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.

#### Completion Report

- status: implemented
- what was done: Core discovery подключён отдельной durable scan стадией через фиксированный Python -I -S -B bridge и bounded F28 projection; real core identity/source revision, stack/languages/control-plane/schema candidates, capabilities и stale/unavailable доступны в overview. Target scripts, DB и providers не запускаются.
- files touched / work locations: apps/local-service/src/project-analysis/service.mts; apps/local-service/src/project-analysis/bridge.py; apps/local-service/src/http/application.mts; apps/web/src/features/projects/ProjectAnalysis.tsx; tests/web/project-analysis.test.mts; tests/web/project-analysis-api.test.mts
- technical value delivered: Shared root/policy/revision contracts и final authority fences подтверждены на текущих API/SQLite/FS/build/native fixtures.
- product value delivered: Неполнота и устаревшие данные видимы; файловые ограничения объясняются до dispatch, данные и черновики сохраняются.
- actual implementation date and time: 15-11-2026 21:41
- verification evidence: npm run test:web-m1:594/594,0skip; .tmp/func-g03/full-web-native.log; .tmp/func-g03/browser-final/evidence-IfLiEa/result.json:19/19; .tmp/func-g03/native-candidate-reviewed.log:passed; .tmp/func-g03/native-default-reviewed.log:passed; independent review cycle2:5/5,closed_allowed
- residual risks: Local synthetic engineering acceptance; checkout-only core with explicit packaged unavailable; bounded projection/output without portable OS RSS cap. No provider/human/release acceptance. F14/F33/F34 own future consumers.
- follow-up: Нет незавершённой работы этой карточки; будущие consumers/packaging/performance имеют собственные задачи.
- Documentation impact: updated; docs/code-intelligence/discovery.md; docs/code-intelligence/discovery.en.md; docs/architecture/data-flow.md; docs/architecture/data-flow.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/sources/registry.md; docs/sources/registry.en.md; scoped source checks passed.

### Task `PAOS-FUNC-30`

- Delivery group: `FUNC-G02`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-30 — Проверить dependency-cruiser для графа зависимостей JS/TS
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца перенести GitHub research в план с UI/UX и dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-14`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [sverweij/dependency-cruiser](https://github.com/sverweij/dependency-cruiser)
- Short description: Проверить dependency-cruiser для графа зависимостей JS/TS.
- Technical value: Проверить reuse анализатора импортов вместо расширения собственного lexical parser; согласовать adapter JSON и семантику ребра.
- Product value: Пользователь и агент видят проверяемые зависимости файла, циклы и путь к месту изменения.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Предложенные пути; существующие shared UI/API/storage файлы изменяются последовательно.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; сторонний cache не является PAOS control-plane DB
- Non-goals: Реализация вне выбранных capabilities; изменение target/global configuration; provider/live DB calls, публикация или установка текущим планированием. PoC не означает production integration.
- Expected result: Сравнительный evidence и adopt/bounded_adopt/reject, контракт адаптера и изолированный UI-прототип.
- Acceptance criteria: AC1: До запуска зафиксированы версия/commit, MIT и лицензии поставки, Windows/Node compatibility, fixture corpus, baseline текущего lexical graph и бюджеты времени/RSS/размера ответа; результаты не выводятся из README. AC2: На synthetic JS/TS fixtures проверены ESM/CommonJS, tsconfig aliases, re-exports, cycles, missing imports, dynamic import и monorepo boundaries; импорт не называется вызовом функции. Известные ожидаемые рёбра сопоставлены с output: false positives/negatives и unresolved перечислены. AC3: JSON adapter сохраняет normalized path/root identity, source revision, тип/направление ребра и evidence; соблюдает согласованный контракт F28 без зависимости от завершения его реализации. Конфигурация передаётся PAOS как данные: target JS-config/scripts/hooks не исполняются; target hashes не меняются. AC4: В изолированном UI-прототипе существующей «Карты» есть режим «Зависимости»: поиск файла, incoming/outgoing, фильтр типа, выделение пути/цикла, переход к строке/файлу и синхронные graph/list/Mermaid. Ошибки и unsupported показаны; peer review сценария не считается human acceptance. AC5: На одинаковых заданиях поиска места изменения сравнены время, файлы/объём контекста и правильность результата с baseline; parser failure/timeout не скрывает дерево. Provider calls не нужны для deterministic benchmark; оценка с моделью — только при отдельной точной авторизации. AC6: Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом. AC7: Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance.
- UI/UX scope: До build подготовлены и согласованы wireframes и карта навигации в существующем V3 design: проект → «Файлы», «Карта», «База данных»; названия уточняются на design review. Для затронутого экрана определены loading/empty/partial/error/unavailable/stale, progress/cancel/retry по capabilities, RU/EN, обе темы, keyboard/focus, читаемые подписи и доступная таблица вместо обязательного чтения диаграммы. Смена проекта, возврат назад, фильтр и выбранный объект не смешивают данные; видны source/revision/coverage. PoC использует изолированный прототип, production UI принимается в F14/F33/F34.
- Verification gates: До запуска закрепить executable commands и versions в Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. Ни одна команда не выполнена текущей планировкой.
- Risks / approval gates: poc_protocol_and_graph_ui_design_required; Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.
- Complexity: high — source accuracy, process/data boundaries и UI consistency
- Estimated execution time: 12–20 ч PoC; build отдельно в F14; rough_range_not_commitment, не обязательство по сроку.
- Agents: architect + graph-cockpit-engineer + tester; роли предложены, сейчас subagents не запущены
- Skills: Task-matching skills выбрать при старте; текущая планировка не устанавливает и не активирует skills/plugins.
- Output artifacts: Результат и receipts — этот Completion Report, status — JSON группы; обновления existing architecture/design/help по реальному scope.
- Rollback: Только свои hunks после проверки drift; disposable PoC artifacts очищаются в согласованных границах, user processes не завершаются; прежние snapshots сохраняются до успешной публикации.
- Next step: F14: ограниченный import-only adapter и текущие lexical queries; semantic/call-path остаётся gap.

#### Completion Report

- status: implemented
- what was done: dependency-cruiser18.6.0: подтверждены 10/10 импортов против 7/10 lexical baseline и 3/3 задания против 2/3. Пройдены 17 engine scenarios и 4 model tests; проверены import-only adapter и изолированный V3-прототип. Решение: bounded_adopt_import_only; внедрение F14 planned.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; соответствующие domain docs RU/EN.
- technical value delivered: версионированный adapter proposal, воспроизводимое измеренное решение и явные границы rejected capabilities.
- product value delivered: проверен изолированный graph/list/Mermaid/evidence/source прототип; полезность для человека не измерялась.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: результаты FUNC-G02 выше; engine receipts .tmp/func-g02/; combined unit22/22, browser22/22, scoped typecheck/build; реальные candidate failures сохранены.
- residual risks: исследовательский PoC; production integration и human acceptance не подтверждены; F31 downstream cases не запускались после admission rejection.
- follow-up: F14: import-only F30 + bounded lexical; semantic/call-path gap.
- Documentation impact: обновлены adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry и владеющие карточки RU/EN; Control-Plane Sync выполнен.

### Task `PAOS-FUNC-31`

- Delivery group: `FUNC-G02`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-31 — Проверить codebase-memory-mcp как движок индексации для агентов
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца перенести GitHub research в план с UI/UX и dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-14`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)
- Short description: Проверить codebase-memory-mcp как движок индексации для агентов.
- Technical value: Оценить SQLite-backed индекс, многоязычные связи, запросы и управляемость отдельного native процесса через версионированный adapter.
- Product value: Агент получает небольшой релевантный контекст и объяснимый путь к изменению, а пользователь видит основания поиска.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Предложенные пути; существующие shared UI/API/storage файлы изменяются последовательно.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; сторонний cache не является PAOS control-plane DB
- Non-goals: Реализация вне выбранных capabilities; изменение target/global configuration; provider/live DB calls, публикация или установка текущим планированием. PoC не означает production integration.
- Expected result: Сравнительный evidence и adopt/bounded_adopt/reject, контракт адаптера и изолированный UI-прототип.
- Acceptance criteria: AC1: Закреплены version/commit/license и зависимости поставки, Windows packaging, поддерживаемые языки/виды связей, workload и бюджеты. Сравнение с текущим поиском использует те же ground-truth fixtures и задания, что F30; F30 не обязан завершиться раньше. AC2: Проверены search/definition/references/call path/impact и related tests только для заявленных capabilities; measured precision/recall, unresolved и unsupported опубликованы. Bounded ответы дают file/line evidence, revision, truncation/pagination; stale индекс не выдаётся за текущий. AC3: Измерены cold/incremental indexing, rename/delete/branch-like change, cancel/retry/restart, два проекта, memory/disk и latency; SQLite/cache/locks принадлежат движку и не открываются PAOS как неофициальный writable API. AC4: На disposable профиле доказаны lifecycle/cleanup daemon, timeout и child-process ownership; account-wide coordination и конфликт другого build/cache исследованы. Нельзя завершать пользовательский daemon или менять global MCP/skills/hooks/PATH, скачивать модели или отправлять код наружу. Если изоляция несовместима с PAOS, результат bounded_adopt/reject, не обход защиты. AC5: Прототип «Карты» содержит поиск символа, callers/callees/path/impact, панель объяснения и переход к исходнику; состояния недоступного движка, partial coverage, stale и превышенного бюджета видны. Контракт UI не зависит от внутренних таблиц движка; изучается использование уже существующего graph UI PAOS. AC6: Сравнительный отчёт определяет роли F30/F31: один выбранный backend либо явная композиция по языкам без дублей/конфликтующих revisions. До подключения engine учитывает inventory policy F28; при невозможности ограничить индексирование чувствительных файлов вариант отклонён. AC7: Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом. AC8: Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance.
- UI/UX scope: До build подготовлены и согласованы wireframes и карта навигации в существующем V3 design: проект → «Файлы», «Карта», «База данных»; названия уточняются на design review. Для затронутого экрана определены loading/empty/partial/error/unavailable/stale, progress/cancel/retry по capabilities, RU/EN, обе темы, keyboard/focus, читаемые подписи и доступная таблица вместо обязательного чтения диаграммы. Смена проекта, возврат назад, фильтр и выбранный объект не смешивают данные; видны source/revision/coverage. PoC использует изолированный прототип, production UI принимается в F14/F33/F34.
- Verification gates: До запуска закрепить executable commands и versions в Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. Ни одна команда не выполнена текущей планировкой.
- Risks / approval gates: poc_daemon_isolation_and_agent_query_design_required; Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.
- Complexity: high — source accuracy, process/data boundaries и UI consistency
- Estimated execution time: 20–36 ч PoC; integration отдельно в F14; rough_range_not_commitment, не обязательство по сроку.
- Agents: architect + graph-cockpit-engineer + tester; роли предложены, сейчас subagents не запущены
- Skills: Task-matching skills выбрать при старте; текущая планировка не устанавливает и не активирует skills/plugins.
- Output artifacts: Результат и receipts — этот Completion Report, status — JSON группы; обновления existing architecture/design/help по реальному scope.
- Rollback: Только свои hunks после проверки drift; disposable PoC artifacts очищаются в согласованных границах, user processes не завершаются; прежние snapshots сохраняются до успешной публикации.
- Next step: F14: ограниченный import-only adapter и текущие lexical queries; semantic/call-path остаётся gap.

#### Completion Report

- status: implemented
- what was done: codebase-memory-mcp0.12.1 отклонён до index admission; выполнены 12 проверок admission/целостности/сохранности и 3 unit tests. Последующие сценарии not_executed_after_failed_admission, метрики null. Проверены unavailable UI и отдельный неизмеренный call-contract fixture. Решение: reject_current_windows_workspace_profile.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; соответствующие domain docs RU/EN.
- technical value delivered: версионированный adapter proposal, воспроизводимое измеренное решение и явные границы rejected capabilities.
- product value delivered: проверен изолированный graph/list/Mermaid/evidence/source прототип; полезность для человека не измерялась.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: результаты FUNC-G02 выше; engine receipts .tmp/func-g02/; combined unit22/22, browser22/22, scoped typecheck/build; реальные candidate failures сохранены.
- residual risks: исследовательский PoC; production integration и human acceptance не подтверждены; F31 downstream cases не запускались после admission rejection.
- follow-up: F14: import-only F30 + bounded lexical; semantic/call-path gap.
- Documentation impact: обновлены adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry и владеющие карточки RU/EN; Control-Plane Sync выполнен.

### Task `PAOS-FUNC-32`

- Delivery group: `FUNC-G02`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-32 — Проверить tbls для извлечения схемы БД и Mermaid ERD
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца перенести GitHub research в план с UI/UX и dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 15-11-2026 19:24
- Priority: P2
- Evidence level: poc_research_locally_verified
- Execution authority: owner_authorized_isolated_synthetic_poc; FUNC-G02,15.11.2026.
- Depends on: нет
- Blocks: `PAOS-FUNC-33`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [k1LoW/tbls](https://github.com/k1LoW/tbls), [www.sqlite.org/pragma.html](https://www.sqlite.org/pragma.html)
- Short description: Проверить tbls для извлечения схемы БД и Mermaid ERD.
- Technical value: Оценить внешний schema adapter JSON/Mermaid против встроенной SQLite introspection и закрепить контракт schema snapshot.
- Product value: Получить достоверную карту таблиц без ручного рисования и без чтения пользовательских строк.
- Scope: `docs/planning/functional-remediation-2026-11-15.md`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`. Предложенные пути; существующие shared UI/API/storage файлы изменяются последовательно.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; сторонний cache не является PAOS control-plane DB
- Non-goals: Реализация вне выбранных capabilities; изменение target/global configuration; provider/live DB calls, публикация или установка текущим планированием. PoC не означает production integration.
- Expected result: Сравнительный evidence и adopt/bounded_adopt/reject, контракт адаптера и изолированный UI-прототип.
- Acceptance criteria: AC1: Закреплены version/commit/MIT/dependency licenses, Windows distribution, минимальный SQLite-first scope и бюджеты; tbls JSON/Mermaid сравниваются с metadata introspection существующего SQLite driver. PostgreSQL и другие СУБД — отдельные capability targets, не автоматический scope. AC2: Synthetic SQLite покрывает PK/FK, composite FK, UNIQUE/index, views, nullable/generated columns, self-reference и отсутствие FK. Список объектов и рёбер сравнен с ground truth; ограничение формата/драйвера и inferred relation не скрыты. AC3: Используется явно выбранный read-only fixture/consistent snapshot; данные строк, credentials и DSN не попадают в logs/output. Проверены locked/WAL/change-during-read, недоступный и повреждённый файл; соединение не создаёт отсутствующую БД, не мигрирует её и не исполняет project config/extensions/hooks. AC4: Результат содержит source kind, schema fingerprint/revision, tables/columns/keys/indexes/views, coverage и warnings; canonical JSON и Mermaid согласованы. Проверены экранирование имён и limits на размер ERD, неисполнение HTML/скриптов. AC5: Изолированный прототип будущего раздела «База данных» показывает источник, ERD и таблицу объектов, выбор таблицы/колонки, поиск/фильтр и явный no-database/unsupported/stale/error. Экспорт Mermaid не требует внешнего сервиса; tiny Mermaid проверяется на нужной ERD-семантике. AC6: Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом. AC7: Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance.
- UI/UX scope: До build подготовлены и согласованы wireframes и карта навигации в существующем V3 design: проект → «Файлы», «Карта», «База данных»; названия уточняются на design review. Для затронутого экрана определены loading/empty/partial/error/unavailable/stale, progress/cancel/retry по capabilities, RU/EN, обе темы, keyboard/focus, читаемые подписи и доступная таблица вместо обязательного чтения диаграммы. Смена проекта, возврат назад, фильтр и выбранный объект не смешивают данные; видны source/revision/coverage. PoC использует изолированный прототип, production UI принимается в F14/F33/F34.
- Verification gates: До запуска закрепить executable commands и versions в Completion Report; synthetic fixtures, baseline comparison, target preservation and isolated UI checks. Ни одна команда не выполнена текущей планировкой.
- Risks / approval gates: poc_database_readonly_and_erd_ui_design_required; Результат — adopt / bounded_adopt / reject с receipts, закреплёнными version/commit/license, поддерживаемыми платформами и сравнением с baseline. Обоснованный reject закрывает PoC как исследование, но не реализует функцию; downstream design выбирает альтернативу или фиксирует blocker, без молчаливого fallback. Установка/запуск не разрешены текущим planning-only запросом.
- Complexity: high — source accuracy, process/data boundaries и UI consistency
- Estimated execution time: 12–20 ч PoC; integration отдельно в F33; rough_range_not_commitment, не обязательство по сроку.
- Agents: architect + graph-cockpit-engineer + tester; роли предложены, сейчас subagents не запущены
- Skills: Task-matching skills выбрать при старте; текущая планировка не устанавливает и не активирует skills/plugins.
- Output artifacts: Результат и receipts — этот Completion Report, status — JSON группы; обновления existing architecture/design/help по реальному scope.
- Rollback: Только свои hunks после проверки drift; disposable PoC artifacts очищаются в согласованных границах, user processes не завершаются; прежние snapshots сохраняются до успешной публикации.
- Next step: F33: выбранный node:sqlite metadata adapter proposal; production integration planned.

#### Completion Report

- status: implemented
- what was done: tbls1.96.1: 26 наблюдений, из них 23 positive и 3 candidate failures: пропуск generated, ошибка валидного имени и создание отсутствующей БД. Явно выбрана read-only metadata alternative node:sqlite; исправлена effective nullable, пройдены 6 unit tests и schema UI/export. Решение: reject_authoritative_sqlite_metadata.
- files touched / work locations: tests/web/poc/func-g02/; tests/fixtures/func_g02/; design/2026-11-15-func-g02/prototype/; соответствующие domain docs RU/EN.
- technical value delivered: версионированный adapter proposal, воспроизводимое измеренное решение и явные границы rejected capabilities.
- product value delivered: проверен изолированный graph/list/Mermaid/evidence/source прототип; полезность для человека не измерялась.
- actual implementation date and time: 15-11-2026 19:24
- verification evidence: результаты FUNC-G02 выше; engine receipts .tmp/func-g02/; combined unit22/22, browser22/22, scoped typecheck/build; реальные candidate failures сохранены.
- residual risks: исследовательский PoC; production integration и human acceptance не подтверждены; F31 downstream cases не запускались после admission rejection.
- follow-up: F33: explicit node:sqlite metadata adapter; production integration planned.
- Documentation impact: обновлены adapters/queries-impact/db/erd, product/user-journeys, testing/test-map, source registry и владеющие карточки RU/EN; Control-Plane Sync выполнен.

### Task `PAOS-FUNC-33`

- Delivery group: `FUNC-G04`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-33 — Добавить карту БД и раздел «База данных» проекта
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца перенести GitHub research в план с UI/UX и dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-26`, `PAOS-FUNC-27`, `PAOS-FUNC-28`, `PAOS-FUNC-32`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`, `PAOS-FUNC-34`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [k1LoW/tbls](https://github.com/k1LoW/tbls), [www.sqlite.org/pragma.html](https://www.sqlite.org/pragma.html)
- Short description: Добавить карту БД и раздел «База данных» проекта.
- Technical value: Версионированные schema snapshots, schema diff и read-only адаптер выбранного источника с provenance и freshness.
- Product value: Пользователь просматривает таблицы и связи, понимает источник и актуальность схемы и переходит к её определению.
- Scope: `apps/local-service/src/storage/sqlite-worker.mts`; `apps/local-service/src/storage/migrations/schema.mts`; `apps/local-service/src/project-scans/service.mts`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Sidebar.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`; `packages/contracts/database-map.ts` (новый планируемый файл); `apps/local-service/src/database-map/service.mts` (новый планируемый файл); `apps/web/src/features/database/DatabaseExplorer.tsx` (новый планируемый файл); `tests/web/database-map.test.mts` (новый планируемый файл); `tests/web/single-window/database-map-browser-acceptance.mts` (новый планируемый файл). Предложенные пути; существующие shared UI/API/storage файлы изменяются последовательно.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; сторонний cache не является PAOS control-plane DB
- Non-goals: Реализация вне выбранных capabilities; изменение target/global configuration; provider/live DB calls, публикация или установка текущим планированием. PoC не означает production integration.
- Expected result: Рабочий ограниченный API/UI сценарий по AC с evidence и явными gaps.
- Acceptance criteria: AC1: Перед build по F32 выбраны adapter, поддерживаемые источники и budgets; отсутствие выбранного backend остаётся blocker. БД самого PAOS и БД анализируемого проекта различаются. Обнаружение кандидата в дереве не открывает БД автоматически: пользователь выбирает разрешённый источник; external/live/credentials требуют точной авторизации. AC2: Контракт различает фактическую DB schema, статические ORM/миграции и предложенные связи. Неприменённая миграция не объявляется текущей БД; execute migrations/project code/extensions запрещён. SQLite-first read-only schema extraction не читает строки и не создаёт/меняет БД; PostgreSQL scope не предполагается из поддержки tbls. AC3: В project navigation добавлен раздел «База данных» с вкладками «Схема» и «Изменения»; в «Схеме» доступны ERD/табличный режим, поиск, фильтры, details таблицы/колонки, PK/FK/index/views и переход к разрешённому schema/migration source. Settings сохраняет регистрацию и выбор источника, не становится вторым независимым browser. AC4: ERD и таблица показывают одну revision; composite FK и direction корректны, inferred связи отличаются от declared. Выбор узла синхронизируется с details/list, большие схемы дают bounded subgraph и предупреждение, Mermaid export экранирует имена, не раскрывает secrets и сообщает фильтры/coverage. AC5: Вкладка «Изменения» сравнивает два совместимых snapshots: added/removed/changed objects; rename без доказательства показан как add/remove или гипотеза. При отсутствии baseline явное empty; дрейф источника/политики маркирует stale, schema fingerprint и время наблюдения видимы. AC6: Этап database_schema в F27 имеет независимые progress/cancel/retry/recovery/partial/error; ошибка сохраняет прежний успешный snapshot с stale и не блокирует Files/code. Невыбранная/отсутствующая БД — not_configured/none_found, а не бесконечная загрузка. Late responses другого проекта/revision отклоняются. AC7: Пройдены API/adapter и browser сценарии F32 на disposable fixtures: RU/EN, обе темы, keyboard/focus, table alternative, deep link/back, restart и switching projects. До/после target и контрольных файлов не меняются; отсутствуют sensitive DSN/rows в UI/export/logs; runtime evidence привязан к build. AC8: На workload F20 измерены schema extraction, cold/warm view, large ERD, memory и response size; budget deviations имеют bounded outcome. Docs/capabilities F24/F25 обновляются по реально внедрённому scope; UI mock не закрывает acceptance. AC9: Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance.
- UI/UX scope: До build подготовлены и согласованы wireframes и карта навигации в существующем V3 design: проект → «Файлы», «Карта», «База данных»; названия уточняются на design review. Для затронутого экрана определены loading/empty/partial/error/unavailable/stale, progress/cancel/retry по capabilities, RU/EN, обе темы, keyboard/focus, читаемые подписи и доступная таблица вместо обязательного чтения диаграммы. Смена проекта, возврат назад, фильтр и выбранный объект не смешивают данные; видны source/revision/coverage. PoC использует изолированный прототип, production UI принимается в F14/F33/F34.
- Verification gates: Adapter/API tests, UI type-check/build и synthetic browser acceptance на выбранном runtime; exact commands фиксируются до build. Новый harness сейчас не существует.
- Risks / approval gates: database_source_adapter_and_ui_design_required; После PoC выбрать backend и согласовать architecture/UI contract; без этого build не начинается.
- Complexity: high — source accuracy, process/data boundaries и UI consistency
- Estimated execution time: 16–24 ч design; build уточнить после F32; rough_range_not_commitment, не обязательство по сроку.
- Agents: architect + builder + graph-cockpit-engineer + tester; роли предложены, сейчас subagents не запущены
- Skills: Task-matching skills выбрать при старте; текущая планировка не устанавливает и не активирует skills/plugins.
- Output artifacts: Результат и receipts — этот Completion Report, status — JSON группы; обновления existing architecture/design/help по реальному scope.
- Rollback: Только свои hunks после проверки drift; disposable PoC artifacts очищаются в согласованных границах, user processes не завершаются; прежние snapshots сохраняются до успешной публикации.
- Next step: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.

#### Completion Report

- status: implemented
- what was done: Добавлены явный SQLite source в Settings, purpose-specific admission, native SHARE_READ lease, schema-only authorizer/extractor, profile CAS/two snapshots/diff, независимый F27schema stage и production Database Schema/Changes/ERD/table/details UI.
- files touched / work locations: packages/contracts/database-map.ts; apps/local-service/src/database-map/; apps/local-service/src/project-inventory/service.mts; apps/local-service/src/project-scans/service.mts; apps/local-service/src/http/application.mts; apps/web/src/features/database/; apps/web/src/ui/App.tsx; tests/web/database-map.test.mts; tests/web/database-source-admission.test.mts; tests/web/database-map-api.test.mts
- technical value delivered: Native write/rename/reparse/WAL/row/extension guards, late selection fences и retained stale metadata доказаны без target mutation.
- product value delivered: Схема выбранной БД, ключи, индексы, views и изменения доступны через RU/EN UI и API без чтения строк.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; native34/34 initial backend, final full658 includes new late-source-revocation regression and shared watchdog; actual readOnly adapter/API/private-source stages; profile DB excluded; target hashes and directory contents preserved; 200 unique objects, four revision-consistent pages of 50; current ERD timings in .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; prior 100-object/1969 ms failure retained; browser realcancel/retry/writerfailure/staleDDLdiff/restart/2projectlatefence/deepanchor; corrected390px header/scroll table actualscreenshots
- residual risks: Windows/offline project-local SQLite, без WAL/sidecars/real credentials/remote DB/rows. Views/virtual partial; rename какadd/remove. Schema128MiB stat/200objects/512KiB output, UI50objects perpage. Browser groupaggregate RSS не квалифицирован как whole-system peak.
- follow-up: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.
- Documentation impact: updated; docs/db/erd.md; docs/db/erd.en.md; docs/code-intelligence/adapters.md; docs/code-intelligence/adapters.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/frontend/components.md; docs/frontend/components.en.md; docs/product/capabilities.md; docs/product/capabilities.en.md; scoped source checks passed.

### Task `PAOS-FUNC-34`

- Delivery group: `FUNC-G04`; группа не заменяет Depends on и исходные AC.
- Task: PAOS-FUNC-34 — Связать код с таблицами и показать влияние изменений
- Status: implemented
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: запрос владельца перенести GitHub research в план с UI/UX и dependencies; planning_only
- Validator target: detailed task blocks
- Date and time of task implementation: 16-11-2026 00:43
- Priority: P2
- Evidence level: locally_verified
- Execution authority: owner_authorized_func_g04_local_synthetic; 15.11.2026.
- Depends on: `PAOS-FUNC-14`, `PAOS-FUNC-33`
- Blocks: `PAOS-FUNC-19`, `PAOS-FUNC-24`
- Source: GitHub research 15.11.2026: upstream README/license review; integration, performance and compatibility not verified locally. [sverweij/dependency-cruiser](https://github.com/sverweij/dependency-cruiser), [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp), [k1LoW/tbls](https://github.com/k1LoW/tbls)
- Short description: Связать код с таблицами и показать влияние изменений.
- Technical value: Добавить provenance-aware рёбра code→query/ORM→table с разрешением в совместимых code/schema revisions и bounded impact queries.
- Product value: Пользователь и агент видят, какой код читает или меняет таблицу и какие участки нужно проверить при изменении схемы.
- Scope: `apps/local-service/src/code-index/service.mts`; `apps/local-service/src/impact/service.mts`; `apps/local-service/src/database-map/service.mts`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/features/database/DatabaseExplorer.tsx`; `apps/web/src/features/files/ProjectFiles.tsx`; `apps/web/src/api/client.ts`; `apps/web/src/locales/app.ts`; `research/product-agent-os-web-architecture-2026-11-05.md`; `docs/planning/2026-11-13-v3-ui-implementation-plan.md`; `packages/contracts/code-database-links.ts` (новый планируемый файл); `apps/local-service/src/code-database/service.mts` (новый планируемый файл); `tests/web/code-database-links.test.mts` (новый планируемый файл); `tests/web/single-window/code-database-browser-acceptance.mts` (новый планируемый файл). Предложенные пути; существующие shared UI/API/storage файлы изменяются последовательно.
- Architecture boundary: read-only source → bounded versioned adapter → PAOS snapshot/query contract → UI/agent; сторонний cache не является PAOS control-plane DB
- Non-goals: Реализация вне выбранных capabilities; изменение target/global configuration; provider/live DB calls, публикация или установка текущим планированием. PoC не означает production integration.
- Expected result: Рабочий ограниченный API/UI сценарий по AC с evidence и явными gaps.
- Acceptance criteria: AC1: До build выбрана ограниченная language/SQL/ORM матрица на основе F30/F31/F32; code call paths включаются лишь при подтверждённой семантике, import edges не подменяют CALLS. Ground-truth cases и пороги precision/recall фиксируются до измерений. AC2: Связь хранит file/symbol/line span, query or model evidence, table identity/source, operation read/write/schema/unknown, extraction method/confidence и code+schema revisions. Dynamic SQL, naming heuristics, aliases и непрослеживаемый вызов остаются inferred/unresolved; unknown не считается отсутствием зависимости. AC3: Проверены raw SQL, выбранный ORM, join/aliases, одинаковые имена таблиц в разных источниках, rename/drop, generated/dynamic query и unsupported language. Код/запросы не исполняются; secrets/строки БД не извлекаются; precision/recall и ограничения представлены для каждого поддерживаемого типа. AC4: В «Базе данных» добавлена вкладка «Использование в коде»: таблица → места чтения/записи → файл/строка; в существующей «Карте» — фильтр связей с БД и панель пути/влияния. В reader файла доступен переход к связанным таблицам. Selection/deep link/back/filter сохраняются в пределах проекта; произвольные связи не рисуются как подтверждённые. AC5: Пользователь переключает confirmed/inferred и read/write/unknown, открывает evidence ребра и видит incomplete impact. Доступная таблица/список дублирует смысл графа; RU/EN, обе темы, keyboard/focus, empty/unsupported/partial/error/stale и большие результаты проверены в browser. AC6: Agent queries возвращают ограниченные source-backed paths и кандидаты тестов, truncation/cursors и обе revisions; rename/delete/change источника инвалидирует только совместимый snapshot. Смешение code/schema разных проектов или устаревших ревизий запрещено; rebuild/restart/cancel/retry проверены. AC7: На согласованных задачах сравнен поиск места изменения без связей и с ними: correctness, пропущенные affected files/tests, контекст и время; никаких обещаний полного runtime call graph. Budgets F20 и guardrails F27/F28 соблюдены; failures одного analyzer не блокируют дерево и schema map. AC8: Документация объясняет разницу schema ERD и code-to-table impact; release claims и capability states синхронизированы с F24/F25. Закрытие требует рабочей интеграции UI/API/agent contract, а не только схемы или прототипа. AC9: Общий UI/UX-контракт дополнения F30–F34 выполнен в пределах PoC-прототипа или production slice этой задачи; результаты design review и scoped browser checks записаны отдельно от human acceptance.
- UI/UX scope: До build подготовлены и согласованы wireframes и карта навигации в существующем V3 design: проект → «Файлы», «Карта», «База данных»; названия уточняются на design review. Для затронутого экрана определены loading/empty/partial/error/unavailable/stale, progress/cancel/retry по capabilities, RU/EN, обе темы, keyboard/focus, читаемые подписи и доступная таблица вместо обязательного чтения диаграммы. Смена проекта, возврат назад, фильтр и выбранный объект не смешивают данные; видны source/revision/coverage. PoC использует изолированный прототип, production UI принимается в F14/F33/F34.
- Verification gates: Adapter/API tests, UI type-check/build и synthetic browser acceptance на выбранном runtime; exact commands фиксируются до build. Новый harness сейчас не существует.
- Risks / approval gates: code_database_semantics_and_impact_ui_design_required; После PoC выбрать backend и согласовать architecture/UI contract; без этого build не начинается.
- Complexity: high — source accuracy, process/data boundaries и UI consistency
- Estimated execution time: 20–32 ч design; build после language/ORM scope; rough_range_not_commitment, не обязательство по сроку.
- Agents: architect + builder + graph-cockpit-engineer + tester; роли предложены, сейчас subagents не запущены
- Skills: Task-matching skills выбрать при старте; текущая планировка не устанавливает и не активирует skills/plugins.
- Output artifacts: Результат и receipts — этот Completion Report, status — JSON группы; обновления existing architecture/design/help по реальному scope.
- Rollback: Только свои hunks после проверки drift; disposable PoC artifacts очищаются в согласованных границах, user processes не завершаются; прежние snapshots сохраняются до успешной публикации.
- Next step: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.

#### Completion Report

- status: implemented
- what was done: Добавлены static literal JS/TS/SQL и Prisma subset, подтверждение только selected-source binding, both-revision/HMAC/32KiB queries, независимый F27code_database stage, Database Code usages/Map DB network/Files relatedtables и claimed App-agent project-query port.
- files touched / work locations: packages/contracts/code-database.ts; apps/local-service/src/code-database/; apps/local-service/src/runtime/app-agent-channel.mts; apps/local-service/src/runtime/app-agent-gateway.mts; apps/local-service/src/http/application.mts; apps/local-service/src/main.mts; apps/web/src/features/database/CodeDatabaseUsages.tsx; apps/web/src/features/files/ProjectFiles.tsx; tests/web/code-database-*.test.mts; tests/web/database-map-api.test.mts
- technical value delivered: Точные source/confidence/operation/span pins, native child containment, late-CAS/lease guards и безопасный bounded context вместо угаданных связей.
- product value delivered: Можно найти код и кандидаты тестов для таблицы, перейти к source evidence и отличить confirmed от inferred/unresolved.
- actual implementation date and time: 16-11-2026 00:43
- verification evidence: node --test --test-concurrency=1 tests/web/*.test.mts: 658/658, 0 fail, 0 skip; .tmp/func-g04/web-closure-native-final.log (authorized native synthetic executor); npm run check:web-m1: passed, .tmp/func-g04/typecheck-closure.log; npm run build:web: passed, .tmp/func-g04/build-responsive-final.log; UI/build hashes unchanged and verified by current browser receipt; production browser 18/18, 204 current source hashes and dist binding; .tmp/func-g04/browser-acceptance/evidence-m9Vcjh/result.json; native candidate/default passed, 0 provider/model/credential operations; .tmp/func-g04/native-closure-candidate.json + native-closure-default.json; adapter b7d5d1eb2a129763feacba96735d4ba40c0c0bd00dced861c1d83af6cf94726b; 32 changed Markdown sources + RU/EN matrices + preservation/source/build/native checks: see .tmp/func-g04/docs-closure.log, matrix-closure.log and closure-consistency.json; final audit result is owned by verification.latest; ground truth24/24; confirmed literalSQL8/8 andPrisma2/2 precision1/recall1 forliteraldenominators; rootshadowURL/TSparam/nestedDELETE regressions included; actual owned childnative stackfailure3221225725 contained,parentalive; deadline/cancel/bothpins/HMAC/source/policy/CAS/400-link32KiB pagination; production API + private claimed synthetic worker roundtrip; post-read/post-scope lease expiry rejects; no model/provider/credentials; static-search comparison finds missed ORM files; structured context/time notgenerally smaller/faster; literalproxy limits recorded; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.; P2 arbitrary SQLite table names: actual __proto__/constructor/toString persistence+restart RED→GREEN; reject array candidates. .tmp/func-g04/prototype-red.log + full658 current regression.
- residual risks: Prisma v6 static subset/JS/TS/SQL only; dynamic/env/untraced/other-source остаются uncertain. Нет выполненияSQL/ORM, rows/DSN/runtime callgraph. Snapshot/agentqueries требуют currentcode+schema pins. Human agent/model superiority и общий выигрыш времени/контекста не заявлены.
- follow-up: Обязательных незавершённых работ внутри карточки нет; измеренные ограничения сохранены. Общая следующая группа и human/release acceptance отдельно.
- Documentation impact: updated; docs/code-intelligence/queries-impact.md; docs/code-intelligence/queries-impact.en.md; docs/api/endpoints.md; docs/api/endpoints.en.md; docs/backend/modules.md; docs/backend/modules.en.md; docs/frontend/navigation.md; docs/frontend/navigation.en.md; docs/product/capabilities.md; docs/product/capabilities.en.md; scoped source checks passed.
