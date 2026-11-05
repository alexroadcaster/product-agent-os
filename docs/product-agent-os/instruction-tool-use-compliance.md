# Instruction and tool-use compliance

Source status: `official + project evidence`

Источники: [Agent Skills](https://developers.openai.com/codex/skills), [Plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [`AGENTS.md`](https://developers.openai.com/codex/guides/agents-md), [Hooks](https://developers.openai.com/codex/hooks), [Permissions](https://developers.openai.com/codex/permissions), [Subagents](https://developers.openai.com/codex/subagents), [Skill exposure and invocation boundary](../diagrams/skill-exposure-and-invocation.md), `docs/superpowers/specs/batch42-instruction-tool-use-compliance-matrix.json`.

Эта страница описывает, как Product-Agent OS должен обрабатывать запросы про instruction compliance, tool-use compliance, skill/plugin exposure и self-learning-loop. Она не утверждает, что auto-engagement уже исправлен. Текущее состояние: `planned-only` для Batch 42 execution и `implemented_source_docs_no_site_rebuild` для этой документационной страницы.

## Что проверяется

| Слой | Что доказывает | Чего не доказывает |
| --- | --- | --- |
| Source bundle | В repository есть plugin, skills, scripts, templates и docs. | Skill доступен в installed cache или active session. |
| Installed plugin cache | Локальная установленная копия может существовать. | Current Codex session видит все skills или вызывает их implicitly. |
| Active session | Session реально получила часть skill/plugin metadata. | Route выбран правильно для каждого prompt. |
| Route/eval evidence | Prompt classified через нужный lifecycle/compliance path. | Config/cache mutation, release readiness или external action approval. |
| Fresh-session proof | Новая session видит ожидаемое состояние после changes. | Старые sessions автоматически обновились. |

## Политика invocation

Codex official docs описывают два способа skill invocation: explicit invocation, когда пользователь прямо называет skill, и implicit invocation, когда task matches skill `description`. Product-Agent OS применяет более строгую локальную политику:

| Mode | Когда использовать | Gate |
| --- | --- | --- |
| `explicit_only` | Высокорисковые skills, release, automation, external write, cache/config mutation, provider/API, browser/runtime или security-sensitive work. | Пользователь явно просит skill/plugin/agent route. |
| `narrow_implicit` | Read-only discovery, docs-maintenance, planning, compliance audit или learning-loop triage, когда prompt clearly matches Product-Agent OS boundary. | Route/eval evidence и no-unapproved-actions proof. |
| `blocked_implicit` | Любой skill с `allow_implicit_invocation: false`, unclear ownership или missing evidence. | Нужен explicit user request или policy change approval. |

`allow_implicit_invocation` является policy metadata, а не самостоятельным proof качества. Даже если implicit invocation разрешён, approval settings, sandbox, permissions, hooks trust и external-service auth продолжают действовать.

## No-auto-apply learning loop

Self-learning-loop в Product-Agent OS может записать lesson, candidate rule, skill update candidate, eval follow-up или owner question. Он не должен сам:

- менять `~/.codex/config.toml`, project `.codex/config.toml`, installed plugin cache или global guidance;
- активировать hooks, automations, MCP servers, Agents SDK runner или external workflows;
- stage/commit/push/create PR, publish, deploy или share plugin;
- сохранять secrets, raw private chat logs, customer data или unredacted findings.

Любой candidate должен пройти owner review, rollback/disable path и separate approval.

## Compliance packet

Для claim "Product-Agent OS now engages correctly" нужен packet со следующими полями:

| Field | Required evidence |
| --- | --- |
| `source_bundle_status` | Source tree path, manifest/skill list, agent metadata and policy class. |
| `installed_cache_status` | Read-only cache inventory or explicit not-inspected gap. |
| `active_session_status` | Fresh session exposure, missing skills and restart/new-thread boundary. |
| `route_eval_status` | Prompt fixtures or transcript evals for compliance/tool-use prompts. |
| `official_source_status` | Current official Codex docs checked date and supported/unsupported claims. |
| `approval_boundary` | Exact surfaces that remain approval_required. |
| `no_unapproved_actions` | Cache/config/global/external/git/release/browser/provider/automation flags all false unless explicitly approved. |

## Unsupported claims

Эта страница не поддерживает claims:

- all Product-Agent OS skills are visible in every active session;
- auto-engagement is fixed;
- installed cache has been refreshed;
- global Codex policy or project config has been changed;
- hooks are trusted in every new session;
- self-learning-loop can mutate skills, memory, rules, hooks or automations automatically;
- docs/source evidence proves runtime/browser/provider behavior, publication or release readiness.

## Next safe action

Если operator видит, что Product-Agent OS не включился на релевантный prompt, первый безопасный шаг: создать read-only source/cache/session packet, затем route/eval packet. Cache refresh, global config writes, plugin sharing, hook trust changes and fresh-session proof остаются отдельными approvals.

## Актуальный маршрут и evidence

Применимый full/concise lifecycle, trust и terminal marker описаны в [hook guide](../runtime/worktrees-hooks-rules.md). Local receipt от 03.11 покрывает проверенные Desktop routes; полнота всех mutation channels и silent Stop trace не заявляются.
