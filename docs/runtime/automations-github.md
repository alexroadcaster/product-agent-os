# Automations и GitHub

Source status: `official + experiment`  
Источники: [Codex automations](https://developers.openai.com/codex/app/automations), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Codex GitHub integration](https://developers.openai.com/codex/integrations/github), [Codex GitHub Action](https://developers.openai.com/codex/automation/github-action).

## Skills define method, automations define schedule

Codex best practices формулируют практическое правило: skill описывает метод, automation задает cadence. Если workflow еще требует ручного steering, сначала превратите его в skill и прогоните вручную.

## Хорошие automation candidates

- summarize recent commits;
- scan likely bugs;
- draft заметки к release;
- check CI failures;
- produce standup summaries;
- запуск scheduled documentation freshness audit;
- запуск recurring security/threat-model review.

## GitHub delivery loop

```mermaid
flowchart LR
    Issue["Issue / spec"] --> Plan["PLAN.md"]
    Plan --> Branch["Worktree / branch"]
    Branch --> Diff["Codex changes"]
    Diff --> Checks["Tests / evals"]
    Checks --> Review["Review"]
    Review --> PR["PR"]
    PR --> Notes["Release notes"]
```

## Permission baseline

Для CI/PR automation:

- prefer read-only analysis для review jobs;
- использовать least-privilege repository tokens;
- separate comment/review jobs из писать jobs;
- требуют explicit branch или PR scope;
- сохраняйте final evidence в PR body или check summary.

