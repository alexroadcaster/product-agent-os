# Non-interactive Codex и MCP

Source status: `official + experiment`  
Источники: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python).

## `codex exec`

`codex exec` запускает Codex задачу non-interactively и подходит для scripts, CI helpers и повторяемых локальных checks.

Хороший prompt для `codex exec` должен быть самодостаточным:

```text
Read AGENTS.md.
Goal: ...
Allowed changes: ...
Вне scope: ...
Verification: ...
Output: changed files, commands run, result, risks.
```

Используйте для:

- fixing known CI failures;
- generating заметки к release;
- running docs audits;
- checking dependency update impact;
- applying prepared plan.

Не используйте для:

- vague product design;
- work requiring frequent пользователь judgment;
- первый запуск untested workflow;
- задачи с broad filesystem или network permissions.

## Codex MCP

Codex MCP делает Codex execution backend для Agents SDK. Полезный pattern:

- Project Manager agent владеет goal и source-of-truth docs.
- Specialist agents read control-plane files.
- Codex MCP выполняет workspace work с явной sandbox/approval policy.
- Tester/Reviewer returns results к Manager.

## App server и remote TUI

Remote app-server mode полезен, когда код и credentials живут на удаленной машине, а оператор хочет локальный terminal UI. Если listener выходит за localhost, нужны authentication и TLS controls.

## MCP и API: разные границы

В [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents) MCP наследуется от родителя. Agent-local declaration не переопределяет parent MCP и не доказывает доступность tool. Проверяйте загруженную конфигурацию и результат обращения в разрешенном runtime; документационное изменение не активирует сервер.

Command network policy не является политикой web search, connectors, MCP и browser. Для каждого инструмента нужны собственные controls и допустимый scope; см. [security](../codex/security.md). Не переносите API-параметры в CLI runner: [API compatibility](../agent-systems/sdk-patterns.md) относится к соответствующему endpoint. Текущий проектный runner не заменяется Responses или Agents API.
