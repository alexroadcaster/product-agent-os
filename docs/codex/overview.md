# Обзор Codex

Codex - это coding agent OpenAI, который может читать, изменять и запускать код. В официальных материалах Codex описывается как агент для ускорения разработки, исправления ошибок, понимания незнакомого кода и делегирования задач в локальных или облачных средах.

Source status: `official`  
Основные источники: [Codex cloud](https://developers.openai.com/codex/cloud), [Codex app](https://developers.openai.com/codex/app), [Codex CLI](https://developers.openai.com/codex/cli), [Codex IDE extension](https://developers.openai.com/codex/ide).

## Ментальная модель

Codex лучше рассматривать не как автодополнение, а как оператора workflow:

- получает задачу, контекст и критерий готовности;
- исследует код, документы или данные;
- вносит изменения или готовит артефакт;
- запускает проверки;
- возвращает краткий результат с evidence.

Для продвинутого использования ключевой навык - не "написать промпт", а построить управляемую систему: инструкции, источники, skills, subagents, sandbox, approvals, memory и eval loops.

## Что входит в v1 этой базы

| Область | Что изучаем | Где читать |
| --- | --- | --- |
| Surfaces | App, CLI, IDE extension, cloud | [Поверхности работы](surfaces.md) |
| Configuration | Approval policies, skill metadata, Codex MCP | [Конфигурация](configuration.md) |
| Security | Sandbox, approvals, network boundaries | [Безопасность](security.md) |
| Workflows | Prompting, verification, handoff | [Рабочие процессы](workflows.md) |
| Agent systems | Subagents, skills, AGENTS.md, memory | [Архитектура](../agent-systems/overview.md) |
| SDK layer | Agents SDK, Responses API, guardrails, tracing | [Agents SDK patterns](../agent-systems/sdk-patterns.md) |
| Insights | User tricks, hypotheses, experiments | [Insights](../insights/index.md) |

## Нормы качества

Каждая инструкция в основной базе должна иметь один из трех статусов:

- ссылка на официальный источник;
- ссылка на community-источник и явный `trust_level`;
- локальная гипотеза со сценарием проверки.

Без этого утверждение остается заметкой, а не инструкцией.
