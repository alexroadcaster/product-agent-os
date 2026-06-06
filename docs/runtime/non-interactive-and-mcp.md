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
Out из scope: ...
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
