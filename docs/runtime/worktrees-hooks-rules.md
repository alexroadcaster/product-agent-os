# Worktrees, hooks, rules

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions).

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

Product-Agent OS поставляет staged hooks через `plugins/product-agent-os/assets/templates/hooks/` и `render_infrastructure.py --stage`. Для конечного проекта они попадают в `.codex/hooks/` как proposal/staged asset, а не как silently activated automation.

Lifecycle guard устроен так:

- `SessionStart` показывает наличие control-plane и lifecycle файлов;
- `PreToolUse` пропускает read-only discovery по fast path без чтения marker, но блокирует mutating/non-read-only команды без `.codex/product-agent-os/lifecycle-state.json`;
- Перед mutation покажите применимый scope: для large/high-risk/material/release — `task_start_brief_v2`, `brief_format: bold_fields` и девять полей; для ordinary — `task_scope_note_v1`, `brief_format: concise`, поля Scope/Evidence/Limits. Затем запишите marker с task_id, scope, updated_at, approval_boundary, brief_digest и brief_fields_present; `task_start_brief_shown` относится только к full route. `task_start_brief_v1` / `field_list` сохраняется для уже начатых legacy sessions.
- per-write `PostToolUse` проверяет comment sufficiency только для путей текущего patch, а не повторно для всего dirty worktree;
- после всех записей, проверок и control-plane sync marker переходит в `ready_for_completion_ledger` (full) или `ready_for_completion_brief` (concise/legacy); дальнейшие mutations блокируются;
- Проектный `Stop` рекомендательный: он не проверяет формат чата и не запрашивает корректирующую continuation. Полный scope использует стартовый brief (9 полей) и Completion Ledger (13 пунктов); обычная работа — краткие результаты, проверки и ограничения. Все инструменты и control-plane sync завершаются до финального ответа. Явная локальная проверка пакета не доказывает активацию.

Marker не является transcript store: в него нельзя помещать raw chat, secrets, private source bodies, private customer data или credentials. Activation hooks остаётся отдельным approval boundary.

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
