# Playbook: проектирование AI-native команды

Source status: `official + experiment`  
Источники: [Building an AI-Native Engineering Team](https://developers.openai.com/codex/guides/build-ai-native-engineering-team), [Codex use cases](https://developers.openai.com/codex/use-cases), [Agent Skills](https://developers.openai.com/codex/skills).

## Цель

Спроектировать набор агентных ролей и повторяемых workflows для команды или проекта.

## Карта ролей

| Роль | Workflow | Артефакт |
| --- | --- | --- |
| Researcher | Сбор источников и требований | source cards, brief |
| Planner | План реализации | implementation plan |
| Builder | Scoped implementation | diff, tests |
| Reviewer | Review по рискам | findings |
| Maintainer | Обновление docs и changelog | docs update |

## Вопросы дизайна

- Какие задачи повторяются чаще трех раз?
- Какие правила должны жить в `AGENTS.md`?
- Какие workflows стоит вынести в skills?
- Какие задачи read-heavy и подходят для subagents?
- Где нужна память, а где достаточно checked-in docs?
- Какие verification commands считаются обязательными?

## Prompt

```text
Спроектируй AI-native operating model для проекта "{project}".

Верни:
- повторяемые workflows;
- какие из них оформить как skills;
- какие роли агентов нужны;
- какие правила положить в AGENTS.md;
- какие memory boundaries нужны;
- какие проверки доказывают качество.
```

