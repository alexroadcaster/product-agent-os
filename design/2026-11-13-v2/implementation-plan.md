# План desktop UI/UX редизайна Product-Agent OS — V2

План хранится рядом с концепциями вне публикуемого MkDocs: это предложение для выбора владельца, а не новая страница действующего руководства.

Source status: project-authored proposal, 13.11.2026; все задачи planned, реализация приложения не начата.

## Scope

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Owning design: [DESIGN.md](../../DESIGN.md)
- План отдельный от существующих M1–M5; их ID, статусы и зависимости не меняются.
- Разрешённый текущий этап: исследование, концепции и план. Карточки ниже описывают будущее внедрение после отдельного запроса.
- Функциональные non-goals: backend/API/schema/permissions/provider/queue semantics/новые продуктовые возможности. Только UI/UX, без мобильной версии.
- Оценки предварительные: 108–182 инженерных часа суммарно, последовательное исполнение; не календарное обещание. Пересмотреть после UI-01. Зависимости определяют порядок, а не разрешают автоматический запуск.
- Rollback: own UI hunks по baseline каждого slice; без DB changes, git reset, deploy или удаления чужих правок.
- Проверка задачи включает текущее состояние исходников, current-build receipts и обязательные gates из TEST.md; число тестов заранее не обещается.

## Уточнение V2 — обязательное покрытие

Редакция V2 заменяет раннее сравнение A/B/C единым paired design Porcelain/Obsidian. Исходный план сохранён в `../2026-11-13/implementation-plan.md`; ID UI-01–UI-12 обозначают те же будущие задачи, а не новую параллельную очередь. Все карточки остаются planned.

- Канонический реестр макетов: [coverage.json](coverage.json). Для UI-01 каждый source-owned tab/action сопоставляется с actual app baseline; proposed organization не выдаётся за существующий route.
- UI-02/03: обе темы, 14 назначений, token parity, desktop 1280/1440/1920; review controls альбома не попадают в приложение.
- UI-04: список/доска; все 8 вкладок задачи; create/move/delete; components/versions/release policy/board/archive.
- UI-05/06: general/project/connection/shutdown; assignments, states, transitions, diagram/recipes, publication, migration, versions/archive; execution steps/recovery и queue.
- UI-07/08: оба уровня sessions, все tabs agents/skills и генерация, discovery/import, graph/list/node, document proposal/diff.
- UI-09: overview/checks/autonomy/decisions/search/import/backup со всеми preview/confirmation и receipt surfaces.
- UI-10/11: loading/empty/error/stale/disabled/dirty/confirmation/paused; keyboard/focus, контраст обеих тем, отсутствие root overflow. Проверить реальные HTTP outcomes; прототипная симуляция не переносится в production.
- UI-12: human approval экранами и сценариями отдельно от автоматической проверки.

Motion вводится в каждый UI-срез после проверки его реальных состояний; UI-10 — итоговая согласованность, не позднее украшение. Установка новых зависимостей, функциональные расширения и публикация не разрешаются этой матрицей. Оценка V1 108–182 ч остаётся историческим предварительным диапазоном; UI-01 должен переоценить объём после полного baseline и утверждения V2.

## Индекс

| ID | Задача | Зависимости | Оценка | Статус |
| --- | --- | --- | --- | --- |
| UI-01 | Выбор направления и фиксация baseline | none | 4–8 ч | planned |
| UI-02 | Семантические tokens и библиотека элементов | UI-01 | 8–14 ч | planned |
| UI-03 | Shell, навигация и ширина контента | UI-01, UI-02 | 8–14 ч | planned |
| UI-04 | Задачи и панель объекта | UI-02, UI-03 | 12–20 ч | planned |
| UI-05 | Настройки и подключение | UI-02, UI-03 | 8–12 ч | planned |
| UI-06 | Процессы, переходы, миграция и очередь | UI-02, UI-03 | 14–22 ч | planned |
| UI-07 | Сессии и контекст выполнения | UI-02, UI-03 | 10–16 ч | planned |
| UI-08 | Каталоги ресурсов и карта проекта | UI-02, UI-03 | 10–18 ч | planned |
| UI-09 | Обзор, проверки, решения и служебные операции | UI-02, UI-03 | 10–16 ч | planned |
| UI-10 | Motion, состояния и доступность | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09 | 8–14 ч | planned |
| UI-11 | Регрессия контрактов и визуальная проверка | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10 | 12–20 ч | planned |
| UI-12 | Приёмка дизайна и документация внедрения | UI-11 | 4–8 ч | planned |

## Подробные карточки

### Task `UI-01`

- Task: UI-01 — Выбор направления и фиксация baseline
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: none
- Blocks: UI-02, UI-03
- Source: DESIGN.md; App.tsx; TaskManager.tsx; WorkflowManager.tsx
- Short description: Согласовать paired Porcelain/Obsidian и полный каталог V2; снять до-кадры всех 14 разделов и состояний; составить parity map существующих действий и 8 вкладок задачи.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: design/2026-11-13-v2/; apps/web/src/ (read-only baseline)
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Baseline screenshots; parity map в DESIGN.md
- Acceptance criteria: Все назначения/поля/подтверждения перечислены; viewport 1280/1440/1920 и узкое desktop окно; выбор владельца зафиксирован отдельно от технической проверки.
- Verification gates: Сверка исходников и before-captures; keyboard smoke на disposable fixture.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 4–8 ч; предварительная оценка, без ожидания решения владельца.
- Agents: product-manager + read-only explorer; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Baseline screenshots; parity map в DESIGN.md
- Next step: Предъявить обе темы, все screen IDs и motion lab владельцу.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Предъявить обе темы, все screen IDs и motion lab владельцу.

### Task `UI-02`

- Task: UI-02 — Семантические tokens и библиотека элементов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-01
- Blocks: UI-03, UI-04, UI-05, UI-06, UI-07
- Source: apps/web/src/design/theme.css; apps/web/package.json
- Short description: Создать выбранную palette/type/spacing/radius/motion шкалу, общие button/input/select/badge/alert/tooltip wrappers; единый набор SVG.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/design/; presentation primitives под apps/web/src/ui/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Tokens, primitives, icon mapping, component specimens
- Acceptance criteria: Все цвета/fonts через tokens; 8 применимых control states; label/focus/error доступны; контраст текст4.5/UI3; существующие handlers сохранены.
- Verification gates: Component rendering, contrast checks, typecheck/build; зависимости только после локального review лицензий и решения владельца.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 8–14 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; reviewer read-only; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Tokens, primitives, icon mapping, component specimens
- Next step: Зафиксировать выбранную тему и package decision до установки.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Зафиксировать выбранную тему и package decision до установки.

### Task `UI-03`

- Task: UI-03 — Shell, навигация и ширина контента
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-01, UI-02
- Blocks: UI-04, UI-05, UI-07, UI-08, UI-09
- Source: App.tsx:77–92,220–267,341–397; design/app.css
- Short description: Сгруппировать 14 назначений, добавить иконки, compact header, project switcher; определить responsive desktop grid и путь для inspector.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/ui/App.tsx; apps/web/src/design/app.css; apps/web/src/locales/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Shell и navigation presentation
- Acceptance criteria: Все 14 назначений доступны; проектный контекст сохраняется; нет root overflow; current/focus видимы; поведение narrow viewport не регрессирует.
- Verification gates: Source parity; bounding boxes/scrollWidth на 1024/1280/1440/1920; keyboard navigation; RU/EN labels; existing App tests.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 8–14 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Shell и navigation presentation
- Next step: Воспроизвести overflow на baseline, затем минимальный исправляющий UI slice.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Воспроизвести overflow на baseline, затем минимальный исправляющий UI slice.

### Task `UI-04`

- Task: UI-04 — Задачи и панель объекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/TaskManager.tsx; Editor.tsx; Panels.tsx
- Short description: Compact list/board и inspector; 8 вкладок с отдельным содержимым; create/move/delete и task settings panels по coverage.json; сохранить текущие parent links.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/tasks/; task CSS; ui/TaskRelations.tsx; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Task workspace, detail panel, tab overflow
- Acceptance criteria: Сохранены 8 вкладок, filter/group/archive/attachments/links/comments; dirty data и scroll не теряются; move ведёт в прежний preview; длинные значения доступны целиком.
- Verification gates: Repro RED для overflow/утраты selection; scoped tests; task lifecycle browser; payload/revision parity; screenshot at all desktop sizes.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: 12–20 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; tester по scenario ownership; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Task workspace, detail panel, tab overflow
- Next step: Сделать один вертикальный срез list → detail → existing edit/preview.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Сделать один вертикальный срез list → detail → existing edit/preview.

### Task `UI-05`

- Task: UI-05 — Настройки и подключение
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/Settings.tsx; ui/ConnectionControls.tsx; design/app.css
- Short description: Разделить settings на короткие локальные панели: общие, проекты, подключение, локальный сервис; вынести большие формы процессов из общего полотна.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/tasks/Settings.tsx; apps/web/src/ui/ConnectionControls.tsx; settings presentation; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Compact settings navigation, connection states
- Acceptance criteria: Native picker/Add/Cancel прежние; состояние соединения не имитируется; technical details доступны; Quit требует прежний checkbox; active BYOK state сохранён.
- Verification gates: Existing settings/connection tests; bounded fixture disconnected/waiting/connected/error; keyboard; Cancel no-mutation; screenshots.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 8–12 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Compact settings navigation, connection states
- Next step: Сохранить owning state на переключении local settings panel.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Сохранить owning state на переключении local settings panel.

### Task `UI-06`

- Task: UI-06 — Процессы, переходы, миграция и очередь
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: WorkflowManager.tsx; recipes/RecipeRunner.tsx; recipes/QueueManager.tsx
- Short description: Список состояний/переходов плюс selected editor; отдельные вкладки assignments/recipes/version/migration; execution/queue подпанель.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/workflows/; workflow CSS; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Transition workbench и compact execution views
- Acceptance criteria: Каждое исходное поле доступно; error раскрывает группу; draft сохранён; validate/preview/publish/migrate confirmations идентичны; все pinned IDs и required checks неизменны.
- Verification gates: Workflow/recipe/queue tests; keyboard editing; stale revision rejection; migration preview; fixture destructive confirmation; schematic/table parity.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: 14–22 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; tester; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Transition workbench и compact execution views
- Next step: Сначала заменить только вывод transition map, сохранив state и command functions.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Сначала заменить только вывод transition map, сохранив state и command functions.

### Task `UI-07`

- Task: UI-07 — Сессии и контекст выполнения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/sessions/SessionsCatalog.tsx; ui/SessionContext.tsx; ui/Operations.tsx
- Short description: Работа/Полная доступная история и Чат/Контекст/Изменения; центральный transcript, run profile/checks/questions/decision; компактные events, стабильный composer.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/sessions/; apps/web/src/ui/SessionContext.tsx; ui/Operations.tsx; session CSS
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Session workbench и state specimens
- Acceptance criteria: Send/Stop и approvals видимы; terminal ACK не заменён анимацией; нет auto-send; selected session и draft сохранены; stale/disconnected отделены.
- Verification gates: Session tests; synthetic send/pending/stop/ACK/no-agent scenarios; long transcript/long path; keyboard focus; screenshot evidence.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: 10–16 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; tester; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Session workbench и state specimens
- Next step: Проверить existing polling/scroll behavior, не менять transport.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Проверить existing polling/scroll behavior, не менять transport.

### Task `UI-08`

- Task: UI-08 — Каталоги ресурсов и карта проекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/team/TeamManager.tsx; features/skills/SkillGenerator.tsx; features/graph/GraphExplorer.tsx; features/artifacts/ArtifactExplorer.tsx
- Short description: Agents и skills: все Profile/Edit/History/Activity; генерация и discovery/import; documents reader/proposal/diff; graph/list/node с source/occurrences/related tasks.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/team/; skills/; graph/; artifacts/; соответствующий CSS
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Resource catalogs, readable graph inspector
- Acceptance criteria: Source/staged/stale/unresolved видимы; graph сохраняет реальные типы связи и limits; исходник открывается прежним способом; текстовая альтернатива полна.
- Verification gates: Existing catalog/graph/artifact tests; exact fixture node-edge label comparison; keyboard graph/list; long paths; rendered contrast.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 10–18 ч; предварительная оценка, без ожидания решения владельца.
- Agents: graph-cockpit-engineer либо builder; reviewer read-only; один владелец записи на slice, независимый reviewer только read-only.
- Skills: data-visualization, ui-ux-pro-max
- Output artifacts: Resource catalogs, readable graph inspector
- Next step: Использовать существующий SVG/DOM renderer до выбора новых зависимостей.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Использовать существующий SVG/DOM renderer до выбора новых зависимостей.

### Task `UI-09`

- Task: UI-09 — Обзор, проверки, решения и служебные операции
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: ui/App.tsx; features/decisions/DecisionBoard.tsx; features/autonomy/AutonomyManager.tsx; existing search/import/backup surfaces
- Short description: Объединить visual patterns обзора, проверки, autonomy, decisions, search, import и backup; dangerous/review actions вынести из primary content.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/ui/App.tsx; decisions/; autonomy/; presentation components; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Remaining sections visual parity
- Acceptance criteria: Все существующие действия доступны; no fake KPI; acceptance отдельно от test result; import/restore preview и confirmations сохранены; permissions unchanged.
- Verification gates: Existing decisions/autonomy/import/backup tests; expiry/stale/denied fixture states; keyboard; before/after action map; screenshots.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 10–16 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Remaining sections visual parity
- Next step: Взять список действий из UI-01, обновлять по одному разделу.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Взять список действий из UI-01, обновлять по одному разделу.

### Task `UI-10`

- Task: UI-10 — Motion, состояния и доступность
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09
- Blocks: UI-11
- Source: DESIGN.md: движение, состояния, доступность; TEST.md existing a11y
- Short description: Согласовать уже встроенные по срезам micro-interactions: 100–240ms, skeleton/refresh/progress, result/error/stale/empty, focus/keyboard/modal, reduced motion; убрать layout shift и ложный success.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/design/; affected presentation components; tests/web/accessibility/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Motion tokens, state coverage, a11y repairs
- Acceptance criteria: No transition all/layout property animation; reduced-motion корректен; content readable without animation; tab order stable; hidden sections не прячут errors; нет auto-dismiss важных ошибок.
- Verification gates: Current-build contrast; RU/EN; light/dark only supported approved themes; keyboard/modal focus; browser zoom; reduced-motion screenshot; current a11y gates.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 8–14 ч; предварительная оценка, без ожидания решения владельца.
- Agents: builder для CSS; tester для независимых проверок; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Motion tokens, state coverage, a11y repairs
- Next step: Проверить общий component layer до локальных исключений.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Проверить общий component layer до локальных исключений.

### Task `UI-11`

- Task: UI-11 — Регрессия контрактов и визуальная проверка
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10
- Blocks: UI-12
- Source: TEST.md; EVALS.md; current Web tests and browser harnesses
- Short description: Сравнить функциональную parity с baseline; измерить overflow и layout states на финальном build; закрыть реальные дефекты.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: tests/web/; isolated fixture evidence; own UI repairs
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Regression receipts, visual captures, unresolved gaps
- Acceptance criteria: Ни один прежний API contract/permission/preview/draft flow не изменён; все нужные tests проходят; required gates не пропущены; screen evidence tied to current source.
- Verification gates: npm run check:web-m1; npm run build:web; node --test tests/web/*.test.mts; applicable synthetic browser/a11y gates из TEST.md; docs gates и diff check.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: 12–20 ч; предварительная оценка, без ожидания решения владельца.
- Agents: tester + reviewer (read-only assurance); builder для scoped fixes; один владелец записи на slice, независимый reviewer только read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Regression receipts, visual captures, unresolved gaps
- Next step: Запустить focused gates, затем required integrated suite один раз на итоговом состоянии.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Запустить focused gates, затем required integrated suite один раз на итоговом состоянии.

### Task `UI-12`

- Task: UI-12 — Приёмка дизайна и документация внедрения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-11
- Blocks: none
- Source: DESIGN.md; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md
- Short description: Провести просмотр полного каталога в обеих темах и owner-сценарии задач/процессов/сессий/импорта/backup; сверить качество с выбранной концепцией; записать limits, откат и следующий шаг.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: DESIGN.md; control-plane pointers; owning implementation evidence
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Acceptance record, актуальный DESIGN, handoff
- Acceptance criteria: Owner feedback отдельно от automatic tests; результаты и gaps честны; функциональные расширения не скрыты в UI scope; ни deployment ни Git без запроса.
- Verification gates: Самопроверка/independent review отчёта; python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; python tools/check_docs.py; git diff --check.
- Risks / approval gates: Выбор направления и отдельный запрос на внедрение; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Новая зависимость требует проверки лицензии и отдельного разрешения на установку.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: 4–8 ч; предварительная оценка, без ожидания решения владельца.
- Agents: product-manager + docs-maintainer; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Acceptance record, актуальный DESIGN, handoff
- Next step: Предъявить финальные изображения и рабочие сценарии владельцу.

#### Completion Report

- status: planned
- what was done: Описан будущий scope и acceptance; работа по внедрению этой карточки не выполнена.
- files touched / work locations: Только эта плановая карточка; целевые implementation files пока не изменены в рамках плана.
- technical value delivered: Контракт будущего среза; runtime результат отсутствует.
- product value delivered: Обозначен проверяемый UX outcome; улучшение ещё не измерено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Требуемые будущие проверки перечислены в Verification gates; результат выполнения карточки отсутствует.
- residual risks: Выбор владельца, детали baseline и регрессионные эффекты ещё предстоит проверить.
- follow-up: Предъявить финальные изображения и рабочие сценарии владельцу.


