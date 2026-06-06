# Product lifecycle

Source status: `official + experiment`  
Источники: [How OpenAI uses Codex](https://openai.com/business/guides-and-resources/how-openai-uses-codex/), [Codex best practices](https://developers.openai.com/codex/learn/best-practices), [Iterate на difficult problems](https://developers.openai.com/codex/use-cases/iterate-on-difficult-problems), [Codex workflows](https://developers.openai.com/codex/workflows).

## End-to-end loop

| Stage | Работа агента | Артефакт | Gate |
| --- | --- | --- | --- |
| Idea | Уточнить пользовательскую ценность, гипотезу, метрику и ограничения | `REQUIREMENTS.md` | Scope и success metric явные |
| Spec | Превратить идею в поведение и acceptance criteria | `REQUIREMENTS.md` | Намерение пользователя и source-of-truth docs зафиксированы |
| Plan | Разложить работу, architecture boundary и ownership | `PLAN.md` | Рабочие единицы достаточно независимы |
| Build | Реализовать один focused slice за раз | Diff | Есть test-first или eval-first путь |
| Eval | Оценить deterministic, subjective и AI quality | `TEST.md`, `EVALS.md`, reports | Threshold достигнут или gap принят |
| Review | Найти bugs, security risks и test gaps | Review findings | Нет unresolved blocker |
| PR | Подготовить branch, PR body, влияние на docs и заметки к release | PR / changelog | Доказательства проверки включено |
| Learn | Зафиксировать reusable method | `AGENTS.md`, skill, insight | Следующий запуск становится лучше |

## Ask Mode до Code Mode

Рекомендации OpenAI Codex предлагают начинать крупные изменения с плана до реализации. В этом проекте это означает:

```text
Сначала создай PLAN.md из REQUIREMENTS.md.
Не редактируй product code, пока план не называет:
- файлы или подсистемы;
- acceptance criteria;
- verification commands;
- risks и rollback;
- что вне scope.
```

## Work granularity

Хорошая работа для Codex достаточно ограничена, чтобы человек мог выполнить ее за один сфокусированный блок. Если запрос одновременно затрагивает product, design, backend, frontend, tests, docs и release, разделите его на lifecycle stages и используйте control-plane files как handoff.

## Learning loop

Каждый завершенный product-agent workflow должен ответить:

- Какие инструкции стоит перенести в `AGENTS.md`?
- Какие повторяемые шаги заслуживают skill?
- Какая проверка должна стать automation?
- Какой failure требует eval?
- Какой source или architecture decision нужно задокументировать?
- Какая metric или пользователь feedback должна двигать следующую product iteration?
