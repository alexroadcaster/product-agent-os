# Product-Agent OS — направление A: внутреннее качество и архитектура

Source status: repository_source / owner_requested_planning / internal_quality_plan; user_project_work_split_to_direction_B; implementation_not_started.
Создан 15.11.2026, редакция 18.11.2026. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Два направления — редакция 3, 18.11.2026

A улучшает сам Product-Agent OS и процесс его сопровождения: **17 исполняемых planned задач**, 8 P1 / 7 P2 / 2 P3. B развивает применение методологий в проектах пользователей: [26 продуктовых задач](user-project-methodologies-2026-11-15.md), [JSON](user-project-methodologies-2026-11-15.json). Между направлениями нет hard dependencies.

Прежняя METH-16 сохранена с ID, названием и тремя legacy AC как **reference-only**, вне массива tasks в JSON v2; она не запускается и не владеет продуктовым status. Canonical owners: PMETH-03/07/10/11/16/17/22/23/26; точное соответствие AC и прежние edges сохранены в JSON. Для неё V-REFERENCE означает проверить ссылки/покрытие у B, без выполнения кода из A. METH-18 оценивает только варианты расширения A в METH-10/11/13–15. Направление B поставляется по своему плану.

Редакция 2 опиралась на HEAD `5a9c87bea374accc953a8401fa1ac32678ff6e6e` и состояние FUNC 10 implemented / 24 planned. Редакция 3 использует текущую сверку владельца FUNC от 18.11.2026. Сохранены все 18 ID, включая METH-16 как ссылку.

## Цель, полномочия и владельцы

Направление A развивает Spec-DD, Design-DD, TDD, ADD и границы frontend. Первый технический пилот ограничен Dashboard и доработкой проверки импортов. Все 17 исполняемых записей имеют status planned и `pending_execution_timestamp`.

[JSON-состояние v2](methodology-improvement-2026-11-15.json) владеет status/priority/dependencies 17 задач A; cross_track_references отдельно хранит METH-16. RU/EN карточки согласуются с JSON; таблицы — индекс. English доступен через переключатель языка. B имеет отдельного владельца и [подробный план](user-project-methodologies-2026-11-15.md). Создание этой редакции не закрывает A/B/FUNC/Web/V3.

## Исходное состояние и доказательства

Source snapshot: git HEAD `35458110145d928b9b14d9312b60d852f11f6e88`; hashes семи прочитанных implementation/test owners находятся в JSON. Снимок относится к первоначальному планированию. Во время планирования выполнено чтение исходников/владельцев; прежние tests/browser/native receipts заново не выполнялись.

- [Владелец FUNC](functional-remediation-2026-11-15.json) и [результаты G07](functional-remediation-2026-11-15.md#func-g07-results) на 18.11.2026 фиксируют 33 implemented / 1 awaiting_user_decision (F23). Для F05–F08, F14, F19 и F24 используем уже проверенные контракты и сценарии в пределах их доказательств. Human pilot F23 остаётся открытым. Срез [G01](functional-remediation-2026-11-15.md#func-g01-results) 7/27 относится к первой редакции.
- Spec-DD уже отражён в [требованиях и capability model](../product/capabilities.md) и конкретных task matrices; файлы workspace `TEST.md` и `EVALS.md` владеют выбором проверок и claim ceiling.
- Design-DD имеет файл workspace `DESIGN.md`, V3 coverage и [план внедрения](2026-11-13-v3-ui-implementation-plan.md). Исторический V3 review выявил разрыв composition coverage; это не утверждение о новом дефекте текущего build.
- TDD поддержан правилами и отдельными historical RED/GREEN receipts; готовый набор тестов не доказывает test-first для каждой задачи.
- ADD имеет build/review/handoff contracts и разделение ownership. Улучшение качества/стоимости agentic работы требует сопоставимого baseline, а не подсчёта ролей.
- Frontend сгруппирован по features, но dashboard/tasks/team/workflows используют внутренние соседние модули. Строгий FSD не доказан; тест workspace `tests/web/contracts-boundaries.test.mts` защищает application boundary, а не все FSD imports. METH-09 должен явно включить TSX и aliases, чтобы новая проверка не имела скрытого coverage gap.

Исходники: `apps/web/src/features/dashboard/model.ts`, `tasks/TaskManager.tsx`, `workflows/WorkflowManager.tsx`, `team/TeamManager.tsx`, `apps/web/src/ui/App.tsx`; Python owner `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`. Перед будущими edits перечитать их актуальное состояние.

Методологические первоисточники, проверенные в предшествующем анализе 15.11.2026: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html), [FSD layers](https://feature-sliced.design/docs/reference/layers), [FSD public API](https://feature-sliced.design/docs/reference/public-api), [Spec Kit process](https://github.github.io/spec-kit/quickstart.html), [IBM human-centered design](https://www.ibm.com/training/enterprise-design-thinking/framework), [AWS AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/). ADD/Design-DD здесь — явно заданные рабочие подходы; план не утверждает их единую отраслевую стандартизацию. Предложения и оценки ниже — project-authored, не результаты внешних исследований.

## Приоритеты, этапы и зависимости

P1 — защита контрактов и достоверность приёмки; P2 — основной ограниченный пилот и улучшение процесса; P3 — optional scale после evidence. P1 не означает production incident. Номер задачи не задаёт порядок.

### Группы задач

Группы объединяют задачи по результату. Каждую задачу можно начинать после выполнения её `depends_on` и применимых условий выбора.

| Группа | Задачи | Условие старта и результат |
| --- | --- | --- |
| **A1. Критерии и границы Dashboard** | 01, 02, 03, 04, 08, 09 | После 01 ветка 02 → 03 → 04 фиксирует поведение и состояния Dashboard, ветка 08 → 09 — допустимые импорты и способы их проверки. |
| **A2. Пилот Dashboard и решение о расширении** | 12, 17, 18 | После 04 и 09 задача 12 проверяет границу Dashboard и Tasks. Задача 17 принимает технический результат, а 18 решает, стоит ли расширять пилот. Допустима остановка на Dashboard. |
| **A3. Качество тестирования и работы агентов** | 05, 06, 07 | После 02 можно параллельно пилоту выполнить 05 → 06 → 07. Результаты — карта пробелов в проверках, проверенный порядок передачи задач и отдельная оценка работы агентов. Для реальных запусков в 07 нужны разрешение и сопоставимые условия. |
| **A4. Выборочное расширение архитектурных границ** | 10, 11, 13, 14, 15 | После 18 выбираются обоснованные изменения для общих UI-компонентов, API Tasks или отдельных экранов. Для каждого выбранного участка фиксируются ожидаемая польза, проверка и способ отката. |

После METH-01 идут две ветки. METH-02 → 03 → 04 задаёт критерии и состояния Dashboard. METH-08 → 09 задаёт ADR и проверку импортов. Они сходятся в METH-12 → 17 → 18. METH-05/06/07 идут отдельно и не задерживают техническую приёмку. Каждое расширение METH-10/11/13–15 требует решения METH-18 по конкретному scope. `depends_on` в JSON задаёт обязательные рёбра, `blocks` хранит обратные. Условия выбора записаны в `activation_condition`.

## Совмещение с действующим backlog

| Existing owner | Как используется | Что не дублируется |
| --- | --- | --- |
| F01/F03–F08, FUNC-G01 | Baseline и regression protections | Исправления, native qualification и их completion statuses |
| F02/F28 | Reference для будущих artifact traceability/canonical paths | Реализация task↔artifact links и inventory; METH-02 не зависит от F28 |
| F11/F12/F16 | Ограничения metrics/team/skills | Telemetry, external search и real loaded-profile proof |
| F18/F20 | Refresh semantics и бюджеты производительности | Изменение refresh и повторные benchmarks |
| F14/F30 | F14 использует Rolldown AST и ограниченный resolver; сверяем семантику импортов и reuse fixtures | Повторный runtime graph и установка PoC dependency-cruiser |
| F19/F21/F22/F23/F24, UI-12 | Переиспользуемые сценарии/evidence и отдельная full/human приёмка | Полный E2E, recovery, backup/restore, feature availability и human acceptance |
| F25, DOCS-01–16 | Canonical docs/status ownership | Повторное создание guides или изменение feature task-state |
| F26–29/F31–34, M5 | Запрет расширить migration scope | Новые Files/Map/Database/usages, hosting/auth/team capabilities |

Ссылки `external_refs` указывают владельцев и evidence. F08 защищает application-independent contracts, F18 владеет refresh semantics. Актуальность F01 проверяется при изменении pinned runtime sources. Общие файлы правятся последовательно.

## Предлагаемые границы постепенного FSD

В METH-08 сравнить сохранение текущих модулей, усиление их границ и локальный FSD. Предпочтителен минимальный вариант, который убирает обнаруженную проблему Dashboard и допускает простой откат.

- Сохранить `App.tsx` владельцем composition/session/project scope. Начать с явного API для востребованных селекторов Tasks (`semanticStatus`, `isBlocked`) и одного источника логики. При выборе FSD допустим pages-first.

- Выделять widgets, entities/task и shared только при подтверждённой потребности. Пригодность API и регрессии проверяются до переноса других экранов. Общие business contracts остаются в `packages/contracts`.

- Разрешённые compatibility bridges используют одну реализацию и имеют владельца удаления. Новые нарушения проверяются относительно привязанного к revision baseline. Для выбранной границы Dashboard фиксируются и закрываются неразрешённые нарушения.

- Dashboard может стать конечным результатом. Для очередного выбранного экрана фиксируются самостоятельные guards и откат. При затронутых общих путях повторно проверяются draft/CAS, project/session isolation, focus и действующие state semantics.

## Проверка будущих задач

Эти профили — proposed task acceptance; текущий verification route остаётся у TEST.md и не изменён этим планом.

| Профиль | Минимальное доказательство |
| --- | --- |
| V-PLAN | Semantic/source/link review и `python -B plugins/product-agent-os/scripts/validate_task_matrix.py <changed-plan>`; docs checks по changed paths из TEST; DAG/MD–JSON/RU–EN parity; без runtime claims |
| V-TDD | Existing risk/check inventory, focused regression при новых tests; ожидаемый observable RED только для changed behavior, GREEN и scoped refactor evidence; документы/moves не требуют искусственного RED |
| V-BOUNDARY | `node --test tests/web/contracts-boundaries.test.mts` с meaningful negative/positive parser/import cases; configured alias resolution, TSX и remaining exceptions; дальнейшие checks по affected contract |
| V-WEB | Focused Node tests текущих consumers, `npm run check:web-m1`, `npm run build:web`; synthetic current-build browser/visual/keyboard checks изменённого journey в обоих themes; native/recovery только при соответствующем изменении |
| V-ADD | Baseline/candidate на названных representative/negative cases; explicit self-review либо separately authorized independent review; deterministic correctness отдельно от actual model quality и activation |
| V-PLUGIN | Focused `tests.product_agent_os.test_methodology_audit` и `test_methodology_catalog`, affected fixture/eval scenarios по TEST; baseline comparison при routing changes; без target/provider mutation |
| V-INTEGRATED | Совмещённое состояние пилота: affected integration checks, source/build/harness provenance, visual/state coverage, findings disposition; full suites только по TEST trigger, human acceptance отдельная |

Новая dependency/installation, активные durable prompts/rules, hooks/trust, actual model/provider, target workspace, Git/publication и production требуют соответствующей отдельной authority. Будущий запрос на реализацию выбранного local slice не расширяется автоматически на эти действия. Использовать существующие temporary synthetic profiles; не записывать pairing/session material, secrets и private raw chats.

## Метрики, stop и rollback

Baseline/pilot: unauthorized import edges, meaningful regression findings, reopened tasks, repair cycles, owner interventions и elapsed с явной provenance. Tokens/cost — только если доступны достоверно; отсутствие данных не означает ноль. Время/качество/стоимость агента не объявляются улучшенными без сопоставимого actual-agent evidence.

Обязательный минимум: zero новых unauthorized edges, zero unresolved critical regressions в pilot scope, все его обязательные AC с evidence; прочие thresholds/measurement windows определить до candidate run и зафиксировать в METH-01/07. Полезность FSD оценивается по локализации изменения, review effort и поддерживаемости; число папок, тестов или агентов не считается успехом.

Stop: потеря draft/data, scope/approval violation, непроверяемые aliases, отсутствующий существенный baseline, неподтверждённый source owner, конфликт одновременной записи или необходимость расширить разрешения. Rollback — только собственные hunks/checkpoint, сохранение public compatibility и пользовательских данных; никаких destructive Git или DB operations. Изменившийся pinned runtime source требует квалификации по действующему TEST, не механической замены hashes.

## Первоначальная проверка подготовки плана — 15.11.2026

Проверена подготовка planning artifact, а не выполнение METH-задач. Review mode: self_review; independent review и runtime acceptance не заявлены.

- `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/methodology-improvement-2026-11-15.md` — ok, errors=[]; EN counterpart — такой же результат.
- `python -B tools/check_docs.py --paths` с девятью изменёнными Markdown owners (оба новых плана, оба planning index, оба registry, REQUIREMENTS/PLAN/RUNLOG) — OK: 9 changed Markdown source(s); site/archive не проверялись.
- Локальные read-only assertions через `python -B -`: 18 уникальных planned задач, 54 bilingual AC, 27 reciprocal dependency edges; DAG acyclic; RU/EN/JSON titles/status/priority/dependencies/AC/profiles согласованы; P3 не блокирует METH-17/18; METH-14 требует rollout decision METH-18.
- Preservation: hashes 19 existing source/contract owners не изменены; удаление только добавленных planning sections восстанавливает исходные bytes семи изменённых existing documents. Чужие session markers и параллельные workstreams не затрагивались.
- `git diff --check` — exit 0. Application tests/build/browser/native/provider и generated site не запускались. Все 18 implementation timestamps остаются pending_execution_timestamp.
- Control-plane sync: updated REQUIREMENTS/PLAN/RUNLOG и planning/source pointers; TEST/EVALS/prod_test no_change_needed — active verification policy и historical execution evidence не менялись.

## Проверка разделения — редакция 2

Static split/parity/preservation evidence редакции 2 хранится в направлении B. Редакция 3 сохраняет прежние формулировки изменённых AC и снятые рёбра в `pilot_revision` JSON. Даты и результаты первоначальной проверки выше относятся к исходной редакции.

## Индекс задач

| ID | Приоритет | Группа / методы | Задача | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-METH-01 | P1 | A1; Spec-DD, ADD | Зафиксировать baseline и владельцев улучшений | — |
| PAOS-METH-02 | P1 | A1; Spec-DD | Связать критерии Dashboard с исходниками и проверками | PAOS-METH-01 |
| PAOS-METH-03 | P1 | A1; Design-DD, Spec-DD | Уточнить design-контракт состояний пилота | PAOS-METH-02 |
| PAOS-METH-04 | P1 | A1; Design-DD, TDD | Проверять композицию и поведение интерфейса по design-контракту | PAOS-METH-03 |
| PAOS-METH-05 | P1 | A3; TDD, Spec-DD | Закрыть пробелы TDD и regression evidence для критических контрактов | PAOS-METH-02 |
| PAOS-METH-06 | P2 | A3; ADD, Spec-DD | Упростить контракты agent slice и handoff по baseline eval | PAOS-METH-05 |
| PAOS-METH-07 | P2 | A3; ADD | Измерить результат agentic-пилота на сопоставимых задачах | PAOS-METH-06 |
| PAOS-METH-08 | P1 | A1; FSD, Design-DD | Спроектировать постепенные границы FSD и переходный ADR | PAOS-METH-01 |
| PAOS-METH-09 | P1 | A1; FSD, TDD | Добавить инкрементальную проверку frontend imports | PAOS-METH-08 |
| PAOS-METH-10 | P2 | A4; FSD | Выделить необходимые shared UI и инфраструктурные модули | PAOS-METH-18 |
| PAOS-METH-11 | P2 | A4; FSD, Spec-DD | Стабилизировать публичные интерфейсы домена Tasks | PAOS-METH-18 |
| PAOS-METH-12 | P2 | A2; FSD, Design-DD, Spec-DD | Проверить архитектурные границы на Dashboard | PAOS-METH-04, PAOS-METH-09 |
| PAOS-METH-13 | P2 | A4; FSD, Design-DD, TDD | При подтверждённой пользе улучшить границы Tasks и Workflows | PAOS-METH-18 |
| PAOS-METH-14 | P3 | A4; FSD, ADD | Расширить FSD на team и skills после go-решения | PAOS-METH-18 |
| PAOS-METH-15 | P3 | A4; FSD, Design-DD | Перенести оставшиеся выбранные экраны и завершить composition boundary | PAOS-METH-18 |
| PAOS-METH-16 | P3 (legacy) | reference-only B | Уточнить условную поддержку методологий в Python plugin | —; не исполнять из A |
| PAOS-METH-17 | P1 | A2; Spec-DD, Design-DD, TDD, ADD, FSD | Принять технический пилот Dashboard и проверить контракты | PAOS-METH-12 |
| PAOS-METH-18 | P2 | A2; ADD, FSD, Spec-DD | Принять решение о дальнейшем rollout и обновить владельцев документации | PAOS-METH-17 |

## Подробные карточки задач

### Task `PAOS-METH-01`

- Task: PAOS-METH-01
- Task name: Зафиксировать baseline и владельцев улучшений
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет.
- Blocks: PAOS-METH-02, PAOS-METH-08
- External references: PAOS-FUNC-01, PAOS-FUNC-02, PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-19, PAOS-FUNC-23, PAOS-FUNC-24, PAOS-FUNC-25, PAOS-FUNC-30
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Снять актуальный source/contract/test baseline и устранить дублирование с FUNC, Web и V3.
- Technical value: Снять актуальный source/contract/test baseline и устранить дублирование с FUNC, Web и V3.
- Product value: Сохранить уже исправленное поведение и назначить одного владельца каждой новой работы.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/planning/methodology-improvement-2026-11-15.json`; `docs/frontend/index.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Baseline и карта ownership в этой карточке; без нового глобального реестра.
- Acceptance criteria: PAOS-METH-01-AC01: Зафиксированы revision, локальные изменения, imports и действующие проверки web/plugin; прежние receipts помечены своей датой. PAOS-METH-01-AC02: Для каждой METH-карточки указано own/reuse/reference относительно FUNC/Web/V3; существующие AC и статусы не скопированы в новую владеющую очередь. PAOS-METH-01-AC03: Назначены владельцы файлов и очередность общих правок. Текущий FUNC JSON и раздел G07 задают baseline 33 implemented / 1 awaiting_user_decision (F23) на 18.11.2026. F01/F03–F08 и F14/F19/F24/F25 используются в пределах подтверждённого evidence.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Concurrent planning edits; перед записью сверить revision. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: architect + product-manager; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Baseline и карта ownership в этой карточке; без нового глобального реестра.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Concurrent planning edits; перед записью сверить revision.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-02`

- Task: PAOS-METH-02
- Task name: Связать критерии Dashboard с исходниками и проверками
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-03, PAOS-METH-05
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-19, PAOS-FUNC-25
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сопоставить состояния Dashboard с действующими критериями F05–F07 и существующими проверками. Затронутые контракты редактора учитывать как защиту от регрессии.
- Technical value: Сопоставить состояния Dashboard с действующими критериями F05–F07 и существующими проверками. Затронутые контракты редактора учитывать как защиту от регрессии.
- Product value: Проверять результат по пользовательскому контракту и быстро находить недостающую проверку.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/testing/index.md`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Одна таблица критериев Dashboard и указатели на существующие проверки и пробелы.
- Acceptance criteria: PAOS-METH-02-AC01: Для применимых критериев Dashboard записана связь criterion → canonical owner → source → existing test/browser scenario → receipt или явный gap. Использованы F05–F07 и действующие TEST checks. PAOS-METH-02-AC02: Частичное portfolio явно помечено. Empty/error/stale покрыты по применимости. Если меняется общий путь навигации или состояния редактора, действующая проверка подтверждает сохранность и изоляцию draft. PAOS-METH-02-AC03: Одна изменённая предпосылка API/данных отражена в основном владельце, mirrors согласованы; traceability не реализует F02 и не ждёт её F28.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не менять продуктовый scope и статусы FUNC; gaps не выдавать за passed. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: product-manager + tester; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Одна таблица критериев Dashboard и указатели на существующие проверки и пробелы.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Не менять продуктовый scope и статусы FUNC; gaps не выдавать за passed.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-03`

- Task: PAOS-METH-03
- Task name: Уточнить design-контракт состояний пилота
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-04
- External references: PAOS-FUNC-05, PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Уточнить применимые состояния Dashboard по действующему V3, F05 и доступным данным API.
- Technical value: Уточнить применимые состояния Dashboard по действующему V3, F05 и доступным данным API.
- Product value: Устранить разрыв между утверждённым макетом, данными и реальным сценарием пользователя.
- Scope: `DESIGN.md`; `design/2026-11-13-v3/coverage.json`; `docs/frontend/state-management.md`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Дополнение существующих state/coverage owners; новые макеты только для отсутствующего необходимого состояния.
- Acceptance criteria: PAOS-METH-03-AC01: Для Dashboard отмечены применимые default/loading/empty/error/partial/stale и keyboard/focus в обеих темах. Dirty/validation/confirmation проверяются при затронутом контракте, остальные состояния имеют обоснованный not_applicable. PAOS-METH-03-AC02: Источник, единицы и unavailable для показателей явные; synthetic usage не становится данными приложения, F11 не реализуется этой задачей. PAOS-METH-03-AC03: Design differences получают disposition: исправить/предложить владельцу/принятый gap; согласование макета не закрывает UI-12 или human acceptance.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Новый пользовательский сценарий требует отдельного решения владельца; текущий V3 не переутверждается молча. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: product-manager + frontend owner; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Дополнение существующих state/coverage owners; новые макеты только для отсутствующего необходимого состояния.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Новый пользовательский сценарий требует отдельного решения владельца; текущий V3 не переутверждается молча.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-04`

- Task: PAOS-METH-04
- Task name: Проверять композицию и поведение интерфейса по design-контракту
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-03
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-05, PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Расширить существующий UI harness для пилота без второй системы screenshot/evidence.
- Technical value: Расширить существующий UI harness для пилота без второй системы screenshot/evidence.
- Product value: Ловить композиционные и интерактивные регрессии, которые не выявляет один overflow/contrast check.
- Scope: `tests/web/single-window/func-g01-dashboard-acceptance.mts`; `tests/web/single-window/ui-v3-scenario.mts`; `tests/web/ui-v3-dashboard.test.mts`; `design/2026-11-13-v3/implementation-evidence.md`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Пилотные проверки в существующем harness и evidence в прежнем владельце.
- Acceptance criteria: PAOS-METH-04-AC01: На текущей сборке проверены обе темы, partial/error и применимые keyboard/focus-состояния Dashboard. Если пилот меняет общий overlay/navigation, действующий сценарий проверяет focus return и сохранение draft. PAOS-METH-04-AC02: Проверки обнаруживают намеренно изменённую fixture геометрию/состояние; thresholds и стабильные области обоснованы, обновление baseline явно reviewable. PAOS-METH-04-AC03: Расхождения сравниваются с design owner; automated technical pass отделён от human acceptance, receipt привязан к hashes build/harness.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Synthetic profiles only; без provider/credentials, без снимков реальных пользовательских данных. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + frontend owner; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Пилотные проверки в существующем harness и evidence в прежнем владельце.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Synthetic profiles only; без provider/credentials, без снимков реальных пользовательских данных.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-05`

- Task: PAOS-METH-05
- Task name: Закрыть пробелы TDD и regression evidence для критических контрактов
- Status: planned
- Priority: P1
- Delivery group: A3
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-06
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Разделить текущие защиты, недостающие regression cases и правила RED для следующего изменения поведения.
- Technical value: Разделить текущие защиты, недостающие regression cases и правила RED для следующего изменения поведения.
- Product value: Не потерять draft/retry/recovery/approval invariants при рефакторинге и изменениях tooling.
- Scope: `TEST.md`; `tests/web/ui-draft-autosave.test.mts`; `tests/web/contracts-boundaries.test.mts`; `tests/product_agent_os/test_methodology_audit.py`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Компактная risk/test карта в TEST и текущих task evidence; только недостающие meaningful tests.
- Acceptance criteria: PAOS-METH-05-AC01: Карта risk → invariant → lowest reliable check покрывает draft conflict/lost ACK, import boundary, Stop/recovery, backup/restore и approval routing; существующие тесты переиспользованы. PAOS-METH-05-AC02: До нового проверяемого изменения определены ожидаемая причина RED и минимальный GREEN. METH-09 владеет своими import fixtures и может стартовать по ADR независимо от этой карты. Продуктовый Python routing принадлежит B. PAOS-METH-05-AC03: Setup/import failures не считаются RED; behavior-preserving moves используют characterization/regression без искусственно сломанного production code; F21/F22 остаются отдельными владельцами полного recovery scope.
- Verification gates: V-TDD; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не дублировать full recovery suites и не требовать RED для docs или чистого перемещения. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Компактная risk/test карта в TEST и текущих task evidence; только недостающие meaningful tests.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Не дублировать full recovery suites и не требовать RED для docs или чистого перемещения.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-06`

- Task: PAOS-METH-06
- Task name: Упростить контракты agent slice и handoff по baseline eval
- Status: planned
- Priority: P2
- Delivery group: A3
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05
- Blocks: PAOS-METH-07
- External references: Нет; текущий план — владелец.
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Проверить достаточность существующего краткого контракта, устраняя измеренные дубли без нового обязательного пакета.
- Technical value: Проверить достаточность существующего краткого контракта, устраняя измеренные дубли без нового обязательного пакета.
- Product value: Снизить overhead и потерю контекста при сохранении ownership и границ полномочий.
- Scope: `.codex/workflows/build-slice.md`; `.codex/workflows/review-slice.md`; `.codex/evals/agent-context-contract.json`; `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Изменение только доказанно избыточных sections и baseline/candidate evidence в существующем eval owner.
- Acceptance criteria: PAOS-METH-06-AC01: Baseline и один candidate сравниваются на bounded fix, docs-only, missing context, overlapping ownership, premature success и unapproved external action. PAOS-METH-06-AC02: Goal/AC, source revision, owned/forbidden files, checks, stop conditions и handoff сохраняются; ordinary concise route не превращается в full packet. PAOS-METH-06-AC03: Candidate продвигается только при отсутствии новых boundary/claim failures; static contract pass не объявляется fresh-session activation или LLM quality improvement.
- Verification gates: V-ADD; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Это будущие durable instruction changes: отдельный authorized slice, baseline eval, сохранение before-image; hooks/trust не менять. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: lifecycle-orchestrator + reviewer; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Изменение только доказанно избыточных sections и baseline/candidate evidence в существующем eval owner.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Это будущие durable instruction changes: отдельный authorized slice, baseline eval, сохранение before-image; hooks/trust не менять.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-07`

- Task: PAOS-METH-07
- Task name: Измерить результат agentic-пилота на сопоставимых задачах
- Status: planned
- Priority: P2
- Delivery group: A3
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-06
- Blocks: Нет.
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сравнить baseline и candidate на одном наборе задач, отделив orchestration correctness от качества решения.
- Technical value: Сравнить baseline и candidate на одном наборе задач, отделив orchestration correctness от качества решения.
- Product value: Принимать решение о процессе по качеству результата и затратам, а не числу агентов или tests.
- Scope: `EVALS.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Сравнение baseline/candidate в evidence карточки; отдельный verdict correctness/quality/cost.
- Acceptance criteria: PAOS-METH-07-AC01: Зафиксированы одинаковые task inputs/AC/revision, разрешения и инструменты, сопоставимые модель и reasoning effort при actual-agent сравнении. Accepted/reopened, repair cycles, owner interventions и elapsed имеют provenance. PAOS-METH-07-AC02: Tokens/cost приводятся только при достоверном источнике; unavailable не заменяется нулём; F11 telemetry не реализуется ради этого пилота. PAOS-METH-07-AC03: Если actual-agent сравнение недоступно без нового разрешения, результат ограничен deterministic routing; model-quality benefit остаётся insufficient_evidence и не разрешает promotion.
- Verification gates: V-ADD; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Без автоматических provider calls, raw private chats и неподтверждённых productivity claims; human acceptance остаётся отдельной. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + product-manager; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Сравнение baseline/candidate в evidence карточки; отдельный verdict correctness/quality/cost.
- Next step: По отдельному разрешению и при зафиксированных сопоставимых условиях эксперимента. Допустим отдельный deterministic-only результат. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Без автоматических provider calls, raw private chats и неподтверждённых productivity claims; human acceptance остаётся отдельной.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-08`

- Task: PAOS-METH-08
- Task name: Спроектировать постепенные границы FSD и переходный ADR
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-09
- External references: PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-30
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сравнить сохранение структуры, усиление границ текущих feature modules и ограниченный FSD. Выбрать минимальный способ исправить подтверждённую связанность.
- Technical value: Сравнить сохранение структуры, усиление границ текущих feature modules и ограниченный FSD. Выбрать минимальный способ исправить подтверждённую связанность.
- Product value: Сделать следующую миграцию проверяемой без полного rewrite и лишних папок.
- Scope: `docs/architecture/decisions/`; `docs/frontend/index.md`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Один ADR с выбором scope проверки и границы Dashboard, стоимостью и условиями отката.
- Acceptance criteria: PAOS-METH-08-AC01: ADR сравнивает оставить feature folders, улучшить только boundaries и частично внедрить FSD; решение опирается на coupling, тестируемость и стоимость переноса. PAOS-METH-08-AC02: Определены владелец текущей композиции Dashboard и минимальный публичный API. При выборе FSD допустим pages-first; widgets, entities и shared выделяются при доказанной потребности. Whole-screen TaskManager/Dashboard не становятся interaction features по имени. PAOS-METH-08-AC03: Зафиксированы public APIs, legacy exception list с owner/removal task, направление bridge legacy→new, fallback/rollback и критерий достаточности; FSD не распространяется на backend/Python.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: ADR в этом плане — будущий deliverable, не уже принятое архитектурное решение; F30 не является обязательной зависимостью. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: architect; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Один ADR с выбором scope проверки и границы Dashboard, стоимостью и условиями отката.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: ADR в этом плане — будущий deliverable, не уже принятое архитектурное решение; F30 не является обязательной зависимостью.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-09`

- Task: PAOS-METH-09
- Task name: Добавить инкрементальную проверку frontend imports
- Status: planned
- Priority: P1
- Delivery group: A1
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-08
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-08, PAOS-FUNC-14, PAOS-FUNC-30
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Расширить существующий тест границ установленным AST parser и правилами ADR. Проверка работает без запуска F14 или установки dependency-cruiser.
- Technical value: Расширить существующий тест границ установленным AST parser и правилами ADR. Проверка работает без запуска F14 или установки dependency-cruiser.
- Product value: Остановить рост связанности до начала перемещений, не блокируя весь legacy.
- Scope: `tests/web/contracts-boundaries.test.mts`; `tests/web/graph-imports.test.mts`; `tsconfig.web-m1.json`; `apps/web/src/`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Существующая команда проверяет frontend scope и прежние backend/contracts границы. Примеры resolution переиспользуют действующие fixtures, где семантика совпадает.
- Acceptance criteria: PAOS-METH-09-AC01: Расширенный tests/web/contracts-boundaries.test.mts проверяет .ts/.tsx/.mts, type imports/reexports/literal dynamic imports и поддерживаемые aliases. RED/GREEN отличает запрещённый edge от ошибки resolution. Неподдерживаемый alias или динамическая цель явно диагностируются. PAOS-METH-09-AC02: В пилотном scope соблюдаются public API и согласованные ADR правила upward/same-layer/deep imports и циклов. Entity cross-imports разрешаются через конкретный API, только если эта структура выбрана. PAOS-METH-09-AC03: Текущие legacy edges revision-pinned и не растут; перенесённый модуль удаляется из exceptions; действующие contracts→apps и backend→frontend запреты сохраняются.
- Verification gates: V-BOUNDARY; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не прятать реальные imports за exclusions; baseline обновлять reviewable. Не устанавливать dependency-cruiser автоматически. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + builder; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Существующая команда проверяет frontend scope и прежние backend/contracts границы. Примеры resolution переиспользуют действующие fixtures, где семантика совпадает.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Не прятать реальные imports за exclusions; baseline обновлять reviewable. Не устанавливать dependency-cruiser автоматически.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-10`

- Task: PAOS-METH-10
- Task name: Выделить необходимые shared UI и инфраструктурные модули
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: Нет.
- External references: Нет; текущий план — владелец.
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Выделить подтверждённый недоменный компонент после решения METH-18 и проверки существующего владельца.
- Technical value: Выделить подтверждённый недоменный компонент после решения METH-18 и проверки существующего владельца.
- Product value: Убрать зависимость общих представлений от внутренних task/graph screens.
- Scope: `apps/web/src/ui/Icon.tsx`; `apps/web/src/ui/Modal.tsx`; `apps/web/src/features/tasks/CommentMarkdown.tsx`; `apps/web/src/locales/`; `apps/web/src/features/graph/GraphViews.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Минимальный shared public API, compatibility bridges и обновлённая migration map.
- Acceptance criteria: PAOS-METH-10-AC01: Каждое выделение привязано к выбранной METH-18 проблеме и актуальным потребителям. В shared попадают только востребованные primitives, safe Markdown/rendering или i18n infrastructure. Task status rules и task labels остаются у домена. PAOS-METH-10-AC02: Mermaid/graph renderer разделён на generic rendering и domain mapping только при подтверждённом reuse; no wildcard public exports, frontend→backend зависимости не добавлены. PAOS-METH-10-AC03: Compatibility reexports однонаправленные, implementation/state единственные; прежние theme/focus/Markdown-safety/reduced-motion regressions проходят.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Это behavior-preserving move; не менять visual design, sanitize policy, API или данные. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — shared frontend ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Минимальный shared public API, compatibility bridges и обновлённая migration map.
- Next step: METH-18 выбрала эту работу и подтверждён конкретный повторно используемый недоменный компонент либо затруднение сопровождения. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Это behavior-preserving move; не менять visual design, sanitize policy, API или данные.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-11`

- Task: PAOS-METH-11
- Task name: Стабилизировать публичные интерфейсы домена Tasks
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: Нет.
- External references: PAOS-FUNC-08
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Расширить существующую границу Tasks по подтверждённой необходимости. Выделение entities/task требует прозрачной пользы для потребителей.
- Technical value: Расширить существующую границу Tasks по подтверждённой необходимости. Выделение entities/task требует прозрачной пользы для потребителей.
- Product value: Dashboard и team используют стабильный task API вместо deep imports в task screen.
- Scope: `apps/web/src/features/tasks/model.ts`; `apps/web/src/features/tasks/labels.ts`; `apps/web/src/features/dashboard/model.ts`; `packages/contracts/issues/task-profile.ts`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Поддержанный ADR публичный API, переходные адаптеры при необходимости и regression evidence.
- Acceptance criteria: PAOS-METH-11-AC01: Повторно используемые selectors/status presentation/task labels имеют одного владельца и подтверждённых потребителей. Entities/task выделяется только при доказанной пользе. Draft и commands остаются у interaction, backend authority сохраняется. PAOS-METH-11-AC02: packages/contracts остаётся application-independent, не импортирует React/UI; типы и decode/persistence semantics F08 сохраняются. PAOS-METH-11-AC03: Потребители пилота используют явный public API; tests semanticStatus/isBlocked/aggregation и contracts boundaries проходят, legacy bridges имеют removal owner.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не копировать business rules между сервисом и UI и не менять подсчёт прогресса/blocked ради структуры. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: architect + builder — task domain; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Поддержанный ADR публичный API, переходные адаптеры при необходимости и regression evidence.
- Next step: METH-18 выбрала эту работу после подтверждения повторного использования или сложности сопровождения существующего API Tasks. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Не копировать business rules между сервисом и UI и не менять подсчёт прогресса/blocked ради структуры.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-12`

- Task: PAOS-METH-12
- Task name: Проверить архитектурные границы на Dashboard
- Status: planned
- Priority: P2
- Delivery group: A2
- Methodologies: FSD, Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-04, PAOS-METH-09
- Blocks: PAOS-METH-17
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-18
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Улучшить границу Dashboard одним обратимым изменением по ADR. Сохранить data flow и состав экранов, если для результата достаточно публичного API Tasks.
- Technical value: Улучшить границу Dashboard одним обратимым изменением по ADR. Сохранить data flow и состав экранов, если для результата достаточно публичного API Tasks.
- Product value: Проверить FSD на реальном ограниченном экране с измеряемыми контрактами.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `apps/web/src/features/tasks/model.ts`; `apps/web/src/ui/App.tsx`; `tests/web/ui-v3-dashboard.test.mts`; `tests/web/single-window/func-g01-dashboard-acceptance.mts`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Dashboard checkpoint с результатом import ratchet, измеренным изменением границ и evidence в существующем владельце.
- Acceptance criteria: PAOS-METH-12-AC01: Изменённая граница Dashboard использует минимальный явный API Tasks для востребованных селекторов, в том числе semanticStatus/isBlocked, с одной реализацией. Новые pages/widgets или entities/task появляются только по ADR и при доказанной необходимости. Services и F18 refresh semantics сохранены. PAOS-METH-12-AC02: F05 partial coverage, F06 queue numbering и F07 recent-task ordering сохранены на current source; обе themes и state matrix METH-03 проходят. PAOS-METH-12-AC03: Записаны before/after boundary edges, touched files, regression/visual results и rollback; отрицательный результат позволяет остановить rollout без переписывания остальных экранов.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Никаких новых metrics/synthetic numbers, API requests или performance claims без измерений; native qualification только если затронуты pinned sources. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — dashboard ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Dashboard checkpoint с результатом import ratchet, измеренным изменением границ и evidence в существующем владельце.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Никаких новых metrics/synthetic numbers, API requests или performance claims без измерений; native qualification только если затронуты pinned sources.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-13`

- Task: PAOS-METH-13
- Task name: При подтверждённой пользе улучшить границы Tasks и Workflows
- Status: planned
- Priority: P2
- Delivery group: A4
- Methodologies: FSD, Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: Нет.
- External references: PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-21
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Вынести выбранные METH-18 изменения в самостоятельные checkpoints и сохранить semantics редактора и очереди.
- Technical value: Вынести выбранные METH-18 изменения в самостоятельные checkpoints и сохранить semantics редактора и очереди.
- Product value: Изолировать два наиболее связанных пользовательских сценария и сохранить незавершённую работу.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/tasks/Editor.tsx`; `apps/web/src/features/workflows/WorkflowManager.tsx`; `apps/web/src/features/workflows/recipes/`; `apps/web/src/ui/App.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Выбранные Tasks и/или Workflows checkpoints с guards и обновлёнными owner docs при необходимости.
- Acceptance criteria: PAOS-METH-13-AC01: METH-18 явно выбрала Tasks и/или Workflows. Каждый экран имеет отдельные source hashes, проверки, visual evidence и обратимые изменения. Если выбраны оба и выявлена зависимость, Tasks идёт первым. PAOS-METH-13-AC02: Сохранены F03 new-task reset, F04 workflow drafts/CAS, dialog focus/8 tabs, preview/confirmation и queue controls; full F21 recovery не объявляется закрытой. PAOS-METH-13-AC03: Migrated consumers не зависят от соседних screen internals; перенесённые edges удалены из baseline exceptions, новые interaction features создаются только при реальной ответственности.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Shared App/navigation/labels changes последовательны; без новых workflow rules, DB migrations и scope расширения. Текущий запрос разрешает только планирование.
- Complexity: L
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — tasks, затем builder — workflows; sequential; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Выбранные Tasks и/или Workflows checkpoints с guards и обновлёнными owner docs при необходимости.
- Next step: METH-18 выбрала Tasks и/или Workflows после оценки Dashboard. Для каждого выбранного экрана отдельный checkpoint с сохранением draft, CAS, navigation и focus. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Shared App/navigation/labels changes последовательны; без новых workflow rules, DB migrations и scope расширения.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-14`

- Task: PAOS-METH-14
- Task name: Расширить FSD на team и skills после go-решения
- Status: planned
- Priority: P3
- Delivery group: A4
- Methodologies: FSD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: Нет.
- External references: PAOS-FUNC-11, PAOS-FUNC-12, PAOS-FUNC-16
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Применить проверенные boundaries к team/skills без реализации новых capabilities.
- Technical value: Применить проверенные boundaries к team/skills без реализации новых capabilities.
- Product value: Упростить использование task/dashboard primitives и безопасные следующие изменения каталогов.
- Scope: `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/features/skills/SkillGenerator.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Migrated team/skills по одному checkpoint; без обязательства мигрировать весь frontend.
- Acceptance criteria: PAOS-METH-14-AC01: Начало после go/bounded_go METH-18 для подтверждённого scope. Выбранные Team и Skills имеют собственные checkpoints и владельцев. PAOS-METH-14-AC02: Catalog/profile/edit/history/generation preview и unavailable usage сохранены; F11/F12/F16 остаются своими задачами, provider search не вызывается. PAOS-METH-14-AC03: Public APIs/boundary tests и scoped UI checks проходят; отчёт показывает удалённые legacy edges и оставшиеся exceptions.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: P3 необязательна для принятия пилота; не включать provider calls или asset promotion. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — team/skills ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Migrated team/skills по одному checkpoint; без обязательства мигрировать весь frontend.
- Next step: METH-18 выбрала Team и/или Skills по подтверждённой локальной проблеме. METH-13 учитывается только при фактической зависимости, выявленной в ADR. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: P3 необязательна для принятия пилота; не включать provider calls или asset promotion.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-15`

- Task: PAOS-METH-15
- Task name: Перенести оставшиеся выбранные экраны и завершить composition boundary
- Status: planned
- Priority: P3
- Delivery group: A4
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-18
- Blocks: Нет.
- External references: PAOS-FUNC-02, PAOS-FUNC-14, PAOS-FUNC-26, PAOS-FUNC-33, PAOS-FUNC-34
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Продолжить только одобренные screen moves и оставить App владельцем composition/session scope.
- Technical value: Продолжить только одобренные screen moves и оставить App владельцем composition/session scope.
- Product value: Снизить общий import coupling без потери history, documents и graph contexts.
- Scope: `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Operations.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Selected-screen checkpoints, App composition map и disposition остальных legacy exceptions.
- Acceptance criteria: PAOS-METH-15-AC01: Выбранные METH-18 Sessions, Artifacts, Graph или composition изменения выполняются по одному и в порядке подтверждённых зависимостей. Scope исключает новые Files/Database/usages функции, ownership conflicts с FUNC разрешаются до edits. PAOS-METH-15-AC02: App содержит composition/global providers/session selection, feature-local state вынесен только по подтверждённой необходимости; behavior и route IDs сохранены. PAOS-METH-15-AC03: В выбранном migrated scope нет неразрешённых legacy/deep/upward imports; compatibility adapters удаляются лишь после consumer inventory и regression checks.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не обещать full FSD по наличию папок; весь невыбранный scope остаётся legacy с явными границами. Текущий запрос разрешает только планирование.
- Complexity: L
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — один screen owner за раз; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Selected-screen checkpoints, App composition map и disposition остальных legacy exceptions.
- Next step: METH-18 выбрала конкретные экраны или изменение composition. Порядок определяется подтверждёнными зависимостями каждого экрана. Сверить выбранный scope и отдельно подтвердить полномочия на реализацию.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Не обещать full FSD по наличию папок; весь невыбранный scope остаётся legacy с явными границами.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-16`

- Task: PAOS-METH-16
- Task name: Уточнить условную поддержку методологий в Python plugin
- Status: planned
- Priority: P3
- Record kind: cross_track_reference
- Canonical implementation owner: [direction B](user-project-methodologies-2026-11-15.md); PAOS-PMETH-03, PAOS-PMETH-07, PAOS-PMETH-10, PAOS-PMETH-11, PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-22, PAOS-PMETH-23, PAOS-PMETH-26
- Acceptance semantics: Три прежних AC ниже сохранены как legacy coverage; выполнять их у canonical B owners. Здесь нет отдельного implementation status.
- Methodologies: Spec-DD, FSD, TDD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет; reference-only.
- Blocks: Нет.
- External references: PAOS-PMETH-03, PAOS-PMETH-07, PAOS-PMETH-10, PAOS-PMETH-11, PAOS-PMETH-16, PAOS-PMETH-17, PAOS-PMETH-22, PAOS-PMETH-23, PAOS-PMETH-26; reference-only, no hard dependency.
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сохранить прежний ID и AC, передав implementation ownership направлению B.
- Technical value: Перенести только доказанные уроки пилота в recommendations и verification evidence plugin.
- Product value: Целевой проект получает соразмерную рекомендацию вместо FSD mandate по названию folders.
- Scope: Только cross-track reference и AC mapping; прежние work locations сохранены в JSON reference. Не исполнять код из этой записи.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Один canonical owner продукта в B, без дублирующей задачи A.
- Acceptance criteria: PAOS-METH-16-AC01: Baseline/candidate cases: small frontend, growing coupled frontend, backend-only, native-only, misleading features folders, missing source и already-bounded frontend. PAOS-METH-16-AC02: RED/GREEN нового detection/routing behavior; рекомендации различают not_applicable/applicable_missing/present_unverified; отсутствие сведений не становится доказательством нарушения. PAOS-METH-16-AC03: Proposal не мутирует target, не активирует hooks/agents и не выдаёт folder detection за import/runtime proof; docs RU/EN и catalog/evals согласованы.
- Verification gates: V-REFERENCE; ссылки/AC mapping/status ownership и отсутствие прежних active edges.
- Risks / approval gates: Пилот этого repo не доказывает массовую пользу; prompts/routing требуют отдельного baseline сравнения, не новой установки. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: Нет исполнения/delegation из reference; owners назначены в B.
- Skills: python-design-patterns + python-code-style; advisory, только для будущего Python slice.
- Output artifacts: Сохранённый reference и links на B; implementation artifacts принадлежат B.
- Next step: Выбирать отдельно разрешённую PMETH-задачу из B; внутреннего METH-18 go не ждать.

#### Completion Report

- status: planned
- what was done: Planning record переведён в reference-only; implementation не начата.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Пилот этого repo не доказывает массовую пользу; prompts/routing требуют отдельного baseline сравнения, не новой установки.
- follow-up: Следить за coverage у B, не создавать вторую реализацию или второй status owner.

### Task `PAOS-METH-17`

- Task: PAOS-METH-17
- Task name: Принять технический пилот Dashboard и проверить контракты
- Status: planned
- Priority: P1
- Delivery group: A2
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-12
- Blocks: PAOS-METH-18
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22, PAOS-FUNC-23, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Свести evidence Dashboard и import ratchet к одной проверенной сборке и её исходникам. Учесть изменённые общие контракты и владельцев их проверок.
- Technical value: Свести evidence Dashboard и import ratchet к одной проверенной сборке и её исходникам. Учесть изменённые общие контракты и владельцев их проверок.
- Product value: Принять полезный ограниченный результат с честными gaps до масштабирования.
- Scope: `tests/web/contracts-boundaries.test.mts`; `tests/web/ui-v3-dashboard.test.mts`; `tests/web/single-window/func-g01-dashboard-acceptance.mts`; `docs/planning/methodology-improvement-2026-11-15.md`. Будущие участки работы, точные файлы уточняются по выбранному scope.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: AC/evidence reconciliation и verdict pilot_accepted/partial/blocked с причинами.
- Acceptance criteria: PAOS-METH-17-AC01: Каждый обязательный Dashboard AC и import rule имеет текущий check/receipt либо явный gap. Обязательные проверки затронутых контрактов проходят, findings имеют disposition. PAOS-METH-17-AC02: Проверены partial/error Dashboard, navigation/focus и contracts independence в затронутом scope. При изменении общих paths проверены scope/session и drafts. Recovery/backup receipts переиспользуются при неизменном релевантном состоянии. PAOS-METH-17-AC03: Review и решение ограничены техническим пилотом Dashboard. METH-07 и METH-10/11/13–15 не входят в условия приёмки. UI-12/F23 human acceptance и F19 full product E2E сохраняют своих владельцев.
- Verification gates: V-INTEGRATED; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Без release-readiness или full product acceptance claims; unresolved critical pilot gap запрещает accepted verdict. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + reviewer; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: AC/evidence reconciliation и verdict pilot_accepted/partial/blocked с причинами.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Без release-readiness или full product acceptance claims; unresolved critical pilot gap запрещает accepted verdict.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-18`

- Task: PAOS-METH-18
- Task name: Принять решение о дальнейшем rollout и обновить владельцев документации
- Status: planned
- Priority: P2
- Delivery group: A2
- Methodologies: ADD, FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-17
- Blocks: PAOS-METH-10, PAOS-METH-11, PAOS-METH-13, PAOS-METH-14, PAOS-METH-15
- External references: PAOS-FUNC-25
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Выбрать go/bounded_go/hold/stop отдельно для каждого следующего направления по evidence.
- Technical value: Выбрать go/bounded_go/hold/stop отдельно для каждого следующего направления по evidence.
- Product value: Масштабировать полезное и остановить неподтверждённые усложнения.
- Scope: `docs/architecture/decisions/`; `docs/frontend/`; `docs/testing/`; `docs/sources/registry.md`; `PLAN.md`; `RUNLOG.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Reviewable rollout decision в существующем ADR/evidence owner и компактный handoff.
- Acceptance criteria: PAOS-METH-18-AC01: Сравнены baseline и Dashboard pilot по unauthorized edges, regression findings и change/review effort. ADD outcome metrics учитываются отдельно только при доступном сопоставимом METH-07 evidence. PAOS-METH-18-AC02: Для выбранных METH-10/11/13–15 записаны собственные scope, owner, measurable benefit, go/bounded_go/hold/stop и rollback. Без измеренного основания расширение можно остановить на Dashboard. B принимает независимое решение. PAOS-METH-18-AC03: Обновлены только изменившиеся docs/registry/control-plane owners; active rules изменяются только отдельным разрешённым slice, existing FUNC/Web статусы и release gates сохранены.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Go-решение не является автоматической авторизацией implementation/provider/install/Git или deployment. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: product-manager + architect; owner decision; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Reviewable rollout decision в существующем ADR/evidence owner и компактный handoff.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Go-решение не является автоматической авторизацией implementation/provider/install/Git или deployment.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

