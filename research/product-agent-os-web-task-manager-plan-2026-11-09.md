# Product-Agent OS Web — план полноценного Task Manager

Source status: project-authored / proposed / requirements-backed. Дата: 2026-11-09.

Статус: **draft_for_review**. Это очередь будущей реализации, не разрешение начать разработку. Все 38 задач имеют статус planned; фактическое время отсутствует. Пользовательский scope расширен относительно read-only M1. Исходные M1–M3 сохраняются как история; при расхождении приоритет имеет дополнение Task Manager в PRD и этот план.

Связи: [PRD](product-agent-os-web-prd-2026-11-05.md), [архитектура](product-agent-os-web-architecture-2026-11-05.md), [экраны](product-agent-os-web-task-manager-screens-2026-11-09.md), [машинные группы](product-agent-os-web-task-manager-task-group-2026-11-09.json).

## Протокол документационной задачи PAOS-WEB-TASK-MANAGER-2026-11-09

Это evidence подготовки документов и изображений. Не является Completion Report ни одной будущей карточки PAOS-0001–0030. Все implementation statuses остаются planned.

| Проверка текущего запуска | Наблюдаемый результат |
| --- | --- |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | Exit 0; 100 tests, OK |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0; ok=true, errors=[] |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-task-manager/site` | Exit 0 после исправления research pointers; Documentation built in 16.28 seconds. Research pages вне docs_dir не становятся опубликованными страницами; Mermaid source проверен чтением, browser rendering не проверен |
| `git diff --check` | Exit 0 после удаления добавленных пустых строк в конце трёх Web MD; CRLF warnings не являются whitespace errors |
| `python -`, bounded inline artifact checker | 30 уникальных IDs, 8 групп без пропусков, полный набор полей, все planned/actual=null, DAG без циклов, TM-01–14, 24 экрана, local links/UTF-8 и шесть PNG прошли |
| Hallmark finish review | separate_fresh_context, agent hallmark_review; verdict fix; один пакет исправлений пяти листов; последующий self-review корневого агента по returned images |
| Изображения | 6 PNG, 24 композиции, 1536×1024 каждый; final hashes в assets/task-manager-2026-11-09/manifest.json |

Первый запуск task-matrix validator отверг Markdown bold вокруг имён полей; приведено к каноническому формату. Первый strict MkDocs остановился на четырёх EN registry ссылках за docs_dir; заменены на source-path notation в обоих реестрах. Это исправления документации; validators/hooks не ослаблялись.

Review исправления: read-only discovery S02; единый основной пример PAOS-0001; agent IDs вместо придуманных людей; список/доска и вкладки task; честный coverage сессии; proposal vs apply; незаполненная policy не разрешает запуск; тёмная EN Settings соответствует выбранной теме. Адаптация Rim названа явно.

Остаточные visual gaps: image generation допускает неточные мелкие labels, gloss и отличия secondary fixtures между листами; в S18 рисунок не является нормативной схемой symbol identity (повторяющийся label status не задаёт два реальных символа). Использовать контракт graph из архитектуры и данные плана, а не считывать seed data из картинок. Mobile/keyboard/error/loading layouts описаны текстом, но отдельные изображения этих состояний не изготовлены. Все 24 основные экранные композиции присутствуют. pixel-perfect/contrast/a11y/render acceptance не заявляется.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG updated только собственными компактными pointers; source registry RU/EN updated. prod_test not_applicable (историческая серия не затронута). Другие PAOS-AUD изменения сохранены. Все пять root control-plane файлов остаются в пределах 50 KiB. Application source, runtime/host configuration, hooks, provider connections, Git history и публикация вне scope.

Итог подготовки: docs_static_verified; визуальный пакет draft_for_review / needs_user_acceptance; implementation not_started. Следующий шаг — выбрать/скорректировать визуальное направление и отдельно разрешить первую группу реализации. Архитектурные integration gaps относятся к PAOS-0001.

## Этапы и группы

## Проверка расширения v0.3 — PAOS-WEB-ISSUE-WORKFLOWS-2026-11-09

Source status: current-run local evidence. Это проверка документов, не реализация PAOS-0001–0038. Previous v0.2 receipts выше остаются историческими.

| Проверка | Наблюдаемый результат текущего запуска |
| --- | --- |
| `python plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` | Exit 0; ok=true; errors=[] |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | 105 tests, OK, exit 0 при process-local TEMP/TMP = workspace .docs-tools/reports/web-task-manager/test-temp |
| Первоначальный docs unittest | 105 tests, 5 errors: sandbox temporary directory PermissionError; после переноса TEMP/TMP в writable workspace повтор прошёл. Код/права ОС/тесты не менялись |
| `python tools/check_docs.py` | Exit 0; documentation structure checks passed |
| Bounded inline `python -` consistency check | 38 уникальных карточек, 10 групп, DAG, reverse Blocks, JSON/MD fields, TM-01–24, 11 components, 8 statuses, local links/UTF-8, root budget; все actual values null; PNG hashes прежние |
| `git diff --check` | Промежуточный exit 0 после исправления своего EOF; финальный общий запуск exit 2 на новом чужом EOF в research/product-agent-os-audit-remediation-task-plan-2026-11-09.md:2197. Scoped запуск с 12 собственными docs paths: exit 0; чужой план не исправлялся |
| `.venv-docs/Scripts/python.exe -m mkdocs build --strict --site-dir .docs-tools/reports/web-task-manager/site-v03` | **Exit 1**: два warnings в прежних G6 разделах docs/product-agent-os/control-plane-current-state.en.md и docs/sources/registry.en.md; ссылка ../superpowers/specs/paos-aud-g6-pilot-results.json не найдена среди documentation files. Сам файл существует; причина его отсутствия в build index в этом scope не исправлялась |
| Source review | 13 официальных Atlassian reference pages; facts отделены от PAOS proposals в PRD §14. Community/API assumptions не использованы |
| Self-review | Проверены hierarchy vs links, affects vs fix, status vs resolution, creator vs initiator, manual completion, cancellation receipt, workflow pinning/migration, dependency cycles, comments/history и attachment boundaries |

Изменённые owning artifacts: PRD §14, plan/JSON, architecture §18, UX v0.3 impact; компактные собственные sections REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG и registry RU/EN. Прежние 24 image concepts сохранены; S25/S26 описаны текстом, итог — 26 routes. Sources/metadata поддерживают proposed поведение; browser/runtime/provider evidence не выполнялись.

Control-plane sync: пять root files update_required и обновлены в своём scope; prod_test not_applicable; source registries RU/EN updated. Root files <50 KiB на момент проверки. Handoff_required: владелец PAOS-AUD-G6 должен устранить два существовавших G6 link warnings; наша задача не переписывает его разделы. Незакрытый strict-build gate не объявлен accepted gap и не скрыт.

Completion ceiling: **documentation_updated / partially_verified**. Requested content сохранён; документационные unit/structure/plan/consistency checks passed; общий strict build остаётся failed по указанным внешним для slice ссылкам. Реализация Web not_started; все 38 implementation tasks planned. Product/domain owner acceptance и runtime проверки будущие. Общий requirements_ready/plan_ready/release-ready не заявляется.


### Актуальная очередь v0.3

Актуализация v0.3: 38 задач, 10 групп. Исходные PAOS-0001–0030 сохранены; PAOS-0031–0038 добавляют Jira-informed issue model. Предыдущий протокол выше относится к пакету v0.2 и не является проверкой этого расширения.

| Группа | Содержание | Задачи |
| --- | --- | --- |
| G01 | Основа и контракты | PAOS-0001, PAOS-0002, PAOS-0003, PAOS-0004 |
| G02 | Задачи | PAOS-0005, PAOS-0006, PAOS-0007, PAOS-0008 |
| G03 | Сессии | PAOS-0009, PAOS-0010, PAOS-0011 |
| G04 | Агенты | PAOS-0012, PAOS-0013, PAOS-0014, PAOS-0015 |
| G05 | Скиллы | PAOS-0016, PAOS-0017, PAOS-0018, PAOS-0019 |
| G06 | Карта проекта | PAOS-0020, PAOS-0021, PAOS-0022 |
| G07 | Автономная работа | PAOS-0023, PAOS-0024, PAOS-0025, PAOS-0026 |
| G08 | Общие поверхности и пилот | PAOS-0027, PAOS-0028, PAOS-0029, PAOS-0030 |
| G09 | Иерархия, поля и контекст | PAOS-0031, PAOS-0032, PAOS-0033, PAOS-0034 |
| G10 | Kanban, workflow и взаимозависимости | PAOS-0035, PAOS-0036, PAOS-0037, PAOS-0038 |

TM0: G01 и контракты PAOS-0031/0032. TM1: основной UI G02–G06, контекст/версии G09, Kanban PAOS-0035 и документы PAOS-0027. TM2: управляемые agent/skill changes, editor/versioning workflow PAOS-0036. TM3: execution recipes PAOS-0037, links PAOS-0038 и автономность G07. TM4: G08 проверяет весь путь и пилот. Это roadmap; индивидуальные Depends on имеют приоритет над порядком номеров и групп.

Shared contracts: один writer. Иерархия/поля G09 публикуют contract до потребляющего UI; recipes/links G10 до scheduler G07; G08 принимает итоговый контракт. Предлагаемые apps/web, apps/local-service, packages/contracts не означают существующие файлы. PAOS-0001 уточняет точки интеграции до кода.

Оценки — предварительные часы инженерной работы, не календарное обещание и не измеренная скорость AI. Обновлены оценки PAOS-0002/0005/0006/0008/0028 из-за нового scope; прежние версии сохраняются Git/source history. Actual timestamps/duration всех задач null. Development not_started. Ни одна карточка не разрешает внешние вызовы, установку или публикацию.

Изменение scope: PRD §14 — источник требований TM-15–TM-24; G01/G02/G07/G08 адаптированы, G09/G10 добавлены. Статусы карточек плана planned не мигрируют в пользовательский Kanban. В JSON issue_model_proposal — предложение будущей модели, не активная runtime schema. Неизвестные legacy creators/dates/versions не выдумываются.

Rollback будущих изменений: versioned proposal, revision check, migration preview и сохранение источника. Rollback текущих документов — только hunks этого scope, без потери предыдущих концептов и чужих изменений.

## Проверка плана и условия старта

Документы проверяются существующими docs gates и validate_task_matrix.py. Для будущей реализации каждая карточка требует source discovery, подтверждения файлов, executable acceptance tests и доступности зависимостей. Команды build/E2E фиксируются в PAOS-0001 после выбора scaffolding; сейчас plan_ready для разработки не заявляется. Rollback будущих записей: versioned proposal, source revision check, сохранение предыдущей версии; rollback документации — только изменения этого scope.


### Task `PAOS-0001`

- Task: Контракты и адаптеры проекта
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: none
- Blocks: PAOS-0002, PAOS-0004, PAOS-0009, PAOS-0016, PAOS-0020
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Установить доступность источников и API установленного host; определить project binding и coverage
- Technical value: Установить доступность источников и API установленного host; определить project binding и coverage
- Product value: Пользователь сразу видит, какие сведения проекта доступны, и не принимает неполную историю за полную.
- Scope: apps/local-service/src/adapters; packages/contracts
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Контракты и адаптеры проекта доступна в соответствующем этапе
- Acceptance criteria: Подключённый проект показывает доступные и отсутствующие источники; чужой проект исключён
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/adapters; packages/contracts
- Next step: Проверить источники и контракт адаптеров
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0002`

- Task: Модель задачи и идентификаторы
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001
- Blocks: PAOS-0003, PAOS-0005, PAOS-0006, PAOS-0031
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Контракт прежних 12 и дополнительных полей §14 PRD; отдельные product status и planning status
- Technical value: Единый контракт всех полей задачи, стабильные ID и миграция старых записей
- Product value: Пользователь ставит полную задачу один раз и сохраняет устойчивую ссылку на неё при изменениях проекта.
- Scope: packages/contracts/tasks; apps/local-service/src/tasks
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Модель задачи и идентификаторы доступна в соответствующем этапе
- Acceptance criteria: Все поля §13–§14 проходят round-trip; стабильные ID; creator provenance; product workflow status не подменяет task_matrix_plan_v1 status
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: packages/contracts/tasks; apps/local-service/src/tasks
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0003`

- Task: Время и журнал событий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0002
- Blocks: PAOS-0006, PAOS-0015
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Оценка до старта, идемпотентные интервалы и измерение факта
- Technical value: Оценка до старта, идемпотентные интервалы и измерение факта
- Product value: Пользователь сравнивает ожидаемое и затраченное время без двойного учёта параллельной работы.
- Scope: apps/local-service/src/events; packages/contracts/time
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Время и журнал событий доступна в соответствующем этапе
- Acceptance criteria: Повтор события не удваивает время; pause/retry/crash и параллельные агенты не искажают длительность
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/events; packages/contracts/time
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0004`

- Task: Темы и локализация
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001
- Blocks: PAOS-0005, PAOS-0006, PAOS-0009, PAOS-0016, PAOS-0021, PAOS-0032
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Общие токены и RU/EN для всех экранов
- Technical value: Общие токены и RU/EN для всех экранов
- Product value: Пользователь работает на удобном языке и в выбранной теме без потери читаемости и действий.
- Scope: apps/web/src/design; apps/web/src/locales
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Темы и локализация доступна в соответствующем этапе
- Acceptance criteria: Переключатели сохраняют выбор; длинный EN/RU текст и обе темы не скрывают действия
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/design; apps/web/src/locales
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0005`

- Task: Список и доска задач
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0002, PAOS-0004, PAOS-0032
- Blocks: PAOS-0035
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Фильтры, группировка, сохранённый вид и доступная смена статуса
- Technical value: Фильтры, группировка, сохранённый вид и доступная смена статуса
- Product value: Пользователь быстро находит нужную работу и видит, на каком этапе находится каждая задача.
- Scope: apps/web/src/features/tasks/list; apps/web/src/features/tasks/board
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Список и доска задач доступна в соответствующем этапе
- Acceptance criteria: Список/Kanban согласованы; type/parent/creator/priority/components/versions/dates filters сохраняются; расширенные mappings и transitions проверяются в PAOS-0035
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/tasks/list; apps/web/src/features/tasks/board
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0006`

- Task: Карточка и редактор задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0002, PAOS-0003, PAOS-0004, PAOS-0032
- Blocks: PAOS-0007, PAOS-0008
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Полная постановка задачи и понятная техническая/продуктовая ценность
- Technical value: Полная постановка задачи и понятная техническая/продуктовая ценность
- Product value: Пользователь понимает пользу задачи, формулирует ожидаемый результат и управляет её выполнением.
- Scope: apps/web/src/features/tasks/detail; apps/web/src/features/tasks/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Карточка и редактор задачи доступна в соответствующем этапе
- Acceptance criteria: Все поля §13–§14 доступны; пользователь создаёт draft сам; отдельные Comments/History/Attachments/Linked Issues подключаются через PAOS-0034/0038; Ready проверяет обязательные поля
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/tasks/detail; apps/web/src/features/tasks/editor
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0007`

- Task: Файлы, артефакты и исполнители
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0006
- Blocks: PAOS-0008, PAOS-0010, PAOS-0012, PAOS-0022, PAOS-0027, PAOS-0034, PAOS-0038
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Связать планируемые/фактические изменения, агентские runs и доказательства
- Technical value: Связать планируемые/фактические изменения, агентские runs и доказательства
- Product value: Пользователь видит, кто и что изменит, и открывает подтверждающий документ из задачи.
- Scope: apps/local-service/src/task-links; apps/web/src/features/tasks/links
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Файлы, артефакты и исполнители доступна в соответствующем этапе
- Acceptance criteria: Создание/изменение/удаление различимы; ссылка открывает нужную версию и контекст
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/task-links; apps/web/src/features/tasks/links
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0008`

- Task: Приёмка и жизненный цикл
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0006, PAOS-0007
- Blocks: PAOS-0023, PAOS-0027, PAOS-0035
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверки и решение пользователя определяют завершение
- Technical value: Проверки и решение пользователя определяют завершение
- Product value: Пользователь принимает результат по проверяемым условиям и видит незакрытые требования.
- Scope: apps/local-service/src/task-workflow; apps/web/src/features/tasks/acceptance
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Приёмка и жизненный цикл доступна в соответствующем этапе
- Acceptance criteria: Completion, cancellation и reopening различены; criteria/child/dependency gates и manual evidence определены; действия расширяются PAOS-0035
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/task-workflow; apps/web/src/features/tasks/acceptance
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0009`

- Task: Каталог всех доступных сессий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001, PAOS-0004
- Blocks: PAOS-0010, PAOS-0012
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Постраничная история проекта с archived/fork/subagent связями
- Technical value: Постраничная история проекта с archived/fork/subagent связями
- Product value: Пользователь возвращается к любому доступному обсуждению проекта, включая архив и дочерние сессии.
- Scope: apps/local-service/src/sessions; apps/web/src/features/sessions/list
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог всех доступных сессий доступна в соответствующем этапе
- Acceptance criteria: Нет потерь и дублей между страницами; coverage показан; недоступная история обозначена
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/sessions; apps/web/src/features/sessions/list
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0010`

- Task: Сообщения и переходы по контексту
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0007, PAOS-0009
- Blocks: PAOS-0011, PAOS-0015
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Полный доступный диалог с авторами, задачами и сообщениями агентов
- Technical value: Полный доступный диалог с авторами, задачами и сообщениями агентов
- Product value: Пользователь читает обсуждение целиком и переходит от сообщения к соответствующей задаче или файлу.
- Scope: apps/web/src/features/sessions/transcript; packages/contracts/messages
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Сообщения и переходы по контексту доступна в соответствующем этапе
- Acceptance criteria: Порядок событий стабилен; длинный диалог открывает выбранное сообщение; fork и агент различимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/sessions/transcript; packages/contracts/messages
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0011`

- Task: Поиск, приватность и хранение сессий
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0010
- Blocks: PAOS-0025, PAOS-0027
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Искать историю без раскрытия секретов и чужих проектов
- Technical value: Искать историю без раскрытия секретов и чужих проектов
- Product value: Пользователь находит нужное сообщение без раскрытия чужих проектов и чувствительных данных.
- Scope: apps/local-service/src/session-search; apps/local-service/src/redaction
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Поиск, приватность и хранение сессий доступна в соответствующем этапе
- Acceptance criteria: Редакция секретов и project isolation подтверждены; пропуск/усечение и retention видимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 10:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/session-search; apps/local-service/src/redaction
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0012`

- Task: Каталог и профиль агента
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0007, PAOS-0009
- Blocks: PAOS-0013, PAOS-0015, PAOS-0016
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Инструкции, источник, действующая версия и назначенные задачи
- Technical value: Инструкции, источник, действующая версия и назначенные задачи
- Product value: Пользователь понимает назначение каждого агента и инструкции, по которым он работает.
- Scope: apps/local-service/src/agents; apps/web/src/features/agents/catalog
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог и профиль агента доступна в соответствующем этапе
- Acceptance criteria: Effective/proposed/loaded версии различимы; переход к task/run/session работает
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agents; apps/web/src/features/agents/catalog
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0013`

- Task: Создание, изменение и удаление агента
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0012
- Blocks: PAOS-0014, PAOS-0023
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Ручной CRUD с diff, проверкой, архивом и восстановлением
- Technical value: Ручной CRUD с diff, проверкой, архивом и восстановлением
- Product value: Пользователь меняет состав команды и инструкции с возможностью сравнения и восстановления.
- Scope: apps/local-service/src/agent-proposals; apps/web/src/features/agents/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Создание, изменение и удаление агента доступна в соответствующем этапе
- Acceptance criteria: Конфликт версии отклоняется; активный run не меняется; удалённый агент остаётся в истории
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-proposals; apps/web/src/features/agents/editor
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0014`

- Task: Управление агентом по описанию
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0013
- Blocks: none
- Source: PRD: дополнение Task Manager; screen specification
- Short description: По описанию создать, изменить или подготовить удаление агента через редактируемый proposal
- Technical value: Разобрать intent create/update/archive/delete, разрешить однозначный target и применить общий versioned proposal contract
- Product value: Пользователь описывает нужное изменение команды обычным языком и проверяет последствия до применения.
- Scope: apps/local-service/src/agent-generation; apps/web/src/features/agents/generator
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Генерация агента по описанию доступна в соответствующем этапе
- Acceptance criteria: Create/update/delete intent создаёт draft; target и diff видны; неоднозначное имя требует уточнения; active run и history не удаляются молча
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 10:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-generation; apps/web/src/features/agents/generator
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0015`

- Task: Назначения и статистика агентов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0003, PAOS-0010, PAOS-0012
- Blocks: PAOS-0024
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Наблюдать частоту, исходы, активные и прошлые задачи
- Technical value: Наблюдать частоту, исходы, активные и прошлые задачи
- Product value: Пользователь видит, как часто агент применяется, над чем работает и чем закончились его задачи.
- Scope: apps/local-service/src/agent-metrics; apps/web/src/features/agents/activity
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Назначения и статистика агентов доступна в соответствующем этапе
- Acceptance criteria: Метрики имеют период, знаменатель и coverage; отсутствующие данные не превращаются в нули
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/agent-metrics; apps/web/src/features/agents/activity
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0016`

- Task: Каталог и профиль скилла
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001, PAOS-0004, PAOS-0012
- Blocks: PAOS-0017
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать назначение, источник, версию, зависимости и использование
- Technical value: Показать назначение, источник, версию, зависимости и использование
- Product value: Пользователь находит доступные навыки и понимает, какие агенты их используют.
- Scope: apps/local-service/src/skills; apps/web/src/features/skills/catalog
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Каталог и профиль скилла доступна в соответствующем этапе
- Acceptance criteria: Project/global/vendor scopes различимы; effective версия и связь с агентами доступны
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 08:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skills; apps/web/src/features/skills/catalog
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0017`

- Task: Редактор и версии скиллов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0016
- Blocks: PAOS-0018, PAOS-0019, PAOS-0023
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Создавать и менять project-owned skills с проверкой структуры
- Technical value: Создавать и менять project-owned skills с проверкой структуры
- Product value: Пользователь адаптирует навык проекта и возвращается к прежней версии при ошибке.
- Scope: apps/local-service/src/skill-proposals; apps/web/src/features/skills/editor
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Редактор и версии скиллов доступна в соответствующем этапе
- Acceptance criteria: Preview diff и rollback работают; vendor original не перезаписывается; зависимость удаления видна
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-proposals; apps/web/src/features/skills/editor
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0018`

- Task: Добавление по пути и find-skills
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0017
- Blocks: PAOS-0019
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Единый выбор локального источника или найденного скилла
- Technical value: Единый выбор локального источника или найденного скилла
- Product value: Пользователь добавляет навык из папки или поиска, понимая его происхождение до установки.
- Scope: apps/local-service/src/skill-discovery; apps/web/src/features/skills/import
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Добавление по пути и find-skills доступна в соответствующем этапе
- Acceptance criteria: Поиск не устанавливает; path containment проверен; origin/license показаны до применения
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-discovery; apps/web/src/features/skills/import
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0019`

- Task: Генерация по требованиям и описанию
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0017, PAOS-0018
- Blocks: PAOS-0024
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Предложить недостающие навыки проекта и сгенерировать draft
- Technical value: Предложить недостающие навыки проекта и сгенерировать draft
- Product value: Пользователь получает недостающие навыки из требований проекта или собственного описания.
- Scope: apps/local-service/src/skill-generation; apps/web/src/features/skills/generator
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Генерация по требованиям и описанию доступна в соответствующем этапе
- Acceptance criteria: Рекомендация связана с requirement; повтор не создаёт дубликат; применение имеет preview
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/skill-generation; apps/web/src/features/skills/generator
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0020`

- Task: Индекс файлов и символов
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0001
- Blocks: PAOS-0021, PAOS-0022
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Типизированные зависимости файлов и переменных с source anchors
- Technical value: Типизированные зависимости файлов и переменных с source anchors
- Product value: Пользователь получает понятную основу карты зависимостей с явными пробелами анализа.
- Scope: apps/local-service/src/code-index; packages/contracts/graph
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Индекс файлов и символов доступна в соответствующем этапе
- Acceptance criteria: Неподдержанный язык и dynamic reference обозначены; индекс привязан к revision
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/code-index; packages/contracts/graph
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0021`

- Task: Граф и навигация к исходникам
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0004, PAOS-0020
- Blocks: PAOS-0022
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Фильтровать graph и раскрывать соседей выбранного узла
- Technical value: Фильтровать graph и раскрывать соседей выбранного узла
- Product value: Пользователь исследует структуру проекта и быстро находит связанные файлы без чтения всех папок.
- Scope: apps/web/src/features/graph
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Граф и навигация к исходникам доступна в соответствующем этапе
- Acceptance criteria: Есть search, depth, edge type, keyboard list alternative; большие графы не загружаются целиком
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/graph
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0022`

- Task: Влияние переменной и изменения
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0007, PAOS-0020, PAOS-0021
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать define/read/write/reference по scope и задачам
- Technical value: Показать define/read/write/reference по scope и задачам
- Product value: Пользователь видит, какие места могут быть затронуты изменением конкретной переменной.
- Scope: apps/local-service/src/impact; apps/web/src/features/graph/inspector
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Влияние переменной и изменения доступна в соответствующем этапе
- Acceptance criteria: Одноимённые переменные разных scope различены; stale и unresolved edges видимы
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: graph-cockpit-engineer, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/impact; apps/web/src/features/graph/inspector
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0023`

- Task: Политика автономности и лимиты
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0008, PAOS-0013, PAOS-0017
- Blocks: PAOS-0024, PAOS-0026, PAOS-0037
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Задать заранее разрешённые действия, бюджеты и stop conditions
- Technical value: Задать заранее разрешённые действия, бюджеты и stop conditions
- Product value: Пользователь задаёт границы самостоятельной работы один раз и сохраняет возможность остановки.
- Scope: apps/local-service/src/autonomy-policy; apps/web/src/features/autonomy
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Политика автономности и лимиты доступна в соответствующем этапе
- Acceptance criteria: Preview policy объясняет возможности; UI не расширяет host permissions; pause доступна
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/autonomy-policy; apps/web/src/features/autonomy
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0024`

- Task: Очередь, назначения и владение файлами
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0015, PAOS-0019, PAOS-0023, PAOS-0037, PAOS-0038
- Blocks: PAOS-0025
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Назначать агентов и skills в пределах scope без конфликтующих writers
- Technical value: Назначать агентов и skills в пределах scope без конфликтующих writers
- Product value: Пользователь запускает независимые задачи параллельно без незаметного перезаписывания одних файлов.
- Scope: apps/local-service/src/scheduler
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Очередь, назначения и владение файлами доступна в соответствующем этапе
- Acceptance criteria: Очередь соблюдает pinned recipe, blocks links, hard WIP и ownership; независимые writers допускаются только при отсутствии пересечения
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/scheduler
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0025`

- Task: Исполнение, восстановление и отмена
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0011, PAOS-0024
- Blocks: PAOS-0026
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Run adapter выполняет ограниченный план с восстановлением
- Technical value: Run adapter выполняет ограниченный план с восстановлением
- Product value: Пользователь может продолжить или отменить работу после сбоя, сохранив понятную историю.
- Scope: apps/local-service/src/runtime; apps/local-service/src/recovery
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Исполнение, восстановление и отмена доступна в соответствующем этапе
- Acceptance criteria: Повтор команды идемпотентен; timeout/cancel/crash дают определённое состояние и evidence
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 24:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/local-service/src/runtime; apps/local-service/src/recovery
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0026`

- Task: Решения и наблюдаемость автономности
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0023, PAOS-0025
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Показать что выполняется, почему остановилось и какое решение требуется
- Technical value: Показать что выполняется, почему остановилось и какое решение требуется
- Product value: Пользователь вмешивается там, где действительно требуется решение, и видит его последствия.
- Scope: apps/web/src/features/decisions; apps/local-service/src/decisions
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Решения и наблюдаемость автономности доступна в соответствующем этапе
- Acceptance criteria: Из решения доступен diff/scope/evidence; истёкшее решение не применяется; история сохраняется
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Повтор действий, конкурирующие writers, выход за разрешённый scope; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/decisions; apps/local-service/src/decisions
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0027`

- Task: Документы, проверки и общий поиск
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0007, PAOS-0008, PAOS-0011
- Blocks: PAOS-0028
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Объединить артефакты и результаты с задачами и источниками
- Technical value: Объединить артефакты и результаты с задачами и источниками
- Product value: Пользователь находит планы и проверки прямо из задачи, не разбираясь в расположении Markdown.
- Scope: apps/web/src/features/documents; apps/web/src/features/checks; apps/web/src/features/search
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Документы, проверки и общий поиск доступна в соответствующем этапе
- Acceptance criteria: Source version и время видны; результат теста не выдаётся за пользовательскую приёмку
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/web/src/features/documents; apps/web/src/features/checks; apps/web/src/features/search
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0028`

- Task: Интеграционная проверка пути
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0022, PAOS-0026, PAOS-0027, PAOS-0033, PAOS-0034, PAOS-0035, PAOS-0036, PAOS-0037, PAOS-0038
- Blocks: PAOS-0029
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить создание задачи, план, запуск, сессию, изменения и приёмку
- Technical value: Проверить создание задачи, план, запуск, сессию, изменения и приёмку
- Product value: Пользователь проходит весь путь от постановки до приёмки без разрывов между разделами.
- Scope: tests/web; tests/local-service
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Интеграционная проверка пути доступна в соответствующем этапе
- Acceptance criteria: Все 10 acceptance scenarios PRD §14 и прежний основной путь проверены; user-only completion и active-run cancellation подтверждены; отрицательные сценарии migration/links/attachments не теряют данные
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 24:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: tests/web; tests/local-service
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0029`

- Task: Доступность, языки и темы
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0028
- Blocks: PAOS-0030
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить клавиатуру, контраст, responsive и все локализованные состояния
- Technical value: Проверить клавиатуру, контраст, responsive и все локализованные состояния
- Product value: Пользователь сохраняет доступ ко всем действиям с клавиатуры, на узком экране и в обеих локализациях.
- Scope: tests/web/accessibility; docs/web/accessibility
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Доступность, языки и темы доступна в соответствующем этапе
- Acceptance criteria: Все 26 описанных экранов и новые task tabs проверены в RU/EN × Light/Dark; keyboard Kanban/workflow и длинные значения не теряют действия
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: tests/web/accessibility; docs/web/accessibility
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0030`

- Task: Упаковка и пилот
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Task Manager expansion, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0029
- Blocks: none
- Source: PRD: дополнение Task Manager; screen specification
- Short description: Проверить install/start/backup/rollback и полезность на реальном проекте
- Technical value: Проверить install/start/backup/rollback и полезность на реальном проекте
- Product value: Пользователь устанавливает и восстанавливает локальный продукт по проверенному процессу.
- Scope: apps/desktop-local; docs/web/pilot
- Non-goals: Глобальные permissions, внешняя публикация и несвязанный refactor
- Expected result: Упаковка и пилот доступна в соответствующем этапе
- Acceptance criteria: Пилот согласован отдельно; restore проверен; наблюдения отделены от продуктовых гипотез
- Verification gates: Focused contract tests; relevant integration checks; UI state and evidence review before closure
- Risks / approval gates: Потеря связей, неверный источник данных, конфликт версий или недоступный adapter; внешние/разрушительные действия отдельно авторизуются
- Complexity: medium/high, уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; task-matching implementation/verification skills selected at start
- Output artifacts: apps/desktop-local; docs/web/pilot
- Next step: Завершить зависимости, затем уточнить tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; create/modify/delete receipts recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending

### Task `PAOS-0031`

- Task: Иерархия Epic / Task / Bug / UserStory / Sub-Task
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0002
- Blocks: PAOS-0032, PAOS-0034, PAOS-0038
- Source: PRD §14; TM-15, TM-16
- Short description: Родительские связи, преобразование типов и roll-up без двойного счёта
- Technical value: Родительские связи, преобразование типов и roll-up без двойного счёта
- Product value: Пользователь разбивает инициативу на работы и подзадачи и видит общий прогресс
- Scope: packages/contracts/issues; apps/local-service/src/issue-hierarchy; apps/web/src/features/tasks/hierarchy
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Иерархия Epic / Task / Bug / UserStory / Sub-Task в будущем Web
- Acceptance criteria: Epic содержит standard types; Sub-Task имеет один standard parent; циклы и недопустимый reparent отклоняются; закрытие parent проверяет children
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: packages/contracts/issues; apps/local-service/src/issue-hierarchy; apps/web/src/features/tasks/hierarchy
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0032`

- Task: Поля, авторство, приоритеты, компоненты и даты
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0031, PAOS-0004
- Blocks: PAOS-0005, PAOS-0006, PAOS-0033, PAOS-0035
- Source: PRD §14; TM-16
- Short description: Неизменяемый creator, отдельный initiator, project components и календарные поля
- Technical value: Неизменяемый creator, отдельный initiator, project components и календарные поля
- Product value: Пользователь знает источник задачи, её важность, область и сроки
- Scope: packages/contracts/issue-fields; apps/local-service/src/components; apps/web/src/features/tasks/editor
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Поля, авторство, приоритеты, компоненты и даты в будущем Web
- Acceptance criteria: 11 исходных components доступны; multi-select; creator неизменяем; start/due validation и timezone проверены; unknown import не подменяется user
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: packages/contracts/issue-fields; apps/local-service/src/components; apps/web/src/features/tasks/editor
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0033`

- Task: Версии продукта и release policy
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0032
- Blocks: PAOS-0028
- Source: PRD §14; TM-17
- Short description: Раздельные affects/fix version references и условия планирования релиза
- Technical value: Раздельные affects/fix version references и условия планирования релиза
- Product value: Пользователь различает затронутый продукт и выпуск, который получит исправление
- Scope: apps/local-service/src/versions; apps/web/src/features/releases; packages/contracts/versions
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Версии продукта и release policy в будущем Web
- Acceptance criteria: Bug affects v1.2/fix v1.3 фильтруется корректно; archive сохраняет ссылки; Done не выпускает релиз
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 12:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/versions; apps/web/src/features/releases; packages/contracts/versions
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0034`

- Task: Attachments, комментарии и история изменений
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0031, PAOS-0007
- Blocks: PAOS-0028
- Source: PRD §14; TM-18, TM-24
- Short description: Managed files, comment revisions и append-only audit событий пользователя/агентов
- Technical value: Managed files, comment revisions и append-only audit событий пользователя/агентов
- Product value: Пользователь добавляет контекст и видит, кто, что и когда изменил
- Scope: apps/local-service/src/attachments; apps/local-service/src/comments; apps/local-service/src/audit; apps/web/src/features/tasks/activity
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Attachments, комментарии и история изменений в будущем Web
- Acceptance criteria: Upload quota/MIME/path checks; source file не меняется; tabs разделены; edits/tombstones/actor attribution и redaction проверены
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/attachments; apps/local-service/src/comments; apps/local-service/src/audit; apps/web/src/features/tasks/activity
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0035`

- Task: Kanban и ручной жизненный цикл задачи
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0005, PAOS-0008, PAOS-0032
- Blocks: PAOS-0028, PAOS-0036
- Source: PRD §14; TM-19, TM-20
- Short description: Восемь статусов, семь колонок, transitions/guards, WIP и resolution
- Technical value: Восемь статусов, семь колонок, transitions/guards, WIP и resolution
- Product value: Пользователь сам создаёт, ведёт, закрывает и переоткрывает задачи без обязательного agent run
- Scope: apps/web/src/features/tasks/board; apps/local-service/src/task-workflow
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Kanban и ручной жизненный цикл задачи в будущем Web
- Acceptance criteria: Drag/menu равнозначны; multi-status column требует выбора; manual Done проверяет criteria; Cancelled сохраняет reason; active run ждёт cancel receipt
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 16:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/web/src/features/tasks/board; apps/local-service/src/task-workflow
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0036`

- Task: Редактор, версии и миграции workflow
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0035
- Blocks: PAOS-0028, PAOS-0037
- Source: PRD §14; TM-21
- Short description: Workflow definitions, type mapping, draft/publish и pinned versions
- Technical value: Workflow definitions, type mapping, draft/publish и pinned versions
- Product value: Пользователь создаёт собственный процесс, не меняя незаметно уже идущую работу
- Scope: apps/local-service/src/workflows; apps/web/src/features/workflows; packages/contracts/workflows
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Редактор, версии и миграции workflow в будущем Web
- Acceptance criteria: S25/S26 доступны; invalid graph rejected; publish не меняет v1 runs; migration preview/status mapping/revision guards и rollback проверены
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/workflows; apps/web/src/features/workflows; packages/contracts/workflows
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0037`

- Task: Цепочки агентов и привязка к workflow
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0036, PAOS-0023
- Blocks: PAOS-0024, PAOS-0028
- Source: PRD §14; TM-22
- Short description: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Technical value: Recipes с branches/join, ownership, budgets и идемпотентным запуском
- Product value: Пользователь направляет агентов по разным цепочкам для features, bugs и non-code работы
- Scope: apps/local-service/src/execution-recipes; apps/local-service/src/scheduler; apps/web/src/features/workflows/recipes
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Цепочки агентов и привязка к workflow в будущем Web
- Acceptance criteria: Replay не дублирует run; bounded retry останавливается; parallel writers проверяются; policy нельзя расширить recipe; Manual не запускает agent
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 20:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/execution-recipes; apps/local-service/src/scheduler; apps/web/src/features/workflows/recipes
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending


### Task `PAOS-0038`

- Task: Linked Issues и блокирующие зависимости
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: User-requested Jira-informed issue model, 2026-11-09
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-0031, PAOS-0007
- Blocks: PAOS-0024, PAOS-0028
- Source: PRD §14; TM-23
- Short description: Canonical typed edges, inverse display, DAG blocking и авторство
- Technical value: Canonical typed edges, inverse display, DAG blocking и авторство
- Product value: Пользователь и агенты связывают работы и понимают, что мешает продолжению
- Scope: apps/local-service/src/issue-links; apps/web/src/features/tasks/links; packages/contracts/issue-links
- Non-goals: Jira sync, external publication, runtime config mutation outside authorized implementation
- Expected result: Linked Issues и блокирующие зависимости в будущем Web
- Acceptance criteria: Self/duplicate/cyclic blocks rejected; relates не блокирует; cancellation blocker требует решения; обе стороны и history согласованы
- Verification gates: Contract and negative-case tests; integration with adjacent modules; UI/accessibility scenarios from PRD §14
- Risks / approval gates: Потеря связей и истории, неоднозначная миграция, неверный terminal outcome или повтор agent run; preview/revision checks обязательны
- Complexity: high; уточнить после discovery
- Estimated execution time: 14:00:00 (предварительно)
- Agents: architect, builder, tester
- Skills: implementation-planner; verification skills selected for implementation
- Output artifacts: apps/local-service/src/issue-links; apps/web/src/features/tasks/links; packages/contracts/issue-links
- Next step: Завершить Depends on, зафиксировать contract/tests и file ownership
- Actual time: not_started; start/end/duration = null.
- Project artifacts: product-agent-os-web-prd-2026-11-05.md; product-agent-os-web-architecture-2026-11-05.md; product-agent-os-web-task-manager-screens-2026-11-09.md.
- Affected files: proposed paths above; actual create/modify/delete recorded after execution.

#### Completion Report

- Status: planned
- What was done: pending
- Files touched / work locations: pending
- Technical value delivered: pending
- Product value delivered: pending
- Actual implementation date and time: pending_execution_timestamp
- Verification evidence: pending
- Residual risks: pending
- Follow-up: pending
