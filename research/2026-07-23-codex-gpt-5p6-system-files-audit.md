# Критический аудит системных файлов `.codex` для GPT-5.6

Source status: current repository evidence plus official OpenAI documentation; checked 2026-07-23.

- Audit ID: `CODEX-GPT56-SYSTEM-AUDIT-REMEDIATION-20260723`
- Scope: все 92 фактически присутствующих файла под `.codex`, включая 89 tracked source/evidence files и 3 производных `.pyc`.
- Основной объект: active config, 15 custom agents, назначенные skills, hooks, workflows, artifact templates, eval contract и lifecycle marker.
- Исторический объект: 36 Batch 45 review-файлов; они проверены на тип и границу доказательств, но не мигрированы задним числом.
- Статус: `implemented_with_gaps`.
- Closure level: `active_config_and_contracts_updated_fresh_session_and_behavioral_promotion_pending`.

## Итог

Аудит выявил три P1-дефекта, семь P2-дефектов и два P3-дефекта. Все P1 устранены. Из P2 остаётся один осознанный portability gap: user-level skills по-прежнему заданы абсолютными host-local путями, потому что официальная схема допускает `skills.config.path`, текущие 31 уникальный путь существуют, а перенос или vendoring чужих skills не входил в разрешённый scope. Три `.pyc` классифицированы как производный cache, а не source truth; они не изменялись и не использовались как доказательство.

Ключевые изменения:

- 15 активных agent profiles переведены с GPT-5.5/GPT-5.4 Mini на role-aware `gpt-5.6-sol`/`gpt-5.6-terra` без автоматического повышения reasoning effort.
- Активный `.codex/config.toml` и генерационный config template приведены к текущему `[agents]` contract; policy-only поля вынесены в `[product_agent_os.*]`.
- Hooks переведены с самодельных payloads на документированные `hookSpecificOutput`, `permissionDecision`, `permissionDecisionReason`, `additionalContext` и `systemMessage`.
- Lifecycle marker получил строгий SHA-256 digest, freshness window, timezone check, `in_progress`/completion checks и отказ при stale/completed state.
- `fork_context` заменён на фактически поддерживаемый параметр `fork_turns` во всех активных packets, workflows, skills и генерационных templates.
- Phase-specific Batch 39/B37 routing удалён из durable templates/workflows; исторические evidence-файлы сохранены.
- Model/eval templates теперь требуют same-effort и one-lower-effort сравнение с quality/cost/latency/fresh-session evidence.

Не заявляется:

- что GPT-5.6 уже дал лучшее качество или меньшую стоимость;
- что все hooks проверены после нового `SessionStart` в отдельной свежей сессии;
- что absolute user-level skill paths переносимы на другой компьютер;
- что исторические GPT-5.5 результаты Batch 45 были повторно измерены на GPT-5.6.

## Метод аудита

Под «построчным» анализом здесь понимается проверка каждой исполняемой или нормативной строки, а не комментарий к каждой пустой строке. Для TOML проверялись все top-level keys, tables, model/effort/sandbox fields, `developer_instructions` и каждый `[[skills.config]]`. Для JSON проверялись все events, matchers, handlers и stdout contracts. Для Markdown — каждый нормативный imperative, ownership/stop/approval/evidence gate и phase-specific literal. Для Python hooks — все branches, input extraction, deny/allow path, sensitive-path checks, lifecycle validation и JSON output.

Проверка включала:

1. Файловый inventory и tracked/non-tracked классификацию.
2. Сопоставление с официальной документацией, актуальной на 2026-07-23.
3. Поиск drift-маркеров: устаревшие model IDs, `fork_context`, unsupported config keys, custom hook decisions, stale batch routing, duplicate canonical files, absolute skill paths, weak lifecycle digest.
4. Проверку source templates плагина, чтобы последующий renderer не вернул исправленные дефекты.
5. Контрактные тесты, Codex Doctor, agent validator, JSON/TOML/Python parse checks и docs checks.

## Матрица официальных источников

| Source | Поддерживаемое утверждение | Relevance | Freshness | Confidence | Конфликты/оговорки |
| --- | --- | --- | --- | --- | --- |
| [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6) | `gpt-5.6` маршрутизируется к Sol; при миграции следует сохранить baseline effort и сравнить тот же effort с одним более низким | Прямое основание model migration/eval policy | 2026-07-23 | high | Не предписывает проектную role matrix; Sol/Terra mapping ниже является проектным решением |
| [Codex models](https://learn.chatgpt.com/docs/models) | Sol предназначен для сложной открытой работы; Terra — balanced everyday work; Luna — high-volume candidate | Основание role-aware pins | 2026-07-23 | high | Luna не активирован: нет bounded project eval |
| [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Обязательны `name`, `description`, `developer_instructions`; допустимы `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`; официальный concurrency key — `max_concurrent_threads_per_session`; `max_threads` — legacy alias | Agent/config schema | 2026-07-23 | high | Документ показывает absolute skill path как допустимый пример, но не доказывает cross-host portability |
| [Config reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Official keys следует держать в их документированных tables; project policy metadata не должна маскироваться под runtime settings | Config remediation | 2026-07-23 | high | Product-Agent OS tables являются project extension и не интерпретируются как native runtime settings |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | `PreToolUse` deny возвращает `hookSpecificOutput` с `permissionDecision`; Session/Post используют `additionalContext`; common reminders используют `systemMessage`; hook — guardrail, а не proof | Hook wire contract | 2026-07-23 | high | Текущая сессия дала live Pre/Post evidence, но fresh `SessionStart` не запускался |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | Skills — отдельные `SKILL.md` workflows, обнаруживаемые через поддерживаемые каталоги/config | Skill audit | 2026-07-23 | high | Наличие пути не доказывает качество или переносимость skill |
| [`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Инструкции наследуются по иерархии и имеют ограниченный combined size; durable rules должны быть компактными | Instruction audit | 2026-07-23 | high | Точный runtime context всё равно зависит от активной сессии и ближайшего `AGENTS.md` |

## Инвентаризация

| Категория | Файлов | Tracked | Критичность |
| --- | ---: | ---: | --- |
| Agent profiles | 15 | 15 | active runtime contract |
| Artifact templates | 15 | 15 | durable generation/input contract |
| Eval contracts | 1 | 1 | active behavioral/contract gate |
| Hooks, включая canonical/mirror/scripts/cache | 10 | 8 | active runtime guardrail; 2 derived cache files |
| Workflows | 7 | 7 | durable lifecycle instructions |
| Product-Agent OS lifecycle/pilot/reviews | 42 | 41 | 1 active marker, 4 pilot sources, 36 historical reviews, 1 derived cache |
| Root `.codex` files | 2 | 2 | active config and canonical hooks |
| **Всего** | **92** | **89** | **3 untracked/ignored `.pyc`** |

## Findings по severity

### P1 — устранены

#### F-01. Устаревшие model pins и недифференцированная роль моделей

- До: 14 profiles были pinned на `gpt-5.5`, explorer — на `gpt-5.4-mini`.
- Риск: новый model family не активировался; лёгкие и judge-роли имели одинаковый cost/latency profile; отсутствовал migration gate.
- Исправление: строки 3-4 каждого `.codex/agents/*.toml` теперь используют Sol/Terra и сохраняют прежний effort. Policy и promotion gate находятся в `.codex/config.toml:111` и `.codex/artifact-templates/model-reasoning-policy.md:11`.
- Статус: `fixed_contract`; behavioral superiority остаётся `present_unverified`.

#### F-02. Недокументированные stdout payloads hooks

- До: scripts печатали custom `hook`, `decision`, `blocking`, `reminders`; PreToolUse завершался кодом 1 вместо документированного deny payload.
- Риск: Codex мог проигнорировать «решение», а пользователь получил бы ложное впечатление активного enforcement.
- Исправление: `.codex/hooks/pre_tool_use_policy.py:224-227`, `post_tool_use_evidence.py:19-22`, `session_start_context.py:91-94`, `permission_request_summary.py:17`, `stop_runlog_reminder.py:17`; active/mirror/plugin templates синхронизированы.
- Current activation evidence: текущая Codex-сессия показала model-visible PostToolUse reminder и реально отклонила команду, содержащую буквальный destructive test command.
- Статус: `fixed_and_partially_runtime_observed`; новый SessionStart остаётся непроверенным.

#### F-03. Lifecycle marker не доказывал актуальный Task Brief

- До: короткий digest, фиксированная старая дата, отсутствие строгих `status`/completion/freshness checks.
- Риск: старый marker мог бесконечно разрешать новые mutations.
- Исправление: `brief_digest` теперь `sha256:<64 hex>`, `updated_at` timezone-aware, max age 48 часов, future skew 5 минут; `status=in_progress`, `completion_brief_shown=false`; stale/completed/invalid markers denied (`pre_tool_use_policy.py:16`, `181`, `213`).
- Статус: `fixed_and_tested`.

### P2 — шесть устранены, один gap принят

#### F-04. Drift config schema

- До: `max_threads`, `max_depth`, `job_max_runtime_seconds`, top-level `[sandbox]`/`[approvals]`, agent path aliases и custom metadata в native namespace.
- Исправление: `.codex/config.toml:20` использует `max_concurrent_threads_per_session`; policy metadata перемещена в `[product_agent_os.*]`; source template переписан на `[agents.<name>].config_file` и canonical hook route.
- Evidence: `codex --strict-config doctor --summary` загрузил config с 0 fail.
- Статус: `fixed`.

#### F-05. Два hook JSON выглядели как два active policy owners

- До: config и eval перечисляли `.codex/hooks.json` и `.codex/hooks/hooks.json` как равноправные active files.
- Исправление: `.codex/hooks.json` — canonical policy; `.codex/hooks/hooks.json` — явно названный template mirror через `.codex/config.toml:94-95`; eval/SessionStart требуют только canonical file.
- Статус: `fixed`; byte-for-byte equality проверяется тестом.

#### F-06. Несуществующий/дрейфующий `fork_context`

- До: handoff packets, workflows, evals и skill references требовали `fork_context`.
- Исправление: везде заменено на доступный orchestration parameter `fork_turns`; active references: `.codex/workflows/worktree-ownership.md:28`, `.codex/artifact-templates/subagent-context-packet.md:14`, `.codex/evals/agent-context-contract.json:58`.
- Статус: `fixed`.

#### F-07. Phase-specific routing в durable instructions

- До: durable workflow/eval/template содержали Batch 39 и B37-S2 как обязательный текущий маршрут.
- Риск: новый task мог ошибочно обновлять исторический ledger или считать временную фазу вечным contract.
- Исправление: current routing принадлежит `PLAN.md`/`RUNLOG.md`; `prod_test.md` обновляется только при явном изменении Batch 39 evidence; B37 marker удалён из task template.
- Статус: `fixed`; исторические документы не переписаны.

#### F-08. Host-local absolute skill paths

- Наблюдение: 75 назначений, 31 уникальный `SKILL.md`, 0 missing на текущем host. 12 project skills, 18 user `.agents` skills и 1 system `openai-docs` skill.
- Риск: clone на другой host не получит user-level skills по тем же путям.
- Решение в этом slice: не vendorить и не переписывать third-party/user assets без отдельного owner decision; `.codex/config.toml` теперь прямо ограничивает claim текущим host.
- Статус: `accepted_gap_not_portable`; follow-up trigger — перенос репозитория или packaging plugin.

#### F-09. Model migration не имела traceable eval matrix

- До: template не фиксировал model ID, effort, prompt/tools/settings, quality, latency, tokens/cost и fresh-session evidence.
- Исправление: `.codex/artifact-templates/test-eval-matrix.md:23-32`, `.codex/artifact-templates/model-reasoning-policy.md:21-31`, `.codex/evals/agent-context-contract.json:252-266`.
- Статус: `fixed_contract`; live comparison не запускался.

#### F-10. Source template мог регенерировать старые дефекты

- До: plugin templates сохраняли old config namespace, `fork_context`, phase markers и старый hook output contract.
- Исправление: matching files под `plugins/product-agent-os/assets/templates/` и `plugins/product-agent-os/skills/` обновлены вместе с active `.codex` files; infrastructure tests обновлены.
- Статус: `fixed_and_template_tested`.

### P3 — устранено/классифицировано

#### F-11. Дублирующие schema notes и слабая skill routing семантика

- Удалены unsupported `nickname_candidates` и повторяющиеся optional-field notes из agent profiles.
- Product Manager теперь маршрутизируется в project `implementation-planner`, Research Source Analyst — в `verification-before-completion`; exact skill count перестал называться quality gate, хотя текущие profiles сохраняют по 5 назначений.
- Статус: `fixed`.

#### F-12. Три `.pyc` внутри audit scope

- Файлы являются derived cache, не tracked source и не должны участвовать в source/evidence claims.
- Они не удалялись: user request не содержал отдельного cleanup approval, а существующий cache не мешает contract validation.
- Статус: `classified_non_source`; cleanup optional.

## Agent files: построчный contract-аудит

Во всех 15 profiles проверены строки `name`, `description`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, полный `developer_instructions` contract, ownership/inputs/outputs/stop/handoff и пять `[[skills.config]]`. `validate_agents.py` вернул 15/15 без ошибок.

| Файл | Было → стало | Effort | Sandbox | Skills | Анализ инструкций и правка |
| --- | --- | --- | --- | ---: | --- |
| `architect.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | workspace-write | 5 | Удалён Batch 39 routing; write разрешён только по approved plan; сохранены architecture/rollback boundaries |
| `builder.toml` | `gpt-5.5` → `gpt-5.6-terra` | medium | workspace-write | 5 | `fork_turns`; implementation scope и no-external-actions согласованы |
| `completion-skeptic.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | read-only | 5 | Judge-only contract сохранён; unsupported optional schema notes удалены |
| `docs-maintainer.toml` | `gpt-5.5` → `gpt-5.6-terra` | medium | workspace-write | 5 | Source-registry/docs ownership сохранён; `fork_turns`; no readiness without evidence |
| `explorer.toml` | `gpt-5.4-mini` → `gpt-5.6-terra` | low | read-only | 5 | Удалён Batch 39 current-queue bias; read-only/no edit contract согласован |
| `graph-cockpit-engineer.toml` | `gpt-5.5` → `gpt-5.6-terra` | medium | workspace-write | 5 | Generated graph остаётся orientation only; schema notes удалены |
| `learning-loop-engineer.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | workspace-write | 5 | Candidate-only/manual-promotion gate сохранён |
| `lifecycle-orchestrator.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | workspace-write | 5 | Lifecycle/fresh-context ownership сохранён; no delegated launch implied |
| `plugin-runtime-builder.toml` | `gpt-5.5` → `gpt-5.6-terra` | medium | workspace-write | 5 | Focused plugin implementation и approval boundaries сохранены |
| `product-manager.toml` | `gpt-5.5` → `gpt-5.6-sol` | medium | workspace-write | 5 | Удалён Batch 39 queue; sandbox больше не конфликтует с requirements ownership; default planning skill исправлен |
| `release-operator.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | read-only | 5 | Удалён Batch 39 release gate; draft-only/no git-release action сохранён |
| `research-source-analyst.toml` | `gpt-5.5` → `gpt-5.6-sol` | medium | read-only | 5 | Source-matrix role сохранён; default verification skill заменил broad skill discovery |
| `reviewer.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | read-only | 5 | Удалён Batch 39 routing; findings-first/read-only contract сохранён |
| `security-privacy-supply-chain-reviewer.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | read-only | 5 | Secret/PII/supply-chain boundaries сохранены; schema notes удалены |
| `tester.toml` | `gpt-5.5` → `gpt-5.6-sol` | high | workspace-write | 5 | Удалён Batch 39 gate; write ограничен test artifacts/assigned verification files |

## Skills: назначение и критическая оценка

- Назначений в agent TOML: `75`.
- Уникальных paths: `31`.
- Missing paths на текущем host: `0`.
- Каждый agent имеет 5 focused assignments; это текущая конфигурация, не quality metric.
- Project skills проверяются как source-owned; user/system skills — как available host dependencies, а не repository-owned source truth.
- `qa`, `to-prd`, `find-skills` остаются installed-but-unassigned: это осознанное уменьшение broad/default routing.

### Полный реестр уникальных skill dependencies
| Scope | Skill | References | Current-host status |
| --- | --- | ---: | --- |
| user | `<user-home>/.agents/skills/adk-evals/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/antv-g6-graph/SKILL.md` | 1 | present |
| user | `<user-home>/.agents/skills/changelog-writer/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/dispatching-parallel-agents/SKILL.md` | 1 | present |
| user | `<user-home>/.agents/skills/documentation-and-adrs/SKILL.md` | 7 | present |
| user | `<user-home>/.agents/skills/documentation-writer/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/executing-plans/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/graphify/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/handoff/SKILL.md` | 3 | present |
| user | `<user-home>/.agents/skills/improve-codebase-architecture/SKILL.md` | 3 | present |
| user | `<user-home>/.agents/skills/python-code-style/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/python-design-patterns/SKILL.md` | 3 | present |
| user | `<user-home>/.agents/skills/security-best-practices/SKILL.md` | 1 | present |
| user | `<user-home>/.agents/skills/security-review/SKILL.md` | 2 | present |
| user | `<user-home>/.agents/skills/subagent-driven-development/SKILL.md` | 1 | present |
| user | `<user-home>/.agents/skills/tdd/SKILL.md` | 3 | present |
| user | `<user-home>/.agents/skills/verification-before-completion/SKILL.md` | 7 | present |
| user | `<user-home>/.agents/skills/writing-plans/SKILL.md` | 2 | present |
| system | `<user-home>/.codex/skills/.system/openai-docs/SKILL.md` | 3 | present |
| project | `plugins/product-agent-os/skills/agent-team-designer/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/automation-promoter/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/completion-skeptic/SKILL.md` | 3 | present |
| project | `plugins/product-agent-os/skills/docs-maintainer/SKILL.md` | 2 | present |
| project | `plugins/product-agent-os/skills/implementation-planner/SKILL.md` | 4 | present |
| project | `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/pr-release-operator/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/requirements-author/SKILL.md` | 1 | present |
| project | `plugins/product-agent-os/skills/risk-reviewer/SKILL.md` | 4 | present |
| project | `plugins/product-agent-os/skills/test-eval-designer/SKILL.md` | 4 | present |
| project | `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md` | 3 | present |

## Config: line-by-line decision ledger

| Lines | Проверка | Решение |
| --- | --- | --- |
| 1-18 | Permission profile | Сохранён как Codex App/managed workspace extension; write roots остаются локальными, external actions отдельно approval-bound |
| 20 | Agent concurrency | `max_concurrent_threads_per_session = 6`; legacy/unsupported siblings удалены |
| 22-65 | Agent registry | 15 hyphenated IDs, каждый через `config_file`; имена совпадают с `name` field |
| 67-107 | Autonomy/lifecycle/reasoning | Project-only metadata находится в `[product_agent_os.*]`; canonical hook и mirror разделены |
| 111-117 | Model migration | Family, baseline effort, same/lower comparison, fresh-session и quality/cost/latency gates |
| 119-138 | Sandbox/approval contracts | Policy metadata отделена от native agent file `sandbox_mode`; все risky surfaces explicit/forbidden |
| 140-153 | Workflow/eval routing | Только current source-owned workflow/eval paths |
| 155+ | Project/skill routing | Current focus phase-neutral; host-local skill portability явно ограничена |

## Hooks: файл за файлом

| Файл | Роль | Критический результат |
| --- | --- | --- |
| `.codex/hooks.json` | canonical active route | Официальные events/matchers/command handlers; `commandWindows`, timeout, statusMessage; один owner |
| `.codex/hooks/hooks.json` | template mirror | Не участвует как второй active contract; идентичен canonical JSON |
| `pre_tool_use_policy.py` | deterministic deny guard | Allow печатает nothing; deny использует официальный wire; lifecycle freshness/digest/completion checks; exit 0 |
| `permission_request_summary.py` | approval reminder | Не принимает решение за пользователя; только `systemMessage` |
| `post_tool_use_evidence.py` | evidence reminder | `PostToolUse.additionalContext`; hook output не объявляется proof |
| `session_start_context.py` | compact startup context | Только relative file presence; no absolute path output; canonical hook list |
| `stop_runlog_reminder.py` | completion ledger reminder | `systemMessage`; не блокирует и не заставляет продолжать |
| `comment_sufficiency_advisory.py` | reviewer-only code signal | Zero-output без warnings; official PostToolUse context при warning; fail-open; host path redaction; phase-neutral env names с legacy aliases |
| 2 `.pyc` в hooks cache | derived runtime cache | Не source, не proof, не tracked |

## Workflows

| Файл | Статус | Вывод |
| --- | --- | --- |
| `build-slice.md` | inspected/no change | Focused implementation, verification и approval boundaries актуальны |
| `coding-standards.md` | inspected/no change | Existing-capability/professional-code gate остаётся применимым независимо от модели |
| `control-plane-sync.md` | changed | Исторический Batch 39 ledger стал conditional; source-owned current evidence generalised |
| `review-slice.md` | changed | Stop condition больше не требует Batch 39 для любого review |
| `source-context-pack.md` | inspected/no change | Source truth/limited context contract совместим с GPT-5.6 |
| `task-plan-lifecycle.md` | inspected/no change | Task/Completion Brief routing остаётся config-owned |
| `worktree-ownership.md` | changed | `fork_turns`, ownership/fresh-context packet terminology синхронизированы |

## Artifact templates и eval

| Файл/группа | Результат |
| --- | --- |
| `model-reasoning-policy.md` | Полностью обновлён под Sol/Terra/Luna-candidate, same/lower effort, fresh-session, quality/cost/latency promotion |
| `test-eval-matrix.md` | Добавлены model, effort, settings fingerprint, latency, tokens/cost и GPT-5.6 comparison rows |
| `task-matrix-plan.md` | Удалён временный `B37-S2`; lifecycle/evidence contract сохранён |
| `subagent-context-packet.md`, `subagent-result-packet.md` | `fork_turns` вместо drifted `fork_context` |
| `agent-context-contract.json` | Canonical hook owner, official hook wire, marker freshness, GPT-5.6 role/eval cases, phase-neutral ledger routing |
| Остальные 10 artifact templates | Построчно проверены; model-independent, source/evidence/approval contracts актуальны, изменений не требовали |

## Исторические Batch 45 и manual-pilot files

36 review-файлов под `.codex/product-agent-os/**/batch45/**` — historical evidence. Упоминания GPT-5.5, прошлых verdicts, timestamp и approval state в них не являются active pins и поэтому сохранены без переписывания. Четыре manual-pilot source files также не содержат active model selection; они остаются reproducibility artifacts. Это предотвращает подмену истории новой конфигурацией.

## Применённые изменения вне active `.codex`

Чтобы renderer не возвращал drift, синхронно обновлены:

- `plugins/product-agent-os/assets/templates/agents/*.toml` для 8 генерируемых ролей;
- `plugins/product-agent-os/assets/templates/config/config.toml`;
- `plugins/product-agent-os/assets/templates/hooks/*`;
- matching workflows, evals и artifact templates;
- `plugins/product-agent-os/skills/agent-team-designer/SKILL.md` и `skills/references/handoff-contract.md`;
- `tests/product_agent_os/test_lifecycle_hooks.py`, `test_infrastructure_templates.py`, `test_infrastructure_renderer.py`, `test_batch45_s3_professional_code_authoring.py` и `test_coding_standards_artifacts.py`;
- `plugins/product-agent-os/scripts/product_agent_os/windows_codex_permissions.py` и его Windows contract tests.

## Дополнительные дефекты, найденные broad verification

Эти defects находятся вне исходного 92-файлового `.codex` severity count, но непосредственно мешали честной repo-wide проверке remediation:

- `V-01 (P2)`: 15 исторических Batch 45 tests читали mutable `.codex/product-agent-os/lifecycle-state.json` и отвергали любой новый task ID. Исправление: при unrelated active task они проверяют последний source-owned T22 projection; текущий marker не подменяется, исторические packets не меняются.
- `V-02 (P2)`: legacy test требовал phase-specific `coding-standards.md` в общем PreToolUse hook. Исправление: candidate reminder остаётся видимым в `hook-governance.md`, а active PreToolUse/Stop tests требуют phase-neutral lifecycle/official-wire contract.
- `V-03 (P2)`: Windows permission CLI декодировал локализованный `icacls` как UTF-8 и падал на системной code page. Исправление: platform text encoding (`mbcs` на Windows) с bounded replacement, плюс intent docstrings для ACL mutation/deny parsing.

Первый broad run выявил `18 failures`, `1 error`, `1 skip`; второй после V-01/V-03 оставил только V-02; финальный повтор завершился `1191 tests`, `OK (skipped=1)`. Эти правки не поддерживают runtime или GPT-5.6 quality claim.

`apply_patch` в этой Windows-сессии воспроизводимо завершался `os error 206` даже на минимальном hunk. После проверки target paths изменения применялись deterministic exact replacements/whole-file writes через PowerShell с assertions. Это tooling gap, а не product behavior claim.

## Verification evidence

| Check | Current-run result |
| --- | --- |
| `python plugins\product-agent-os\scripts\validate_agents.py .codex\agents` | PASS, 15 files, `errors: []` |
| 31 unique skill paths existence check | PASS, missing 0 |
| `codex --strict-config doctor --summary` | Config loaded, 0 fail; unrelated warnings: optional MCP env and rollout scan |
| `python -m unittest tests.product_agent_os.test_lifecycle_hooks -v` | PASS, 19 tests |
| `python -m unittest tests.product_agent_os.test_infrastructure_templates -q` | PASS, 94 tests |
| JSON/TOML/Python parse and mirror equality | PASS: 25 TOML, 10 JSON, 12 Python AST; 7/7 mirror sets equal |
| Audit-ledger reconciliation against recursive `.codex` inventory | PASS, exit 0: `Actual=92`, `Ledger=92`, `Missing=0`, `Extra=0` |
| Active drift-term scan | PASS: `NO_STALE_ACTIVE_TERMS` for removed keys/model pins in active/template surfaces |
| `python -m unittest tests.product_agent_os.test_product_agent_os_docs -v` | PASS, 100 tests |
| `python -m unittest tests.product_agent_os.test_task_plan_lifecycle -v` | PASS, 4 tests |
| Focused Batch 45/renderer/Windows/comment checks | PASS: 38 + 27 + 5 + 12 tests; one non-Windows guard skip in Windows module |
| Fixture eval / transcript eval / Codex compatibility | PASS: fixture exit 0; transcript 26/26; compatibility `compatible` |
| `python -m unittest discover -s tests -p "test_*.py" -v` | PASS: 1191 tests, `OK (skipped=1)` |
| `python tools\check_docs.py` | PASS, `OK: documentation structure checks passed` |
| `git diff --check` | PASS, exit 0; only non-blocking CRLF-to-LF normalization warnings |
| Scope/diff self-review | PASS for the requested local-only scope; `reviewer_gap`: no reviewer/subagent was launched because delegation was not authorized for this request |
| Fresh-session `SessionStart` proof | NOT RUN; explicit residual gap |
| GPT-5.6 same/lower-effort behavioral quality/cost/latency eval | NOT RUN; provider/model execution was outside approved local-only scope |

## Supported facts, assumptions и unsupported claims

### Supported

- Current files содержат 15 GPT-5.6 pins и strict config загружается.
- Все 31 назначенных unique skill path существуют на текущем host.
- Hook unit/contract tests и template tests проходят.
- В текущей сессии наблюдались PostToolUse context и PreToolUse deny после изменения hook contract; это observation-only, а не fresh-session activation или product acceptance proof.

### Project decisions, а не требования OpenAI

- Какие именно роли идут на Sol, а какие на Terra.
- 48-часовой freshness window lifecycle marker.
- Шесть concurrent subagent threads.
- Пять skills на agent как текущая конфигурация; exact count не считается quality gate.

### Unsupported до отдельного evidence run

- GPT-5.6 лучше GPT-5.5 на задачах этого репозитория.
- Более низкий effort не ухудшает качество.
- Новая конфигурация снижает стоимость/latency.
- SessionStart/PermissionRequest/Stop уже перезагружены в fresh Codex session.
- User-level skills переносимы на другой host.

## Residual risks и следующий gate

1. Запустить новую Codex session и проверить `SessionStart`, один safe allow, один synthetic deny, `PermissionRequest`, `PostToolUse` и `Stop`; не использовать destructive real command.
2. Выполнить representative role matrix: Sol/Terra при сохранённом effort и тот же model на один effort ниже; зафиксировать quality, tool completion, unsupported claims, latency, tokens и cost.
3. При packaging/переносе решить, какие user skills vendorить, какие объявить optional dependencies, а какие удалить из project agent profiles.
4. По желанию очистить три `.pyc`; это hygiene-only и не меняет runtime contract.

## Полный файловый ledger `.codex`

Каждый фактически присутствующий файл перечислен ниже. `changed` означает изменение в этом slice; `inspected_no_change` — построчная проверка без необходимости правки; `historical_evidence_immutable` — проверенная, но намеренно не переписанная история; `derived_cache_not_source` — производный бинарный cache.
| Path | Lines/bytes | Disposition |
| --- | ---: | --- |
| `.codex/agents/architect.toml` | 98 | `changed` |
| `.codex/agents/builder.toml` | 93 | `changed` |
| `.codex/agents/completion-skeptic.toml` | 68 | `changed` |
| `.codex/agents/docs-maintainer.toml` | 95 | `changed` |
| `.codex/agents/explorer.toml` | 89 | `changed` |
| `.codex/agents/graph-cockpit-engineer.toml` | 68 | `changed` |
| `.codex/agents/learning-loop-engineer.toml` | 68 | `changed` |
| `.codex/agents/lifecycle-orchestrator.toml` | 77 | `changed` |
| `.codex/agents/plugin-runtime-builder.toml` | 72 | `changed` |
| `.codex/agents/product-manager.toml` | 88 | `changed` |
| `.codex/agents/release-operator.toml` | 88 | `changed` |
| `.codex/agents/research-source-analyst.toml` | 70 | `changed` |
| `.codex/agents/reviewer.toml` | 92 | `changed` |
| `.codex/agents/security-privacy-supply-chain-reviewer.toml` | 71 | `changed` |
| `.codex/agents/tester.toml` | 91 | `changed` |
| `.codex/artifact-templates/adr.md` | 63 | `inspected_no_change` |
| `.codex/artifact-templates/agent-task-packet.md` | 103 | `inspected_no_change` |
| `.codex/artifact-templates/approval-record.md` | 35 | `inspected_no_change` |
| `.codex/artifact-templates/architecture-overview.md` | 100 | `inspected_no_change` |
| `.codex/artifact-templates/coding-standard-checklist.md` | 101 | `inspected_no_change` |
| `.codex/artifact-templates/doubt-verification-packet.md` | 78 | `inspected_no_change` |
| `.codex/artifact-templates/model-reasoning-policy.md` | 55 | `changed` |
| `.codex/artifact-templates/quality-strategy.md` | 46 | `inspected_no_change` |
| `.codex/artifact-templates/requirement-registry.md` | 39 | `inspected_no_change` |
| `.codex/artifact-templates/requirements-traceability-matrix.md` | 45 | `inspected_no_change` |
| `.codex/artifact-templates/subagent-context-packet.md` | 41 | `changed` |
| `.codex/artifact-templates/subagent-result-packet.md` | 39 | `changed` |
| `.codex/artifact-templates/system-file-hygiene-report.md` | 53 | `inspected_no_change` |
| `.codex/artifact-templates/task-matrix-plan.md` | 92 | `changed` |
| `.codex/artifact-templates/test-eval-matrix.md` | 55 | `changed` |
| `.codex/automation-candidates/self-learning-automation-candidate.md` | 35 | `inspected_no_change` |
| `.codex/config.toml` | 184 | `changed` |
| `.codex/evals/agent-context-contract.json` | 270 | `changed` |
| `.codex/hooks.json` | 85 | `changed` |
| `.codex/hooks/__pycache__/post_tool_use_evidence.cpython-313.pyc` | 1256 bytes | `derived_cache_not_source` |
| `.codex/hooks/__pycache__/stop_runlog_reminder.cpython-313.pyc` | 3966 bytes | `derived_cache_not_source` |
| `.codex/hooks/comment_sufficiency_advisory.py` | 172 | `changed` |
| `.codex/hooks/hooks.json` | 85 | `changed` |
| `.codex/hooks/permission_request_summary.py` | 15 | `changed` |
| `.codex/hooks/post_tool_use_evidence.py` | 24 | `changed` |
| `.codex/hooks/pre_tool_use_policy.py` | 228 | `changed` |
| `.codex/hooks/session_start_context.py` | 90 | `changed` |
| `.codex/hooks/stop_runlog_reminder.py` | 15 | `changed` |
| `.codex/product-agent-os/b45-manual-pilot/__pycache__/v3_reference_runner.cpython-313.pyc` | 27980 bytes | `derived_cache_not_source` |
| `.codex/product-agent-os/b45-manual-pilot/coding-standard-checklists.md` | 493 | `inspected_no_change` |
| `.codex/product-agent-os/b45-manual-pilot/multilang-test-tasks.md` | 505 | `inspected_no_change` |
| `.codex/product-agent-os/b45-manual-pilot/v3_js_runner.mjs` | 177 | `inspected_no_change` |
| `.codex/product-agent-os/b45-manual-pilot/v3_reference_runner.py` | 387 | `inspected_no_change` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/architect.md` | 6 | `historical_evidence_immutable` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/completion-skeptic.md` | 5 | `historical_evidence_immutable` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/docs-maintainer.md` | 5 | `historical_evidence_immutable` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/plugin-runtime-builder.md` | 5 | `historical_evidence_immutable` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/security-privacy.md` | 5 | `historical_evidence_immutable` |
| `.codex/product-agent-os/batch45/t13-agent-reviews/tester.md` | 5 | `historical_evidence_immutable` |
| `.codex/product-agent-os/lifecycle-state.json` | 34 | `changed` |
| `.codex/product-agent-os/reviews/batch45/agent-01-architecture-lifecycle.md` | 261 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/agent-02-runtime-code.md` | 139 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/agent-03-verification-evals.md` | 165 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/agent-04-docs-source-sync.md` | 134 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/agent-05-security-privacy-approvals.md` | 150 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/agent-06-product-scenarios-scorecard.md` | 86 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-01-architecture.md` | 246 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-02-runtime-validator.md` | 138 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-03-test-eval-plan.md` | 238 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-04-security-privacy-approval.md` | 172 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-05-product-lifecycle.md` | 144 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/quality-retest-agent-06-completion-skeptic.md` | 164 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/remediation-agent-02-docs-control-plane.md` | 63 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/remediation-agent-03-final-review.md` | 178 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/remediation-agent-04-code-repair.md` | 25 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t06-agent-01-source-evidence.md` | 69 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t06-agent-02-test-eval-contract.md` | 192 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t06-agent-03-release-promotion-risk.md` | 138 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t06-agent-04-docs-control-plane.md` | 108 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t06-agent-05-completion-skeptic.md` | 219 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t10-agent-01-eval-architecture.md` | 306 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t10-agent-02-timeout-pairing.md` | 337 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t10-agent-03-approval-privacy.md` | 123 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t10-agent-04-docs-control-plane.md` | 207 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t10-agent-05-completion-skeptic.md` | 158 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t11-agent-01-architecture.md` | 154 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t11-agent-02-eval-design.md` | 155 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t11-agent-03-product-requirements.md` | 113 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t11-agent-04-docs-control-plane.md` | 148 | `historical_evidence_immutable` |
| `.codex/product-agent-os/reviews/batch45/t11-agent-05-completion-skeptic.md` | 262 | `historical_evidence_immutable` |
| `.codex/workflows/build-slice.md` | 39 | `inspected_no_change` |
| `.codex/workflows/coding-standards.md` | 47 | `inspected_no_change` |
| `.codex/workflows/control-plane-sync.md` | 45 | `changed` |
| `.codex/workflows/review-slice.md` | 34 | `changed` |
| `.codex/workflows/source-context-pack.md` | 35 | `inspected_no_change` |
| `.codex/workflows/task-plan-lifecycle.md` | 84 | `inspected_no_change` |
| `.codex/workflows/worktree-ownership.md` | 48 | `changed` |
