# Skill Lifecycle

Source status: `official + experiment`

Эта диаграмма показывает, как повторяемый workflow становится reusable skill, а затем может стать automation candidate.

## Диаграмма

```mermaid
stateDiagram-v2
    [*] --> PlaybookStep
    PlaybookStep --> ManualRuns: repeated need
    ManualRuns --> FailureLog: failures observed
    FailureLog --> SkillDraft: method stabilizes
    SkillDraft --> EvalCases: define examples and rubric
    EvalCases --> ManualRuns: eval fails
    EvalCases --> PackagedSkill: eval passes
    PackagedSkill --> ProjectUse: used by agents
    ProjectUse --> Maintenance: failures or docs change
    Maintenance --> SkillDraft: update instructions
    ProjectUse --> AutomationCandidate: stable cadence
    AutomationCandidate --> [*]
```

## Когда создавать skill

Создавайте skill, когда workflow:

- повторяется в нескольких проектах или нескольких задачах одного проекта;
- имеет узнаваемые trigger words;
- требует специальных правил, checklist или источников;
- может вернуть понятный результат;
- имеет failure modes, которые можно описать заранее.

Не создавайте skill для одноразовой инструкции, временного решения или workflow без проверки.

## Rubric качества skill

| Критерий | Хороший skill | Слабый skill |
| --- | --- | --- |
| Scope | Одна работа | Несколько несвязанных работ |
| Trigger | Понятные слова запуска | “Используй когда полезно” |
| Inputs | Явно перечислены | Модель угадывает |
| Outputs | Формат результата задан | Ответ произвольный |
| Verification | Есть eval cases | Проверка отсутствует |
| Scripts | Только deterministic behavior | Скрипты скрывают reasoning |

## Примеры product skills

- `product-spec-writer` — превращает идею в `REQUIREMENTS.md`.
- `implementation-planner` — делает `PLAN.md` из требований и repo context.
- `test-gap-finder` — ищет несоответствие между изменениями и тестами.
- `eval-loop-runner` — запускает focused improvement loop и обновляет score history.
- `ui-visual-reviewer` — проверяет layout, screenshots, overlap, responsive states.
- `release-note-writer` — пишет release notes на основе diff, PR и user-facing changes.

## Stop conditions

Остановите упаковку skill, если:

- workflow не воспроизводится вручную;
- нет eval examples;
- source policy неясна;
- skill требует secrets;
- результат нельзя проверить человеком или deterministic checks.
