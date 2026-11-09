# Worktrees, hooks, rules

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions).

## GAP-05: точное разрешение на отчёт — 05.11.2026

Optional pinned report authority разрешает один новый Markdown через grant, закреплённый SHA-256 в доверенной hook-команде: `--report-authority` и `--report-authority-sha256`. Research/review/planning marker по умолчанию не разрешает запись; payload инструмента не выдаёт authority.

Разрешение связывает хеш workspace, новый и предыдущий task ID, точные байты marker, путь отчёта и срок до 24 часов. Нужен актуальный незавершённый marker с явным переходом задачи. Принимается один literal `apply_patch` Add File, напрямую или единственный literal call внутри `functions.exec`. Существующие и соседние файлы, control-plane/config/hooks, выход за границы пути, симлинки, динамические или множественные вызовы и запись через shell отклоняются. В режиме pinned authority чтение shell ограничено literal `Get-Content`/`Get-ChildItem -LiteralPath 'path'` с `login: false`; другие команды требуют review.

Это preflight guard, не атомарная filesystem transaction. Sandbox, secret/path/command restrictions и host approvals сохраняются. Active/package source синхронизирован; `hooks.json`, trust и cache не изменены. Fresh-host positive/negative probe остаётся отдельным gate. Следующий artifact — exact-hash approval packet и разрешённый probe receipt. Формат grant описан в active/package `task-plan-lifecycle.md`; rollback возвращает только source changes данного slice, не меняя trust.

## Worktree strategy

Используйте worktrees, когда:

- несколько threads могут менять одни файлы;
- задача потенциально широкая;
- нужен изолированный PR;
- long-running job может продолжаться параллельно с локальной работой.

Не используйте один live thread на весь проект. Один thread должен соответствовать одному coherent unit из work.

## Hooks

Hooks подходят для deterministic checks around agent work:

- block generated-file edits без approval;
- запуск lightweight format/lint check;
- log command execution metadata;
- enforce forbidden paths;
- remind about required verification.

Hooks не заменяют human review и не должны хранить secrets.

## Product-Agent OS lifecycle hooks

Product-Agent OS поставляет staged hooks через `plugins/product-agent-os/assets/templates/hooks/` и `render_infrastructure.py --stage`. Для конечного проекта definition предназначен для `.codex/hooks.json`, скрипты — для `.codex/hooks/`; это proposal/staged assets до approved apply и trust.

Lifecycle guard устроен так:

- `SessionStart` показывает наличие control-plane и lifecycle файлов;
- `PreToolUse` пропускает распознанное read-only discovery по fast path; mutations и нераспознанные команды требуют текущего marker своего чата;
- Перед mutation покажите применимый scope: для large/high-risk/material/release — `task_start_brief_v2`, `brief_format: bold_fields` и девять полей; для ordinary — `task_scope_note_v1`, `brief_format: concise`, поля Scope/Evidence/Limits. Затем запишите marker с task_id, scope, updated_at, approval_boundary, brief_digest и brief_fields_present; `task_start_brief_shown` относится только к full route. `task_start_brief_v1` / `field_list` сохраняется для уже начатых legacy sessions.
- per-write `PostToolUse` проверяет comment sufficiency только для путей текущего patch, а не повторно для всего dirty worktree;
- после всех записей, проверок и control-plane sync marker переходит в `ready_for_completion_ledger` (full) или `ready_for_completion_brief` (concise/legacy); дальнейшие mutations блокируются;
- Проектный `Stop` рекомендательный: он не проверяет формат чата и не запрашивает корректирующую continuation. Полный scope использует стартовый brief (9 полей) и Completion Ledger (13 пунктов); обычная работа — краткие результаты, проверки и ограничения. Все инструменты и control-plane sync завершаются до финального ответа. Явная локальная проверка пакета не доказывает активацию.

Marker не является transcript store: в него нельзя помещать raw chat, secrets, private source bodies, private customer data или credentials. Activation hooks остаётся отдельным approval boundary.

С 2026-11-09 local implementation выбирает `.codex/product-agent-os/lifecycle-state.<sha256(session_id)>.json` по top-level host `session_id` и проверяет owner в marker. `SessionStart`, `PreToolUse` и `Stop` используют один selector. Чужой marker не блокирует независимую задачу и не разрешает её действия. Unsuffixed `.codex/product-agent-os/lifecycle-state.json` — legacy только при отсутствии session identity; с session_id fallback запрещён. Scope, freshness и terminal guards сохраняются. Состояние marker не является разрешением на произвольные файлы; пересечения по одним файлам всё ещё требуют coordination. Основание поля session_id: [официальный Hooks contract](https://learn.chatgpt.com/docs/hooks#common-input-fields). Local evidence и пределы host verification: `research/product-agent-os-session-lifecycle-fix-2026-11-09.md`.

## Rules

Rules описывают policy, которую Codex должен учитывать перед действиями. Хорошие rules:

- narrow;
- auditable;
- aligned с sandbox/approvals;
- проверено на real workflows.

## Режимы отказа

| Failure | Prevention |
| --- | --- |
| Two agents edit same files | Worktree per task или explicit ownership |
| Hook blocks valid task | Narrow rule и allow documented approval |
| Agent misses project conventions | `AGENTS.md` + nested instructions |
| Long thread drifts | `/compact`, `/fork`, один thread per coherent task |
| Automation запускается too early | Manual skill workflow first |

## Текущий hook contract и диагностика активации

Проверено 2026-11-03: [Hooks reference](https://learn.chatgpt.com/docs/hooks). Non-managed hooks требуют review/trust текущего hash; новые или измененные определения пропускаются до trust. Доверенный project layer и корректный JSON сами по себе не доказывают исполнение. Поддерживаются `command` и `mcp_tool`; `prompt`/`agent` handlers парсятся, но пропускаются. Несколько matching command hooks одного события могут выполняться параллельно: не рассчитывайте на порядок записи общего состояния.

| Событие | Граница |
| --- | --- |
| `SessionStart` | Контекст старта; не приемка реализации |
| `PreToolUse` | Поддерживаемый deny может предотвратить действие; ошибка callback не равна гарантированному запрету |
| `PostToolUse` | Проверка после действия; не может отменить уже выполненный side effect |
| `Stop` | Может запросить continuation; учитывать `stop_hook_active`, чтобы не создать цикл |
| `SessionEnd`, `Interrupt` | Короткий best-effort lifecycle, не долгий gate |

`timeout` задается в секундах: обычно по умолчанию 600, для `SessionEnd`/`Interrupt` — 1 и максимум 3. У MCP действует меньший hook/server timeout; ожидание elicitation имеет отдельную семантику. Покрытие зависит от tool/event и runtime. Cloud-orchestrated enterprise remote MCP hooks имеют отдельные ограничения; локальный command hook нельзя считать универсальным cloud guardrail. Перед использованием проверяйте точную строку покрытия в reference.

Для доказательства активации нужны: client/runtime, загруженный источник, hash/trust, реально сработавший event/tool, разрешенный сценарий и наблюдаемый результат. Разбор JSON, unit tests и прямой запуск hook script — локальные evidence, не fresh-session proof. Receipt от 03.11.2026 фиксирует `verified_local_runtime` для проверенных Desktop маршрутов: large, ordinary и terminal-marker denial. ACT-F1..F6 закрыты в source-owned `lifecycle_parity.repair`; это исторически выполненный run, не новая проверка этой страницы. Silent Stop execution и полнота всех mutation channels не доказаны. [Текущая граница evidence](../product-agent-os/control-plane-current-state.md). Проектный `Stop` lifecycle выше остается правилом проекта, а не универсальной семантикой OpenAI.

## Trust и границы исполнения

Проверено 05.11.2026 по [Hooks](https://learn.chatgpt.com/docs/hooks). Определения hooks из применимых источников объединяются; более близкий файл не заменяет все предыдущие hooks. Matching command hooks могут стартовать параллельно. После изменения определения или bundled plugin script нужен повторный review; install/enabled не равны trusted/executed.

MCP hook использует уже доступный сервер: он не запускает и не переподключает MCP. Недоступный сервер, tool или ошибка MCP hook не дают гарантированного запрета — fail-closed нужно проверять отдельно. В cloud-orchestrated Work локальные command/plugin hooks не поддерживаются; поддерживаемые admin-managed MCP hooks настраиваются отдельно.

Worktree разделяет Git working files, но не создаёт отдельные permissions. Для одного небольшого изменения обычно достаточно текущего workspace. Git-only worktrees, setup и Handoff выбирайте по [официальному маршруту](https://learn.chatgpt.com/docs/environments/git-worktrees) и project authority. Проверка: загруженная definition и trust → allowed case → denied case → evidence конкретного tool/runtime.

## Локальные исправления PAOS-AUD-G1 — 09.11.2026

Generated manifest и `hook_policy` теперь указывают `.codex/hooks.json`; скрипты
остаются в `.codex/hooks/`. Старый mirror не является discovery config. Staging
не активирует hooks; merge создаёт definition только с точным `enable_hooks`
approval, сохраняет существующий пользовательский файл и поддерживает rollback.
Trust и fresh-host acceptance проверяются отдельно. Основание discovery/trust:
[официальный Hooks contract](https://learn.chatgpt.com/docs/hooks).

Guard проверяет весь ограниченно распознаваемый read-only command; составные и
неизвестные формы требуют текущего mutation scope. Текст Markdown patch является
данными; отдельно проверяются destination paths. Реальные destructive commands
и sensitive destinations остаются защищены.

Корневой `.rules` — проверяемый proposal, не установленный discovery-файл.
`match`/`not_match` — примеры для parser assertions, а не исключения из prefix.
Поскольку произвольные trailing arguments могут менять действие команды,
proposal использует `prompt` для review и сохраняет `forbidden` для системных
изменений; широких `allow` нет. Проверка: `codex execpolicy check --rules .rules -- rg --files`.
Команда проверяет решение без исполнения `rg`. Файл `.codex/rules/default.rules`
не создаётся. Семантика: [официальные Rules](https://learn.chatgpt.com/docs/agent-configuration/rules).

Опциональный report authoring v2 явно использует `work_type: report_authoring`,
пин одного grant, session ownership, exact Markdown path и previous digest на
каждую create/update. Legacy create-only v1 сохранён. Подробный контракт находится
в `.codex/workflows/task-plan-lifecycle.md`; источник и local verification —
`research/product-agent-os-audit-remediation-task-plan-2026-11-09.md`.
CAS preflight отклоняет уже возникший conflict, но не блокирует промежуток между
hook и записью: требуется один writer; атомарность и fresh-host activation не доказаны.
