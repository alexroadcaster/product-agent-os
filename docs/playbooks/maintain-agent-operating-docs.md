# Playbook: maintain agent operating docs

Source status: `official + experiment`  
Источники: [AGENTS.md docs](https://developers.openai.com/codex/guides/agents-md), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [AGENTS.md open format](https://agents.md/).

## Цель

Поддерживать `AGENTS.md`, skills, playbooks и templates как живую операционную систему проекта.

## Update triggers

- Agent repeatedly asks the same clarification.
- Test command changed.
- Workflow repeated three or more times.
- New failure mode appears in review.
- Automation failed due to missing setup.
- Team adds new package, service, or deployment path.

## Maintenance loop

1. Collect recurring friction from RUNLOG and review notes.
2. Decide destination:
   - always-on rule -> `AGENTS.md`;
   - task method -> skill;
   - one-off lesson -> insight;
   - source-backed fact -> source registry and docs.
3. Keep instructions short and scoped.
4. Run docs checks.
5. Verify a sample Codex prompt can follow the updated instructions.

## Anti-patterns

- Put every possible rule into root `AGENTS.md`.
- Hide task-specific workflows in persistent instructions.
- Create broad skills that overlap.
- Automate before manual workflow is stable.
- Keep run logs only in chat history.

