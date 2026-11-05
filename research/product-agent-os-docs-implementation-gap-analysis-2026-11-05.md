# Product-Agent OS: документация, реализация и следующие работы

Source status: `official + project-local inspection`. Дата: 05.11.2026. Статус: **исследование завершено / inspection findings verified**. Это не implementation closure или product promotion.

## Главный вывод

Product-Agent OS уже имеет существенную локальную реализацию: discovery, staged infrastructure, безопасное применение с approval/rollback, lifecycle contracts, methodology routing, graph/cockpit/status surfaces, ручной learning loop и часть code-quality pipeline. Новая документация **не требует переписывать систему на Agents API/SDK или автоматически включать Cloud, memory и schedules**.

Главный разрыв — между реализованными локальными компонентами и целостным пользовательским маршрутом. Короткий ordinary workflow заявлен, но generator/router/активные инструкции остаются тяжёлыми; новые quality selectors есть, но прямые production call sites не найдены; installed skills отличаются от source; compatibility/inventory расходятся. Поэтому следующий полезный результат — связать и упростить существующую систему, а затем завершить уже запланированную независимую оценку T30–T34.

Не следует заново выполнять ACT-F1..F6 или T23–T29 как будто они отсутствуют. Для ACT repair совпали **12/12 сохранённых source hashes**; его узкое local Desktop evidence остаётся применимым к тем же файлам. Но оно не доказывает всю hook coverage, другие hosts, качество новых моделей или production readiness.

## Область и метод

По запросу владельца после обновления пользовательской документации сопоставляются guides → планы и task receipts → код → tests → наблюдаемые результаты. Разрешена запись только этого Markdown и, после отдельного ответа владельца, служебного `.codex/product-agent-os/lifecycle-state.json`. Реализация, существующие документы и планы, site, Git, настройки и hook trust не меняются. Не выполняются provider/model/browser calls, новые runtime activation probes или deployment.

Статусы реализации и исторические test counts не равны новому запуску тестов. Разделяются: код существует; локальная проверка записана в receipt; runtime наблюдался в ограниченном сценарии; поведенческое/продуктовое доказательство отсутствует. Отрицательный поиск означает отсутствие в проверенной области, а не универсальное отсутствие функции.

## Журнал исследования

### 1. Control-plane и текущая очередь

- PLAN.md:67,79 и source-owned `batch45-code-quality-runtime-recovery-task-group.json` подтверждают локально выполненные T23–T29; следующая зависимость T30. В RUNLOG.md ниже свежей сводки остаётся таблица, предлагающая начать T28. Это ошибка актуальности маршрутизации, а не отсутствие T28/T29.
- PLAN.md:70 сохраняет legacy `ready_for_completion_brief` и one-Stop-correction, хотя текущий `.codex/workflows/task-plan-lifecycle.md` разделяет full/concise и advisory Stop. Свежий вводный раздел не устраняет противоречия ниже.
- EVALS.md:58,69 и T22-A02 сохраняют no-go до независимой оценки. Обновление сайта не подтверждает улучшение модели или promotion.
- При создании этого отчёта реальный PreToolUse отказал с `completion_ready marker cannot authorize further mutation`: оставался terminal marker предыдущей задачи. После отдельного разрешения владельца marker переведён на report-only запись. Это наблюдение о переходе между задачами; оно не отменяет успешное ACT-F1 denial evidence.

### 2. Первые подтверждённые расхождения кода

- `codex_runtime_runner/routes.py:94–101`: даже maintenance route перечисляет шесть обязательных control-plane файлов, полный unittest discovery и fixture eval. `routes.py:122,155` продолжает требовать coding-standard-checklist. Это расходится с коротким ordinary workflow и компактным contract в guides.
- `code_quality_selector.py:174` и `test_strategy_selector.py:147` уже реализуют pure selectors, но принимают объявленный inventory/risk; сами не читают проект и не исполняют tools. Поиск consumers в scripts пока находит определения и tests, но не adapter в discovery/runner. Следует подключать готовые блоки, а не переписывать их.
- `codex_compatibility.py:102` читает flat `context7`; `batch39_inventory.py:139` ожидает `mcpServers`. Текущий пакет содержит flat object. Вызов обеих функций дал одновременно `compatible / Context7 ... secret-free` и `mcp_server_keys: []`. Это воспроизведённое внутреннее расхождение.
- Manifest `.codex-plugin/plugin.json:4` всё ещё объявляет `Production-ready`, несмотря на локальную/manual claim ceiling и promotion no-go. Compatibility result объединяет Codex App, CLI, IDE extension без component-level различения.

### 3. Реализованные задачи и незакрытые gates

- T23/T24: versioned promotion contract, normalization, invalid-output quarantine и regression fixtures существуют.
- T25: восьмипольный code-change-contract существует; full checklist остаётся reviewer/reference.
- T26/T27: stack/tool и risk/test selectors существуют; значения остаются present_unverified до выполнения проверок.
- T28/T29: source-owned A06 подтверждает semantic test repair и deterministic metrics; self-scores не участвуют в promotion decision.
- T30–T33 имеют planned_not_started; T34 approval_required_not_started. Independent blinded reviewer, новый multi-stack corpus, isolated prompt contract и local preflight нельзя считать выполненными.
- Batch 44 S7: один manual pilot, 1 feedback row, 1 metrics row, 2 candidates; Promptfoo export содержит 8 cases, но runner Promptfoo не запускался. Это основание для owner review, а не автоматизации.

### 4. Генератор и активный workflow: упрощение ещё не подключено полностью

- `templates.py:1224` возвращает весь `_TEMPLATES`; `_build_result` в `infrastructure.py:142` проходит этот список без отбора по profile. Статический вызов `required_templates()` дал **209** templates: 6 control-plane, 1 config, 150 artifact templates, 8 agents, 6 hooks, 27 workflows, 1 runlog, 5 evals, 3 automation candidates, 2 PR artifacts. Это размер набора предложений, не число автоматически активированных файлов. Даже guided-small не меняет сам список; существующие пользовательские файлы и authority далее защищаются отдельными механизмами.
- `.codex/workflows/coding-standards.md:25,44` всё ещё использует full checklist. Packaged workflow:11–14,31,62 уже использует compact code-change-contract. В активном `.codex/artifact-templates/` этого contract нет. Следовательно T25 завершён для staged package, но не доказан как применённый текущий workflow.
- `state.py:20–35` выводит lifecycle по строкам Acceptance Criteria, Verification, Quality gates и наличию builder.toml. На текущем репозитории pure inference вернул team_ready. Это эвристическая project state, не надёжная очередь конкретной задачи; переходы не связаны с новым task scope или authoritative task-group status.

### 5. Canonical skill source, installed cache и exposure

- Все 12 canonical skills существуют и все 12 имеют `allow_implicit_invocation: false` в agents/openai.yaml. Это сознательный explicit-only контракт, не доказательство неисправности. Обещание автоматического подхвата нельзя делать до отдельной policy/eval работы.
- В проверенном установленном cache версии 0.1.0 также 12 skills; **11/12 SKILL.md содержательно отличаются** от canonical source даже после нормализации BOM/CRLF. Для docs-maintainer cache сохраняет staged-only / запрет прямого редактирования; canonical разрешает назначенные локальные docs edits при explicit_task_authority. Completion-skeptic совпадает.
- Этот факт не доказывает, что текущий chat использует cache: проект явно маршрутизирует canonical source, и здесь использован именно он. Для другого workspace установка пакета может дать другое поведение. Нужны source/cache hash и fresh-session exposure receipts, а не повторное объявление «12 skills installed».
- Batch 42 M02, M04–M08 уже планирует inventory, invocation policy, metadata validator и fresh-session route/evals. Следует уточнить и исполнить эту существующую очередь, не создавать параллельный проект.

### 6. Source-policy и проверки совместимости

- Pure `_has_official_source_hint` возвращает false для ссылок learn.chatgpt.com и platform.openai.com без английского Sources:, true для developers.openai.com, но также true для строки `Sources: unsupported assertion`. Это намеренно heuristic marker check, а не проверка истинности; актуальные official domains и claim/source linkage в ней не представлены.
- Текущие read-only validators: active agents 15/15, active hooks 7 files, staged hooks 7 files — exit 0. Compatibility validator тоже exit 0, несмотря на воспроизведённое расхождение MCP inventory. Успех существующего validator не закрывает неизвестные ему контракты.
- `.codex/config.toml` уже содержит default_permissions=:workspace, generic gpt-6.1-sol/medium; 15 active и 8 staged profiles используют inheritance contracts. Повторная migration с устаревшего sandbox_mode или повторное исправление ACT-F3..F6 не обоснованы.

### 7. Состояние прежних gates

- T21: abort на первом primary output из-за tests_or_checks.status; T22: 0 valid pairs вместо требуемых 8, reviewer gate не запускался, promotion=false. T23/T24 исправляют local contract, но нового оплаченного сравнения это не заменяет.
- Старый Batch 39 S5 содержит blocker «MkDocs unavailable». После site refresh от 05.11 он больше не описывает текущее локальное состояние docs toolchain. Исторический receipt менять не следует; нужен current closure overlay для этого blocker, сохранив отдельные owner-feedback, target/runtime, MCP и release gates.
- Архивные labels добавлены также на планы, которые остаются current source pointers для активной очереди, включая loop-remediation и Track 11. Label history допустим для receipts, но не должен означать retirement незавершённых задач. При будущей правке navigation/status нужно различить history и действующий backlog.

### 8. Проверка интеграционных точек и отрицательных примеров

- AST-поиск вызовов во всех Python-файлах `plugins/product-agent-os/scripts/` не нашёл consumers `select_code_quality_profile`, `select_test_strategy` и `evaluate_deterministic_promotion`. `evaluate_code_quality_metrics` вызывается только wrapper в promotion_contract.py:147. Это сильное статическое свидетельство незавершённого подключения; динамические вызовы или ручное использование agent tools этим методом не исключаются.
- На синтетическом in-memory RU context, содержащем «Требования / Критерии приёмки / План / Проверка», state inference выдал infrastructure_planned; отсутствие оставшихся control-plane файлов дало needs_context. Файлы fixture не создавались. Результат согласуется с literal-English heading checks, но не доказывает поведение на всех RU проектах.
- Плановые файлы T30–T34 по proposed_files отсутствуют. Это подтверждает planned statuses в source-owned task group; наличие старых reviewer roles не заменяет независимый blinded reviewer contract.
- В старых планах Track 1–5 остались 0 checked и соответственно 41/28/39/48/48 unchecked steps, хотя код существует. Эти планы — исторические recipes; их checkbox counts нельзя интерпретировать как фактический backlog невыполненной реализации.

## Матрица: что уже реализовано

| Область | Что есть в файлах | Доказательство / задача | Чего это не доказывает |
| --- | --- | --- | --- |
| Read-only discovery, stack и usage modes | `discovery.py`, source-policy, profile и intent routing, stage proposals | Track 1, Track 8 S1–S16; detailed backlog и текущие функции | Семантически правильный маршрут любой задачи; английские keyword/heading эвристики имеют ограничения |
| Генератор инфраструктуры | Реестр 209 templates, renderer, dry-run/stage; запрет stage внутри target; companion proposals для пользовательских файлов | Track 3; `infrastructure.py:67–78,340–378` | Минимальный набор для small task; auto-apply в target |
| Approval-aware merge и rollback | plan-bound approval, повторная проверка target digest, rollback manifest | Track 4; `merge_infrastructure.py:44–105,554–615` | Безопасность произвольного target без его проверки/разрешения |
| Contract-mode runtime helper | Context loader, state inference, route/status/approval/redaction contracts | Track 5; `codex_runtime_runner/cli.py:20–83` | Автономное выполнение агентами или hosted runtime; helper сам не запускает модель |
| Methodology intelligence | Discovery signals, conditional applicability, domain synthesis и evidence gaps | Track 9, 12 методологических областей, methodology_audit/catalog/synthesis | Полную бизнес-корректность или реальное выполнение рекомендованных tools |
| Guided questions / dashboard / graph | Ограничение blocking questions, snapshots, staged HTML/graph и evidence boundaries | Track 10, Batch 41; question_protocol/status_dashboard/project_graph modules | Что generated view всегда свежий, либо что Cosmos.gl/WebGL/target apply проверены |
| Lifecycle reporting и hooks | Full v2 / concise, marker validation, advisory Stop, inherited authority, safe negative denial | 03.11 lifecycle parity + ACT repair; 12/12 receipt hashes совпадают | Silent Stop tracing, все aliases/tools/MCP paths, другие sessions/hosts |
| Agent configuration | 15 active + 8 staged profiles; parent permissions/provider/MCP; GPT-6.1 Sol/Terra pins | 03.11 technical_followup; свежий active-agent validator exit 0 | Quality/cost/latency improvement, effective availability каждой модели в аккаунте |
| Компактное code authoring | Восьмипольный contract в package templates, full checklist как reference | B45 T25, A05 | Что текущая `.codex` среда или основной router уже использует этот contract |
| Stack/risk selection | Pure typed inventory → profile; declared risks → test/comment/performance strategy | B45 T26/T27; code_quality_selector/test_strategy_selector; A05 54-test receipt | Автоматическое сканирование/исполнение или end-to-end integration |
| Output schema и quarantine | Versioned schema, status normalization, invalid output isolation | B45 T23/T24, A04; promotion_contract/model_output | Что новый live run уже выдал валидные сравнимые пары |
| Deterministic promotion inputs | Required acceptance/regression/seeded_faults/reviewer/dependency; conditional performance/cost; self-score diagnostic-only | B45 T29/A06; code_quality_metrics.py:7–80 | Независимость, blinding и происхождение переданного reviewer verdict; для этого остаётся T30 |
| Test-debt repair | Semantic corruption cases, 196→34 repeated families, 3 exceptions, LOC 8130→5658 | B45 T28/A06; исторический receipt 48 focused tests | Универсальное качество tests по LOC или доказательство лучше работающего агента |
| Self-learning | State/due check, ручной runner, redacted metrics/feedback, candidate proposals, export, loop diagnostics | B44 S0–S7; PAOS-R4; source modules | Автообучение, auto-apply, scheduler activation, statistically adequate promotion |
| User documentation/site | F01–F18, RU/EN, local strict build, routes/search/diagrams | 05.11 `site-docs-refresh-2026-11-05.json` | Исправление implementation gaps этого исследования или опубликованный сайт |

Исторические числа тестов в этой таблице взяты из указанных receipts, а не выданы за новый full test run.

## Подтверждённые расхождения и приоритет

### IMP-01 — P1: минимальный workflow отсутствует на стыке generator и runner

**Факт:** [renderer](../plugins/product-agent-os/scripts/product_agent_os/infrastructure.py) без profile filtering обходит [209 templates](../plugins/product-agent-os/scripts/product_agent_os/templates.py). [Runtime routes](../plugins/product-agent-os/scripts/codex_runtime_runner/routes.py) задают шесть required inputs и широкие проверки даже для maintenance. Это сильнее, чем совет новой документации «переиспользуйте минимально достаточные artifacts».

**Влияние:** небольшой bugfix или onboarding получает лишние файлы, роли и проверки; value откладывается до подготовки инфраструктуры. Это не нарушение target-write boundary: предложения всё ещё staged и approval-aware.

**Нужное изменение:** отдельно учитывать project profile и task scope/risk; выбирать artifacts и проверки по задаче, сохраняя full route для high-risk/financial/release. Реестр всех доступных templates оставить, но `required_templates` не должен означать «всё обязательно каждому». Owner: architect + plugin-runtime-builder; тесты: обычная правка, docs-only, зелёный проект без agents, high-risk change, existing user files.

### IMP-02 — P1: T25–T29 реализованы локально, но не собраны в основной процесс

**Факт:** активный [coding workflow](../.codex/workflows/coding-standards.md) всё ещё требует full checklist; [packaged workflow](../plugins/product-agent-os/assets/templates/workflows/coding-standards.md) уже ссылается на compact contract. Активного `code-change-contract.md` нет. AST inventory не нашёл production call sites selectors и deterministic promotion wrapper.

**Влияние:** утверждение «компактный процесс уже используется» превышает доказательство. Это integration gap, а не основание переписывать selectors или снова выполнять T25–T29.

**Нужное изменение:** adapter от реального discovery inventory и change risk к готовым selectors; их выход должен определять route packet и command evidence. Применение compact workflow к активному workspace — отдельная reviewable migration с сохранением локальных правил. В connected test должно быть видно, какой selector отработал и почему широкие fallback checks не скрыли новый маршрут. Для promotion wiring дождаться T30–T33.

### IMP-03 — P1: lifecycle state выводится из структуры документов, а не состояния задачи

**Факт:** [state.py](../plugins/product-agent-os/scripts/codex_runtime_runner/state.py) ищет точные English headings и builder.toml. В текущем repo inference дал team_ready; in-memory RU пример — infrastructure_planned / needs_context. [cli.py](../plugins/product-agent-os/scripts/codex_runtime_runner/cli.py) блокирует отсутствующий control-plane context после uninitialized.

**Влияние:** русский проект, single-agent задача или уже реализованный workspace могут получить подготовительный маршрут повторно. Явный request lifecycle_state в низкоуровневой функции поддержан, но CLI собирает пустой state и не использует current task-group как authoritative selector.

**Нужное изменение:** разделить structural readiness workspace, фактическое состояние task и inferred recommendation; explicit task state должен иметь provenance, а не угадываться по словам. Поддержать reuse RU/EN документов без зависимости от буквального заголовка. Это часть IMP-01, не отдельный большой framework.

### IMP-04 — P1: MCP inventory и compatibility проверяют разные форматы

**Факт:** [compatibility.py:95–107](../plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py) принимает flat context7; [inventory.py:123–142](../plugins/product-agent-os/scripts/product_agent_os/batch39_inventory.py) читает mcpServers. На одном реальном package функции вернули compatible и пустой server inventory.

**Влияние:** оператор видит взаимоисключающие сведения; новый portable mcp.json будет также пропущен legacy-only paths. Данный результат не устанавливает, какой формат реально загрузит конкретный host: live MCP в этом исследовании не запускался.

**Нужное изменение:** общий parser/resolver с явно названным format/version и normalized component inventory; malformed, unsupported, absent, present_unverified и host_verified должны различаться. Дать fixtures для текущего legacy package и официального portable schema; не просто переименовывать `.mcp.json`.

### IMP-05 — P1 для claim integrity / P2 для distribution: package metadata отстаёт от guides

**Факт:** [manifest](../plugins/product-agent-os/.codex-plugin/plugin.json) описывает продукт как Production-ready, содержит example.invalid repository/privacy/terms, а [compatibility result](../plugins/product-agent-os/scripts/product_agent_os/codex_compatibility.py) объединяет App/CLI/IDE как supported surfaces. [Официальный plugin guide](https://learn.chatgpt.com/docs/plugins) исключает native plugins в IDE; standalone skills/repo workflows — отдельная возможность.

**Нужное изменение:** capability matrix по компоненту и execution/orchestration surface; honest maturity metadata. Placeholder URLs допустимы для локального prototype, но не дают distribution readiness. Portable root manifest — поддерживаемое направление следующего package revision, **не срочная поломка legacy**: [официальная документация](https://developers.openai.com/plugins/build/plugins) сохраняет compatibility fallback. Desktop-only prerequisites проверять только при конкретной задаче distribution, без публикации сейчас.

### IMP-06 — P1: source/package/cache/exposure не образуют проверяемую цепочку

**Факт:** 11/12 installed SKILL.md содержательно отличаются от canonical; все 12 explicit-only. Содержательное отличие docs-maintainer меняет разрешённый способ работы. В текущем каталоге сессии видимы четыре plugin-prefixed Product-Agent OS skills; это наблюдение доступного каталога, не исчерпывающий host registry и не доказательство отсутствия остальных.

**Нужное изменение:** выполнить существующие B42 M02/M04–M08: source/package/cache digest, effective selection path, metadata policy, fresh-chat exposure/invocation results. Обновление cache — отдельное разрешённое действие, не побочный эффект audit. Не включать implicit invocation у всех skills: safe read-only discovery и write/release/automation routes требуют разных правил.

### IMP-07 — P2: current pointers и labels всё ещё могут отправить в старую задачу

**Факт:** [PLAN.md:70](../PLAN.md) содержит старый Stop contract; [RUNLOG.md:97,124](../RUNLOG.md) — Start T28 и generic hook activation pending. В то же время верхние записи и source-owned receipts уже подтверждают T28/T29 и bounded ACT repair. Архивная маркировка текущих source plans добавляет неоднозначность. Это включает остаток последнего documentation refresh: сайт обновлён, но не весь operating backlog семантически reconciled.

**Нужное изменение:** один current next-action pointer на task-group; старые строки явно superseded, а не параллельная current state. Исторические receipts не переписывать. Validity check должен ловить конфликт active queue с новым receipt и различать history от незавершённого backlog. Owner: docs-maintainer/lifecycle-orchestrator.

### IMP-08 — P2: source-policy heuristic не покрывает актуальную official source map

**Факт:** [source_policy.py:14–17,146](../plugins/product-agent-os/scripts/product_agent_os/source_policy.py) не распознаёт learn.chatgpt.com/platform.openai.com без других английских hints, но принимает одно слово Sources:. Это не semantic verification и не должен быть такой claim.

**Нужное изменение:** распознавание канонических official URLs с проверкой hostname, одинаковое RU/EN поведение, отдельные поля source presence / supported claim / freshness. Для источника нужны claim scope, checked date и surface; заголовок Sources не равен подтверждению. Не строить новый crawler или autonomous updater ради этой локальной проверки.

### IMP-09 — P2 usability/contract: read-only analysis с явно разрешённым report artifact

**Факт:** текущий hook правильно отказал записи после terminal marker. В [pre_tool_use_policy.py:211–224](../.codex/hooks/pre_tool_use_policy.py) work_type research/review/planning запрещает любую mutation, даже если пользователь отдельно попросил MD output. Для текущего отчёта владелец отдельно разрешил marker; write scope ограничен только authoring отчёта.

**Нужное изменение:** в будущем явно моделировать read-only target inspection + bounded output artifact, переход к новой задаче и её authority. Нельзя решать это отключением guard, расширением whitelist всех report-like paths, обходом shell или изменением hook trust без согласования. Это новый UX/contract случай, не повторное открытие ACT-F1. Для исправления нужны positive allowed-output и negative outside-output cases плюс свежий host probe после изменения определения.

### IMP-10 — незакрытая запланированная работа: независимая оценка качества

**Факт:** T30–T34 planned; proposed files отсутствуют. Старый T21 не дал валидных pairs; T22 сохранил no-go. Метрики T29 принимают typed evidence, но сами не удостоверяют независимость reviewer или происхождение check results.

**Нужное изменение:** продолжить существующий DAG: T30 blinded reviewer и T31 frozen multi-stack corpus → T32 isolated baseline/treatment → T33 local preflight → T34 только с новым exact approval. Корпус должен включать случаи reuse/config/no new code, ordinary fixes, legacy, boundary/security и performance applicability. Новый model/effort нельзя менять одновременно с оцениваемым process intervention.

### IMP-11 — evidence gap: user outcomes, learning и target pilot

**Факт:** B44 — один manual pilot, B39 — conditional owner-feedback, B41 — generated-artifact proof. Документационная сборка не закрывает target apply, graph runtime или устойчивую полезность для пользователей.

**Следующий результат:** провести bounded owner review существующих S7/B39 packets; выбрать представительные обычные задачи и измерить время до полезного результата, ненужные вопросы/артефакты, повторные проверки, correctness и требуемый owner intervention. Эти данные могут питать уже имеющийся manual learning loop. Native memories или Scheduled tasks не заменяют такую оценку.

## Что новая документация НЕ требует автоматически внедрять

1. **Agents API/Agents SDK/Responses orchestration.** Local contract-mode helper намеренно dependency-free; добавлять hosted runtime следует только под конкретный пользовательский сценарий и отдельную архитектуру. Это не обязательная миграция Product-Agent OS.
2. **Собственное управление native memory.** Не читать/переписывать generated memory store как замену project evidence; достаточно объяснить и диагностировать scope. Project cache, native memory и API prompt cache — разные механизмы.
3. **Автоматическую настройку Cloud и secrets.** Сначала честно описать unsupported/unknown capability. Наличие guide не делает local shell hooks пригодными для cloud orchestration.
4. **Активные schedules / auto-apply.** Сохранить manual_only/candidate_only. B44-S8 требует owner decision и достаточного denominator; native scheduling availability не является approval.
5. **Безусловную многоагентность или обязательный Manager.** Сохранить ownership и независимость review, но выбирать fan-out по задаче.
6. **Новую смену model pins.** GPT-6.1 конфигурация уже существует. Следующий этап — сопоставимые quality/cost/latency measurements при согласованном scope, а не очередное редактирование TOML.
7. **Повторную реализацию ACT-F1..F6.** Уточнить текущие pointers и расширять coverage только для новых требований; старый successful bounded receipt не превращать в универсальную гарантию.

## Связь с F01–F18 обновлённой документации

| Finding docs-аудита | Требует ли Product-Agent OS изменения? | Решение по текущим файлам |
| --- | --- | --- |
| F01 — stale site | Нет нового runtime кода | Закрыто local docs/site slice; не смешивать с release/pilot |
| F02 — portable plugin contract | Да, bounded compatibility/packaging work | IMP-04/05; legacy сохраняется, dual-format resolver раньше migration |
| F03 — lifecycle contradictions | В основном уже реализовано; есть residual routing/UX | ACT repair сохраняется; IMP-07/09, не новый полный lifecycle rewrite |
| F04 — surfaces/cloud boundaries | Да, для capability reporting | Component-level matrix вместо общего supported_surfaces; Cloud executor не добавлять по умолчанию |
| F05 — Scheduled tasks | Не требует activation | Candidate validator/manual workflow уже есть; следующий шаг owner evidence, а не scheduler |
| F06 — trust/tool coverage | Часть реализована, coverage ограничена | 12/12 ACT hashes совпадают; нужны адресные cases после будущих изменений, не объявление универсальной защиты |
| F07 — simplify/multi-agent | Да, наиболее существенный integration gap | IMP-01/02/03: scoped renderer, task routing, active compact workflow |
| F08 — skill exposure | Да, существующий Batch 42 | IMP-06; canonical/cache/exposure/invocation должны измеряться отдельно |
| F09 — memory | Документация + диагностика, не новый store | Не смешивать native memory с self-learning candidates; optional future capability report |
| F10 — current Cloud setup | Не требует переносить local runtime | Capability limitation и отдельный design только по целевому сценарию |
| F11 — runtime ownership/failure paths | Не требует Agents API/SDK rewrite | Сохранить contract-mode boundary; app-runtime integration — отдельный продуктовый запрос |
| F12 — models/cache | Config уже обновлён; behavior evidence ещё нет | Закончить planned comparison route; cache tuning только measured/applicable |
| F13 — RU/EN | Да, также structural parser/locale compatibility | IMP-03 и единый source schema; перевод не должен менять runtime identifiers |
| F14 — Mermaid/anchor | Нет plugin runtime изменения | Закрыто docs render correction; существующие checks могут стать повторяемым локальным gate |
| F15 — history overload | Да для status/projection correctness | IMP-07: current route и archive не должны конфликтовать; historical evidence сохранять |
| F16 — docs maintenance validation | Возможная небольшая tooling-задача | Аудит link/route/diagram выполнен; повторяемый repository gate можно оформить без scheduler. Не смешивать с source-policy semantic claim |
| F17 — IDE plugin support | Да, compatibility result | IMP-05: native plugin installation отдельно от repo/skill capabilities |
| F18 — onboarding | Текст обновлён; поведение требует IMP-01/06 | Проверить реальный small-task first result и exposure, а не только homepage |

## Рекомендуемый следующий порядок

Ниже предложения, а не изменение текущих PLAN/task statuses и не разрешение на выполнение. Existing IDs сохраняются; новые названия — bounded slices для согласования.

| Порядок | Работа и владелец | Основные файлы / зависимость | Приёмка и граница |
| --- | --- | --- | --- |
| 0 | Reconcile current state и maturity metadata; docs-maintainer + lifecycle-orchestrator | PLAN/RUNLOG/current-state, manifest, current task-group pointer | Один next action=T30 для B45; legacy Stop строки superseded; отсутствует неподтверждённый Production-ready. Historical receipts сохранены |
| 1 | Один сквозной ordinary task route; architect + plugin-runtime-builder | templates/infrastructure, state/routes/cli, active/staged coding workflow; reuse T25–T27 | Ordinary/docs-only/single-agent cases не требуют полного template pack, builder.toml и всех suite layers. High-risk cases сохраняют gates. Проверка source→selector→route→result подтверждает новый путь |
| 2 | Compatibility и component inventory; plugin-runtime-builder + tester | codex_compatibility, batch39_inventory, discovery/hygiene paths | Один normalized результат legacy/portable; корректные IDE/component boundaries; malformed/unsupported не превращается в compatible. Без MCP startup/install |
| 3 | B42 M02/M04–M08: source/cache/exposure; lifecycle-orchestrator + tester | Canonical skills, metadata validator, package/cache inventory; свежая session только в отдельном approval scope | Доказано, какая версия и skill доступны и вызываются. Safe implicit class отдельно от explicit-only actions; rollback cache update определён. Никаких global policy изменений по умолчанию |
| 4 | B45-CQRR-T30 и T31 | reviewer contract/rubric и frozen multi-stack corpus; T29 уже удовлетворён локально | Blinding без arm labels/self-scores; critical findings блокируют; 12–16 sanitized/synthetic tasks, ≥4 stack families и ≥5 risk classes; no-new-code cases включены |
| 5 | B45-CQRR-T32 → T33 | Exact baseline/treatment prompts, design и local readiness packet | Одна intervention, одинаковые model/effort/tools/timeouts; hashes frozen до treatment inspection; schema, corruption, reviewer, corpus и reproducibility checks проходят локально |
| 6 | B45-CQRR-T34 только после нового exact approval | Approval packet → comparable run → independent reviewer → decision | Новый бюджет/call cap/retention; старый consumed T20 approval не переиспользовать; invalid pair/critical finding оставляет no-go. Live run не обязателен до local readiness |
| 7 | B39 owner-feedback и B44-S8 decision | Существующие manual pilot/feedback packets; улучшенный ordinary route | Реальные outcomes, confusion, unwanted questions/artifacts/check repeats; owner review. Не считать один manual pilot достаточным denominator для автоматизации |

Порядок 1–3 можно готовить как независимые design slices, но нельзя одновременно менять protocol, model, prompts, cache и reviewer в одном quality experiment. Если владелец выбирает строго продолжить утверждённый B45 DAG, **следующая существующая задача — T30**, без повторения T28/T29. Если приоритет — ощутимое упрощение продукта, сначала следует согласовать bounded ordinary-route integration из пункта 1; этот пробел не закрыт одним T30.

### Минимальные acceptance scenarios для следующей реализации

1. **Обычная правка:** существующий проект, одна функция и один regression seam; нет нового набора из 209 artifacts, автоматической команды или полного общего gate без причины.
2. **Docs-only / research + report:** target read-only, разрешён один output artifact; остальные paths запрещены, marker относится к текущей задаче.
3. **Высокий риск:** authorization/security/data-loss change сохраняет полный необходимый scope, негативные проверки и owner gates; simplified route не используется как обход.
4. **RU/EN existing project:** одинаковая задача и evidence дают одинаковый route независимо от языка headings; отсутствие custom builder не запрещает single-agent работу.
5. **Existing user files:** generator предлагает companions/managed sections без перезаписи user content; повторный plan стабилен; apply требует актуального plan-bound approval.
6. **Package formats:** текущий legacy пакет и portable fixture имеют одинаковый component inventory; incompatible forms дают needs_review с причиной.
7. **Skills:** canonical и installed digest расходятся — система сообщает это, не заявляет activation. Новый chat подтверждает exposure и отдельный invocation result.
8. **Promotion:** self-score alone, missing check evidence, label leakage, invalid output и critical reviewer finding не дают promotion; correct no-op/reuse solution не штрафуется как отсутствие ценности.

### Что не нужно делать первым

- Новый большой plan/framework с параллельной нумерацией существующих T30–T34.
- Массовую миграцию всех portable/plugin/cloud форматов, одновременно меняя local runtime.
- Пересобирать всю систему заново из-за unchecked boxes в старых recipes.
- Добавлять ещё больше templates и mandatory review loops до исправления selection/integration.
- Автоматически обновлять installed cache, включать implicit invocation всем skills или активировать schedules.
- Запускать дорогой model comparison, пока нет T30–T33 и разрешённого бюджета.

## Просмотренные планы и выполненные задачи

| Артефакт | Как использован в исследовании |
| --- | --- |
| [Track 1 plugin core](../docs/superpowers/plans/2026-05-14-product-agent-os-plugin-core.md) | Scope/структура/исторические task recipes; сопоставлено с manifest/discovery/validators/merge/fixture tooling |
| [Track 2 lifecycle skills](../docs/superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md) | Scope 12 skills/shared references, package metadata и current/cache comparison |
| [Track 3 infrastructure](../docs/superpowers/plans/2026-05-14-product-agent-os-generated-infrastructure.md) | Staged-first architecture и profile обещания против текущего registry/renderer |
| [Track 4 hardening](../docs/superpowers/plans/2026-05-14-product-agent-os-production-hardening.md) | Approval/merge/rollback и automation/source-policy boundaries |
| [Track 5 runtime runner](../docs/superpowers/plans/2026-05-15-product-agent-os-codex-runtime-runner.md) | Contract helper scope; context/state/routes/guards; отсутствие обязательной SDK migration |
| [Track 9 methodology](../docs/superpowers/plans/2026-05-25-track-9-methodology-intelligence.md) и [backlog](../docs/sources/product-agent-os-track-9-backlog.md) | Структурная inventory, domain queue и synthesis/runtime boundaries; не повторный аудит всех методологических тезисов |
| [Track 10](../docs/superpowers/plans/2026-05-27-track-10-guided-questions-status-dashboard.md), [Track 8 history](../docs/sources/product-agent-os-track-8-detailed-backlog.md), [Track 10 history](../docs/sources/product-agent-os-track-10-backlog.md) | Реализованные usage-mode/first-run/question/status families и отдельные Batch 39/41/42 gates |
| [Track 11](../docs/superpowers/plans/2026-06-20-track-11-documentation-architecture-refresh.md) | Маршрутизация B44/B45 и docs/site evidence ownership |
| [GPT56 remediation](../docs/superpowers/plans/2026-08-05-gpt56-r1-r6-remediation.md) | Исторический этап; не переносился поверх более свежего 03.11 alignment |
| [S9 team readiness](../docs/superpowers/plans/2026-08-10-batch45-s9-0-team-readiness.md) | Историческое разделение ownership; team readiness не равно execution |
| [S9-A](../docs/superpowers/plans/2026-08-10-batch45-s9-a-durable-contract-recovery.md) | T23/T24 local schema и normalization completion |
| [S9-B](../docs/superpowers/plans/2026-08-11-batch45-s9-b-compact-authoring-runtime.md) | T25–T27 completion, exact changed file classes и integration ceiling |
| [S9-C](../docs/superpowers/plans/2026-08-14-batch45-s9-c-test-metric-repair.md), [loop remediation](../docs/superpowers/plans/2026-08-17-product-agent-os-loop-remediation.md) | Старый незавершённый attempt против последующей A06/R2–R4 repair; T28/T29 фактически локально завершены |
| [03.11 refresh/alignment/lifecycle](../docs/superpowers/plans/2026-11-03-gpt6-documentation-refresh.md) и [task-group](../docs/superpowers/specs/gpt6-documentation-refresh-task-group.json) | 20 docs tasks, technical followup, failed activation и последующий ACT repair; newer scoped receipt имеет приоритет |
| [B45 recovery task-group](../docs/superpowers/specs/batch45-code-quality-runtime-recovery-task-group.json) | Текущий источник статусов T23–T34, dependencies, acceptance и proposed files |
| [T21 run](../docs/superpowers/specs/batch45-postq4-t21-promotion-grade-eval-results.json), [T22 decision](../docs/superpowers/specs/batch45-postq4-t22-promotion-grade-decision-packet.json) | Фактический no-go, consumed approval и отсутствие valid pairs/reviewer result |
| [B42 matrix](../docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json) | Существующий backlog для exposure/implicit policy; не выдан за выполненный |
| [B44 S7](../docs/superpowers/specs/batch44-self-learning-loop-approved-manual-pilot-summary.json), [B39 S5](../docs/superpowers/specs/batch39-s5-go-no-go-decision-packet.json) | Manual evidence, owner/pilot/release gates; obsolete local docs blocker отделён от остальных |
| [05.11 docs refresh](../docs/superpowers/specs/site-docs-refresh-2026-11-05.json) | Исходная F01–F18 карта и доказательство, что docs/site изменения не меняли реализацию |

Все **15 RU/original plan files** инвентаризированы по структуре/status/checkbox markers; для текущих B45 и 03.11 задач прочитаны detailed acceptance/completion и machine receipts. Это не построчный повторный аудит всех строк исторических планов и не новая аттестация каждого старого test result.

## Текущие проверки и источники доказательств

| Проверка в этой задаче | Наблюдаемый результат | Ограничение |
| --- | --- | --- |
| `python -B plugins/product-agent-os/scripts/validate_agents.py .codex/agents` | exit 0; 15 profiles, no config/file errors | Static schema/configuration, не effective host behavior |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks` | exit 0; 7 files | Static contract, не все hook execution paths |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py plugins/product-agent-os/assets/templates/hooks` | exit 0; 7 files | Staged templates не активированы |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | exit 0; compatible | Известные validator blind spots раскрыты в IMP-04/05 |
| In-memory `validate_codex_compatibility` + `_package_inventory` | Context7 ok и пустой server list | Реальный MCP не запускался |
| In-memory `plan_route('maintenance', allow_subagents=False)` | 6 files, full unittest + fixture eval, checklist/doubt packet | Pure recommendation result, без исполнения рекомендованных команд |
| `required_templates()` | 209 entries; 8 agents; profile-independent tuple | Renderer stage/apply не запускался |
| `infer_lifecycle_state` | Current repo team_ready; synthetic RU infrastructure_planned | Проверена эвристика, не реальный task success |
| Static AST call-site scan | Selectors/wrapper не имеют прямых production callers | Dynamic/manual use не исключается |
| Source-hint cases | learn/platform false; developers true; plain Sources: true | Marker heuristic, не semantic truth judge |
| Skill text comparison | 11/12 различаются после BOM/newline normalization | Не доказывает effective source конкретной другой сессии |
| ACT repair source hashes | 12/12 совпали | Историческое runtime evidence сохраняет исходную узкую область |
| Actual PreToolUse response при первой записи отчёта | Deny terminal marker; после согласованного нового marker запись разрешена | Это текущий наблюдаемый переход, не самостоятельная полная hook qualification |

Pure probes выполнены через `python -B -` со stdin-кодом и stdout JSON. Пример воспроизведения центрального расхождения без записи:

```python
from pathlib import Path
from product_agent_os.codex_compatibility import validate_codex_compatibility
from product_agent_os.batch39_inventory import _package_inventory

workspace = Path.cwd()
plugin = workspace / "plugins/product-agent-os"
print(validate_codex_compatibility(plugin)["checks"]["context7_mcp"])
print(_package_inventory(workspace, plugin)["mcp_server_keys"])
```

Для запуска нужен module search path `plugins/product-agent-os/scripts`; probes задавали его в памяти. Новые tests/fixtures/scripts не создавались, полный unittest/eval suite не запускался: задача — анализ неизменяемой реализации. Исторические 1253/1247/208/100-test receipts рассматриваются только в своих исходных scopes.

### Официальные источники, повторно полученные 05.11.2026

- [Package your plugin](https://developers.openai.com/plugins/build/plugins): portable layout и поддерживаемый legacy fallback; простое переименование MCP файла недостаточно.
- [Plugins](https://learn.chatgpt.com/docs/plugins): component/surface/auth limits, отсутствие native plugins в IDE, новый chat/session после установки.
- [Build skills](https://learn.chatgpt.com/docs/build-skills): discovery и initial exposure отличаются от invocation; explicit/implicit policy; full skill body загружается при выборе.
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): inheritance permissions/provider/MCP/skills; role profile не создаёт отдельную authority.
- [Hooks](https://learn.chatgpt.com/docs/hooks): exact-definition trust, supported denial semantics и cloud/local boundaries; ошибки MCP callbacks не равны гарантированному denial.
- [Desktop-only plugins](https://developers.openai.com/plugins/deploy/desktop-only): отдельные local-execution/distribution prerequisites; не разрешение на публикацию.

Источники получены через OpenAI Developers connector, а не по search snippets. Product architecture priorities и предложенные slices — вывод исследования, не инструкция OpenAI и не новое разрешение владельца.

## Control-plane handoff, ограничения и сохранность

- PLAN/RUNLOG/current-state требуют будущей согласованной правки по IMP-07: **handoff_required**, потому что текущая задача запрещает менять существующие документы. REQUIREMENTS может потребовать уточнения ordinary-route acceptance в следующем implementation slice; EVALS — только при утверждённом изменении rubric. Исторический prod_test не меняется.
- Не менялись runtime, model pins, permissions, hooks/trust, installed cache, Git history, site или зависимости. Режим manual_only/candidate_only сохранён.
- Контекст review: **self_review**. Независимые subagents не запускались. Новые provider/model/browser/target calls не выполнялись.
- До анализа сохранён aggregate SHA-256 по 2403 существующим tracked/untracked non-ignored файлам, исключая только разрешённые report и marker: `c4abfed31472ea10855050324371d7199099d4f07adb10e192d45ea5a83433b9`. Финальное сравнение совпало: 2403/2403 файлов в контрольном наборе побайтно неизменны. Это не checksum всего диска или ignored caches.
- Статическая проверка отчёта: 41 локальная Markdown-ссылка существует; replacement characters нет; code fences сбалансированы; `git -c core.safecrlf=false diff --check` — exit 0. Никакие проверки не объявлены подтверждением production acceptance.
- Report completeness означает завершённое исследование этих contract seams. Оно не снимает product no-go и не утверждает, что все остальные части реализации бездефектны.

### Решение, которое стоит принять следующим

Рекомендуется согласовать **один bounded implementation slice для ordinary route**, переиспользующий T25–T27 и не затрагивающий models, provider calls, installed cache или hooks/trust. Параллельная продуктовая очередь не должна дублировать B45: после устранения integration blockers продолжить существующие T30 и T31 → T32 → T33, а T34 оставить отдельным exact-approval gate. T30 и T31 независимы друг от друга после своих уже выполненных prerequisites. Если владелец предпочитает сначала закрывать формально утверждённый B45 DAG, начать с T30; это улучшит достоверность quality evaluation, но само по себе не устранит тяжёлый onboarding/generator route.
