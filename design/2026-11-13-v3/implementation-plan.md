# План desktop UI/UX редизайна Product-Agent OS — V3

План хранится рядом с концепциями вне публикуемого MkDocs: дизайн утверждён владельцем; документ управляет локальным внедрением UI/UX, а не публикацией.

Source status: approved V3 + Sidebar collapse, 13.11.2026; UI-01–UI-12 reopened: V3 repair locally verified; UI-12 needs_user_acceptance; общий статус in_progress до приёмки. Владелец разрешил внедрение UI/UX, сохранение функциональных контрактов обязательно.


## Повторное открытие после визуального аудита

Текущий checkpoint: полный визуальный review85 экранов ×2 темы выполнен; финальная сборка, web500 и V3 browser378 passed. Повторно проверены все170 состояний. [Попарный альбом](implementation-gallery.html), [ledger](implementation-visual-review.json), [актуальные проверки и отличия](implementation-evidence.md). UI-01–UI-11 имеют локальное evidence; карточки остаются in_progress до разрешения отличий при приёмке, UI-12 не закрыт. Старые Completion Reports ниже не подменяют текущую сверку.

Предыдущие Completion Report ниже — исторические результаты первого внедрения, не доказательство visual parity. Владелец отклонил реализацию. Все UI-01–UI-12 переоткрыты 13.11.2026.

1. Shell: группы sidebar, header, локальная навигация, единый ритм.
2. Задачи: компактный список, инспектор 420px, полная форма в две колонки, полноэкранное окно и действия.
3. Settings/workflows: вертикальная навигация, формы и вложенные состояния с сохранением черновиков.
4. Dashboard/team/sessions/graph/artifacts/operations: перенос композиции, не подмена синтетикой.
5. Motion: source springs sidebar, tabs/panels/modal/reduced motion.
6. Сопоставить 87 записей coverage.json: продуктовые экраны отдельно от двух review labs; светлая и тёмная тема каждого доступного состояния, снимок + оценка композиции.
7. Регрессия существующих контрактов и обновление evidence. Приёмка владельца отдельно.

RED визуального аудита: title задачи в четырёхколоночном ряду, planning в пяти, create-agent button 63px; filters/settings/archive не на местах V3. Старые tests проверяли overflow/contrast, но не композицию.

## Scope

- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Owning design: [DESIGN.md](../../DESIGN.md)
- План отдельный от существующих M1–M5; их ID, статусы и зависимости не меняются.
- Владелец утвердил дизайн и разрешил UI-01–UI-12. Выполняется локальное frontend внедрение и synthetic verification. Приёмка результата реализации отдельно от утверждения макета.
- Функциональные non-goals: backend/API/schema/permissions/provider/queue semantics/новые продуктовые возможности. Только UI/UX, без мобильной версии.
- Оценки V1 108–182 ч архивные и не действуют для V3. Новый объём включает portfolio/agent dashboards, task overlay и два graph renderer; отдельные времена карточек не измерялись, календарное обещание не даётся.
- Rollback: own UI hunks по baseline каждого slice; без DB changes, git reset, deploy или удаления чужих правок.
- Проверка задачи включает текущее состояние исходников, current-build receipts и обязательные gates из TEST.md; число тестов заранее не обещается.

## Уточнение V2 — обязательное покрытие

Редакция V2 заменяет раннее сравнение A/B/C единым paired design Porcelain/Obsidian. Исходный план сохранён в `../2026-11-13/implementation-plan.md`; ID UI-01–UI-12 обозначают те же задачи внедрения, а не новую параллельную очередь. Статусы текущего внедрения принадлежат индексу и карточкам ниже.

- Канонический реестр макетов: [coverage.json](coverage.json). Для UI-01 каждый source-owned tab/action сопоставляется с actual app baseline; proposed organization не выдаётся за существующий route.
- UI-02/03: обе темы, 15 назначений, token parity, desktop 1280/1440/1920; review controls альбома не попадают в приложение.
- UI-04: список/доска; все 8 вкладок задачи; create/move/delete; components/versions/release policy/board/archive.
- UI-05/06: general/project/connection/shutdown; assignments, states, transitions, diagram/recipes, publication, migration, versions/archive; execution steps/recovery и queue.
- UI-07/08: оба уровня sessions, все tabs agents/skills и генерация, discovery/import, graph/list/node, document proposal/diff.
- UI-09: overview/checks/autonomy/decisions/search/import/backup со всеми preview/confirmation и receipt surfaces.
- UI-10/11: loading/empty/error/stale/disabled/dirty/confirmation/paused; keyboard/focus, контраст обеих тем, отсутствие root overflow. Проверить реальные HTTP outcomes; прототипная симуляция не переносится в production.
- UI-12: human approval экранами и сценариями отдельно от автоматической проверки.

Motion вводится в каждый UI-срез после проверки его реальных состояний; UI-10 — итоговая согласованность, не позднее украшение. Необходимые локальные frontend зависимости входят в разрешённое внедрение; версии и лицензии проверяются, глобальная установка не требуется. Функциональные расширения и публикация исключены. Оценка V1 108–182 ч остаётся историческим предварительным диапазоном; UI-01 должен переоценить объём после полного baseline утверждённого V3.

## Уточнение V3 — обязательные критерии шести доработок

V3 заменяет V2 как утверждённое направление; архив V2 неизменен. Карточки UI-01–UI-12 разрешены к внедрению. Выполненный прототип сам по себе не закрывает проверки приложения. [Полная карта полей](task-field-map.md), [исследование](research.md) и [coverage](coverage.json) уточняют следующие критерии:

| Карточка | Обязательная доработка V3 | Проверка при внедрении |
| --- | --- | --- |
| UI-01 | Разделить доступные исходные данные и предложенную аналитику; утвердить все экраны/оба режима | in_progress |
| UI-02 | Duoicons из icons0/Iconify, единая двухтонная геометрия и семантические цвета | in_progress |
| UI-03 | Общая среда всех проектов и явный вход в конкретный проект | in_progress |
| UI-04 | Полная task dialog по двойному клику + кнопка/Enter, все поля Editor и 8 вкладок | in_progress |
| UI-07 | Расход сессии/задачи с источником и неизвестными значениями | in_progress |
| UI-08 | Dashboard всех агентов и каждого; D3 graph + Mermaid whole/module + список | in_progress |
| UI-09 | Portfolio/project dashboards: прогресс, осталось, очередь, загрузка, расход | in_progress |
| UI-10 | GSAP lifecycle, reduced motion, локальные loading/feedback transitions | in_progress |
| UI-11 | Числовые инварианты, реальные renderer activation, все маршруты обеих тем | in_progress |
| UI-12 | Утверждение нового альбома и контракта будущей аналитики | in_progress |

Сбор токеномики требует отдельного функционального решения. Portfolio агрегирует существующие полные task snapshots в presentation layer. В UI-срезе сначала допускается честное unavailable-состояние. Настоящий сбор/хранение usage и цены провайдеров не входят в этот план. Исторические оценки V1/V2 не учитывают новый объём и должны быть пересмотрены в UI-01.

## Индекс

| ID | Задача | Зависимости | Архивная оценка V1 | Статус |
| --- | --- | --- | --- | --- |
| UI-01 | Выбор направления и фиксация baseline | none | baseline V3 | in_progress |
| UI-02 | Семантические tokens и библиотека элементов | UI-01 | 8–14 ч | in_progress |
| UI-03 | Shell, навигация и ширина контента | UI-01, UI-02 | 8–14 ч | in_progress |
| UI-04 | Задачи и панель объекта | UI-02, UI-03 | 12–20 ч | in_progress |
| UI-05 | Настройки и подключение | UI-02, UI-03 | 8–12 ч | in_progress |
| UI-06 | Процессы, переходы, миграция и очередь | UI-02, UI-03 | 14–22 ч | in_progress |
| UI-07 | Сессии и контекст выполнения | UI-02, UI-03 | 10–16 ч | in_progress |
| UI-08 | Каталоги ресурсов и карта проекта | UI-02, UI-03 | 10–18 ч | in_progress |
| UI-09 | Обзор, проверки, решения и служебные операции | UI-02, UI-03 | 10–16 ч | in_progress |
| UI-10 | Motion, состояния и доступность | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09 | 8–14 ч | in_progress |
| UI-11 | Регрессия контрактов и визуальная проверка | UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10 | 12–20 ч | in_progress |
| UI-12 | Приёмка дизайна и документация внедрения | UI-11 | 4–8 ч | in_progress |

## Подробные карточки

### Task `UI-01`

- Task: UI-01 — Выбор направления и фиксация baseline
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: none
- Blocks: UI-02, UI-03
- Source: DESIGN.md; App.tsx; TaskManager.tsx; WorkflowManager.tsx
- Short description: Зафиксировать утверждение V3/Sidebar; снять actual app baseline, карту действий/полей/источников данных и исходные checks. Все 87 prototype routes — образцы компоновки, не обещание новых backend routes.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: design/2026-11-13-v3/; apps/web/src/ (read-only baseline)
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Baseline screenshots; parity map в DESIGN.md
- Acceptance criteria: Все назначения/поля/подтверждения перечислены; viewport 1280/1440/1920 и узкое desktop окно; выбор владельца зафиксирован отдельно от технической проверки.
- Verification gates: Сверка исходников и before-captures; keyboard smoke на disposable fixture.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: product-manager + read-only explorer; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Baseline screenshots; parity map в DESIGN.md
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Утверждение V3/Sidebar зафиксировано; actual app baseline и источники данных сопоставлены.
- files touched / work locations: DESIGN.md; implementation-evidence.md; baseline browser/build/test logs
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Baseline build0; integration112; исходные sandbox errors сохранены, финальный full suite вне ограничения symlink500 passed. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-02`

- Task: UI-02 — Семантические tokens и библиотека элементов
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-01
- Blocks: UI-03, UI-04, UI-05, UI-06, UI-07
- Source: apps/web/src/design/theme.css; apps/web/package.json
- Short description: Перенести Porcelain/Obsidian tokens, compact controls, semantic statuses, Duoicons SVG, focus/error/loading primitives и локальную motion основу без изменения handlers.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/design/; presentation primitives под apps/web/src/ui/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Tokens, primitives, icon mapping, component specimens
- Acceptance criteria: Все цвета/fonts через tokens; 8 применимых control states; label/focus/error доступны; контраст текст4.5/UI3; существующие handlers сохранены.
- Verification gates: Component rendering, contrast checks, typecheck/build; зависимости только после локального review лицензий и решения владельца.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; reviewer read-only; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Tokens, primitives, icon mapping, component specimens
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Porcelain/Obsidian tokens, компактные controls, цветные local Duoicons, семантические состояния и SVG notices.
- files touched / work locations: apps/web/src/design/theme.css; workspace.css; ui/Icon.tsx; package.json; THIRD_PARTY_NOTICES.md
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Typecheck/build0; contrast desktop matrix; зависимости закреплены, npm audit0 vulnerabilities при установке. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-03`

- Task: UI-03 — Shell, навигация и ширина контента
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-01, UI-02
- Blocks: UI-04, UI-05, UI-07, UI-08, UI-09
- Source: App.tsx:77–92,220–267,341–397; design/app.css
- Short description: Внедрить Sidebar collapse 216↔64 с исходными springs 260/24,300/22,380/28,300/26, tooltip/keyboard/reduced motion, compact header, project switcher и вход во все проекты. Сохранить navigationEpoch и существующие deep links.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/ui/App.tsx; apps/web/src/design/app.css; apps/web/src/locales/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Shell и navigation presentation
- Acceptance criteria: Все 14 назначений доступны; проектный контекст сохраняется; нет root overflow; current/focus видимы; поведение narrow viewport не регрессирует.
- Verification gates: Source parity; bounding boxes/scrollWidth на 1024/1280/1440/1920; keyboard navigation; RU/EN labels; existing App tests.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Shell и navigation presentation
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: React Sidebar collapse 216↔64, исходные springs260/24,300/22,380/28,300/26; tooltip, reduced motion и все15 назначений; navigationEpoch сохранён.
- files touched / work locations: apps/web/src/ui/Sidebar.tsx; App.tsx; design/workspace.css
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Browser collapse/expand, keyboard tooltip/Escape, route persistence, reduced motion, desktop widths1280/1440/1920. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-04`

- Task: UI-04 — Задачи и панель объекта
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/TaskManager.tsx; Editor.tsx; Panels.tsx
- Short description: Сохранить все поля TaskEditor и 8 existing tabs; добавить task usage unavailable surface, dblclick/Enter/explicit full-card overlay с focus return. Не дублировать editors/commands; сохранить draft, filters, drag/drop, create/save/preview/move/delete guards.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/tasks/; task CSS; ui/TaskRelations.tsx; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Task workspace, detail panel, tab overflow
- Acceptance criteria: Сохранены 8 вкладок, filter/group/archive/attachments/links/comments; dirty data и scroll не теряются; move ведёт в прежний preview; длинные значения доступны целиком.
- Verification gates: Repro RED для overflow/утраты selection; scoped tests; task lifecycle browser; payload/revision parity; screenshot at all desktop sizes.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; tester по scenario ownership; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Task workspace, detail panel, tab overflow
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Единственный редактор задачи переключается в native modal по dblclick/Enter/кнопке; все8 вкладок/поля/guards и черновики сохранены.
- files touched / work locations: features/tasks/TaskManager.tsx; task-detail.css; ui/Modal.tsx
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: RED→GREEN task-overlay19; existing integration112; raw multiline/invalid estimate/unsaved title и тот же DOM подтверждены. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-05`

- Task: UI-05 — Настройки и подключение
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/tasks/Settings.tsx; ui/ConnectionControls.tsx; design/app.css
- Short description: Разделить Settings на общие/проекты/подключение/локальный сервис с сохранением форм, native folder flow, connection statuses и shutdown confirmation; процессы открыть в отдельной локальной панели.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/tasks/Settings.tsx; apps/web/src/ui/ConnectionControls.tsx; settings presentation; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Compact settings navigation, connection states
- Acceptance criteria: Native picker/Add/Cancel прежние; состояние соединения не имитируется; technical details доступны; Quit требует прежний checkbox; active BYOK state сохранён.
- Verification gates: Existing settings/connection tests; bounded fixture disconnected/waiting/connected/error; keyboard; Cancel no-mutation; screenshots.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Compact settings navigation, connection states
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Настройки разделены на Общие/Проекты/Подключение/Сервис/Процессы/Все; формы остаются mounted.
- files touched / work locations: ui/App.tsx; ui/settings-workspace.css
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: settings-layout14; клавиатурные local tabs, сохранность preference/project drafts, existing callbacks. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-06`

- Task: UI-06 — Процессы, переходы, миграция и очередь
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: WorkflowManager.tsx; recipes/RecipeRunner.tsx; recipes/QueueManager.tsx
- Short description: Компактный workbench состояний/переходов и панели assignments/recipes/publication/migration/version/archive/execution/queue; текущие preview digests, pinned versions, refresh-preserve-form и stop confirmations сохранить.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/workflows/; workflow CSS; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Transition workbench и compact execution views
- Acceptance criteria: Каждое исходное поле доступно; error раскрывает группу; draft сохранён; validate/preview/publish/migrate confirmations идентичны; все pinned IDs и required checks неизменны.
- Verification gates: Workflow/recipe/queue tests; keyboard editing; stale revision rejection; migration preview; fixture destructive confirmation; schematic/table parity.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; tester; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Transition workbench и compact execution views
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Workbench процесса: definition/publication/migration/versions/execution/queue, компактные state/transition rows, раскрытие invalid field; guards/preview/CAS прежние.
- files touched / work locations: features/workflows/WorkflowManager.tsx; workflow-workbench.css
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: settings-layout14 после исправления row opening; M2b51 сценарий с публикацией/миграцией passed. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-07`

- Task: UI-07 — Сессии и контекст выполнения
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/sessions/SessionsCatalog.tsx; ui/SessionContext.tsx; ui/Operations.tsx
- Short description: Сохранить каталоги работы/истории, transcript/context/changes/run/checks/questions/decision и composer/drafts; добавить контекст расхода сессии без вымышленных значений и новых backend calls.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/sessions/; apps/web/src/ui/SessionContext.tsx; ui/Operations.tsx; session CSS
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Session workbench и state specimens
- Acceptance criteria: Send/Stop и approvals видимы; terminal ACK не заменён анимацией; нет auto-send; selected session и draft сохранены; stale/disconnected отделены.
- Verification gates: Session tests; synthetic send/pending/stop/ACK/no-agent scenarios; long transcript/long path; keyboard focus; screenshot evidence.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; tester; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Session workbench и state specimens
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Компактные session catalog/transcript/composer/context grids и явное unavailable расхода; история, polling и draft lifecycle сохранены.
- files touched / work locations: features/sessions/SessionsCatalog.tsx; design/workspace.css
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Existing M2b51; все destinations RU/EN light/dark; session screenshots; общая web regression500. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-08`

- Task: UI-08 — Каталоги ресурсов и карта проекта
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: features/team/TeamManager.tsx; features/skills/SkillGenerator.tsx; features/graph/GraphExplorer.tsx; features/artifacts/ArtifactExplorer.tsx
- Short description: Перестроить agents/skills profiles/edit/history/activity, общий и персональный agent dashboard на existing metrics; documents reader/proposal/diff; D3 graph и Mermaid whole-available-page/module плюс список с общей revision/coverage и node IDs.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/features/team/; skills/; graph/; artifacts/; соответствующий CSS
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Resource catalogs, readable graph inspector
- Acceptance criteria: Source/staged/stale/unresolved видимы; graph сохраняет реальные типы связи и limits; исходник открывается прежним способом; текстовая альтернатива полна.
- Verification gates: Existing catalog/graph/artifact tests; exact fixture node-edge label comparison; keyboard graph/list; long paths; rendered contrast.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: graph-cockpit-engineer либо builder; reviewer read-only; один владелец записи на slice, независимый reviewer только read-only.
- Skills: data-visualization, ui-ux-pro-max
- Output artifacts: Resource catalogs, readable graph inspector
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Team/per-agent dashboards, existing catalog/profile actions, D3/strict Mermaid и list по общей revision-pinned странице; модульный фильтр, zoom/pan/reset.
- files touched / work locations: features/team/TeamManager.tsx; features/graph/GraphExplorer.tsx; GraphViews.tsx; diagram-source.ts; features/dashboard/
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: M2b51; M2c37; real renderer activation/node parity; unit escaping special labels; fresh review2 findings исправлены. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-09`

- Task: UI-09 — Обзор, проверки, решения и служебные операции
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-02, UI-03
- Blocks: UI-10, UI-11
- Source: ui/App.tsx; features/decisions/DecisionBoard.tsx; features/autonomy/AutonomyManager.tsx; existing search/import/backup surfaces
- Short description: Portfolio и project dashboard по существующим taskManager/teamMetrics/queue sources: прогресс, осталось, состояния, очередь, нагрузка. Usage unavailable там, где нет измерения. Сохранить Sources, checks, autonomy, decisions, search, import, backup и подтверждения.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/ui/App.tsx; decisions/; autonomy/; presentation components; locales
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Remaining sections visual parity
- Acceptance criteria: Все существующие действия доступны; no fake KPI; acceptance отдельно от test result; import/restore preview и confirmations сохранены; permissions unchanged.
- Verification gates: Existing decisions/autonomy/import/backup tests; expiry/stale/denied fixture states; keyboard; before/after action map; screenshots.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Remaining sections visual parity
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: Portfolio/project dashboards по taskManager/scheduler/teamMetrics; progress denominator, очередь, текущие назначения и observed runs. Остальные operational surfaces получили общие tokens/layout без handler changes.
- files touched / work locations: features/dashboard/Dashboard.tsx; model.ts; ui/App.tsx; design/workspace.css
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Dashboard invariants RED→GREEN5 focused tests вместе с diagram; no fabricated cost/tool_use; existing functional journeys. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-10`

- Task: UI-10 — Motion, состояния и доступность
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:40
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09
- Blocks: UI-11
- Source: DESIGN.md: движение, состояния, доступность; TEST.md existing a11y
- Short description: Согласовать motion и loading/empty/error/stale/disabled/dirty/confirmation/paused states, keyboard/focus/modal и reduced motion. Sidebar width spring — явное утверждённое исключение, прочая motion transform/opacity; очистка tween/rAF при unmount.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: apps/web/src/design/; affected presentation components; tests/web/accessibility/
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Motion tokens, state coverage, a11y repairs
- Acceptance criteria: No transition all; Sidebar width spring — утверждённое исключение; reduced-motion корректен; content readable without animation; tab order stable; hidden sections не прячут errors; нет auto-dismiss важных ошибок.
- Verification gates: Current-build contrast; RU/EN; light/dark only supported approved themes; keyboard/modal focus; browser zoom; reduced-motion screenshot; current a11y gates.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: builder для CSS; tester для независимых проверок; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max, data-visualization
- Output artifacts: Motion tokens, state coverage, a11y repairs
- Next step: Приёмка текущей реализации по попарному альбому и учёт отмеченных отличий; локальные проверки см. implementation-evidence.md.

#### Completion Report

- status: in_progress
- what was done: GSAP route heading transition с cleanup, native dialog motion, CSS state feedback/skeleton и reduced motion; exact sidebar springs остаются отдельным owner.
- files touched / work locations: ui/App.tsx; ui/Sidebar.tsx; design/workspace.css; task/settings/workflow CSS
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:40
- verification evidence: Browser reduced motion/collapse/focus; accessibility core136 checks20views; contrast issue4.428 исправлен на accent-text. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Приёмка реализации владельцем по UI-12.

### Task `UI-11`

- Task: UI-11 — Регрессия контрактов и визуальная проверка
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: 13-11-2026 17:47
- Depends on: UI-04, UI-05, UI-06, UI-07, UI-08, UI-09, UI-10
- Blocks: UI-12
- Source: TEST.md; EVALS.md; current Web tests and browser harnesses
- Short description: Проверить actual built application: baseline contract parity, RU/EN, две темы, desktop1280/1440/1920, root overflow, full task fields, sidebar, numeric source/coverage и реальные D3/Mermaid render. Synthetic isolated service, без provider calls.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: tests/web/; isolated fixture evidence; own UI repairs
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Regression receipts, visual captures, unresolved gaps
- Acceptance criteria: Ни один прежний API contract/permission/preview/draft flow не изменён; все нужные tests проходят; required gates не пропущены; screen evidence tied to current source.
- Verification gates: npm run check:web-m1; npm run build:web; node --test tests/web/*.test.mts; applicable synthetic browser/a11y gates из TEST.md; docs gates и diff check.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: high: сложные состояния и регрессионные риски
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: tester + reviewer (read-only assurance); builder для scoped fixes; один владелец записи на slice, независимый reviewer только read-only.
- Skills: ui-ux-pro-max, hallmark
- Output artifacts: Regression receipts, visual captures, unresolved gaps
- Next step: Приёмка реализации владельцем в UI-12.

#### Completion Report

- status: in_progress
- what was done: Integrated verification завершена: 500 web tests, 356 V3 browser checks, профильные suites и docs gates прошли. Неуспешные промежуточные receipts сохранены.
- files touched / work locations: tests/web/; implementation-evidence.md
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: 13-11-2026 17:47
- verification evidence: Full web500 passed; build/typecheck exit0; V3 356 checks/120 views, accessibility136, docs105/check_docs passed. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: UI-12: приёмка реализации владельцем.

### Task `UI-12`

- Task: UI-12 — Приёмка дизайна и документация внедрения
- Status: in_progress
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Многосрезовый desktop UI редизайн с functional parity и owner acceptance.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: UI-11
- Blocks: none
- Source: DESIGN.md; REQUIREMENTS.md; PLAN.md; TEST.md; RUNLOG.md
- Short description: Предъявить реализованные экраны и сценарии, обновить DESIGN/plan/evidence/control-plane; отдельно записать owner acceptance или awaiting acceptance, не объявлять пользовательскую приёмку по автоматическим тестам.
- Technical value: Единое представление существующих контрактов; управляемые UI boundaries и проверяемый откат.
- Product value: Меньше поиска и лишней прокрутки; понятные действия и результаты без изменения возможностей.
- Scope: DESIGN.md; control-plane pointers; owning implementation evidence
- Non-goals: Изменения backend/API/DB/permissions/model providers и бизнес-логики; mobile; публикация и Git actions.
- Expected result: Acceptance record, актуальный DESIGN, handoff
- Acceptance criteria: Owner feedback отдельно от automatic tests; результаты и gaps честны; функциональные расширения не скрыты в UI scope; ни deployment ни Git без запроса.
- Verification gates: Самопроверка/independent review отчёта; python -m unittest tests.product_agent_os.test_product_agent_os_docs -v; python tools/check_docs.py; git diff --check.
- Risks / approval gates: Дизайн и внедрение разрешены владельцем; не терять drafts и confirmations; при необходимости изменения контракта остановить конкретный slice. Необходимые UI-зависимости устанавливаются локально с закреплённой версией и проверкой лицензии; backend зависимости исключены.
- Complexity: medium: ограниченная presentation область с обязательной parity
- Estimated execution time: Архивная оценка V1 не применяется; отдельный wall time карточки недоступен, срезы выполнялись последовательно в общей сессии.
- Agents: product-manager + docs-maintainer; один владелец записи на slice, независимый reviewer только read-only.
- Skills: hallmark, ui-ux-pro-max
- Output artifacts: Acceptance record, актуальный DESIGN, handoff
- Next step: Завершить текущие gates и передать результат владельцу.

#### Completion Report

- status: in_progress
- what was done: Подготовлен handoff внедрения; дизайн уже утверждён, пользовательская приёмка реализации не подменяется automatic checks.
- files touched / work locations: DESIGN.md; implementation-plan.md; implementation-evidence.md; control-plane pointers
- technical value delivered: Presentation layer сохраняет существующие команды, версии, авторизацию и данные; отдельные frontend projections проверяемы.
- product value delivered: Компактная навигация и обозримая работа проекта; измерение пользовательской эффективности отдельно от реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Human implementation acceptance pending; UI-12 остаётся in_progress до решения владельца. Полные receipts: [implementation-evidence.md](implementation-evidence.md).
- residual risks: Human acceptance pending; unavailable telemetry не реализуется в UI; performance на больших реальных проектах не измерена.
- follow-up: Закрыть только после соответствующих gates/решения владельца.
