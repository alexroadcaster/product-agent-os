# Worktrees, hooks, rules

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex worktrees](https://developers.openai.com/codex/app/worktrees), [Codex hooks](https://developers.openai.com/codex/hooks), [Codex rules](https://developers.openai.com/codex/config/rules), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

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
- marker должен появиться только после видимого пользователю полного стартового брифа в формате списка полей и содержать `task_start_brief_shown`, `task_id`, `scope`, `updated_at`, `approval_boundary`, `brief_schema_version: task_start_brief_v1`, `brief_format: field_list`, `brief_digest` и `brief_fields_present` со всеми обязательными полями стартового брифа;
- per-write `PostToolUse` проверяет comment sufficiency только для путей текущего patch, а не повторно для всего dirty worktree;
- после всех записей, проверок и control-plane sync marker переходит в `ready_for_completion_brief`; дальнейшие mutations блокируются;
- `Stop` принимает один terminal `Completion Brief` с полным набором полей без continuation, а при неполном Brief запрашивает не более одной корректирующей continuation. После валидного Brief tool calls запрещены.

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
