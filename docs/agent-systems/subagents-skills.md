# Subagents, Skills и AGENTS.md

Source status: `official`  
Источники: [Subagent concepts](https://developers.openai.com/codex/concepts/subagents), [Subagents configuration](https://developers.openai.com/codex/subagents), [Agent Skills](https://developers.openai.com/codex/skills), [AGENTS.md](https://developers.openai.com/codex/guides/agents-md).

## Когда что использовать

| Механизм | Использовать когда | Пример |
| --- | --- | --- |
| `AGENTS.md` | Нужно постоянное правило для проекта | Как запускать тесты, стиль документации, source policy |
| Skill | Повторяется workflow с явными шагами | "Собери источник, сделай карточку, проверь claims" |
| Subagent | Работа независима и параллелится | Один агент ищет docs, второй проверяет links, третий анализирует insights |
| Plugin | Нужно упаковать skills, MCP и agents для команды | Внутренний пакет документационных workflows |

## Subagents

Официальная модель: Codex не должен запускать subagents автоматически. Нужно явно просить "spawn agents", "delegate in parallel" или "use one agent per point".

Хороший subagent prompt:

```text
Spawn one agent for each source family:
1. Codex official docs
2. Agents SDK memory docs
3. Community insight backlog

Each agent must return:
- sources used;
- verified claims;
- uncertain claims;
- suggested doc updates.
Wait for all agents, then synthesize without copying raw logs.
```

Официальный review pattern масштабируется так же: один agent на security, один на code quality, один на bugs, один на race conditions, один на test flakiness, один на maintainability. Main thread должен дождаться всех результатов и сделать consolidated summary без дублирующих findings.

## Skills

Skill должен быть узким и проверяемым. Официальная рекомендация для skills: фокус на одной задаче, явные inputs/outputs, инструкции важнее scripts, scripts нужны только для deterministic behavior или external tooling.

## Skill design rubric

| Критерий | Проверка |
| --- | --- |
| One job | Skill решает один повторяемый workflow |
| Trigger words | `description` явно говорит, когда использовать и когда не использовать |
| Inputs | Required inputs перечислены |
| Outputs | Формат результата фиксирован |
| Progressive disclosure | `SKILL.md` краткий, references/scripts/assets подгружаются по необходимости |
| Determinism | Scripts используются только для воспроизводимого поведения или external tooling |
| Eval cases | Есть примеры should trigger и should not trigger |

Кандидаты skills для этого проекта:

- `source-card-writer` - превращает ссылку в карточку источника.
- `claim-verifier` - проверяет утверждения против source registry.
- `insight-intake` - принимает community trick и оформляет insight card.
- `docs-refresh` - сравнивает changelog с текущими разделами.
- `product-spec-writer` - превращает идею в requirements packet.
- `implementation-planner` - строит PLAN.md из REQUIREMENTS.md.
- `test-gap-finder` - ищет gaps между diff и TEST.md.
- `release-note-writer` - готовит release notes из PR diff and RUNLOG.
- `eval-loop-runner` - ведет scored improvement loop.
- `ui-visual-reviewer` - проверяет визуальные artifacts against rubric.

Дополнительная metadata может жить в `agents/openai.yaml`: display name, short description, icons, default prompt, invocation policy и tool dependencies. Для source-sensitive skills в этом проекте implicit invocation лучше отключать, чтобы сбор источников и перенос claims происходили явно.

## AGENTS.md

`AGENTS.md` должен содержать только правила, которые агент обязан соблюдать при каждом запуске проекта:

```markdown
# AGENTS.md

## Documentation rules

- Write Russian documentation, but keep official OpenAI terms in English on first mention.
- Treat official OpenAI docs as source of truth.
- Put community tricks under docs/insights/ with trust and verification status.
- Run python tools/check_docs.py after editing docs.
- Run python -m mkdocs build --strict before claiming the site builds.
```
