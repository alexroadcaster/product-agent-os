# Playbook: workspace readiness audit

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations).

## Цель

Проверить, готов ли workspace к product-agent workflows.

## Audit checklist

| Area | Pass condition |
| --- | --- |
| Instructions | `AGENTS.md` exists и names setup/test commands |
| Политика источников | Правила official/community/experiment явно записаны |
| Build | Build command documented |
| Tests | Test command documented |
| Evals | Для subjective outputs есть eval или review rubric |
| Sandbox | Правила approval и network известны |
| Worktrees | Parallel work strategy exists |
| Skills | Повторяемые workflows имеют skill candidates |
| Automation | Только stable workflows получают schedule |
| Runtime evidence | `RUNLOG.md` или аналог существует для long запускается |

## Prompt

```text
Audit эта workspace для Codex product-agent readiness.

Не edit files.
Check:
- AGENTS.md;
- setup/build/test commands;
- evals;
- skills candidates;
- automation candidates;
- sandbox/approval risks;
- missing control-plane files.

Return:
- readiness score 0-100;
- blockers;
- recommended docs или skill additions;
- first workflow к automate.
```

## Inventory и readiness

Наличие skills/plugins/config — `present_unverified`. Для runtime claim нужны effective settings, supported client/auth, skill exposure и observed result. Используйте [surface matrix](../codex/surfaces.md) и [skill diagnostics](../agent-systems/subagents-skills.md); audit не активирует найденные assets.
