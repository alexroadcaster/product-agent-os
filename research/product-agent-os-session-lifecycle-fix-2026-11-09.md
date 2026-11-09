# Исправление изоляции lifecycle по чатам

## G6 handoff — 09.11.2026

G6 partially_verified: уточнённый HOST-пакет разрешён и применён — два cache-файла и 210 target files проверены readback. Свежая целевая сессия не запустилась: App API не задаёт произвольный cwd, elevated CLI остановлен auto-review, sandbox CLI не может открыть локальное состояние. Нужен штатный запуск пользователем существующего host-target в Codex App, без повторного разрешения. Пилоты not_run; acceptance null; T34 no-go.

Source status: `project-authored / implemented_locally_verified / current_host_partially_verified`.

Task: `PAOS-SESSION-LIFECYCLE-2026-11-09`. Дата: 2026-11-09. Пользователь явно поручил исправить блокировки PreToolUse при независимой работе чатов. Связанная исходная задача — сохранить M1 wireframes без Web-разработки.

## Причина и решение

Активные и packaged PreToolUse, SessionStart и Stop обращались к единственному `.codex/product-agent-os/lifecycle-state.json`. Статус другой задачи влиял на текущую. Это локальный механизм PAOS, а не обязательная блокировка Codex или Git.

Официальный [Hooks contract](https://learn.chatgpt.com/docs/hooks#common-input-fields), прочитан 2026-11-09: top-level `session_id` идентифицирует сессию; subagents используют parent session ID. Выбор marker должен происходить только по этому host envelope, никогда по вложенному tool_input. Наличие строки в пользовательском содержимом не создаёт authority.

Выбран путь `.codex/product-agent-os/lifecycle-state.<sha256(session_id)>.json`: фиксированный basename без traversal и отдельный файл на чат. Marker содержит исходный `session_id`; mismatch закрывает mutation route. Нет fallback на общий marker при наличии session_id. Для legacy callers без session_id сохраняется прежний путь; они не получают доказательства параллельной изоляции.

SessionStart сообщает выбранный путь; PreToolUse проверяет собственный marker; Stop остаётся advisory и использует тот же selector. Один root координирует subagents своего чата. Пересечения по рабочим файлам по-прежнему требуют ownership coordination: это не filesystem lock manager.

Bootstrap ограничивается точной записью своего marker; mere mention, соседний marker и mixed patch не предоставляют exemption. Сохраняются sandbox, native approvals, destructive/path/secret checks, свежесть, terminal-state и full/concise reporting. Pinned-report route остаётся opt-in и привязывается к выбранному marker.

## План и границы

Bounded bugfix: отдельная task_matrix_plan_v1 не создаётся; эта запись и регрессионная таблица владеют acceptance/rollback. Full Task Start Brief показан из-за guardrail risk.

| Slice | Acceptance | Status |
| --- | --- | --- |
| S1 | RED: два независимых чата; invalid/foreign ID; exact marker bootstrap | observed_red |
| S2 | Selector и owner check во всех трёх hooks, active/package parity | implemented; static parity passed |
| S3 | Legacy/pinned-report compatibility, negative suite, docs/control-plane sync | passed locally; package compatibility gap remains |
| S4 | Сохранение и проверка подготовленных M1 wireframes | docs_static_verified; product/UI acceptance pending |

Scope: active/package hooks и lifecycle workflows/config, связанные tests и owning docs, compact control-plane pointers. No Web implementation, providers, Git publication, sandbox/trust changes. Existing audit report не редактировать. Rollback: вернуть только этот diff hooks/contracts/tests; сохранить session markers/evidence; старый shared workflow не считать безопасной параллельной fallback-схемой.

## Текущие проверки

RED 2026-11-09: четыре новых tests из `tests.product_agent_os.test_lifecycle_hooks.LifecycleHooksTest` — session_markers_isolate_parallel_chats_and_ignore_shared_terminal, session_identity_cannot_be_spoofed_from_tool_input_or_foreign_marker, session_start_and_stop_use_the_same_session_marker, marker_bootstrap_is_exact_and_session_bound. Запущены через `python -m unittest ... -v`: exit 1, 5 failures и 5 errors. Errors были попыткой разобрать пустой stdout после ошибочного allow; добавлен явный assertion, чтобы этот случай отображался как ожидаемый denial failure. Причины: общий marker вместо session marker; owner не проверяется; свой marker bootstrap блокируется; mention в другом patch ошибочно освобождает от проверки.

Отдельный дополнительный safety-test с инертными command strings не был сохранён: текущий PreToolUse сканирует также содержимое patch и отверг его как команду. Этот дублирующий тест убран из draft; существующие safety regression tests остаются обязательными. Guard не отключался и strings не маскировались. Ограничение классификации данных patch отдельно от исполняемой команды этим concurrency slice не объявляется устранённым.

GREEN: `python -m unittest tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_infrastructure_templates tests.product_agent_os.test_product_agent_os_docs -v` — 236 tests, 12.864s, exit 0. Затем добавлены две дополнительные проверки в существующие tests: чужой/mixed marker patch при активном своём marker и session-bound pinned report. Финальный `python -m unittest tests.product_agent_os.test_lifecycle_hooks -v` — 35 tests, 8.113s, exit 0; те же tests входят в запущенный полный набор.

Промежуточные failures/retests: первый интеграционный запуск выявил несовпадение ожидаемой строки workflow и ложное обнаружение `{64}` как template substitution; формулировка и regex исправлены. Следующий запуск с workspace-local TEMP выявил пять ошибок fixture isolation: git discovery находил родительский репозиторий. Test helper теперь явно передаёт synthetic workspace root. Это исправление тестовой среды, не отключение product guard. Полный набор использует `.docs-tools/reports/session-lifecycle-tmp` как TEMP/TMP; системный TEMP первоначально отклонял запись synthetic AGENTS.md.

Текущие дополнительные checks: оба `validate_hooks.py` для `.codex/hooks.json` и `.codex/hooks` — `ok: true`; `python tools/check_docs.py` — exit 0; `git diff --check` — exit 0. AST comparison с HEAD подтвердил неизменность пяти существующих списков destructive/path/secret/mutation/read-only patterns. Три active/package hook pairs совпадают побайтно; оба TOML parse; UTF-8, парность fences, W01–W10/J01–J05/UX-01–12 и три local links wireframes проверены Python — exit 0.

`python plugins/product-agent-os/scripts/validate_codex_compatibility.py` — exit 1, `needs_review`: `context7_mcp` имеет `legacy_flat_observed`. Это известный до slice package gap, подтверждённый текущим запуском. Проверка выполнена, но не пройдена; compatibility/readiness пакета не объявляется.

## Наблюдение в текущем Codex

После переключения на собственный session marker сохранение wireframes/ссылок прошло при terminal legacy marker. Отдельный синтетический Add File patch к marker с чужим hash был отклонён действующим PreToolUse с причиной `lifecycle writes must target only this session's marker`; файл отсутствовал до и после пробы. Определения hooks.json, trust и sandbox не менялись. Это положительная/отрицательная проверка текущего host route, а не просто импорт Python-функции.

После compaction в этом же чате поступил startup context с правильным session marker и `Scope=own_session`. Это наблюдение resume текущего чата; два новых одновременно работающих host chats и fresh installation не проверялись. Synthetic two-chat tests доказывают локальный contract, но не подменяют этот gap.

## Ограничения и дальнейшая эксплуатация

Общий marker возник в локальной реализации PAOS как единственная запись текущей задачи. Он не является блокировкой Git. Для session-aware host calls очередь между независимыми чатами больше не нужна; согласовывать нужно реальные пересечения файлов, например одновременные правки RUNLOG. Существующий shared marker сохранён как terminal migration snapshot; чужой audit report не редактировался. Legacy callers без session_id сохраняют старую схему без обещания concurrency isolation.

Guard распознаёт ограниченный набор command/patch shapes и не является универсальным shell parser или filesystem authorization. Наличие marker не доказывает пользовательское разрешение, а hash не является секретом. Историческое смешение анализа patch content и executable commands остаётся отдельной задачей; этот slice не обещает устранить все возможные false positives. Native sandbox/approvals остаются независимыми.

`python plugins/product-agent-os/scripts/run_fixture_eval.py` — exit 0, все 91 records имеют `ok: true`. `python plugins/product-agent-os/scripts/run_transcript_eval.py` — exit 0, 26 passed, 0 failed. Synthetic evals не используют live model/provider и не являются usability test Web.

Дополнительный review нашёл Windows case-insensitive variant чужого marker: регрессионный `test_marker_bootstrap_is_exact_and_session_bound` сначала дал exit 1 (`only this session` отсутствовало), затем filename recognition получил `re.IGNORECASE` в обоих mirrors. Финальный затронутый набор по команде GREEN выше: 236 tests, 14.455s, exit 0. Оба hook validators и AST/parity rerun — pass. Full discovery уже выполнялся во время этой коррекции; последний новый Windows assertion отдельно покрыт финальным focused run, а не приписывается ранее импортированной версии полного discovery. Fixture/transcript receipts относятся к состоянию до этой последней локальной коррекции; её контракт проверен focused suite.

Integrated `python -m unittest discover -s tests -v` — exit 0, 1288 tests in 479.665s, `OK (skipped=1)`; пропуск — non-Windows guard на Windows. Финальный focused run отдельно покрывает последнюю Windows assertion, как указано выше. `python tools/check_docs.py` и `git diff --check` повторены после evidence edits — exit 0. Strict MkDocs not_applicable: navigation, Mermaid, extensions/config и site evidence не менялись.

Логи текущего запуска находятся в `.docs-tools/reports/session-lifecycle-{focused,final-focused,hooks-final,full-tests,fixtures,transcripts,compatibility}.log`; это локальные диагностические outputs, не source of truth вместо этой записи.

## Финальный review и control-plane sync

`context_mode=self_review`, `tester_verdict=closed_allowed` для bounded repair и сохранения wireframes; это не independent review и не закрытие parent GAP-03/GAP-05. Проверены изоляция двух synthetic sessions, missing/terminal/foreign marker, host-only identity, own bootstrap versus foreign/mixed/mention, Windows case handling, legacy и pinned-report route, three-hook parity, неизменность safety patterns и definitions, M1 read-only scope. Открытые gaps названы выше; production/whole-package readiness не заявляется.

Изменённые implementation artifacts: `.codex/hooks/{pre_tool_use_policy,session_start_context,stop_runlog_reminder}.py` и соответствующие три packaged templates; `.codex/config.toml` и packaged config; active/packaged `task-plan-lifecycle.md`; root/staged AGENTS pointers; `tests/product_agent_os/test_lifecycle_hooks.py`. Старый marker сохранён как migration snapshot; текущая задача закрывается только в своём session marker. Связанные RU/EN runtime docs и registries синхронизированы.

Control-plane sync: REQUIREMENTS/PLAN/TEST/EVALS/RUNLOG — updated по scope, последовательности, verification route, claim ceiling и handoff. `prod_test.md` — not_applicable, historical Batch 39 evidence не менялся. Overflow/refactor — not_applicable, каждый root control-plane файл меньше 50 KiB. Handoffs required — none для локального slice; fresh-host multi-chat evidence и M1 product acceptance остаются отдельными этапами. Чужой full-audit report сохранён без правок.

Closure: `closure_level = implemented_locally_verified`; current-host PreToolUse positive/negative route наблюдался, полная fresh-host multi-chat activation не доказана. M1 wireframes: `draft_for_review / docs_static_verified`, разработка Web не начата. Допустимый итог: исправлена локальная причина общей lifecycle-очереди для session-aware calls; все возможные PreToolUse false positives не объявляются устранёнными.

После финальных control-plane edits: `python -m unittest tests.product_agent_os.test_product_agent_os_docs -q` — 100 tests, 2.997s, exit 0; `python tools/check_docs.py` и `git diff --check` — exit 0; финальный wireframes text check — 30 fence delimiters, четыре local links, UTF-8 без replacement characters, pass.
