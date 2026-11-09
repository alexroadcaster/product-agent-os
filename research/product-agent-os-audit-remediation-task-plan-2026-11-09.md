# Product-Agent OS — задачи и группы исправлений по полному аудиту

Source status: project-local planning artifact, 09.11.2026; составлен по сохранённому аудиту и текущим owning plans. Статус документа: `planned / implementation_not_started_by_this_plan`. Сохранение карточек не означает выполнение, promotion или разрешение на перечисленные внешние действия.

Document ID: `PAOS-AUDIT-REMEDIATION-2026-11-09`. Authoring task: `PAOS-AUDIT-TASK-MATRIX-2026-11-09`. Часовой пояс: `Europe/Moscow`.

## Назначение и источники

В документе **6 групп и 26 карточек**: 18 задач по F01–F18, пять существующих B45-CQRR-T30–T34 и три этапа host/usefulness. Для каждой группы и задачи указаны ID, название, описание, техническое и продуктовое значение, затрагиваемые файлы и критерии приёмки. Поля task_matrix_plan_v1 сохраняют совместимость с существующим validator; русский текст рядом с каноническим именем поля поясняет его назначение.

- [Полный аудит 09.11.2026](product-agent-os-full-audit-2026-11-09.md): F01–F18 и границы evidence.
- [Последующее исправление lifecycle по чатам](product-agent-os-session-lifecycle-fix-2026-11-09.md): выполненные session isolation и exact marker bootstrap.
- [Ordinary/GAP implementation plan](product-agent-os-ordinary-route-implementation-plan-2026-11-05.md): ORD, GAP-03 M06, GAP-05 и GAP-06.
- [Canonical B45 task group](../docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json): ID, названия, dependencies и acceptance T30–T34.
- [PLAN.md](../PLAN.md), [TEST.md](../TEST.md), [EVALS.md](../EVALS.md), [RUNLOG.md](../RUNLOG.md): текущие owning pointers и обязательные verification routes.

## Что не выполнять повторно

- T23–T29 и ORD-01–ORD-06 уже реализованы локально. Новая задача их переиспользует; обнаруженная регрессия требует конкретного evidence и ограниченного исправления.
- Session-bound markers, host-envelope identity, own/foreign/mixed marker bootstrap и Windows case handling реализованы отдельным lifecycle slice. F06 теперь относится к оставшимся command/patch classification defects; F18 — к новому ограниченному authoring contract.
- Существующий GAP-05 create-only grant не считается сломанным лишь потому, что не умеет Update File; его расширение требует явного нового контракта.
- PAOS-AUD-F01–F18 — ID новых corrective slices, связанные с соответствующим F в аудите 09.11.2026; они не подменяют старые одинаково названные findings других исследований.
- T30–T34 и PAOS-GAP-06 здесь представлены для общего порядка работ. Их source-owned machine status и canonical acceptance остаются в исходных артефактах. PAOS-AUD-HOST-01/02 адресуют оставшиеся verification этапы существующих GAP gates, не создают второй status registry.
- Planned в карточке означает, что описанный остаточный объём не выполнен этим планом; он не отменяет ранее выполненные части parent задачи.

## Матрица групп

| ID | Группа | Карточки | Основной результат |
| --- | --- | --- | --- |
| PAOS-AUD-G1 | Надёжные hooks, rules и установка | PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F11, PAOS-AUD-F07, PAOS-AUD-F18 | Согласованные active/package contracts, точные границы записи и корректные staging/merge paths. |
| PAOS-AUD-G2 | Совместимость package и диагностика host | PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04 | Один источник диагностики package schema и surface capabilities без нового doctor framework. |
| PAOS-AUD-G3 | Достоверные evidence и текущие статусы | PAOS-AUD-F03, PAOS-AUD-F08, PAOS-AUD-F16 | Устранение ложноположительных и ложных missing-сигналов без нового status registry. |
| PAOS-AUD-G4 | Простой ordinary route и компактные инструкции | PAOS-AUD-F05, PAOS-AUD-F09, PAOS-AUD-F10, PAOS-AUD-F15 | Минимальный task context, совместимость callers, меньшая нагрузка инструкций и повторных scans. |
| PAOS-AUD-G5 | Документация, offline tooling и актуальный site | PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F17 | Воспроизводимый offline command contract и согласованный source/build output. |
| PAOS-AUD-G6 | Проверка GPT-6, host activation и пользовательской пользы | B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32, B45-CQRR-T33, B45-CQRR-T34, PAOS-AUD-HOST-01, PAOS-AUD-HOST-02, PAOS-GAP-06 | Раздельные воспроизводимые evidence для конфигурации, активации, качества и acceptance. |

## Порядок, зависимости и ускорение

1. G1 и G2 — первые local corrective slices. G3 можно вести независимо по core files; shared control-plane обновляется последовательно.
2. В G1 не объединять все guard changes в один неразличимый diff: F06 → F18; generated hooks F12 проверяется на согласованном контракте. F07 и F11 независимы и не требуют настоящих ACL/rules activation для code-level проверки.
3. В G2 F01 и F02 можно подготовить независимо; F04 использует оба результата. Отдельный doctor framework не создаётся.
4. G4: F10 → F09; intake F05 можно вести независимо, incremental report scenario требует F18; измерения F15 допустимы раньше, правка — только при подтверждённой пользе. Не смешивать skill shortening, model switch и compact-contract intervention в одном eval treatment.
5. T30 и T31 можно готовить до завершения local fixes по независимым файлам. Canonical dependency graph: T29 → T30; T27/T29 → T31; T25/T30/T31 → T32; T24/T28/T29/T30/T31/T32 → T33; T33 → T34. G4 freeze — дополнительное условие воспроизводимости выбранного окружения, не скрытая правка canonical B45 dependencies.
6. Документация следует за поведением в каждом slice. Финальный local site build G5 после стабилизации G1–G4; новые host/eval receipts затем добавляются малой адресной синхронизацией.
7. AUD-HOST-01 после финального package/skills; AUD-HOST-02 после финальных hooks/definitions. Изменившийся source/hash вновь открывает относящийся к нему activation gate.
8. GAP-06 начинается с одного pilot в рамках ранее запланированного набора 3–5 задач. Один удачный кейс не закрывает весь набор; T34 не является обязательным условием обычной проверки полезности.

Возможность независимой работы означает допустимое разделение ownership, а не запуск subagents по этому документу. Минимальный состав — один исполнитель. При будущей разрешённой параллельной работе разные владельцы не редактируют один файл одновременно; hooks/lifecycle tests, compatibility module, canonical skills, README и root pointers имеют одного writer на текущий slice.

## Общие границы реализации и проверки

- Все пути ниже workspace-relative. Существующие paths проверены при authoring. Отсутствующие файлы T30–T34 явно помечены `proposed new` и пока не создаются. Directory scope требует точного file manifest до начала соответствующего slice.
- Scope каждой будущей реализации — названные файлы и относящиеся к ней tests. При изменении source-backed claims синхронизируются затронутые RU/EN пары и оба registry. Общие PLAN/TEST/EVALS/REQUIREMENTS/RUNLOG pointers меняет один writer только по применимому control-plane-sync trigger; старый исторический ledger не переписывается.
- Новые behavior/bug fixes: observable RED → минимальный GREEN → scoped refactor. Behavior-neutral документация и форматирование — static checks. Relevant regression, fixture/transcript и compatibility gates выбираются по TEST.md; не повторять неизменные проверки без причины.
- Локальные contract tests, schema validation и generated artifact не доказывают actual host loading, trust, model selection или product acceptance. Для таких claims нужны отдельные receipts выбранного проверенного состояния.
- Указанные роли — будущая ownership recommendation. Они не означают запущенных subagents. Skill выбирать по конкретному подэтапу; canonical Product-Agent OS skills брать из repository, не смешивать с installed cache.
- Этот запрос разрешает сохранить план, но не выполнять его implementation, provider/model/reviewer calls, cache/global edits, target apply, ACL/trust/rules activation, browser/server, Git или publication. Для будущего локального implementation request повторное общее согласование не нужно; конкретные внешние границы сохраняются.
- Rollback будущего slice: отменить только его собственные изменения относительно снятого baseline, сохранив чужие hunks и историческое evidence. Для ACL/target/trust заранее нужен отдельный rollback route.
- Оценки длительности не зафиксированы: нет достаточного measured baseline. Не подменять расписание выдуманными сроками; после первого slice оценить фактический объём.

## Проверка этого документа

Authoring не меняет реализацию. Текущие результаты validator, docs checks и scope review записываются ниже после фактического запуска; будущие проверки в карточках — критерии, а не уже полученное evidence.

Verification status: `plan_static_verified`; только качество и полнота документа, не реализация карточек.

| Выполненная проверка 09.11.2026 | Результат |
| --- | --- |
| `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-audit-remediation-task-plan-2026-11-09.md` | Exit 0; ok=true; errors=[]; task_matrix_plan_v1. После уточнения dependencies финальный текст также проверен той же validate_task_matrix_text в memory-only checker: errors=[] |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` | Exit 0; 100 tests, 3.476 s, OK. Последующие правки затрагивают только этот research plan, не implementation/docs fixtures |
| `python -B tools/check_docs.py` | Exit 0; OK: documentation structure checks passed |
| `git diff --check` | Exit 0. Новый untracked Markdown дополнительно проверен на trailing whitespace напрямую |
| Memory-only Python integrity checker через `python -B -` | Exit 0: 6 групп, 26 уникальных карточек, F01–F18 полностью покрыты, семь запрошенных полей присутствуют, все task statuses planned, exact T30–T34 titles сохранены, existing/proposed paths и relative links валидны, UTF-8 без replacement characters |
| `git diff --name-only` и `git ls-files --others --exclude-standard` | Существующие tracked файлы не изменены; добавлены только этот Markdown и собственный session marker authoring задачи |

Self-review: новые corrective slices отделены от уже выполненных session isolation/ORD/T23–T29; existing T30–T34 и GAP-06 не получили второй machine status. Убраны искусственные hard dependencies: generated path F12 и intake F05 можно исправлять независимо, общие host/authoring gates остаются для соответствующих сценариев. Внешние действия и новые файлы помечены явно. Independent reviewer не запускался.

Граница доказательства: не запускались implementation задач, full runtime suite, fresh host, live model/reviewer, browser, site build или публикация. В этом authoring они не нужны; все будущие acceptance gates остаются открытыми.

## Control-plane sync для сохранения плана

- REQUIREMENTS.md, TEST.md, EVALS.md, prod_test.md: not_applicable — продуктовые требования, обязательные gates, thresholds и историческое evidence этим authoring не изменяются.
- PLAN.md и RUNLOG.md: handoff_required — компактная ссылка на этот отдельный план и выбор первого execution slice нужны при запуске реализации; текущая authority ограничена новым файлом и служебным marker.
- Registry RU/EN: not_applicable для этого research plan — новые official behavior claims не добавляются; источник findings остаётся аудит. Обновления registry включены в соответствующие будущие slices.
- Site/navigation/diagrams: not_applicable для authoring; план не включён в site и не содержит claim о свежей сборке.
- Overflow/refactor: not_applicable. Исторические артефакты, machine status и прочие файлы сохранены.

## PAOS-AUD-G1 — Надёжные hooks, rules и установка

- **ID:** `PAOS-AUD-G1`
- **Название группы:** Надёжные hooks, rules и установка
- **Описание группы:** Закрыть оставшиеся ошибки классификации действий и generated onboarding; ограничить ACL repair и добавить безопасное последовательное ведение отчёта. Сохранить уже реализованную session isolation.
- **Техническое значение (для проекта):** Согласованные active/package contracts, точные границы записи и корректные staging/merge paths.
- **Продуктовое значение (для пользователя):** Меньше ложных блокировок и повторных согласований без ослабления защиты пользовательских файлов.
- **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `.rules`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Все пять карточек имеют локальные positive/negative evidence; active/package mirrors согласованы; нет автоматической активации hooks/rules или изменения рабочих ACL. Host acceptance закрывается отдельно в G6.
- **Зависимости и порядок:** Начинать первой. F06 перед F18; F12 можно исправлять независимо по своим файлам, integrated host probe после итоговых hooks. ACL и rules — независимые ограниченные изменения.
- **Предлагаемая ответственность:** plugin-runtime-builder; assurance — security-privacy-supply-chain-reviewer.

### Task `PAOS-AUD-F06`

- ID: `PAOS-AUD-F06`
- Task: **Название задачи:** Исправить оставшиеся ошибки классификации команд и patch
- Short description: **Описание задачи:** Различать executable command, аргументы и содержимое patch. Не признавать всю составную команду read-only по начальному префиксу; неизвестные формы направлять в ограниченную проверку. Сохранить текущий session-bound selector, exact bootstrap, sandbox и approvals; не писать универсальный shell interpreter.
- Technical value: **Техническое значение (для проекта):** Устранение false allow и false deny в PreToolUse без расширения полномочий.
- Product value: **Продуктовое значение (для пользователя):** Обычные чтения и документационные примеры не блокируются ошибочно, а потенциальные записи проверяются последовательно.
- Scope: **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `tests/product_agent_os/test_lifecycle_hooks.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Инертные cases: чистое чтение разрешено; составная read/write строка не классифицируется как чистое чтение; неизвестная запись не получает allow через отсутствие match. 2) Упоминание опасной команды как данных в обычном Markdown не трактуется как её выполнение; реальные destructive/path/secret проверки сохранены. 3) Регрессии own/foreign/mixed marker, Windows case handling и session isolation проходят; active/package файлы совпадают.
- Group: PAOS-AUD-G1
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана. PAOS-SESSION-LIFECYCLE-2026-11-09 — использовать, не переделывать.
- Blocks: PAOS-AUD-F18, PAOS-AUD-HOST-02; для F05 только incremental report scenario.
- Source: F06; последующий session-lifecycle repair уже закрыл exact marker bootstrap и изоляцию чатов.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Устранение false allow и false deny в PreToolUse без расширения полномочий. Missing host/product gates остаются открытыми.
- Verification gates: RED/GREEN в test_lifecycle_hooks; validate_hooks.py для active/package definitions; AST/parity; свежий host отдельно AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; изменение definition/trust и host probe не входит в локальное исправление. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; изменение definition/trust и host probe не входит в локальное исправление.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F12`

- ID: `PAOS-AUD-F12`
- Task: **Название задачи:** Согласовать generated hooks config и безопасный merge
- Short description: **Описание задачи:** Исправить mapping в templates/merge на discovered .codex/hooks.json; согласовать manifest и generated config. Сохранить существующие user-authored hooks. Явно разделить staging, approved apply и фактическую активацию.
- Technical value: **Техническое значение (для проекта):** Устранение несовпадения generated filesystem layout с контрактом загрузки.
- Product value: **Продуктовое значение (для пользователя):** Установка не создаёт видимость включённого hook, который host не загрузит.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/product_agent_os/merge_infrastructure.py`; `plugins/product-agent-os/assets/templates/config/config.toml`; `tests/product_agent_os/test_merge_infrastructure.py`; `tests/product_agent_os/test_infrastructure_templates.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Dry-run, staging manifest и config указывают один правильный путь; mirror не считается discovery config. 2) Existing unmarked config не перезаписывается; approved merge/rollback проверены на synthetic workspace. 3) Тест проверяет реальный expected discovery path; результат установки не объявляет trust/activation доказанными.
- Group: PAOS-AUD-G1
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет жёсткой local code зависимости; integration/host probe выполняется после итогового F06.
- Blocks: PAOS-AUD-HOST-02
- Source: F12
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Устранение несовпадения generated filesystem layout с контрактом загрузки. Missing host/product gates остаются открытыми.
- Verification gates: Focused infrastructure/merge tests и dry-run на synthetic fixtures; actual target activation отдельно AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; apply в реальный target и trust требуют своей точной authority. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; apply в реальный target и trust требуют своей точной authority.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F11`

- ID: `PAOS-AUD-F11`
- Task: **Название задачи:** Исправить семантику и статус rules-файла
- Short description: **Описание задачи:** Устранить использование not_match как исключения; выбрать узкие patterns и корректные проверочные примеры. Отдельно определить, остаётся ли файл proposal или переносится в discovery path по разрешённой активации. Не активировать широкие allow путём простого перемещения.
- Technical value: **Техническое значение (для проекта):** Native parser принимает политику, а разрешения соответствуют проверяемому контракту.
- Product value: **Продуктовое значение (для пользователя):** Пользователь понимает, какие команды реально разрешены и активна ли эта политика.
- Scope: **Затрагиваемые файлы:** `.rules`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) codex execpolicy check принимает файл и даёт ожидаемые решения для positive/negative cases. 2) Patterns не расширяют прежнюю заявленную authority; потенциально опасные варианты не получают широкое allow. 3) Фактический loading status указан отдельно; путь .codex/rules/default.rules не создаётся без отдельного решения об активации.
- Group: PAOS-AUD-G1
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F11
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Native parser принимает политику, а разрешения соответствуют проверяемому контракту. Missing host/product gates остаются открытыми.
- Verification gates: Native execpolicy parser/check на фиксированных inert arguments; docs checks. Исполнение разрешённых команд не требуется. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; relocation/activation rules — отдельная граница разрешения. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: security-privacy-supply-chain-reviewer для read-only review; plugin-runtime-builder для правки; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; relocation/activation rules — отдельная граница разрешения.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F07`

- ID: `PAOS-AUD-F07`
- Task: **Название задачи:** Исключить широкий ACL repair из onboarding
- Short description: **Описание задачи:** Убрать normal-onboarding рекомендацию broad ACL repair. Если helper остаётся доступным как repair tool, ограничить target/SID, запретить неоднозначные reparse paths, добавить preview, ACL snapshot/restore и привязку apply к согласованному plan digest.
- Technical value: **Техническое значение (для проекта):** Сохранение системных и проектных deny ACE; обратимый и ограниченный ремонт permissions.
- Product value: **Продуктовое значение (для пользователя):** Настройка Product-Agent OS не снимает пользовательские ограничения доступа и не требует опасного универсального исправления.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py`; `plugins/product-agent-os/scripts/prepare_windows_codex_permissions.py`; `tests/product_agent_os/test_windows_codex_permissions.py`; `plugins/product-agent-os/README.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Default/help/onboarding не предлагают broad apply; dry-run не меняет ACL. 2) Посторонние DENY SID не удаляются; unexpected target, digest drift и reparse ambiguity останавливают apply. 3) Backup/restore и формирование команд проверены через существующий mock/stub слой; настоящий ACL acceptance явно остаётся отдельным разрешённым сценарием.
- Group: PAOS-AUD-G1
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F07
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Сохранение системных и проектных deny ACE; обратимый и ограниченный ремонт permissions. Missing host/product gates остаются открытыми.
- Verification gates: test_windows_codex_permissions: command contract, SID/path allowlist, digest mismatch, rollback preservation. Без реального icacls apply. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; реальные ACL/permissions изменения требуют точных target, owner и rollback. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; независимая проверка security-privacy-supply-chain-reviewer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; реальные ACL/permissions изменения требуют точных target, owner и rollback.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F18`

- ID: `PAOS-AUD-F18`
- Task: **Название задачи:** Добавить ограниченное последовательное authoring одного отчёта
- Short description: **Описание задачи:** Спроектировать отдельный opt-in report-authoring scope на один exact Markdown path: create/update, expected previous digest, срок действия, session ownership и terminal handling. Определить честное отображение этого work type в lifecycle schema. Существующий create-only grant не расширять неявно.
- Technical value: **Техническое значение (для проекта):** Поддержка incremental research без общего разрешения на запись и без маскировки документации под runtime implementation.
- Product value: **Продуктовое значение (для пользователя):** Наблюдения сохраняются по мере работы без повторной ручной разблокировки каждой записи.
- Scope: **Затрагиваемые файлы:** `.codex/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/task_plan_lifecycle.py`; `plugins/product-agent-os/scripts/product_agent_os/validators.py`; `.codex/workflows/task-plan-lifecycle.md`; `plugins/product-agent-os/assets/templates/workflows/task-plan-lifecycle.md`; `tests/product_agent_os/test_lifecycle_hooks.py`; `tests/product_agent_os/test_task_plan_lifecycle.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Несколько последовательных обновлений своего exact report проходят при совпадении digest и действующем scope. 2) Чужой marker/path, stale digest, expired grant, terminal state, symlink/alias и mixed patch отклоняются. 3) Legacy create-only поведение сохранено; новая authoring authority явно выражена и не меняет sandbox/trust. 4) Конкурирующее изменение отчёта даёт conflict, а не silent overwrite; host behavior закрывается отдельно.
- Group: PAOS-AUD-G1
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F06
- Blocks: PAOS-AUD-HOST-02; для F05 только incremental report scenario.
- Source: F18; GAP-05 create-only grant; session isolation уже реализована.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Поддержка incremental research без общего разрешения на запись и без маскировки документации под runtime implementation. Missing host/product gates остаются открытыми.
- Verification gates: Contract design + focused lifecycle/validators tests с RED/GREEN; source parity; после итоговых hashes AUD-HOST-02. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; изменение opt-in grant не даёт права активировать его в hook definition. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; изменение opt-in grant не даёт права активировать его в hook definition.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

## PAOS-AUD-G2 — Совместимость package и диагностика host

- **ID:** `PAOS-AUD-G2`
- **Название группы:** Совместимость package и диагностика host
- **Описание группы:** Исправить MCP declaration, capability matrix и расширить существующий compatibility report наблюдаемыми данными host/model/provenance.
- **Техническое значение (для проекта):** Один источник диагностики package schema и surface capabilities без нового doctor framework.
- **Продуктовое значение (для пользователя):** Пользователь видит, что доступно, что не поддерживается и что ещё не проверено.
- **Затрагиваемые файлы:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Поддерживаемый локальный package проходит compatibility check; unsupported и not_verified различены; version/model/cache/trust не получают вымышленных значений.
- **Зависимости и порядок:** Можно вести независимо от G1 при отдельном владельце. F01 и F02 перед F04. Выход используется G5/G6.
- **Предлагаемая ответственность:** plugin-runtime-builder.

### Task `PAOS-AUD-F01`

- ID: `PAOS-AUD-F01`
- Task: **Название задачи:** Исправить MCP declaration и distribution metadata
- Short description: **Описание задачи:** Исправить flat .mcp.json в рамках поддерживаемого текущего manifest format; проверить resolver precedence. Проверить placeholder publisher/URLs: использовать только подтверждённые данные владельца, иначе явно оставить distribution gate открытым.
- Technical value: **Техническое значение (для проекта):** Совместимый package без необязательной wholesale migration на portable format.
- Product value: **Продуктовое значение (для пользователя):** Пакет устанавливается по понятному контракту и не вводит в заблуждение относительно издателя.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/.mcp.json`; `plugins/product-agent-os/.codex-plugin/plugin.json`; `plugins/product-agent-os/scripts/product_agent_os/plugin_components.py`; `tests/product_agent_os/test_codex_compatibility.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Текущий package проходит локальный compatibility check по MCP shape; malformed/ambiguous fixtures остаются rejected/needs_review. 2) Legacy manifest сохраняется, если нет отдельного требования переносимости; не смешиваются два независимых manifest authority. 3) Publisher/URLs проверены или distribution остаётся явно gated; MCP server не запускается проверкой структуры.
- Group: PAOS-AUD-G2
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F01
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Совместимый package без необязательной wholesale migration на portable format. Missing host/product gates остаются открытыми.
- Verification gates: validate_codex_compatibility.py; existing component/compatibility fixtures; JSON syntax и resolver regression. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; неизвестные identity/URL не выдумывать; publication и MCP execution вне scope. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; неизвестные identity/URL не выдумывать; publication и MCP execution вне scope.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F02`

- ID: `PAOS-AUD-F02`
- Task: **Название задачи:** Разделить поддержку и проверенность host capabilities
- Short description: **Описание задачи:** В существующей capability matrix разделить documented support, unsupported и observed/not_verified для Codex App, CLI и IDE extension; различать native plugin и standalone skills.
- Technical value: **Техническое значение (для проекта):** Типизированный capability contract без смешения невозможного и ещё не протестированного.
- Product value: **Продуктовое значение (для пользователя):** Пользователь не тратит время на попытку включить неподдерживаемую функцию.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) App/CLI/IDE получают документированные разные capabilities; unsupported не заменяется requires_host_receipt. 2) Host receipt не может повысить documented unsupported до supported без обновления source-backed contract. 3) Local structure scope и отсутствие активационного доказательства сохранены.
- Group: PAOS-AUD-G2
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F04, PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F02
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Типизированный capability contract без смешения невозможного и ещё не протестированного. Missing host/product gates остаются открытыми.
- Verification gates: Focused compatibility tests: surface/component matrix, unknown surface, unsupported versus unverified; актуальные official sources при реализации. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; capability facts сверить заново на дату реализации. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; capability facts сверить заново на дату реализации.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F04`

- ID: `PAOS-AUD-F04`
- Task: **Название задачи:** Дополнить диагностику GPT-6 и provenance без promotion claims
- Short description: **Описание задачи:** Расширить существующий compatibility report сведениями client version/surface, configured versus observed model, canonical/cache provenance и trust unknown/observed. Клиентский minimum проверять только для конкретной documented surface. Не менять model pins или effort.
- Technical value: **Техническое значение (для проекта):** Один наблюдаемый compatibility contract связывает конфигурацию с доступным evidence.
- Product value: **Продуктовое значение (для пользователя):** Видно, почему выбранная модель или skill пока не подтверждены в текущем окружении.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py`; `plugins/product-agent-os/scripts/validate_codex_compatibility.py`; `tests/product_agent_os/test_codex_compatibility.py`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Missing/old/unknown version, недоступный model receipt, source/cache drift и unknown trust отражаются явно. 2) Установленный CLI не выдаётся за проверенную версию App или доступность аккаунта. 3) Нет provider вызовов, cache writes, автоматического повышения effort или promotion по одному model ID. 4) Read-only inputs/report редактируют только allowlisted non-secret данные; baseline T23–T29 сохранён.
- Group: PAOS-AUD-G2
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02
- Blocks: PAOS-AUD-F14, PAOS-AUD-HOST-01
- Source: F04 — локальная диагностика; качество treatment остаётся в B45-CQRR-T30–T34.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Один наблюдаемый compatibility contract связывает конфигурацию с доступным evidence. Missing host/product gates остаются открытыми.
- Verification gates: Focused version/capability/provenance fixtures и read-only CLI output; actual host receipt — AUD-HOST-01. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; диагностика не требует credential use или изменения active profiles. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; диагностика не требует credential use или изменения active profiles.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

## PAOS-AUD-G3 — Достоверные evidence и текущие статусы

- **ID:** `PAOS-AUD-G3`
- **Название группы:** Достоверные evidence и текущие статусы
- **Описание группы:** Исправить freshness parser, пустой feedback и precedence текущего состояния относительно исторических receipts.
- **Техническое значение (для проекта):** Устранение ложноположительных и ложных missing-сигналов без нового status registry.
- **Продуктовое значение (для пользователя):** Понятно, что действительно проверено и какие действия ещё нужны; отсутствие данных не выглядит успехом.
- **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Unknown/empty/stale/conflicting cases имеют корректные результаты; текущие projections привязаны к source revision; история сохранена.
- **Зависимости и порядок:** Независима от G1/G2 по core modules. Общие control-plane pointers обновляет один владелец последовательно.
- **Предлагаемая ответственность:** plugin-runtime-builder; feedback — learning-loop-engineer; projections — graph-cockpit-engineer.

### Task `PAOS-AUD-F03`

- ID: `PAOS-AUD-F03`
- Task: **Название задачи:** Исправить freshness и классификацию source evidence
- Short description: **Описание задачи:** Поддержать используемые RU/EN date labels, строгую валидацию календарной даты и ссылки на локальный registry. Разделить official behavior, project contract и historical receipt; не считать простое упоминание Codex behavioral claim.
- Technical value: **Техническое значение (для проекта):** Меньше ложных missing/review результатов; date presence, freshness и semantic support остаются разными измерениями.
- Product value: **Продуктовое значение (для пользователя):** Пользователь видит реальные пробелы источников вместо массового списка ложных предупреждений.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/source_policy.py`; `tests/product_agent_os/test_source_policy.py`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Форматы «Проверено YYYY-MM-DD.» и фактические EN формы распознаются; invalid/future/missing/stale cases различены по явной политике. 2) Registry reference разрешается безопасно внутри workspace; broken refs отражены как missing evidence. 3) Project-local и historical claims не получают ложный official verdict; дата/URL не меняют claim_supported на verified без semantic review.
- Group: PAOS-AUD-G3
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F03
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Меньше ложных missing/review результатов; date presence, freshness и semantic support остаются разными измерениями. Missing host/product gates остаются открытыми.
- Verification gates: test_source_policy: formats, dates, registry resolution, claim classes; scan текущих docs с разбором изменения findings, docs checks. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; сохранить exact-host URL и secret protections; не превращать scanner в crawler. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; сохранить exact-host URL и secret protections; не превращать scanner в crawler.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F08`

- ID: `PAOS-AUD-F08`
- Task: **Название задачи:** Исправить положительный сигнал при отсутствии owner feedback
- Short description: **Описание задачи:** При нулевом числе допустимых owner labels возвращать insufficient_evidence. Раздельно учитывать валидность записи, human label count и тональность; public summary должен сохранять эту семантику.
- Technical value: **Техническое значение (для проекта):** Отсутствие evidence перестаёт выглядеть основанием для promotion.
- Product value: **Продуктовое значение (для пользователя):** Система не делает вывод об удовлетворённости пользователя, пока он не дал пригодную обратную связь.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/self_learning_feedback.py`; `tests/product_agent_os/test_self_learning_extensions.py`; `tests/product_agent_os/test_self_learning_state.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Empty ledger, missing ledger и wholly rejected records дают insufficient_evidence и не positive promotion signal. 2) Допустимые positive/negative/mixed labels сохраняют корректные denominator/counts и summary. 3) Candidate-only/manual-only safeguards не меняются; fixtures не содержат реальных персональных данных.
- Group: PAOS-AUD-G3
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-GAP-06
- Source: F08
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Отсутствие evidence перестаёт выглядеть основанием для promotion. Missing host/product gates остаются открытыми.
- Verification gates: RED на evaluate_satisfaction([]) и public summary; focused self-learning regression. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; изменение output enum требует проверки существующих consumers. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: learning-loop-engineer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; изменение output enum требует проверки существующих consumers.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F16`

- ID: `PAOS-AUD-F16`
- Task: **Название задачи:** Определить precedence текущего статуса и исторических receipts
- Short description: **Описание задачи:** В существующих projections определить source ownership и precedence новых execution evidence. Добавить компактный current pointer с revision, не создавая второй registry. Различать task/run/verification/acceptance; при конфликте показывать conflict/unknown.
- Technical value: **Техническое значение (для проекта):** Воспроизводимое вычисление current state из owning sources вместо выбора первой записи Current.
- Product value: **Продуктовое значение (для пользователя):** Понятно, что уже выполнено, что ждёт проверки и какая задача следующая.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/status_snapshot.py`; `tests/product_agent_os/test_status_snapshot.py`; `PLAN.md`; `RUNLOG.md`; `TEST.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Historical planned плюс более новый execution receipt не возвращает выполненную задачу в planned. 2) Current result содержит источник/revision и различает implemented, verified, accepted; ambiguous/conflicting evidence не скрывается. 3) Исторические B42/B45 receipts сохранены; T23–T29 и machine statuses не переписаны из-за новой projection.
- Group: PAOS-AUD-G3
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F16
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Воспроизводимое вычисление current state из owning sources вместо выбора первой записи Current. Missing host/product gates остаются открытыми.
- Verification gates: test_status_snapshot с historical/current/conflict cases; validate_task_state_consistency.py; docs checks. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; control-plane файлы общие — изменения только последовательно. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: graph-cockpit-engineer; control-plane writer один; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; control-plane файлы общие — изменения только последовательно.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

## PAOS-AUD-G4 — Простой ordinary route и компактные инструкции

- **ID:** `PAOS-AUD-G4`
- **Название группы:** Простой ordinary route и компактные инструкции
- **Описание группы:** Упростить вход в существующий ordinary route, убрать повторяющиеся инструкции и только измеренную лишнюю работу модулей.
- **Техническое значение (для проекта):** Минимальный task context, совместимость callers, меньшая нагрузка инструкций и повторных scans.
- **Продуктовое значение (для пользователя):** Меньше лишних вопросов, файлов и времени ожидания для обычной задачи при сохранении high-risk escalation.
- **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/skills/`; `tests/AGENTS.md`; `plugins/product-agent-os/scripts/product_agent_os/discovery.py`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Representative ordinary/edge/adversarial cases сохраняют корректность и границы; сокращение контекста/сканирования измерено; бездоказательный рефакторинг не выполняется.
- **Зависимости и порядок:** Intake F05 независим; изменяемый authoring scenario — после нужных G1 gates. F10 перед или совместно с F09; F15 — измерение сначала. Финальный baseline перед T32.
- **Предлагаемая ответственность:** plugin-runtime-builder; инструкции — lifecycle-orchestrator.

### Task `PAOS-AUD-F05`

- ID: `PAOS-AUD-F05`
- Task: **Название задачи:** Упростить вход в существующий ordinary route
- Short description: **Описание задачи:** Добавить минимальный явный intake/task-context на существующем public entrypoint. Объяснить и диагностировать legacy fallback; проверить callers до возможной смены default. Поддержать RU/EN/no-builder без нового onboarding на каждую задачу.
- Technical value: **Техническое значение (для проекта):** Использование готовых selectors через минимальный контракт вместо полного template registry по умолчанию.
- Product value: **Продуктовое значение (для пользователя):** Обычная задача начинается с небольшого числа нужных действий и не создаёт сотни лишних предложений файлов.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/infrastructure.py`; `plugins/product-agent-os/scripts/product_agent_os/templates.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/cli.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/state.py`; `plugins/product-agent-os/scripts/codex_runtime_runner/routes.py`; `tests/product_agent_os/test_codex_runtime_runner_cli.py`; `tests/product_agent_os/test_codex_runtime_runner_state_routes.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Small ordinary case выбирает согласованный минимальный artifact set; high-risk/unknown case сохраняет escalation. 2) RU/EN проекты и отсутствие builder не вызывают скрытого full onboarding. 3) Legacy callers имеют явный fallback receipt; default меняется только после compatibility regression и отдельного решения в задаче. 4) Нет автоматического target apply или повторной реализации T25–T29.
- Group: PAOS-AUD-G4
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: ORD-01–ORD-06 выполнены. Intake можно реализовать независимо; incremental report scenario использует завершённые F06/F18.
- Blocks: PAOS-AUD-F15, PAOS-AUD-F14, PAOS-GAP-06
- Source: F05; ORD-01–ORD-06 и T23–T29 уже реализованы.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Использование готовых selectors через минимальный контракт вместо полного template registry по умолчанию. Missing host/product gates остаются открытыми.
- Verification gates: Existing ORD positive/negative cases, CLI-to-selector-to-staging integration; сравнение artifact count и лишних вопросов с baseline. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; authority и readiness не выводятся только из task context. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; authority и readiness не выводятся только из task context.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F09`

- ID: `PAOS-AUD-F09`
- Task: **Название задачи:** Сократить повторяющиеся skill instructions
- Short description: **Описание задачи:** Сохранить trigger, authority, inputs, outputs и stop в canonical SKILL.md; общие повторения и длинные conditional процедуры перенести в существующие references. Сначала снять baseline реально прочитанных файлов; не менять implicit invocation или installed cache.
- Technical value: **Техническое значение (для проекта):** Progressive disclosure без повторной загрузки одинаковых политик и искусственного увеличения context budget.
- Product value: **Продуктовое значение (для пользователя):** Меньше задержек и ненужных шагов при сохранении качества и предсказуемости результата.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/skills/`; `tests/product_agent_os/test_lifecycle_skills.py`; `tests/product_agent_os/test_validators.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Все 12 canonical skills сохраняют свои role boundaries и metadata; ссылки на references валидны. 2) Измерено сокращение реально загружаемого контекста на выбранных задачах, включая conditional reference reads. 3) Typical/edge/adversarial cases не теряют authority и необходимые gates; local checks и live behavioral evaluation обозначены отдельно. 4) No implicit enable, cache install или повышение context limit как замена сокращению.
- Group: PAOS-AUD-G4
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F10
- Blocks: PAOS-AUD-HOST-01
- Source: F09
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Progressive disclosure без повторной загрузки одинаковых политик и искусственного увеличения context budget. Missing host/product gates остаются открытыми.
- Verification gates: Skill metadata/links/contract tests, baseline/source digest comparison; behavioral comparison — через отдельный замороженный treatment, не смешивать с B45 compact-contract intervention. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; directory scope означает только 12 canonical skills и непосредственно используемые references; точный file manifest фиксируется до правки. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; directory scope означает только 12 canonical skills и непосредственно используемые references; точный file manifest фиксируется до правки.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F10`

- ID: `PAOS-AUD-F10`
- Task: **Название задачи:** Устранить дублирование и конфликт instruction authority
- Short description: **Описание задачи:** Заменить устаревший tests/AGENTS.md короткими English test-specific правилами. В canonical skills отделить default read-only роль от явно авторизованной задачи; согласовать использование неизменившегося evidence. Не удалить намеренные role restrictions.
- Technical value: **Техническое значение (для проекта):** Единая иерархия инструкций; factual source authority не смешивается с instruction precedence.
- Product value: **Продуктовое значение (для пользователя):** Меньше противоречащих указаний и повторных запросов уже данного разрешения.
- Scope: **Затрагиваемые файлы:** `tests/AGENTS.md`; `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`; `plugins/product-agent-os/skills/completion-skeptic/SKILL.md`; `plugins/product-agent-os/skills/`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) tests/AGENTS.md на английском, содержит только уместные test-specific инструкции и корректную hierarchy. 2) Общие правила не конфликтуют с действующей root policy; read-only assurance и approval boundaries сохранены. 3) Проверено отсутствие дублирующих противоречий в остальных canonical skills; правятся только найденные случаи. 4) Static correction не объявляется runtime discovery proof; при таком claim нужен fresh-session receipt.
- Group: PAOS-AUD-G4
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F09
- Source: F10
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Единая иерархия инструкций; factual source authority не смешивается с instruction precedence. Missing host/product gates остаются открытыми.
- Verification gates: Static instruction comparison, skill contract tests; snapshot baseline; source loading проверяется отдельно при необходимости. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; глобальный AGENTS.md и настройки host не входят в scope. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: lifecycle-orchestrator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; глобальный AGENTS.md и настройки host не входят в scope.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F15`

- ID: `PAOS-AUD-F15`
- Task: **Название задачи:** Устранить измеренные повторные scans и дублирование модулей
- Short description: **Описание задачи:** На fixed synthetic workspace измерить повторные inventory/scans и стоимость ordinary route. Переиспользовать immutable inventory snapshot и выделять detector/render contracts лишь там, где измерения и callers подтверждают пользу. Размер файлов сам по себе не основание для правки.
- Technical value: **Техническое значение (для проекта):** Снижение повторной работы и связности без новой БД, workflow engine или provider abstraction.
- Product value: **Продуктовое значение (для пользователя):** Быстрее анализ проекта и меньше противоречивых выводов между представлениями.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/scripts/product_agent_os/discovery.py`; `plugins/product-agent-os/scripts/product_agent_os/methodology_audit.py`; `plugins/product-agent-os/scripts/product_agent_os/first_run_analysis.py`; `plugins/product-agent-os/scripts/product_agent_os/code_quality_metrics.py`; `tests/product_agent_os/test_methodology_audit.py`; `tests/product_agent_os/test_infrastructure_renderer.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) До изменения записан baseline scan counts/runtime/output на одинаковом fixture и окружении. 2) После изменения output contracts и safety boundaries сохранены; уменьшение повторных операций измерено. 3) Если существенного дублирования не подтверждено, задача закрывается accepted_gap с обоснованием без рефакторинга. 4) Выделение нового модуля допускается только после фиксации конкретной границы и собственного test coverage; live semantic/provider claims не добавляются.
- Group: PAOS-AUD-G4
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F05
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F15
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Снижение повторной работы и связности без новой БД, workflow engine или provider abstraction. Missing host/product gates остаются открытыми.
- Verification gates: Characterization existing tests, deterministic output comparison, bounded repeated timing/scan measurement; расширение file scope только по выявленным callers. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; условная оптимизация, не обязательное переписывание больших модулей. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; условная оптимизация, не обязательное переписывание больших модулей.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

## PAOS-AUD-G5 — Документация, offline tooling и актуальный site

- **ID:** `PAOS-AUD-G5`
- **Название группы:** Документация, offline tooling и актуальный site
- **Описание группы:** Исправить offline installer, обновить package README и синхронизировать RU/EN, registry и generated site после локальных правок.
- **Техническое значение (для проекта):** Воспроизводимый offline command contract и согласованный source/build output.
- **Продуктовое значение (для пользователя):** Пользователь следует актуальному стартовому маршруту и получает одинаковые инструкции на русском и английском.
- **Затрагиваемые файлы:** `tools/docs_install.ps1`; `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `site/`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** Offline path не формирует сетевых install-команд; README/examples согласованы; strict build, RU/EN links/anchors и Mermaid check проходят; публикации нет.
- **Зависимости и порядок:** F13 можно раньше. Документацию обновлять вместе с каждой группой; итоговый F14/F17 после G1–G4. После G6 обновлять только новые receipts и затронутые страницы.
- **Предлагаемая ответственность:** docs-maintainer; installer — plugin-runtime-builder.

### Task `PAOS-AUD-F13`

- ID: `PAOS-AUD-F13`
- Task: **Название задачи:** Обеспечить offline contract документационного installer
- Short description: **Описание задачи:** Убрать unconditional pip upgrade до offline branch либо провести весь install через указанный wheelhouse. Проверить формирование команд через stub, сохранив project-local tooling.
- Technical value: **Техническое значение (для проекта):** Offline режим действительно не строит сетевых package-install команд.
- Product value: **Продуктовое значение (для пользователя):** В закрытой сети установка не зависает на неожиданном обращении к package index.
- Scope: **Затрагиваемые файлы:** `tools/docs_install.ps1`; `tests/product_agent_os/test_product_agent_os_docs.py`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) OfflineWheelhouse path исключает index/network для всех pip вызовов, включая upgrade/bootstrap. 2) Online mode остаётся явным; отсутствие нужного wheel даёт понятную локальную ошибку. 3) Command-contract test не устанавливает зависимости и не меняет глобальную среду.
- Group: PAOS-AUD-G5
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана.
- Blocks: PAOS-AUD-F17
- Source: F13
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Offline режим действительно не строит сетевых package-install команд. Missing host/product gates остаются открытыми.
- Verification gates: Stubbed installer command inspection + existing docs tests; настоящая установка не требуется для локального command contract. Общие gates — TEST.md и правила выше.
- Risks / approval gates: low; dependency installation вне текущей задачи планирования и отдельно согласуется при необходимости. Rollback — по общим правилам.
- Complexity: low
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: plugin-runtime-builder; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: low; dependency installation вне текущей задачи планирования и отдельно согласуется при необходимости.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F14`

- ID: `PAOS-AUD-F14`
- Task: **Название задачи:** Обновить package README и стартовый маршрут
- Short description: **Описание задачи:** Сделать короткий start path с explicit skill invocation и ordinary task context. Согласовать MCP example, supported surfaces и manifest variants; убрать исторические counts из актуального summary, сохранив ссылки на owning evidence.
- Technical value: **Техническое значение (для проекта):** Package entrypoint соответствует public CLI и текущим compatibility contracts.
- Product value: **Продуктовое значение (для пользователя):** Новый пользователь начинает с рабочего минимального пути и понимает ограничения установки.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/README.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Примеры args/JSON соответствуют реализации и проходят локальные syntax/CLI contract checks. 2) Виден supported/unsupported/not_verified; explicit-only skills вызываются явно; ordinary route не скрыт за full generation. 3) Historical receipts доступны по ссылкам и не выданы за текущий запуск; неизвестные distribution данные не придуманы.
- Group: PAOS-AUD-G5
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F05
- Blocks: PAOS-AUD-F17
- Source: F14
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Package entrypoint соответствует public CLI и текущим compatibility contracts. Missing host/product gates остаются открытыми.
- Verification gates: Docs tests/check_docs, example syntax, локальная проверка CLI help/dry-run; без MCP execution. Общие gates — TEST.md и правила выше.
- Risks / approval gates: low; не заявлять activation на основании source tests. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: docs-maintainer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: low; не заявлять activation на основании source tests.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-F17`

- ID: `PAOS-AUD-F17`
- Task: **Название задачи:** Синхронизировать RU/EN и пересобрать локальный site
- Short description: **Описание задачи:** Согласовать изменённые user guides и registry; проверить затронутые Mermaid diagrams. После локальных changes пересобрать site существующими project-local средствами, проверить routes, links, anchors и диаграммы. После host receipts обновлять только новые claims.
- Technical value: **Техническое значение (для проекта):** Generated site воспроизводимо соответствует проверенным source files.
- Product value: **Продуктовое значение (для пользователя):** На русском и английском доступны одинаково актуальные инструкции и рабочая навигация.
- Scope: **Затрагиваемые файлы:** `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`; `docs/codex/models-and-reasoning.md`; `docs/codex/models-and-reasoning.en.md`; `docs/sources/registry.md`; `docs/sources/registry.en.md`; `docs/diagrams/`; `mkdocs.yml`; `site/`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Ручная semantic parity затронутых RU/EN пар и Source status актуальны; 10 English-original plans не объявляются missing translations. 2) Docs checks и strict MkDocs build проходят; internal routes/links/anchors проверены по generated output. 3) Затронутые Mermaid diagrams успешно разобраны/отрендерены разрешённым инструментом; отсутствие runtime render явно оставляет соответствующий gate открытым. 4) Site receipt связан с source revision; сайт не опубликован; dependencies/automation/hooks не активированы автоматически.
- Group: PAOS-AUD-G5
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F03, PAOS-AUD-F13, PAOS-AUD-F14, PAOS-AUD-F16 Финальная local сборка после всех фактически выполненных G1–G4 изменений, включая F09/F10/F15; host receipts обновляются отдельной малой синхронизацией.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: F17
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Generated site воспроизводимо соответствует проверенным source files. Missing host/product gates остаются открытыми.
- Verification gates: 100-case docs suite в текущем составе, check_docs, strict MkDocs, generated link/anchor check и Mermaid rendering при точной authority; git diff --check. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; mkdocs.yml/diagrams правятся только если затронуты новой документацией; browser/server/install/publication не следуют из сохранения плана. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: docs-maintainer; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; mkdocs.yml/diagrams правятся только если затронуты новой документацией; browser/server/install/publication не следуют из сохранения плана.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

## PAOS-AUD-G6 — Проверка GPT-6, host activation и пользовательской пользы

- **ID:** `PAOS-AUD-G6`
- **Название группы:** Проверка GPT-6, host activation и пользовательской пользы
- **Описание группы:** Продолжить существующие T30–T34 и оставшиеся GAP gates; отдельно доказать local readiness, host behavior, качество treatment и полезность ordinary flow.
- **Техническое значение (для проекта):** Раздельные воспроизводимые evidence для конфигурации, активации, качества и acceptance.
- **Продуктовое значение (для пользователя):** Улучшение оценивается по успешной работе и затратам пользователя, а не по наличию GPT-6 ID или числу тестов.
- **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `EVALS.md`; `RUNLOG.md`. Полный task-specific scope — в карточках.
- **Критерии приёмки группы:** T30–T34 закрываются только по своим canonical gates; fresh-host receipts привязаны к версиям/хешам; pilot имеет owner acceptance; missing evidence сохраняет no-go/partial.
- **Зависимости и порядок:** T30/T31 готовить параллельно локальным fixes по независимым файлам; T32 после стабильного baseline, T33 после T32, T34 только после T33 и exact approval. Host gates после итоговых G1/G2.
- **Предлагаемая ответственность:** Роли существующих T30–T34; host — tester; pilot — product-manager.

### Task `B45-CQRR-T30`

- ID: `B45-CQRR-T30`
- Task: **Название задачи:** Implement an independent blinded reviewer contract
- Short description: **Описание задачи:** Реализовать контракт независимого reviewer для baseline/treatment patches без arm labels и primary self-scores. Reviewer допускается только после valid deterministic pair evidence; critical findings имеют приоритет над средними оценками.
- Technical value: **Техническое значение (для проекта):** Независимая проверка качества отделена от самооценки generating model.
- Product value: **Продуктовое значение (для пользователя):** Ошибки корректности, безопасности и лишняя сложность не скрываются хорошим средним баллом.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/assets/templates/evals/code-quality-reviewer-rubric.json` (proposed new); `plugins/product-agent-os/scripts/codex_runtime_runner/reviewer_contract.py` (proposed new); `tests/product_agent_os/test_batch45_code_quality_reviewer.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Reviewer input не содержит baseline/treatment labels и primary self-scores. 2) Verdict blocked до валидного deterministic pair evidence. 3) Critical correctness/security/data-loss/regression findings перекрывают averages.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана. B45-CQRR-T29 — локально выполнена.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Существующая B45-CQRR-T30; canonical title/depends_on/acceptance сохранены из task-group JSON. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Независимая проверка качества отделена от самооценки generating model. Missing host/product gates остаются открытыми.
- Verification gates: Blinding, invalid pair gate и critical override tests на synthetic pairs. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; live reviewer call требует отдельного exact approval, локальная реализация его не разрешает. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: architect; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; live reviewer call требует отдельного exact approval, локальная реализация его не разрешает.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `B45-CQRR-T31`

- ID: `B45-CQRR-T31`
- Task: **Название задачи:** Build a representative multi-stack held-out corpus
- Short description: **Описание задачи:** Подготовить 12–16 sanitized/synthetic задач минимум четырёх stack families и пяти risk classes. Включить small change, legacy bug, boundary, unnecessary-abstraction и performance cases, а также решения через reuse/config/delete/no-new-code. Freeze до просмотра treatment outputs.
- Technical value: **Техническое значение (для проекта):** Проверка на репрезентативном отложенном наборе вместо подгонки под внутренние восемь задач.
- Product value: **Продуктовое значение (для пользователя):** Оценка ближе к разным реальным проектам и не поощряет ненужное написание кода.
- Scope: **Затрагиваемые файлы:** `tests/fixtures/product_agent_os/batch45/code-quality-corpus/` (proposed new); `docs/superpowers/specs/batch45-code-quality-heldout-corpus.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_corpus.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Представлены минимум четыре stack families и пять risk classes; 12–16 задач с проверяемым ожидаемым результатом. 2) Корпус заморожен с hashes до inspection treatment; последующая настройка под результат запрещена. 3) Нет secrets/private source/raw chats/customer data/absolute user paths. 4) Присутствуют случаи правильного отказа от нового кода, reuse, config и deletion.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: Нет новых обязательных задач этого плана. B45-CQRR-T27 и T29 — локально выполнены; независима от T30.
- Blocks: B45-CQRR-T32, B45-CQRR-T33
- Source: Существующая B45-CQRR-T31. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Проверка на репрезентативном отложенном наборе вместо подгонки под внутренние восемь задач. Missing host/product gates остаются открытыми.
- Verification gates: Schema, privacy/secret scan, difficulty/risk matrix и hash freeze validation. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; не использовать неразрешённый target source для наполнения корпуса. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить актуальность finding и baseline, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; не использовать неразрешённый target source для наполнения корпуса.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `B45-CQRR-T32`

- ID: `B45-CQRR-T32`
- Task: **Название задачи:** Freeze an isolated treatment and executable prompt contract
- Short description: **Описание задачи:** Зафиксировать exact baseline/treatment prompt/context templates. В первичном сравнении меняется только compact pre-edit contract; reviewer assistance и comment advisory остаются отдельными later factors. Итоговые skill/route changes G4 должны быть одинаковы в обеих arms или исключены из comparison.
- Technical value: **Техническое значение (для проекта):** Причина результата измерима: один фактор вместо одновременной смены модели, effort, prompts и маршрута.
- Product value: **Продуктовое значение (для пользователя):** Решение об улучшении основано на проверяемом эффекте, а не на впечатлении от новой модели.
- Scope: **Затрагиваемые файлы:** `plugins/product-agent-os/assets/templates/evals/code-quality-baseline-prompt.md` (proposed new); `plugins/product-agent-os/assets/templates/evals/code-quality-treatment-prompt.md` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-design.json` (proposed new); `tests/product_agent_os/test_batch45_code_quality_eval_design.py` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Baseline/treatment используют одинаковые model, effort, runner, timeout, tools и corpus. 2) Ровно один planned intervention различается; точные templates/context digests воспроизводимы без private raw data. 3) Full research/checklist не вставлен в каждый generation prompt. 4) Изменение model/effort или отдельное skill-shortening treatment требует нового изолированного design, не приписывается этому сравнению.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T30, B45-CQRR-T31 B45-CQRR-T25 выполнена; freeze после стабильного baseline затронутых G1–G4. Не объявлять внешнюю sequencing рекомендацию изменением canonical depends_on.
- Blocks: B45-CQRR-T33
- Source: Существующая B45-CQRR-T32. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Причина результата измерима: один фактор вместо одновременной смены модели, effort, prompts и маршрута. Missing host/product gates остаются открытыми.
- Verification gates: Prompt/context diff, digest reproducibility и no-extra-variable contract tests. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; не корректировать prompts после просмотра held-out treatment outputs. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: architect; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; не корректировать prompts после просмотра held-out treatment outputs.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `B45-CQRR-T33`

- ID: `B45-CQRR-T33`
- Task: **Название задачи:** Run the local promotion-readiness preflight
- Short description: **Описание задачи:** Проверить локальную воспроизводимость executable schema, normalization, deterministic metrics, reviewer gate, frozen corpus и isolated prompt contract. Сохранить readiness evidence до подготовки нового live approval packet.
- Technical value: **Техническое значение (для проекта):** Локальные дефекты контрактов выявлены до затрат на provider/model/reviewer вызовы.
- Product value: **Продуктовое значение (для пользователя):** Меньше бесполезных запусков и более понятное решение о готовности к эксперименту.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-local-readiness.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Все valid fixtures проходят, все invalid дают ожидаемый failure class. 2) Seeded faults обнаруживаются предназначенным тестом/метрикой. 3) Blinding/reviewer gate работают на synthetic pairs; corpus/prompts hashes воспроизводимы. 4) Нет provider/model/reviewer calls; любой обязательный failed/missing gate сохраняет no-go.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T30, B45-CQRR-T31, B45-CQRR-T32 B45-CQRR-T24, T28, T29 выполнены.
- Blocks: B45-CQRR-T34
- Source: Существующая B45-CQRR-T33. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Локальные дефекты контрактов выявлены до затрат на provider/model/reviewer вызовы. Missing host/product gates остаются открытыми.
- Verification gates: Focused contract/strategy tests, seeded-fault replay, freeze checks, docs/source registry checks и diff hygiene. Общие gates — TEST.md и правила выше.
- Risks / approval gates: medium; local readiness не равна behavioral promotion или product acceptance. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: completion-skeptic; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: medium; local readiness не равна behavioral promotion или product acceptance.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `B45-CQRR-T34`

- ID: `B45-CQRR-T34`
- Task: **Название задачи:** Prepare, execute and decide a new promotion eval only after exact approval
- Short description: **Описание задачи:** После T33 подготовить конкретный reviewable approval packet; только после exact owner approval выполнить frozen same-model comparison. Reviewer вызывается после valid pairs. Решение promotion/no-go основывается на deterministic evidence и независимых findings.
- Technical value: **Техническое значение (для проекта):** Связанные с checked state quality/cost/latency evidence для выбранной GPT-6 конфигурации.
- Product value: **Продуктовое значение (для пользователя):** Продвигается только улучшение с приемлемой корректностью, затратами и временем ответа.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch45-code-quality-eval-approval-packet.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-eval-results.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-promotion-decision.json` (proposed new); `docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json`; `EVALS.md`; `RUNLOG.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Exact approval задаёт model, effort, call cap, timeout, cost, retention и reviewer policy до вызовов. 2) Все учитываемые pairs schema-valid и имеют deterministic acceptance; reviewer выполнен без unresolved critical findings. 3) Latency/token/cost/performance за frozen tolerance блокируют promotion либо имеют отдельное owner-accepted исключение. 4) При incomplete/invalid/mixed evidence остаётся no-go; raw private outputs не сохраняются. 5) Same-model результат не объявляется доказательством превосходства всей GPT-6 family; model/effort changes сравниваются отдельно.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: B45-CQRR-T33
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: Существующая B45-CQRR-T34; behavioral часть F04. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Связанные с checked state quality/cost/latency evidence для выбранной GPT-6 конфигурации. Missing host/product gates остаются открытыми.
- Verification gates: Approval preflight, sanitized results validation, independent reviewer evidence, retention/no-unapproved-actions checks, control-plane sync. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; approval_required_not_started; сохранение этого плана не разрешает live calls. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: release-operator; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; approval_required_not_started; сохранение этого плана не разрешает live calls.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-HOST-01`

- ID: `PAOS-AUD-HOST-01`
- Task: **Название задачи:** Закрыть оставшийся GAP-03 M06: exposure и invocation выбранного host
- Short description: **Описание задачи:** На выбранной поддерживаемой surface проверить canonical/installed source provenance, exposure и явный вызов skill. Записать client/surface, hashes, observed model при доступном receipt. Если нужен cache update, сначала подготовить конкретный preview/rollback и получить точную authority.
- Technical value: **Техническое значение (для проекта):** Связь source package с реально загруженными host компонентами.
- Product value: **Продуктовое значение (для пользователя):** Пользователь знает, что установленные skills соответствуют исправленной версии и вызываются ожидаемым способом.
- Scope: **Затрагиваемые файлы:** `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `docs/product-agent-os/control-plane-current-state.md`; `docs/product-agent-os/control-plane-current-state.en.md`; `TEST.md`; `RUNLOG.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Выбранный host/surface поддерживается; version/source/cache digests и invocation evidence связаны с проверенным состоянием. 2) Configured model отдельно от observed; при отсутствии model receipt поле остаётся not_verified. 3) Explicit-only skill не объявляется implicit; source/cache mismatch имеет явное решение и не скрывается. 4) GAP-03 M06 закрывается только своим evidence; parent статус обновляется в owning плане, а не независимом registry.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F01, PAOS-AUD-F02, PAOS-AUD-F04, PAOS-AUD-F09
- Blocks: PAOS-GAP-06
- Source: GAP-03 M06; F02/F04/F09. ID — адрес конкретного этапа этого плана, не новая замена parent GAP-03.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Связь source package с реально загруженными host компонентами. Missing host/product gates остаются открытыми.
- Verification gates: Ограниченный fresh-host exposure/invocation receipt; exact commands/target выбираются после host scope, не выдумываются в общем плане. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; installation/cache/trust/provider actions имеют отдельную точную authority. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; installation/cache/trust/provider actions имеют отдельную точную authority.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-AUD-HOST-02`

- ID: `PAOS-AUD-HOST-02`
- Task: **Название задачи:** Закрыть оставшиеся GAP-05 и fresh-host lifecycle gates
- Short description: **Описание задачи:** После финальных source hashes проверить фактическую загрузку hooks, positive/negative сценарии, report-authoring и независимость новых чатов. Отдельно проверить generated target route на точном разрешённом disposable target. Сохранить различие current-host observation и fresh-host evidence.
- Technical value: **Техническое значение (для проекта):** Подтверждение активного исправленного пути и отсутствия маскирующего legacy fallback.
- Product value: **Продуктовое значение (для пользователя):** Новые чаты не мешают друг другу; разрешённый отчёт сохраняется, чужие/выходящие за scope записи блокируются.
- Scope: **Затрагиваемые файлы:** `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`; `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`; `TEST.md`; `RUNLOG.md`; `docs/runtime/worktrees-hooks-rules.md`; `docs/runtime/worktrees-hooks-rules.en.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) Receipt содержит version, exact definition/source hashes, выбранный config path, trust observation и workspace scope. 2) Fresh positive и безопасный negative probe подтверждены output/absence evidence; filesystem failure не выдан за hook denial. 3) Два новых session-aware чата изолированы; чужой marker и старый shared marker не авторизуют mutation. 4) Generated config действительно загружается; ранее неактивный mirror/legacy route не маскирует результат. 5) Report create/update проходит только в согласованных границах; изменение hashes после проверки вновь открывает затронутый gate.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-F06, PAOS-AUD-F12, PAOS-AUD-F18 Если активируются rules из F11, effective-policy probe оформляется отдельным ограниченным подпунктом с собственной authority.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: GAP-05; F06/F12/F18; PAOS-SESSION-LIFECYCLE-2026-11-09. ID — объединённый verification этап, не повторная реализация parent задач.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Подтверждение активного исправленного пути и отсутствия маскирующего legacy fallback. Missing host/product gates остаются открытыми.
- Verification gates: Fresh-host bounded positive/negative receipts и source hashes; synthetic tests повторять только по изменённому контракту. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; actual target writes, hook trust/definitions и fresh-host execution требуют точного разрешения; permission не выводится из plan status. Rollback — по общим правилам.
- Complexity: high
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: tester; security review read-only; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; actual target writes, hook trust/definitions и fresh-host execution требуют точного разрешения; permission не выводится из plan status.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

### Task `PAOS-GAP-06`

- ID: `PAOS-GAP-06`
- Task: **Название задачи:** Проверить ordinary user outcomes через существующие B39/B44 manual packets
- Short description: **Описание задачи:** Сначала согласовать 3–5 representative задач и конкретные targets: bugfix, docs, legacy, no-new-code, boundary change. Начать с одного bounded ordinary pilot, затем продолжить выбранный набор. Измерять время до полезного результата, лишние вопросы/артефакты, повторные проверки, correctness и owner intervention.
- Technical value: **Техническое значение (для проекта):** Проверка сквозного пользовательского пути после локальных contract gates.
- Product value: **Продуктовое значение (для пользователя):** Подтверждение, что Product-Agent OS действительно уменьшает усилия пользователя и даёт пригодный результат.
- Scope: **Затрагиваемые файлы:** `docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json`; `prod_test.md`; `RUNLOG.md`; `research/product-agent-os-ordinary-route-implementation-plan-2026-11-05.md`. Общий docs/control-plane scope — по правилам выше.
- Acceptance criteria: **Критерии приёмки:** 1) До запуска согласованы tasks/targets/allowed actions/rollback и baseline measurements. 2) Есть per-task outcome, owner feedback/acceptance и сохранённые failed cases; один pilot не объявляется закрытием полного representative набора. 3) Выявленные улучшения идут в существующий manual candidate loop; нет automatic promotion/schedules/auto-apply. 4) prod_test.md меняется только если действительно создаётся evidence его B39 family; прочая история не переписывается.
- Group: PAOS-AUD-G6
- Status: planned
- Schema version: task_matrix_plan_v1
- Timezone: Europe/Moscow
- Plan trigger: Сохранение плана по запросу владельца; execution не разрешён.
- Validator target: detailed task blocks
- Date and time of task implementation: pending_execution_timestamp
- Depends on: PAOS-AUD-HOST-01, PAOS-AUD-F05, PAOS-AUD-F08 ORD-06 выполнена; AUD-HOST-02 требуется только для выбранных report-authority/hook scenarios. T34 не является обязательной зависимостью обычного owner pilot.
- Blocks: Нет обязательной downstream implementation зависимости в этом документе; собственный acceptance gate сохраняется.
- Source: Существующая PAOS-GAP-06 из ordinary implementation plan; canonical scope сохранён. Исходный owning план/JSON сохраняет authority; эта карточка не является новым machine status.
- Non-goals: См. общие границы; completed baseline не переделывать.
- Expected result: Проверка сквозного пользовательского пути после локальных contract gates. Missing host/product gates остаются открытыми.
- Verification gates: Разрешённый target journey и structured owner feedback. Точные live команды задаются после выбора target; no invented current-run receipt. Общие gates — TEST.md и правила выше.
- Risks / approval gates: high; target/runtime/provider/browser действия не разрешены текущим запросом на файл. Rollback — по общим правилам.
- Complexity: medium
- Estimated execution time: not_estimated; после preflight конкретного slice.
- Agents: product-manager; evidence — learning-loop-engineer; acceptance — пользователь; ownership recommendation, delegation не запущена.
- Skills: По типу slice и общим правилам выше; в authoring не применялись.
- Output artifacts: Scope files и evidence в owning плане; proposed paths пока отсутствуют.
- Next step: Проверить названные зависимости, затем согласовать точный local file scope, воспроизвести исходный case и выполнить только эту задачу после запроса на реализацию.

#### Completion Report

- status: planned
- what was done: Не выполнялась.
- files touched / work locations: Не изменены.
- technical value delivered: Не подтверждено.
- product value delivered: Не подтверждено.
- actual implementation date and time: pending_execution_timestamp
- verification evidence: pending_execution; authoring checks не доказывают implementation.
- residual risks: high; target/runtime/provider/browser действия не разрешены текущим запросом на файл.
- follow-up: Выполнить Dependencies и Acceptance в авторизованном slice.

