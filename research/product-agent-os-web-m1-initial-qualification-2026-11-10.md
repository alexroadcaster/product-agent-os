# Web M1 — первичная проверка PAOS-0001 и PAOS-0054

Source status: historical local implementation evidence, 2026-11-10, Europe/Moscow. Research receipt вне публикуемой базы знаний. Прежняя Windows execution qualification была blocked в AppContainer; [нативная проверка 2026-11-11](product-agent-os-web-m1-execution-2026-11-11.md#разрешение-paos-0054) подтвердила MXC write/deny. Исторические отказы и команды ниже сохранены; они не являются текущим статусом M1.

## PAOS-0001 — обнаружение источников

`bindProject` закрепляет canonical root и identity каталога за project ID. `inspectProjectSources` принимает binding от локального сервиса и возвращает только coverage фиксированных имён control-plane. Подменённый каталог и чужой project ID отклоняются. Ссылки и hard links исключаются. Наличие файла означает обнаружение metadata, парсинг содержимого остаётся за его адаптером.

| Сценарий и проверка | Результат |
| --- | --- |
| `node --test tests/web/project-sources.test.mts` RED | Exit 1, отсутствовала ожидаемая запись `AGENTS.md` со статусом `available` |
| Та же команда после реализации и добавления проверки подмены каталога | Exit 0, 2/2. Доступный и отсутствующий файлы различаются, junction в соседний проект исключается, чужой ID и замена каталога отклоняются |
| Прямой вызов `bindProject` / `inspectProjectSources` на текущем рабочем каталоге | Exit 0, 6 известных файлов обнаружены, `runtimeHistory` имеет `unavailable / runtime_not_connected`. Результат содержит относительные имена |

Схема установленного CLI содержит `thread/list` с `cwd`, `cursor`, `archived`, а также `thread/read`. Полнота выдачи и project binding host-сессий требуют изолированного runtime-прогона. Каталоги агентов и скиллов, граф, write routes и UI остаются отдельными поверхностями приёмки. Владелец evidence — PAOS-0001.

## PAOS-0054 — параметры среды и офлайн-проверки

| Компонент | Наблюдённое значение |
| --- | --- |
| Windows | `10.0.26200`, `win32/x64` |
| Codex CLI | `0.167.0`, native binary SHA-256 `edfdd48f8b458af0906e507b4cb05217b326c3d6e515e9f024e05e3b8d650f70` |
| Node.js | `v26.5.0`, SHA-256 `119d6fa70e6ae1b15b90688ab6bcc8e3a2819acea021af196895cab1843645af` |
| Python | `3.13.5`, SHA-256 `5341746f92483a93e44c313de830f2fba2956f0759094404a16b2fed06c9a2ed` |
| Chrome / Edge, metadata бинарников | `157.0.8103.38` / `157.0.4341.46` |
| Схемы App Server SHA-256 | Envelope `486c7c8daa5dc7f3ab2a1fb56de5316804caf7a4210fda1dc28d3f0f4e90cfe1`, v2 `b1e5d17224b9d9732b5976012438ba78e2cf7e418b67f8f8a5f5cffe301b875d` |
| SQLite | `3.53.3`, compile option `ENABLE_FTS5`, запрос `MATCH` вернул одну строку для `проект` |

| Команда | Наблюдение |
| --- | --- |
| `codex app-server generate-json-schema --experimental --out .codex-tmp/paos-m1-schema` | Exit 0. Два bundles сгенерированы локально. CLI предупредил об отказе доступа к временному каталогу alias в пользовательском профиле |
| `node --test tests/web/runtime-compatibility.test.mts` RED | Exit 1 на отсутствующем отчёте о `ServerRequest:item/tool/call` |
| `node --test tests/web/*.test.mts` | Exit 0, 3/3. Упоминание `dynamicTools` в тексте или `item/tool/call` в неверном направлении не проходит проверку |
| `node packages/contracts/runtime/probe-local.mts .codex-tmp/paos-m1-schema` | Exit 0, `static_checks_passed`, `schema.missing=[]`, `fts5Match=true`. Probe печатает полный список SQLite compile options |

Сгенерированные схемы перенесены в игнорируемый `.tmp/paos-m1/schema`. Повтор `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema` завершился с exit 0, с теми же digest и результатами. Для нового прогона использовать `codex app-server generate-json-schema --experimental --out .tmp/paos-m1/schema`.

Способ генерации схемы сверён с [OpenAI Docs — Codex App Server](https://learn.chatgpt.com/docs/app-server#message-schema). Опция хранения `ephemeral` сверена с [OpenAI Docs — Credential storage](https://learn.chatgpt.com/docs/auth#credential-storage). Точный build и поведение процесса квалифицируются отдельно.

## Один изолированный запуск App Server

Выполнен один явно разрешённый запуск закреплённого `codex app-server --listen stdio://` через `python -B .tmp/paos-m1/stdio-qualification.py --binary <pinned-codex.exe> --run-once`. Хеш бинарника совпал. Системный Windows TEMP отказал в записи на предварительной проверке, до запуска процесса. Повтор preflight и единственный запуск использовали временный профиль в `.tmp/paos-m1/`. Изолированный профиль отключал поиск родительских project settings, `config/read` подтвердил 0 project layers. Провайдером был синтетический профиль с адресом loopback, RPC ограничены перечисленными сценариями, turn не запускался. Процесс завершился сам с exit 0, stderr пуст, временный профиль удалён. [OpenAI Docs — project root detection](https://learn.chatgpt.com/docs/config-file/config-advanced#project-root-detection)

| Проверка | Наблюдение |
| --- | --- |
| `initialize` / `initialized` | Процесс сообщил Windows и точный временный `codexHome` |
| `config/read`, `account/read` с `refreshToken: false` | Подтверждены временный user layer, `ephemeral`, пустой account и отсутствие `auth.json`. Вход и изоляция после входа остаются открытыми |
| `experimentalFeature/list`, `thread/start` и `thread/inject_items` | Список features вернул первую страницу в 100 записей. Две сессии с верными `cwd` стартовали в `paginated`; обе команды инъекции получили ответ без ошибки. `dynamicTools` принят при старте Alpha, вызов инструмента не проверялся |
| `thread/read` | Чтение по известному ID Beta вернуло эту сессию. Этот RPC не получает project binding, поэтому доступ по ID требует отдельной проверки владения в PAOS |
| `thread/list` | Фильтры `cwd` для Alpha, Beta и пустого каталога вернули `0/0/0`. Контроль без `cwd`, но с тем же `sourceKinds: [appServer]`, тоже вернул 0. Положительная выборка отсутствует. Некорректный `archived` отклонён с `-32600` |
| Эффективная политика Alpha | `readOnly`, `networkAccess: false`, approval `never` |
| Эффективная политика Beta | На запрошенные `workspace-write` и `on-request` сервер ответил `readOnly` и `on-request`, writable roots отсутствовали |

Санитизированное наблюдение находится в `.tmp/paos-m1/stdio-qualification-result.json`, SHA-256 `3f25b572a94b314d5dd7e8b942dec07e0f527df58e1703141b46f462bb34db0f`. Ключи, содержимое истории и абсолютные пути в receipt не сохранены.

### Расхождения, блокирующие зависимые задачи

1. **PAOS-0001, полнота истории.** Нулевая выборка всех контролей совместима с различиями source classification или с отсутствием индексированной истории. Причина не установлена. Для следующего разрешённого прогона нужно записать фактический `source`, наличие persisted path и сравнить поиск с наблюдённым source и без фильтра `cwd`, сохраняя два положительных контроля. До этого coverage runtime history остаётся `unavailable`. [OpenAI Docs — `thread/list` filters](https://learn.chatgpt.com/docs/app-server#list-threads-with-pagination--filters)
2. **PAOS-0054, Execution.** В этом временном профиле запрос не дал ожидаемой эффективной политики. Нужно установить, какой поддерживаемый Windows sandbox и permission profile применяются к дочернему процессу, и повторить проверку без изменения managed restrictions. Точный writable root и отсутствие сети должны подтверждаться ответом runtime и отрицательными сценариями. [OpenAI Docs — Windows sandbox diagnostics](https://learn.chatgpt.com/docs/windows/windows-sandbox#troubleshooting-and-faq)

`node --test tests/web/runtime-compatibility.test.mts` сначала обнаружил ложный пропуск двух сценариев (RED, exit 1). Добавлен разбор stdio receipt, который отдельно от наличия схемы проверяет положительные контроли истории и эффективную политику. `node --test tests/web/*.test.mts` — exit 0, 4/4. `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema .tmp/paos-m1/stdio-qualification-result.json` — ожидаемый exit 1, `stdio_checks_blocked` с `project_history` и `scoped_execution_policy`. Команда без stdio receipt сохраняет `static_checks_passed`, exit 0.

После обновления карточек и реестров раздельные `unittest` для docs, task-plan lifecycle и templates (209 тестов) и для hooks (42 теста) прошли с exit 0. `check_docs.py`, валидация Web-плана, валидация обоих hook paths и `git diff --check` — exit 0. Сверка транзитивных зависимостей подтвердила, что все 16 ещё не начатых задач M1 зависят от заблокированных карточек.

## Второй изолированный запуск App Server

`python -B .tmp/paos-m1/stdio-diagnostics.py --binary <pinned-codex.exe> --run-once` израсходовал одно дополнительное разрешение. Один процесс, exit 0, изолированный handshake, временный профиль удалён. Наблюдение без содержимого сессий сохранено в `.tmp/paos-m1/stdio-diagnostics-result.json`, SHA-256 `3846634cfd7b84f372a02e56a1302c9ed831c39a92cdc7a73c73e0eebdbc2516`.

- Два заранее сохранённых synthetic CLI rollout по формату тестов закреплённого релиза дали `thread/list` Alpha/Beta/Empty/All = `1/1/0/2`, с ожидаемыми ID и `cwd`. Те же количества вернул `useStateDbOnly: true`. `thread/read` подтвердил правильный `cwd`, существующий persisted file и preview. [Тестовый fixture Codex 0.167.0](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/app-server/tests/common/rollout.rs#L222)
- Свежие Alpha и Beta сообщили `source=vscode`. Файл отсутствовал при `thread/start` и появился после `thread/inject_items` и `thread/name/set`. Preview остался пустым; свежие ID отсутствовали в `thread/list` и с `vscode`, и со всеми проверенными sources. Для UI это частичное покрытие. Причина конкретного внутреннего фильтра по одному наблюдению не установлена.
- `windowsSandbox/readiness` вернул `notConfigured`. Запрос legacy `workspace-write` вновь вернул `readOnly`. Именованный профиль `paos_fixture_write` с одной синтетической runtime workspace root вернул `workspaceWrite`, `networkAccess=false`, `on-request` и оба tmp exclusions. Legacy `writableRoots` был пуст. Выбор профиля и фактическое Windows-ограничение файловых операций остаются разными проверками. [OpenAI Docs — named permission profiles](https://learn.chatgpt.com/docs/app-server#start-or-resume-a-thread)
- Адаптер PAOS-0001 отправляет `thread/list` с `cwd` реестра и перепроверяет каждую строку. Возвращается только количество видимых сессий и частичный coverage; абсолютные пути и payload не выходят из адаптера. `node --test tests/web/project-sources.test.mts` — RED exit 1 на неизменном `runtime_not_connected`, GREEN exit 0, 3/3.

Оценка обоих receipts выполнена `node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema <receipt>`. Первый остаётся `stdio_checks_blocked` с `project_history,scoped_execution_policy`. Второй возвращает `stdio_checks_blocked` только с `scoped_execution_policy`. Оба кода 1 ожидаемы. Regression test нового receipt сначала падал на лишнем `project_history`, затем прошёл. Наличие `workspaceWrite` в metadata именованного профиля нельзя использовать вместо `windowsSandbox/readiness=ready` и доказательства ограничения записи.

## Windows sandbox — проверка на текущем хосте

Проверка выполнена на Windows 11 25H2 `26200.9711` и закреплённом Codex CLI `0.167.0`. Номер сборки выше указанного минимума для MXC. Каждый запуск использовал отдельный временный профиль и синтетические соседние каталоги. До App Server та же команда записала в оба каталога, затем контрольные файлы были сброшены. Оба процесса App Server завершились с exit 0, временные профили удалены. Файлы учётных данных не создавались. System policy, браузер и вызовы провайдера в проверке не использовались. [OpenAI Docs — Windows sandbox, MXC compatibility](https://learn.chatgpt.com/docs/windows/windows-sandbox#mxc-compatibility)

| Backend | Статус и выбор | Наблюдение записи |
| --- | --- | --- |
| `mxc` | RPC вернул `ready`, startup log сообщил `Windows sandbox selection: mxc` и `MXC availability: false` | Именованный `workspaceWrite` совпал с синтетическим корнем, без сети и дополнительных writable roots. `command/exec` вернул `-32603` без exit code дочерней команды. Внутренняя запись отсутствует, внешний контрольный файл сохранился. Фактический отказ записи не наблюдался |
| `unelevated` | RPC вернул `ready`, startup log сообщил `Windows sandbox selection: unelevated` | Выполнены только `initialize`, `config/read`, `configRequirements/read`, `windowsSandbox/readiness`. Проверка записи не запускалась |

В закреплённом релизе проверка readiness возвращает `ready` при выборе MXC или restricted token без проверки запуска команды. При `unelevated` подготовка дочернего процесса может менять DACL системного устройства `\\.\NUL`, поэтому `command/exec` и setup этого режима исключены из проверки с границей временного профиля и каталогов. Причина `MXC availability: false` в текущем контексте отдельно не установлена. [Codex 0.167.0 — readiness](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/app-server/src/request_processors/windows_sandbox_processor.rs#L306), [подготовка команды](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/windows-sandbox-rs/src/spawn_prep.rs#L250), [DACL устройства NUL](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/windows-sandbox-rs/src/acl.rs#L1061)

Локальные команды `python -B .tmp/paos-m1/windows-boundary.py --binary <pinned-codex.exe> --mode mxc --run-once` и с `--mode unelevated` вернули exit 1, так как ни один из запусков не получил пару write/deny. Санитизированные receipts в `.tmp/paos-m1/`: `windows-mxc-boundary-result.json` SHA-256 `21b335eb2a8833d292de1fb49d261abb437da8d766332ae5d2f6269cd2ac29e1`, `windows-unelevated-boundary-result.json` SHA-256 `c9ee43be70a716dbce0b2028848eba2ccf1dad2bc93c96d90233aef7d1a345d0`.

`probe-local.mts` теперь принимает дополнительный boundary receipt с тем же SHA-256 бинарника. Для `scoped_execution_policy` требуются нативная доступность выбранного MXC, именованный профиль, успешная запись в корне и явный отказ вне корня при положительном контроле обоих путей. RED воспроизвёл ложный пропуск `ready` без receipt. GREEN проверил положительный синтетический receipt и отклонение несовпадающего SHA-256, невалидного контроля, недоступного MXC и отсутствия дочернего процесса. Воспроизведение обоих Windows receipts сохраняет `stdio_checks_blocked` с `scoped_execution_policy`. Повтор без receipts сохраняет `static_checks_passed`, exit 0. Это локальная проверка синтетической файловой границы. Network enforcement, dynamic tools, изоляция после входа и сквозная приёмка PAOS-0045 открыты.

Проверки текущего среза:

- `node --test tests/web/runtime-compatibility.test.mts` — RED exit 1, GREEN exit 0, 3/3. `node --test tests/web/*.test.mts` — с inherited TEMP/TMP 21/23, ошибки `EPERM` на `rename` и создании junction. Повтор с TEMP/TMP в игнорируемом workspace — 22/23, `rename` прошёл, создание junction в fixture `project-sources.test.mts` по-прежнему возвращает `EPERM` до вызова адаптера.
- `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_infrastructure_templates -q` — 209/209. `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks -q` — 42/42. `python -B tools/check_docs.py`, `python -B plugins/product-agent-os/scripts/validate_task_matrix.py research/product-agent-os-web-task-manager-plan-2026-11-09.md` и `git diff --check` — exit 0.
- Повторная сверка M1 по JSON — 3 `implemented`, 2 `in_progress`, 2 `blocked`, 11 `planned`, среди `planned` нет карточек со всеми закрытыми зависимостями. `PLAN.md`, `TEST.md`, `RUNLOG.md`, карточка PAOS-0054 и реестры RU/EN синхронизированы. Статусы и порядок в JSON, требования и eval gates не изменились.

## Независимые ветки после PAOS-0001

| Задача | Статус | Локальная проверка и граница |
| --- | --- | --- |
| PAOS-0002 | `implemented` | `node --test tests/web/task-profile.test.mts`, 3/3. Typed M1 exchange round-trip, stable ID/key, provenance и unknown actual time; import, SQL и UI принадлежат другим карточкам |
| PAOS-0003 | `implemented` | `node --test tests/web/task-time.test.mts`, 3/3. Idempotent scoped event projection, пауза/retry/crash, elapsed union и effort по исполнителям; durable writer/runtime отдельно |
| PAOS-0004 | `in_progress` | `node --test tests/web/theme-locale.test.mts`, 3/3. RU/EN, Light/Dark/System и preference store contract; фактическая интеграция хранилища и browser acceptance открыты |
| PAOS-0039 | `blocked` | `node --test tests/web/auth-route.test.mts`, 2/2. Local API BYOK preview и отсутствие скрытого fallback; коммерческий AUTH-G1 требует owner decision |
| PAOS-0040 | `in_progress` | `node --test tests/web/launcher.test.mts`, 6/6. Missing/incompatible runtime, health, reuse, timeout и recovery-before-stop через fake ports; native launcher/instance reservation и связанный service entrypoint ещё нужны |

Работа над моделью/временем, темами и launcher выполнялась параллельно с непересекающимся владением. Авторизацию и отчёт вёл корневой агент. `node --test tests/web/*.test.mts` на объединённом срезе — exit 0, 23/23. Ключи, провайдер, браузер и изменение системных настроек для этих веток не использовались.

Итоговые проверки среза: 209 unittest для docs, task-plan lifecycle и templates, 42 unittest для hooks, `check_docs.py`, валидация Web-плана, валидация hook paths и `git diff --check` прошли. Markdown и JSON совпадают по статусам всех 56 карточек, порядок зависимостей прежний. M1 содержит 3 `implemented`, 2 `in_progress`, 2 `blocked`, 11 `planned`; среди `planned` нет задач с закрытыми зависимостями. `PLAN.md`, `TEST.md`, `RUNLOG.md`, Web-план, JSON, auth notes и реестры RU/EN обновлены; критерии `REQUIREMENTS.md` и `EVALS.md` в этом срезе не менялись.

## Продолжение реализации PAOS-M1 — локальные контракты

Независимая проверка закреплённого Codex 0.167.0 установила, что нативная проба MXC загружает PSEC API, создаёт среду с запретом egress и формирует атрибуты запуска. Общий результат кэшируется в процессе. `availability: false` не показывает этап или HRESULT, а sandbox manager прекращает выполнение до старта дочерней команды. Read-only `TOKEN_QUERY` процесса текущего runner вернул `isAppContainer=true`, `hasRestrictions=true`, `elevated=false`, `inJob=true`. Вложенная изоляция остаётся гипотезой о причине сбоя. В этом срезе нового App Server или setup не запускали. [Проба PSEC](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/mxc-sandbox/src/availability.rs#L17-L50), [выбор sandbox](https://github.com/openai/codex/blob/rust-v0.167.0/codex-rs/sandboxing/src/manager.rs#L365-L372), [Microsoft Learn — поля Windows token](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ne-winnt-token_information_class), [OpenAI Docs — MXC compatibility](https://learn.chatgpt.com/docs/windows/windows-sandbox#mxc-compatibility)

| Карточка | Что добавлено и проверено | Открытая интеграция |
| --- | --- | --- |
| PAOS-0004 | Нативная форма восстанавливает RU/EN и Light/Dark/System из `UiPreferencesStore`, сохраняет настройки перед применением, оставляет черновик при ошибке и отслеживает смену системной темы. `node --test tests/web/theme-locale.test.mts` — 6/6 | S24, реальное хранилище и UX-AC-15 в браузере |
| PAOS-0040 | Атомарное резервирование и публикация endpoint. Второй процесс получает `startup_unresolved` до публикации, переиспользует endpoint после неё и может занять профиль после подтверждённого Quit. `node --test tests/web/launcher-instance.test.mts tests/web/launcher.test.mts` — 9/9 | Реальный service host, native shortcut, pairing PAOS-0041 и reconciliation оставшейся после сбоя записи в PAOS-0040/0044 |
| PAOS-0054 | Расширена проверка схемы App Server. Маппер разделяет принятие turn, состояние turn, исход item и закрытие запроса. Независимое review воспроизвело некорректные статусы item, пробельные ID и ошибочный переход к recovery на штатном progress. После исправлений `node --test tests/web/runtime-compatibility.test.mts tests/web/runtime-events.test.mts` — 9/9 | Runtime correlation по generation/thread/request и replay принадлежат PAOS-0042/0044. Native write/deny и полный runtime manifest ещё открыты |
| PAOS-0054 | Опциональная файловая SQLite-проба. `node --test tests/web/runtime-sqlite.test.mts` — 3/3. Зафиксированные строки сохранились при повторном открытии, rollback отбросил строку, `VACUUM INTO` сохранил снимок активного WAL до следующей записи, восстановленная БД прошла integrity/FK, orphan insert отклонён | Worker, crash recovery, миграции и backup продукта принадлежат PAOS-0048/0051 |

`node packages/contracts/runtime/probe-local.mts .tmp/paos-m1/schema --sqlite-fixture-root .tmp/paos-m1` вернул exit 0, `schema.missing=[]`, `static_checks_passed` и три `true` файловой SQLite-пробы. С каждым из прежних Windows receipts — ожидаемый exit 1 и единственный blocker `scoped_execution_policy`. Context7 использован для документации Codex и Node.js. Поведение и поля сверены с закреплённой схемой и первичными источниками. [OpenAI Docs — App Server turns](https://learn.chatgpt.com/docs/app-server#turns), [Node.js 26.5.0 — SQLite](https://nodejs.org/download/release/v26.5.0/docs/api/sqlite.html), [SQLite — VACUUM INTO](https://sqlite.org/lang_vacuum.html#vacuuminto)

В текущем runner с `TEMP`/`TMP` в workspace `node --test tests/web/*.test.mts` дал 37/38. Единственное падение `EPERM` при создании junction в неизменённом `tests/web/project-sources.test.mts` произошло до вызова адаптера. У агента junction прошёл в промежуточном прогоне с незафиксированным токеном. В повторе с токеном AppContainer и унаследованным TEMP тот же агент получил 1/3, два `EPERM` на создании junction и `rename` до вызова адаптера. Отдельного доступного native Windows-контекста эти проверки не подтвердили.

PAOS-0039 для M1 использует уже определённый `local_api_byok` preview. Критерий самой карточки требует решения владельца по exact route для AUTH-G1. Официальная документация App Server по-прежнему описывает ограничение commercial/hosted auth. Регистрация, коммерческий допуск и вызовы провайдера в этом срезе отсутствуют. [OpenAI Docs — Auth endpoints](https://learn.chatgpt.com/docs/app-server#auth-endpoints)

Итоговая верификация среза: 27/27 затронутых Web-тестов, 209/209 unittest для docs/lifecycle/templates и 42/42 для hooks. `python -B tools/check_docs.py`, Web `validate_task_matrix.py`, сверка 56 статусов Markdown/JSON и `git diff --check` прошли. В M1 3 `implemented`, 2 `in_progress`, 2 `blocked`, 11 `planned`. Среди `planned` нет карточек со всеми закрытыми зависимостями. `PLAN.md`, `TEST.md`, `RUNLOG.md`, карточки PAOS-0004/0040/0054 и реестры RU/EN синхронизированы. Для `REQUIREMENTS.md`, `EVALS.md` и `prod_test.md` изменение области, eval gate или historical ledger не потребовалось.

## Открытые проверки

- PAOS-0001 реализован в границах project adapter. PAOS-0054 сохраняет `blocked`. Текущий tuple остаётся candidate до подтверждения Windows sandbox, изоляции credentials после входа, package lock и adapter revision. Дополнительная квалификация должна соблюдать отдельные границы `TEST.md`.
- Browser и реальный provider относятся к последующей PAOS-0045. Scoped file-write enforcement, dynamic tool execution, migration/restore и workload в этом прогоне не проверялись.
- Связь с приёмкой: PRD §17 и архитектура §21 → scoped source coverage и fail-closed compatibility → команды выше → задачи-владельцы PAOS-0001/0054. Runtime, browser, migration/restore и workload gates остаются открытыми.

## Проверки репозитория

- Первый совмещённый unittest-прогон завершился с ошибками. Evidence Markdown внутри `docs/` изменил зафиксированный объём публикуемых страниц, поэтому receipt перенесён в `research/`. В двух совмещённых попытках Windows удерживал временный каталог lifecycle test (`WinError 32`). Раздельный повтор прошёл. `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs tests.product_agent_os.test_task_plan_lifecycle tests.product_agent_os.test_infrastructure_templates -q` — exit 0, 209 tests. `python -B -m unittest tests.product_agent_os.test_lifecycle_hooks -q` — exit 0, 42 tests.
- `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` — первый exit 1 на создании каталогов в sandbox TEMP, повтор exit 0 после установки `TEMP` и `TMP` процесса внутри workspace.
- `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` — exit 0, 26/26. `validate_codex_compatibility.py` — exit 0, `compatible` для локальной структуры существующего пакета.
- `python -B -m unittest discover -s tests -p 'test_*.py' -q` — exit 0, 1450 tests, 1 skip, 910.696 s. Прогон начался до финальной корректировки ссылок на evidence. Затронутые docs/lifecycle checks дополнительно прошли раздельными прогонами на итоговых ссылках.
- `python -B tools/check_docs.py`, `validate_task_matrix.py` для Web-плана, `validate_hooks.py` для `.codex/hooks.json` и `.codex/hooks`, `git diff --check` — exit 0. Сверка Markdown с JSON подтвердила 56 задач, 18 задач M1, 234 ч, совпадающие статусы и отсутствие нарушений порядка зависимостей.

Control-plane sync: обновлены `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `RUNLOG.md`, карточки 0001/0054, JSON и реестры RU/EN. `EVALS.md` и `prod_test.md` не требовали обновления. Rollback среза — убрать созданные модули и тесты и вернуть собственные правки планирования. Данные проекта и legacy authority сохранены.
