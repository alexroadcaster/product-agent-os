# Product-Agent OS Codex compatibility

Source status: `official + experiment`

Источники: [Codex plugins](https://developers.openai.com/codex/plugins), [Build plugins](https://developers.openai.com/codex/plugins/build), [Agent Skills](https://learn.chatgpt.com/docs/build-skills), [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Agent approvals and security](https://learn.chatgpt.com/docs/permissions), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [Product-Agent OS architecture](architecture.md).

Compatibility report описывает проверенную локальную структуру package. Он не доказывает поддержку каждого компонента конкретным host и не разрешает live execution, provider calls, external writes или git actions.

## Component inventory — GAP-02, 05.11.2026

Вход: путь локального package. Общий resolver `plugin_components.py` используется compatibility, package inventory, discovery, methodology audit и system-file hygiene. Он возвращает format/version, выбранные component paths, имена skills/MCP servers, transports, issues и `host_status: not_verified`; команды, URL, env values и secrets в результат не копируются и не исполняются.

| Вход | Правило | Результат |
| --- | --- | --- |
| Recognized root `plugin.json` | Agent Plugins 1.0.0 identity; portable `skills/` и `mcp.json` имеют приоритет | `present_unverified` при поддерживаемой структуре |
| `extensions.com.openai` | Целиком заменяет compatibility settings; поля не смешиваются | Явный `settings_source` |
| `.codex-plugin/plugin.json` | Compatibility format при отсутствии root manifest | Component paths проверяются внутри package |
| MCP `mcpServers` wrapper | Portable schema либо Codex compatibility wrapper | Transport проверяется отдельно от host |
| Flat `.mcp.json`, неизвестная schema, неверный тип, escape path | Наблюдение сохраняется без молчаливого fallback | `needs_review` |

Текущий package остаётся `needs_review`: `context7` обнаружен в legacy flat `.mcp.json`. Формат не мигрирован автоматически. Validator выполняет ограниченную структурную проверку, а не полную JSON Schema validation. Auth extensions и неподдерживаемые конструкции требуют отдельного review.

| Component / surface | Codex App | CLI | IDE extension |
| --- | --- | --- | --- |
| Standalone skills | Документированный механизм; selected path и invocation проверяются отдельно | То же | То же |
| Local executors/scripts | Требуются проверки проекта | Требуются проверки проекта | Требуются проверки проекта |
| Native package, MCP, hooks | Нужен receipt client/version/auth/component | Нужен отдельный receipt | Нужен отдельный receipt |

Выход: reviewable inventory и конкретный следующий шаг — решить миграцию MCP declaration, затем проверить выбранный host. Ни `supported_surfaces`, ни manifest presence не являются runtime acceptance. Источники проверены 05.11.2026: [Build plugins](https://developers.openai.com/plugins/build/plugins), [manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json), [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json).

## Входы

- текущий `.codex-plugin/plugin.json` и packaged plugin metadata;
- local skills, scripts, templates, MCP declarations и staged hooks;
- Codex App, CLI и IDE extension workflow expectations;
- текущий `AGENTS.md`, sandbox, approvals и политика источников;
- compatibility validator output и any accepted gaps.

## Выходы

- package compatibility status;
- supported Codex surfaces и non-goals;
- approval boundary для live systems, provider calls, external writes, hosted docs, database access, active automation и git actions;
- verification commands для package и docs closure;
- residual risks когда compatibility claim depends на текущий official Codex behavior.

## Canonical Safety Boundary

Product-Agent OS keeps conservative Codex boundary:

- нет live model call из compatibility checks;
- нет separate OpenAI API key requirement для Codex runtime runner;
- нет standalone Agents SDK activation hidden behind plugin;
- нет global config mutation;
- нет silent MCP/server/hook/automation activation;
- нет unapproved external writes;
- нет hosted docs или DB introspection bypass;
- нет readiness claims из detection.

Codex App, CLI и IDE extension перечислены как intended workflow surfaces. Поддержка native package, skills, MCP и hooks проверяется раздельно по матрице выше. Перечень не разрешает target, GitHub, CI, registry, database или schedule mutations.

## Compatible Surfaces

| Surface | Supported использовать | Boundary |
| --- | --- | --- |
| `.codex-plugin/plugin.json` | Plugin manifest и packaged capability declaration. | Manifest presence является compatibility evidence, не publication approval. |
| Codex App | Interactive steering, ambiguity resolution, review и local workspace work. | User approvals и sandbox still govern actions. |
| CLI | Local deterministic checks, renderers, validators и staged artifact generation. | Commands должен respect project policy и approval scope. |
| IDE extension | Code navigation, review и implementation support. | IDE context является не является каноническим источником через itself. |
| skills | Repeatable methods с inputs, outputs, verification и failure modes. | A skill может recommend actions но не может grant external permission. |
| subagents | Parallel или specialized work когда ownership является clear. | Handoff должен включают files, context, ожидаемые доказательства и stop conditions. |
| `AGENTS.md` | Durable project rules и operating constraints. | Local project rules не может override stronger system/developer instructions. |
| staged hooks | Hook templates и staged proposals. | Hooks являются не silently activated. |
| MCP | Declared tool context и integration boundaries. | MCP access является не automatically safe или approval-free. |
| Agents SDK | Product/runtime app architecture когда explicitly chosen. | Это является не hidden runtime layer для эта plugin. |

## Non-Goals

Product-Agent OS compatibility checks не выполняют:

- publish plugins или docs;
- create schedules, recurring automations или GitHub Actions;
- старт local servers для verification;
- запуск browser automation;
- call external providers или live model/API endpoints;
- mutate canonical graph facts;
- stage, commit, push или open PRs;
- certify legal, security или compliance readiness.

Those actions требуют explicit owner approval, текущий evidence и rollback или stop condition.

## Проверка

Используйте these checks когда package boundaries или docs change:

```powershell
python plugins\product-agent-os\scripts\validate_codex_compatibility.py
python tools\check_docs.py
```

Используйте strict MkDocs когда navigation, Mermaid, Markdown extensions или generated site output changes:

```powershell
python -m mkdocs build --strict
```

Этот compatibility validator следует stay deterministic. Если это требует live provider, browser, hosted docs или database evidence, который evidence belongs в separate approval-bound route, не в baseline compatibility.

## Live Execution Boundaries

Этот live layer stays disabled пока каждый action имеет его own owner-approved packet:

- local runtime launch;
- browser automation smoke;
- external embedding/reranker/LLM provider pilot;
- canonical graph mutation pilot;
- git release, push, PR или publication action.

Approvals являются не bundled. Approval для один surface не grant another.

## Риски

- A compatible package может still быть operationally unsafe если пользователь activates hooks, MCP servers, automations или external systems без evidence.
- Generated cockpit/dashboard/report outputs может look authoritative; docs должен keep source-boundary labels visible.
- Agent handoff quality matters more than number из subagents. Parallel work без ownership может increase risk.
- Official Codex behavior может evolve; source-backed claims следует быть reviewed against текущий official docs когда product surfaces change.

Следующий artifact: используйте [Packaging And Closure](packaging-and-closure.md) для release evidence и [Approval-Bound Real Testing](approval-bound-real-testing.md) до any live execution.

## Актуальность контракта: 2026-11-03

Документационный аудит не повышает package compatibility до доказанной работоспособности всех текущих Codex surfaces. Для acceptance фиксируйте client/version/auth, выбранную модель, effective permissions, parent MCP и evidence конкретного сценария. Официальные источники: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Permissions](https://learn.chatgpt.com/docs/permissions), [Hooks](https://learn.chatgpt.com/docs/hooks).

| ID аудита | Текущее состояние | Что требуется отдельно |
| --- | --- | --- |
| OPEN-PERM | Parent `:workspace`; неподдерживаемые overrides удалены; ограничения ролей поведенческие | Доказательство эффективных permissions в свежей сессии |
| OPEN-MCP | MCP настроен у родителя; агенты наследуют его; требование agent-local MCP удалено | Проверка эффективной доступности инструментов в свежей сессии |
| OPEN-MODEL | Выбраны GPT-6.1 Sol/Terra; effort сохранён во всех 23 профилях | Разрешённое сравнение качества, стоимости и задержки при прежнем effort |
| OPEN-BASELINE | Устаревшее требование исправлено; проверяется семантика parent и rendered config | Локальные регрессионные проверки без заявления о runtime |
| OPEN-RUNTIME | Новые Agents API/Responses возможности описаны | Отдельная реализация и runtime evidence, если маршрут выбран |

Техническое продолжение разрешено владельцем 2026-11-03. Конфигурация, профили, шаблоны и валидаторы обновлены; активация и behavioral promotion остаются открыты. Результаты и точные команды принадлежат [плану](../superpowers/plans/2026-11-03-gpt6-documentation-refresh.md).

## Компоненты и runtime evidence

Совместимость фиксируйте по client/version/auth/component. Local fixture или наличие manifest не доказывают native install, trust или успешный runtime. Для текущего package действует `needs_review` выше; native host support нельзя выводить из standalone skills. [Surface matrix](../codex/surfaces.md), [package contract](technical.md).
