# Product-Agent OS — план улучшений по методологиям

Source status: repository_source / owner_requested_planning / proposed_methodology_improvements; implementation_not_started.
Дата: 15.11.2026. Schema version: task_matrix_plan_v1. Timezone: Europe/Moscow.

## Цель, полномочия и владельцы

Подготовлены 18 конкретных задач для Spec-Driven Development (Spec-DD), Design-Driven Development (Design-DD), Test-Driven Development (TDD), Agentic-Driven Development (ADD) и постепенного Feature-Sliced Design (FSD). Все задачи имеют статус planned и pending_execution_timestamp. Разрешено только создание этого плана, JSON, полного EN-перевода и их planning/control-plane/source pointers. Реализация, новые активные инструкции, runtime/browser/provider, установки, Git и публикация этим запросом не разрешены.

[JSON-состояние](methodology-improvement-2026-11-15.json) владеет status/priority/dependencies; RU/EN карточки содержат согласованное описание и AC. Обновлять их совместно; таблицы — индекс, не отдельная очередь. [English](methodology-improvement-2026-11-15.en.md). METH описывает улучшение способа разработки; функциональный scope и статусы остаются у FUNC/Web/V3. Создание плана не закрывает ни одну METH-задачу.

## Исходное состояние и доказательства

Source snapshot: git HEAD `35458110145d928b9b14d9312b60d852f11f6e88`; hashes семи прочитанных implementation/test owners находятся в JSON. Снимок не является release qualification. Во время планирования выполнено чтение исходников/владельцев; прежние tests/browser/native receipts заново не выполнялись.

- [FUNC-G01](functional-remediation-2026-11-15.md#func-g01-results) на этом baseline содержит 7 implemented: F01/F03–F08; другие 27 FUNC planned. Это состояние владельца, не новый результат текущего запуска. Повторно планировать исправления drafts/dashboard/contracts не требуется.
- Spec-DD уже отражён в [требованиях и capability model](../product/capabilities.md) и конкретных task matrices; [TEST](../../TEST.md) и [EVALS](../../EVALS.md) владеют выбором проверок и claim ceiling.
- Design-DD имеет [DESIGN](../../DESIGN.md), V3 coverage и [план внедрения](2026-11-13-v3-ui-implementation-plan.md). Исторический V3 review выявил разрыв composition coverage; это не утверждение о новом дефекте текущего build.
- TDD поддержан правилами и отдельными historical RED/GREEN receipts; готовый набор тестов не доказывает test-first для каждой задачи.
- ADD имеет build/review/handoff contracts и разделение ownership. Улучшение качества/стоимости agentic работы требует сопоставимого baseline, а не подсчёта ролей.
- Frontend сгруппирован по features, но dashboard/tasks/team/workflows используют внутренние соседние модули. Строгий FSD не доказан; [contracts-boundaries test](../../tests/web/contracts-boundaries.test.mts) защищает application boundary, а не все FSD imports. METH-09 должен явно включить TSX и aliases, чтобы новая проверка не имела скрытого coverage gap.

Исходники: `apps/web/src/features/dashboard/model.ts`, `tasks/TaskManager.tsx`, `workflows/WorkflowManager.tsx`, `team/TeamManager.tsx`, `apps/web/src/ui/App.tsx`; Python owner `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`. Перед будущими edits перечитать их актуальное состояние.

Методологические первоисточники, проверенные в предшествующем анализе 15.11.2026: [TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html), [FSD layers](https://feature-sliced.design/docs/reference/layers), [FSD public API](https://feature-sliced.design/docs/reference/public-api), [Spec Kit process](https://github.github.io/spec-kit/quickstart.html), [IBM human-centered design](https://www.ibm.com/training/enterprise-design-thinking/framework), [AWS AI-DLC](https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/). ADD/Design-DD здесь — явно заданные рабочие подходы; план не утверждает их единую отраслевую стандартизацию. Предложения и оценки ниже — project-authored, не результаты внешних исследований.

## Приоритеты, этапы и зависимости

P1 — защита контрактов и достоверность приёмки; P2 — основной ограниченный пилот и улучшение процесса; P3 — optional scale после evidence. P1 не означает production incident. Номер задачи не задаёт порядок.

| Этап | Задачи | Условие выхода |
| --- | --- | --- |
| A. Baseline и контракты | METH-01–06 | Владельцы/AC/states/TDD gaps и bounded agent contract определены; активные правила меняются лишь в будущих отдельных slices |
| B. FSD foundation | METH-08–11 | Принятое архитектурное решение, import ratchet, минимальные shared/entity APIs; без массового move |
| C. Два последовательных пилота | METH-12, METH-13; затем METH-07 | Dashboard → tasks → workflows; каждый checkpoint обратим; outcome comparison имеет честный ceiling |
| D. Проверка и решение | METH-17 → METH-18 | Bounded pilot verdict и отдельное go/bounded_go/hold/stop |
| E. Необязательное расширение | METH-14–16 | Только выбранная область после go; не блокирует приёмку пилота |

Ранний старт: METH-01; затем независимые ветки METH-02 и METH-08. Критическая структурная цепочка: 01 → 08/05 → 09 → 10 → 11 → 12 → 13 → 17 → 18. Design-ветка 02 → 03 → 04 входит в 12. Agentic-ветка 06 + 12 → 07 входит в 17. Полный DAG определяется depends_on в JSON; Blocks — обратное ребро. Для начала задачи достаточно её task dependencies, завершение целого этапа не является новым prerequisite.

## Совмещение с действующим backlog

| Existing owner | Как используется | Что не дублируется |
| --- | --- | --- |
| F01/F03–F08, FUNC-G01 | Baseline и regression protections | Исправления, native qualification и их completion statuses |
| F02/F28 | Reference для будущих artifact traceability/canonical paths | Реализация task↔artifact links и inventory; METH-02 не ждёт F28 |
| F11/F12/F16 | Ограничения metrics/team/skills | Telemetry, external search и real loaded-profile proof |
| F18/F20/F30 | Data-refresh/performance/engine boundaries | Изменение refresh semantics, benchmark или обязательный dependency-cruiser install |
| F19/F21/F22/F23/F24, UI-12 | Переиспользуемые сценарии/evidence и отдельная full/human приёмка | Полный E2E, recovery, backup/restore, feature availability и human acceptance |
| F25, DOCS-01–16 | Canonical docs/status ownership | Повторное создание guides или изменение feature task-state |
| F14/F26–34, M5 | Запрет расширить migration scope | Новые Files/Map/Database/usages, hosting/auth/team capabilities |

Ссылки external_refs — references и ownership constraints, а не новые рёбра чужого DAG. Hard prerequisite текущего FSD pilot: F08 уже implemented; перед edits проверить это и актуальность F01 только при затрагивании pinned runtime sources. Shared file conflict — последовательная запись, не новая функциональная зависимость.

## Предлагаемые границы постепенного FSD

Это proposal для METH-08, а не уже принятый ADR:

- `app` — composition/global providers/session/project scope; `pages` — screen composition; `widgets` — только повторно используемые самостоятельные блоки.
- `features` — реальные пользовательские interactions; `entities/task` — task projection/selectors/presentation; `shared` — недоменные primitives/infrastructure.
- Не создавать пустые слои; сначала выделить public APIs и разрешённые imports, затем перемещать подтверждённый scope. Общие business contracts сохраняются в `packages/contracts`, FSD не применяется к Python/backend.
- Legacy→new compatibility bridges допустимы с одним implementation/state и removal owner; migrated code не импортирует legacy internals. Нет blanket exceptions и wildcard exports.
- Начальная enforcement — no new violations относительно revision-pinned legacy baseline; migrated scope имеет zero unresolved violations. Ratchet ужесточается после каждого принятого checkpoint.
- Возможен stop после dashboard или после tasks/workflows: сохранить работающий пилот и явный legacy remainder. Миграция остальных экранов не является условием выпуска функциональных исправлений.

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

## Проверка подготовки плана — 15.11.2026

Проверена подготовка planning artifact, а не выполнение METH-задач. Review mode: self_review; independent review и runtime acceptance не заявлены.

- `python -B plugins/product-agent-os/scripts/validate_task_matrix.py docs/planning/methodology-improvement-2026-11-15.md` — ok, errors=[]; EN counterpart — такой же результат.
- `python -B tools/check_docs.py --paths` с девятью изменёнными Markdown owners (оба новых плана, оба planning index, оба registry, REQUIREMENTS/PLAN/RUNLOG) — OK: 9 changed Markdown source(s); site/archive не проверялись.
- Локальные read-only assertions через `python -B -`: 18 уникальных planned задач, 54 bilingual AC, 27 reciprocal dependency edges; DAG acyclic; RU/EN/JSON titles/status/priority/dependencies/AC/profiles согласованы; P3 не блокирует METH-17/18; METH-14 требует rollout decision METH-18.
- Preservation: hashes 19 existing source/contract owners не изменены; удаление только добавленных planning sections восстанавливает исходные bytes семи изменённых existing documents. Чужие session markers и параллельные workstreams не затрагивались.
- `git diff --check` — exit 0. Application tests/build/browser/native/provider и generated site не запускались. Все 18 implementation timestamps остаются pending_execution_timestamp.
- Control-plane sync: updated REQUIREMENTS/PLAN/RUNLOG и planning/source pointers; TEST/EVALS/prod_test no_change_needed — active verification policy и historical execution evidence не менялись.

## Индекс задач

| ID | Приоритет | Подход | Задача | Depends on |
| --- | --- | --- | --- | --- |
| PAOS-METH-01 | P1 | Spec-DD, ADD | Зафиксировать baseline и владельцев улучшений | — |
| PAOS-METH-02 | P1 | Spec-DD | Связать требования, исходники и проверки в двух пилотных сценариях | PAOS-METH-01 |
| PAOS-METH-03 | P1 | Design-DD, Spec-DD | Уточнить design-контракт состояний пилота | PAOS-METH-02 |
| PAOS-METH-04 | P1 | Design-DD, TDD | Проверять композицию и поведение интерфейса по design-контракту | PAOS-METH-03 |
| PAOS-METH-05 | P1 | TDD, Spec-DD | Закрыть пробелы TDD и regression evidence для критических контрактов | PAOS-METH-01, PAOS-METH-02 |
| PAOS-METH-06 | P2 | ADD, Spec-DD | Упростить контракты agent slice и handoff по baseline eval | PAOS-METH-01, PAOS-METH-02, PAOS-METH-05 |
| PAOS-METH-07 | P2 | ADD | Измерить результат agentic-пилота на сопоставимых задачах | PAOS-METH-06, PAOS-METH-12 |
| PAOS-METH-08 | P1 | FSD, Design-DD | Спроектировать постепенные границы FSD и переходный ADR | PAOS-METH-01 |
| PAOS-METH-09 | P1 | FSD, TDD | Добавить инкрементальную проверку frontend imports | PAOS-METH-05, PAOS-METH-08 |
| PAOS-METH-10 | P2 | FSD | Выделить необходимые shared UI и инфраструктурные модули | PAOS-METH-09 |
| PAOS-METH-11 | P2 | FSD, Spec-DD | Выделить frontend entities/task и публичные интерфейсы домена | PAOS-METH-10 |
| PAOS-METH-12 | P2 | FSD, Design-DD, Spec-DD | Перевести dashboard на FSD-пилот | PAOS-METH-02, PAOS-METH-04, PAOS-METH-11 |
| PAOS-METH-13 | P2 | FSD, Design-DD, TDD | Перевести tasks и workflows отдельными совместимыми срезами | PAOS-METH-12 |
| PAOS-METH-14 | P3 | FSD, ADD | Расширить FSD на team и skills после go-решения | PAOS-METH-13, PAOS-METH-18 |
| PAOS-METH-15 | P3 | FSD, Design-DD | Перенести оставшиеся выбранные экраны и завершить composition boundary | PAOS-METH-14 |
| PAOS-METH-16 | P3 | Spec-DD, FSD, TDD, ADD | Уточнить условную поддержку методологий в Python plugin | PAOS-METH-05, PAOS-METH-18 |
| PAOS-METH-17 | P1 | Spec-DD, Design-DD, TDD, ADD, FSD | Принять интегрированный пилот и проверить сохранность контрактов | PAOS-METH-07, PAOS-METH-13 |
| PAOS-METH-18 | P2 | ADD, FSD, Spec-DD | Принять решение о дальнейшем rollout и обновить владельцев документации | PAOS-METH-17 |

## Подробные карточки задач

### Task `PAOS-METH-01`

- Task: PAOS-METH-01
- Task name: Зафиксировать baseline и владельцев улучшений
- Status: planned
- Priority: P1
- Methodologies: Spec-DD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет.
- Blocks: PAOS-METH-02, PAOS-METH-05, PAOS-METH-06, PAOS-METH-08
- External references: PAOS-FUNC-01, PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-08, PAOS-FUNC-25
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Снять актуальный source/contract/test baseline и устранить дублирование с FUNC, Web и V3.
- Technical value: Снять актуальный source/contract/test baseline и устранить дублирование с FUNC, Web и V3.
- Product value: Сохранить уже исправленное поведение и назначить одного владельца каждой новой работы.
- Scope: `docs/planning/methodology-improvement-2026-11-15.md`; `docs/planning/methodology-improvement-2026-11-15.json`; `docs/frontend/index.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Baseline и карта ownership в этой карточке; без нового глобального реестра.
- Acceptance criteria: PAOS-METH-01-AC01: Зафиксированы revision, локальные изменения, imports и действующие проверки web/plugin; прежние receipts помечены своей датой. PAOS-METH-01-AC02: Для каждой METH-карточки указано own/reuse/reference относительно FUNC/Web/V3; существующие AC и статусы не скопированы в новую владеющую очередь. PAOS-METH-01-AC03: Назначены file/subsystem owners и точки последовательной работы; исходные F01/F03–F08 проверены по текущему владельцу, а не переоткрыты автоматически.
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
- Task name: Связать требования, исходники и проверки в двух пилотных сценариях
- Status: planned
- Priority: P1
- Methodologies: Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-03, PAOS-METH-05, PAOS-METH-06, PAOS-METH-12
- External references: PAOS-FUNC-02, PAOS-FUNC-25
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Использовать существующие владельцы требований для dashboard coverage и сохранения task/workflow drafts.
- Technical value: Использовать существующие владельцы требований для dashboard coverage и сохранения task/workflow drafts.
- Product value: Проверять результат по пользовательскому контракту и быстро находить недостающую проверку.
- Scope: `docs/product/capabilities.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Две traceability-таблицы в существующих product/testing owners и ссылки на AC в плане.
- Acceptance criteria: PAOS-METH-02-AC01: В каждой из двух цепочек criterion → canonical owner → source → test/browser scenario → receipt либо explicit gap; все применимые критерии пилота покрыты строкой. PAOS-METH-02-AC02: Неполное portfolio не выглядит полным, draft не теряется и не переносится в новый объект; пустые/error/stale сценарии названы явно. PAOS-METH-02-AC03: Одна изменённая предпосылка API/данных отражена в основном владельце, mirrors согласованы; traceability не реализует F02 и не ждёт её F28.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не менять продуктовый scope и статусы FUNC; gaps не выдавать за passed. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: product-manager + tester; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Две traceability-таблицы в существующих product/testing owners и ссылки на AC в плане.
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
- Methodologies: Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02
- Blocks: PAOS-METH-04
- External references: PAOS-FUNC-24, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сопоставить dashboard и task/workflow editing с утверждённым V3 и реальными возможностями API.
- Technical value: Сопоставить dashboard и task/workflow editing с утверждённым V3 и реальными возможностями API.
- Product value: Устранить разрыв между утверждённым макетом, данными и реальным сценарием пользователя.
- Scope: `DESIGN.md`; `design/2026-11-13-v3/coverage.json`; `design/2026-11-13-v3/task-field-map.md`; `docs/frontend/state-management.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Дополнение существующих state/coverage owners; новые макеты только для отсутствующего необходимого состояния.
- Acceptance criteria: PAOS-METH-03-AC01: Для пилота описаны default/loading/empty/error/partial/stale/dirty/validation/confirmation с обоими themes и keyboard/focus, либо обоснованное not_applicable. PAOS-METH-03-AC02: Источник, единицы и unavailable для показателей явные; synthetic usage не становится данными приложения, F11 не реализуется этой задачей. PAOS-METH-03-AC03: Design differences получают disposition: исправить/предложить владельцу/принятый gap; согласование макета не закрывает UI-12 или human acceptance.
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
- Methodologies: Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-03
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-19, PAOS-FUNC-24, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Расширить существующий UI harness для пилота без второй системы screenshot/evidence.
- Technical value: Расширить существующий UI harness для пилота без второй системы screenshot/evidence.
- Product value: Ловить композиционные и интерактивные регрессии, которые не выявляет один overflow/contrast check.
- Scope: `tests/web/single-window/ui-v3-scenario.mts`; `tests/web/ui-v3-dashboard.test.mts`; `design/2026-11-13-v3/implementation-evidence.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Пилотные проверки в существующем harness и evidence в прежнем владельце.
- Acceptance criteria: PAOS-METH-04-AC01: Проверяются current-build screenshots пилота в двух themes, открытие/закрытие редактора, focus return, сохранение draft при навигации и partial/error feedback. PAOS-METH-04-AC02: Проверки обнаруживают намеренно изменённую fixture геометрию/состояние; thresholds и стабильные области обоснованы, обновление baseline явно reviewable. PAOS-METH-04-AC03: Расхождения сравниваются с design owner; automated technical pass отделён от human acceptance, receipt привязан к hashes build/harness.
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
- Methodologies: TDD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01, PAOS-METH-02
- Blocks: PAOS-METH-06, PAOS-METH-09, PAOS-METH-16
- External references: PAOS-FUNC-21, PAOS-FUNC-22
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Разделить текущие защиты, недостающие regression cases и правила RED для следующего изменения поведения.
- Technical value: Разделить текущие защиты, недостающие regression cases и правила RED для следующего изменения поведения.
- Product value: Не потерять draft/retry/recovery/approval invariants при рефакторинге и изменениях tooling.
- Scope: `TEST.md`; `tests/web/ui-draft-autosave.test.mts`; `tests/web/contracts-boundaries.test.mts`; `tests/product_agent_os/test_methodology_audit.py`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Компактная risk/test карта в TEST и текущих task evidence; только недостающие meaningful tests.
- Acceptance criteria: PAOS-METH-05-AC01: Карта risk → invariant → lowest reliable check покрывает draft conflict/lost ACK, import boundary, Stop/recovery, backup/restore и approval routing; существующие тесты переиспользованы. PAOS-METH-05-AC02: Для нового TS boundary behavior METH-09 и нового Python routing behavior METH-16 определены ожидаемые RED причины и минимальный GREEN; evidence записывается при их реализации. PAOS-METH-05-AC03: Setup/import failures не считаются RED; behavior-preserving moves используют characterization/regression без искусственно сломанного production code; F21/F22 остаются отдельными владельцами полного recovery scope.
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
- Methodologies: ADD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01, PAOS-METH-02, PAOS-METH-05
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
- Methodologies: ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-06, PAOS-METH-12
- Blocks: PAOS-METH-17
- External references: PAOS-FUNC-11, PAOS-FUNC-23
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Сравнить baseline и candidate на одном наборе задач, отделив orchestration correctness от качества решения.
- Technical value: Сравнить baseline и candidate на одном наборе задач, отделив orchestration correctness от качества решения.
- Product value: Принимать решение о процессе по качеству результата и затратам, а не числу агентов или tests.
- Scope: `EVALS.md`; `docs/testing/index.md`; `docs/planning/methodology-improvement-2026-11-15.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Сравнение baseline/candidate в evidence карточки; отдельный verdict correctness/quality/cost.
- Acceptance criteria: PAOS-METH-07-AC01: Одинаковые task inputs/AC/revision и доступный runtime; фиксируются accepted/reopened, repair cycles, owner interventions и elapsed с provenance. PAOS-METH-07-AC02: Tokens/cost приводятся только при достоверном источнике; unavailable не заменяется нулём; F11 telemetry не реализуется ради этого пилота. PAOS-METH-07-AC03: Если actual-agent сравнение недоступно без нового разрешения, результат ограничен deterministic routing; model-quality benefit остаётся insufficient_evidence и не разрешает promotion.
- Verification gates: V-ADD; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Без автоматических provider calls, raw private chats и неподтверждённых productivity claims; human acceptance остаётся отдельной. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + product-manager; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Сравнение baseline/candidate в evidence карточки; отдельный verdict correctness/quality/cost.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-01
- Blocks: PAOS-METH-09
- External references: PAOS-FUNC-08, PAOS-FUNC-30
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Выбрать минимальные слои и владельцев по реальным imports и продуктовым сценариям.
- Technical value: Выбрать минимальные слои и владельцев по реальным imports и продуктовым сценариям.
- Product value: Сделать следующую миграцию проверяемой без полного rewrite и лишних папок.
- Scope: `docs/architecture/decisions/`; `docs/frontend/index.md`; `apps/web/src/ui/App.tsx`; `apps/web/src/features/`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Один proposed ADR в существующем decisions-каталоге и migration map; номер выбрать после актуального inventory.
- Acceptance criteria: PAOS-METH-08-AC01: ADR сравнивает оставить feature folders, улучшить только boundaries и частично внедрить FSD; решение опирается на coupling, тестируемость и стоимость переноса. PAOS-METH-08-AC02: Предложена карта App composition → pages/widgets при необходимости → interaction features → entities → shared; whole-screen TaskManager/Dashboard не названы features автоматически. PAOS-METH-08-AC03: Зафиксированы public APIs, legacy exception list с owner/removal task, направление bridge legacy→new, fallback/rollback и критерий достаточности; FSD не распространяется на backend/Python.
- Verification gates: V-PLAN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: ADR в этом плане — будущий deliverable, не уже принятое архитектурное решение; F30 не является обязательной зависимостью. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: architect; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Один proposed ADR в существующем decisions-каталоге и migration map; номер выбрать после актуального inventory.
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
- Methodologies: FSD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05, PAOS-METH-08
- Blocks: PAOS-METH-10
- External references: PAOS-FUNC-08, PAOS-FUNC-30
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Развить существующий AST boundary check для migrated scopes и запрета новых нарушений.
- Technical value: Развить существующий AST boundary check для migrated scopes и запрета новых нарушений.
- Product value: Остановить рост связанности до начала перемещений, не блокируя весь legacy.
- Scope: `tests/web/contracts-boundaries.test.mts`; `apps/web/package.json`; `apps/web/src/`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Расширение существующего parser/check и synthetic cases; новая dependency только при доказанной необходимости.
- Acceptance criteria: PAOS-METH-09-AC01: RED/GREEN fixtures покрывают .ts/.tsx/.mts, type imports/reexports/literal dynamic imports и настроенные aliases; unmapped alias является явным gap/failure, не silently skipped. PAOS-METH-09-AC02: В migrated scopes отклоняются upward/same-layer/deep imports и циклы по принятому ADR; допустимые entity cross-imports только через согласованный API, не blanket exception. PAOS-METH-09-AC03: Текущие legacy edges revision-pinned и не растут; перенесённый модуль удаляется из exceptions; действующие contracts→apps и backend→frontend запреты сохраняются.
- Verification gates: V-BOUNDARY; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не прятать реальные imports за exclusions; baseline обновлять reviewable. Не устанавливать dependency-cruiser автоматически. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: tester + builder; proposed ownership, сейчас delegation=0.
- Skills: documentation-and-adrs; дополнительные skills выбирать по фактическому изменению.
- Output artifacts: Расширение существующего parser/check и synthetic cases; новая dependency только при доказанной необходимости.
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
- Methodologies: FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-09
- Blocks: PAOS-METH-11
- External references: Нет; текущий план — владелец.
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Извлечь переиспользуемые недоменные primitives и infrastructure, нужные пилоту.
- Technical value: Извлечь переиспользуемые недоменные primitives и infrastructure, нужные пилоту.
- Product value: Убрать зависимость общих представлений от внутренних task/graph screens.
- Scope: `apps/web/src/ui/Icon.tsx`; `apps/web/src/ui/Modal.tsx`; `apps/web/src/features/tasks/CommentMarkdown.tsx`; `apps/web/src/locales/`; `apps/web/src/features/graph/GraphViews.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Минимальный shared public API, compatibility bridges и обновлённая migration map.
- Acceptance criteria: PAOS-METH-10-AC01: В shared попадают только используемые primitives, safe Markdown/rendering и i18n infrastructure; task status rules и task-specific labels остаются у домена. PAOS-METH-10-AC02: Mermaid/graph renderer разделён на generic rendering и domain mapping только при подтверждённом reuse; no wildcard public exports, frontend→backend зависимости не добавлены. PAOS-METH-10-AC03: Compatibility reexports однонаправленные, implementation/state единственные; прежние theme/focus/Markdown-safety/reduced-motion regressions проходят.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Это behavior-preserving move; не менять visual design, sanitize policy, API или данные. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — shared frontend ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Минимальный shared public API, compatibility bridges и обновлённая migration map.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Task name: Выделить frontend entities/task и публичные интерфейсы домена
- Status: planned
- Priority: P2
- Methodologies: FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-10
- Blocks: PAOS-METH-12
- External references: PAOS-FUNC-08
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Разделить task presentation/model selectors, interaction state и server-owned contracts.
- Technical value: Разделить task presentation/model selectors, interaction state и server-owned contracts.
- Product value: Dashboard и team используют стабильный task API вместо deep imports в task screen.
- Scope: `apps/web/src/features/tasks/model.ts`; `apps/web/src/features/tasks/labels.ts`; `apps/web/src/features/dashboard/model.ts`; `packages/contracts/issues/task-profile.ts`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: entities/task public API по ADR, переходные adapters и domain regression evidence.
- Acceptance criteria: PAOS-METH-11-AC01: Reusable selectors/status presentation/task labels имеют один frontend domain owner; editor draft и commands остаются interaction-owned, backend authority не дублируется. PAOS-METH-11-AC02: packages/contracts остаётся application-independent, не импортирует React/UI; типы и decode/persistence semantics F08 сохраняются. PAOS-METH-11-AC03: Потребители пилота используют явный public API; tests semanticStatus/isBlocked/aggregation и contracts boundaries проходят, legacy bridges имеют removal owner.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не копировать business rules между сервисом и UI и не менять подсчёт прогресса/blocked ради структуры. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: architect + builder — task domain; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: entities/task public API по ADR, переходные adapters и domain regression evidence.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Task name: Перевести dashboard на FSD-пилот
- Status: planned
- Priority: P2
- Methodologies: FSD, Design-DD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-02, PAOS-METH-04, PAOS-METH-11
- Blocks: PAOS-METH-07, PAOS-METH-13
- External references: PAOS-FUNC-05, PAOS-FUNC-06, PAOS-FUNC-07, PAOS-FUNC-18
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Перенести dashboard composition в минимальные pages/widgets по ADR, сохранив существующий data flow.
- Technical value: Перенести dashboard composition в минимальные pages/widgets по ADR, сохранив существующий data flow.
- Product value: Проверить FSD на реальном ограниченном экране с измеряемыми контрактами.
- Scope: `apps/web/src/features/dashboard/Dashboard.tsx`; `apps/web/src/features/dashboard/model.ts`; `apps/web/src/ui/App.tsx`; `tests/web/ui-v3-dashboard.test.mts`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Один migrated dashboard, evidence в этой карточке и frontend owner docs.
- Acceptance criteria: PAOS-METH-12-AC01: У migrated dashboard нет imports в legacy feature internals; selectors берутся из domain public API, services и F18 refresh behavior не меняются. PAOS-METH-12-AC02: F05 partial coverage, F06 queue numbering и F07 recent-task ordering сохранены на current source; обе themes и state matrix METH-03 проходят. PAOS-METH-12-AC03: Записаны before/after boundary edges, touched files, regression/visual results и rollback; отрицательный результат позволяет остановить rollout без переписывания остальных экранов.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Никаких новых metrics/synthetic numbers, API requests или performance claims без измерений; native qualification только если затронуты pinned sources. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — dashboard ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Один migrated dashboard, evidence в этой карточке и frontend owner docs.
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
- Task name: Перевести tasks и workflows отдельными совместимыми срезами
- Status: planned
- Priority: P2
- Methodologies: FSD, Design-DD, TDD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-12
- Blocks: PAOS-METH-14, PAOS-METH-17
- External references: PAOS-FUNC-03, PAOS-FUNC-04, PAOS-FUNC-21
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Отделить screen composition от editing/queue interactions без изменения task/workflow semantics.
- Technical value: Отделить screen composition от editing/queue interactions без изменения task/workflow semantics.
- Product value: Изолировать два наиболее связанных пользовательских сценария и сохранить незавершённую работу.
- Scope: `apps/web/src/features/tasks/TaskManager.tsx`; `apps/web/src/features/tasks/Editor.tsx`; `apps/web/src/features/workflows/WorkflowManager.tsx`; `apps/web/src/features/workflows/recipes/`; `apps/web/src/ui/App.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Два последовательных migrated checkpoints и обновлённые domain/state docs.
- Acceptance criteria: PAOS-METH-13-AC01: Сначала tasks checkpoint, затем workflows checkpoint; каждый имеет собственные source hashes, affected tests, visual evidence и обратимые hunks. PAOS-METH-13-AC02: Сохранены F03 new-task reset, F04 workflow drafts/CAS, dialog focus/8 tabs, preview/confirmation и queue controls; full F21 recovery не объявляется закрытой. PAOS-METH-13-AC03: Migrated consumers не зависят от соседних screen internals; перенесённые edges удалены из baseline exceptions, новые interaction features создаются только при реальной ответственности.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Shared App/navigation/labels changes последовательны; без новых workflow rules, DB migrations и scope расширения. Текущий запрос разрешает только планирование.
- Complexity: L
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — tasks, затем builder — workflows; sequential; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Два последовательных migrated checkpoints и обновлённые domain/state docs.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Methodologies: FSD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-13, PAOS-METH-18
- Blocks: PAOS-METH-15
- External references: PAOS-FUNC-11, PAOS-FUNC-12, PAOS-FUNC-16
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Применить проверенные boundaries к team/skills без реализации новых capabilities.
- Technical value: Применить проверенные boundaries к team/skills без реализации новых capabilities.
- Product value: Упростить использование task/dashboard primitives и безопасные следующие изменения каталогов.
- Scope: `apps/web/src/features/team/TeamManager.tsx`; `apps/web/src/features/skills/SkillGenerator.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Migrated team/skills по одному checkpoint; без обязательства мигрировать весь frontend.
- Acceptance criteria: PAOS-METH-14-AC01: Начало только после METH-18 go для этой области; team и skills имеют отдельные checkpoints и owners. PAOS-METH-14-AC02: Catalog/profile/edit/history/generation preview и unavailable usage сохранены; F11/F12/F16 остаются своими задачами, provider search не вызывается. PAOS-METH-14-AC03: Public APIs/boundary tests и scoped UI checks проходят; отчёт показывает удалённые legacy edges и оставшиеся exceptions.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: P3 необязательна для принятия пилота; не включать provider calls или asset promotion. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — team/skills ownership; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Migrated team/skills по одному checkpoint; без обязательства мигрировать весь frontend.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Methodologies: FSD, Design-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-14
- Blocks: Нет.
- External references: PAOS-FUNC-02, PAOS-FUNC-14, PAOS-FUNC-26, PAOS-FUNC-33, PAOS-FUNC-34
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Продолжить только одобренные screen moves и оставить App владельцем composition/session scope.
- Technical value: Продолжить только одобренные screen moves и оставить App владельцем composition/session scope.
- Product value: Снизить общий import coupling без потери history, documents и graph contexts.
- Scope: `apps/web/src/features/sessions/SessionsCatalog.tsx`; `apps/web/src/features/artifacts/ArtifactExplorer.tsx`; `apps/web/src/features/graph/GraphExplorer.tsx`; `apps/web/src/ui/App.tsx`; `apps/web/src/ui/Operations.tsx`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Selected-screen checkpoints, App composition map и disposition остальных legacy exceptions.
- Acceptance criteria: PAOS-METH-15-AC01: sessions → artifacts → graph выполняются по одному; новый Files/Database/usages функционал не включается, ownership conflicts с FUNC разрешаются до edits. PAOS-METH-15-AC02: App содержит composition/global providers/session selection, feature-local state вынесен только по подтверждённой необходимости; behavior и route IDs сохранены. PAOS-METH-15-AC03: В выбранном migrated scope нет неразрешённых legacy/deep/upward imports; compatibility adapters удаляются лишь после consumer inventory и regression checks.
- Verification gates: V-WEB; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Не обещать full FSD по наличию папок; весь невыбранный scope остаётся legacy с явными границами. Текущий запрос разрешает только планирование.
- Complexity: L
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: builder — один screen owner за раз; proposed ownership, сейчас delegation=0.
- Skills: build-web-apps:frontend-testing-debugging; только для будущей UI проверки; архитектурные решения по ADR.
- Output artifacts: Selected-screen checkpoints, App composition map и disposition остальных legacy exceptions.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

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
- Methodologies: Spec-DD, FSD, TDD, ADD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-05, PAOS-METH-18
- Blocks: Нет.
- External references: Нет; текущий план — владелец.
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Перенести только доказанные уроки пилота в recommendations и verification evidence plugin.
- Technical value: Перенести только доказанные уроки пилота в recommendations и verification evidence plugin.
- Product value: Целевой проект получает соразмерную рекомендацию вместо FSD mandate по названию folders.
- Scope: `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/assets/methodology/methodology-catalog.json`; `tests/product_agent_os/test_methodology_audit.py`; `docs/methodologies/frontend.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Один focused plugin slice с representative eval comparison; без blanket methodology requirement.
- Acceptance criteria: PAOS-METH-16-AC01: Baseline/candidate cases: small frontend, growing coupled frontend, backend-only, native-only, misleading features folders, missing source и already-bounded frontend. PAOS-METH-16-AC02: RED/GREEN нового detection/routing behavior; рекомендации различают not_applicable/applicable_missing/present_unverified; отсутствие сведений не становится доказательством нарушения. PAOS-METH-16-AC03: Proposal не мутирует target, не активирует hooks/agents и не выдаёт folder detection за import/runtime proof; docs RU/EN и catalog/evals согласованы.
- Verification gates: V-PLUGIN; профиль выше; текущий маршрут TEST имеет приоритет; запуск при будущей реализации.
- Risks / approval gates: Пилот этого repo не доказывает массовую пользу; prompts/routing требуют отдельного baseline сравнения, не новой установки. Текущий запрос разрешает только планирование.
- Complexity: M
- Estimated execution time: Оценить после актуального discovery и выбора bounded slice; календарное обещание не дано.
- Agents: plugin-runtime-builder + tester; proposed ownership, сейчас delegation=0.
- Skills: python-design-patterns + python-code-style; advisory, только для будущего Python slice.
- Output artifacts: Один focused plugin slice с representative eval comparison; без blanket methodology requirement.
- Next step: Проверить dependencies и текущие source owners; запросить/получить отдельный scope реализации выбранной задачи.

#### Completion Report

- status: planned
- what was done: Реализация не начата; сформирована карточка.
- files touched / work locations: Сейчас implementation files не менялись; будущие locations указаны в Scope.
- technical value delivered: Не заявлена до реализации.
- product value delivered: Не заявлена до реализации.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: Проверяется только подготовка плана; выполнение AC этой задачи не заявлено.
- residual risks: Пилот этого repo не доказывает массовую пользу; prompts/routing требуют отдельного baseline сравнения, не новой установки.
- follow-up: Выбор следующего разрешённого slice по DAG; автоматический старт запрещён.

### Task `PAOS-METH-17`

- Task: PAOS-METH-17
- Task name: Принять интегрированный пилот и проверить сохранность контрактов
- Status: planned
- Priority: P1
- Methodologies: Spec-DD, Design-DD, TDD, ADD, FSD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-07, PAOS-METH-13
- Blocks: PAOS-METH-18
- External references: PAOS-FUNC-19, PAOS-FUNC-21, PAOS-FUNC-22, PAOS-FUNC-23, UI-12
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Свести evidence dashboard/tasks/workflows и методологического процесса на одном состоянии исходников.
- Technical value: Свести evidence dashboard/tasks/workflows и методологического процесса на одном состоянии исходников.
- Product value: Принять полезный ограниченный результат с честными gaps до масштабирования.
- Scope: `tests/web/`; `docs/testing/index.md`; `docs/frontend/`; `docs/planning/methodology-improvement-2026-11-15.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: AC/evidence reconciliation и verdict pilot_accepted/partial/blocked с причинами.
- Acceptance criteria: PAOS-METH-17-AC01: Каждый pilot AC имеет current check/receipt либо явный unresolved gap; все обязательные checks affected contracts проходят, findings имеют disposition. PAOS-METH-17-AC02: Проверены scope/session selection, drafts, partial data, navigation/focus и contracts independence; runtime recovery/backup evidence переиспользуется только при неизменном релевантном состоянии. PAOS-METH-17-AC03: Review и техническая приёмка ограничены пилотом; UI-12/F23 human acceptance и F19 full product E2E сохраняют своих owners; P3 задачи не блокируют bounded pilot closure.
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
- Methodologies: ADD, FSD, Spec-DD
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Owner-requested multi-slice methodology/FSD plan; planning only.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-METH-17
- Blocks: PAOS-METH-14, PAOS-METH-16
- External references: PAOS-FUNC-25
- Source: [baseline и source hashes](methodology-improvement-2026-11-15.json); актуальные пути ниже; external refs — только references.
- Short description: Выбрать go/bounded_go/hold/stop отдельно для каждого следующего направления по evidence.
- Technical value: Выбрать go/bounded_go/hold/stop отдельно для каждого следующего направления по evidence.
- Product value: Масштабировать полезное и остановить неподтверждённые усложнения.
- Scope: `docs/architecture/decisions/`; `docs/frontend/`; `docs/testing/`; `docs/sources/registry.md`; `PLAN.md`; `RUNLOG.md`. Будущие work locations, не список изменённых сейчас файлов.
- Non-goals: Новые продуктовые функции, provider/credentials, target/Git/publication/production; чужие FUNC/Web статусы; всё вне указанного slice.
- Expected result: Reviewable rollout decision в существующем ADR/evidence owner и компактный handoff.
- Acceptance criteria: PAOS-METH-18-AC01: Сравнены baseline/pilot по unauthorized edges, regression findings, change/review effort и доступным outcome metrics; размер тестового набора не используется как benefit metric. PAOS-METH-18-AC02: Для METH-14/15/16 записаны отдельные решения, scope, owner и rollback; hold/stop сохраняет рабочий пилот и не создаёт бессрочного migration mandate. PAOS-METH-18-AC03: Обновлены только изменившиеся docs/registry/control-plane owners; active rules изменяются только отдельным разрешённым slice, existing FUNC/Web статусы и release gates сохранены.
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

