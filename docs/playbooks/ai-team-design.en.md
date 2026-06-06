# Playbook: designing an AI-native team

Source status: `official + experiment`  
Sources: [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent Skills](https://developers.openai.com/codex/skills).

## Goal

Design a set of agent roles and repeatable workflows for a team or project.

## Role Map

| Role | Workflow | Artifact |
| --- | --- | --- |
| Researcher | Source and requirements collection | source cards, brief |
| Planner | Implementation plan | implementation plan |
| Builder | Scoped implementation | diff, tests |
| Reviewer | Risk-based review | findings |
| Maintainer | Docs and changelog update | docs update |

## Design Questions

- Which tasks repeat more than three times?
- Which rules must live in `AGENTS.md`?
- Which workflows should be extracted into skills?
- Which tasks are read-heavy and fit subagents?
- Where is memory needed, and where are checked-in docs enough?
- Which verification commands are mandatory?

## Prompt

```text
Design an AI-native operating model for the project "{project}".

Return:
- repeatable workflows;
- which of them should become skills;
- which agent roles are needed;
- which rules should go into AGENTS.md;
- which memory boundaries are needed;
- which checks prove quality.
```

