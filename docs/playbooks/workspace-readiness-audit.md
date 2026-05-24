# Playbook: workspace readiness audit

Source status: `official + experiment`  
Источники: [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [Agent approvals and security](https://developers.openai.com/codex/agent-approvals-security), [Codex automations](https://developers.openai.com/codex/app/automations).

## Цель

Проверить, готов ли workspace к product-agent workflows.

## Audit checklist

| Area | Pass condition |
| --- | --- |
| Instructions | `AGENTS.md` exists and names setup/test commands |
| Source policy | Official/community/experiment rules are explicit |
| Build | Build command documented |
| Tests | Test command documented |
| Evals | Subjective outputs have eval or review rubric |
| Sandbox | Approval and network rules are known |
| Worktrees | Parallel work strategy exists |
| Skills | Repeated workflows have skill candidates |
| Automation | Only stable workflows are scheduled |
| Runtime evidence | `RUNLOG.md` or equivalent exists for long runs |

## Prompt

```text
Audit this workspace for Codex product-agent readiness.

Do not edit files.
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
- recommended docs or skill additions;
- first workflow to automate.
```

