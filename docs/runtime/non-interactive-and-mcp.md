# Non-interactive Codex and MCP

Source status: `official + experiment`  
Источники: [Codex CLI features](https://developers.openai.com/codex/cli/features), [Codex with Agents SDK](https://developers.openai.com/codex/guides/agents-sdk), [OpenAI Agents SDK Python](https://github.com/openai/openai-agents-python).

## `codex exec`

`codex exec` запускает Codex задачу non-interactively и подходит для scripts, CI helpers и повторяемых локальных checks.

Хороший prompt для `codex exec` должен быть самодостаточным:

```text
Read AGENTS.md.
Task: ...
Allowed changes: ...
Out of scope: ...
Verification: ...
Output: changed files, commands run, result, risks.
```

Используйте для:

- fixing known CI failures;
- generating release notes;
- running docs audits;
- checking dependency update impact;
- applying a prepared plan.

Не используйте для:

- vague product design;
- work requiring frequent user judgment;
- first run of an untested workflow;
- tasks with broad filesystem or network permissions.

## Codex MCP

Codex MCP делает Codex execution backend для Agents SDK. Полезный pattern:

- Project Manager agent owns goal and source of truth docs.
- Specialist agents read control-plane files.
- Codex MCP performs workspace work with explicit sandbox/approval policy.
- Tester/Reviewer returns results to Manager.

## App server and remote TUI

Remote app-server mode полезен, когда код и credentials живут на удаленной машине, а оператор хочет локальный terminal UI. Если listener выходит за localhost, нужны authentication and TLS controls.

