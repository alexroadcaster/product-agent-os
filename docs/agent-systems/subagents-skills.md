# Subagents, Skills и AGENTS.md

Source status: `official + experiment`
Источники: [Subagent concepts](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Subagents configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Agent Skills](https://learn.chatgpt.com/docs/build-skills), [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Product-Agent OS plugin](../product-agent-os/index.md).

## Когда что использовать

| Механизм | Использовать когда | Пример |
| --- | --- | --- |
| `AGENTS.md` | Нужно постоянное правило для проекта | Как запускать тесты, стиль документации, политика источников |
| Skill | Повторяется workflow с явными шагами | "Собери источник, сделай карточку, проверь claims" |
| Subagent | Работа независима и параллелится | Один агент ищет docs, второй проверяет links, третий анализирует insights |
| Plugin | Нужно упаковать skills, MCP и agents для команды | Внутренний пакет документационных workflows |

## Subagents

Local Codex запускает subagents по явному запросу пользователя или применимым инструкциям AGENTS/skill. ChatGPT Work Ultra может делегировать проактивно. Более строгая политика проекта остается отдельной: здесь нужна независимая задача, явный ownership и разрешение применимых инструкций. Наличие инструмента само по себе не является основанием делегации.

Хороший subagent prompt:

```text
Spawn один agent для каждый source family:
1. Codex official docs
2. Agents SDK memory docs
3. Community insight backlog

Каждая agent должен return:
- sources used;
- verified claims;
- uncertain claims;
- suggested doc updates.
Wait для all agents, затем synthesize без copying raw logs.
```

Официальный review pattern масштабируется так же: один agent на security, один на code quality, один на bugs, один на race conditions, один на test flakiness, один на maintainability. Main thread должен дождаться всех результатов и сделать consolidated summary без дублирующих findings.

## Fresh-context handoff contract

Product-Agent OS использует практическое правило для subagents и skills: generated `agent-skill-handoff.json` помогает routing, но не заменяет task packet. Перед параллельной работой main thread должен выдать каждому worker свежий контекст, ownership и stop condition.

| Поле handoff | Что должно быть явно |
| --- | --- |
| Ownership | Owned files/subsystems, forbidden files и expected handoff artifact. |
| Свежий контекст | Текущий запрос пользователя, релевантные правила проекта, использованные source files/docs и допущения. |
| Доказательства проверки | Команды, docs checks, evals, screenshots, logs или accepted gap, ожидаемые от исполнителя. |
| Условия остановки | Граница approval, отсутствующий source, пересечение ownership, падающая проверка или устаревший контекст. |
| Пакет возврата | Использованные sources, затронутые или предложенные файлы, результат проверки, открытые риски и рекомендуемая следующая роль. |

Если ownership пересекается или ожидаемые доказательства невозможно получить, используйте последовательный fallback вместо параллельных subagents. Для source-sensitive docs work community claims остаются intake material, пока trust level и verification status не записаны явно.

## Skills

Skill должен быть узким и проверяемым. Официальная рекомендация для skills: фокус на одной задаче, явные inputs/outputs, инструкции важнее scripts, scripts нужны только для deterministic behavior или external tooling.

### Completion-skeptic promotion path

`completion-skeptic` идет по той же promotion chain, что и другие repeatable methods: manual -> playbook -> skill -> plugin -> automation candidate. До promotion нужны owner review, rollback notes, failure log, eval cases и candidate-only status. Generated handoff или dashboard недостаточны.

Для documentation и scorecards явный approval checkpoint - owner review.

Automation blockers остаются явными: active hook, schedule, MCP server, Agents SDK runner, provider call или external write не создаются, пока нет manual evidence, scorecard review и отдельного approval packet.

## Skill design rubric

| Критерий | Проверка |
| --- | --- |
| One job | Skill решает один повторяемый workflow |
| Trigger words | `description` явно говорит, когда использовать и когда не использовать |
| Входы | Обязательные входы перечислены |
| Выходы | Формат результата фиксирован |
| Progressive disclosure | `SKILL.md` краткий, references/scripts/assets подгружаются по необходимости |
| Determinism | Scripts используются только для воспроизводимого поведения или external tooling |
| Eval cases | Есть примеры следует trigger и следует не trigger |

Кандидаты skills для этого проекта:

- `source-card-writer` - превращает ссылку в карточку источника.
- `claim-verifier` - проверяет утверждения против source registry.
- `insight-intake` - принимает community trick и оформляет insight card.
- `docs-refresh` - сравнивает changelog с текущими разделами.
- `product-spec-writer` - превращает идею в requirements packet.
- `implementation-planner` - строит PLAN.md из REQUIREMENTS.md.
- `test-gap-finder` - ищет gaps между diff и TEST.md.
- `release-note-writer` - готовит заметки к release из PR diff и RUNLOG.
- `eval-loop-runner` - ведет scored improvement loop.
- `ui-visual-reviewer` - проверяет визуальные artifacts against rubric.

Дополнительная metadata может храниться в `agents/openai.yaml`: `display name`, `short description`, `icons`, `default prompt`, `invocation policy` и зависимости tools. Для source-sensitive skills в этом проекте implicit invocation лучше отключать, чтобы сбор источников и перенос claims происходили явно.

## AGENTS.md

`AGENTS.md` должен содержать только правила, которые агент обязан соблюдать при каждом запуске проекта:

```markdown
# AGENTS.md

## Documentation rules

- Создайте Russian documentation, но keep official OpenAI terms в English на first mention.
- Treat official OpenAI docs как source of truth.
- Put community tricks в рамках docs/insights/ с trust и verification status.
- Запустите python tools/check_docs.py после editing docs.
- Запустите python -m mkdocs build --strict до claiming site builds.
```

## Наследование и активация custom agents

Проверено 2026-11-03: [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents). Custom agent file задает `name`, `description`, `developer_instructions`, поддерживаемые model/effort и ограничения capabilities. Permissions, approvals, provider и MCP наследуются от родителя; agent-local `sandbox_mode`, `approval_policy`, `model_provider`, `mcp_servers` не переопределяют их. Read-only роль — поведенческая обязанность, пока техническая изоляция не доказана отдельно.

Явные spawn model/effort имеют приоритет над defaults, затем используются defaults/parent по официальным правилам. Смена model без effort может выбрать default новой модели; custom-file overrides имеют собственный порядок. Проверяйте resolved model/effort, не выводите их из одного имени роли.

Skill `allow_implicit_invocation: false` отключает implicit selection, но не explicit invocation. Metadata dependencies не выдаёт permissions и не доказывает доступность MCP. Нужны эффективная конфигурация родителя и текущая проверка инструмента; в этом обновлении MCP не активируется.

## Входы и выходы

Входы: текущая цель, применимые инструкции, источники, ownership и требуемые доказательства. Выходы: ограниченный пакет работы, обоснованный результат и handoff с открытыми рисками. Проверяйте применимость, полномочия и наблюдаемые evidence. Основные риски: пересечение записей, устаревший контекст и выдача предложения за активированное поведение.
