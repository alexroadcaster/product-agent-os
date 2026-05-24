# Playbook: code review через Codex

Source status: `official + experiment`  
Источники: [Codex workflows](https://developers.openai.com/codex/workflows), [Codex subagents](https://developers.openai.com/codex/concepts/subagents), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security).

## Цель

Использовать Codex как reviewer, который ищет bugs, regressions, test gaps, security risks и maintainability issues.

## Prompt для одного агента

```text
Review current changes as a code reviewer.

Prioritize:
1. Bugs and behavioral regressions.
2. Security or data-safety risks.
3. Missing tests for changed behavior.
4. Maintainability issues only if they affect correctness.

Output findings first.
Each finding must include file, line, severity, and why it matters.
Do not rewrite code unless asked.
```

## Parallel review

Для больших PR можно явно попросить subagents:

```text
Use one parallel subagent per review track:
- Security risks
- Correctness bugs
- Test gaps
- Maintainability

Wait for all agents and return a consolidated review.
Do not include duplicate findings.
```

## Verification

- Проверить, что findings ссылаются на реальные файлы и строки.
- Запросить reproduction или failing test для каждого high-severity bug.
- Не принимать stylistic comments как blockers без behavioral risk.

