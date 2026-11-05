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

## Планирование перед реализацией

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

## Guardrail стартового брифа

Для сложной Product-Agent OS работы стартовый бриф теперь поддерживается staged hook-механизмом:

- lifecycle contract живёт в `.codex/config.toml` и `.codex/workflows/task-plan-lifecycle.md`;
- packaged hook templates живут в `plugins/product-agent-os/assets/templates/hooks/`;
- `PreToolUse` hook блокирует команды с изменениями, если после видимого пользователю стартового брифа не создан `.codex/product-agent-os/lifecycle-state.json`;
- `Stop` hook напоминает показать завершающий бриф и выполнить control-plane sync, если менялись scope, plan, tests, evals, runlog или evidence state.

Это guardrail, а не доказательство само по себе. Completion/readiness claims всё равно требуют current command/runtime/eval evidence или explicit accepted gap.

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

## Размер задачи определяет маршрут

Проверено 05.11.2026: [model guidance](https://developers.openai.com/api/docs/guides/latest-model) и [eval guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices). Для ordinary fix: краткий scope, изменение, affected checks, результат и ограничения. Переиспользуйте существующие requirements/plan/test/runlog; не создавайте новый набор файлов только ради названий этапов. Полный маршрут выше нужен для большой, рискованной или финансово значимой реализации и release/readiness.

В Product-Agent OS full route — `task_start_brief_v2` (9 полей) и Completion Ledger (13 пунктов); ordinary route — `task_scope_note_v1` и краткий итог. Legacy v1 сохраняется только для ранее начатых sessions. `Stop` advisory не валидирует чат. Применимость и marker определяет [lifecycle hooks guide](../runtime/worktrees-hooks-rules.md).

Single-agent — достаточная отправная точка. Делегирование оправдано независимыми задачами, явным ownership, бюджетом и измеримой пользой. PR preparation не даёт полномочий создавать branch, публиковать PR или release. Повторяйте проверки после релевантной правки, failure или неустранённого риска; не запускайте бесконечный общий gate.
