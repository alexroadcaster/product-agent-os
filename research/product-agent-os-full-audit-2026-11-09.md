# Product-Agent OS — сквозной аудит реализации и актуальности

Дата: 09.11.2026. Статус: `audit_complete_with_findings`; реализация не изменена.

Task ID: `PAOS-FULL-AUDIT-2026-11-09`.

Source status: текущие исходники, планы и локальные проверки репозитория; официальная документация OpenAI, полученная 09.11.2026. Исторические receipts не считаются новым запуском.

## Главный результат

Product-Agent OS существенно обновлён под текущий Codex/GPT-6, но полную согласованность документации, generated target package и host behavior заявлять пока нельзя. Найдено **18 observations: 5 P1 и 13 P2**. P1 здесь означает исправить до соответствующей активации/распространения, а не доказанный production incident.

- **Сначала correctness boundaries:** обычный hook classifier и marker exemption (F06), Windows ACL repair (F07), невалидный root `.rules` (F11), неправильный generated hook path (F12), flat MCP declaration (F01).
- **Затем evidence/UX:** freshness parser (F03), empty-feedback signal (F08), offline install (F13), capability matrix (F02), README/site drift (F14/F17).
- **Упростить без переписывания:** opt-in ordinary intake, длинные повторяющиеся skills, historical/current projections (F05/F09/F10/F15/F16/F18).
- **GPT-6:** configuration/source alignment подтверждён; quality/cost/latency promotion не подтверждён (F04). T23–T29 сохраняются; T30–T34 закрывают другую, ещё открытую задачу доказательства качества.

В этом запуске 327 unittest cases: 326 прошли, 1 skipped; fixture 91/91, synthetic transcript 26/26. Compatibility exit 1 и execpolicy parse exit 1 — реальные незакрытые findings. Green tests не означают отсутствие пробелов в покрытии.

## Область и метод

Проверка охватывает реализованные модули, CLI, skills, active/staged agents, lifecycle/hooks, templates, evals/tests, планы, документацию RU/EN и Web-предложения. Код и существующая документация не изменяются. Единственные записи: этот отчёт и необходимый lifecycle marker. Без provider/model calls, host/trust/cache mutation, Git actions, server/browser, сборки или публикации site.

Различаем: подтверждённое исходниками; проверенное локально; историческое evidence; предложение; отсутствие host/model/product evidence. Каждый существенный finding должен иметь источник, последствие и минимальное рекомендуемое действие. Сам размер модуля или число артефактов не доказывают оверинжиниринг.

## Журнал наблюдений

### Проход 1 — состояние и источники

- Рабочее дерево при начале проверки чистое (`git status --short` без вывода). Это отличается от состояния предыдущей сессии; старые dirty-work предположения не перенесены.
- В `.codex/config.toml` уже указаны `gpt-6.1-sol` и политика Sol/Terra; migration status — `config_pinned_behavioral_promotion_pending`. Конфигурация не выдаёт локальный pin за доказанную эффективность моделей.
- Последняя завершённая запись marker относится к Web-документам, а не только GAP-03: Web PRD/architecture также входят в аудит как предложения.
- Официальные Models и Model selection подтверждают существование семейства GPT-6, GPT-6.1 Sol/Terra и различие model selection / reasoning effort / client availability. GPT-6.1 Terra требует Codex CLI 0.159.0+. Это требование будет сопоставлено с локальными проверками совместимости.

## Официальные источники

| ID | Источник | Использование |
| --- | --- | --- |
| S01 | [Models](https://learn.chatgpt.com/docs/models) | Модели, retirement, client prerequisites, Max/Ultra |
| S02 | [Model selection](https://learn.chatgpt.com/docs/model-selection) | Сравнение на одинаковых задачах и reasoning effort |
| S03 | [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model) | API migration, tools, instruction sensitivity, новые возможности |
| S04 | [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Effort, endpoints, context и граница API/client |
| S05 | [GPT-6.1 Terra](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | Effort, endpoints, context |
| S06 | [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Manifest precedence, MCP wrapper, portable/compatibility formats |
| S07 | [Plugins](https://learn.chatgpt.com/docs/plugins) | Supported surfaces, IDE exclusion |
| S08 | [Build skills](https://learn.chatgpt.com/docs/build-skills) | Metadata, invocation policy, progressive disclosure |
| S09 | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Defaults, inherited capabilities/permissions и custom profiles |
| S10 | [Hooks](https://learn.chatgpt.com/docs/hooks) | Discovery, trust, tool coverage, limitations |
| S11 | [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules) | Discovery path, prefix matching, inline test examples |
| S12 | [Permissions](https://learn.chatgpt.com/docs/permissions) | Protected paths, profiles, policy/runtime boundaries |
| S13 | [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Config keys, model effort, skills/context budgets |
| S14 | [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Discovery chain и byte limit |
| S15 | [Codex App Server](https://learn.chatgpt.com/docs/app-server) | stdio, schema generation, handshake, experimental WebSocket, unsafe raw method surfaces |
| S16 | [Prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) | Cache prefix, TTL, model-specific differences |
| S17 | [Responses Multi-agent](https://developers.openai.com/api/docs/guides/responses-multi-agent) | Отдельная beta и model availability |

Все 17 страниц получены через OpenAI Developers MCP в текущем запуске; search snippets использовались для навигации, выводы проверены по fetched pages. Recommendations и P1/P2 priorities — инженерная оценка автора, не утверждение OpenAI о качестве этого проекта.

### Проход 2 — package, модели, runtime и source policy

- Базовый commit: `bbf518363eaae3d73184742950bf233a6e51708e`. 2412 tracked files: 665 plugin, 614 docs, 660 site, 256 tests, 92 `.codex`, 80 research; остальные — tooling/config/control plane.
- Python inventory: 142 файла scripts, из них 91 core module и 10 файлов `codex_runtime_runner`. AST parse выполнен для всех 142. Это структурная проверка всего Python-пакета, не построчное доказательство корректности.
- 15 active agent profiles и 8 staged profiles используют Sol/Terra; старых model pins в этих профилях не найдено. 12 source skills валидны по локальному metadata validator; 11/12 отличаются от установленного cache. Cache не обновлялся.
- Registry содержит 209 templates. В task-scoped route применяется `selected_templates`; legacy path без task context по-прежнему берёт весь registry. Сокращение ordinary route действительно реализовано, но не стало общим default.
- `codex_runtime_runner/cli.py:22,104` запускает только deterministic `--contract`. Название runner нельзя трактовать как собственный исполняющий агент или live model transport. Graph provider modules также прямо запрещают live calls и строят contracts/gates; отсутствие Responses SDK в этих модулях само по себе не дефект миграции.

## Покрытие, findings и рекомендации

### F01 — P1 перед распространением: собственная MCP-конфигурация не проходит новый контракт

Факт: `plugins/product-agent-os/.mcp.json:1` содержит плоский `context7`; `plugin_components.py:67–76` маркирует это как `legacy_flat_mcp_requires_schema_review`. Текущий вызов `validate_codex_compatibility(Path(...))` вернул `needs_review`. Официальный [Package your plugin](https://developers.openai.com/plugins/build/plugins) описывает `mcpServers` wrapper; portable `mcp.json` имеет отдельную schema.

Минимум: исправить именно MCP declaration и проверить выбранный host. Legacy `.codex-plugin/plugin.json` остаётся поддерживаемым; wholesale migration не обязательна. Portable root manifest нужен при реальном требовании переносимости. Перед distribution заменить `example.invalid` и misleading publisher identity/official-site ссылки на настоящие данные владельца; это не blocker локального аудита.

### F02 — P2: capability matrix не различает запрещённую и ещё не проверенную поверхность

`codex_compatibility.py:64` создаёт одинаковый `native_plugin=requires_surface_specific_host_receipt` для App/CLI/IDE. [Plugins](https://learn.chatgpt.com/docs/plugins) прямо исключает IDE extension из plugin surfaces; standalone skills там поддерживаются. Нужны разные поля `supported/documented`, `not_supported`, `not_verified`: host probe не может сделать неподдерживаемую surface поддерживаемой. `compatibility_scope` уже корректно ограничен local structure — сохранить.

### F03 — P2: freshness parser не распознаёт даты собственной документации

Текущая `validate_source_policy('.')`: 310 Markdown files; freshness `missing` у всех 310; `needs_review`, 188 registry-review rows, 151 missing official-source hint; secret findings 0. Пример: `docs/codex/models-and-reasoning.md:5` содержит `Проверено 2026-11-03.`, а `source_policy.py:18` требует двоеточие после метки. Нужно согласовать форматы дат или принять существующие RU/EN формы. Эти результаты не означают, что все документы устарели.

Отдельно keyword scanner принимает упоминание Codex/MCP/model за behavioral claim и не разрешает source links через локальный registry; проектные diagram pages получают тот же review, что и неподтверждённые официальные claims. Нужна классификация project contract / official behavior / historical receipt и resolution registry refs. Сохранить `claim_supported=not_verified`: date/URL никогда не должны подтверждать смысл утверждения автоматически.

### F04 — P2: GPT-6 pin готов, behavioral promotion не выполнен

`.codex/config.toml` и active/staged agents согласованы с официальными Sol/Terra IDs; `validators.py:137` явно обозначает allowlist как repository policy. Это допустимое ограничение, а не отсутствие поддержки Astra/Luna у OpenAI. Нет основания автоматически повышать effort или переключать роли на Astra. Нужны version/capability receipt выбранного host и task-representative quality/cost/latency comparison на том же effort, затем отдельно на более низком. Official Terra CLI minimum 0.159.0 уже указан в RU/EN model guide, но package validator не проверяет клиент.

### F05 — P2: ordinary route остаётся opt-in, старый путь сохраняет тяжёлый default

`infrastructure.py:152–155` выбирает все 209 templates без `task_context`; `templates.py:1228–1251` умеет минимальный выбор; `state.py:57–93` legacy inference зависит от English headings и наличия builder. Это сохранённая совместимость ORD, а не новая поломка. Следующий шаг — один простой task-context intake и явное объяснение legacy fallback, затем отдельная migration default на основании regression evidence. Не удалять старый путь без оценки callers.

### Проход 3 — guardrails, learning и размер инструкций

Проверены active/staged instruction patterns, mutation classification, разрешения, merge/rollback, public runtime CLI, graph contracts, learning feedback и источник B45 statuses. Существующие 131 focused tests прошли (25.384 s; skipped=1). Они не обнаруживают нижеописанные edge cases; инертные pure-function probes воспроизвели их отдельно. Shell payloads не исполнялись, sentinel files не создавались.

### F06 — P1: обычный lifecycle hook имеет обходы классификации записи

Источники: `.codex/hooks/pre_tool_use_policy.py:67–72,146–159,424–431` и packaged mirror. `_is_read_only` смотрит только на начальный префикс; `_is_mutating` возвращает false до анализа остального текста. `_is_lifecycle_marker_write` ищет два фрагмента текста, не проверяя реальную область patch.

Инертные probes, текущий запуск:

| Case | observed | Ожидаемая консервативная классификация |
| --- | --- | --- |
| `Get-Content README.md` | read_only=true, mutating=false | Допустимо |
| Строка `Get-Content` с последующим `Set-Content` через `;` | read_only=true, mutating=false | Не считать чистым read |
| Строка Python `-c` с `Path(...).write_text(...)` | read_only=false, mutating=false | Unknown/potential mutation, требуется review |
| Add File в другой Markdown, в body только имя marker и `scope_note_shown` | marker_write=true | Не является записью marker |

Последствие: обычный guard может не проверить terminal/missing marker для некоторых shell writes или ошибочно дать marker exemption. Это локально воспроизведённый дефект parser/classifier; успешный обход sandbox/host **не проверялся и не утверждается**. Исторический ACT negative probe остаётся валидным для своей конкретной формы `apply_patch`, но не покрывает эти случаи. Новый pinned report mode строже, однако его наличие не исправляет default path.

Минимум: запретить prefix-based read fast path для составных/непонятных команд; marker exemption привязать к точному target, patch structure и разрешённому transition. Не строить универсальный PowerShell/JS interpreter в hook. Неизвестный action передавать в отдельную проверку, сохраняя независимые sandbox/approval controls. После focused regression — отдельный exact-hash trust и fresh-host positive/negative test. Официальный [Hooks](https://learn.chatgpt.com/docs/hooks) подтверждает зависимость от exact definition trust и ограничения hook coverage.

### F07 — P1 перед повторным использованием: Windows ACL helper слишком широко меняет deny ACE

`windows_codex_permissions.py:73–107`: `apply_permissions` объединяет все DENY SIDs родителя и child, выключает наследование и вызывает `/remove:d` для каждого. Нет фильтра принадлежности SID именно Codex, snapshot/restore исходных ACL или проверки reparse/symlink для каждого target. CLI `prepare_windows_codex_permissions.py:23–26` имеет только `--apply`, без plan-digest binding. Это статический finding; реальный ACL apply не запускался.

Документированная owner approval не заменяет точность операции: могут быть удалены намеренные запреты проекта/организации. Рекомендуется исключить helper из обычного onboarding, сначала использовать поддерживаемые permission profiles с точечными overrides; если OS repair действительно нужен — отдельный preview, точный SID/target allowlist, ACL backup, rollback и проверка resolved paths. Не менять текущие ACL в рамках аудита. [Permissions](https://learn.chatgpt.com/docs/permissions) различает policy profiles и ограничения исполнения; открытие `.codex/agents` также является изменением instruction surface, а не обычного отчёта.

### F08 — P2: пустой feedback создаёт положительно названный promotion signal

`self_learning_feedback.py:119–131`: `evaluate_satisfaction([])` возвращает `denominator=0`, `human_label_count=0`, `promotion_signal=owner_label_supported`. Это воспроизведено текущим pure-function вызовом. `summarize_owner_feedback_ledger:246–254` вкладывает такой результат в `no_owner_feedback_ledger`, поэтому противоречие реально доходит до public summary. Это не auto-promotion: кандидатный контур и guardrails сохраняются.

Нужно состояние `insufficient_evidence` при zero rows/zero owner labels, раздельная валидность/тональность feedback, regression для пустого и wholly rejected ledger. Не выводить удовлетворённость из отсутствия данных.

### F09 — P2: progressive disclosure декларируется, но большие skill bodies повторяют общие политики

12 SKILL.md имеют 6.6–41.5 KB каждый; `implementation-planner` — 41,505 bytes, `workspace-discovery-auditor` — 38,770, `risk-reviewer` — 34,031, orchestrator — 32,324. Один одинаковый metrics paragraph (639 символов) встречается во всех 12; workflow checklist (823 символа) — в 11; release checklist (627) — в 9. Это измеренное дублирование, а не предположение по числу файлов.

[Build skills](https://learn.chatgpt.com/docs/build-skills) использует progressive disclosure: после selection читается полный SKILL.md. `skills.max_context_tokens` ограничивает начальный список, а не тело выбранного skill. Поэтому простое повышение context window или начального бюджета не устраняет избыточную нагрузку.

Минимум: оставить в body trigger/authority/inputs/output/stop; domain-specific gates и полные списки вынести в уже существующие references, с условными ссылками. Сохранить отдельную authority для read-only ролей; не включать implicit invocation всех skills. Сначала сравнить task success/лишние вопросы/артефакты/latency на неизменных cases, только затем принимать сокращение. GPT-6 guide отдельно предупреждает о чувствительности к противоречащим инструкциям.

### F10 — P2: отдельные durable instructions всё ещё повторяют старую иерархию и абсолютные запреты

`tests/AGENTS.md:8–11` ставит checked-in docs в инструкционную иерархию и сравнивает их с global preferences; файл русскоязычный и дублирует старые общие operating instructions. Это расходится с нынешним root правилом: factual source authority не равна instruction authority. Его нужно заменить короткими test-specific правилами; discovery/activation проверить в соответствующем cwd.

В skill bodies встречаются `Ask for approval before any write`, `Do not use network access` и требования только current-run evidence. Для read-only assurance роли это может быть намеренной границей; нельзя автоматически удалить её. Но общий consumer должен явно различать default role scope и уже авторизованную задачу, а повторное использование неизменившегося evidence — от нового запуска. Общее правило priority определить один раз, убрать конфликтующие копии. Пример: `agent-team-designer/SKILL.md:14,27–31`, `completion-skeptic/SKILL.md:24–28`.

Проверка контргипотезы: root `AGENTS.md` 17,856 bytes + global 16,687 > default 32 KiB, **но на этом host явно задан `project_doc_max_bytes=65536`**. Поэтому текущая truncation не установлена; остаётся portability risk при переносе на default host. Не повышать лимит ещё раз без нужды.

### Проход 4 — прочие control surfaces, distribution и tools

Проверены `.rules`, active hooks и generated config, вспомогательные installer scripts, graph/learning entrypoints и Web architecture. На host `codex-cli 0.167.0`, Python 3.13.5. CLI version выше документированного Terra minimum, но не доказывает App build или account/model access. CLI сообщил о невозможности housekeeping в собственном temp; команды version/execpolicy исполнялись без model calls.

### F11 — P1 перед активацией: корневой `.rules` невалиден и находится вне стандартного discovery path

Текущий `codex execpolicy check --rules .rules -- rg --files` завершился **exit 1**: отрицательный пример `rg --replace value` совпадает с разрешающим prefix `["rg"]`. `not_match` — тест правила, а не исключение из allow. Документированный discovery — `rules/*.rules` рядом с active config layer, например `.codex/rules/default.rules`; обычный `<repo>/.rules` сам по себе не является таким файлом. Нестандартная загрузка в текущем host не доказана.

Следствие: файл выглядит как действующая policy, но штатный parser его отвергает; простое перемещение может создать слишком широкое разрешение вне sandbox. Нужны узкие patterns, корректные positive/negative examples и отдельная активация с проверкой effective policy. Не переносить/активировать автоматически. Источники: `.rules:5–11`, [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules).

### F12 — P1 для target onboarding: `enable_hooks` пишет mirror вместо discovered config

`templates.py:179` и `merge_infrastructure.py:26,504–527` направляют approval-bound hook creation в `.codex/hooks/hooks.json`. При этом generated `config/config.toml:141–142` объявляет `hook_policy=.codex/hooks.json`, а старый путь — mirror. В generated config нет inline `[hooks]` загрузки mirror. [Hooks](https://learn.chatgpt.com/docs/hooks) описывает `.codex/hooks.json` рядом с config, отдельно от plugin-root `hooks/hooks.json`.

Текущие merge tests проверяют появление файла в старом пути (`test_merge_infrastructure.py:436–454`), поэтому проходят при этом несовпадении. Active repository имеет правильный `.codex/hooks.json`; finding относится к **generated target route**, а не отсутствию active config здесь. Нужен отдельный явный install/activation plan для правильного пути, preserve-existing behavior, trust review и fresh host test. До этого `enable_hooks` не следует описывать как фактическое включение.

### F13 — P2: offline docs installation содержит безусловный online-capable шаг

`tools/docs_install.ps1:48` выполняет `pip install --upgrade pip` до ветки `OfflineWheelhouse`; только requirements install получает `--no-index --find-links`. Поэтому offline option не гарантирует отсутствие сетевого обращения. Installation не выполнялась. Исправление: убрать ненужный unconditional upgrade либо проводить его через тот же approved source/offline boundary; добавить stubbed command-contract check без настоящей установки.

### F14 — P2: package README не догнал обновлённые пользовательские руководства

`plugins/product-agent-os/README.md:291–305` всё ещё выдаёт flat Context7 example за соответствующий текущему примеру Codex; `341` говорит о manifest без чёткого portable/compatibility distinction; scripted first flow `479–488` не показывает `--task-context` и ведёт в полный template registry. В начале README находятся длинные Batch receipts, включая старые counts и состояния. Site guides уже объясняют GAP/ordinary и `needs_review`; package entrypoint не синхронизирован с ними.

Нужны короткий актуальный start path, две явные surface/component таблицы, explicit `$skill` entry при `allow_implicit_invocation=false`, link на ordinary route и ссылка на историю вместо её копирования. Старые receipts сохранить в owning evidence, не переписывать как текущие.

### F15 — P2: размер и разделение модулей требуют адресного упрощения

Наиболее большие core files: methodology audit 5944 строки, discovery 4132, first-run renderer 3469, metrics 2432, first-run analysis 2247. AST показывает крупные независимые domain checks, а `analyze_workspace` повторно запускает methodology inventory. Graph subsystem — 27 `project_graph_*` modules плюс code graph/cockpit; многие являются gate/packet builders, а не live providers.

Размер сам по себе не defect. Практические причины упростить: повторное сканирование workspace, дублирование boundary/status/approval схем и несколько HTML render paths; тяжёлый legacy default и путаница между packet-ready и runtime-ready. Измерить latency и объём обычного route, затем передавать единый immutable inventory snapshot и выделять только реально независимые domain detectors. Не заменять всё универсальным workflow engine, RAG store или новой БД.

У semantic слоя `_cross_encoder_score` (`project_graph_semantic.py:629–647`) — lexical heuristic, а vectors (`649–660`) — deterministic hash projection. Docs называют это local deterministic cache, поэтому это **не найденная ложь о live embeddings**. Но назвать backend/semantic/LLM gate «готовым AI-модулем» было бы неверно. Прежде нового provider integration нужен retrieval baseline против lexical search и пользовательская польза.

### F16 — P2: статусы распределены корректно по истории, но их слишком легко прочитать как текущие

B45 machine JSON подтверждает T23–T29 local completion, T30–T33 planned_not_started, T34 approval_required_not_started. В B42 одновременно существуют historical `status=planned` и newer `execution_evidence.status=implemented_locally_verified_explicit_only`. Это намеренное сохранение истории, однако generic status consumer должен иметь explicit precedence, иначе UI покажет неверную очередь.

PLAN/RUNLOG/TEST содержат несколько секций Current с разными датами; верхние записи GAP корректно ограничивают старые compatibility/runtime receipts. Нужен один current pointer с source revision и derived projection, а не новый независимый status registry. В Web architecture уже правильно предложены отдельные task/run/verification/acceptance состояния — сохранить это разделение.

### F17 — P2: checked-in site отстаёт от текущего source

В обоих source `docs/product-agent-os/control-plane-current-state{,.en}.md` присутствуют ORD-01, GAP-01, `94 focused`, `needs_review`; в соответствующих `site/{,en/}product-agent-os/control-plane-current-state.html` все четыре отсутствуют. Это прямое локальное сравнение конкретной пары страниц, не предположение по времени изменения файлов. Site не пересобирался в этом аудите. После будущего docs fix нужен согласованный rebuild, RU/EN links/anchors и diagram check; старый build receipt не подтверждает свежесть нового source.

RU/EN inventory: 310 pages, 150 EN siblings, 10 English-original plan pages без дублирующего sibling. Автоматическая проверка canonical model/route tokens дала только два кандидата для ручного review, не общий parity failure: current-state и historical Context7 research. 100 existing docs tests прошли. На sampled graph страницах остаётся тяжёлый смешанный RU/EN prose; исправлять пользовательские объяснения, сохраняя identifiers и historical evidence.

### F18 — P2, design gap: bounded report authority не покрывает последовательное ведение отчёта

GAP-05 разрешает только один literal Add File в новый Markdown; `_report_action_ok` отказывает для существующего output и Update File. Это соответствует сохранённому узкому plan, поэтому не regression. Но запрос «по мере анализа собирай наблюдения» требует нескольких записей в один отчёт. Сейчас для такого authoring приходится явно вести отдельный mutation scope, поскольку lifecycle schema допускает лишь implementation/fix и не имеет report-authoring type.

Не расширять pinned grant молча. В следующем scoped design решить: atomic final report из read-only исследования либо authoring scope на один exact path с expected previous digest, bounded lifetime и безопасным update. Отдельно проверить concurrent-root ownership marker: другой чат не должен перезаписывать активную задачу. В этом запуске соседний Web-чат сообщил, что ждёт terminal transition; его файлы не редактировались аудитом.

## Что уже соответствует текущей документации OpenAI

| Поверхность | Проверенный результат | Что не доказано |
| --- | --- | --- |
| Модели/effort | 15 active + 8 staged Sol/Terra profiles; прежние efforts сохранены; defaults Sol/medium | Quality/cost/latency superiority, account availability, effective App picker |
| Parent/subagent contract | Нет agent-local sandbox/provider/MCP override; permissions наследуются; read-only роль не объявлена отдельным sandbox | Независимая техническая изоляция reviewer |
| Skill metadata | 12/12 source files валидны; `policy.allow_implicit_invocation=false`; четыре прежние ошибки размещения исправлены | Cache sync, fresh exposure, actual invocation |
| Package precedence | Portable root identity, skills/MCP precedence, whole-object OpenAI overlay замещение реализованы | Полная JSON Schema validation, OAuth extensions, distribution acceptance |
| Ordinary route | Task-context adapter использует существующие T26/T27; проверки не исполняются из untrusted command text; receipt hash не превращается в proof | Default adoption, реальная польза на проектах, полный live route |
| API guide | Tools для 6.1 Sol/Terra через Responses; effort/parameters/context не смешиваются с UI/CLI | Собственный API adapter отсутствует и сейчас не нужен |
| Max/Ultra | Guides различают single-agent Max и product-level subagent Ultra; API enum не расширен до Ultra | Доступность для конкретного аккаунта/host |
| Memory/caching | Memory не source of truth; docs различают cache TTL и storage retention | Измеренный cache hit/cost в Product-Agent OS |
| Hooks | Active repo config в правильном path; Stop advisory; exact trust и historical receipts названы | F06 classifier completeness; новые source hashes и target activation |
| Learning/automation | Candidate-only, manual-only, no auto-apply; redacted feedback/metrics и repair proposal | Learning outcome, достаточный denominator, autonomous promotion |
| Web proposal | App Server stdio, version/schema binding, allowlist, source/DB authority split, run ≠ acceptance | Реализованного Web продукта/UX/runtime adapter ещё нет |

Текущие official API model pages для Sol/Terra подтверждают 1,050,000 context / 922,000 input / 128,000 output; Codex/Work default Sol — 500,000. Это не повод увеличивать prompt или переносить API quotas в Codex. Публичные models docs подтверждают Terra CLI minimum 0.159.0; наблюдаемый CLI 0.167.0 проходит только этот version prerequisite. Не считаем sunset GPT-5.5 в sign-in Codex отменой API availability.

Новые API-возможности GPT-6 (async tools, steering, configuration updates, cache control, Responses Multi-agent) не требуют внедрения в deterministic Python core. В guides эти различия уже отражены. Responses Multi-agent остаётся отдельной beta (текущий источник: GPT-6.1 Sol и GPT-5.6), а не повод объявлять все GPT-6 роли взаимозаменяемыми.

## Покрытие проекта и предел глубины

Аудит прошёл через все верхнеуровневые tracked surfaces, полный Python inventory и все 310 docs по структуре/source markers/canonical token parity. У всех 302 tracked Python files проверен AST. 1608 tracked text files в выбранных текстовых расширениях прочитаны на UTF-8 и replacement characters: ошибок не обнаружено. Vendor/minified binaries не разбирались как вручную написанный код; их наличие не является проверкой supply-chain security. Игнорируемые временные reports, caches и чужие raw sessions не использовались как authority.

Глубокое чтение направлено на public entrypoints, authority/side-effect boundaries, shared selectors, current status ownership и сомнительные места; это **не построчное доказательство каждой функции**. Таблица покрывает все 91 core modules по ownership-группам; отдельные historical evidence builders проверены структурно и через fixtures, без повторения старых реальных экспериментов.

| Группа | Core modules | Что проверено | Вывод |
| --- | ---: | --- | --- |
| Discovery / methodology / intake | 8 | discovery, first-run analysis, methodology audit/catalog/report/synthesis, question ledger/protocol | Routing/conditional gates есть; тяжёлые повторные inventories и keyword heuristics требуют измерения/упрощения |
| Ordinary / code quality | 5 | code quality metrics/selector, comment sufficiency, task routing, test strategy | T26/T27 reused; ORD path подключён; не переделывать T23–T29 |
| Staging / merge / permissions | 6 | infrastructure, merge infrastructure/Markdown, manifest, templates, Windows permissions | User-file preservation и approval-bound merge полезны; F07/F12 требуют исправления до onboarding claims |
| Validation / contracts / evidence | 12 | init, behavioral evals, compatibility, handoff contracts, doubt verification, component resolver, real target evidence, source policy, hygiene, task plan, transcript evals, validators | Структурные и содержательные claims разделены; F01–03 и freshness/shape limitations |
| Metrics / views | 7 | agent metrics/report, analysis renderer, offline export/safety, status dashboard/snapshot | Generated views явно ограничены; нет основания заменять их live telemetry или product proof |
| Learning / automation | 9 | automation policy и 8 self-learning modules | Manual/candidate boundary соответствует продукту; F08 и недостаток real feedback |
| Graph / cockpit | 29 | code graph/cockpit + 27 graph modules: adapters, analysis, backend, canonical mutation, chunking, embedding, extension closure, hybrid, index, live audit/governance/runtime, LLM extraction/proposal, manifest, observations, ontology, queries, real testing, renderer, reranker, review ledger, runtime QA, sanitization, search quality, semantic, visual model | Полезный offline baseline и много proposal/gate слоёв; live claims только по конкретным receipts; не наращивать provider complexity до пилота |
| B39 evidence | 14 | command results, failure taxonomy, inventory, plugin pilot, run manifest, redaction, rollup, hardening/remaining gates/closure, scorecard, session visibility, target fixture pack/mutation | Historical evidence machinery; source-owned status не равен release-ready |
| B41 evidence | 1 | batch41 closure | Evidence aggregation; product/owner acceptance отдельно |

Прочие поверхности:

- 41 Python entrypoints: сверены flags, side effects и contract-only/default/stage distinctions; не запускались apply/disable/provider/server modes.
- 10 runner files: CLI/context/state/routes/contracts/guards/redaction/promotion/model-output/init; reviewed control flow и focused tests.
- 12 skills, shared references, 15 active agents, 8 staged agents, config, 6 active hook scripts и mirrors: проверены model policy, authority, duplication и activation boundaries.
- 209 registered templates: selection/default, schema/managed sections и conditional evidence; чтение не означает необходимость генерировать все.
- 96 unittest modules: inventory, representative suites и aggregate fixture/transcript path; полный unittest discovery не повторялся, поскольку реализация не менялась.
- Root control plane, detailed plans/backlogs, B39/B42/B44/B45 receipts, ORD/GAP plan: status reconciliation, без повторного открытия исторически завершённых задач.
- Docs группы: agent-systems, artifact-templates, codex, diagrams, insights, methodologies, playbooks, product-agent-os, product-agent, prompting, runtime, sources, superpowers; links/structure gate и смысловая сверка актуальных OpenAI-facing contracts. Исторические research/fixture model IDs не считались current defaults.
- Site/MkDocs/JS/Node/Python docs tooling: source/build drift, local dependency boundaries, offline installer issue; без нового build, browser render, dependency install или vulnerability crawl.
- Web PRD и architecture: draft-only, current App Server сопоставлен; wireframes соседнего чата ещё не входили в стартовый snapshot.

## Что упростить, сохранить и добавить

| Решение | Конкретное действие | Почему |
| --- | --- | --- |
| Сохранить | T23–T29, ordinary selectors, plan-bound merge, conservative readiness, exact host/source receipts | Это реализованная основа, которую новое семейство моделей не делает ненужной |
| Сократить | Дублированные общие инструкции в 12 skills, историю в README/Current sections, безусловный полный template route для обычных задач | Измеренная нагрузка/неясность; переносить в existing references/evidence, не терять историю |
| Убрать из normal onboarding | Broad ACL repair, invalid root `.rules`, предположение что `enable_hooks` уже означает activation | Лишние риски и фактические несовпадения host contract |
| Не добавлять сейчас | Новый hosted orchestrator, собственную universal agent framework, default embeddings/vector DB, auto-learning, mandatory multi-agent team | Пока не закрыты конкретные defects и product/behavioral evidence |
| Добавить узко | Один read-only compatibility/doctor report: package schema, host version/surface, effective skill provenance, trust status как unknown/observed, owner policy | Нужен наблюдаемый контракт вместо уверенности по наличию файла; расширить существующий compatibility модуль |
| Добавить узко | Zero/unknown/stale/conflicting evidence cases, compound shell/marker exemption regressions, source-date formats, offline install stub | Обнаружены реальные пробелы, а не тесты ради количества |
| Добавить по очереди | Независимый reviewer, frozen held-out corpus, изолированный treatment, local preflight | Уже предусмотрено T30–T33; не создавать параллельный backlog |
| Добавить после разрешения | Один ordinary task pilot + owner feedback, source/cache/host exposure receipt, bounded hook probe | Закрывает разные gaps; не объединять их в один success label |

## Рекомендуемый порядок следующей реализации

Это рекомендация, не новая утверждённая очередь и не разрешение на изменения.

1. **Guard/installation correctness:** F06, F07, F11, F12. Каждый surface исправлять отдельно; локальные regressions сначала. Activation/trust/ACL changes не входят автоматически в code fix.
2. **Package and evidence truth:** F01–03, F08, F13–14. Acceptance: выбранный supported package format проходит local compatibility; IDE native plugin явно unsupported; даты RU/EN читаются; empty feedback не positive; offline branch не формирует network-capable pip command.
3. **Ordinary usability + concise instructions:** F05, F09–10, F16, F18. Acceptance: small task без лишней regeneration и repeated approval, exact scope preserved, high-risk escalation не потеряна, no hidden fallback. Заморозить итоговый baseline до T32.
4. **Продолжить B45 существующими IDs:** T30 зависит от T29; T31 — от T27/T29 и может готовиться независимо; T32 — от T25/T30/T31; T33 — от T24/T28/T29/T30/T31/T32. T34 — только после T33 и отдельного exact approval. Не менять prompt/model/effort/route одновременно внутри сравнения.
5. **Fresh-host и польза:** GAP-03 M06, GAP-05 trust/probe, GAP-06 owner usefulness. Cache source, version, selected model, definitions и scope привязать к receipt; старые ACT проверки сохранять как исторические.
6. **Docs/site closure:** обновить package README и relevant RU/EN, registry, затем согласованный site build/links/diagrams. Для Web сначала принять A0/M1 product decisions и minimal read-only experience; App Server execution adapter остаётся более поздним отдельным этапом.

Критерий успеха программы — меньше пользовательских действий и ненужных артефактов при сохранении correctness и approval boundaries. Ни размер отчёта, ни число тестов, ни новый model ID этого не доказывают.

## Проверки и ограничения

Environment: Windows PowerShell, Python 3.13.5, `codex-cli 0.167.0`. Test subprocesses запускались с `-B`, `PYTHONDONTWRITEBYTECODE=1`, synthetic `%TEMP%/paos-audit-tests`. Не выполнялись ACL apply, live model, browser, server, target install, hook trust или cache update.

| Проверка текущего запуска | Наблюдение |
| --- | --- |
| `python -B -m unittest tests.product_agent_os.test_product_agent_os_docs -q` | exit 0; 100 tests, 4.250 s, OK |
| `python -B -m unittest tests.product_agent_os.test_source_policy tests.product_agent_os.test_codex_compatibility tests.product_agent_os.test_validators tests.product_agent_os.test_lifecycle_hooks tests.product_agent_os.test_codex_runtime_runner_state_routes tests.product_agent_os.test_codex_runtime_runner_cli tests.product_agent_os.test_windows_codex_permissions -q` | exit 0; 131 tests, 25.384 s, OK, skipped=1 |
| `python -B -m unittest tests.product_agent_os.test_self_learning_extensions tests.product_agent_os.test_self_learning_state tests.product_agent_os.test_merge_infrastructure tests.product_agent_os.test_project_graph_semantic tests.product_agent_os.test_project_graph_safety tests.product_agent_os.test_batch45_code_quality_behavior tests.product_agent_os.test_batch45_code_quality_metrics tests.product_agent_os.test_codex_runtime_runner_model_output -q` | exit 0; 96 tests, 6.070 s, OK |
| `python -B plugins/product-agent-os/scripts/run_fixture_eval.py` | exit 0; 91/91, failures 0 |
| `python -B plugins/product-agent-os/scripts/run_transcript_eval.py` | exit 0; 26/26, synthetic only |
| `python -B plugins/product-agent-os/scripts/validate_codex_compatibility.py` | exit 1; needs_review / legacy flat MCP; не waived |
| `codex execpolicy check --rules .rules -- rg --files` | exit 1; invalid negative example; F11 |
| `python -B plugins/product-agent-os/scripts/validate_agents.py .codex/agents` | exit 0; 15 profiles, config/file errors 0 |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py .codex/hooks.json` | exit 0; schema only |
| `python -B plugins/product-agent-os/scripts/validate_hooks.py plugins/product-agent-os/assets/templates/hooks/hooks.json` | exit 0; schema only |
| `python -B plugins/product-agent-os/scripts/validate_task_state_consistency.py .` | exit 0; errors 0; эта проверка не заменяет анализ всех B42 projections |
| `python -B tools/check_docs.py` | exit 0; documentation structure passed |
| `git -c core.safecrlf=false diff --check` | exit 0; tracked diff hygiene |
| Read-only AST inventory (`ast.parse` всех tracked `.py`) | exit 0; 302 files, syntax errors 0 |
| Read-only UTF-8/replacement-character scan | exit 0; 1608 selected tracked text files, findings 0 |
| Pure function probes: source policy / skill provenance / hook classifiers / satisfaction | Exit 0 у корректных вызовов; результаты F03/F06/F08 и 12 valid skills, drift 11/12 |
| Source/site comparison | RU/EN current-state HTML отстаёт; F17 |

Первый ad-hoc compatibility probe ошибочно передал `str` вместо объявленного `Path` и завершился AttributeError; после исправления вызывающего кода получен штатный `needs_review`. Это ошибка аудиторского вызова, не дефект продукта. Несколько path lookups по предполагаемым именам отсутствовали; последующий inventory использовал фактические пути. Никакие неудачные lookup не засчитаны как покрытие.

Исторические 1284 unittest / ORD/GAP/site receipts сохранены в owning sources и не выданы за новый полный запуск. Full unittest discovery, actual Codex model eval, fresh-session hook/invocation test, full site rebuild/browser/Mermaid render и vulnerability scan не выполнялись. Новый отдельный отчёт не изменяет nav/diagrams/site, поэтому strict MkDocs не требуется для claim об этом файле.

Self-review: каждый P1 сопоставлен с конкретным code/CLI result и official contract; intentional restrictions (explicit-only skills, local model allowlist, staged providers, supported legacy manifest, historical GPT-5 receipts) не объявлены устаревшими ошибками. Различены pure classifier defect, schema success, host loading и platform permissions. Independent reviewer не запускался; это `self_review`, не blinded review.

### Привязка к проверенной версии и передача между чатами

До передачи marker соседнему Web/PreToolUse чату зафиксированы SHA-256. Его последующие исправления могут закрыть findings, но не меняют результаты этого baseline. Для оценки исправлений нужен diff и новые целевые checks; не переименовывать этот аудит в post-fix acceptance.

| Source | SHA-256 |
| --- | --- |
| `.codex/hooks/pre_tool_use_policy.py` | `244ced9c58aedb2ace885fa4ad5e2f6d1bd1a03c3b8d7b858ef1ef0297bb0878` |
| `plugins/product-agent-os/assets/templates/hooks/pre_tool_use_policy.py` | `244ced9c58aedb2ace885fa4ad5e2f6d1bd1a03c3b8d7b858ef1ef0297bb0878` |
| `.codex/hooks.json`, `.codex/hooks/hooks.json`, packaged `assets/templates/hooks/hooks.json` | `8a40cbbb7bdc0b1d1b48d1ec873b109ee21358d85daae1479891e3a4fec74abb` |
| `.rules` | `16081151166429eaf466de5e93c8a91329834c2e013b81b65c6e4ac681f7aab2` |
| `windows_codex_permissions.py` | `c62f9ec05fa69c2b5f11c4301327c87a2f4d2d95956cb779ae3aebc74817f4d2` |
| `merge_infrastructure.py` | `454d96bd6024764b479f3b9380bc521bf0d09320d4420c0edfee7a067450f6b2` |
| `self_learning_feedback.py` | `30a357273a288440deb0d4051d54c79323a5b62eec77091554d935b925bb3c40` |
| `source_policy.py` | `9fd84e0ce9119f8b0d01a250de95c01da1a3b84e6d4cae6a24505cd833c6f651` |
| `tools/docs_install.ps1` | `1104c2488e6158be92c5e071a5af6d9aa707539f78324b557577f1e9f773bb14` |

Короткие имена core modules в этой таблице относятся к `plugins/product-agent-os/scripts/product_agent_os/`. SHA относятся к точным байтам, а не newline-normalized skill digest.

Финальная проверка отчёта: 18 уникальных findings, пять P1; UTF-8 без replacement characters, парные code fences, trailing whitespace отсутствует. Рабочее дерево перед closure содержит только новый отчёт и изменение marker; implementation/docs/site diffs отсутствуют. Research report не включён в navigation и не является новым site build.

### Воспроизводимые инертные probes

```python
# Выполнять из repo root; не исполняет строки как shell commands.
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, 'plugins/product-agent-os/scripts')
from product_agent_os.source_policy import validate_source_policy
from product_agent_os.self_learning_feedback import evaluate_satisfaction

report = validate_source_policy('.')
print(report['status'], len(report['files']))
print(evaluate_satisfaction([])['promotion_signal'])

spec = importlib.util.spec_from_file_location('audit_hook', '.codex/hooks/pre_tool_use_policy.py')
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)
inert = 'Get-Content README.md; Set-Content audit-sentinel.txt x'
print(hook._is_read_only(inert), hook._is_mutating('Bash', inert))
patch_text = ('*** Begin Patch\n*** Add File: audit-sentinel.md\n'
              '+.codex/product-agent-os/lifecycle-state.json scope_note_shown\n*** End Patch')
print(hook._is_lifecycle_marker_write(patch_text))
# Нет subprocess, apply_patch, write_text или shell execution.
```

## Control-plane sync

REQUIREMENTS/PLAN/TEST/EVALS/prod_test — `not_applicable`: исследование не меняет продуктовые контракты, принятую очередь или historical receipts. RUNLOG — `handoff_required`: compact audit pointer можно добавить при следующей согласованной записи; существующие файлы вне scope. Registry RU/EN — `handoff_required` вместе с будущими docs fixes, поскольку сейчас findings сохранены только в research. Overflow/refactor — `not_applicable`; root files не увеличивались.

Evidence owner: этот отчёт. Авторизованные изменённые пути: данный Markdown и `.codex/product-agent-os/lifecycle-state.json`. Scope ограничен research authoring; implementation, docs source, site, target/cache/trust/ACL и Git history не менялись. Terminal marker освобождает общий scope для следующей отдельной задачи, не закрывая перечисленные findings.
